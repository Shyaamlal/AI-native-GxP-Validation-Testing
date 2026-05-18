# `.claude/skills/` — Specialist Validation Agents

This folder contains the Claude Code skills that make up the agentic IT GxP validation framework. Each specialist skill is one rung of the V-model methodology. The Orchestrator skill (`validate-feature`) coordinates them.

**Status:** Phase 3 build in progress. Per design v1.1 — see `../../00_Project_Context/Agentic_Framework_Design.md` §6 (Specialist Agent Specifications) and §7 (Orchestrator Specification).

## Eight-rung specialist chain

| # | Rung | Skill file |
|---|---|---|
| 1 | Feature Scoping | `validation-feature-scoping.md` |
| 2 | Risk Assessment | `validation-risk-assessment.md` |
| 3 | Validation Scope | `validation-scope.md` |
| 4 | URS | `validation-urs-author.md` |
| 5 | FRS | `validation-frs-author.md` |
| 6 | OQ Protocol | `validation-oq-protocol-author.md` |
| 7 | OQ Execution | `validation-oq-execution.md` |
| 8 | Validation Summary Report | `validation-summary-report.md` |

## Higher-order skill (optional)

- `validation-release-summary.md` — consolidates multiple per-feature Validation Summary Reports into a release-level rollup for change requests / Change Advisory Boards. Operates one layer above the per-feature chain.

## Orchestrator

- `validate-feature.md` — `/validate-feature <feature-name> [--rung <rung>]`. Walks a feature through the eight-rung chain one rung at a time. Spawns specialist agents, runs schema validators, gates on human approval. See orchestrator skill itself for current scope.

## Directional isolation

Each specialist skill operates under directional isolation — it reads upstream artifacts only and writes its own artifact only. Tool permissions are scoped via skill frontmatter where possible, and enforced by prompt where not. The Validation Summary Report and Release Summary skills are declared exceptions (they need read access across the feature folder / release scope).
