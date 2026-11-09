#!/usr/bin/env python3
"""Deterministic Research Stage 4 package authoring and closeout.

A current-policy Stage 3B COMPLETE checkpoint carries a small durable
stage4-authoring capsule containing package-ready opponents.csv, venues.csv,
and conferences.csv. This command projects the accepted Stage 3B ledger into
source-games.csv, generates notes from durable checkpoint evidence, and then
invokes the permanent Stage 4 closeout.

It does not research, consult current registries, or reconstruct missing
historical authority. Missing authoring state is an explicit prior-stage stop.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from research_authoring_capsule import checkpoint_continuity_defects
from research_stage3a4_accounting import (
    reconcile_opponent_home_outside_responsibility,
)

from research_stage4_closeout import (
    closeout,
    first_literal,
    normalize_game_type,
    normalize_site,
    project_administrative_status,
    project_game_id,
    project_season_label,
    explicit_opponent_home_site,
    resolve_stage3b_parent_layout,
    sha256_bytes,
    validate_checkpoint_manifest,
    write_json,
)

AUTHORING_DIR = "stage4-authoring"
AUTHORING_FILES = ("opponents.csv", "venues.csv", "conferences.csv")
EARLY_HISTORY_AUTHORING_FILE = "early-history-uncertainty.json"
AGGREGATE_COVERAGE_AUTHORING_FILE = "season-coverage.json"

OPPONENT_FIELDS = {
    "source_program_key",
    "source_opponent_label",
    "canonical_opponent_key",
    "canonical_opponent_name",
    "current_d1",
    "games_with_source_label",
    "first_season",
    "last_season",
    "resolution_status",
    "resolution_method",
    "user_choice",
    "audit_note",
}
VENUE_FIELDS = {
    "source_program_key",
    "venue_key",
    "venue_id",
    "canonical_name",
    "aliases",
    "city",
    "state",
    "venue_type",
    "known_opened",
    "known_closed",
    "venue_date_precision",
    "games_currently_assigned",
    "first_assigned_game",
    "last_assigned_game",
    "relationship_type",
    "relationship_start",
    "relationship_end",
    "relationship_date_precision",
    "site_rule",
    "source_basis",
    "notes",
}
CONFERENCE_FIELDS = {
    "source_program_key",
    "start_season",
    "end_season",
    "conference_key",
    "conference_name",
    "membership_type",
    "ongoing",
    "basis",
    "notes",
}
SOURCE_GAME_FIELDS = [
    "source_game_id",
    "source_program_key",
    "source_era",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_key",
    "normalized_opponent_name",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "source_site_candidate",
    "curated_site_type",
    "source_venue_name",
    "curated_venue_name",
    "city",
    "state",
    "country",
    "event_or_tournament",
    "source_round",
    "curated_game_type",
    "curated_postseason_round",
    "source_page",
    "raw_text",
    "normalization_status",
    "administrative_status",
    "administrative_note",
    "notes",
    "site_research_status",
    "site_research_basis",
]
ALLOWED_RESEARCH_STATUSES = {
    "RESEARCHED_PARTIAL",
    "RESEARCHED_UNRESOLVED",
    "RESEARCHED_UNRESOLVED_HOME_VENUE",
}
D1_VALUES = {"yes", "true", "1", "y", "d1", "current_d1", "current-d1"}
NON_D1_VALUES = {"no", "false", "0", "n", "non_d1", "non-d1", "non d1"}


def _csv_bytes(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""))
    return list(reader.fieldnames or []), list(reader)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def _first(row: dict[str, str], *fields: str) -> str:
    for field in fields:
        value = row.get(field, "").strip()
        if value:
            return value
    return ""


def _research_accounting(
    row: dict[str, str],
) -> tuple[str, str]:
    """Project accepted research-accounting fields across schema generations.

    Legacy Stage 3A ledgers may split H/A/N accounting from venue accounting.
    Skip resolved/nonterminal status values and preserve the first actual
    research-debt status together with its matching basis instead of letting
    an unrelated resolved status mask a later unresolved one.
    """

    candidates = (
        (
            "stage3b_site_research_status",
            ("stage3b_site_research_basis",),
        ),
        (
            "stage3b_postseason_han_status",
            ("stage3b_postseason_han_basis",),
        ),
        (
            "stage3a_site_research_status",
            ("stage3a_site_research_basis",),
        ),
        (
            "site_research_status",
            ("site_research_basis",),
        ),
        (
            "han_research_status",
            ("han_research_note", "han_research_basis"),
        ),
        (
            "venue_research_status",
            ("venue_research_note", "venue_research_basis"),
        ),
        (
            "stage3a1_status",
            ("stage3a1_evidence_basis", "stage3a1_review_notes"),
        ),
    )
    for status_field, basis_fields in candidates:
        status = row.get(status_field, "").strip().upper()
        if status not in ALLOWED_RESEARCH_STATUSES:
            continue
        return status, _first(row, *basis_fields)

    # Accepted current-transition Stage 3 statuses may encode terminal research
    # debt with a prefixed workflow vocabulary rather than the controlled
    # six-file status tokens. Translate only the narrow semantic shapes already
    # established by the parent row; unrelated or active status strings remain
    # fail-closed.
    site = normalize_site(_first(
        row, "curated_site_type", "stage3b_site_type",
        "stage3a_final_site_type", "stage3a_final_han", "site_type",
    ))
    game_type = normalize_game_type(_first(
        row, "curated_game_type", "game_type", "structured_game_type",
    ))
    accepted_venue = _first(
        row, "stage3b_physical_venue_name", "stage3b_curated_venue_name",
        "stage3a_final_physical_venue_name", "stage3a_final_venue_name",
        "accepted_venue_name", "stage3a_curated_venue_name",
        "stage3a2_physical_venue_name", "stage3a3_physical_venue_name",
        "curated_venue_name", "venue_name",
    )

    legacy_han_status = row.get("site_research_status", "").strip().upper()
    legacy_han_basis = row.get("site_research_basis", "").strip()
    if legacy_han_status.startswith("STAGE3A1_RESEARCHED_UNRESOLVED_"):
        if (
            game_type == "REGULAR_SEASON"
            and site == "UNKNOWN"
            and not accepted_venue
            and legacy_han_basis
        ):
            return "RESEARCHED_UNRESOLVED", legacy_han_basis
        return "", ""

    legacy_venue_status = row.get("venue_research_status", "").strip().upper()
    legacy_venue_basis = row.get("venue_research_basis", "").strip()
    if legacy_venue_status == "RESEARCHED_UNRESOLVED_STAGE3A3_HISTORICAL_LOCALITY":
        season = _first(row, "season_label", "season")
        if (
            game_type == "REGULAR_SEASON"
            and site == "NEUTRAL"
            and not accepted_venue
            and season[:4].isdigit()
            and int(season[:4]) <= 1995
            and legacy_venue_basis
        ):
            return "RESEARCHED_UNRESOLVED", legacy_venue_basis
        return "", ""

    if legacy_venue_status in {
        "RESEARCHED_UNRESOLVED_STAGE3A3_MODERN_ONEOFF_EXACT_VENUE",
        "RESEARCHED_UNRESOLVED_STAGE3A3_MODERN_RECURRING_EXACT_VENUE",
    }:
        season = _first(row, "season_label", "season")
        city = _first(
            row, "curated_venue_city", "curated_city", "city", "venue_city"
        )
        state = _first(
            row, "curated_venue_state", "curated_state", "state", "venue_state"
        )
        if (
            game_type == "REGULAR_SEASON"
            and site == "NEUTRAL"
            and not accepted_venue
            and season[:4].isdigit()
            and int(season[:4]) >= 1996
            and city
            and state
            and legacy_venue_basis
        ):
            return "RESEARCHED_UNRESOLVED", legacy_venue_basis
        return "", ""

    # Accepted historical-location-only neutral building debt is not a new
    # absence of research.  Preserve the exact checkpoint basis, not merely
    # a generic status inferred from the missing building.
    historical = row.get("neutral_venue_research_status", "").strip().upper()
    if historical == "HISTORICAL_LOCATION_ACCEPTED_EXACT_BUILDING_ENRICHMENT_UNRESOLVED":
        site = normalize_site(_first(row, "curated_site_type", "stage3b_site_type",
                                    "stage3a_final_site_type", "site_type"))
        game_type = normalize_game_type(_first(row, "curated_game_type",
                                               "game_type", "structured_game_type"))
        season = _first(row, "season_label", "season")
        city = _first(row, "curated_venue_city", "curated_city", "city")
        state = _first(row, "curated_venue_state", "curated_state", "state")
        venue = _first(row, "curated_venue_name", "accepted_venue_name")
        basis = _first(row, "neutral_venue_research_basis")
        if (game_type == "REGULAR_SEASON" and site == "NEUTRAL"
                and season[:4].isdigit() and int(season[:4]) <= 1995
                and city and state and not venue and basis):
            return "RESEARCHED_PARTIAL", (
                f"Accepted historical-neutral location {city}, {state}: {basis}; "
                "exact-building enrichment remains unresolved under location-first policy."
            )
        return "", ""  # Projection parity preflight will fail this unsupported shape.

    # Narrow owner-approved campus-road conference-tournament boundary.
    # This is NOT a claim of exhaustive venue research, or a general waiver
    # for NIT/NCAA/neutral/postseason sites.
    postseason = row.get("postseason_site_research_status", "").strip().upper()
    if postseason == "OPPONENT_HOME_VENUE_OUTSIDE_TARGET_RESEARCH_RESPONSIBILITY":
        site = normalize_site(_first(row, "curated_site_type", "stage3b_site_type",
                                    "stage3a_final_site_type", "site_type"))
        game_type = normalize_game_type(_first(row, "curated_game_type",
                                               "game_type", "structured_game_type"))
        basis = _first(row, "postseason_site_research_basis")
        shared_row = _first(row, "postseason_shared_ref_source_row")
        if (site == "OPPONENT_HOME" and game_type == "CONFERENCE_TOURNAMENT"
                and basis.startswith("OWNER_EXPLICIT_NEC_ROAD_SITE_SCOPE")
                and shared_row):
            return "RESEARCHED_PARTIAL", (
                "Owner-approved NEC campus-hosted road conference-tournament "
                f"opponent-building research exclusion: {basis}; shared site "
                f"reference row {shared_row}; not claimed research-exhausted."
            )
        return "", ""  # Fail closed for unrelated game/site/research shapes.

    # Preserve terminal historical site research across accepted schema eras.
    # The site classification, locality and blank venue must all be accepted;
    # never apply the historical building exception to postseason or modern rows.
    site = normalize_site(_first(
        row, "curated_site_type", "stage3b_site_type",
        "stage3a_final_site_type", "stage3a_final_han", "site_type",
    ))
    game_type = normalize_game_type(_first(
        row, "curated_game_type", "game_type", "structured_game_type",
    ))
    accepted_venue = _first(
        row, "stage3b_physical_venue_name", "stage3b_curated_venue_name",
        "stage3a_final_physical_venue_name", "stage3a_final_venue_name",
        "accepted_venue_name", "stage3a_curated_venue_name",
        "stage3a2_physical_venue_name", "stage3a3_physical_venue_name",
        "curated_venue_name", "venue_name",
    )
    if game_type == "REGULAR_SEASON" and site == "NEUTRAL" and not accepted_venue:
        modern_status = _first(row, "stage3a3_modern_recurring_status")
        if modern_status.startswith("RESEARCHED_UNRESOLVED_EXACT_VENUE"):
            basis = _first(row, "stage3a3_modern_recurring_provenance")
            if basis:
                notes = _first(row, "stage3a3_modern_recurring_notes")
                return "RESEARCHED_UNRESOLVED", (
                    f"Accepted Stage 3A-3 modern tournament evidence: {basis}"
                    + (f"; {notes}" if notes else "")
                )
        season = _first(row, "season_label", "season")
        city = _first(row, "stage3a_final_city", "accepted_city",
                      "curated_venue_city", "curated_city", "city", "venue_city")
        state = _first(row, "stage3a_final_state", "accepted_state",
                       "curated_venue_state", "curated_state", "state", "venue_state")
        if season[:4].isdigit() and int(season[:4]) <= 1995 and city and state:
            basis = _first(
                row, "stage3a3_historical_evidence_basis",
                "venue_research_basis", "site_research_basis",
            )
            if basis:
                return "RESEARCHED_PARTIAL", (
                    f"Accepted Stage 3A-3 historical neutral location {city}, {state}: "
                    f"{basis}; exact building not established under location-first policy."
                )
            return "RESEARCHED_PARTIAL", (
                f"Accepted Stage 3A neutral location {city}, {state}; "
                "exact physical building not established and is historical "
                "enrichment debt under the location-first research standard."
            )

    # Opponent-home venue archaeology is outside the source-school obligation.
    # Preserve the literal label instead of inventing a physical identity from
    # shorthand such as (MSG), (NY), or (Palestra). The accepted source was
    # already examined for H/A/N in Stage 3A-1.
    if game_type == "REGULAR_SEASON" and site == "OPPONENT_HOME":
        literal = _first(row, "source_venue_name")
        if literal and not explicit_opponent_home_site(row):
            source_basis = _first(row, "stage3a1_evidence_basis")
            if source_basis:
                return "RESEARCHED_PARTIAL", (
                    f"Accepted opponent-home source label {literal!r} retained "
                    "without asserting an unidentified physical venue or locality; "
                    f"Stage 3A-1 institutional H/A/N evidence: {source_basis}. "
                    "Opponent-home building archaeology remains outside this "
                    "source-school's Research obligation."
                )
    return "", ""


def _project_overtime(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.isdigit():
        return value
    match = re.fullmatch(r"(?:(\d+))?OT", value.upper())
    if match:
        return match.group(1) or "1"
    return value


_LEGACY_LITERAL_SCORE_RESULT_RE = re.compile(
    r"(?<!\d)(?P<a>\d{1,3})\s+(?P<b>\d{1,3})\s+(?P<result>[WLT])\s*$",
    re.IGNORECASE,
)
_LEGACY_LITERAL_SCORE_PAIR_RE = re.compile(
    r"(?<!\d)(?P<a>\d{1,3})\s+(?P<b>\d{1,3})(?!\d)"
)


def _score_result_consistent(team: int, opponent: int, result: str) -> bool:
    result = (result or "").strip().upper()
    if result == "W":
        return team > opponent
    if result == "L":
        return team < opponent
    if result == "T":
        return team == opponent
    return False


def _legacy_score_projection(
    row: dict[str, str],
    *,
    game_id: str,
) -> tuple[str, str, str, list[dict[str, Any]]]:
    """Project an accepted legacy positional score pair into team/opponent order.

    This is deliberately fail-closed. Current-schema team/opponent fields are
    never reinterpreted. A legacy row is eligible only when it carries the older
    research-ledger topology (season rather than season_label and no
    source_program_key), the accepted W/L/T conflicts with the current numeric
    orientation, and the preserved source literal ends with exactly the same two
    accepted numbers plus the same result token. The unordered numeric pair and
    played result remain unchanged; only package-field orientation changes.
    """

    team = _first(row, "team_score", "wagner_points", "dayton_score", "source_points_for")
    opponent = _first(row, "opponent_score", "opponent_points", "source_points_against")
    result = _first(
        row, "played_result", "on_court_result", "source_result", "result"
    ).upper()
    if not team or not opponent:
        return team, opponent, "", []
    if not (team.isdigit() and opponent.isdigit()) or result not in {"W", "L", "T"}:
        return team, opponent, "", []

    team_value = int(team)
    opponent_value = int(opponent)
    if _score_result_consistent(team_value, opponent_value, result):
        return team, opponent, "", []

    legacy_topology = (
        bool(row.get("research_game_id", "").strip())
        and bool(row.get("season", "").strip())
        and not row.get("season_label", "").strip()
        and not row.get("source_program_key", "").strip()
    )
    raw_text = first_literal(row, "raw_text", "source_raw_text", "source_entry_literal")
    literal = _LEGACY_LITERAL_SCORE_RESULT_RE.search(raw_text)
    literal_pairs = [
        (int(match.group("a")), int(match.group("b")))
        for match in _LEGACY_LITERAL_SCORE_PAIR_RE.finditer(raw_text)
    ]
    accepted_pair = sorted((team_value, opponent_value))
    if (
        not legacy_topology
        or literal is None
        or literal.group("result").upper() != result
        or sorted((int(literal.group("a")), int(literal.group("b")))) != accepted_pair
        or len(literal_pairs) != 1
        or sorted(literal_pairs[0]) != accepted_pair
    ):
        return team, opponent, "", [
            {
                "reason": "LEGACY_SCORE_ORIENTATION_AMBIGUOUS",
                "source_game_id": game_id,
                "team_score": team,
                "opponent_score": opponent,
                "played_result": result,
            }
        ]

    if result == "T":
        return team, opponent, "", [
            {
                "reason": "LEGACY_SCORE_ORIENTATION_AMBIGUOUS",
                "source_game_id": game_id,
                "team_score": team,
                "opponent_score": opponent,
                "played_result": result,
            }
        ]

    projected_team = (
        max(team_value, opponent_value)
        if result == "W"
        else min(team_value, opponent_value)
    )
    projected_opponent = (
        min(team_value, opponent_value)
        if result == "W"
        else max(team_value, opponent_value)
    )
    note = (
        "Stage 4 legacy score-orientation compatibility: preserved accepted "
        f"unordered score pair {{{min(accepted_pair)}, {max(accepted_pair)}}} and "
        f"played_result={result}; source literal {raw_text!r} deterministically "
        "orients package team_score/opponent_score without changing the parent ledger."
    )
    return str(projected_team), str(projected_opponent), note, []


def _norm_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def _coverage_declaration(
    status: dict[str, Any],
    *,
    primary_source_historical_cutoff: str = "",
    required_completed_season_cutoff: str = "",
) -> tuple[dict[str, str], list[dict[str, Any]]]:
    nested = status.get("research_coverage", {})
    if not isinstance(nested, dict):
        nested = {}
    primary = (
        primary_source_historical_cutoff.strip()
        or str(status.get("primary_source_historical_cutoff", "")).strip()
        or str(nested.get("primary_source_historical_cutoff", "")).strip()
    )
    required = (
        required_completed_season_cutoff.strip()
        or str(status.get("required_completed_season_cutoff", "")).strip()
        or str(nested.get("required_completed_season_cutoff", "")).strip()
    )
    defects: list[dict[str, Any]] = []
    normalized: dict[str, str] = {
        "primary_source_historical_cutoff": "",
        "required_completed_season_cutoff": "",
    }
    for key, value in (
        ("primary_source_historical_cutoff", primary),
        ("required_completed_season_cutoff", required),
    ):
        if not value:
            defects.append(
                {
                    "reason": "RESEARCH_COVERAGE_DECLARATION_MISSING",
                    "field": key,
                }
            )
            continue
        try:
            normalized[key] = project_season_label(value)
        except ValueError:
            defects.append(
                {
                    "reason": "INVALID_RESEARCH_COVERAGE_SEASON",
                    "field": key,
                    "value": value,
                }
            )
    if all(normalized.values()) and int(
        normalized["required_completed_season_cutoff"][:4]
    ) < int(normalized["primary_source_historical_cutoff"][:4]):
        defects.append(
            {
                "reason": "REQUIRED_COVERAGE_PRECEDES_PRIMARY_SOURCE_CUTOFF",
                **normalized,
            }
        )
    return normalized, defects


def _manifest_names(manifest: dict[str, Any]) -> set[str]:
    files = manifest.get("files", {})
    if isinstance(files, list):
        return {
            str(item.get("name", ""))
            for item in files
            if isinstance(item, dict) and item.get("name")
        }
    if isinstance(files, dict):
        return {str(name) for name in files}
    return set()


def _table_defects(
    fields: list[str],
    rows: list[dict[str, str]],
    required: set[str],
    *,
    school_key: str,
    table: str,
) -> list[dict[str, Any]]:
    defects: list[dict[str, Any]] = []
    missing = sorted(required - set(fields))
    if missing:
        defects.append({"reason": "MISSING_COLUMNS", "table": table, "columns": missing})
    for line, row in enumerate(rows, start=2):
        owner = row.get("source_program_key", "").strip()
        if owner and owner != school_key:
            defects.append(
                {
                    "reason": "WRONG_SOURCE_PROGRAM",
                    "table": table,
                    "line": line,
                    "source_program_key": owner,
                }
            )
    return defects


def _projection(
    ledger: list[dict[str, str]],
    opponents: list[dict[str, str]],
    venues: list[dict[str, str]],
    *,
    school_key: str = "",
    opponent_home_outside_responsibility: dict[str, dict[str, str]] | None = None,
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
    opponent_home_outside_responsibility = (
        opponent_home_outside_responsibility or {}
    )
    names: dict[str, set[str]] = defaultdict(set)
    for row in opponents:
        key = row.get("canonical_opponent_key", "").strip()
        name = row.get("canonical_opponent_name", "").strip()
        if key and name:
            names[key].add(name)

    canonical_name: dict[str, str] = {}
    defects: list[dict[str, Any]] = []
    for key, values in names.items():
        if len(values) != 1:
            defects.append(
                {
                    "reason": "OPPONENT_CANONICAL_NAME_CONFLICT",
                    "canonical_opponent_key": key,
                    "names": sorted(values),
                }
            )
        else:
            canonical_name[key] = next(iter(values))

    venues_by_key: dict[str, list[dict[str, str]]] = defaultdict(list)
    for venue in venues:
        venue_key = venue.get("venue_key", "").strip()
        if venue_key:
            venues_by_key[venue_key].append(venue)

    projected: list[dict[str, str]] = []
    seen: set[str] = set()
    for row in ledger:
        game_id = project_game_id(row)
        if not game_id:
            defects.append({"reason": "BLANK_GAME_ID"})
            continue
        if game_id in seen:
            defects.append({"reason": "DUPLICATE_GAME_ID", "source_game_id": game_id})
            continue
        seen.add(game_id)

        opponent_key = _first(
            row,
            "normalized_opponent_key",
            "opponent_program_key",
            "opponent_key",
            "canonical_opponent_key",
        )
        opponent_name = canonical_name.get(opponent_key, "")
        if not opponent_name:
            defects.append(
                {
                    "reason": "OPPONENT_AUTHORITY_MISSING",
                    "source_game_id": game_id,
                    "canonical_opponent_key": opponent_key,
                }
            )

        research_status, research_basis = _research_accounting(row)
        source_round, curated_round, round_note = _round_projection(row)
        literal_opponent_home = explicit_opponent_home_site(row)

        accepted_venue_key = _first(row, "accepted_venue_key")
        accepted_venue: dict[str, str] = {}
        if accepted_venue_key:
            candidates = venues_by_key.get(accepted_venue_key, [])
            if len(candidates) != 1:
                defects.append(
                    {
                        "reason": "ACCEPTED_VENUE_KEY_NOT_UNIQUE",
                        "source_game_id": game_id,
                        "accepted_venue_key": accepted_venue_key,
                        "matches": len(candidates),
                    }
                )
            else:
                accepted_venue = candidates[0]

        if not research_status:
            supplemental = opponent_home_outside_responsibility.get(game_id)
            source_token = _first(row, "source_venue_token")
            accepted_physical_venue = _first(
                row,
                "stage3b_physical_venue_name",
                "stage3b_curated_venue_name",
                "stage3a_final_physical_venue_name",
                "stage3a_final_venue_name",
                "accepted_venue_name",
                "stage3a_curated_venue_name",
                "stage3a2_physical_venue_name",
                "stage3a3_physical_venue_name",
                "curated_venue_name",
                "venue_name",
            )
            if (
                supplemental
                and source_token
                and not accepted_physical_venue
                and not accepted_venue
            ):
                research_status = "RESEARCHED_PARTIAL"
                research_basis = supplemental.get("basis", "")

        administrative_status, administrative_note = (
            project_administrative_status(row)
        )
        projected_team_score, projected_opponent_score, score_note, score_defects = (
            _legacy_score_projection(row, game_id=game_id)
        )
        defects.extend(score_defects)

        projected.append(
            {
                "source_game_id": game_id,
                "source_program_key": _first(row, "source_program_key") or school_key,
                "source_era": _first(row, "source_era", "season_source"),
                "season_label": project_season_label(
                    _first(row, "season_label", "season")
                ),
                "game_date": _first(row, "game_date"),
                "source_opponent_label": _first(
                    row,
                    "source_opponent_label",
                    "source_opponent_text",
                    "source_opponent_field",
                ),
                "normalized_opponent_key": opponent_key,
                "normalized_opponent_name": opponent_name,
                "team_score": projected_team_score,
                "opponent_score": projected_opponent_score,
                "played_result": _first(
                    row,
                    "played_result",
                    "on_court_result",
                    "source_result",
                    "result",
                ),
                "overtime_periods": _project_overtime(
                    _first(row, "overtime_periods", "overtime", "source_overtime_token")
                ),
                "source_site_candidate": _first(
                    row, "source_site_candidate", "source_site_token"
                ),
                "curated_site_type": normalize_site(
                    _first(
                        row,
                        "curated_site_type",
                        "stage3b_site_type",
                        "stage3a_final_site_type",
                        "stage3a_final_han",
                        "site_type",
                    )
                ),
                "source_venue_name": _first(row, "source_venue_name", "source_venue_token"),
                "curated_venue_name": _first(
                    row,
                    "stage3b_physical_venue_name",
                    "stage3b_curated_venue_name",
                    "stage3a_final_physical_venue_name",
                    "stage3a_final_venue_name",
                    "accepted_venue_name",
                    "stage3a_curated_venue_name",
                    "stage3a2_physical_venue_name",
                    "stage3a3_physical_venue_name",
                    "curated_venue_name",
                    "venue_name",
                )
                or accepted_venue.get("canonical_name", "").strip()
                or (literal_opponent_home[0] if literal_opponent_home else ""),
                "city": _first(
                    row,
                    "stage3b_venue_city",
                    "stage3b_site_city",
                    "curated_venue_city",
                    "stage3a_final_venue_city",
                    "stage3a_final_city",
                    "accepted_city",
                    "stage3a_site_city",
                    "stage3a2_venue_city",
                    "stage3a3_venue_city",
                    "curated_city",
                    "city",
                    "venue_city",
                )
                or accepted_venue.get("city", "").strip()
                or (literal_opponent_home[1] if literal_opponent_home else ""),
                "state": _first(
                    row,
                    "stage3b_venue_state",
                    "stage3b_site_state",
                    "curated_venue_state",
                    "stage3a_final_venue_state",
                    "stage3a_final_state",
                    "accepted_state",
                    "stage3a_site_state",
                    "stage3a2_venue_state",
                    "stage3a3_venue_state",
                    "curated_state",
                    "state",
                    "venue_state",
                )
                or accepted_venue.get("state", "").strip()
                or (literal_opponent_home[2] if literal_opponent_home else ""),
                "country": _first(
                    row, "curated_venue_country", "country", "venue_country"
                ),
                "event_or_tournament": _first(
                    row, "event_or_tournament", "stage3a3_event_name"
                ),
                "source_round": source_round,
                "curated_game_type": normalize_game_type(
                    _first(row, "curated_game_type", "game_type", "structured_game_type")
                ),
                "curated_postseason_round": curated_round,
                "source_page": _first(row, "source_page", "source_pdf_page", "source_locator"),
                "raw_text": first_literal(
                    row, "raw_text", "source_raw_text", "source_entry_literal"
                ),
                "normalization_status": _first(row, "normalization_status")
                or "RESEARCH_ACCEPTED",
                "administrative_status": administrative_status,
                "administrative_note": administrative_note,
                "notes": " ".join(part for part in (
                    _first(row, "notes", "stage1_notes"), round_note, score_note
                ) if part),
                "site_research_status": research_status,
                "site_research_basis": research_basis if research_status else "",
            }
        )
        defects.extend(_semantic_projection_defects(row, projected[-1]))
    return projected, defects


def _round_projection(row: dict[str, str]) -> tuple[str, str, str]:
    """Preserve accepted postseason detail without violating controlled round vocab.

    For non-NCAA tournaments only Championship belongs in the curated field;
    earlier-round detail remains in source_round and, if source wording differs,
    in notes.  First Four -> Play-in is controlled-vocabulary normalization.
    """
    game_type = normalize_game_type(_first(row, "curated_game_type",
                                           "game_type", "structured_game_type"))
    accepted = _first(row, "curated_postseason_round",
                      "stage3b_postseason_round", "postseason_round")
    source = _first(row, "source_round", "stage3b_source_round")
    if game_type == "NCAA_TOURNAMENT":
        curated = "Play-in" if accepted == "First Four" else accepted
    elif game_type in {"CONFERENCE_TOURNAMENT", "NIT", "POSTSEASON"}:
        curated = accepted if accepted == "Championship" else ""
    else:
        curated = ""
    evidence_note = (
        f"Accepted Stage 3B postseason round: {accepted}."
        if accepted and accepted != curated and source and accepted != source
        else ""
    )
    return source or accepted, curated, evidence_note


def _semantic_projection_defects(
    parent: dict[str, str], projected: dict[str, str],
) -> list[dict[str, str]]:
    """Independent population-level anti-loss checks for accepted source facts."""
    pairs = {
        "season_label": ("season_label", "season"),
        "team_score": ("team_score", "wagner_points", "dayton_score", "source_points_for"),
        "opponent_score": ("opponent_score", "opponent_points", "source_points_against"),
        "played_result": (
            "played_result",
            "on_court_result",
            "source_result",
            "result",
        ),
        "source_page": ("source_page", "source_pdf_page", "source_locator"),
        "overtime_periods": ("overtime_periods", "overtime", "source_overtime_token"),
        "source_venue_name": ("source_venue_name", "source_venue_token"),
        "raw_text": ("raw_text", "source_raw_text", "source_entry_literal"),
    }
    defects = []
    game_id = projected["source_game_id"]
    for target, aliases in pairs.items():
        original = (
            first_literal(parent, *aliases)
            if target == "raw_text"
            else _first(parent, *aliases)
        )
        if not original:
            continue
        if target == "season_label":
            expected = project_season_label(original)
        elif target == "overtime_periods":
            expected = _project_overtime(original)
        else:
            expected = original
        if projected[target] != expected:
            if target in {"team_score", "opponent_score"}:
                original_team = _first(
                    parent, "team_score", "wagner_points", "dayton_score", "source_points_for"
                )
                original_opponent = _first(
                    parent, "opponent_score", "opponent_points", "source_points_against"
                )
                projected_team = projected.get("team_score", "").strip()
                projected_opponent = projected.get("opponent_score", "").strip()
                if all(value.isdigit() for value in (
                    original_team,
                    original_opponent,
                    projected_team,
                    projected_opponent,
                )):
                    unordered_preserved = sorted(
                        (int(original_team), int(original_opponent))
                    ) == sorted(
                        (int(projected_team), int(projected_opponent))
                    )
                    result = projected.get("played_result", "").strip().upper()
                    if unordered_preserved and _score_result_consistent(
                        int(projected_team), int(projected_opponent), result
                    ):
                        continue
            defects.append({"reason": "ACCEPTED_SOURCE_FIELD_LOST",
                            "source_game_id": game_id, "field": target})

    accepted_round = _first(parent, "curated_postseason_round",
                            "stage3b_postseason_round", "postseason_round")
    if accepted_round and all(
        accepted_round not in projected[field]
        for field in ("source_round", "curated_postseason_round", "notes")
    ):
        defects.append({"reason": "ACCEPTED_POSTSEASON_ROUND_LOST",
                        "source_game_id": game_id})
    for source_status in (
        "neutral_venue_research_status", "postseason_site_research_status"
    ):
        if parent.get(source_status, "").strip().upper() in {
            "HISTORICAL_LOCATION_ACCEPTED_EXACT_BUILDING_ENRICHMENT_UNRESOLVED",
            "OPPONENT_HOME_VENUE_OUTSIDE_TARGET_RESEARCH_RESPONSIBILITY",
        } and (not projected["site_research_status"]
               or not projected["site_research_basis"]):
            defects.append({"reason": "ACCEPTED_SITE_RESEARCH_ACCOUNTING_LOST",
                            "source_game_id": game_id, "field": source_status})
    return defects


def _opponent_home_accounting_projection_defects(
    games: list[dict[str, str]],
    reconciled: dict[str, dict[str, str]],
) -> list[dict[str, str]]:
    """Guard package accounting for reconciled material opponent-home literals."""

    defects: list[dict[str, str]] = []
    for game in games:
        game_id = game.get("source_game_id", "").strip()
        item = reconciled.get(game_id)
        if not item:
            continue
        if (
            normalize_game_type(game.get("curated_game_type", "")) != "REGULAR_SEASON"
            or normalize_site(game.get("curated_site_type", "")) != "OPPONENT_HOME"
        ):
            continue
        if (
            not game.get("source_venue_name", "").strip()
            or game.get("curated_venue_name", "").strip()
        ):
            continue
        expected_basis = item.get("basis", "").strip()
        if (
            game.get("site_research_status", "").strip() != "RESEARCHED_PARTIAL"
            or game.get("site_research_basis", "").strip() != expected_basis
        ):
            defects.append(
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_PACKAGE_ACCOUNTING_LOST",
                    "source_game_id": game_id,
                }
            )
    return defects


def _mapping_defects(
    games: list[dict[str, str]],
    opponents: list[dict[str, str]],
) -> list[dict[str, Any]]:
    allowed = {
        (
            row.get("source_opponent_label", "").strip(),
            row.get("canonical_opponent_key", "").strip(),
        )
        for row in opponents
    }
    return [
        {
            "reason": "SOURCE_LABEL_OPPONENT_MAPPING_MISSING",
            "source_game_id": row["source_game_id"],
            "source_opponent_label": row["source_opponent_label"],
            "canonical_opponent_key": row["normalized_opponent_key"],
        }
        for row in games
        if (
            row["source_opponent_label"],
            row["normalized_opponent_key"],
        )
        not in allowed
    ]


def _venue_defects(
    games: list[dict[str, str]],
    venues: list[dict[str, str]],
) -> list[dict[str, Any]]:
    names: set[str] = set()
    for row in venues:
        canonical = row.get("canonical_name", "").strip()
        if canonical:
            names.add(_norm_name(canonical))
        for alias in row.get("aliases", "").split(";"):
            alias = alias.strip()
            if alias:
                names.add(_norm_name(alias))
    return [
        {
            "reason": "CURATED_VENUE_NOT_IN_AUTHORING_TABLE",
            "source_game_id": row["source_game_id"],
            "curated_venue_name": row["curated_venue_name"],
        }
        for row in games
        if row["curated_venue_name"]
        and _norm_name(row["curated_venue_name"]) not in names
    ]


def _notes(
    school_key: str,
    parent_sha: str,
    status: dict[str, Any],
    games: list[dict[str, str]],
    coverage: dict[str, str],
) -> str:
    types = Counter(row["curated_game_type"] for row in games)
    sites = Counter(row["curated_site_type"] for row in games)
    lines = [
        f"# {school_key} research package notes",
        "",
        "## Stage 4 deterministic authoring",
        "",
        f"- Stage 3B checkpoint SHA-256: {parent_sha}",
        f"- Research base SHA: {status.get('research_base_sha', '')}",
        f"- Stage 3B status: {status.get('status', '')}",
        f"- Competitive games: {len(games):,}",
        f"- Primary-source historical results cutoff: {coverage['primary_source_historical_cutoff']}",
        f"- Required completed-season cutoff: {coverage['required_completed_season_cutoff']}",
        "- Coverage cutoffs are explicit Research declarations; media-guide titles and filenames are not coverage inference rules.",
        "- Package authoring was mechanical from durable Stage 3B state; no historical research or reinterpretation was performed by Stage 4.",
        "",
        "## Final game census",
        "",
    ]
    lines.extend(f"- {key or '[blank]'}: {count:,}" for key, count in sorted(types.items()))
    lines.extend(["", "## Final H/A/N census", ""])
    lines.extend(f"- {key or '[blank]'}: {count:,}" for key, count in sorted(sites.items()))
    return "\n".join(lines) + "\n"


def _source_notes(
    school_key: str,
    ledger: list[dict[str, str]],
    archive: zipfile.ZipFile,
    prefix: str,
    coverage: dict[str, str],
    early_history: dict[str, Any] | None = None,
    aggregate_coverage: dict[str, Any] | None = None,
) -> str:
    kinds = Counter(
        _first(row, "source_kind")
        for row in ledger
        if _first(row, "source_kind")
    )
    urls = sorted(
        {
            _first(row, "source_url")
            for row in ledger
            if _first(row, "source_url")
        }
    )
    lines = [
        f"# {school_key} source notes",
        "",
        "Generated mechanically from durable Research checkpoint evidence. Literal row-level evidence remains preserved in source-games.csv.",
        "",
        "## Research coverage declaration",
        "",
        f"- Primary-source historical results cutoff: {coverage['primary_source_historical_cutoff']}",
        f"- Required completed-season cutoff: {coverage['required_completed_season_cutoff']}",
        "- These cutoffs come from explicit Research source inventory and target coverage. A media-guide title or filename never establishes the results cutoff.",
    ]
    if early_history:
        lines.extend(
            [
                "",
                "## Early-history uncertainty",
                "",
                "The following structured payload is carried unchanged from the "
                "independently verified Stage 1 terminal-debt closeout.",
                "",
                "```json",
                json.dumps(early_history, indent=2, sort_keys=True),
                "```",
            ]
        )
    if aggregate_coverage:
        lines.extend(
            [
                "",
                "## Research-exhausted institutional aggregate coverage gap",
                "",
                "This is season-level historical accounting, not one or more game records.",
                "The official season record and separately identified games are "
                "not interchangeable. Do not allocate unidentified games to invented "
                "dates, opponents, or scores. Any accounting_contradictions entries "
                "are diagnostic source conflicts only; their deltas must never be "
                "treated as missing-game counts, overlap identities, or result allocations.",
                "",
                "```json",
                json.dumps(aggregate_coverage, indent=2, sort_keys=True),
                "```",
            ]
        )
    lines.extend(["", "## Durable row-level source families", ""])
    lines.extend(f"- {key}: {count:,} game rows" for key, count in sorted(kinds.items()))
    if urls:
        lines.extend(["", "## Row-level source URLs", ""])
        lines.extend(f"- {url}" for url in urls)

    for name in sorted(archive.namelist()):
        if not name.startswith(prefix) or not name.endswith("source-register.json"):
            continue
        try:
            register = json.loads(archive.read(name))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        sources = register.get("sources", []) if isinstance(register, dict) else []
        if not sources:
            continue
        lines.extend(["", f"## Durable source register: {name[len(prefix):]}", ""])
        for source in sources:
            if not isinstance(source, dict):
                continue
            label = (
                source.get("title")
                or source.get("artifact")
                or source.get("path")
                or source.get("type")
                or "source"
            )
            detail = source.get("url") or source.get("use") or ""
            lines.append(f"- {label}" + (f" — {detail}" if detail else ""))
    return "\n".join(lines) + "\n"


def _aggregate_coverage_payload(
    archive: zipfile.ZipFile,
    prefix: str,
    manifest: dict[str, Any],
    *,
    school_key: str,
    research_base_sha: str,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], dict[str, Any]]:
    logical = AUTHORING_DIR + "/" + AGGREGATE_COVERAGE_AUTHORING_FILE
    member = prefix + logical
    if member not in archive.namelist():
        return None, [], {"present": False}
    defects: list[dict[str, Any]] = []
    if logical not in _manifest_names(manifest):
        defects.append({"reason": "AGGREGATE_COVERAGE_NOT_MANIFESTED", "name": logical})
    raw = archive.read(member)
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None, [{"reason": "AGGREGATE_COVERAGE_INVALID_JSON"}], {"present": True}

    entries = payload.get("coverage") if isinstance(payload, dict) else None
    accounting = payload.get("accounting_contradictions", []) if isinstance(payload, dict) else []
    if (
        not isinstance(payload, dict)
        or payload.get("schema_version") != 1
        or not isinstance(entries, list)
        or not entries
        or not isinstance(accounting, list)
    ):
        defects.append({"reason": "AGGREGATE_COVERAGE_INVALID_STRUCTURE"})
        entries = [] if not isinstance(entries, list) else entries
        accounting = [] if not isinstance(accounting, list) else accounting

    years: set[str] = set()
    for item in entries:
        if not isinstance(item, dict):
            defects.append({"reason": "AGGREGATE_COVERAGE_INVALID_ITEM"})
            continue
        season = str(item.get("season", "")).strip()
        if not season or season in years:
            defects.append({"reason": "AGGREGATE_COVERAGE_DUPLICATE_SEASON", "season": season})
        years.add(season)
        if item.get("school_key") != school_key or item.get("research_base_sha") != research_base_sha:
            defects.append({"reason": "AGGREGATE_COVERAGE_AUTHORITY_MISMATCH", "season": season})
        if item.get("terminal_classification") != "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP":
            defects.append({"reason": "AGGREGATE_COVERAGE_TERMINAL_MISMATCH", "season": season})
        if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("audit_sha256", ""))):
            defects.append({"reason": "AGGREGATE_COVERAGE_AUDIT_HASH_INVALID", "season": season})
        official = item.get("institutional_record", {})
        named = item.get("identified_record", {})
        missing = item.get("unidentified_record", {})
        if (
            not all(isinstance(record, dict) for record in (official, named, missing))
            or any(
                not isinstance(record.get(key), int) or record[key] < 0
                for record in (official, named, missing)
                for key in ("wins", "losses", "games")
            )
            or any(
                official[key] - named[key] != missing[key]
                for key in ("wins", "losses", "games")
            )
            or official.get("wins", 0) + official.get("losses", 0) != official.get("games", -1)
            or named.get("wins", 0) + named.get("losses", 0) != named.get("games", -1)
            or missing.get("wins", 0) + missing.get("losses", 0) != missing.get("games", -1)
            or not missing.get("games", 0)
        ):
            defects.append({"reason": "AGGREGATE_COVERAGE_ARITHMETIC_INVALID", "season": season})

    accounting_years: set[str] = set()
    for item in accounting:
        if not isinstance(item, dict):
            defects.append({"reason": "ACCOUNTING_CONTRADICTION_INVALID_ITEM"})
            continue
        season = str(item.get("season", "")).strip()
        if not season or season in accounting_years:
            defects.append({"reason": "ACCOUNTING_CONTRADICTION_DUPLICATE_SEASON", "season": season})
        accounting_years.add(season)
        if item.get("school_key") != school_key or item.get("research_base_sha") != research_base_sha:
            defects.append({"reason": "ACCOUNTING_CONTRADICTION_AUTHORITY_MISMATCH", "season": season})
        if item.get("terminal_classification") != "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION":
            defects.append({"reason": "ACCOUNTING_CONTRADICTION_TERMINAL_MISMATCH", "season": season})
        if not re.fullmatch(r"[0-9a-f]{64}", str(item.get("audit_sha256", ""))):
            defects.append({"reason": "ACCOUNTING_CONTRADICTION_AUDIT_HASH_INVALID", "season": season})
        official = item.get("institutional_record", {})
        named = item.get("identified_record", {})
        delta = item.get("mechanical_delta", {})
        if (
            not all(isinstance(record, dict) for record in (official, named, delta))
            or any(
                not isinstance(record.get(key), int)
                for record in (official, named, delta)
                for key in ("wins", "losses", "games")
            )
            or official.get("wins", 0) < 0
            or official.get("losses", 0) < 0
            or official.get("games", 0) < 0
            or named.get("wins", 0) < 0
            or named.get("losses", 0) < 0
            or named.get("games", 0) < 0
            or official.get("wins", 0) + official.get("losses", 0) != official.get("games", -1)
            or named.get("wins", 0) + named.get("losses", 0) != named.get("games", -1)
            or any(
                official[key] - named[key] != delta[key]
                for key in ("wins", "losses", "games")
            )
        ):
            defects.append({"reason": "ACCOUNTING_CONTRADICTION_ARITHMETIC_INVALID", "season": season})

    return payload, defects, {
        "present": True,
        "sha256": sha256_bytes(raw),
        "seasons": sorted(years),
        "unidentified_games": sum(
            item.get("unidentified_record", {}).get("games", 0)
            for item in entries
            if isinstance(item, dict)
        ),
        "accounting_contradiction_seasons": sorted(accounting_years),
    }


def _early_history_payload(
    archive: zipfile.ZipFile,
    prefix: str,
    manifest: dict[str, Any],
    *,
    school_key: str,
    research_base_sha: str,
) -> tuple[dict[str, Any] | None, list[dict[str, Any]], dict[str, Any]]:
    logical = AUTHORING_DIR + "/" + EARLY_HISTORY_AUTHORING_FILE
    member = prefix + logical
    if member not in archive.namelist():
        return None, [], {"present": False}

    defects: list[dict[str, Any]] = []
    if logical not in _manifest_names(manifest):
        defects.append(
            {
                "reason": "EARLY_HISTORY_AUTHORING_MEMBER_NOT_MANIFESTED",
                "name": logical,
            }
        )
    data = archive.read(member)
    try:
        payload = json.loads(data)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return (
            None,
            defects
            + [
                {
                    "reason": "INVALID_EARLY_HISTORY_AUTHORING_JSON",
                    "name": logical,
                }
            ],
            {"present": True, "sha256": sha256_bytes(data)},
        )
    if not isinstance(payload, dict):
        defects.append(
            {
                "reason": "INVALID_EARLY_HISTORY_AUTHORING_PAYLOAD",
                "name": logical,
            }
        )
        return payload, defects, {"present": True, "sha256": sha256_bytes(data)}

    if payload.get("school_key") != school_key:
        defects.append(
            {
                "reason": "EARLY_HISTORY_SCHOOL_KEY_MISMATCH",
                "value": payload.get("school_key"),
            }
        )
    if payload.get("research_base_sha") != research_base_sha:
        defects.append(
            {
                "reason": "EARLY_HISTORY_RESEARCH_BASE_MISMATCH",
                "value": payload.get("research_base_sha"),
            }
        )
    if payload.get("terminal_classifications") != {
        "class_a": "EARLY_HISTORY_UNQUANTIFIED_SEASON_COVERAGE",
        "class_b": "EARLY_HISTORY_IDENTIFIED_GAME_RESULT_UNKNOWN",
    }:
        defects.append({"reason": "EARLY_HISTORY_TERMINAL_CLASSIFICATIONS_INVALID"})
    audit_sha = str(payload.get("audit_sha256", "")).strip()
    if not re.fullmatch(r"[0-9a-f]{64}", audit_sha):
        defects.append({"reason": "EARLY_HISTORY_AUDIT_SHA_INVALID"})

    class_a = payload.get("class_a", [])
    class_b = payload.get("class_b", [])
    if not isinstance(class_a, list) or not isinstance(class_b, list):
        defects.append({"reason": "EARLY_HISTORY_CLASS_COLLECTION_INVALID"})
        class_a, class_b = [], []

    class_a_seasons = sorted(
        str(item.get("season", "")).strip()
        for item in class_a
        if isinstance(item, dict) and str(item.get("season", "")).strip()
    )
    class_b_game_ids = sorted(
        str(item.get("research_game_id", "")).strip()
        for item in class_b
        if isinstance(item, dict)
        and str(item.get("research_game_id", "")).strip()
    )
    if len(class_a_seasons) != len(set(class_a_seasons)):
        defects.append({"reason": "EARLY_HISTORY_DUPLICATE_CLASS_A_SEASON"})
    if len(class_b_game_ids) != len(set(class_b_game_ids)):
        defects.append({"reason": "EARLY_HISTORY_DUPLICATE_CLASS_B_GAME_ID"})

    return (
        payload,
        defects,
        {
            "present": True,
            "sha256": sha256_bytes(data),
            "audit_sha256": audit_sha,
            "class_a_seasons": class_a_seasons,
            "class_b_game_ids": class_b_game_ids,
        },
    )


def inspect_checkpoint(
    school_key: str,
    checkpoint: Path,
    *,
    primary_source_historical_cutoff: str = "",
    required_completed_season_cutoff: str = "",
    allow_preflight_ready: bool = False,
) -> dict[str, Any]:
    parent = checkpoint.read_bytes()
    parent_sha = sha256_bytes(parent)
    with zipfile.ZipFile(io.BytesIO(parent)) as archive:
        layout = resolve_stage3b_parent_layout(archive)
        manifest = validate_checkpoint_manifest(archive, layout)
        status = json.loads(archive.read(layout["status_path"]))
        _, ledger = _csv_bytes(archive.read(layout["ledger_path"]))
        coverage, coverage_defects = _coverage_declaration(
            status,
            primary_source_historical_cutoff=primary_source_historical_cutoff,
            required_completed_season_cutoff=required_completed_season_cutoff,
        )
        research_base_sha = status.get(
            "research_base_sha", manifest.get("research_base_sha", "")
        )
        (
            opponent_home_responsibility,
            opponent_home_responsibility_defects,
            opponent_home_responsibility_summary,
        ) = reconcile_opponent_home_outside_responsibility(
            archive,
            layout["prefix"],
            manifest,
            ledger,
            normalize_game_type=normalize_game_type,
            normalize_site=normalize_site,
            project_game_id=project_game_id,
        )
        (
            early_history,
            early_history_defects,
            early_history_summary,
        ) = _early_history_payload(
            archive,
            layout["prefix"],
            manifest,
            school_key=school_key,
            research_base_sha=research_base_sha,
        )
        (
            aggregate_coverage,
            aggregate_coverage_defects,
            aggregate_coverage_summary,
        ) = _aggregate_coverage_payload(
            archive, layout["prefix"], manifest,
            school_key=school_key, research_base_sha=research_base_sha,
        )

        members = {
            filename: layout["prefix"] + AUTHORING_DIR + "/" + filename
            for filename in AUTHORING_FILES
        }
        missing = [
            filename
            for filename, member in members.items()
            if member not in archive.namelist()
        ]
        continuity_defects = checkpoint_continuity_defects(archive)
        result: dict[str, Any] = {
            "schema_version": 1,
            "school_key": school_key,
            "stage": "STAGE_4_AUTHORING_PREFLIGHT",
            "status": "PASS" if not missing else "STAGE4_AUTHORING_INPUT_INCOMPLETE",
            "stage3b_checkpoint_sha256": parent_sha,
            "stage3b_parent_topology": layout["topology"],
            "stage3b_status": status.get("status", ""),
            "research_base_sha": research_base_sha,
            "ledger_rows": len(ledger),
            "authoring_members": members,
            "missing_authoring_files": missing,
            "coverage": coverage,
            "early_history_uncertainty": early_history_summary,
            "stage3a4_opponent_home_responsibility": (
                opponent_home_responsibility_summary
            ),
            **({"historical_season_coverage": aggregate_coverage_summary}
               if aggregate_coverage else {}),
            "defects": (
                list(coverage_defects)
                + early_history_defects
                + aggregate_coverage_defects
                + opponent_home_responsibility_defects
                + continuity_defects
            ),
        }
        if missing:
            return result

        manifest_names = _manifest_names(manifest)
        for filename in AUTHORING_FILES:
            logical = AUTHORING_DIR + "/" + filename
            if logical not in manifest_names:
                result["defects"].append(
                    {"reason": "AUTHORING_MEMBER_NOT_MANIFESTED", "name": logical}
                )

        opp_fields, opponents = _csv_bytes(archive.read(members["opponents.csv"]))
        venue_fields, venues = _csv_bytes(archive.read(members["venues.csv"]))
        conf_fields, conferences = _csv_bytes(archive.read(members["conferences.csv"]))
        games, projection_defects = _projection(
            ledger,
            opponents,
            venues,
            school_key=school_key,
            opponent_home_outside_responsibility=(
                opponent_home_responsibility
                if not opponent_home_responsibility_defects
                else {}
            ),
        )
        projection_defects.extend(
            _opponent_home_accounting_projection_defects(
                games,
                (
                    opponent_home_responsibility
                    if not opponent_home_responsibility_defects
                    else {}
                ),
            )
        )
        if early_history:
            by_game_id = {row["source_game_id"]: row for row in games}
            for game_id in early_history_summary.get("class_b_game_ids", []):
                projected = by_game_id.get(game_id)
                if projected is None:
                    result["defects"].append(
                        {
                            "reason": "EARLY_HISTORY_CLASS_B_GAME_MISSING",
                            "source_game_id": game_id,
                        }
                    )
                    continue
                if (
                    projected.get("team_score", "").strip()
                    or projected.get("opponent_score", "").strip()
                    or projected.get("played_result", "").strip()
                ):
                    result["defects"].append(
                        {
                            "reason": "EARLY_HISTORY_CLASS_B_RESULT_NOT_BLANK",
                            "source_game_id": game_id,
                        }
                    )

        result["defects"].extend(
            _table_defects(
                opp_fields,
                opponents,
                OPPONENT_FIELDS,
                school_key=school_key,
                table="opponents.csv",
            )
        )
        result["defects"].extend(
            _table_defects(
                venue_fields,
                venues,
                VENUE_FIELDS,
                school_key=school_key,
                table="venues.csv",
            )
        )
        result["defects"].extend(
            _table_defects(
                conf_fields,
                conferences,
                CONFERENCE_FIELDS,
                school_key=school_key,
                table="conferences.csv",
            )
        )
        result["defects"].extend(projection_defects)
        result["defects"].extend(_mapping_defects(games, opponents))
        result["defects"].extend(_venue_defects(games, venues))

        for line, row in enumerate(opponents, start=2):
            value = row.get("current_d1", "").strip().casefold()
            if value not in D1_VALUES | NON_D1_VALUES:
                result["defects"].append(
                    {
                        "reason": "INVALID_CURRENT_D1",
                        "table": "opponents.csv",
                        "line": line,
                        "value": row.get("current_d1", ""),
                    }
                )

        if status.get("school_key") and status.get("school_key") != school_key:
            result["defects"].append(
                {
                    "reason": "SCHOOL_KEY_MISMATCH",
                    "checkpoint_school_key": status.get("school_key"),
                }
            )
        stage3b_status = str(status.get("status", "")).strip().upper()
        stage3b_ready_for_preflight = (
            allow_preflight_ready
            and stage3b_status.endswith("PREFLIGHT_READY")
        )
        if stage3b_status != "COMPLETE" and not stage3b_ready_for_preflight:
            result["defects"].append(
                {
                    "reason": "STAGE3B_NOT_COMPLETE",
                    "status": status.get("status", ""),
                }
            )

        result.update(
            {
                "status": "PASS"
                if not result["defects"]
                else "STAGE4_AUTHORING_INPUT_INVALID",
                "opponent_rows": len(opponents),
                "venue_rows": len(venues),
                "conference_rows": len(conferences),
                "projected_source_games": len(games),
            }
        )
        return result


def author(
    school_key: str,
    checkpoint: Path,
    main_sha: str,
    output_dir: Path,
    *,
    primary_source_historical_cutoff: str = "",
    required_completed_season_cutoff: str = "",
) -> dict[str, Any]:
    preflight = inspect_checkpoint(
        school_key,
        checkpoint,
        primary_source_historical_cutoff=primary_source_historical_cutoff,
        required_completed_season_cutoff=required_completed_season_cutoff,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "stage4-authoring-preflight.json", preflight)
    if preflight["status"] != "PASS":
        return preflight

    parent = checkpoint.read_bytes()
    package = output_dir / "package"
    if package.exists():
        shutil.rmtree(package)
    package.mkdir(parents=True)

    with zipfile.ZipFile(io.BytesIO(parent)) as archive:
        layout = resolve_stage3b_parent_layout(archive)
        status = json.loads(archive.read(layout["status_path"]))
        _, ledger = _csv_bytes(archive.read(layout["ledger_path"]))
        manifest = validate_checkpoint_manifest(archive, layout)
        (
            opponent_home_responsibility,
            opponent_home_responsibility_defects,
            _opponent_home_responsibility_summary,
        ) = reconcile_opponent_home_outside_responsibility(
            archive,
            layout["prefix"],
            manifest,
            ledger,
            normalize_game_type=normalize_game_type,
            normalize_site=normalize_site,
            project_game_id=project_game_id,
        )
        if opponent_home_responsibility_defects:
            raise ValueError(
                "Stage 3A-4 opponent-home accounting reconciliation defects: "
                + json.dumps(
                    opponent_home_responsibility_defects[:10],
                    sort_keys=True,
                )
            )
        early_member = (
            layout["prefix"]
            + AUTHORING_DIR
            + "/"
            + EARLY_HISTORY_AUTHORING_FILE
        )
        early_history = (
            json.loads(archive.read(early_member))
            if early_member in archive.namelist()
            else None
        )
        aggregate_member = (
            layout["prefix"] + AUTHORING_DIR + "/"
            + AGGREGATE_COVERAGE_AUTHORING_FILE
        )
        aggregate_coverage = (
            json.loads(archive.read(aggregate_member))
            if aggregate_member in archive.namelist()
            else None
        )
        members = {
            filename: layout["prefix"] + AUTHORING_DIR + "/" + filename
            for filename in AUTHORING_FILES
        }
        _, opponents = _csv_bytes(archive.read(members["opponents.csv"]))
        _, venues = _csv_bytes(archive.read(members["venues.csv"]))
        games, defects = _projection(
            ledger,
            opponents,
            venues,
            school_key=school_key,
            opponent_home_outside_responsibility=opponent_home_responsibility,
        )
        defects.extend(
            _opponent_home_accounting_projection_defects(
                games,
                opponent_home_responsibility,
            )
        )
        if defects:
            raise ValueError(
                "Stage 4 source-game projection defects: "
                + json.dumps(defects[:10], sort_keys=True)
            )
        _write_csv(package / "source-games.csv", SOURCE_GAME_FIELDS, games)
        for filename in AUTHORING_FILES:
            (package / filename).write_bytes(archive.read(members[filename]))
        (package / "notes.md").write_text(
            _notes(
                school_key,
                sha256_bytes(parent),
                status,
                games,
                preflight["coverage"],
            ),
            encoding="utf-8",
        )
        (package / "source-notes.md").write_text(
            _source_notes(
                school_key,
                ledger,
                archive,
                layout["prefix"],
                preflight["coverage"],
                early_history,
                aggregate_coverage,
            ),
            encoding="utf-8",
        )

    closeout_status = closeout(
        school_key,
        package,
        checkpoint,
        main_sha,
        output_dir / "closeout",
    )
    result = {
        "schema_version": 1,
        "school_key": school_key,
        "stage": "STAGE_4",
        "status": closeout_status["status"],
        "stage3b_checkpoint_sha256": sha256_bytes(parent),
        "research_base_sha": preflight["research_base_sha"],
        "coverage": preflight["coverage"],
        "early_history_uncertainty": preflight["early_history_uncertainty"],
        "package_dir": str(package),
        "closeout": closeout_status,
        "repository_mutations": 0,
    }
    write_json(output_dir / "stage4-status.json", result)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Deterministic Research Stage 4 package authoring and closeout."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    preflight = sub.add_parser("preflight")
    preflight.add_argument("school_key")
    preflight.add_argument("stage3b_checkpoint", type=Path)
    preflight.add_argument("--output-dir", type=Path)
    preflight.add_argument("--primary-source-historical-cutoff", default="")
    preflight.add_argument("--required-completed-season-cutoff", default="")

    author_p = sub.add_parser("author")
    author_p.add_argument("school_key")
    author_p.add_argument("stage3b_checkpoint", type=Path)
    author_p.add_argument("--main-sha", required=True)
    author_p.add_argument("--output-dir", type=Path)
    author_p.add_argument("--primary-source-historical-cutoff", default="")
    author_p.add_argument("--required-completed-season-cutoff", default="")

    args = parser.parse_args()
    output = args.output_dir or Path(".research") / args.school_key / "stage4"
    try:
        if args.command == "preflight":
            result = inspect_checkpoint(
                args.school_key,
                args.stage3b_checkpoint,
                primary_source_historical_cutoff=args.primary_source_historical_cutoff,
                required_completed_season_cutoff=args.required_completed_season_cutoff,
                allow_preflight_ready=True,
            )
            output.mkdir(parents=True, exist_ok=True)
            write_json(output / "stage4-authoring-preflight.json", result)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 0 if result["status"] == "PASS" else 2

        result = author(
            args.school_key,
            args.stage3b_checkpoint,
            args.main_sha,
            output,
            primary_source_historical_cutoff=args.primary_source_historical_cutoff,
            required_completed_season_cutoff=args.required_completed_season_cutoff,
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return (
            0
            if result["status"] == "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY"
            else 2
        )
    except (
        OSError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
