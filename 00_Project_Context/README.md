# `00_Project_Context/` — Project Context

This folder holds the design, methodology, and application-knowledge documents that govern the framework.

---

## Files

**Active (v1.1):**

- **`Agentic_Framework_Design.md`** — The design document for the agentic IT GxP validation framework. Architecture, ADRs, methodology, deferred decisions. Version 1.1 (reviewed 2026-05-17). **The single source of truth for the current framework.**
- **`Application_Context.md`** — Knowledge about the application under validation (voice-analysis platform standing in for the regulated target system). System overview, user workflows, technical architecture, business rules, risk context. Read by specialist agents that need application-domain awareness.

**Historical (v1, deprecated):**

- **`Methodology.md`** — The original v1 ten-step retrospective methodology, manually executed via Claude Web. Frozen as a historical reference. The deprecation header at the top documents the v1 → v1.1 changes.
- **`Review_Notes_2026-03-19.md`** — Early-stage review notes from before the agentic pivot. Historical only.

**Supporting:**

- **`Templates/`** — Reusable artifact templates referenced by specialist skills.

---

## Where to start

- **Reviewing the framework:** read `Agentic_Framework_Design.md`.
- **Running a feature through the framework:** the entry point is `/validate-feature <FeatureName>` in Claude Code (orchestrator skill at `.claude/skills/validate-feature.md`).
- **Understanding the evolution from v1 to v1.1:** read the deprecation headers at the top of `Methodology.md` and `../AI_Process_Documentation.md`.
- **Understanding the target system:** read `Application_Context.md`.

---

## Reference

- Top-level [`../README.md`](../README.md) — repository overview, current build state, how to run a feature
- Orchestrator skill: [`../.claude/skills/validate-feature.md`](../.claude/skills/validate-feature.md)
- AI Assistance Record format: [`Agentic_Framework_Design.md`](./Agentic_Framework_Design.md) §9
- Audit CLI: [`../tools/audit.py`](../tools/audit.py)
