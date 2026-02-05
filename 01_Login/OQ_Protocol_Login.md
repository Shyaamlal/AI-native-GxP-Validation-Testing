# Operational Qualification Test Protocol: Admin Login

**Feature:** Admin Login  
**Protocol ID:** OQ-LOGIN-v1.0  
**Date:** 2026-02-04  
**Author:** Shyaam (Validation Engineer)  
**Status:** Draft - Ready for Execution

---

## Document Purpose

This Operational Qualification (OQ) Test Protocol defines test cases to verify that the Admin Login feature meets its functional requirements (FRS). Tests are conducted from the user perspective (black box) without knowledge of internal implementation.

---

## Traceability

**Tests:** FRS_Login.md (Functional Requirements)  
**Validates:** URS_Login.md (User Requirements)  
**Based On:** Feature_Boundary_Definition_Login.md (Scope)

---

## Test Approach

### Testing Level

**OQ (Operational Qualification)** - Functional verification from user perspective

### Test Method

- Black box testing (no code inspection)
- Manual test execution
- Browser-based testing
- Evidence capture (screenshots/notes)

### Pass/Fail Criteria

- **Pass:** Actual result matches expected result
- **Fail:** Actual result deviates from expected result
- **Blocked:** Test cannot execute due to dependency

---

## Test Environment

### Application

- **Name:** Sambhava
- **URL:** [Document actual URL]
- **Version:** [Document version if known]

### Browser

- **Browser:** [Chrome/Firefox/Edge]
- **Version:** [Document version]

### Test Data

- **Valid Username:** admin
- **Valid Password:** password
- **Invalid Username:** wronguser
- **Invalid Password:** wrongpass

---

## Test Execution

### Tester Information

- **Tester Name:** ___________________________
- **Date:** ___________________________
- **Execution Time:** Start: _______ End: _______

---

## Test Cases

### OQ-LOGIN-001: User Interface Elements

**Requirement:** FR-LOGIN-001.1, FR-LOGIN-001.2, FR-LOGIN-001.3, FR-LOGIN-005.3  
**User Requirement:** URS-LOGIN-001 (Secure credential entry)  
**Priority:** Critical

**Objective:**  
Verify that all required login UI elements are present and functional.

**Preconditions:**

- Application is accessible
- Browser is open
- User is not logged in

**Test Steps:**

1. Navigate to application login page
2. Observe and verify username input field presence
3. Observe and verify password input field presence
4. Type characters in password field
5. Observe character masking behavior
6. Observe and verify login button presence
7. Verify button is enabled/clickable

**Expected Results:**

- Username input field is visible and labeled
- Password input field is visible and labeled
- Password field masks characters (bullets/dots) in real-time as typed
- Login button is visible, labeled, and enabled
- All elements are accessible and functional

**Actual Results:**  
_[To be filled during execution]_

**Evidence:**  
_[Screenshot reference or notes]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Tester Signature:** _________________ Date: _________

---

### OQ-LOGIN-002: Successful Login with Valid Credentials

**Requirement:** FR-LOGIN-002.1, FR-LOGIN-004.1, FR-LOGIN-005.2  
**User Requirement:** URS-LOGIN-002 (Authentication and access), URS-LOGIN-004 (Feedback)  
**Priority:** Critical

**Objective:**  
Verify that valid administrator credentials result in successful authentication and access to admin dashboard.

**Preconditions:**

- On login page
- Not currently logged in
- Valid credentials known (admin/password)

**Test Steps:**

1. Enter username: "admin"
2. Enter password: "password"
3. Click "Login" button
4. Observe system response
5. Verify navigation to admin dashboard
6. Verify admin functionality is accessible

**Expected Results:**

- No error message displayed
- User is automatically redirected to admin dashboard
- Dashboard loads with admin features visible
- URL changes to admin area
- Implicit success feedback through navigation

**Actual Results:**  
_[To be filled during execution]_

**Evidence:**  
_[Screenshot of successful dashboard access]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Tester Signature:** _________________ Date: _________

---

### OQ-LOGIN-003: Failed Login with Invalid Credentials

**Requirement:** FR-LOGIN-002.2, FR-LOGIN-004.2, FR-LOGIN-005.1  
**User Requirement:** URS-LOGIN-002 (Authentication blocking), URS-LOGIN-004 (Feedback)  
**Priority:** Critical

**Objective:**  
Verify that invalid credentials are rejected and clear error feedback is provided.

**Preconditions:**

- On login page
- Not currently logged in

**Test Steps:**

1. Enter username: "wronguser"
2. Enter password: "wrongpass"
3. Click "Login" button
4. Observe system response
5. Note error message content
6. Verify user remains on login page
7. Verify no access to admin dashboard

**Expected Results:**

- Error message is displayed (browser alert)
- Message clearly indicates authentication failure
- User remains on login page (no navigation)
- Can retry login (form still functional)
- No access granted to admin features

**Actual Results:**  
_[To be filled during execution - include exact error text]_

**Evidence:**  
_[Screenshot of error message]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Tester Signature:** _________________ Date: _________

---

### OQ-LOGIN-004: Empty Field Validation

**Requirement:** FR-LOGIN-002.3  
**User Requirement:** URS-LOGIN-001 (Secure credential entry)  
**Priority:** High

**Objective:**  
Verify that system prevents login submission when required fields are empty.

**Preconditions:**

- On login page
- Fields are empty/cleared

**Test Steps:**

**Part A: Empty Username**

1. Leave username field empty
2. Enter password: "password"
3. Click "Login" button
4. Observe validation behavior

**Part B: Empty Password** 5. Clear all fields 6. Enter username: "admin" 7. Leave password field empty 8. Click "Login" button 9. Observe validation behavior

**Part C: Both Empty** 10. Clear all fields 11. Click "Login" button 12. Observe validation behavior

**Expected Results:**

- **Part A:** Tooltip displays: "Please fill out this field" for username
- **Part B:** Tooltip displays: "Please fill out this field" for password
- **Part C:** Tooltip displays for first required field encountered
- Form submission is prevented in all cases
- User can fill fields and retry

**Actual Results:**  
_[To be filled during execution]_

**Evidence:**  
_[Screenshots of validation tooltips]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Tester Signature:** _________________ Date: _________

---

### OQ-LOGIN-005: Session Creation

**Requirement:** FR-LOGIN-003.1  
**User Requirement:** URS-LOGIN-003 (Session persistence)  
**Priority:** High

**Objective:**  
Verify that successful login creates an authenticated session.

**Preconditions:**

- On login page
- Browser DevTools available

**Test Steps:**

1. Open browser DevTools (F12)
2. Navigate to Application tab → Local Storage
3. Note current localStorage contents
4. Perform successful login (admin/password)
5. Check localStorage after login
6. Verify session key exists
7. Note session key value

**Expected Results:**

- Before login: No authentication session key present (or value is false/null)
- After login: localStorage contains key "isAdminLoggedIn" with value "true"
- Session key is created during login process
- Key persists in localStorage

**Actual Results:**  
_[To be filled during execution - document exact key name and value]_

**Evidence:**  
_[Screenshot of localStorage showing session key]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Tester Signature:** _________________ Date: _________

---

### OQ-LOGIN-006: Session Persistence Across Page Refresh

**Requirement:** FR-LOGIN-003.2  
**User Requirement:** URS-LOGIN-003 (Session persistence)  
**Priority:** High

**Objective:**  
Verify that authenticated session persists across browser page refresh.

**Preconditions:**

- User is logged in as admin
- On admin dashboard

**Test Steps:**

1. Verify currently logged in (admin dashboard visible)
2. Refresh browser page (F5 or Ctrl+R)
3. Observe page reload behavior
4. Verify authentication state maintained
5. Verify admin dashboard still displayed
6. Verify admin functionality still accessible

**Expected Results:**

- Page refreshes successfully
- User remains logged in (no redirect to login page)
- Admin dashboard reloads with all features
- No re-authentication required
- Session continues seamlessly

**Actual Results:**  
_[To be filled during execution]_

**Evidence:**  
_[Note that dashboard remained accessible]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Tester Signature:** _________________ Date: _________

---

### OQ-LOGIN-007: Session Persistence Across Browser Restart

**Requirement:** FR-LOGIN-003.3  
**User Requirement:** URS-LOGIN-003 (Session persistence)  
**Priority:** Medium

**Objective:**  
Verify that authenticated session persists across browser close and restart.

**Preconditions:**

- User is logged in as admin
- On admin dashboard

**Test Steps:**

1. Verify currently logged in
2. Note current session state (localStorage key present)
3. Close browser completely (all windows)
4. Reopen browser
5. Navigate to application URL
6. Observe authentication state
7. Verify if re-authentication required

**Expected Results:**

- Browser closes and reopens successfully
- Upon returning to application, user remains logged in
- No redirect to login page
- Admin dashboard accessible without re-authentication
- Session persists indefinitely (no automatic expiration)

**Actual Results:**  
_[To be filled during execution]_

**Evidence:**  
_[Note session persistence behavior]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Tester Signature:** _________________ Date: _________

---

### OQ-LOGIN-008: Logout Functionality Presence

**Requirement:** FR-LOGIN-006.1  
**User Requirement:** URS-LOGIN-005 (Session termination)  
**Priority:** Low

**Objective:**  
Verify that logout functionality is available to logged-in administrators.

**Preconditions:**

- User is logged in as admin
- On admin dashboard

**Test Steps:**

1. Login as admin
2. Navigate to admin dashboard
3. Look for logout button/link
4. Verify logout control is visible
5. Click logout
6. Observe result

**Expected Results:**

- Logout button/link is visible in dashboard
- Logout control is clearly labeled
- Clicking logout terminates session
- User is returned to logged-out state or login page
- Cannot access admin pages after logout without re-authentication

**Actual Results:**  
_[To be filled during execution]_

**Evidence:**  
_[Screenshot of logout button and post-logout state]_

**Pass/Fail:** ☐ Pass ☐ Fail ☐ Blocked

**Notes:**  
_Logout may be validated more thoroughly in separate Logout feature validation_

**Tester Signature:** _________________ Date: _________

---

## Test Summary

### Test Execution Summary

**Total Test Cases:** 8  
**Tests Passed:** _____  
**Tests Failed:** _____  
**Tests Blocked:** _____

**Pass Rate:** _____%

---

### Requirements Coverage

|Requirement|Test Case(s)|Status|
|---|---|---|
|FR-LOGIN-001.1|OQ-LOGIN-001||
|FR-LOGIN-001.2|OQ-LOGIN-001||
|FR-LOGIN-001.3|OQ-LOGIN-001||
|FR-LOGIN-002.1|OQ-LOGIN-002||
|FR-LOGIN-002.2|OQ-LOGIN-003||
|FR-LOGIN-002.3|OQ-LOGIN-004||
|FR-LOGIN-003.1|OQ-LOGIN-005||
|FR-LOGIN-003.2|OQ-LOGIN-006||
|FR-LOGIN-003.3|OQ-LOGIN-007||
|FR-LOGIN-004.1|OQ-LOGIN-002||
|FR-LOGIN-004.2|OQ-LOGIN-003||
|FR-LOGIN-005.1|OQ-LOGIN-003||
|FR-LOGIN-005.2|OQ-LOGIN-002||
|FR-LOGIN-005.3|OQ-LOGIN-001||
|FR-LOGIN-006.1|OQ-LOGIN-008||

**Total FRS Requirements:** 15  
**Requirements Covered:** 15  
**Coverage:** 100%

---

## Defects Found

|Defect ID|Test Case|Description|Severity|Status|
|---|---|---|---|---|
||||||
||||||

_[To be filled during execution if defects are found]_

---

## Test Protocol Approval

**Prepared by:** Shyaam, Validation Engineer  
**Signature:** _________________ Date: _________

**Reviewed by:** [If applicable]  
**Signature:** _________________ Date: _________

**Approved for Execution by:** [If applicable]  
**Signature:** _________________ Date: _________

---

## Test Execution Sign-Off

**Executed by:** _________________  
**Signature:** _________________ Date: _________

**Reviewed by:** [If applicable]  
**Signature:** _________________ Date: _________

**Approved by:** [If applicable]  
**Signature:** _________________ Date: _________

---

## Notes

This OQ Protocol validates the Admin Login feature against functional requirements (FRS_Login.md). All tests are conducted from user perspective (black box) without code inspection.

Test cases are numbered OQ-LOGIN-001 through OQ-LOGIN-008 and provide complete traceability to FRS and URS requirements.

Test execution should be conducted in a controlled environment with documented browser and application versions. All test results, pass/fail status, and evidence should be captured during execution.

Any deviations from expected results should be documented as defects and assessed for impact on validation conclusion.