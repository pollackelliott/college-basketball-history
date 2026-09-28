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
def run(tmp_path,ledger_rows,input_path=None,extra_args=None):
    ledger=tmp_path/"ledger.csv";out=tmp_path/"out";write_csv(ledger,ledger_rows)
    target=input_path or ledger
    args=[sys.executable,str(SCRIPT),"clemson",str(target),"--output-dir",str(out),"--main-sha","PINNED"]
    if extra_args:args.extend(extra_args)
    p=subprocess.run(args,text=True,capture_output=True,cwd=tmp_path)
    return p,json.loads((out/"stage3a0-status.json").read_text()),out
def base_rows():
    return [
      {"research_game_id":"C-1","season_label":"2024-2025","game_date":"2024-11-01","opponent_key":"duke","site_type":"HOME","game_type":"REGULAR_SEASON"},
      {"research_game_id":"C-2","season_label":"1990-1991","game_date":"1991-03-15","opponent_key":"unc","site_type":"NEUTRAL","game_type":"NCAA"},
      {"research_game_id":"C-3","season_label":"1995-1996","game_date":"1995-12-01","opponent_key":"wake-forest","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"}]
def test_complete_checkpoint_only_partition_without_repository(tmp_path):
    p,s,out=run(tmp_path,base_rows())
    assert p.returncode==0 and s["status"]=="COMPLETE" and s["protected_main_sha"]=="PINNED"
    assert s["entry_mode"]=="ledger_csv"
    assert s["repository_state_required"] is False
    assert s["project_evidence_reuse"]["performed_in_stage3a0"] is False
    assert s["partition"]=={"postseason":1,"regular_season":2,"unclassified":0}
    assert s["regular_season_site_census"]=={"HOME":1,"OPPONENT_HOME":0,"NEUTRAL":1,"UNKNOWN":0}
    assert len(json.loads((out/"stage3a2-home-queue.json").read_text()))==1
    assert len(json.loads((out/"stage3b-postseason-handoff.json").read_text()))==1
    assert len(json.loads((out/"stage3a3-historical-neutral-queue.json").read_text()))==1
    assert not (out/"target-canonical-matches.json").exists()
    assert not (tmp_path/"data").exists()
def test_stage2_checkpoint_zip_is_direct_entrypoint(tmp_path):
    ledger_rows=base_rows();checkpoint=tmp_path/"stage2-complete.zip"
    with zipfile.ZipFile(checkpoint,"w") as z:
        z.writestr("nested/structured-stage2-ledger.csv",csv_text(ledger_rows));z.writestr("manifest.json","{}")
    p,s,out=run(tmp_path,ledger_rows,checkpoint)
    assert p.returncode==0 and s["status"]=="COMPLETE"
    assert s["entry_mode"]=="checkpoint_zip"
    assert s["input_checkpoint_member"]=="nested/structured-stage2-ledger.csv"
    assert (out/"stage3a0-input-ledger.csv").exists()
def test_checkpoint_zip_fallback_finds_unique_structured_ledger(tmp_path):
    ledger_rows=base_rows();checkpoint=tmp_path/"legacy-stage2.zip"
    with zipfile.ZipFile(checkpoint,"w") as z:
        z.writestr("stage2/final-games.csv",csv_text(ledger_rows));z.writestr("stage2/season-summary.csv","season,count\n2024-2025,1\n")
    p,s,out=run(tmp_path,ledger_rows,checkpoint)
    assert p.returncode==0 and s["input_checkpoint_member"]=="stage2/final-games.csv"
def test_checkpoint_zip_without_ledger_fails_entry_without_join(tmp_path):
    ledger_rows=base_rows();checkpoint=tmp_path/"bad.zip"
    with zipfile.ZipFile(checkpoint,"w") as z:z.writestr("counts.csv","season,count\n2024-2025,1\n")
    p,s,out=run(tmp_path,ledger_rows,checkpoint)
    assert p.returncode==2 and s["status"]=="STAGE_3A0_ENTRY_NOT_READY"
    assert s["entry_error"]=="NO_STAGE2_LEDGER_FOUND"
    assert not (out/"target-canonical-matches.json").exists()
def test_missing_game_type_fails_readiness_before_join(tmp_path):
    p,s,out=run(tmp_path,[{"research_game_id":"C-1","season_label":"1912-1913","game_date":"1913-01-01","opponent_key":"davidson","site_type":"HOME","game_type":""}])
    assert p.returncode==2 and s["status"]=="STAGE_3A0_INPUT_NOT_READY"
    assert s["readiness"]["blocking_defects"]["missing_game_type"]==["C-1"]
    assert s["remediation_code"]=="MISSING_GAME_TYPE_ONLY"
    assert not (out/"target-canonical-matches.json").exists()
def test_explicit_unknown_site_is_a_valid_queue_value(tmp_path):
    p,s,out=run(tmp_path,[{"research_game_id":"C-U","season_label":"1912-1913","game_date":"1913-01-01","opponent_key":"davidson","site_type":"UNKNOWN","game_type":"REGULAR_SEASON"}])
    assert p.returncode==0
    assert s["regular_season_site_census"]["UNKNOWN"]==1
    q=json.loads((out/"stage3a1-unknown-han-queue.json").read_text())
    assert [row["research_game_id"] for row in q]==["C-U"]

def test_unrecognized_site_type_is_rejected(tmp_path):
    p,s,out=run(tmp_path,[{"research_game_id":"C-BAD","season_label":"1912-1913","game_date":"1913-01-01","opponent_key":"davidson","site_type":"MYSTERY","game_type":"REGULAR_SEASON"}])
    assert p.returncode==2
    assert s["readiness"]["blocking_defects"]["unrecognized_site_type"]==["C-BAD"]
def test_legacy_migration_rejects_non_game_type_change(tmp_path):
    base=tmp_path/"base.csv";fixed=tmp_path/"fixed.csv";migration=Path(__file__).parents[1]/"tools"/"research_stage3a0_migrate.py"
    write_csv(base,[{"research_game_id":"C-1","game_date":"1982-02-13","opponent_key":"virginia","site_type":"HOME","game_type":""}])
    write_csv(fixed,[{"research_game_id":"C-1","game_date":"1982-03-05","opponent_key":"virginia","site_type":"HOME","game_type":"CONFERENCE_TOURNAMENT"}])
    p=subprocess.run([sys.executable,str(migration),str(base),str(fixed)],text=True,capture_output=True)
    assert p.returncode==2 and "non-game-type fields changed" in p.stdout


def test_policy_makes_stage3a0_checkpoint_only_and_connector_portable():
    root = Path(__file__).parents[1]

    contract = (root / "docs" / "stage3a0-local-only-contract.md").read_text(encoding="utf-8")
    bounded = (root / "docs" / "research-lane-bounded-execution.md").read_text(encoding="utf-8")
    portable = (root / "docs" / "research-portable-execution.md").read_text(encoding="utf-8")
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")

    assert "checkpoint-only" in contract.lower()
    assert "checkpoint-only" in bounded.lower()
    assert "checkpoint-only" in agents.lower()
    assert "repository archive is not required for Stage 3A-0" in portable
    assert "fetch the exact `tools/research_stage3a0.py` file" in portable
    assert "codeload" not in contract.lower()
    assert "target-only canonical exact-game join" not in contract
