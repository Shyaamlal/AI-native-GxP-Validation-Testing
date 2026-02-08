# AI-Native GxP Validation Testing

**Project:** Systematic software validation for regulated life sciences environments using modern AI tooling while maintaining compliance with GAMP 5 and IEC 62304.

**Objective:** Demonstrate reproducible, feature-level validation workflows that use AI to accelerate documentation and analysis, with clear human oversight and regulatory accountability.

**Key Differentiator:** Includes reusable **Skills Library** - 8 validation skills that work with any AI tool (Claude, ChatGPT, Gemini).

**Status:** Active development - 2 features validated (Login, Logout).

---

## Quick Start

**Want to try this methodology?**
1. **For transparency:** Read [AI_Process_Documentation.md](./AI_Process_Documentation.md) - see how AI was used
2. **For replication:** Explore [`/skills/`](./skills/) folder - use these skills on your own features
3. **For examples:** Review [`/01_Login/`](./01_Login/) - complete validation package

---

## Repository Structure

```
AI-native-GxP-Validation-Testing/
│
├── skills/                          # 🎯 Reusable Validation Skills
│   ├── README.md                    # Skills Library overview
│   ├── Skills_Quick_Reference.md   # One-page lookup guide
│   ├── Skill_1_Feature_Observation_Documenter.md
│   ├── Skill_2_Scope_Boundary_Analyzer.md
│   ├── Skill_3_Technical_Investigator.md
│   ├── Skill_4_Design_Specification_Writer.md
│   ├── Skill_5_Functional_Requirements_Writer.md
│   ├── Skill_6_User_Requirements_Writer.md
│   ├── Skill_7_Test_Protocol_Generator.md
│   └── Skill_8_Verification_Reporter.md
│
├── AI_Process_Documentation.md     # 📋 How AI was used (transparency)
│
├── 00_Project_Context/              # Application and methodology knowledge
│   ├── Methodology.md               # Validation approach and workflow
│   ├── Sambhava_Application_Context.md  # Application-specific knowledge
│   └── Templates/                   # Document templates
│
├── 01_Login/                        # ✅ Feature 1: Admin Login (Complete)
│   ├── Feature_Observation_Login.md
│   ├── Feature_Boundary_Definition_Login.md
│   ├── DS_Login.md                 # Design Specification
│   ├── FRS_Login.md                # Functional Requirements
│   ├── URS_Login.md                # User Requirements
│   ├── OQ_Protocol_Login.md        # Operational Qualification
│   ├── Verification_Report_Login.md
│   └── Validation_Summary_Login.md
│
├── 02_Logout/                       # ✅ Feature 2: Admin Logout (Complete)
│   └── [Complete validation package]
│
└── README.md                        # This file
```

---

## Skills Library - The Core Differentiator

**What is it?**  
8 reusable validation skills that encapsulate domain expertise, quality criteria, and verification methods. Each skill provides fill-in-the-blank invocation patterns that work with any AI tool.

**Why it matters:**  
Most people share "prompts I used once." This shares **methodology-as-code** - reusable expertise applicable to any feature validation.

**The 8 Skills:**
1. **Feature Observation Documenter** - Organize manual test notes into structured observations
2. **Scope Boundary Analyzer** - Define IN SCOPE vs OUT OF SCOPE with rationale
3. **Technical Investigator** - Analyze code implementation systematically
4. **Design Specification Writer** - Document as-built technical design
5. **Functional Requirements Writer** - Define system behaviors (implementation-agnostic)
6. **User Requirements Writer** - Capture business needs and user expectations
7. **Test Protocol Generator** - Create executable test cases with traceability
8. **Verification Reporter** - Document AI verification methods and results

**See:** [`/skills/README.md`](./skills/README.md) for complete documentation.

**Tool-agnostic:** Works with Claude, ChatGPT, Gemini, or any AI tool.

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
1. **Learn the approach:** Read [`/skills/README.md`](./skills/README.md) - understand the Skills Library concept
2. **See it in action:** Review [AI_Process_Documentation.md](./AI_Process_Documentation.md) - real examples from Login/Logout
3. **Try a skill:** Pick Skill 1 (Feature Observation Documenter) and apply to your feature
4. **See complete package:** Explore [`/01_Login/`](./01_Login/) - full validation artifacts
5. **Adapt for your work:** Use skills as templates for your own validation projects

### For QA/Testing Practitioners
1. **Black-box testing:** See `Feature_Observation_Login.md` for systematic observation approach
2. **AI verification:** Review `Verification_Report_Login.md` for how AI outputs are validated
3. **Traceability:** Study URS → FRS → DS → OQ structure
4. **Skills application:** Try Skill 7 (Test Protocol Generator) for your test case creation

### For AI Practitioners
1. **Context engineering:** See `Sambhava_Application_Context.md` for application knowledge structure
2. **Verification methods:** Learn commission vs omission error checking approaches
3. **Methodology patterns:** Extract reusable patterns from Skills Library
4. **Transparency:** Study how AI usage is documented for audit readiness

---

## Technical Details

### Application Under Validation
**Sambhava** - Voice analysis application for employability assessment
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

- **Skills-first:** Reusable methodology encoded as skills (not just examples)
- **Feature-centric:** Each feature validated as independent unit with complete traceability
- **Transparency:** All AI usage documented with verification methods
- **Tool-agnostic:** Skills work with any AI tool (Claude, ChatGPT, Gemini)
- **Audit-friendly:** All documents human-readable, version-controlled, traceable

---

## Repository Goals

1. **Demonstrate systematic validation methodology** suitable for regulated industries
2. **Provide reusable Skills Library** applicable to other validation projects
3. **Document AI-assisted workflows** that maintain GxP compliance
4. **Enable methodology replication** through transparent process documentation

---

## Contributing

This repository documents an active exploration. Feedback, questions, and discussions are welcome through GitHub issues or discussions.

**Areas of interest:**
- GxP validation best practices
- AI tool usage in regulated environments
- Skills Library application to other validation projects
- Verification methods for AI-generated content
- Context engineering for domain-specific AI applications

---

## License

This methodology documentation is shared for educational and professional reference purposes.

**Code and validation artifacts:** Demonstration purposes only. Not for production use without proper qualification and validation.

---

## Contact

**LinkedIn:** [Connect for discussions on AI-native validation](https://www.linkedin.com/in/shyaamlal/)  
**GitHub Issues:** For questions, feedback, or methodology discussions

---

*This repository represents a practical exploration of AI-assisted validation methodologies for regulated industries. All validation decisions, risk assessments, and regulatory conclusions remain under human authority and accountability.*

**Key Differentiator:** The Skills Library is methodology-as-code - reusable validation expertise that works across features, teams, and AI tools.
