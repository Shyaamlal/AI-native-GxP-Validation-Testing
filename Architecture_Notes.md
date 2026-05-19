# Architecture Notes

Operational architecture of the agentic validation framework. Written to support visual / diagram work and external explanation (reviewers, recruiters, technical leaders).

---

## 1. Orchestration

**Phases execute** via Claude Code skills + the Task tool launching specialist subagents.

- Orchestrator skill: `Skills/validate-feature.md` (natural-language skill, not Python script, not LangGraph, not custom DSL).
- Specialist skills: one per phase under `Skills/validation-<phase>.md` — feature-scoping, risk-assessment, validation-scope, urs-author, frs-author, oq-protocol-author, oq-execution, summary-report, release-summary.
- Each phase is dispatched by the orchestrator as a subagent invocation via the Task tool, with prior-phase artefacts and approval comments passed as context.
- Sequential execution, gated by HITL approval between phases. Not parallel, not event-driven.

**State machine** lives in `<feature_folder>/state.json`:
- `current_phase`, `chain_status` (`in_progress` / `complete`), `validation_status` (`Pass` / `Conditional Pass` / `Fail`)
- `phases[]` array with per-phase: `phase`, `name`, `agent_skill`, `artifact_path`, `schema_result`, `file_list_check`, `approval { approved, reviewer, reviewer_role, timestamp, comment }`
- Persisted on every transition. Doubles as session handoff: a session can be killed mid-chain and resumed by reading state.json (deferred fix: persist Step 0 inputs too).

**Validators** are Python scripts in `validators/`:
- One validator module per phase (`feature_scoping.py`, `risk_assessment.py`, `validation_scope.py`, `urs.py`, `frs.py`, `oq_protocol.py`, `oq_execution.py`, `summary_report.py`, `release_summary.py`).
- Shared helpers in `_common.py` — frontmatter parsing (no YAML dependency, dotted-key flattening), placeholder pattern detection, section-emptiness checks, ID uniqueness.
- Phase-specific modules add the artifact-type-specific schema: required frontmatter fields, required body sections, ID patterns and counts.
- Run by the orchestrator after each specialist produces its artifact. Pass/fail recorded in `state.json.phases[i].schema_result`.
- Smoke harness: `_smoke_test.py` against `_smoke_artifacts/`. 18 cases (one valid + one invalid per phase). Run with `python validators/_smoke_test.py`.

**Approvals** are file-level, not API-level:
- Reviewer edits artefact frontmatter (`approved_by`, `approval_comment`, `approval_timestamp`) OR responds to orchestrator's HITL prompt, which writes the approval block into `state.json.phases[i].approval`.
- Orchestrator polls state until approval recorded, then advances `current_phase`.

**Audit logging** is append-only JSONL:
- `ai_assistance_log.jsonl` at repo root.
- Two lines per phase: one `approval: pending` line when the specialist emits its artifact, one `approval: approved` (or `rejected`) line when the reviewer signs off.
- Fields per line: `timestamp`, `feature`, `phase`, `phase_name`, `agent_skill`, `model`, `prompt_version`, `artifact_path`, `artifact_hash` (sha256 of the artifact content at the time of writing), `schema_result`, `reviewer`, `reviewer_role`, `approval`, `approval_timestamp`, optional `approval_comment`. Re-validation cases also carry `prior_surfaced_hash` referencing the superseded artifact hash (used at Phase 6 TC-017 amendment in the Logout run).
- Tamper-evidence: each artifact's sha256 is logged at the time of writing, so post-hoc modification of an artifact is detectable against the logged hash. The log itself is not entry-to-entry chained.
- Queryable via `tools/audit.py` — filter by feature, phase, phase-name, skill, model, reviewer, status, artifact, time window.

---

## 2. Execution trace — Phase 3 → Phase 4

What actually happens when Phase 3 (Validation Scope) completes and Phase 4 (URS) begins:

```
1. Phase 3 specialist (validation-scope skill) finishes drafting
   → 02_Logout/Validation_Scope_Logout.md written

2. validators/validation_scope.py runs against the artefact
   → state.json.phases[2].schema_result = "pass"
   → ai_assistance_log.jsonl appended: {phase: 3, action: "validator_pass", artefact_sha256: ...}

3. Orchestrator presents artefact summary to reviewer (HITL gate)
   → reviewer responds "approve" (with or without comment)

4. Orchestrator writes approval block into state.json:
     phases[2].approval = {
       approved: true,
       reviewer: "shyaamlal",
       reviewer_role: "Validation lead",
       timestamp: "<ISO-8601 UTC>",
       comment: "<optional reviewer note>"
     }
   → state.json.current_phase = 4

5. ai_assistance_log.jsonl appended:
     {phase: 3, action: "approval_recorded", reviewer, comment_sha256, prior_entry_sha256}

6. Orchestrator launches Phase 4 specialist via Task tool:
     - Skill: validation-urs-author
     - Context: Feature_Scoping_Logout.md + Risk_Assessment_Logout.md +
                Validation_Scope_Logout.md + Phase 3 approval comment

7. Phase 4 specialist drafts URS_Logout.md, citing prior-phase artefacts

8. validators/urs.py runs → schema_result recorded → loop back to step 3
```

The trace above is simplified — in the actual implementation, the audit log carries two entries per phase (one `approval: pending` when the artifact is written, one `approval: approved` after the reviewer signs off), the `artifact_hash` is computed in step 2 (not asserted in the audit-log step), and the orchestrator runs a post-invocation file-list check between steps 2 and 3 as a directional-isolation backstop.

Reference run (Logout, 2026-05-18): 16 audit-log entries, chain_status: complete, validation_status: Conditional Pass. Full state in `02_Logout/state.json`.

---

## 3. What this is NOT

To pre-empt likely reader assumptions:

- **Not a LangGraph / LangChain agent.** No graph DSL, no router, no agent framework dependency. The "agent" is Claude Code with skills + Task tool.
- **Not a Python orchestrator.** The orchestrator is a markdown skill. Python is used only for validators and audit tooling.
- **Not a workflow engine** (Airflow, Prefect, Temporal). No DAG, no retries, no scheduler. Sequential HITL-gated chain.
- **Not autonomous.** Every phase has a human gate. The framework's value is the *structure of the human gates*, not removal of humans.
- **Not production GxP-deployed yet.** Reference implementation tested end-to-end against a live web application (Sambhava test environment). Not running inside a pharma client's validation system.

---

## 4. Known limits (named honestly)

Surfaced by the first end-to-end dog-food run on Logout:

1. **AI-as-primary-author vs AI-as-assistant** — current flow has AI drafting, human approving. v2 direction: AI proposes structure, human authors content. ADR-007 candidate.
2. **Single-gate HITL.** Approval comes after the artefact. v2: two-gate (plan-approval before execution, artefact-approval after).
3. **Validation Scope can over-include integration/security tests** if it doesn't honour Risk Assessment's "reference vs produce" disposition.
4. **URS / OQ over-decomposition** when atomicity rules are read at observable-contract level instead of user-need level.
5. **Hallucination cascade through approval comments** — AI-suggested comment templates propagate as confirmed facts downstream. Mitigation: mark suggestions "to be verified."
6. **Reviewer UX** is flat-file markdown. A web view over markdown + audit log would surface traceability visually.
7. **state.json** does not yet persist Step 0 inputs (system URL, exec mode); resume re-asks.
8. **Token tracking** not yet in audit log (per-invocation tokens / cost / model).
9. **Model selection per phase** — specialists currently inherit orchestrator's model. Should explicitly downshift specialists to Sonnet/Haiku for cost.

---

## 5. Visual style guidance

For diagrams generated from this document:

- Audience: technical leaders (engineering directors, AI architects, governance heads).
- Style: technical-but-readable. Serious systems architecture. Not corporate boxes-and-arrows; not investor-deck gradients.
- Reference look: Vellum / Anthropic engineering-blog style — precise, restrained, hand-drawn-leaning.
- Show: skills + Task tool + state.json + validators + JSONL audit log + HITL gates as distinct components.
- Do not show: imaginary microservices, queues, brokers, or cloud-native infra that does not exist in the framework.
