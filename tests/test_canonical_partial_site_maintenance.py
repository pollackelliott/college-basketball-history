"""Canonical city/state partial-site detection and exact shared-data repair regression."""
from __future__ import annotations

import csv
import io
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from canonical_partial_site_maintenance import _git_blob, inspect_and_repair, run
from onboarding_plan import preexisting_partial_canonical_location_error


class CanonicalPartialSiteMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.fields = [
            "canonical_game_id", "season_label", "game_date",
            "team_a_key", "team_b_key", "team_a_score", "team_b_score",
            "site_type", "venue_id", "venue_key", "site_city", "site_state",
            "game_type", "notes"
        ]
        self.row = {
            "canonical_game_id": "CBBG-ONE",
            "season_label": "2019-2020", "game_date": "2019-11-27",
            "team_a_key": "alpha", "team_b_key": "beta",
            "team_a_score": "84", "team_b_score": "90",
            "site_type": "NEUTRAL", "venue_id": "", "venue_key": "",
            "site_city": "Maui", "site_state": "", "game_type": "REGULAR_SEASON",
            "notes": "Original evidence and sites stay unchanged.",
        }
        self.other = {**self.row, "canonical_game_id": "CBBG-TWO", "site_city": "", "notes": "untouched"}
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=self.fields, lineterminator="\r\n")
        writer.writeheader()
        writer.writerow(self.row)
        writer.writerow(self.other)
        self.canonical = out.getvalue().encode()
        s = io.StringIO(newline="")
        writer = csv.DictWriter(s, fieldnames=["source_game_id", "source_program_key",
                              "season_label", "game_date", "normalized_opponent_key",
                              "curated_site_type", "city", "state", "team_score",
                              "opponent_score", "raw_text"], lineterminator="\r\n")
        writer.writeheader()
        writer.writerow({
            "source_game_id": "BETA-ONE", "source_program_key": "beta",
            "season_label": "2019-2020", "game_date": "2019-11-27",
            "normalized_opponent_key": "alpha", "curated_site_type": "NEUTRAL",
            "city": "Maui", "state": "", "team_score": "90",
            "opponent_score": "84", "raw_text": "Maui, Hawai’i",
        })
        self.source = s.getvalue().encode()
        self.spec = {
            "game_id": "CBBG-ONE", "source_game_id": "BETA-ONE",
            "expected_canonical_blob": _git_blob(self.canonical),
            "source_expected": {
                "source_game_id": "BETA-ONE",
                "source_program_key": "beta", "normalized_opponent_key": "alpha",
                "curated_site_type": "NEUTRAL",
                "game_date": "2019-11-27", "city": "Maui", "state": "",
            },
            "literal_evidence": "Maui, Hawai’i",
            "canonical_expected": {
                "canonical_game_id": "CBBG-ONE", "site_type": "NEUTRAL",
                "site_city": "Maui", "site_state": "",
            },
            "approved_site_state": "HI",
        }

    def test_existing_partial_detected_before_reconciliation(self):
        error = preexisting_partial_canonical_location_error(self.row)
        self.assertIn("PREEXISTING_PARTIAL_CANONICAL_LOCATION CBBG-ONE", error)
        self.assertIn("source-supported shared-data maintenance", error)

    def test_state_only_partial_detected(self):
        row = {**self.row, "site_city": "", "site_state": "HI"}
        self.assertIn("PREEXISTING_PARTIAL_CANONICAL_LOCATION", preexisting_partial_canonical_location_error(row))

    def test_complete_or_fully_blank_location_not_a_false_positive(self):
        self.assertEqual(preexisting_partial_canonical_location_error(
            {**self.row, "site_state": "HI"}), "")
        self.assertEqual(preexisting_partial_canonical_location_error(
            {**self.row, "site_city": "", "site_state": ""}), "")

    def test_exact_one_row_only_and_raw_evidence_unchanged(self):
        revised, report = inspect_and_repair(self.canonical, self.source, self.spec)
        self.assertEqual(report["canonical_only_changed"], ["site_state"])
        self.assertEqual(revised.count(b"CBBG-TWO,"), 1)
        self.assertEqual(revised.count(b"site_city"), 1)
        self.assertEqual(revised.count(b"Maui,HI,"), 1)
        self.assertEqual(revised.replace(b"Maui,HI,", b"Maui,,", 1), self.canonical)
        self.assertEqual(report["result_git_blob"], _git_blob(revised))
        self.assertEqual(self.source.count(b"Hawai"), 1)

    def test_changed_canonical_blob_rejected(self):
        with self.assertRaisesRegex(ValueError, "CANONICAL_BLOB_SHA_MISMATCH"):
            inspect_and_repair(self.canonical + b"x", self.source, self.spec)

    def test_source_literal_missing_rejected(self):
        with self.assertRaisesRegex(ValueError, "SOURCE_RAW_LITERAL_UNSUPPORTED"):
            inspect_and_repair(self.canonical, self.source.replace("Hawai’i".encode(), b"unknown"), self.spec)

    def test_unsupported_precondition_rejected(self):
        self.spec["canonical_expected"]["site_type"] = "TEAM_A_HOME"
        with self.assertRaisesRegex(ValueError, "CANONICAL_ROW_PRECONDITION_CHANGED"):
            inspect_and_repair(self.canonical, self.source, self.spec)

    def test_no_inferred_state_without_source(self):
        self.spec["source_expected"]["city"] = "Honolulu"
        with self.assertRaisesRegex(ValueError, "SOURCE_EVIDENCE_CHANGED"):
            inspect_and_repair(self.canonical, self.source, self.spec)

    def test_real_case_remains_source_grounded_without_pinning_future_global_history(self):
        spec = json.loads((ROOT / "data/maintenance/canonical-location-dayton-kansas-2019-11-27.json").read_text())
        source_path = ROOT / spec["source_path"]
        with source_path.open(newline="", encoding="utf-8-sig") as handle:
            support = [row for row in csv.DictReader(handle)
                       if row["source_game_id"] == spec["source_game_id"]]
        self.assertEqual(len(support), 1)
        self.assertIn(spec["literal_evidence"], support[0]["raw_text"])
        self.assertEqual(support[0]["curated_site_type"], "NEUTRAL")

        with (ROOT / "data/canonical/games.csv").open(newline="", encoding="utf-8-sig") as handle:
            games = [row for row in csv.DictReader(handle)
                     if row["canonical_game_id"] == spec["game_id"]]
        self.assertEqual(len(games), 1)
        game = games[0]
        self.assertEqual(game["site_type"], "NEUTRAL")
        self.assertEqual(game["site_city"], "Maui")
        self.assertEqual(game["site_state"], "HI")
        self.assertEqual(game["venue_id"], "")
        self.assertEqual(game["venue_key"], "")


if __name__ == "__main__":
    unittest.main()
