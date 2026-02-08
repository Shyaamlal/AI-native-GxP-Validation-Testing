# Validation Guides

**What's in this folder:** 8 step-by-step guides for each phase of the validation workflow

**Last Updated:** 2026-02-08

---

## What's in This Folder?

This folder contains 8 guides that walk you through each phase of validation, from initial testing through final verification. Each guide includes:

- **Step-by-step instructions** for what to do
- **Real examples** from the Login and Logout features
- **Templates** you can adapt for your own work
- **Quality checks** to verify your results

---

## The 8 Guides

| # | Guide Name | Validation Phase | When to Use |
|---|------------|------------------|-------------|
| 1 | **Feature Observation** | Initial Testing | After you've manually tested the feature |
| 2 | **Scope Definition** | Boundary Setting | Before you start analyzing code |
| 3 | **Code Investigation** | Technical Analysis | When you need to understand the implementation |
| 4 | **Design Specification** | Technical Documentation | After you've analyzed the code |
| 5 | **Functional Requirements** | System Behaviors | After design spec is complete |
| 6 | **User Requirements** | Business Needs | After functional requirements are done |
| 7 | **Test Protocol** | Test Planning | When you're ready to execute formal tests |
| 8 | **Verification Report** | Quality Verification | After AI has generated any documentation |

---

## How to Use These Guides

### Basic Workflow

```
1. Identify which validation phase you're in
   ↓
2. Open the corresponding guide
   ↓
3. Read the guide to understand the process
   ↓
4. Follow the step-by-step instructions
   ↓
5. Provide your feature-specific information
   ↓
6. Use AI to help generate documentation (following the guide)
   ↓
7. Review the output using the quality checklist
   ↓
8. Approve or refine as needed
```

---

## Example: Using Guide 1 (Feature Observation)

### What You Have:
After manually testing the Logout feature, you have these notes:
- Logout button appears in header (far right)
- Hover shows "Logout" tooltip
- Single click logs out immediately
- No confirmation dialog
- localStorage key "isAdminLoggedIn" is deleted
- After logout, /admin/dashboard shows 404

### What You Do:

**Step 1:** Open `Skill_1_Feature_Observation_Documenter.md`

**Step 2:** Read the guide to understand what makes good feature documentation

**Step 3:** Follow the instructions to organize your notes

**Step 4:** Use the AI prompt template from the guide:
```
I've manually tested the Admin Logout feature. Here are my observations:
[paste your notes]

Please organize these into a structured Feature Observation document.
```

**Step 5:** Review the AI output using the quality checklist in the guide

**Step 6:** Edit or approve

**Result:** Professional Feature Observation document ready for your validation package

---

## What Each Guide Contains

### Every guide includes:

**1. Purpose**
- What this validation phase accomplishes
- Why it's important
- Where it fits in the workflow

**2. Instructions**
- Clear steps for what to do
- What information you need
- How to provide it to AI

**3. AI Prompt Templates**
- Ready-to-use prompts for AI tools
- Fill-in-the-blank format
- Works with Claude, ChatGPT, Gemini, or other AI

**4. Real Examples**
- Actual prompts used in Login/Logout validation
- What the AI generated
- How it was verified

**5. Quality Checklists**
- What to look for in AI outputs
- Common issues to watch for
- When to regenerate vs manually edit

**6. Templates**
- Document structure to use
- Required sections
- Format specifications

---

## Works with Any AI Tool

These guides work with:

| AI Tool | How Well It Works | Notes |
|---------|------------------|-------|
| **Claude (Anthropic)** | ✅ Excellent | Good at long documents, technical content |
| **ChatGPT (OpenAI)** | ✅ Excellent | Fast iterations, alternative perspectives |
| **Gemini (Google)** | ✅ Good | Helpful for UI documentation |
| **Other AI Tools** | ✅ Varies | Most modern AI tools will work |

**Key requirement:** The AI tool needs to handle reasonably long context (your methodology + application info + templates).

---

## Validation Workflow (Complete Picture)

```
Manual Testing
    ↓
Guide 1: Feature Observation
    ↓
Guide 2: Scope Definition
    ↓
Guide 3: Code Investigation
    ↓
Guide 4: Design Specification
    ↓
Guide 5: Functional Requirements
    ↓
Guide 6: User Requirements
    ↓
Guide 7: Test Protocol
    ↓
Execute Tests
    ↓
Guide 8: Verification Report
    ↓
Validation Summary
```

---

## Benefits of Using These Guides

### Consistency
- Same quality standards applied every time
- Predictable document structure
- Easier to compare across features

### Speed
- AI handles the writing
- You focus on review and approval
- Demonstrated: 67% faster on second feature

### Quality
- Best practices built into the guides
- Quality checks prevent common mistakes
- GAMP 5 / IEC 62304 principles included

### Reusability
- Use for any feature you validate
- Adapt to your specific application
- Share with your team

---

## Tips for Best Results

### Before You Start:
1. **Complete the previous phase** - Each guide builds on the previous one
2. **Have your information ready** - Test notes, code access, etc.
3. **Read the guide first** - Understand the process before jumping in

### While Using AI:
1. **Be specific** - Provide clear, detailed information
2. **Use the templates** - They ensure consistency
3. **Follow the prompt format** - The guides provide tested patterns

### After AI Generates Output:
1. **Use the quality checklist** - Every guide has one
2. **Verify accuracy** - AI can make mistakes
3. **Edit if needed** - You're accountable, not the AI
4. **Document your review** - Note any changes you made

---

## Understanding the Architecture

### How These Guides Work

Each guide is structured in three layers:

**Layer 1: Instructions (What You Do)**
- The steps you follow manually
- Information you need to gather
- Decisions you need to make

**Layer 2: AI Assistance (What AI Does)**
- Prompt templates you use
- How AI helps with documentation
- What AI generates

**Layer 3: Verification (What You Check)**
- Quality criteria for outputs
- How to verify accuracy
- When to regenerate or edit

**Important:** You're always in control. AI assists with writing, you maintain accountability.

---

### How Guides Use Templates

Each guide references specific templates in `/templates/` folder:

**The relationship:**
```
Guide (Instructions)
    ↓ uses
Template (Structure)
    ↓ produces
Document (Output)
    ↓ reviewed by
Human (Accountability)
```

**Example:**
- Guide 1 (Feature Observation) → uses → Feature_Observation_Template.md
- Template provides section headers, required fields
- AI fills in the template with your specific data
- You review and approve

---

### How Guides Connect to Methodology

All guides implement principles from `Methodology.md`:

- **Retrospective validation** approach
- **GAMP 5 Appendix M3** guidelines
- **IEC 62304** traceability requirements
- **Human accountability** for all decisions
- **AI as Category 1 authoring tool** classification

The guides are the practical application of these principles.

---

## Folder Structure

```
/Skills/
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

**Note:** File names use "Skill_X" for consistency with initial development, but they function as step-by-step guides.

---

## Success Criteria

**You've successfully used a guide when:**

1. ✅ You followed the instructions in sequence
2. ✅ AI generated output following the template
3. ✅ You verified quality using the checklist
4. ✅ You approved the output with confidence
5. ✅ The document is audit-ready

**If any criteria aren't met:** Review the guide, adjust your prompt, regenerate, or manually edit.

---

## How This Fits Into Your Portfolio

### Relationship to Other Components:

**These guides generate documents** that go in feature folders:
- `/01_Login/` - Login validation documents
- `/02_Logout/` - Logout validation documents

**These guides follow the methodology** documented in:
- `/00_Project_Context/Methodology.md`

**These guides reference application knowledge** from:
- `/00_Project_Context/Sambhava_Application_Context.md`

**The AI process** is documented in:
- `AI_Process_Documentation.md` (shows real examples)

---

## Adapting for Your Own Work

### To use these guides for your application:

**Step 1: Update Application Context**
- Create your own application context document
- Include: business purpose, workflows, technical architecture
- Reference it when using the guides

**Step 2: Customize Templates**
- Adapt templates to your organization's standards
- Keep the core structure, adjust details
- Maintain consistency across features

**Step 3: Follow the Guides**
- Use the same workflow sequence
- Adapt examples to your features
- Apply the quality checklists

**Step 4: Refine as You Learn**
- Each feature teaches you something
- Update your process based on lessons learned
- The methodology improves over time

---

## Getting Help

**Questions about a specific guide?**
- Read the guide's "Purpose" and "When to Use" sections
- Check the examples section for similar scenarios
- Review the quality checklist for common issues

**Issues with AI outputs?**
- Verify you're using the prompt template correctly
- Check that you provided enough detail
- Try regenerating with more specific instructions
- Remember: You can always edit manually

**Want to improve a guide?**
- Document what worked better
- Test your improvement on another feature
- Consider contributing back to the methodology

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-02-08 | Initial guides created for Login/Logout validation workflow |

---

## Contributing

**Found a better way to use a guide?**
- Document your improvement
- Test it on multiple features
- Share your refined approach

**Created a guide for a new phase?**
- Follow the same structure
- Include real examples
- Add quality checklists
- Update this README

---

**Remember:** These guides are tools to make your validation work faster and more consistent. You're always the decision-maker and remain accountable for the results.

---

**End of Validation Guides README**