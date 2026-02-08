# Skill 5: Functional Requirements Specification Writer

**Validation Phase:** 4B - Functional Requirements (FRS)  
**Template Used:** FRS_Template.md  
**AI Tools Compatible:** Claude, ChatGPT, Gemini, any LLM  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Transforms Design Specifications into Functional Requirements that describe WHAT the system does (behaviors) without specifying HOW it's implemented.

**Problem it solves:**  
DS describes technical implementation. FRS describes user-observable behaviors. This separation enables:
- Implementation-agnostic requirements
- Testable functional specifications
- Clear traceability DS → FRS → URS
- Regulatory compliance (requirement levels)

**Why it matters:**  
FRS is where testers work. Test cases trace to FRS. If FRS is implementation-specific or incomplete, testing will be inadequate.

---

## When to Use This Skill

```
Design Specification Complete
        ↓
[USE THIS SKILL]
        ↓
Functional Requirements Created
        ↓
User Requirements (Skill 6)
```

**Use when:**
- ✅ DS verified and approved
- ✅ Need behavioral specifications for testing
- ✅ Ready to define WHAT system does (not HOW)

---

## Domain Knowledge Embedded

### FRS Principles

**Behavioral Focus:**
- "System SHALL terminate admin session when logout is triggered"
- NOT "System SHALL call localStorage.removeItem()" (that's DS, not FRS)

**Implementation-Agnostic:**
- Could swap localStorage for cookies → FRS stays same
- FRS describes observable result, not mechanism

**Testable:**
- Each FRS must be verifiable through testing
- Clear pass/fail criteria
- Observable outcomes

**Traceable:**
- Each FRS traces to one or more DS
- Each FRS will be tested in OQ Protocol

### Requirement Granularity

**Moderate Granularity (Recommended):**
- 4-8 FRS per feature (typical)
- Each FRS covers meaningful behavior
- Not too high-level (vague) or too detailed (micro-management)

**Example Good Granularity:**
- FRS-LOGOUT-001: Session Termination
- FRS-LOGOUT-002: UI Control Presence
- FRS-LOGOUT-003: Post-Logout Navigation
- FRS-LOGOUT-004: Logout Confirmation (or lack thereof)

---

## How to Invoke This Skill

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: DS_[FeatureName].md (approved)
- Load: Feature_Observation_[FeatureName].md

**Skill Invocation:**
Using the Functional Requirements Specification Writer skill, create FRS from Design Specifications for [FEATURE].

**Requirements:**

1. **Derive from DS:**
   - Each FRS must trace to DS
   - Transform technical implementation into behavioral requirement
   - Remove implementation details

2. **Observable Behaviors:**
   - "System SHALL [observable action/result]"
   - No internal mechanisms (leave those in DS)

3. **Testable Statements:**
   - Clear pass/fail criteria
   - Can verify through testing

4. **Moderate Granularity:**
   - 4-8 FRS typical for feature
   - One behavior per FRS
   - Not too granular, not too vague

**Output Format:**
Use template: FRS_Template.md
```

---

## Quality Criteria

✅ Implementation-agnostic (no localStorage, API calls, file paths)  
✅ Observable behaviors (can test)  
✅ Traces to DS (documented)  
✅ Uses SHALL language (requirement)  
✅ Moderate granularity (not micro-level)

---

## Human Verification Checklist

- [ ] Each FRS is implementation-agnostic?
- [ ] Each FRS is testable?
- [ ] Traceability to DS documented?
- [ ] Appropriate granularity (not too many/few)?
- [ ] No technical implementation details leaked from DS?

---

## Template Reference

**Template:** FRS_Template.md  
**Sections:** Requirements, Traceability, Test Considerations

---

## Related Skills

**Upstream:** Skill 4 (DS)  
**Downstream:** Skill 6 (URS), Skill 7 (OQ Protocol)

---

**End of Skill 5: Functional Requirements Writer**
