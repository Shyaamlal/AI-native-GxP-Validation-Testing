"""Schema validator for Feature Scoping artifacts (Phase 1).

Invoked by the Orchestrator at phase-complete handoff. Returns exit code 0 on pass,
1 on fail. Pass/fail and the list of failed checks are printed as JSON on stdout
so the Orchestrator can parse them and (on fail) return them to the agent.

Per ADR-003: this is the deterministic check that gates whether the human reviewer
is bothered with an artifact. LLM self-checks miss; regex doesn't.

Reference: 00_Project_Context/Agentic_Framework_Design.md sections 6.1 and 10.1.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration — what this validator enforces
# ---------------------------------------------------------------------------

ARTIFACT_TYPE = "Feature_Scoping"

REQUIRED_FRONTMATTER_FIELDS = [
    "artifact_type",
    "feature",
    "version",
    "status",
    "ai_assistance",
    "human_review",
    "traceability",
]

REQUIRED_AI_ASSISTANCE_SUBFIELDS = [
    "agent_skill",
    "model",
    "invocation_timestamp",
    "prompt_version",
]

REQUIRED_SECTIONS = [
    "## 1. Feature Identity",
    "## 2. Observed Behaviour",
    "## 3. User Interface Elements",
    "## 4. Feature Boundary",
    "## 5. Open Questions",
    "## 6. Observation Notes",
]

# Forbidden placeholder patterns. Matches the Login Feature Observation Gap #2
# regression and adds the standard set declared in the skill's "Hard rules".
FORBIDDEN_PLACEHOLDER_PATTERNS = [
    r"\[Document what happened.*?\]",
    r"\[If any.*?\]",
    r"\[Empty fields.*?\]",
    r"\[describe.*?\]",
    r"\[fill in.*?\]",
    r"\[Fill in.*?\]",
    r"\[TBD.*?\]",
    r"\bTODO\b",
    r"\bTBD\b",
    r"<fill in>",
]


# ---------------------------------------------------------------------------
# Frontmatter parsing — minimal YAML-ish, deliberately no dependency
# ---------------------------------------------------------------------------

def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_block, body) where frontmatter_block is the raw YAML
    string between the leading --- fences (without the fences), or None if no
    frontmatter is present."""
    if not text.startswith("---"):
        return None, text
    end = text.find("\n---", 3)
    if end == -1:
        return None, text
    fm = text[3:end].lstrip("\n")
    body = text[end + 4:].lstrip("\n")
    return fm, body


def parse_frontmatter_keys(fm: str) -> dict[str, str]:
    """Extract the top-level keys present in the frontmatter and a flattened
    set of nested keys under ai_assistance/human_review/traceability. Deliberately
    not a full YAML parser — we only need presence + non-emptiness checks."""
    top_keys: dict[str, str] = {}
    current_top: str | None = None
    indent_for_top = 0

    for raw_line in fm.splitlines():
        line = raw_line.rstrip()
        if not line or line.startswith("#"):
            continue
        stripped = line.lstrip()
        indent = len(line) - len(stripped)

        if indent == 0 and ":" in stripped:
            key, _, value = stripped.partition(":")
            key = key.strip()
            value = value.strip()
            top_keys[key] = value
            current_top = key
            indent_for_top = 0
        elif current_top and indent > indent_for_top and ":" in stripped:
            sub_key, _, sub_value = stripped.partition(":")
            top_keys[f"{current_top}.{sub_key.strip()}"] = sub_value.strip()

    return top_keys


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def check_frontmatter(fm: str | None) -> list[str]:
    errors: list[str] = []
    if fm is None:
        return ["Frontmatter block (--- ... ---) is missing."]

    keys = parse_frontmatter_keys(fm)

    for field in REQUIRED_FRONTMATTER_FIELDS:
        if field not in keys:
            errors.append(f"Frontmatter field missing: {field}")

    artifact_type = keys.get("artifact_type", "")
    if artifact_type and artifact_type != ARTIFACT_TYPE:
        errors.append(
            f"Frontmatter artifact_type must be {ARTIFACT_TYPE!r}, "
            f"got {artifact_type!r}."
        )

    for sub in REQUIRED_AI_ASSISTANCE_SUBFIELDS:
        full = f"ai_assistance.{sub}"
        if full not in keys:
            errors.append(f"Frontmatter ai_assistance.{sub} missing.")
        elif not keys[full]:
            errors.append(f"Frontmatter ai_assistance.{sub} is empty.")

    feature = keys.get("feature", "")
    if not feature:
        errors.append("Frontmatter feature is empty.")

    return errors


def check_required_sections(body: str) -> list[str]:
    errors: list[str] = []
    for section in REQUIRED_SECTIONS:
        if section not in body:
            errors.append(f"Required section missing: {section!r}")
            continue
        if _section_is_empty(body, section):
            errors.append(f"Required section is empty: {section!r}")
    return errors


def _section_is_empty(body: str, heading: str) -> bool:
    """A section is empty if there is no substantive content between this
    heading and the next ## heading (or end of file)."""
    start = body.find(heading)
    if start == -1:
        return False
    after = body[start + len(heading):]
    next_heading = re.search(r"\n## ", after)
    block = after[: next_heading.start()] if next_heading else after
    content = block.strip()
    # An empty section is one with no content at all, or only a sub-heading stub.
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


def check_observed_behaviour_structure(body: str) -> list[str]:
    """Section 2 must contain at least one numbered sub-behaviour (### 2.<N>)
    with the four required fields. Gap #2 prevention — sections that look
    populated but contain only the boilerplate skeleton get caught here."""
    errors: list[str] = []
    section_start = body.find("## 2. Observed Behaviour")
    if section_start == -1:
        return errors  # already caught by check_required_sections
    after = body[section_start:]
    next_heading = re.search(r"\n## (?!#)", after[1:])
    section = after[: next_heading.start() + 1] if next_heading else after

    sub_headings = re.findall(r"### 2\.\d+\b", section)
    if not sub_headings:
        errors.append(
            "Section 2 (Observed Behaviour) must contain at least one numbered "
            "sub-behaviour (e.g. '### 2.1. Successful Login')."
        )
        return errors

    for required_field in [
        "**User action(s):**",
        "**System response:**",
        "**Visual feedback:**",
        "**Behavioural outcome:**",
    ]:
        if section.count(required_field) < len(sub_headings):
            errors.append(
                f"Section 2: every numbered sub-behaviour must include "
                f"{required_field} — found fewer instances than sub-behaviours."
            )

    return errors


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def validate(artifact_path: Path) -> tuple[bool, list[str]]:
    if not artifact_path.exists():
        return False, [f"Artifact file does not exist: {artifact_path}"]

    text = artifact_path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)

    errors: list[str] = []
    errors.extend(check_frontmatter(fm))
    errors.extend(check_required_sections(body))
    errors.extend(check_no_placeholders(text))
    errors.extend(check_observed_behaviour_structure(body))

    return (not errors), errors


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(
            json.dumps(
                {
                    "pass": False,
                    "errors": [
                        "Usage: python validators/feature_scoping.py <artifact_path>"
                    ],
                }
            )
        )
        return 1

    artifact_path = Path(argv[1])
    passed, errors = validate(artifact_path)

    print(
        json.dumps(
            {
                "pass": passed,
                "artifact": str(artifact_path),
                "validator": "feature_scoping",
                "errors": errors,
            },
            indent=2,
        )
    )
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
