#!/usr/bin/env python3
"""Exact, owner-authorized 2019 Kansas Maui canonical-site maintenance.

Applies only to CBBG-0014297 and CBBG-0014299. Fails closed on drift.
Does not change source assertions, H/A/N, game type, score, date, or notes.
Run only on the owner-approved, main-bound dedicated maintenance branch.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EXPECTED_MAIN = "0a28151cf0c193afea2641cc5bd6f5557ab76d5b"
EXPECTED_CANONICAL_SHA256 = "9c3b705b1f64918010bf8ef650575b7e712f43192a1329f49fd39797906a0200"
EXPECTED_ASSERTIONS_SHA256 = "e57eef4766cf90022bdef2f78f514dc2fec95d69730965d2eab03539dd303cd9"
VENUE = {"venue_id": "VEN-000108", "venue_key": "lahaina-civic-center",
         "display_name": "Lahaina Civic Center", "city": "Lahaina", "state": "HI"}
EXPECTED = {
    "CBBG-0014297": {
        "season_label": "2019-2020", "game_date": "2019-11-25",
        "team_a_key": "chaminade", "team_b_key": "kansas",
    },
    "CBBG-0014299": {
        "season_label": "2019-2020", "game_date": "2019-11-27",
        "team_a_key": "dayton", "team_b_key": "kansas",
    },
}
CURRENT = {
    "site_type": "NEUTRAL", "game_type": "REGULAR_SEASON",
    "site_city": "Maui", "site_state": "", "venue_id": "", "venue_key": "",
}
NEW = {
    "site_city": "Lahaina", "site_state": "HI",
    "venue_id": "VEN-000108", "venue_key": "lahaina-civic-center",
}
CHANGE_FIELDS = frozenset(NEW)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def validate_venue(rows: list[dict[str, str]]) -> None:
    matching = [r for r in rows if r.get("venue_id") == VENUE["venue_id"]]
    if len(matching) != 1:
        raise ValueError("Expected exactly one registered Lahaina Civic Center venue")
    for key, value in VENUE.items():
        if matching[0].get(key) != value:
            raise ValueError(f"Registered venue drift: {key}")


def patch_rows(rows: list[dict[str, str]]) -> dict[str, object]:
    seen = set()
    changes = []
    for row in rows:
        gid = row.get("canonical_game_id", "").strip()
        if gid not in EXPECTED:
            continue
        if gid in seen:
            raise ValueError(f"Duplicate affected canonical ID: {gid}")
        seen.add(gid)
        required = {**EXPECTED[gid], **CURRENT}
        for key, expected in required.items():
            if row.get(key, "") != expected:
                raise ValueError(f"{gid}: expected {key}={expected!r}; got {row.get(key)!r}")
        for key, value in NEW.items():
            row[key] = value
        changes.append({"canonical_game_id": gid, "changed_fields": dict(NEW)})
    if seen != set(EXPECTED):
        raise ValueError("Expected exactly both authorized canonical IDs")
    return {"game_count": len(rows), "changed_game_ids": sorted(seen),
            "changes": sorted(changes, key=lambda r: r["canonical_game_id"])}


def write_csv_preserving_format(path: Path, fields: list[str],
                                rows: list[dict[str, str]]) -> None:
    raw = path.read_bytes()
    encoding = "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
    ending = "\r\n" if b"\r\n" in raw else "\n"
    temp = path.with_suffix(".csv.tmp")
    with temp.open("w", newline="", encoding=encoding) as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator=ending)
        writer.writeheader()
        writer.writerows(rows)
    temp.replace(path)


def execute(repo: Path, apply: bool) -> dict[str, object]:
    canonical = repo / "data/canonical/games.csv"
    assertions = repo / "data/evidence/game-assertions.csv"
    venues = repo / "data/reference/venues.csv"
    original = sha256_file(canonical)
    source_hash = sha256_file(assertions)
    if original != EXPECTED_CANONICAL_SHA256:
        raise ValueError(f"Canonical drift: {original}")
    if source_hash != EXPECTED_ASSERTIONS_SHA256:
        raise ValueError(f"Source assertion drift: {source_hash}")
    _, venue_rows = read_csv(venues)
    validate_venue(venue_rows)
    fields, rows = read_csv(canonical)
    if len(rows) != 186583:
        raise ValueError(f"Canonical row-count drift: {len(rows)}")
    if not set(NEW) <= set(fields):
        raise ValueError("Canonical geography/venue schema mismatch")
    # No source or nonapproved canonical fields are ever assigned.
    report = patch_rows(rows)
    report.update({
        "expected_main_sha": EXPECTED_MAIN,
        "original_canonical_sha256": original,
        "original_assertions_sha256": source_hash,
        "venue_id": VENUE["venue_id"],
        "site_type_preserved": "NEUTRAL",
        "apply": apply,
    })
    if not apply:
        return report
    write_csv_preserving_format(canonical, fields, rows)
    updated_fields, updated_rows = read_csv(canonical)
    if updated_fields != fields or len(updated_rows) != len(rows):
        raise ValueError("Postwrite canonical structure changed unexpectedly")
    updated_by_id = {r["canonical_game_id"]: r for r in updated_rows}
    if len(updated_by_id) != len(updated_rows):
        raise ValueError("Postwrite canonical IDs are not unique")
    for row in rows:
        if updated_by_id[row["canonical_game_id"]] != row:
            raise ValueError("Canonical CSV round-trip semantic drift")
    if sha256_file(assertions) != source_hash:
        raise ValueError("Source assertions changed unexpectedly")
    report["updated_canonical_sha256"] = sha256_file(canonical)
    subprocess.run([sys.executable, str(repo / "tools/build_site_data.py"),
                    str(repo), "--apply"], cwd=repo, check=True,
                   stdout=subprocess.DEVNULL)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()
    try:
        report = execute(args.repo.resolve(), args.apply)
        encoded = json.dumps(report, indent=2, sort_keys=True) + "\n"
        if args.manifest:
            args.manifest.write_text(encoded, encoding="utf-8")
        print(encoded)
        return 0
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"STOP: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
