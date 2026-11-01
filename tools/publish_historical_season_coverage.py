"""Publish an audited season-level coverage note during sealed onboarding apply only.

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
AUTHORITY_PATH = "data/reference/early-aggregate-coverage-authorities.json"
FIELDS = [
    "program_key", "season_label",
    "official_wins", "official_losses", "official_games",
    "documented_wins", "documented_losses", "documented_games",
    "unidentified_wins", "unidentified_losses", "unidentified_games",
    "source_label", "owner_disposition", "stage1_audit_sha256", "public_note",
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


def _entry_row(entry: dict, authority: dict) -> dict[str, str]:
    if (entry.get("terminal_classification") != "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP"
        or entry.get("owner_disposition") != authority.get("owner_disposition")
        or entry.get("parent_checkpoint_sha256") != authority.get("parent_checkpoint_sha256")
        or entry.get("research_base_sha") != authority.get("research_base_sha")):
        raise ValueError("AGGREGATE_COVERAGE_OWNER_AUTHORITY_MISMATCH")
    audit = str(entry.get("audit_sha256", ""))
    if not re.fullmatch(r"[0-9a-f]{64}", audit):
        raise ValueError("AGGREGATE_COVERAGE_AUDIT_HASH_INVALID")
    row = {
        "program_key": entry["school_key"], "season_label": entry["season"],
        "source_label": entry.get("source_description", ""),
        "owner_disposition": entry["owner_disposition"],
        "stage1_audit_sha256": audit, "public_note": "",
    }
    for prefix, field in (("official", "institutional_record"),
                          ("documented", "identified_record"),
                          ("unidentified", "unidentified_record")):
        record = entry.get(field)
        if not isinstance(record, dict) or record != authority.get(field):
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
    if any(int(row["official_" + k]) - int(row["documented_" + k])
           != int(row["unidentified_" + k]) for k in ("wins", "losses", "games")):
        raise ValueError("AGGREGATE_COVERAGE_DELTA_MISMATCH")
    return row


def integrate_approved_coverage(repo: Path, school_key: str) -> dict:
    notes = repo / "schools" / school_key / "source-notes.md"
    if not notes.is_file():
        return {"status": "NO_AGGREGATE_COVERAGE"}
    payload = _extract(notes.read_text(encoding="utf-8"))
    if payload is None:
        return {"status": "NO_AGGREGATE_COVERAGE"}
    coverage = payload.get("coverage")
    if not isinstance(coverage, list) or len(coverage) != 1:
        raise ValueError("AGGREGATE_COVERAGE_COUNT_INVALID")
    entry = coverage[0]
    if not isinstance(entry, dict) or entry.get("school_key") != school_key:
        raise ValueError("AGGREGATE_COVERAGE_SCHOOL_IDENTITY_MISMATCH")
    owner = json.loads((repo / AUTHORITY_PATH).read_text(encoding="utf-8"))
    if owner.get("authority_type") != "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE":
        raise ValueError("AGGREGATE_COVERAGE_REGISTRY_INVALID")
    cases = [r for r in owner.get("cases", [])
             if r.get("school_key") == school_key and r.get("season") == entry.get("season")]
    if len(cases) != 1:
        raise ValueError("AGGREGATE_COVERAGE_EXACT_OWNER_AUTHORITY_REQUIRED")
    row = _entry_row(entry, cases[0])
    path = repo / CSV_PATH
    if not path.is_file():
        raise ValueError("AGGREGATE_COVERAGE_PUBLIC_CSV_MISSING")
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != FIELDS:
            raise ValueError("AGGREGATE_COVERAGE_PUBLIC_CSV_SCHEMA")
        rows = list(reader)
    existing = [r for r in rows if r["program_key"] == school_key
                and r["season_label"] == entry["season"]]
    if len(existing) > 1 or (existing and existing[0] != row):
        raise ValueError("AGGREGATE_COVERAGE_EXISTING_ROW_CONFLICT")
    if existing:
        return {"status": "EXACT_ALREADY_PRESENT", "season": entry["season"]}
    rows.append(row)
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(sorted(rows, key=lambda r: (r["program_key"], r["season_label"])))
    path.write_text(out.getvalue(), encoding="utf-8")
    return {"status": "ADDED_VERIFIED_SEASON_COVERAGE",
            "season": entry["season"], "audit_sha256": row["stage1_audit_sha256"]}
