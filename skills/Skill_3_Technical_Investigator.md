# Skill 3: Technical Investigator

**Validation Phase:** 3 - Code Investigation  
**Template Used:** Code_Investigation_Template.md  
**AI Tools Compatible:** Claude Code (primary), Claude, ChatGPT with code access  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Uses AI to investigate source code and document technical implementation details needed for creating Design Specifications and understanding how a feature actually works.

**Problem it solves:**  
Manual code investigation is time-consuming and error-prone, especially for:
- Large codebases with unclear structure
- Unfamiliar technologies or frameworks
- Finding all files related to a feature
- Understanding implementation patterns

**Why it matters:**  
Code investigation bridges the gap between observable behavior (from Skill 1) and technical specifications (for Skill 4). Without accurate code understanding, Design Specifications will be wrong, leading to cascading errors in all downstream documentation.

---

## When to Use This Skill

### Timing in Validation Workflow

```
Feature Boundary Defined
        ↓
[USE THIS SKILL]
        ↓
Code Investigation Complete
        ↓
Design Specification (Skill 4)
```

**Use this skill when:**
- ✅ Feature boundaries are defined (you know what to investigate)
- ✅ You have code access
- ✅ You need technical details for Design Specifications
- ✅ You want to verify observed behaviors trace to code

**Don't use this skill when:**
- ❌ You don't have code access (black-box validation only)
- ❌ Boundaries aren't defined yet (might investigate wrong things)
- ❌ System is pure COTS/SaaS (no code to investigate)

---

## Prerequisites

**Before using this skill, you must have:**

1. **Code Access:**
   - Source code available locally or remotely
   - Ability to navigate codebase
   - Understanding of repository structure (if known)

2. **Feature Context:**
   - Feature Observation document (Skill 1)
   - Feature Boundary definition (Skill 2)
   - Clear investigation questions

3. **AI Tool Setup:**
   - Claude Code installed (for local investigation)
   - OR Claude/ChatGPT with code viewing capability
   - Repository cloned and accessible

---

## Domain Knowledge Embedded in This Skill

### Code Investigation Principles

**Follow the Execution Path:**
- Start at UI (user action)
- Follow to event handlers
- Trace to business logic
- Track to data layer
- Map return path to UI

**Ask Implementation Questions:**
- WHERE is functionality implemented? (file paths, components)
- WHAT does the code do? (step-by-step logic)
- HOW is it implemented? (technical approach, patterns)
- WHY this approach? (design decisions visible in code)

**Verify Observations:**
- Does code match observed behavior?
- Are there hidden features not observed in testing?
- Are there dead code paths or unused logic?

### GAMP 5 Alignment

**Category 1 Tool:**
- AI investigates code, human verifies findings
- Human responsible for accuracy of Design Specifications
- AI outputs are hypotheses until verified

**Retrospective Validation:**
- Documenting as-built system (not designing new system)
- Code is source of truth
- Implementation drives specifications (not vice versa)

### Verification Rigor

**High Confidence Required:**
- Code investigation findings will become Design Specifications
- DS becomes source for FRS and URS
- Errors cascade through entire validation package

**Multiple Verification Methods:**
- Commission check: Did AI claim something false?
- Omission check: Did AI miss files or logic?
- Scope check: Did AI investigate beyond boundaries?

---

## How to Invoke This Skill

### Standard Invocation Pattern (Claude Code)

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Sambhava_Application_Context.md
- Load: Feature_Observation_[FeatureName].md
- Load: Feature_Boundary_[FeatureName].md

**Skill Invocation:**
Using the Technical Investigator skill, investigate the code implementation for [FEATURE NAME] and document technical details needed for Design Specifications.

**Investigation Scope:**
IN SCOPE (from Feature Boundary document):
- [List IN SCOPE items to investigate]

OUT OF SCOPE (do not investigate):
- [List OUT OF SCOPE items to avoid]

**Investigation Questions:**

1. **Implementation Location:**
   - Which files/components implement [FEATURE]?
   - What is the file structure?
   - Are there multiple implementations (code duplication)?

2. **Execution Flow:**
   - What happens when user performs [ACTION]?
   - Step-by-step code execution path
   - Which functions call which?

3. **Technical Mechanisms:**
   - How is [SPECIFIC BEHAVIOR] implemented?
   - What libraries/frameworks are used?
   - What data structures are involved?

4. **State Management:**
   - How is state stored? (localStorage, cookies, session, database)
   - Where is state modified?
   - What triggers state changes?

5. **API Interactions:**
   - Are there any API calls?
   - What endpoints are used?
   - What data is sent/received?

6. **Error Handling:**
   - What error conditions are handled in code?
   - What error messages can be triggered?
   - Are there try-catch blocks or error boundaries?

7. **Security Controls:**
   - What security mechanisms are visible in code?
   - Authentication/authorization patterns
   - Input validation or sanitization

8. **Code Quality Observations:**
   - Code duplication?
   - Consistent patterns or inconsistencies?
   - Dead code or unused functions?

**Verification Requirements:**
- Provide file paths and line numbers for all findings
- Include code snippets for key implementation details
- Flag any uncertainties or ambiguities
- Note any discrepancies between code and observed behavior

**Output Format:**
Use template: Code_Investigation_Template.md
```

---

## Real Example: Admin Logout Feature

### Input to AI (Using This Skill with Claude Code)

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Sambhava_Application_Context.md  
- Load: Feature_Observation_Logout.md
- Load: Feature_Boundary_Logout.md

**Skill Invocation:**
Using the Technical Investigator skill, investigate the code implementation for Admin Logout and document technical details.

**Investigation Scope:**

IN SCOPE:
- Logout action trigger (button/UI control)
- Session termination mechanism (localStorage handling)
- Post-logout navigation

OUT OF SCOPE:
- Route protection (404 behavior - separate feature)
- Login implementation (already validated)
- Header component layout (UI concern, not functional)

**Investigation Questions:**

1. **Implementation Location:**
   - Where is logout functionality implemented?
   - How many files contain logout code?
   - Is there code duplication?

2. **Execution Flow:**
   - What happens when logout button is clicked?
   - Step-by-step code path from click to completion

3. **Session Termination:**
   - How is localStorage managed?
   - What keys are modified?
   - Any server-side session invalidation?

4. **Navigation:**
   - How is post-logout navigation implemented?
   - What triggers navigation to home page?

5. **Consistency:**
   - Is logout implemented consistently across components?
   - Any variations in implementation?

6. **Error Handling:**
   - Any error handling for logout?
   - What happens if localStorage access fails?

**Verification Requirements:**
- Exact file paths and line numbers
- Code snippets for logout logic
- Flag any inconsistencies found

**Output Format:**
Document findings in Code_Investigation_Template.md format
```

### AI Output (Generated Using This Skill - Claude Code)

```markdown
# Code Investigation: Admin Logout

## Investigation Metadata

**Feature:** Admin Logout  
**Investigation Date:** 2026-02-06  
**Investigator:** Shyaam (with Claude Code assistance)  
**Repository:** sambhava-app (local clone)  
**Branch:** main  
**Commit:** a3f8b92 (latest)

---

## Implementation Location

### Files Containing Logout Logic

**Found 3 components with logout implementation:**

1. **src/components/AdminDashboard.tsx**
   - Lines: 45-47
   - Location: Dashboard page component

2. **src/components/ClientManagement.tsx**
   - Lines: 38-40
   - Location: Client list page component

3. **src/components/ClientDashboard.tsx**
   - Lines: 52-54
   - Location: Individual client detail page component

**Code Duplication:** ⚠️ YES - Same logout logic duplicated in 3 places

---

## Execution Flow

### Logout Sequence (All Components - Identical)

```typescript
// Example from AdminDashboard.tsx (lines 45-47)
const handleLogout = () => {
  localStorage.removeItem("isAdminLoggedIn");
  navigate("/");
};
```

**Step-by-Step:**

1. User clicks logout button/icon
2. `handleLogout()` function invoked
3. localStorage key "isAdminLoggedIn" removed
4. React Router navigate("/") called
5. User redirected to home page
6. Component unmounts

**No async operations:** Logout is synchronous

---

## Technical Implementation Details

### 1. Session Termination Mechanism

**Method:** Client-side localStorage manipulation

**Implementation:**
```typescript
localStorage.removeItem("isAdminLoggedIn");
```

**Technical Characteristics:**
- Synchronous operation (no await/promises)
- Browser localStorage API (domain-scoped)
- Key deletion (not set to false, completely removed)
- No error handling (assumes localStorage always accessible)

**Server-Side Invalidation:** ❌ NONE FOUND
- No API calls during logout
- No backend session cleanup
- Purely client-side operation

---

### 2. Post-Logout Navigation

**Method:** React Router programmatic navigation

**Implementation:**
```typescript
import { useNavigate } from 'react-router-dom';

const navigate = useNavigate();
navigate("/");
```

**Technical Characteristics:**
- React Router v6 hook pattern
- Navigate to root route ("/")
- No state passed in navigation
- No redirect configuration in route definitions

---

### 3. Logout UI Control

**Location:** Header component (`src/components/Header.tsx`)

**Implementation:**
```typescript
// Line 28-32
<button
  onClick={handleLogout}
  className="logout-button"
  title="Logout"
>
  <LogoutIcon />
</button>
```

**Technical Characteristics:**
- Button element (accessible)
- onClick handler attached
- CSS class for styling
- Title attribute for tooltip ("Logout")
- Icon component (LogoutIcon from icon library)

---

### 4. Logout Consistency Analysis

**Finding:** IDENTICAL implementation across all 3 components

**Duplication Pattern:**
```
AdminDashboard.tsx    →  handleLogout() { removeItem + navigate }
ClientManagement.tsx  →  handleLogout() { removeItem + navigate }
ClientDashboard.tsx   →  handleLogout() { removeItem + navigate }
```

**Why Duplication Exists:**
- No shared logout utility/hook
- Each component implements logout independently
- Copy-paste pattern (same function name, same logic)

**Implication:**
- If logout logic changes, must update 3 places
- Risk of inconsistency if one component updated but not others

---

## API Interactions

**Findings:** ✅ NONE

**Verification:**
- Searched codebase for API calls during logout
- Checked network logs during manual testing
- Confirmed no fetch(), axios, or HTTP requests

**Conclusion:** Logout is entirely client-side (no backend involvement)

---

## Error Handling

**Findings:** ❌ NONE

**No Error Handling For:**
- localStorage access failure (e.g., privacy mode blocking localStorage)
- Navigation failure
- Component unmount errors

**Code Pattern:**
```typescript
// No try-catch, no error checking
localStorage.removeItem("isAdminLoggedIn");  // Assumes success
navigate("/");  // Assumes navigation works
```

**Implication:**
- Logout assumes "happy path" always succeeds
- No fallback behavior if localStorage unavailable
- No user feedback if logout fails (silent failure possible)

---

## Security Controls

**Findings:** Minimal

**What's Present:**
- Session termination (removes authentication token)

**What's Missing:**
- No CSRF protection (not needed - client-side only)
- No rate limiting (logout is benign action)
- No audit logging (no record of who logged out when)
- No session timeout (logout is manual action only)

**Production Considerations:**
- Should add server-side session invalidation
- Should add audit trail for compliance
- Consider session timeout (auto-logout after inactivity)

---

## Code Quality Observations

### Issues Identified

**1. Code Duplication (HIGH):**
- Same logout logic in 3 places
- Maintenance burden
- Inconsistency risk

**2. No Error Handling (MEDIUM):**
- Silent failures possible
- Poor UX if localStorage unavailable

**3. No Server-Side Cleanup (HIGH for Production):**
- Security risk if this were production
- Sessions not invalidated server-side
- Acceptable for demo/prototype only

### Positive Patterns

**1. Consistent Implementation:**
- Despite duplication, all 3 implementations identical
- Predictable behavior

**2. Simple, Readable Code:**
- Easy to understand
- No over-engineering

**3. Uses React Best Practices:**
- Hooks (useNavigate)
- Functional components
- Event handlers

---

## Verification Results

### Commission Error Check: ✅ PASS
- All AI claims verified against actual code
- File paths confirmed correct
- Line numbers accurate
- Code snippets match source

### Omission Error Check: ✅ PASS
- Full file search conducted for "logout" keyword
- All logout implementations found
- No hidden logout logic detected

### Scope Accuracy Check: ✅ PASS
- Investigation stayed within IN SCOPE boundaries
- Did not investigate route protection (OUT OF SCOPE)
- Did not investigate login logic (OUT OF SCOPE)

**Overall Confidence:** HIGH - Safe to proceed with Design Specifications

---

## Discrepancies Between Code and Observations

**Finding:** ✅ NO DISCREPANCIES

- Feature Observation claimed: localStorage key removed → Code confirms: `removeItem("isAdminLoggedIn")`
- Feature Observation claimed: Navigate to / → Code confirms: `navigate("/")`
- Feature Observation claimed: No confirmation → Code confirms: Direct execution, no dialog

**Conclusion:** Observed behavior matches code implementation exactly

---

## Questions for Design Specification

Based on code investigation, DS should address:

1. **Why is logout client-side only?** (Design decision)
2. **Why is code duplicated in 3 components?** (Technical debt)
3. **Why no error handling?** (Acceptable for demo? Should be added?)
4. **Why no confirmation dialog?** (UX decision - intentional?)

---

## Next Steps

1. **Create Design Specifications (Skill 4):**
   - Document as-built implementation
   - Include technical decisions found in code
   - Note code quality issues as "implementation notes"

2. **Flag Issues for Future Work:**
   - Code duplication should be refactored (create shared hook)
   - Add error handling for production readiness
   - Add server-side session invalidation

---

**Investigator Sign-Off:** Shyaam  
**Verification Status:** Verified  
**Confidence Level:** High  
**Date:** 2026-02-06
```

---

## Quality Criteria for This Skill

### Good Output Includes:

✅ **Exact file paths and line numbers** (verifiable)  
✅ **Code snippets** for key implementation details  
✅ **Step-by-step execution flow** (what calls what)  
✅ **Technical mechanisms explained** (how it works)  
✅ **Verification results** (commission, omission, scope checks)  
✅ **Discrepancies flagged** (code vs observations)  
✅ **Questions raised** for Design Specifications

### Poor Output Includes:

❌ **Vague descriptions** ("logout uses localStorage" - need specifics)  
❌ **No file paths** (can't verify without locations)  
❌ **Hallucinated code** (AI inventing implementations)  
❌ **Out of scope investigation** (investigating boundary violations)  
❌ **No verification** (AI claims trusted without checking)

---

## Human Verification Checklist

After AI generates Code Investigation document using this skill:

### Step 1: File Verification
- [ ] Open each file path mentioned by AI
- [ ] Navigate to line numbers provided
- [ ] Confirm code matches AI descriptions
- [ ] Check for any files AI might have missed

### Step 2: Execution Flow Verification
- [ ] Trace execution path manually in code
- [ ] Confirm sequence matches AI description
- [ ] Verify function calls and data flow

### Step 3: Behavior Verification
- [ ] Cross-reference with Feature Observation document
- [ ] Confirm code explains observed behaviors
- [ ] Identify any discrepancies

### Step 4: Scope Verification
- [ ] Check AI stayed within IN SCOPE boundaries
- [ ] Confirm OUT OF SCOPE items not investigated
- [ ] Verify no scope creep

### Step 5: Completeness Verification
- [ ] All investigation questions answered?
- [ ] Any missing implementation details?
- [ ] Any uncertainties flagged by AI?

**If all checks pass:** ✅ Approve investigation and proceed to DS  
**If any check fails:** Re-investigate or refine findings

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Trusting AI Without Verification

**Bad:** AI says logout calls API endpoint `/api/logout` → you write DS claiming server-side invalidation

**Why bad:** AI might hallucinate API calls that don't exist

**Good:** 
1. Check code at file path AI provided
2. Search codebase for "/api/logout"
3. Run feature and check network tab
4. Verify API call exists OR flag as AI error

**Fix:** ALWAYS verify AI claims against actual code

---

### Pitfall 2: Incomplete File Search

**Bad:** AI investigates one file, misses logout in other components

**Why bad:** Incomplete picture leads to incomplete DS

**Good:**
1. Ask AI to search entire codebase for "logout" keyword
2. Check multiple locations (components, utils, services)
3. Verify all implementations found

**Fix:** Use thorough search strategies (grep, find, IDE search)

---

### Pitfall 3: Investigating Out of Scope

**Bad:** Asked to investigate Logout, AI documents entire session management architecture

**Why bad:** Wasted effort, scope creep, validates wrong features

**Good:**
1. Provide clear IN SCOPE boundaries
2. Monitor AI output for scope violations
3. Stop AI when it goes off-track

**Fix:** Reference Feature Boundary document in prompt

---

### Pitfall 4: No Confidence Assessment

**Bad:** AI provides findings, you immediately create DS without verification

**Why bad:** Cascading errors if AI made mistakes

**Good:**
1. Perform commission/omission/scope checks
2. Assign confidence level (High/Medium/Low)
3. Only proceed if HIGH confidence
4. Document verification method

**Fix:** Always include verification results in investigation document

---

## Template Reference

**Template Location:** `Code_Investigation_Template.md`

**Key Sections:**
1. Investigation Metadata
2. Implementation Location (files, lines)
3. Execution Flow (step-by-step)
4. Technical Details (how it works)
5. Verification Results (commission, omission, scope)
6. Discrepancies (code vs observations)
7. Questions for DS

**Usage:** AI should follow this structure when documenting investigation findings

---

## Tool-Specific Guidance

### Using Claude Code (Recommended)

**Strengths:**
- Direct code access
- Can search entire repositories
- Provides file paths and line numbers
- Good at explaining code logic

**Best Practices:**
- Start with broad search ("find all files mentioning logout")
- Then drill into specific files
- Ask for code snippets (not just explanations)
- Request file paths and line numbers

### Using Claude/ChatGPT (Alternative)

**Strengths:**
- Good at analyzing provided code snippets
- Can explain complex logic

**Limitations:**
- Need to manually provide code
- Can't search repository
- Requires more human effort

**Best Practices:**
- Copy relevant code files into conversation
- Ask focused questions per code snippet
- Verify findings by checking actual code

---

## Success Metrics

**You've successfully used this skill when:**

1. ✅ All investigation questions answered
2. ✅ File paths and line numbers documented
3. ✅ Code verified to match AI descriptions
4. ✅ Execution flow understood
5. ✅ HIGH confidence in findings
6. ✅ Ready to write Design Specifications

---

## Related Skills

**Upstream:**
- Skill 1: Feature Observation Documenter (provides behaviors to investigate)
- Skill 2: Scope Boundary Analyzer (defines what to investigate)

**Downstream:**
- Skill 4: Design Specification Writer (uses investigation findings)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial skill created based on Login and Logout code investigation experience |

---

**End of Skill 3: Technical Investigator**
