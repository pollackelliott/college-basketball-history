"""Historical season coverage must never create fictional games or distort series."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_site_data import validated_historical_coverage, validated_historical_accounting


class HistoricalCoverageBuildTests(unittest.TestCase):
    def setUp(self):
        self.authority = {
            ("example", "1919-20"): {
                "institutional_record": {"wins": 6, "losses": 10, "games": 16},
                "identified_record": {"wins": 3, "losses": 7, "games": 10},
                "unidentified_record": {"wins": 3, "losses": 3, "games": 6},
                "owner_disposition": "https://github.com/example/history/issues/1",
            }
        }
        self.seasons = {"1919-20": [{"result": "W"}] * 3 + [{"result": "L"}] * 7}
        self.row = {
            "program_key": "example", "season_label": "1919-20",
            "official_wins": "6", "official_losses": "10", "official_games": "16",
            "documented_wins": "3", "documented_losses": "7", "documented_games": "10",
            "unidentified_wins": "3", "unidentified_losses": "3", "unidentified_games": "6",
            "source_label": "Example institutional record book",
            "owner_disposition": "https://github.com/example/history/issues/1",
            "stage1_audit_sha256": "f" * 64,
            "public_note": "",
        }

    def build(self, rows=None, seasons=None, authority=None):
        return validated_historical_coverage(
            [self.row] if rows is None else rows,
            "example",
            self.seasons if seasons is None else seasons,
            self.authority if authority is None else authority,
        )

    def test_official_and_documented_records_remain_distinct(self):
        before = {key: list(value) for key, value in self.seasons.items()}
        result = self.build()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["unidentified_record"]["games"], 6)
        self.assertEqual(result[0]["official_record"]["wins"], 6)
        self.assertIn("10 individual game results", result[0]["note"])
        self.assertIn("six", result[0]["note"].lower().replace("6", "six"))
        self.assertEqual(self.seasons, before)

    def test_no_coverage_row_preserves_current_build(self):
        self.assertEqual(self.build(rows=[]), [])

    def test_canonical_result_drift_is_rejected(self):
        games = {"1919-20": [{"result": "W"}] * 4 + [{"result": "L"}] * 6}
        with self.assertRaisesRegex(ValueError, "arithmetic/canonical discrepancy"):
            self.build(seasons=games)

    def test_unauthorized_season_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "lacks owner authority"):
            self.build(authority={})

    def test_missing_closeout_hash_is_rejected(self):
        self.row["stage1_audit_sha256"] = ""
        with self.assertRaisesRegex(ValueError, "audit SHA-256 required"):
            self.build()

    def test_changed_source_aggregate_is_rejected(self):
        self.row["official_wins"] = "7"
        with self.assertRaisesRegex(ValueError, "arithmetic/canonical discrepancy"):
            self.build()

    def test_duplicate_coverage_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.build(rows=[self.row, dict(self.row)])

    def test_missing_or_phantom_canonical_games_rejected(self):
        with self.assertRaisesRegex(ValueError, "arithmetic/canonical discrepancy"):
            self.build(seasons={})

    def test_zero_documented_coverage_season_is_allowed(self):
        authority = {
            ("example", "1909-10"): {
                "institutional_record": {"wins": 2, "losses": 0, "games": 2},
                "identified_record": {"wins": 0, "losses": 0, "games": 0},
                "unidentified_record": {"wins": 2, "losses": 0, "games": 2},
                "owner_disposition": "https://github.com/example/history/issues/2",
            }
        }
        row = {
            "program_key": "example", "season_label": "1909-10",
            "official_wins": "2", "official_losses": "0", "official_games": "2",
            "documented_wins": "0", "documented_losses": "0", "documented_games": "0",
            "unidentified_wins": "2", "unidentified_losses": "0", "unidentified_games": "2",
            "source_label": "Institutional aggregate",
            "owner_disposition": "https://github.com/example/history/issues/2",
            "stage1_audit_sha256": "e" * 64, "public_note": "",
        }
        result = validated_historical_coverage([row], "example", {}, authority)
        self.assertEqual(result[0]["documented_record"]["games"], 0)
        self.assertEqual(result[0]["official_record"]["games"], 2)

    def test_accounting_contradiction_preserves_negative_delta(self):
        authority = {
            ("example", "1903-04"): {
                "institutional_record": {"wins": 0, "losses": 0, "games": 0},
                "identified_record": {"wins": 1, "losses": 0, "games": 1},
                "mechanical_delta": {"wins": -1, "losses": 0, "games": -1},
                "owner_disposition": "https://github.com/example/history/issues/2",
            }
        }
        rows = [{
            "program_key": "example", "season_label": "1903-04",
            "official_wins": "0", "official_losses": "0", "official_games": "0",
            "documented_wins": "1", "documented_losses": "0", "documented_games": "1",
            "delta_wins": "-1", "delta_losses": "0", "delta_games": "-1",
            "classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
            "source_label": "Conflicting institutional structures",
            "owner_disposition": "https://github.com/example/history/issues/2",
            "stage1_audit_sha256": "e" * 64, "public_note": "Diagnostic only",
        }]
        seasons = {"1903-04": [{"result": "W"}]}
        result = validated_historical_accounting(rows, "example", seasons, authority)
        self.assertEqual(result[0]["mechanical_delta"]["games"], -1)
        self.assertEqual(seasons["1903-04"], [{"result": "W"}])


if __name__ == "__main__":
    unittest.main()
