import csv, json, subprocess, sys
from pathlib import Path

def write_csv(path, rows):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

def run(tmp_path, ledger_rows, canonical_rows):
    ledger=tmp_path/"ledger.csv"; canonical=tmp_path/"canonical.csv"; assertions=tmp_path/"assertions.csv"; out=tmp_path/"out"
    write_csv(ledger,ledger_rows); write_csv(canonical,canonical_rows)
    assertions.write_text("canonical_game_id,source_program_key\n",encoding="utf-8")
    subprocess.run([sys.executable,"tools/research_stage3a0.py","clemson",str(ledger),"--canonical",str(canonical),"--assertions",str(assertions),"--output-dir",str(out)],check=True)
    return json.loads((out/"stage3a0-summary.json").read_text()),out

def test_stage3a0_mechanical_partition_and_target_join(tmp_path):
    s,out=run(tmp_path,[
      {"research_game_id":"C-1","season_label":"2024-2025","game_date":"2024-11-01","opponent_key":"duke","site_type":"HOME","game_type":"REGULAR_SEASON"},
      {"research_game_id":"C-2","season_label":"1990-1991","game_date":"1991-03-15","opponent_key":"unc","site_type":"NEUTRAL","game_type":"NCAA"},
      {"research_game_id":"C-3","season_label":"1995-1996","game_date":"1995-12-01","opponent_key":"wake-forest","site_type":"NEUTRAL","game_type":"REGULAR_SEASON"},
    ],[
      {"canonical_game_id":"G-1","game_date":"2024-11-01","team_a_key":"clemson","team_b_key":"duke"},
    ])
    assert s["status"]=="COMPLETE"
    assert s["partition"]=={"postseason":1,"regular_season":2,"unclassified":0}
    assert s["regular_season_site_census"]["HOME"]==1
    assert s["neutral_era_census"]["HISTORICAL_1995_96_OR_EARLIER"]==1
    assert s["target_only_join"]["matched"]==1
    assert s["target_only_join"]["unmatched"]==1
    assert json.loads((out/"local-contradictions.json").read_text())==[]

def test_stage3a0_missing_partition_is_durable_output_not_discovery(tmp_path):
    s,out=run(tmp_path,[
      {"research_game_id":"C-1","season_label":"1912-1913","game_date":"","opponent_key":"davidson","site_type":"","game_type":""},
    ],[
      {"canonical_game_id":"G-X","game_date":"1913-01-01","team_a_key":"clemson","team_b_key":"davidson"},
    ])
    assert s["status"]=="INCOMPLETE_STRUCTURED_PARTITION"
    residual=json.loads((out/"unclassified-partition-rows.json").read_text())
    assert [r["_research_row_id"] for r in residual]==["C-1"]
    assert s["external_historical_research_used"] is False
