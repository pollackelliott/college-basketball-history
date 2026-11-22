#!/usr/bin/env python3
"""Deterministic pre-Phase0 historical opponent-display reconciliation.

This module does not choose opponent identities or historical meaning. It reuses
the repository's permanent historical opponent-display normalizer against one
exact expansion Stage-1 candidate and the exact protected-main project
representation.  Only two representation fields are eligible:

* opponents.csv: canonical_opponent_name
* source-games.csv: normalized_opponent_name

Opponent keys, literal source labels, raw evidence, current_d1, and every
historical game field remain immutable.  The resulting reconciliation document
is canonical JSON and can be hash-bound through Integration Freeze, guarded
Phase 0, write-ahead, successor, and fresh replay.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import re
import shutil
import tempfile
from pathlib import Path
from typing import Any

import normalize_historical_opponent_displays as normalization


KIND = "ALL_HISTORY_EXPANSION_OPPONENT_DISPLAY_RECONCILIATION"
SCHEMA_VERSION = 1
HEX40 = re.compile(r"^[0-9a-f]{40}$")
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class OpponentDisplayReconciliationError(RuntimeError):
    """Fail-closed representation authority or field-contract violation."""


def require(condition: bool, code: str) -> None:
    if not condition:
        raise OpponentDisplayReconciliationError(code)


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _rows(data: bytes, label: str) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise OpponentDisplayReconciliationError(
            "EXPANSION_OPPONENT_DISPLAY_UTF8_INVALID:" + label
        ) from exc
    reader = csv.DictReader(io.StringIO(text, newline=""))
    fields = list(reader.fieldnames or [])
    rows = list(reader)
    require(bool(fields), "EXPANSION_OPPONENT_DISPLAY_SCHEMA_MISSING:" + label)
    return fields, rows


def _copy_authority_view(
    repo: Path,
    school_key: str,
    candidate_dir: Path,
    view: Path,
) -> None:
    programs = repo / "data" / "reference" / "programs.csv"
    require(programs.is_file(), "EXPANSION_OPPONENT_DISPLAY_PROGRAMS_MISSING")
    target_ref = view / "data" / "reference"
    target_ref.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(programs, target_ref / "programs.csv")

    schools = view / "schools"
    schools.mkdir(parents=True, exist_ok=True)
    for path in sorted((repo / "schools").glob("*/opponents.csv")):
        key = path.parent.name
        if key == school_key:
            continue
        target = schools / key
        target.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target / "opponents.csv")

    target = schools / school_key
    target.mkdir(parents=True, exist_ok=True)
    for name in ("opponents.csv", "source-games.csv"):
        source = candidate_dir / name
        require(
            source.is_file(),
            "EXPANSION_OPPONENT_DISPLAY_CANDIDATE_MEMBER_MISSING:" + name,
        )
        shutil.copyfile(source, target / name)


def _field_level_proof(
    *,
    school_key: str,
    before_opponents: bytes,
    after_opponents: bytes,
    before_source_games: bytes,
    after_source_games: bytes,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    opp_fields_before, opp_before = _rows(before_opponents, "opponents-before")
    opp_fields_after, opp_after = _rows(after_opponents, "opponents-after")
    require(
        opp_fields_before == opp_fields_after and len(opp_before) == len(opp_after),
        "EXPANSION_OPPONENT_DISPLAY_OPPONENT_TABLE_SHAPE_CHANGED",
    )
    require(
        "canonical_opponent_key" in opp_fields_before
        and "canonical_opponent_name" in opp_fields_before,
        "EXPANSION_OPPONENT_DISPLAY_OPPONENT_COLUMNS_MISSING",
    )

    opponent_changes: list[dict[str, Any]] = []
    changed_keys: set[str] = set()
    for line, (before, after) in enumerate(
        zip(opp_before, opp_after), start=2
    ):
        changed = [
            field
            for field in opp_fields_before
            if before.get(field, "") != after.get(field, "")
        ]
        if not changed:
            continue
        require(
            changed == ["canonical_opponent_name"],
            "EXPANSION_OPPONENT_DISPLAY_OPPONENT_FIELD_CHANGED:"
            + ",".join(changed),
        )
        key = before.get("canonical_opponent_key", "").strip()
        require(
            key and key == after.get("canonical_opponent_key", "").strip(),
            "EXPANSION_OPPONENT_DISPLAY_OPPONENT_KEY_CHANGED",
        )
        changed_keys.add(key)
        opponent_changes.append(
            {
                "line": line,
                "source_opponent_label": before.get(
                    "source_opponent_label", ""
                ),
                "canonical_opponent_key": key,
                "from_name": before.get("canonical_opponent_name", ""),
                "to_name": after.get("canonical_opponent_name", ""),
            }
        )

    src_fields_before, src_before = _rows(
        before_source_games, "source-games-before"
    )
    src_fields_after, src_after = _rows(
        after_source_games, "source-games-after"
    )
    require(
        src_fields_before == src_fields_after and len(src_before) == len(src_after),
        "EXPANSION_OPPONENT_DISPLAY_SOURCE_TABLE_SHAPE_CHANGED",
    )
    for required in (
        "source_game_id",
        "normalized_opponent_key",
        "normalized_opponent_name",
    ):
        require(
            required in src_fields_before,
            "EXPANSION_OPPONENT_DISPLAY_SOURCE_COLUMN_MISSING:" + required,
        )

    source_changes: list[dict[str, Any]] = []
    source_changed_keys: set[str] = set()
    for line, (before, after) in enumerate(
        zip(src_before, src_after), start=2
    ):
        changed = [
            field
            for field in src_fields_before
            if before.get(field, "") != after.get(field, "")
        ]
        if not changed:
            continue
        require(
            changed == ["normalized_opponent_name"],
            "EXPANSION_OPPONENT_DISPLAY_SOURCE_FIELD_CHANGED:"
            + ",".join(changed),
        )
        source_id = before.get("source_game_id", "").strip()
        key = before.get("normalized_opponent_key", "").strip()
        require(
            source_id
            and key
            and source_id == after.get("source_game_id", "").strip()
            and key == after.get("normalized_opponent_key", "").strip(),
            "EXPANSION_OPPONENT_DISPLAY_SOURCE_IDENTITY_CHANGED",
        )
        source_changed_keys.add(key)
        source_changes.append(
            {
                "line": line,
                "source_game_id": source_id,
                "normalized_opponent_key": key,
                "from_name": before.get("normalized_opponent_name", ""),
                "to_name": after.get("normalized_opponent_name", ""),
            }
        )

    require(
        source_changed_keys <= changed_keys,
        "EXPANSION_OPPONENT_DISPLAY_SOURCE_KEY_OUTSIDE_OPPONENT_CHANGE",
    )
    final_name_by_key: dict[str, str] = {}
    for row in opp_after:
        key = row.get("canonical_opponent_key", "").strip()
        if key not in changed_keys:
            continue
        name = row.get("canonical_opponent_name", "")
        if key in final_name_by_key:
            require(
                final_name_by_key[key] == name,
                "EXPANSION_OPPONENT_DISPLAY_FINAL_NAME_NOT_UNIQUE:" + key,
            )
        else:
            final_name_by_key[key] = name
    for row in src_after:
        key = row.get("normalized_opponent_key", "").strip()
        if key in changed_keys:
            require(
                row.get("normalized_opponent_name", "")
                == final_name_by_key.get(key, ""),
                "EXPANSION_OPPONENT_DISPLAY_SOURCE_NOT_ALIGNED:" + key,
            )

    proof = {
        "schema_version": 1,
        "school_key": school_key,
        "allowed_fields": {
            "opponents.csv": ["canonical_opponent_name"],
            "source-games.csv": ["normalized_opponent_name"],
        },
        "changed_keys": sorted(changed_keys),
        "opponent_changed_row_count": len(opponent_changes),
        "source_game_changed_row_count": len(source_changes),
        "source_game_changed_ids": [
            item["source_game_id"] for item in source_changes
        ],
        "opponent_key_changes": 0,
        "source_game_key_changes": 0,
        "source_game_non_name_field_changes": 0,
        "literal_evidence_changes": 0,
        "current_d1_changes": 0,
    }
    return proof, opponent_changes, source_changes


def derive_reconciliation(
    repo: Path,
    school_key: str,
    candidate_dir: Path,
    *,
    protected_main_sha: str,
    research_freeze_sha256: str,
) -> dict[str, Any]:
    """Derive the exact current-main representation reconciliation, if any."""
    repo = repo.resolve()
    candidate_dir = candidate_dir.resolve()
    protected_main_sha = str(protected_main_sha or "").strip().lower()
    research_freeze_sha256 = str(research_freeze_sha256 or "").strip().lower()
    require(
        bool(HEX40.fullmatch(protected_main_sha)),
        "EXPANSION_OPPONENT_DISPLAY_MAIN_SHA_INVALID",
    )
    require(
        bool(HEX64.fullmatch(research_freeze_sha256)),
        "EXPANSION_OPPONENT_DISPLAY_RESEARCH_SHA_INVALID",
    )
    observed_head = normalization.git(repo, "rev-parse", "HEAD")
    require(
        observed_head == protected_main_sha,
        "EXPANSION_OPPONENT_DISPLAY_RUNTIME_MAIN_MISMATCH",
    )

    before_opponents = (candidate_dir / "opponents.csv").read_bytes()
    before_source = (candidate_dir / "source-games.csv").read_bytes()

    with tempfile.TemporaryDirectory(
        prefix="expansion-opponent-display-authority-"
    ) as tmp:
        view = Path(tmp)
        _copy_authority_view(repo, school_key, candidate_dir, view)
        try:
            plan = normalization.build_normalization_plan(
                view,
                school_key,
                sync_current_d1=False,
            )
        except (FileNotFoundError, ValueError) as exc:
            raise OpponentDisplayReconciliationError(
                "EXPANSION_OPPONENT_DISPLAY_NORMALIZER_FAILED:" + str(exc)
            ) from exc
        require(
            plan.get("status") == "PASS"
            and int(plan.get("ambiguous_key_count", -1)) == 0,
            "EXPANSION_OPPONENT_DISPLAY_AUTHORITY_AMBIGUOUS",
        )
        try:
            source_plan = normalization.build_source_display_plan(
                view,
                school_key,
                plan,
                limit_to_opponent_changes=True,
            )
        except (FileNotFoundError, ValueError) as exc:
            raise OpponentDisplayReconciliationError(
                "EXPANSION_OPPONENT_DISPLAY_SOURCE_PLAN_FAILED:" + str(exc)
            ) from exc

        if not plan["change_row_count"] and not source_plan["change_row_count"]:
            return {
                "required": False,
                "document": None,
                "projected_bytes": {
                    "opponents.csv": before_opponents,
                    "source-games.csv": before_source,
                },
            }

        if plan["change_row_count"]:
            normalization.write_csv_preserving(
                plan["path"],
                plan["fields"],
                plan["rows"],
                plan["encoding"],
                plan["line_ending"],
            )
        if source_plan["change_row_count"]:
            normalization.write_csv_preserving(
                source_plan["path"],
                source_plan["fields"],
                source_plan["rows"],
                source_plan["encoding"],
                source_plan["line_ending"],
            )
        after_opponents = (
            view / "schools" / school_key / "opponents.csv"
        ).read_bytes()
        after_source = (
            view / "schools" / school_key / "source-games.csv"
        ).read_bytes()

    proof, opponent_changes, source_changes = _field_level_proof(
        school_key=school_key,
        before_opponents=before_opponents,
        after_opponents=after_opponents,
        before_source_games=before_source,
        after_source_games=after_source,
    )
    plan_keys = sorted(
        str(item.get("canonical_opponent_key") or "")
        for item in plan.get("changes") or []
    )
    require(
        plan_keys == proof["changed_keys"],
        "EXPANSION_OPPONENT_DISPLAY_PLAN_KEY_POPULATION_MISMATCH",
    )
    report = normalization.public_report(plan)
    report["source_game_display_change_rows"] = source_plan["change_row_count"]
    report["source_game_display_change_keys"] = source_plan["change_key_count"]
    report["source_game_display_changes"] = source_plan["changes"]

    document = {
        "schema_version": SCHEMA_VERSION,
        "kind": KIND,
        "status": "PASS",
        "school_key": school_key,
        "protected_main_sha": protected_main_sha,
        "research_freeze_sha256": research_freeze_sha256,
        "pre_candidate_sha256": {
            "opponents.csv": sha256_bytes(before_opponents),
            "source-games.csv": sha256_bytes(before_source),
        },
        "projected_candidate_sha256": {
            "opponents.csv": sha256_bytes(after_opponents),
            "source-games.csv": sha256_bytes(after_source),
        },
        "changed_keys": proof["changed_keys"],
        "opponent_changes": opponent_changes,
        "source_game_changes": source_changes,
        "field_level_proof": proof,
        "normalizer_report": report,
    }
    return {
        "required": True,
        "document": document,
        "projected_bytes": {
            "opponents.csv": after_opponents,
            "source-games.csv": after_source,
        },
    }


def validate_reconciliation(
    repo: Path,
    school_key: str,
    candidate_dir: Path,
    sidecar_path: Path,
    *,
    protected_main_sha: str,
    research_freeze_sha256: str,
) -> dict[str, Any]:
    """Recompute current authority and require exact canonical sidecar equality."""
    raw = sidecar_path.read_bytes()
    try:
        supplied = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise OpponentDisplayReconciliationError(
            "EXPANSION_OPPONENT_DISPLAY_SIDECAR_JSON_INVALID"
        ) from exc
    require(
        isinstance(supplied, dict),
        "EXPANSION_OPPONENT_DISPLAY_SIDECAR_NOT_OBJECT",
    )
    require(
        raw == canonical_json_bytes(supplied),
        "EXPANSION_OPPONENT_DISPLAY_SIDECAR_NOT_CANONICAL",
    )
    derived = derive_reconciliation(
        repo,
        school_key,
        candidate_dir,
        protected_main_sha=protected_main_sha,
        research_freeze_sha256=research_freeze_sha256,
    )
    require(
        derived["required"],
        "EXPANSION_OPPONENT_DISPLAY_SIDECAR_UNEXPECTED_NOOP",
    )
    require(
        supplied == derived["document"],
        "EXPANSION_OPPONENT_DISPLAY_SIDECAR_AUTHORITY_DRIFT",
    )
    return derived
