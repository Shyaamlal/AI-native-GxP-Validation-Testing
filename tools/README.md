# `tools/` — Audit and Utility CLIs (Python)

Small Python command-line tools that operate over the validation artifacts and the central AI Assistance Log.

**Status:** Built in Phase 3 (2026-05-17).

---

## `audit.py` — Audit Log Query CLI

Reads the central `ai_assistance_log.jsonl` at repo root and answers queries that a regulator's audit, a Change Advisory Board, or a developer's inspection would ask.

```bash
python tools/audit.py --feature Add_Client
python tools/audit.py --model claude-opus-4-7 --since 2026-05-01
python tools/audit.py --reviewer shyaamlal --status approved
python tools/audit.py --artifact 03_Add_Client/URS_Add_Client.md
python tools/audit.py --phase-name feature-scoping
python tools/audit.py --tail 10 --format json
python tools/audit.py --help
```

Filters: `--feature`, `--model`, `--reviewer`, `--artifact`, `--status` (pending / approved / rejected), `--phase` (number), `--phase-name` (e.g. `feature-scoping`), `--skill`, `--since`, `--until`, `--tail`. Output formats: `table` (default), `json`, `jsonl`.

Per ADR-005, Python is used here because structured filters over an append-only log are not something a prompt does deterministically.

**Reference:** [`../00_Project_Context/Agentic_Framework_Design.md`](../00_Project_Context/Agentic_Framework_Design.md) §9.2 (Central JSONL Audit Log) and §10 (Python Reliability Layer).

---

## Traceability

Per design v1.2, traceability is produced inline by the **Validation Summary Report** specialist skill (Phase 8 of the chain — see §5 Traceability Matrix) and consolidated across releases by the **Release Summary** higher-order skill — not by a standalone Python tool. The Phase 0 audit's call for a `traceability.py` tool was satisfied by the agentic approach instead.

If a future need arises for an out-of-band traceability matrix generator (e.g. dashboard rendering, BI export), it would belong here.

---

## Deliberately not in scope

Per ADR-005 (Python Only Where It Beats Prompts):

- A CLI wrapper for the Orchestrator (Claude Code is already the runtime)
- FastAPI / web service around the audit log
- Pydantic models for every schema
- GitHub Actions CI

These would inflate the Python surface without strengthening the agentic story. Documented as considered and deliberately excluded.
