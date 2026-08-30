#!/usr/bin/env python3
"""Summarize the Wave A2 owner-review dossier into decision-relevant evidence classes.

This is read-only. It consumes the permanent A2 review builder and reports which
participant is the UNKNOWN side, the raw/curated site evidence forms supporting
the proposed H/A/N value, match-method confidence, and physical-support splits.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from site_remediation_a2_review import build_a2_review


def _parts(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split("|") if item.strip()]


def _unknown_side(row: dict[str, str]) -> str:
    participants = {
        row.get("team_a_key", "").strip(),
        row.get("team_b_key", "").strip(),
    } - {""}
    supporters = set(_parts(row.get("supporting_programs", "")))
    remaining = sorted(participants - supporters)
    return remaining[0] if len(remaining) == 1 else "|".join(remaining) or "[none]"


def _raw_indicator_state(row: dict[str, str]) -> str:
    """Classify whether source_site_candidate contains an explicit raw site cue."""
    values = _parts(row.get("source_site_candidates", ""))
    if not values:
        return "NO_RAW_SITE_CANDIDATE"

    explicit_tokens = {
        "H",
        "A",
        "N",
        "HOME",
        "AWAY",
        "NEUTRAL",
        "SOURCE_PROGRAM_HOME",
        "OPPONENT_HOME",
    }
    normalized = {
        value.upper().replace("-", "_").replace(" ", "_") for value in values
    }
    if normalized & explicit_tokens:
        return "EXPLICIT_RAW_HAN_TOKEN"

    text = " ".join(normalized)
    if any(token in text for token in ("HOME", "AWAY", "NEUTRAL")):
        return "EXPLICIT_RAW_HAN_TEXT"
    return "OTHER_RAW_SITE_CANDIDATE"


def build_census(repo: Path) -> dict[str, Any]:
    review = build_a2_review(repo)
    if review["summary"]["status"] != "PASS":
        raise ValueError("A2 owner-review dossier must PASS before census")

    rows = review["rows"]
    counters: dict[str, Counter[str]] = {
        "unknown_side_program": Counter(),
        "supporting_program": Counter(),
        "proposed_site_type": Counter(),
        "evidence_profile": Counter(),
        "review_bucket": Counter(),
        "source_site_forms": Counter(),
        "source_site_candidates": Counter(),
        "raw_indicator_state": Counter(),
        "match_methods": Counter(),
        "supporting_assertion_count": Counter(),
        "physical_support_by_site": Counter(),
        "site_only_by_site": Counter(),
    }

    exceptions: list[dict[str, str]] = []
    site_only_without_explicit_raw: list[dict[str, str]] = []

    for row in rows:
        unknown = _unknown_side(row)
        counters["unknown_side_program"][unknown] += 1
        for program in _parts(row.get("supporting_programs", "")):
            counters["supporting_program"][program] += 1
        for key in (
            "proposed_site_type",
            "evidence_profile",
            "review_bucket",
            "source_site_forms",
            "source_site_candidates",
            "match_methods",
            "supporting_assertion_count",
        ):
            counters[key][row.get(key, "").strip() or "[blank]"] += 1

        raw_state = _raw_indicator_state(row)
        counters["raw_indicator_state"][raw_state] += 1
        site = row.get("proposed_site_type", "").strip()
        profile = row.get("evidence_profile", "").strip()
        if profile == "SITE_ASSERTION_ONLY":
            counters["site_only_by_site"][site] += 1
            if raw_state not in {"EXPLICIT_RAW_HAN_TOKEN", "EXPLICIT_RAW_HAN_TEXT"}:
                site_only_without_explicit_raw.append(row)
        else:
            counters["physical_support_by_site"][site] += 1

        if unknown != "alabama":
            exceptions.append(row)

    return {
        "candidate_games": len(rows),
        "counts": {
            name: dict(sorted(counter.items()))
            for name, counter in counters.items()
        },
        "non_alabama_unknown_side": [
            {
                "canonical_game_id": row["canonical_game_id"],
                "season_label": row["season_label"],
                "team_a_key": row["team_a_key"],
                "team_b_key": row["team_b_key"],
                "proposed_site_type": row["proposed_site_type"],
                "supporting_programs": row["supporting_programs"],
                "evidence_profile": row["evidence_profile"],
                "source_site_forms": row["source_site_forms"],
                "source_site_candidates": row["source_site_candidates"],
                "match_methods": row["match_methods"],
            }
            for row in exceptions
        ],
        "site_only_without_explicit_raw_count": len(site_only_without_explicit_raw),
        "site_only_without_explicit_raw_examples": [
            {
                "canonical_game_id": row["canonical_game_id"],
                "season_label": row["season_label"],
                "team_a_key": row["team_a_key"],
                "team_b_key": row["team_b_key"],
                "proposed_site_type": row["proposed_site_type"],
                "supporting_programs": row["supporting_programs"],
                "source_site_forms": row["source_site_forms"],
                "source_site_candidates": row["source_site_candidates"],
                "raw_text_excerpt": row["raw_text_excerpt"],
            }
            for row in site_only_without_explicit_raw[:20]
        ],
    }


def print_census(census: dict[str, Any]) -> None:
    print("College Basketball History — Wave A2 evidence census")
    print(f"Candidate games: {census['candidate_games']:,}")
    for name, values in census["counts"].items():
        print(f"{name}: {json.dumps(values, sort_keys=True)}")
    print(
        "site_only_without_explicit_raw_count: "
        f"{census['site_only_without_explicit_raw_count']:,}"
    )
    if census["non_alabama_unknown_side"]:
        print("Non-Alabama UNKNOWN-side exceptions:")
        for row in census["non_alabama_unknown_side"]:
            print("  " + json.dumps(row, sort_keys=True))
    if census["site_only_without_explicit_raw_examples"]:
        print("Site-only rows without explicit raw H/A/N indicator (examples):")
        for row in census["site_only_without_explicit_raw_examples"]:
            print("  " + json.dumps(row, sort_keys=True))
    print("PASS: census only; no tracked basketball data was changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Summarize Wave A2 evidence classes.")
    parser.add_argument("--repo", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        census = build_census(repo)
        print_census(census)
        return 0
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
