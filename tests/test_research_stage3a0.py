import csv,json,subprocess,sys,zipfile
from pathlib import Path
SCRIPT=Path(__file__).parents[1]/"tools"/"research_stage3a0.py"
def write_csv(path,rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def csv_text(rows):
    import io
    s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows);return s.getvalue()
def run(tmp_path,ledger_rows,canonical_rows,input_path=None):
    ledger=tmp_path/"ledger.csv";canonical=tmp_path/"canonical.csv";out=tmp_path/"out";write_csv(ledger,ledger_rows);write_csv(canonical,canonical_rows)
    target=input_path or ledger
    p=subprocess.run([sys.executable,str(SCRIPT),"clemson",str(target),"--canonical",str(canonical),"--output-dir",str(out),"--main-sha","PINNED"],text=True,capture_output=True)
    return p,json.loads((out/"stage3a0-status.json").read_text()),out
def base_rows():
    return [
      {"research_game_id":"C-1","season_label":"2024-2025","game_date":"2024-11-01","opponent_key":"duke","site_type":"HOME","game_type":"REGULAR_SEASON"},
      {"research_game_id":"C-2","season_label":"1990-1991","game_date":"1991-03-15","opponent_key":"unc","site_type":"NEUTRAL","game_type":"NCAA"},
      {"research_game_id":"C-3","season_label":"1995-1996","game_date":"1995-12-01","opponent_key":"wake-forest","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}]
def canonical_rows():return [{"canonical_game_id":"G-1","game_date":"2024-11-01","team_a_key":"clemson","team_b_key":"duke"}]
def test_complete_target_only_join(tmp_path):
    p,s,out=run(tmp_path,base_rows(),canonical_rows())
    assert p.returncode==0 and s["status"]=="COMPLETE" and s["protected_main_sha"]=="PINNED"
    assert s["entry_mode"]=="ledger_csv"
    assert s["partition"]=={"postseason":1,"regular_season":2,"unclassified":0}
    assert s["target_only_join"]["matched"]==1 and s["target_only_join"]["unmatched_is_blocking_stage3a0"] is False
    assert len(json.loads((out/"stage3a1-home-queue.json").read_text()))==1
    assert len(json.loads((out/"stage3b-postseason-handoff.json").read_text()))==1
    assert len(json.loads((out/"stage3a3-historical-neutral-queue.json").read_text()))==1
def test_stage2_checkpoint_zip_is_direct_entrypoint(tmp_path):
    ledger_rows=base_rows();checkpoint=tmp_path/"stage2-complete.zip"
    with zipfile.ZipFile(checkpoint,"w") as z:
        z.writestr("nested/structured-stage2-ledger.csv",csv_text(ledger_rows));z.writestr("manifest.json","{}")
    p,s,out=run(tmp_path,ledger_rows,canonical_rows(),checkpoint)
    assert p.returncode==0 and s["status"]=="COMPLETE"
    assert s["entry_mode"]=="checkpoint_zip"
    assert s["input_checkpoint_member"]=="nested/structured-stage2-ledger.csv"
    assert (out/"stage3a0-input-ledger.csv").exists()
def test_checkpoint_zip_fallback_finds_unique_structured_ledger(tmp_path):
    ledger_rows=base_rows();checkpoint=tmp_path/"legacy-stage2.zip"
    with zipfile.ZipFile(checkpoint,"w") as z:
        z.writestr("stage2/final-games.csv",csv_text(ledger_rows));z.writestr("stage2/season-summary.csv","season,count\n2024-2025,1\n")
    p,s,out=run(tmp_path,ledger_rows,canonical_rows(),checkpoint)
    assert p.returncode==0 and s["input_checkpoint_member"]=="stage2/final-games.csv"
def test_checkpoint_zip_without_ledger_fails_entry_without_join(tmp_path):
    ledger_rows=base_rows();checkpoint=tmp_path/"bad.zip"
    with zipfile.ZipFile(checkpoint,"w") as z:z.writestr("counts.csv","season,count\n2024-2025,1\n")
    p,s,out=run(tmp_path,ledger_rows,canonical_rows(),checkpoint)
    assert p.returncode==2 and s["status"]=="STAGE_3A0_ENTRY_NOT_READY"
    assert s["entry_error"]=="NO_STAGE2_LEDGER_FOUND"
    assert not (out/"target-canonical-matches.json").exists()
def test_missing_game_type_fails_readiness_before_join(tmp_path):
    p,s,out=run(tmp_path,[{"research_game_id":"C-1","season_label":"1912-1913","game_date":"1913-01-01","opponent_key":"davidson","site_type":"HOME","game_type":""}],
      [{"canonical_game_id":"G-X","game_date":"1913-01-01","team_a_key":"clemson","team_b_key":"davidson"}])
    assert p.returncode==2 and s["status"]=="STAGE_3A0_INPUT_NOT_READY"
    assert s["readiness"]["blocking_defects"]["missing_game_type"]==["C-1"]
    assert s["remediation_code"]=="MISSING_GAME_TYPE_ONLY"
    assert not (out/"target-canonical-matches.json").exists()
def test_collision_is_serialized_not_chosen(tmp_path):
    p,s,out=run(tmp_path,[{"research_game_id":"C-V","season_label":"1981-1982","game_date":"1982-03-05","opponent_key":"virginia","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}],
      [{"canonical_game_id":"G-A","game_date":"1982-03-05","team_a_key":"clemson","team_b_key":"virginia"},{"canonical_game_id":"G-B","game_date":"1982-03-05","team_a_key":"virginia","team_b_key":"clemson"}])
    assert p.returncode==0
    c=json.loads((out/"local-contradictions.json").read_text())
    assert len(c)==1 and c[0]["reason"]=="MULTIPLE_EXACT_DATE_OPPONENT_MATCHES"
def test_legacy_migration_rejects_non_game_type_change(tmp_path):
    base=tmp_path/"base.csv";fixed=tmp_path/"fixed.csv";migration=Path(__file__).parents[1]/"tools"/"research_stage3a0_migrate.py"
    write_csv(base,[{"research_game_id":"C-1","game_date":"1982-02-13","opponent_key":"virginia","site_type":"HOME","game_type":""}])
    write_csv(fixed,[{"research_game_id":"C-1","game_date":"1982-03-05","opponent_key":"virginia","site_type":"HOME","game_type":"CONFERENCE_TOURNAMENT"}])
    p=subprocess.run([sys.executable,str(migration),str(base),str(fixed)],text=True,capture_output=True)
    assert p.returncode==2 and "non-game-type fields changed" in p.stdout
