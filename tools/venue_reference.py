#!/usr/bin/env python3
"""Global physical-venue identity helpers."""

from __future__ import annotations

import calendar
import csv
import datetime as dt
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

RETIRED_VENUE_IDS = {"VEN-000075", "VEN-000207", "VEN-000407", "VEN-000409", "VEN-000410", "VEN-000476", "VEN-000680", "VEN-000682", "VEN-000686"}

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



def _registry_venue_boundary(value: str, *, end: bool) -> dt.date | None:
    """Parse only stated YEAR/MONTH/DAY physical bounds, never guess an era."""
    value = (value or "").strip()
    if not value:
        return None
    try:
        if re.fullmatch(r"\d{4}", value):
            year = int(value)
            return dt.date(year, 12 if end else 1, 31 if end else 1)
        if re.fullmatch(r"\d{4}-\d{2}", value):
            year, month = map(int, value.split("-"))
            return dt.date(year, month, calendar.monthrange(year, month)[1] if end else 1)
        return dt.date.fromisoformat(value)
    except ValueError:
        return None


def registered_opponent_home_venue(
    source: dict[str, str],
    local_venues: list[dict[str, str]],
    global_venues_by_id: dict[str, dict[str, str]],
    global_name_ids: dict[str, set[str]],
) -> dict[str, str] | None:
    """Resolve an explicitly researched opponent-host site already registered globally.

    An opponent's facility need not be copied into every visiting school's
    local venue relationship list. This lookup never establishes H/A/N, never
    infers a building from geography, and does not alter frozen source data.
    Name *and* complete locality must identify exactly one registered physical
    identity, with an exact game date respecting every stated physical bound.
    A local name relationship, whether valid or conflicting, always takes
    precedence and must pass the existing local-name resolver.
    """
    if source.get("curated_site_type", "").strip() != "OPPONENT_HOME":
        return None
    if (
        not source.get("source_program_key", "").strip()
        or not source.get("normalized_opponent_key", "").strip()
        or source["source_program_key"].strip() == source["normalized_opponent_key"].strip()
    ):
        return None
    raw_name = source.get("curated_venue_name", "").strip()
    city = source.get("city", "").strip()
    state = source.get("state", "").strip()
    if not raw_name or not city or not state:
        return None
    try:
        game_date = dt.date.fromisoformat(source.get("game_date", "").strip())
    except ValueError:
        return None

    name = normalized_venue_name(raw_name)
    if not name:
        return None
    for local in local_venues:
        local_names = [local.get("canonical_name", "")]
        local_names.extend(local.get("aliases", "").split(";"))
        if any(normalized_venue_name(value.strip()) == name for value in local_names if value.strip()):
            return None

    possibilities: list[dict[str, str]] = []
    for venue_id in sorted(global_name_ids.get(name, set())):
        identity = global_venues_by_id.get(venue_id)
        if identity is None:
            return None
        if (
            identity.get("city", "").strip().casefold() != city.casefold()
            or identity.get("state", "").strip().upper() != state.upper()
        ):
            continue
        opened = identity.get("opened", "").strip()
        closed = identity.get("closed", "").strip()
        start = _registry_venue_boundary(opened, end=False)
        finish = _registry_venue_boundary(closed, end=True)
        # A matching registered identity with impossible/unknown stated
        # chronology cannot be silently discarded in favor of another.
        if (opened and start is None) or (closed and finish is None):
            return None
        if (start is not None and game_date < start) or (
            finish is not None and game_date > finish
        ):
            return None
        if not identity.get("venue_key", "").strip() or not identity.get("venue_id", "").strip():
            return None
        possibilities.append(identity)
    return possibilities[0] if len(possibilities) == 1 else None

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



def _verified_distinct_historical_local_alias(
    local: dict[str, str],
    physical: dict[str, str],
    alias: str,
    venues_by_id: dict[str, dict[str, str]],
    name_ids: dict[str, set[str]],
) -> bool:
    """Permit a source-school historical alias *without* a second global alias.

    A documented former facility may have the exact historical label now
    registered to a distinct newer physical building on the same campus.
    Registering that bare name to two VEN IDs would reintroduce ambiguous
    physical-site matching. This is not a name-to-identity inference: the
    original keyed venue must already be globally registered, its *canonical*
    name must remain registered, and complete facility/relationship chronology
    must independently prove that the later same-locality identity cannot have
    hosted the older relationship. Missing evidence fails closed.
    """

    def year(value: str) -> int | None:
        s = (value or "").strip()
        return int(s) if re.fullmatch(r"\d{4}", s) else None

    def season(value: str) -> tuple[int, int] | None:
        m = re.fullmatch(r"(\d{4})-(\d{4})", (value or "").strip())
        if not m:
            return None
        start, end = int(m[1]), int(m[2])
        return (start, end) if end == start + 1 else None

    def locality(value: dict[str, str]) -> tuple[str, str]:
        return (
            (value.get("city") or "").strip().casefold(),
            (value.get("state") or "").strip().upper(),
        )

    venue_id = local.get("venue_id", "").strip()
    if (
        not venue_id or physical.get("venue_id", "").strip() != venue_id
        or physical.get("venue_key", "").strip() != local.get("venue_key", "").strip()
        or not all(locality(local)) or locality(local) != locality(physical)
        or not local.get("source_basis", "").strip()
        or not local.get("site_rule", "").strip()
        or not local.get("notes", "").strip()
        or not physical.get("source_basis", "").strip()
    ):
        return False

    canonical = normalized_venue_name(local.get("canonical_name", ""))
    normalized_alias = normalized_venue_name(alias)
    if (
        not canonical or canonical == normalized_alias
        or venue_id not in name_ids.get(canonical, set())
    ):
        return False

    closed = year(local.get("known_closed", ""))
    registered_closed = year(physical.get("closed", ""))
    start = season(local.get("relationship_start", ""))
    end = season(local.get("relationship_end", ""))
    if (
        closed is None or registered_closed != closed
        or start is None or end is None
        or start[0] > end[0] or end[1] > closed
    ):
        return False
    older_opened = year(local.get("known_opened", ""))
    if older_opened is not None and older_opened > start[0]:
        return False
    if local.get("known_opened", "").strip() and older_opened is None:
        return False

    # Only one *other* building in the same complete locality may own this
    # historical alias. Different-city name homonyms convey no identity.
    same_locality = [
        row for candidate_id in name_ids.get(normalized_alias, set())
        if candidate_id != venue_id
        for row in [venues_by_id.get(candidate_id)]
        if row is not None and locality(row) == locality(local)
    ]
    if len(same_locality) != 1:
        return False
    newer = same_locality[0]
    newer_opened = year(newer.get("opened", ""))
    return (
        bool(newer.get("venue_key", "").strip())
        and bool(newer.get("source_basis", "").strip())
        and normalized_venue_name(newer.get("display_name", "")) != normalized_alias
        and newer_opened is not None
        and closed < newer_opened
        and end[1] < newer_opened
    )

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

        physical = venues_by_id[venue_id]
        for name_index, name in enumerate(names):
            if not name:
                continue
            if venue_id not in name_ids.get(normalized_venue_name(name), set()):
                if name_index > 0 and _verified_distinct_historical_local_alias(
                    row, physical, name, venues_by_id, name_ids
                ):
                    continue
                errors.append(
                    f"line {line_number}: name/alias {name!r} is not "
                    f"registered to {venue_id}"
                )

    return errors
