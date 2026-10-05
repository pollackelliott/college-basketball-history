import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "schools" / "oklahoma-state" / "source-games.csv"

# "plain ot" here means the literal single-OT token immediately after the
# printed final score. Explicit multi-OT notation such as "... 2 OT" does not
# match this topology.
PLAIN_OT_AFTER_SCORE = re.compile(
    r"\b\d+\s*-\s*\d+\s+ot\s*$",
    re.IGNORECASE,
)


class OklahomaStatePlainOvertimeRegressionTests(unittest.TestCase):
    def rows(self):
        with SOURCE.open(encoding="utf-8-sig", newline="") as handle:
            return list(csv.DictReader(handle))

    def test_plain_ot_rows_encode_one_overtime_period(self):
        candidates = [
            row
            for row in self.rows()
            if PLAIN_OT_AFTER_SCORE.search(row.get("raw_text", ""))
        ]
        self.assertTrue(candidates)
        offenders = [
            (
                row.get("source_game_id", ""),
                row.get("overtime_periods", ""),
                row.get("raw_text", ""),
            )
            for row in candidates
            if row.get("overtime_periods", "").strip() != "1"
        ]
        self.assertEqual([], offenders)

    def test_smu_regression_examples_preserve_raw_evidence(self):
        by_id = {
            row.get("source_game_id", ""): row
            for row in self.rows()
        }
        expected = {
            "OKSTRAW-00837": "Dec. 11 13 at - SMU W 50-45 ot",
            "OKSTRAW-02056": "Dec. 9 rv at - SMU W 67-60 ot",
        }
        for source_id, raw_text in expected.items():
            self.assertIn(source_id, by_id)
            self.assertEqual(raw_text, by_id[source_id]["raw_text"])
            self.assertEqual("1", by_id[source_id]["overtime_periods"])


if __name__ == "__main__":
    unittest.main()
