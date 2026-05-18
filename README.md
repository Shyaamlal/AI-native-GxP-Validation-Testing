# Agentic IT GxP Validation Framework

An agentic framework for IT GxP validation work (computerised systems validation under GxP). A single Orchestrator skill coordinates eight specialist agents — each one rung of a V-model methodology — under Human-in-the-Loop gates and a deterministic Python reliability layer.

The framework is a portfolio piece. It demonstrates how agentic systems could augment validation work in regulated environments. It is not enterprise-deployable; the relationship to production GxP requirements is set out explicitly in [§2 of the design doc](./00_Project_Context/Agentic_Framework_Design.md).

---

## Status

| Phase | Description | State |
|---|---|---|
| 0 | Repo audit | Complete |
| 1 | Design | Complete — see `00_Project_Context/Agentic_Framework_Design.md` v1.1 |
| 2 | Cleanup | Complete |
| 3 | Build agentic framework (skills + orchestrator + Python reliability layer) | Complete |
| 4 | First dog-food run (real feature end-to-end) | Pending |
| 5 | Substantive non-auth feature run | Pending |
| 6 | Governance docs | Pending |
| 7 | Polish | Pending |
| 8 | Narrative artifacts | Pending |

Validators are unit-tested via `validators/_smoke_test.py` (18 cases — valid and invalid synthetic artifacts per rung). End-to-end framework validation requires a live feature run (Phase 4).

---

## What this framework is

- A demonstration of how agentic systems could augment IT GxP validation work
- A working prototype of HITL gates, AI Assistance Records, and traceability automation
- A set of deliberate engineering choices about what belongs in prompts versus code (ADR-005)
- An artifact that can be cloned and run end-to-end on a real application

## What this framework is not

- A production-ready GxP validation system
- A replacement for Veeva Vault, ValGenesis, Kneat, or any controlled document system
- Compliant on its own with 21 CFR Part 11, EU Annex 11, or GAMP 5 tool qualification requirements

Production GxP deployment would require formal tool qualification (GAMP 5 Category 5), enterprise controlled-document hosting, and integration with regulated audit trail systems — none of which are in scope here.

---

## Architecture at a glance

The Orchestrator walks the V-model. Feature Scoping, Risk Assessment, and Validation Scope are pre-V bounding activities; the chain then descends the specification arm (URS → FRS), jumps to the OQ rung (OQ Protocol → OQ Execution), and climbs back to the Validation Summary Report. A higher-order Release Summary skill consolidates per-feature summaries for change-request / release rollups.

```
                           ┌────────────────────────┐
                           │     Human Reviewer     │
                           │  (approves at every    │
                           │   rung transition)     │
                           └───────────┬────────────┘
                                       │ approve / reject
                                       ▼
        ┌─────────────────────────────────────────────────────────────┐
        │              Orchestrator  (validate-feature)               │
        │   - Spawns specialist agents one rung at a time             │
        │   - Runs the Python schema validator at each handoff        │
        │   - Writes an append-only entry to ai_assistance_log.jsonl  │
        │   - Persists state.json per feature                         │
        └─┬──────────────┬──────────────┬───────────────┬─────────────┘
          │              │              │               │
          ▼              ▼              ▼               ▼
     Feature       Risk Assessment   ... (eight rungs total) ...   Summary
     Scoping                                                        Report
```

Agents are bounded by role and by directional isolation (ADR-001) — each specialist reads upstream artifacts only and writes its own artifact only. The Validation Summary Report skill is a declared exception.

For the full architecture, V-model traversal details, ADRs, and deferred design decisions, see [`00_Project_Context/Agentic_Framework_Design.md`](./00_Project_Context/Agentic_Framework_Design.md).

---

## Repository structure

```
AI-native-GxP-Validation-Testing/
├── 00_Project_Context/
│   ├── Agentic_Framework_Design.md     # The design doc (v1.1, reviewed)
│   ├── Application_Context.md
│   ├── Methodology.md                  # v1 methodology — deprecated, retained for narrative arc
│   └── Templates/
├── 00_Validation_Management/
├── 01_Login/                           # First validated feature (v1 artifacts, pre-agentic)
├── 02_Logout/                          # Second validated feature (v1 artifacts)
├── .claude/skills/                     # The agentic framework
│   ├── validate-feature.md             # Orchestrator (entry point)
│   ├── validation-feature-scoping.md
│   ├── validation-risk-assessment.md
│   ├── validation-scope.md
│   ├── validation-urs-author.md
│   ├── validation-frs-author.md
│   ├── validation-oq-protocol-author.md
│   ├── validation-oq-execution.md
│   ├── validation-summary-report.md
│   └── validation-release-summary.md   # Higher-order, for change-request / release rollup
├── validators/                         # Python schema validators (one per rung)
│   ├── _common.py
│   ├── _smoke_test.py                  # 18-case unit test suite
│   ├── feature_scoping.py
│   ├── risk_assessment.py
│   ├── validation_scope.py
│   ├── urs.py
│   ├── frs.py
│   ├── oq_protocol.py
│   ├── oq_execution.py
│   ├── summary_report.py
│   └── release_summary.py
├── tools/
│   └── audit.py                        # CLI to query ai_assistance_log.jsonl
├── ai_assistance_log.jsonl             # Append-only AI assistance record
└── README.md                           # This file
```

---

## Running a feature through the framework

Prerequisites:
- Claude Code installed
- Python 3.10+ (for the validator + audit CLI)
- (For OQ Execution against a live system) Playwright MCP configured

From Claude Code in the repo root:

```
/validate-feature <FeatureName>
```

The Orchestrator will walk through the eight rungs one at a time. At each rung:

1. The specialist agent produces its artifact (e.g. `Feature_Scoping_<feature>.md`).
2. The Python schema validator for that rung runs. If it fails, the agent is asked to correct and re-emit.
3. The artifact is surfaced to you for `approve` / `reject <reason>` / `changes <description>`.
4. An entry is appended to `ai_assistance_log.jsonl`.
5. On approve, the chain advances to the next rung.

For a single rung: `/validate-feature <FeatureName> --rung <rung-name>`.

To resume an interrupted validation: `/validate-feature <FeatureName> --resume`.

Per-rung skills, allowed upstream reads, and the state.json schema are documented in `.claude/skills/validate-feature.md`.

---

## AI Assistance Record

Every artifact carries YAML frontmatter declaring the agent skill, model, invocation timestamp, prompt version, and human review fields. The same information is written as a JSON line to the central `ai_assistance_log.jsonl` at each handoff, with an SHA-256 hash anchoring the audit entry to the specific artifact content at approval time.

Query the log:

```bash
python tools/audit.py --feature <FeatureName>
python tools/audit.py --model claude-opus-4-7 --since 2026-05-01
python tools/audit.py --reviewer shyaamlal --status approved
python tools/audit.py --artifact 01_Login/URS_Login.md
python tools/audit.py --tail 10 --format json
```

The audit trail is real, not claimed. The CLI is the demonstration.

---

## Methodology

Eight-phase, V-model:

1. **Feature Scoping** — observable behaviour, user-visible boundaries, system responses
2. **Risk Assessment** — GxP impact, patient safety, data integrity (organisation's chosen framework: GAMP 5 RBA, FMEA, HACCP, or equivalent)
3. **Validation Scope** — what will and will not be validated, justified against the risk assessment
4. **URS** — user requirements in user-facing language
5. **FRS** — functional requirements with explicit acceptance criteria per item
6. **OQ Protocol** — executable test cases tracing to FRS acceptance criteria
7. **OQ Execution** — executed test record
8. **Validation Summary Report** — consolidated package, the unit of audit for a single change

Plus an optional higher-order **Release Summary** that consolidates multiple per-feature Validation Summary Reports for change-request / release rollups.

Design Specification (DS) is deliberately deferred (see [§11.1](./00_Project_Context/Agentic_Framework_Design.md)) — in computerised systems validation, configurable systems typically substitute Configuration Specifications, and the chain URS → FRS (with acceptance criteria) → OQ Protocol traces cleanly without it.

This is prospective validation methodology (ADR-004), applied to features as they are introduced.

---

## Existing v1 artifacts (Login, Logout)

`01_Login/` and `02_Logout/` contain artifacts produced under the pre-agentic v1 methodology (retrospective, ten-step). They are retained as the narrative arc — *"started with manual prompts in Claude Web → reusable Skills → agentic orchestrator with HITL gates."* See [Appendix A of the design doc](./00_Project_Context/Agentic_Framework_Design.md). The v1 artifacts will be regenerated through the agentic framework in Phase 4-5.

---

## Smoke-testing the validators

```bash
python validators/_smoke_test.py
```

Generates synthetic valid and invalid artifacts for every rung, runs each through its validator, and reports expected-vs-actual. 18 cases. This is a unit test of the validator layer — not an end-to-end framework test. The end-to-end test is Phase 4 (live feature run).

---

## Enterprise toolchain context

In a real deployment, requirements would flow from JIRA / Azure DevOps; OQ protocols and execution records would land in HP ALM / X-Ray / TestRail; the AI assistance log would feed enterprise audit trails. This framework does not implement those integrations — its role is to demonstrate the agent orchestration patterns those plug-in points would consume.

---

## Reference

- [Design document v1.1](./00_Project_Context/Agentic_Framework_Design.md) — architecture, ADRs, deferred decisions
- [Orchestrator skill](./.claude/skills/validate-feature.md) — invocation, per-rung protocol, state.json schema
- [Specialist skills](./.claude/skills/) — one per rung
- [Validators](./validators/) — per-rung schema validators + shared helpers + smoke test
- [Audit CLI](./tools/audit.py) — queries over the AI assistance log

---

## License

Shared for educational and professional reference purposes. The validation artifacts and code in this repository are for demonstration only and would require formal tool qualification before any production use under GxP.

---

## Contact

**LinkedIn:** [shyaamlal-n-n](https://www.linkedin.com/in/shyaamlal-n-n/)
