"""Smoke test for the 8 per-rung validators + release_summary.

Generates minimal synthetic valid and invalid artifacts for each rung, runs
the corresponding validator, and reports expected-vs-actual outcomes. This is
a unit test of the validators — NOT an end-to-end framework test. The end-to-
end test is Phase 4 of the Build Plan (dog-food run against a real feature).

Run from repo root:
    python validators/_smoke_test.py

Cleans up after itself (the _smoke_artifacts/ folder is rewritten on each run).
"""

from __future__ import annotations

import importlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEST_ROOT = REPO_ROOT / "validators" / "_smoke_artifacts"

# ---------------------------------------------------------------------------
# Synthetic artifact bodies
# ---------------------------------------------------------------------------

VALID_FRONTMATTER_BASE = """---
artifact_type: {artifact_type}
feature: SmokeTest
version: 1.0
status: Draft
ai_assistance:
  agent_skill: {skill}
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-17T15:00:00Z
  prompt_version: v1.0
human_review:
  reviewer: null
  approval_timestamp: null
  comment: null
traceability:
  upstream: {upstream_list}
{extra_fm}---

"""


def fm(artifact_type: str, skill: str, upstream_list: str = "[]", extra_fm: str = "") -> str:
    return VALID_FRONTMATTER_BASE.format(
        artifact_type=artifact_type,
        skill=skill,
        upstream_list=upstream_list,
        extra_fm=extra_fm,
    )


# ---- Feature Scoping ------------------------------------------------------

VALID_FEATURE_SCOPING = fm("Feature_Scoping", "validation-feature-scoping") + """# Feature Scoping — SmokeTest

## 1. Feature Identity
- **Feature name:** SmokeTest
- **System under observation:** synthetic test system
- **Access method:** synthetic
- **Observer date:** 2026-05-17
- **Scoping scenario:** Synthetic minimal scoping for validator smoke test.

## 2. Observed Behaviour

### 2.1. Successful Submit
- **User action(s):** 1. Click Submit
- **System response:** Confirmation message appears.
- **Visual feedback:** Green banner displayed at top of page.
- **Behavioural outcome:** New record created in the system.

## 3. User Interface Elements
- Submit button (primary action)
- Confirmation banner area

## 4. Feature Boundary
- **In the feature:** the submit flow
- **Adjacent but separate:** authentication, downstream notifications

## 5. Open Questions
1. Is the confirmation banner dismissable?

## 6. Observation Notes
Synthetic artifact for validator smoke test. No real system was observed.
"""

INVALID_FEATURE_SCOPING_PLACEHOLDER = VALID_FEATURE_SCOPING.replace(
    "Green banner displayed at top of page.",
    "[Document what happened - placeholder injected for smoke test]",
)


# ---- Risk Assessment ------------------------------------------------------

VALID_RISK_ASSESSMENT = fm(
    "Risk_Assessment",
    "validation-risk-assessment",
    upstream_list="[Feature_Scoping_SmokeTest.md]",
    extra_fm="risk_classification:\n  framework: GAMP 5 RBA\n  category: GAMP Category 4\n",
) + """# Risk Assessment — SmokeTest

## 1. Framework Applied
- **Framework:** GAMP 5 RBA
- **Selection rationale:** Organisation-standard for IT GxP systems.

## 2. GxP Impact Assessment
The feature touches no GxP records directly. Medium impact via downstream notification.

## 3. Patient Safety Risk
No direct patient safety risk identified. Severity Low.

## 4. Data Integrity Risk
Creates a record; ALCOA+ Attributable and Contemporaneous attributes apply. Audit trail required.

## 5. Risk Classification
GAMP Category 4. Configured COTS with low patient-safety impact.

## 6. Downstream Implications
Standard OQ depth required. No supplier audit. OQ should target audit-trail capture.
"""

INVALID_RISK_ASSESSMENT_MISSING_FRAMEWORK_FM = fm(
    "Risk_Assessment",
    "validation-risk-assessment",
    upstream_list="[Feature_Scoping_SmokeTest.md]",
    extra_fm="risk_classification:\n  category: GAMP Category 4\n",
) + VALID_RISK_ASSESSMENT.split("---\n\n", 1)[1]


# ---- Validation Scope -----------------------------------------------------

VALID_VALIDATION_SCOPE = fm(
    "Validation_Scope",
    "validation-scope",
    upstream_list="[Feature_Scoping_SmokeTest.md, Risk_Assessment_SmokeTest.md]",
) + """# Validation Scope — SmokeTest

## 1. Validation Objective
Demonstrate the submit flow operates correctly under defined acceptance criteria.

## 2. In Scope

### 2.1. Successful submit
- **Observed behaviour reference:** Feature Scoping §2.1
- **Risk reference:** Risk Assessment §4
- **Validation depth:** functional verification, audit-trail capture
- **Rationale:** Primary risk driver per Risk Assessment.

## 3. Out of Scope

### 3.1. Cosmetic banner styling
- **Observed behaviour reference:** Feature Scoping §3
- **Rationale for exclusion:** Cosmetic-only, no data integrity impact.

## 4. Assumptions
The authentication layer is qualified separately.

## 5. Exit Criteria
All in-scope test cases pass; audit-trail entries observed.

## 6. Open Questions for the Human
None.
"""

INVALID_VALIDATION_SCOPE_NO_RISK_REF = VALID_VALIDATION_SCOPE.replace(
    "- **Risk reference:** Risk Assessment §4\n", ""
)


# ---- URS ------------------------------------------------------------------

VALID_URS = fm(
    "URS",
    "validation-urs-author",
    upstream_list="[Feature_Scoping_SmokeTest.md, Validation_Scope_SmokeTest.md]",
) + """# User Requirements Specification — SmokeTest

## 1. Purpose
Specify user requirements for the submit flow.

## 2. Scope Reference
Covers Validation Scope §2.1.

## 3. User Requirements

| ID | Requirement | Trace |
|---|---|---|
| URS-001 | The user shall be able to submit a record. | Validation Scope §2.1 / Feature Scoping §2.1 |
| URS-002 | The system shall confirm submission with a visible message. | Validation Scope §2.1 / Feature Scoping §2.1 |

## 4. User Roles Referenced
- End user

## 5. Open Questions for the Human
None.
"""

INVALID_URS_DUPLICATE_ID = VALID_URS.replace(
    "URS-002", "URS-001"  # duplicate ID
)


# ---- FRS ------------------------------------------------------------------

VALID_FRS = fm(
    "FRS",
    "validation-frs-author",
    upstream_list="[URS_SmokeTest.md]",
) + """# Functional Requirements Specification — SmokeTest

## 1. Purpose
Specify functional behaviour for the submit flow.

## 2. Functional Requirements

### FRS-001: Record submission
- **Statement:** The system shall accept a submitted record and persist it.
- **Trace:** URS-001
- **Acceptance criteria:**
  - **AC-FRS-001.1** — Given a valid record, when the user submits, then the system persists the record and returns a confirmation within 2 seconds.

### FRS-002: Confirmation display
- **Statement:** The system shall display a confirmation message after a successful submit.
- **Trace:** URS-002
- **Acceptance criteria:**
  - **AC-FRS-002.1** — Given a successful submit, when the response returns, then the confirmation message shall be visible to the user.

## 3. Functional Roles
- Submission service
- Audit logger

## 4. Open Questions for the Human
None.
"""

INVALID_FRS_NO_AC = VALID_FRS.replace(
    "  - **AC-FRS-001.1** — Given a valid record, when the user submits, then the system persists the record and returns a confirmation within 2 seconds.\n",
    "",
)


# ---- OQ Protocol ----------------------------------------------------------

VALID_OQ_PROTOCOL = fm(
    "OQ_Protocol",
    "validation-oq-protocol-author",
    upstream_list="[URS_SmokeTest.md, FRS_SmokeTest.md]",
) + """# OQ Protocol — SmokeTest

## 1. Purpose
Verify the submit flow meets its acceptance criteria.

## 2. Test Environment Requirements
- **System under test:** synthetic test system
- **Required role(s):** End user
- **Test data prerequisites:** None
- **Browser / tool requirements (if applicable):** N/A

## 3. Test Cases

### TC-001: Successful submit
- **Trace:** AC-FRS-001.1
- **Preconditions:** User is authenticated.
- **Steps:**
  1. Enter valid record data.
  2. Click Submit.
- **Expected result:** Confirmation message appears within 2 seconds.
- **Pass criteria:** AC-FRS-001.1 satisfied — record persisted and confirmation visible.

### TC-002: Confirmation visibility
- **Trace:** AC-FRS-002.1
- **Preconditions:** TC-001 has executed successfully.
- **Steps:**
  1. Observe the page after submit.
- **Expected result:** Confirmation message is visible.
- **Pass criteria:** AC-FRS-002.1 satisfied — message visible to user.

## 4. Traceability Coverage
AC-FRS-001.1 covered by TC-001; AC-FRS-002.1 covered by TC-002. All FRS acceptance criteria covered.
"""

INVALID_OQ_PROTOCOL_NO_AC_TRACE = VALID_OQ_PROTOCOL.replace(
    "- **Trace:** AC-FRS-001.1\n", "- **Trace:** (intentionally omitted for smoke test)\n"
)


# ---- OQ Execution Record --------------------------------------------------

VALID_OQ_EXECUTION = fm(
    "OQ_Execution_Record",
    "validation-oq-execution",
    upstream_list="[OQ_Protocol_SmokeTest.md]",
    extra_fm="execution_context:\n  mode: human-record-consumed\n  executor: shyaamlal\n  environment_url: https://synthetic.local\n  execution_start: 2026-05-17T15:30:00Z\n  execution_end: 2026-05-17T15:45:00Z\n",
) + """# OQ Execution Record — SmokeTest

## 1. Execution Summary
- Total cases: 2
- Passed: 2
- Failed: 0
- Blocked / not executed: 0

## 2. Test Case Results

### TC-001: Successful submit
- **Trace:** AC-FRS-001.1
- **Steps executed:** Executed exactly as written in OQ Protocol §3.
- **Actual result:** Confirmation message appeared within 1.2 seconds.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** n/a (synthetic smoke test)
- **Deviations:** none

### TC-002: Confirmation visibility
- **Trace:** AC-FRS-002.1
- **Steps executed:** Executed exactly as written in OQ Protocol §3.
- **Actual result:** Confirmation message visible.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** n/a
- **Deviations:** none

## 3. Deviations Summary
No deviations from the protocol.

## 4. Bugs / Anomalies Surfaced
None.
"""

INVALID_OQ_EXECUTION_MISSING_TC = VALID_OQ_EXECUTION.replace(
    """### TC-002: Confirmation visibility
- **Trace:** AC-FRS-002.1
- **Steps executed:** Executed exactly as written in OQ Protocol §3.
- **Actual result:** Confirmation message visible.
- **Pass / Fail / Blocked:** Pass
- **Evidence:** n/a
- **Deviations:** none

""",
    "",
)


# ---- Summary Report -------------------------------------------------------

VALID_SUMMARY_REPORT = fm(
    "Validation_Summary_Report",
    "validation-summary-report",
    upstream_list="[Feature_Scoping_SmokeTest.md, Risk_Assessment_SmokeTest.md, Validation_Scope_SmokeTest.md, URS_SmokeTest.md, FRS_SmokeTest.md, OQ_Protocol_SmokeTest.md, OQ_Execution_Record_SmokeTest.md]",
    extra_fm="validation_status: Pass\n",
) + """# Validation Summary Report — SmokeTest

## 1. Executive Summary
SmokeTest feature validated end-to-end. All acceptance criteria met.

## 2. Risk Classification
GAMP Category 4 per Risk_Assessment_SmokeTest.md §5. Framework: GAMP 5 RBA.

## 3. Validation Scope Summary
- In-scope items: 1 (Validation_Scope_SmokeTest.md §2.1)
- Out-of-scope items: 1 (Validation_Scope_SmokeTest.md §3.1)

## 4. Requirements Coverage
- URS items: 2
- FRS items: 2
- AC count: 2
- OQ test cases: 2
- AC coverage by test cases: 100%

## 5. Test Execution Outcome
- Total cases executed: 2
- Pass: 2
- Fail: 0
- Blocked: 0
- Deviations: 0
- Bugs / anomalies: 0

## 6. AI Assistance Summary
Synthetic test — no real agent invocations logged. Audit log would show 7 entries.

## 7. Validation Status
- **Status:** Pass
- **Justification:** Full AC coverage; 2/2 test cases passed; no deviations.

## 8. Open Items
None.

## 9. References
All artifacts listed in frontmatter.
"""

INVALID_SUMMARY_REPORT_BAD_STATUS = VALID_SUMMARY_REPORT.replace(
    "validation_status: Pass", "validation_status: TotallyValid"
)


# ---- Release Summary ------------------------------------------------------

VALID_RELEASE_SUMMARY = """---
artifact_type: Release_Validation_Summary
change_request: CR-SMOKE-001
features_in_scope: [SmokeTest]
version: 1.0
status: Draft
ai_assistance:
  agent_skill: validation-release-summary
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-17T16:00:00Z
  prompt_version: v1.0
human_review:
  reviewer: null
  approval_timestamp: null
  comment: null
release_status: Pass
---

# Release Validation Summary — CR-SMOKE-001

## 1. Release Scope
- Change request: CR-SMOKE-001
- Features in scope: SmokeTest (Validation_Summary_Report_SmokeTest.md)
- Out of scope: none

## 2. Per-Feature Outcomes

| Feature | Validation Status | Risk Classification | Pass / Fail / Blocked | Report Path |
|---|---|---|---|---|
| SmokeTest | Pass | GAMP Category 4 | 2 / 0 / 0 | `01_SmokeTest/Validation_Summary_Report_SmokeTest.md` |

## 3. Aggregate Risk Profile
Highest classification: GAMP Category 4. Single feature in scope.

## 4. Aggregate Requirements Coverage
- Total URS items across release: 2
- Total FRS items: 2
- Total acceptance criteria: 2
- Total OQ test cases: 2
- Aggregate AC coverage: 100%

## 5. Aggregate Test Outcome
- Total cases executed: 2
- Pass: 2
- Fail: 0
- Blocked: 0
- Open deviations: 0
- Open bugs / anomalies: 0

## 6. Aggregate AI Assistance Summary
Synthetic test — no real entries.

## 7. Release Validation Status
- **Status:** Pass
- **Justification:** Single feature in scope, fully validated, no open items.
- **Recommendation to CAB:** approve

## 8. Open Items for the Change Advisory Board
None.

## 9. References
- 01_SmokeTest/Validation_Summary_Report_SmokeTest.md
"""

INVALID_RELEASE_SUMMARY_BAD_STATUS = VALID_RELEASE_SUMMARY.replace(
    "release_status: Pass", "release_status: ShipIt"
)


# ---------------------------------------------------------------------------
# Test case registry
# ---------------------------------------------------------------------------

CASES = [
    # (case_name, validator_module, artifact_filename, content, expected_pass)
    ("feature_scoping / valid", "feature_scoping", "Feature_Scoping_SmokeTest.md", VALID_FEATURE_SCOPING, True),
    ("feature_scoping / placeholder", "feature_scoping", "Feature_Scoping_SmokeTest.md", INVALID_FEATURE_SCOPING_PLACEHOLDER, False),
    ("risk_assessment / valid", "risk_assessment", "Risk_Assessment_SmokeTest.md", VALID_RISK_ASSESSMENT, True),
    ("risk_assessment / missing framework", "risk_assessment", "Risk_Assessment_SmokeTest.md", INVALID_RISK_ASSESSMENT_MISSING_FRAMEWORK_FM, False),
    ("validation_scope / valid", "validation_scope", "Validation_Scope_SmokeTest.md", VALID_VALIDATION_SCOPE, True),
    ("validation_scope / missing risk ref", "validation_scope", "Validation_Scope_SmokeTest.md", INVALID_VALIDATION_SCOPE_NO_RISK_REF, False),
    ("urs / valid", "urs", "URS_SmokeTest.md", VALID_URS, True),
    ("urs / duplicate ID", "urs", "URS_SmokeTest.md", INVALID_URS_DUPLICATE_ID, False),
    ("frs / valid", "frs", "FRS_SmokeTest.md", VALID_FRS, True),
    ("frs / no AC on item", "frs", "FRS_SmokeTest.md", INVALID_FRS_NO_AC, False),
    ("oq_protocol / valid", "oq_protocol", "OQ_Protocol_SmokeTest.md", VALID_OQ_PROTOCOL, True),
    ("oq_protocol / no AC trace", "oq_protocol", "OQ_Protocol_SmokeTest.md", INVALID_OQ_PROTOCOL_NO_AC_TRACE, False),
    # OQ Execution requires the sibling protocol file in same folder — handled below.
    ("oq_execution / valid", "oq_execution", "OQ_Execution_Record_SmokeTest.md", VALID_OQ_EXECUTION, True),
    ("oq_execution / missing TC result", "oq_execution", "OQ_Execution_Record_SmokeTest.md", INVALID_OQ_EXECUTION_MISSING_TC, False),
    ("summary_report / valid", "summary_report", "Validation_Summary_Report_SmokeTest.md", VALID_SUMMARY_REPORT, True),
    ("summary_report / bad status", "summary_report", "Validation_Summary_Report_SmokeTest.md", INVALID_SUMMARY_REPORT_BAD_STATUS, False),
    ("release_summary / valid", "release_summary", "Release_Validation_Summary_CR-SMOKE-001.md", VALID_RELEASE_SUMMARY, True),
    ("release_summary / bad status", "release_summary", "Release_Validation_Summary_CR-SMOKE-001.md", INVALID_RELEASE_SUMMARY_BAD_STATUS, False),
]


def run_one(case_name: str, validator: str, filename: str, content: str, expected: bool) -> dict:
    case_dir = TEST_ROOT / case_name.replace(" / ", "__").replace(" ", "_")
    case_dir.mkdir(parents=True, exist_ok=True)

    # OQ Execution validator looks for sibling OQ_Protocol_*.md in same folder.
    if validator == "oq_execution":
        (case_dir / "OQ_Protocol_SmokeTest.md").write_text(VALID_OQ_PROTOCOL, encoding="utf-8")

    artifact = case_dir / filename
    artifact.write_text(content, encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "validators" / f"{validator}.py"), str(artifact)],
        capture_output=True,
        text=True,
    )

    try:
        parsed = json.loads(result.stdout)
    except json.JSONDecodeError:
        parsed = {"pass": None, "errors": ["validator output not parseable"]}

    actual = parsed.get("pass")
    match = (actual == expected)

    return {
        "case": case_name,
        "validator": validator,
        "expected": "pass" if expected else "fail",
        "actual": "pass" if actual else ("fail" if actual is False else "?"),
        "match": match,
        "errors": parsed.get("errors", []),
    }


def main() -> int:
    if TEST_ROOT.exists():
        shutil.rmtree(TEST_ROOT)
    TEST_ROOT.mkdir(parents=True)

    results = [run_one(*case) for case in CASES]

    # Pretty table
    header = f"{'CASE':<42} {'VALIDATOR':<18} {'EXPECTED':<10} {'ACTUAL':<10} {'MATCH'}"
    print(header)
    print("-" * len(header))
    for r in results:
        flag = "OK" if r["match"] else "MISMATCH"
        print(
            f"{r['case']:<42} {r['validator']:<18} "
            f"{r['expected']:<10} {r['actual']:<10} {flag}"
        )

    mismatches = [r for r in results if not r["match"]]
    print()
    print(f"Total: {len(results)}  Matches: {len(results) - len(mismatches)}  Mismatches: {len(mismatches)}")

    if mismatches:
        print()
        print("--- Mismatch details ---")
        for r in mismatches:
            print(f"\n{r['case']} (validator: {r['validator']})")
            print(f"  expected {r['expected']}, got {r['actual']}")
            print(f"  errors returned:")
            for err in r["errors"][:10]:
                print(f"    - {err}")

    return 0 if not mismatches else 1


if __name__ == "__main__":
    sys.exit(main())
