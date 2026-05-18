---
artifact_type: Risk_Assessment
feature: SmokeTest
version: 1.0
status: Draft
ai_assistance:
  agent_skill: validation-risk-assessment
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-17T15:00:00Z
  prompt_version: v1.0
human_review:
  reviewer: null
  approval_timestamp: null
  comment: null
traceability:
  upstream: [Feature_Scoping_SmokeTest.md]
risk_classification:
  category: GAMP Category 4
---

# Risk Assessment — SmokeTest

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
