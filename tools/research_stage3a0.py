#!/usr/bin/env python3
"""Deterministic Stage 3A-0 census/partition and target-only local join.

This command intentionally performs no network access, document reading, opponent-package
enumeration, or historical adjudication. Missing structured fields are serialized as
residuals instead of triggering discovery.
"""
from __future__ import annotations
import argparse, csv, hashlib, json
from collections import Counter
from pathlib import Path

REGULAR={"REGULAR_SEASON","REGULAR","RS"}
POST={"POSTSEASON","NCAA","NIT","CONFERENCE_TOURNAMENT","OTHER_POSTSEASON","CBI","CIT","CROWN"}
HOME={"HOME","TEAM_HOME","TARGET_HOME"}
AWAY={"AWAY","OPPONENT_HOME","OPP_HOME","ROAD"}
NEUTRAL={"NEUTRAL","N"}
UNKNOWN={"","UNKNOWN","UNK"}

def rows(path):
    with open(path,newline="",encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def pick(r,*names):
    for n in names:
        v=r.get(n)
        if v is not None and str(v).strip()!="": return str(v).strip()
    return ""
def season_start(label):
    try: return int(label[:4])
    except Exception: return None
def site_class(v):
    x=(v or "").strip().upper()
    if x in HOME:return "HOME"
    if x in AWAY:return "OPPONENT_HOME"
    if x in NEUTRAL:return "NEUTRAL"
    return "UNKNOWN"
def game_class(v):
    x=(v or "").strip().upper()
    if x in REGULAR:return "REGULAR_SEASON"
    if x in POST:return "POSTSEASON"
    return "UNCLASSIFIED"
def rid(r,i): return pick(r,"research_game_id","source_game_id","game_id","id") or f"ROW-{i:06d}"
def canon_index(canonical,school):
    out={}
    for r in canonical:
        a=pick(r,"team_a_key"); b=pick(r,"team_b_key")
        if school not in (a,b): continue
        opp=b if a==school else a
        key=(pick(r,"game_date"),opp)
        out.setdefault(key,[]).append(r)
    return out
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("school_key")
    ap.add_argument("ledger",type=Path)
    ap.add_argument("--canonical",type=Path,default=Path("data/canonical/games.csv"))
    ap.add_argument("--assertions",type=Path,default=Path("data/evidence/game-assertions.csv"))
    ap.add_argument("--output-dir",type=Path)
    a=ap.parse_args()
    out=a.output_dir or Path(".research")/a.school_key/"stage3a0"
    out.mkdir(parents=True,exist_ok=True)
    ledger=rows(a.ledger)
    canonical=rows(a.canonical) if a.canonical.exists() else []
    idx=canon_index(canonical,a.school_key)
    enriched=[]; unclassified=[]; contradictions=[]; unmatched=[]; matches=[]
    counts=Counter(); neutral_era=Counter()
    for i,r0 in enumerate(ledger,1):
        r=dict(r0); r["_research_row_id"]=rid(r,i)
        gc=game_class(pick(r,"game_type","season_type","competition_type"))
        sc=site_class(pick(r,"site_type","site","han","home_away_neutral"))
        r["_stage3a0_game_class"]=gc; r["_stage3a0_site_class"]=sc
        counts[gc]+=1
        if gc=="UNCLASSIFIED": unclassified.append(r)
        if gc=="REGULAR_SEASON":
            counts["RS_"+sc]+=1
            if sc=="NEUTRAL":
                y=season_start(pick(r,"season_label","season"))
                era="MODERN_1996_97_PLUS" if y is not None and y>=1996 else "HISTORICAL_1995_96_OR_EARLIER"
                neutral_era[era]+=1; r["_stage3a0_neutral_era"]=era
            date=pick(r,"game_date","date"); opp=pick(r,"opponent_key","opponent_program_key","opponent")
            cands=idx.get((date,opp),[]) if date and opp else []
            if len(cands)==1:
                c=cands[0]; matches.append({"research_row_id":r["_research_row_id"],"canonical_game_id":pick(c,"canonical_game_id"),"game_date":date,"opponent_key":opp})
            elif len(cands)>1:
                contradictions.append({"research_row_id":r["_research_row_id"],"reason":"MULTIPLE_TARGET_CANONICAL_MATCHES","game_date":date,"opponent_key":opp,"candidate_ids":[pick(x,"canonical_game_id") for x in cands]})
            else:
                unmatched.append({"research_row_id":r["_research_row_id"],"game_date":date,"opponent_key":opp,"reason":"NO_UNIQUE_TARGET_CANONICAL_MATCH"})
        enriched.append(r)
    def dump(name,obj):
        p=out/name; p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8"); return p
    status="COMPLETE" if not unclassified else "INCOMPLETE_STRUCTURED_PARTITION"
    summary={"schema_version":1,"school_key":a.school_key,"status":status,"external_historical_research_used":False,
      "ledger_rows":len(ledger),"partition":{"regular_season":counts["REGULAR_SEASON"],"postseason":counts["POSTSEASON"],"unclassified":counts["UNCLASSIFIED"]},
      "regular_season_site_census":{k:counts["RS_"+k] for k in ("HOME","OPPONENT_HOME","NEUTRAL","UNKNOWN")},
      "neutral_era_census":dict(neutral_era),"target_only_join":{"matched":len(matches),"unmatched":len(unmatched),"contradictions":len(contradictions)},
      "next_action":"serialize residuals and stop; do not discover sources" if status!="COMPLETE" else "STAGE 3A-0 complete; stop before Stage 3A-1"}
    artifacts={"summary":dump("stage3a0-summary.json",summary),"matches":dump("target-canonical-matches.json",matches),
      "unmatched":dump("unmatched-local-candidates.json",unmatched),"contradictions":dump("local-contradictions.json",contradictions),
      "unclassified":dump("unclassified-partition-rows.json",unclassified)}
    manifest={k:{"path":str(p),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()} for k,p in artifacts.items()}
    dump("manifest.json",manifest)
    print(json.dumps(summary,indent=2,sort_keys=True))
    print("STAGE 3A-0: COMPLETE" if status=="COMPLETE" else "STAGE 3A-0: INCOMPLETE — STRUCTURED RESIDUAL PRESERVED")
    return 0
if __name__=="__main__": raise SystemExit(main())
