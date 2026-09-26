#!/usr/bin/env python3
"""Stage 3A-3 Tier 1: deterministic accepted exact-game/project-evidence reuse.

No network access, document reading, event research, or historical adjudication.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,subprocess
from collections import Counter
from pathlib import Path

def read(p):
    with p.open(newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def pick(r,*ns):
    for n in ns:
        v=r.get(n)
        if v is not None and str(v).strip():return str(v).strip()
    return ""
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def head():
    return subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
def rid(r):return pick(r,"research_game_id","source_game_id","game_id","id")
def is_regular(r):return pick(r,"game_type","curated_game_type","season_type","competition_type").upper() in {"REGULAR_SEASON","REGULAR","RS"}
def is_neutral(r):return pick(r,"site_type","curated_site_type","site","han","home_away_neutral").upper() in {"NEUTRAL","N"}
def opp(r):return pick(r,"opponent_key","opponent_program_key","normalized_opponent_key")
def venue(r):return pick(r,"curated_venue_name","venue_name","venue")
def city(r):return pick(r,"city","venue_city")
def state(r):return pick(r,"state","venue_state")
def season_year(r):
    try:return int(pick(r,"season_label","season")[:4])
    except:return None
def exact_key(r,school=None):
    d=pick(r,"game_date","date");o=opp(r)
    if school and not o:
        a=pick(r,"team_a_key");b=pick(r,"team_b_key")
        if school in (a,b):o=b if a==school else a
    return (d,o) if d and o else None
def evidence_rows(root,school):
    out=[]
    can=root/"data/canonical/games.csv"
    if can.exists():
        for r in read(can):
            a=pick(r,"team_a_key");b=pick(r,"team_b_key")
            if school in (a,b):
                x=dict(r);x["_evidence_source"]="canonical";x["_evidence_path"]=str(can);x["_opponent_key"]=b if a==school else a;out.append(x)
    for p in sorted((root/"schools").glob("*/source-games.csv")):
        if p.parent.name==school:continue
        for r in read(p):
            if pick(r,"normalized_opponent_key")==school:
                x=dict(r);x["_evidence_source"]="published_reciprocal";x["_evidence_path"]=str(p);x["_opponent_key"]=pick(r,"source_program_key");out.append(x)
    return out
def main():
    ap=argparse.ArgumentParser();ap.add_argument("school_key");ap.add_argument("ledger",type=Path);ap.add_argument("--repo-root",type=Path,default=Path("."));ap.add_argument("--output-dir",type=Path);ap.add_argument("--main-sha")
    a=ap.parse_args();root=a.repo_root.resolve();out=a.output_dir or Path(".research")/a.school_key/"stage3a3-tier1";out.mkdir(parents=True,exist_ok=True);pinned=a.main_sha or head()
    ledger=read(a.ledger);neutral=[r for r in ledger if is_regular(r) and is_neutral(r)]
    defects=[];ids=[rid(r) for r in neutral];dups=[k for k,v in Counter(ids).items() if k and v>1]
    if dups:defects.append({"reason":"DUPLICATE_RESEARCH_IDS","ids":dups})
    missing=[rid(r) or f"ROW-{i+1}" for i,r in enumerate(neutral) if not rid(r) or not exact_key(r)]
    if missing:defects.append({"reason":"MISSING_EXACT_GAME_KEY","ids":missing})
    status={"schema_version":1,"school_key":a.school_key,"protected_main_sha":pinned,"input_ledger_sha256":sha(a.ledger),"neutral_rows":len(neutral),"status":"INPUT_READY" if not defects else "STAGE_3A3_TIER1_INPUT_NOT_READY","defects":defects,"external_research_used":False}
    def dump(n,o):
        p=out/n;p.write_text(json.dumps(o,indent=2,sort_keys=True)+"\n",encoding="utf-8");return p
    if defects:dump("stage3a3-tier1-status.json",status);print(json.dumps(status,indent=2));return 2
    ev=evidence_rows(root,a.school_key);idx={}
    for r in ev:
        k=(pick(r,"game_date","date"),pick(r,"_opponent_key"))
        if all(k):idx.setdefault(k,[]).append(r)
    accepted=[];contr=[];unresolved=[];remaining=[];modern=historical=0
    for r in neutral:
        k=exact_key(r);cands=idx.get(k,[]);facts={}
        for e in cands:
            f=(venue(e),city(e),state(e))
            if any(f):facts.setdefault(f,[]).append(e)
        if len(facts)==1:
            f,srcs=next(iter(facts.items()));accepted.append({"research_game_id":rid(r),"game_date":k[0],"opponent_key":k[1],"venue_name":f[0],"city":f[1],"state":f[2],"provenance":[{"kind":x["_evidence_source"],"path":x["_evidence_path"],"evidence_game_id":pick(x,"canonical_game_id","source_game_id")} for x in srcs]})
        elif len(facts)>1:
            contr.append({"research_game_id":rid(r),"game_date":k[0],"opponent_key":k[1],"reason":"CONFLICTING_ACCEPTED_PROJECT_SITE_EVIDENCE","candidate_facts":[{"venue_name":f[0],"city":f[1],"state":f[2],"count":len(xs)} for f,xs in facts.items()]});remaining.append(r)
        else:
            unresolved.append({"research_game_id":rid(r),"game_date":k[0],"opponent_key":k[1],"reason":"NO_ACCEPTED_EXACT_GAME_SITE_EVIDENCE"});remaining.append(r)
    for r in remaining:
        y=season_year(r)
        if y is not None and y>=1996:modern+=1
        else:historical+=1
    status.update({"status":"COMPLETE","accepted_count":len(accepted),"contradiction_count":len(contr),"unresolved_count":len(unresolved),"remaining_modern":modern,"remaining_historical":historical,"next_bounded_assignment":"Stage 3A-3 — modern recurring event/site families"})
    arts={"status":dump("stage3a3-tier1-status.json",status),"accepted":dump("accepted-project-evidence.json",accepted),"contradictions":dump("tier1-contradictions.json",contr),"unresolved":dump("tier1-unresolved.json",unresolved),"remaining":dump("remaining-neutral-queue.json",remaining)}
    dump("manifest.json",{k:{"path":str(p),"sha256":sha(p)} for k,p in arts.items()});print(json.dumps(status,indent=2));print("STAGE 3A-3: IN PROGRESS — TIER 1 COMPLETE");return 0
if __name__=="__main__":raise SystemExit(main())
