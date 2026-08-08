#!/usr/bin/env python3
"""
Resolve five known Kentucky cross-source discrepancies after Kentucky ingestion.

Default: DRY RUN
Apply:   python tools/resolve_known_kentucky_reconciliation.py --apply

This script is deliberately narrow. It checks the canonical game identity and the
expected Kentucky discrepancy before changing anything. Source assertions are never
rewritten; only canonical values and discrepancy resolution metadata are updated.
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
        "game_id":"CBBG-0012502","season":"1959-1960","date":"1959-12-14",
        "team_a":"kansas","team_b":"kentucky","field":"overtime_periods",
        "source_value":"1","old_canonical":"0","new_canonical":"1",
        "basis":"Kentucky official record-book game row explicitly marks the Dec. 14, 1959 win at Kansas as overtime; independent historical schedule data corroborates OT. Kansas's current schedule listing gives the score but omits an OT marker.",
    },
    {
        "game_id":"CBBG-0007001","season":"1966-1967","date":"1966-12-05",
        "team_a":"illinois","team_b":"kentucky","field":"overtime_periods",
        "source_value":"1","old_canonical":"0","new_canonical":"1",
        "basis":"Kentucky's official record book marks the Dec. 5, 1966 Illinois game as overtime, and Illinois Athletics' current historical schedule/opponent history independently identifies the 98-97 win as OT.",
    },
    {
        "game_id":"CBBG-0002602","season":"2012-2013","date":"2013-02-23",
        "team_a":"kentucky","team_b":"missouri","field":"overtime_periods",
        "source_value":"1","old_canonical":"0","new_canonical":"1",
        "basis":"Kentucky's official record book marks the Feb. 23, 2013 Missouri game as overtime; Missouri Athletics' official schedule, recap and box score also explicitly record a 90-83 OT result.",
    },
    {
        "game_id":"CBBG-0005736","season":"2022-2023","date":"2023-02-07",
        "team_a":"arkansas","team_b":"kentucky","field":"score",
        "source_value":"86-73","old_canonical":"88-73","new_canonical":"88-73",
        "basis":"Contemporary official Arkansas and Kentucky records establish Arkansas 88, Kentucky 73. The later Kentucky record-book row showing 86-73 is retained as source evidence but does not replace the canonical final score.",
    },
    {
        "game_id":"CBBG-0005768","season":"2023-2024","date":"2024-01-27",
        "team_a":"arkansas","team_b":"kentucky","field":"score",
        "source_value":"57-63","old_canonical":"51-63","new_canonical":"57-63",
        "basis":"Contemporary official Arkansas and Kentucky box scores both establish Kentucky 63, Arkansas 57. Arkansas's later guide assertion of 51-63 remains preserved as source evidence.",
    },
]

def read_csv(path: Path):
    with path.open(newline="",encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def write_csv(path: Path, rows, fields):
    tmp=path.with_suffix(path.suffix+".tmp")
    with tmp.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k:r.get(k,"") for k in fields})
    tmp.replace(path)

def canonical_field_value(row, field):
    if field=="score":
        return f"{row.get('team_a_score','')}-{row.get('team_b_score','')}"
    return row.get(field,"")

def set_canonical_field(row, field, value):
    if field=="score":
        a,b=value.split("-",1)
        row["team_a_score"]=a
        row["team_b_score"]=b
    else:
        row[field]=value

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--apply",action="store_true")
    ap.add_argument("--repo",type=Path,default=None)
    args=ap.parse_args()
    repo=args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    cp=repo/"data"/"canonical"/"games.csv"
    dp=repo/"data"/"reconciliation"/"discrepancies.csv"
    canonical=read_csv(cp); discrepancies=read_csv(dp)
    cby={r.get("canonical_game_id",""):r for r in canonical}

    print("College Basketball History — Kentucky known reconciliation")
    print(f"Repository: {repo}")
    print(f"Mode:       {'APPLY' if args.apply else 'DRY RUN'}")
    print()

    resolved=[]
    for spec in RESOLUTIONS:
        c=cby.get(spec["game_id"])
        if c is None:
            print(f"FAIL: missing canonical game {spec['game_id']}")
            return 1
        for key,field in [("season","season_label"),("date","game_date"),("team_a","team_a_key"),("team_b","team_b_key")]:
            if c.get(field,"")!=spec[key]:
                print(f"FAIL: {spec['game_id']} identity check failed: {field}={c.get(field,'')!r}, expected {spec[key]!r}")
                return 1
        current=canonical_field_value(c,spec["field"])
        if current not in {spec["old_canonical"],spec["new_canonical"]}:
            print(f"FAIL: {spec['game_id']} unexpected canonical {spec['field']}: {current!r}")
            return 1

        matches=[d for d in discrepancies if d.get("canonical_game_id","")==spec["game_id"] and d.get("field_name","")==spec["field"] and d.get("source_a_program_key","")=="kentucky" and d.get("source_a_value","")==spec["source_value"]]
        if len(matches)!=1:
            print(f"FAIL: expected exactly one Kentucky discrepancy for {spec['game_id']} {spec['field']}; found {len(matches)}")
            return 1
        d=matches[0]
        print(f"- {spec['game_id']} | {spec['date']} | {spec['field']}: {current} -> {spec['new_canonical']} | {d.get('status','')} -> RESOLVED")
        set_canonical_field(c,spec["field"],spec["new_canonical"])
        d["canonical_value"]=spec["new_canonical"]
        d["status"]="RESOLVED"
        d["resolution_basis"]=spec["basis"]
        d["notes"]="Source assertion preserved; canonical resolution recorded after Kentucky cross-source QA."
        resolved.append(d)

    print()
    if not args.apply:
        print("DRY RUN COMPLETE: no files changed.")
        return 0

    write_csv(cp,canonical,CANONICAL_FIELDS)
    write_csv(dp,discrepancies,DISCREPANCY_FIELDS)
    validator=repo/"tools"/"validate_data.py"
    if validator.exists():
        r=subprocess.run([sys.executable,str(validator),str(repo)])
        if r.returncode:
            print("FAIL: resolutions written, but validator failed.")
            return r.returncode
    print()
    print(f"PASS: resolved {len(resolved)} known Kentucky cross-source discrepancies.")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
