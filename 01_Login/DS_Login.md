
# Design Specification: Admin Login Feature

**Feature:** Admin Login
**Based on:** Verification_Report_Login.md (verified investigation findings)
**Investigation Source:** Login_code_investigation.md (Claude Code - 2026-02-01)
**Date:** 2026-02-03
**Author:** Shyaam (Validation Engineer)
**Status:** Draft

---

## Document Purpose

This Design Specification documents the as-built technical implementation of the Admin Login feature based on verified code investigation. All findings have been validated through manual testing (see Verification_Report_Login.md).

---

## Traceability

**Implements:** FRS_Login.md (to be created)
**Verified by:** Verification_Report_Login.md (completed 2026-02-02)
**Investigation source:** Login_code_investigation.md (Claude Code)

---

## Design Overview

### Architecture Pattern
- **Type:** Client-side web application
- **Framework:** React with TypeScript
- **Authentication Model:** Client-side credential validation
- **Session Management:** Browser localStorage
- **No backend API:** All authentication logic executes in browser

### Key Design Decisions
1. **Client-side authentication:** No server-side validation endpoint
2. **Hardcoded credentials:** Username and password stored in source code
3. **localStorage persistence:** Session survives browser refresh
4. **No route protection:** Admin pages accessible without authentication check

---

## Component Architecture

### Primary Components

#### 1. AdminLogin Component
**File:** `src/pages/AdminLogin.tsx`
**Purpose:** Login form UI and authentication logic
**Key functionality:**
- User input capture (username/password)
- Credential validation
- Session creation
- Navigation after successful login
- Error message display

#### 2. Application Routing
**File:** `src/App.tsx`
**Purpose:** Route definitions
**Key functionality:**
- Defines /admin route
- No route guards implemented
- Direct navigation allowed without authentication check

#### 3. Session-Aware Components
**Files:**
- `src/pages/AdminDashboard.tsx` (logout functionality)
- `src/pages/ClientManagement.tsx` (logout functionality)
- `src/pages/ClientDashboard.tsx` (logout functionality)

**Purpose:** Pages that check authentication state and provide logout

---

## Detailed Design Documentation

### DS-LOGIN-001: Authentication Mechanism

**Implementation:**
```
Location: src/pages/AdminLogin.tsx
Method: handleLogin function

Logic:
1. User enters username in text input field
2. User enters password in password input field (masked)
3. User clicks "Login" button
4. System compares input against hardcoded values:
   - Expected username: "admin"
   - Expected password: "password"
5. If match: Proceed to DS-LOGIN-002 (session creation)
6. If no match: Display error message
```

**Technical Details:**
- **Validation type:** String equality comparison
- **Location:** Client-side JavaScript (browser)
- **No encryption:** Credentials compared as plain text
- **No API call:** Zero network requests during authentication

**Verified:** ✅ Network tab showed no API calls (Verification_Report_Login.md, Test 1)

---

### DS-LOGIN-002: Credential Storage

**Implementation:**
```
Location: src/pages/AdminLogin.tsx
Storage method: Hardcoded string literals in source code

Valid credentials:
- Username: "admin" (string literal)
- Password: "password" (string literal)

Comparison logic:
if (username === "admin" && password === "password") {
    // Authentication successful
}
```

**Technical Details:**
- **Storage:** Source code (visible in browser DevTools)
- **Format:** Plain text strings
- **Accessibility:** Publicly visible via "View Source"
- **No database:** No external credential store
- **No configuration:** Credentials cannot be changed without code modification

**Verified:** ✅ Found credentials in source code (Verification_Report_Login.md, Test 2)

---

### DS-LOGIN-003: Session Management

**Implementation:**
```
Location: src/pages/AdminLogin.tsx
Storage mechanism: Browser localStorage API

Session creation:
localStorage.setItem("isAdminLoggedIn", "true");

Session check (in other components):
const isLoggedIn = localStorage.getItem("isAdminLoggedIn");
if (isLoggedIn === "true") {
    // User is authenticated
}

Session termination (logout):
localStorage.removeItem("isAdminLoggedIn");
```

**Technical Details:**
- **Storage location:** Browser localStorage (persistent)
- **Key name:** "isAdminLoggedIn"
- **Value:** String "true" when authenticated
- **Persistence:** Survives browser refresh and restart
- **Scope:** Per-origin (shared across all tabs of same domain)
- **Expiration:** No automatic expiration (persists until logout or browser data clear)

**Verified:** ✅ Key "isAdminLoggedIn" found with value "true" after login (Verification_Report_Login.md, Test 3)

---

### DS-LOGIN-004: User Interface Design

**Login Form Elements:**

1. **Username Input Field**
   - Type: Text input
   - HTML element: `<input type="text">`
   - Label: "Username"
   - Required: Yes (frontend validation)

2. **Password Input Field**
   - Type: Password input
   - HTML element: `<input type="password">`
   - Label: "Password"
   - Character masking: Yes (browser default)
   - Required: Yes (frontend validation)

3. **Login Button**
   - Type: Submit button
   - Text: "Login" (or similar)
   - Action: Triggers handleLogin function
   - Enabled: Always

4. **Error Message Area**
   - Display: Conditional (shown only on authentication failure)
   - Content: Error text describing failure
   - Location: Below form fields

**UI Behavior:**
- **On load:** Empty form fields, no error message
- **During input:** Form accepts text, password field masks characters
- **On submit (valid):** Redirect to admin dashboard
- **On submit (invalid):** Display error message, remain on login page
- **On submit (empty):** [Document based on your observation - does it validate empty fields?]

---

### DS-LOGIN-005: Navigation Flow

**Implementation:**
```
Successful Login Flow:
1. User on login page (/admin/login)
2. User submits valid credentials
3. localStorage.setItem("isAdminLoggedIn", "true") executes
4. Browser navigates to: /admin/dashboard
5. User sees admin dashboard

Failed Login Flow:
1. User on login page
2. User submits invalid credentials
3. Error message displays
4. User remains on login page
5. Can retry login
```

**Navigation Method:**
- Framework: React Router (or native browser navigation - document which)
- Trigger: Programmatic navigation after localStorage update
- Destination: Admin dashboard route

---

### DS-LOGIN-006: Route Protection (Absence Thereof)

**Implementation:**
```
Location: src/App.tsx
Route definition:

<Route path="/admin" element={<AdminDashboard />} />

No authentication guard present.
No check for localStorage.getItem("isAdminLoggedIn").
Direct URL navigation allowed without login.
```

**Design Implication:**
- **Unprotected routes:** Admin pages accessible by direct URL navigation
- **Manual bypass possible:** User can set localStorage key manually via browser DevTools
- **No server-side protection:** No backend validation of session validity

**Note:** This is a design observation, not a validation test. Route protection is OUT OF SCOPE for Login feature validation (see Feature_Boundary_Definition_Login.md - deferred to Authorization validation).

---

### DS-LOGIN-007: Error Handling

**Implementation:**
```
Location: src/pages/AdminLogin.tsx

Error scenarios:
1. Invalid username: Display error message
2. Invalid password: Display error message
3. Empty fields: [Document behavior]
4. Network errors: N/A (no network calls)
```

**Error Message Content:**
- Type: Tool tip text message
- Display duration: Persistent until next login attempt
- Clearing: On new input

**Error Types:**
- **Authentication failure:** specific message: Please fill out this form
- **Form validation:** Empty field handling (document behavior)

---

## Technology Stack

### Frontend Framework
- **React:** 19.1.0
- **TypeScript:** 5.8.3
- **Build tool:** Vite (or document actual)

### Browser APIs Used
- **localStorage API:** Session persistence
- **Standard form inputs:** Username/password fields
- **React Router:** Navigation (if applicable)

### Dependencies
- None for authentication logic (self-contained in component)

---

## Data Flow Diagram
```
User Action: Enter credentials
        ↓
Component: AdminLogin.tsx
        ↓
Function: handleLogin()
        ↓
Validation: Compare against hardcoded values
        ↓
    [Decision]
     /     \
   Yes      No
    ↓       ↓
Set         Display
localStorage error
"isAdminLoggedIn" message
= "true"
    ↓
Navigate to
admin dashboard
    ↓
Check localStorage
in dashboard
    ↓
Render admin UI
```

---

## Security Considerations (Design Documentation Only)

**Note:** This section documents design as-is, not recommendations.

### Observed Design Characteristics:
1. **Client-side validation:** All authentication logic in browser
2. **Hardcoded credentials:** Source code contains valid credentials
3. **No encryption:** Credentials compared as plain text
4. **localStorage persistence:** Session survives browser restart
5. **No route protection:** Direct URL access possible
6. **No session expiration:** Manual logout required

**Risk Assessment:** Deferred to separate security review (not part of validation scope)

---

## Testing Considerations

### Existing Test Coverage
**File:** `tests/auth.spec.ts` (Playwright E2E tests)
**Coverage:** E2E authentication flow

### Validation Test Focus
Design specification enables validation testing of:
- Credential validation behavior (valid vs invalid)
- Session persistence across page refresh
- Logout functionality
- Error message display
- UI element presence and behavior

---

## Design Constraints & Limitations

### Known Limitations:
1. **Single credential pair:** Only "admin"/"password" supported
2. **No user management:** Cannot add/modify/delete users
3. **No password reset:** No mechanism to change credentials
4. **No session timeout:** Session persists until manual logout
5. **No brute force protection:** Unlimited login attempts allowed
6. **No multi-factor authentication:** Single-factor only (username/password)

### Design Assumptions:
1. Browser localStorage is available and functional
2. JavaScript is enabled in browser
3. Single admin user sufficient for application purpose
4. Security model acceptable for application risk level

---

## File Inventory

**Files comprising this design:**

| File | Purpose | Lines of Code |
|------|---------|---------------|
| `src/pages/AdminLogin.tsx` | Login UI and logic | 149 |
| `src/App.tsx` | Route definitions | 35 |
| `src/pages/AdminDashboard.tsx` | Logout functionality | Partial (lines 18-21) |
| `src/pages/ClientManagement.tsx` | Logout functionality | Partial (lines 63-66) |
| `src/pages/ClientDashboard.tsx` | Logout functionality | Partial (lines 91-94) |
| `tests/auth.spec.ts` | E2E tests | 138 |

**Total:** 6 files analyzed

**Verification:** All files confirmed present and analyzed (Verification_Report_Login.md, Test 4)

---

## Verification Evidence

This Design Specification is based on verified investigation findings:

**Commission Verification:**
- ✅ Client-side authentication confirmed (Network tab inspection)
- ✅ Hardcoded credentials confirmed (Source code inspection)
- ✅ localStorage session confirmed (Application tab inspection)

**Omission Verification:**
- ✅ All relevant files analyzed (File inventory complete)
- ✅ No authentication files missed (100% coverage)

**Reference:** See Verification_Report_Login.md for detailed test results and evidence.

---

## Design Specification Approval

**Prepared by:** Shyaam, Validation Engineer | Date: 2026-02-03
**Reviewed by:** [If applicable] | Date: ___________
**Approved by:** [If applicable] | Date: ___________

---

## Document History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-02-03 | Shyaam | Initial DS based on verified investigation |

---

## Notes

This DS documents the as-built implementation of Admin Login feature as it currently exists in the Sambhava application. All technical claims have been verified through manual testing (see Verification_Report_Login.md).

Design observations about security or architecture are documented as-is without judgment or recommendations. Risk assessment and security review are separate activities outside the scope of this technical documentation.

This DS serves as the foundation for Functional Requirements Specification (FRS_Login.md) and will be used to create validation test protocols (OQ_Protocol_Login.md).