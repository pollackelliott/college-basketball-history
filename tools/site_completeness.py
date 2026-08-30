#!/usr/bin/env python3
"""Reusable site-completeness accounting for research and implementation gates.

The project deliberately prefers an explicit unknown over unsupported certainty.  This
module therefore does not require every historical venue/location to be known.  It
requires material source-side gaps to be visible, deliberately researched, and
explained before a portfolio may be treated as research-frozen.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from typing import Any, Iterable


ALLOWED_SITE_RESEARCH_STATUSES = {
    "RESEARCHED_PARTIAL",
    "RESEARCHED_UNRESOLVED",
}
POSTSEASON_TYPES_REQUIRING_ACCOUNTING = {
    "CONFERENCE_TOURNAMENT",
    "NIT",
    "POSTSEASON",
}


def _season_decade(season_label: str) -> str:
    match = re.match(r"(\d{4})-", season_label or "")
    if not match:
        return "UNKNOWN"
    start_year = int(match.group(1))
    return f"{start_year // 10 * 10}s"


def _row_gap_categories(row: dict[str, str]) -> list[str]:
    site = row.get("curated_site_type", "").strip().upper()
    game_type = row.get("curated_game_type", "").strip().upper()
    venue = row.get("curated_venue_name", "").strip()
    city = row.get("city", "").strip()
    state = row.get("state", "").strip()
    location_missing = not city and not state

    categories: list[str] = []

    if site == "SOURCE_PROGRAM_HOME":
        if not venue:
            categories.append("home_missing_venue")
        if location_missing:
            categories.append("home_missing_location")
        if not venue and location_missing:
            categories.append("home_missing_both")

    if site == "UNKNOWN":
        categories.append("unknown_site_type")

    # NCAA Tournament site completeness is already a strict, non-waivable research
    # gate.  Avoid treating a status marker as a substitute for that requirement.
    if game_type != "NCAA_TOURNAMENT" and site == "NEUTRAL":
        if not venue:
            categories.append("neutral_missing_venue")
        if location_missing:
            categories.append("neutral_missing_location")

    if game_type in POSTSEASON_TYPES_REQUIRING_ACCOUNTING:
        if not venue:
            categories.append("postseason_missing_venue")
        if location_missing:
            categories.append("postseason_missing_location")

    return categories


def source_site_completeness_report(
    game_fields: Iterable[str],
    games: Iterable[dict[str, str]],
    *,
    example_limit: int = 12,
) -> dict[str, Any]:
    """Return machine-readable source-side site coverage and freeze blockers.

    A material gap is one of:

    - source-program HOME missing venue and/or location;
    - UNKNOWN H/A/N;
    - non-NCAA NEUTRAL missing venue and/or location;
    - conference-tournament, NIT, or generic POSTSEASON missing venue/location.

    Away regular-season rows are intentionally not research-freeze blockers here: a
    school's own research lane is not required to reconstruct every opponent building.
    NCAA Tournament rows remain governed by the stricter non-waivable NCAA gate.
    """

    fields = set(game_fields)
    rows = list(games)
    has_status = "site_research_status" in fields
    has_basis = "site_research_basis" in fields

    errors: list[str] = []
    warnings: list[str] = []
    if has_status != has_basis:
        errors.append(
            "source-games.csv must contain both site_research_status and "
            "site_research_basis when either site-research column is present"
        )

    category_counts: Counter[str] = Counter()
    decade_counts: dict[str, Counter[str]] = defaultdict(Counter)
    season_counts: dict[str, Counter[str]] = defaultdict(Counter)
    material_gap_rows = 0
    researched_gap_rows = 0
    unaccounted_gap_rows = 0
    invalid_status_rows: list[str] = []
    missing_basis_rows: list[str] = []
    orphan_basis_rows: list[str] = []
    unnecessary_status_rows: list[str] = []
    unaccounted_examples: list[dict[str, Any]] = []

    for line_number, row in enumerate(rows, start=2):
        source_game_id = row.get("source_game_id", "").strip() or f"line {line_number}"
        season = row.get("season_label", "").strip()
        categories = _row_gap_categories(row)
        status = row.get("site_research_status", "").strip().upper()
        basis = row.get("site_research_basis", "").strip()

        if status and status not in ALLOWED_SITE_RESEARCH_STATUSES:
            invalid_status_rows.append(source_game_id)
        if status and not basis:
            missing_basis_rows.append(source_game_id)
        if basis and not status:
            orphan_basis_rows.append(source_game_id)

        if not categories:
            if status or basis:
                unnecessary_status_rows.append(source_game_id)
            continue

        material_gap_rows += 1
        for category in categories:
            category_counts[category] += 1
            decade_counts[category][_season_decade(season)] += 1
            season_counts[category][season or "UNKNOWN"] += 1

        accounted = (
            status in ALLOWED_SITE_RESEARCH_STATUSES
            and bool(basis)
        )
        if accounted:
            researched_gap_rows += 1
        else:
            unaccounted_gap_rows += 1
            if len(unaccounted_examples) < example_limit:
                unaccounted_examples.append(
                    {
                        "source_game_id": source_game_id,
                        "season_label": season,
                        "categories": sorted(categories),
                    }
                )

    if invalid_status_rows:
        errors.append(
            "invalid site_research_status on "
            f"{len(invalid_status_rows):,} row(s); allowed values are "
            "RESEARCHED_PARTIAL and RESEARCHED_UNRESOLVED; examples: "
            + ", ".join(invalid_status_rows[:example_limit])
        )
    if missing_basis_rows:
        errors.append(
            "site_research_basis is required when site_research_status is populated; "
            f"{len(missing_basis_rows):,} row(s) affected; examples: "
            + ", ".join(missing_basis_rows[:example_limit])
        )
    if orphan_basis_rows:
        errors.append(
            "site_research_status is required when site_research_basis is populated; "
            f"{len(orphan_basis_rows):,} row(s) affected; examples: "
            + ", ".join(orphan_basis_rows[:example_limit])
        )
    if unaccounted_gap_rows:
        rendered = "; ".join(
            f"{item['source_game_id']} ({item['season_label'] or 'season unknown'}: "
            + ", ".join(item["categories"])
            + ")"
            for item in unaccounted_examples
        )
        errors.append(
            f"{unaccounted_gap_rows:,} material site-gap row(s) are not "
            "research-accounted. Resolve the site data or populate both "
            "site_research_status and site_research_basis after deliberate research. "
            f"Examples: {rendered}"
        )
    if unnecessary_status_rows:
        warnings.append(
            "site-research metadata is populated on rows with no material site gap; "
            f"{len(unnecessary_status_rows):,} row(s) affected; examples: "
            + ", ".join(unnecessary_status_rows[:example_limit])
        )

    return {
        "errors": errors,
        "warnings": warnings,
        "counts": {
            **dict(sorted(category_counts.items())),
            "material_gap_rows": material_gap_rows,
            "researched_gap_rows": researched_gap_rows,
            "unaccounted_gap_rows": unaccounted_gap_rows,
        },
        "by_decade": {
            category: dict(sorted(counts.items()))
            for category, counts in sorted(decade_counts.items())
        },
        "by_season": {
            category: dict(sorted(counts.items()))
            for category, counts in sorted(season_counts.items())
        },
        "unaccounted_examples": unaccounted_examples,
    }
