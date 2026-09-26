#!/usr/bin/env python3
"""Deterministic Stage 3A-0 readiness, census/partition, and target-only canonical join."""
from __future__ import annotations
import argparse,csv,hashlib,json,subprocess
from collections import Counter
from pathlib import Path

REGULAR={"REGULAR_SEASON","REGULAR","RS"}
POST={"POSTSEASON","NCAA","NIT","CONFERENCE_TOURNAMENT","OTHER_POSTSEASON","CBI","CIT","CROWN"}
HOME={"HOME","TEAM_HOME","TARGET_HOME"}; AWAY={"AWAY","OPPONENT_HOME","OPP_HOME","ROAD"}; NEUTRAL={"NEUTRAL","N"}
def rows(p):
    with open(p,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def pick(r,*ns):
    for n in ns:
        v=r.get(n)
        if v is not None and str(v).strip():return str(v).strip()
    return ""
def rid(r):return pick(r,"research_game_id","source_game_id","game_id","id")
def game_class(v):
    x=(v or "").strip().upper()
    if x in REGULAR:return "REGULAR_SEASON"
    if x in POST:return "POSTSEASON"
    return "UNCLASSIFIED"
def site_class(v):
    x=(v or "").strip().upper()
    if x in HOME:return "HOME"
    if x in AWAY:return "OPPONENT_HOME"
    if x in NEUTRAL:return "NEUTRAL"
    return "UNKNOWN"
def sha256(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git_sha():
    try:return subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    except Exception:return None
def dump(out,name,obj):
    p=out/name;p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8");return p
def readiness(ledger):
    ids=[rid(r) for r in ledger]; c=Counter(x for x in ids if x)
    defects={
      "missing_stable_row_id":[i+1 for i,x in enumerate(ids) if not x],
      "duplicate_row_ids":sorted(k for k,v in c.items() if v>1),
      "missing_game_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if not pick(r,"game_type","season_type","competition_type")],
      "unrecognized_game_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if pick(r,"game_type","season_type","competition_type") and game_class(pick(r,"game_type","season_type","competition_type"))=="UNCLASSIFIED"],
      "missing_site_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if not pick(r,"site_type","site","han","home_away_neutral")],
      "unrecognized_site_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if pick(r,"site_type","site","han","home_away_neutral") and site_class(pick(r,"site_type","site","han","home_away_neutral"))=="UNKNOWN"],
      "missing_opponent_key":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if not pick(r,"opponent_key","opponent_program_key")],
    }
    blocking={k:v for k,v in defects.items() if v}
    return {"ready":not blocking,"blocking_defects":blocking,"date_blank_count":sum(not bool(pick(r,"game_date","date")) for r in ledger)}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("school_key");ap.add_argument("ledger",type=Path)
    ap.add_argument("--canonical",type=Path,default=Path("data/canonical/games.csv"));ap.add_argument("--output-dir",type=Path)
    ap.add_argument("--main-sha");a=ap.parse_args();out=a.output_dir or Path(".research")/a.school_key/"stage3a0";out.mkdir(parents=True,exist_ok=True)
    ledger=rows(a.ledger); pre=readiness(ledger); pinned=a.main_sha or git_sha()
    status={"schema_version":2,"school_key":a.school_key,"status":"INPUT_READY" if pre["ready"] else "STAGE_3A0_INPUT_NOT_READY",
      "input_ledger":str(a.ledger),"input_ledger_sha256":sha256(a.ledger),"protected_main_sha":pinned,"readiness":pre,
      "external_historical_research_used":False}
    if not pre["ready"]:
        status["remediation"]="For a pre-hardening accepted checkpoint only: exit Stage 3A-0, perform one narrow compatibility repair from accepted source/state, validate it with research_stage3a0_migrate.py, then rerun. Do not improvise discovery inside Stage 3A-0."
        dump(out,"stage3a0-status.json",status);print(json.dumps(status,indent=2));return 2
    canonical=rows(a.canonical);idx={}
    for r in canonical:
        aa=pick(r,"team_a_key");bb=pick(r,"team_b_key")
        if a.school_key not in (aa,bb):continue
        opp=bb if aa==a.school_key else aa;idx.setdefault((pick(r,"game_date"),opp),[]).append(r)
    counts=Counter();eras=Counter();matches=[];unmatched=[];contradictions=[]
    for r in ledger:
        gc=game_class(pick(r,"game_type","season_type","competition_type"));sc=site_class(pick(r,"site_type","site","han","home_away_neutral"));counts[gc]+=1
        if gc!="REGULAR_SEASON":continue
        counts["RS_"+sc]+=1
        if sc=="NEUTRAL":
            try:y=int(pick(r,"season_label","season")[:4])
            except Exception:y=None
            eras["MODERN_1996_97_PLUS" if y is not None and y>=1996 else "HISTORICAL_1995_96_OR_EARLIER"]+=1
        date=pick(r,"game_date","date");opp=pick(r,"opponent_key","opponent_program_key");cs=idx.get((date,opp),[]) if date else []
        if len(cs)==1:matches.append({"research_game_id":rid(r),"canonical_game_id":pick(cs[0],"canonical_game_id"),"game_date":date,"opponent_key":opp})
        elif len(cs)>1:contradictions.append({"research_game_id":rid(r),"reason":"MULTIPLE_EXACT_DATE_OPPONENT_MATCHES","game_date":date,"opponent_key":opp,"candidate_ids":[pick(x,"canonical_game_id") for x in cs]})
        else:unmatched.append({"research_game_id":rid(r),"reason":"NO_UNIQUE_EXACT_DATE_OPPONENT_MATCH","game_date":date,"opponent_key":opp})
    summary={**status,"status":"COMPLETE","ledger_rows":len(ledger),"partition":{"regular_season":counts["REGULAR_SEASON"],"postseason":counts["POSTSEASON"],"unclassified":0},
      "regular_season_site_census":{k:counts["RS_"+k] for k in ("HOME","OPPONENT_HOME","NEUTRAL","UNKNOWN")},"neutral_era_census":dict(eras),
      "target_only_join":{"matched":len(matches),"unmatched":len(unmatched),"contradictions":len(contradictions),"unmatched_is_blocking_stage3a0":False,"external_discovery_authorized":False,"handoff_to_later_stage":True},
      "next_bounded_assignment":"Stage 3A-1 — H/A/N completion"}
    arts={"summary":dump(out,"stage3a0-summary.json",summary),"status":dump(out,"stage3a0-status.json",summary),"matches":dump(out,"target-canonical-matches.json",matches),"unmatched":dump(out,"unmatched-local-candidates.json",unmatched),"contradictions":dump(out,"local-contradictions.json",contradictions)}
    dump(out,"manifest.json",{k:{"path":str(p),"sha256":sha256(p)} for k,p in arts.items()});print(json.dumps(summary,indent=2));print("STAGE 3A-0: COMPLETE");return 0
if __name__=="__main__":raise SystemExit(main())
