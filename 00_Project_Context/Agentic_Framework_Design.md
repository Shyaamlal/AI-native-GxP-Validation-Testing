---
title: Agentic Validation Framework — Design Document
version: 1.2
status: Phase 4 complete — first end-to-end agentic run on Logout (2026-05-18); validation_status Conditional Pass
date: 2026-05-17
author: Shyaamlal Nandalal
ai_assistance: |
  v1.0 (2026-05-16): Initial design developed in a structured Q&A session with Claude (Opus 4.7).
  11 architectural decisions resolved through that session. Claude drafted v1.0 from those decisions.
  v1.1 (2026-05-17): Review pass with Shyaamlal — 22 inline review comments worked through together.
  Substantive changes: IT GxP framing, V-model reframing, DS phase dropped, Release Summary added as
  higher-order skill, ADRs moved to §3, FRS acceptance criteria + validator enforcement, Risk framework
  plug-in, Playwright + Python qualification out-of-scope notes.
  v1.2 (2026-05-17, evening): Orchestrator-skill review pass — 6 inline review comments addressed.
  Substantive changes: vocabulary standardised to "phase" (V-model framing retained as conceptual);
  §6 preamble expanded with CR-as-input + Master Validation Plan / planning-skill note framed as
  planned Phase 6 deliverable (waterfall + SAFe ART contexts); §6.3 scope-first rationale added;
  §11.11 multi-role approval note refined; §11.12 (tool-permission enforcement) and §11.13
  (within-phase checkpointing) added as deferred decisions. Human author owns the methodology
  choices, role framing, regulated-industry interpretation, and final review.
---

# Agentic Validation Framework — Design

## 1. Executive Summary

This document specifies the design of an agentic framework for **IT GxP validation work** (computerised systems validation under GxP). The framework consists of a single Orchestrator skill that coordinates eight specialist agents (plus an optional higher-order Release Summary skill), each responsible for producing one validation artifact under a Human-in-the-Loop (HITL) gate. A minimal Python reliability layer (artifact validators + audit query CLI) sits alongside the agents to enforce structural correctness and queryable audit history.

Agents are bounded by role and by directional isolation — a **separation-of-concerns** model that mirrors how real validation chains hand off between roles (validation tester, validation lead, business analyst, systems analyst, designer, QA tester). No agent reaches across the chain.

The framework is implemented using agentic LLM tooling — **Claude Code as the orchestration platform**. It is designed to be cloned, inspected, and run end-to-end by a reviewer with Claude Code installed. The Orchestrator drives an eight-phase methodology — Feature Scoping → Risk Assessment → Validation Scope → URS → FRS → OQ Protocol → OQ Execution → Validation Summary Report — with a human approval gate after every phase.

**Enterprise toolchain context.** In a real deployment, requirements would flow from JIRA / Azure DevOps; OQ protocols and execution records would land in HP ALM / X-Ray / TestRail; the AI assistance log would feed enterprise audit trails. This framework does not implement those integrations — its role is to demonstrate the agent orchestration patterns those plug-in points would consume.
## 2. Scope and Non-Scope

**In scope:**
- An eight-phase validation chain orchestrated as Claude Code skills, with a human approval gate after each phase
- HITL gates, AI Assistance Records, and traceability automation across the chain
- Per-phase Python schema validators and an audit-log query CLI
- Worked end-to-end runs against a non-pharma web application (a stand-in for a regulated target system)

**Out of scope:**
- A production-ready GxP validation system
- A replacement for Veeva Vault, ValGenesis, Kneat, or any controlled document system
- Standalone compliance with 21 CFR Part 11, EU Annex 11, or GAMP 5 tool qualification requirements

Production GxP deployment would require formal tool qualification (GAMP 5 Category 5), enterprise controlled-document hosting, and integration with regulated audit trail systems — none of which are in scope here.

**Intended fit:**
Agents that plug into existing validation stacks — drafting inputs for Veeva Vault, triaging deviations, cross-checking traceability matrices, pre-reviewing supplier documentation against compliance checklists. Narrow, augmentative, never touching the system of record directly. This framework implements the orchestration patterns those plug-in agents would use.

## 3. Architectural Decision Records (ADRs)

These five decisions shape every choice in sections 4-10. Read them first to understand the framework's spine.

### ADR-001: Directional Isolation Between Agents

**Decision:** Each specialist agent runs in a fresh context window with read access to upstream artifacts only and write access to its own artifact only. Tool permissions are enforced via skill `tools:` frontmatter, not by convention.

**Rationale:** Prevents whole classes of failure (agents "helpfully" editing another phase's artifact) without relying on agent good behaviour. Matches how real validation chains work — each role reads upstream specs and hands off, never reaching back or jumping forward.

**Exception:** The Validation Summary Report agent has read access across the entire feature folder plus the audit log. The summary cannot be produced without this access; the exception is deliberate and declared.

### ADR-002: HITL Gate at Every Phase Transition

**Decision:** The Orchestrator pauses for explicit human approval after every phase transition. No phase advances on agent confidence alone.

**Rationale:** Defensible under a GAMP 5 / EU Annex 11 mindset — every AI-generated artifact receives human attestation before it is consumed downstream. The cost is review cycles; the benefit is that no agent decision is unverified.

**Considered alternative:** Risk-classified gates (pause only at high-risk transitions). Rejected because it requires the framework to itself perform risk classification on its own outputs, which introduces a recursion the design did not want to handle.

### ADR-003: Schema Validation as the Phase-Complete Gate

**Decision:** A phase is considered complete only when (a) the specialist agent emits a structured `phase_complete(artifact_path, summary)` signal AND (b) the Python validator for that phase passes against the artifact. Only schema-passing artifacts reach the human gate.

**Rationale:** The agent self-report alone is insufficient — agents have been observed declaring phases complete with placeholder content still present (see Gap #2 in the Phase 0 repo audit, where `[Document what happened]` shipped in a Feature Scoping). Schema validation is the deterministic check that catches what the agent missed. The human gate is then reserved for substantive review, not janitor work.

### ADR-004: Prospective Validation Framing

**Decision:** The methodology is framed as prospective validation applied to features as they are added, not retrospective validation of pre-existing systems.

**Rationale:** Retrospective framing requires awkward derivation gymnastics (e.g. "URS reconstruction from observation") that read as weird to any reader familiar with standard GAMP 5 lifecycle. Prospective framing is cleaner, transferable, and what readers expect. The fact that the target application happens to already exist is treated as a starting point ("we observe the existing feature as if it were proposed") rather than reframing the entire methodology around retrospection.

### ADR-005: Python Only Where It Beats Prompts

**Decision:** Python is used for (a) artifact schema validators and (b) the audit log query CLI. It is not used for orchestration UX, web services, or scaffolding around capabilities Claude Code already provides.

**Rationale:** Python adds value where it provides a reliability gain a prompt cannot match — deterministic regex checks against an artifact body, structured queries over an append-only log. Wrapping Claude Code's existing capabilities in Python adds maintenance cost without a reliability gain.

## 4. Architecture Overview

```
                           ┌────────────────────────┐
                           │     Human Reviewer     │
                           │  (approves at every    │
                           │   phase transition)    │
                           └───────────┬────────────┘
                                       │ approve / reject
                                       │
        ┌──────────────────────────────▼──────────────────────────────┐
        │                       Orchestrator                          │
        │   /validate-feature <feature-name> [--resume]               │
        │                                                             │
        │   - Spawns specialist agents one phase at a time            │
        │   - Catches phase_complete signal from each agent           │
        │   - Runs schema validator before surfacing to human         │
        │   - Writes audit log entry per invocation                   │
        │   - Persists state.json per feature                         │
        └─────┬──────────────┬────────────────┬──────────────┬────────┘
              │              │                │              │
              ▼              ▼                ▼              ▼
        ┌─────────┐    ┌──────────┐     ┌─────────┐    ┌─────────┐
        │ Phase 1 │    │ Phase 2  │ ... │ Phase 7 │    │ Phase 8 │
        │ Feature │    │ Risk     │     │ OQ Exec │    │ Summary │
        │ Scoping │    │ Assess   │     │         │    │  Report │
        └────┬────┘    └────┬─────┘     └────┬────┘    └────┬────┘
             │              │                │              │
             ▼              ▼                ▼              ▼
        ┌─────────────────────────────────────────────────────────────┐
        │              Feature Folder (artifact store)                │
        │   <NN>_<feature_name>/                                      │
        │     ├── Feature_Scoping_<feature>.md                    │
        │     ├── Risk_Assessment_<feature>.md                        │
        │     ├── Validation_Scope_<feature>.md                         │
        │     ├── URS_<feature>.md                                    │
        │     ├── FRS_<feature>.md                                    │
        │     ├── OQ_Protocol_<feature>.md                            │
        │     ├── OQ_Execution_Record_<feature>.md                    │
        │     ├── Validation_Summary_Report_<feature>.md              │
        │     └── state.json                                          │
        └─────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
        ┌─────────────────────────────────────────────────────────────┐
        │              Python Reliability Layer                       │
        │   validators/<phase>.py — schema validators (called         │
        │                           by Orchestrator at handoff)       │
        │   tools/audit.py        — CLI to query the central log      │
        └─────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
        ┌─────────────────────────────────────────────────────────────┐
        │   ai_assistance_log.jsonl  (central, immutable, append-only)│
        └─────────────────────────────────────────────────────────────┘
```

## 5. Methodology — The 8-Phase Chain

| # | Phase | Agent voice | Purpose |
|---|---|---|---|
| 1 | Feature Scoping | Validation tester / observer | Scope what the feature does — observable behaviour, user-visible boundaries, system responses |
| 2 | Risk Assessment | Quality risk lead | Determine GxP impact, patient safety risk, data integrity risk, risk classification |
| 3 | Validation Scope | Validation lead | Define what is in/out of scope based on risk |
| 4 | URS | Business user / business analyst | User requirements in user language |
| 5 | FRS | Systems analyst | Functional requirements with explicit acceptance criteria, derived from URS |
| 6 | OQ Protocol | QA tester | Test cases tracing to URS / FRS acceptance criteria |
| 7 | OQ Execution | QA tester | Executed test record |
| 8 | Validation Summary Report | Validation lead | Consolidated summary referencing all upstream artifacts |

**OQ-only scope.** This methodology covers the OQ layer (Operational Qualification — confirming the feature performs as specified). IQ (Installation Qualification — infrastructure and environment) and PQ (Performance Qualification — end-to-end business process under realistic load) are out of scope: IQ is infrastructure-layer and orthogonal to feature work, PQ is release-level and lives downstream of feature validation.

**Pre-validation activity is out of scope.** This framework operates in the validated environment, after development and functional testing have stabilised the feature. Informal testing, bug discovery, and dry runs happen upstream of this chain in DEV/QA environments. Bugs found during OQ Execution are handled as deviations against the protocol, not as ordinary test cycle output.

**Framing:** This is prospective validation methodology — features are validated as they are introduced, not reconstructed after the fact.

**Role-specific voice:** Each agent's prompt explicitly instructs the agent to write from the perspective of the role that normally produces that artifact. A real URS reads in user language; a real FRS in functional/systems language; an OQ Protocol in QA-tester language. Mixing voices is the single fastest credibility leak in a validation document set.

## 6. Specialist Agent Specifications

Each specialist agent is implemented as a repo-local Claude Code skill at `.claude/skills/<skill-name>.md`. Each runs in a fresh context window (no pollution from prior agents). Tool permissions are scoped per agent to enforce **directional isolation**: read access to upstream artifacts only, write access to own artifact only.

**Prompts live with the skill.** Each specialist agent's prompt is the body of its `.claude/skills/<skill-name>.md` file. The skill file IS the prompt, version-controlled in Git. Prompt edits are git commits; prompt versions are git tags or commit SHAs. Governance questions (baselining, peer review of prompt edits, re-generation discipline) are deferred to §11.6.

**Sequential within a feature, iterative across features.** Within a single feature, the methodology is sequential by design — each artifact traces to the upstream artifact and cannot exist without it. Across features, the framework is iterative: each feature carries its own end-to-end chain. This is not a critique of agile delivery; it is the shape of traceability under GxP.

**Change request / release context — planned Phase 6 deliverable.** This section specifies the per-feature chain. In production deployment, the per-feature chain is driven by a change request (waterfall context) or a PI scope decision (SAFe Agile Release Train context — at PI planning, the ART decides which CRs are in scope, and a Master Validation Plan is drafted in the org's controlled-document system such as TIMS, Veeva Vault, or ValGenesis). A higher-order **planning skill** — `validation-plan-author` — is a planned Phase 6 deliverable in the build plan. It takes a change request as input and emits the per-feature work plan (which features are in scope, what risk classification each carries, what scope decisions apply) that drives this chain. The `Master_Validation_Plan.md` placeholder at the repo root is reserved for that layer; building it now would be aspirational fiction (it would describe wished-for state, not real state), which is why the build plan sequences it after Phases 3-5 prove the per-feature pattern works. The Release Summary skill (§6.9) consolidates the per-feature outputs back to release level.

### 6.1 Feature Scoping

- **Skill name:** `validation-feature-scoping`
- **Voice:** Validation tester scoping the feature against the live system
- **Inputs:** The live application (no upstream artifacts — this is phase 1)
- **Outputs:** `<feature_folder>/Feature_Scoping_<feature>.md`
- **Tool permissions:** Read (live app via browser/MCP), Write (`<feature_folder>/Feature_Scoping_*.md` only)
- **Prompt contract (summary):** Observe the feature end-to-end. Document what the feature does, what the user sees, what visual feedback the system provides, what the behavioural responses are. No code reading. No assumptions about intent — describe what was observed.
- **Real-time use against an existing system:** Where the feature is already configured (e.g. a Veeva Vault module a configurator has set up), the agent scopes from the live, configured instance. The framework does not generate features that don't yet exist — it scopes and validates features that do. This is not test-driven development.
### 6.2 Risk Assessment

- **Skill name:** `validation-risk-assessment`
- **Voice:** Quality risk lead applying GAMP 5 Risk-Based Approach
- **Inputs:** `Feature_Scoping_<feature>.md`
- **Outputs:** `<feature_folder>/Risk_Assessment_<feature>.md`
- **Tool permissions:** Read (Feature Scoping artifact only), Write (`<feature_folder>/Risk_Assessment_*.md` only)
- **Prompt contract (summary):** Apply the organisation's chosen risk framework (GAMP 5 RBA, FMEA, HACCP, or equivalent) to assess GxP impact, patient safety risk, data integrity risk. Determine the resulting risk classification and rationale that drives downstream scope decisions. The framework choice itself is configurable in the agent prompt; the orchestrator does not assume a specific methodology.

### 6.3 Validation Scope

- **Skill name:** `validation-scope`
- **Voice:** Validation lead deciding what to validate given the risk profile
- **Inputs:** `Feature_Scoping_<feature>.md`, `Risk_Assessment_<feature>.md`
- **Outputs:** `<feature_folder>/Validation_Scope_<feature>.md`
- **Tool permissions:** Read (Feature Scoping, Risk Assessment), Write (`<feature_folder>/Validation_Scope_*.md`)
- **Prompt contract (summary):** Define in-scope and out-of-scope items for the validation effort. Justify each scope decision against the risk assessment. Output should make explicit what will be tested and what will not, and why.
- **Why scope precedes URS/FRS:** In prospective validation under GxP, scope decisions are made before requirements are written. Writing URS/FRS for out-of-scope behaviour is wasted effort and obscures the validation surface. An agile-iterative approach where requirements drive scope is a different methodology, not addressed here.

### 6.4 URS — User Requirements Specification

- **Skill name:** `validation-urs-author`
- **Voice:** Business user / business analyst — user language ("The user shall be able to...")
- **Inputs:** `Feature_Scoping_<feature>.md`, `Validation_Scope_<feature>.md`
- **Outputs:** `<feature_folder>/URS_<feature>.md`
- **Tool permissions:** Read (Feature Scoping, Validation Scope), Write (`<feature_folder>/URS_*.md`)
- **Prompt contract (summary):** Write user requirements in user-facing language. Each requirement is testable, atomic, and traceable. Avoid implementation language.

### 6.5 FRS — Functional Requirements Specification

- **Skill name:** `validation-frs-author`
- **Voice:** Systems analyst — functional/systems language
- **Inputs:** `URS_<feature>.md`
- **Outputs:** `<feature_folder>/FRS_<feature>.md`
- **Tool permissions:** Read (URS), Write (`<feature_folder>/FRS_*.md`)
- **Prompt contract (summary):** Derive functional requirements from URS. Each FRS item traces to one or more URS items. Each FRS item carries explicit acceptance criteria — the testable conditions under which the requirement is considered met (Given/When/Then form, or measurable binary condition). Functional but not yet technical — describes what the system does, not how. The OQ Protocol phase derives test cases directly from these acceptance criteria.
- **Schema validator enforces:** every FRS item has ≥1 acceptance criterion; each AC has a unique ID; each AC follows a testable pattern. Deterministic check — no separate AC-author agent needed.
### 6.6 OQ Protocol

- **Skill name:** `validation-oq-protocol-author`
- **Voice:** QA tester designing executable test cases
- **Inputs:** `URS_<feature>.md`, `FRS_<feature>.md`
- **Outputs:** `<feature_folder>/OQ_Protocol_<feature>.md`
- **Tool permissions:** Read (URS, FRS), Write (`<feature_folder>/OQ_Protocol_*.md`)
- **Prompt contract (summary):** Author test cases. Each test case traces to one or more FRS acceptance criteria. Include preconditions, steps, expected results. Tests are executable by a human or by an automated tool.

### 6.7 OQ Execution

- **Skill name:** `validation-oq-execution`
- **Voice:** QA tester executing the protocol
- **Inputs:** `OQ_Protocol_<feature>.md`, the live application
- **Outputs:** `<feature_folder>/OQ_Execution_Record_<feature>.md`
- **Tool permissions:** Read (OQ Protocol, live app), Write (`<feature_folder>/OQ_Execution_Record_*.md`)
- **Prompt contract (summary):** Execute each test case from the protocol. Record actual results, pass/fail, deviations, evidence references.
- **Tool qualification — out of scope:** Test tool qualification (Playwright, or any equivalent automation tool used here) is out of scope for this framework. Production deployment would require formal tool qualification under GAMP 5 (typically Category 4 for configured automation frameworks). For demonstration purposes, this framework shows the agent-driven execution path; a real validated environment would either use a qualified automation tool or fall back to human execution with the agent only consuming the human-produced execution record.

### 6.8 Validation Summary Report

- **Skill name:** `validation-summary-report`
- **Voice:** Validation lead consolidating the package
- **Inputs:** All upstream artifacts in `<feature_folder>/` + relevant entries from `ai_assistance_log.jsonl`
- **Outputs:** `<feature_folder>/Validation_Summary_Report_<feature>.md`
- **Tool permissions:** Read (all artifacts in feature folder, audit log), Write (`<feature_folder>/Validation_Summary_Report_*.md`)
- **Prompt contract (summary):** Produce a consolidated summary referencing all upstream artifacts. Summarise risk classification, scope, requirements coverage, test execution results, AI involvement (from audit log). Conclude with a validation status statement.
- **Exception to directional isolation:** This agent has read access across the entire feature folder + the audit log. This is a deliberate exception (see ADR-001) — the summary cannot be produced without it.
- **Unit of audit:** The feature-level Validation Summary Report is the unit of audit for a single change. Where a release bundles multiple change requests, see §6.9 Release Summary.

### 6.9 Release Summary (Optional Higher-Order Skill)

The eight-phase chain produces one Validation Summary Report per feature. In real organisations, releases bundle multiple change requests and need a roll-up summary across them. The Release Summary skill operates one layer above the feature chain — it consolidates already-approved feature-level summaries without re-validating any feature.

- **Skill name:** `validation-release-summary`
- **Voice:** Validation lead consolidating a change request / release
- **Inputs:** A list of feature folders in scope for the release + `ai_assistance_log.jsonl`
- **Outputs:** `<release_folder>/Release_Validation_Summary_<change_request>.md`
- **Tool permissions:** Read (named feature folders, audit log), Write (`<release_folder>/Release_Validation_Summary_*.md`)
- **Prompt contract (summary):** Reference each per-feature `Validation_Summary_Report_*.md` in scope. Roll up overall risk profile, requirements coverage, deviations, AI involvement across the release. Does not re-validate features — it consolidates already-approved feature-level summaries. Conclude with a release-level validation status statement.
- **Relationship to feature chain:** This skill is invoked independently of the per-feature Orchestrator. It assumes every feature in scope has already been through the eight-phase chain and has an approved Validation Summary Report. This separation preserves the feature-level chain as the unit-of-change audit while adding the release-level rollup needed by release managers and Change Advisory Boards.

## 7. Orchestrator Specification

The Orchestrator is implemented as a top-level Claude Code skill: `/validate-feature <feature-name> [--resume]`.

### 7.1 V-Model Traversal

The Orchestrator walks the V-model. Feature Scoping, Risk Assessment, and Validation Scope are pre-V bounding activities. The chain then descends the specification arm (URS → FRS), jumps across to the OQ phases (OQ Protocol → OQ Execution), and climbs back to the Validation Summary Report.

```
   URS  ─────────────────────────────────  UAT (out of scope)
     ↘                                  ↗
      FRS  ────────────────────────  OQ Protocol → OQ Execution
        ↘                          ↗
         [DS deferred]  ─────  [IT out of scope]
                    ↘       ↗
                     [Build out of scope]
```

Each V-model phase is implemented as a specialist agent (see §6). The orchestrator state machine traverses them in order with a human approval gate after each transition. On `reject <reason>`, the current phase's agent is re-spawned with the rejection reason in context.

"Phase" language is retained internally as the field name in `state.json` and the JSONL log (it is the cleanest term for a state-machine step). The framing concept is V-model traversal; phases are the implementation detail.
### 7.2 Per-Phase Protocol

For each phase, the Orchestrator:

1. Reads `state.json` to determine the current phase and prior artifact paths
2. Spawns the specialist agent for the current phase as a subagent, passing only the paths of upstream artifacts it is allowed to read
3. Waits for the agent's `phase_complete(artifact_path, summary)` signal
4. Calls the Python validator for that phase: `python validators/<phase>.py <artifact_path>`
   - If validation fails, the Orchestrator returns the failure to the agent for correction (loop until pass or escalate to human)
5. Writes one line to `ai_assistance_log.jsonl` capturing the agent invocation
6. Surfaces the artifact + summary + schema result to the human via the gate
7. On `approve`: updates `state.json`, advances to next phase
8. On `reject <reason>`: re-spawns the same phase's agent with the rejection reason in context

### 7.3 `state.json` Schema (sketch — fields to finalise in build)

```json
{
  "feature_name": "add_client",
  "feature_folder": "03_Add_Client",
  "current_phase": 4,
  "phases": [
    {
      "phase": 1,
      "name": "Feature Scoping",
      "agent_skill": "validation-feature-scoping",
      "artifact_path": "03_Add_Client/Feature_Scoping_Add_Client.md",
      "schema_result": "pass",
      "human_approval": {
        "approved": true,
        "approver": "shyaamlal",
        "timestamp": "2026-05-17T09:42:00Z",
        "comment": null
      }
    }
  ],
  "started": "2026-05-17T09:00:00Z",
  "last_updated": "2026-05-17T09:42:00Z"
}
```

### 7.4 Operational Concerns

**Resume behaviour.** If the orchestrator is invoked with `--resume`, it reads `state.json` and continues from the last unapproved phase. State persists across sessions, so real validation cycles (which span days) work cleanly. The state file is itself part of the audit trail.

## 8. Artifact Handoff Contracts

### 8.1 Feature Folder Structure

Feature folders are sequence-prefixed at repo root:
```
01_Login/
02_Logout/
03_<next_feature>/
```

### 8.2 File Naming Convention

`<ArtifactType>_<FeatureName>.md` — for example `URS_Add_Client.md`, `OQ_Protocol_Add_Client.md`.

### 8.3 Handoff Mechanism

**File paths only, stateless specialists.** Each phase writes its artifact to disk. The Orchestrator passes the file path to the next specialist agent, which reads from disk. No in-context passing of artifact contents between agents.

Rationale: the on-disk artifact IS what the human approved at the gate. There is never ambiguity between "what the agent has" and "what the human signed off on." This also aligns with how real validation chains work — the DS author reads the controlled DS document, not an engineer's working memory.

## 9. AI Assistance Record Standard

Captured in two places, written simultaneously by the Orchestrator at each phase-complete handoff.

### 9.1 Per-Artifact Frontmatter (human-visible)

Every artifact begins with YAML frontmatter:

```yaml
---
artifact_type: URS
feature: Add_Client
version: 1.0
status: Approved
ai_assistance:
  agent_skill: validation-urs-author
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-17T10:14:00Z
  prompt_version: v1.2
human_review:
  reviewer: shyaamlal
  approval_timestamp: 2026-05-17T10:31:00Z
  comment: null
traceability:
  upstream:
    - Feature_Scoping_Add_Client.md
    - Validation_Scope_Add_Client.md
---
```

### 9.2 Central JSONL Audit Log (machine-queryable)

`ai_assistance_log.jsonl` at repo root. One line per agent invocation, append-only.

```json
{"timestamp":"2026-05-17T10:14:00Z","feature":"Add_Client","phase":4,"agent_skill":"validation-urs-author","model":"claude-opus-4-7","prompt_version":"v1.2","artifact_path":"03_Add_Client/URS_Add_Client.md","artifact_hash":"sha256:abc...","schema_result":"pass","human_reviewer":"shyaamlal","human_approval":"approved","human_approval_timestamp":"2026-05-17T10:31:00Z"}
```

The hash field anchors the audit record to the specific artifact content at approval time. If the artifact is later edited, a re-validation can detect the divergence.

### 9.3 Why Two Surfaces

- **Frontmatter** — self-describing to any human reader opening the artifact
- **JSONL log** — machine-queryable across the whole repo ("show me every artifact produced by model X" / "show me every approval by reviewer Y in date range Z")

A regulator's audit trail and a developer's inspection are two different queries; they are served by two surfaces from one source of truth.

## 10. Python Reliability Layer

Python is used only where it provides reliability gains a prompt cannot match.

**On Python qualification.** Python the language is GAMP 5 Category 1 (infrastructure / operating environment) and is not itself subject to tool qualification — it sits alongside the OS, file system, and Git. The custom validator code in `validators/` would be subject to GAMP 5 Category 5 custom application qualification in a production deployment. As with Playwright (§6.7), formal qualification is out of scope for this framework; the validators are presented as a reference implementation of the pattern.

### 10.1 Validators (`validators/<phase>.py`)

One per phase. Each validator:
- Opens the artifact file
- Validates required frontmatter fields present and non-empty
- Validates required content sections present and non-empty
- Regex-greps for forbidden placeholder patterns (`[Document what happened]`, `TODO`, `TBD`, `[If any.*describe]`, etc.)
- Validates content-specific rules (e.g. URS validator confirms each requirement has a unique ID; OQ Protocol validator confirms every test case traces to at least one requirement)
- Returns structured pass/fail + error list

These checks are deterministic and never miss. An LLM doing the same self-check is reliable most of the time, not all of the time. For a regulated framing, "most of the time" is the wrong reliability tier for a phase-complete gate.

### 10.2 Audit CLI (`tools/audit.py`)

A small CLI that queries `ai_assistance_log.jsonl`. Example invocations:

```bash
python tools/audit.py --feature Add_Client
python tools/audit.py --model claude-opus-4-7 --since 2026-05-01
python tools/audit.py --reviewer shyaamlal --phase 7
python tools/audit.py --artifact 03_Add_Client/URS_Add_Client.md
```

The CLI reads the on-disk JSONL only; structured filters over the append-only log are not something a prompt does deterministically.

### 10.3 What Is Out of Scope

Explicitly not built:
- A CLI wrapper for the Orchestrator (Claude Code is already the runtime — wrapping it is scaffolding, not engineering)
- FastAPI / web service around the audit log
- Pydantic models for every schema
- GitHub Actions CI

These would inflate the Python surface without strengthening the agentic story. Listed here so a reviewer understands they were considered and deliberately excluded.

## 11. Deferred Design Decisions

The following decisions are intentionally not resolved in this document. They are better resolved during build, when concrete implementation surfaces force the choice. Each is listed with its trigger and the constraints any resolution must satisfy.
### 11.1 Design Specification (DS) Phase — Deliberately Deferred

A Design Specification phase between FRS and OQ Protocol is sometimes included in IT GxP validation chains. It has been deliberately omitted here: in computerised systems validation, configurable systems (Veeva, SAP, custom) typically use Configuration Specifications or Technical Specifications rather than a separate DS, and the chain URS → FRS (with acceptance criteria) → OQ Protocol traces cleanly without it. To be reintroduced if a feature target requires it (e.g. bespoke design control under IEC 62304 / 21 CFR 820.30 for a SaMD context).

### 11.2 Exact JSONL Audit Log Schema

The shape sketched in §9.2 is illustrative. Final field set (e.g. whether full prompts are stored or only prompt versions, whether each schema validation result is logged separately from each agent invocation) to be resolved when the validator implementation forces the field list.

### 11.3 Validator Schema Format

Validators in §10.1 are described as Python modules. An alternative is YAML schema files consumed by a single generic validator. Decision depends on whether the per-phase rules turn out to be largely declarative (favour YAML) or genuinely procedural (favour Python modules). To resolve when the first two validators are written.

### 11.4 `state.json` Final Schema

The shape sketched in §7.3 covers the obvious fields. Final shape (including rejection history, retry counts, model parameter snapshots) to be resolved as the Orchestrator state machine is implemented.

### 11.5 Rejected-Artifact Retention Policy

When a reviewer rejects at a gate, the design says "loop back to same phase with rejection reason." Open: does the agent's prior artifact get deleted, archived, or kept as a versioned `.rejected` file? Does the audit log capture the rejected artifact as well as the eventually-approved one? Resolution affects the audit story and is best decided once the rejection flow is being implemented.

### 11.6 Prompt Versioning Discipline

Where prompts live is answered in §6 preamble: the skill file is the prompt, version-controlled in Git. Open:

1. **Baselining.** Is there a frozen `prompt_version` string in skill frontmatter that bumps on every prompt edit, or is the git SHA the authoritative version? Frontmatter-as-version is more human-readable; git SHA is more automatic.
2. **Proofing.** How is a prompt edit reviewed and approved before it goes live? Peer review by another validation engineer? A regression set of past artifacts re-generated under the new prompt to confirm consistent behaviour?
3. **Re-generation discipline.** Does an artifact produced under prompt v1.1 need to be regenerated under v1.2 for consistency, or does the audit log's record-of-version-used satisfy the trace?

These are governance questions deferred until there is evidence of how often prompts change in practice.

### 11.7 Feature Folder Sequence Numbering

Sequence-prefixed folders (`01_Login`, `02_Logout`, `03_Add_Client`) imply an order. Open: what order — chronological by validation start date, or by some other criterion? Trivial to resolve but worth being explicit about before the third feature folder is created.

### 11.8 Risk Assessment Output — GAMP 5 Category as Explicit Field?

The Risk Assessment phase will produce a GAMP 5 category (1-5) as part of its output. Open: is the category a structured field in the artifact frontmatter (machine-readable, queryable via the audit CLI) or only narrative text in the body? Structured is cleaner and supports downstream queries; narrative is faster to draft. To resolve when the Risk Assessment skill prompt is being written.

### 11.9 Summary Report Agent's Read Access to Audit Log

ADR-001 declares the Summary Report agent as an exception to directional isolation. Open: does that read access cover the entire `ai_assistance_log.jsonl`, or only entries scoped to the current feature? Scoping is more defensible (the summary describes one feature; it should not read entries unrelated to that feature) but adds a filtering step.

### 11.10 Risk Framework Selection

The Risk Assessment phase delegates the framework choice (GAMP 5 RBA, FMEA, HACCP, or equivalent) to the agent prompt. Open: should the framework choice surface as a structured configuration field (machine-readable, queryable, swap-per-feature) rather than a prompt-level variant? Worth revisiting once a second framework is used in practice.

### 11.11 Multi-Role Human Approval Workflow

Current design treats the human-in-the-loop as a single approver. In real validation chains, sign-off is role-based: tester writes, lead reviews, quality approves. Open: extend `state.json` and the gate protocol to support multi-role approval routing (e.g. `tester_signoff`, `lead_signoff`, `quality_signoff` per phase) — or keep the single-approver simplification and declare it as a known limitation. Production deployment would require the former. The orchestrator currently bridges this by surfacing the *role being represented* by the reviewer at each phase gate (see orchestrator skill, "Reviewer role per phase" table) — single approver, named role-hat.

### 11.12 Tool-Permission Enforcement at Skill Level

Directional isolation (ADR-001) is enforced three ways: (a) prompt — the skill body tells the agent "write only your file"; (b) orchestrator — the Orchestrator passes only allowed paths to each subagent; (c) post-invocation file-list check — the Orchestrator lists the feature folder after each agent invocation and flags unexpected writes. What is not currently enforced at the platform level: file-system path scoping on Read/Write tools at the skill `tools:` frontmatter level (the primitive does not exist in Claude Code today). The current three-way enforcement covers the common cases. The gap closes if Claude Code adds path-scoped tool permissions, at which point the post-invocation file-list check becomes belt-and-braces rather than the primary backstop.

### 11.13 Within-Phase Checkpointing

Resume behaviour (`--resume`) handles interruption *between* phases — the reviewer steps away, returns later, the chain picks up at the last unapproved phase. Resume does not handle interruption *within* a phase — if the reviewer stops mid-agent-execution, the agent's partial work is lost. For short phases (most artifact-only phases run in minutes) this is acceptable. For longer phases (notably oq-execution against a live system with many test cases) the loss is more painful. Open: should the specialist agents emit partial-progress signals during execution that the Orchestrator persists, enabling fine-grained resume? Best resolved once the live runs surface concrete data on phase durations.

### 11.14 Bug Lifecycle Integration

The framework captures bugs and anomalies surfaced during OQ Execution (§4 of the OQ Execution Record) and references their count in the Validation Summary Report (§6). Downstream of that — bug triage, assignment, fix, retest, and any re-validation of affected phases — is **out of scope for this framework**. In a regulated production deployment, bugs route to the organisation's defect-tracking system (JIRA, Azure DevOps, ALM defect modules, or equivalent) and follow that system's lifecycle. The framework's responsibility ends at *bug observed, recorded, and made traceable to the executed test case*.

Open: should the framework define an integration seam (e.g. a `bug_log.jsonl` mirroring `ai_assistance_log.jsonl`, or a per-bug markdown artifact under `<feature_folder>/bugs/`) so that mid-cycle re-validation can be audited? Worth revisiting after the first live execution surfaces bugs and the practical boundary between framework-internal and external-system-managed becomes clearer.

### 11.15 Framework Packaging — Demonstration Repo vs Reusable Plugin

The current repository is a demonstration *instance*: the framework (`.claude/skills/`, `validators/`, `tools/`) is portable, but it coexists with feature folders (`01_Login/`, `02_Logout/`), an application context file, and an audit log that are specific to the application under test. For a new application, the lightest pattern today is clone-and-customise (clone the repo, blank the feature folders and audit log, rewrite the application context). The framework files themselves carry no application coupling.

Open: should the framework be packaged separately — as a Claude Code plugin, a pip package, or an installable skill set — so new application repositories can pull it in cleanly? Plugin packaging gives clean framework / instance separation, version pinning, and a path to a marketplace listing. Trade-off is setup overhead (a second repo to maintain, plugin distribution, version migration). Best resolved once the framework has been run against at least one second application (Phase 5) and the actually-stable surface is known. Until then, the demonstration repo serves both purposes — the framework is *visibly* portable even if not yet *packaged* portable.

### 11.16 Feature Naming Convention

Across a team, the same feature may be referred to differently — `logout`, `log-out`, `sign-out`, `logout-process`. Without a convention, the framework gets duplicate feature folders, broken upstream traceability references between artifacts, and audit log entries that fragment across name variants. The single canonical name is also what binds change requests, JIRA tickets, validated scope, and final summary report into one auditable unit.

Open: define a canonical-name convention enforced at Step 0 of the Orchestrator. Likely shape: (a) feature names are lowercase, hyphen-separated slugs (`logout`, `add-client`, `voice-assessment-submission`); (b) the Orchestrator's Step 0 checks for existing feature folders and proposes the canonical name; (c) optional alias mapping (`log-out`, `sign-out` → `logout`) registered in `00_Project_Context/feature_aliases.json` so reviewers can refer to a feature by any internal name and resolve to the canonical one; (d) tie the canonical name to the upstream change request / ticket where possible so naming inherits an existing convention. Best resolved after Phase 5 surfaces real team-coordination friction in the dog-food runs.

---

## Appendix A — Relationship to the Existing `Methodology.md`

The existing `Methodology.md` in this folder documents the original retrospective ten-step methodology (Observe → Boundary → Investigate → Verify → DS → FRS → URS → OQ → Execute → Summary). This design supersedes that methodology in three ways:

1. **Code Investigation and Verification are dropped.** Both were retrospective-validation artefacts that confused the role being demonstrated.
2. **Risk Assessment is added.** Its absence in the original methodology was a credibility gap.
3. **Design Specification is deferred** (see §11.1). CSV chains for configurable systems typically substitute Configuration Specifications; the framework now goes URS → FRS (with acceptance criteria) → OQ Protocol.

`Methodology.md` will be updated to reference this document and deprecate the retrospective chain. To be handled in Phase 2 (Cleanup).

## Appendix B — Decision Log Reference

The 11 architectural decisions that produced this design were resolved in a structured Q&A session on 2026-05-16. The decision log lives in the project tracking folder (outside this repo) at `Oaths/AI-GxP-Framework/Session State.md`. This appendix is a stub reference, not a duplicate — the decisions themselves are embedded throughout sections 2-10 above.
