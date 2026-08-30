#!/usr/bin/env python3
"""Build the deterministic Wave A site-remediation candidate universe.

This tool is deliberately read-only with respect to tracked repository data.  It
examines canonical games, participant assertions, reconciliation provenance, and
venue registries, then writes review artifacts under ``.onboarding`` (or an
explicit output directory).

The audit does *not* infer H/A/N from venue or geography.  Venue/location evidence
is considered mechanically usable only when its source assertion independently
agrees with the canonical site classification (or with a mechanically unanimous
site-type candidate for a currently UNKNOWN canonical row).
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


FIELDNAMES = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "game_type",
    "canonical_site_type",
    "canonical_venue_id",
    "canonical_venue_key",
    "canonical_city",
    "canonical_state",
    "field_name",
    "classification",
    "proposed_value",
    "proposed_venue_id",
    "proposed_venue_key",
    "proposed_city",
    "proposed_state",
    "supporting_programs",
    "supporting_source_game_ids",
    "known_program_count",
    "blank_program_count",
    "evidence_values",
    "reason",
]

DISCREPANCY_FIELDS = {
    "site_type": {"site_type"},
    "venue": {"venue", "venue_key", "venue_id"},
    "location": {"location", "site_city", "site_state"},
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def canonical_site_from_assertion(row: dict[str, str]) -> str:
    """Translate one source-program H/A/N assertion to canonical orientation."""

    source_program = row.get("source_program_key", "").strip()
    opponent = row.get("normalized_opponent_key", "").strip()
    source_site = row.get("curated_site_type", "").strip().upper()
    if not source_program or not opponent or source_program == opponent:
        return "UNKNOWN"
    team_a, team_b = sorted((source_program, opponent))
    if source_site == "SOURCE_PROGRAM_HOME":
        return "TEAM_A_HOME" if source_program == team_a else "TEAM_B_HOME"
    if source_site == "OPPONENT_HOME":
        return "TEAM_A_HOME" if opponent == team_a else "TEAM_B_HOME"
    if source_site == "NEUTRAL":
        return "NEUTRAL"
    return "UNKNOWN"


def review_acknowledges(rows: Iterable[dict[str, str]], kind: str) -> bool:
    accepted = DISCREPANCY_FIELDS[kind]
    for row in rows:
        if row.get("field_name", "").strip() not in accepted:
            continue
        status = row.get("status", "").strip().upper()
        if status == "UNDER_REVIEW":
            return True
        if status == "RESOLVED" and row.get("resolution_basis", "").strip():
            return True
    return False


def canonical_venue_blank(game: dict[str, str]) -> bool:
    return not (
        game.get("venue_id", "").strip() or game.get("venue_key", "").strip()
    )


def canonical_location_state(game: dict[str, str]) -> str:
    city = game.get("site_city", "").strip()
    state = game.get("site_state", "").strip()
    if city and state:
        return "KNOWN"
    if not city and not state:
        return "BLANK"
    return "PARTIAL"


def participant_programs(game: dict[str, str]) -> set[str]:
    return {
        game.get("team_a_key", "").strip(),
        game.get("team_b_key", "").strip(),
    } - {""}


def _source_program_value_state(
    assertions: list[dict[str, str]],
    value_getter,
) -> tuple[dict[str, set[Any]], set[str]]:
    """Return nonblank values by participant source plus programs with blank evidence."""

    values_by_program: dict[str, set[Any]] = defaultdict(set)
    programs_seen: set[str] = set()
    programs_with_blank: set[str] = set()
    for row in assertions:
        program = row.get("source_program_key", "").strip()
        if not program:
            continue
        programs_seen.add(program)
        value = value_getter(row)
        if value is None or value == "" or value == "UNKNOWN":
            programs_with_blank.add(program)
        else:
            values_by_program[program].add(value)
    blank_only = {
        program
        for program in programs_seen
        if not values_by_program.get(program)
    }
    return values_by_program, blank_only


def classify_support(values_by_program: dict[str, set[Any]], blank_programs: set[str]) -> str:
    known_programs = {program for program, values in values_by_program.items() if values}
    if len(known_programs) >= 2:
        return "RECIPROCAL_CONSENSUS"
    if len(known_programs) == 1 and blank_programs:
        return "RECIPROCAL_ONLY"
    return "SINGLE_SOURCE_PROPAGATION"


class VenueResolver:
    """Conservatively resolve assertion venue strings to immutable global IDs."""

    def __init__(self, repo: Path):
        _, global_rows = read_csv(repo / "data/reference/venues.csv")
        self.global_by_id = {
            row.get("venue_id", "").strip(): row
            for row in global_rows
            if row.get("venue_id", "").strip()
        }
        self.global_names: dict[str, set[str]] = defaultdict(set)
        for row in global_rows:
            venue_id = row.get("venue_id", "").strip()
            for value in (row.get("display_name", ""), row.get("venue_key", "")):
                normalized = normalize_name(value)
                if venue_id and normalized:
                    self.global_names[normalized].add(venue_id)

        names_path = repo / "data/reference/venue-names.csv"
        if names_path.is_file():
            _, name_rows = read_csv(names_path)
            for row in name_rows:
                venue_id = row.get("venue_id", "").strip()
                normalized = row.get("normalized_name", "").strip() or normalize_name(
                    row.get("venue_name", "")
                )
                if venue_id and normalized:
                    self.global_names[normalized].add(venue_id)

        self.school_names: dict[str, dict[str, set[str]]] = defaultdict(
            lambda: defaultdict(set)
        )
        schools_root = repo / "schools"
        for path in sorted(schools_root.glob("*/venues.csv")):
            _, rows = read_csv(path)
            fallback_school = path.parent.name
            for row in rows:
                program = row.get("source_program_key", "").strip() or fallback_school
                venue_id = row.get("venue_id", "").strip()
                if not venue_id:
                    continue
                raw_names = [
                    row.get("canonical_name", ""),
                    row.get("venue_key", ""),
                ]
                raw_names.extend(row.get("aliases", "").split(";"))
                for value in raw_names:
                    normalized = normalize_name(value)
                    if normalized:
                        self.school_names[program][normalized].add(venue_id)

    def _location_matches(self, venue_id: str, city: str, state: str) -> bool:
        row = self.global_by_id.get(venue_id, {})
        if not city or not state:
            return True
        return (
            row.get("city", "").strip().casefold() == city.casefold()
            and row.get("state", "").strip().casefold() == state.casefold()
        )

    def resolve(self, assertion: dict[str, str]) -> tuple[str, str]:
        """Return (venue_id, reason); blank venue_id means not safely resolvable."""

        raw_name = assertion.get("curated_venue_name", "").strip()
        if not raw_name:
            return "", "blank venue assertion"
        normalized = normalize_name(raw_name)
        program = assertion.get("source_program_key", "").strip()
        city = assertion.get("city", "").strip()
        state = assertion.get("state", "").strip()

        school_candidates = set(self.school_names.get(program, {}).get(normalized, set()))
        if school_candidates:
            location_filtered = {
                venue_id
                for venue_id in school_candidates
                if self._location_matches(venue_id, city, state)
            }
            candidates = location_filtered or school_candidates
            if len(candidates) == 1:
                return next(iter(candidates)), "school venue registry"
            return "", "ambiguous school venue registry identity"

        global_candidates = set(self.global_names.get(normalized, set()))
        if global_candidates:
            location_filtered = {
                venue_id
                for venue_id in global_candidates
                if self._location_matches(venue_id, city, state)
            }
            candidates = location_filtered or global_candidates
            if len(candidates) == 1:
                return next(iter(candidates)), "unique global venue name/location"
            return "", "ambiguous global venue identity"
        return "", "venue name absent from school/global registries"


def _base_output_row(game: dict[str, str], field_name: str) -> dict[str, str]:
    return {
        "canonical_game_id": game.get("canonical_game_id", "").strip(),
        "season_label": game.get("season_label", "").strip(),
        "game_date": game.get("game_date", "").strip(),
        "team_a_key": game.get("team_a_key", "").strip(),
        "team_b_key": game.get("team_b_key", "").strip(),
        "game_type": game.get("game_type", "").strip(),
        "canonical_site_type": game.get("site_type", "").strip(),
        "canonical_venue_id": game.get("venue_id", "").strip(),
        "canonical_venue_key": game.get("venue_key", "").strip(),
        "canonical_city": game.get("site_city", "").strip(),
        "canonical_state": game.get("site_state", "").strip(),
        "field_name": field_name,
        "classification": "",
        "proposed_value": "",
        "proposed_venue_id": "",
        "proposed_venue_key": "",
        "proposed_city": "",
        "proposed_state": "",
        "supporting_programs": "",
        "supporting_source_game_ids": "",
        "known_program_count": "0",
        "blank_program_count": "0",
        "evidence_values": "",
        "reason": "",
    }


def _support_metadata(
    row: dict[str, str],
    assertions: list[dict[str, str]],
    supporting_rows: list[dict[str, str]],
    values_by_program: dict[str, set[Any]],
    blank_programs: set[str],
) -> None:
    row["supporting_programs"] = "|".join(
        sorted({item.get("source_program_key", "").strip() for item in supporting_rows} - {""})
    )
    row["supporting_source_game_ids"] = "|".join(
        sorted({item.get("source_game_id", "").strip() for item in supporting_rows} - {""})
    )
    row["known_program_count"] = str(
        len({program for program, values in values_by_program.items() if values})
    )
    row["blank_program_count"] = str(len(blank_programs))
    row["classification"] = classify_support(values_by_program, blank_programs)


def build_audit(repo: Path) -> dict[str, Any]:
    _, canonical = read_csv(repo / "data/canonical/games.csv")
    _, assertions = read_csv(repo / "data/evidence/game-assertions.csv")
    _, discrepancies = read_csv(repo / "data/reconciliation/discrepancies.csv")
    resolver = VenueResolver(repo)

    assertions_by_game: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        canonical_id = row.get("canonical_game_id", "").strip()
        if canonical_id:
            assertions_by_game[canonical_id].append(row)

    discrepancies_by_game: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in discrepancies:
        canonical_id = row.get("canonical_game_id", "").strip()
        if canonical_id:
            discrepancies_by_game[canonical_id].append(row)

    mechanical: list[dict[str, str]] = []
    review: list[dict[str, str]] = []
    counts: Counter[str] = Counter()

    def add(bucket: list[dict[str, str]], row: dict[str, str], reason: str) -> None:
        row["reason"] = reason
        bucket.append(row)
        counts[f"{row['field_name']}:{row['classification']}"] += 1

    for game in canonical:
        canonical_id = game.get("canonical_game_id", "").strip()
        game_assertions = [
            row
            for row in assertions_by_game.get(canonical_id, [])
            if row.get("source_program_key", "").strip() in participant_programs(game)
        ]
        if not game_assertions:
            continue
        game_discrepancies = discrepancies_by_game.get(canonical_id, [])

        # 1. Site type. Venue/geography never participates in this decision.
        proposed_site = ""
        current_site = game.get("site_type", "").strip()
        if current_site in {"", "UNKNOWN"}:
            out = _base_output_row(game, "site_type")
            values_by_program, blank_programs = _source_program_value_state(
                game_assertions, canonical_site_from_assertion
            )
            known_values = {
                value for values in values_by_program.values() for value in values
            }
            supporting = [
                row
                for row in game_assertions
                if canonical_site_from_assertion(row) not in {"", "UNKNOWN"}
            ]
            _support_metadata(out, game_assertions, supporting, values_by_program, blank_programs)
            out["evidence_values"] = "|".join(sorted(str(value) for value in known_values))
            if review_acknowledges(game_discrepancies, "site_type"):
                out["classification"] = "RECONCILIATION_HOLD"
                add(review, out, "field-specific reconciliation provenance already exists")
            elif len(known_values) == 1:
                proposed_site = str(next(iter(known_values)))
                out["proposed_value"] = proposed_site
                add(mechanical, out, "all known participant site assertions agree")
            elif len(known_values) > 1:
                out["classification"] = "CONFLICT_REVIEW"
                add(review, out, "participant site assertions conflict")
            else:
                out["classification"] = "NO_USEFUL_EVIDENCE"
                add(review, out, "no participant assertion establishes H/A/N")
        else:
            proposed_site = current_site

        effective_site = proposed_site or current_site
        if effective_site in {"", "UNKNOWN"}:
            # Without independently established H/A/N, venue/geography are review-only.
            continue

        agreeing_assertions = [
            row
            for row in game_assertions
            if canonical_site_from_assertion(row) == effective_site
        ]
        if not agreeing_assertions:
            continue

        # 2. Venue identity. Only immutable, uniquely resolved venue IDs are mechanical.
        if canonical_venue_blank(game):
            out = _base_output_row(game, "venue")

            def venue_value(assertion: dict[str, str]):
                venue_id, _ = resolver.resolve(assertion)
                return venue_id or None

            values_by_program, blank_programs = _source_program_value_state(
                agreeing_assertions, venue_value
            )
            resolved_values = {
                value for values in values_by_program.values() for value in values
            }
            raw_nonblank = [
                row for row in agreeing_assertions if row.get("curated_venue_name", "").strip()
            ]
            unresolved_rows = [
                row for row in raw_nonblank if not resolver.resolve(row)[0]
            ]
            supporting = [
                row for row in raw_nonblank if resolver.resolve(row)[0]
            ]
            _support_metadata(out, agreeing_assertions, supporting, values_by_program, blank_programs)
            out["evidence_values"] = "|".join(sorted(str(value) for value in resolved_values))

            if review_acknowledges(game_discrepancies, "venue"):
                out["classification"] = "RECONCILIATION_HOLD"
                add(review, out, "field-specific reconciliation provenance already exists")
            elif unresolved_rows:
                out["classification"] = "VENUE_IDENTITY_REVIEW"
                details = sorted(
                    {
                        f"{row.get('source_program_key','')}:{row.get('curated_venue_name','')} ({resolver.resolve(row)[1]})"
                        for row in unresolved_rows
                    }
                )
                add(review, out, "; ".join(details))
            elif len(resolved_values) == 1:
                venue_id = str(next(iter(resolved_values)))
                venue = resolver.global_by_id.get(venue_id, {})
                out["proposed_value"] = venue.get("display_name", "").strip()
                out["proposed_venue_id"] = venue_id
                out["proposed_venue_key"] = venue.get("venue_key", "").strip()
                add(mechanical, out, "all safely resolved agreeing venue assertions identify one physical venue")
            elif len(resolved_values) > 1:
                out["classification"] = "CONFLICT_REVIEW"
                add(review, out, "agreeing participant assertions resolve to different physical venues")
            elif raw_nonblank:
                out["classification"] = "VENUE_IDENTITY_REVIEW"
                add(review, out, "venue evidence exists but physical identity is not uniquely resolved")

        # 3. Location pair. Partial canonical geography is never overwritten mechanically.
        location_state = canonical_location_state(game)
        if location_state != "KNOWN":
            out = _base_output_row(game, "location")

            def location_value(assertion: dict[str, str]):
                city = assertion.get("city", "").strip()
                state = assertion.get("state", "").strip()
                if city and state:
                    return (city, state)
                return None

            values_by_program, blank_programs = _source_program_value_state(
                agreeing_assertions, location_value
            )
            known_values = {
                value for values in values_by_program.values() for value in values
            }
            supporting = [
                row for row in agreeing_assertions if location_value(row) is not None
            ]
            _support_metadata(out, agreeing_assertions, supporting, values_by_program, blank_programs)
            out["evidence_values"] = "|".join(
                sorted(f"{city}, {state}" for city, state in known_values)
            )

            if location_state == "PARTIAL":
                out["classification"] = "PARTIAL_CANONICAL_REVIEW"
                add(review, out, "canonical city/state is partially populated; mechanical overwrite refused")
            elif review_acknowledges(game_discrepancies, "location"):
                out["classification"] = "RECONCILIATION_HOLD"
                add(review, out, "field-specific reconciliation provenance already exists")
            elif len(known_values) == 1:
                city, state = next(iter(known_values))
                out["proposed_value"] = f"{city}, {state}"
                out["proposed_city"] = city
                out["proposed_state"] = state
                add(mechanical, out, "all known agreeing participant location assertions agree")
            elif len(known_values) > 1:
                out["classification"] = "CONFLICT_REVIEW"
                add(review, out, "agreeing participant location assertions conflict")

    mechanical.sort(key=lambda row: (row["canonical_game_id"], row["field_name"]))
    review.sort(key=lambda row: (row["canonical_game_id"], row["field_name"], row["classification"]))

    summary_counts = Counter()
    for row in mechanical:
        summary_counts[f"mechanical:{row['field_name']}"] += 1
        summary_counts[f"mechanical:{row['classification']}"] += 1
    for row in review:
        summary_counts[f"review:{row['field_name']}"] += 1
        summary_counts[f"review:{row['classification']}"] += 1

    return {
        "mechanical": mechanical,
        "review": review,
        "summary": {
            "canonical_games_scanned": len(canonical),
            "assertions_scanned": len(assertions),
            "mechanical_field_candidates": len(mechanical),
            "review_field_rows": len(review),
            "counts": dict(sorted(summary_counts.items())),
        },
    }


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_report(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "mechanical-candidates.csv", report["mechanical"])
    write_csv(output_dir / "review-candidates.csv", report["review"])
    (output_dir / "summary.json").write_text(
        json.dumps(report["summary"], indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def print_summary(report: dict[str, Any], output_dir: Path) -> None:
    summary = report["summary"]
    print("College Basketball History — site remediation Wave A audit")
    print(f"Canonical games scanned:       {summary['canonical_games_scanned']:,}")
    print(f"Assertions scanned:            {summary['assertions_scanned']:,}")
    print(f"Mechanical field candidates:   {summary['mechanical_field_candidates']:,}")
    print(f"Review field rows:              {summary['review_field_rows']:,}")
    for key, value in summary["counts"].items():
        print(f"  {key}: {value:,}")
    print(f"Artifacts: {output_dir}")
    print("PASS: audit only; no tracked basketball data was changed.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the read-only Wave A site-remediation candidate universe."
    )
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else repo / ".onboarding" / "site-remediation-wave-a"
    )
    try:
        report = build_audit(repo)
        write_report(report, output_dir)
        print_summary(report, output_dir)
        return 0
    except (FileNotFoundError, ValueError, KeyError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
