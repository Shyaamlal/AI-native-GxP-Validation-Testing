"""Schema validator for Risk Assessment artifacts (Phase 2)."""

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

ARTIFACT_TYPE = "Risk_Assessment"

REQUIRED_FRONTMATTER = [
    "artifact_type",
    "feature",
    "version",
    "status",
    "ai_assistance",
    "human_review",
    "traceability",
    "risk_classification",
]

REQUIRED_SECTIONS = [
    "## 1. Framework Applied",
    "## 2. GxP Impact Assessment",
    "## 3. Patient Safety Risk",
    "## 4. Data Integrity Risk",
    "## 5. Risk Classification",
    "## 6. Downstream Implications",
]


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

    # Rung-specific: risk_classification subfields
    for sub in ("framework", "category"):
        full = f"risk_classification.{sub}"
        if full not in keys:
            errors.append(f"Frontmatter risk_classification.{sub} missing.")
        elif not keys[full]:
            errors.append(f"Frontmatter risk_classification.{sub} is empty.")

    errors.extend(check_required_sections(body, REQUIRED_SECTIONS))
    errors.extend(check_no_placeholders(text))

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("risk_assessment", validate))
