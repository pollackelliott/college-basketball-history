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

from research_stage4_closeout import (
    closeout,
    first_literal,
    normalize_game_type,
    normalize_site,
    project_administrative_status,
    project_game_id,
    project_season_label,
    resolve_stage3b_parent_layout,
    sha256_bytes,
    validate_checkpoint_manifest,
    write_json,
)

AUTHORING_DIR = "stage4-authoring"
AUTHORING_FILES = ("opponents.csv", "venues.csv", "conferences.csv")

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
    )
    for status_field, basis_fields in candidates:
        status = row.get(status_field, "").strip().upper()
        if status not in ALLOWED_RESEARCH_STATUSES:
            continue
        return status, _first(row, *basis_fields)
    return "", ""


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
) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
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

        administrative_status, administrative_note = (
            project_administrative_status(row)
        )

        projected.append(
            {
                "source_game_id": game_id,
                "source_program_key": _first(row, "source_program_key"),
                "source_era": _first(row, "source_era", "season_source"),
                "season_label": project_season_label(
                    _first(row, "season_label")
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
                "team_score": _first(row, "team_score"),
                "opponent_score": _first(row, "opponent_score"),
                "played_result": _first(row, "played_result", "on_court_result"),
                "overtime_periods": _first(row, "overtime_periods"),
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
                "source_venue_name": _first(row, "source_venue_name"),
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
                or accepted_venue.get("canonical_name", "").strip(),
                "city": _first(
                    row,
                    "stage3b_venue_city",
                    "stage3b_site_city",
                    "stage3a_final_venue_city",
                    "stage3a_final_city",
                    "accepted_city",
                    "stage3a_site_city",
                    "stage3a2_venue_city",
                    "stage3a3_venue_city",
                    "city",
                    "venue_city",
                )
                or accepted_venue.get("city", "").strip(),
                "state": _first(
                    row,
                    "stage3b_venue_state",
                    "stage3b_site_state",
                    "stage3a_final_venue_state",
                    "stage3a_final_state",
                    "accepted_state",
                    "stage3a_site_state",
                    "stage3a2_venue_state",
                    "stage3a3_venue_state",
                    "state",
                    "venue_state",
                )
                or accepted_venue.get("state", "").strip(),
                "event_or_tournament": _first(
                    row, "event_or_tournament", "stage3a3_event_name"
                ),
                "source_round": _first(row, "source_round", "stage3b_source_round"),
                "curated_game_type": normalize_game_type(
                    _first(row, "curated_game_type", "game_type", "structured_game_type")
                ),
                "curated_postseason_round": _first(
                    row, "curated_postseason_round", "stage3b_postseason_round"
                ),
                "source_page": _first(row, "source_page", "source_pdf_page"),
                "raw_text": first_literal(
                    row, "raw_text", "source_raw_text"
                ),
                "normalization_status": _first(row, "normalization_status")
                or "RESEARCH_ACCEPTED",
                "administrative_status": administrative_status,
                "administrative_note": administrative_note,
                "notes": _first(row, "notes", "stage1_notes"),
                "site_research_status": research_status,
                "site_research_basis": research_basis if research_status else "",
            }
        )
    return projected, defects


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
        "",
        "## Durable row-level source families",
        "",
    ]
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

        members = {
            filename: layout["prefix"] + AUTHORING_DIR + "/" + filename
            for filename in AUTHORING_FILES
        }
        missing = [
            filename
            for filename, member in members.items()
            if member not in archive.namelist()
        ]
        result: dict[str, Any] = {
            "schema_version": 1,
            "school_key": school_key,
            "stage": "STAGE_4_AUTHORING_PREFLIGHT",
            "status": "PASS" if not missing else "STAGE4_AUTHORING_INPUT_INCOMPLETE",
            "stage3b_checkpoint_sha256": parent_sha,
            "stage3b_parent_topology": layout["topology"],
            "stage3b_status": status.get("status", ""),
            "research_base_sha": status.get(
                "research_base_sha", manifest.get("research_base_sha", "")
            ),
            "ledger_rows": len(ledger),
            "authoring_members": members,
            "missing_authoring_files": missing,
            "coverage": coverage,
            "defects": list(coverage_defects),
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
        games, projection_defects = _projection(ledger, opponents, venues)

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
        members = {
            filename: layout["prefix"] + AUTHORING_DIR + "/" + filename
            for filename in AUTHORING_FILES
        }
        _, opponents = _csv_bytes(archive.read(members["opponents.csv"]))
        _, venues = _csv_bytes(archive.read(members["venues.csv"]))
        games, defects = _projection(ledger, opponents, venues)
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
