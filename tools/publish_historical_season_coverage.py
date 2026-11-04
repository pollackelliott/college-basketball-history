"""Publish audited season-level historical accounting during sealed onboarding apply.

The signed Stage 4 source-notes.md is immutable input. No synthetic game or
opponent-series row is created. The site builder independently reconciles counts.
"""
from __future__ import annotations

import csv
import io
import json
import re
from pathlib import Path

HEADING = "## Research-exhausted institutional aggregate coverage gap"
CSV_PATH = "data/reference/historical-season-coverage.csv"
ACCOUNTING_CSV_PATH = "data/reference/historical-season-accounting.csv"
AUTHORITY_PATH = "data/reference/early-aggregate-coverage-authorities.json"
ACCOUNTING_AUTHORITY_PATH = "data/reference/early-history-accounting-authorities.json"
FIELDS = [
    "program_key", "season_label",
    "official_wins", "official_losses", "official_games",
    "documented_wins", "documented_losses", "documented_games",
    "unidentified_wins", "unidentified_losses", "unidentified_games",
    "source_label", "owner_disposition", "stage1_audit_sha256", "public_note",
]
ACCOUNTING_FIELDS = [
    "program_key", "season_label",
    "official_wins", "official_losses", "official_games",
    "documented_wins", "documented_losses", "documented_games",
    "delta_wins", "delta_losses", "delta_games",
    "classification", "source_label", "owner_disposition",
    "stage1_audit_sha256", "public_note",
]


def _extract(text: str) -> dict | None:
    if HEADING not in text:
        return None
    if text.count(HEADING) != 1:
        raise ValueError("AGGREGATE_COVERAGE_DUPLICATE_HEADING")
    section = text.split(HEADING, 1)[1].split("\n## ", 1)[0]
    fence = chr(96) * 3
    if section.count(fence + "json\n") != 1:
        raise ValueError("AGGREGATE_COVERAGE_JSON_MISSING")
    raw = section.split(fence + "json\n", 1)[1].split("\n" + fence, 1)[0]
    payload = json.loads(raw)
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError("AGGREGATE_COVERAGE_PAYLOAD_INVALID")
    return payload


def _read_registry(path: Path, authority_type: str) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("authority_type") != authority_type:
        raise ValueError("HISTORICAL_ACCOUNTING_REGISTRY_INVALID")
    return data


def _coverage_authority(repo: Path, school_key: str, season: str) -> dict | None:
    legacy_path = repo / AUTHORITY_PATH
    if legacy_path.is_file():
        legacy = _read_registry(legacy_path, "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE")
        cases = [
            case for case in legacy.get("cases", [])
            if case.get("school_key") == school_key and case.get("season") == season
        ]
        if len(cases) > 1:
            raise ValueError("AGGREGATE_COVERAGE_DUPLICATE_OWNER_AUTHORITY")
        if cases:
            return cases[0]
    mixed_path = repo / ACCOUNTING_AUTHORITY_PATH
    if mixed_path.is_file():
        mixed = _read_registry(
            mixed_path, "OWNER_APPROVED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT"
        )
        school_cases = [
            case for case in mixed.get("cases", [])
            if case.get("school_key") == school_key
        ]
        if len(school_cases) > 1:
            raise ValueError("AGGREGATE_COVERAGE_DUPLICATE_OWNER_AUTHORITY")
        if school_cases:
            case = school_cases[0]
            entries = [
                item for item in case.get("aggregate_only_seasons", [])
                if item.get("season") == season
            ]
            if len(entries) > 1:
                raise ValueError("AGGREGATE_COVERAGE_DUPLICATE_OWNER_AUTHORITY")
            if entries:
                return {
                    **entries[0],
                    "school_key": school_key,
                    "season": season,
                    "parent_checkpoint_sha256": case.get("parent_checkpoint_sha256"),
                    "research_base_sha": case.get("research_base_sha"),
                    "owner_disposition": case.get("owner_disposition"),
                    "unidentified_record": {
                        key: entries[0]["institutional_record"][key]
                        - entries[0]["identified_record"][key]
                        for key in ("wins", "losses", "games")
                    },
                }
    return None


def _accounting_authority(repo: Path, school_key: str, season: str) -> dict | None:
    path = repo / ACCOUNTING_AUTHORITY_PATH
    if not path.is_file():
        return None
    data = _read_registry(path, "OWNER_APPROVED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT")
    school_cases = [case for case in data.get("cases", []) if case.get("school_key") == school_key]
    if len(school_cases) > 1:
        raise ValueError("ACCOUNTING_CONTRADICTION_DUPLICATE_OWNER_AUTHORITY")
    if not school_cases:
        return None
    case = school_cases[0]
    entries = [
        item for item in case.get("accounting_contradiction_seasons", [])
        if item.get("season") == season
    ]
    if len(entries) > 1:
        raise ValueError("ACCOUNTING_CONTRADICTION_DUPLICATE_OWNER_AUTHORITY")
    if not entries:
        return None
    return {
        **entries[0],
        "school_key": school_key,
        "season": season,
        "parent_checkpoint_sha256": case.get("parent_checkpoint_sha256"),
        "research_base_sha": case.get("research_base_sha"),
        "owner_disposition": case.get("owner_disposition"),
    }


def _entry_row(entry: dict, authority: dict) -> dict[str, str]:
    if (
        entry.get("terminal_classification") != "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP"
        or entry.get("owner_disposition") != authority.get("owner_disposition")
        or entry.get("parent_checkpoint_sha256")
        != authority.get("parent_checkpoint_sha256")
        or entry.get("research_base_sha") != authority.get("research_base_sha")
    ):
        raise ValueError("AGGREGATE_COVERAGE_OWNER_AUTHORITY_MISMATCH")
    audit = str(entry.get("audit_sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", audit):
        raise ValueError("AGGREGATE_COVERAGE_AUDIT_HASH_INVALID")
    row = {
        "program_key": entry["school_key"],
        "season_label": entry["season"],
        "source_label": entry.get("source_description", ""),
        "owner_disposition": entry["owner_disposition"],
        "stage1_audit_sha256": audit,
        "public_note": "",
    }
    for prefix, field in (
        ("official", "institutional_record"),
        ("documented", "identified_record"),
        ("unidentified", "unidentified_record"),
    ):
        record = entry.get(field)
        expected = authority.get(field)
        if not isinstance(record, dict) or record != expected:
            raise ValueError("AGGREGATE_COVERAGE_RECORD_AUTHORITY_MISMATCH")
        for key in ("wins", "losses", "games"):
            value = record.get(key)
            if not isinstance(value, int) or value < 0:
                raise ValueError("AGGREGATE_COVERAGE_RECORD_INVALID")
            row[prefix + "_" + key] = str(value)
        if record["wins"] + record["losses"] != record["games"]:
            raise ValueError("AGGREGATE_COVERAGE_RECORD_ARITHMETIC")
    if not row["source_label"]:
        raise ValueError("AGGREGATE_COVERAGE_SOURCE_MISSING")
    if any(
        int(row["official_" + key]) - int(row["documented_" + key])
        != int(row["unidentified_" + key])
        for key in ("wins", "losses", "games")
    ):
        raise ValueError("AGGREGATE_COVERAGE_DELTA_MISMATCH")
    return row


def _accounting_row(entry: dict, authority: dict) -> dict[str, str]:
    if (
        entry.get("terminal_classification")
        != "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION"
        or entry.get("owner_disposition") != authority.get("owner_disposition")
        or entry.get("parent_checkpoint_sha256")
        != authority.get("parent_checkpoint_sha256")
        or entry.get("research_base_sha") != authority.get("research_base_sha")
    ):
        raise ValueError("ACCOUNTING_CONTRADICTION_OWNER_AUTHORITY_MISMATCH")
    audit = str(entry.get("audit_sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", audit):
        raise ValueError("ACCOUNTING_CONTRADICTION_AUDIT_HASH_INVALID")
    official = entry.get("institutional_record")
    documented = entry.get("identified_record")
    delta = entry.get("mechanical_delta")
    if (
        official != authority.get("institutional_record")
        or documented != authority.get("identified_record")
        or delta != authority.get("mechanical_delta")
    ):
        raise ValueError("ACCOUNTING_CONTRADICTION_RECORD_AUTHORITY_MISMATCH")
    for value in list(official.values()) + list(documented.values()) + list(delta.values()):
        if not isinstance(value, int):
            raise ValueError("ACCOUNTING_CONTRADICTION_RECORD_INVALID")
    if official["wins"] + official["losses"] != official["games"]:
        raise ValueError("ACCOUNTING_CONTRADICTION_OFFICIAL_ARITHMETIC")
    if documented["wins"] + documented["losses"] != documented["games"]:
        raise ValueError("ACCOUNTING_CONTRADICTION_DOCUMENTED_ARITHMETIC")
    if any(
        official[key] - documented[key] != delta[key]
        for key in ("wins", "losses", "games")
    ):
        raise ValueError("ACCOUNTING_CONTRADICTION_DELTA_MISMATCH")
    return {
        "program_key": entry["school_key"],
        "season_label": entry["season"],
        "official_wins": str(official["wins"]),
        "official_losses": str(official["losses"]),
        "official_games": str(official["games"]),
        "documented_wins": str(documented["wins"]),
        "documented_losses": str(documented["losses"]),
        "documented_games": str(documented["games"]),
        "delta_wins": str(delta["wins"]),
        "delta_losses": str(delta["losses"]),
        "delta_games": str(delta["games"]),
        "classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
        "source_label": entry.get("source_description", ""),
        "owner_disposition": entry["owner_disposition"],
        "stage1_audit_sha256": audit,
        "public_note": entry.get("warning", ""),
    }


def _load_csv(path: Path, fields: list[str], error: str) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError(error + "_MISSING")
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != fields:
            raise ValueError(error + "_SCHEMA")
        return list(reader)


def _write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(sorted(rows, key=lambda row: (row["program_key"], row["season_label"])))
    path.write_text(out.getvalue(), encoding="utf-8")


def integrate_approved_coverage(repo: Path, school_key: str) -> dict:
    notes = repo / "schools" / school_key / "source-notes.md"
    if not notes.is_file():
        return {"status": "NO_AGGREGATE_COVERAGE"}
    payload = _extract(notes.read_text(encoding="utf-8"))
    if payload is None:
        return {"status": "NO_AGGREGATE_COVERAGE"}

    coverage = payload.get("coverage", [])
    contradictions = payload.get("accounting_contradictions", [])
    if not isinstance(coverage, list) or not isinstance(contradictions, list):
        raise ValueError("HISTORICAL_ACCOUNTING_PAYLOAD_INVALID")
    if not coverage and not contradictions:
        raise ValueError("HISTORICAL_ACCOUNTING_PAYLOAD_EMPTY")

    coverage_rows: list[dict[str, str]] = []
    seen_coverage: set[str] = set()
    for entry in coverage:
        if not isinstance(entry, dict) or entry.get("school_key") != school_key:
            raise ValueError("AGGREGATE_COVERAGE_SCHOOL_IDENTITY_MISMATCH")
        season = str(entry.get("season", ""))
        if not season or season in seen_coverage:
            raise ValueError("AGGREGATE_COVERAGE_DUPLICATE_SEASON")
        seen_coverage.add(season)
        authority = _coverage_authority(repo, school_key, season)
        if authority is None:
            raise ValueError("AGGREGATE_COVERAGE_EXACT_OWNER_AUTHORITY_REQUIRED")
        coverage_rows.append(_entry_row(entry, authority))

    accounting_rows: list[dict[str, str]] = []
    seen_accounting: set[str] = set()
    for entry in contradictions:
        if not isinstance(entry, dict) or entry.get("school_key") != school_key:
            raise ValueError("ACCOUNTING_CONTRADICTION_SCHOOL_IDENTITY_MISMATCH")
        season = str(entry.get("season", ""))
        if not season or season in seen_accounting:
            raise ValueError("ACCOUNTING_CONTRADICTION_DUPLICATE_SEASON")
        seen_accounting.add(season)
        authority = _accounting_authority(repo, school_key, season)
        if authority is None:
            raise ValueError("ACCOUNTING_CONTRADICTION_EXACT_OWNER_AUTHORITY_REQUIRED")
        accounting_rows.append(_accounting_row(entry, authority))

    coverage_added = False
    accounting_added = False
    if coverage_rows:
        coverage_path = repo / CSV_PATH
        existing_coverage = _load_csv(
            coverage_path, FIELDS, "AGGREGATE_COVERAGE_PUBLIC_CSV"
        )
        for row in coverage_rows:
            existing = [
                item for item in existing_coverage
                if item["program_key"] == school_key
                and item["season_label"] == row["season_label"]
            ]
            if len(existing) > 1 or (existing and existing[0] != row):
                raise ValueError("AGGREGATE_COVERAGE_EXISTING_ROW_CONFLICT")
            if not existing:
                existing_coverage.append(row)
                coverage_added = True
        _write_csv(coverage_path, FIELDS, existing_coverage)

    if accounting_rows:
        accounting_path = repo / ACCOUNTING_CSV_PATH
        existing_accounting = _load_csv(
            accounting_path, ACCOUNTING_FIELDS, "ACCOUNTING_CONTRADICTION_PUBLIC_CSV"
        )
        for row in accounting_rows:
            existing = [
                item for item in existing_accounting
                if item["program_key"] == school_key
                and item["season_label"] == row["season_label"]
            ]
            if len(existing) > 1 or (existing and existing[0] != row):
                raise ValueError("ACCOUNTING_CONTRADICTION_EXISTING_ROW_CONFLICT")
            if not existing:
                existing_accounting.append(row)
                accounting_added = True
        _write_csv(accounting_path, ACCOUNTING_FIELDS, existing_accounting)

    if len(coverage_rows) == 1 and not accounting_rows:
        row = coverage_rows[0]
        return {
            "status": "ADDED_VERIFIED_SEASON_COVERAGE" if coverage_added else "EXACT_ALREADY_PRESENT",
            "season": row["season_label"],
            "audit_sha256": row["stage1_audit_sha256"],
        }
    return {
        "status": "ADDED_OR_VERIFIED_HISTORICAL_ACCOUNTING",
        "coverage_seasons": sorted(seen_coverage),
        "accounting_contradiction_seasons": sorted(seen_accounting),
        "coverage_rows": len(coverage_rows),
        "accounting_rows": len(accounting_rows),
        "coverage_added": coverage_added,
        "accounting_added": accounting_added,
    }
