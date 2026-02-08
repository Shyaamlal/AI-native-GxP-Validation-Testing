# Skill 4: Design Specification Writer

**Validation Phase:** 4A - Design Specification (DS)  
**Template Used:** DS_Template.md  
**AI Tools Compatible:** Claude, ChatGPT, Gemini, any LLM  
**Skill Version:** 1.0  
**Last Updated:** 2026-02-08

---

## Purpose

**What this skill does:**  
Transforms code investigation findings into structured Design Specification (DS) documents that describe how the system is technically implemented.

**Problem it solves:**  
Code investigation produces raw technical details. DS documents organize these details into specification format required for:
- GAMP 5 retrospective validation
- Requirements traceability (DS → FRS → URS)
- Technical audit trail
- Future maintenance reference

**Why it matters:**  
DS is the technical source of truth for validation. It documents "what is built" and becomes the foundation for FRS (what the system does) and URS (what users need). Poor DS = poor traceability.

---

## When to Use This Skill

### Timing in Validation Workflow

```
Code Investigation Complete
        ↓
[USE THIS SKILL]
        ↓
Design Specification Created
        ↓
Functional Requirements (Skill 5)
```

**Use this skill when:**
- ✅ Code investigation verified (HIGH confidence)
- ✅ Technical implementation understood
- ✅ Ready to document as-built system
- ✅ Need DS for traceability to FRS

**Don't use this skill when:**
- ❌ Code investigation incomplete
- ❌ Low confidence in technical findings
- ❌ Trying to specify ideal design (DS documents reality, not wishes)

---

## Prerequisites

**Before using this skill, you must have:**

1. **Verified Code Investigation:**
   - Document from Skill 3
   - HIGH confidence level
   - All verification checks passed

2. **Feature Context:**
   - Feature Observation (Skill 1)
   - Feature Boundary (Skill 2)
   - Application Context

3. **Template Understanding:**
   - Know DS format and requirements
   - Understand DS vs FRS distinction
   - Clear on GAMP 5 retrospective validation approach

---

## Domain Knowledge Embedded in This Skill

### Design Specification Principles

**Describes Implementation:**
- "System uses localStorage to store authentication state"
- NOT "System should use secure session tokens" (that's a requirement, not as-built)

**Technical but Readable:**
- Written for validators, not just developers
- Explains WHAT and HOW, with enough WHY to understand rationale
- Avoids unnecessary jargon

**Traceable to Code:**
- Every DS statement must trace to code investigation findings
- Include file paths and line numbers as evidence
- Reference code snippets where helpful

**One Specification Per Decision:**
- DS-LOGOUT-001: Session termination mechanism
- DS-LOGOUT-002: Navigation implementation
- DS-LOGOUT-003: UI control design
- Each DS captures ONE technical decision

### GAMP 5 Alignment

**Retrospective Validation:**
- Document existing system (not designing new one)
- Code is source of truth
- DS describes "what is built"

**Traceability Required:**
- DS must trace backward to code
- DS must trace forward to FRS
- Every DS has rationale

### Typical DS Categories

**1. Data Structures:**
- What data is stored/processed
- Data types and formats
- Storage mechanisms

**2. Processing Logic:**
- Algorithms and workflows
- Business rules implementation
- Calculation methods

**3. Interface Design:**
- UI components and behavior
- API endpoints and contracts
- External system integrations

**4. Security Controls:**
- Authentication mechanisms
- Authorization patterns
- Data protection

**5. Error Handling:**
- Error detection methods
- Error response strategies
- Logging and monitoring

---

## How to Invoke This Skill

### Standard Invocation Pattern

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Sambhava_Application_Context.md
- Load: Code_Investigation_[FeatureName].md (verified, HIGH confidence)
- Load: Feature_Boundary_[FeatureName].md

**Skill Invocation:**
Using the Design Specification Writer skill, create DS document describing the as-built implementation of [FEATURE NAME].

**Source Material:**
[Provide or reference Code Investigation findings]

**Specification Requirements:**

1. **One DS per Technical Decision:**
   - Each DS should capture ONE implementation detail
   - Use format: DS-[FEATURE]-001, DS-[FEATURE]-002, etc.

2. **Describe As-Built (Not Ideal):**
   - Document what IS implemented, not what SHOULD BE
   - Include implementation limitations or quirks
   - Note technical debt or code quality issues as "implementation notes"

3. **Provide Technical Details:**
   - Mechanisms used (localStorage, API calls, algorithms)
   - Technical characteristics (synchronous, client-side, etc.)
   - File paths and line numbers (traceability to code)

4. **Include Design Rationale:**
   - Why this approach? (if evident from code/context)
   - What constraints led to this design?
   - What trade-offs were made?

5. **Note Production Considerations:**
   - Would this implementation be acceptable in production?
   - What would need to change for regulated environment?
   - Any security or quality concerns?

**Output Format:**
Use template: DS_Template.md
```

---

## Example (abbreviated for space - see full example in actual usage)

Input: Code investigation showing logout is client-side localStorage removal

Output DS:
```
DS-LOGOUT-001: Session Termination Mechanism

Implementation:
Session termination achieved by removing browser localStorage key "isAdminLoggedIn".

Technical Details:
- Method: localStorage.removeItem("isAdminLoggedIn")
- Scope: Browser localStorage (domain-specific)
- Code Location: 3 components (AdminDashboard.tsx line 45, ClientManagement.tsx line 38, ClientDashboard.tsx line 52)

Design Rationale:
Client-side session management chosen for demo application simplicity.

Production Considerations:
Production systems should implement server-side session invalidation for security.
```

---

## Quality Criteria

✅ Each DS describes ONE technical decision  
✅ DS statements trace to code investigation  
✅ Technical but readable (not just for developers)  
✅ Includes rationale (why this approach)  
✅ Notes limitations or concerns  
✅ Uses as-built language ("uses", "implements") not requirements language ("shall", "must")

---

## Human Verification Checklist

- [ ] Every DS traces to code investigation findings?
- [ ] Technical details accurate?
- [ ] One specification per decision (not mixing multiple concerns)?
- [ ] Rationale included where relevant?
- [ ] Production considerations noted?
- [ ] No requirements creep (sticks to describing what IS)?

---

## Template Reference

**Template:** DS_Template.md  
**Sections:** Implementation, Technical Details, Rationale, Traceability, Production Notes

---

## Related Skills

**Upstream:** Skill 3 (Code Investigation)  
**Downstream:** Skill 5 (FRS), Skill 6 (URS)

---

**End of Skill 4: Design Specification Writer**
