# Skill 1: Feature Observation Documenter

**Validation Phase:** 1 - Feature Observation  
**Template Used:** Feature_Observation_Template.md  
**AI Tools Compatible:** Claude, ChatGPT, Gemini, any LLM  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Converts raw manual testing notes into structured, well-organized Feature Observation documents that serve as the foundation for all downstream validation activities.

**Problem it solves:**  
Raw testing notes are often messy, unorganized, and incomplete. This skill helps transform scattered observations into systematic documentation that validators can rely on.

**Why it matters:**  
Feature Observation documents are the **single source of truth** for what the system actually does. All requirements, specifications, and test cases trace back to these observations. If observations are incomplete or incorrect, all downstream documents inherit those flaws.

---

## When to Use This Skill

### Timing in Validation Workflow

```
Manual Black-Box Testing (Human)
        ↓
[USE THIS SKILL]
        ↓
Feature Observation Document Created
        ↓
Code Investigation (Next Phase)
```

**Use this skill when:**
- ✅ You've completed manual testing of a feature
- ✅ You have raw notes, screenshots, or test results
- ✅ You need to document what you observed in structured format
- ✅ You're ready to create the foundation document for validation

**Don't use this skill when:**
- ❌ You haven't tested the feature yet (test first, document second)
- ❌ You're documenting code behavior (use Skill 3: Technical Investigator)
- ❌ You're writing requirements (use Skill 4-6: Requirements Writers)

---

## Prerequisites

**Before using this skill, you must have:**

1. **Completed manual testing:**
   - Tested happy path (normal usage)
   - Tested edge cases (boundary conditions)
   - Tested error conditions (invalid inputs, failures)
   - Documented all behaviors observed

2. **Raw testing notes:**
   - What you did (actions taken)
   - What happened (system responses)
   - What you saw (UI elements, messages)
   - Any surprises or unexpected behaviors

3. **Test environment details:**
   - Date of testing
   - System/environment tested
   - Tools used (browser, DevTools, etc.)

**You do NOT need:**
- ❌ Code access or understanding
- ❌ Technical implementation knowledge
- ❌ Requirements documents (you're creating the foundation)

---

## Domain Knowledge Embedded in This Skill

### Black-Box Testing Principles

**Observable behaviors only:**
- Record what you SEE, not what you THINK is happening
- Avoid assumptions about implementation
- Distinguish between observation and interpretation

**Example:**
- ✅ Good: "localStorage key 'isAdminLoggedIn' disappears after logout" (observed in DevTools)
- ❌ Poor: "Session is invalidated" (interpretation, not observation)

### GAMP 5 Alignment

**Category 1 approach:**
- Human performs testing (AI doesn't test)
- AI organizes human observations (authoring tool)
- Human verifies organized document

**Documentation standards:**
- Clear, unambiguous descriptions
- Observable, measurable, testable behaviors
- Organized workflow sequence
- Complete coverage (happy path + edge cases + errors)

### IEC 62304 Considerations

**Software item behavior:**
- Document user-visible behaviors
- Include error handling observations
- Note any safety-relevant behaviors
- Record unexpected or surprising results

---

## How to Invoke This Skill

### Standard Invocation Pattern

```markdown
**Context Loading:**
- Load: Methodology.md (validation approach)
- Load: Sambhava_Application_Context.md (application-specific knowledge)

**Skill Invocation:**
Using the Feature Observation Documenter skill, organize these raw test notes into a structured Feature Observation document.

**Feature Information:**
- Feature Name: [e.g., Admin Logout]
- Test Date: [YYYY-MM-DD]
- Tester: [Your Name]
- Test Environment: [Browser, OS, System]

**Raw Testing Notes:**
[Paste your unorganized notes here - bullets, paragraphs, whatever format you have]

**Observed Behaviors:**
[List what you saw the system do]

**Edge Cases Tested:**
[List boundary conditions you tested]

**Error Conditions Tested:**
[List failure scenarios you tested]

**Unexpected Behaviors:**
[Anything surprising or confusing]

**Quality Requirements:**
- Observable behaviors only (no implementation assumptions)
- Clear, specific descriptions
- Organized by workflow sequence
- Complete coverage of testing performed

**Output Format:**
Use template: Feature_Observation_Template.md
```

---

## Real Example: Admin Logout Feature

### Input to AI (Using This Skill)

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Sambhava_Application_Context.md

**Skill Invocation:**
Using the Feature Observation Documenter skill, organize these raw test notes into a structured Feature Observation document.

**Feature Information:**
- Feature Name: Admin Logout
- Test Date: 2026-02-06
- Tester: Shyaam
- Test Environment: Chrome v120, macOS, Production (sambhava.org)

**Raw Testing Notes:**
- logout button in header on right side
- when hover over it says "Logout" in tooltip
- clicked it and went back to home page
- opened devtools and checked localStorage - the admin key was gone
- tried to go back to /admin/dashboard and got 404 error
- no popup asking "are you sure?" - just logged out immediately
- tested from different admin pages (dashboard, client management) - same behavior everywhere

**Observed Behaviors:**
- Button click logs out instantly
- No confirmation dialog
- localStorage cleared
- Navigation to / (home)
- Admin routes become inaccessible

**Edge Cases Tested:**
- Logout from different admin pages (dashboard, client list, client detail)
- Logout and try to navigate back to admin routes

**Error Conditions Tested:**
- None specific to logout (it's a simple action)

**Unexpected Behaviors:**
- No logout confirmation (expected a confirmation dialog for such a destructive action)
- 404 error when accessing admin routes after logout (expected redirect to login)

**Quality Requirements:**
- Observable behaviors only
- Clear, specific descriptions  
- Organized by workflow sequence
- Document unexpected behaviors for future investigation

**Output Format:**
Use template: Feature_Observation_Template.md
```

### AI Output (Generated Using This Skill)

```markdown
# Feature Observation: Admin Logout

## Test Metadata

**Feature Name:** Admin Logout  
**Observation Date:** 2026-02-06  
**Observer:** Shyaam  
**Test Environment:**
- Browser: Chrome v120
- Operating System: macOS
- System: Production (sambhava.org)
- Testing Method: Manual black-box testing

---

## Feature Description (High-Level)

Admin Logout allows authenticated admin users to end their session and return to the public home page.

---

## Observed Behaviors

### 1. Logout UI Control

**Location:** Header component, far right position  
**Appearance:** Icon button (specific icon not documented in notes)  
**Interaction:**
- Hover state: Tooltip displays "Logout" text
- Click behavior: Single click triggers logout action

### 2. Logout Action Sequence

**User Action:** Click logout button  
**System Response:**
1. No confirmation dialog appears
2. Logout executes immediately
3. User navigated to `/` (home page)
4. Admin session terminated

### 3. Session State Changes

**Observable in Browser DevTools (Application tab):**
- Before logout: localStorage key `isAdminLoggedIn` exists
- After logout: localStorage key `isAdminLoggedIn` removed completely

### 4. Post-Logout Authorization Behavior

**Test:** Navigate to `/admin/dashboard` after logout  
**Result:** 404 error page displayed  
**Interpretation:** Admin routes become inaccessible after logout

### 5. Consistency Across Admin Pages

**Test:** Logout from different admin pages
- Logout from Admin Dashboard → Same behavior
- Logout from Client Management → Same behavior  
- Logout from Client Detail → Same behavior

**Result:** Logout behavior consistent regardless of origin page

---

## Edge Cases Observed

### Edge Case 1: Logout from Different Admin Pages
**Scenario:** User initiates logout while on various admin screens  
**Observation:** Logout behavior identical across all admin pages tested  
**Conclusion:** Implementation appears consistent

---

## Error Conditions Observed

No error conditions specific to logout functionality identified during testing.

**Note:** Logout is a simple action with minimal failure modes in current implementation.

---

## Unexpected or Surprising Behaviors

### 1. No Logout Confirmation Dialog
**Expected:** Confirmation prompt ("Are you sure you want to log out?")  
**Observed:** Immediate logout with no confirmation  
**Impact:** User could accidentally logout with single misclick

### 2. 404 Error on Admin Routes After Logout
**Expected:** Redirect to login page when accessing admin routes  
**Observed:** 404 error page displayed  
**Impact:** User experience issue - error suggests page doesn't exist rather than access denied

---

## Questions for Code Investigation

1. Why is logout implemented identically in multiple components? (code duplication concern)
2. Is there any server-side session invalidation, or is logout purely client-side?
3. Why do admin routes return 404 instead of redirecting to login?
4. Is the lack of confirmation intentional, or should it be added?

---

## Testing Limitations

**Not tested:**
- Logout with multiple browser tabs open (session behavior across tabs)
- Logout with slow/failed network (does localStorage clear even if navigation fails?)
- Logout from mobile devices or different browsers

**Reason:** Initial feature observation focused on core happy path and basic edge cases.

---

## Next Steps

1. **Code Investigation:** Understand technical implementation (Skill 3)
2. **Boundary Definition:** Determine logout scope vs route protection (Skill 2)
3. **Requirements Documentation:** Create DS → FRS → URS based on these observations

---

**Observer Signature:** Shyaam  
**Date:** 2026-02-06
```

---

## Quality Criteria for This Skill

### Good Output Includes:

✅ **Observable facts only** (no speculation about implementation)  
✅ **Clear workflow sequence** (what happens in order)  
✅ **Specific details** (exact UI elements, messages, navigation targets)  
✅ **Edge cases documented** (boundary conditions tested)  
✅ **Unexpected behaviors flagged** (surprises for investigation)  
✅ **Questions raised** (what to investigate in code)  
✅ **Testing limitations acknowledged** (what wasn't tested)

### Poor Output Includes:

❌ **Implementation assumptions** ("uses JWT tokens" - can't observe this in black-box testing)  
❌ **Vague descriptions** ("logout works fine" - not specific enough)  
❌ **Missing edge cases** (only happy path documented)  
❌ **Mixed observation and requirements** (what IS vs what SHOULD BE)  
❌ **Hallucinated behaviors** (AI inventing features not in your notes)

---

## Human Verification Checklist

After AI generates Feature Observation document using this skill:

### Step 1: Completeness Check
- [ ] All behaviors from my raw notes are documented?
- [ ] No behaviors are missing?
- [ ] All edge cases I tested are included?
- [ ] All error conditions I tested are included?

### Step 2: Accuracy Check
- [ ] Every statement is factually correct?
- [ ] No hallucinated behaviors AI invented?
- [ ] Descriptions match what I actually observed?
- [ ] Technical details accurate (localStorage keys, routes, etc.)?

### Step 3: Clarity Check
- [ ] Descriptions are specific and unambiguous?
- [ ] Someone else could understand what system does from this doc?
- [ ] Workflow sequence is clear?
- [ ] No confusing or contradictory statements?

### Step 4: Scope Check
- [ ] Document sticks to observations only (no requirements creep)?
- [ ] No speculation about implementation?
- [ ] Clearly distinguishes observed vs expected behaviors?

### Step 5: Metadata Check
- [ ] Test date, tester, environment documented?
- [ ] Observer signature present?
- [ ] Template structure followed?

**If all checks pass:** ✅ Approve document  
**If any check fails:** Edit document or regenerate with improved prompt

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Mixing Observation with Interpretation

**Bad:**
> "System validates credentials against database"

**Why bad:** You can't observe database queries in black-box testing

**Good:**
> "After entering credentials and clicking Submit, system displays 'Invalid credentials' error message"

**Fix:** Stick to what you can SEE, HEAR, or MEASURE

---

### Pitfall 2: Incomplete Edge Case Documentation

**Bad:**
> "Logout works from dashboard"

**Why bad:** Doesn't document whether it works from OTHER pages

**Good:**
> "Logout tested from 3 admin pages: Dashboard, Client Management, Client Detail. Behavior identical in all cases."

**Fix:** Document what you tested AND what you didn't test

---

### Pitfall 3: Vague Descriptions

**Bad:**
> "Error message appears when login fails"

**Why bad:** Doesn't specify WHAT error message

**Good:**
> "Browser alert displays: 'sambhava.org says Invalid credentials. Use username: admin, password: password'"

**Fix:** Include exact text, UI elements, navigation targets

---

### Pitfall 4: Hallucinated Features

**Watch for:** AI adding behaviors you never mentioned in raw notes

**Example:**
- You said: "Clicked logout, went to home page"
- AI wrote: "User session is encrypted using AES-256 and invalidated server-side"

**Fix:** Cross-check AI output against your raw notes - every statement should trace to something YOU observed

---

## Template Reference

**Template Location:** `Feature_Observation_Template.md`

**Key Sections:**
1. Test Metadata (who, when, where, how)
2. Feature Description (high-level overview)
3. Observed Behaviors (detailed workflow)
4. Edge Cases Observed
5. Error Conditions Observed
6. Unexpected Behaviors
7. Questions for Code Investigation
8. Testing Limitations
9. Next Steps

**Usage:** AI should follow this template structure when organizing your raw notes.

---

## Success Metrics

**You've successfully used this skill when:**

1. ✅ Raw testing notes transformed into structured document
2. ✅ All observations are factually correct
3. ✅ Document is clear enough for someone else to understand system behavior
4. ✅ Downstream validation activities can proceed with confidence
5. ✅ Document passes all verification checklist items

---

## Related Skills

**Upstream:** None (this is the first skill in validation workflow)  
**Downstream:**
- Skill 2: Scope Boundary Analyzer (uses Feature Observation to define scope)
- Skill 3: Technical Investigator (answers questions raised in Feature Observation)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial skill created based on Login and Logout feature validation experience |

---

**End of Skill 1: Feature Observation Documenter**
