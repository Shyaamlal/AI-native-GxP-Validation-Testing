---
artifact_type: OQ_Execution_Record
feature: Logout
version: 1.0
status: Approved
ai_assistance:
  agent_skill: validation-oq-execution
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-18T21:33:00Z
  prompt_version: v1.0
human_review:
  reviewer: shyaamlal
  approval_timestamp: 2026-05-18T21:49:41Z
  comment: "Approved. Execution record accurately reflects the run. Four open questions carry forward to Phase 8 as inputs to validation_status determination: (1) external evidence for relocated ACs 006.3/008.1/008.2 — likely not available for this dog-food, gap to be documented in Summary; (2) platform SLO documentation for timing thresholds 002.1/006.2 — not formalised for the platform, gap to be documented; (3) audit-DB access for TC-019/020/021 — committed as pre-deployment coordination item; (4) Phase 3 over-scoping — carried as framework-improvement item, not a Logout defect. Expected Phase 8 outcome: Conditional Pass — functional behaviour verified (15 PASS, 0 FAIL); gaps in external evidence, SLO docs, and audit-DB access conditions. The Logout feature itself shows no defects; conditional disposition reflects gaps in the surrounding validation package, not in the feature."
traceability:
  upstream:
    - OQ_Protocol_Logout.md
execution_context:
  mode: human-record-consumed
  executor: shyaamlal
  environment_url: https://test-env.example
  execution_start: 2026-05-18T20:50:00Z
  execution_end: 2026-05-18T21:30:00Z
---

# OQ Execution Record — Logout

## 1. Execution Summary

- **Total cases:** 21
- **Passed:** 15 — TC-001, TC-002, TC-003, TC-004 (functional component only — see §3), TC-005, TC-006, TC-007, TC-008, TC-009, TC-010, TC-011, TC-012, TC-013 (functional component only — see §3), TC-015, TC-016
- **Failed:** 0
- **Scope-Revised (not executed in OQ; coverage relocated):** 3 — TC-014, TC-017, TC-018
- **Blocked:** 3 — TC-019, TC-020, TC-021

The execution was conducted in human-record-consumed mode against the live system at `https://test-env.example` by the executor `shyaamlal`. The execution was performed following a senior-QA-consolidated parallel protocol (`OQ_Protocol_Logout_Consolidated.md` v1.1) which re-organised the canonical 21 test cases into two consolidated functional cases (TC-A, TC-B). This record maps results back to the canonical 21 TC IDs from the approved `OQ_Protocol_Logout.md` v1.0 for traceability; the consolidation is recorded as a deviation in §3.

## 2. Test Case Results

### TC-001: Sign-Out control is visible in the user menu
- **Trace:** AC-FRS-001.1
- **Steps executed:** Protocol steps 1-3 executed as written, within Consolidated TC-A Step 2.
- **Actual result:** Sign-out control present exactly once in the user menu, rendered as an activatable button.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 2 evidence (Consolidated Protocol §TC-A).
- **Deviations:** None for this test case specifically; the overall consolidation deviation is recorded in §3.

### TC-002: Sign-Out activates on a single click with no confirmation dialog
- **Trace:** AC-FRS-001.2
- **Steps executed:** Protocol steps 1-2 executed as written, within Consolidated TC-A Step 2.
- **Actual result:** A single click on Sign-Out initiated the sign-out transition immediately; no confirmation dialog, modal, or secondary prompt was rendered.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 2.
- **Deviations:** None.

### TC-003: User menu and Sign-Out control reachable from every in-scope authenticated route (discovery)
- **Trace:** AC-FRS-001.3
- **Steps executed:** Protocol steps 1-4 executed for all eight in-scope routes within Consolidated TC-A Step 1.
- **Actual result:** Workspace navigation present and Sign-Out reachable in the user menu on every in-scope route. Per-route observation:
  - `/dashboard`: menu yes / Sign-Out yes
  - `/voice/record`: menu yes / Sign-Out yes
  - `/voice/history`: menu yes / Sign-Out yes
  - `/users`: menu yes / Sign-Out yes
  - `/usage`: menu yes / Sign-Out yes
  - `/sop`: menu yes / Sign-Out yes
  - `/change-password`: menu yes / Sign-Out yes
  - `/voice/report/<id>`: menu yes / Sign-Out yes
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 1.
- **Deviations:** None. URS Q1 deferred discovery is satisfied at execution time; no re-scope required.

### TC-004: Active tab redirects to sign-in page within 5 seconds
- **Trace:** AC-FRS-002.1
- **Steps executed:** Protocol step 1, 3, 4 executed as written. Protocol step 2 (start stopwatch / note t0) and the elapsed-time portion of step 4 were not executed — see Deviations.
- **Actual result:** The active tab's URL changed to `https://test-env.example/login` and the sign-in form was rendered. Functional assertion satisfied. Timing component not asserted in this OQ execution.
- **Pass / Fail / Blocked:** Pass (functional component only). The timing assertion ("≤ 5 seconds") is recorded as scope-revised — see §3.
- **Evidence:** Covered by Consolidated TC-A Step 3.
- **Deviations:** Timing assertion not executed in OQ. The senior validation lead re-categorised the "within 5 seconds" portion as performance/SLO scope, out of OQ scope for this run. See §3 and §5 Open Question 2.

### TC-005: No authenticated identity displayed after sign-out
- **Trace:** AC-FRS-002.2
- **Steps executed:** Protocol steps 1-2 executed as written, within Consolidated TC-A Step 4.
- **Actual result:** No authenticated identifier visible on the post-sign-out page. Searched identifier match counts (each expected 0): `testclient@platform.test` = 0; `Test Client 1` = 0; "TC" avatar = 0.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 4.
- **Deviations:** None.

### TC-006: Workspace navigation absent from DOM after sign-out
- **Trace:** AC-FRS-003.1
- **Steps executed:** Protocol steps 1-2 executed as written, within Consolidated TC-A Step 4.
- **Actual result:** Workspace navigation absent from the rendered post-sign-out page. DOM-search match counts (each expected 0): Dashboard = 0; New Analysis = 0; Analysis History = 0; Users = 0; Usage & Limits = 0; Recording Guide = 0.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 4.
- **Deviations:** Verification performed by visual inspection (sidebar absent) rather than explicit DOM inspector search. Outcome unchanged.

### TC-007: User identity area absent from DOM after sign-out
- **Trace:** AC-FRS-003.2
- **Steps executed:** Protocol steps 1-2 executed as written, within Consolidated TC-A Step 4.
- **Actual result:** User identity area absent. DOM-search match counts (each expected 0): "TC" avatar = 0; "Test Client 1" = 0; `testclient@platform.test` = 0.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 4.
- **Deviations:** Verification performed by visual inspection. Outcome unchanged.

### TC-008: Direct navigation to protected routes while signed out redirects to sign-in
- **Trace:** AC-FRS-004.1
- **Steps executed:** Protocol steps 1-4 executed for all six in-scope routes, within Consolidated TC-A Step 5.
- **Actual result:** Every directly-entered protected URL redirected to the sign-in URL. Per-route (final URL is sign-in URL? yes/no): `/dashboard` = yes; `/voice/history` = yes; `/voice/record` = yes; `/users` = yes; `/usage` = yes; `/voice/report/<id>` = yes.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 5.
- **Deviations:** None.

### TC-009: No protected content visible during direct-navigation redirect
- **Trace:** AC-FRS-004.2
- **Steps executed:** Protocol steps 2-4 executed as written, within Consolidated TC-A Step 5. Protocol step 1 (DevTools Performance recording) not performed — see Deviations.
- **Actual result:** No protected content visible in any rendered output during redirect. Marker-search match counts (each expected 0): analysis-history table headers = 0; dashboard widget labels ("Good afternoon", "My Users", "Analyses") = 0; subject names = 0.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 5.
- **Deviations:** Frame-by-frame Performance recording not performed; verification by visual inspection during the redirect transitions. The user-visible outcome (no flash of protected content) was confirmed; the more rigorous frame-capture check is recorded as a deviation in §3.

### TC-010: Refresh/forward after sign-out does not restore prior workspace page
- **Trace:** AC-FRS-005.1
- **Steps executed:** Protocol steps 1-3 executed as written, within Consolidated TC-A Step 6.
- **Actual result:** All three actions land on the sign-in page. Outcomes: refresh = `/login`; forward = `/login`; manual URL re-entry = `/login`.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 6.
- **Deviations:** None.

### TC-011: A new tab opened after sign-out cannot reach protected content
- **Trace:** AC-FRS-005.2
- **Steps executed:** Protocol steps 1-4 executed as written, within Consolidated TC-A Step 6.
- **Actual result:** New tab redirected to the sign-in page for every protected route exercised. Per-route: `/dashboard` = `/login`; `/voice/history` = `/login`.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 6.
- **Deviations:** None.

### TC-012: Stale tab retains rendered content after sign-out elsewhere (no proactive redirect)
- **Trace:** AC-FRS-006.1
- **Steps executed:** Protocol steps 1-3 executed as written, within Consolidated TC-B Step 1.
- **Actual result:** Tab B retained its rendered `/voice/history` view, including the analyses table, throughout the 30-second observation window. URL at end of window: `https://test-env.example/voice/history`. Analyses table still visible: yes.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-B Step 1.
- **Deviations:** None.

### TC-013: Stale tab redirects within 5 seconds of next user-initiated navigation
- **Trace:** AC-FRS-006.2
- **Steps executed:** Protocol step 2 executed as written, within Consolidated TC-B Step 2. Protocol step 1 (note t0) and the elapsed-time portion of step 3 were not formally measured — see Deviations.
- **Actual result:** Stale Tab B redirected to `/login` on next navigation (sidebar Dashboard click) and rendered the sign-in form. Functional assertion satisfied. Elapsed time was observed informally to be approximately 2 seconds; not formally measured.
- **Pass / Fail / Blocked:** Pass (functional component only). The timing assertion ("≤ 5 seconds") is recorded as scope-revised — see §3.
- **Evidence:** Covered by Consolidated TC-B Step 2.
- **Deviations:** Timing assertion not formally measured in OQ. The senior validation lead re-categorised the "within 5 seconds" portion as performance/SLO scope, out of OQ scope for this run. See §3 and §5 Open Question 2.

### TC-014: Authenticated action issued from a stale tab does not succeed
- **Trace:** AC-FRS-006.3
- **Steps executed:** Not executed.
- **Actual result:** Test case re-categorised by senior validation judgment from OQ scope to integration-testing scope before execution. Backend response inspection (DevTools Network panel for HTTP response shape from a stale-tab authenticated request) was assessed as integration-test territory rather than feature-level OQ. Coverage of AC-FRS-006.3 is therefore referenced from the platform's integration test suite, not produced within this OQ.
- **Pass / Fail / Blocked:** Scope-Revised (not executed in OQ; coverage relocated to integration-testing scope). For execution-summary tallying, this row is counted in the "Scope-Revised" category, not "Blocked" and not "Pass" or "Fail".
- **Evidence:** No OQ-internal evidence. Reference: platform integration test suite (artefacts external to this validation chain; see §5 Open Question 1).
- **Deviations:** Test case removed from OQ execution mid-protocol per senior validation judgment. This is a substantive deviation from the approved Phase 6 OQ Protocol and is recorded as such in §3. The framework-level finding behind the deviation is recorded in §5 Open Question 4.

### TC-015: Browser back navigation after sign-out lands on the sign-in page
- **Trace:** AC-FRS-007.1
- **Steps executed:** Protocol steps 1-3 executed as written, within Consolidated TC-A Step 6.
- **Actual result:** All three back actions land on the sign-in page. Final URL after each: 1 = `/login`; 2 = `/login`; 3 = `/login`.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 6.
- **Deviations:** None.

### TC-016: Browser forward navigation after back lands on the sign-in page
- **Trace:** AC-FRS-007.2
- **Steps executed:** Protocol steps 1-3 executed as written, within Consolidated TC-A Step 6.
- **Actual result:** All three forward actions land on the sign-in page. Final URL after each: 1 = `/login`; 2 = `/login`; 3 = `/login`.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** Covered by Consolidated TC-A Step 6.
- **Deviations:** None.

### TC-017: A captured session cookie returns an unauthenticated response after sign-out
- **Trace:** AC-FRS-008.1
- **Steps executed:** Not executed.
- **Actual result:** Test case re-categorised by senior validation judgment from OQ scope to security-review / penetration-testing scope before execution. Captured-cookie replay against backend endpoints was assessed as a one-time architectural security verification, properly referenced from feature OQs as supporting evidence rather than re-validated per feature. Coverage of AC-FRS-008.1 is therefore referenced from the platform's security review / penetration test, not produced within this OQ.
- **Pass / Fail / Blocked:** Scope-Revised (not executed in OQ; coverage relocated to security-review scope).
- **Evidence:** No OQ-internal evidence. Reference: platform security review / penetration test (artefacts external to this validation chain; see §5 Open Question 1).
- **Deviations:** Test case removed from OQ execution mid-protocol per senior validation judgment. Recorded in §3. Framework finding in §5 Open Question 4.

### TC-018: Replayed session-cookie response contains no workspace data
- **Trace:** AC-FRS-008.2
- **Steps executed:** Not executed.
- **Actual result:** Test case re-categorised by senior validation judgment from OQ scope to security-review scope, together with TC-017 (same AC family).
- **Pass / Fail / Blocked:** Scope-Revised (not executed in OQ; coverage relocated to security-review scope).
- **Evidence:** No OQ-internal evidence. Reference: platform security review (external).
- **Deviations:** Same as TC-017. Recorded in §3.

### TC-019: Audit record for sign-out event exists in the database
- **Trace:** AC-FRS-009.1
- **Steps executed:** Not executed.
- **Actual result:** Blocked. Audit DB query parameters (audit table or view name, user-identifier column, event-time column, event-type literal denoting sign-out, and DB connection access) were not supplied at execution start. The OQ Protocol §2 Audit-log access prerequisite was not satisfied, per the QA gate decision recorded at Phase 6 approval.
- **Pass / Fail / Blocked:** Blocked
- **Evidence:** n/a
- **Deviations:** Blocked — protocol prerequisite not satisfied. The validation lead has committed to coordinating audit-database access with the platform owner before any production deployment of this validation outcome.

### TC-020: Sign-out audit record carries user identifier and timestamp within ±30 seconds of T_test
- **Trace:** AC-FRS-009.2
- **Steps executed:** Not executed.
- **Actual result:** Blocked. Depends on TC-019, which is Blocked.
- **Pass / Fail / Blocked:** Blocked
- **Evidence:** n/a
- **Deviations:** Same as TC-019.

### TC-021: No spurious sign-out audit record exists when no sign-out has been performed
- **Trace:** AC-FRS-009.3
- **Steps executed:** Not executed.
- **Actual result:** Blocked. Depends on audit-DB access prerequisite (TC-019).
- **Pass / Fail / Blocked:** Blocked
- **Evidence:** n/a
- **Deviations:** Same as TC-019.

## 3. Deviations Summary

This execution involved four classes of deviation from the approved Phase 6 OQ Protocol. All deviations are recorded transparently; none were silently corrected. The validation lead's judgment in approving each deviation is captured at this gate (Phase 7 reviewer approval).

**D1. Consolidated parallel protocol used at execution time.** The execution followed a senior-QA-consolidated parallel protocol artefact, `OQ_Protocol_Logout_Consolidated.md` v1.1, which re-organised the canonical 21 test cases into two consolidated functional cases (TC-A, TC-B). This artefact was authored by the validation lead during execution preparation and was not the artefact approved at the Phase 6 gate. The framework's directional-isolation contract expects a single artifact per phase; the presence of the consolidated artefact in `02_Logout/` is a file-list-check deviation from the orchestrator's strict contract. The deviation was transparent (the consolidated artefact was named, versioned, and committed alongside the canonical artefact rather than substituted for it) and the results recorded in this execution record map 1:1 back to the canonical TC IDs.

**D2. Timing assertions not executed (TC-004, TC-013).** The "within 5 seconds" timing portions of TC-004 and TC-013 were not asserted during execution. The senior validation lead re-categorised these as performance / service-level expectations, out of OQ scope for this run. The functional components of both test cases were executed and passed; the timing components remain unverified within this validation chain. AC-FRS-002.1 and AC-FRS-006.2 carry a partial-coverage caveat into the Validation Summary Report.

**D3. Three test cases relocated to external coverage scopes (TC-014, TC-017, TC-018).** TC-014 (stale-tab authenticated action) was relocated to integration-testing scope. TC-017 (captured-cookie replay) and TC-018 (replayed-cookie response) were relocated to security-review / penetration-testing scope. The senior validation lead judged that AC-FRS-006.3, AC-FRS-008.1, and AC-FRS-008.2 are better verified once at an architectural / security-review level and referenced from feature OQs, rather than re-validated per feature. The original Risk Assessment artefact §6 already specified the latter two ACs as "evidence to reference rather than to produce within this chain"; the Validation Scope artefact §2.6 over-scoped them into the OQ. The relocation aligns the executed scope with the Risk Assessment's intent. Coverage of the three ACs within this validation chain therefore depends on external evidence (see §5 Open Question 1).

**D4. Verification methodology lighter than protocol for TC-006, TC-007, TC-009.** Verification was performed by visual inspection of the rendered page rather than by explicit DOM inspector search (TC-006, TC-007) or DevTools Performance frame capture (TC-009). The user-visible outcomes were confirmed and the test cases passed; the more rigorous capture-and-search method specified in the protocol was not exercised. Recorded as a deviation; outcomes unchanged.

## 4. Bugs / Anomalies Surfaced

No defects in the Logout feature were surfaced during this execution. The feature behaved as specified by the URS and FRS across every test case that was executed.

One framework-level anomaly was surfaced and is recorded in §5 (Open Question 4): the Validation Scope phase did not honour the Risk Assessment's "reference, do not produce within this chain" disposition for security and integration concerns, leading to TC-014, TC-017, TC-018 being authored at OQ depth and subsequently relocated by the senior validation lead. This is a finding about the framework's Phase 3 (Validation Scope) skill behaviour, not a defect in the Logout feature itself.

## 5. Open Questions for the Human

1. **External evidence for scope-revised ACs.** TC-014 (AC-FRS-006.3), TC-017 (AC-FRS-008.1), and TC-018 (AC-FRS-008.2) were relocated to integration-testing and security-review scopes. Does referenceable evidence exist for these ACs in the platform's integration test suite and security review / penetration test? If yes, the Validation Summary Report must cite the specific evidence artefacts. If no, the Validation Summary must record an explicit coverage gap for these three ACs and the validation lead must decide how to close it (commission the missing evidence, accept the gap with documented residual-risk justification, or re-introduce the tests into the OQ).

2. **Platform SLO documentation for timing assertions.** AC-FRS-002.1 and AC-FRS-006.2 carried a 5-second threshold approved at Phase 5. The timing components were not asserted (D2). Does a documented platform service-level expectation exist that would cover these thresholds? If yes, the Validation Summary references it. If no, the validation lead must decide whether the timing thresholds remain undocumented obligations or are dropped as out-of-scope expectations.

3. **Audit-database access for TC-019/020/021 closure.** TC-019, TC-020, TC-021 are Blocked pending audit DB access parameters (table name, columns, event-type literal, connection access). The validation lead has committed to coordinating this access with the platform owner before any production deployment of this validation outcome. The Validation Summary Report must record the gap and the close-out commitment.

4. **Framework finding — Validation Scope over-scoping of "reference-only" Risk Assessment items.** The Risk Assessment artefact §6 specified AC-FRS-008.1 and AC-FRS-008.2 (and arguably AC-FRS-006.3) as "evidence to reference rather than to produce within this chain". The Validation Scope artefact §2.6 nonetheless included them as OQ-depth in-scope items, which propagated through URS, FRS, and OQ Protocol, until the senior validation lead reverted the decision at execution time. The framework's `validation-scope` skill prompt does not currently instruct the agent to honour Risk Assessment's `validation_depth` or "reference vs produce" disposition explicitly; this should be fixed in the framework's Phase 3 skill prompt. Logged for post-run framework tuning, separate from the Logout feature validation outcome.

## 6. Notes

- This execution record is mapped 1:1 against the canonical 21 test cases from `OQ_Protocol_Logout.md` v1.0 (Phase 6 approved artefact). The senior-QA `OQ_Protocol_Logout_Consolidated.md` v1.1 served as the operational execution guide; mapping back to the canonical artefact preserves traceability through URS and FRS to the original ACs.
- Pass/Fail tally in §1 treats Scope-Revised (3) and Blocked (3) as distinct outcome categories. They are not counted as Pass or Fail. The Validation Summary Report in Phase 8 will need to reflect the partial-coverage profile when computing the overall validation outcome.
- No credentials, session cookie values, or other secrets are recorded in this artifact, evidence references, or the deviations summary, per the framework's hard rule.
- Evidence file placement convention is `02_Logout/evidence/` per the OQ Execution skill default. No evidence files were physically committed for this run; the Consolidated TC step references in §2 stand in for evidence pointers and the validation lead has accepted this disposition.
- The Validation Summary Report (Phase 8) will consume this record together with the upstream artefacts and is expected to surface the partial coverage (3 Scope-Revised + 3 Blocked) and the four open questions above to the validation lead / QA head for final disposition.
