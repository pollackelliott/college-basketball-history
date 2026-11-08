#!/usr/bin/env python3
"""Guarded RESEARCH_FROZEN -> INTEGRATION_FROZEN / Phase 0 staging.

Normal use from a clean ``data/<school>-onboarding`` branch created from current
``origin/main``:

    python tools/stage_research_portfolio.py <school> <research.zip> \
      --expected-sha256 <zip-sha> \
      --research-base <research_base_sha> \
      --history-start-season YYYY-YYYY \
      --history-scope-basis ALWAYS_TOP_LEVEL_FROM_INCEPTION \
      --history-scope-intervals "" \
      --history-scope-notes "Owner-confirmed scope..." \
      --apply --commit

The command verifies the immutable transport artifact, runs the permanent
research acceptance checks, rebases local venue identities against current
global references, registers only mechanically safe aliases/new identities,
installs the exact six-file package, applies the Research-Frozen history scope to
both target-program metadata and the reusable top-level scope baseline, validates
the repository, writes an ignored integration-freeze manifest, and
optionally creates the stable Phase 0 checkpoint commit.

Ambiguous physical venue identity is a STOP, never a guess.
"""

from __future__ import annotations

import argparse
import calendar
import csv
import datetime as dt
import hashlib
import json
import re
import shutil
import unicodedata
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from integration_freeze_guard import (
    build_source_game_semantic_snapshot,
    semantic_snapshot_sha256,
)
from onboarding_hardening import (
    research_portfolio_report,
    venue_summary_consistency_report,
)
from onboarding_plan import (
    REQUIRED_PACKAGE_FILES,
    WorkflowError,
    write_csv_preserving_format,
)
from program_history import history_scope_errors
from venue_geography import normalize_jurisdiction
from stage1_venue_reconciliation import (
    explicit_reuse_locality_compatible,
    load_venue_reconciliation,
    representation_consolidation_conflicts,
    venue_reconciliation_for_row,
)
from stage1_reference_reconciliation import (
    conference_reconciliation_inventory,
    load_conference_reconciliation,
    register_conferences,
)


def run(command: list[str], *, cwd: Path, echo: bool = False) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = result.stdout.rstrip()
    if echo and output:
        print(output)
    if result.returncode:
        raise WorkflowError(f"command failed ({' '.join(command)}):\n{output}")
    return output


def git(repo: Path, *args: str, echo: bool = False) -> str:
    return run(["git", *args], cwd=repo, echo=echo)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def load_existing_school_venues(
    repo: Path,
    *,
    exclude_school_key: str = "",
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in sorted((repo / "schools").glob("*/venues.csv")):
        if exclude_school_key and path.parent.name == exclude_school_key:
            continue
        _, school_rows = load_csv(path)
        for row in school_rows:
            copy = dict(row)
            copy["_school_key"] = path.parent.name
            rows.append(copy)
    return rows


def snapshot_file_bytes(paths: list[Path]) -> dict[Path, bytes | None]:
    return {path: path.read_bytes() if path.exists() else None for path in paths}


def restore_file_bytes(snapshot: dict[Path, bytes | None]) -> None:
    for path, data in snapshot.items():
        if data is None:
            if path.exists():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)



def season_start(value: str) -> int | None:
    text = (value or "").strip()
    if len(text) >= 4 and text[:4].isdigit():
        return int(text[:4])
    return None


def truthy(value: str) -> bool:
    return (value or "").strip().lower() in {"yes", "true", "1", "y"}


def program_alias_applies(
    alias: dict[str, str],
    first_season: str,
    last_season: str,
) -> bool:
    # A bounded alias must cover the package row's full known era.
    start = season_start(alias.get("effective_start_season", ""))
    end = season_start(alias.get("effective_end_season", ""))
    first = season_start(first_season)
    last = season_start(last_season)

    if start is not None and first is not None and first < start:
        return False
    if end is not None and last is not None and last > end:
        return False
    return True


def rebase_program_aliases(
    programs: list[dict[str, str]],
    alias_rows: list[dict[str, str]],
    opponent_rows: list[dict[str, str]],
    source_rows: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, Any]]]:
    # Exact, unique VERIFIED aliases only. No fuzzy or sibling-name inference.
    programs_by_key = {
        row.get("program_key", "").strip(): row
        for row in programs
        if row.get("program_key", "").strip()
    }

    aliases_by_name: dict[str, list[dict[str, str]]] = {}
    for alias in alias_rows:
        if alias.get("verification_status", "").strip() != "VERIFIED":
            continue
        key = alias.get("program_key", "").strip()
        if key not in programs_by_key:
            raise WorkflowError(
                f"verified program alias points to unknown program_key {key!r}"
            )
        normalized = normalize_name(alias.get("alias_name", ""))
        if normalized:
            aliases_by_name.setdefault(normalized, []).append(alias)

    mappings: list[dict[str, Any]] = []
    source_mapping: dict[tuple[str, str], tuple[str, str, str]] = {}

    for row in opponent_rows:
        old_key = row.get("canonical_opponent_key", "").strip()
        if not old_key or old_key in programs_by_key:
            continue

        canonical_name = row.get("canonical_opponent_name", "").strip()
        normalized = normalize_name(canonical_name)
        if not normalized:
            continue

        applicable = [
            alias
            for alias in aliases_by_name.get(normalized, [])
            if program_alias_applies(
                alias,
                row.get("first_season", ""),
                row.get("last_season", ""),
            )
        ]
        keys = sorted(
            {
                alias.get("program_key", "").strip()
                for alias in applicable
                if alias.get("program_key", "").strip()
            }
        )
        if len(keys) > 1:
            raise WorkflowError(
                f"ambiguous verified program alias {canonical_name!r} maps to "
                + ", ".join(keys)
            )
        if not keys:
            continue

        target_key = keys[0]
        target = programs_by_key[target_key]
        target_name = (
            target.get("display_name", "").strip()
            or target.get("program_name", "").strip()
            or target_key
        )
        target_current = "TRUE" if truthy(target.get("current_d1", "")) else "FALSE"

        label = row.get("source_opponent_label", "").strip()
        map_key = (label, old_key)
        prior = source_mapping.get(map_key)
        proposed = (target_key, target_name, target_current)
        if prior and prior != proposed:
            raise WorkflowError(
                f"inconsistent alias rebase for source label {label!r}/{old_key!r}"
            )
        source_mapping[map_key] = proposed

        try:
            expected_games = int(row.get("games_with_source_label", "").strip())
        except ValueError as exc:
            raise WorkflowError(
                f"invalid games_with_source_label for {label!r}"
            ) from exc

        row["canonical_opponent_key"] = target_key
        row["canonical_opponent_name"] = target_name
        if "current_d1" in row:
            row["current_d1"] = target_current

        mappings.append(
            {
                "source_opponent_label": label,
                "canonical_opponent_name": canonical_name,
                "from_program_key": old_key,
                "to_program_key": target_key,
                "to_program_name": target_name,
                "expected_source_games": expected_games,
                "alias_name": applicable[0].get("alias_name", ""),
                "alias_type": applicable[0].get("alias_type", ""),
                "verification_status": applicable[0].get(
                    "verification_status", ""
                ),
            }
        )

    actual_counts: dict[tuple[str, str], int] = {}
    for row in source_rows:
        label = row.get("source_opponent_label", "").strip()
        old_key = row.get("normalized_opponent_key", "").strip()
        map_key = (label, old_key)
        target = source_mapping.get(map_key)
        if target is None:
            continue
        target_key, target_name, target_current = target
        row["normalized_opponent_key"] = target_key
        row["normalized_opponent_name"] = target_name
        if "opponent_current_d1" in row:
            row["opponent_current_d1"] = target_current
        actual_counts[map_key] = actual_counts.get(map_key, 0) + 1

    for mapping in mappings:
        map_key = (
            mapping["source_opponent_label"],
            mapping["from_program_key"],
        )
        actual = actual_counts.get(map_key, 0)
        expected = mapping["expected_source_games"]
        if actual != expected:
            raise WorkflowError(
                f"program alias rebase source-game count mismatch for "
                f"{mapping['source_opponent_label']!r}: expected {expected}, "
                f"found {actual}"
            )
        mapping["source_games_rebased"] = actual

    return opponent_rows, source_rows, mappings


def copy_package(package: Path, destination: Path) -> None:
    if package.is_dir():
        names = sorted(p.name for p in package.iterdir() if p.is_file())
        if names != sorted(REQUIRED_PACKAGE_FILES):
            raise WorkflowError(
                "package directory must contain exactly the six required files"
            )
        for name in REQUIRED_PACKAGE_FILES:
            shutil.copy2(package / name, destination / name)
        return

    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        if sorted(names) != sorted(REQUIRED_PACKAGE_FILES):
            raise WorkflowError(
                "research ZIP must contain exactly the six required flat files"
            )
        if any("/" in name or "\\" in name for name in names):
            raise WorkflowError("research ZIP members must be flat")
        archive.extractall(destination)


def venue_number(value: str) -> int | None:
    match = re.fullmatch(r"VEN-(\d{6})", value or "")
    return int(match.group(1)) if match else None


def next_venue_id(used: set[str]) -> str:
    numbers = [venue_number(value) for value in used]
    high = max((number for number in numbers if number is not None), default=0)
    while True:
        high += 1
        candidate = f"VEN-{high:06d}"
        if candidate not in used:
            return candidate


_DOMESTIC_COUNTRY_TOKENS = {
    "US",
    "USA",
    "UNITED STATES",
    "UNITED STATES OF AMERICA",
}


def foreign_country_registry_jurisdiction(
    local: dict[str, str],
    source_games: list[dict[str, str]],
) -> str:
    """Return one exact foreign country value for the legacy global
    venue jurisdiction slot when the Research venue has city but no state.

    This is representation-only compatibility. Frozen source-game geography
    remains untouched, and domestic/mixed/incomplete evidence never fills the
    missing state field.
    """
    if local.get("state", "").strip():
        return local.get("state", "").strip()

    city = local.get("city", "").strip()
    canonical_name = local.get("canonical_name", "").strip()
    if not city or not canonical_name:
        return ""

    accepted_names = {normalize_name(canonical_name)}
    accepted_names.update(
        normalize_name(alias)
        for alias in local.get("aliases", "").split(";")
        if alias.strip()
    )
    accepted_names.discard("")
    city_folded = city.casefold()

    matches = []
    for game in source_games:
        game_name = (
            game.get("curated_venue_name", "").strip()
            or game.get("source_venue_name", "").strip()
        )
        if normalize_name(game_name) not in accepted_names:
            continue
        if game.get("city", "").strip().casefold() != city_folded:
            continue
        matches.append(game)

    if not matches:
        return ""
    if any(game.get("state", "").strip() for game in matches):
        return ""

    countries = [game.get("country", "").strip() for game in matches]
    if any(not country for country in countries):
        return ""
    unique = {country for country in countries}
    if len(unique) != 1:
        return ""

    country = next(iter(unique))
    if country.upper() in _DOMESTIC_COUNTRY_TOKENS:
        return ""
    return country


# A handful of existing foreign venues use a country code in the global
# registry while incoming Research may retain a more precise region name.
# This is not a general waiver of physical-venue geography. Only a known
# country/subdivision pair, the *same exact venue key*, and the *same populated
# city* make the representations mechanically compatible.
_COUNTRY_SUBDIVISION_EQUIVALENTS = {
    "MX": {"JALISCO", "QUINTANA ROO"},
}


def same_venue_country_subdivision_representation(
    local: dict[str, str],
    global_row: dict[str, str],
) -> bool:
    local_key = local.get("venue_key", "").strip()
    global_key = global_row.get("venue_key", "").strip()
    local_city = local.get("city", "").strip().casefold()
    global_city = global_row.get("city", "").strip().casefold()
    if not (local_key and local_key == global_key and local_city and local_city == global_city):
        return False
    local_state = normalize_jurisdiction(local.get("state", ""))
    global_state = normalize_jurisdiction(global_row.get("state", ""))
    return any(
        (local_state == country and global_state in subdivisions)
        or (global_state == country and local_state in subdivisions)
        for country, subdivisions in _COUNTRY_SUBDIVISION_EQUIVALENTS.items()
    )


def jurisdiction_compatible(
    local: dict[str, str],
    global_row: dict[str, str],
) -> bool:
    lstate = normalize_jurisdiction(local.get("state", ""))
    gstate = normalize_jurisdiction(global_row.get("state", ""))
    return (
        not (lstate and gstate and lstate != gstate)
        or same_venue_country_subdivision_representation(local, global_row)
    )


def geography_compatible(
    local: dict[str, str],
    global_row: dict[str, str],
) -> bool:
    lcity = local.get("city", "").strip().casefold()
    lstate = normalize_jurisdiction(local.get("state", ""))
    gcity = global_row.get("city", "").strip().casefold()
    gstate = normalize_jurisdiction(global_row.get("state", ""))
    if lcity and gcity and lcity != gcity:
        return False
    if lstate and gstate and lstate != gstate:
        return same_venue_country_subdivision_representation(local, global_row)
    return True



def venue_date_bounds(value: str) -> tuple[dt.date, dt.date] | None:
    """Conservative inclusive bounds for an exact, month-only, or year-only date."""
    match = re.fullmatch(
        r"(\d{4})(?:-(\d{2})(?:-(\d{2}))?)?",
        (value or "").strip(),
    )
    if not match:
        return None
    year, month, day = match.groups()
    try:
        start = dt.date(int(year), int(month or "1"), int(day or "1"))
        if day:
            end = start
        elif month:
            end = dt.date(
                start.year,
                start.month,
                calendar.monthrange(start.year, start.month)[1],
            )
        else:
            end = dt.date(start.year, 12, 31)
        return start, end
    except ValueError:
        return None


def _source_game_window(
    game: dict[str, str],
) -> tuple[dt.date, dt.date] | None:
    exact = game.get("game_date", "").strip()
    if exact:
        bounds = venue_date_bounds(exact)
        if bounds is not None and bounds[0] == bounds[1]:
            return bounds
        return None
    season = game.get("season_label", "").strip()
    match = re.fullmatch(r"(\d{4})-(\d{4})", season)
    if not match or int(match.group(2)) != int(match.group(1)) + 1:
        return None
    return (
        dt.date(int(match.group(1)), 7, 1),
        dt.date(int(match.group(2)), 6, 30),
    )


def _relationship_window(
    row: dict[str, str],
) -> tuple[dt.date | None, dt.date | None] | None:
    start_text = row.get("relationship_start", "").strip()
    end_text = row.get("relationship_end", "").strip()
    if not start_text and not end_text:
        return None
    precision = row.get("relationship_date_precision", "").strip().casefold()

    if "season" in precision:
        def season_edge(value: str, *, end: bool) -> dt.date | None:
            match = re.fullmatch(r"(\d{4})-(\d{4})", value)
            if not match or int(match.group(2)) != int(match.group(1)) + 1:
                return None
            return (
                dt.date(int(match.group(2)), 6, 30)
                if end
                else dt.date(int(match.group(1)), 7, 1)
            )

        start = season_edge(start_text, end=False) if start_text else None
        end = season_edge(end_text, end=True) if end_text else None
    else:
        start_bounds = venue_date_bounds(start_text) if start_text else None
        end_bounds = venue_date_bounds(end_text) if end_text else None
        start = start_bounds[0] if start_bounds else None
        end = end_bounds[1] if end_bounds else None

    if start_text and start is None:
        return None
    if end_text and end is None:
        return None
    return start, end


def _relationship_contains_game(
    row: dict[str, str],
    game: dict[str, str],
) -> bool:
    relationship = _relationship_window(row)
    game_window = _source_game_window(game)
    if relationship is None or game_window is None:
        return False
    start, end = relationship
    game_start, game_end = game_window
    if start is not None and game_start < start:
        return False
    if end is not None and game_end > end:
        return False
    return True


def _assignment_summary(rows: list[dict[str, str]]) -> dict[str, str]:
    dates = [row.get("game_date", "").strip() for row in rows]
    exact = [value for value in dates if value]
    return {
        "games_currently_assigned": str(len(rows)),
        "first_assigned_game": (
            min(exact) if rows and len(exact) == len(rows) else ""
        ),
        "last_assigned_game": (
            max(exact) if rows and len(exact) == len(rows) else ""
        ),
    }


def refresh_local_venue_assignment_summaries(
    local_rows: list[dict[str, str]],
    source_games: list[dict[str, str]],
    venue_reconciliation: dict[str, dict[str, Any]] | None = None,
    *,
    source_match_rows: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Refresh only stale derived venue summaries, never historical game fields.

    Unique local representations receive all matching frozen games. Multiple
    relationship rows for one physical identity are partitioned only when each
    game fits exactly one relationship window. Multiple physical identities with
    one reused display name require an explicit hash-bound split proof.

    source_match_rows may carry an authenticated pre-canonical representation
    for source matching while summaries are written to the corresponding staged
    rows. This is used only when reconciliation explicitly preserves such a row.
    """
    venue_reconciliation = venue_reconciliation or {}
    if source_match_rows is None:
        source_match_rows = local_rows
    if len(source_match_rows) != len(local_rows):
        raise WorkflowError(
            "venue summary source-match rows must align exactly with staged local rows"
        )

    groups: dict[tuple[str, str, str], list[int]] = {}
    alias_lookup: dict[
        tuple[str, str, str], set[tuple[str, str, str]]
    ] = {}

    for index, match_row in enumerate(source_match_rows):
        name = match_row.get("canonical_name", "").strip()
        if not name:
            continue
        group = (
            normalize_name(name),
            match_row.get("city", "").strip().casefold(),
            normalize_jurisdiction(match_row.get("state", "")),
        )
        groups.setdefault(group, []).append(index)
        labels = [name]
        labels.extend(
            alias.strip()
            for alias in match_row.get("aliases", "").split(";")
            if alias.strip()
        )
        for label in labels:
            key = (
                normalize_name(label),
                match_row.get("city", "").strip().casefold(),
                normalize_jurisdiction(match_row.get("state", "")),
            )
            alias_lookup.setdefault(key, set()).add(group)

    group_games: dict[
        tuple[str, str, str], list[dict[str, str]]
    ] = {group: [] for group in groups}
    for game in source_games:
        name = game.get("curated_venue_name", "").strip()
        if not name:
            continue
        lookup = (
            normalize_name(name),
            game.get("city", "").strip().casefold(),
            normalize_jurisdiction(game.get("state", "")),
        )
        if lookup in groups:
            group_games[lookup].append(game)
            continue
        matches = alias_lookup.get(lookup, set())
        if len(matches) == 1:
            group_games[next(iter(matches))].append(game)
        elif len(matches) > 1:
            raise WorkflowError(
                "venue summary refresh found an ambiguous local alias for "
                f"source game {game.get('source_game_id','[unknown]')}"
            )

    split_game_target: dict[str, str] = {}
    for mapping in venue_reconciliation.values():
        if mapping.get("action") != "SPLIT_LOCAL_ROW_BY_CUTOVER":
            continue
        for target in mapping.get("split_targets", []):
            target_key = target["global_venue_key"]
            for game_id in target.get("source_game_ids", []):
                prior = split_game_target.get(game_id)
                if prior is not None and prior != target_key:
                    raise WorkflowError(
                        "venue split proof assigns one source game to multiple targets"
                    )
                split_game_target[game_id] = target_key

    refreshed: list[dict[str, Any]] = []
    for group, row_indexes in groups.items():
        rows = [local_rows[index] for index in row_indexes]
        games = group_games.get(group, [])
        raw_counts = [
            row.get("games_currently_assigned", "").strip()
            for row in rows
        ]
        if raw_counts and all(value == "" for value in raw_counts):
            continue
        declared = (
            sum(int(value) for value in raw_counts)
            if raw_counts and all(value.isdigit() for value in raw_counts)
            else None
        )
        expected = len(games)
        all_exact_dates = bool(games) and all(
            game.get("game_date", "").strip()
            for game in games
        )
        bounds_stale = False
        if all_exact_dates:
            exact_dates = sorted(
                game.get("game_date", "").strip()
                for game in games
            )
            declared_first = sorted(
                value
                for row in rows
                if (value := row.get("first_assigned_game", "").strip())
            )
            declared_last = sorted(
                value
                for row in rows
                if (value := row.get("last_assigned_game", "").strip())
            )
            bounds_stale = (
                bool(declared_first)
                and min(declared_first) != exact_dates[0]
            ) or (
                bool(declared_last)
                and max(declared_last) != exact_dates[-1]
            )

        if declared == expected and not bounds_stale:
            continue

        assignments: dict[int, list[dict[str, str]]] = {
            index: [] for index in range(len(rows))
        }

        if len(rows) == 1:
            assignments[0] = list(games)
        else:
            row_by_key: dict[str, list[int]] = {}
            for index, row in enumerate(rows):
                key = row.get("venue_key", "").strip()
                if key:
                    row_by_key.setdefault(key, []).append(index)

            if games and all(
                game.get("source_game_id", "").strip() in split_game_target
                for game in games
            ):
                for game in games:
                    target_key = split_game_target[
                        game.get("source_game_id", "").strip()
                    ]
                    indexes = row_by_key.get(target_key, [])
                    if len(indexes) != 1:
                        raise WorkflowError(
                            "venue split summary refresh cannot locate exactly one "
                            f"retained local target row for {target_key!r}"
                        )
                    assignments[indexes[0]].append(game)
            elif (
                len({
                    row.get("venue_key", "").strip()
                    for row in rows
                    if row.get("venue_key", "").strip()
                }) == 1
                and all(_relationship_window(row) is not None for row in rows)
            ):
                for game in games:
                    indexes = [
                        index
                        for index, row in enumerate(rows)
                        if _relationship_contains_game(row, game)
                    ]
                    if len(indexes) != 1:
                        raise WorkflowError(
                            "venue relationship summary refresh cannot assign "
                            f"source game {game.get('source_game_id','[unknown]')} "
                            "to exactly one retained relationship row"
                        )
                    assignments[indexes[0]].append(game)
            else:
                raise WorkflowError(
                    "stale venue summary cannot be refreshed safely for "
                    f"{rows[0].get('canonical_name','[blank]')!r} "
                    f"{rows[0].get('city','')}, {rows[0].get('state','')}"
                )

        for index, assigned in assignments.items():
            rows[index].update(_assignment_summary(assigned))

        refreshed.append(
            {
                "canonical_name": rows[0].get("canonical_name", "").strip(),
                "city": rows[0].get("city", "").strip(),
                "state": rows[0].get("state", "").strip(),
                "before_declared_count": declared,
                "after_declared_count": sum(
                    int(row.get("games_currently_assigned", "0") or "0")
                    for row in rows
                ),
                "source_game_count": expected,
                "venue_rows": len(rows),
            }
        )

    return {
        "status": "PASS",
        "refreshed_group_count": len(refreshed),
        "groups": refreshed,
    }



def venue_chronology_conflicts(
    local: dict[str, str],
    global_row: dict[str, str],
) -> list[str]:
    """Report provable physical-building date conflicts during identity reuse.

    Unknown or partial dates are not evidence for choosing a building. Year-only
    boundaries are deliberately inclusive so events in a boundary year are not
    rejected without an exact opening or closing date. Never infer H/A/N here.
    """
    opened_text = global_row.get("opened", "").strip()
    closed_text = global_row.get("closed", "").strip()
    opened = venue_date_bounds(opened_text)
    closed = venue_date_bounds(closed_text)
    conflicts: list[str] = []
    for field in ("first_assigned_game", "last_assigned_game"):
        use_text = local.get(field, "").strip()
        use = venue_date_bounds(use_text)
        if use is None:
            continue
        if opened and use[1] < opened[0]:
            conflicts.append(
                f"{field}={use_text} is before physical opening={opened_text}"
            )
        if closed and use[0] > closed[1]:
            conflicts.append(
                f"{field}={use_text} is after physical closing={closed_text}"
            )

    local_close_text = local.get("known_closed", "").strip()
    local_close = venue_date_bounds(local_close_text)
    if opened and local_close and local_close[1] < opened[0]:
        conflicts.append(
            f"known_closed={local_close_text} is before physical opening={opened_text}"
        )

    local_open_text = local.get("known_opened", "").strip()
    local_open = venue_date_bounds(local_open_text)
    if closed and local_open and local_open[0] > closed[1]:
        conflicts.append(
            f"known_opened={local_open_text} is after physical closing={closed_text}"
        )
    return conflicts


def _exact_local_assignment_window(
    local: dict[str, str],
) -> tuple[dt.date, dt.date] | None:
    """Return one exact inclusive assignment window or None.

    Date-aware venue-name disambiguation is deliberately stricter than physical
    chronology validation: both assignment endpoints must be exact dates so a
    shared historical name cannot be resolved from partial or inferred time.
    """
    first = venue_date_bounds(local.get("first_assigned_game", "").strip())
    last = venue_date_bounds(local.get("last_assigned_game", "").strip())
    if (
        first is None
        or last is None
        or first[0] != first[1]
        or last[0] != last[1]
        or first[0] > last[0]
    ):
        return None
    return first[0], last[0]


def _registered_name_window(
    row: dict[str, str],
) -> tuple[dt.date | None, dt.date | None] | None:
    """Return conservative inclusive bounds for one shared venue-name row."""
    start_text = row.get("valid_from", "").strip()
    end_text = row.get("valid_to", "").strip()
    start_bounds = venue_date_bounds(start_text) if start_text else None
    end_bounds = venue_date_bounds(end_text) if end_text else None
    if start_text and start_bounds is None:
        return None
    if end_text and end_bounds is None:
        return None
    start = start_bounds[0] if start_bounds else None
    end = end_bounds[1] if end_bounds else None
    if start is not None and end is not None and start > end:
        return None
    return start, end


def _registered_name_covers_assignment(
    row: dict[str, str],
    assignment: tuple[dt.date, dt.date],
) -> bool:
    window = _registered_name_window(row)
    if window is None:
        return False
    start, end = window
    assignment_start, assignment_end = assignment
    return (
        (start is None or start <= assignment_start)
        and (end is None or end >= assignment_end)
    )


def _registered_name_proves_nonoverlap(
    row: dict[str, str],
    assignment: tuple[dt.date, dt.date],
) -> bool:
    """Return True only for a fully bounded competing period outside assignment."""
    if not row.get("valid_from", "").strip() or not row.get("valid_to", "").strip():
        return False
    window = _registered_name_window(row)
    if window is None:
        return False
    start, end = window
    if start is None or end is None:
        return False
    assignment_start, assignment_end = assignment
    return end < assignment_start or start > assignment_end


def incompatible_school_venue_key_rows(
    local: dict[str, str],
    key: str,
    existing_school_venues: list[dict[str, str]],
) -> list[dict[str, str]]:
    if not key:
        return []
    return [
        row
        for row in existing_school_venues
        if row.get("venue_key", "").strip() == key
        and not geography_compatible(local, row)
    ]


def disambiguated_new_venue_key(
    key: str,
    school_key: str,
    reserved_keys: set[str],
) -> str:
    if not key or not school_key:
        raise WorkflowError("venue-key disambiguation requires key and school_key")
    base = f"{key}-{school_key}"
    candidate = base
    suffix = 2
    while candidate in reserved_keys:
        candidate = f"{base}-{suffix}"
        suffix += 1
    return candidate


def research_base_venue_reuse_hint(
    local: dict[str, str],
) -> tuple[str, str] | None:
    """Read an explicit frozen Research-time global venue reuse hint."""
    match = re.search(
        r"\bresearch-base key=([^;]+);\s*research-base venue_id=(VEN-\d{6})\b",
        local.get("notes", ""),
        flags=re.IGNORECASE,
    )
    if match is None:
        return None
    return match.group(1).strip(), match.group(2).strip()



def research_declares_pending_shared_venue(local: dict[str, str]) -> bool:
    """Return whether frozen Research explicitly deferred global venue identity work."""

    notes = (local.get("notes", "") or "").casefold()
    return any(
        phrase in notes
        for phrase in (
            "defers authoritative id reconciliation to implementation",
            "defers authoritative shared-id reconciliation to implementation",
            "authoritative shared-id reconciliation is deferred to implementation",
            "global registration/current-main reuse decision remains for serialized implementation",
            "global venue registration pending current-main rebase",
            "global registration pending current-main rebase",
            "global registration: pending_current_main_rebase",
        )
    ) or (
        "historical physical identity: resolved" in notes
        and "implementation" in notes
    )


def research_declares_registration_only_pending(local: dict[str, str]) -> bool:
    """Recognize a frozen, settled identity awaiting mechanical registration.

    An explicit registration-only handoff can proceed through guarded Stage 1
    when current-main identity checks are clean. A note that also records an
    unresolved existing identity, collision, or reuse decision is not a waiver.
    """
    notes = (local.get("notes", "") or "").casefold()
    registration_only = any(
        marker in notes
        for marker in (
            "global registration: pending_current_main_rebase",
            "global registration pending current-main rebase",
            "global venue registration pending current-main rebase",
        )
    )
    settled_identity = any(
        marker in notes
        for marker in (
            "historical identity: resolved",
            "historical identity resolved",
            "historical physical identity: resolved",
            "historical physical identity resolved",
            "research-resolved historical identity",
        )
    )
    unresolved_identity = any(
        marker in notes
        for marker in (
            "reuse decision remains",
            "did not establish one authoritative shared venue identity",
            "defers authoritative id reconciliation",
            "defers authoritative shared-id reconciliation",
            "duplicate physical",
            "conflicting physical",
            "multiple physical",
        )
    )
    return registration_only and settled_identity and not unresolved_identity


def venue_reconciliation_inventory(
    local_rows: list[dict[str, str]],
    global_rows: list[dict[str, str]],
    name_rows: list[dict[str, str]],
    *,
    school_key: str = "",
    existing_school_venues: list[dict[str, str]] | None = None,
    venue_reconciliation: dict[str, dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Inventory all venue-reconciliation outcomes without mutating repository state."""

    global_by_key = {
        row.get("venue_key", "").strip(): row
        for row in global_rows
        if row.get("venue_key", "").strip()
    }
    global_by_id = {
        row.get("venue_id", "").strip(): row
        for row in global_rows
        if row.get("venue_id", "").strip()
    }

    ids_by_name: dict[str, set[str]] = {}
    registered_names_by_id: dict[str, set[str]] = {}
    historical_alias_names_by_id: dict[str, set[str]] = {}
    name_rows_by_normalized: dict[str, list[dict[str, str]]] = {}

    for row in global_rows:
        normalized = normalize_name(row.get("display_name", ""))
        if normalized:
            ids_by_name.setdefault(normalized, set()).add(row["venue_id"])

    for row in name_rows:
        venue_id = row.get("venue_id", "").strip()
        normalized = row.get("normalized_name", "").strip() or normalize_name(
            row.get("venue_name", "")
        )
        if not venue_id or not normalized:
            continue
        ids_by_name.setdefault(normalized, set()).add(venue_id)
        registered_names_by_id.setdefault(venue_id, set()).add(normalized)
        name_rows_by_normalized.setdefault(normalized, []).append(row)
        if row.get("name_type", "").strip() == "HISTORICAL_OR_ALIAS":
            historical_alias_names_by_id.setdefault(venue_id, set()).add(normalized)

    results: list[dict[str, Any]] = []
    existing_school_venues = existing_school_venues or []
    venue_reconciliation = venue_reconciliation or {}
    reserved_keys = {
        row.get("venue_key", "").strip()
        for row in [*global_rows, *existing_school_venues, *local_rows]
        if row.get("venue_key", "").strip()
    }

    for row_index, local in enumerate(local_rows, 1):
        key = local.get("venue_key", "").strip()
        name = local.get("canonical_name", "").strip()
        normalized = normalize_name(name)
        local_names = [name]
        local_names.extend(
            alias.strip()
            for alias in local.get("aliases", "").split(";")
            if alias.strip()
        )
        normalized_names = [
            normalize_name(value)
            for value in local_names
            if normalize_name(value)
        ]
        pending_shared = research_declares_pending_shared_venue(local)
        registration_only = research_declares_registration_only_pending(local)

        item: dict[str, Any] = {
            "venue_key": key,
            "canonical_name": name,
            "research_venue_id": local.get("venue_id", "").strip(),
            "city": local.get("city", "").strip(),
            "state": local.get("state", "").strip(),
            "classification": "",
            "resolution": "",
            "target_venue_id": "",
            "target_venue_key": "",
            "issues": [],
            "candidate_venue_ids": [],
            "missing_registered_names": [],
            "chronology_conflicts": [],
        }

        chosen: dict[str, str] | None = None
        reason = ""
        hard_stop = ""

        explicit = venue_reconciliation_for_row(
            venue_reconciliation, local, row_index
        )
        if explicit is not None:
            explicit_action = str(
                explicit.get("action") or "REUSE_CURRENT_IDENTITY"
            )
            if explicit_action == "DROP_REDUNDANT_LOCAL_ROW":
                item["classification"] = "SAFE_REPRESENTATION_DROP"
                item["resolution"] = "DROP_REDUNDANT_LOCAL_ROW"
                item["issues"].append("EXPLICIT_REDUNDANT_LOCAL_ROW_DROP")
                results.append(item)
                continue
            if explicit_action == "SPLIT_LOCAL_ROW_BY_CUTOVER":
                item["classification"] = "SAFE_REPRESENTATION_SPLIT"
                item["resolution"] = "SPLIT_LOCAL_ROW_BY_CUTOVER"
                item["issues"].append(
                    "EXPLICIT_HASH_BOUND_SOURCE_GAME_CUTOVER_SPLIT"
                )
                item["target_venue_id"] = "|".join(
                    target["global_venue_id"]
                    for target in explicit.get("split_targets", [])
                )
                item["target_venue_key"] = "|".join(
                    target["global_venue_key"]
                    for target in explicit.get("split_targets", [])
                )
                results.append(item)
                continue
            if explicit_action == "REGISTER_NEW_IDENTITY":
                item["classification"] = "NEW_GLOBAL_IDENTITY"
                item["resolution"] = "REGISTER_NEW_IDENTITY"
                item["target_venue_key"] = explicit["new_global_venue_key"]
                item["issues"].append(
                    "EXPLICIT_HASH_BOUND_NEW_IDENTITY_REGISTRATION"
                )
                results.append(item)
                continue

        hint = research_base_venue_reuse_hint(local)
        if explicit is not None:
            candidate = global_by_id.get(explicit["global_venue_id"])
            if (candidate is None
                or candidate.get("venue_key", "").strip() != explicit["global_venue_key"]):
                hard_stop = "EXPLICIT_RECONCILIATION_STALE"
            elif not explicit_reuse_locality_compatible(
                local, candidate, explicit
            ):
                hard_stop = "EXPLICIT_RECONCILIATION_GEOGRAPHY_CONFLICT"
            else:
                chosen = candidate
                reason = (
                    "REUSE_EXPLICIT_RECONCILIATION_PRESERVE_LOCAL_ROW"
                    if explicit.get("preserve_local_representation")
                    else "REUSE_EXPLICIT_RECONCILIATION"
                )
        elif hint is not None:
            hinted_key, hinted_id = hint
            hinted_by_key = global_by_key.get(hinted_key)
            hinted_by_id = global_by_id.get(hinted_id)
            if (
                hinted_by_key is None
                or hinted_by_id is None
                or hinted_by_key.get("venue_id", "").strip() != hinted_id
                or hinted_by_id.get("venue_key", "").strip() != hinted_key
            ):
                hard_stop = "RESEARCH_BASE_HINT_STALE"
            elif not jurisdiction_compatible(local, hinted_by_id):
                hard_stop = "JURISDICTION_CONFLICT"
            else:
                chosen = hinted_by_id
                reason = "REUSE_RESEARCH_BASE_IDENTITY"
        elif key and key in global_by_key:
            candidate = global_by_key[key]
            if not jurisdiction_compatible(local, candidate):
                hard_stop = "JURISDICTION_CONFLICT"
            else:
                chosen = candidate
                reason = "REUSE_EXACT_KEY"

        canonical_candidate_ids: set[str] = set()
        if not hard_stop and chosen is None and normalized:
            canonical_candidate_ids = {
                venue_id
                for venue_id in ids_by_name.get(normalized, set())
                if venue_id in global_by_id
                and geography_compatible(local, global_by_id[venue_id])
            }
            if len(canonical_candidate_ids) == 1:
                candidate_id = next(iter(canonical_candidate_ids))
                if normalized in historical_alias_names_by_id.get(
                    candidate_id, set()
                ):
                    chosen = global_by_id[candidate_id]
                    reason = "REUSE_REGISTERED_ALIAS"

            if chosen is None and canonical_candidate_ids:
                resolved_name_ids: list[set[str]] = []
                for normalized_name in normalized_names:
                    ids = {
                        venue_id
                        for venue_id in ids_by_name.get(normalized_name, set())
                        if venue_id in global_by_id
                        and geography_compatible(local, global_by_id[venue_id])
                    }
                    if ids:
                        resolved_name_ids.append(ids)

                if (
                    len(normalized_names) >= 2
                    and len(resolved_name_ids) == len(normalized_names)
                    and all(len(ids) == 1 for ids in resolved_name_ids)
                ):
                    resolved_ids = {next(iter(ids)) for ids in resolved_name_ids}
                    if len(resolved_ids) == 1:
                        candidate_id = next(iter(resolved_ids))
                        if any(
                            normalized_name
                            in historical_alias_names_by_id.get(candidate_id, set())
                            for normalized_name in normalized_names
                        ):
                            chosen = global_by_id[candidate_id]
                            reason = "REUSE_REGISTERED_NAME_CLUSTER"

        all_name_candidates: set[str] = set()
        for normalized_name in normalized_names:
            all_name_candidates.update(
                venue_id
                for venue_id in ids_by_name.get(normalized_name, set())
                if venue_id in global_by_id
                and geography_compatible(local, global_by_id[venue_id])
            )
        item["candidate_venue_ids"] = sorted(all_name_candidates)

        if hard_stop:
            item["classification"] = "STOP_AMBIGUOUS"
            item["issues"].append(hard_stop)
        elif chosen is not None:
            chosen_id = chosen.get("venue_id", "").strip()
            chronology_conflicts = venue_chronology_conflicts(local, chosen)
            item["chronology_conflicts"] = chronology_conflicts
            chosen_notes = (chosen.get("notes", "") or "").casefold()
            conflicting_ids = sorted(all_name_candidates - {chosen_id})

            intentional_split_ids = [
                venue_id
                for venue_id in conflicting_ids
                if reason in {
                    "REUSE_EXACT_KEY",
                    "REUSE_RESEARCH_BASE_IDENTITY",
                    "REUSE_EXPLICIT_RECONCILIATION",
                    "REUSE_EXPLICIT_RECONCILIATION_PRESERVE_LOCAL_ROW",
                }
                and chosen.get("identity_status", "").strip() == "RESEARCHED_SPLIT"
                and global_by_id[venue_id].get("identity_status", "").strip()
                == "RESEARCHED_SPLIT"
            ]

            date_disambiguated_ids: list[str] = []
            assignment_window = _exact_local_assignment_window(local)
            if (
                assignment_window is not None
                and reason in {
                    "REUSE_EXACT_KEY",
                    "REUSE_RESEARCH_BASE_IDENTITY",
                    "REUSE_EXPLICIT_RECONCILIATION",
                    "REUSE_EXPLICIT_RECONCILIATION_PRESERVE_LOCAL_ROW",
                }
            ):
                local_name_set = set(normalized_names)
                chosen_period_rows = [
                    row
                    for normalized_name in local_name_set
                    for row in name_rows_by_normalized.get(normalized_name, [])
                    if row.get("venue_id", "").strip() == chosen_id
                ]
                chosen_period_matches = any(
                    _registered_name_covers_assignment(row, assignment_window)
                    for row in chosen_period_rows
                )
                if chosen_period_matches:
                    for venue_id in conflicting_ids:
                        competing_rows = [
                            row
                            for normalized_name in local_name_set
                            for row in name_rows_by_normalized.get(normalized_name, [])
                            if row.get("venue_id", "").strip() == venue_id
                        ]
                        if (
                            competing_rows
                            and all(
                                _registered_name_proves_nonoverlap(
                                    row, assignment_window
                                )
                                for row in competing_rows
                            )
                        ):
                            date_disambiguated_ids.append(venue_id)

            unresolved_conflicting_ids = sorted(
                set(conflicting_ids)
                - set(intentional_split_ids)
                - set(date_disambiguated_ids)
            )
            if intentional_split_ids:
                item["issues"].append("INTENTIONAL_RESEARCHED_SPLIT_NAME_OVERLAP")
            if date_disambiguated_ids:
                item["issues"].append(
                    "DATE_BOUNDED_REGISTERED_NAME_DISAMBIGUATION"
                )

            if chronology_conflicts:
                item["classification"] = "STOP_AMBIGUOUS"
                item["issues"].append("PHYSICAL_VENUE_CHRONOLOGY_CONFLICT")
            elif unresolved_conflicting_ids:
                item["classification"] = (
                    "SHARED_GLOBAL_MAINTENANCE"
                    if pending_shared
                    else "STOP_AMBIGUOUS"
                )
                item["issues"].append("CONFLICTING_REGISTERED_NAME_IDENTITIES")
            elif (
                pending_shared
                and reason == "REUSE_EXACT_KEY"
                and not registration_only
                and not any(
                    marker in chosen_notes
                    for marker in (
                        "retired during shared-reference reconciliation",
                        "registered during shared-reference reconciliation",
                    )
                )
            ):
                item["classification"] = "SHARED_GLOBAL_MAINTENANCE"
                item["issues"].append(
                    "RESEARCH_SETTLED_GLOBAL_RECONCILIATION_PENDING"
                )
            else:
                retained_same_key = (
                    [
                        other
                        for other in local_rows
                        if other is not local
                        and other.get("venue_key", "").strip()
                        == chosen.get("venue_key", "").strip()
                        and other.get("canonical_name", "").strip() == name
                        and explicit_reuse_locality_compatible(
                            local, other, explicit
                        )
                    ]
                    if explicit is not None
                    else []
                )
                consolidation_conflicts = (
                    representation_consolidation_conflicts(
                        local, retained_same_key
                    )
                    if explicit is not None
                    and not key
                    and retained_same_key
                    else []
                )
                if (
                    explicit is not None
                    and not key
                    and retained_same_key
                    and explicit.get("preserve_local_representation")
                ):
                    item["classification"] = "SAFE_REPRESENTATION_PRESERVE"
                    item["issues"].append(
                        "EXPLICIT_REUSE_PRESERVES_RELATIONSHIP_LOCAL_ROW"
                    )
                    item["issues"].append(
                        "PRESERVED_LOCAL_AUTHORITY:"
                        + ",".join(consolidation_conflicts)
                    )
                elif (
                    explicit is not None
                    and not key
                    and retained_same_key
                    and not consolidation_conflicts
                ):
                    item["classification"] = (
                        "SAFE_REPRESENTATION_CONSOLIDATION"
                    )
                    item["issues"].append(
                        "EXPLICIT_REUSE_CONSOLIDATES_EXISTING_LOCAL_IDENTITY"
                    )
                elif (
                    explicit is not None
                    and not key
                    and retained_same_key
                    and consolidation_conflicts
                ):
                    item["classification"] = "STOP_AMBIGUOUS"
                    item["issues"].append(
                        "LOCAL_REPRESENTATION_CONSOLIDATION_NOT_SAFE:"
                        + ",".join(consolidation_conflicts)
                    )
                else:
                    item["classification"] = "SAFE_REPRESENTATION_REUSE"
                if pending_shared and registration_only:
                    item["issues"].append(
                        "SETTLED_PENDING_REGISTRATION_RESOLVED_BY_EXACT_REUSE"
                    )

            item["resolution"] = reason
            item["target_venue_id"] = chosen_id
            item["target_venue_key"] = chosen.get("venue_key", "").strip()

            if (
                local.get("city", "").strip() != chosen.get("city", "").strip()
                or normalize_jurisdiction(local.get("state", ""))
                != normalize_jurisdiction(chosen.get("state", ""))
                or local.get("state", "").strip() != chosen.get("state", "").strip()
            ):
                item["issues"].append("CANONICAL_GEOGRAPHY_NORMALIZATION")

            registered = registered_names_by_id.get(chosen_id, set())
            missing = [
                original
                for original in local_names
                if normalize_name(original)
                and normalize_name(original) not in registered
            ]
            item["missing_registered_names"] = missing
            if missing:
                item["issues"].append("GLOBAL_NAME_REGISTRATION_DURING_PHASE0")
        else:
            if pending_shared and not registration_only:
                item["classification"] = "SHARED_GLOBAL_MAINTENANCE"
                item["issues"].append(
                    "RESEARCH_SETTLED_GLOBAL_RECONCILIATION_PENDING"
                )
            elif all_name_candidates or canonical_candidate_ids:
                item["classification"] = "STOP_AMBIGUOUS"
                item["issues"].append(
                    "POSSIBLE_PHYSICAL_MATCH_REQUIRES_RECONCILIATION"
                )
            else:
                if not key:
                    item["classification"] = "STOP_AMBIGUOUS"
                    item["issues"].append(
                        "BLANK_KEY_NEW_IDENTITY_REQUIRES_EXPLICIT_REGISTRATION"
                    )
                    item["resolution"] = ""
                    item["target_venue_key"] = ""
                    results.append(item)
                    continue
                item["classification"] = "NEW_GLOBAL_IDENTITY"
                if pending_shared and registration_only:
                    item["issues"].append(
                        "SETTLED_PENDING_REGISTRATION_READY_FOR_PHASE0"
                    )
                collisions = incompatible_school_venue_key_rows(
                    local,
                    key,
                    existing_school_venues,
                )
                if collisions:
                    target_key = disambiguated_new_venue_key(
                        key,
                        school_key,
                        reserved_keys,
                    )
                    reserved_keys.add(target_key)
                    item["resolution"] = "NEW_GLOBAL_IDENTITY_DISAMBIGUATED_KEY"
                    item["target_venue_key"] = target_key
                    item["issues"].append("SCHOOL_LOCAL_KEY_GEOGRAPHY_COLLISION")
                    item["issues"].append(
                        "COLLIDES_WITH_SCHOOL_KEYS:"
                        + ",".join(
                            sorted(
                                {
                                    row.get("_school_key", "").strip() or "[unknown]"
                                    for row in collisions
                                }
                            )
                        )
                    )
                else:
                    item["resolution"] = "NEW_GLOBAL_IDENTITY"
                    item["target_venue_key"] = key

        results.append(item)

    counts: dict[str, int] = {}
    for row in results:
        classification = row["classification"]
        counts[classification] = counts.get(classification, 0) + 1

    blockers = [
        row
        for row in results
        if row["classification"]
        in {"SHARED_GLOBAL_MAINTENANCE", "STOP_AMBIGUOUS"}
    ]
    return {
        "schema_version": 1,
        "venue_count": len(results),
        "classification_counts": dict(sorted(counts.items())),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "rows": results,
    }


def program_alias_inventory(
    programs: list[dict[str, str]],
    alias_rows: list[dict[str, str]],
    opponent_rows: list[dict[str, str]],
) -> dict[str, Any]:
    """Inventory verified current-program alias rebases without mutating rows."""

    program_keys = {
        row.get("program_key", "").strip()
        for row in programs
        if row.get("program_key", "").strip()
    }
    aliases_by_name: dict[str, list[dict[str, str]]] = {}
    for alias in alias_rows:
        if alias.get("verification_status", "").strip() != "VERIFIED":
            continue
        normalized = normalize_name(alias.get("alias_name", ""))
        if normalized:
            aliases_by_name.setdefault(normalized, []).append(alias)

    results: list[dict[str, Any]] = []
    for row in opponent_rows:
        old_key = row.get("canonical_opponent_key", "").strip()
        if not old_key or old_key in program_keys:
            continue
        name = row.get("canonical_opponent_name", "").strip()
        normalized = normalize_name(name)
        applicable = [
            alias
            for alias in aliases_by_name.get(normalized, [])
            if program_alias_applies(
                alias,
                row.get("first_season", ""),
                row.get("last_season", ""),
            )
        ]
        keys = sorted(
            {
                alias.get("program_key", "").strip()
                for alias in applicable
                if alias.get("program_key", "").strip()
            }
        )
        classification = (
            "STOP_AMBIGUOUS"
            if len(keys) > 1
            else "SAFE_PROGRAM_ALIAS_REUSE"
            if len(keys) == 1
            else "NO_CURRENT_VERIFIED_ALIAS"
        )

        results.append(
            {
                "source_opponent_label": row.get("source_opponent_label", "").strip(),
                "canonical_opponent_name": name,
                "from_program_key": old_key,
                "classification": classification,
                "candidate_program_keys": keys,
            }
        )

    counts: dict[str, int] = {}
    for row in results:
        classification = row["classification"]
        counts[classification] = counts.get(classification, 0) + 1

    blockers = [
        row for row in results if row["classification"] == "STOP_AMBIGUOUS"
    ]
    return {
        "schema_version": 1,
        "row_count": len(results),
        "classification_counts": dict(sorted(counts.items())),
        "blocker_count": len(blockers),
        "blockers": blockers,
        "rows": results,
    }


def build_stage1_reconciliation_inventory(
    school_key: str,
    local_venues: list[dict[str, str]],
    global_venues: list[dict[str, str]],
    venue_names: list[dict[str, str]],
    programs: list[dict[str, str]],
    program_aliases: list[dict[str, str]],
    local_opponents: list[dict[str, str]],
    *,
    local_conferences: list[dict[str, str]] | None = None,
    global_conferences: list[dict[str, str]] | None = None,
    conference_registrations: list[dict[str, str]] | None = None,
    existing_school_venues: list[dict[str, str]] | None = None,
    venue_reconciliation: dict[str, dict[str, str]] | None = None,
) -> dict[str, Any]:
    venue = venue_reconciliation_inventory(
        local_venues,
        global_venues,
        venue_names,
        school_key=school_key,
        existing_school_venues=existing_school_venues,
        venue_reconciliation=venue_reconciliation,
    )
    program = program_alias_inventory(
        programs,
        program_aliases,
        local_opponents,
    )
    conference = conference_reconciliation_inventory(
        local_conferences or [],
        global_conferences or [],
        conference_registrations or [],
    )
    blocker_count = (
        venue["blocker_count"]
        + program["blocker_count"]
        + conference["blocker_count"]
    )
    maintenance = venue["classification_counts"].get(
        "SHARED_GLOBAL_MAINTENANCE", 0
    )
    ambiguous = (
        venue["classification_counts"].get("STOP_AMBIGUOUS", 0)
        + program["classification_counts"].get("STOP_AMBIGUOUS", 0)
        + conference["classification_counts"].get("STOP_AMBIGUOUS", 0)
    )
    return {
        "schema_version": 2,
        "school_key": school_key,
        "status": (
            "MAINTENANCE_REQUIRED"
            if maintenance
            else "BLOCKED"
            if ambiguous
            else "PASS"
        ),
        "blocker_count": blocker_count,
        "maintenance_required_count": maintenance,
        "ambiguous_stop_count": ambiguous,
        "venue": venue,
        "program_alias": program,
        "conference": conference,
    }


def write_stage1_reconciliation_inventory(
    repo: Path,
    school_key: str,
    report: dict[str, Any],
) -> Path:
    output = repo / ".onboarding" / school_key / "stage1-reconciliation.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def rebase_venues(
    school_key: str,
    local_rows: list[dict[str, str]],
    global_rows: list[dict[str, str]],
    name_rows: list[dict[str, str]],
    *,
    existing_school_venues: list[dict[str, str]] | None = None,
    venue_reconciliation: dict[str, dict[str, Any]] | None = None,
    source_games: list[dict[str, str]] | None = None,
    summary_match_rows_out: list[dict[str, str]] | None = None,
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, Any]],
]:
    global_by_key = {
        row.get("venue_key", "").strip(): row
        for row in global_rows
        if row.get("venue_key", "").strip()
    }
    global_by_id = {
        row.get("venue_id", "").strip(): row
        for row in global_rows
        if row.get("venue_id", "").strip()
    }

    ids_by_name: dict[str, set[str]] = {}
    for row in global_rows:
        normalized = normalize_name(row.get("display_name", ""))
        if normalized:
            ids_by_name.setdefault(normalized, set()).add(row["venue_id"])
    for row in name_rows:
        normalized = row.get("normalized_name", "").strip() or normalize_name(
            row.get("venue_name", "")
        )
        if normalized:
            ids_by_name.setdefault(normalized, set()).add(row["venue_id"])

    registered_names_by_id: dict[str, set[str]] = {}
    historical_alias_names_by_id: dict[str, set[str]] = {}
    for row in name_rows:
        normalized_registered = (
            row.get("normalized_name", "").strip()
            or normalize_name(row.get("venue_name", ""))
        )
        registered_names_by_id.setdefault(row["venue_id"], set()).add(
            normalized_registered
        )
        if row.get("name_type", "").strip() == "HISTORICAL_OR_ALIAS":
            historical_alias_names_by_id.setdefault(row["venue_id"], set()).add(
                normalized_registered
            )

    used_ids = set(global_by_id)
    existing_school_venues = existing_school_venues or []
    venue_reconciliation = venue_reconciliation or {}
    source_games = source_games or []
    reserved_keys = {
        row.get("venue_key", "").strip()
        for row in [*global_rows, *existing_school_venues, *local_rows]
        if row.get("venue_key", "").strip()
    }
    mappings: list[dict[str, Any]] = []
    staged_local_rows: list[dict[str, str]] = []
    summary_match_rows: list[dict[str, str]] = []

    for row_index, local in enumerate(local_rows, 1):
        frozen_summary_match_row = dict(local)
        key = local.get("venue_key", "").strip()
        name = local.get("canonical_name", "").strip()
        research_id = local.get("venue_id", "").strip()
        normalized = normalize_name(name)

        chosen: dict[str, str] | None = None
        reason = ""

        explicit = venue_reconciliation_for_row(
            venue_reconciliation, local, row_index
        )
        register_new_key = ""
        if explicit is not None:
            explicit_action = str(
                explicit.get("action") or "REUSE_CURRENT_IDENTITY"
            )
            if explicit_action == "DROP_REDUNDANT_LOCAL_ROW":
                mappings.append(
                    {
                        "venue_key": key,
                        "final_venue_key": "",
                        "canonical_name": name,
                        "research_venue_id": research_id,
                        "final_venue_id": "",
                        "resolution": "DROP_REDUNDANT_LOCAL_ROW",
                        "frozen_row_index": row_index,
                    }
                )
                continue
            if explicit_action == "SPLIT_LOCAL_ROW_BY_CUTOVER":
                mappings.append(
                    {
                        "venue_key": key,
                        "final_venue_key": "",
                        "canonical_name": name,
                        "research_venue_id": research_id,
                        "final_venue_id": "",
                        "resolution": "SPLIT_LOCAL_ROW_BY_CUTOVER",
                        "frozen_row_index": row_index,
                        "split_source_game_count": explicit.get(
                            "split_source_game_count", ""
                        ),
                    }
                )
                continue
            if explicit_action == "REUSE_CURRENT_IDENTITY" and not key:
                target_key = explicit["global_venue_key"]
                retained = [
                    other
                    for other in local_rows
                    if other is not local
                    and other.get("venue_key", "").strip() == target_key
                    and other.get("canonical_name", "").strip() == name
                    and explicit_reuse_locality_compatible(
                        local, other, explicit
                    )
                ]
                if retained:
                    conflicts = representation_consolidation_conflicts(
                        local, retained
                    )
                    if explicit.get("preserve_local_representation"):
                        if "RELATIONSHIP_AUTHORITY_PRESENT" not in conflicts:
                            raise WorkflowError(
                                "preserved local venue representation lost its "
                                "relationship-authority predicate"
                            )
                    else:
                        if conflicts:
                            raise WorkflowError(
                                "explicit same-identity venue consolidation is unsafe: "
                                + ",".join(conflicts)
                            )
                        mappings.append(
                            {
                                "venue_key": key,
                                "final_venue_key": target_key,
                                "canonical_name": name,
                                "research_venue_id": research_id,
                                "final_venue_id": explicit["global_venue_id"],
                                "resolution": "CONSOLIDATE_EXPLICIT_REUSE",
                                "frozen_row_index": row_index,
                            }
                        )
                        continue
            if explicit_action == "REGISTER_NEW_IDENTITY":
                register_new_key = explicit["new_global_venue_key"]
                already_created = global_by_key.get(register_new_key)
                if already_created is not None:
                    if (
                        normalize_name(already_created.get("display_name", ""))
                        != normalized
                        or not geography_compatible(local, already_created)
                    ):
                        raise WorkflowError(
                            "same-package registered venue identity no longer "
                            f"matches frozen row {row_index}"
                        )
                    chosen = already_created
                    reason = "REUSE_SAME_PACKAGE_NEW_IDENTITY"

        research_base_hint = research_base_venue_reuse_hint(local)

        if (
            explicit is not None
            and explicit_action == "REUSE_CURRENT_IDENTITY"
        ):
            candidate = global_by_id.get(explicit["global_venue_id"])
            if (
                candidate is None
                or candidate.get("venue_key", "").strip()
                != explicit["global_venue_key"]
                or not explicit_reuse_locality_compatible(
                    local, candidate, explicit
                )
            ):
                raise WorkflowError(
                    f"explicit venue reconciliation no longer matches current main: {key!r}"
                )
            chosen = candidate
            reason = (
                "REUSE_EXPLICIT_RECONCILIATION_PRESERVE_LOCAL_ROW"
                if explicit.get("preserve_local_representation")
                else "REUSE_EXPLICIT_RECONCILIATION"
            )
        elif research_base_hint is not None:
            hinted_key, hinted_id = research_base_hint
            hinted_by_key = global_by_key.get(hinted_key)
            hinted_by_id = global_by_id.get(hinted_id)

            if (
                hinted_by_key is None
                or hinted_by_id is None
                or hinted_by_key.get("venue_id", "").strip() != hinted_id
                or hinted_by_id.get("venue_key", "").strip() != hinted_key
            ):
                raise WorkflowError(
                    "research-base venue reuse hint no longer matches current main: "
                    f"local_key={key!r}, hinted_key={hinted_key!r}, "
                    f"hinted_id={hinted_id!r}"
                )

            if not jurisdiction_compatible(local, hinted_by_id):
                raise WorkflowError(
                    f"research-base venue reuse hint jurisdiction conflicts for {key!r}: "
                    f"local={local.get('city','')},{local.get('state','')} "
                    f"global={hinted_by_id.get('city','')},"
                    f"{hinted_by_id.get('state','')}"
                )

            # The global venue registry owns canonical physical-venue geography.
            # Frozen school source assertions keep their own game-level city/state.
            # Therefore an exact key+VEN-ID reuse hint may survive a same-state
            # locality-label difference without rewriting frozen historical evidence.
            chosen = hinted_by_id
            reason = "REUSE_RESEARCH_BASE_IDENTITY"

        elif key and key in global_by_key:
            candidate = global_by_key[key]
            if not jurisdiction_compatible(local, candidate):
                raise WorkflowError(
                    f"venue key {key!r} exists globally but jurisdiction conflicts: "
                    f"local={local.get('city','')},{local.get('state','')} "
                    f"global={candidate.get('city','')},{candidate.get('state','')}"
                )
            chosen = candidate
            reason = "REUSE_EXACT_KEY"

        if chosen is None and normalized and not register_new_key:
            candidate_ids = {
                venue_id
                for venue_id in ids_by_name.get(normalized, set())
                if geography_compatible(local, global_by_id[venue_id])
            }
            if len(candidate_ids) == 1:
                candidate_id = next(iter(candidate_ids))
                if normalized in historical_alias_names_by_id.get(
                    candidate_id, set()
                ):
                    chosen = global_by_id[candidate_id]
                    reason = "REUSE_REGISTERED_ALIAS"

            if chosen is None and candidate_ids:
                local_name_set = [name]
                local_name_set.extend(
                    alias.strip()
                    for alias in local.get("aliases", "").split(";")
                    if alias.strip()
                )
                normalized_name_set = [
                    normalize_name(value)
                    for value in local_name_set
                    if normalize_name(value)
                ]

                resolved_name_ids: list[set[str]] = []
                for normalized_name in normalized_name_set:
                    ids = {
                        venue_id
                        for venue_id in ids_by_name.get(normalized_name, set())
                        if geography_compatible(local, global_by_id[venue_id])
                    }
                    if ids:
                        resolved_name_ids.append(ids)

                if (
                    len(normalized_name_set) >= 2
                    and len(resolved_name_ids) == len(normalized_name_set)
                    and all(len(ids) == 1 for ids in resolved_name_ids)
                ):
                    resolved_ids = {
                        next(iter(ids))
                        for ids in resolved_name_ids
                    }
                    if len(resolved_ids) == 1:
                        candidate_id = next(iter(resolved_ids))
                        has_registered_alias = any(
                            normalized_name
                            in historical_alias_names_by_id.get(candidate_id, set())
                            for normalized_name in normalized_name_set
                        )
                        if has_registered_alias:
                            chosen = global_by_id[candidate_id]
                            reason = "REUSE_REGISTERED_NAME_CLUSTER"

            if chosen is None and candidate_ids:
                raise WorkflowError(
                    f"venue {name!r} has a possible physical venue match "
                    f"({', '.join(sorted(candidate_ids))}) by name/geography, "
                    f"but venue_key {key!r} does not exactly match current main; "
                    "resolve physical identity explicitly before Phase 0"
                )

        # Exact keys, research-base hints, and registered aliases cannot override
        # a provably impossible physical-building chronology.
        if chosen is not None:
            chronology_conflicts = venue_chronology_conflicts(local, chosen)
            if chronology_conflicts:
                raise WorkflowError(
                    "physical venue chronology conflict before Phase 0: "
                    f"local_key={key!r}, global_id={chosen['venue_id']!r}: "
                    + "; ".join(chronology_conflicts)
                )

        # Research-time numeric venue IDs are transport provenance only.
        # A genuinely new physical identity always receives the next
        # authoritative global ID from current main.
        if chosen is None:
            final_id = next_venue_id(used_ids)
            used_ids.add(final_id)

            final_key = register_new_key or key
            collisions = incompatible_school_venue_key_rows(
                local,
                final_key,
                existing_school_venues,
            )
            if register_new_key:
                if collisions:
                    raise WorkflowError(
                        "explicit new venue key conflicts with an existing "
                        f"school-local representation: {register_new_key!r}"
                    )
                reason = "NEW_GLOBAL_IDENTITY_EXPLICIT_REGISTRATION"
            else:
                reason = "NEW_GLOBAL_IDENTITY"
                if collisions:
                    final_key = disambiguated_new_venue_key(
                        key,
                        school_key,
                        reserved_keys,
                    )
                    reserved_keys.add(final_key)
                    reason = "NEW_GLOBAL_IDENTITY_DISAMBIGUATED_KEY"

            registry_state = (
                local.get("state", "").strip()
                or foreign_country_registry_jurisdiction(local, source_games)
            )
            chosen = {
                "venue_id": final_id,
                "venue_key": final_key,
                "display_name": name,
                "city": local.get("city", "").strip(),
                "state": registry_state,
                "opened": local.get("known_opened", "").strip(),
                "closed": local.get("known_closed", "").strip(),
                "date_precision": (
                    local.get("venue_date_precision", "").strip().upper()
                    if local.get("venue_date_precision", "").strip().lower()
                    != "unknown"
                    else ""
                ),
                "identity_status": (
                    f"RESEARCHED_{school_key.upper().replace('-', '_')}_ONBOARDING"
                ),
                "source_basis": local.get("source_basis", "").strip(),
                "notes": (
                    f"Integrated from {school_key} research portfolio after "
                    "current-main physical-identity rebase."
                ),
            }
            if not chosen["venue_key"] or not chosen["display_name"]:
                raise WorkflowError(
                    "new venue identity requires venue_key and canonical_name: "
                    f"{local}"
                )
            global_rows.append(chosen)
            global_by_key[chosen["venue_key"]] = chosen
            global_by_id[chosen["venue_id"]] = chosen
            ids_by_name.setdefault(normalize_name(chosen["display_name"]), set()).add(
                chosen["venue_id"]
            )
            if reason == "NEW_GLOBAL_IDENTITY":
                reserved_keys.add(chosen["venue_key"])

        final_id = chosen["venue_id"]
        local["venue_id"] = final_id
        local["venue_key"] = chosen["venue_key"]

        # School-local venues.csv is integration representation, not literal
        # game-level source evidence. Once a physical identity is reused, its
        # canonical geography must match the global venue registry so the same
        # venue_key cannot carry conflicting location representations across
        # school packages. Frozen source-games.csv geography is untouched.
        if not reason.startswith("NEW_GLOBAL_IDENTITY"):
            local["city"] = chosen.get("city", "").strip()
            local["state"] = chosen.get("state", "").strip()
        elif (
            not local.get("state", "").strip()
            and chosen.get("state", "").strip()
        ):
            # venues.csv is integration representation. Preserve the accepted
            # foreign country in the registry's legacy jurisdiction slot while
            # leaving frozen source-games.csv city/state/country untouched.
            local["state"] = chosen.get("state", "").strip()

        local_notes = local.get("notes", "").strip()
        integration_note = f"Integration rebase resolved final global venue ID {final_id}."
        local["notes"] = local_notes + (" " if local_notes else "") + integration_note

        candidate_names = [
            (
                name,
                "PROJECT_DISPLAY"
                if reason.startswith("NEW_GLOBAL_IDENTITY")
                else "HISTORICAL_OR_ALIAS",
            )
        ]
        for alias in local.get("aliases", "").split(";"):
            alias = alias.strip()
            if alias:
                candidate_names.append((alias, "HISTORICAL_OR_ALIAS"))

        for candidate_name, name_type in candidate_names:
            normalized_candidate = normalize_name(candidate_name)
            if not normalized_candidate:
                continue
            if normalized_candidate in registered_names_by_id.get(final_id, set()):
                continue
            name_rows.append(
                {
                    "venue_id": final_id,
                    "venue_name": candidate_name,
                    "normalized_name": normalized_candidate,
                    "name_type": name_type,
                    "valid_from": "",
                    "valid_to": "",
                    "date_precision": "",
                    "source_basis": local.get("source_basis", "").strip(),
                    "notes": (
                        f"Registered during {school_key} onboarding current-main rebase."
                    ),
                }
            )
            registered_names_by_id.setdefault(final_id, set()).add(normalized_candidate)

        mappings.append(
            {
                "venue_key": key,
                "final_venue_key": chosen["venue_key"],
                "canonical_name": name,
                "research_venue_id": research_id,
                "final_venue_id": final_id,
                "resolution": reason,
            }
        )
        staged_local_rows.append(local)
        summary_match_rows.append(
            frozen_summary_match_row
            if reason == "REUSE_EXPLICIT_RECONCILIATION_PRESERVE_LOCAL_ROW"
            else dict(local)
        )

    if source_games:
        refresh_local_venue_assignment_summaries(
            staged_local_rows,
            source_games,
            venue_reconciliation,
            source_match_rows=summary_match_rows,
        )

    if summary_match_rows_out is not None:
        summary_match_rows_out.extend(dict(row) for row in summary_match_rows)

    return staged_local_rows, global_rows, name_rows, mappings


def update_program_scope(
    programs: list[dict[str, str]],
    school_key: str,
    *,
    start_season: str,
    basis: str,
    intervals: str,
    notes: str,
) -> None:
    targets = [row for row in programs if row.get("program_key") == school_key]
    if len(targets) != 1:
        raise WorkflowError(
            f"expected exactly one programs.csv row for {school_key}; found {len(targets)}"
        )
    row = targets[0]
    row["history_start_season"] = start_season
    row["history_scope_status"] = "OWNER_CONFIRMED"
    row["history_scope_basis"] = basis
    row["history_scope_notes"] = notes
    row["history_scope_intervals"] = intervals


def accepted_top_level_scope_expression(
    *,
    start_season: str,
    basis: str,
    intervals: str,
) -> str:
    interval_text = (intervals or "").strip()
    basis_text = (basis or "").strip()
    if interval_text:
        return interval_text
    if basis_text == "ALWAYS_TOP_LEVEL_FROM_INCEPTION":
        return "INCEPTION+"
    if basis_text == "FIRST_TOP_LEVEL_SEASON":
        start = (start_season or "").strip()
        match = re.fullmatch(r"(\d{4})-(\d{4})", start)
        if not match:
            raise WorkflowError(
                "FIRST_TOP_LEVEL_SEASON requires a valid YYYY-YYYY history start"
            )
        return f"{match.group(1)}-{match.group(2)[-2:]}+"
    raise WorkflowError(
        "accepted Research Freeze history scope cannot be projected into "
        "program-top-level-scope.csv; provide explicit history_scope_intervals "
        "for TOP_LEVEL_INTERVALS"
    )


def reconcile_top_level_scope_reference(
    rows: list[dict[str, str]],
    target_program: dict[str, str],
    *,
    accepted_scope: str,
) -> dict[str, Any]:
    names = {
        value.strip()
        for value in (
            target_program.get("program_name", ""),
            target_program.get("display_name", ""),
        )
        if value.strip()
    }
    matches = [row for row in rows if row.get("school", "").strip() in names]
    if len(matches) > 1:
        raise WorkflowError(
            "program-top-level-scope.csv has multiple target rows for "
            + "/".join(sorted(names))
        )

    if matches:
        row = matches[0]
        prior = row.get("top_level_scope", "").strip()
        row["top_level_scope"] = accepted_scope
        school = row.get("school", "").strip()
        action = "CONFIRMED" if prior == accepted_scope else "UPDATED"
    else:
        school = (
            target_program.get("display_name", "").strip()
            or target_program.get("program_name", "").strip()
        )
        if not school:
            raise WorkflowError(
                "cannot register target top-level scope without a program/display name"
            )
        prior = ""
        rows.append({"school": school, "top_level_scope": accepted_scope})
        rows.sort(key=lambda item: item.get("school", "").casefold())
        action = "ADDED"

    return {
        "school": school,
        "prior_top_level_scope": prior,
        "accepted_top_level_scope": accepted_scope,
        "action": action,
        "changed": prior != accepted_scope,
    }


def write_top_level_scope_reference(
    path: Path,
    fieldnames: list[str],
    rows: list[dict[str, str]],
) -> None:
    if fieldnames != ["school", "top_level_scope"]:
        raise WorkflowError(
            "unexpected program-top-level-scope.csv fields: "
            + ",".join(fieldnames)
        )
    original = path.read_bytes() if path.exists() else b""
    has_bom = original.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in original else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding=encoding) as handle:
        handle.write("school,top_level_scope" + line_ending)
        writer = csv.writer(
            handle,
            lineterminator=line_ending,
            quoting=csv.QUOTE_ALL,
        )
        for row in rows:
            writer.writerow(
                [row.get("school", ""), row.get("top_level_scope", "")]
            )
    temporary.replace(path)


def package_hashes(root: Path) -> dict[str, str]:
    return {name: sha256_file(root / name) for name in REQUIRED_PACKAGE_FILES}


def ensure_phase0_state(
    repo: Path,
    school_key: str,
    research_base: str,
) -> tuple[str, str]:
    branch = git(repo, "branch", "--show-current").strip()
    if branch != f"data/{school_key}-onboarding":
        raise WorkflowError(
            f"Phase 0 requires branch data/{school_key}-onboarding; "
            f"current={branch or '[detached]'}"
        )
    if git(repo, "status", "--porcelain", "--untracked-files=all").strip():
        raise WorkflowError("Phase 0 requires a clean working tree")
    head = git(repo, "rev-parse", "HEAD").strip()
    origin_main = git(repo, "rev-parse", "origin/main").strip()
    if head != origin_main:
        raise WorkflowError(
            "Phase 0 branch must still point exactly at current origin/main before staging; "
            f"HEAD={head}, origin/main={origin_main}"
        )
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", research_base, head],
        cwd=repo,
    )
    if result.returncode != 0:
        raise WorkflowError(
            f"research_base_sha {research_base} is not an ancestor of current main {head}"
        )
    return head, origin_main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Guarded current-main staging of one RESEARCH_FROZEN portfolio."
    )
    parser.add_argument("school_key")
    parser.add_argument("package", type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--research-base", required=True)
    parser.add_argument("--history-start-season", required=True)
    parser.add_argument("--history-scope-basis", required=True)
    parser.add_argument("--history-scope-intervals", default="")
    parser.add_argument("--history-scope-notes", required=True)
    parser.add_argument("--conference-reconciliation", type=Path, default=None)
    parser.add_argument("--venue-reconciliation", type=Path, default=None)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--commit", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    package = args.package.resolve()

    try:
        if args.commit and not args.apply:
            raise WorkflowError("--commit requires --apply")

        actual_sha = sha256_file(package)
        if actual_sha.lower() != args.expected_sha256.lower():
            raise WorkflowError(
                f"research ZIP SHA-256 mismatch: expected {args.expected_sha256}, "
                f"found {actual_sha}"
            )

        current_head, origin_main = ensure_phase0_state(
            repo,
            args.school_key,
            args.research_base,
        )

        acceptance = research_portfolio_report(
            package,
            school_key=args.school_key,
            expected_sha256=args.expected_sha256,
            allow_venue_summary_reconciliation=True,
        )
        if acceptance["status"] != "PASS":
            for error in acceptance["errors"]:
                print("  - " + error)
            raise WorkflowError(
                "research portfolio acceptance failed with "
                f"{len(acceptance['errors'])} error(s)"
            )

        if (repo / "schools" / args.school_key).exists():
            raise WorkflowError(
                f"schools/{args.school_key} already exists; Phase 0 will not overwrite it"
            )

        with tempfile.TemporaryDirectory(prefix=f"stage-{args.school_key}-") as temporary:
            temp_root = Path(temporary)
            package_root = temp_root / "package"
            package_root.mkdir()
            copy_package(package, package_root)

            local_fields, local_venues = load_csv(package_root / "venues.csv")
            opponent_fields, local_opponents = load_csv(
                package_root / "opponents.csv"
            )
            source_fields, source_games = load_csv(
                package_root / "source-games.csv"
            )
            conference_history_fields, local_conferences = load_csv(
                package_root / "conferences.csv"
            )
            global_fields, global_venues = load_csv(repo / "data/reference/venues.csv")
            name_fields, venue_names = load_csv(repo / "data/reference/venue-names.csv")
            program_fields, programs = load_csv(repo / "data/reference/programs.csv")
            scope_reference_fields, scope_reference_rows = load_csv(
                repo / "data/reference/program-top-level-scope.csv"
            )
            _, program_aliases = load_csv(repo / "data/reference/program-names.csv")
            conference_fields, global_conferences = load_csv(
                repo / "data/reference/conferences.csv"
            )
            existing_school_venues = load_existing_school_venues(
                repo,
                exclude_school_key=args.school_key,
            )

            venue_reconciliation, venue_reconciliation_meta = load_venue_reconciliation(
                args.venue_reconciliation,
                school_key=args.school_key,
                package_path=package,
                local_venues=local_venues,
                global_venues=global_venues,
            )
            replacement_history, conference_registrations, conference_meta = (
                load_conference_reconciliation(
                    args.conference_reconciliation,
                    school_key=args.school_key,
                    conferences_path=package_root / "conferences.csv",
                    local_fields=conference_history_fields,
                )
            )
            if replacement_history is not None:
                local_conferences = replacement_history

            stage1_inventory = build_stage1_reconciliation_inventory(
                args.school_key,
                local_venues,
                global_venues,
                venue_names,
                programs,
                program_aliases,
                local_opponents,
                local_conferences=local_conferences,
                global_conferences=global_conferences,
                conference_registrations=conference_registrations,
                existing_school_venues=existing_school_venues,
                venue_reconciliation=venue_reconciliation,
            )
            stage1_inventory["venue_reconciliation"] = venue_reconciliation_meta
            inventory_path = write_stage1_reconciliation_inventory(
                repo,
                args.school_key,
                stage1_inventory,
            )
            print("Stage 1 reconciliation inventory:")
            print(f"  status: {stage1_inventory['status']}")
            print(f"  blockers: {stage1_inventory['blocker_count']}")
            print(
                "  shared/global maintenance: "
                f"{stage1_inventory['maintenance_required_count']}"
            )
            print(
                "  ambiguous stops: "
                f"{stage1_inventory['ambiguous_stop_count']}"
            )
            print(f"  artifact: {inventory_path}")
            if stage1_inventory["blocker_count"]:
                for row in stage1_inventory["venue"]["blockers"]:
                    print(
                        "  venue blocker: "
                        f"{row['venue_key']} | {row['canonical_name']} | "
                        f"{row['classification']} | "
                        f"{','.join(row['issues'])}"
                    )
                for row in stage1_inventory["program_alias"]["blockers"]:
                    print(
                        "  program blocker: "
                        f"{row['canonical_opponent_name']} | "
                        f"{row['classification']} | "
                        f"{','.join(row['candidate_program_keys'])}"
                    )
                for row in stage1_inventory["conference"]["blockers"]:
                    print(
                        "  conference blocker: "
                        f"{row['conference_key']} | {row['conference_name']} | "
                        f"{row['classification']} | {','.join(row['issues'])}"
                    )
                raise WorkflowError(
                    "Stage 1 reconciliation inventory is not clean. "
                    "Resolve the complete declared blocker/maintenance population "
                    "before retrying Phase 0; do not use repeated staging attempts "
                    "as a discovery loop."
                )

            staged_venue_source_matches: list[dict[str, str]] = []
            (
                local_venues,
                global_venues,
                venue_names,
                mappings,
            ) = rebase_venues(
                args.school_key,
                local_venues,
                global_venues,
                venue_names,
                existing_school_venues=existing_school_venues,
                venue_reconciliation=venue_reconciliation,
                source_games=source_games,
                summary_match_rows_out=staged_venue_source_matches,
            )

            staged_venue_summary = venue_summary_consistency_report(
                source_games,
                local_venues,
                source_match_venues=staged_venue_source_matches,
            )
            if staged_venue_summary["errors"]:
                raise WorkflowError(
                    "post-rebase venue summary consistency failed: "
                    + "; ".join(staged_venue_summary["errors"][:10])
                )

            global_conferences, conference_mappings = register_conferences(
                global_conferences,
                conference_registrations,
            )

            (
                local_opponents,
                source_games,
                program_alias_mappings,
            ) = rebase_program_aliases(
                programs,
                program_aliases,
                local_opponents,
                source_games,
            )

            update_program_scope(
                programs,
                args.school_key,
                start_season=args.history_start_season,
                basis=args.history_scope_basis,
                intervals=args.history_scope_intervals,
                notes=args.history_scope_notes,
            )
            target_program = next(
                row
                for row in programs
                if row.get("program_key") == args.school_key
            )
            accepted_scope_expression = accepted_top_level_scope_expression(
                start_season=args.history_start_season,
                basis=args.history_scope_basis,
                intervals=args.history_scope_intervals,
            )
            scope_reference_result = reconcile_top_level_scope_reference(
                scope_reference_rows,
                target_program,
                accepted_scope=accepted_scope_expression,
            )
            scope_problems = history_scope_errors(target_program, required=True)
            if scope_problems:
                raise WorkflowError(
                    "history scope staging failed: " + "; ".join(scope_problems)
                )

            write_csv_preserving_format(
                package_root / "venues.csv",
                local_fields,
                local_venues,
            )
            write_csv_preserving_format(
                package_root / "opponents.csv",
                opponent_fields,
                local_opponents,
            )
            write_csv_preserving_format(
                package_root / "source-games.csv",
                source_fields,
                source_games,
            )
            write_csv_preserving_format(
                package_root / "conferences.csv",
                conference_history_fields,
                local_conferences,
            )
            notes_path = package_root / "notes.md"
            notes = notes_path.read_text(encoding="utf-8")
            if not notes.endswith("\n"):
                notes += "\n"
            notes += (
                "\n## Integration staging\n\n"
                "Current-main shared-reference rebase completed against "
                f"`integration_base_sha={current_head}` from "
                f"`research_base_sha={args.research_base}`. "
                "The authoritative final venue-ID mapping is recorded in the ignored "
                "`.onboarding/<school>/integration-freeze.json` manifest. "
                "Status: **INTEGRATION_FROZEN**.\n"
            )
            if venue_reconciliation_meta is not None:
                notes += (
                    "\nExplicit Stage 1 venue-identity reconciliation applied; "
                    "the hash-bound spec and historical basis are recorded in "
                    "the Integration Freeze manifest.\n"
                )
            if conference_meta is not None:
                notes += (
                    "\nOwner-authorized Stage 1 conference-history reconciliation "
                    "was applied during current-main integration; the exact correction "
                    "specification and hash are recorded in the Integration Freeze manifest.\n"
                )
            notes_path.write_text(notes, encoding="utf-8")

            staged_hashes = {
                name: sha256_file(package_root / name)
                for name in REQUIRED_PACKAGE_FILES
            }
            semantic_snapshot = build_source_game_semantic_snapshot(
                package_root / "source-games.csv"
            )
            manifest = {
                "schema_version": 2,
                "school_key": args.school_key,
                "status": "INTEGRATION_FROZEN",
                "research_base_sha": args.research_base,
                "integration_base_sha": current_head,
                "origin_main_sha": origin_main,
                "research_zip_sha256": actual_sha,
                "package_member_sha256": staged_hashes,
                "source_game_semantic_guard": {
                    "schema_version": 1,
                    "snapshot_sha256": semantic_snapshot_sha256(semantic_snapshot),
                    "snapshot": semantic_snapshot,
                },
                "venue_mapping": mappings,
                "program_alias_mapping": program_alias_mappings,
                "conference_mapping": conference_mappings,
                "conference_reconciliation": conference_meta,
                "venue_reconciliation": venue_reconciliation_meta,
                "history_scope": {
                    "history_start_season": args.history_start_season,
                    "history_scope_status": "OWNER_CONFIRMED",
                    "history_scope_basis": args.history_scope_basis,
                    "history_scope_intervals": args.history_scope_intervals,
                    "history_scope_notes": args.history_scope_notes,
                    "top_level_scope_reference": scope_reference_result,
                },
            }

            print("College Basketball History — Phase 0 staging")
            print(f"School:                {args.school_key}")
            print(f"Research base:         {args.research_base}")
            print(f"Integration base:      {current_head}")
            print(f"Research ZIP SHA-256:  {actual_sha}")
            print(
                "Top-level scope:        "
                f"{scope_reference_result['accepted_top_level_scope']} "
                f"({scope_reference_result['action']})"
            )
            print(f"Venue rows rebased:    {len(mappings)}")
            print(
                "Semantic freeze rows:  "
                f"{len(semantic_snapshot['rows']):,} "
                f"({semantic_snapshot_sha256(semantic_snapshot)})"
            )
            print(
                f"Program aliases rebased: {len(program_alias_mappings)} "
                f"mapping row(s), "
                f"{sum(row['source_games_rebased'] for row in program_alias_mappings)} "
                "source game(s)"
            )
            print(
                f"Conference registrations: {len(conference_mappings)} mapping row(s)"
            )
            print("Venue outcomes:")
            for key, count in sorted(
                {
                    value: sum(
                        1 for row in mappings if row["resolution"] == value
                    )
                    for value in {row["resolution"] for row in mappings}
                }.items()
            ):
                print(f"  {key}: {count}")

            if not args.apply:
                print(
                    "\nDRY RUN COMPLETE: no repository files changed. "
                    "Rerun with --apply (and normally --commit) after reviewing the mapping."
                )
                return 0

            school_dir = repo / "schools" / args.school_key
            output_dir = repo / ".onboarding" / args.school_key
            output_dir.mkdir(parents=True, exist_ok=True)
            manifest_path = output_dir / "integration-freeze.json"
            protected_paths = [
                repo / "data/reference/programs.csv",
                repo / "data/reference/program-top-level-scope.csv",
                repo / "data/reference/venues.csv",
                repo / "data/reference/venue-names.csv",
                repo / "data/reference/conferences.csv",
                manifest_path,
            ]
            pre_apply_snapshot = snapshot_file_bytes(protected_paths)

            try:
                school_dir.mkdir()
                for name in REQUIRED_PACKAGE_FILES:
                    shutil.copy2(package_root / name, school_dir / name)

                write_csv_preserving_format(
                    repo / "data/reference/programs.csv",
                    program_fields,
                    programs,
                )
                if scope_reference_result["changed"]:
                    write_top_level_scope_reference(
                        repo / "data/reference/program-top-level-scope.csv",
                        scope_reference_fields,
                        scope_reference_rows,
                    )
                write_csv_preserving_format(
                    repo / "data/reference/venues.csv",
                    global_fields,
                    global_venues,
                )
                write_csv_preserving_format(
                    repo / "data/reference/venue-names.csv",
                    name_fields,
                    venue_names,
                )
                write_csv_preserving_format(
                    repo / "data/reference/conferences.csv",
                    conference_fields,
                    global_conferences,
                )

                manifest_path.write_text(
                    json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )

                run(
                    [sys.executable, str(repo / "tools/validate_data.py")],
                    cwd=repo,
                    echo=True,
                )
            except Exception:
                if school_dir.exists():
                    shutil.rmtree(school_dir)
                restore_file_bytes(pre_apply_snapshot)
                raise

        expected_paths = [
            "data/reference/programs.csv",
            "data/reference/program-top-level-scope.csv",
            "data/reference/venues.csv",
            "data/reference/venue-names.csv",
            "data/reference/conferences.csv",
            *[
                f"schools/{args.school_key}/{name}"
                for name in REQUIRED_PACKAGE_FILES
            ],
        ]
        print("\nPASS: Phase 0 files installed and repository validation passed.")
        print(
            "Integration manifest: "
            f"{repo / '.onboarding' / args.school_key / 'integration-freeze.json'}"
        )

        if args.commit:
            git(repo, "add", *expected_paths)
            staged = [
                line.strip()
                for line in git(repo, "diff", "--cached", "--name-only").splitlines()
                if line.strip()
            ]
            unexpected = sorted(set(staged) - set(expected_paths))
            if unexpected:
                raise WorkflowError(
                    "refusing Phase 0 commit with unexpected staged paths: "
                    + ", ".join(unexpected)
                )
            if not staged:
                raise WorkflowError("Phase 0 produced no staged files")
            message = (
                f"Add {args.school_key.replace('-', ' ').title()} onboarding source package"
            )
            git(repo, "commit", "-m", message, echo=True)
            print("\nPHASE 0 CHECKPOINT CREATED")
            print("HEAD: " + git(repo, "rev-parse", "HEAD").strip())
            if git(repo, "status", "--porcelain").strip():
                raise WorkflowError(
                    "Phase 0 checkpoint created but worktree is not clean"
                )
            print("Worktree: clean")
            print(
                f"Next: python tools/onboard_school.py {args.school_key} --preflight"
            )
        else:
            print(
                "Next: explicitly stage and commit the Phase 0 paths before preflight, "
                "or rerun with --commit in a fresh checkout."
            )
        return 0

    except (
        WorkflowError,
        FileNotFoundError,
        KeyError,
        ValueError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
