import csv
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "research_stage3a0.py"


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def test_stage3a0_is_target_only_deterministic_and_serializes_residuals(tmp_path):
    source_fields = [
        "source_game_id", "source_program_key", "season_label", "game_date",
        "normalized_opponent_key", "normalized_opponent_name", "team_score",
        "opponent_score", "curated_site_type", "curated_venue_name", "city",
        "state", "curated_game_type",
    ]
    rows = [
        dict(source_game_id="T-1", source_program_key="test", season_label="2000-2001", game_date="2000-11-01", normalized_opponent_key="alpha", normalized_opponent_name="Alpha", team_score="70", opponent_score="60", curated_site_type="SOURCE_PROGRAM_HOME", curated_venue_name="", city="", state="", curated_game_type="REGULAR_SEASON"),
        dict(source_game_id="T-2", source_program_key="test", season_label="1990-1991", game_date="1990-12-01", normalized_opponent_key="beta", normalized_opponent_name="Beta", team_score="65", opponent_score="64", curated_site_type="NEUTRAL", curated_venue_name="", city="", state="", curated_game_type="REGULAR_SEASON"),
        dict(source_game_id="T-3", source_program_key="test", season_label="2000-2001", game_date="2001-03-15", normalized_opponent_key="gamma", normalized_opponent_name="Gamma", team_score="80", opponent_score="75", curated_site_type="NEUTRAL", curated_venue_name="", city="", state="", curated_game_type="NCAA_TOURNAMENT"),
    ]
    write_csv(tmp_path / "schools/test/source-games.csv", source_fields, rows)

    canonical_fields = [
        "canonical_game_id", "season_label", "game_date", "team_a_key", "team_b_key",
        "team_a_score", "team_b_score", "site_type", "designated_home_team_key",
        "venue_key", "venue_id", "site_city", "site_state",
    ]
    write_csv(tmp_path / "data/canonical/games.csv", canonical_fields, [
        dict(canonical_game_id="C-1", season_label="2000-2001", game_date="2000-11-01", team_a_key="alpha", team_b_key="test", team_a_score="60", team_b_score="70", site_type="TEAM_B_HOME", designated_home_team_key="test", venue_key="test-arena", venue_id="VEN-1", site_city="Testville", site_state="TS"),
    ])

    # A local opponent package deliberately contains tempting evidence. Stage 3A-0 must
    # not read it; the unmatched Beta row must survive as output.
    write_csv(tmp_path / "schools/beta/source-games.csv", source_fields, [
        dict(source_game_id="B-1", source_program_key="beta", season_label="1990-1991", game_date="1990-12-01", normalized_opponent_key="test", normalized_opponent_name="Test", team_score="64", opponent_score="65", curated_site_type="NEUTRAL", curated_venue_name="Forbidden Discovery Arena", city="Somewhere", state="TS", curated_game_type="REGULAR_SEASON"),
    ])

    proc = subprocess.run([sys.executable, str(TOOL), "test", str(tmp_path)], text=True, capture_output=True)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "STAGE 3A-0: COMPLETE" in proc.stdout
    assert "External historical research used: NO" in proc.stdout

    ledger = json.loads((tmp_path / ".research/test/stage3a0-ledger.json").read_text())
    assert ledger["counts"]["stage1_total"] == 3
    assert ledger["counts"]["regular_season"] == 2
    assert ledger["counts"]["postseason_handoff"] == 1
    assert ledger["counts"]["home"] == 1
    assert ledger["counts"]["neutral"] == 1
    assert ledger["counts"]["historical_neutral_1995_96_and_earlier"] == 1
    assert ledger["counts"]["canonical_join_accepted"] == 1
    assert ledger["counts"]["canonical_join_unmatched"] == 1
    assert ledger["external_historical_research_used"] is False
    text = json.dumps(ledger)
    assert "Forbidden Discovery Arena" not in text
    assert ledger["queues"]["canonical_join_unmatched"][0]["source_game_id"] == "T-2"


def test_stage3a0_serializes_bad_partition_and_stops(tmp_path):
    fields = ["source_game_id", "source_program_key", "season_label", "game_date", "normalized_opponent_key", "normalized_opponent_name", "team_score", "opponent_score", "curated_site_type", "curated_venue_name", "city", "state", "curated_game_type"]
    write_csv(tmp_path / "schools/test/source-games.csv", fields, [
        dict(source_game_id="T-X", source_program_key="test", season_label="2000-2001", game_date="", normalized_opponent_key="alpha", normalized_opponent_name="Alpha", team_score="", opponent_score="", curated_site_type="", curated_venue_name="", city="", state="", curated_game_type=""),
    ])
    write_csv(tmp_path / "data/canonical/games.csv", ["canonical_game_id", "season_label", "game_date", "team_a_key", "team_b_key"], [])

    proc = subprocess.run([sys.executable, str(TOOL), "test", str(tmp_path)], text=True, capture_output=True)
    assert proc.returncode == 1
    assert "INCOMPLETE: 1 rows have invalid/unclassified game_type" in proc.stdout
    ledger = json.loads((tmp_path / ".research/test/stage3a0-ledger.json").read_text())
    assert ledger["counts"]["invalid_or_unclassified_game_type"] == 1
    assert ledger["invalid_or_unclassified_rows"][0]["source_game_id"] == "T-X"
