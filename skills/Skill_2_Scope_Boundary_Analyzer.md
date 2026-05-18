# Skill 2: Scope Boundary Analyzer

**Validation Phase:** 2 - Feature Boundary Definition  
**Template Used:** Feature_Boundary_Template.md  
**AI Tools Compatible:** Claude, ChatGPT, Gemini, any LLM  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Helps define clear boundaries between what should be validated together (IN SCOPE) versus what should be validated separately (OUT OF SCOPE) for a specific feature.

**Problem it solves:**  
Without clear boundaries, validation projects suffer from:
- Scope creep (validating too much)
- Scope gaps (missing critical functionality)
- Unclear separation of concerns (mixing unrelated features)
- Wasted effort (re-validating same functionality across features)

**Why it matters:**  
Scope boundaries determine how much work validation requires, what risks are addressed, and how validation artifacts can be reused. Good boundaries make validation efficient; poor boundaries make it chaotic.

---

## When to Use This Skill

### Timing in Validation Workflow

```
Feature Observation Complete
        ↓
[USE THIS SKILL]
        ↓
Feature Boundary Defined
        ↓
Code Investigation (Next Phase)
```

**Use this skill when:**
- ✅ Feature Observation document is complete
- ✅ You understand what the feature does
- ✅ You need to decide validation scope before code investigation
- ✅ Multiple related features exist and boundaries are unclear

**Don't use this skill when:**
- ❌ You haven't documented observations yet
- ❌ Boundaries are obvious (simple, isolated feature)
- ❌ You're defining requirements (that's downstream)

---

## Prerequisites

**Before using this skill, you must have:**

1. **Completed Feature Observation:**
   - Document created using Skill 1
   - All behaviors documented
   - Edge cases identified
   - Questions for investigation noted

2. **Application Context:**
   - Understanding of overall application architecture
   - Knowledge of related features
   - Awareness of system boundaries

3. **Validation Constraints:**
   - Time/budget available
   - Risk tolerance
   - Regulatory requirements (if any)

---

## Domain Knowledge Embedded in This Skill

### Scope Definition Principles

**Cohesion:**
- Features that work together should be validated together
- Example: Login form + Login button + Error messages = ONE scope

**Coupling:**
- Loosely coupled features should be separate scopes
- Example: Login (authentication) vs Dashboard (authorization) = SEPARATE scopes

**Testability:**
- Scope should be testable as a unit
- Can execute tests without validating entire system

**Reusability:**
- Validate once, reference elsewhere
- Example: Session management validated with Login, referenced in Logout

### GAMP 5 Alignment

**Risk-based approach:**
- Higher risk features → narrower, more focused scope
- Lower risk features → can combine related functionality

**Proportionality:**
- Validation effort should match complexity and criticality
- Don't over-validate low-risk features

### Common Boundary Patterns

**Pattern 1: Action vs Consequence**
- IN SCOPE: The action itself (e.g., clicking Logout)
- OUT OF SCOPE: What happens after (e.g., route protection)
- Example: Logout ends session. Route protection prevents unauthorized access.

**Pattern 2: UI vs Logic**
- IN SCOPE: User-facing behavior
- OUT OF SCOPE: Internal implementation (unless safety-critical)
- Example: Form validation (UI) vs API authentication logic (separate concern)

**Pattern 3: Core vs Related**
- IN SCOPE: Core feature functionality
- OUT OF SCOPE: Related features that happen to use same components
- Example: Logout button (core) vs Header component (used by many features)

---

## How to Invoke This Skill

### Standard Invocation Pattern

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Application_Context.md
- Load: Feature_Observation_[FeatureName].md

**Skill Invocation:**
Using the Scope Boundary Analyzer skill, help me define clear boundaries for validating [FEATURE NAME].

**Feature Observations:**
[Provide link to or summary of Feature Observation document]

**Related Features:**
[List features that might overlap or interact]

**Boundary Questions:**
1. Where does [FEATURE] end and [RELATED FEATURE] begin?
2. What is core functionality vs nice-to-have?
3. What can be validated independently vs what requires full system?
4. What has been validated elsewhere and can be referenced?

**Constraints:**
- Time: [e.g., "2-3 hours for validation"]
- Risk: [e.g., "Low risk demo app" or "High risk medical device"]
- Standards: [e.g., "GAMP 5 Category 1"]

**Output Requirements:**
- IN SCOPE: List with rationale
- OUT OF SCOPE: List with rationale and reference (if validated elsewhere)
- ASSUMPTIONS: Any assumptions made in boundary definition
- RISKS: Risks of chosen boundaries

**Output Format:**
Use template: Feature_Boundary_Template.md
```

---

## Real Example: Admin Logout Feature

### Input to AI (Using This Skill)

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Application_Context.md
- Load: Feature_Observation_Logout.md

**Skill Invocation:**
Using the Scope Boundary Analyzer skill, help me define clear boundaries for validating Admin Logout.

**Feature Observations:**
From Feature_Observation_Logout.md:
- Logout button in header (far right)
- Single click logs out immediately, no confirmation
- localStorage key "isAdminLoggedIn" deleted
- Navigation to home page (/)
- After logout, /admin/dashboard returns 404

**Related Features:**
1. Admin Login (session creation - already validated)
2. Route Protection (404 behavior on unauthorized access)
3. Header Component (logout button lives here)
4. Session Management (localStorage handling)

**Boundary Questions:**
1. Where does Logout end and Route Protection begin?
2. Is the 404 behavior part of Logout or separate authorization?
3. Should Header component be validated with Logout?
4. Is localStorage management part of Logout or Session Management?

**Constraints:**
- Time: Target 2-3 hours for Logout validation
- Risk: Low (demo application, not production medical device)
- Standards: GAMP 5 Category 1 approach

**Output Requirements:**
- Clear IN SCOPE vs OUT OF SCOPE with strong rationale
- Explain boundary decisions (why Logout ends HERE, not THERE)
- Identify what can reference Login validation artifacts
- Flag any residual risks from scope choices

**Output Format:**
Use template: Feature_Boundary_Template.md
```

### AI Output (Generated Using This Skill)

```markdown
# Feature Boundary Definition: Admin Logout

## Feature Name
Admin Logout

## Boundary Analysis Date
2026-02-06

## Analyst
Shyaam (with AI assistance)

---

## IN SCOPE: Admin Logout Validation

### 1. Logout Action Trigger
**What:** UI control that initiates logout  
**Rationale:** Core logout functionality - without trigger, no logout possible  
**Includes:**
- Logout button presence and location
- Button accessibility (hover state, tooltip)
- Click behavior

### 2. Session Termination
**What:** Ending the admin session  
**Rationale:** Core logout function - this IS logout  
**Includes:**
- localStorage key deletion (`isAdminLoggedIn`)
- Session state change from authenticated → unauthenticated
- No lingering session artifacts

### 3. Post-Logout Navigation
**What:** Where user lands after logout  
**Rationale:** Logout completes with navigation; part of logout UX  
**Includes:**
- Navigation target (home page `/`)
- Navigation behavior (immediate redirect)

### 4. Logout Consistency
**What:** Logout behavior across different admin pages  
**Rationale:** Validate implementation consistency  
**Includes:**
- Logout from Dashboard
- Logout from Client Management
- Logout from Client Detail pages

---

## OUT OF SCOPE: Not Part of Logout Validation

### 1. Route Protection / Authorization (404 Behavior)
**What:** Preventing unauthorized access to admin routes  
**Rationale:** Separate concern - this is "locked doors after light switch is off"  
**Boundary:** Logout ends when session is terminated and navigation completes.  
Route protection is the NEXT system behavior (access control).  
**Validation Status:** Deferred to separate Route Protection / Authorization validation  
**Residual Risk:** LOW - observed that it works, formal validation deferred

### 2. Admin Login (Session Creation)
**What:** How sessions are created  
**Rationale:** Already validated in Login feature validation  
**Reference:** See Login validation artifacts (URS_Login, FRS_Login, OQ_Protocol_Login)  
**Why separate:** Login = "turn light on", Logout = "turn light off". Inverse operations validated separately.

### 3. Header Component Layout
**What:** Header UI structure, positioning, styling  
**Rationale:** Logout happens to use Header, but Header is shared component used by many features  
**Boundary:** Validate that logout button EXISTS and is FUNCTIONAL. Don't validate Header's CSS, layout decisions, or other Header elements.  
**Validation Status:** Out of scope (UI component, not functional requirement)

### 4. Error Handling / Failure Scenarios
**What:** What happens if logout fails (network error, localStorage access denied)  
**Rationale:** Current implementation is client-side only with no failure modes observed  
**Boundary:** No error conditions identified during feature observation  
**Validation Status:** Not applicable (feature has no error handling to validate)  
**Risk Note:** Future enhancement could add error handling (would require re-validation)

### 5. Multi-Tab / Multi-Browser Session Behavior
**What:** How logout affects other open tabs or browsers  
**Rationale:** Not tested during feature observation; implementation specifics unknown  
**Boundary:** Validation limited to single-tab, single-browser scenario  
**Validation Status:** Out of scope for initial validation  
**Residual Risk:** MEDIUM - potential UX issue if user has multiple tabs open  
**Future Work:** Consider testing if becomes production feature

### 6. Server-Side Session Invalidation
**What:** Backend session cleanup  
**Rationale:** Feature observation showed purely client-side logout (no API calls)  
**Boundary:** Validate observed behavior (client-side). Server-side would be separate validation if implemented.  
**Validation Status:** Not applicable (not implemented)  
**Risk Note:** Production system should have server-side invalidation (security concern)

---

## BOUNDARY RATIONALE

### Core Principle: "Turning Off the Light Switch"

**Logout is:**
- The action of ending a session
- The immediate effects of that action (localStorage cleared, navigation)

**Logout is NOT:**
- What happens when you try to enter a room after the light is off (route protection)
- How the light was turned on (login)
- The entire electrical system (session management architecture)

### Why This Boundary Makes Sense

**1. Testability:**
- Can test logout independently without full system validation
- Clear pass/fail criteria
- Reproducible in 2-3 hours

**2. Reusability:**
- Login validation already done → reference, don't re-validate
- Route protection can be validated separately for all admin routes

**3. Risk Alignment:**
- Low-risk demo app doesn't need exhaustive validation
- Focus on core behavior, defer edge cases

**4. Efficiency:**
- Avoiding scope creep (don't validate Header, route protection, multi-tab behavior)
- Avoiding redundancy (don't re-validate Login)

---

## ASSUMPTIONS

1. **Login Validation Complete:**
   - Assume session creation (Login) already validated
   - Reference Login artifacts for session management questions

2. **Route Protection Deferred:**
   - Assume 404 behavior will be validated separately
   - Acknowledged as OUT OF SCOPE for Logout

3. **Client-Side Implementation:**
   - Assume logout remains client-side (no server API)
   - If implementation changes, re-validation required

4. **Single-Tab Usage:**
   - Assume single browser tab scenario
   - Multi-tab behavior not tested or validated

---

## RESIDUAL RISKS FROM BOUNDARY DECISIONS

### Risk 1: Route Protection Gap
**Risk:** 404 behavior after logout not formally validated  
**Severity:** LOW  
**Mitigation:** Observed during testing, works as expected. Formal validation deferred.  
**Acceptance:** Acceptable for demo application

### Risk 2: Multi-Tab Session Behavior
**Risk:** Unknown behavior if user has multiple tabs open  
**Severity:** MEDIUM  
**Mitigation:** None (out of scope)  
**Acceptance:** Acceptable for initial validation. Consider future testing if production deployment.

### Risk 3: No Server-Side Session Invalidation
**Risk:** Security vulnerability (sessions not invalidated server-side)  
**Severity:** HIGH (if production system)  
**Mitigation:** Documented as implementation limitation  
**Acceptance:** Acceptable for demo app. Production system should add server-side invalidation.

---

## BOUNDARY DEPENDENCIES

**Depends on (must exist before Logout validation):**
- Login validation complete (session creation understood)
- Application context documented (architecture understood)

**Enables (can proceed after Logout validation):**
- Route protection validation (can test unauthorized access)
- Session management validation (can validate full lifecycle)

---

## TRACEABILITY

**Upstream:**
- Feature_Observation_Logout.md (source of observations)
- Application_Context.md (application knowledge)

**Downstream (will use this boundary definition):**
- Code Investigation (Skill 3)
- Design Specifications (Skill 4)
- Functional Requirements (Skill 5)
- User Requirements (Skill 6)
- Test Protocol (Skill 7)

---

## APPROVAL

**Boundary Definition Approved By:** Shyaam  
**Date:** 2026-02-06  
**Rationale:** Boundaries align with risk-based approach, enable efficient validation, and create clear separation of concerns.

---

**End of Feature Boundary Definition: Admin Logout**
```

---

## Quality Criteria for This Skill

### Good Output Includes:

✅ **Clear IN SCOPE list** with strong rationale for each item  
✅ **Clear OUT OF SCOPE list** explaining WHY excluded  
✅ **Boundary rationale** explaining the core principle  
✅ **Assumptions documented** (what you're taking for granted)  
✅ **Residual risks** from scope decisions  
✅ **Dependencies** (what must exist before/after)

### Poor Output Includes:

❌ **Vague boundaries** ("validate logout feature" - too general)  
❌ **Missing rationale** (lists items without explaining WHY)  
❌ **Scope creep** (including everything remotely related)  
❌ **Scope gaps** (missing core functionality)  
❌ **No risk acknowledgment** (pretending boundaries have no trade-offs)

---

## Human Verification Checklist

After AI generates Feature Boundary document using this skill:

### Step 1: Completeness Check
- [ ] All core functionality in IN SCOPE?
- [ ] All exclusions in OUT OF SCOPE with rationale?
- [ ] Assumptions documented?
- [ ] Residual risks identified?

### Step 2: Logic Check
- [ ] Boundaries make logical sense?
- [ ] IN SCOPE items are actually related?
- [ ] OUT OF SCOPE items truly separate concerns?
- [ ] No obvious gaps or overlaps?

### Step 3: Testability Check
- [ ] Can validate IN SCOPE items independently?
- [ ] Clear pass/fail criteria possible?
- [ ] Scope is achievable within time/budget constraints?

### Step 4: Risk Check
- [ ] Residual risks acceptable?
- [ ] High-risk items not excluded?
- [ ] Risk level aligns with application criticality?

### Step 5: Traceability Check
- [ ] References to Feature Observation correct?
- [ ] Dependencies on other validations clear?
- [ ] Future validation needs identified?

**If all checks pass:** ✅ Approve boundaries and proceed  
**If any check fails:** Refine boundaries before proceeding

---

## Common Pitfalls and How to Avoid Them

### Pitfall 1: Kitchen Sink Scope (Too Broad)

**Bad:**
> IN SCOPE: Logout, Login, Session Management, Route Protection, Header Component, Error Handling, Multi-Browser Support

**Why bad:** Trying to validate everything at once - inefficient and risky

**Good:**
> IN SCOPE: Logout action, session termination, post-logout navigation  
> OUT OF SCOPE: Login (separate), Route Protection (separate), Header (UI component)

**Fix:** Apply "cohesion" test - does everything HAVE to be validated together?

---

### Pitfall 2: Swiss Cheese Scope (Gaps)

**Bad:**
> IN SCOPE: Logout button  
> (Missing: What happens when you CLICK logout button)

**Why bad:** Validates trigger but not the actual function

**Good:**
> IN SCOPE: Logout trigger (button), session termination (action), post-logout state (result)

**Fix:** Trace end-to-end workflow - from user action to final system state

---

### Pitfall 3: No Rationale (Just Lists)

**Bad:**
> IN SCOPE:
> - Logout button
> - Session termination
> 
> OUT OF SCOPE:
> - Route protection

**Why bad:** No explanation of WHY these boundaries were chosen

**Good:**
> IN SCOPE: Session termination  
> RATIONALE: This IS logout - ending the session  
> 
> OUT OF SCOPE: Route protection  
> RATIONALE: Separate concern - access control after logout, not part of logout action itself

**Fix:** Every boundary decision needs a "why" - explain your reasoning

---

### Pitfall 4: Ignoring Residual Risks

**Bad:**
> OUT OF SCOPE: Multi-tab behavior  
> (No mention of risk)

**Why bad:** Pretending exclusions have no consequences

**Good:**
> OUT OF SCOPE: Multi-tab behavior  
> RESIDUAL RISK: MEDIUM - User may have unexpected UX if multiple tabs open  
> ACCEPTANCE: Acceptable for demo app; future work if production deployment

**Fix:** Acknowledge trade-offs - every OUT OF SCOPE decision has a residual risk

---

## Template Reference

**Template Location:** `Feature_Boundary_Template.md`

**Key Sections:**
1. IN SCOPE (what to validate with rationale)
2. OUT OF SCOPE (what not to validate with rationale)
3. Boundary Rationale (core principle)
4. Assumptions
5. Residual Risks
6. Dependencies
7. Traceability
8. Approval

**Usage:** AI should follow this structure when defining boundaries

---

## Success Metrics

**You've successfully used this skill when:**

1. ✅ Clear, defensible boundaries defined
2. ✅ All stakeholders understand what will/won't be validated
3. ✅ Scope is testable within constraints
4. ✅ Residual risks acknowledged and accepted
5. ✅ Downstream validation activities can proceed with clarity

---

## Related Skills

**Upstream:**
- Skill 1: Feature Observation Documenter (provides observations for boundary analysis)

**Downstream:**
- Skill 3: Technical Investigator (investigates IN SCOPE items only)
- Skill 4-7: Requirements & Testing (limited to defined scope)

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-02-08 | Initial skill created based on Login and Logout boundary definition experience |

---

**End of Skill 2: Scope Boundary Analyzer**
