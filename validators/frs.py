"""Schema validator for FRS artifacts (Phase 5).

Enforces the design v1.1 decision: every FRS item carries ≥1 acceptance criterion
(no separate AC-author agent — validator handles this deterministically).
"""

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

ARTIFACT_TYPE = "FRS"

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
    "## 2. Functional Requirements",
    "## 3. Functional Roles",
]

FRS_HEADING_PATTERN = r"^### (FRS-\d{3,})\b"  # only counts heading definitions
FRS_ID_PATTERN = r"(?<!AC-)\bFRS-\d{3,}\b"     # excludes AC-FRS-NNN matches
AC_ID_PATTERN = r"\bAC-FRS-\d{3,}\.\d+\b"


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

    requirements_block = get_section_block(body, "## 2. Functional Requirements")

    if not requirements_block:
        return (not errors), errors

    # Definitions = heading occurrences. Body references to the same FRS-NNN
    # are not duplicates.
    heading_ids = re.findall(FRS_HEADING_PATTERN, requirements_block, flags=re.MULTILINE)
    heading_seen: dict[str, int] = {}
    for h in heading_ids:
        heading_seen[h] = heading_seen.get(h, 0) + 1
    frs_dupes = [h for h, c in heading_seen.items() if c > 1]
    frs_ids = heading_ids
    if not frs_ids:
        errors.append(
            "Section 2: no FRS items found. Expected at least one ID in FRS-NNN format."
        )
    for dup in frs_dupes:
        errors.append(f"Duplicate FRS ID: {dup}")

    ac_ids, ac_dupes = find_unique_ids(requirements_block, AC_ID_PATTERN)
    for dup in ac_dupes:
        errors.append(f"Duplicate AC ID: {dup}")

    # Critical design v1.1 rule: every FRS item has ≥1 AC.
    # Split the block on FRS headings and check each FRS item carries AC content.
    frs_item_blocks = re.split(r"(?=^### FRS-\d{3,})", requirements_block, flags=re.MULTILINE)
    for block in frs_item_blocks:
        block = block.strip()
        frs_match = re.search(FRS_ID_PATTERN, block)
        if not frs_match:
            continue
        frs_id = frs_match.group(0)
        ac_in_block = re.findall(AC_ID_PATTERN, block)
        if not ac_in_block:
            errors.append(
                f"{frs_id}: no acceptance criterion found. Every FRS item must "
                f"carry ≥1 AC in AC-FRS-NNN.M form."
            )
        if "Trace:" not in block and "trace:" not in block:
            errors.append(
                f"{frs_id}: no upstream trace to URS found. Each FRS item must "
                f"reference URS-NNN it derives from."
            )

    # AC pattern check — each AC must use Given/When/Then or be a measurable binary condition.
    ac_blocks = re.findall(
        r"(\bAC-FRS-\d{3,}\.\d+\b[^\n]*)", requirements_block
    )
    for ac_line in ac_blocks:
        lower = ac_line.lower()
        gwt = ("given" in lower and "when" in lower and "then" in lower)
        # Heuristic for measurable binary: contains a comparator or measurable verb.
        measurable = bool(re.search(
            r"\b(returns|equals|matches|is\s+\w+|shall\s+\w+|within \d+|less than|greater than|<|>|=)\b",
            lower,
        ))
        if not (gwt or measurable):
            errors.append(
                f"Acceptance criterion lacks testable pattern (Given/When/Then "
                f"or measurable binary condition): {ac_line.strip()!r}"
            )

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("frs", validate))
