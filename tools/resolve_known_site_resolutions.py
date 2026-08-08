#!/usr/bin/env python3
"""
Apply three already-curated Arkansas-Missouri site resolutions that were preserved
as discrepancies during ingestion but were not propagated into canonical games.

Default: DRY RUN
Apply:   python tools/resolve_known_site_resolutions.py --apply

This script is intentionally narrow and assertion-checked. It refuses to touch a row
unless the expected game identity and discrepancy record are present.
"""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path


CANONICAL_FIELDS = [
    "canonical_game_id","season_label","game_date","date_precision","team_a_key","team_b_key",
    "team_a_score","team_b_score","overtime_periods","site_type","designated_home_team_key",
    "venue_key","site_city","site_state","game_type","postseason_round","administrative_status",
    "administrative_note","canonical_status","notes",
]

DISCREPANCY_FIELDS = [
    "discrepancy_id","canonical_game_id","field_name","source_a_program_key","source_a_value",
    "source_b_program_key","source_b_value","canonical_value","status","resolution_basis","notes",
]

RESOLUTIONS = [
    {
        "canonical_game_id":"CBBG-0002600","discrepancy_id":"DISC-000009",
        "season_label":"2012-2013","game_date":"2013-02-16","team_a_key":"arkansas","team_b_key":"missouri",
        "team_a_score":"73","team_b_score":"71",
    },
    {
        "canonical_game_id":"CBBG-0002629","discrepancy_id":"DISC-000010",
        "season_label":"2013-2014","game_date":"2014-01-28","team_a_key":"arkansas","team_b_key":"missouri",
        "team_a_score":"71","team_b_score":"75",
    },
    {
        "canonical_game_id":"CBBG-0002703","discrepancy_id":"DISC-000011",
        "season_label":"2015-2016","game_date":"2016-02-20","team_a_key":"arkansas","team_b_key":"missouri",
        "team_a_score":"84","team_b_score":"72",
    },
]

BASIS = (
    "Resolved during Arkansas cross-source curation: Arkansas official year-by-year history "
    "places this game in Fayetteville; Bud Walton Arena was Arkansas's primary home venue. "
    "Missouri's prior home-site assertion is superseded; on-court score/result is unchanged."
)


def read_csv(path: Path) -> list[dict[str,str]]:
    with path.open(newline="",encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict[str,str]], fields: list[str]) -> None:
    tmp=path.with_suffix(path.suffix+".tmp")
    with tmp.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k:r.get(k,"") for k in fields})
    tmp.replace(path)


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--apply",action="store_true")
    ap.add_argument("--repo",type=Path,default=None)
    args=ap.parse_args()

    repo=args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    cpath=repo/"data"/"canonical"/"games.csv"
    dpath=repo/"data"/"reconciliation"/"discrepancies.csv"
    canonical=read_csv(cpath)
    discrepancies=read_csv(dpath)
    c_by={r.get("canonical_game_id",""):r for r in canonical}
    d_by={r.get("discrepancy_id",""):r for r in discrepancies}

    print("College Basketball History — known site resolutions")
    print(f"Repository: {repo}")
    print(f"Mode:       {'APPLY' if args.apply else 'DRY RUN'}")
    print()

    for spec in RESOLUTIONS:
        gid=spec["canonical_game_id"]
        did=spec["discrepancy_id"]
        c=c_by.get(gid)
        d=d_by.get(did)
        if c is None or d is None:
            print(f"FAIL: missing expected canonical/discrepancy row for {gid} / {did}")
            return 1

        for field in ["season_label","game_date","team_a_key","team_b_key","team_a_score","team_b_score"]:
            if c.get(field,"") != spec[field]:
                print(f"FAIL: {gid} identity check failed on {field}: {c.get(field,'')!r} != {spec[field]!r}")
                return 1

        if d.get("canonical_game_id","") != gid or d.get("field_name","") != "site_type":
            print(f"FAIL: {did} is not the expected site_type discrepancy for {gid}")
            return 1
        if d.get("source_a_program_key","") != "arkansas" or d.get("source_a_value","") != "TEAM_A_HOME":
            print(f"FAIL: {did} does not contain the expected Arkansas TEAM_A_HOME assertion.")
            return 1

        print(
            f"- {gid} | {spec['game_date']} | Arkansas-Missouri: "
            f"{c.get('site_type','')} / {c.get('venue_key','') or '(blank)'} "
            f"-> TEAM_A_HOME / bud-walton-arena / Fayetteville, AR"
        )

        c["site_type"]="TEAM_A_HOME"
        c["designated_home_team_key"]="arkansas"
        c["venue_key"]="bud-walton-arena"
        c["site_city"]="Fayetteville"
        c["site_state"]="AR"

        d["canonical_value"]="TEAM_A_HOME"
        d["status"]="RESOLVED"
        d["resolution_basis"]=BASIS
        d["notes"]="Canonical site corrected to Arkansas home; prior source assertions remain preserved."

    print()
    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        return 0

    write_csv(cpath,canonical,CANONICAL_FIELDS)
    write_csv(dpath,discrepancies,DISCREPANCY_FIELDS)

    validator=repo/"tools"/"validate_data.py"
    if validator.exists():
        result=subprocess.run([sys.executable,str(validator),str(repo)])
        if result.returncode != 0:
            print("FAIL: corrections applied, but validator failed.")
            return result.returncode
    print()
    print("PASS: three known Arkansas-Missouri site resolutions applied.")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
