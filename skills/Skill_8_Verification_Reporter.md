# Skill 8: Verification Reporter

**Validation Phase:** 6 - Verification  
**Template Used:** Verification_Report_Template.md  
**AI Tools Compatible:** Claude, ChatGPT, Gemini, any LLM  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Documents how AI-generated outputs were verified by humans before approval, creating audit trail and accountability.

**Problem it solves:**  
Using AI without verification documentation creates audit risk. Verification Reports provide:
- Evidence of human review
- Documentation of verification methods
- Confidence levels for decisions
- Accountability trail

**Why it matters:**  
"Trust but verify" principle. Auditors need proof that AI outputs were validated, not blindly accepted. Verification Reports are the proof.

---

## When to Use This Skill

```
AI Generates Output (Any Phase)
        ↓
Human Performs Verification
        ↓
[USE THIS SKILL]
        ↓
Verification Documented
        ↓
Output Approved (or Rejected)
```

**Use when:**
- ✅ After AI generates any validation artifact
- ✅ Before approving AI output for use
- ✅ When audit trail is required

---

## Domain Knowledge Embedded

### Verification Principles

**Three Error Types:**

1. **Commission Errors (False Claims):**
   - AI claims something that isn't true
   - Example: "Logout calls /api/logout" but no API call exists
   - Check: Verify every factual claim

2. **Omission Errors (Missing Info):**
   - AI misses something important
   - Example: AI finds 2 logout implementations, misses 3rd
   - Check: Search for what AI might have missed

3. **Scope Errors (Boundary Violations):**
   - AI investigates/documents out-of-scope items
   - Example: Asked for Logout, AI documents entire session management
   - Check: Compare output to defined scope

### Verification Methods

**Code Review:**
- Manual inspection of code files
- Compare AI descriptions to actual code
- Check file paths and line numbers

**Manual Testing:**
- Execute feature in browser
- Verify AI claims about behavior
- Check error conditions

**Traceability Check:**
- Verify requirement mapping correct
- Confirm no orphaned requirements
- Check bidirectional traceability

**Template Compliance:**
- Verify output follows template structure
- Check all required sections present
- Confirm format consistency

### Confidence Levels

**High:** Multiple verification methods, all passed, safe to proceed  
**Medium:** Single method, passed, but limited scope  
**Low:** Limited verification, some concerns, needs more work  
**Deferred:** Not verified (risk accepted, documented)

---

## How to Invoke This Skill

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: [AI_Generated_Document].md (document being verified)
- Load: [Source_Documents] (Feature Observation, Code Investigation, etc.)

**Skill Invocation:**
Using the Verification Reporter skill, document the verification process for [AI-GENERATED DOCUMENT].

**Verification Context:**

**Document Being Verified:**
- Name: [e.g., Code_Investigation_Logout.md]
- Created By: AI (Claude Code)
- Created Date: [date]
- Purpose: [what this document is for]

**Verification Performed:**

1. **Commission Error Check:**
   - Method: [e.g., Manual code review]
   - What I checked: [list factual claims verified]
   - Results: [PASS/FAIL with details]

2. **Omission Error Check:**
   - Method: [e.g., File search for "logout" keyword]
   - What I checked: [completeness verification]
   - Results: [PASS/FAIL with details]

3. **Scope Accuracy Check:**
   - Method: [e.g., Compare output to Feature Boundary doc]
   - What I checked: [IN SCOPE vs OUT OF SCOPE adherence]
   - Results: [PASS/FAIL with details]

**Findings:**
- Commission errors found: [count, describe if any]
- Omission errors found: [count, describe if any]
- Scope violations found: [count, describe if any]

**Confidence Assessment:**
- Overall confidence: [High / Medium / Low]
- Rationale: [why this confidence level]

**Decision:**
- Approved for use? [YES / NO / CONDITIONAL]
- Action taken: [what was done based on verification]
- Approver: [human name]
- Date: [approval date]

**Output Format:**
Use template: Verification_Report_Template.md
```

---

## Quality Criteria

✅ All three error types checked (commission, omission, scope)  
✅ Verification methods documented  
✅ Findings clearly stated  
✅ Confidence level assigned with rationale  
✅ Human accountability clear (name, date, decision)

---

## Human Verification Checklist

### Step 1: Commission Check
- [ ] Identified all factual claims in AI output
- [ ] Verified each claim through independent method
- [ ] Documented verification results
- [ ] No false claims found (or flagged if found)

### Step 2: Omission Check
- [ ] Reviewed AI output for completeness
- [ ] Compared against source materials
- [ ] Searched for potentially missed items
- [ ] No critical omissions (or flagged if found)

### Step 3: Scope Check
- [ ] Compared output to defined scope
- [ ] Verified IN SCOPE items covered
- [ ] Verified OUT OF SCOPE items not included
- [ ] No scope violations (or flagged if found)

### Step 4: Confidence Assessment
- [ ] Multiple verification methods used? (High confidence)
- [ ] All checks passed? (High confidence)
- [ ] Any uncertainties remaining? (Medium/Low confidence)
- [ ] Confidence level appropriate?

### Step 5: Decision Documentation
- [ ] Clear approve/reject/conditional decision
- [ ] Rationale for decision documented
- [ ] Human name and date recorded
- [ ] Action taken specified

**If all checks pass with HIGH confidence:** ✅ Approve  
**If checks pass with MEDIUM confidence:** ⚠️ Conditional approval, document limitations  
**If any check fails with LOW confidence:** ❌ Reject, require revision or additional verification

---

## Common Pitfalls

### Pitfall 1: Skipping Verification (Trust Without Verify)
**Bad:** AI generates document → immediately use it  
**Fix:** ALWAYS verify before approval, document verification

### Pitfall 2: Single-Method Verification
**Bad:** Only code review, no manual testing  
**Fix:** Use multiple methods for HIGH confidence

### Pitfall 3: No Confidence Assessment
**Bad:** Verify but don't assign confidence level  
**Fix:** Always state confidence (High/Medium/Low) with rationale

### Pitfall 4: Missing Accountability
**Bad:** "Verified" with no human name/date  
**Fix:** Always sign and date verification decisions

---

## Template Reference

**Template:** Verification_Report_Template.md  
**Sections:** Verification Methods, Findings, Confidence, Decision, Accountability

---

## Success Metrics

**Successful verification when:**
1. ✅ All error types checked
2. ✅ Methods documented
3. ✅ Confidence assessed
4. ✅ Decision clear
5. ✅ Human accountability present
6. ✅ Audit trail complete

---

## Related Skills

**Applies to outputs from:**
- All skills (1-7) generate outputs requiring verification
- This skill documents the verification process

---

**End of Skill 8: Verification Reporter**
