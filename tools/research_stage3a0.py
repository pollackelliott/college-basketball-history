#!/usr/bin/env python3
"""Deterministic Stage 3A-0 entry/readiness, census/partition, and target-only canonical join."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,subprocess,zipfile
from collections import Counter
from pathlib import Path

REGULAR={"REGULAR_SEASON","REGULAR","RS"}
POST={"POSTSEASON","NCAA","NIT","CONFERENCE_TOURNAMENT","OTHER_POSTSEASON","CBI","CIT","CROWN"}
HOME={"HOME","TEAM_HOME","TARGET_HOME"}; AWAY={"AWAY","OPPONENT_HOME","OPP_HOME","ROAD"}; NEUTRAL={"NEUTRAL","N"}
LEDGER_BASENAMES=("structured-stage2-ledger.csv","structured-stage2-ledger-with-game-type.csv","stage2-ledger.csv","stage2-working-ledger.csv")
ID_FIELDS=("research_game_id","source_game_id","game_id","id")
OPP_FIELDS=("opponent_key","opponent_program_key")
SITE_FIELDS=("site_type","site","han","home_away_neutral")
SEASON_FIELDS=("season_label","season")

def rows(p):
    with open(p,newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def csv_bytes(data):
    with io.TextIOWrapper(io.BytesIO(data),encoding="utf-8-sig",newline="") as f:return list(csv.DictReader(f))
def csv_header(z,member):
    with z.open(member) as raw,io.TextIOWrapper(raw,encoding="utf-8-sig",newline="") as f:return next(csv.reader(f),[])
def pick(r,*ns):
    for n in ns:
        v=r.get(n)
        if v is not None and str(v).strip():return str(v).strip()
    return ""
def rid(r):return pick(r,*ID_FIELDS)
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
def sha256_bytes(b):return hashlib.sha256(b).hexdigest()
def git_sha():
    try:return subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
    except Exception:return None
def dump(out,name,obj):
    p=out/name;p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8");return p

def ledger_header_score(header,name):
    h=set(header)
    required=(any(x in h for x in ID_FIELDS),any(x in h for x in OPP_FIELDS),any(x in h for x in SITE_FIELDS),any(x in h for x in SEASON_FIELDS))
    if not all(required):return -1
    score=sum(required)
    low=name.lower()
    if "stage2" in low:score+=2
    if "ledger" in low:score+=2
    if any(x in h for x in ("game_type","season_type","competition_type")):score+=1
    return score

def load_input(path,out):
    if path.suffix.lower()!=".zip":
        return rows(path),{"entry_mode":"ledger_csv","input_artifact":str(path),"input_artifact_sha256":sha256(path),"input_ledger":str(path),"input_ledger_sha256":sha256(path)}
    checkpoint_sha=sha256(path)
    try:z=zipfile.ZipFile(path)
    except zipfile.BadZipFile as e:raise ValueError(f"INVALID_CHECKPOINT_ZIP: {e}")
    with z:
        members=[n for n in z.namelist() if not n.endswith("/") and n.lower().endswith(".csv")]
        exact=[]
        for base in LEDGER_BASENAMES:
            hits=[n for n in members if Path(n).name.lower()==base]
            if hits:
                exact=hits;break
        if len(exact)>1:raise ValueError("AMBIGUOUS_STAGE2_LEDGER: "+",".join(sorted(exact)))
        selected=exact[0] if exact else None
        if selected is None:
            scored=[]
            for n in members:
                try:score=ledger_header_score(csv_header(z,n),n)
                except (UnicodeDecodeError,csv.Error):continue
                if score>=0:scored.append((score,n))
            if scored:
                best=max(x[0] for x in scored);best_members=sorted(n for score,n in scored if score==best)
                if len(best_members)==1:selected=best_members[0]
                else:raise ValueError("AMBIGUOUS_STAGE2_LEDGER: "+",".join(best_members))
        if selected is None:raise ValueError("NO_STAGE2_LEDGER_FOUND")
        data=z.read(selected)
    ledger_copy=out/"stage3a0-input-ledger.csv";ledger_copy.write_bytes(data)
    return csv_bytes(data),{"entry_mode":"checkpoint_zip","input_artifact":str(path),"input_artifact_sha256":checkpoint_sha,"input_checkpoint_member":selected,"input_ledger":str(ledger_copy),"input_ledger_sha256":sha256_bytes(data)}

def readiness(ledger):
    ids=[rid(r) for r in ledger]; c=Counter(x for x in ids if x)
    defects={
      "missing_stable_row_id":[i+1 for i,x in enumerate(ids) if not x],
      "duplicate_row_ids":sorted(k for k,v in c.items() if v>1),
      "missing_game_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if not pick(r,"game_type","season_type","competition_type")],
      "unrecognized_game_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if pick(r,"game_type","season_type","competition_type") and game_class(pick(r,"game_type","season_type","competition_type"))=="UNCLASSIFIED"],
      "missing_site_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if not pick(r,*SITE_FIELDS)],
      "unrecognized_site_type":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if pick(r,*SITE_FIELDS) and site_class(pick(r,*SITE_FIELDS))=="UNKNOWN"],
      "missing_opponent_key":[rid(r) or f"ROW-{i+1}" for i,r in enumerate(ledger) if not pick(r,*OPP_FIELDS)],
    }
    blocking={k:v for k,v in defects.items() if v}
    return {"ready":not blocking,"blocking_defects":blocking,"date_blank_count":sum(not bool(pick(r,"game_date","date")) for r in ledger)}

def main():
    ap=argparse.ArgumentParser(description="Command-first Stage 3A-0 gate. INPUT may be the Stage 2 checkpoint ZIP or structured Stage 2 ledger CSV.")
    ap.add_argument("school_key");ap.add_argument("input",type=Path)
    ap.add_argument("--canonical",type=Path,default=Path("data/canonical/games.csv"));ap.add_argument("--output-dir",type=Path)
    ap.add_argument("--main-sha");a=ap.parse_args();out=a.output_dir or Path(".research")/a.school_key/"stage3a0";out.mkdir(parents=True,exist_ok=True)
    pinned=a.main_sha or git_sha()
    try:ledger,input_meta=load_input(a.input,out)
    except (OSError,ValueError) as e:
        status={"schema_version":3,"school_key":a.school_key,"status":"STAGE_3A0_ENTRY_NOT_READY","protected_main_sha":pinned,
          "input_artifact":str(a.input),"entry_error":str(e),"external_historical_research_used":False,
          "next_action":"STOP_AND_FIX_STAGE2_INPUT_ARTIFACT","remediation":"Provide the durable Stage 2 checkpoint ZIP or structured Stage 2 ledger directly to this command. Do not inspect checkpoint members or conduct historical/source discovery inside Stage 3A-0."}
        if a.input.exists():status["input_artifact_sha256"]=sha256(a.input)
        dump(out,"stage3a0-status.json",status);print(json.dumps(status,indent=2));return 2
    pre=readiness(ledger)
    blocking_keys=set(pre["blocking_defects"])
    missing_game_type_only=blocking_keys=={"missing_game_type"}
    status={"schema_version":3,"school_key":a.school_key,"status":"INPUT_READY" if pre["ready"] else "STAGE_3A0_INPUT_NOT_READY",
      **input_meta,"protected_main_sha":pinned,"readiness":pre,"external_historical_research_used":False}
    if not pre["ready"]:
        status["remediation_code"]="MISSING_GAME_TYPE_ONLY" if missing_game_type_only else "STRUCTURED_INPUT_DEFECTS"
        status["next_action"]="STOP_STAGE_3A0_AND_RUN_NARROW_GAME_TYPE_MIGRATION" if missing_game_type_only else "STOP_AND_REPAIR_STRUCTURED_INPUT_AT_PRIOR_STAGE"
        status["remediation"]="For a pre-hardening accepted checkpoint only: exit Stage 3A-0, perform one narrow compatibility repair from accepted source/state, validate it with research_stage3a0_migrate.py, then rerun. Do not improvise discovery inside Stage 3A-0." if missing_game_type_only else "Stop Stage 3A-0. Repair only the serialized structured-input defects at the controlling prior stage/checkpoint; do not research around the readiness gate."
        dump(out,"stage3a0-status.json",status);print(json.dumps(status,indent=2));return 2
    canonical=rows(a.canonical);idx={}
    for r in canonical:
        aa=pick(r,"team_a_key");bb=pick(r,"team_b_key")
        if a.school_key not in (aa,bb):continue
        opp=bb if aa==a.school_key else aa;idx.setdefault((pick(r,"game_date"),opp),[]).append(r)
    counts=Counter();eras=Counter();matches=[];unmatched=[];contradictions=[]
    for r in ledger:
        gc=game_class(pick(r,"game_type","season_type","competition_type"));sc=site_class(pick(r,*SITE_FIELDS));counts[gc]+=1
        if gc!="REGULAR_SEASON":continue
        counts["RS_"+sc]+=1
        if sc=="NEUTRAL":
            try:y=int(pick(r,"season_label","season")[:4])
            except Exception:y=None
            eras["MODERN_1996_97_PLUS" if y is not None and y>=1996 else "HISTORICAL_1995_96_OR_EARLIER"]+=1
        date=pick(r,"game_date","date");opp=pick(r,*OPP_FIELDS);cs=idx.get((date,opp),[]) if date else []
        if len(cs)==1:matches.append({"research_game_id":rid(r),"canonical_game_id":pick(cs[0],"canonical_game_id"),"game_date":date,"opponent_key":opp})
        elif len(cs)>1:contradictions.append({"research_game_id":rid(r),"reason":"MULTIPLE_EXACT_DATE_OPPONENT_MATCHES","game_date":date,"opponent_key":opp,"candidate_ids":[pick(x,"canonical_game_id") for x in cs]})
        else:unmatched.append({"research_game_id":rid(r),"reason":"NO_UNIQUE_EXACT_DATE_OPPONENT_MATCH","game_date":date,"opponent_key":opp})
    summary={**status,"status":"COMPLETE","ledger_rows":len(ledger),"partition":{"regular_season":counts["REGULAR_SEASON"],"postseason":counts["POSTSEASON"],"unclassified":0},
      "regular_season_site_census":{k:counts["RS_"+k] for k in ("HOME","OPPONENT_HOME","NEUTRAL","UNKNOWN")},"neutral_era_census":dict(eras),
      "target_only_join":{"matched":len(matches),"unmatched":len(unmatched),"contradictions":len(contradictions),"unmatched_is_blocking_stage3a0":False,"external_discovery_authorized":False,"handoff_to_later_stage":True},
      "next_action":"STOP_AT_STAGE_3A0_BOUNDARY","next_bounded_assignment":"Stage 3A-1 — H/A/N completion"}
    arts={"summary":dump(out,"stage3a0-summary.json",summary),"status":dump(out,"stage3a0-status.json",summary),"matches":dump(out,"target-canonical-matches.json",matches),"unmatched":dump(out,"unmatched-local-candidates.json",unmatched),"contradictions":dump(out,"local-contradictions.json",contradictions)}
    dump(out,"manifest.json",{k:{"path":str(p),"sha256":sha256(p)} for k,p in arts.items()});print(json.dumps(summary,indent=2));print("STAGE 3A-0: COMPLETE");return 0
if __name__=="__main__":raise SystemExit(main())
