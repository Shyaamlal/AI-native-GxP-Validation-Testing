# 01_Login — v1 Methodology Reference

This folder holds validation artifacts for the Login feature, produced under the **v1 methodology** (retrospective, ten-step, manual prompts in Claude Web / ChatGPT). It is retained for reference and to document the v1 → v2 transition.

The v1 chain includes phases that no longer exist in v2:

- **Design Specification (DS)** — deferred under v2 (see [ADR-004](../00_Project_Context/Agentic_Framework_Design.md)). In computerised systems validation, configurable systems typically substitute Configuration Specifications; the chain URS → FRS (with explicit acceptance criteria per item) → OQ Protocol traces cleanly without DS.
- **Verification Report** — dropped under v2. Retrospective-validation artefact that does not apply under prospective framing.
- **Test Readiness Report** — v1-only intermediate artefact.

For the v2 end-to-end run, see [`../02_Logout/`](../02_Logout/) and its `state.json` / `ai_assistance_log.jsonl` trace.

## Files in this folder

| File | v2 equivalent |
|---|---|
| `Feature_Observation_Login.md` | `Feature_Scoping_<feature>.md` (renamed in v2) |
| `Feature_Boundary_Definition_Login.md` | folded into `Validation_Scope_<feature>.md` |
| `DS_Login.md` | deferred (no v2 equivalent) |
| `FRS_Login.md` | `FRS_<feature>.md` |
| `URS_Login.md` | `URS_<feature>.md` |
| `OQ_Protocol_Login.md` | `OQ_Protocol_<feature>.md` |
| `Test_Readiness_Report_Login.md` | dropped |
| `Verification_Report_Login.md` | dropped |
| `Validation_Summary_Report_Login.md` | `Validation_Summary_Report_<feature>.md` |
