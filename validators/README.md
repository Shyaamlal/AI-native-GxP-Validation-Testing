# `validators/` — Schema Validation Layer (Python)

This folder contains Python schema validators, one per rung that produces an artifact. The Orchestrator calls these at the phase-complete handoff to verify the specialist agent's artifact passes structural checks before surfacing it to the human review gate.

**Status:** Phase 3 build in progress. Per design v1.1 — see `../00_Project_Context/Agentic_Framework_Design.md` §10.1 (Validators) and ADR-003 (Schema Validation as the Phase-Complete Gate).

## Planned validators (one per rung)

- `feature_scoping.py` — Phase 1 (built)
- `risk_assessment.py` — Phase 2
- `validation_scope.py` — Phase 3
- `urs.py` — Phase 4
- `frs.py` — Phase 5 (also enforces acceptance criteria per FRS item)
- `oq_protocol.py` — Phase 6
- `oq_execution.py` — Phase 7
- `summary_report.py` — Phase 8
- `release_summary.py` — Higher-order Release Summary skill

Each validator checks:
- Required frontmatter fields present and non-empty (artifact_type, feature, version, status, ai_assistance, human_review, traceability)
- Required content sections present and non-empty
- No forbidden placeholder patterns (`[Document what happened]`, `TODO`, `TBD`, `[describe...]`, etc.)
- Content-specific rules per rung (e.g. URS validator confirms unique requirement IDs; FRS validator confirms every requirement has ≥1 acceptance criterion; OQ validator confirms every test case traces to at least one requirement)

## Why Python and not prompt-based self-check

Deterministic regex and structural checks never miss; LLM self-checks miss sometimes. For a phase-complete gate that decides whether to bother the human reviewer, "never misses" is the right reliability tier.

See `feature_scoping.py` as the reference implementation. New validators follow the same shape: a `validate(path) -> (bool, list[str])` function returning pass/fail + structured error list, printed as JSON for the Orchestrator to parse.

## Invocation

```bash
python validators/<rung>.py <artifact_path>
```

Returns exit code 0 on pass, 1 on fail. Stdout is a JSON object with `pass`, `artifact`, `validator`, `errors`.
