# Validation Methodology

**Purpose:** This document defines the systematic validation approach used throughout this repository. It serves as the "playbook" for AI-assisted validation work while maintaining GxP compliance.

---

## Validation Approach

### Primary Mode: Retrospective Validation

This methodology primarily demonstrates **retrospective (as-built) validation** per GAMP 5 Appendix M3.

**Characteristics:**
- System already exists without formal validation documentation
- Requirements are documented retrospectively based on observed behavior
- Implementation is analyzed to understand design decisions
- Validation verifies system operates as documented

**When to use:** Validating existing systems (legacy applications, undocumented features)

This approach is common in startups, internal tools, and systems developed prior to formal validation adoption.
---

### Secondary Capability: Greenfield Validation

The same workflow adapts to **greenfield validation** when formal requirements exist upfront.

**Characteristics:**
- Requirements (FRS/acceptance criteria) provided before implementation
- Test cases derived directly from requirements
- Less investigation needed, more verification focus
- Faster execution (2-3 hours vs 6-8 hours per feature)

**When to use:** New features with documented requirements, formal development projects

---

## Scope of This Methodology

This methodology defines **how validation work is performed**, not the content of any single validation package.

Feature-specific details, risks, and test cases are documented within individual feature folders (e.g., `01_Login/`) and are not duplicated here.

This document remains stable across features and evolves only when:
- Validation patterns change
- Regulatory interpretation changes
- Workflow improvements are identified

---

## Core Validation Workflow

### Standard Process (10 Steps)

**Phase 1: Investigation**

**1. Feature Observation**
- Manual UI testing and behavioral documentation
- Black-box functional testing from user perspective
- Text-based descriptions (no proprietary screenshots to cloud services)
- Document: `Feature_Observation_[Feature].md`

**2. Feature Boundary Definition**
- Define IN/OUT scope with clear rationale
- Separate feature validation from related features
- Document assumptions and constraints
- Document: `Feature_Boundary_Definition_[Feature].md`

**3. Code Investigation** (optional - for retrospective validation)
- Use local AI tools (Claude Code) to investigate implementation
- Analyze technical architecture and design decisions
- Identify all relevant files and components
- Document: `[Feature]_Code_Investigation.md`

**4. AI Investigation Verification**
- Validate AI investigation accuracy through manual testing
- Three-layer checks: commission errors, omission errors, scope accuracy
- Establish ground truth before proceeding to requirements
- Document: `Verification_Report_[Feature].md`

---

**Phase 2: Requirements Documentation**

**5. Design Specification (DS)**
- Document as-built implementation details
- Technical architecture and data flow
- Implementation decisions and constraints
- Document: `DS_[Feature].md`

**6. Functional Requirements Specification (FRS)**
- Document system behavior (WHAT the system does)
- Functional behaviors without implementation details
- Acceptance criteria for each requirement
- Document: `FRS_[Feature].md`

**7. User Requirements Specification (URS)**
- Document user needs (WHY users need it)
- Business rationale and user perspective
- Risk context and acceptance criteria
- Document: `URS_[Feature].md`

**Note:** Steps 5-7 may be iterated or reordered depending on available documentation and system maturity. In retrospective validation, this DS→FRS→URS ordering is normal and appropriate.

---

**Phase 3: Test Planning & Execution**

**8. OQ Protocol Development**
- Create test cases with full traceability
- Map requirements to test cases (URS → FRS → DS → OQ)
- Define acceptance criteria and evidence requirements
- Document: `OQ_Protocol_[Feature].md`

**9. Test Execution**
- Execute test cases manually
- Capture evidence (screenshots, notes, observations)
- Document pass/fail results
- Update OQ Protocol with actual results

**10. Validation Summary**
- Package overview and status
- Traceability verification
- Validation conclusion
- Document: `Validation_Summary_[Feature].md`

---

## AI Tool Usage

### Tools and Roles

**Claude Code (Local AI):**
- Code investigation and file analysis
- Validation document creation
- Local file editing and generation
- No code uploaded to cloud servers

**Claude Web (Cloud AI):**
- Strategic discussions and methodology
- Requirements analysis and refinement
- Template generation
- Text-based inputs only (no proprietary code/screenshots)

---

### AI as GAMP 5 Category 1 Tool

AI tools are used as **authoring tools** (GAMP 5 Category 1), not qualified execution tools.

**Key Principles:**

**AI outputs are treated as hypotheses until verified**
- All AI-generated investigation findings verified through manual testing
- All AI-generated requirements reviewed for accuracy and completeness
- All AI-generated test cases reviewed for adequacy and traceability

**Human oversight retained for:**
- All validation decisions and approvals
- Risk assessments and scope boundaries
- Traceability decisions and mappings (not clerical work)
- Final regulatory accountability

**Compliance boundaries:**
- No proprietary code uploaded to cloud AI services
- No screenshots containing IP uploaded to cloud services
- Text-based descriptions used for cloud AI interactions
- Local AI tools used for code analysis

---

### Verification Methodology

**Three-Layer Verification of AI Outputs:**

**1. Commission Error Check**
- Verify factual claims made by AI are accurate
- Manual testing to confirm behaviors documented
- Code inspection to verify technical claims

**2. Omission Error Check**
- Verify AI didn't miss relevant files, features, or behaviors
- File inventory comparison
- Completeness verification through systematic checks

**3. Scope Accuracy Check**
- Verify AI correctly identified feature boundaries
- Confirm no conflation of separate features
- Validate that out-of-scope items correctly excluded

---

## Regulatory Standards

### Primary Standards

**GAMP 5: Good Automated Manufacturing Practice**
- Risk-based approach to GxP compliance
- Category 1 tool classification for AI authoring tools
- Appendix M3: Retrospective validation of legacy systems

**IEC 62304: Medical Device Software Lifecycle**
- Software requirements and design documentation
- Traceability maintenance throughout lifecycle
- Risk management integration

**21 CFR Part 11: Electronic Records and Signatures** (where applicable)
- Electronic record integrity
- System access controls
- Audit trail requirements

---

## Quality Gates

### Requirements for Proceeding

Before moving to next validation phase:

✅ **All requirements have test coverage**
- Every URS requirement traces to FRS
- Every FRS requirement traces to DS
- Every requirement has corresponding test case(s)

✅ **Bidirectional traceability complete**
- URS ↔ FRS ↔ DS ↔ OQ mapping verified
- No orphaned requirements
- No untraceable test cases

✅ **AI outputs verified by manual testing**
- Commission errors: Specific AI claims tested and confirmed
- Omission errors: Completeness verified through [full inventory | filtered search | sampling]
- Verification method and confidence level documented in Verification Report

✅ **Scope boundaries documented with rationale**
- IN/OUT scope clearly defined
- Rationale provided for all boundary decisions
- Assumptions and constraints documented

✅ **Validation artifacts reproducible from documented context**
- All decisions traceable to requirements or observations
- Context files enable regeneration of documentation
- Methodology and rationale clearly documented

✅ **Test execution complete with evidence (for "Validated" status)**
- OQ Protocol exists
- Tests executed by qualified tester (with date)
- Results documented (pass/fail for each test case)
- Evidence captured (screenshots/notes/observations)
- Deviations documented (if any failures/anomalies)
Note: This gate distinguishes "Documentation Complete" from "Validation Complete"

---

## Time Estimates

### Typical Feature Validation Duration

**First feature (establishing methodology):** 6-8 hours
- Includes learning and methodology refinement
- Full investigation and verification
- Template creation

**Subsequent features (methodology established):** 2-4 hours
- Applying proven workflow
- Reusing templates and patterns
- Faster verification (spot checks vs full validation)

**Complex features (multi-step workflows):** 4-6 hours
- Multiple sub-features or workflows
- Extensive integration points
- Higher risk requiring thorough analysis

**Note:** Time varies based on documentation availability (greenfield vs retrospective) and feature complexity. These are estimates, not commitments.

---

## Adaptations for Different Scenarios

### Retrospective Validation (No Existing Requirements)

**Starting point:** Existing feature, no documentation

**Workflow emphasis:**
1. Thorough observation and investigation
2. AI investigation verification (critical step)
3. Requirements written retrospectively from behavior
4. Full 10-step process

**Time:** 6-8 hours first feature, 3-4 hours subsequent

---

### Greenfield Validation (Requirements Exist)

**Starting point:** FRS or acceptance criteria provided

**Workflow emphasis:**
1. Paste requirements into AI tool
2. Analyze for testability
3. Define test boundaries
4. Create OQ protocol directly from requirements
5. Skip investigation/verification steps

**Time:** 2-3 hours per feature

---

### Decision Tree

**Do formal requirements (FRS) exist?**

**YES → Greenfield approach:**
- Paste FRS, analyze, create OQ
- Focus on test case quality
- Minimal investigation needed

**NO → Retrospective approach:**
- Observe, investigate, verify
- Create requirements retrospectively
- Full 10-step workflow

---

## Traceability Management

### Requirements Hierarchy
```
Business Need
    ↓
User Requirements (URS) - WHAT users need
    ↓
Functional Requirements (FRS) - WHAT system does
    ↓
Design Specification (DS) - HOW system implements
    ↓
Test Cases (OQ) - VERIFY it works
```

### Traceability Rules

**Forward traceability:**
- Each URS requirement → one or more FRS requirements
- Each FRS requirement → one or more DS specifications
- Each FRS requirement → one or more OQ test cases

**Backward traceability:**
- Each test case → specific FRS requirement
- Each FRS requirement → specific URS requirement
- Each DS specification → specific FRS requirement

**Verification:**
- No orphaned requirements (missing traces)
- No untraceable test cases
- 100% coverage verified before test execution

---

## Context Management

### Context Files Enable AI Accuracy

**Without context:**
- AI produces generic, templated outputs
- No application-specific risk awareness
- Missing domain knowledge

**With context:**
- AI produces Sambhava-specific documentation
- Considers business impact and workflows
- Applies learned patterns from previous features

### Required Context Loading

**Every AI validation session begins with:**
```
Read 00_Project_Context\ for full context:
- Methodology.md (this file)
- Sambhava_Application_Context.md (application knowledge)
- Skills\ (accumulated patterns)

Starting [Feature Name] validation...
```

---

## Session Workflow

### Starting a Validation Session

**1. Load Context**
```
Read 00_Project_Context\ for full context.
Starting [Feature] validation...
```

**2. Define Objective**
- Which feature are you validating?
- Retrospective or greenfield approach?
- What's the expected outcome?

**3. Execute Workflow**
- Follow 10-step process
- Use AI for investigation and drafting
- Human reviews and approves all outputs

---

### Ending a Validation Session

**1. Ask AI for Update Recommendations**
```
Session complete. Based on today's work, what should I update in 00_Project_Context/?
```

**2. AI Suggests Updates**
- Create Thread Summary? (always yes)
- Update Skills? (if new patterns learned)
- Update Application Context? (if new facts discovered)

**3. Commit to Version Control**
```bash
git add .
git commit -m "Complete [Feature] validation - [brief summary]"
```

---

## Continuous Improvement

### After Each Feature Validation

**Document learnings:**
- What worked well?
- What could be streamlined?
- What patterns emerged?

**Update Skills:**
- Add new decision frameworks
- Refine existing patterns
- Document edge cases discovered

**Refine Templates:**
- Improve document structures
- Add sections that proved valuable
- Remove unnecessary content

---

## Validation Package Structure

### Complete Feature Validation Package

Each validated feature produces:

**Investigation & Observation:**
- Feature_Observation_[Feature].md
- Feature_Boundary_Definition_[Feature].md
- Verification_Report_[Feature].md (if retrospective)

**Requirements Documentation:**
- URS_[Feature].md
- FRS_[Feature].md
- DS_[Feature].md

**Testing Documentation:**
- OQ_Protocol_[Feature].md (with test execution results)
- Validation_Summary_[Feature].md

**Supporting Materials:**
- Traceability matrix updates
- Thread summary
- Skills updates (if applicable)

---

## Success Criteria

### What Defines a Successful Validation?

**Documentation completeness:**
- All required documents created
- All sections filled with meaningful content
- No placeholders or "TBD" items

**Traceability integrity:**
- 100% requirements coverage
- Bidirectional tracing verified
- No gaps or orphaned items

**Test adequacy:**
- All requirements have test cases
- Test cases are executable and specific
- Acceptance criteria are verifiable

**Audit readiness:**
- Clear rationale for all decisions
- Evidence of verification activities
- Human oversight and approval documented

**Reproducibility:**
- Another validator could recreate the work
- Decisions traceable to requirements or context
- Methodology clearly documented

---

## Risk-Based Approach

### Validation Rigor Based on Risk

**High-Risk Features:**
- Patient safety impact
- Data integrity critical
- Regulatory submission required
- **Approach:** Full 10-step process, extensive verification

**Medium-Risk Features:**
- Business process impact
- User experience critical
- Audit scrutiny expected
- **Approach:** Standard workflow, focused verification

**Low-Risk Features:**
- Cosmetic or minor changes
- Limited user impact
- Internal tools only
- **Approach:** Streamlined workflow, spot checks acceptable

---

## Common Challenges & Solutions

### Challenge: AI Investigation Incomplete

**Solution:** Three-layer verification methodology
- Always verify AI findings manually
- Use file inventory comparison
- Check for omission errors systematically

### Challenge: Scope Creep During Validation

**Solution:** Feature Boundary Definition document
- Define scope upfront with rationale
- Separate concerns (authentication vs authorization)
- Document what's OUT of scope explicitly

### Challenge: Maintaining Traceability

**Solution:** Centralized traceability matrix
- Update after each requirements document
- Verify bidirectional traces
- Flag gaps before test execution

### Challenge: Context Gets Outdated

**Solution:** Ask AI at session end
- "What should I update in context?"
- Update when it makes sense
- Quality over exhaustiveness

---

## Methodology Evolution

This methodology is a living document. It evolves based on:
- Lessons learned from validation work
- Industry best practice developments
- Regulatory guidance updates
- Practical workflow refinements

**Update triggers:**
- After validating 3-5 features (patterns solidify)
- When discovering better approaches
- When regulatory guidance changes
- When tools or technology evolves

---

## Key Principles

**1. Systematic over ad-hoc**
- Defined workflow, consistent application
- Reproducible process

**2. Verified over assumed**
- AI outputs are hypotheses until proven
- Manual verification essential

**3. Traceable over convenient**
- Every decision has rationale
- Every requirement has test coverage

**4. Practical over perfect**
- Good documentation beats perfect documentation
- Ship complete validation packages

**5. Context-aware over generic**
- Application knowledge drives accuracy
- Domain expertise accumulates over time

---

Note: Thread summaries document intentions and learnings. Verification reports document what was actually verified. When in doubt, verification report is source of truth.

*This methodology balances regulatory compliance with practical efficiency. It leverages AI capabilities while maintaining human oversight and accountability required in GxP environments.*