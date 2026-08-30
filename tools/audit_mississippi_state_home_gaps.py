#!/usr/bin/env python3
"""Read-only audit of Mississippi State published HOME venue/location debt.

This diagnostic intentionally does not assign venues. It inventories the exact
remaining source/canonical HOME-gap universe and classifies rows into historically
meaningful eras so remediation can be researched without back-projecting Tin Gym
or another later facility onto earlier games.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

PROGRAM = "mississippi-state"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def canonical_home(row: dict[str, str]) -> bool:
    site = row.get("site_type", "").strip()
    return (
        site == "TEAM_A_HOME" and row.get("team_a_key", "").strip() == PROGRAM
    ) or (
        site == "TEAM_B_HOME" and row.get("team_b_key", "").strip() == PROGRAM
    )


def source_gap(row: dict[str, str]) -> bool:
    return (
        row.get("curated_site_type", "").strip() == "SOURCE_PROGRAM_HOME"
        and (
            not row.get("curated_venue_name", "").strip()
            or not row.get("city", "").strip()
            or not row.get("state", "").strip()
        )
    )


def canonical_gap(row: dict[str, str]) -> bool:
    return canonical_home(row) and (
        not row.get("venue_id", "").strip()
        or not row.get("site_city", "").strip()
        or not row.get("site_state", "").strip()
    )


def era(season: str, date: str) -> str:
    if not season or len(season) < 4:
        return "INVALID_OR_UNKNOWN"
    try:
        start = int(season[:4])
    except ValueError:
        return "INVALID_OR_UNKNOWN"
    if start <= 1918:
        return "PRE_1920_NO_INDOOR_COURT"
    if start == 1919:
        return "1919_20_TRANSITION_CALENDAR_1920"
    if 1920 <= start <= 1928:
        return "1920S_PRE_TIN_INDOOR_FACILITY"
    if start == 1929:
        return "1929_30_OFFICIAL_ALL_ROAD_SEASON"
    if start == 1930:
        return "1930_31_NO_TEAM"
    if start == 1931:
        if date and date < "1932-01-25":
            return "1931_32_BEFORE_TIN_OPENER"
        return "TIN_GYM_ERA"
    if start <= 1949:
        return "TIN_GYM_ERA"
    if start == 1950 and date and date < "1950-12-15":
        return "TIN_GYM_ERA"
    if start <= 1974:
        return "MCCARTHY_GYM_ERA"
    if start == 1975 and date and date < "1975-12-01":
        return "MCCARTHY_GYM_ERA"
    return "HUMPHREY_COLISEUM_ERA"


def source_summary(row: dict[str, str]) -> dict[str, str]:
    return {
        "source_game_id": row.get("source_game_id", ""),
        "season_label": row.get("season_label", ""),
        "game_date": row.get("game_date", ""),
        "opponent": row.get("normalized_opponent_key", ""),
        "source_site_candidate": row.get("source_site_candidate", ""),
        "curated_site_type": row.get("curated_site_type", ""),
        "venue": row.get("curated_venue_name", ""),
        "city": row.get("city", ""),
        "state": row.get("state", ""),
        "raw_text": row.get("raw_text", ""),
        "era": era(row.get("season_label", ""), row.get("game_date", "")),
    }


def canonical_summary(row: dict[str, str]) -> dict[str, str]:
    return {
        "canonical_game_id": row.get("canonical_game_id", ""),
        "season_label": row.get("season_label", ""),
        "game_date": row.get("game_date", ""),
        "team_a_key": row.get("team_a_key", ""),
        "team_b_key": row.get("team_b_key", ""),
        "site_type": row.get("site_type", ""),
        "designated_home_team_key": row.get("designated_home_team_key", ""),
        "venue_key": row.get("venue_key", ""),
        "venue_id": row.get("venue_id", ""),
        "site_city": row.get("site_city", ""),
        "site_state": row.get("site_state", ""),
        "era": era(row.get("season_label", ""), row.get("game_date", "")),
    }


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    sources = read_csv(repo / "schools/mississippi-state/source-games.csv")
    canonical = read_csv(repo / "data/canonical/games.csv")
    assertions = read_csv(repo / "data/evidence/game-assertions.csv")

    source_rows = [r for r in sources if source_gap(r)]
    canonical_rows = [r for r in canonical if canonical_gap(r)]
    canonical_by_id = {
        r.get("canonical_game_id", "").strip(): r
        for r in canonical
        if r.get("canonical_game_id", "").strip()
    }

    assertion_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        if row.get("source_program_key", "").strip() == PROGRAM:
            assertion_by_source[row.get("source_game_id", "").strip()].append(row)

    source_to_canonical: dict[str, list[str]] = {}
    for row in source_rows:
        sid = row.get("source_game_id", "").strip()
        source_to_canonical[sid] = sorted({
            a.get("canonical_game_id", "").strip()
            for a in assertion_by_source.get(sid, [])
            if a.get("canonical_game_id", "").strip()
        })

    src_eras = Counter(era(r.get("season_label", ""), r.get("game_date", "")) for r in source_rows)
    can_eras = Counter(era(r.get("season_label", ""), r.get("game_date", "")) for r in canonical_rows)

    src_missing = Counter()
    for r in source_rows:
        if not r.get("curated_venue_name", "").strip():
            src_missing["venue"] += 1
        if not r.get("city", "").strip():
            src_missing["city"] += 1
        if not r.get("state", "").strip():
            src_missing["state"] += 1

    can_missing = Counter()
    for r in canonical_rows:
        if not r.get("venue_id", "").strip():
            can_missing["venue"] += 1
        if not r.get("site_city", "").strip():
            can_missing["city"] += 1
        if not r.get("site_state", "").strip():
            can_missing["state"] += 1

    canonical_ids = {r.get("canonical_game_id", "").strip() for r in canonical_rows}
    mapped_ids = {cid for ids in source_to_canonical.values() for cid in ids if cid}
    problematic_mappings = {sid: ids for sid, ids in source_to_canonical.items() if len(ids) != 1}

    print("College Basketball History — Mississippi State HOME-gap audit")
    print(f"Source HOME gaps:      {len(source_rows)}")
    print(f"Canonical HOME gaps:   {len(canonical_rows)}")
    print(f"Source missing fields: {json.dumps(dict(src_missing), sort_keys=True)}")
    print(f"Canon missing fields:  {json.dumps(dict(can_missing), sort_keys=True)}")
    print(f"Source era counts:     {json.dumps(dict(sorted(src_eras.items())), sort_keys=True)}")
    print(f"Canon era counts:      {json.dumps(dict(sorted(can_eras.items())), sort_keys=True)}")
    print(f"Bad source mappings:   {len(problematic_mappings)}")
    print(f"Canonical-only gaps:   {len(canonical_ids - mapped_ids)}")
    print(f"Mapped outside gaps:   {len(mapped_ids - canonical_ids)}")

    if problematic_mappings:
        print("SOURCE MAPPING EXCEPTIONS:")
        for sid, ids in sorted(problematic_mappings.items()):
            print("  " + json.dumps({"source_game_id": sid, "canonical_ids": ids}, sort_keys=True))

    if canonical_ids - mapped_ids:
        print("CANONICAL-ONLY GAP IDS:")
        for gid in sorted(canonical_ids - mapped_ids):
            row = next(r for r in canonical_rows if r.get("canonical_game_id", "").strip() == gid)
            print("  " + json.dumps(canonical_summary(row), sort_keys=True))

    outside_ids = sorted(mapped_ids - canonical_ids)
    if outside_ids:
        print("MAPPED OUTSIDE CURRENT CANONICAL-HOME GAP SET:")
        for gid in outside_ids:
            row = canonical_by_id.get(gid)
            source_matches = [
                r for r in source_rows
                if gid in source_to_canonical.get(r.get("source_game_id", "").strip(), [])
            ]
            payload = {
                "canonical": canonical_summary(row) if row else {"canonical_game_id": gid, "missing": "true"},
                "source_rows": [source_summary(r) for r in source_matches],
            }
            print("  " + json.dumps(payload, sort_keys=True))

    print("\nSEASON BREAKDOWN (source gaps):")
    season_counts = Counter(r.get("season_label", "") for r in source_rows)
    for season, count in sorted(season_counts.items()):
        print(f"  {season}: {count}")

    print("\n1919-20 TRANSITION SOURCE ROWS:")
    transition_rows = [
        r for r in source_rows
        if era(r.get("season_label", ""), r.get("game_date", ""))
        == "1919_20_TRANSITION_CALENDAR_1920"
    ]
    for row in sorted(transition_rows, key=lambda r: (r.get("game_date", ""), r.get("source_game_id", ""))):
        print("  " + json.dumps(source_summary(row), sort_keys=True))

    print("\nPOST-1932 SOURCE HOME GAPS:")
    post_1932_rows = [
        r for r in source_rows
        if era(r.get("season_label", ""), r.get("game_date", ""))
        in {"MCCARTHY_GYM_ERA", "HUMPHREY_COLISEUM_ERA"}
    ]
    for row in sorted(post_1932_rows, key=lambda r: (r.get("game_date", ""), r.get("source_game_id", ""))):
        print("  " + json.dumps(source_summary(row), sort_keys=True))

    print("\nJACKSON SOURCE HOME GAPS:")
    jackson_rows = [r for r in source_rows if r.get("city", "").strip().lower() == "jackson"]
    for row in sorted(jackson_rows, key=lambda r: (r.get("game_date", ""), r.get("source_game_id", ""))):
        print("  " + json.dumps(source_summary(row), sort_keys=True))

    print("\nEARLIEST/LATEST SOURCE GAP ROWS:")
    ordered = sorted(source_rows, key=lambda r: (r.get("game_date", ""), r.get("source_game_id", "")))
    for row in (ordered[:8] + ordered[-8:] if ordered else []):
        print("  " + json.dumps(source_summary(row), sort_keys=True))

    suspicious = [
        r for r in source_rows
        if era(r.get("season_label", ""), r.get("game_date", ""))
        in {"1929_30_OFFICIAL_ALL_ROAD_SEASON", "1930_31_NO_TEAM", "1931_32_BEFORE_TIN_OPENER"}
    ]
    print(f"\nHistorically suspicious HOME gaps: {len(suspicious)}")
    for row in suspicious:
        print("  " + json.dumps(source_summary(row), sort_keys=True))

    print("\nPASS: diagnostic only; no tracked basketball data changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
