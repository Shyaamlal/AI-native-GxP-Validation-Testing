"""Shared helpers for per-phase schema validators.

The validators are standalone Python modules invoked by the Orchestrator (see
`.claude/skills/validate-feature.md`). This module exists only to avoid
duplicating the small set of operations every validator needs — frontmatter
parsing, placeholder detection, section-emptiness checks. Anything phase-specific
lives in the phase's own validator module.

Per ADR-005: Python is used only where it beats prompts. These helpers are
deterministic checks that an LLM self-check would miss intermittently.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Iterable

# ---------------------------------------------------------------------------
# Forbidden placeholder patterns — shared across every phase
# ---------------------------------------------------------------------------

FORBIDDEN_PLACEHOLDER_PATTERNS = [
    r"\[Document what happened.*?\]",
    r"\[If any.*?\]",
    r"\[Empty fields.*?\]",
    r"\[describe.*?\]",
    r"\[Describe.*?\]",
    r"\[fill in.*?\]",
    r"\[Fill in.*?\]",
    r"\[TBD.*?\]",
    r"\bTODO\b",
    r"\bTBD\b",
    r"<fill in>",
]

# Common required ai_assistance subfields — every artifact carries these
REQUIRED_AI_ASSISTANCE_SUBFIELDS = [
    "agent_skill",
    "model",
    "invocation_timestamp",
    "prompt_version",
]


# ---------------------------------------------------------------------------
# Frontmatter parsing — minimal YAML-ish, deliberately no dependency
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_block, body). frontmatter_block is the raw content
    between the leading --- fences (without the fences), or None if absent."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[3:end].lstrip("\n")
    body = text[end + 4:].lstrip("\n")
    return fm, body


def parse_frontmatter_keys(fm: str) -> dict[str, str]:
    """Flatten frontmatter into dotted keys: e.g. `ai_assistance.model`.
    Deliberately not a full YAML parser — we only need presence + non-emptiness
    checks. Nested lists (e.g. traceability.upstream) are not parsed deeply;
    callers can re-read the raw block for list contents if needed."""
    top_keys: dict[str, str] = {}
    current_top: str | None = None

    for raw_line in fm.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("#"):
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == 0 and ":" in stripped:
            key, _, value = stripped.partition(":")
            top_keys[key.strip()] = value.strip()
            current_top = key.strip()
        elif current_top and indent > 0 and ":" in stripped:
            sub_key, _, sub_value = stripped.partition(":")
            top_keys[f"{current_top}.{sub_key.strip()}"] = sub_value.strip()

    return top_keys


# ---------------------------------------------------------------------------
# Common check primitives
# ---------------------------------------------------------------------------

def check_frontmatter_present(fm: str | None) -> list[str]:
    if fm is None:
        return ["Frontmatter block (--- ... ---) is missing."]
    return []


def check_required_fields(
    keys: dict[str, str], required: Iterable[str]
) -> list[str]:
    """Field is satisfied if it has an inline value OR has at least one nested
    child (key with `<field>.` prefix). YAML parents like `ai_assistance:`
    legitimately have no inline value when they hold a nested mapping."""
    errors: list[str] = []
    for field in required:
        if field not in keys:
            errors.append(f"Frontmatter field missing: {field}")
            continue
        if keys[field]:
            continue
        prefix = f"{field}."
        has_child = any(k.startswith(prefix) for k in keys)
        if not has_child:
            errors.append(f"Frontmatter field empty: {field}")
    return errors


def check_artifact_type(keys: dict[str, str], expected: str) -> list[str]:
    actual = keys.get("artifact_type", "")
    if actual and actual != expected:
        return [
            f"Frontmatter artifact_type must be {expected!r}, got {actual!r}."
        ]
    return []


def check_ai_assistance_subfields(keys: dict[str, str]) -> list[str]:
    errors: list[str] = []
    for sub in REQUIRED_AI_ASSISTANCE_SUBFIELDS:
        full = f"ai_assistance.{sub}"
        if full not in keys:
            errors.append(f"Frontmatter ai_assistance.{sub} missing.")
        elif not keys[full]:
            errors.append(f"Frontmatter ai_assistance.{sub} is empty.")
    return errors


def check_required_sections(body: str, sections: Iterable[str]) -> list[str]:
    """Each section heading must be present and the section must have content
    between this heading and the next ## heading."""
    errors: list[str] = []
    for section in sections:
        if section not in body:
            errors.append(f"Required section missing: {section!r}")
            continue
        if _section_is_empty(body, section):
            errors.append(f"Required section is empty: {section!r}")
    return errors


def _section_is_empty(body: str, heading: str) -> bool:
    start = body.find(heading)
    if start == -1:
        return False
    after = body[start + len(heading):]
    next_heading = re.search(r"\n## ", after)
    block = after[: next_heading.start()] if next_heading else after
    content = block.strip()
    if not content:
        return True
    text_lines = [
        ln for ln in content.splitlines()
        if ln.strip() and not ln.strip().startswith("###")
    ]
    return len(text_lines) == 0


def check_no_placeholders(text: str) -> list[str]:
    errors: list[str] = []
    for pattern in FORBIDDEN_PLACEHOLDER_PATTERNS:
        for match in re.finditer(pattern, text):
            line_no = text.count("\n", 0, match.start()) + 1
            errors.append(
                f"Forbidden placeholder at line {line_no}: {match.group(0)!r}"
            )
    return errors


def find_unique_ids(text: str, id_pattern: str) -> tuple[list[str], list[str]]:
    """Return (all_ids, duplicate_ids). id_pattern is a regex with the ID group
    in position 0 (whole match)."""
    matches = re.findall(id_pattern, text)
    seen: dict[str, int] = {}
    for m in matches:
        seen[m] = seen.get(m, 0) + 1
    duplicates = [m for m, count in seen.items() if count > 1]
    return matches, duplicates


def get_section_block(body: str, heading: str) -> str:
    """Return the text of a section between its heading and the next ## heading
    (or end of file). Empty string if the heading is not found."""
    start = body.find(heading)
    if start == -1:
        return ""
    after = body[start + len(heading):]
    next_heading = re.search(r"\n## ", after)
    return after[: next_heading.start()] if next_heading else after


# ---------------------------------------------------------------------------
# Validator entry point — shared shell each phase-specific module uses
# ---------------------------------------------------------------------------

def run_validator(
    validator_name: str,
    artifact_path: Path,
    validate_fn,
) -> int:
    """Run the per-phase validate function, print structured JSON, return exit code."""
    if not artifact_path.exists():
        print(
            json.dumps(
                {
                    "pass": False,
                    "artifact": str(artifact_path),
                    "validator": validator_name,
                    "errors": [f"Artifact file does not exist: {artifact_path}"],
                },
                indent=2,
            )
        )
        return 1

    passed, errors = validate_fn(artifact_path)
    print(
        json.dumps(
            {
                "pass": passed,
                "artifact": str(artifact_path),
                "validator": validator_name,
                "errors": errors,
            },
            indent=2,
        )
    )
    return 0 if passed else 1


def standard_cli(validator_name: str, validate_fn) -> int:
    if len(sys.argv) != 2:
        print(
            json.dumps(
                {
                    "pass": False,
                    "errors": [
                        f"Usage: python validators/{validator_name}.py <artifact_path>"
                    ],
                }
            )
        )
        return 1
    return run_validator(validator_name, Path(sys.argv[1]), validate_fn)
