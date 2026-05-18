"""Schema validator for Release Validation Summary artifacts.

Higher-order skill — operates on a release folder containing references to
multiple per-feature Validation Summary Reports.
"""

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

ARTIFACT_TYPE = "Release_Validation_Summary"

REQUIRED_FRONTMATTER = [
    "artifact_type",
    "change_request",
    "features_in_scope",
    "version",
    "status",
    "ai_assistance",
    "human_review",
    "release_status",
]

REQUIRED_SECTIONS = [
    "## 1. Release Scope",
    "## 2. Per-Feature Outcomes",
    "## 3. Aggregate Risk Profile",
    "## 4. Aggregate Requirements Coverage",
    "## 5. Aggregate Test Outcome",
    "## 6. Aggregate AI Assistance Summary",
    "## 7. Release Validation Status",
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

    status = keys.get("release_status", "")
    if status and status not in VALID_STATUSES:
        errors.append(
            f"Frontmatter release_status must be one of {sorted(VALID_STATUSES)}, "
            f"got {status!r}."
        )

    errors.extend(check_required_sections(body, REQUIRED_SECTIONS))
    errors.extend(check_no_placeholders(text))

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("release_summary", validate))
