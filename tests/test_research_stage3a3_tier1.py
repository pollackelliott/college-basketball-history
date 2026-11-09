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
def test_tier1_date_unknown_stays_in_residual(tmp_path):
    l=tmp_path/"ledger.csv";write(l,[{"research_game_id":"C-1","season_label":"1990-1991","game_date":"","opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}])
    out=tmp_path/"out";p=subprocess.run([sys.executable,"tools/research_stage3a3_tier1.py","clemson",str(l),"--repo-root",str(tmp_path),"--output-dir",str(out),"--main-sha","PIN"],capture_output=True,text=True)
    s=json.loads((out/"stage3a3-tier1-status.json").read_text())
    assert p.returncode==0 and s["status"]=="COMPLETE"
    assert s["unresolved_count"]==1 and s["remaining_historical"]==1
    unresolved=json.loads((out/"tier1-unresolved.json").read_text())
    assert unresolved==[{"research_game_id":"C-1","game_date":"","opponent_key":"virginia","reason":"NO_EXACT_DATE_FOR_TIER1_MATCH"}]

def test_tier1_still_requires_row_identity(tmp_path):
    l=tmp_path/"ledger.csv";write(l,[{"research_game_id":"C-1","season_label":"1990-1991","game_date":"1990-12-20","opponent_key":"","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}])
    out=tmp_path/"out";p=subprocess.run([sys.executable,"tools/research_stage3a3_tier1.py","clemson",str(l),"--repo-root",str(tmp_path),"--output-dir",str(out),"--main-sha","PIN"],capture_output=True,text=True)
    s=json.loads((out/"stage3a3-tier1-status.json").read_text())
    assert p.returncode==2 and s["status"]=="STAGE_3A3_TIER1_INPUT_NOT_READY"
    assert s["defects"]==[{"reason":"MISSING_EXACT_GAME_KEY","ids":["C-1"]}]

def test_tier1_modern_partial_site_evidence_stays_in_residual(tmp_path):
    p,s,out=run(tmp_path,{"virginia":[{"source_game_id":"V-PART","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"","city":"Atlanta","state":"GA"}]})
    assert p.returncode==0
    assert s["accepted_count"]==1
    assert s["accepted_complete_count"]==0
    assert s["accepted_partial_count"]==1
    assert s["remaining_modern"]==1
    accepted=json.loads((out/"accepted-project-evidence.json").read_text())
    assert accepted[0]["downstream_complete"] is False
    assert accepted[0]["missing_required_fields"]==["venue_name"]
    remaining=json.loads((out/"remaining-neutral-queue.json").read_text())
    assert any(row["research_game_id"]=="C-1" for row in remaining)

def test_tier1_historical_locality_without_building_is_complete(tmp_path):
    p,s,out=run(tmp_path,{"duke":[{"source_game_id":"D-HIST","source_program_key":"duke","game_date":"1990-12-20","normalized_opponent_key":"clemson","curated_venue_name":"","city":"Orlando","state":"FL"}]})
    assert p.returncode==0
    assert s["accepted_count"]==1
    assert s["accepted_complete_count"]==1
    assert s["accepted_partial_count"]==0
    assert s["remaining_historical"]==0
    accepted=json.loads((out/"accepted-project-evidence.json").read_text())
    assert accepted[0]["downstream_complete"] is True
    assert accepted[0]["missing_required_fields"]==[]

def test_tier1_historical_partial_locality_stays_in_residual(tmp_path):
    p,s,out=run(tmp_path,{"duke":[{"source_game_id":"D-HIST-PART","source_program_key":"duke","game_date":"1990-12-20","normalized_opponent_key":"clemson","curated_venue_name":"","city":"Orlando","state":""}]})
    assert p.returncode==0
    assert s["accepted_count"]==1
    assert s["accepted_complete_count"]==0
    assert s["accepted_partial_count"]==1
    assert s["remaining_historical"]==1
    accepted=json.loads((out/"accepted-project-evidence.json").read_text())
    assert accepted[0]["missing_required_fields"]==["state"]


def run_durable_schema_case(tmp, ledger_row, evidence_rows):
    ledger_path=tmp/"ledger.csv";write(ledger_path,[ledger_row])
    write(tmp/"schools"/"virginia"/"source-games.csv",evidence_rows)
    can=tmp/"data/canonical/games.csv";write(can,[{"canonical_game_id":"OTHER","game_date":"2000-01-01","team_a_key":"a","team_b_key":"b","venue_name":"","city":"","state":""}])
    out=tmp/"out";p=subprocess.run([sys.executable,"tools/research_stage3a3_tier1.py","clemson",str(ledger_path),"--repo-root",str(tmp),"--output-dir",str(out),"--main-sha","PIN"],capture_output=True,text=True)
    return p,json.loads((out/"stage3a3-tier1-status.json").read_text()),out

def test_tier1_accepts_stage2_opponent_key_and_projects_fall_source_date(tmp_path):
    ledger_row={"research_game_id":"C-DURABLE-FALL","season_label":"2024-25","source_date_literal":"11/20","stage2_opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}
    evidence=[{"source_game_id":"V-FALL","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}]
    p,s,out=run_durable_schema_case(tmp_path,ledger_row,evidence)
    assert p.returncode==0 and s["status"]=="COMPLETE" and s["accepted_count"]==1
    accepted=json.loads((out/"accepted-project-evidence.json").read_text())
    assert accepted[0]["game_date"]=="2024-11-20" and accepted[0]["opponent_key"]=="virginia"

def test_tier1_projects_second_half_source_date_to_season_end_year(tmp_path):
    ledger_row={"research_game_id":"C-DURABLE-JAN","season_label":"2024-25","source_date_literal":"1/15","stage2_opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}
    evidence=[{"source_game_id":"V-JAN","source_program_key":"virginia","game_date":"2025-01-15","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}]
    p,s,out=run_durable_schema_case(tmp_path,ledger_row,evidence)
    assert p.returncode==0 and s["accepted_count"]==1
    accepted=json.loads((out/"accepted-project-evidence.json").read_text())
    assert accepted[0]["game_date"]=="2025-01-15"

def test_tier1_projects_two_digit_century_rollover(tmp_path):
    ledger_row={"research_game_id":"C-DURABLE-2000","season_label":"1999-00","source_date_literal":"1/15","stage2_opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}
    evidence=[{"source_game_id":"V-2000","source_program_key":"virginia","game_date":"2000-01-15","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}]
    p,s,out=run_durable_schema_case(tmp_path,ledger_row,evidence)
    assert p.returncode==0 and s["accepted_count"]==1
    accepted=json.loads((out/"accepted-project-evidence.json").read_text())
    assert accepted[0]["game_date"]=="2000-01-15"

def test_tier1_explicit_game_date_precedes_source_date_literal(tmp_path):
    ledger_row={"research_game_id":"C-DURABLE-EXPLICIT","season_label":"2024-25","game_date":"2024-11-20","source_date_literal":"1/15","stage2_opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}
    evidence=[{"source_game_id":"V-EXPLICIT","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}]
    p,s,out=run_durable_schema_case(tmp_path,ledger_row,evidence)
    assert p.returncode==0 and s["accepted_count"]==1
    accepted=json.loads((out/"accepted-project-evidence.json").read_text())
    assert accepted[0]["game_date"]=="2024-11-20"

def test_tier1_blank_source_date_remains_unresolved(tmp_path):
    ledger_row={"research_game_id":"C-DURABLE-BLANK","season_label":"2024-25","source_date_literal":"","stage2_opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}
    evidence=[{"source_game_id":"V-BLANK","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}]
    p,s,out=run_durable_schema_case(tmp_path,ledger_row,evidence)
    assert p.returncode==0 and s["status"]=="COMPLETE" and s["accepted_count"]==0 and s["unresolved_count"]==1
    unresolved=json.loads((out/"tier1-unresolved.json").read_text())
    assert unresolved==[{"research_game_id":"C-DURABLE-BLANK","game_date":"","opponent_key":"virginia","reason":"NO_EXACT_DATE_FOR_TIER1_MATCH"}]

def test_tier1_malformed_or_impossible_source_date_remains_unresolved(tmp_path):
    for index,literal in enumerate(("Nov 20","2/30"),1):
        case=tmp_path/str(index);case.mkdir()
        ledger_row={"research_game_id":f"C-DURABLE-BAD-{index}","season_label":"2024-25","source_date_literal":literal,"stage2_opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}
        evidence=[{"source_game_id":f"V-BAD-{index}","source_program_key":"virginia","game_date":"2024-11-20","normalized_opponent_key":"clemson","curated_venue_name":"Arena A","city":"Atlanta","state":"GA"}]
        p,s,out=run_durable_schema_case(case,ledger_row,evidence)
        assert p.returncode==0 and s["status"]=="COMPLETE" and s["accepted_count"]==0 and s["unresolved_count"]==1
        unresolved=json.loads((out/"tier1-unresolved.json").read_text())
        assert unresolved[0]["game_date"]=="" and unresolved[0]["reason"]=="NO_EXACT_DATE_FOR_TIER1_MATCH"
