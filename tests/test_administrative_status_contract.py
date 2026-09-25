import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from administrative_status import (  # noqa: E402
    administrative_status_errors,
    normalize_legacy_vacated_season_context_row,
)
from normalize_legacy_administrative_status import normalize_rows  # noqa: E402


class AdministrativeStatusContractTests(unittest.TestCase):
    def test_supported_status_requires_note(self):
        row = {
            "administrative_status": "VACATED_WIN",
            "administrative_note": "",
        }
        self.assertTrue(
            any(
                "administrative_note is required" in error
                for error in administrative_status_errors(row, "TEST-1")
            )
        )

    def test_unsupported_status_is_rejected(self):
        row = {
            "administrative_status": "VACATED_SEASON_CONTEXT",
            "administrative_note": "Victories from this season were later vacated.",
        }
        self.assertTrue(
            any(
                "invalid administrative_status" in error
                for error in administrative_status_errors(row, "TEST-1")
            )
        )

    def test_legacy_context_win_becomes_vacated_win(self):
        row = {
            "source_game_id": "TEST-W",
            "played_result": "W",
            "administrative_status": "VACATED_SEASON_CONTEXT",
            "administrative_note": "Victories from this season were later vacated.",
        }
        normalized, changed = normalize_legacy_vacated_season_context_row(row)
        self.assertTrue(changed)
        self.assertEqual(normalized["administrative_status"], "VACATED_WIN")
        self.assertEqual(
            normalized["administrative_note"],
            row["administrative_note"],
        )

    def test_legacy_context_loss_becomes_context_only(self):
        row = {
            "source_game_id": "TEST-L",
            "played_result": "L",
            "administrative_status": "VACATED_SEASON_CONTEXT",
            "administrative_note": "Victories from this season were later vacated.",
        }
        normalized, changed = normalize_legacy_vacated_season_context_row(row)
        self.assertTrue(changed)
        self.assertEqual(normalized["administrative_status"], "")
        self.assertEqual(
            normalized["administrative_note"],
            row["administrative_note"],
        )

    def test_legacy_context_requires_explicit_frozen_premise(self):
        row = {
            "source_game_id": "TEST-X",
            "played_result": "W",
            "administrative_status": "VACATED_SEASON_CONTEXT",
            "administrative_note": "Season subject to later administrative action.",
        }
        with self.assertRaisesRegex(ValueError, "victories were vacated"):
            normalize_legacy_vacated_season_context_row(row)

    def test_population_normalization_reports_exact_partition(self):
        rows = [
            {
                "source_game_id": "W1",
                "played_result": "W",
                "administrative_status": "VACATED_SEASON_CONTEXT",
                "administrative_note": "Victories from this season were later vacated.",
            },
            {
                "source_game_id": "L1",
                "played_result": "L",
                "administrative_status": "VACATED_SEASON_CONTEXT",
                "administrative_note": "Victories from this season were later vacated.",
            },
        ]
        normalized, counts = normalize_rows(rows)
        self.assertEqual(counts["legacy_rows"], 2)
        self.assertEqual(counts["vacated_wins"], 1)
        self.assertEqual(counts["context_only_nonwins"], 1)
        self.assertEqual(
            [row["administrative_status"] for row in normalized],
            ["VACATED_WIN", ""],
        )


if __name__ == "__main__":
    unittest.main()
