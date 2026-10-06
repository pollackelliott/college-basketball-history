#!/usr/bin/env python3
"""Reusable site-completeness accounting for research and implementation gates.

The project deliberately prefers an explicit unknown over unsupported certainty. Most
historical site gaps may therefore remain unresolved when deliberate research is made
machine-visible. A program's own HOME venue/location is different: HOME location is
always mandatory, and HOME venue is mandatory unless exhaustive historical research
qualifies for the dedicated researched-unresolved-home-venue exception.
"""

from __future__ import annotations

import datetime as dt
import re
from collections import Counter, defaultdict
from typing import Any, Iterable


RESEARCHED_UNRESOLVED_HOME_VENUE_STATUS = "RESEARCHED_UNRESOLVED_HOME_VENUE"
ALLOWED_SITE_RESEARCH_STATUSES = {
    "RESEARCHED_PARTIAL",
    "RESEARCHED_UNRESOLVED",
    RESEARCHED_UNRESOLVED_HOME_VENUE_STATUS,
}
POSTSEASON_TYPES_REQUIRING_ACCOUNTING = {
    "CONFERENCE_TOURNAMENT",
    "NIT",
    "POSTSEASON",
}
HOME_PUBLICATION_BLOCKER_CATEGORIES = {
    "home_missing_venue",
    "home_missing_location",
    "home_missing_both",
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
    source_venue = row.get("source_venue_name", "").strip()
    venue = row.get("curated_venue_name", "").strip()
    city = row.get("city", "").strip()
    state = row.get("state", "").strip()
    location_missing = not city or not state

    categories: list[str] = []

    if site == "SOURCE_PROGRAM_HOME":
        if not venue:
            categories.append("home_missing_venue")
        if location_missing:
            categories.append("home_missing_location")
        if not venue and location_missing:
            categories.append("home_missing_both")

    if site == "OPPONENT_HOME" and source_venue:
        if not venue:
            categories.append("opponent_home_source_venue_unpreserved")
        if location_missing:
            categories.append("opponent_home_source_site_location_missing")

    if site == "UNKNOWN":
        categories.append("unknown_site_type")

    # NCAA Tournament site completeness is already a strict, non-waivable research
    # gate. Avoid treating a status marker as a substitute for that requirement.
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


def _normalize_venue_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def _season_interval(value: str) -> tuple[dt.date, dt.date] | None:
    match = re.fullmatch(r"(\d{4})-(\d{2}|\d{4})", (value or "").strip())
    if not match:
        return None
    start = int(match.group(1))
    end_token = match.group(2)
    end = (
        int(end_token)
        if len(end_token) == 4
        else (start // 100) * 100 + int(end_token)
    )
    if end != start + 1:
        return None
    return dt.date(start, 7, 1), dt.date(end, 6, 30)


def _relationship_bound(value: str, *, end: bool) -> dt.date | None:
    raw = (value or "").strip()
    if not raw:
        return None
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        pass
    season = _season_interval(raw)
    if season:
        return season[1] if end else season[0]
    if re.fullmatch(r"\d{4}", raw):
        year = int(raw)
        return dt.date(year, 12, 31) if end else dt.date(year, 1, 1)
    return None


def _game_interval(row: dict[str, str]) -> tuple[dt.date, dt.date] | None:
    raw_date = row.get("game_date", "").strip()
    if raw_date:
        try:
            game_date = dt.date.fromisoformat(raw_date)
        except ValueError:
            pass
        else:
            return game_date, game_date
    return _season_interval(row.get("season_label", ""))


def _home_relationship_supports_game(
    venue: dict[str, str],
    game: dict[str, str],
) -> bool:
    relationship = venue.get("relationship_type", "").strip().casefold()
    if "home" not in relationship:
        return False

    game_interval = _game_interval(game)
    if game_interval is None:
        # Missing/ambiguous dates cannot prove a chronology contradiction.
        return True

    relation_start = _relationship_bound(
        venue.get("relationship_start", ""), end=False
    )
    relation_end = _relationship_bound(
        venue.get("relationship_end", ""), end=True
    )
    game_start, game_end = game_interval
    if relation_start and game_end < relation_start:
        return False
    if relation_end and game_start > relation_end:
        return False
    return True


def source_home_chronology_report(
    games: Iterable[dict[str, str]],
    venues: Iterable[dict[str, str]],
    *,
    school_key: str,
    example_limit: int = 25,
) -> dict[str, Any]:
    """Challenge exact HOME venues against documented HOME relationships.

    This is an adversarial signal only. It never infers or rewrites H/A/N from
    geography, venue identity, or opponent identity. A legitimate alternate or
    temporary HOME site should be represented by a dated venue relationship whose
    relationship_type contains the word home.
    """

    game_rows = list(games)
    venue_rows = list(venues)
    chronology_rows = [
        row
        for row in venue_rows
        if row.get("source_program_key", "").strip() in {"", school_key}
        and "home" in row.get("relationship_type", "").strip().casefold()
    ]
    warnings: list[str] = []
    if not chronology_rows:
        warnings.append(
            "venues.csv has no documented HOME relationship chronology; exact "
            "SOURCE_PROGRAM_HOME venue chronology challenge skipped for legacy "
            "compatibility"
        )
        return {
            "errors": [],
            "warnings": warnings,
            "counts": {
                "chronology_rows": 0,
                "home_rows_checked": 0,
                "home_chronology_conflicts": 0,
            },
            "conflict_examples": [],
        }

    by_name: dict[str, list[dict[str, str]]] = defaultdict(list)
    for venue in venue_rows:
        names = [venue.get("canonical_name", "")]
        names.extend(venue.get("aliases", "").split(";"))
        for name in names:
            normalized = _normalize_venue_name(name)
            if normalized:
                by_name[normalized].append(venue)

    checked = 0
    conflict_count = 0
    conflicts: list[dict[str, str]] = []
    for row in game_rows:
        if row.get("curated_site_type", "").strip().upper() != "SOURCE_PROGRAM_HOME":
            continue
        venue_name = row.get("curated_venue_name", "").strip()
        if not venue_name:
            continue
        candidates = by_name.get(_normalize_venue_name(venue_name), [])
        if not candidates:
            # The general research acceptance gate separately rejects an unknown
            # curated venue identity. Do not duplicate that error here.
            continue
        checked += 1
        if any(_home_relationship_supports_game(venue, row) for venue in candidates):
            continue
        conflict_count += 1
        if len(conflicts) < example_limit:
            conflicts.append(
                {
                    "source_game_id": row.get("source_game_id", "").strip(),
                    "season_label": row.get("season_label", "").strip(),
                    "game_date": row.get("game_date", "").strip(),
                    "curated_venue_name": venue_name,
                }
            )

    errors: list[str] = []
    if conflict_count:
        rendered = "; ".join(
            f"{item['source_game_id'] or '[unknown id]'} "
            f"({item['game_date'] or item['season_label'] or 'date unknown'}: "
            f"{item['curated_venue_name']})"
            for item in conflicts
        )
        errors.append(
            f"{conflict_count:,} SOURCE_PROGRAM_HOME row(s) use an exact venue "
            "not supported by the documented source-program HOME relationship "
            "chronology. This is an adversarial review signal only: do not infer "
            "H/A/N from geography. Correct H/A/N from accepted historical evidence "
            "or document the venue as a supported HOME relationship/exception in "
            f"venues.csv. Examples: {rendered}"
        )

    return {
        "errors": errors,
        "warnings": warnings,
        "counts": {
            "chronology_rows": len(chronology_rows),
            "home_rows_checked": checked,
            "home_chronology_conflicts": conflict_count,
        },
        "conflict_examples": conflicts,
    }


def researched_unresolved_home_venue(row: dict[str, str]) -> bool:
    """Return True only for the owner-approved historical HOME venue exception.

    This exception is deliberately field-specific: HOME H/A/N and complete city/state
    must already be established, the curated venue must remain blank, the dedicated
    status and a research basis must be present, and NCAA Tournament rows are excluded.
    Reciprocal/target evidence checks are performed later by the implementation gate.
    """

    return (
        row.get("curated_site_type", "").strip().upper() == "SOURCE_PROGRAM_HOME"
        and not row.get("curated_venue_name", "").strip()
        and bool(row.get("city", "").strip())
        and bool(row.get("state", "").strip())
        and row.get("site_research_status", "").strip().upper()
        == RESEARCHED_UNRESOLVED_HOME_VENUE_STATUS
        and bool(row.get("site_research_basis", "").strip())
        and row.get("curated_game_type", "").strip().upper() != "NCAA_TOURNAMENT"
    )


def source_site_completeness_report(
    game_fields: Iterable[str],
    games: Iterable[dict[str, str]],
    *,
    example_limit: int = 12,
) -> dict[str, Any]:
    """Return machine-readable source-side site coverage and freeze blockers.

    A material gap is one of:

    - source-program HOME missing venue and/or location;
    - OPPONENT_HOME rows that already carry explicit source venue evidence but
      silently drop the curated venue and/or normalized locality;
    - UNKNOWN H/A/N;
    - non-NCAA NEUTRAL missing venue and/or location;
    - conference-tournament, NIT, or generic POSTSEASON missing venue/location.

    Ordinary away regular-season blanks remain outside source-school research
    responsibility. Only already-present source venue evidence activates the
    OPPONENT_HOME preservation accounting here; this does not require opponent-home
    archaeology. NCAA Tournament rows remain governed by the stricter non-waivable
    NCAA gate.

    Research metadata may account for most material gaps. A HOME location gap is never
    waivable. A HOME venue-only gap is waivable only through the dedicated
    RESEARCHED_UNRESOLVED_HOME_VENUE status after exhaustive research.
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
    home_publication_blocker_rows = 0
    researched_unresolved_home_venue_rows = 0
    invalid_status_rows: list[str] = []
    missing_basis_rows: list[str] = []
    orphan_basis_rows: list[str] = []
    invalid_home_exception_rows: list[str] = []
    unnecessary_status_rows: list[str] = []
    unaccounted_examples: list[dict[str, Any]] = []
    home_blocker_examples: list[dict[str, Any]] = []
    home_exception_examples: list[dict[str, Any]] = []

    for line_number, row in enumerate(rows, start=2):
        source_game_id = row.get("source_game_id", "").strip() or f"line {line_number}"
        season = row.get("season_label", "").strip()
        categories = _row_gap_categories(row)
        status = row.get("site_research_status", "").strip().upper()
        basis = row.get("site_research_basis", "").strip()
        home_exception = researched_unresolved_home_venue(row)

        if status and status not in ALLOWED_SITE_RESEARCH_STATUSES:
            invalid_status_rows.append(source_game_id)
        if status and not basis:
            missing_basis_rows.append(source_game_id)
        if basis and not status:
            orphan_basis_rows.append(source_game_id)
        if status == RESEARCHED_UNRESOLVED_HOME_VENUE_STATUS and not home_exception:
            invalid_home_exception_rows.append(source_game_id)

        if not categories:
            if status or basis:
                unnecessary_status_rows.append(source_game_id)
            continue

        material_gap_rows += 1
        for category in categories:
            category_counts[category] += 1
            decade_counts[category][_season_decade(season)] += 1
            season_counts[category][season or "UNKNOWN"] += 1

        has_home_gap = any(
            category in HOME_PUBLICATION_BLOCKER_CATEGORIES for category in categories
        )
        if has_home_gap and home_exception:
            researched_unresolved_home_venue_rows += 1
            if len(home_exception_examples) < example_limit:
                home_exception_examples.append(
                    {
                        "source_game_id": source_game_id,
                        "season_label": season,
                        "categories": sorted(
                            category
                            for category in categories
                            if category in HOME_PUBLICATION_BLOCKER_CATEGORIES
                        ),
                    }
                )
        elif has_home_gap:
            home_publication_blocker_rows += 1
            if len(home_blocker_examples) < example_limit:
                home_blocker_examples.append(
                    {
                        "source_game_id": source_game_id,
                        "season_label": season,
                        "categories": sorted(
                            category
                            for category in categories
                            if category in HOME_PUBLICATION_BLOCKER_CATEGORIES
                        ),
                    }
                )

        accounted = status in ALLOWED_SITE_RESEARCH_STATUSES and bool(basis)
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
            "RESEARCHED_PARTIAL, RESEARCHED_UNRESOLVED, and "
            "RESEARCHED_UNRESOLVED_HOME_VENUE; examples: "
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
    if invalid_home_exception_rows:
        errors.append(
            "RESEARCHED_UNRESOLVED_HOME_VENUE is valid only for a SOURCE_PROGRAM_HOME "
            "row with blank curated venue, complete city/state, nonblank research basis, "
            "and non-NCAA game type; "
            f"{len(invalid_home_exception_rows):,} row(s) violate that shape; examples: "
            + ", ".join(invalid_home_exception_rows[:example_limit])
        )
    if home_publication_blocker_rows:
        rendered = "; ".join(
            f"{item['source_game_id']} ({item['season_label'] or 'season unknown'}: "
            + ", ".join(item["categories"])
            + ")"
            for item in home_blocker_examples
        )
        errors.append(
            f"{home_publication_blocker_rows:,} source-program HOME row(s) are missing "
            "venue and/or complete location without a valid historical-unrecoverable "
            "venue exception. Complete location is always mandatory; ordinary "
            "RESEARCHED_PARTIAL/RESEARCHED_UNRESOLVED cannot waive HOME completeness. "
            f"Examples: {rendered}"
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
            "home_publication_blocker_rows": home_publication_blocker_rows,
            "researched_unresolved_home_venue_rows": researched_unresolved_home_venue_rows,
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
        "home_publication_blocker_examples": home_blocker_examples,
        "researched_unresolved_home_venue_examples": home_exception_examples,
    }
