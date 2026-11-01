"""Historical season coverage must never create fictional games or distort series."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_site_data import validated_historical_coverage


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
            "stage1_closeout_sha256": "f" * 64,
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
        self.row["stage1_closeout_sha256"] = ""
        with self.assertRaisesRegex(ValueError, "closeout SHA-256 required"):
            self.build()

    def test_changed_source_aggregate_is_rejected(self):
        self.row["official_wins"] = "7"
        with self.assertRaisesRegex(ValueError, "arithmetic/canonical discrepancy"):
            self.build()

    def test_duplicate_coverage_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.build(rows=[self.row, dict(self.row)])

    def test_missing_or_phantom_canonical_games_rejected(self):
        with self.assertRaisesRegex(ValueError, "no canonical games"):
            self.build(seasons={})


if __name__ == "__main__":
    unittest.main()
