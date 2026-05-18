---
artifact_type: OQ_Protocol
feature: SmokeTest
version: 1.0
status: Draft
ai_assistance:
  agent_skill: validation-oq-protocol-author
  model: claude-opus-4-7
  invocation_timestamp: 2026-05-17T15:00:00Z
  prompt_version: v1.0
human_review:
  reviewer: null
  approval_timestamp: null
  comment: null
traceability:
  upstream: [URS_SmokeTest.md, FRS_SmokeTest.md]
---

# OQ Protocol — SmokeTest

## 1. Purpose
Verify the submit flow meets its acceptance criteria.

## 2. Test Environment Requirements
- **System under test:** synthetic test system
- **Required role(s):** End user
- **Test data prerequisites:** None
- **Browser / tool requirements (if applicable):** N/A

## 3. Test Cases

### TC-001: Successful submit
- **Trace:** (intentionally omitted for smoke test)
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
