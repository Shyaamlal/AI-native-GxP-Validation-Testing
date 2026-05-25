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
- **Not production GxP-deployed yet.** Reference implementation tested end-to-end against a live multi-role web platform in a test environment. Not running inside a pharma client's validation system.

---

## 4. Findings from the worked Logout run

The first end-to-end run of this framework validated the **Logout feature of a non-pharma web application** — classified under GAMP 5 Category 5 as an **access control** with direct 21 CFR Part 11 and EU Annex 11 obligations (full rationale in `02_Logout/Risk_Assessment_Logout.md`).

The run completed all eight phases — chain_status: complete, validation_status: Conditional Pass, zero feature defects — and surfaced a set of framework-level findings. The three foregrounded below are the most consequential for anyone designing AI workflows in a regulated context. Three further findings, named more briefly, follow.

### Three findings worth foregrounding

**1. Human ownership of substance — where AI assists vs where humans author.**

The current framework has AI drafting each artefact and the human reviewer approving. Output style varies with the model — Opus 4.7 today, Opus 5 tomorrow, another model next month each produce different decompositions, framing, and voice. The validator's role collapses to "gate." From a regulator's chair this is hard to defend ("Why does your URS look different month-to-month when your validation discipline hasn't changed?"). The v2 direction is to invert authorship: AI proposes structure and traceability, humans author content, diff-based revision becomes the norm rather than approve/reject. The AI Assistance Record then becomes granular — "AI proposed URS-001 through 004; validator authored URS-005 through 007; AI verified traceability." (ADR-007 candidate.)

**2. Pre-execution review — approving the plan, not just the output.**

The current framework has a single HITL gate per phase: the reviewer approves *after* the artefact is produced. In regulated practice, the auditor question is often "who decided what to test?" — answered *before* resources are committed. A two-gate-per-phase HITL pattern would close this: the specialist agent first produces a plan (observation scope, risk dimensions, scope decisions, test cases) with rationale; the validation lead reviews, edits and approves the plan; *then* the agent executes against the approved plan. This applies most directly to Phases 1, 2, 3 and 6 — the phases where the specialist is making choices a reviewer ought to be shaping in advance.

**3. Hallucinations propagating through human review.**

The most easily-missed failure mode the run surfaced. AI suggestions offered to the human during HITL approval — for example, a suggested approval-comment template — propagate as confirmed facts to downstream phases. At Phase 5 approval, the suggested comment included "Laravel default is 302 redirect to /login"; the validator pasted it verbatim; the Phase 6 agent then wrote TC-017 asserting a 302 specifically, when the actual response shape had not been empirically verified (Laravel's unauthenticated response depends on middleware configuration). The amendment at the gate replaced the assertion with an observed-then-asserted set. The human-in-the-loop can be deceptively present when AI is seeding what the human says. Mitigations: approval comments authored by the validator without AI-suggested templates; AI-suggested comments where offered marked "to be verified"; test cases defaulting to "observe shape, then assert" rather than asserting a specific shape that has not been observed.

### Three additional named findings

**4. URS / OQ over-decomposition.** The atomicity rule "one item per row" was read by the URS agent at *observable-contract* level rather than at *user-need* level — producing 11 URS items for a feature where a senior validation lead would produce 4–5. The same root cause cascaded into the OQ Protocol: 1:1 AC-to-TC mapping enforced by the skill produced 21 test cases where one comprehensive test case can often cover multiple related acceptance criteria. Skill-level tuning needed: atomicity defined at user-need level for URS, many-ACs-to-one-TC permitted for OQ where the ACs are practically exercised in the same scenario.

**5. OQ vs integration vs security testing — scope discipline.** The Validation Scope artefact for Logout included server-side session-revocation tests as in-scope OQ test cases (cookie capture + replay, Network panel inspection). The Risk Assessment had correctly designated these as "evidence to reference rather than produce within this chain" — but the Validation Scope skill did not honour that disposition, and the items were promoted to OQ depth. Senior validation judgment caught this at execution time and relocated the test cases. The framework fix is to require the Validation Scope skill to inherit Risk Assessment's "reference vs produce" disposition explicitly. OQ verifies user-facing functional behaviour; backend security assertions belong in security review and are referenced as supporting evidence in the validation package, not re-verified per feature.

**6. Approval-comment propagation behaviour.** Approval comments written by the human reviewer do propagate as context to the next phase's specialist — *when supplied*. At Phase 2 → Phase 3, the reviewer approved without supplying a comment (frontmatter `comment: null`), and the next phase's agent did not inherit any disposition. At Phase 3 → Phase 4 the same mechanism worked correctly when a comment was present. The current behaviour is "propagate if supplied, ignore if null" — which is technically correct but operationally fragile. The orchestrator should prompt the reviewer for a comment at each approval, even if the comment is "approved as-is, no additional disposition."

### Findings from the methodology-metrics pass

A second tool, `tools/methodology_metrics.py`, reads the same audit log and computes methodology-level metrics for the run (timing, HITL distribution, validator outcomes, integrity scan). Running it against the Logout log surfaced three further findings.

**7. Audit-log integrity — an inverted-timestamp pair.** The metrics tool computes per-phase duration as `approval_timestamp − emission_timestamp`. Phase 4 (URS) returned a *negative* duration: the approval timestamp (`2026-05-18T20:53:38Z`) precedes the emission timestamp (`2026-05-18T20:54:00Z`) by 22 seconds. This directly challenges the framework's tamper-evidence claim. The audit log is presented as append-only with monotonic timestamps; a decision recorded as occurring before the artifact it approves was emitted is, on its face, impossible. The cause here was almost certainly a manual edit to the log during the run, not a malicious change — but that is the point: the integrity guarantee is only as strong as the discipline that timestamps must be machine-generated at the moment of write by a single authoritative clock, never hand-entered or back-filled. The tool reports the negative duration honestly rather than taking its absolute value. (ADR/backlog candidate: timestamp generation moved server-side / write-time only; consider entry-to-entry hash chaining so a post-hoc edit is detectable, not just an artifact edit.)

**8. Wall-clock conflates compute with reviewer wait.** Phase 2 (risk-assessment) shows 6h 48m of "duration" — but the agent emitted its artifact at 13:51 UTC and human approval landed at 20:39 UTC. That interval is the artifact sitting in a reviewer's queue, not work. The current schema cannot separate agent compute time from human-gate latency, so any timing metric overstates effort wherever a review spanned a break. A `review_started_at` field at each gate would make the distinction recoverable.

**9. Self-correction loops and rejection paths are invisible to the log.** Two instrumentation gaps, both meaning "the log records less than the run contained": (a) every `schema_result` in the Logout run is `pass`, but the log captures only the *final* validator outcome surfaced to the gate — a specialist that failed validation and self-corrected before the entry was written would still log a single `pass`, so validator-driven retry loops cannot be counted; (b) the run had a 0% HITL rejection rate, but the reject / request-changes paths were never exercised, and the schema does not enforce a decision enum — so the log offers no evidence that rejection is even recorded distinctly. Recommendation: log each validator attempt (not just the surfaced outcome) and confirm reject/changes events emit as distinct entries.

### Where the other observations live

Implementation-level deferred decisions surfaced by the same run — state.json schema additions (Step 0 inputs persistence), token tracking in the audit log, per-phase model selection (orchestrator on Opus, specialists downshifted to Sonnet/Haiku for cost), and the reviewer-UX gap between flat-file markdown and an integrated traceability view — are recorded in the design document's deferred-decisions register (§11) rather than here, since they are work-in-progress backlog rather than insight from the run.

Per-run open items and conditions for upgrade from Conditional Pass to Pass are documented in `02_Logout/Validation_Summary_Report_Logout.md` §8.

---

## 5. Visual style guidance

For diagrams generated from this document:

- Audience: technical leaders (engineering directors, AI architects, governance heads).
- Style: technical-but-readable. Serious systems architecture. Not corporate boxes-and-arrows; not investor-deck gradients.
- Reference look: Vellum / Anthropic engineering-blog style — precise, restrained, hand-drawn-leaning.
- Show: skills + Task tool + state.json + validators + JSONL audit log + HITL gates as distinct components.
- Do not show: imaginary microservices, queues, brokers, or cloud-native infra that does not exist in the framework.
