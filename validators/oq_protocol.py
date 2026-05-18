"""Schema validator for OQ Protocol artifacts (Phase 6).

Enforces: every test case traces to ≥1 acceptance criterion. Coverage of FRS
acceptance criteria is checked at AC level — every AC in the upstream FRS must
be referenced by ≥1 test case.
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

ARTIFACT_TYPE = "OQ_Protocol"

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
    "## 2. Test Environment Requirements",
    "## 3. Test Cases",
    "## 4. Traceability Coverage",
]

TC_HEADING_PATTERN = r"^### (TC-\d{3,})\b"  # only counts heading definitions
TC_ID_PATTERN = r"\bTC-\d{3,}\b"
AC_REF_PATTERN = r"\bAC-FRS-\d{3,}\.\d+\b"


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

    test_block = get_section_block(body, "## 3. Test Cases")
    if not test_block:
        return (not errors), errors

    heading_ids = re.findall(TC_HEADING_PATTERN, test_block, flags=re.MULTILINE)
    heading_seen: dict[str, int] = {}
    for h in heading_ids:
        heading_seen[h] = heading_seen.get(h, 0) + 1
    tc_dupes = [h for h, c in heading_seen.items() if c > 1]
    tc_ids = heading_ids
    if not tc_ids:
        errors.append(
            "Section 3: no test cases found. Expected at least one ID in TC-NNN format."
        )
    for dup in tc_dupes:
        errors.append(f"Duplicate TC ID: {dup}")

    # Each TC block must include a trace to ≥1 AC.
    tc_item_blocks = re.split(r"(?=^### TC-\d{3,})", test_block, flags=re.MULTILINE)
    for block in tc_item_blocks:
        block = block.strip()
        tc_match = re.search(TC_ID_PATTERN, block)
        if not tc_match:
            continue
        tc_id = tc_match.group(0)
        # Trace must be declared on a **Trace:** line, not merely mentioned in
        # the block (e.g. inside Pass criteria narrative). Anchors the check
        # to the declared traceability field.
        trace_lines = re.findall(r"\*\*Trace:\*\*[^\n]*", block)
        trace_ac_refs = [
            ac for line in trace_lines for ac in re.findall(AC_REF_PATTERN, line)
        ]
        if not trace_ac_refs:
            errors.append(
                f"{tc_id}: no acceptance criterion trace declared. Each test case "
                f"must have a **Trace:** line referencing ≥1 AC in AC-FRS-NNN.M form."
            )
        for required_field in ("Preconditions:", "Steps:", "Expected result:", "Pass criteria:"):
            if required_field not in block:
                errors.append(f"{tc_id}: missing {required_field!r}")

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("oq_protocol", validate))
