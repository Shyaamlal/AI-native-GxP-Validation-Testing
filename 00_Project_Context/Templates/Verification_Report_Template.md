# Verification Report: [Feature Name]

**Purpose:** Verify accuracy and completeness of AI-generated code investigation findings before using them in validation documentation.

**Investigation Source:** [Name of investigation document] (Tool used - Date)  
**Verification Date:** [YYYY-MM-DD]  
**Verified By:** [Your name]  
**Method:** Manual testing, code inspection, and completeness analysis

---

## Investigation Claims to Verify

[AI tool name] investigated the [feature name] and made the following claims about implementation:

1. [Claim 1 - e.g., "Authentication is 100% client-side (no backend API)"]
2. [Claim 2 - e.g., "Credentials hardcoded: username='admin', password='password'"]
3. [Claim 3 - e.g., "Session stored in localStorage with key 'isAdminLoggedIn'"]
4. [Claim 4 - e.g., "No route protection on admin pages"]
5. [Add all major claims from investigation]

**Purpose of verification:** Confirm these claims are accurate and complete before using them to write Design Specification (DS).

---

## Verification Test Results

### Test 1: [Claim Description]

**Claim:** "[Exact quote from investigation]"

**Test Method:**
- [Describe how you verified this - e.g., "Open DevTools → Network tab, attempt login, observe requests"]

**Expected if claim is true:** [Specific observable outcome]

**Actual Result:**
[Document exactly what you observed]

**Evidence:**
[Screenshot reference, code snippet location, or detailed notes]

**Conclusion:** ✅ Verified / ❌ Incorrect / ⚠️ Partially Correct

**Notes:**
[Any additional observations, uncertainties, or context]

---

### Test 2: [Claim Description]

**Claim:** "[Exact quote from investigation]"

**Test Method:**
[How you verified]

**Expected if claim is true:** [Expected outcome]

**Actual Result:**
[What you observed]

**Evidence:**
[Reference]

**Conclusion:** ✅ Verified / ❌ Incorrect / ⚠️ Partially Correct

**Notes:**
[Any additional context]

---

[Repeat for each major claim - typically 3-5 commission error tests]

---

## Completeness Verification (Omission Errors)

### Objective
Verify that AI investigation didn't miss relevant files, features, or implementation details.

### Files Analyzed by AI

**From investigation report:**
[List all files that AI documented analyzing]

**Total files analyzed:** [Count]

---

### Completeness Check Method

**Select ONE method and document thoroughly:**

#### Method 1: Full File Inventory ✅ Most Rigorous
- [ ] Generated complete list of all files in codebase
- [ ] Filtered list to potentially relevant files (by location, name, or content)
- [ ] Compared filtered list against AI's analyzed files
- [ ] Manually reviewed any files AI didn't analyze to confirm they're not relevant
- **Files in codebase (potentially relevant):** [Count]
- **Files analyzed by AI:** [Count]
- **Files missed by AI:** [List or "None"]
- **Confidence level:** High

#### Method 2: Keyword Search 🔍 Medium Rigor
- [ ] Searched codebase for keywords related to feature
- [ ] Keywords used: [List - e.g., "login|auth|admin"]
- [ ] Compared search results against AI's analyzed files
- [ ] AI found additional files beyond keyword search? [Yes/No - list them]
- **Files found by keyword search:** [Count]
- **Files analyzed by AI:** [Count]
- **Assessment:** AI exceeded/matched/missed keyword search
- **Confidence level:** Medium

#### Method 3: Manual Sampling 📊 Lower Rigor
- [ ] Randomly sampled [N] files not in AI's analysis
- [ ] Checked if any contain relevant feature code
- [ ] Relevant files found in sample: [Count]
- [ ] Extrapolated potential missed files: [Estimate]
- **Confidence level:** Low to Medium

#### Method 4: Deferred Verification ⚠️ Risk Accepted
- [ ] Omission verification deferred to test execution phase
- [ ] Rationale: [Why deferring - e.g., "low-risk feature, time constraints"]
- [ ] Will verify during: [When - e.g., "OQ test execution"]
- **Confidence level:** Pending

---

### Completeness Analysis

**Files AI analyzed that keyword search missed:**
[List files AI found beyond basic search - shows AI thoroughness]

**Potentially relevant files AI might have missed:**
[List any files you found that AI didn't document]

**Coverage Assessment:**
- AI analysis appears: ✅ Comprehensive / ⚠️ Adequate / ❌ Incomplete
- Rationale: [Explain your assessment]

**Missing areas identified:**
[List any aspects of the feature that may not have been investigated]

---

## Overall Verification Summary

### Commission Errors (False Claims)

**Claims tested:** [Count]  
**Claims verified as accurate:** [Count]  
**Claims found incorrect:** [Count]  
**Partially correct claims:** [Count]

**Commission Accuracy:** [X]% ✅ / ⚠️ / ❌

---

### Omission Errors (Missed Items)

**Verification method used:** [Full Inventory / Keyword Search / Sampling / Deferred]

**Completeness assessment:**
- Files/areas analyzed by AI: [Count or description]
- Files/areas verified as complete: [Assessment]
- Known gaps identified: [List or "None identified"]

**Omission Confidence Level:** High / Medium / Low / Pending

**Rationale for confidence level:**
[Explain why you have this confidence level based on verification method used]

---

### Scope Assessment

**AI correctly identified feature boundaries:** ✅ Yes / ❌ No / ⚠️ Partially

**Evidence:**
- AI included relevant files: [Assessment]
- AI excluded non-feature files: [Assessment]  
- AI distinguished this feature from related features: [Assessment]

**Scope issues identified:**
[Any cases where AI conflated features or missed boundaries]

---

## Final Assessment

### Overall Confidence Level

**Select one:**
- ✅ **HIGH** - Commission accuracy 100%, omission verification comprehensive, scope correct
- ⚠️ **MEDIUM** - Minor issues found but corrected, or omission verification adequate but not comprehensive
- ❌ **LOW** - Significant issues found, or omission verification insufficient

**Selected:** [High / Medium / Low]

---

### Rationale

[Explain your confidence assessment based on:
- Commission test results
- Omission verification method and findings
- Scope accuracy
- Any corrections needed]

---

### Decision

**Select one:**

✅ **PROCEED to Design Specification (DS) documentation**
- AI investigation findings are sufficiently accurate and complete
- Any issues identified have been documented and corrected
- Confidence level supports using findings as DS foundation

⚠️ **PROCEED WITH CAUTION**
- Some gaps identified but acceptable for current risk level
- Document assumptions and limitations in DS
- Plan to verify during test execution

❌ **DO NOT PROCEED - Additional investigation required**
- Significant inaccuracies or gaps found
- Re-investigation needed before documentation
- List specific areas requiring additional work: [List]

**Decision:** [Proceed / Proceed with Caution / Do Not Proceed]

---

## Key Learnings

### What Worked Well
[Document successful aspects of verification approach]

### Process Improvements for Future Features
[Note any better methods or approaches discovered]

### Confidence in AI-Assisted Approach
[Reflect on whether AI investigation + verification is working effectively]

---

## Action Items

**Before proceeding to DS:**
- [ ] [Any corrections needed to investigation findings]
- [ ] [Any additional verification needed]
- [ ] [Any assumptions to document]

**During DS writing:**
- [ ] [Any specific areas to handle carefully based on verification findings]
- [ ] [Any design aspects requiring special attention]

**For future validations:**
- [ ] [Process improvements to implement]
- [ ] [Verification method refinements]

---

## Verification Evidence Archive

**Evidence collected during verification:**
- Screenshots: [Location or description]
- Code snippets: [Location]
- Browser DevTools observations: [Summary]
- Manual test results: [Summary]
- File listings: [Location]

**Evidence retention:**
[Where evidence is stored for audit purposes]

---

## Document Metadata

**Author:** [Your name]  
**Created:** [YYYY-MM-DD]  
**Status:** Portfolio Demonstration  
**Version Control:** Git repository

---

## Change Log

Significant changes to this document:

| Date | Change Rationale |
|------|------------------|
| [YYYY-MM-DD] | Initial verification of [Feature] investigation |

*Note: In regulated environments, formal review/approval workflows would be managed through organizational QMS. This portfolio demonstrates validation methodology, not regulatory submission.*

---

## Notes

**Purpose reminder:** This verification establishes ground truth before writing requirements documentation. It catches AI errors early and builds confidence in AI-assisted validation approach.

**Quality over speed:** Invest time in thorough verification - it prevents cascading errors in all downstream documentation (DS, FRS, URS, OQ Protocol).

**Document what you don't know:** If verification reveals uncertainties, document them explicitly rather than making assumptions. Unknowns can be resolved during test execution.

**Verification is a validation tester's core skill:** Healthy skepticism about AI completeness and accuracy is exactly what makes this approach audit-ready and professionally rigorous.