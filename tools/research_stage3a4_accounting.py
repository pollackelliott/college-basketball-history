"""Stage 3A-4 opponent-home research-accounting reconciliation.

This module does not infer venue identity or locality. It only reconciles an
already-manifested Stage 3A-4 outside-responsibility sidecar against the
authoritative downstream ledger so later permanent tooling can preserve that
accepted accounting without reopening historical research.
"""
from __future__ import annotations

import json
from collections import defaultdict
from typing import Any, Callable

OPPONENT_HOME_RESPONSIBILITY_FILE = (
    "stage3a4-opponent-home-outside-responsibility.json"
)
STAGE3A4_STATUS_FILE = "stage3a4-status.json"


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


def _first(row: dict[str, str], *fields: str) -> str:
    for field in fields:
        value = str(row.get(field, "") or "").strip()
        if value:
            return value
    return ""


def _ledger_opponent_key(row: dict[str, str]) -> str:
    return _first(
        row,
        "stage2_opponent_key",
        "opponent_program_key",
        "normalized_opponent_key",
        "opponent_key",
        "canonical_opponent_key",
    )


def _accepted_physical_venue(row: dict[str, str]) -> str:
    return _first(
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
        "accepted_venue_key",
    )


def reconcile_opponent_home_outside_responsibility(
    archive,
    prefix: str,
    manifest: dict[str, Any],
    ledger: list[dict[str, str]],
    *,
    normalize_game_type: Callable[[str], str],
    normalize_site: Callable[[str], str],
    project_game_id: Callable[[dict[str, str]], str],
) -> tuple[dict[str, dict[str, str]], list[dict[str, Any]], dict[str, Any]]:
    """Validate one manifested Stage 3A-4 opponent-home responsibility sidecar.

    The sidecar is accepted only when it exactly reconciles to the complete
    regular-season OPPONENT_HOME population in the authoritative ledger.
    Existing row-level accounting may be blank or already equal to the
    controlled package representation; contradictory accounting fails closed.
    """

    logical = OPPONENT_HOME_RESPONSIBILITY_FILE
    member = prefix + logical
    if member not in archive.namelist():
        return {}, [], {"present": False}

    defects: list[dict[str, Any]] = []
    manifested = _manifest_names(manifest)
    if logical not in manifested:
        defects.append(
            {
                "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_NOT_MANIFESTED",
                "name": logical,
            }
        )

    try:
        payload = json.loads(archive.read(member))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return (
            {},
            [
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_INVALID_JSON",
                    "name": logical,
                }
            ],
            {"present": True},
        )
    if not isinstance(payload, list):
        return (
            {},
            [
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_INVALID_STRUCTURE",
                    "name": logical,
                }
            ],
            {"present": True},
        )

    ledger_by_id: dict[str, list[dict[str, str]]] = defaultdict(list)
    expected_population: set[str] = set()
    for row in ledger:
        game_id = project_game_id(row)
        if game_id:
            ledger_by_id[game_id].append(row)
        game_type = normalize_game_type(
            _first(row, "curated_game_type", "game_type", "structured_game_type")
        )
        site = normalize_site(
            _first(
                row,
                "curated_site_type",
                "stage3b_site_type",
                "stage3a_final_site_type",
                "stage3a_final_han",
                "site_type",
            )
        )
        if game_type == "REGULAR_SEASON" and site == "OPPONENT_HOME":
            if not game_id:
                defects.append(
                    {
                        "reason": "STAGE3A4_OPPONENT_HOME_LEDGER_ROW_MISSING_ID",
                    }
                )
            else:
                expected_population.add(game_id)

    reconciled: dict[str, dict[str, str]] = {}
    seen: set[str] = set()
    for index, raw in enumerate(payload):
        if not isinstance(raw, dict):
            defects.append(
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_INVALID_ITEM",
                    "index": index,
                }
            )
            continue
        item = {str(k): str(v or "").strip() for k, v in raw.items()}
        game_id = item.get("research_game_id", "")
        basis = item.get("basis", "")
        if not game_id:
            defects.append(
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_BLANK_ID",
                    "index": index,
                }
            )
            continue
        if game_id in seen:
            defects.append(
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_DUPLICATE_ID",
                    "research_game_id": game_id,
                }
            )
            continue
        seen.add(game_id)
        if not basis:
            defects.append(
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_BLANK_BASIS",
                    "research_game_id": game_id,
                }
            )

        matches = ledger_by_id.get(game_id, [])
        if len(matches) != 1:
            defects.append(
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_LEDGER_ID_MATCH_COUNT",
                    "research_game_id": game_id,
                    "matches": len(matches),
                }
            )
            continue
        row = matches[0]
        game_type = normalize_game_type(
            _first(row, "curated_game_type", "game_type", "structured_game_type")
        )
        site = normalize_site(
            _first(
                row,
                "curated_site_type",
                "stage3b_site_type",
                "stage3a_final_site_type",
                "stage3a_final_han",
                "site_type",
            )
        )
        if game_type != "REGULAR_SEASON" or site != "OPPONENT_HOME":
            defects.append(
                {
                    "reason": "STAGE3A4_OPPONENT_HOME_CLASSIFICATION_MISMATCH",
                    "research_game_id": game_id,
                    "game_type": game_type,
                    "site_type": site,
                }
            )

        comparisons = (
            (
                "source_venue_token",
                item.get("source_venue_token", ""),
                _first(row, "source_venue_token"),
            ),
            ("game_date", item.get("game_date", ""), _first(row, "game_date")),
            (
                "season",
                item.get("season", ""),
                _first(row, "season_label", "season"),
            ),
            (
                "opponent_key",
                item.get("opponent_key", ""),
                _ledger_opponent_key(row),
            ),
        )
        for field, sidecar_value, ledger_value in comparisons:
            if sidecar_value and sidecar_value != ledger_value:
                defects.append(
                    {
                        "reason": "STAGE3A4_OPPONENT_HOME_SIDECAR_LEDGER_MISMATCH",
                        "research_game_id": game_id,
                        "field": field,
                        "sidecar_value": sidecar_value,
                        "ledger_value": ledger_value,
                    }
                )
            if field == "source_venue_token" and sidecar_value != ledger_value:
                defects.append(
                    {
                        "reason": "STAGE3A4_OPPONENT_HOME_SOURCE_TOKEN_MISMATCH",
                        "research_game_id": game_id,
                        "sidecar_value": sidecar_value,
                        "ledger_value": ledger_value,
                    }
                )

        existing_status = _first(row, "stage3a_site_research_status").upper()
        existing_basis = _first(row, "stage3a_site_research_basis")
        if existing_status or existing_basis:
            if (
                existing_status != "RESEARCHED_PARTIAL"
                or existing_basis != basis
            ):
                defects.append(
                    {
                        "reason": "STAGE3A4_OPPONENT_HOME_ROW_ACCOUNTING_CONFLICT",
                        "research_game_id": game_id,
                        "status": existing_status,
                        "basis": existing_basis,
                    }
                )

        reconciled[game_id] = item

    sidecar_population = set(reconciled)
    if sidecar_population != expected_population:
        defects.append(
            {
                "reason": "STAGE3A4_OPPONENT_HOME_POPULATION_MISMATCH",
                "sidecar_rows": len(sidecar_population),
                "ledger_rows": len(expected_population),
                "missing_from_sidecar": sorted(expected_population - sidecar_population)[:25],
                "extra_in_sidecar": sorted(sidecar_population - expected_population)[:25],
            }
        )

    status_logical = STAGE3A4_STATUS_FILE
    status_member = prefix + status_logical
    declared_count = None
    if status_member in archive.namelist():
        if status_logical not in manifested:
            defects.append(
                {
                    "reason": "STAGE3A4_STATUS_NOT_MANIFESTED",
                    "name": status_logical,
                }
            )
        try:
            stage3a4_status = json.loads(archive.read(status_member))
        except (json.JSONDecodeError, UnicodeDecodeError):
            defects.append({"reason": "STAGE3A4_STATUS_INVALID_JSON"})
            stage3a4_status = {}
        if isinstance(stage3a4_status, dict):
            raw_count = stage3a4_status.get(
                "opponent_home_rows_outside_source_school_building_responsibility"
            )
            if raw_count is not None:
                try:
                    declared_count = int(raw_count)
                except (TypeError, ValueError):
                    defects.append(
                        {
                            "reason": "STAGE3A4_OPPONENT_HOME_DECLARED_COUNT_INVALID",
                            "value": raw_count,
                        }
                    )
                else:
                    if declared_count != len(sidecar_population) or declared_count != len(
                        expected_population
                    ):
                        defects.append(
                            {
                                "reason": "STAGE3A4_OPPONENT_HOME_DECLARED_COUNT_MISMATCH",
                                "declared": declared_count,
                                "sidecar_rows": len(sidecar_population),
                                "ledger_rows": len(expected_population),
                            }
                        )

    material_rows = material_opponent_home_accounting_expectations(
        ledger,
        reconciled,
        project_game_id=project_game_id,
    )
    summary = {
        "present": True,
        "sidecar_rows": len(sidecar_population),
        "ledger_regular_season_opponent_home_rows": len(expected_population),
        "material_literal_source_gap_rows": len(material_rows),
        "declared_stage3a4_rows": declared_count,
        "reconciled": not defects,
    }
    return reconciled, defects, summary


def material_opponent_home_accounting_expectations(
    ledger: list[dict[str, str]],
    reconciled: dict[str, dict[str, str]],
    *,
    project_game_id: Callable[[dict[str, str]], str],
) -> dict[str, dict[str, str]]:
    """Return only rows whose literal source token creates publication debt.

    A blank opponent-home building by itself is not source-school publication
    debt. A preserved literal source venue token with no accepted physical
    venue is material and must carry package research accounting.
    """

    expected: dict[str, dict[str, str]] = {}
    for row in ledger:
        game_id = project_game_id(row)
        item = reconciled.get(game_id)
        if not item:
            continue
        token = _first(row, "source_venue_token")
        if not token or _accepted_physical_venue(row):
            continue
        expected[game_id] = {
            "status": "RESEARCHED_PARTIAL",
            "basis": item.get("basis", ""),
            "source_venue_token": token,
        }
    return expected
