# Skills Library Quick Reference

**Purpose:** Quick lookup guide for which skill to use when

---

## The 8 Validation Skills

### 📋 Skill 1: Feature Observation Documenter
**Phase:** Feature Observation (Manual Testing)  
**Input:** Raw testing notes, observations  
**Output:** Feature_Observation_[Feature].md  
**When:** After completing manual black-box testing  
**Key Benefit:** Transforms messy notes into structured, audit-ready observations

**Example Invocation:**
```
Using the Feature Observation Documenter skill, organize these raw test notes:
[your messy testing notes]
```

---

### 🎯 Skill 2: Scope Boundary Analyzer
**Phase:** Feature Boundary Definition  
**Input:** Feature observations, application context  
**Output:** Feature_Boundary_Definition_[Feature].md  
**When:** Before code investigation, after observations complete  
**Key Benefit:** Defines IN SCOPE vs OUT OF SCOPE with clear rationale

**Example Invocation:**
```
Using the Scope Boundary Analyzer skill, help me define boundaries for [Feature]:
IN SCOPE: What should be validated together?
OUT OF SCOPE: What belongs to separate features?
```

---

### 🔍 Skill 3: Technical Investigator
**Phase:** Code Investigation  
**Input:** Feature observations, code access  
**Output:** Code_Investigation_Reference_[Feature].md  
**When:** Need to understand technical implementation  
**Key Benefit:** Systematically analyzes code with verification guidance

**Example Invocation:**
```
Using the Technical Investigator skill, investigate the [Feature] implementation:
1. Find relevant files and components
2. Explain how it works (plain English)
3. Identify security/validation concerns
```

---

### ⚙️ Skill 4: Design Specification Writer
**Phase:** DS Documentation  
**Input:** Code investigation results, observations  
**Output:** DS_[Feature].md  
**When:** After code investigation verified  
**Key Benefit:** Documents as-built technical design at appropriate granularity

**Example Invocation:**
```
Using the Design Specification Writer skill, create DS for [Feature]:
Document as-built implementation (not ideal design)
Technical details for validators to understand system
```

---

### 📝 Skill 5: Functional Requirements Writer
**Phase:** FRS Documentation  
**Input:** DS, feature observations  
**Output:** FRS_[Feature].md  
**When:** After DS approved  
**Key Benefit:** Defines system behaviors (implementation-agnostic)

**Example Invocation:**
```
Using the Functional Requirements Writer skill, create FRS for [Feature]:
Define WHAT system does (not HOW it does it)
Implementation-agnostic behavioral requirements
```

---

### 👤 Skill 6: User Requirements Writer
**Phase:** URS Documentation  
**Input:** FRS, application context  
**Output:** URS_[Feature].md  
**When:** After FRS approved  
**Key Benefit:** Captures business needs and user expectations

**Example Invocation:**
```
Using the User Requirements Writer skill, create URS for [Feature]:
Document WHY this feature exists
Business value and user needs
High-level (non-technical) requirements
```

---

### 🧪 Skill 7: Test Protocol Generator
**Phase:** OQ Protocol Creation  
**Input:** URS, FRS, DS  
**Output:** OQ_Protocol_[Feature].md  
**When:** Requirements complete, ready to execute tests  
**Key Benefit:** Generates executable test cases with full traceability

**Example Invocation:**
```
Using the Test Protocol Generator skill, create OQ Protocol for [Feature]:
Executable test cases covering all requirements
Acceptance criteria for each test
Traceability matrix (test → requirement)
```

---

### ✅ Skill 8: Verification Reporter
**Phase:** AI Output Verification (Used Throughout)  
**Input:** AI-generated documents  
**Output:** Verification_Report_[Feature].md  
**When:** After ANY AI output generation  
**Key Benefit:** Documents how AI outputs were verified and approved

**Example Invocation:**
```
Using the Verification Reporter skill, document verification of [AI Output]:
Commission check: Did AI claim anything false?
Omission check: Did AI miss anything important?
Confidence level: High/Medium/Low
```

---

## Workflow: Which Skill When?

```
START: Manual Testing
   ↓
✅ Skill 1: Feature Observation Documenter
   ↓
✅ Skill 2: Scope Boundary Analyzer
   ↓
✅ Skill 3: Technical Investigator
   ↓
✅ Skill 8: Verification Reporter (verify investigation)
   ↓
✅ Skill 4: Design Specification Writer
   ↓
✅ Skill 5: Functional Requirements Writer
   ↓
✅ Skill 6: User Requirements Writer
   ↓
✅ Skill 7: Test Protocol Generator
   ↓
✅ Skill 8: Verification Reporter (verify all docs)
   ↓
END: Test Execution (manual by human)
```

---

## Skills vs Prompts vs Templates

### Skills (This Library)
**What:** Reusable AI expertise for specific validation tasks  
**Contains:** Domain knowledge, quality criteria, invocation patterns, verification checklists  
**Example:** "Feature Observation Documenter" skill  
**Reusable:** Works for ANY feature (Login, Logout, Client Creation, etc.)

### Prompts (What You Write)
**What:** Specific invocation of a skill with YOUR data  
**Contains:** Skill name + your feature-specific information  
**Example:** "Using Feature Observation Documenter skill, organize these Logout notes: [notes]"  
**One-time:** Unique to each feature

### Templates (Output Structures)
**What:** Document skeletons that get filled in  
**Contains:** Section headers, required fields, format standards  
**Example:** Feature_Observation_Template.md  
**Consistent:** Same structure across all features

---

## Architecture Flow

```
┌─────────────────────────────────────┐
│ SKILL                               │
│ "I know HOW to do this task well"  │
│ - Embedded domain knowledge         │
│ - Quality criteria                  │
│ - Best practices                    │
└─────────────┬───────────────────────┘
              │ uses
              ↓
┌─────────────────────────────────────┐
│ TEMPLATE                            │
│ "This is the OUTPUT structure"     │
│ - Section headers                   │
│ - Required fields                   │
│ - Format specifications             │
└─────────────┬───────────────────────┘
              │ produces
              ↓
┌─────────────────────────────────────┐
│ FEATURE DOCUMENT                    │
│ "Completed validation artifact"    │
│ - Login_URS.md                      │
│ - Logout_FRS.md                     │
│ - [Your Feature]_DS.md              │
└─────────────┬───────────────────────┘
              │ reviewed by
              ↓
┌─────────────────────────────────────┐
│ HUMAN VERIFICATION                  │
│ "I verify and approve this"        │
│ - Commission check                  │
│ - Omission check                    │
│ - Final accountability              │
└─────────────────────────────────────┘
```

---

## Key Benefits of Skills Architecture

### 1. Tool-Agnostic
✅ Works with Claude, ChatGPT, Gemini, or any AI tool  
✅ Not locked into specific vendor  
✅ Methodology portable across platforms

### 2. Reproducible
✅ Others can follow your skills and get similar results  
✅ Methodology can be taught and scaled  
✅ Knowledge transfer enabled

### 3. Quality-Embedded
✅ AI knows what "good" looks like for each task  
✅ Consistent output across features  
✅ Human review time reduced (not drafting time)

### 4. Continuously Improving
✅ Skills evolve based on lessons learned  
✅ Update skill once → benefits all future features  
✅ Git-versioned for traceability

---

## How to Use This Library

### For Your Next Feature Validation:

**Step 1:** Start manual testing  
**Step 2:** Use Skill 1 to document observations  
**Step 3:** Use Skill 2 to define boundaries  
**Step 4:** Use Skill 3 to investigate code  
**Step 5:** Use Skill 8 to verify investigation  
**Step 6:** Use Skills 4-6 to create requirements  
**Step 7:** Use Skill 7 to generate test protocol  
**Step 8:** Use Skill 8 to verify all outputs  

### For Someone Learning Your Methodology:

**Step 1:** Read this Quick Reference (you are here!)  
**Step 2:** Read /skills/README.md (big picture)  
**Step 3:** Pick one skill (start with Skill 1)  
**Step 4:** Read the full skill document  
**Step 5:** Try it on a simple feature  
**Step 6:** Review output using verification checklist  
**Step 7:** Move to next skill

---

## File Locations

**Skills Library:** `/skills/` folder  
**Individual Skills:** `/skills/Skill_[1-8]_[Name].md`  
**Templates:** `/templates/` folder  
**Feature Docs:** `/[Feature_Number]_[Feature_Name]/` folders  
**Methodology:** `/Methodology.md`  
**Context:** `/Application_Context.md`

---

## Success Criteria

**You've successfully used a skill when:**

1. ✅ AI output follows template structure
2. ✅ Quality criteria from skill are met  
3. ✅ Verification checklist completed
4. ✅ Human approves with high confidence
5. ✅ Output is audit-ready

---

## Next Steps

**For Phase 1 Portfolio Completion:**
- ✅ Skills library exists (8 comprehensive skills)
- ✅ AI_Process_Documentation.md exists (transparency)
- ⏳ Add AI metadata to 3 sample docs (Login URS, FRS, OQ)
- ⏳ Quick README review
- ⏳ Push to GitHub
- ⏳ Finalize LinkedIn Post 1

**Your skills library is ALREADY complete for Phase 1!** 🎉

---

**End of Quick Reference**
