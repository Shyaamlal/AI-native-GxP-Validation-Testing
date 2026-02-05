# Learning Journey - 2026-01-31

## What I Did Today
- Created Sambhava application overview
- Understood difference between development vs validation testing
- Clarified AI tool usage in GxP environments
### **The regulatory landscape:**
**Pre-validation (Development phase):**

✅ **AI tools generally OK:**
- Code is not locked/validated yet
- Development environment, not production
- Changes tracked in version control
- "Computer Software Assurance" mindset (risk-based)

**What you CAN do:**
- Use Claude Code for test generation
- Use AI for code review
- Use AI for documentation
- Generate test cases with AI

**Requirements:**
- All AI-generated content must be reviewed by qualified person
- Changes must be tracked (Git commits)
- Rationale documented
- Part of development records
- Learned validation tester reviews test logic, not code quality



### **Where AI fits in GxP testing:**
**Development phase (your opportunity):**

```
Requirements Analysis
  ↓ [AI can help here]
Test Design
  ↓ [AI can help here]
Test Script Generation
  ↓ [AI can help here]
Review & Approval ← [Human must do this]
  ↓
Execution
  ↓ [Can be AI-assisted if tool is validated]
Results Documentation
  ↓
Validation Report ← [Human reviews AI-generated draft]
```

##**Scenario: New medical device software**

**Phase 1 - Development (AI-native approach):**

- Use Claude Code to analyze requirements
- Generate comprehensive test cases
- Create traceability matrices
- Draft validation protocols
- **You review everything for GxP compliance**

**Phase 2 - Validation (Traditional approach):**

- Execute protocols manually
- Document in validated system
- No AI tools touching production
- Follow SOPs strictly
- Generate validation report

**Phase 3 - Maintenance (Hybrid approach):**

- Changes require validation
- Use AI to assess impact
- Generate change documentation
- Execute regression tests
- Validate changes formally
## Key Insights
- **Leapwork parallel:** Claude Code + Playwright = same approach as Leapwork (no-code), just different interface
- **Validation focus:** Functional correctness > code elegance
- **Tool qualification:** Applies to execution tools (Playwright), not authoring tools (Claude Code)
- **My value:** GxP mindset + AI-native skills = rare combination

## Questions Answered
- ✅ Can I use AI in validation environments? (Yes, for authoring with review)
- ✅ Do I need to understand code deeply? (No, functional review sufficient)
- ✅ What test types for dev vs validation? (All types in dev, functional in validation)

## Questions Still Open
- How do I map UI workflows to codebase?
- How do I structure test strategy document?
- What does good traceability matrix look like?

## Challenges Today
- Felt overwhelmed by 8-folder Obsidian structure → simplified to organic growth
- Wanted to jump ahead → slowed down to build foundation properly
- Uncertainty about code review → clarified functional review is sufficient

## Tomorrow's Focus
- Map admin login workflow to code
- Start identifying test requirements
- Continue building inside-out knowledge structure

## Resources Referenced
- IEC 62304 principles
- GxP compliance requirements
- Leapwork comparison (from past experience)

## Mood/Confidence
Starting to feel less overwhelmed. The step-by-step approach is working. Understanding the validation boundaries gives me confidence.