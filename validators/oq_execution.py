"""Schema validator for OQ Execution Record artifacts (Phase 7).

Enforces: every test case in the upstream OQ Protocol has an execution result
in this record. (Coverage check is cross-artifact — the validator reads the
upstream OQ_Protocol_<feature>.md to enumerate expected TC IDs.)
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
    get_section_block,
    parse_frontmatter_keys,
    split_frontmatter,
    standard_cli,
)

ARTIFACT_TYPE = "OQ_Execution_Record"

REQUIRED_FRONTMATTER = [
    "artifact_type",
    "feature",
    "version",
    "status",
    "ai_assistance",
    "human_review",
    "traceability",
    "execution_context",
]

REQUIRED_EXECUTION_CONTEXT = ["mode", "executor", "environment_url", "execution_start"]

REQUIRED_SECTIONS = [
    "## 1. Execution Summary",
    "## 2. Test Case Results",
    "## 3. Deviations Summary",
    "## 4. Bugs / Anomalies Surfaced",
]

TC_ID_PATTERN = r"\bTC-\d{3,}\b"


def _find_upstream_protocol(record_path: Path) -> Path | None:
    """Locate the OQ_Protocol_<feature>.md sibling artifact in the same folder."""
    folder = record_path.parent
    for candidate in folder.glob("OQ_Protocol_*.md"):
        return candidate
    return None


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
    for sub in REQUIRED_EXECUTION_CONTEXT:
        full = f"execution_context.{sub}"
        if full not in keys:
            errors.append(f"Frontmatter execution_context.{sub} missing.")
        elif not keys[full]:
            errors.append(f"Frontmatter execution_context.{sub} is empty.")
    errors.extend(check_required_sections(body, REQUIRED_SECTIONS))
    errors.extend(check_no_placeholders(text))

    # Cross-artifact check: every TC in the upstream OQ Protocol has a result here.
    upstream = _find_upstream_protocol(artifact_path)
    if upstream is None:
        errors.append(
            "Upstream OQ Protocol artifact not found in feature folder — cannot "
            "verify test case coverage."
        )
        return (not errors), errors

    upstream_text = upstream.read_text(encoding="utf-8")
    upstream_tc_ids = set(re.findall(TC_ID_PATTERN, upstream_text))
    record_tc_ids = set(re.findall(TC_ID_PATTERN, text))

    missing = upstream_tc_ids - record_tc_ids
    for tc in sorted(missing):
        errors.append(
            f"Test case {tc} from {upstream.name} has no execution result in this record."
        )

    return (not errors), errors


if __name__ == "__main__":
    sys.exit(standard_cli("oq_execution", validate))
