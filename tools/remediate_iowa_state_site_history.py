#!/usr/bin/env python3
"""Sealed deterministic site-history remediation for Iowa State onboarding.

This tool records a bounded Implementation Stage 2 repair discovered by the
pre-Gate releaseability challenge.  It fixes only the explicitly enumerated
canonical rows below plus two Iowa State source-normalization rows whose H/A/N
classification was contradicted by stronger official evidence.

Literal source labels and raw_text are preserved.  Existing reciprocal assertions
remain untouched as evidence.  Default mode is dry-run; --apply requires the exact
SHA-256 emitted by a dry-run against the same repository state.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


class IowaStateSiteError(RuntimeError):
    pass


def clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head(repo: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    raw = path.read_bytes()
    has_bom = raw.startswith(b"\xef\xbb\xbf")
    line_ending = "\r\n" if b"\r\n" in raw else "\n"
    encoding = "utf-8-sig" if has_bom else "utf-8"
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=line_ending)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})
    temp.replace(path)


def append_note(existing: str, marker: str) -> str:
    text = clean(existing)
    if marker in text:
        return text
    return f"{text} | {marker}" if text else marker


# Expected values intentionally include identity/score controls as well as the fields
# being changed.  Any drift causes a stop rather than an opportunistic rewrite.
CANONICAL_REPAIRS: list[dict[str, Any]] = [
    {
        "id": "CBBG-0000483",
        "expected": {
            "season_label": "1934-1935", "game_date": "1935-01-26",
            "team_a_key": "iowa-state", "team_b_key": "missouri",
            "team_a_score": "37", "team_b_score": "28",
            "site_type": "TEAM_A_HOME", "designated_home_team_key": "iowa-state",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "site_type": "TEAM_B_HOME", "designated_home_team_key": "missouri",
            "site_city": "Columbia", "site_state": "MO",
        },
        "basis": "Iowa State official 1934-35 schedule and opponent history place the Jan. 26, 1935 Missouri game at Missouri in Columbia; this supersedes the stale canonical Iowa State-home classification.",
    },
    {
        "id": "CBBG-0001414",
        "expected": {
            "season_label": "1975-1976", "game_date": "1976-02-15",
            "team_a_key": "iowa-state", "team_b_key": "missouri",
            "team_a_score": "64", "team_b_score": "85",
            "site_type": "TEAM_A_HOME", "designated_home_team_key": "iowa-state",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "game_date": "1976-02-14", "site_type": "TEAM_B_HOME",
            "designated_home_team_key": "missouri", "site_city": "Columbia",
            "site_state": "MO",
        },
        "basis": "Iowa State official 1975-76 schedule/opponent history place the 64-85 Missouri game on Feb. 14, 1976 at Missouri in Columbia; the prior Feb. 15 Iowa State-home canonical row is stale.",
    },
    {
        "id": "CBBG-0043910",
        "expected": {
            "season_label": "1974-1975", "game_date": "1974-12-12",
            "team_a_key": "iowa", "team_b_key": "iowa-state",
            "team_a_score": "77", "team_b_score": "66",
            "site_type": "TEAM_B_HOME", "designated_home_team_key": "iowa-state",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "site_type": "TEAM_A_HOME", "designated_home_team_key": "iowa",
            "venue_id": "VEN-000091", "venue_key": "iowa-field-house",
            "site_city": "Iowa City", "site_state": "IA",
        },
        "basis": "Iowa State official 1974-75 schedule places the Dec. 12 game at Iowa in Iowa City; contemporaneous Daily Iowan coverage says Iowa hosted Iowa State at the Field House.",
    },
    {
        "id": "CBBG-0054503",
        "expected": {
            "season_label": "1943-1944", "game_date": "1944-01-08",
            "team_a_key": "iowa-state", "team_b_key": "nebraska",
            "team_a_score": "56", "team_b_score": "24",
            "site_type": "TEAM_A_HOME", "designated_home_team_key": "iowa-state",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "venue_id": "VEN-000493", "venue_key": "iowa-state-state-gym",
            "site_city": "Ames", "site_state": "IA",
        },
        "basis": "Iowa State official Nebraska opponent history places Jan. 8, 1944 in Ames, and Iowa State's official All-Time Home Courts history establishes State Gym as the home court through 1945-46.",
    },
    {
        "id": "CBBG-0054512",
        "expected": {
            "season_label": "1944-1945", "game_date": "1945-01-08",
            "team_a_key": "iowa-state", "team_b_key": "nebraska",
            "team_a_score": "50", "team_b_score": "38",
            "site_type": "TEAM_A_HOME", "designated_home_team_key": "iowa-state",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "site_type": "TEAM_B_HOME", "designated_home_team_key": "nebraska",
            "venue_id": "VEN-000312", "venue_key": "nebraska-coliseum",
            "site_city": "Lincoln", "site_state": "NE",
        },
        "basis": "Iowa State official 1944-45 schedule and Nebraska opponent history place Jan. 8, 1945 at Nebraska in Lincoln; Nebraska Coliseum is the registered 1926-era Nebraska home venue.",
    },
    {
        "id": "CBBG-0085298",
        "expected": {
            "season_label": "1923-1924", "game_date": "1924-03-01",
            "team_a_key": "iowa-state", "team_b_key": "kansas-state",
            "team_a_score": "20", "team_b_score": "24",
            "site_type": "TEAM_A_HOME", "designated_home_team_key": "iowa-state",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "site_type": "TEAM_B_HOME", "designated_home_team_key": "kansas-state",
            "site_city": "Manhattan", "site_state": "KS",
        },
        "basis": "Iowa State official Kansas State opponent history places Mar. 1, 1924 away in Manhattan, Kansas; exact building is not asserted here.",
    },
    {
        "id": "CBBG-0007429",
        "expected": {
            "season_label": "1982-1983", "game_date": "1983-01-03",
            "team_a_key": "illinois", "team_b_key": "iowa-state",
            "team_a_score": "74", "team_b_score": "57",
            "site_type": "NEUTRAL", "designated_home_team_key": "",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "venue_id": "VEN-000004", "venue_key": "allstate-arena",
            "site_city": "Rosemont", "site_state": "IL",
        },
        "basis": "Illinois official opponent history places Jan. 3, 1983 at neutral Rosemont; Rosemont's official arena history identifies the Rosemont Horizon as the physical arena now registered as Allstate Arena.",
    },
    {
        "id": "CBBG-0061770",
        "expected": {
            "season_label": "1944-1945", "game_date": "",
            "team_a_key": "iowa-state", "team_b_key": "oklahoma",
            "team_a_score": "31", "team_b_score": "29",
            "site_type": "NEUTRAL", "designated_home_team_key": "",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "game_date": "1945-02-24", "site_type": "TEAM_B_HOME",
            "designated_home_team_key": "oklahoma", "site_city": "Norman",
            "site_state": "OK",
        },
        "basis": "Iowa State official 1944-45 schedule and Oklahoma opponent history identify the 31-29 game as Feb. 24, 1945 at Oklahoma in Norman; no exact building is forced.",
    },
    {
        "id": "CBBG-0029729",
        "expected": {
            "season_label": "2019-2020", "game_date": "2019-11-28",
            "team_a_key": "alabama", "team_b_key": "iowa-state",
            "team_a_score": "89", "team_b_score": "104",
            "site_type": "UNKNOWN", "designated_home_team_key": "",
            "venue_id": "", "venue_key": "", "site_city": "", "site_state": "",
        },
        "patch": {
            "site_type": "NEUTRAL", "venue_id": "VEN-000088",
            "venue_key": "imperial-arena", "site_city": "Nassau", "site_state": "BS",
        },
        "basis": "Official 2019 Battle 4 Atlantis material places Alabama-Iowa State at neutral Imperial Arena in the Bahamas; the existing venue registry owns Nassau, BS geography.",
    },
]

SOURCE_REPAIRS: list[dict[str, Any]] = [
    {
        "id": "ISURAW-00590",
        "expected": {
            "season_label": "1943-1944", "game_date": "1944-01-08",
            "normalized_opponent_key": "nebraska", "team_score": "56",
            "opponent_score": "24", "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": "", "city": "", "state": "",
        },
        "patch": {
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "State Gym", "city": "Ames", "state": "IA",
        },
        "basis": "Implementation Stage 2 correction: Iowa State official Nebraska opponent history places Jan. 8, 1944 in Ames; official All-Time Home Courts history establishes State Gym for this season. Literal raw_text is retained as conflicting source evidence.",
    },
    {
        "id": "ISURAW-01529",
        "expected": {
            "season_label": "1982-1983", "game_date": "1983-01-03",
            "normalized_opponent_key": "illinois", "team_score": "57",
            "opponent_score": "74", "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": "", "city": "", "state": "",
        },
        "patch": {
            "curated_site_type": "NEUTRAL", "curated_venue_name": "Allstate Arena",
            "city": "Rosemont", "state": "IL",
        },
        "basis": "Implementation Stage 2 correction: Illinois official history identifies this as a neutral game in Rosemont; the Rosemont Horizon physical venue is the registered Allstate Arena identity. Literal raw_text is retained as source evidence.",
    },
]


def validate_venue_patch(venues: dict[str, dict[str, str]], patch: dict[str, str], game_id: str) -> None:
    venue_id = clean(patch.get("venue_id"))
    venue_key = clean(patch.get("venue_key"))
    if bool(venue_id) != bool(venue_key):
        raise IowaStateSiteError(f"{game_id}: venue_id/key must be supplied together")
    if not venue_id:
        return
    venue = venues.get(venue_id)
    if venue is None:
        raise IowaStateSiteError(f"{game_id}: unknown venue_id {venue_id}")
    if clean(venue.get("venue_key")) != venue_key:
        raise IowaStateSiteError(f"{game_id}: venue key mismatch for {venue_id}")
    city, state = clean(patch.get("site_city")), clean(patch.get("site_state"))
    if city and city != clean(venue.get("city")):
        raise IowaStateSiteError(f"{game_id}: proposed city disagrees with venue registry")
    if state and state != clean(venue.get("state")):
        raise IowaStateSiteError(f"{game_id}: proposed state disagrees with venue registry")


def build_plan(repo: Path) -> dict[str, Any]:
    repo = repo.resolve()
    canonical_path = repo / "data/canonical/games.csv"
    source_path = repo / "schools/iowa-state/source-games.csv"
    venue_path = repo / "data/reference/venues.csv"
    for path in (canonical_path, source_path, venue_path):
        if not path.is_file():
            raise IowaStateSiteError(f"required file missing: {path}")

    _, canonical_rows = read_csv(canonical_path)
    _, source_rows = read_csv(source_path)
    _, venue_rows = read_csv(venue_path)
    canonical = {clean(r.get("canonical_game_id")): r for r in canonical_rows}
    source = {clean(r.get("source_game_id")): r for r in source_rows}
    venues = {clean(r.get("venue_id")): r for r in venue_rows if clean(r.get("venue_id"))}

    planned_canonical: list[dict[str, Any]] = []
    for spec in CANONICAL_REPAIRS:
        game_id = spec["id"]
        row = canonical.get(game_id)
        if row is None:
            raise IowaStateSiteError(f"{game_id}: canonical row missing")
        for field, expected in spec["expected"].items():
            actual = clean(row.get(field))
            if actual != clean(expected):
                raise IowaStateSiteError(
                    f"{game_id}: expected {field}={expected!r}, found {actual!r}"
                )
        patch = {k: clean(v) for k, v in spec["patch"].items()}
        if bool(patch.get("site_city")) != bool(patch.get("site_state")):
            raise IowaStateSiteError(f"{game_id}: location patch must be an atomic pair")
        validate_venue_patch(venues, patch, game_id)
        final_site = patch.get("site_type", clean(row.get("site_type")))
        final_home = patch.get("designated_home_team_key", clean(row.get("designated_home_team_key")))
        if final_site == "TEAM_A_HOME" and final_home != clean(row.get("team_a_key")):
            raise IowaStateSiteError(f"{game_id}: TEAM_A_HOME designated-home mismatch")
        if final_site == "TEAM_B_HOME" and final_home != clean(row.get("team_b_key")):
            raise IowaStateSiteError(f"{game_id}: TEAM_B_HOME designated-home mismatch")
        if final_site == "NEUTRAL" and final_home:
            raise IowaStateSiteError(f"{game_id}: neutral game must not designate a home team")
        planned_canonical.append({"canonical_game_id": game_id, "patch": patch, "basis": spec["basis"]})

    planned_source: list[dict[str, Any]] = []
    for spec in SOURCE_REPAIRS:
        source_id = spec["id"]
        row = source.get(source_id)
        if row is None:
            raise IowaStateSiteError(f"{source_id}: source row missing")
        for field, expected in spec["expected"].items():
            actual = clean(row.get(field))
            if actual != clean(expected):
                raise IowaStateSiteError(
                    f"{source_id}: expected {field}={expected!r}, found {actual!r}"
                )
        patch = {k: clean(v) for k, v in spec["patch"].items()}
        if bool(patch.get("city")) != bool(patch.get("state")):
            raise IowaStateSiteError(f"{source_id}: source location patch must be atomic")
        planned_source.append({"source_game_id": source_id, "patch": patch, "basis": spec["basis"]})

    payload = {
        "schema_version": 1,
        "git_head": git_head(repo),
        "canonical_repairs": planned_canonical,
        "source_repairs": planned_source,
        "accepted_unmodified_residual": {
            "source_game_id": "ISURAW-01207",
            "description": "1970-12-19 Holy Cross, Marshall Tournament, Huntington WV; exact physical building remains RESEARCHED_UNRESOLVED by accepted Research freeze.",
        },
        "fingerprints": {
            "data/canonical/games.csv": sha_file(canonical_path),
            "schools/iowa-state/source-games.csv": sha_file(source_path),
            "data/reference/venues.csv": sha_file(venue_path),
        },
    }
    return {"sha256": sha_text(stable(payload)), "payload": payload}


def apply_plan(repo: Path, expected_sha256: str) -> dict[str, Any]:
    plan = build_plan(repo)
    if clean(expected_sha256) != plan["sha256"]:
        raise IowaStateSiteError(
            f"sealed plan hash mismatch: expected {expected_sha256}, actual {plan['sha256']}"
        )
    canonical_path = repo / "data/canonical/games.csv"
    source_path = repo / "schools/iowa-state/source-games.csv"
    originals = {canonical_path: canonical_path.read_bytes(), source_path: source_path.read_bytes()}
    try:
        canonical_fields, canonical_rows = read_csv(canonical_path)
        source_fields, source_rows = read_csv(source_path)
        canonical = {clean(r.get("canonical_game_id")): r for r in canonical_rows}
        source = {clean(r.get("source_game_id")): r for r in source_rows}

        canonical_changes = 0
        source_changes = 0
        for item in plan["payload"]["canonical_repairs"]:
            row = canonical[item["canonical_game_id"]]
            for field, value in item["patch"].items():
                if field not in canonical_fields:
                    raise IowaStateSiteError(f"{item['canonical_game_id']}: missing canonical field {field}")
                if clean(row.get(field)) != value:
                    row[field] = value
                    canonical_changes += 1
            marker = (
                "[IOWA_STATE_IMPLEMENTATION_SITE_RECONCILIATION "
                f"basis={item['basis']}]"
            )
            before = clean(row.get("notes"))
            row["notes"] = append_note(before, marker)
            if clean(row.get("notes")) != before:
                canonical_changes += 1

        for item in plan["payload"]["source_repairs"]:
            row = source[item["source_game_id"]]
            raw_before = row.get("raw_text", "")
            label_before = row.get("source_opponent_label", "")
            for field, value in item["patch"].items():
                if field not in source_fields:
                    raise IowaStateSiteError(f"{item['source_game_id']}: missing source field {field}")
                if clean(row.get(field)) != value:
                    row[field] = value
                    source_changes += 1
            row["notes"] = append_note(row.get("notes", ""), item["basis"])
            if row.get("raw_text", "") != raw_before or row.get("source_opponent_label", "") != label_before:
                raise IowaStateSiteError(f"{item['source_game_id']}: literal source evidence changed")

        write_csv(canonical_path, canonical_fields, canonical_rows)
        write_csv(source_path, source_fields, source_rows)

        completed = subprocess.run([sys.executable, "tools/validate_data.py"], cwd=repo, text=True)
        if completed.returncode != 0:
            raise IowaStateSiteError("repository validation failed after Iowa State site remediation")
    except Exception:
        for path, raw in originals.items():
            path.write_bytes(raw)
        raise

    return {
        "plan_sha256": plan["sha256"],
        "canonical_games_repaired": len(plan["payload"]["canonical_repairs"]),
        "source_rows_repaired": len(plan["payload"]["source_repairs"]),
        "canonical_fields_changed": canonical_changes,
        "source_fields_changed": source_changes,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--expected-plan-sha256", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        plan = build_plan(repo)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        if not args.apply:
            payload = plan["payload"]
            print("College Basketball History — Iowa State deterministic site-history plan")
            print(f"Git HEAD:             {payload['git_head']}")
            print(f"Canonical repairs:    {len(payload['canonical_repairs'])}")
            print(f"Source corrections:   {len(payload['source_repairs'])}")
            print(f"Accepted residual:    {payload['accepted_unmodified_residual']['source_game_id']}")
            print(f"Plan SHA-256:         {plan['sha256']}")
            for item in payload["canonical_repairs"]:
                print(f"  {item['canonical_game_id']} -> " + json.dumps(item["patch"], sort_keys=True))
            print("DRY RUN: no tracked basketball data changed.")
            return 0
        result = apply_plan(repo, args.expected_plan_sha256)
        print("PASS: IOWA STATE DETERMINISTIC SITE-HISTORY REMEDIATION")
        for key, value in result.items():
            print(f"{key}={value}")
        return 0
    except (IowaStateSiteError, FileNotFoundError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
