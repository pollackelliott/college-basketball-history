import csv,json,subprocess,sys
from pathlib import Path
def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def run(tmp_path,ledger_rows,canonical_rows):
    ledger=tmp_path/"ledger.csv";canonical=tmp_path/"canonical.csv";out=tmp_path/"out";write_csv(ledger,ledger_rows);write_csv(canonical,canonical_rows)
    p=subprocess.run([sys.executable,"tools/research_stage3a0.py","clemson",str(ledger),"--canonical",str(canonical),"--output-dir",str(out),"--main-sha","PINNED"],text=True,capture_output=True)
    return p,json.loads((out/"stage3a0-status.json").read_text()),out
def test_complete_target_only_join(tmp_path):
    p,s,out=run(tmp_path,[
      {"research_game_id":"C-1","season_label":"2024-2025","game_date":"2024-11-01","opponent_key":"duke","site_type":"HOME","game_type":"REGULAR_SEASON"},
      {"research_game_id":"C-2","season_label":"1990-1991","game_date":"1991-03-15","opponent_key":"unc","site_type":"NEUTRAL","game_type":"NCAA"},
      {"research_game_id":"C-3","season_label":"1995-1996","game_date":"1995-12-01","opponent_key":"wake-forest","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}],
      [{"canonical_game_id":"G-1","game_date":"2024-11-01","team_a_key":"clemson","team_b_key":"duke"}])
    assert p.returncode==0 and s["status"]=="COMPLETE" and s["protected_main_sha"]=="PINNED"
    assert s["partition"]=={"postseason":1,"regular_season":2,"unclassified":0}
    assert s["target_only_join"]["matched"]==1 and s["target_only_join"]["unmatched_is_blocking_stage3a0"] is False
def test_missing_game_type_fails_readiness_before_join(tmp_path):
    p,s,out=run(tmp_path,[{"research_game_id":"C-1","season_label":"1912-1913","game_date":"1913-01-01","opponent_key":"davidson","site_type":"HOME","game_type":""}],
      [{"canonical_game_id":"G-X","game_date":"1913-01-01","team_a_key":"clemson","team_b_key":"davidson"}])
    assert p.returncode==2 and s["status"]=="STAGE_3A0_INPUT_NOT_READY"
    assert s["readiness"]["blocking_defects"]["missing_game_type"]==["C-1"]
    assert not (out/"target-canonical-matches.json").exists()
def test_collision_is_serialized_not_chosen(tmp_path):
    p,s,out=run(tmp_path,[{"research_game_id":"C-V","season_label":"1981-1982","game_date":"1982-03-05","opponent_key":"virginia","site_type":"NEUTRAL","game_type":"CONFERENCE_TOURNAMENT"}],
      [{"canonical_game_id":"G-A","game_date":"1982-03-05","team_a_key":"clemson","team_b_key":"virginia"},{"canonical_game_id":"G-B","game_date":"1982-03-05","team_a_key":"virginia","team_b_key":"clemson"}])
    assert p.returncode==0
    c=json.loads((out/"local-contradictions.json").read_text())
    assert len(c)==1 and c[0]["reason"]=="MULTIPLE_EXACT_DATE_OPPONENT_MATCHES"
def test_legacy_migration_rejects_non_game_type_change(tmp_path):
    base=tmp_path/"base.csv";fixed=tmp_path/"fixed.csv"
    write_csv(base,[{"research_game_id":"C-1","game_date":"1982-02-13","opponent_key":"virginia","site_type":"HOME","game_type":""}])
    write_csv(fixed,[{"research_game_id":"C-1","game_date":"1982-03-05","opponent_key":"virginia","site_type":"HOME","game_type":"CONFERENCE_TOURNAMENT"}])
    p=subprocess.run([sys.executable,"tools/research_stage3a0_migrate.py",str(base),str(fixed)],text=True,capture_output=True)
    assert p.returncode==2 and "non-game-type fields changed" in p.stdout
