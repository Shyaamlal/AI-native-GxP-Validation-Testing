# Skill 7: Test Protocol Generator

**Validation Phase:** 5 - Operational Qualification (OQ) Protocol  
**Template Used:** OQ_Protocol_Template.md  
**AI Tools Compatible:** Claude, ChatGPT, Gemini, any LLM  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Transforms Functional Requirements into executable test cases that verify system behaviors match specifications.

**Problem it solves:**  
Requirements without tests = unverified claims. OQ Protocol provides:
- Systematic test coverage
- Clear test procedures
- Pass/fail criteria
- Traceability requirements → tests → results

**Why it matters:**  
OQ Protocol is validation evidence. Auditors review test execution records. Poor test protocol = failed validation, even if system works correctly.

---

## When to Use This Skill

```
Requirements Complete (URS, FRS, DS)
        ↓
[USE THIS SKILL]
        ↓
OQ Protocol Created
        ↓
Test Execution (Manual)
```

**Use when:**
- ✅ All requirements approved (URS, FRS, DS)
- ✅ Ready to define test procedures
- ✅ Need executable validation evidence

---

## Domain Knowledge Embedded

### Test Design Principles

**Traceability:**
- Every FRS must have at least one test case
- Each test case traces to FRS(s)
- Gap analysis ensures no untested requirements

**Executability:**
- Clear step-by-step procedures
- Explicit expected results
- Observable pass/fail criteria

**Completeness:**
- Happy path coverage
- Edge cases from Feature Observation
- Error conditions (if applicable)

**Repeatability:**
- Anyone can execute tests following protocol
- Same inputs → same results
- No ambiguity in procedures

### GAMP 5 OQ Standards

**Operational Qualification:**
- Tests performed in target environment
- System operating in intended manner
- Evidence documented and reviewed

**Risk-Based Testing:**
- Higher risk → more test coverage
- Lower risk → lighter testing
- Proportional to criticality

---

## How to Invoke This Skill

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: URS_[FeatureName].md
- Load: FRS_[FeatureName].md (primary source for test cases)
- Load: DS_[FeatureName].md
- Load: Feature_Observation_[FeatureName].md (edge cases)

**Skill Invocation:**
Using the Test Protocol Generator skill, create OQ Protocol for [FEATURE] that tests all Functional Requirements.

**Test Requirements:**

1. **Complete FRS Coverage:**
   - At least one test case per FRS
   - All behaviors verified
   - Include edge cases from Feature Observation

2. **Executable Procedures:**
   - Step-by-step test steps
   - Clear expected results
   - Observable outcomes

3. **Traceability:**
   - Each test case references FRS ID(s)
   - Gap analysis ensures no untested requirements

4. **Pass/Fail Criteria:**
   - Explicit criteria for each test
   - Observable results
   - No ambiguity

**Output Format:**
Use template: OQ_Protocol_Template.md
```

---

## Quality Criteria

✅ 100% FRS coverage (every FRS has test)  
✅ Clear procedures (step-by-step)  
✅ Observable expected results  
✅ Traceability documented (test → FRS)  
✅ Edge cases included

---

## Human Verification Checklist

- [ ] All FRS covered by at least one test?
- [ ] Test procedures clear and executable?
- [ ] Expected results observable?
- [ ] Traceability correct?
- [ ] Edge cases from Feature Observation included?

---

## Template Reference

**Template:** OQ_Protocol_Template.md  
**Sections:** Test Cases, Procedures, Expected Results, Traceability Matrix

---

## Related Skills

**Upstream:** Skills 4-6 (DS, FRS, URS)  
**Downstream:** Test execution (manual), Skill 8 (Verification Reporter)

---

**End of Skill 7: Test Protocol Generator**
