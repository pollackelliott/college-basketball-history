#!/usr/bin/env python3
# Permanent NCAA Tournament venue/location and historical-round safety rules.

from __future__ import annotations

import csv
from pathlib import Path


NCAA_GAME_TYPE = "NCAA_TOURNAMENT"
FIRST_R64_SEASON = "1978-1979"

NCAA_SITE_FIELDS = (
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
)

REQUIRED_NCAA_EVIDENCE_COLUMNS = {
    "canonical_game_id",
    "venue_id",
    "venue_key",
    "site_city",
    "site_state",
    "source_authority",
    "source_index_url",
    "source_document_title",
    "source_document_url",
    "source_locator",
    "source_scope",
    "resolution_basis",
    "notes",
}


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.is_file():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def canonical_ncaa_errors(
    canonical_rows: list[dict[str, str]],
    global_venues_by_id: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []

    for row in canonical_rows:
        if row.get("game_type", "").strip() != NCAA_GAME_TYPE:
            continue

        game_id = row.get("canonical_game_id", "").strip() or "[unknown game]"
        missing = [
            field
            for field in NCAA_SITE_FIELDS
            if not row.get(field, "").strip()
        ]
        if missing:
            errors.append(
                f"{game_id}: NCAA Tournament site is incomplete; missing "
                + ", ".join(missing)
            )
            continue

        venue_id = row.get("venue_id", "").strip()
        global_venue = global_venues_by_id.get(venue_id)
        if global_venue is None:
            errors.append(
                f"{game_id}: NCAA Tournament venue_id {venue_id!r} is absent "
                "from the global venue registry"
            )
        else:
            actual_geo = (
                row.get("site_city", "").strip(),
                row.get("site_state", "").strip(),
            )
            expected_geo = (
                global_venue.get("city", "").strip(),
                global_venue.get("state", "").strip(),
            )
            if actual_geo != expected_geo:
                errors.append(
                    f"{game_id}: NCAA Tournament geography "
                    f"{actual_geo[0]!r}, {actual_geo[1]!r} disagrees with "
                    f"venue_id {venue_id} global geography "
                    f"{expected_geo[0]!r}, {expected_geo[1]!r}"
                )

        if (
            row.get("postseason_round", "").strip() == "R64"
            and row.get("season_label", "").strip() < FIRST_R64_SEASON
        ):
            errors.append(
                f"{game_id}: NCAA Tournament R64 is invalid before "
                f"{FIRST_R64_SEASON}"
            )

    return errors


def ncaa_evidence_errors(
    repo_root: Path,
    canonical_rows: list[dict[str, str]],
    global_venues_by_id: dict[str, dict[str, str]],
) -> list[str]:
    path = repo_root / "data" / "evidence" / "ncaa-tournament-sites.csv"
    try:
        columns, evidence_rows = _read_csv(path)
    except FileNotFoundError:
        return ["data/evidence/ncaa-tournament-sites.csv is required"]

    errors: list[str] = []
    missing_columns = sorted(REQUIRED_NCAA_EVIDENCE_COLUMNS - set(columns))
    if missing_columns:
        return [
            "data/evidence/ncaa-tournament-sites.csv is missing required columns: "
            + ", ".join(missing_columns)
        ]

    canonical_by_id = {
        row.get("canonical_game_id", "").strip(): row
        for row in canonical_rows
        if row.get("canonical_game_id", "").strip()
    }

    seen: set[str] = set()
    for line_number, row in enumerate(evidence_rows, start=2):
        game_id = row.get("canonical_game_id", "").strip()
        label = game_id or f"line {line_number}"

        if not game_id:
            errors.append(f"{label}: NCAA evidence canonical_game_id is required")
            continue
        if game_id in seen:
            errors.append(f"{game_id}: duplicate NCAA site evidence row")
            continue
        seen.add(game_id)

        if row.get("source_authority", "").strip() != "NCAA":
            errors.append(f"{game_id}: NCAA evidence source_authority must be NCAA")

        for field in (
            "source_index_url",
            "source_document_title",
            "source_document_url",
            "source_locator",
            "source_scope",
            "resolution_basis",
        ):
            if not row.get(field, "").strip():
                errors.append(f"{game_id}: NCAA evidence {field} is required")

        canonical = canonical_by_id.get(game_id)
        if canonical is None:
            errors.append(f"{game_id}: NCAA evidence references missing canonical game")
            continue
        if canonical.get("game_type", "").strip() != NCAA_GAME_TYPE:
            errors.append(f"{game_id}: NCAA evidence target is not NCAA_TOURNAMENT")

        for field in NCAA_SITE_FIELDS:
            evidence_value = row.get(field, "").strip()
            canonical_value = canonical.get(field, "").strip()
            if not evidence_value:
                errors.append(f"{game_id}: NCAA evidence {field} is required")
            elif evidence_value != canonical_value:
                errors.append(
                    f"{game_id}: NCAA evidence {field}={evidence_value!r} "
                    f"does not match canonical {canonical_value!r}"
                )

        venue_id = row.get("venue_id", "").strip()
        global_venue = global_venues_by_id.get(venue_id)
        if global_venue is None:
            errors.append(
                f"{game_id}: NCAA evidence venue_id {venue_id!r} is absent "
                "from the global venue registry"
            )
            continue

        evidence_geo = (
            row.get("site_city", "").strip(),
            row.get("site_state", "").strip(),
        )
        global_geo = (
            global_venue.get("city", "").strip(),
            global_venue.get("state", "").strip(),
        )
        if evidence_geo != global_geo:
            errors.append(
                f"{game_id}: NCAA evidence geography {evidence_geo} does not "
                f"match global venue geography {global_geo}"
            )

        global_key = global_venue.get("venue_key", "").strip()
        if row.get("venue_key", "").strip() != global_key:
            errors.append(
                f"{game_id}: NCAA evidence venue_key "
                f"{row.get('venue_key', '').strip()!r} does not match global "
                f"venue_key {global_key!r}"
            )

    return errors
