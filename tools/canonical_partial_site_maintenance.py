#!/usr/bin/env python3
"""Exact-evidence shared-canonical city/state maintenance.

Census/audit is read-only. Applying one owner-authorized row requires a clean
isolated maintenance branch and the exact pinned canonical input Git blob.
No H/A/N, venue, source/assertion, raw-history, or school package field changes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from pathlib import Path


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _find_source(source: bytes, spec: dict) -> dict[str, str]:
    rows = list(csv.DictReader(io.StringIO(source.decode("utf-8-sig"), newline="")))
    hits = [row for row in rows if row.get("source_game_id") == spec["source_game_id"]]
    if len(hits) != 1:
        raise ValueError("SOURCE_GAME_ID_NOT_UNIQUE")
    row = hits[0]
    expected = spec["source_expected"]
    for key, value in expected.items():
        if row.get(key) != value:
            raise ValueError("SOURCE_EVIDENCE_CHANGED:" + key)
    if spec["literal_evidence"] not in row.get("raw_text", ""):
        raise ValueError("SOURCE_RAW_LITERAL_UNSUPPORTED")
    return row


def inspect_and_repair(raw: bytes, source: bytes, spec: dict) -> tuple[bytes, dict]:
    if _git_blob(raw) != spec["expected_canonical_blob"]:
        raise ValueError("CANONICAL_BLOB_SHA_MISMATCH")
    _find_source(source, spec)
    token = (spec["game_id"] + ",").encode()
    if raw.count(token) != 1:
        raise ValueError("CANONICAL_GAME_ID_NOT_UNIQUE")
    lines = raw.splitlines(keepends=True)
    hit = [i for i, line in enumerate(lines) if line.startswith(token)]
    if len(hit) != 1:
        raise ValueError("CANONICAL_GAME_LINE_NOT_UNIQUE")
    index = hit[0]
    line = lines[index]
    header = lines[0].decode("utf-8-sig").rstrip("\r\n").split(",")
    fields = list(csv.reader([line.decode("utf-8-sig").rstrip("\r\n")]))[0]
    if len(fields) != len(header):
        raise ValueError("CANONICAL_ROW_SCHEMA_MISMATCH")
    before = dict(zip(header, fields))
    for key, value in spec["canonical_expected"].items():
        if before.get(key) != value:
            raise ValueError("CANONICAL_ROW_PRECONDITION_CHANGED:" + key)
    if before.get("site_city", "") == "" or before.get("site_state", "") != "":
        raise ValueError("NOT_EXACT_CITY_ONLY_PARTIAL")
    new_state = spec["approved_site_state"]
    if not re.fullmatch(r"[A-Z]{2}", new_state):
        raise ValueError("INVALID_APPROVED_STATE_CODE")
    fields[header.index("site_state")] = new_state
    delimiter = "\r\n" if line.endswith(b"\r\n") else "\n"
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator=delimiter)
    writer.writerow(fields)
    updated_line = output.getvalue().encode("utf-8")
    # Preserve every original byte outside the single intended row.
    lines[index] = updated_line
    repaired = b"".join(lines)
    if repaired.replace(updated_line, line, 1) != raw:
        raise ValueError("NON_TARGET_HISTORICAL_BYTE_DRIFT")
    report = {
        "schema_version": 1,
        "status": "EXACT_SHARED_CANONICAL_STATE_CORRECTION_READY",
        "game_id": spec["game_id"],
        "source_game_id": spec["source_game_id"],
        "original_git_blob": _git_blob(raw),
        "result_git_blob": _git_blob(repaired),
        "original_sha256": _sha256(raw),
        "result_sha256": _sha256(repaired),
        "old_site_city": before["site_city"],
        "old_site_state": before["site_state"],
        "new_site_state": new_state,
        "raw_source_preserved": True,
        "canonical_only_changed": ["site_state"],
    }
    return repaired, report


def run(root: Path, spec_path: Path, *, apply: bool) -> dict:
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    if spec.get("schema_version") != 1 or spec.get("authority_kind") != "OWNER_AUTHORIZED_CANONICAL_LOCATION_REPAIR":
        raise ValueError("UNAPPROVED_CANONICAL_SITE_REPAIR_SPEC")
    root = root.resolve()
    original = root / "data/canonical/games.csv"
    evidence = root / spec["source_path"]
    raw = original.read_bytes()
    revised, report = inspect_and_repair(raw, evidence.read_bytes(), spec)
    if apply:
        branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=root, text=True).strip()
        if not branch.startswith("maintenance/") or branch in {"main", "master"}:
            raise ValueError("MAINTENANCE_BRANCH_REQUIRED")
        status = subprocess.check_output(["git", "status", "--porcelain"], cwd=root, text=True).strip()
        if status:
            raise ValueError("CLEAN_MAINTENANCE_WORKTREE_REQUIRED")
        original.write_bytes(revised)
        if original.read_bytes() != revised:
            raise ValueError("POSTWRITE_CANONICAL_DRIFT")
        report["status"] = "EXACT_SHARED_CANONICAL_STATE_CORRECTION_APPLIED"
    else:
        report["status"] = "READ_ONLY_CANONICAL_CORRECTION_REHEARSAL_PASS"
    return report


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--spec", type=Path, required=True)
    p.add_argument("--apply", action="store_true")
    args = p.parse_args()
    try:
        print(json.dumps(run(args.repo, args.spec, apply=args.apply), indent=2, sort_keys=True))
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, sort_keys=True))
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
