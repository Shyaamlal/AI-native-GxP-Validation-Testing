"""Audit CLI — query the AI Assistance Log.

The Orchestrator writes one append-only line to `ai_assistance_log.jsonl` at the
repo root per agent invocation (see design doc §9.2). This CLI runs structured
queries over that log:

    python tools/audit.py --feature Logout
    python tools/audit.py --model claude-opus-4-7 --since 2026-05-01
    python tools/audit.py --reviewer shyaamlal --phase 7
    python tools/audit.py --artifact 02_Logout/URS_Logout.md
    python tools/audit.py --status rejected
    python tools/audit.py --since 2026-05-01 --format json
    python tools/audit.py --tail 10

Per ADR-005, Python is used here because structured queries over an append-only
log are not something a prompt does deterministically.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable

DEFAULT_LOG_PATH = Path(__file__).resolve().parent.parent / "ai_assistance_log.jsonl"


def _parse_log(path: Path) -> list[dict]:
    if not path.exists():
        return []
    entries: list[dict] = []
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError as e:
            print(
                f"Warning: malformed JSONL at line {line_no}: {e}",
                file=sys.stderr,
            )
    return entries


def _parse_iso(value: str) -> datetime:
    # Accept both 2026-05-17 and 2026-05-17T09:00:00Z forms.
    if "T" not in value:
        value = value + "T00:00:00Z"
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _matches(entry: dict, args: argparse.Namespace) -> bool:
    if args.feature and entry.get("feature") != args.feature:
        return False
    if args.model and entry.get("model") != args.model:
        return False
    if args.reviewer and entry.get("reviewer") != args.reviewer:
        return False
    if args.artifact and entry.get("artifact_path") != args.artifact:
        return False
    if args.status and entry.get("approval") != args.status:
        return False
    if args.phase is not None and entry.get("phase") != args.phase:
        return False
    if args.phase_name and entry.get("phase_name") != args.phase_name:
        return False
    if args.skill and entry.get("agent_skill") != args.skill:
        return False
    if args.since:
        ts = entry.get("timestamp")
        if not ts:
            return False
        try:
            if _parse_iso(ts) < _parse_iso(args.since):
                return False
        except ValueError:
            return False
    if args.until:
        ts = entry.get("timestamp")
        if not ts:
            return False
        try:
            if _parse_iso(ts) > _parse_iso(args.until):
                return False
        except ValueError:
            return False
    return True


def _render_table(entries: Iterable[dict]) -> str:
    rows = list(entries)
    if not rows:
        return "(no matching entries)"

    headers = ["timestamp", "feature", "phase", "phase_name", "skill", "model", "schema", "approval", "reviewer"]
    table: list[list[str]] = [headers]
    for e in rows:
        table.append(
            [
                str(e.get("timestamp", "")),
                str(e.get("feature", "")),
                str(e.get("phase", "")),
                str(e.get("phase_name", "")),
                str(e.get("agent_skill", "")),
                str(e.get("model", "")),
                str(e.get("schema_result", "")),
                str(e.get("approval", "")),
                str(e.get("reviewer", "") or ""),
            ]
        )

    widths = [max(len(row[i]) for row in table) for i in range(len(headers))]
    lines = []
    for i, row in enumerate(table):
        lines.append("  ".join(cell.ljust(widths[j]) for j, cell in enumerate(row)))
        if i == 0:
            lines.append("  ".join("-" * w for w in widths))
    lines.append(f"\n{len(rows)} matching entr{'y' if len(rows) == 1 else 'ies'}.")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Query the AI Assistance Log for the validation framework."
    )
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG_PATH, help="Path to ai_assistance_log.jsonl")
    parser.add_argument("--feature", help="Filter by feature name")
    parser.add_argument("--model", help="Filter by model identifier")
    parser.add_argument("--reviewer", help="Filter by reviewer")
    parser.add_argument("--artifact", help="Filter by exact artifact_path")
    parser.add_argument("--status", choices=["pending", "approved", "rejected"], help="Filter by approval status")
    parser.add_argument("--phase", type=int, help="Filter by phase number (1-8)")
    parser.add_argument("--phase-name", dest="phase_name", help="Filter by phase name (e.g. feature-scoping)")
    parser.add_argument("--skill", help="Filter by agent_skill")
    parser.add_argument("--since", help="Earliest timestamp (YYYY-MM-DD or ISO-8601)")
    parser.add_argument("--until", help="Latest timestamp (YYYY-MM-DD or ISO-8601)")
    parser.add_argument("--tail", type=int, help="Show only the last N matching entries")
    parser.add_argument(
        "--format",
        choices=["table", "json", "jsonl"],
        default="table",
        help="Output format",
    )

    args = parser.parse_args(argv)

    entries = _parse_log(args.log)
    matched = [e for e in entries if _matches(e, args)]
    if args.tail:
        matched = matched[-args.tail :]

    if args.format == "json":
        print(json.dumps(matched, indent=2))
    elif args.format == "jsonl":
        for e in matched:
            print(json.dumps(e))
    else:
        print(_render_table(matched))

    return 0


if __name__ == "__main__":
    sys.exit(main())
