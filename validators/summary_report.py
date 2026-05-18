"""Schema validator for Validation Summary Report artifacts (Phase 8)."""

from __future__ import annotations

import sys
from pathlib import Path

from _common import (
    check_ai_assistance_subfields,
    check_artifact_type,
    check_frontmatter_present,
    check_no_placeholders,
    check_required_fields,
    check_required_sections,
    parse_frontmatter_keys,
    split_frontmatter,
    standard_cli,
)

ARTIFACT_TYPE = "Validation_Summary_Report"

REQUIRED_FRONTMATTER = [
    "artifact_type",
    "feature",
    "version",
    "status",
    "ai_assistance",
    "human_review",
    "traceability",
    "validation_status",
]

REQUIRED_SECTIONS = [
    "## 1. Executive Summary",
    "## 2. Risk Classification",
    "## 3. Validation Scope Summary",
    "## 4. Requirements Coverage",
    "## 5. Test Execution Outcome",
    "## 6. AI Assistance Summary",
    "## 7. Validation Status",
]

VALID_STATUSES = {"Pass", "Conditional Pass", "Fail"}


def validate(artifact_path: Path) -> tuple[bool, list[str]]:
    text = artifact_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)

    errors: list[str] = []
    errors.extend(check_frontmatter_present(fm))
    if fm is None:
        return False, errors

    keys = parse_frontmatter_keys(fm)
    errors.extend(check_required_fields(keys, REQUIRED_FRONTMATTER))
    errors.extend(check_artifact_type(keys, ARTIFACT_TYPE))
    errors.extend(check_ai_assistance_subfields(keys))

    status = keys.get("validation_status", "")
    if status and status not in VALID_STATUSES:
        errors.append(
            f"Frontmatter validation_status must be one of {sorted(VALID_STATUSES)}, "
            f"got {status!r}."
        )

    errors.extend(check_required_sections(body, REQUIRED_SECTIONS))
    errors.extend(check_no_placeholders(text))

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("summary_report", validate))
