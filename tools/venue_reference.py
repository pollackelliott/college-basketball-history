#!/usr/bin/env python3
"""Global physical-venue identity helpers."""

from __future__ import annotations

import csv
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

RETIRED_VENUE_IDS = {"VEN-000075", "VEN-000207"}

REQUIRED_VENUE_COLUMNS = {
    "venue_id", "venue_key", "display_name", "city", "state",
    "opened", "closed", "date_precision", "identity_status",
    "source_basis", "notes",
}

REQUIRED_NAME_COLUMNS = {
    "venue_id", "venue_name", "normalized_name", "name_type",
    "valid_from", "valid_to", "date_precision", "source_basis", "notes",
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    if not path.exists():
        raise FileNotFoundError(path)
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return (reader.fieldnames or []), list(reader)


def normalized_venue_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def load_global_venue_reference(
    repo_root: Path,
) -> tuple[
    dict[str, dict[str, str]],
    dict[str, dict[str, str]],
    dict[str, set[str]],
]:
    venue_path = repo_root / "data/reference/venues.csv"
    names_path = repo_root / "data/reference/venue-names.csv"

    venue_columns, venue_rows = read_csv(venue_path)
    name_columns, name_rows = read_csv(names_path)

    missing = sorted(REQUIRED_VENUE_COLUMNS - set(venue_columns))
    if missing:
        raise ValueError("venues.csv missing columns: " + ", ".join(missing))

    missing = sorted(REQUIRED_NAME_COLUMNS - set(name_columns))
    if missing:
        raise ValueError("venue-names.csv missing columns: " + ", ".join(missing))

    ids = [row.get("venue_id", "").strip() for row in venue_rows]
    keys = [row.get("venue_key", "").strip() for row in venue_rows]

    if "" in ids or len(ids) != len(set(ids)):
        raise ValueError("venues.csv has blank or duplicate venue_id")
    if "" in keys or len(keys) != len(set(keys)):
        raise ValueError("venues.csv has blank or duplicate venue_key")

    reused = sorted(set(ids) & RETIRED_VENUE_IDS)
    if reused:
        raise ValueError("retired venue_id reused: " + ", ".join(reused))

    venues_by_id = {row["venue_id"].strip(): row for row in venue_rows}
    venues_by_key = {row["venue_key"].strip(): row for row in venue_rows}

    name_ids: dict[str, set[str]] = defaultdict(set)
    display_counts = Counter()

    for line_number, row in enumerate(name_rows, start=2):
        venue_id = row.get("venue_id", "").strip()
        name = row.get("venue_name", "").strip()

        if venue_id not in venues_by_id:
            raise ValueError(
                f"venue-names.csv line {line_number}: unknown venue_id {venue_id!r}"
            )
        if not name:
            raise ValueError(
                f"venue-names.csv line {line_number}: venue_name is required"
            )

        expected = normalized_venue_name(name)
        if row.get("normalized_name", "").strip() != expected:
            raise ValueError(
                f"venue-names.csv line {line_number}: normalized_name drift"
            )

        name_ids[expected].add(venue_id)

        if row.get("name_type", "").strip() == "PROJECT_DISPLAY":
            display_counts[venue_id] += 1
            if name != venues_by_id[venue_id].get("display_name", "").strip():
                raise ValueError(
                    f"{venue_id}: PROJECT_DISPLAY does not match display_name"
                )

    for venue_id, row in venues_by_id.items():
        if display_counts[venue_id] != 1:
            raise ValueError(
                f"{venue_id}: expected exactly one PROJECT_DISPLAY row; "
                f"found {display_counts[venue_id]}"
            )
        display_name = row.get("display_name", "").strip()
        city = row.get("city", "").strip()
        state = row.get("state", "").strip()
        if not display_name or not city or not state:
            raise ValueError(
                f"{venue_id}: display_name and complete geography are required"
            )
        if display_name.casefold() == city.casefold():
            raise ValueError(
                f"{venue_id}: display_name must identify a venue, not merely its city"
            )

    return venues_by_id, venues_by_key, name_ids


def canonical_venue_geography_errors(
    canonical_rows: list[dict[str, str]],
    venues_by_id: dict[str, dict[str, str]],
) -> list[str]:
    # Require canonical city/state to agree with physical venue identity.
    # This validates geography only; it never establishes or modifies H/A/N.
    errors: list[str] = []

    for row in canonical_rows:
        venue_id = row.get("venue_id", "").strip()
        if not venue_id:
            continue

        game_id = row.get("canonical_game_id", "").strip() or "[unknown game]"
        venue = venues_by_id.get(venue_id)
        if venue is None:
            errors.append(
                f"{game_id}: venue_id {venue_id!r} is absent from global venues.csv"
            )
            continue

        actual = (
            row.get("site_city", "").strip(),
            row.get("site_state", "").strip(),
        )
        expected = (
            venue.get("city", "").strip(),
            venue.get("state", "").strip(),
        )
        if actual != expected:
            errors.append(
                f"{game_id}: canonical geography {actual[0]!r}, {actual[1]!r} "
                f"does not match venue_id {venue_id} global geography "
                f"{expected[0]!r}, {expected[1]!r}"
            )

    return errors


def school_venue_reference_errors(
    venue_path: Path,
    rows: list[dict[str, str]],
    venues_by_id: dict[str, dict[str, str]],
    name_ids: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []

    for line_number, row in enumerate(rows, start=2):
        key = row.get("venue_key", "").strip()
        venue_id = row.get("venue_id", "").strip()

        if key and not venue_id:
            errors.append(
                f"line {line_number}: venue_key {key!r} requires venue_id"
            )
            continue
        if venue_id and venue_id not in venues_by_id:
            errors.append(
                f"line {line_number}: unknown venue_id {venue_id!r}"
            )
            continue
        if not venue_id:
            continue

        names = [row.get("canonical_name", "").strip()]
        names.extend(
            alias.strip()
            for alias in row.get("aliases", "").split(";")
            if alias.strip()
        )

        for name in names:
            if not name:
                continue
            if venue_id not in name_ids.get(normalized_venue_name(name), set()):
                errors.append(
                    f"line {line_number}: name/alias {name!r} is not "
                    f"registered to {venue_id}"
                )

    return errors
