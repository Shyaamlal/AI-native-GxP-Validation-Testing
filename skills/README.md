# Validation Skills Library

**Purpose:** Reusable AI expertise for GxP validation testing

**Status:** Core methodology skills (v1.0)  
**Last Updated:** 2026-02-08

---

## What Are Skills?

**Skills** are reusable AI behaviors that encapsulate domain expertise, quality criteria, and best practices for specific validation tasks.

Think of skills as **specialized assistants** that know:
- What makes good validation documentation
- What quality criteria to apply
- What templates to use
- What verification steps humans should perform

---

## Skills vs Prompts vs Templates

### Skills (Reusable Expertise)
**What:** Specialized AI capabilities with embedded domain knowledge  
**Example:** "Feature Observation Documenter" skill  
**Contains:**
- Domain knowledge (GAMP 5, IEC 62304 principles)
- Quality criteria (what makes good vs poor output)
- Invocation pattern (how to use this skill)
- Verification checklist (how humans review output)

### Prompts (One-Time Instructions)
**What:** Specific instance of using a skill  
**Example:** "Using Feature Observation Documenter skill, organize these Logout test notes: [notes]"  
**Contains:**
- Skill name to invoke
- Actual data for THIS feature
- Context for this specific use

### Templates (Output Structures)
**What:** Document skeletons that get filled in  
**Example:** `Feature_Observation_Template.md`  
**Contains:**
- Section headings
- Required fields
- Format specifications
- Consistency standards

---

## How to Use This Skill Library

### Basic Workflow

```
1. Identify which validation phase you're in
   ↓
2. Select the corresponding skill
   ↓
3. Read the skill document (understand what it does)
   ↓
4. Follow the invocation pattern
   ↓
5. Provide your feature-specific data
   ↓
6. AI generates output using skill's embedded knowledge
   ↓
7. Human verifies output using skill's verification checklist
   ↓
8. Approve or refine
```

---

## Available Skills

### Core Validation Workflow Skills

| # | Skill Name | Validation Phase | Template Used | When to Use |
|---|------------|------------------|---------------|-------------|
| 1 | **Feature Observation Documenter** | Feature Observation | Feature_Observation_Template.md | After manual black-box testing |
| 2 | **Scope Boundary Analyzer** | Boundary Definition | Feature_Boundary_Template.md | Before code investigation |
| 3 | **Technical Investigator** | Code Investigation | Code_Investigation_Template.md | When analyzing implementation |
| 4 | **Design Specification Writer** | DS Documentation | DS_Template.md | After code investigation complete |
| 5 | **Functional Requirements Writer** | FRS Documentation | FRS_Template.md | After DS approved |
| 6 | **User Requirements Writer** | URS Documentation | URS_Template.md | After FRS approved |
| 7 | **Test Protocol Generator** | OQ Protocol | OQ_Protocol_Template.md | When ready to execute tests |
| 8 | **Verification Reporter** | Verification | Verification_Report_Template.md | After AI outputs generated |

---

## Skill Invocation Pattern

### Standard Format

All skills follow this invocation pattern:

```markdown
**Context Loading:**
- Load: Methodology.md (validation approach)
- Load: Sambhava_Application_Context.md (application knowledge)
- Load: [Previous phase documents as needed]

**Skill Invocation:**
Using the [SKILL_NAME] skill, [task description]

**Feature-Specific Data:**
[Your actual data for this feature]

**Quality Requirements:**
- [Any specific quality criteria]
- [Compliance standards to apply]

**Output Format:**
Use template: [Template_Name.md]
```

### Example (Skill 1: Feature Observation Documenter)

```markdown
**Context Loading:**
- Load: Methodology.md
- Load: Sambhava_Application_Context.md

**Skill Invocation:**
Using the Feature Observation Documenter skill, organize these raw test notes into a structured Feature Observation document.

**Feature-Specific Data:**
Feature: Admin Logout
Test Date: 2026-02-06
Tester: Shyaam

Raw observations:
- Logout button appears in header (far right)
- Hover shows "Logout" tooltip
- Single click triggers logout
- No confirmation dialog
- localStorage key "isAdminLoggedIn" deleted (verified in DevTools)
- After logout, /admin/dashboard returns 404

**Quality Requirements:**
- Observable behaviors only (no assumptions about implementation)
- Clear, specific descriptions
- Organized by workflow sequence

**Output Format:**
Use template: Feature_Observation_Template.md
```

---

## Why Use Skills Instead of Raw Prompts?

### Benefits

**1. Consistency Across Features**
- Same quality criteria applied every time
- Predictable output structure
- Easier to compare documents

**2. Domain Knowledge Embedded**
- AI knows GAMP 5 / IEC 62304 principles
- Quality standards built-in
- Reduces human burden of specifying criteria

**3. Tool Agnostic**
- Works with Claude, ChatGPT, Gemini, or any LLM
- Methodology portable across AI platforms
- Not locked into specific vendor

**4. Reproducible Methodology**
- Others can use your skills
- Enables knowledge transfer
- Supports team scaling

**5. Continuous Improvement**
- Skills can be refined based on lessons learned
- Version controlled (Git)
- Evolves with experience

---

## How to Extend This Library

### Adding New Skills

When you identify a repeatable validation task:

1. **Document the skill:**
   - What problem does it solve?
   - What domain knowledge is required?
   - What quality criteria apply?

2. **Create skill file:**
   - Follow the skill template structure
   - Include real examples from your work
   - Define verification checklist

3. **Test the skill:**
   - Use it on a feature
   - Verify outputs
   - Refine based on results

4. **Add to library:**
   - Update this README with skill entry
   - Commit to Git with description
   - Share with community

---

## Skill Development Best Practices

### What Makes a Good Skill?

**Clear Purpose:**
- ✅ Solves one specific problem
- ✅ Clear boundaries (what it does/doesn't do)
- ❌ Avoid multi-purpose "do everything" skills

**Embedded Expertise:**
- ✅ Contains domain knowledge (GAMP 5, regulations)
- ✅ Quality criteria defined
- ✅ Common pitfalls documented
- ❌ Don't assume users know validation principles

**Practical Examples:**
- ✅ Real examples from actual work
- ✅ Shows both good and problematic outputs
- ✅ Demonstrates verification process
- ❌ Avoid theoretical-only examples

**Verification Guidance:**
- ✅ Clear checklist for human review
- ✅ Confidence criteria defined
- ✅ Edge cases to watch for
- ❌ Don't skip verification documentation

---

## Tool Compatibility

These skills work with:

| AI Tool | Compatibility | Notes |
|---------|--------------|-------|
| **Claude (Anthropic)** | ✅ Excellent | Long context, good at technical documentation |
| **ChatGPT (OpenAI)** | ✅ Excellent | Alternative perspectives, fast iterations |
| **Gemini (Google)** | ✅ Good | Multi-modal capabilities useful for UI documentation |
| **GitHub Copilot** | ⚠️ Partial | Better for code than long-form documentation |
| **Custom LLMs** | ✅ Depends | Effectiveness varies by model capability |

**Key requirement:** AI tool must handle long context (methodology + application context + templates).

---

## Skill Library Structure

```
/skills/
├── README.md (this file)
├── Skill_1_Feature_Observation_Documenter.md
├── Skill_2_Scope_Boundary_Analyzer.md
├── Skill_3_Technical_Investigator.md
├── Skill_4_Design_Specification_Writer.md
├── Skill_5_Functional_Requirements_Writer.md
├── Skill_6_User_Requirements_Writer.md
├── Skill_7_Test_Protocol_Generator.md
└── Skill_8_Verification_Reporter.md
```

---

## Relationship to Other Portfolio Components

### Skills Use Templates
Each skill references specific template(s) in `/templates/` folder.

### Skills Generate Artifacts
Skill outputs become validation documents in feature folders (e.g., `/01_Login/`, `/02_Logout/`).

### Skills Follow Methodology
All skills implement principles documented in `Methodology.md`.

### Skills Reference Application Context
Most skills load `Sambhava_Application_Context.md` for domain knowledge.

---

## Success Criteria

**You've successfully used a skill when:**

1. ✅ AI output follows template structure
2. ✅ Quality criteria from skill are met
3. ✅ Verification checklist completed
4. ✅ Human approves output with confidence
5. ✅ Output is audit-ready

**If any criteria fail:** Refine prompt, regenerate, or manually edit output.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-02-08 | Initial skill library created. Core 8 skills for Login/Logout validation workflow. |

---

## Contributing

**Found a better way to use a skill?**
- Document your improvement
- Test on multiple features
- Submit refined skill version

**Created a new skill?**
- Follow skill template structure
- Include real examples
- Add verification checklist
- Update this README

---

**Remember:** Skills are **methodology artifacts**, not just prompts. They encode your expertise so others can reproduce your results.

---

**End of Skills Library README**
