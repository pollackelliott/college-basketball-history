#!/usr/bin/env python3
"""Protected-main authority for exact researched HOME locality exceptions.

Ordinary source-program HOME rows still require complete city/state. This module
recognizes only exact owner-authorized rows recorded in the protected-main registry.
A school package cannot create its own waiver by writing a status string or note.
"""

from __future__ import annotations

import csv
import re
from functools import lru_cache
from pathlib import Path


RESEARCHED_UNRESOLVED_HOME_LOCATION_STATUS = "RESEARCHED_UNRESOLVED_HOME_LOCATION"
HOME_LOCATION_EXCEPTION_MARKER = "[RESEARCHED_UNRESOLVED_HOME_LOCATION"
REGISTRY_RELATIVE_PATH = Path("data/reference/research-home-location-exceptions.csv")
_HASH_RE = re.compile(r"^[0-9a-f]{64}$")

_REQUIRED_FIELDS = {
    "school_key",
    "authority_checkpoint_sha256",
    "authority_ledger_sha256",
    "authority_population_sha256",
    "source_game_id",
    "season_label",
    "game_date",
    "normalized_opponent_key",
    "team_score",
    "opponent_score",
    "curated_site_type",
    "decision_date",
    "authority_basis",
}


def registry_path() -> Path:
    return Path(__file__).resolve().parents[1] / REGISTRY_RELATIVE_PATH


def _clean(value: str | None) -> str:
    return str(value or "").strip()


def _site(value: str) -> str:
    folded = _clean(value).upper()
    return {
        "HOME": "SOURCE_PROGRAM_HOME",
        "SOURCE_PROGRAM_HOME": "SOURCE_PROGRAM_HOME",
    }.get(folded, folded)


def _first(row: dict[str, str], *fields: str) -> str:
    for field in fields:
        value = _clean(row.get(field))
        if value:
            return value
    return ""


@lru_cache(maxsize=8)
def _load_registry(path_text: str) -> dict[tuple[str, str], dict[str, str]]:
    path = Path(path_text)
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = set(reader.fieldnames or [])
        missing = sorted(_REQUIRED_FIELDS - fields)
        if missing:
            raise ValueError(
                "research HOME-location exception registry missing columns: "
                + ", ".join(missing)
            )
        result: dict[tuple[str, str], dict[str, str]] = {}
        for line, raw in enumerate(reader, start=2):
            row = {key: _clean(value) for key, value in raw.items()}
            key = (row["school_key"], row["source_game_id"])
            if not all(key) or not row["authority_basis"] or not row["decision_date"]:
                raise ValueError(
                    f"invalid research HOME-location exception registry row {line}"
                )
            for field in (
                "authority_checkpoint_sha256",
                "authority_ledger_sha256",
                "authority_population_sha256",
            ):
                if not _HASH_RE.fullmatch(row[field].casefold()):
                    raise ValueError(
                        f"invalid {field} on research HOME-location exception row {line}"
                    )
            if row["curated_site_type"] != "SOURCE_PROGRAM_HOME":
                raise ValueError(
                    "research HOME-location exception registry may contain only "
                    f"SOURCE_PROGRAM_HOME rows; line {line}"
                )
            if key in result:
                raise ValueError(
                    "duplicate research HOME-location exception registry key: "
                    f"{key[0]}/{key[1]}"
                )
            result[key] = row
    return result


def owner_authorized_home_location_exception(
    row: dict[str, str],
    *,
    registry: Path | None = None,
) -> bool:
    """Return whether one source/research row exactly matches protected-main authority."""

    path = registry.resolve() if registry is not None else registry_path()
    entries = _load_registry(str(path))
    school_key = _first(row, "source_program_key", "school_key")
    source_game_id = _first(row, "source_game_id", "research_game_id")
    entry = entries.get((school_key, source_game_id))
    if entry is None:
        return False

    actual = {
        "season_label": _first(row, "season_label", "season"),
        "game_date": _first(row, "game_date"),
        "normalized_opponent_key": _first(
            row,
            "normalized_opponent_key",
            "canonical_opponent_key",
            "stage2_canonical_opponent_key",
        ),
        "team_score": _first(row, "team_score"),
        "opponent_score": _first(row, "opponent_score"),
        "curated_site_type": _site(
            _first(row, "curated_site_type", "site_type")
        ),
    }
    return all(entry[field] == value for field, value in actual.items())


def canonical_marker_for_source(row: dict[str, str]) -> str:
    if not owner_authorized_home_location_exception(row):
        return ""
    return (
        f"{HOME_LOCATION_EXCEPTION_MARKER} "
        f"source={_first(row, 'source_program_key')}/"
        f"{_first(row, 'source_game_id', 'research_game_id')}]"
    )
