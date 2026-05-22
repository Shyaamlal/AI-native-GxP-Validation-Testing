---
artifact_type: Validation_Scope
feature: Logout
version: 1.0
status: Approved
ai_assistance:
  agent_skill: validation-scope
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-18T20:42:00Z
  prompt_version: v1.0
human_review:
  reviewer: shyaamlal
  approval_timestamp: 2026-05-18T20:48:31Z
  comment: "Approved with open-question resolutions: Q1 (stale-tab) record observed behaviour as known property; treat as design constraint pending product-owner disposition. Q2 (in-flight requests) stays out of scope per §3.5. Q3 — no SSO on this deployment. Q4 — single-role assumption holds for this run. Q5 / A5 — audit-log + session-replay access confirmed achievable via test-env admin."
traceability:
  upstream:
    - Feature_Scoping_Logout.md
    - Risk_Assessment_Logout.md
---

# Validation Scope — Logout

## 1. Validation Objective

Demonstrate that the Logout feature of the multi-role web platform terminates an authenticated session reliably and consistently from the user's perspective, such that no protected content or authenticated capability remains accessible to the user (or a subsequent user of the same browser) after logout, in support of 21 CFR Part 11 §11.10(d)(e)(g) and EU Annex 11 §12 access-control obligations.

## 2. In Scope

### 2.1. Explicit logout via the sidebar user menu (Sign out control)
- **Observed behaviour reference:** Feature Scoping §2.1, §2.2.
- **Risk reference:** Risk Assessment §2 (GxP impact — primary access-control surface); §5 (Category 5 custom application).
- **Validation depth:** Functional verification of the happy path. Confirm that activating Sign out from the user menu terminates the session and redirects the current tab to `/login` consistently.
- **Rationale:** This is the user-initiated path the entire access-control posture depends on. Any defect here is a direct §11.10(d) exposure.

### 2.2. Post-logout redirect of the active tab
- **Observed behaviour reference:** Feature Scoping §2.1 (system response — current tab redirects to `/login`).
- **Risk reference:** Risk Assessment §2 (access control), §4 (ALCOA+ Attributable — visible identity must change with the session).
- **Validation depth:** Functional verification. Confirm the URL transition and that the authenticated chrome (sidebar, user identity button) no longer renders.
- **Rationale:** The user-visible signal that logout has succeeded.

### 2.3. Direct navigation to protected routes while signed out
- **Observed behaviour reference:** Feature Scoping §2.3.
- **Risk reference:** Risk Assessment §2 (21 CFR Part 11 §11.10(d) limit access to authorised individuals); §6 item 1 (server-side session revocation).
- **Validation depth:** Functional + negative testing across a representative sample of protected routes (at minimum `/dashboard`, `/voice/history`, `/voice/record`, `/users`, `/usage`, `/voice/report/<id>`). Verify each redirects to `/login` without rendering protected content.
- **Rationale:** This is the route-guard contract that backs logout's access-control claim.

### 2.4. Cross-tab behaviour after logout in another tab
- **Observed behaviour reference:** Feature Scoping §2.4.
- **Risk reference:** Risk Assessment §4 (audit-trail considerations — stale-tab disclosure window), §6 item 2.
- **Validation depth:** Functional verification of the observed lazy-redirect contract. Specifically: (a) confirm a stale tab does not allow any *new* protected action (every subsequent navigation or protected API request is rejected and the tab redirects to `/login`); (b) document the observed disclosure window (stale rendered content remains visible until next user-initiated navigation) and capture it as a known behavioural property of the system.
- **Rationale:** The risk assessment classifies this as a disclosure concern rather than a record-integrity concern, but its disposition (intended vs defect) is a load-bearing decision that the OQ Protocol must record evidence for. See Open Question 1.

### 2.5. Browser back-button / history navigation after logout
- **Observed behaviour reference:** Feature Scoping §2.5.
- **Risk reference:** Risk Assessment §6 item 3 (back-button / bfcache).
- **Validation depth:** Functional + negative testing. From a representative set of post-logout starting points, exercise browser back (and forward) and confirm no protected authenticated view is restored — `/login` is rendered in every case.
- **Rationale:** A common practical bypass vector for access-control failures; the OQ should make redirect-to-login an explicit pass criterion.

### 2.6. Server-side session revocation
- **Observed behaviour reference:** Not directly observed at Phase 1 (Feature Scoping Open Question Q2). Inferred from the redirect behaviour in §2.3 and §2.4.
- **Risk reference:** Risk Assessment §6 item 1 (highest-priority OQ-target).
- **Validation depth:** Negative testing. With audit-log / network inspection, verify that a session token issued before logout is rejected by the server after logout (i.e. server-side invalidation, not merely client-side state clearing). Method: capture a session token while authenticated, perform logout, replay an authenticated request with the captured token, confirm rejection (401/403 or equivalent).
- **Rationale:** Without server-side revocation, all other observed redirects are cosmetic and the §2 GxP claim collapses. This is the single most important test in the scope.

### 2.7. Audit-trail emission on logout
- **Observed behaviour reference:** Not directly observable from end-user UI (Feature Scoping Open Question Q7).
- **Risk reference:** Risk Assessment §4 (audit-trail considerations — 21 CFR Part 11 §11.10(e)); §6 item 4.
- **Validation depth:** Inspection of server-side audit log. Verify a logout event is recorded with, at minimum, the user identity, timestamp (contemporaneous), and source identifier. Cross-check against ALCOA+ Attributable and Contemporaneous.
- **Rationale:** Required for Part 11 §11.10(e). Cannot be validated through the UI alone — requires audit-log access; the Validation Scope phase commits to this access being arranged before OQ Execution.

## 3. Out of Scope

### 3.1. Authentication / sign-in flow
- **Observed behaviour reference:** Feature Scoping §4 (Adjacent but separate — authentication).
- **Rationale for exclusion:** Authentication is a separate feature with a separate validation scope. Logout terminates a session; it does not establish one.
- **If applicable, where this is covered:** Per the project repo convention, the Login feature is validated under `01_Login/`.

### 3.2. Change Password and Recording Guide entries in the user menu
- **Observed behaviour reference:** Feature Scoping §2.2 (user-menu surface).
- **Rationale for exclusion:** These controls share the dropdown with Sign out but are independent features. Including them would conflate scope.
- **If applicable, where this is covered:** Separate per-feature validation efforts (Change Password, SOP/Recording Guide content). Not produced by this chain.

### 3.3. Visual / cosmetic styling of the user menu and login form
- **Observed behaviour reference:** Feature Scoping §2.1, §3.
- **Rationale for exclusion:** Cosmetic UI states (colours, typography, dropdown animation) do not affect the access-control contract. Excluded per the Risk Assessment §5 rationale: testing depth is driven by GxP impact, not visual polish.

### 3.4. Inactivity-driven / absolute session timeout (if any)
- **Observed behaviour reference:** Feature Scoping §4 (Adjacent but separate — session timeout); Open Question Q1.
- **Rationale for exclusion:** Session timeout is a distinct mechanism from user-initiated logout. If it exists in the system, it warrants its own validation effort (or merger via a change request). Including it here would expand scope beyond what was scoped in Phase 1.
- **If applicable, where this is covered:** A separate Session Timeout validation effort, if and when commissioned. Surface to the validation lead as a follow-on need.

### 3.5. In-flight request handling at the moment of logout
- **Observed behaviour reference:** Risk Assessment §6 item 5; Feature Scoping Open Question Q3.
- **Rationale for exclusion:** Excluded from the OQ-Execution depth of the *initial* validation chain because (a) it was not exercised in Phase 1 observation, and (b) reliable test stimulus requires either a known long-running endpoint or developer cooperation, which the validation lead has not yet confirmed available. Surface as a residual risk and as a candidate for a focused follow-on test if Open Question 2 below is answered affirmatively.
- **If applicable, where this is covered:** Recommended follow-on test scenario; not part of this chain unless explicitly added.

### 3.6. SSO / federated single-sign-out propagation
- **Observed behaviour reference:** Risk Assessment §7 item 5 (Open Question).
- **Rationale for exclusion:** No SSO integration was observed in Phase 1. If the system later integrates with an identity provider, single-sign-out behaviour becomes a distinct validation scope. Excluded here unless the human confirms SSO is in use (Open Question 3 below); in that case this scope must be revisited before approval.

### 3.7. Multi-role / multi-workspace logout variants
- **Observed behaviour reference:** Feature Scoping §1 (Client Workspace, role Client only); Risk Assessment §7 item 4.
- **Rationale for exclusion:** Only one role in one workspace was observed in Phase 1. Other-role variants (if they exist) are formally out of this scope. Surface as Open Question 4 — if other roles materially differ, a re-scope is required.

### 3.8. Browser back-forward cache (bfcache) policy verification at HTTP-header level
- **Observed behaviour reference:** Feature Scoping §4 (Adjacent but separate — bfcache policy).
- **Rationale for exclusion:** The user-observable effect of bfcache policy is validated in §2.5. The HTTP-header configuration (e.g. `Cache-Control: no-store`) that produces that effect is an implementation concern verified by the application's existing security review or by a separate technical test. Validation here verifies the user-visible outcome, not the configuration mechanism.

## 4. Assumptions

A1. **The platform is a GAMP 5 Category 5 custom application** for this validation effort. If the platform is in fact a configured deployment of a third-party product, the depth implied by §2 (notably the server-side and audit-log tests in §2.6 and §2.7) may shift toward supplier-evidence-referencing rather than direct testing.

A2. **The platform falls within 21 CFR Part 11 and/or EU Annex 11 regulated scope** for the client's intended use. The §1 objective and the §2.6, §2.7 depths assume Part 11 §11.10(d)(e)(g) and Annex 11 §12 apply. (Risk Assessment Open Question 2.)

A3. **No SSO / federated identity provider** is configured for this account. If SSO is enabled, §3.6 must be revisited.

A4. **The Client role observed in Phase 1 is representative of how logout behaves for all roles** in the Client Workspace. Other-role variants, if present, will be re-scoped.

A5. **Audit-log access and the ability to inspect server-side records and replay session tokens** will be available to the OQ Execution phase. §2.6 and §2.7 are unverifiable end-to-end without this access; the validation lead commits to arranging it before Phase 7.

A6. **The validation effort treats logout in isolation from the broader application security review.** Where the application's existing security review or penetration test covers session management, those artefacts are referenceable as supporting evidence but are not consumed as a substitute for the OQ tests above.

## 5. Exit Criteria

This feature is considered validated when the OQ Execution Record (Phase 7) provides documented evidence, traceable to each in-scope item, demonstrating that:

EC1. Activating Sign out from the sidebar user menu redirects the active tab to `/login` and removes the authenticated chrome. (§2.1, §2.2)

EC2. Across every protected route exercised, direct navigation while signed out redirects to `/login` without rendering protected content. (§2.3)

EC3. A stale tab open at the moment of logout-elsewhere cannot initiate any new protected action: the next user-initiated navigation or protected API request is rejected and the tab is redirected to `/login`. (§2.4)

EC4. Browser back, forward, and history navigation from any post-logout state result in `/login` rendering — no protected authenticated view is restored. (§2.5)

EC5. A session token captured pre-logout is rejected by the server when replayed post-logout. (§2.6)

EC6. The server-side audit log contains a logout event with user identity, timestamp, and source identifier, traceable to the test execution. (§2.7)

EC7. None of the in-scope tests reveals an unmitigated defect in the access-control contract; any defects found are either remediated and re-tested or accepted with documented residual-risk justification by the validation lead.

## 6. Open Questions for the Human

1. **Stale-tab disclosure window — intended or defect?** Feature Scoping §2.4 records that a stale tab retains its previously rendered protected content until the next navigation. §2.4 of this scope validates the *redirect* contract; whether the *display* of stale content is acceptable is a design call that the validation lead, in conjunction with the product owner, must record. The OQ Protocol will capture observed behaviour either way; the disposition determines whether this is a pass or a defect.

2. **Is in-flight request testing in scope for this initial validation, or follow-on?** §3.5 currently excludes it. If the validation lead believes the risk warrants inclusion, scope must be re-opened.

3. **Is the deployment SSO-enabled?** If yes, §3.6 must move into §2 and the upstream IdP becomes a referenced qualified component (or in-scope counterparty for testing).

4. **Are there roles or workspaces beyond the observed Client / Client Workspace that materially differ in logout placement or behaviour?** If yes, scope must be expanded or the feature split.

5. **Will audit-log and session-replay access be available to the OQ Execution phase?** A5 above depends on this; without it, §2.6 and §2.7 cannot be executed and the chain must either fall back to defensible alternatives (e.g. supplier evidence) or pause pending access provisioning.

## 7. Notes

- Out-of-scope items in §3 are explicitly listed rather than silently excluded, per the framework's expectation that scope artifacts disclose their boundaries.
- §2.6 (server-side session revocation) and §2.7 (audit-trail emission) cannot be validated through end-user UI observation alone and require access to either network inspection or audit-log records during OQ Execution. The validation lead is committing to this access via Assumption A5.
- The scope deliberately does not include any mitigation language (controls to be added, code changes required); the framework places mitigations in the FRS acceptance criteria (Phase 5) and the OQ Protocol (Phase 6). This artifact only delineates what will be tested.
- Open Questions 1-5 above are decision-blocking for the next phase only insofar as the validation lead chooses to wait on them. The questions are surfaced; the framework does not assume answers.
