"""Schema validator for URS artifacts (Phase 4)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from _common import (
    check_ai_assistance_subfields,
    check_artifact_type,
    check_frontmatter_present,
    check_no_placeholders,
    check_required_fields,
    check_required_sections,
    find_unique_ids,
    get_section_block,
    parse_frontmatter_keys,
    split_frontmatter,
    standard_cli,
)

ARTIFACT_TYPE = "URS"

REQUIRED_FRONTMATTER = [
    "artifact_type",
    "feature",
    "version",
    "status",
    "ai_assistance",
    "human_review",
    "traceability",
]

REQUIRED_SECTIONS = [
    "## 1. Purpose",
    "## 2. Scope Reference",
    "## 3. User Requirements",
    "## 4. User Roles Referenced",
]

URS_ID_PATTERN = r"\bURS-\d{3,}\b"


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
    errors.extend(check_required_sections(body, REQUIRED_SECTIONS))
    errors.extend(check_no_placeholders(text))

    # Rung-specific: URS IDs must exist, be unique, and follow URS-NNN pattern.
    requirements_block = get_section_block(body, "## 3. User Requirements")
    if requirements_block:
        urs_ids, duplicates = find_unique_ids(requirements_block, URS_ID_PATTERN)
        if not urs_ids:
            errors.append(
                "Section 3 (User Requirements): no URS items found. "
                "Expected at least one ID in URS-NNN format."
            )
        for dup in duplicates:
            errors.append(f"Duplicate URS ID: {dup}")

        # Every URS item should reference a trace upstream — Validation Scope or Feature Scoping.
        if "Validation Scope" not in requirements_block and "Feature Scoping" not in requirements_block:
            errors.append(
                "Section 3: no traceability references to upstream artifacts found. "
                "Each URS item should reference Validation Scope §<N> and/or Feature Scoping §<N>."
            )

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("urs", validate))
