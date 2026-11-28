#!/usr/bin/env python3
"""Bounded New Mexico 2012–2017 neutral modern-event venue research write-through."""
import csv, hashlib, json, pathlib, shutil
from collections import Counter
R=pathlib.Path("research/new-mexico/checkpoints")
P=R/"0013-stage3a3-tier1-accepted-evidence"
O=R/"0014-stage3a3-tier2-modern-events-tranche1"
BASE="242370fc551fd749c157c74d92917ddfafbe40e0"
PARENT="9a1930309b5f01f10ab4f1eec469ad7d377546d3"
families={
"P":("2012 Paradise Jam","https://uconnhuskies.com/news/2012/5/26/uconn_to_open_2012_paradise_jam_vs_wake_forest","https://gomason.com/news/2012/11/17/205748571.aspx"),
"C":("2013 Charleston Classic","https://umassathletics.com/news/2013/7/17/2013_charleston_classic_bracket_announced","https://uabsports.com/news/2013/4/10/eight_team_field_completed_for_charleston_classic"),
"R":("2014 Puerto Rico Tip-Off","https://12thman.com/news/2014/08/05/puerto-rico-tip-off-brackets-announced","https://gomason.com/news/2014/8/5/209604872.aspx"),
"D":("2015 Diamond Head Classic","https://golobos.com/news/2014/12/21/209819017","https://wsucougars.com/diamond-head-classic-washington-state-vs-new-mexico-stats"),
"W":("2016 Wooden Legacy","https://espnpressroom.com/press-release/matchups-2016-espn-events-early-season-basketball-tournaments-revealed/","https://uclabruins.com/news/2016/05/31/ucla-announces-non-conference-schedule-2"),
"E":("2017 Emerald Coast Classic","https://gofrogs.com/news/2017/11/22/preview_new_mexico","https://gobonnies.com/news/2017/11/23/11_23_2017_2496")
}
venues={
"sports-and-fitness-center":("VEN-000191","Sports and Fitness Center","St. Thomas","VI","USA","arena"),
"td-arena":("VEN-000280","TD Arena","Charleston","SC","USA","arena"),
"coliseo-roberto-clemente":("VEN-000467","Coliseo Roberto Clemente","San Juan","PR","USA","arena"),
"stan-sheriff-center":("VEN-000194","Stan Sheriff Center","Honolulu","HI","USA","arena"),
"titan-gym":("VEN-000212","Titan Gym","Fullerton","CA","USA","gymnasium"),
"honda-center":("VEN-000082","Honda Center","Anaheim","CA","USA","arena"),
"raider-arena":("VEN-000271","Raider Arena","Niceville","FL","USA","arena")
}
decisions={
"NM-2012-13-0002":("2012-11-16","UIC","P","sports-and-fitness-center"),
"NM-2012-13-0003":("2012-11-18","George Mason","P","sports-and-fitness-center"),
"NM-2012-13-0004":("2012-11-19","Connecticut","P","sports-and-fitness-center"),
"NM-2013-14-0003":("2013-11-21","UAB","C","td-arena"),
"NM-2013-14-0004":("2013-11-22","Massachusetts","C","td-arena"),
"NM-2013-14-0005":("2013-11-24","Davidson","C","td-arena"),
"NM-2014-15-0003":("2014-11-20","Boston College","R","coliseo-roberto-clemente"),
"NM-2014-15-0004":("2014-11-21","George Mason","R","coliseo-roberto-clemente"),
"NM-2014-15-0005":("2014-11-23","Texas A&M","R","coliseo-roberto-clemente"),
"NM-2015-16-0011":("2015-12-22","Auburn","D","stan-sheriff-center"),
"NM-2015-16-0012":("2015-12-23","BYU","D","stan-sheriff-center"),
"NM-2015-16-0013":("2015-12-25","Washington State","D","stan-sheriff-center"),
"NM-2016-17-0004":("2016-11-24","Virginia Tech","W","titan-gym"),
"NM-2016-17-0005":("2016-11-25","CSUN","W","titan-gym"),
"NM-2016-17-0006":("2016-11-27","Dayton","W","honda-center"),
"NM-2017-18-0005":("2017-11-24","TCU","E","raider-arena"),
"NM-2017-18-0006":("2017-11-25","Maryland","E","raider-arena")
}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):
 with p.open(newline="",encoding="utf-8") as f:
  x=csv.DictReader(f)
  return x.fieldnames,list(x)
def write(p,fields,rows):
 with p.open("w",newline="",encoding="utf-8") as f:
  w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
  w.writeheader()
  w.writerows(rows)
def jd(p,obj): p.write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
ps=json.loads((P/"stage3a3-tier1-status.json").read_text())
assert ps["status"]=="COMPLETE" and ps["neutral_rows"]==99 and ps["remaining_modern"]==57 and ps["remaining_historical"]==42
assert ps["protected_main_sha"]==BASE
pm=json.loads((P/"checkpoint-content-hashes.json").read_text())
assert pm["kind"]=="NEW_MEXICO_STAGE3A3_TIER1_CHECKPOINT_V1"
assert pm["research_base_sha"]==BASE and pm["parent_research_commit_sha"]=="3339b0848e6ab6ae2e92d18db69b7d4ab602f55f"
for f in pm["files"]:
 p=P/f["path"]
 assert len(p.read_bytes())==f["bytes"] and sha(p)==f["sha256"],f["path"]
source=P/"parent-stage3a2-working-ledger.csv"
assert sha(source)==ps["input_ledger_sha256"]
headers,rows=load(source)
assert len(rows)==2891 and len(decisions)==17 and len(families)==6 and len(venues)==7
original={x["research_game_id"]:dict(x) for x in rows}
assert len(original)==2891
queue=json.loads((P/"remaining-neutral-queue.json").read_text())
assert len(queue)==99 and len({x["research_game_id"] for x in queue})==99
assert set(decisions)<={x["research_game_id"] for x in queue}
assert sum(x["site_type"]=="UNKNOWN" and x["game_type"]=="REGULAR_SEASON" for x in rows)==2
assert sum(x["site_type"]=="HOME" and x["game_type"]=="REGULAR_SEASON" for x in rows)==1564
basefile=pathlib.Path(".exact-main/data/reference/venues.csv")
_,refrows=load(basefile)
ref={x["venue_key"]:x for x in refrows}
for key,(vid,name,city,state,country,kind) in venues.items():
 assert ref[key]["venue_id"]==vid and ref[key]["display_name"]==name
 assert ref[key]["city"]==city and ref[key]["state"]==state
assert not O.exists()
O.mkdir(parents=True)
output_fields=headers+["stage3a3_resolution_note"]
for row in rows:row["stage3a3_resolution_note"]=""
audit=[]
for gid,(date,opp,fam,key) in decisions.items():
 row=next(x for x in rows if x["research_game_id"]==gid)
 event,sourceurl,backup=families[fam]
 vid,name,city,state,country,kind=venues[key]
 assert row["source_game_date"]==date and row["canonical_opponent_name"]==opp
 assert row["site_type"]=="NEUTRAL" and row["game_type"]=="REGULAR_SEASON"
 assert row["source_site_token"].strip().lower()=="vs"
 for k in ("curated_venue_name","curated_venue_city","curated_venue_state","curated_venue_country","accepted_venue_key","curation_provenance","site_research_status","site_research_basis"):
  assert not row[k],(gid,k)
 row.update(curated_venue_name=name,curated_venue_city=city,curated_venue_state=state,
    curated_venue_country=country,accepted_venue_key=key,
    curation_provenance=sourceurl+" | "+backup,
    stage3a3_resolution_note="Exact edition and game-date event/venue proof: "+event+"; "+sourceurl)
 audit.append(dict(research_game_id=gid,game_date=date,opponent=opp,event=event,venue_name=name,venue_key=key,venue_id=vid,city=city,state=state,country=country,source=sourceurl,corroboration=backup))
write(O/"stage3a3-tier2-working-ledger.csv",output_fields,rows)
f2,check=load(O/"stage3a3-tier2-working-ledger.csv")
assert f2==output_fields and len(check)==2891
allowed={"curated_venue_name","curated_venue_city","curated_venue_state","curated_venue_country","accepted_venue_key","curation_provenance"}
for row in check:
 gid=row["research_game_id"]
 changes={k for k in headers if row[k]!=original[gid][k]}
 assert changes==(allowed if gid in decisions else set()),(gid,changes)
 if gid not in decisions: assert not row["stage3a3_resolution_note"]
assert len(audit)==17
vh,vr=load(P/"stage4-authoring/venues.csv")
assert len(vr)==3 and not (set(venues)&{x["venue_key"] for x in vr})
cap=O/"stage4-authoring"
cap.mkdir()
for n in ("opponents.csv","institutional-scope.json"):shutil.copyfile(P/"stage4-authoring"/n,cap/n)
for key,(vid,name,city,state,country,kind) in venues.items():
 matched=[x for x in audit if x["venue_key"]==key]
 fkey=next(f for (_,_,f,k) in decisions.values() if k==key)
 row=dict.fromkeys(vh,"")
 row.update(source_program_key="new-mexico",venue_key=key,venue_id=vid,
 canonical_name=name,aliases="UVI Sports and Fitness Center" if key=="sports-and-fitness-center" else ("The Arena at Northwest Florida State College" if key=="raider-arena" else ""),
 city=city,state=state,venue_type=kind,
 games_currently_assigned=str(len(matched)),first_assigned_game=min(x["game_date"] for x in matched),
 last_assigned_game=max(x["game_date"] for x in matched),
 site_rule="Only exact supported event edition and game dates; no chronology inference",
 source_basis=families[fkey][1]+" | "+families[fkey][2],
 notes="Reused existing protected research-base physical venue identity; exact regular-season neutral sites")
 vr.append(row)
write(cap/"venues.csv",vh,vr)
newvh,newvr=load(cap/"venues.csv")
assert newvh==vh and newvr[:3]==load(P/"stage4-authoring/venues.csv")[1]
assert len(newvr)==10 and sum(int(x["games_currently_assigned"]) for x in newvr[3:])==17
remaining=[x for x in queue if x["research_game_id"] not in decisions]
assert len(remaining)==82
modern=sum(int(x["season"][:4])>=1996 for x in remaining)
historical=82-modern
assert (modern,historical)==(40,42)
jd(O/"stage3a3-tier2-evidence.json",audit)
jd(O/"source-family-audit.json",[{ "family":k,"name":v[0],"primary_url":v[1],"corroboration_url":v[2]} for k,v in families.items()])
jd(O/"remaining-neutral-queue.json",remaining)
status=dict(schema_version=1,kind="NEW_MEXICO_STAGE3A3_TIER2_TRANCHE1_V1",state="TRANCHE1_COMPLETE_TIER2_IN_PROGRESS",
 school_key="new-mexico",research_base_sha=BASE,parent_research_commit_sha=PARENT,
 parent_checkpoint="0013-stage3a3-tier1-accepted-evidence",parent_ledger_sha256=sha(source),
 total_competitive_games=2891,total_regular_season_neutral=99,accepted_exact_venue_rows=17,
 verified_venue_identity_count=7,source_event_families=6,
 remaining_neutral=82,remaining_modern=modern,remaining_historical=historical,
 unchanged_regular_season_unknown_han=2,unchanged_home_rows=1564,
 no_historical_fact_changes=True,external_research_used=True,
 source_mode="official tournament/event/participating institutional editions",
 next_bounded_assignment="STAGE_3A3_TIER2_MODERN_RECURRING_REMAINING")
jd(O/"stage3a3-tier2-status.json",status)
(O/"README.md").write_text(
 "# New Mexico — Stage 3A-3 Tier 2 checkpoint 0014\n\n"
 "Exact Research parent: "+PARENT+"\nResearch base: "+BASE+"\n\n"
 "Six official-event 2012–2017 editions: 17 fully researched venue rows; seven existing physical venue keys.\n"
 "Wooden Legacy Nov 24/25 Titan Gym and Nov 27 Honda Center separated by exact edition evidence.\n"
 "Full 2,891-row ledger preserved; changed fields isolated to 17 supported site/provenance cells.\n"
 "Two accepted Arizona UNKNOWN H/A/N unchanged, all HOME dispositions unchanged.\n"
 "Residual queue: 40 modern + 42 historical regular-season neutral games.\n"
 "Stage 3A-3 Tier 2 remains open. Stage 3A-4 and Stage 3B not started.\n",
 encoding="utf-8")
files=[]
for p in sorted(O.rglob("*")):
 if p.is_file() and p.name!="checkpoint-content-hashes.json":
  b=p.read_bytes()
  files.append(dict(path=p.relative_to(O).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest()))
jd(O/"checkpoint-content-hashes.json",dict(schema_version=1,kind="NEW_MEXICO_STAGE3A3_TIER2_TRANCHE1_CHECKPOINT_V1",
 research_base_sha=BASE,parent_research_commit_sha=PARENT,
 parent_ledger_sha256=sha(source),status=status["state"],files=files))
print(json.dumps(status,indent=2))
