"""Schema validator for Validation Scope artifacts (Phase 3)."""

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
    get_section_block,
    parse_frontmatter_keys,
    split_frontmatter,
    standard_cli,
)

ARTIFACT_TYPE = "Validation_Scope"

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
    "## 1. Validation Objective",
    "## 2. In Scope",
    "## 3. Out of Scope",
    "## 4. Assumptions",
    "## 5. Exit Criteria",
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
    errors.extend(check_required_sections(body, REQUIRED_SECTIONS))
    errors.extend(check_no_placeholders(text))

    # Every in-scope item must trace to both Feature Scoping and Risk Assessment.
    in_scope = get_section_block(body, "## 2. In Scope")
    if in_scope:
        # Count numbered sub-items (### 2.<N>) and check each carries both
        # the Observed behaviour reference and Risk reference markers.
        sub_items = [
            block
            for block in in_scope.split("### 2.")
            if block.strip() and not block.startswith("In Scope")
        ]
        for idx, item in enumerate(sub_items, start=1):
            if "Observed behaviour reference" not in item:
                errors.append(
                    f"Section 2 item {idx}: missing 'Observed behaviour reference' "
                    f"(traceability to Feature Scoping)."
                )
            if "Risk reference" not in item:
                errors.append(
                    f"Section 2 item {idx}: missing 'Risk reference' "
                    f"(traceability to Risk Assessment)."
                )

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("validation_scope", validate))
