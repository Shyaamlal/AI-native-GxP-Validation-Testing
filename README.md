# AI-Native GxP Validation Testing

**Project:** Systematic software validation for regulated life sciences environments using modern AI tooling while maintaining compliance with GAMP 5 and IEC 62304.

**Objective:** Demonstrate reproducible, feature-level validation workflows that use AI to accelerate documentation and analysis, with clear human oversight and regulatory accountability.

**Contents:** Validation methodology with reusable templates, complete feature examples, and documented AI assistance process.

**Status:** Active development - 2 features validated (Login, Logout).

---

## Quick Start

**Want to try this methodology?**
1. **For transparency:** Read [AI_Process_Documentation.md](./AI_Process_Documentation.md) - see how AI was used
2. **For replication:** Explore [`/Skills/`](./Skills/) folder - use these skills on your own features
3. **For examples:** Review [`/01_Login/`](./01_Login/) - complete validation package

---

## Repository Structure

```
AI-native-GxP-Validation-Testing/
│
├── Skills/                          # Reusable validation methodology
│   ├── README.md
│   ├── Skills_Quick_Reference.md
│   ├── Skill_1_Feature_Observation_Documenter.md
│   ├── Skill_2_Scope_Boundary_Analyzer.md
│   ├── Skill_3_Technical_Investigator.md
│   ├── Skill_4_Design_Specification_Writer.md
│   ├── Skill_5_Functional_Requirements_Writer.md
│   ├── Skill_6_User_Requirements_Writer.md
│   ├── Skill_7_Test_Protocol_Generator.md
│   └── Skill_8_Verification_Reporter.md
│
├── AI_Process_Documentation.md     # How AI was used (transparency)
│
├── 00_Project_Context/              # Methodology and application knowledge
│   ├── Learning_Journals/           # Process observations and insights
│   ├── Templates/                   # Reusable document templates
│   ├── Thread_Summaries/            # Historical decisions and outcomes
│   ├── Methodology.md               # Validation approach and workflow
│   ├── README.md                    # Context management overview
│   └── Application_Context.md       # Application-specific knowledge
│
├── 00_Validation_Management/        # Cross-feature traceability
│
├── 01_Login/                        # Feature 1: Admin Login
│   ├── Feature_Observation_Login.md
│   ├── Feature_Boundary_Definition_Login.md
│   ├── DS_Login.md                 # Design Specification
│   ├── FRS_Login.md                # Functional Requirements
│   ├── URS_Login.md                # User Requirements
│   ├── OQ_Protocol_Login.md        # Operational Qualification
│   ├── Verification_Report_Login.md
│   └── Validation_Summary_Login.md
│
├── 02_Logout/                       # Feature 2: Admin Logout
│   └── [Complete validation package]
│
├── .gitignore
└── README.md                        # This file
```

---

## Validation Approach

### Methodology
Follows **GAMP 5 Appendix M3** (retrospective validation for legacy systems) combined with modern context engineering practices.

**Key characteristics:**
- Retrospective validation (documenting as-built systems)
- AI-assisted documentation and analysis
- Human verification and approval at all decision points
- Full requirements traceability (URS → FRS → DS → OQ)

**Workflow:**
```
Manual Testing → Feature Observation → Scope Definition → 
Code Investigation → Requirements (DS/FRS/URS) → Test Protocol → 
Test Execution → Validation Summary
```

### Regulatory Standards
- **GAMP 5:** Risk-based approach to GxP compliance
- **IEC 62304:** Software lifecycle requirements and traceability

---

## AI Tool Usage

**Classification:** AI tools used as **GAMP 5 Category 1 authoring tools** (similar to Microsoft Word or Excel)

**What AI does:**
- Code investigation (local AI tools)
- Documentation drafting
- Requirements analysis
- Test case generation
- Traceability matrix creation

**What humans do:**
- All validation decisions
- Risk assessments
- Verification of AI outputs
- Final approvals
- Regulatory accountability

**Transparency:**  
Every AI-assisted document includes metadata showing:
- Which AI tool was used
- When it was drafted
- How human review was performed
- Verification method and confidence level
- Final human accountability

**See:** [AI_Process_Documentation.md](./AI_Process_Documentation.md) for complete details.

**Example format:**
```markdown
## AI Assistance Record

**AI Tool Used:** Claude 3.5 Sonnet (Anthropic)
**Date Generated:** 2026-02-04
**Human Reviewer:** Shyaam
**Verification Method:** Code investigation cross-check, manual testing validation
**Confidence Level:** High
**Final Accountability:** Shyaam (Validation Engineer)
```

---

## Skills Library

The `/Skills/` folder contains 8 step-by-step guides that walk through each phase of the validation workflow. These guides provide:

- Specific instructions for what to do at each step
- Real examples from the Login and Logout features
- Templates you can adapt for your own validation work
- Quality checks to verify your work

**The 8 guides cover:**
1. **Feature Observation** - Document what the software does through manual testing
2. **Scope Definition** - Determine what's included vs excluded in validation
3. **Code Investigation** - Analyze the source code systematically
4. **Design Specification** - Document the technical implementation
5. **Functional Requirements** - Describe what the system does (independent of how it's built)
6. **User Requirements** - Capture what users need the system to do
7. **Test Protocol** - Create test cases with full traceability
8. **Verification Report** - Document how you verified AI-generated content

Each guide includes detailed instructions, real examples, and can be used with any AI tool (Claude, ChatGPT, Gemini, etc.).

**See:** [`/Skills/README.md`](./Skills/README.md) for complete documentation and usage examples.

---

## Validation Results

### Feature 1: Admin Login
- **Status:** ✅ Documentation Complete (Tests pending execution)
- **Time Investment:** ~12 hours (baseline for methodology development)
- **Documents:** 8 validation artifacts (Observation → Summary)
- **Traceability:** Complete (URS → FRS → DS → OQ)

### Feature 2: Admin Logout
- **Status:** ✅ Documentation Complete (Tests pending execution)
- **Time Investment:** ~4 hours (67% faster than Feature 1)
- **Documents:** 8 validation artifacts
- **Methodology Acceleration:** Demonstrated on second feature

**Key Insight:** Methodology acceleration observed - second feature completed in 1/3 the time of the first, showing the approach scales and improves with practice.

---

## How to Use This Repository

### For Validation Professionals
1. **Learn the approach:** Read [`/Skills/README.md`](./Skills/README.md) - see the step-by-step guides
2. **See it in action:** Review [AI_Process_Documentation.md](./AI_Process_Documentation.md) - real examples from Login/Logout
3. **Try a guide:** Start with Feature Observation and apply it to your own software
4. **See complete package:** Explore [`/01_Login/`](./01_Login/) - full validation artifacts
5. **Adapt for your work:** Use the guides as starting points for your own validation projects

### For QA/Testing Practitioners
1. **Black-box testing:** See `Feature_Observation_Login.md` for systematic observation approach
2. **AI verification:** Review `Verification_Report_Login.md` for how AI outputs are validated
3. **Traceability:** Study URS → FRS → DS → OQ structure
4. **Test protocols:** See how test cases are created with full traceability

### For AI Practitioners
1. **Context engineering:** See `Application_Context.md` for application knowledge structure
2. **Verification methods:** Learn commission vs omission error checking approaches
3. **Workflow patterns:** See how AI is integrated into validation workflows
4. **Transparency:** Study how AI usage is documented for audit readiness

---

## Technical Details

### Application Under Validation
**Voice analysis platform** — employability assessment application used by HR professionals and NGO administrators.
- **Technology:** React, TypeScript, Vite
- **Deployment:** Vercel (production)
- **Users:** NGO administrators, HR professionals
- **Purpose:** Behavioral skills assessment through voice analysis
- **Data:** Client PII (persistent), voice recordings (ephemeral), assessment results

### Tools & Technologies
- **AI Tools:** Claude 3.5 Sonnet (Anthropic), Claude Code, ChatGPT
- **Version Control:** Git + GitHub
- **Documentation:** Markdown (human-readable, version-controlled)
- **Traceability:** Markdown cross-references

---

## Structure Principles

- **Step-by-step guides:** Clear instructions for each validation phase (not just examples)
- **Feature-centric:** Each feature validated as independent unit with complete traceability
- **Transparency:** All AI usage documented with verification methods
- **Works with any AI:** Guides work with Claude, ChatGPT, Gemini, or other tools
- **Audit-friendly:** All documents human-readable, version-controlled, traceable

---

## Repository Goals

1. **Demonstrate systematic validation methodology** suitable for regulated industries
2. **Provide practical guides** applicable to other validation projects
3. **Document AI-assisted workflows** that maintain GxP compliance
4. **Enable replication** through transparent process documentation

---

## Contributing

This repository documents an active exploration. Feedback, questions, and discussions are welcome through GitHub issues or discussions.

**Areas of interest:**
- GxP validation best practices
- AI tool usage in regulated environments
- Applying these guides to other validation projects
- Verification methods for AI-generated content
- Building application-specific context for AI tools

---

## License

This methodology documentation is shared for educational and professional reference purposes.

**Code and validation artifacts:** Demonstration purposes only. Not for production use without proper qualification and validation.

---

## Contact

**LinkedIn:** [Connect for discussions on AI-native validation](https://www.linkedin.com/in/shyaamlal-n-n/)  
**GitHub Issues:** For questions, feedback, or methodology discussions

---

*This repository represents a practical exploration of AI-assisted validation methodologies for regulated industries. All validation decisions, risk assessments, and regulatory conclusions remain under human authority and accountability.*