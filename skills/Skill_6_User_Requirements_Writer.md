# Skill 6: User Requirements Specification Writer

**Validation Phase:** 4C - User Requirements (URS)  
**Template Used:** URS_Template.md  
**AI Tools Compatible:** Claude, ChatGPT, Gemini, any LLM  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Transforms Functional Requirements into User Requirements that describe WHY users need the feature and WHAT business problem it solves.

**Problem it solves:**  
FRS describes system behaviors. URS describes user needs and business context. This creates:
- User-centric documentation
- Business justification for validation
- Regulatory compliance (21 CFR Part 11, GAMP 5)
- Complete requirements hierarchy: URS → FRS → DS

**Why it matters:**  
URS is the top level of traceability. Everything else (FRS, DS, tests) traces back to user needs. Poor URS = no business justification for validation work.

---

## When to Use This Skill

```
Functional Requirements Complete
        ↓
[USE THIS SKILL]
        ↓
User Requirements Created
        ↓
Test Protocol (Skill 7)
```

**Use when:**
- ✅ FRS verified and approved
- ✅ Need business-level requirements
- ✅ Ready to document user needs and goals

---

## Domain Knowledge Embedded

### URS Principles

**User-Centric:**
- "Users need ability to securely end their session"
- NOT "System shall delete localStorage" (too technical)

**Business Context:**
- WHY does this feature exist?
- WHAT problem does it solve?
- WHAT value does it provide?

**High-Level:**
- Fewer requirements than FRS (typical: 3-6 URS per feature)
- Each URS covers user goal or business need
- Multiple FRS may trace to single URS

**Traceable:**
- Each URS traces to FRS
- URS reflects business needs from Application Context

### Requirement Hierarchy

```
URS (User/Business Needs)
  ↓ traces to
FRS (System Behaviors)
  ↓ traces to
DS (Technical Implementation)
  ↓ traces to
Code (Actual Build)
```

---

## How to Invoke This Skill

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Sambhava_Application_Context.md (business context)
- Load: FRS_[FeatureName].md (approved)
- Load: Feature_Observation_[FeatureName].md

**Skill Invocation:**
Using the User Requirements Specification Writer skill, create URS from Functional Requirements for [FEATURE].

**Requirements:**

1. **Business Context:**
   - Why do users need this feature?
   - What problem does it solve?
   - What value does it provide?

2. **User-Centric Language:**
   - "Users shall be able to [action]"
   - Focus on user goals, not system mechanics

3. **High-Level:**
   - 3-6 URS typical (fewer than FRS)
   - Each URS = one user need/goal
   - Multiple FRS may support one URS

4. **Traceability:**
   - Document which FRS trace to each URS
   - Show how system behaviors satisfy user needs

**Output Format:**
Use template: URS_Template.md
```

---

## Quality Criteria

✅ User-centric (focuses on user needs)  
✅ Business context explained  
✅ High-level (not system mechanics)  
✅ Traces to FRS (documented)  
✅ Appropriate count (3-6 typical)

---

## Human Verification Checklist

- [ ] Each URS describes user need (not system feature)?
- [ ] Business context clear?
- [ ] Traceability to FRS correct?
- [ ] High-level (not duplicating FRS detail)?
- [ ] Reflects Application Context business goals?

---

## Template Reference

**Template:** URS_Template.md  
**Sections:** User Needs, Business Context, Traceability

---

## Related Skills

**Upstream:** Skill 5 (FRS)  
**Downstream:** Skill 7 (OQ Protocol)

---

**End of Skill 6: User Requirements Writer**
