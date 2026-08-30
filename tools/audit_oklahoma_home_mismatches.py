#!/usr/bin/env python3
"""Read-only diagnostic for Oklahoma HOME source/canonical mismatch rows."""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

PROGRAM = "oklahoma"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def canonical_oklahoma_home(row: dict[str, str]) -> bool:
    site = row.get("site_type", "").strip()
    return (
        site == "TEAM_A_HOME" and row.get("team_a_key", "").strip() == PROGRAM
    ) or (
        site == "TEAM_B_HOME" and row.get("team_b_key", "").strip() == PROGRAM
    )


def has_site_gap(row: dict[str, str]) -> bool:
    return not (
        row.get("venue_key", "").strip()
        and row.get("venue_id", "").strip()
        and row.get("site_city", "").strip()
        and row.get("site_state", "").strip()
    )


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    sources = read_csv(repo / "schools/oklahoma/source-games.csv")
    assertions = read_csv(repo / "data/evidence/game-assertions.csv")
    canonical = read_csv(repo / "data/canonical/games.csv")

    canonical_by_id = {row["canonical_game_id"].strip(): row for row in canonical}
    assertions_by_source: dict[str, list[dict[str, str]]] = defaultdict(list)
    assertions_by_canonical: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in assertions:
        cid = row.get("canonical_game_id", "").strip()
        if cid:
            assertions_by_canonical[cid].append(row)
        if row.get("source_program_key", "").strip() == PROGRAM:
            assertions_by_source[row.get("source_game_id", "").strip()].append(row)

    source_home_gap_ids: set[str] = set()
    source_to_canonical: dict[str, str] = {}
    for source in sources:
        if source.get("curated_site_type", "").strip() != "SOURCE_PROGRAM_HOME":
            continue
        if source.get("curated_venue_name", "").strip() and source.get("city", "").strip() and source.get("state", "").strip():
            continue
        sid = source.get("source_game_id", "").strip()
        matches = assertions_by_source.get(sid, [])
        if len(matches) == 1:
            cid = matches[0].get("canonical_game_id", "").strip()
            source_home_gap_ids.add(cid)
            source_to_canonical[sid] = cid

    canonical_home_gap_ids = {
        row.get("canonical_game_id", "").strip()
        for row in canonical
        if canonical_oklahoma_home(row) and has_site_gap(row)
    }

    print("=== COUNT ARITHMETIC ===")
    print(f"source_home_gap_canonical_ids={len(source_home_gap_ids)}")
    print(f"canonical_home_gap_ids={len(canonical_home_gap_ids)}")
    print(f"source_only={len(source_home_gap_ids - canonical_home_gap_ids)}")
    print(f"canonical_only={len(canonical_home_gap_ids - source_home_gap_ids)}")

    def dump_canonical(cid: str) -> None:
        game = canonical_by_id[cid]
        print(
            f"CANONICAL {cid} {game.get('season_label','')} {game.get('game_date','')} "
            f"{game.get('team_a_key','')} vs {game.get('team_b_key','')} "
            f"score={game.get('team_a_score','')}-{game.get('team_b_score','')} "
            f"site={game.get('site_type','')} home={game.get('designated_home_team_key','')} "
            f"venue={game.get('venue_key','')}/{game.get('venue_id','')} "
            f"location={game.get('site_city','')},{game.get('site_state','')}"
        )
        for a in assertions_by_canonical.get(cid, []):
            print(
                "  ASSERTION "
                f"program={a.get('source_program_key','')} source={a.get('source_game_id','')} "
                f"site_candidate={a.get('source_site_candidate','')!r} "
                f"curated_site={a.get('curated_site_type','')!r} "
                f"venue={a.get('curated_venue_name','')!r} "
                f"location={a.get('city','')!r},{a.get('state','')!r} "
                f"raw={a.get('raw_text','')!r}"
            )

    print("\n=== SOURCE-HOME GAP BUT CANONICAL NOT OKLAHOMA HOME ===")
    for cid in sorted(source_home_gap_ids - canonical_home_gap_ids):
        dump_canonical(cid)

    print("\n=== CANONICAL OKLAHOMA-HOME GAP WITHOUT SOURCE-HOME GAP ===")
    for cid in sorted(canonical_home_gap_ids - source_home_gap_ids):
        dump_canonical(cid)

    print("\n=== KNOWN HELD SOURCE ROWS ===")
    by_source = {row.get("source_game_id", "").strip(): row for row in sources}
    for sid in ("OKLRAW-00218", "OKLRAW-01226"):
        row = by_source[sid]
        print(
            f"SOURCE {sid} {row.get('season_label','')} {row.get('game_date','')} "
            f"opp={row.get('normalized_opponent_key','')} score={row.get('team_score','')}-{row.get('opponent_score','')} "
            f"site_candidate={row.get('source_site_candidate','')!r} curated_site={row.get('curated_site_type','')!r} "
            f"raw={row.get('raw_text','')!r}"
        )
        matches = assertions_by_source.get(sid, [])
        if len(matches) == 1:
            dump_canonical(matches[0].get("canonical_game_id", "").strip())

    print("\nPASS: diagnostic only; no tracked data changed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
