#!/usr/bin/env python3
"""Implementation/release site-completeness gate for one onboarding target.

This gate is intentionally independent of research acceptance. It checks the
post-reconciliation canonical result so a good source portfolio cannot silently
lose site information during matching, enrichment, or publication.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from site_completeness import (
    ALLOWED_SITE_RESEARCH_STATUSES,
    POSTSEASON_TYPES_REQUIRING_ACCOUNTING,
    researched_unresolved_home_venue,
    source_site_completeness_report,
)

HOME_VENUE_EXCEPTION_MARKER = "[RESEARCHED_UNRESOLVED_HOME_VENUE"


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def _complete_pair(first: str, second: str) -> bool:
    return bool((first or "").strip() and (second or "").strip())


def _venue_known(row: dict[str, str]) -> bool:
    return bool(row.get("venue_key", "").strip() or row.get("venue_id", "").strip())


def _source_site_to_canonical(row: dict[str, str]) -> str:
    school = row.get("source_program_key", "").strip()
    opponent = row.get("normalized_opponent_key", "").strip()
    source_site = row.get("curated_site_type", "").strip().upper()
    team_a, team_b = sorted((school, opponent))
    if source_site == "SOURCE_PROGRAM_HOME":
        return "TEAM_A_HOME" if team_a == school else "TEAM_B_HOME"
    if source_site == "OPPONENT_HOME":
        return "TEAM_A_HOME" if team_a == opponent else "TEAM_B_HOME"
    if source_site == "NEUTRAL":
        return "NEUTRAL"
    return "UNKNOWN"


def _target_home(row: dict[str, str], school_key: str) -> bool:
    site = row.get("site_type", "").strip()
    return (
        (site == "TEAM_A_HOME" and row.get("team_a_key", "").strip() == school_key)
        or (site == "TEAM_B_HOME" and row.get("team_b_key", "").strip() == school_key)
    )


def _canonical_gap_categories(
    row: dict[str, str],
    school_key: str,
) -> list[str]:
    site = row.get("site_type", "").strip()
    game_type = row.get("game_type", "").strip()
    venue_missing = not _venue_known(row)
    location_missing = not _complete_pair(
        row.get("site_city", ""),
        row.get("site_state", ""),
    )

    categories: list[str] = []
    if _target_home(row, school_key):
        if venue_missing:
            categories.append("home_missing_venue")
        if location_missing:
            categories.append("home_missing_location")
        if venue_missing and location_missing:
            categories.append("home_missing_both")

    if site in {"", "UNKNOWN"}:
        categories.append("unknown_site_type")

    if site == "NEUTRAL":
        if venue_missing:
            categories.append("neutral_missing_venue")
        if location_missing:
            categories.append("neutral_missing_location")

    if game_type in POSTSEASON_TYPES_REQUIRING_ACCOUNTING:
        if venue_missing:
            categories.append("postseason_missing_venue")
        if location_missing:
            categories.append("postseason_missing_location")

    if game_type == "NCAA_TOURNAMENT":
        if venue_missing:
            categories.append("ncaa_missing_venue")
        if location_missing:
            categories.append("ncaa_missing_location")

    return categories


def _researched_source_row(row: dict[str, str]) -> bool:
    return (
        row.get("site_research_status", "").strip().upper()
        in ALLOWED_SITE_RESEARCH_STATUSES
        and bool(row.get("site_research_basis", "").strip())
    )


def _canonical_home_venue_exception(
    game: dict[str, str],
    school_key: str,
    source_rows: list[dict[str, str]],
    all_assertions: list[dict[str, str]],
) -> bool:
    """Validate the narrow owner-approved historical HOME venue exception.

    The canonical game must remain a target HOME game with complete city/state and
    blank venue, carry an explicit canonical provenance marker, and map to at least
    one target source row that itself satisfies the dedicated research status. No
    assertion that agrees with the canonical H/A/N may already supply a curated
    venue identity; such evidence must be propagated/reconciled instead.
    """

    if not _target_home(game, school_key):
        return False
    if _venue_known(game):
        return False
    if not _complete_pair(game.get("site_city", ""), game.get("site_state", "")):
        return False
    if game.get("game_type", "").strip().upper() == "NCAA_TOURNAMENT":
        return False
    if HOME_VENUE_EXCEPTION_MARKER not in game.get("notes", ""):
        return False

    can_site = game.get("site_type", "").strip()
    qualifying_sources = [
        row
        for row in source_rows
        if researched_unresolved_home_venue(row)
        and _source_site_to_canonical(row) == can_site
    ]
    if not qualifying_sources:
        return False

    agreeing_assertions = [
        assertion
        for assertion in all_assertions
        if _source_site_to_canonical(assertion) == can_site
    ]
    if any(
        assertion.get("curated_venue_name", "").strip()
        for assertion in agreeing_assertions
    ):
        return False

    return True


_DISCREPANCY_FIELDS = {
    "site_type": {"site_type"},
    "venue": {"venue", "venue_key", "venue_id"},
    "location": {"location", "site_city", "site_state"},
}


def _review_acknowledges(
    discrepancies: list[dict[str, str]],
    kind: str,
) -> bool:
    accepted = _DISCREPANCY_FIELDS[kind]
    for row in discrepancies:
        if row.get("field_name", "").strip() not in accepted:
            continue
        status = row.get("status", "").strip().upper()
        if status == "UNDER_REVIEW":
            return True
        if status == "RESOLVED" and row.get("resolution_basis", "").strip():
            return True
    return False


def _review_accounts_for_gap(
    categories: list[str],
    discrepancies: list[dict[str, str]],
) -> bool:
    """Return True when every primitive canonical gap has explicit review provenance."""

    required_kinds: set[str] = set()
    if "unknown_site_type" in categories:
        required_kinds.add("site_type")
    if any(category.endswith("missing_venue") for category in categories):
        required_kinds.add("venue")
    if any(category.endswith("missing_location") for category in categories):
        required_kinds.add("location")
    return bool(required_kinds) and all(
        _review_acknowledges(discrepancies, kind)
        for kind in required_kinds
    )


def implementation_site_report(
    repo: Path,
    school_key: str,
    *,
    example_limit: int = 12,
) -> dict[str, Any]:
    source_path = repo / "schools" / school_key / "source-games.csv"
    programs_path = repo / "data/reference/programs.csv"
    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"
    discrepancies_path = repo / "data/reconciliation/discrepancies.csv"

    source_fields, all_sources = read_csv(source_path)
    _, programs = read_csv(programs_path)
    _, canonical = read_csv(canonical_path)
    _, assertions = read_csv(assertions_path)
    _, discrepancies = read_csv(discrepancies_path)

    program = next(
        (row for row in programs if row.get("program_key", "").strip() == school_key),
        None,
    )
    if program is None:
        raise ValueError(f"program registry has no row for {school_key}")
    history_start = program.get("history_start_season", "").strip()
    if not history_start:
        raise ValueError(f"{school_key} has no history_start_season")

    in_scope_sources = [
        row
        for row in all_sources
        if row.get("season_label", "").strip() >= history_start
    ]
    source_report = source_site_completeness_report(
        source_fields,
        in_scope_sources,
        example_limit=example_limit,
    )

    target_games = [
        row
        for row in canonical
        if school_key
        in {
            row.get("team_a_key", "").strip(),
            row.get("team_b_key", "").strip(),
        }
        and row.get("season_label", "").strip() >= history_start
    ]

    assertions_by_canonical: dict[str, list[dict[str, str]]] = defaultdict(list)
    target_source_ids_by_canonical: dict[str, list[str]] = defaultdict(list)
    for assertion in assertions:
        canonical_id = assertion.get("canonical_game_id", "").strip()
        if not canonical_id:
            continue
        assertions_by_canonical[canonical_id].append(assertion)
        if assertion.get("source_program_key", "").strip() == school_key:
            target_source_ids_by_canonical[canonical_id].append(
                assertion.get("source_game_id", "").strip()
            )

    source_by_id = {
        row.get("source_game_id", "").strip(): row
        for row in in_scope_sources
        if row.get("source_game_id", "").strip()
    }
    discrepancies_by_canonical: dict[str, list[dict[str, str]]] = defaultdict(list)
    for discrepancy in discrepancies:
        discrepancies_by_canonical[
            discrepancy.get("canonical_game_id", "").strip()
        ].append(discrepancy)

    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)

    def record(category: str, canonical_id: str) -> None:
        counts[category] += 1
        if len(examples[category]) < example_limit:
            examples[category].append(canonical_id)

    public_gap_rows = 0
    unaccounted_public_gap_rows = 0
    strict_home_gap_rows = 0
    researched_unresolved_home_venue_rows = 0
    invalid_home_venue_exception_marker_rows = 0
    strict_ncaa_gap_rows = 0

    for game in target_games:
        canonical_id = game.get("canonical_game_id", "").strip()
        game_discrepancies = discrepancies_by_canonical.get(canonical_id, [])
        categories = _canonical_gap_categories(game, school_key)
        source_rows = [
            source_by_id[source_id]
            for source_id in target_source_ids_by_canonical.get(canonical_id, [])
            if source_id in source_by_id
        ]
        all_game_assertions = assertions_by_canonical.get(canonical_id, [])
        home_exception = _canonical_home_venue_exception(
            game,
            school_key,
            source_rows,
            all_game_assertions,
        )
        marker_present = HOME_VENUE_EXCEPTION_MARKER in game.get("notes", "")

        if marker_present and not home_exception:
            invalid_home_venue_exception_marker_rows += 1
            record("invalid_home_venue_exception_marker", canonical_id)

        if categories:
            public_gap_rows += 1
            for category in categories:
                record(category, canonical_id)

            if any(category.startswith("home_missing_") for category in categories):
                if home_exception:
                    researched_unresolved_home_venue_rows += 1
                    record("researched_unresolved_home_venue", canonical_id)
                else:
                    strict_home_gap_rows += 1
                    record("strict_home_gap", canonical_id)

            research_accounted = any(_researched_source_row(row) for row in source_rows)
            review_accounted = _review_accounts_for_gap(categories, game_discrepancies)
            if not (research_accounted or review_accounted):
                unaccounted_public_gap_rows += 1
                record("unaccounted_public_gap", canonical_id)

            if any(category.startswith("ncaa_missing_") for category in categories):
                strict_ncaa_gap_rows += 1
                record("strict_ncaa_gap", canonical_id)

        can_site = game.get("site_type", "").strip()
        venue_missing = not _venue_known(game)
        location_missing = not _complete_pair(
            game.get("site_city", ""),
            game.get("site_state", ""),
        )

        # Target-source information loss is a hard implementation defect unless the
        # exact field is deliberately held under reconciliation review.
        for source_id in target_source_ids_by_canonical.get(canonical_id, []):
            source = source_by_id.get(source_id)
            if source is None:
                continue
            source_site = _source_site_to_canonical(source)
            if (
                source_site != "UNKNOWN"
                and can_site in {"", "UNKNOWN"}
                and not _review_acknowledges(game_discrepancies, "site_type")
            ):
                record("target_source_site_type_lost", canonical_id)

            site_agrees = (
                source_site != "UNKNOWN"
                and can_site != "UNKNOWN"
                and bool(can_site)
                and source_site == can_site
            )
            if (
                site_agrees
                and source.get("curated_venue_name", "").strip()
                and venue_missing
                and not _review_acknowledges(game_discrepancies, "venue")
            ):
                record("target_source_venue_lost", canonical_id)
            if (
                site_agrees
                and _complete_pair(source.get("city", ""), source.get("state", ""))
                and location_missing
                and not _review_acknowledges(game_discrepancies, "location")
            ):
                record("target_source_location_lost", canonical_id)

        # Reciprocal evidence that safely agrees with the current site classification
        # must not sit unused behind a canonical blank. Conflicting evidence belongs
        # in reconciliation and is not treated as automatic enrichment. This naturally
        # allows ordinary away-at-unpublished venue/location debt: there is no published
        # reciprocal assertion to propagate yet.
        other_assertions = [
            assertion
            for assertion in all_game_assertions
            if assertion.get("source_program_key", "").strip() != school_key
        ]
        if can_site in {"", "UNKNOWN"}:
            known_site = any(
                _source_site_to_canonical(assertion) != "UNKNOWN"
                for assertion in other_assertions
            )
            if known_site and not _review_acknowledges(game_discrepancies, "site_type"):
                record("reciprocal_site_type_unpropagated", canonical_id)
        else:
            agreeing = [
                assertion
                for assertion in other_assertions
                if _source_site_to_canonical(assertion) == can_site
            ]
            if (
                venue_missing
                and any(a.get("curated_venue_name", "").strip() for a in agreeing)
                and not _review_acknowledges(game_discrepancies, "venue")
            ):
                record("reciprocal_venue_unpropagated", canonical_id)
            if (
                location_missing
                and any(
                    _complete_pair(a.get("city", ""), a.get("state", ""))
                    for a in agreeing
                )
                and not _review_acknowledges(game_discrepancies, "location")
            ):
                record("reciprocal_location_unpropagated", canonical_id)

    errors = list(source_report["errors"])
    warnings = list(source_report["warnings"])

    loss_categories = [
        "target_source_site_type_lost",
        "target_source_venue_lost",
        "target_source_location_lost",
    ]
    reciprocal_categories = [
        "reciprocal_site_type_unpropagated",
        "reciprocal_venue_unpropagated",
        "reciprocal_location_unpropagated",
    ]
    loss_total = sum(counts[category] for category in loss_categories)
    reciprocal_total = sum(counts[category] for category in reciprocal_categories)

    if strict_home_gap_rows:
        errors.append(
            f"{strict_home_gap_rows:,} in-scope target HOME canonical game(s) are missing "
            "venue and/or complete location without a valid researched-unresolved HOME "
            "venue exception. Complete HOME location is never waivable."
        )
    if invalid_home_venue_exception_marker_rows:
        errors.append(
            f"{invalid_home_venue_exception_marker_rows:,} canonical game(s) carry a "
            "RESEARCHED_UNRESOLVED_HOME_VENUE marker without satisfying the source, "
            "location, H/A/N, NCAA, and reciprocal-evidence requirements."
        )
    if strict_ncaa_gap_rows:
        errors.append(
            f"{strict_ncaa_gap_rows:,} in-scope NCAA canonical game(s) are missing "
            "venue and/or location; NCAA site completeness is non-waivable."
        )
    if loss_total:
        details = ", ".join(
            f"{category}={counts[category]}"
            for category in loss_categories
            if counts[category]
        )
        errors.append("target source evidence was lost in the canonical result: " + details)
    if reciprocal_total:
        details = ", ".join(
            f"{category}={counts[category]}"
            for category in reciprocal_categories
            if counts[category]
        )
        errors.append(
            "safe reciprocal assertion evidence is available but remains "
            "unpropagated without a reconciliation record: " + details
        )
    if unaccounted_public_gap_rows:
        errors.append(
            f"{unaccounted_public_gap_rows:,} canonical public site-gap game(s) are "
            "not backed by explicit research-accounting metadata or field-specific "
            "reconciliation provenance."
        )

    return {
        "status": "PASS" if not errors else "FAIL",
        "school_key": school_key,
        "history_start_season": history_start,
        "errors": errors,
        "warnings": warnings,
        "counts": {
            **dict(sorted(counts.items())),
            "target_canonical_games": len(target_games),
            "public_gap_rows": public_gap_rows,
            "unaccounted_public_gap_rows": unaccounted_public_gap_rows,
            "strict_home_gap_rows": strict_home_gap_rows,
            "researched_unresolved_home_venue_rows": researched_unresolved_home_venue_rows,
            "invalid_home_venue_exception_marker_rows": invalid_home_venue_exception_marker_rows,
            "strict_ncaa_gap_rows": strict_ncaa_gap_rows,
            "target_source_information_loss": loss_total,
            "reciprocal_unpropagated": reciprocal_total,
        },
        "source_site_counts": source_report["counts"],
        "examples": {key: value for key, value in sorted(examples.items())},
    }


def print_report(report: dict[str, Any]) -> None:
    print("College Basketball History — implementation site completeness")
    print(f"School:               {report['school_key']}")
    print(f"Status:               {report['status']}")
    print(f"History start:        {report['history_start_season']}")
    print("Canonical counts:     " + json.dumps(report["counts"], sort_keys=True))
    print(
        "Source-site counts:   "
        + json.dumps(report["source_site_counts"], sort_keys=True)
    )
    if report["examples"]:
        print("Examples:             " + json.dumps(report["examples"], sort_keys=True))
    for warning in report["warnings"]:
        print("WARN: " + warning)
    if report["errors"]:
        print(f"\nFAIL ({len(report['errors'])} errors):")
        for error in report["errors"]:
            print("  - " + error)
    else:
        print(
            "\nPASS: target public canonical site coverage preserves known evidence; "
            "remaining material gaps are research-accounted, including any explicitly "
            "validated historical HOME venue unknowns."
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate post-reconciliation site completeness for one target."
    )
    parser.add_argument("school_key")
    parser.add_argument("--repo", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        report = implementation_site_report(repo, args.school_key)
    except (FileNotFoundError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    print_report(report)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
