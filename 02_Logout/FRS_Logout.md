---
artifact_type: FRS
feature: Logout
version: 1.0
status: Approved
ai_assistance:
  agent_skill: validation-frs-author
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-18T20:56:00Z
  prompt_version: v1.0
human_review:
  reviewer: shyaamlal
  approval_timestamp: 2026-05-18T21:00:13Z
  comment: "Approved with open-question resolutions consumed by OQ Protocol (Phase 6): Q1 (timing thresholds AC-FRS-002.1, AC-FRS-006.2) accept 5-second default — no documented platform SLA. Q2 (audit timestamp tolerance AC-FRS-009.2) accept ±30-second — server clock authoritative for the platform. Q3 (unauthenticated response shape AC-FRS-008.1) — Laravel default is 302 redirect to /login; OQ Protocol shall assert that specifically rather than accepting any of 401/403/redirect. Q4 (audit-record discovery mechanism FRS-009) — DB query via test-env admin access; OQ Protocol to specify the precise query/path."
traceability:
  upstream:
    - URS_Logout.md
---

# Functional Requirements Specification — Logout

## 1. Purpose

This specification states the functional behaviour the multi-role web platform shall provide to satisfy the User Requirements for the Logout feature, with explicit acceptance criteria that the OQ Protocol will translate into executable test cases.

## 2. Functional Requirements

### FRS-001: Sign-Out Control Presentation and Activation
- **Statement:** The system shall present a single Sign-Out control within the user menu, accessible from every authenticated page that renders the workspace navigation, and shall activate sign-out on a single user activation of that control without requesting a confirmation step.
- **Trace:** URS-001, URS-002, URS-011.
- **Acceptance criteria:**
  - **AC-FRS-001.1** — Given the user is signed in and viewing any authenticated page that renders the workspace navigation, when the user opens the user menu, then the menu contains exactly one Sign-Out control identified by an unambiguous label (e.g. "Sign out").
  - **AC-FRS-001.2** — Given the user menu is open with the Sign-Out control visible, when the user activates the Sign-Out control once, then the system initiates sign-out immediately without presenting any intermediate confirmation dialog, modal, or additional prompt.
  - **AC-FRS-001.3** — Given the user is signed in, when the user enumerates the authenticated routes confirmed in scope (per the pre-OQ product-owner check), then the workspace navigation containing the user menu is rendered on each such route.

### FRS-002: Session Termination on Sign Out
- **Statement:** The system shall, on activation of the Sign-Out control, end the user's authenticated session and navigate the active tab to the sign-in page.
- **Trace:** URS-003.
- **Acceptance criteria:**
  - **AC-FRS-002.1** — Given the user is signed in, when the user activates the Sign-Out control, then within 5 seconds the active tab's URL changes to the sign-in URL and the sign-in form is rendered.
  - **AC-FRS-002.2** — Given the user has activated Sign-Out and the active tab now shows the sign-in page, when the user inspects the application chrome, then no authenticated user identity is displayed on the page.

### FRS-003: Removal of Authenticated User Interface After Sign Out
- **Statement:** The system shall, on the post-sign-out page, omit the workspace navigation, the user identity indicator, and any other UI element that is rendered only for authenticated users.
- **Trace:** URS-004.
- **Acceptance criteria:**
  - **AC-FRS-003.1** — Given sign-out has just completed, when the user inspects the page rendered in the active tab, then the workspace navigation (sidebar with links such as Dashboard, New Analysis, Analysis History, Users, Usage & Limits, Recording Guide) is not present in the DOM.
  - **AC-FRS-003.2** — Given sign-out has just completed, when the user inspects the page rendered in the active tab, then the user identity area (avatar, display name, email) is not present in the DOM.

### FRS-004: Protected-Route Access Rejection for Unauthenticated Requests
- **Statement:** The system shall, for any request to a protected route originating from a client without a valid authenticated session, respond by returning the unauthenticated sign-in page in place of the requested protected content.
- **Trace:** URS-005.
- **Acceptance criteria:**
  - **AC-FRS-004.1** — Given the user is not signed in, when the user navigates directly (e.g. by URL bar entry) to a protected route from the in-scope set (at minimum: `/dashboard`, `/voice/history`, `/voice/record`, `/users`, `/usage`, `/voice/report/<id>`), then the rendered page is the sign-in page and the URL displayed is the sign-in URL.
  - **AC-FRS-004.2** — Given the user is not signed in, when the user attempts direct navigation to a protected route, then no protected content (e.g. the requested page's data table, analysis report, user list) is visible in the rendered output, even momentarily.

### FRS-005: No Display of Prior-Session Content After Sign Out
- **Statement:** The system shall not, after sign-out, render any page whose content was retrieved or generated under the prior authenticated session, except to the extent unavoidable for tabs already open at the moment of sign-out — those tabs are governed by FRS-006.
- **Trace:** URS-006.
- **Acceptance criteria:**
  - **AC-FRS-005.1** — Given the user has signed out in the active tab, when the user re-issues any navigation in that tab (forward, refresh, new URL), then the rendered output is the sign-in page or another unauthenticated page; no workspace page rendered during the prior session is restored.
  - **AC-FRS-005.2** — Given the user has signed out in the active tab and opens a new tab in the same browser, when the new tab navigates to any protected route, then the response is the sign-in page (FRS-004 applies).

### FRS-006: Stale-Tab Next-Action Redirect
- **Statement:** The system shall, in any tab that was open with rendered authenticated content at the moment sign-out occurred in another tab, reject the next user-initiated navigation or authenticated request from that tab and render the sign-in page in that tab.
- **Trace:** URS-007.
- **Acceptance criteria:**
  - **AC-FRS-006.1** — Given two tabs A and B are open in the same browser context, both authenticated as the same user; Tab B is displaying a protected page with rendered data, when the user activates Sign-Out in Tab A, then Tab B continues to display its previously-rendered content (no proactive redirect is required, consistent with the approved scope disposition of Q1).
  - **AC-FRS-006.2** — Given two tabs of the same browser context, both signed in as the same user, and sign-out has just been completed in one tab while the other tab is displaying a protected page with stale rendered content, when the user performs the next interaction in the stale tab that requires the server to serve authenticated content (e.g. clicking a navigation link, refreshing, submitting a form), then within 5 seconds the stale tab's URL changes to the sign-in URL and the sign-in page is rendered.
  - **AC-FRS-006.3** — Given two tabs of the same browser context, both signed in as the same user, and sign-out has just been completed in one tab while the other tab is displaying a protected page with stale rendered content, when the user attempts to issue an authenticated client-to-server action from the stale tab (any in-tab action that triggers a request requiring the prior session), then the action does not succeed against the prior session's identity.

### FRS-007: History-Navigation Behaviour After Sign Out
- **Statement:** The system shall not, for any tab in which sign-out has occurred or which has been redirected to the sign-in page after sign-out, restore an authenticated view via the browser's back, forward, or history navigation.
- **Trace:** URS-008.
- **Acceptance criteria:**
  - **AC-FRS-007.1** — Given the user has signed out and the active tab is on the sign-in page, when the user activates the browser's back button one or more times, then each resulting page rendered is the sign-in page (or another unauthenticated page); no protected page rendered during the prior session is restored to its authenticated form.
  - **AC-FRS-007.2** — Given the user has signed out, the active tab is on the sign-in page, and the user has activated the browser's back button one or more times, when the user then activates the browser's forward button one or more times, then each resulting page is the sign-in page or an unauthenticated page; no protected page is restored to its authenticated form.

### FRS-008: Server-Side Session Revocation
- **Statement:** The system shall, on completion of sign-out, invalidate the server-recognised authenticated session such that any request thereafter bearing the prior session's identifiers is treated as unauthenticated.
- **Trace:** URS-009.
- **Acceptance criteria:**
  - **AC-FRS-008.1** — Given a session identifier (e.g. session cookie, token, or equivalent) is captured while the user is signed in, when sign-out has completed and that identifier is subsequently presented in a request to a protected endpoint, then the server responds with an unauthenticated outcome (e.g. HTTP 401 / 403, or a redirect to the sign-in page) and does not return protected data.
  - **AC-FRS-008.2** — Given a session identifier captured while the user was signed in is presented in a request to a protected endpoint after sign-out has completed, when the protected endpoint is one that would have returned the user's workspace data under the prior session (e.g. an endpoint backing `/voice/history` or `/voice/report/<id>`), then the response payload contains no workspace data and no identifiable subject records.

### FRS-009: Audit Record on Sign Out
- **Statement:** The system shall, on each completion of sign-out, write an audit record retrievable by an authorised reviewer that identifies the user who signed out and the time at which sign-out completed.
- **Trace:** URS-010.
- **Acceptance criteria:**
  - **AC-FRS-009.1** — Given a sign-out has completed at a known time T for a known user U, when an authorised reviewer queries the system's audit log for events at or near T, then there exists a record attributable to user U with an event type identifying a sign-out (or equivalent session-end) action.
  - **AC-FRS-009.2** — Given a sign-out audit record exists for user U at or near sign-out completion time T, when an authorised reviewer inspects the record, then it contains at minimum a user identifier corresponding to U and a timestamp whose value is within 30 seconds of T.
  - **AC-FRS-009.3** — Given sign-out has not been performed by user U in the interval surrounding T, when the reviewer queries the audit log, then no spurious sign-out record attributable to user U exists for that interval.

## 3. Functional Roles

Functional roles (one level above implementation; named by responsibility, not by technology):

- **Application UI** — renders the workspace navigation, user menu, Sign-Out control, and sign-in page; receives user activations and forwards them to the application layer.
- **Session Manager** — establishes, validates, and terminates the user's authenticated session in response to sign-in and sign-out actions. Owns the contract referenced by FRS-002 and FRS-008.
- **Authentication / Authorisation Service** — evaluates whether an incoming request bears a valid authenticated session and either permits or denies access to protected resources. Owns the contract referenced by FRS-004 and FRS-008.
- **Route Guard** — for client-side routes, enforces unauthenticated-vs-authenticated separation and triggers redirection to the sign-in page when an unauthenticated client requests a protected route. Cooperates with Authentication / Authorisation Service. Owns the contract referenced by FRS-004 and FRS-007 in the client.
- **Audit Logger** — receives and persists the sign-out event referenced by FRS-009; is queried by authorised reviewers.

## 4. Open Questions for the Human

1. **AC-FRS-002.1 / AC-FRS-006.2 timing thresholds.** A 5-second upper bound for the active-tab redirect and the stale-tab redirect is proposed as a reasonable user-experience threshold for an interactive sign-out. The systems analyst / tech lead should confirm this threshold or substitute the platform's existing service-level expectation if one is documented. The OQ Protocol depends on a concrete value.

2. **AC-FRS-009.2 timestamp tolerance.** A ±30-second window for the audit timestamp is proposed to accommodate clock skew between client and server. The systems analyst should confirm this tolerance or substitute the platform's authoritative clock-sync expectation. If the audit log uses server time exclusively, the tolerance can be tightened.

3. **AC-FRS-008.1 expected unauthenticated response shape.** The criterion accepts any of HTTP 401, HTTP 403, or a redirect to sign-in. The systems analyst should confirm which the platform's API is expected to return; the OQ tests will then assert specifically rather than accepting any of three outcomes.

4. **FRS-009 audit-record discovery mechanism.** The acceptance criteria reference an "authorised reviewer queries the system's audit log". The systems analyst should specify the means of access (admin UI, database query, log-file inspection) so the OQ Protocol can describe a reproducible test action. The Validation Scope (A5) confirms access will be available via the test-env admin; the specific mechanism remains to be named.

## 5. Notes

- FRS-006 is written so that it does not impose a real-time proactive cross-tab logout obligation on the system. The product-owner disposition recorded against URS-007 (and earlier at the Validation Scope gate) treats the lazy-redirect-on-next-action contract as the intended behaviour. AC-FRS-006.1 codifies the stale-content tolerance explicitly so that a tester does not record a defect against an intended property.
- FRS-008 deliberately uses the language "session identifiers (e.g. session cookie, token, or equivalent)" rather than naming a specific mechanism. The OQ Protocol will instantiate the AC against whatever mechanism the application uses; Open Question 3 above asks the systems analyst to name the expected response shape, which is a different decision from naming the identifier type.
- FRS-009 splits the audit-record requirement into three ACs covering existence (.1), content (.2), and absence-of-spurious-records (.3). This gives the OQ Protocol a positive, a content-conformance, and a negative test path against the same FRS.
- No FRS item is written for any URS item that does not exist. URS-011's no-confirmation requirement is captured inside FRS-001 (AC-FRS-001.2) rather than as a standalone FRS to keep the user-menu behaviour cohesive.
