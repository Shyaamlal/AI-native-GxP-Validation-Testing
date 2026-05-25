"""Methodology metrics CLI — surface methodology-level performance from the audit log.

The Orchestrator writes one append-only line to `ai_assistance_log.jsonl` per agent
invocation and per human-in-the-loop decision (see design doc §9.2). This CLI reads
that log and computes methodology-level metrics from any worked run:

    python tools/methodology_metrics.py --feature Logout
    python tools/methodology_metrics.py                # defaults to most recent complete run
    python tools/methodology_metrics.py --feature Logout --json

It closes the measurement loop on the existing audit trail: the same data the
framework relies on for tamper-evident traceability also tells us how the
methodology itself performed.

Honesty principle: where the log does not capture a metric directly, the tool
surfaces the instrumentation gap rather than estimating around it.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

DEFAULT_LOG_PATH = Path(__file__).resolve().parent.parent / "ai_assistance_log.jsonl"

PHASE_ORDER = [
    (1, "feature-scoping"),
    (2, "risk-assessment"),
    (3, "validation-scope"),
    (4, "urs"),
    (5, "frs"),
    (6, "oq-protocol"),
    (7, "oq-execution"),
    (8, "summary-report"),
]


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
            print(f"Warning: malformed JSONL at line {line_no}: {e}", file=sys.stderr)
    return entries


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _resolve_feature(entries: list[dict], requested: str | None) -> str | None:
    """Resolve the feature to report on.

    If --feature is given, accept either the exact feature name (as logged) or a
    directory-style prefix (e.g. '02_Logout' → 'Logout'). If omitted, default to
    the feature whose phase 8 was most recently approved (i.e. most recent
    complete run).
    """
    features_seen = [e.get("feature") for e in entries if e.get("feature")]
    if not features_seen:
        return None

    if requested:
        if requested in features_seen:
            return requested
        # tolerate '02_Logout' when the log stores 'Logout'
        stripped = requested.split("_", 1)[-1] if "_" in requested else requested
        if stripped in features_seen:
            return stripped
        return None

    complete: dict[str, datetime] = {}
    for e in entries:
        if (
            e.get("phase") == 8
            and e.get("approval") == "approved"
            and e.get("approval_timestamp")
        ):
            try:
                complete[e["feature"]] = _parse_iso(e["approval_timestamp"])
            except ValueError:
                continue
    if complete:
        return max(complete, key=complete.get)

    return features_seen[-1]


def _phase_pairs(feature_entries: list[dict]) -> dict[int, dict[str, Any]]:
    """Group entries into pending/decision pairs per phase.

    Returns a dict keyed by phase number with the emission entry, the decision
    entry, and the count of in-gate amendments (prior_surfaced_hash occurrences).
    """
    by_phase: dict[int, dict[str, Any]] = defaultdict(
        lambda: {
            "phase_name": None,
            "emissions": [],
            "decisions": [],
            "amendments": 0,
        }
    )
    for e in feature_entries:
        phase = e.get("phase")
        if phase is None:
            continue
        slot = by_phase[phase]
        slot["phase_name"] = e.get("phase_name") or slot["phase_name"]
        if e.get("approval") == "pending":
            slot["emissions"].append(e)
        else:
            slot["decisions"].append(e)
        if e.get("prior_surfaced_hash"):
            slot["amendments"] += 1
    return dict(by_phase)


def _phase_duration(emission: dict | None, decision: dict | None) -> timedelta | None:
    if not emission or not decision:
        return None
    try:
        start = _parse_iso(emission["timestamp"])
        end = _parse_iso(decision.get("approval_timestamp") or decision["timestamp"])
    except (KeyError, ValueError):
        return None
    return end - start


def _format_duration(delta: timedelta | None) -> str:
    if delta is None:
        return "n/a"
    total = int(delta.total_seconds())
    sign = "-" if total < 0 else ""
    total = abs(total)
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    if h:
        return f"{sign}{h}h {m}m {s}s"
    if m:
        return f"{sign}{m}m {s}s"
    return f"{sign}{s}s"


def _compute(feature: str, feature_entries: list[dict]) -> dict[str, Any]:
    phases = _phase_pairs(feature_entries)

    # Wall-clock
    timestamps: list[datetime] = []
    for e in feature_entries:
        for key in ("timestamp", "approval_timestamp"):
            v = e.get(key)
            if not v:
                continue
            try:
                timestamps.append(_parse_iso(v))
            except ValueError:
                continue
    total_wall = (max(timestamps) - min(timestamps)) if timestamps else None

    # Per-phase metrics
    per_phase: list[dict[str, Any]] = []
    hitl_outcomes: Counter[str] = Counter()
    validator_outcomes: Counter[str] = Counter()
    for phase_num, phase_name in PHASE_ORDER:
        slot = phases.get(phase_num)
        if not slot:
            per_phase.append(
                {
                    "phase": phase_num,
                    "phase_name": phase_name,
                    "status": "missing",
                    "duration": None,
                    "duration_seconds": None,
                    "schema_results": {},
                    "hitl_decisions": {},
                    "in_gate_amendments": 0,
                }
            )
            continue
        emission = slot["emissions"][0] if slot["emissions"] else None
        decision = slot["decisions"][-1] if slot["decisions"] else None
        duration = _phase_duration(emission, decision)
        schema_for_phase = Counter()
        for e in slot["emissions"] + slot["decisions"]:
            r = e.get("schema_result")
            if r:
                schema_for_phase[r] += 1
                validator_outcomes[r] += 1
        hitl_for_phase = Counter()
        for d in slot["decisions"]:
            outcome = d.get("approval")
            if outcome:
                hitl_for_phase[outcome] += 1
                hitl_outcomes[outcome] += 1
        per_phase.append(
            {
                "phase": phase_num,
                "phase_name": slot["phase_name"] or phase_name,
                "status": "ok" if (emission and decision) else "partial",
                "duration": _format_duration(duration),
                "duration_seconds": duration.total_seconds() if duration else None,
                "schema_results": dict(schema_for_phase),
                "hitl_decisions": dict(hitl_for_phase),
                "in_gate_amendments": slot["amendments"],
            }
        )

    # HITL rejection rate
    decisions_total = sum(hitl_outcomes.values())
    non_approved = decisions_total - hitl_outcomes.get("approved", 0)
    rejection_rate = (non_approved / decisions_total) if decisions_total else None

    # Bottlenecks
    durations = [(p["phase"], p["phase_name"], p["duration_seconds"]) for p in per_phase if p["duration_seconds"] is not None]
    longest_phase = max(durations, key=lambda x: x[2]) if durations else None
    amendments_ranked = [(p["phase"], p["phase_name"], p["in_gate_amendments"]) for p in per_phase if p["in_gate_amendments"]]
    most_rework = max(amendments_ranked, key=lambda x: x[2]) if amendments_ranked else None

    # Integrity scan: inverted-timestamp pairs and orphan entries
    integrity_findings: list[dict[str, Any]] = []
    for phase_num, phase_name in PHASE_ORDER:
        slot = phases.get(phase_num)
        if not slot:
            continue
        for emission in slot["emissions"]:
            for decision in slot["decisions"]:
                if not decision.get("approval_timestamp"):
                    continue
                try:
                    em_t = _parse_iso(emission["timestamp"])
                    de_t = _parse_iso(decision["approval_timestamp"])
                except (KeyError, ValueError):
                    continue
                if de_t < em_t:
                    integrity_findings.append(
                        {
                            "type": "inverted_timestamps",
                            "phase": phase_num,
                            "phase_name": slot["phase_name"] or phase_name,
                            "emission_timestamp": emission["timestamp"],
                            "approval_timestamp": decision["approval_timestamp"],
                            "negative_duration_seconds": (de_t - em_t).total_seconds(),
                        }
                    )
        if len(slot["emissions"]) > 1:
            integrity_findings.append(
                {
                    "type": "multiple_emissions",
                    "phase": phase_num,
                    "phase_name": slot["phase_name"] or phase_name,
                    "count": len(slot["emissions"]),
                }
            )
        if not slot["emissions"] and slot["decisions"]:
            integrity_findings.append(
                {
                    "type": "decision_without_emission",
                    "phase": phase_num,
                    "phase_name": slot["phase_name"] or phase_name,
                }
            )

    return {
        "feature": feature,
        "entries_total": len(feature_entries),
        "phases_observed": sum(1 for p in per_phase if p["status"] != "missing"),
        "total_wall_clock": _format_duration(total_wall),
        "total_wall_clock_seconds": total_wall.total_seconds() if total_wall else None,
        "per_phase": per_phase,
        "hitl_decision_distribution": dict(hitl_outcomes),
        "hitl_rejection_rate": rejection_rate,
        "validator_outcomes": dict(validator_outcomes),
        "bottlenecks": {
            "longest_phase": longest_phase,
            "most_in_gate_rework": most_rework,
        },
        "integrity_findings": integrity_findings,
        "instrumentation_gaps": [
            "HITL reject / request-changes paths were not exercised in this run; the log records only the 'approved' outcome. The schema does not enforce a decision enum — future log inspection should confirm reject/changes events are emitted as distinct entries (recommendation: review HITL logging instrumentation).",
            "Validator self-correction loops are not directly observable: only the final schema_result for each emission is logged. A validator failure followed by an agent retry would appear as a single 'pass' entry. Recommendation: log each validator attempt, not just the outcome that surfaces to the gate.",
        ],
    }


def _render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    f = report["feature"]
    lines.append(f"# Methodology Metrics — {f}")
    lines.append("")
    lines.append(f"_Derived from `ai_assistance_log.jsonl`. {report['entries_total']} entries across {report['phases_observed']} phases._")
    lines.append("")

    lines.append("## Run summary")
    lines.append("")
    lines.append(f"- **Total wall-clock:** {report['total_wall_clock']}")
    rr = report["hitl_rejection_rate"]
    lines.append(
        f"- **HITL rejection rate:** "
        + ("n/a (no decisions recorded)" if rr is None else f"{rr * 100:.1f}% ({sum(report['hitl_decision_distribution'].values()) - report['hitl_decision_distribution'].get('approved', 0)} of {sum(report['hitl_decision_distribution'].values())})")
    )
    val_pass = report["validator_outcomes"].get("pass", 0)
    val_fail = report["validator_outcomes"].get("fail", 0)
    lines.append(f"- **Validator outcomes:** {val_pass} pass · {val_fail} fail")
    lines.append("")

    lines.append("## Per-phase timing and gates")
    lines.append("")
    lines.append("| Phase | Name | Duration | Schema | HITL | In-gate amendments |")
    lines.append("|---|---|---|---|---|---|")
    for p in report["per_phase"]:
        if p["status"] == "missing":
            lines.append(f"| {p['phase']} | {p['phase_name']} | — | — | — | — |")
            continue
        schema_str = " · ".join(f"{k}:{v}" for k, v in p["schema_results"].items()) or "—"
        hitl_str = " · ".join(f"{k}:{v}" for k, v in p["hitl_decisions"].items()) or "—"
        lines.append(
            f"| {p['phase']} | {p['phase_name']} | {p['duration']} | {schema_str} | {hitl_str} | {p['in_gate_amendments']} |"
        )
    lines.append("")

    lines.append("## Bottlenecks")
    lines.append("")
    lp = report["bottlenecks"]["longest_phase"]
    mr = report["bottlenecks"]["most_in_gate_rework"]
    if lp:
        lines.append(f"- **Longest phase:** {lp[1]} (phase {lp[0]}) — {_format_duration(timedelta(seconds=lp[2]))}")
    else:
        lines.append("- **Longest phase:** n/a")
    if mr:
        lines.append(f"- **Most in-gate rework:** {mr[1]} (phase {mr[0]}) — {mr[2]} amendment(s)")
    else:
        lines.append("- **Most in-gate rework:** none observed")
    lines.append("")

    lines.append("## Audit log integrity")
    lines.append("")
    lines.append(
        "The framework's value proposition includes tamper-evident logging: append-only entries, SHA-256 artifact hashes, monotonic timestamps. This section scans the log against those guarantees."
    )
    lines.append("")
    findings = report["integrity_findings"]
    if not findings:
        lines.append("- No integrity anomalies detected in this run.")
    else:
        for f_ in findings:
            if f_["type"] == "inverted_timestamps":
                lines.append(
                    f"- **Inverted timestamps — phase {f_['phase']} ({f_['phase_name']}):** "
                    f"approval timestamp `{f_['approval_timestamp']}` precedes emission timestamp `{f_['emission_timestamp']}` "
                    f"by {_format_duration(timedelta(seconds=-f_['negative_duration_seconds']))}. "
                    f"Negative phase duration recorded honestly rather than absolute-valued."
                )
            elif f_["type"] == "multiple_emissions":
                lines.append(
                    f"- **Multiple emission entries — phase {f_['phase']} ({f_['phase_name']}):** "
                    f"{f_['count']} pending entries for a single phase. Suggests re-emission was logged but the schema does not distinguish retry from initial emission."
                )
            elif f_["type"] == "decision_without_emission":
                lines.append(
                    f"- **Decision without emission — phase {f_['phase']} ({f_['phase_name']}):** "
                    f"HITL decision entry exists without a preceding pending entry."
                )
    lines.append("")
    lines.append(
        "**Implication:** any inverted-timestamp finding is a data-integrity signal worth investigating. In a production GxP context this would warrant a deviation record. Here it is a framework-level finding for the improvement backlog."
    )
    lines.append("")

    lines.append("## Instrumentation gaps")
    lines.append("")
    lines.append(
        "Metrics this tool cannot derive from the current log schema. These are framework-level findings, not tool limitations:"
    )
    lines.append("")
    for gap in report["instrumentation_gaps"]:
        lines.append(f"- {gap}")
    lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute methodology-level performance metrics from the AI Assistance Log."
    )
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG_PATH, help="Path to ai_assistance_log.jsonl")
    parser.add_argument(
        "--feature",
        help="Feature to report on (accepts logged feature name, e.g. 'Logout', or directory-style prefix, e.g. '02_Logout'). Defaults to most recent complete run.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of markdown")
    args = parser.parse_args(argv)

    entries = _parse_log(args.log)
    if not entries:
        print(f"No entries found in {args.log}", file=sys.stderr)
        return 1

    feature = _resolve_feature(entries, args.feature)
    if not feature:
        print(
            f"Could not resolve feature (requested: {args.feature!r}). "
            f"Features present in log: {sorted({e.get('feature') for e in entries if e.get('feature')})}",
            file=sys.stderr,
        )
        return 1

    feature_entries = [e for e in entries if e.get("feature") == feature]
    report = _compute(feature, feature_entries)

    if args.json:
        print(json.dumps(report, indent=2, default=str))
    else:
        print(_render_markdown(report))

    return 0


if __name__ == "__main__":
    sys.exit(main())
