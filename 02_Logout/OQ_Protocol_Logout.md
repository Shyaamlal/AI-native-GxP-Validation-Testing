---
artifact_type: OQ_Protocol
feature: Logout
version: 1.0
status: Approved
ai_assistance:
  agent_skill: validation-oq-protocol-author
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-18T21:03:00Z
  prompt_version: v1.0
human_review:
  reviewer: shyaamlal
  approval_timestamp: 2026-05-18T21:13:25Z
  comment: "Approved with TC-017 amendment applied to the artifact pre-approval (observe-then-assert against unauthenticated shape set {301,302,401,403} plus zero workspace-data markers, rather than asserting 302 specifically) — this corrects an unverified Laravel-default assumption that had been carried in from the Phase 5 approval. Open-question resolutions: Q1 (TC-003 failing routes) — re-scope question, not defect; escalate to validation lead. Q2 (TC-019 audit table/column names) — to be supplied by validation lead before Phase 7; tester obtains pre-run. Q3 (TC-017 cookie name) — laravel_session expected; tester confirms at execution."
traceability:
  upstream:
    - URS_Logout.md
    - FRS_Logout.md
---

# OQ Protocol — Logout

## 1. Purpose

This protocol specifies the test cases that, when executed in the non-validated test environment, verify that every acceptance criterion in `FRS_Logout.md` is met, thereby demonstrating conformance of the Sambhava Logout feature to its approved URS and FRS.

## 2. Test Environment Requirements

- **System under test:** Sambhava Voice Intelligence platform, `https://sambhava.neurapses.dev`.
- **Required role(s):** One Client-role test account in the Client Workspace (e.g. `testclient@sambhava.test`). The same account is reused across all test cases unless a test case notes otherwise.
- **Test data prerequisites:** The Client account is enrolled in the workspace with at least one prior analysis record visible on `/voice/history` (so that the protected-content non-disclosure tests can assert against real data). The protocol does not create or modify test data; if the data prerequisites are not satisfied, the tester surfaces a blocker before execution.
- **Browser / tool requirements:** Chromium-family browser at a current stable version. Where the test case calls for network capture or replay (TC-017, TC-018), an HTTP-capture tool (browser DevTools Network panel, or equivalent — `curl` with the captured cookie value, or Playwright's `request` API) is required.
- **Audit-log access:** Per the approved Validation Scope (A5) and the FRS approval resolution to Q4, audit-record discovery is performed by direct database query in the test environment. The tester must have, before execution, a documented database connection string and credentials (handled out-of-band; not recorded in this protocol) and the name of the audit-event table or view that records authentication events. If the table/view name is unknown at execution time, TC-019, TC-020, and TC-021 are blocked.
- **Clock reference:** Per the FRS approval resolution to Q2, the server clock is authoritative for audit timestamps. The tester records the wall-clock time of each sign-out activation from the test machine but evaluates the ±30-second tolerance against the server-recorded timestamp.

## 3. Test Cases

### TC-001: Sign-Out control is visible in the user menu
- **Trace:** AC-FRS-001.1.
- **Preconditions:** The Client test account is signed in and viewing `/dashboard`.
- **Steps:**
  1. Locate the user-identity button at the bottom of the left sidebar.
  2. Click the user-identity button to open the user menu.
  3. Inspect the items rendered in the user menu.
- **Expected result:** The user menu contains exactly one control whose visible label reads "Sign out" (case-insensitive). The control is rendered as a button (not a link to a different page).
- **Pass criteria:** The control labelled "Sign out" is present exactly once and rendered as an activatable button.

### TC-002: Sign-Out activates on a single click with no confirmation dialog
- **Trace:** AC-FRS-001.2.
- **Preconditions:** TC-001 has passed in the same session; the user menu is open with the Sign-Out control visible.
- **Steps:**
  1. Click the "Sign out" button exactly once.
  2. Observe the page and any modal layer for up to 5 seconds.
- **Expected result:** No confirmation dialog, modal, alert, or secondary prompt is rendered. The application begins the sign-out transition immediately after the single click.
- **Pass criteria:** No additional user interaction is required between the single click on "Sign out" and the start of the sign-out transition.

### TC-003: User menu and Sign-Out control are reachable from every in-scope authenticated route (pre-OQ discovery)
- **Trace:** AC-FRS-001.3.
- **Preconditions:** The Client test account is signed in. This test case implements the product-owner check-in deferred from URS Q1; the in-scope route set is enumerated and recorded as it is exercised. Result is feed-forward evidence for the remaining test cases; a failure here surfaces a re-scope question rather than necessarily a defect.
- **Steps:**
  1. Sign in and navigate sequentially to each of the following routes: `/dashboard`, `/voice/record`, `/voice/history`, `/users`, `/usage`, `/sop`, `/change-password`, and one `/voice/report/<id>` route for an existing report.
  2. On each route, confirm the workspace navigation (left sidebar) is rendered and the user-identity button is present at the bottom of the sidebar.
  3. On each route, open the user menu and confirm the "Sign out" control is present and activatable.
  4. Record the result for each route in the execution record (route → menu present yes/no, Sign-Out reachable yes/no).
- **Expected result:** On every route in the list, the workspace navigation is rendered and the "Sign out" control is reachable in the user menu.
- **Pass criteria:** Every route in step 1 returns yes/yes in step 4. If any route returns no, the tester does not record a defect immediately; the result is surfaced to the validation lead and the product owner as a re-scope question per the URS Q1 disposition, and the remaining test cases proceed using the confirmed subset.

### TC-004: Active tab redirects to sign-in page within 5 seconds of Sign-Out activation
- **Trace:** AC-FRS-002.1.
- **Preconditions:** The Client account is signed in and on `/dashboard`. The user menu is closed.
- **Steps:**
  1. Open the user menu.
  2. Start a stopwatch (or note `t0` in milliseconds).
  3. Click the "Sign out" button.
  4. Observe the URL bar and the rendered page until the URL settles on the sign-in URL and the sign-in form is fully rendered. Record the elapsed time `t1 - t0`.
- **Expected result:** The active tab's URL changes to `https://sambhava.neurapses.dev/login` (the sign-in URL) and the sign-in form is rendered. The elapsed time `t1 - t0` is ≤ 5 seconds.
- **Pass criteria:** Final URL equals the sign-in URL AND sign-in form is rendered AND elapsed time ≤ 5 seconds.

### TC-005: No authenticated identity is displayed after sign-out
- **Trace:** AC-FRS-002.2.
- **Preconditions:** TC-004 has just passed in the same tab; the active tab is on the sign-in page.
- **Steps:**
  1. Inspect the rendered page (sign-in form area, header, footer, and any chrome).
  2. Search the visible text and the DOM for the test account's email address (`testclient@sambhava.test`), display name ("Test Client 1"), and initials avatar ("TC").
- **Expected result:** None of these identifiers is present anywhere on the post-sign-out page.
- **Pass criteria:** Search for each of `testclient@sambhava.test`, `Test Client 1`, and the "TC" avatar in the visible text and DOM returns zero matches.

### TC-006: Workspace navigation is absent from the DOM after sign-out
- **Trace:** AC-FRS-003.1.
- **Preconditions:** TC-004 has just passed; the active tab is on the sign-in page.
- **Steps:**
  1. Open the browser's DOM inspector on the post-sign-out page.
  2. Search the DOM for elements containing the workspace-navigation link labels: "Dashboard", "New Analysis", "Analysis History", "Users", "Usage & Limits", "Recording Guide".
- **Expected result:** None of these link labels is present in the DOM of the rendered page.
- **Pass criteria:** Each of the six labels returns zero matches in the post-sign-out DOM.

### TC-007: User identity area is absent from the DOM after sign-out
- **Trace:** AC-FRS-003.2.
- **Preconditions:** TC-004 has just passed; the active tab is on the sign-in page.
- **Steps:**
  1. Open the browser's DOM inspector on the post-sign-out page.
  2. Search the DOM for the avatar element ("TC"), the display name ("Test Client 1"), and the email (`testclient@sambhava.test`) anywhere in the document.
- **Expected result:** No element representing the user-identity area is present in the DOM.
- **Pass criteria:** Each of the three identifiers returns zero matches in the post-sign-out DOM.

### TC-008: Direct navigation to a protected route while signed out redirects to sign-in
- **Trace:** AC-FRS-004.1.
- **Preconditions:** The browser has no active Sambhava session (cookies cleared, or sign-out completed in this browser context).
- **Steps:**
  1. In the URL bar, enter `https://sambhava.neurapses.dev/dashboard` and submit.
  2. Wait for the page to settle.
  3. Inspect the URL bar and the rendered content.
  4. Repeat steps 1-3 for each of `/voice/history`, `/voice/record`, `/users`, `/usage`, and one `/voice/report/<id>` URL whose id matches an existing report.
- **Expected result:** For each URL in steps 1 and 4, the URL bar settles on the sign-in URL and the sign-in form is rendered.
- **Pass criteria:** For every route exercised, final URL equals the sign-in URL AND the sign-in form is rendered.

### TC-009: No protected content is visible during direct-navigation redirect
- **Trace:** AC-FRS-004.2.
- **Preconditions:** Same as TC-008.
- **Steps:**
  1. Begin a browser-DevTools recording (Network and Performance panels) before submitting the URL.
  2. In the URL bar, enter `https://sambhava.neurapses.dev/voice/history` and submit.
  3. Review the rendered output and any intermediate paint frames (DevTools Performance recording) for the appearance of protected content — specifically, the analysis-history table headers ("Subject", "Owner", "Gender", "DOB", "Date", "Status", "Actions") or any subject name from the test workspace.
  4. Repeat for `/dashboard` (looking for "Good afternoon", "My Users", "Analyses" tiles).
- **Expected result:** No frame in the rendered output or the Performance recording contains the listed protected-content markers.
- **Pass criteria:** Each searched marker returns zero matches in the Performance frame capture and in the final rendered DOM.

### TC-010: Refresh/forward of the active tab after sign-out does not restore any prior workspace page
- **Trace:** AC-FRS-005.1.
- **Preconditions:** TC-004 has just passed; the active tab is on the sign-in page; prior to sign-out, the tab had visited at least three protected routes (e.g. `/dashboard`, `/voice/history`, `/voice/record`).
- **Steps:**
  1. Press F5 (or the browser refresh control) on the sign-in page. Confirm the rendered page after refresh.
  2. Activate the browser forward button (if available). Confirm the rendered page.
  3. Manually enter the URL of a route the tab visited prior to sign-out. Confirm the rendered page.
- **Expected result:** Each of the three actions results in the sign-in page being rendered. No previously rendered workspace page is shown in its authenticated form.
- **Pass criteria:** Each action's final URL is the sign-in URL AND the rendered content is the sign-in form (not a restored authenticated view).

### TC-011: A new tab opened after sign-out cannot reach protected content
- **Trace:** AC-FRS-005.2.
- **Preconditions:** TC-004 has just passed in the original tab; the browser context is otherwise unchanged.
- **Steps:**
  1. Open a new tab in the same browser context (Ctrl+T or equivalent).
  2. In the new tab's URL bar, enter `https://sambhava.neurapses.dev/dashboard` and submit.
  3. Inspect the rendered content and the URL bar.
  4. Repeat steps 2-3 for `/voice/history`.
- **Expected result:** Each navigation in the new tab results in the sign-in page.
- **Pass criteria:** For each route exercised, the new tab's final URL equals the sign-in URL AND the sign-in form is rendered.

### TC-012: A stale tab retains its rendered content immediately after sign-out elsewhere (no proactive redirect)
- **Trace:** AC-FRS-006.1.
- **Preconditions:** Two tabs (Tab A and Tab B) are open in the same browser context, both signed in as the same Client account. Tab A is on `/dashboard`; Tab B is on `/voice/history` and has fully rendered the analyses table.
- **Steps:**
  1. Switch to Tab A.
  2. In Tab A, perform sign-out per TC-002 / TC-004 (single click on the "Sign out" control).
  3. Without performing any action in Tab B, switch to Tab B and observe its rendered content for up to 30 seconds.
- **Expected result:** Tab B continues to display the previously-rendered `/voice/history` page, including the analyses table, throughout the observation window. No automatic redirect to the sign-in page is triggered by sign-out in Tab A alone.
- **Pass criteria:** Tab B's URL remains `https://sambhava.neurapses.dev/voice/history` and the analyses table remains visible throughout a 30-second post-sign-out observation window in which no action is performed in Tab B.

### TC-013: A stale tab redirects to the sign-in page within 5 seconds of the next user-initiated navigation after sign-out elsewhere
- **Trace:** AC-FRS-006.2.
- **Preconditions:** TC-012 has just passed; Tab B is the stale tab and is still displaying `/voice/history` with prior data.
- **Steps:**
  1. In Tab B, note `t0` (in milliseconds).
  2. Click the "Dashboard" link in the left sidebar of Tab B.
  3. Observe Tab B's URL bar and rendered content. Note `t1` when the URL settles on the sign-in URL and the sign-in form is rendered.
- **Expected result:** Tab B's URL changes to the sign-in URL and the sign-in form is rendered, with elapsed time `t1 - t0` ≤ 5 seconds.
- **Pass criteria:** Final URL equals the sign-in URL AND sign-in form is rendered AND elapsed time ≤ 5 seconds.

### TC-014: An authenticated action issued from a stale tab does not succeed
- **Trace:** AC-FRS-006.3.
- **Preconditions:** Repeat the setup of TC-012 to obtain a fresh stale tab (the prior TC-013 will have already redirected Tab B; a new stale-tab pair is established).
- **Steps:**
  1. In the stale Tab B, open the DevTools Network panel and clear the existing entries.
  2. In Tab B, attempt an in-page action that triggers an authenticated request that would have succeeded under the prior session — e.g. click on a "Report" or "EN" link in a row of the analyses table to request the report content.
  3. Observe the resulting network response in the DevTools Network panel and the rendered page.
- **Expected result:** The triggered request does not return protected workspace content. The response indicates an unauthenticated outcome (a redirect to the sign-in URL, or an HTTP status indicating unauthenticated access), and the tab does not render the requested protected content.
- **Pass criteria:** The captured response for the action's request does not contain workspace data, AND the resulting rendered page either is the sign-in page or remains the prior stale page without successful authenticated content load.

### TC-015: Browser back navigation after sign-out lands on the sign-in page
- **Trace:** AC-FRS-007.1.
- **Preconditions:** TC-004 has just passed; the active tab is on the sign-in page; the tab had visited at least three protected routes during the prior signed-in session.
- **Steps:**
  1. Activate the browser back button.
  2. Observe the URL bar and the rendered content.
  3. Repeat steps 1-2 two further times (three total back actions).
- **Expected result:** Each back action results in the URL bar settling on the sign-in URL and the sign-in form being rendered.
- **Pass criteria:** After each of the three back actions, final URL equals the sign-in URL AND the sign-in form is rendered.

### TC-016: Browser forward navigation after back lands on the sign-in page
- **Trace:** AC-FRS-007.2.
- **Preconditions:** TC-015 has just passed; the active tab is on the sign-in page after three back actions.
- **Steps:**
  1. Activate the browser forward button.
  2. Observe the URL bar and the rendered content.
  3. Repeat steps 1-2 two further times (three total forward actions).
- **Expected result:** Each forward action results in the URL bar settling on the sign-in URL and the sign-in form being rendered.
- **Pass criteria:** After each of the three forward actions, final URL equals the sign-in URL AND the sign-in form is rendered.

### TC-017: A captured session cookie returns an unauthenticated response after sign-out
- **Trace:** AC-FRS-008.1.
- **Preconditions:** A fresh sign-in is performed in a controlled tab. Before sign-out, the value of the Sambhava session cookie is captured. The captured value is held outside the browser (e.g. in a `curl` command line or a Playwright `request` fixture). The expected cookie name on Sambhava (Laravel) is `laravel_session`; if the actual cookie carrying the session is differently named in the test environment, the tester records the observed name and proceeds with it.
- **Steps:**
  1. Sign in as the Client test account in a controlled browser session.
  2. Open DevTools → Application → Cookies → `https://sambhava.neurapses.dev`. Identify and copy the value of the application's session cookie (record only the cookie name and that a value was captured in the execution record — do not record the value itself).
  3. Verify the cookie is currently valid by issuing a request bearing it to a protected endpoint (e.g. `GET /voice/history` via `curl` or Playwright with `Cookie: <name>=<captured-value>`) and confirming a 200 response with workspace HTML. The request shall not follow redirects automatically (`curl -i --no-location`, or Playwright `request` with `maxRedirects: 0`).
  4. In the browser, sign out via the user menu (per TC-002).
  5. After confirming sign-out has completed (sign-in page visible), re-issue the same request from step 3 — same endpoint, same cookie value, no other change, redirects still not followed.
  6. Inspect the HTTP response from step 5 and record observed values in the execution record: the HTTP status code, the `Location` header (if present), and the response body.
- **Expected result:** The response in step 5 is an unauthenticated response — observed status code is one of 301, 302, 401, or 403; and if a `Location` header is present it resolves to `/login` (absolute or relative); and the response body contains no workspace-data markers (the analysis-history table headers from TC-009, dashboard widget labels, subject names, analysis ids, transcripts, or behavioural scores). On Sambhava (Laravel) the expected shape is 302 with `Location: /login`, but the pass criterion does not depend on a specific status code among the four listed unauthenticated shapes; the tester records what is observed and asserts against the set.
- **Pass criteria:** Observed status code ∈ {301, 302, 401, 403} AND (Location header absent OR resolves to `/login`) AND zero workspace-data markers in the response body.

### TC-018: Replayed session-cookie response contains no workspace data
- **Trace:** AC-FRS-008.2.
- **Preconditions:** TC-017 has just been executed; the captured session cookie has been replayed against `/voice/history` after sign-out.
- **Steps:**
  1. Take the response body from the post-sign-out replay performed in TC-017 step 5.
  2. Repeat the replay against a second workspace data endpoint — `/voice/report/<id>` for an id known to exist in the workspace's reports.
  3. Search both response bodies for: workspace-data markers (the analysis-history table headers from TC-009, subject names, analysis ids, transcripts, behavioural scores).
- **Expected result:** Neither response body contains any workspace-data marker.
- **Pass criteria:** Each searched marker returns zero matches across both response bodies.

### TC-019: An audit record for the sign-out event exists in the database
- **Trace:** AC-FRS-009.1.
- **Preconditions:** Audit-log database access is available (see §2 Audit-log access). The tester has the audit-event table or view name (to be specified by the validation lead before execution per the FRS Q4 disposition). A fresh sign-out is performed in a controlled session; the tester records the user identifier `U` used and the wall-clock sign-out completion time `T_test` (the time the active tab settled on the sign-in page in TC-004).
- **Steps:**
  1. Perform a sign-out and record `U` and `T_test` as in the preconditions.
  2. Within 60 seconds of `T_test`, connect to the test-environment audit database.
  3. Run a query that returns audit events for user `U` with event timestamp in the window [`T_test` − 60s, `T_test` + 60s]. (Concrete query: `SELECT * FROM <audit_table> WHERE user_identifier = '<U>' AND event_time BETWEEN '<T_test - 60s>' AND '<T_test + 60s>' AND event_type IN ('logout','sign_out','session_end','<platform-specific>');` — the exact column names and event-type literal are confirmed against the test environment at execution time.)
  4. Inspect the query result.
- **Expected result:** Exactly one row is returned, with an event type that the validation lead identifies as denoting a sign-out / session-end action.
- **Pass criteria:** Query returns ≥ 1 row attributable to user `U` with an event type that denotes a sign-out / session-end action AND zero unexplained additional rows for the same user in the same window.

### TC-020: The sign-out audit record carries the user identifier and a timestamp within ±30 seconds of T_test
- **Trace:** AC-FRS-009.2.
- **Preconditions:** TC-019 has just passed; the row returned for the sign-out event is available for inspection.
- **Steps:**
  1. Read the user-identifier column from the returned row and compare to the recorded `U`.
  2. Read the event-timestamp column from the returned row, normalise to UTC if necessary, and compute the absolute difference from `T_test` (the wall-clock sign-out completion time, also normalised to UTC).
  3. Record the user identifier match (yes/no) and the computed time difference in the execution record.
- **Expected result:** The user identifier matches `U`. The absolute time difference is ≤ 30 seconds.
- **Pass criteria:** Identifier match equals yes AND absolute time difference ≤ 30 seconds.

### TC-021: No spurious sign-out audit record exists when no sign-out has been performed
- **Trace:** AC-FRS-009.3.
- **Preconditions:** Audit-log database access available (as TC-019). A control window is defined: a five-minute interval `[T_control_start, T_control_end]` during which the Client test account is known not to have signed out (no sign-out activation has been performed; the tester confirms this before the window starts).
- **Steps:**
  1. Note `T_control_start`. Confirm the Client test account is signed in (or known signed out) without any session-state change during the window.
  2. Wait until `T_control_end = T_control_start + 5 minutes`.
  3. Run the same query shape as TC-019, with the window `[T_control_start, T_control_end]` and user identifier `U`.
  4. Inspect the result.
- **Expected result:** The query returns zero rows attributable to user `U` with a sign-out / session-end event type within the control window.
- **Pass criteria:** Row count equals zero.

## 4. Traceability Coverage

This protocol has 21 test cases covering all 21 acceptance criteria in `FRS_Logout.md`. Coverage at AC level (each AC → ≥ 1 TC):

| AC | TC(s) |
|---|---|
| AC-FRS-001.1 | TC-001 |
| AC-FRS-001.2 | TC-002 |
| AC-FRS-001.3 | TC-003 |
| AC-FRS-002.1 | TC-004 |
| AC-FRS-002.2 | TC-005 |
| AC-FRS-003.1 | TC-006 |
| AC-FRS-003.2 | TC-007 |
| AC-FRS-004.1 | TC-008 |
| AC-FRS-004.2 | TC-009 |
| AC-FRS-005.1 | TC-010 |
| AC-FRS-005.2 | TC-011 |
| AC-FRS-006.1 | TC-012 |
| AC-FRS-006.2 | TC-013 |
| AC-FRS-006.3 | TC-014 |
| AC-FRS-007.1 | TC-015 |
| AC-FRS-007.2 | TC-016 |
| AC-FRS-008.1 | TC-017 |
| AC-FRS-008.2 | TC-018 |
| AC-FRS-009.1 | TC-019 |
| AC-FRS-009.2 | TC-020 |
| AC-FRS-009.3 | TC-021 |

Every AC has ≥ 1 covering TC; no AC is uncovered.

## 5. Open Questions for the Human

1. **TC-003 disposition for routes whose menu placement differs.** TC-003 is structured as a discovery step (URS Q1 deferral). If any in-scope route does not render the workspace navigation, the test case directs the tester to surface a re-scope question rather than to record a defect. The validation lead and product owner must confirm that re-scope is the correct response on this run, or substitute alternative guidance.

2. **TC-019 audit-event type literal and column names.** The query in TC-019 is parametric on the audit table name, the event-type literal that denotes sign-out, the user-identifier column name, and the event-time column name. The validation lead (or tech lead) must supply these four values to the tester before execution. If they are not available at execution start, TC-019, TC-020, and TC-021 are blocked.

3. **TC-017 cookie name and storage form.** The protocol assumes the application uses a server-side session cookie named `laravel_session` (Sambhava is on Laravel) and that bearing this cookie suffices to authenticate a request. The tester confirms the cookie name at execution and records any deviation. If the application instead requires additional headers (e.g. CSRF token, bearer token), TC-017 and TC-018 must be augmented with the appropriate header capture-and-replay before execution.

## 6. Notes

- TC-003 is the protocol's implementation of the pre-OQ product-owner check-in deferred from URS Q1. Its result is feed-forward evidence for the rest of the protocol: the in-scope route set assumed by TC-008, TC-010, TC-013, and others is the set of routes that pass TC-003.
- TC-017's expected response is an observe-then-assert step against the set {301, 302, 401, 403} plus zero workspace-data markers in the body. The FRS approval comment carried in a "assert 302 specifically" assumption derived from Laravel's typical default; that assumption was reviewed at the OQ Protocol gate and walked back, because it had not been verified against the test environment. The tester records the observed shape in the execution record so that downstream traceability captures the actual response shape, while pass/fail is judged against any acceptable unauthenticated shape.
- TC-019/TC-020/TC-021 require database access that is not part of the browser-driven test surface. They are written so that the tester executes them after the UI test cases, in a single coordinated audit-log inspection session.
- Pass criteria across all test cases are binary (yes/no, equality, count thresholds, time thresholds). No test case carries an "evaluate by judgement" disposition.
- The protocol does not include test cases for items out of scope per `Validation_Scope_Logout.md` §3 (authentication, sibling menu entries, cosmetic styling, session timeout, in-flight request handling, SSO single-sign-out, multi-role variants, HTTP-header bfcache verification).
