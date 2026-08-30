#!/usr/bin/env python3
"""Build the deterministic Wave A site-remediation candidate universe.

This tool is deliberately read-only with respect to tracked repository data. It
examines canonical games, participant assertions, reconciliation provenance, and
venue registries, then writes review artifacts under ``.onboarding`` (or an
explicit output directory).

The audit does *not* infer H/A/N from venue or geography. Venue/location evidence
is mechanically usable only when its source assertion independently agrees with
the canonical site classification (or with a mechanically unanimous site-type
candidate for a currently UNKNOWN canonical row). A known canonical site that is
contradicted by participant assertion evidence blocks dependent venue/location
enrichment unless that site conflict has already been explicitly resolved.
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
    team_a, _team_b = sorted((source_program, opponent))
    if source_site == "SOURCE_PROGRAM_HOME":
        return "TEAM_A_HOME" if source_program == team_a else "TEAM_B_HOME"
    if source_site == "OPPONENT_HOME":
        return "TEAM_A_HOME" if opponent == team_a else "TEAM_B_HOME"
    if source_site == "NEUTRAL":
        return "NEUTRAL"
    return "UNKNOWN"


def reconciliation_state(rows: Iterable[dict[str, str]], kind: str) -> str:
    """Return UNDER_REVIEW, RESOLVED, or blank for one discrepancy field family.

    UNDER_REVIEW dominates because a live unresolved conflict must never be
    treated as safe merely because an older resolved row also exists.
    """

    accepted = DISCREPANCY_FIELDS[kind]
    resolved = False
    for row in rows:
        if row.get("field_name", "").strip() not in accepted:
            continue
        status = row.get("status", "").strip().upper()
        if status == "UNDER_REVIEW":
            return "UNDER_REVIEW"
        if status == "RESOLVED" and row.get("resolution_basis", "").strip():
            resolved = True
    return "RESOLVED" if resolved else ""


def review_acknowledges(rows: Iterable[dict[str, str]], kind: str) -> bool:
    return bool(reconciliation_state(rows, kind))


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


def source_program_value_state(
    assertions: list[dict[str, str]],
    value_getter,
) -> tuple[dict[str, set[Any]], set[str]]:
    """Return nonblank values by participant source plus blank-only programs."""

    values_by_program: dict[str, set[Any]] = defaultdict(set)
    programs_seen: set[str] = set()
    for row in assertions:
        program = row.get("source_program_key", "").strip()
        if not program:
            continue
        programs_seen.add(program)
        value = value_getter(row)
        if value is None or value == "" or value == "UNKNOWN":
            continue
        values_by_program[program].add(value)
    blank_only = {
        program for program in programs_seen if not values_by_program.get(program)
    }
    return values_by_program, blank_only


def classify_support(
    values_by_program: dict[str, set[Any]], blank_programs: set[str]
) -> str:
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
                    *row.get("aliases", "").split(";"),
                ]
                for value in raw_names:
                    normalized = normalize_name(value)
                    if normalized:
                        self.school_names[program][normalized].add(venue_id)

    def location_matches(self, venue_id: str, city: str, state: str) -> bool:
        row = self.global_by_id.get(venue_id, {})
        if not city or not state:
            return True
        return (
            row.get("city", "").strip().casefold() == city.casefold()
            and row.get("state", "").strip().casefold() == state.casefold()
        )

    def resolve(self, assertion: dict[str, str]) -> tuple[str, str]:
        """Return ``(venue_id, basis)``; blank ID means identity is not safe."""

        raw_name = assertion.get("curated_venue_name", "").strip()
        if not raw_name:
            return "", "blank venue assertion"
        normalized = normalize_name(raw_name)
        program = assertion.get("source_program_key", "").strip()
        city = assertion.get("city", "").strip()
        state = assertion.get("state", "").strip()
        has_location = bool(city and state)

        school_candidates = set(
            self.school_names.get(program, {}).get(normalized, set())
        )
        if school_candidates:
            candidates = school_candidates
            if has_location:
                candidates = {
                    venue_id
                    for venue_id in school_candidates
                    if self.location_matches(venue_id, city, state)
                }
                if not candidates:
                    return "", "school venue identity conflicts with assertion location"
            if len(candidates) == 1:
                return next(iter(candidates)), "school venue registry"
            return "", "ambiguous school venue registry identity"

        global_candidates = set(self.global_names.get(normalized, set()))
        if global_candidates:
            candidates = global_candidates
            if has_location:
                candidates = {
                    venue_id
                    for venue_id in global_candidates
                    if self.location_matches(venue_id, city, state)
                }
                if not candidates:
                    return "", "global venue identity conflicts with assertion location"
            if len(candidates) == 1:
                return next(iter(candidates)), "unique global venue name/location"
            return "", "ambiguous global venue identity"
        return "", "venue name absent from school/global registries"


def base_output_row(game: dict[str, str], field_name: str) -> dict[str, str]:
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


def support_metadata(
    out: dict[str, str],
    supporting_rows: list[dict[str, str]],
    values_by_program: dict[str, set[Any]],
    blank_programs: set[str],
) -> None:
    out["supporting_programs"] = "|".join(
        sorted(
            {row.get("source_program_key", "").strip() for row in supporting_rows}
            - {""}
        )
    )
    out["supporting_source_game_ids"] = "|".join(
        sorted(
            {row.get("source_game_id", "").strip() for row in supporting_rows}
            - {""}
        )
    )
    out["known_program_count"] = str(
        len({program for program, values in values_by_program.items() if values})
    )
    out["blank_program_count"] = str(len(blank_programs))
    out["classification"] = classify_support(values_by_program, blank_programs)


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

    def add(bucket: list[dict[str, str]], out: dict[str, str], reason: str) -> None:
        out["reason"] = reason
        bucket.append(out)

    for game in canonical:
        canonical_id = game.get("canonical_game_id", "").strip()
        participants = participant_programs(game)
        game_assertions = [
            row
            for row in assertions_by_game.get(canonical_id, [])
            if row.get("source_program_key", "").strip() in participants
        ]
        if not game_assertions:
            continue
        game_discrepancies = discrepancies_by_game.get(canonical_id, [])

        site_values_by_program, site_blank_programs = source_program_value_state(
            game_assertions, canonical_site_from_assertion
        )
        site_known_values = {
            value for values in site_values_by_program.values() for value in values
        }
        site_supporting = [
            row
            for row in game_assertions
            if canonical_site_from_assertion(row) not in {"", "UNKNOWN"}
        ]
        site_reconciliation = reconciliation_state(game_discrepancies, "site_type")

        # Site type: never infer this from venue or geography.
        proposed_site = ""
        current_site = game.get("site_type", "").strip()
        site_dependency_blocked = False

        if current_site in {"", "UNKNOWN"}:
            out = base_output_row(game, "site_type")
            support_metadata(
                out,
                site_supporting,
                site_values_by_program,
                site_blank_programs,
            )
            out["evidence_values"] = "|".join(sorted(site_known_values))
            if site_reconciliation:
                out["classification"] = "RECONCILIATION_HOLD"
                add(
                    review,
                    out,
                    "canonical H/A/N is unresolved and field-specific reconciliation provenance exists",
                )
                site_dependency_blocked = True
            elif len(site_known_values) == 1:
                proposed_site = next(iter(site_known_values))
                out["proposed_value"] = proposed_site
                add(mechanical, out, "all known participant site assertions agree")
            elif len(site_known_values) > 1:
                out["classification"] = "CONFLICT_REVIEW"
                add(review, out, "participant site assertions conflict")
                site_dependency_blocked = True
            else:
                out["classification"] = "NO_USEFUL_EVIDENCE"
                add(review, out, "no participant assertion establishes H/A/N")
                site_dependency_blocked = True
        else:
            proposed_site = current_site
            conflicting_site_values = site_known_values - {current_site}
            if conflicting_site_values:
                out = base_output_row(game, "site_type")
                support_metadata(
                    out,
                    site_supporting,
                    site_values_by_program,
                    site_blank_programs,
                )
                out["proposed_value"] = current_site
                out["evidence_values"] = "|".join(sorted(site_known_values))
                if site_reconciliation == "RESOLVED":
                    out["classification"] = "RECONCILIATION_RESOLVED"
                    add(
                        review,
                        out,
                        "participant H/A/N evidence conflicts with canonical, but an explicit resolved site discrepancy retains the canonical classification; dependent enrichment may use only assertions agreeing with canonical",
                    )
                elif site_reconciliation == "UNDER_REVIEW":
                    out["classification"] = "RECONCILIATION_HOLD"
                    add(
                        review,
                        out,
                        "participant H/A/N evidence conflicts with canonical and the site discrepancy remains under review",
                    )
                    site_dependency_blocked = True
                else:
                    out["classification"] = "CANONICAL_ASSERTION_CONFLICT"
                    add(
                        review,
                        out,
                        "participant H/A/N evidence conflicts with the populated canonical classification and no explicit resolution provenance exists",
                    )
                    site_dependency_blocked = True

        effective_site = proposed_site or current_site
        if effective_site in {"", "UNKNOWN"} or site_dependency_blocked:
            continue

        agreeing_assertions = [
            row
            for row in game_assertions
            if canonical_site_from_assertion(row) == effective_site
        ]
        if not agreeing_assertions:
            continue

        # Venue: require one immutable physical identity after name+location checks.
        if canonical_venue_blank(game):
            out = base_output_row(game, "venue")

            def venue_value(assertion: dict[str, str]):
                venue_id, _basis = resolver.resolve(assertion)
                return venue_id or None

            values_by_program, blank_programs = source_program_value_state(
                agreeing_assertions, venue_value
            )
            resolved_values = {
                value for values in values_by_program.values() for value in values
            }
            raw_nonblank = [
                row
                for row in agreeing_assertions
                if row.get("curated_venue_name", "").strip()
            ]
            unresolved = [row for row in raw_nonblank if not resolver.resolve(row)[0]]
            supporting = [row for row in raw_nonblank if resolver.resolve(row)[0]]
            support_metadata(out, supporting, values_by_program, blank_programs)
            out["evidence_values"] = "|".join(sorted(resolved_values))

            if review_acknowledges(game_discrepancies, "venue"):
                out["classification"] = "RECONCILIATION_HOLD"
                add(review, out, "field-specific reconciliation provenance already exists")
            elif unresolved:
                out["classification"] = "VENUE_IDENTITY_REVIEW"
                details = sorted(
                    {
                        f"{row.get('source_program_key','')}:{row.get('curated_venue_name','')} ({resolver.resolve(row)[1]})"
                        for row in unresolved
                    }
                )
                add(review, out, "; ".join(details))
            elif len(resolved_values) == 1:
                venue_id = next(iter(resolved_values))
                venue = resolver.global_by_id.get(venue_id, {})
                out["proposed_value"] = venue.get("display_name", "").strip()
                out["proposed_venue_id"] = venue_id
                out["proposed_venue_key"] = venue.get("venue_key", "").strip()
                add(
                    mechanical,
                    out,
                    "all safely resolved agreeing venue assertions identify one physical venue",
                )
            elif len(resolved_values) > 1:
                out["classification"] = "CONFLICT_REVIEW"
                add(
                    review,
                    out,
                    "agreeing participant assertions resolve to different physical venues",
                )
            elif raw_nonblank:
                out["classification"] = "VENUE_IDENTITY_REVIEW"
                add(
                    review,
                    out,
                    "venue evidence exists but physical identity is not uniquely resolved",
                )

        # Location: require a complete pair; never overwrite a partial canonical pair.
        location_state = canonical_location_state(game)
        if location_state != "KNOWN":
            out = base_output_row(game, "location")

            def location_value(assertion: dict[str, str]):
                city = assertion.get("city", "").strip()
                state = assertion.get("state", "").strip()
                return (city, state) if city and state else None

            values_by_program, blank_programs = source_program_value_state(
                agreeing_assertions, location_value
            )
            known_values = {
                value for values in values_by_program.values() for value in values
            }
            supporting = [
                row for row in agreeing_assertions if location_value(row) is not None
            ]
            support_metadata(out, supporting, values_by_program, blank_programs)
            out["evidence_values"] = "|".join(
                sorted(f"{city}, {state}" for city, state in known_values)
            )

            if location_state == "PARTIAL":
                out["classification"] = "PARTIAL_CANONICAL_REVIEW"
                add(
                    review,
                    out,
                    "canonical city/state is partially populated; mechanical overwrite refused",
                )
            elif review_acknowledges(game_discrepancies, "location"):
                out["classification"] = "RECONCILIATION_HOLD"
                add(review, out, "field-specific reconciliation provenance already exists")
            elif len(known_values) == 1:
                city, state = next(iter(known_values))
                out["proposed_value"] = f"{city}, {state}"
                out["proposed_city"] = city
                out["proposed_state"] = state
                add(
                    mechanical,
                    out,
                    "all known agreeing participant location assertions agree",
                )
            elif len(known_values) > 1:
                out["classification"] = "CONFLICT_REVIEW"
                add(review, out, "agreeing participant location assertions conflict")

    mechanical.sort(key=lambda row: (row["canonical_game_id"], row["field_name"]))
    review.sort(
        key=lambda row: (
            row["canonical_game_id"],
            row["field_name"],
            row["classification"],
        )
    )

    counts: Counter[str] = Counter()
    mechanical_fields_by_game: dict[str, set[str]] = defaultdict(set)
    for row in mechanical:
        counts[f"mechanical:{row['field_name']}"] += 1
        counts[f"mechanical:{row['classification']}"] += 1
        mechanical_fields_by_game[row["canonical_game_id"]].add(row["field_name"])
    for fields in mechanical_fields_by_game.values():
        bundle = "+".join(sorted(fields))
        counts[f"mechanical_bundle:{bundle}"] += 1
    for row in review:
        counts[f"review:{row['field_name']}"] += 1
        counts[f"review:{row['classification']}"] += 1

    return {
        "mechanical": mechanical,
        "review": review,
        "summary": {
            "canonical_games_scanned": len(canonical),
            "assertions_scanned": len(assertions),
            "mechanical_game_candidates": len(mechanical_fields_by_game),
            "mechanical_field_candidates": len(mechanical),
            "review_games": len({row["canonical_game_id"] for row in review}),
            "review_field_rows": len(review),
            "counts": dict(sorted(counts.items())),
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
    print(f"Mechanical game candidates:    {summary['mechanical_game_candidates']:,}")
    print(f"Mechanical field candidates:   {summary['mechanical_field_candidates']:,}")
    print(f"Review games:                  {summary['review_games']:,}")
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
