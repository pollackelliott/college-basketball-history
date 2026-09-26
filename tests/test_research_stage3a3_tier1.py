import csv,json,subprocess,sys
from pathlib import Path
def write(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def ledger():
    return [{"research_game_id":"C-1","season_label":"2024-2025","game_date":"2024-11-20","opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"},
            {"research_game_id":"C-2","season_label":"1990-1991","game_date":"1990-12-20","opponent_key":"duke","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}]
def run(tmp,school_rows):
    l=tmp/"ledger.csv";write(l,ledger())
    for school,rows in school_rows.items():write(tmp/"schools"/school/"source-games.csv",rows)
    can=tmp/"data/canonical/games.csv";write(can,[{"canonical_game_id":"X","game_date":"2000-01-01","team_a_key":"a","team_b_key":"b","venue_name":"","city":"","state":""}])
    out=tmp/"out";p=subprocess.run([sys.executable,"tools/research_stage3a3_tier1.py","clemson",str(l),"--repo-root",str(tmp),"--output-dir",str(out),"--main-sha","PIN"],capture_output=True,text=True)
    return p,json.loads((out/"stage3a3-tier1-status.json").read_text()),out
def test_tier1_reuses_exact_reciprocal_and_stops(tmp_path):
    p,s,out=run(tmp_path,{"virginia":[{"source_game_id":"V-1","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}]})
    assert p.returncode==0 and s["accepted_count"]==1 and s["remaining_modern"]==0 and s["remaining_historical"]==1
    assert s["next_bounded_assignment"]=="Stage 3A-3 — modern recurring event/site families"
def test_tier1_conflict_is_serialized_not_forced(tmp_path):
    rows={"virginia":[{"source_game_id":"V-1","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}],
          "duke":[{"source_game_id":"D-1","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"Arena B","city":"Atlanta","state":"GA"}]}
    p,s,out=run(tmp_path,rows);assert s["accepted_count"]==0 and s["contradiction_count"]==1
def test_tier1_requires_exact_game_key(tmp_path):
    l=tmp_path/"ledger.csv";write(l,[{"research_game_id":"C-1","season_label":"2024-2025","game_date":"","opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}])
    out=tmp_path/"out";p=subprocess.run([sys.executable,"tools/research_stage3a3_tier1.py","clemson",str(l),"--repo-root",str(tmp_path),"--output-dir",str(out),"--main-sha","PIN"],capture_output=True,text=True)
    s=json.loads((out/"stage3a3-tier1-status.json").read_text());assert p.returncode==2 and s["status"]=="STAGE_3A3_TIER1_INPUT_NOT_READY"
