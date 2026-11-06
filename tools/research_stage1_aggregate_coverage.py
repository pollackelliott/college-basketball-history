#!/usr/bin/env python3
"""Audit and close out owner-authorized, research-exhausted early season aggregate gaps.

No unidentified game is ever inserted into the ledger or canonical game universe.
The registry is a protected-main, exact-parent owner authority; raw aggregate
records alone cannot make an arbitrary school or season eligible.

One parent checkpoint may contain one or more independently approved
FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION blockers. Each season is validated
against its exact protected-main authority and all approved seasons close in one
separately hashed successor.

Commands:
  audit PARENT --expected-parent-sha256 SHA [--output REPORT.json]
  closeout PARENT AUDIT.json --expected-parent-sha256 SHA --expected-audit-sha256 SHA --output SUCCESSOR.zip
  verify-closeout PARENT SUCCESSOR.zip AUDIT.json --expected-parent-sha256 SHA --expected-closeout-sha256 SHA --expected-audit-sha256 SHA
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import zipfile
from collections import Counter
from pathlib import Path
from typing import Any

REGISTRY = Path(__file__).resolve().parents[1] / "data/reference/early-aggregate-coverage-authorities.json"
ELIGIBLE = "ELIGIBLE_FOR_EARLY_AGGREGATE_COVERAGE_CLOSEOUT"
VERIFIED = "VERIFIED_EARLY_AGGREGATE_COVERAGE_CLOSEOUT"
TERMINAL = "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP"
CLOSEOUT_MEMBER = "aggregate-coverage-closeout.json"
AUTHORING_MEMBER = "stage4-authoring/season-coverage.json"
SOURCE_MEMBER = "founding-season-evidence-exhaustion.json"
LEGACY_EVIDENCE_MODE = "MANIFESTED_RESIDUAL_SUMMARY"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def read_zip(path: Path, expected: str) -> tuple[dict[str, bytes], str]:
    raw = path.read_bytes()
    actual = digest(raw)
    if not expected or actual != expected:
        raise ValueError("CHECKPOINT_HASH_MISMATCH_OR_UNPINNED")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.testzip():
            raise ValueError("INVALID_ARCHIVE_CRC")
        names = z.namelist()
        if not names or len(names) != len(set(names)):
            raise ValueError("INVALID_ARCHIVE_NAMES")
        root_manifests = {
            "stage1-manifest.json",
            "checkpoint-manifest.json",
            "manifest.json",
        }
        prefixes = {name.split("/", 1)[0] for name in names if "/" in name}
        if root_manifests.intersection(names):
            prefix = ""
        elif len(prefixes) == 1 and all(name.startswith(next(iter(prefixes)) + "/") for name in names):
            prefix = next(iter(prefixes)) + "/"
        else:
            raise ValueError("INVALID_ARCHIVE_LAYOUT")
        members = {}
        for name in names:
            inner = name[len(prefix):]
            if not inner or inner.startswith("/") or ".." in Path(inner).parts:
                raise ValueError("UNSAFE_ARCHIVE_PATH")
            members[inner] = z.read(name)
    return members, actual


def _manifest_records(manifest: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tracked = manifest.get("members")
    if isinstance(tracked, dict):
        return {
            str(name): {
                "size": meta.get("size", meta.get("bytes")) if isinstance(meta, dict) else None,
                "sha256": meta.get("sha256") if isinstance(meta, dict) else None,
            }
            for name, meta in tracked.items()
        }
    legacy_files = manifest.get("files")
    if isinstance(legacy_files, dict):
        return {
            str(name): {
                "size": meta.get("size", meta.get("bytes")) if isinstance(meta, dict) else None,
                "sha256": meta.get("sha256") if isinstance(meta, dict) else None,
            }
            for name, meta in legacy_files.items()
        }
    if isinstance(legacy_files, list):
        normalized: dict[str, dict[str, Any]] = {}
        for item in legacy_files:
            if not isinstance(item, dict):
                raise ValueError("INVALID_MANIFEST_FILES")
            name = str(
                item.get("name")
                or item.get("path")
                or item.get("filename")
                or item.get("file")
                or ""
            ).strip()
            if not name or name in normalized:
                raise ValueError("INVALID_MANIFEST_FILES")
            normalized[name] = {
                "size": item.get("size", item.get("bytes")),
                "sha256": item.get("sha256"),
            }
        return normalized
    raise ValueError("INVALID_MANIFEST_MEMBERS")


def manifest_defects(members: dict[str, bytes]) -> list[str]:
    present = [
        name for name in (
            "stage1-manifest.json",
            "checkpoint-manifest.json",
            "manifest.json",
        )
        if name in members
    ]
    if not present:
        return ["INVALID_MANIFEST"]
    manifest_name = "stage1-manifest.json" if "stage1-manifest.json" in present else present[0]
    try:
        manifest = json.loads(members[manifest_name])
        expected = _manifest_records(manifest)
    except (KeyError, ValueError, TypeError, json.JSONDecodeError, UnicodeError):
        return ["INVALID_MANIFEST"]
    expected.pop(manifest_name, None)
    defects = []
    if set(expected) != set(members) - {manifest_name}:
        defects.append("MANIFEST_MEMBER_SET_MISMATCH")
    for name, meta in expected.items():
        raw = members.get(name)
        if (
            raw is None
            or meta.get("size") != len(raw)
            or meta.get("sha256") != digest(raw)
        ):
            defects.append("MANIFEST_MISMATCH:" + name)
    return defects


def as_csv(raw: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def csv_bytes(rows: list[dict[str, str]]) -> bytes:
    if not rows:
        return b""
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode()


def first(row: dict[str, str], *names: str) -> str:
    for name in names:
        value = str(row.get(name, "") or "").strip()
        if value:
            return value
    return ""


def member_alias(members: dict[str, bytes], *names: str) -> tuple[str, bytes]:
    present = [name for name in names if name in members]
    if len(present) != 1:
        raise ValueError("MISSING_OR_AMBIGUOUS_LEGACY_MEMBER:" + "|".join(names))
    name = present[0]
    return name, members[name]


def row_result(row: dict[str, str]) -> str:
    played = first(
        row,
        "played_result",
        "accepted_result",
        "on_court_result",
        "source_result",
        "result",
    ).upper()
    if played in {"W", "L", "T"}:
        return played
    team = first(
        row,
        "accepted_team_score",
        "team_score",
        "source_program_score",
    )
    opponent = first(
        row,
        "accepted_opponent_score",
        "opponent_score",
        "opponent_points",
    )
    if team and opponent:
        try:
            a, b = int(team), int(opponent)
        except ValueError:
            return ""
        return "W" if a > b else "L" if a < b else "T"
    return ""


def read_registry(registry: Path) -> dict[str, Any]:
    data = json.loads(registry.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("authority_type") != "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE":
        raise ValueError("INVALID_OWNER_AUTHORITY_REGISTRY")
    if not isinstance(data.get("cases"), list):
        raise ValueError("INVALID_OWNER_AUTHORITY_REGISTRY")
    return data


def lookup_authority(school: str, season: str, registry: Path) -> dict[str, Any] | None:
    data = read_registry(registry)
    cases = [case for case in data["cases"] if case.get("school_key") == school and case.get("season") == season]
    if len(cases) > 1:
        raise ValueError("DUPLICATE_OWNER_AUTHORITY")
    return cases[0] if cases else None


def expected_authority_seasons(
    school: str,
    parent_sha: str,
    research_base_sha: str,
    registry: Path,
) -> set[str]:
    data = read_registry(registry)
    return {
        str(case.get("season", ""))
        for case in data["cases"]
        if case.get("school_key") == school
        and case.get("parent_checkpoint_sha256") == parent_sha
        and case.get("research_base_sha") == research_base_sha
    }


def evidence_by_season(members: dict[str, bytes]) -> dict[str, dict[str, Any]]:
    raw = members.get(SOURCE_MEMBER)
    if raw is None:
        return {}
    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, UnicodeError, TypeError):
        raise ValueError("INVALID_SOURCE_CHECKPOINT")
    if not isinstance(payload, dict):
        raise ValueError("INVALID_SOURCE_CHECKPOINT")
    if isinstance(payload.get("seasons"), list):
        result: dict[str, dict[str, Any]] = {}
        for item in payload["seasons"]:
            if not isinstance(item, dict):
                raise ValueError("INVALID_SOURCE_CHECKPOINT")
            season = str(item.get("season", ""))
            if not season or season in result:
                raise ValueError("INVALID_SOURCE_CHECKPOINT")
            result[season] = item
        return result
    season = str(payload.get("season", ""))
    return {season: payload} if season else {}


def authority_cases_for_parent(
    school: str,
    parent_sha: str,
    research_base_sha: str,
    registry: Path,
) -> list[dict[str, Any]]:
    data = read_registry(registry)
    return sorted(
        [
            case for case in data["cases"]
            if case.get("school_key") == school
            and case.get("parent_checkpoint_sha256") == parent_sha
            and case.get("research_base_sha") == research_base_sha
        ],
        key=lambda case: str(case.get("season", "")),
    )


def _manifest_payload(members: dict[str, bytes]) -> dict[str, Any]:
    for name in ("stage1-manifest.json", "checkpoint-manifest.json", "manifest.json"):
        if name in members:
            payload = json.loads(members[name])
            if not isinstance(payload, dict):
                raise ValueError("INVALID_MANIFEST")
            return payload
    raise ValueError("INVALID_MANIFEST")


def _legacy_nonblocking(row: dict[str, str]) -> bool:
    marker = first(row, "blocking", "is_blocking", "blocking_status").upper()
    state = first(row, "status", "residual_status", "resolution_status").upper()
    klass = first(row, "class", "residual_class", "blocker_class").upper()
    if marker in {"0", "FALSE", "NO", "NONBLOCKING", "NON_BLOCKING"}:
        return True
    return (
        "NONBLOCK" in state
        or "NON_BLOCK" in state
        or "PRESERVE_UNCHANGED" in state
        or "NONBLOCK" in klass
        or "NON_BLOCK" in klass
    )


def _parse_int(value: str) -> int | None:
    value = str(value or "").strip()
    if not value:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def _legacy_residuals(
    raw: bytes,
    authorities: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows = as_csv(raw)
    auth = {str(case["season"]): case for case in authorities}
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in rows:
        season = first(row, "season", "season_label")
        if not season:
            if _legacy_nonblocking(row):
                continue
            result.append({
                "blocker_id": first(row, "blocker_id", "residual_id", "id") or "LEGACY_UNSCOPED_RESIDUAL",
                "season": "",
                "class": first(row, "class", "residual_class", "blocker_class") or "LEGACY_UNRELATED_STAGE1_RESIDUAL",
                "research_state": first(row, "research_state", "state", "status"),
                "research_evidence_summary": first(row, "research_evidence_summary", "evidence_summary", "notes", "detail"),
                "detail": {},
            })
            continue
        if season not in auth and _legacy_nonblocking(row):
            continue
        if season in seen:
            raise ValueError("DUPLICATE_LEGACY_RESIDUAL_SEASON:" + season)
        seen.add(season)
        case = auth.get(season)
        if case is None:
            result.append({
                "blocker_id": first(row, "blocker_id", "residual_id", "id") or "LEGACY_UNRELATED:" + season,
                "season": season,
                "class": first(row, "class", "residual_class", "blocker_class") or "LEGACY_UNRELATED_STAGE1_RESIDUAL",
                "research_state": first(row, "research_state", "state", "status"),
                "research_evidence_summary": first(row, "research_evidence_summary", "evidence_summary", "notes", "detail"),
                "detail": {},
            })
            continue

        raw_class = first(row, "class", "residual_class", "blocker_class")
        raw_state = first(row, "research_state", "state")
        identified = _parse_int(first(
            row,
            "identified_game_rows",
            "identified_games",
            "identified_competitive_games",
            "observed_games",
        ))
        unidentified = _parse_int(first(
            row,
            "unidentified_game_rows",
            "unidentified_games",
            "missing_games",
            "coverage_gap_games",
        ))
        result.append({
            "blocker_id": first(row, "blocker_id", "residual_id", "id") or "LEGACY_AGGREGATE:" + season,
            "season": season,
            "class": raw_class or "FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION",
            "research_state": raw_state or "RESEARCH_EXHAUSTED_SOURCE_COVERAGE",
            "detail": {
                "identified_game_rows": (
                    identified if identified is not None
                    else case["identified_record"]["games"]
                ),
                "unidentified_game_rows": (
                    unidentified if unidentified is not None
                    else case["unidentified_record"]["games"]
                ),
            },
            "research_evidence_summary": first(
                row,
                "research_evidence_summary",
                "evidence_summary",
                "research_summary",
                "notes",
                "detail",
            ) or "Legacy manifested Stage 1 residual preserved in stage1-residuals.csv.",
        })
    return result


def _normalized_legacy_ledger(raw: bytes) -> tuple[bytes, list[dict[str, str]]]:
    rows = as_csv(raw)
    normalized: list[dict[str, str]] = []
    for row in rows:
        game_id = first(row, "research_game_id", "source_game_id", "game_id", "id")
        season = first(row, "season_label", "season")
        opponent = first(
            row,
            "opponent_literal",
            "source_opponent",
            "source_opponent_label",
            "opponent",
            "opponent_name",
        )
        game_type = first(
            row,
            "game_type",
            "accepted_game_type",
            "competition_type",
            "season_type",
        )
        if not game_id or not season or not opponent or not game_type:
            raise ValueError("LEGACY_LEDGER_REQUIRED_FIELD_MISSING")
        result = row_result(row)
        if not result:
            raise ValueError("LEGACY_LEDGER_RESULT_UNRESOLVED:" + game_id)
        item = dict(row)
        item.update({
            "research_game_id": game_id,
            "season_label": season,
            "opponent_literal": opponent,
            "game_type": game_type,
            "game_universe_state": first(
                row, "game_universe_state", "accepted_state", "universe_state"
            ) or "ACCEPTED",
            "game_inclusion": first(
                row, "game_inclusion", "accepted_inclusion", "inclusion"
            ) or "INCLUDED",
            "played_result": result,
        })
        normalized.append(item)
    return csv_bytes(normalized), normalized


def _record_from_census(row: dict[str, str]) -> tuple[str, str, str]:
    wins = first(
        row,
        "source_aggregate_wins",
        "institutional_wins",
        "source_wins",
        "aggregate_wins",
    )
    losses = first(
        row,
        "source_aggregate_losses",
        "institutional_losses",
        "source_losses",
        "aggregate_losses",
    )
    games = first(
        row,
        "source_aggregate_games",
        "institutional_games",
        "source_games",
        "expected_games",
        "aggregate_games",
    )
    record = first(row, "source_header_record", "institutional_record", "source_record")
    if (not wins or not losses) and record and "-" in record:
        left, right = record.split("-", 1)
        if left.strip().isdigit() and right.strip().isdigit():
            wins = wins or left.strip()
            losses = losses or right.strip()
    if not games and wins.isdigit() and losses.isdigit():
        games = str(int(wins) + int(losses))
    return wins, losses, games


def _normalized_legacy_census(
    raw: bytes,
    ledger: list[dict[str, str]],
) -> bytes:
    rows = as_csv(raw)
    normalized: list[dict[str, str]] = []
    by_season: dict[str, list[dict[str, str]]] = {}
    for game in ledger:
        by_season.setdefault(game["season_label"], []).append(game)
    for row in rows:
        season = first(row, "season_label", "season")
        if not season:
            raise ValueError("LEGACY_CENSUS_SEASON_MISSING")
        wins, losses, games = _record_from_census(row)
        season_games = by_season.get(season, [])
        tally = Counter(game["played_result"] for game in season_games)
        identified = first(
            row,
            "accepted_or_identified_rows",
            "identified_competitive_games",
            "observed_games",
            "identified_game_rows",
            "identified_games",
        ) or str(len(season_games))
        item = dict(row)
        item.update({
            "season_label": season,
            "source_aggregate_wins": wins,
            "source_aggregate_losses": losses,
            "source_aggregate_games": games,
            "accepted_or_identified_rows": identified,
            "known_played_wins": first(
                row, "known_played_wins", "identified_wins", "known_wins"
            ) or str(tally["W"]),
            "known_played_losses": first(
                row, "known_played_losses", "identified_losses", "known_losses"
            ) or str(tally["L"]),
        })
        normalized.append(item)
    return csv_bytes(normalized)


def normalize_parent_members(
    members: dict[str, bytes],
    *,
    parent_sha: str,
    registry: Path,
) -> tuple[dict[str, bytes], bytes, bool]:
    current_required = {
        "stage1-manifest.json",
        "stage1-status.json",
        "blocking-residuals.json",
        "structured-stage1-ledger.csv",
        "season-census.csv",
    }
    if current_required.issubset(members):
        return dict(members), members["structured-stage1-ledger.csv"], False

    status_name, status_raw = member_alias(
        members,
        "stage1-status.json",
        "status.json",
        "stage1-state.json",
    )
    try:
        status = json.loads(status_raw)
    except (json.JSONDecodeError, UnicodeError, TypeError) as exc:
        raise ValueError("INVALID_LEGACY_STAGE1_STATUS") from exc
    if not isinstance(status, dict):
        raise ValueError("INVALID_LEGACY_STAGE1_STATUS")

    manifest = _manifest_payload(members)
    school = str(status.get("school_key") or status.get("school") or "").strip()
    research_base = str(
        status.get("research_base_sha")
        or manifest.get("research_base_sha")
        or ""
    ).strip()
    if not school:
        raise ValueError("LEGACY_STAGE1_SCHOOL_MISSING")
    if not research_base:
        candidates = {
            str(case.get("research_base_sha", ""))
            for case in read_registry(registry)["cases"]
            if case.get("school_key") == school
            and case.get("parent_checkpoint_sha256") == parent_sha
        }
        if len(candidates) == 1:
            research_base = next(iter(candidates))
        else:
            raise ValueError("LEGACY_STAGE1_RESEARCH_BASE_MISSING")

    authorities = authority_cases_for_parent(
        school, parent_sha, research_base, registry
    )
    if not authorities or any(
        case.get("legacy_evidence_mode") != LEGACY_EVIDENCE_MODE
        or not case.get("identified_ledger_sha256")
        or not isinstance(case.get("identified_rows"), int)
        for case in authorities
    ):
        raise ValueError("LEGACY_STAGE1_EXACT_AUTHORITY_REQUIRED")

    _, ledger_raw = member_alias(
        members,
        "structured-stage1-ledger.csv",
        "stage1-ledger.csv",
    )
    canonical_ledger, ledger_rows = _normalized_legacy_ledger(ledger_raw)
    if any(case["identified_ledger_sha256"] != digest(ledger_raw) for case in authorities):
        raise ValueError("IDENTIFIED_LEDGER_HASH_MISMATCH")
    if any(case["identified_rows"] != len(ledger_rows) for case in authorities):
        raise ValueError("IDENTIFIED_LEDGER_COUNT_MISMATCH")

    _, census_raw = member_alias(
        members,
        "season-census.csv",
        "stage1-season-census.csv",
    )
    canonical_census = _normalized_legacy_census(census_raw, ledger_rows)

    if "blocking-residuals.json" in members:
        residuals_raw = members["blocking-residuals.json"]
        residuals = json.loads(residuals_raw)
    else:
        _, residuals_raw = member_alias(members, "stage1-residuals.csv")
        residuals = _legacy_residuals(residuals_raw, authorities)
    if not isinstance(residuals, list):
        raise ValueError("INVALID_LEGACY_STAGE1_RESIDUALS")

    view = dict(members)
    normalized_status = dict(status)
    normalized_status.update({
        "school_key": school,
        "status": "RESEARCH_BLOCKED_SOURCE_COVERAGE",
        "stage1_complete": False,
        "research_base_sha": research_base,
        "total_candidate_game_rows": len(ledger_rows),
        "blocking_residual_count": len(residuals),
        "legacy_parent_member": status_name,
    })
    view["stage1-status.json"] = json_bytes(normalized_status)
    view["structured-stage1-ledger.csv"] = canonical_ledger
    view["season-census.csv"] = canonical_census
    view["blocking-residuals.json"] = json_bytes(residuals)
    view["stage1-manifest.json"] = json_bytes({
        "schema_version": 1,
        "research_base_sha": research_base,
        "game_rows": len(ledger_rows),
        "blocking_residuals": len(residuals),
        "legacy_parent_projection": True,
        "members": {},
    })
    return view, ledger_raw, True


def audit_checkpoint(parent: Path, *, expected_parent_sha256: str,
                     registry: Path = REGISTRY) -> dict[str, Any]:
    raw_members, parent_sha = read_zip(parent, expected_parent_sha256)
    defects = manifest_defects(raw_members)
    try:
        members, authority_ledger_raw, legacy_parent = normalize_parent_members(
            raw_members,
            parent_sha=parent_sha,
            registry=registry,
        )
        status = json.loads(members["stage1-status.json"])
        manifest = json.loads(members["stage1-manifest.json"])
        residuals = json.loads(members["blocking-residuals.json"])
        ledger = as_csv(members["structured-stage1-ledger.csv"])
        census = as_csv(members["season-census.csv"])
        structured_evidence = evidence_by_season(raw_members)
    except (KeyError, TypeError, ValueError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        return {"status": "FAIL", "defects": [str(exc) or "INVALID_SOURCE_CHECKPOINT"]}

    school = status.get("school_key") or status.get("school")
    research_base = status.get("research_base_sha")
    if status.get("stage1_complete") or status.get("status") != "RESEARCH_BLOCKED_SOURCE_COVERAGE":
        defects.append("PARENT_NOT_RESEARCH_BLOCKED")
    if manifest.get("research_base_sha") != research_base:
        defects.append("RESEARCH_BASE_MISMATCH")
    if manifest.get("game_rows") != len(ledger) or status.get("total_candidate_game_rows") != len(ledger):
        defects.append("LEDGER_COUNT_MISMATCH")

    if not isinstance(residuals, list) or not residuals:
        defects.append("OTHER_STAGE1_BLOCKERS")
        residuals = []

    ids = [row.get("research_game_id", "").strip() for row in ledger]
    if len(set(ids)) != len(ids) or not all(ids):
        defects.append("MISSING_OR_DUPLICATE_GAME_IDS")
    if any(
        not row.get("opponent_literal", "").strip()
        or not row.get("game_type", "").strip()
        or "PLACEHOLDER" in row.get("game_universe_state", "").upper()
        or "UNIDENTIFIED" in row.get("game_universe_state", "").upper()
        for row in ledger
    ):
        defects.append("FABRICATED_OR_UNTYPED_GAME_ROW")

    residual_seasons: list[str] = []
    coverages: list[dict[str, Any]] = []
    for residual in residuals:
        if not isinstance(residual, dict):
            defects.append("UNRELATED_STAGE1_BLOCKER")
            continue
        if residual.get("class") != "FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION":
            defects.append("UNRELATED_STAGE1_BLOCKER")
            defects.append("OTHER_STAGE1_BLOCKERS")
            continue
        if residual.get("research_state") != "RESEARCH_EXHAUSTED_SOURCE_COVERAGE":
            defects.append("RESEARCH_NOT_EXHAUSTED")
        if not residual.get("research_evidence_summary"):
            defects.append("MISSING_RESEARCH_PROVENANCE")
        if not residual.get("blocker_id"):
            defects.append("SOURCE_PROVENANCE_OR_OWNER_AUTHORITY_MISSING")

        season = str(residual.get("season", ""))
        if not season or season in residual_seasons:
            defects.append("DUPLICATE_OR_MISSING_AGGREGATE_SEASON")
            defects.append("OTHER_STAGE1_BLOCKERS")
            continue
        residual_seasons.append(season)

        authority = lookup_authority(school, season, registry)
        if authority is None:
            defects.append("NO_EXACT_OWNER_AUTHORITY")
            authority = {}
        elif (
            authority.get("parent_checkpoint_sha256") != parent_sha
            or authority.get("research_base_sha") != research_base
            or not str(authority.get("owner_disposition", "")).startswith("https://github.com/")
        ):
            defects.append("OWNER_AUTHORITY_BINDING_MISMATCH")

        year = int(season[:4]) if len(season) >= 4 and season[:4].isdigit() else 9999
        if year > int(authority.get("maximum_eligible_season_start_year", 0)):
            defects.append("OUTSIDE_FOUNDING_ERA")

        if "identified_ledger_sha256" in authority and authority.get("identified_ledger_sha256") != digest(authority_ledger_raw):
            defects.append("IDENTIFIED_LEDGER_HASH_MISMATCH")
        if "identified_rows" in authority and authority.get("identified_rows") != len(ledger):
            defects.append("IDENTIFIED_LEDGER_COUNT_MISMATCH")

        rows = [row for row in ledger if row.get("season_label") == season]
        if any(row.get("game_inclusion") != "INCLUDED" for row in rows):
            defects.append("SEASON_INCLUDED_GAME_MISMATCH")
        tally = Counter(row.get("played_result", "") for row in rows)
        if tally.get("", 0) or any(result not in ("W", "L") for result in tally):
            defects.append("UNRESOLVED_KNOWN_GAME_OUTCOMES")
        identified = {"wins": tally["W"], "losses": tally["L"], "games": len(rows)}
        record = authority.get("institutional_record", {})
        if identified != authority.get("identified_record"):
            defects.append("IDENTIFIED_RECORD_AUTHORITY_MISMATCH")
        if record.get("wins", -1) + record.get("losses", -1) != record.get("games", -2):
            defects.append("INSTITUTIONAL_RECORD_ARITHMETIC")
        difference = {
            field: record.get(field, 0) - identified.get(field, 0)
            for field in ("wins", "losses", "games")
        }
        if (
            difference != authority.get("unidentified_record")
            or difference.get("games", 0) <= 0
            or difference["wins"] + difference["losses"] != difference["games"]
        ):
            defects.append("AGGREGATE_RESIDUAL_ARITHMETIC_MISMATCH")

        season_census = [
            row for row in census
            if row.get("season_label", row.get("season")) == season
        ]
        if len(season_census) != 1:
            defects.append("MISSING_OR_DUPLICATE_SEASON_CENSUS")
        else:
            c = season_census[0]
            for field, value in (
                ("source_aggregate_wins", record.get("wins")),
                ("source_aggregate_losses", record.get("losses")),
                ("source_aggregate_games", record.get("games")),
                ("accepted_or_identified_rows", len(rows)),
                ("known_played_wins", tally["W"]),
                ("known_played_losses", tally["L"]),
            ):
                if c.get(field) != str(value):
                    defects.append("SEASON_CENSUS_CONFLICT:" + field)

        detail = residual.get("detail", {})
        if (
            detail.get("identified_game_rows") != len(rows)
            or detail.get("unidentified_game_rows") != difference.get("games")
        ):
            defects.append("RESIDUAL_COUNT_MISMATCH")

        use_legacy_evidence = authority.get("legacy_evidence_mode") == LEGACY_EVIDENCE_MODE
        evidence = None if use_legacy_evidence else structured_evidence.get(season)
        evidence_member: str | None = SOURCE_MEMBER if evidence is not None else None
        if evidence is not None:
            if (
                evidence.get("policy_result") != "RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED"
                or evidence.get("identified_game_rows") != len(rows)
                or evidence.get("unidentified_game_rows") != difference.get("games")
                or evidence.get("rows_added") != 0
                or evidence.get("accepted_game_rows_before") != len(ledger)
                or evidence.get("accepted_game_rows_after") != len(ledger)
                or evidence.get("anonymous_placeholder_rows") != 0
                or evidence.get("rows_added_from_aggregate_inference") != 0
            ):
                defects.append("EVIDENCE_EXHAUSTION_INCONSISTENT")
            sources = evidence.get("systematic_evidence_checked", [])
            if (
                len(sources) < 3
                or not any("target institutional" in s.get("authority", "") for s in sources)
                or not all(s.get("source") and s.get("finding") and s.get("authority") for s in sources)
            ):
                defects.append("INADEQUATE_INSTITUTIONAL_EVIDENCE")
            if evidence.get("school_key") != school or evidence.get("season") != season:
                defects.append("SOURCE_PROVENANCE_OR_OWNER_AUTHORITY_MISSING")
            if evidence.get("institutional_record", {}) != record:
                defects.append("INSTITUTIONAL_RECORD_AUTHORITY_MISMATCH")
        elif authority.get("legacy_evidence_mode") != LEGACY_EVIDENCE_MODE:
            defects.append("MISSING_STRUCTURED_RESEARCH_EVIDENCE")

        gap = {
            "school_key": school,
            "season": season,
            "institutional_record": record,
            "identified_record": identified,
            "unidentified_record": difference,
            "source_description": "Institutional year-by-year season aggregate; individual game details incomplete",
            "owner_disposition": authority.get("owner_disposition"),
            "parent_checkpoint_sha256": parent_sha,
            "research_base_sha": research_base,
            "terminal_classification": TERMINAL,
            "warning": "Missing-game count is derived from a primary institutional aggregate, not directly stated by the institution. No unidentified game rows are represented.",
        }
        if evidence_member:
            gap["evidence_member"] = evidence_member
        else:
            gap["evidence_mode"] = LEGACY_EVIDENCE_MODE
        coverages.append(gap)

    expected_seasons = expected_authority_seasons(school, parent_sha, research_base, registry)
    if set(residual_seasons) != expected_seasons:
        defects.append("OWNER_AUTHORITY_POPULATION_MISMATCH")

    coverages.sort(key=lambda item: item["season"])
    report = {
        "schema_version": 1,
        "status": ELIGIBLE if not defects else "FAIL",
        "school_key": school,
        "parent_checkpoint_sha256": parent_sha,
        "research_base_sha": research_base,
        "identified_game_rows": len(ledger),
        "identified_ledger_sha256": digest(authority_ledger_raw),
        "season_coverages": coverages,
        "season_coverages_sha256": digest(json_bytes(coverages)),
        "defects": sorted(set(defects)),
        "stage1_complete": False,
    }
    if legacy_parent:
        report["legacy_parent_projection"] = True
    if len(coverages) == 1:
        report["season_coverage"] = coverages[0]
        report["season_coverage_sha256"] = digest(json_bytes(coverages[0]))
    return report


def report_coverages(report: dict[str, Any]) -> list[dict[str, Any]]:
    coverages = report.get("season_coverages")
    if isinstance(coverages, list) and coverages:
        return [dict(item) for item in coverages]
    single = report.get("season_coverage")
    if isinstance(single, dict):
        return [dict(single)]
    raise ValueError("AUDIT_COVERAGE_MISSING")


def expected_successor(
    parent_members: dict[str, bytes],
    report: dict[str, Any],
    audit_sha: str,
    *,
    registry: Path = REGISTRY,
) -> dict[str, bytes]:
    logical, _, legacy_parent = normalize_parent_members(
        parent_members,
        parent_sha=report["parent_checkpoint_sha256"],
        registry=registry,
    )
    result = dict(parent_members)
    if legacy_parent:
        result["structured-stage1-ledger.csv"] = logical["structured-stage1-ledger.csv"]
        result["season-census.csv"] = logical["season-census.csv"]
        result["stage1-status.json"] = logical["stage1-status.json"]
        result["blocking-residuals.json"] = logical["blocking-residuals.json"]
        status = json.loads(logical["stage1-status.json"])
        manifest = json.loads(logical["stage1-manifest.json"])
    else:
        status = json.loads(result["stage1-status.json"])
        manifest = json.loads(result["stage1-manifest.json"])
    coverages = report_coverages(report)
    for coverage in coverages:
        coverage["audit_sha256"] = audit_sha

    status.update({
        "status": "COMPLETE",
        "stage1_complete": True,
        "blocking_residual_count": 0,
        "next_bounded_unit": "STAGE_2_AFTER_OWNER_AUTHORIZATION",
        "next_owner_boundary": "Stage 1 terminal aggregate coverage accepted; stop for ordinary Stage 2 owner authorization.",
        "aggregate_coverage_terminal": TERMINAL,
        "aggregate_coverage_count": len(coverages),
        "aggregate_coverage_audit_sha256": audit_sha,
        "aggregate_coverage_parent_sha256": report["parent_checkpoint_sha256"],
    })
    result["stage1-status.json"] = json_bytes(status)
    result["blocking-residuals.json"] = json_bytes([])
    result[CLOSEOUT_MEMBER] = (
        json_bytes(coverages[0])
        if len(coverages) == 1
        else json_bytes({"schema_version": 1, "coverage": coverages})
    )
    result[AUTHORING_MEMBER] = json_bytes({"schema_version": 1, "coverage": coverages})
    manifest.update({
        "status": "COMPLETE",
        "blocking_residuals": 0,
        "parent_checkpoint_sha256": report["parent_checkpoint_sha256"],
        "aggregate_coverage_audit_sha256": audit_sha,
        "aggregate_coverage_terminal": TERMINAL,
        "aggregate_coverage_count": len(coverages),
    })
    manifest["members"] = {
        name: {"size": len(data), "sha256": digest(data)}
        for name, data in result.items()
        if name != "stage1-manifest.json"
    }
    result["stage1-manifest.json"] = json_bytes(manifest)
    return result


def serialize_zip(members: dict[str, bytes], path: Path) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in sorted(members):
            z.writestr(name, members[name])
    return digest(path.read_bytes())


def verified_audit(parent: Path, audit_path: Path, parent_sha: str, audit_sha: str,
                   registry: Path) -> tuple[dict[str, Any], dict[str, bytes]]:
    raw = audit_path.read_bytes()
    if not audit_sha or digest(raw) != audit_sha:
        raise ValueError("AUDIT_HASH_MISMATCH_OR_UNPINNED")
    provided = json.loads(raw)
    computed = audit_checkpoint(parent, expected_parent_sha256=parent_sha, registry=registry)
    if computed["status"] != ELIGIBLE or provided != computed:
        raise ValueError("AUDIT_NOT_ELIGIBLE_OR_CONTENT_MISMATCH")
    members, _ = read_zip(parent, parent_sha)
    return computed, members


def closeout(parent: Path, audit_path: Path, output: Path, *,
             parent_sha: str, audit_sha: str, registry: Path = REGISTRY) -> dict[str, Any]:
    report, members = verified_audit(parent, audit_path, parent_sha, audit_sha, registry)
    successor = expected_successor(
        members,
        report,
        audit_sha,
        registry=registry,
    )
    sha = serialize_zip(successor, output)
    return {
        "status": "STAGE1_CLOSEOUT_CANDIDATE_CREATED",
        "closeout_sha256": sha,
        "parent_checkpoint_sha256": parent_sha,
        "season_coverage_count": len(report_coverages(report)),
        "stage1_complete": False,
        "next_action": "Independently verify-closeout before declaring Stage 1 COMPLETE.",
    }


def verify_closeout(parent: Path, successor: Path, audit_path: Path, *,
                    parent_sha: str, successor_sha: str, audit_sha: str,
                    registry: Path = REGISTRY) -> dict[str, Any]:
    try:
        report, original = verified_audit(parent, audit_path, parent_sha, audit_sha, registry)
        actual, _ = read_zip(successor, successor_sha)
        expected = expected_successor(
            original,
            report,
            audit_sha,
            registry=registry,
        )
        defects = manifest_defects(actual)
        if actual != expected:
            defects.append("CLOSEOUT_CONTENT_OR_HISTORICAL_LEDGER_DRIFT")
    except (OSError, ValueError, TypeError, KeyError, csv.Error, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        return {"status": "FAIL", "defects": [str(exc)], "stage1_complete": False}
    result = {
        "schema_version": 1,
        "status": VERIFIED if not defects else "FAIL",
        "defects": defects,
        "stage1_complete": not defects,
        "parent_checkpoint_sha256": parent_sha,
        "closeout_checkpoint_sha256": successor_sha,
        "audit_sha256": audit_sha,
        "school_key": report["school_key"],
        "season_coverages": report_coverages(report),
    }
    if len(result["season_coverages"]) == 1:
        result["season_coverage"] = result["season_coverages"][0]
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    p = parser.add_subparsers(dest="command", required=True)
    a = p.add_parser("audit")
    a.add_argument("parent", type=Path)
    a.add_argument("--expected-parent-sha256", required=True)
    a.add_argument("--output", type=Path)
    c = p.add_parser("closeout")
    c.add_argument("parent", type=Path)
    c.add_argument("audit", type=Path)
    c.add_argument("--expected-parent-sha256", required=True)
    c.add_argument("--expected-audit-sha256", required=True)
    c.add_argument("--output", type=Path, required=True)
    v = p.add_parser("verify-closeout")
    v.add_argument("parent", type=Path)
    v.add_argument("closeout", type=Path)
    v.add_argument("audit", type=Path)
    v.add_argument("--expected-parent-sha256", required=True)
    v.add_argument("--expected-closeout-sha256", required=True)
    v.add_argument("--expected-audit-sha256", required=True)
    v.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        if args.command == "audit":
            report = audit_checkpoint(args.parent, expected_parent_sha256=args.expected_parent_sha256)
            ok = report["status"] == ELIGIBLE
        elif args.command == "closeout":
            report = closeout(
                args.parent,
                args.audit,
                args.output,
                parent_sha=args.expected_parent_sha256,
                audit_sha=args.expected_audit_sha256,
            )
            ok = True
        else:
            report = verify_closeout(
                args.parent,
                args.closeout,
                args.audit,
                parent_sha=args.expected_parent_sha256,
                successor_sha=args.expected_closeout_sha256,
                audit_sha=args.expected_audit_sha256,
            )
            ok = report["status"] == VERIFIED
    except (OSError, ValueError, TypeError, KeyError, csv.Error, json.JSONDecodeError, zipfile.BadZipFile) as exc:
        report = {"status": "FAIL", "defects": [str(exc)]}
        ok = False
    rendered = json_bytes(report)
    if getattr(args, "output", None) and args.command != "closeout":
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(rendered)
    print(rendered.decode("utf-8"), end="")
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
