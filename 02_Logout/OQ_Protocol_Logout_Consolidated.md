---
artifact_type: OQ_Protocol_Consolidated
feature: Logout
version: 1.1
status: Draft
author: shyaamlal (validation lead, senior QA judgment applied)
relationship_to_canonical: |
  This is a parallel, validator-authored consolidation of `OQ_Protocol_Logout.md` (21 TCs).
  It is NOT a replacement; the framework's canonical 21-TC protocol remains in the v1.1 chain
  as the AI-generated artifact of Phase 6. This consolidation demonstrates how a senior
  validation lead right-sizes OQ coverage for a moderate-risk feature: fewer, broader test
  passes; functional assertions only; backend and security assertions referenced to other
  validation streams.
relationship_to_canonical_coverage: |
  - 14 of 21 ACs covered as direct OQ test cases (TC-A and TC-B)
  - 3 of 21 ACs scope-revised to integration/security testing (referenced, not re-validated in OQ)
  - 3 of 21 ACs blocked (audit-DB inputs pending)
  - 1 of 21 ACs split: functional part covered in OQ; performance part referenced to SLO
traceability:
  upstream:
    - OQ_Protocol_Logout.md
    - FRS_Logout.md
    - Risk_Assessment_Logout.md
---

# OQ Protocol — Logout (Senior QA Consolidation, v1.1)

## Purpose

The canonical `OQ_Protocol_Logout.md` decomposes 21 ACs into 21 test cases on a 1:1 basis. This consolidation re-organises that coverage by senior validation judgment:

1. **Group functional ACs** that share an execution scenario into single test passes.
2. **Split assertions** that mix functional and non-functional concerns (e.g. "redirect happens AND within 5 seconds" → functional verified in OQ, performance/SLO referenced separately).
3. **Re-categorise integration/security assertions** that the canonical protocol mis-scoped as OQ — these belong in security review / integration test suites and are referenced as supporting evidence, not re-verified per feature.

The result is two browser-based test passes (TC-A, TC-B) covering 14 ACs directly, with the remaining 7 ACs honestly categorised: 3 referenced to integration/security scope, 3 blocked pending audit-DB inputs, 1 split between OQ (functional) and SLO (performance).

This applies the discipline that **Risk Assessment §6 already articulated** — "security / penetration / integration evidence: reference, do not produce within this chain" — which the canonical Validation Scope §2.6 did not honor.

## Consolidation Rationale

Logout is a security-critical access-control feature, but it is **not** life-supporting or directly clinical. Per `Risk_Assessment_Logout.md` §3, patient-safety severity is bounded by intended use and confirmed at validation-lead approval as Low (non-clinical employability assessment platform). Risk-proportional OQ does not exhaustively re-verify backend and security behaviour at the feature level; that behaviour is verified once at the system/security level and referenced from feature OQs as supporting evidence.

## Test Cases

### TC-A: Sign-Out Functional Path and Post-Logout Access Enforcement

**Scope:** User-facing functional verification of sign-out activation, post-logout UI state, route-guard enforcement, refresh / new-tab / history navigation behaviour. Binary functional assertions only.

**Trace (functional):** AC-FRS-001.1, AC-FRS-001.2, AC-FRS-001.3, AC-FRS-002.1 (functional part), AC-FRS-002.2, AC-FRS-003.1, AC-FRS-003.2, AC-FRS-004.1, AC-FRS-004.2, AC-FRS-005.1, AC-FRS-005.2, AC-FRS-007.1, AC-FRS-007.2 (13 ACs, functional content).

**Preconditions:**
- Client test account signed in
- At least one prior analysis record visible on `/voice/history`

**Steps:**

1. **Route discovery (AC-FRS-001.3).** Sign in. Navigate to each in-scope authenticated route: `/dashboard`, `/voice/record`, `/voice/history`, `/users`, `/usage`, `/sop`, `/change-password`, one `/voice/report/<id>`. On each route, confirm the workspace navigation is rendered and the user menu contains the "Sign out" control. Record yes/no per route.
2. **Sign-out control presence and activation (AC-FRS-001.1, .001.2).** Return to `/dashboard`. Open the user menu. Confirm "Sign out" is present exactly once and rendered as an activatable button. Click "Sign out" once. Confirm no confirmation dialog appears.
3. **Sign-out redirects to sign-in page (AC-FRS-002.1, functional part).** Observe the active tab transition. Verify the URL settles on `/login` and the sign-in form is rendered. (Note: performance assertion "within 5 seconds" is NOT part of OQ scope — see Note 1 below.)
4. **Post-logout UI state (AC-FRS-002.2, .003.1, .003.2).** On the post-sign-out page, inspect the DOM. Verify: no workspace navigation present (search for labels: Dashboard, New Analysis, Analysis History, Users, Usage & Limits, Recording Guide — all zero matches); no user identity area present (search for `testclient@sambhava.test`, `Test Client 1`, "TC" avatar — all zero matches).
5. **Direct-navigation route guard (AC-FRS-004.1, .004.2).** From the sign-in page, manually enter each protected URL in turn: `/dashboard`, `/voice/history`, `/voice/record`, `/users`, `/usage`, one `/voice/report/<id>`. Verify each redirects to `/login` AND that protected content (history table headers, dashboard widgets, subject names) does not appear.
6. **Refresh, new-tab, browser history (AC-FRS-005.1, .005.2, .007.1, .007.2).** From the sign-in page: refresh the tab — confirm sign-in page renders. Open a new tab in the same browser context, navigate to `/dashboard` — confirm sign-in page renders. Activate browser back button three times — each lands on sign-in page. Activate forward button three times — each lands on sign-in page.

**Pass criteria (binary, functional only):**
- Step 1: every in-scope route returns yes for both menu and Sign-Out reachability (if any returns no, surface as re-scope question per URS Q1)
- Step 2: control present once AND no confirmation dialog
- Step 3: final URL is `/login` AND sign-in form is rendered
- Step 4: zero matches for each searched workspace-nav label AND each user-identity marker
- Step 5: every URL redirects to sign-in AND zero matches for protected-content markers
- Step 6: refresh, new-tab, back×3, forward×3 — each lands on sign-in page

**Evidence to capture:**
- One screenshot per step
- Route discovery table from Step 1, recorded in execution log

---

### TC-B: User-Facing Cross-Tab Behaviour

**Scope:** Browser-observable cross-tab behaviour following sign-out — passive observation and next-action redirect. Functional UI verification only.

**Trace:** AC-FRS-006.1, AC-FRS-006.2 (functional part) (2 ACs, functional content).

**Preconditions:**
- Two-tab browser session, both authenticated as the Client test account
- Tab A on `/dashboard`; Tab B on `/voice/history` with analyses table fully rendered

**Steps:**

1. **Passive observation post-sign-out-elsewhere (AC-FRS-006.1).** In Tab A, click "Sign out". Tab A redirects to `/login`. Switch to Tab B, do nothing for 30 seconds. Verify Tab B's URL remains `/voice/history` AND the analyses table remains visible.
2. **Next-action redirect from stale tab (AC-FRS-006.2, functional part).** In Tab B, click the "Dashboard" link in the left sidebar. Observe the redirect. Verify Tab B's URL settles on `/login` and the sign-in form is rendered. (Note: performance assertion "within 5 seconds" is NOT part of OQ scope — see Note 1.)

**Pass criteria (binary, functional only):**
- Step 1: Tab B URL unchanged AND analyses table visible after 30 seconds
- Step 2: Tab B redirects to `/login` AND sign-in form rendered

**Evidence to capture:**
- Screenshot at Step 1 (Tab B stale state)
- Screenshot at Step 2 (Tab B post-redirect)

---

## Scope-Revised — Referenced, not Tested in OQ

The following ACs were initially scoped as OQ test cases in `OQ_Protocol_Logout.md` but are re-categorised here per senior validation judgment as integration/security concerns, not feature-level OQ:

| AC | Originally in OQ as | Re-categorised to | Reference for evidence |
|---|---|---|---|
| AC-FRS-006.3 — Authenticated action from stale tab does not succeed | TC-014 (Network panel inspection) | Integration / system test | Platform integration test suite covering session-state propagation across browser tabs |
| AC-FRS-008.1 — Captured session cookie returns unauthenticated response after sign-out | TC-017 (cookie capture + replay via curl) | Security review / penetration testing | Platform security review covering server-side session revocation (one-time architectural verification, referenced not re-validated per feature) |
| AC-FRS-008.2 — Replayed session-cookie response contains no workspace data | TC-018 (same as TC-017, different endpoint) | Security review / penetration testing | Same as AC-FRS-008.1 |

**Rationale:** OQ verifies user-facing functional behaviour. Backend assertions (HTTP status on cookie replay, server-side response shape to integration-level requests) are properly covered by:
- The application's existing security review or penetration test (referenced as evidence in the validation package)
- The development team's integration / system test suite (run continuously, referenced via test-suite IDs)

Risk Assessment §6 already articulated this disposition ("recommended as evidence to reference rather than to produce within this chain"). The canonical Validation Scope §2.6 did not honor that disposition; this consolidation corrects it.

**Disposition for the validation package:** the Validation Summary Report (Phase 8) will reference these ACs as covered-by-external-evidence, not as OQ-verified. If platform security review or integration test evidence is not available, this becomes a documented gap — but not one closed by adding more OQ test cases.

---

## Blocked — Audit-DB Inputs Pending

The following ACs are blocked pending audit-database access parameters:

| AC | TC | Reason |
|---|---|---|
| AC-FRS-009.1 — Audit record for sign-out event exists in database | TC-019 | Audit table name, user-id column, event-time column, event-type literal not supplied at execution start |
| AC-FRS-009.2 — Audit record carries user identifier and timestamp ≤ ±30 seconds | TC-020 | Depends on TC-019 |
| AC-FRS-009.3 — No spurious sign-out audit record in control window | TC-021 | Depends on audit DB access |

**Disposition:** record as Blocked in the Execution Record. Carry forward as a known gap to the Validation Summary Report. The validation lead commits to coordinating audit-database access with the platform owner before any production deployment of this validation outcome.

---

## Coverage Mapping (Full)

| Canonical AC | Disposition | Where covered / evidence |
|---|---|---|
| AC-FRS-001.1 | OQ — TC-A Step 2 | This run |
| AC-FRS-001.2 | OQ — TC-A Step 2 | This run |
| AC-FRS-001.3 | OQ — TC-A Step 1 | This run |
| AC-FRS-002.1 (functional) | OQ — TC-A Step 3 | This run |
| AC-FRS-002.1 (≤5s timing) | Performance / SLO | Referenced to platform SLO doc (if any); not OQ |
| AC-FRS-002.2 | OQ — TC-A Step 4 | This run |
| AC-FRS-003.1 | OQ — TC-A Step 4 | This run |
| AC-FRS-003.2 | OQ — TC-A Step 4 | This run |
| AC-FRS-004.1 | OQ — TC-A Step 5 | This run |
| AC-FRS-004.2 | OQ — TC-A Step 5 | This run |
| AC-FRS-005.1 | OQ — TC-A Step 6 | This run |
| AC-FRS-005.2 | OQ — TC-A Step 6 | This run |
| AC-FRS-006.1 | OQ — TC-B Step 1 | This run |
| AC-FRS-006.2 (functional) | OQ — TC-B Step 2 | This run |
| AC-FRS-006.2 (≤5s timing) | Performance / SLO | Referenced to platform SLO doc (if any); not OQ |
| AC-FRS-006.3 | Integration test | Reference to platform integration test suite |
| AC-FRS-007.1 | OQ — TC-A Step 6 | This run |
| AC-FRS-007.2 | OQ — TC-A Step 6 | This run |
| AC-FRS-008.1 | Security review | Reference to platform security review |
| AC-FRS-008.2 | Security review | Reference to platform security review |
| AC-FRS-009.1 | OQ — Blocked | Pending audit-DB inputs |
| AC-FRS-009.2 | OQ — Blocked | Pending audit-DB inputs |
| AC-FRS-009.3 | OQ — Blocked | Pending audit-DB inputs |

**Summary:** 14 ACs OQ-tested in this run; 2 timing assertions split to SLO scope; 3 ACs referenced to security/integration evidence; 3 ACs blocked. All 21 ACs accounted for; none silently dropped.

---

## Notes

1. **Performance assertions are out of OQ scope.** The canonical OQ Protocol's "≤ 5 seconds" assertions (AC-FRS-002.1 step 3, AC-FRS-006.2 step 5) mixed functional and non-functional concerns. OQ verifies functional behaviour (did the redirect occur?). Performance/timing is a separate concern verified against a platform SLO (if one exists) or by a continuous monitoring system. Source of the 5-second value traces to a suggested approval comment at the Phase 5 gate — illustrating the "hallucination cascade through approval comments" finding logged in the post-run observations.

2. **Integration and security tests are out of OQ scope.** AC-FRS-006.3, AC-FRS-008.1, AC-FRS-008.2 require backend-level assertions (Network panel inspection, captured-cookie replay via curl). These are integration/security tests, properly covered by separate validation streams that the OQ references as supporting evidence. Risk Assessment §6 said this; Validation Scope §2.6 over-scoped; this consolidation restores the correct disposition.

3. **Coverage and re-scope are not the same thing.** Re-categorising an AC from "OQ-tested" to "referenced to integration/security testing" does NOT reduce its coverage — it relocates the verification to the appropriate validation stream. If that stream has no evidence to reference, the validation package documents the gap explicitly.

4. **Authorship.** This consolidation is authored by the validation lead, not generated by the framework. It demonstrates the intended HITL model: AI accelerates structure (canonical OQ Protocol with 21 TCs from Phase 6); validator owns scope, decomposition, and proportionality (this consolidation). Both artefacts are retained in the repository.
