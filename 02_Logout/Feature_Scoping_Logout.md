---
artifact_type: Feature_Scoping
feature: Logout
version: 1.0
status: Approved
ai_assistance:
  agent_skill: validation-feature-scoping
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-18T13:40:00Z
  prompt_version: v1.0
human_review:
  reviewer: shyaamlal
  approval_timestamp: 2026-05-18T13:48:45Z
  comment: null
traceability:
  upstream: []
---

# Feature Scoping — Logout

## 1. Feature Identity
- **Feature name:** Logout
- **System under test:** multi-role web platform (test environment)
- **Environment classification:** non-validated (DEV / QA / pre-production)
- **Access method:** browser via Playwright MCP (Chromium)
- **Observer date:** 2026-05-18
- **Scoping scenario:** An authenticated Client-Workspace user (role: Client) ends their session from any authenticated page in the application, terminating their access to protected routes in the current tab and any other tabs of the same browser session.

## 2. Observed Behaviour

### 2.1. Explicit logout from the user menu
- **User action(s):**
  1. From any authenticated page (observed entry point: `/dashboard`), click the user identity button at the bottom of the left sidebar (displays the user's initials, display name, and email address).
  2. In the dropdown that opens above the button, click **Sign out**.
- **System response:** The current tab navigates to `/login`. The authenticated chrome (sidebar with workspace navigation, user identity button, content area) is no longer rendered; the login form is rendered instead. The page title remains the application's product name.
- **Visual feedback:** The dropdown closes; the route changes; the login layout replaces the workspace layout. No intermediate confirmation dialog, no toast or success message, no loading spinner observed.
- **Behavioural outcome:** The session is terminated. Subsequent attempts to reach protected routes (in this tab or in other open tabs of the same browser context) redirect to `/login` — see 2.3 and 2.4.

### 2.2. User-menu surface containing the logout control
- **User action(s):** Click the user identity button at the bottom of the left sidebar.
- **System response:** A dropdown opens directly above the button containing three controls, in order:
  1. `Change password` (link → `/change-password`)
  2. `Recording guide` (link → `/sop`)
  3. `Sign out` (button — the logout trigger)
- **Visual feedback:** The button takes the `expanded` accessibility state while the dropdown is open. Clicking the button again, or pressing `Escape`, collapses the dropdown without performing any action.
- **Behavioural outcome:** No state change unless the user activates one of the three controls. Opening and closing the menu has no effect on the session.

### 2.3. Direct navigation to a protected route while signed out
- **User action(s):**
  1. From the `/login` page (no active session), type a protected URL into the address bar — observed: `/dashboard`, `/voice/history`.
  2. Submit the navigation.
- **System response:** The browser is redirected to `/login`. The protected page is not rendered.
- **Visual feedback:** The login form renders. No error message, no flash of protected content observed.
- **Behavioural outcome:** No protected content is exposed to an unauthenticated user.

### 2.4. Cross-tab behaviour after logout in another tab
- **User action(s):**
  1. In Tab A, sign in and navigate to a protected page (observed: `/dashboard`).
  2. Open Tab B in the same browser context, navigate Tab B to a protected page (observed: `/voice/history`). Tab B renders the page with live data.
  3. In Tab A, perform the explicit logout via the user menu (per 2.1). Tab A navigates to `/login`.
  4. Switch to Tab B without performing any action in it.
  5. In Tab B, click a sidebar navigation link (observed: `Dashboard`).
- **System response:**
  - Between steps 3 and 5, Tab B continues to display the `/voice/history` page as previously rendered, including the analyses table populated with data fetched while the session was active. There is no automatic redirect, no overlay, no banner, and no visible indication in Tab B that the session has been terminated.
  - On step 5, Tab B navigates to `/login` instead of `/dashboard`.
- **Visual feedback:** In Tab B post-logout-elsewhere: the stale authenticated layout (sidebar, user identity button, page content with previously loaded data) remains visible until the next user-initiated navigation. The login form appears only after that navigation.
- **Behavioural outcome:** Logout in one tab does not push a real-time signal to other tabs; stale tabs retain their last-rendered protected view until they attempt their next protected navigation, at which point they are redirected to `/login` and re-authentication is required.

### 2.5. Browser back-button after logout
- **User action(s):**
  1. From the post-logout `/login` page, press the browser back button one or more times.
- **System response:** Each back navigation results in the URL bar showing `/login` and the login form being rendered. Previously rendered protected pages (e.g. `/dashboard`, `/voice/history`) are not restored from the browser's back-forward cache as authenticated views.
- **Visual feedback:** The login form remains displayed; no flash of cached protected content observed in either tab tested.
- **Behavioural outcome:** Protected content viewed during the prior session is not made visible again via browser history navigation after logout.

## 3. User Interface Elements

Elements directly involved in the logout feature:

- **User identity button (sidebar footer)** — interactive button. Accessible name composed of user initials, display name, and email address. Renders the user's initials avatar, display name, email, and a chevron indicator. Acts as the disclosure trigger for the user menu.
- **User menu dropdown** — non-modal popover anchored above the user identity button. Contains:
  - **`Change password` link** — navigates to `/change-password`. Not part of the logout flow.
  - **`Recording guide` link** — navigates to `/sop`. Not part of the logout flow.
  - **`Sign out` button** — the logout trigger. Plain button (no confirmation modal, no `aria-haspopup`).
- **Login form (post-logout landing)** — at `/login`: `Email` textbox, `Password` textbox, `Sign in` button, `Forgot password?` link. The presence of this layout is the user-visible signal that logout has completed.

No logout-specific confirmation dialog, toast, banner, badge, or session-timeout countdown was observed in the authenticated UI during the observation period.

## 4. Feature Boundary

**In the feature:**
- The `Sign out` control in the sidebar user menu (its placement, label, and activation behaviour).
- The state transition from an authenticated session to an unauthenticated session triggered by activating that control.
- The immediate redirect of the current tab from its authenticated location to `/login`.
- The enforcement that, after logout, protected routes are no longer accessible in this tab (route guard / redirect to `/login`).
- The behaviour of other tabs of the same browser context after logout has been triggered elsewhere — specifically, that their next protected navigation is redirected to `/login`.

**Adjacent but separate:**
- **Authentication (sign-in).** Credential entry, validation, and session establishment at `/login` are a separate feature. Logout only ends a session; it does not create one.
- **Session timeout / inactivity-driven session termination.** Not observed during the scoping window. If such a mechanism exists, it is a separate behaviour from explicit user-initiated logout. See Open Question Q1.
- **Route protection / authenticated-route guard.** The mechanism that redirects unauthenticated requests to `/login` is exercised by logout, but it is a cross-cutting concern serving the entire application, not a logout-specific control.
- **Browser back-forward cache (bfcache) policy.** The observation that protected pages are not restored to authenticated state on browser back is a consequence of cache headers and/or route guards, not a logout control surface.
- **Change Password** and **Recording Guide** entries in the user menu — co-located with `Sign out` in the dropdown, but separate features.
- **Notifications** button in the top bar — visible from authenticated pages but unrelated to logout.

## 5. Open Questions

1. Does the system enforce an inactivity-driven or absolute session timeout independent of user-initiated logout? If so, what is the timeout duration, what user-visible signal precedes or accompanies the forced sign-out, and how does it interact with multiple open tabs?
2. Is there a server-side session-revocation step on logout (i.e. is the session invalidated at the server, or only client-side state cleared)? Empirical confirmation would require observing whether a previously valid session token, if reused after logout, is rejected by the server.
3. What happens to in-flight requests that were initiated before `Sign out` was clicked but had not completed? (Not exercised during scoping — no long-running action was in progress at the moment of logout.)
4. What is the intended behaviour in a stale tab that still displays previously fetched protected content (per 2.4)? Should that tab actively detect logout and redirect/blank itself, or is lazy redirect-on-next-navigation the intended design?
5. Is logout available from every authenticated page in the application (e.g. `/voice/record`, `/voice/report/<id>`, `/users`, `/usage`, `/sop`, `/change-password`), or only from pages that render the standard sidebar? The sidebar appeared on every authenticated page navigated during scoping, but the full route surface was not exhaustively traversed.
6. Are there roles or workspaces (other than the Client Workspace observed) whose user menu or logout flow differs? Only the Client role of one workspace was observed.
7. Is there any audit-log or telemetry event emitted on logout that would be visible to an administrator? Not observable from the end-user UI.

## 6. Observation Notes

- Observation was performed via Playwright MCP driving a Chromium browser instance against the test-environment URL. The account used was a Client-Workspace test account (`Test Client 1`); credentials are not recorded here.
- Two tabs were used for cross-tab observation (2.4). Both tabs belonged to the same browser context, so they shared cookies / storage with the application origin.
- No interactive element opened a confirmation dialog before logging out; `Sign out` is single-click destructive of session state. This is recorded as observation, not as judgement.
- Screenshots and accessibility snapshots captured by Playwright MCP during the session reside under `.playwright-mcp/` in the working directory. They are session-scoped and not committed to the repository.
- Console output captured during the session was reviewed only for the presence of error-level messages relevant to the logout flow; none directly attributable to logout were observed. Console contents themselves are not reproduced in this artifact.
- No source code, configuration files, or backend logs were read. All findings are based on observable behaviour of the running system from a user's browser.
- The full route surface of the application was not exhaustively traversed; the logout control was exercised from `/dashboard` and its post-logout effect verified on `/dashboard` and `/voice/history`. Other authenticated routes were not individually verified as entry points to logout — see Open Question Q5.
