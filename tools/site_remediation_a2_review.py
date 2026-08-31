#!/usr/bin/env python3
"""Build a read-only owner-review dossier for Wave A2 site-type remediation.

A2 consists of canonical games whose H/A/N is currently UNKNOWN but for which
participant source assertions provide one uncontested canonical site type.  This
tool does not apply those changes.  It turns the candidate universe into an
evidence census suitable for owner review before any semantic H/A/N mutation.

Artifacts are written under ``.onboarding/site-remediation-wave-a2`` by default.
Tracked basketball data is never modified.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from site_remediation_audit import canonical_site_from_assertion, read_csv
from site_remediation_tier_report import build_tier_report


A2_TIER = "A2_UNCONTESTED_SITE_TYPE"
OUTPUT_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "game_type",
    "current_site_type",
    "proposed_site_type",
    "proposed_home_team_key",
    "evidence_profile",
    "review_bucket",
    "supporting_programs",
    "supporting_source_game_ids",
    "supporting_program_count",
    "supporting_assertion_count",
    "other_participant_evidence_state",
    "source_site_forms",
    "source_site_candidates",
    "match_methods",
    "proposed_venue_id",
    "proposed_venue_key",
    "proposed_city",
    "proposed_state",
    "source_venue_names",
    "curated_venue_names",
    "source_locations",
    "event_or_tournament",
    "source_pages",
    "raw_text_excerpt",
    "site_discrepancy_statuses",
]


class A2ReviewError(RuntimeError):
    """Raised when the A2 candidate universe violates its review invariants."""


def _pipe(values: set[str] | list[str]) -> str:
    return "|".join(sorted({value.strip() for value in values if value and value.strip()}))


def _excerpt(value: str, limit: int = 240) -> str:
    compact = " ".join((value or "").split())
    return compact if len(compact) <= limit else compact[: limit - 1] + "…"


def evidence_profile(candidate: dict[str, str]) -> str:
    has_venue = bool(candidate.get("proposed_venue_id", "").strip())
    has_location = bool(
        candidate.get("proposed_city", "").strip()
        and candidate.get("proposed_state", "").strip()
    )
    if has_venue and has_location:
        return "VENUE_AND_LOCATION"
    if has_venue:
        return "VENUE_ONLY"
    if has_location:
        return "LOCATION_ONLY"
    return "SITE_ASSERTION_ONLY"


def proposed_home_team(candidate: dict[str, str]) -> str:
    site = candidate.get("proposed_site_type", "").strip()
    if site == "TEAM_A_HOME":
        return candidate.get("team_a_key", "").strip()
    if site == "TEAM_B_HOME":
        return candidate.get("team_b_key", "").strip()
    return ""


def classify_review_bucket(profile: str, supporting_program_count: int) -> str:
    if supporting_program_count >= 2:
        return "RECIPROCAL_CONSENSUS"
    if profile in {"VENUE_AND_LOCATION", "VENUE_ONLY", "LOCATION_ONLY"}:
        return "ONE_SIDED_WITH_PHYSICAL_SUPPORT"
    return "ONE_SIDED_SITE_ASSERTION_ONLY"


def _other_participant_state(
    participants: set[str],
    assertions: list[dict[str, str]],
    proposed_site: str,
) -> str:
    programs_with_assertions = {
        row.get("source_program_key", "").strip()
        for row in assertions
        if row.get("source_program_key", "").strip() in participants
    }
    known_by_program: dict[str, set[str]] = defaultdict(set)
    for row in assertions:
        program = row.get("source_program_key", "").strip()
        if program not in participants:
            continue
        value = canonical_site_from_assertion(row)
        if value not in {"", "UNKNOWN"}:
            known_by_program[program].add(value)

    agreeing = {
        program
        for program, values in known_by_program.items()
        if values == {proposed_site}
    }
    others = participants - agreeing
    if not others:
        return "ALL_PARTICIPANTS_AGREE"
    if any(program in known_by_program for program in others):
        return "OTHER_PARTICIPANT_HAS_KNOWN_SITE"
    if any(program in programs_with_assertions for program in others):
        return "OTHER_PARTICIPANT_UNKNOWN_ASSERTION"
    return "OTHER_PARTICIPANT_NO_ASSERTION"


def build_a2_review(repo: Path) -> dict[str, Any]:
    tier_report = build_tier_report(repo)
    _, assertions = read_csv(repo / "data/evidence/game-assertions.csv")
    _, discrepancies = read_csv(repo / "data/reconciliation/discrepancies.csv")

    assertions_by_game: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        game_id = row.get("canonical_game_id", "").strip()
        if game_id:
            assertions_by_game[game_id].append(row)

    discrepancies_by_game: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in discrepancies:
        game_id = row.get("canonical_game_id", "").strip()
        if game_id:
            discrepancies_by_game[game_id].append(row)

    rows: list[dict[str, str]] = []
    errors: list[str] = []

    candidates = [row for row in tier_report["rows"] if row.get("tier") == A2_TIER]
    for candidate in candidates:
        game_id = candidate.get("canonical_game_id", "").strip()
        proposed_site = candidate.get("proposed_site_type", "").strip()
        participants = {
            candidate.get("team_a_key", "").strip(),
            candidate.get("team_b_key", "").strip(),
        } - {""}

        if candidate.get("current_site_type", "").strip() not in {"", "UNKNOWN"}:
            errors.append(f"{game_id}: A2 candidate canonical site is not UNKNOWN")
        if proposed_site not in {"TEAM_A_HOME", "TEAM_B_HOME", "NEUTRAL"}:
            errors.append(f"{game_id}: A2 candidate has invalid proposed site {proposed_site!r}")

        game_assertions = [
            row
            for row in assertions_by_game.get(game_id, [])
            if row.get("source_program_key", "").strip() in participants
        ]
        supporting = [
            row
            for row in game_assertions
            if canonical_site_from_assertion(row) == proposed_site
        ]
        known_values = {
            canonical_site_from_assertion(row)
            for row in game_assertions
            if canonical_site_from_assertion(row) not in {"", "UNKNOWN"}
        }
        if known_values != {proposed_site}:
            errors.append(
                f"{game_id}: participant assertion site universe is {sorted(known_values)}, "
                f"expected only {proposed_site}"
            )
        if not supporting:
            errors.append(f"{game_id}: no supporting source assertion found")

        supporting_programs = {
            row.get("source_program_key", "").strip() for row in supporting
        } - {""}
        supporting_ids = {
            row.get("source_game_id", "").strip() for row in supporting
        } - {""}

        expected_programs = {
            value
            for value in candidate.get("supporting_programs", "").split("|")
            if value
        }
        if expected_programs and not expected_programs.issubset(supporting_programs):
            errors.append(
                f"{game_id}: tier support programs {sorted(expected_programs)} are not "
                f"contained in assertion support {sorted(supporting_programs)}"
            )

        site_discrepancies = [
            row
            for row in discrepancies_by_game.get(game_id, [])
            if row.get("field_name", "").strip() == "site_type"
        ]
        if site_discrepancies:
            errors.append(
                f"{game_id}: A2 candidate unexpectedly has field-specific site reconciliation"
            )

        profile = evidence_profile(candidate)
        home_team = proposed_home_team(candidate)
        if home_team and home_team not in participants:
            errors.append(f"{game_id}: proposed home team is not a participant")

        source_locations = {
            f"{row.get('city','').strip()}, {row.get('state','').strip()}"
            for row in supporting
            if row.get("city", "").strip() and row.get("state", "").strip()
        }
        raw_excerpts = [_excerpt(row.get("raw_text", "")) for row in supporting]

        rows.append(
            {
                "canonical_game_id": game_id,
                "season_label": candidate.get("season_label", "").strip(),
                "game_date": candidate.get("game_date", "").strip(),
                "team_a_key": candidate.get("team_a_key", "").strip(),
                "team_b_key": candidate.get("team_b_key", "").strip(),
                "game_type": candidate.get("game_type", "").strip(),
                "current_site_type": candidate.get("current_site_type", "").strip(),
                "proposed_site_type": proposed_site,
                "proposed_home_team_key": home_team,
                "evidence_profile": profile,
                "review_bucket": classify_review_bucket(profile, len(supporting_programs)),
                "supporting_programs": _pipe(supporting_programs),
                "supporting_source_game_ids": _pipe(supporting_ids),
                "supporting_program_count": str(len(supporting_programs)),
                "supporting_assertion_count": str(len(supporting)),
                "other_participant_evidence_state": _other_participant_state(
                    participants, game_assertions, proposed_site
                ),
                "source_site_forms": _pipe(
                    {row.get("curated_site_type", "") for row in supporting}
                ),
                "source_site_candidates": _pipe(
                    {row.get("source_site_candidate", "") for row in supporting}
                ),
                "match_methods": _pipe({row.get("match_method", "") for row in supporting}),
                "proposed_venue_id": candidate.get("proposed_venue_id", "").strip(),
                "proposed_venue_key": candidate.get("proposed_venue_key", "").strip(),
                "proposed_city": candidate.get("proposed_city", "").strip(),
                "proposed_state": candidate.get("proposed_state", "").strip(),
                "source_venue_names": _pipe(
                    {row.get("source_venue_name", "") for row in supporting}
                ),
                "curated_venue_names": _pipe(
                    {row.get("curated_venue_name", "") for row in supporting}
                ),
                "source_locations": _pipe(source_locations),
                "event_or_tournament": _pipe(
                    {row.get("event_or_tournament", "") for row in supporting}
                ),
                "source_pages": _pipe({row.get("source_page", "") for row in supporting}),
                "raw_text_excerpt": " || ".join(value for value in raw_excerpts if value),
                "site_discrepancy_statuses": _pipe(
                    {row.get("status", "") for row in site_discrepancies}
                ),
            }
        )

    rows.sort(key=lambda row: row["canonical_game_id"])

    counts: Counter[str] = Counter()
    decades: Counter[str] = Counter()
    supporting_programs_count: Counter[str] = Counter()
    for row in rows:
        counts[f"profile:{row['evidence_profile']}"] += 1
        counts[f"bucket:{row['review_bucket']}"] += 1
        counts[f"site:{row['proposed_site_type']}"] += 1
        counts[f"other:{row['other_participant_evidence_state']}"] += 1
        season = row["season_label"]
        decade = f"{season[:3]}0s" if len(season) >= 4 and season[:4].isdigit() else "[unknown]"
        decades[decade] += 1
        for program in row["supporting_programs"].split("|"):
            if program:
                supporting_programs_count[program] += 1

    summary = {
        "status": "PASS" if not errors else "FAIL",
        "candidate_games": len(rows),
        "counts": dict(sorted(counts.items())),
        "decades": dict(sorted(decades.items())),
        "supporting_programs": dict(sorted(supporting_programs_count.items())),
        "errors": errors,
    }
    return {"rows": rows, "summary": summary}


def write_report(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    with (output_dir / "a2-owner-review.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(report["rows"])
    (output_dir / "a2-summary.json").write_text(
        json.dumps(report["summary"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def print_summary(report: dict[str, Any], output_dir: Path) -> None:
    summary = report["summary"]
    print("College Basketball History — Wave A2 owner-review dossier")
    print(f"Status:                {summary['status']}")
    print(f"Candidate games:       {summary['candidate_games']:,}")
    for key, value in summary["counts"].items():
        print(f"  {key}: {value:,}")
    print("Supporting programs:   " + json.dumps(summary["supporting_programs"], sort_keys=True))
    print("Decades:               " + json.dumps(summary["decades"], sort_keys=True))
    for error in summary["errors"]:
        print(f"ERROR: {error}")
    print(f"Artifacts: {output_dir}")
    if summary["status"] == "PASS":
        print("PASS: review dossier only; no tracked basketball data was changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build read-only Wave A2 owner review.")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else repo / ".onboarding" / "site-remediation-wave-a2"
    )
    try:
        report = build_a2_review(repo)
        write_report(report, output_dir)
        print_summary(report, output_dir)
        return 0 if report["summary"]["status"] == "PASS" else 1
    except (A2ReviewError, FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
