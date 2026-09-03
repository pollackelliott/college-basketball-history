import contextlib
import io
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from verify_program_accomplishments import compare_program  # noqa: E402


def ncaa_game(
    game_id,
    season,
    date,
    round_name,
):
    return {
        "canonical_game_id": game_id,
        "season_label": season,
        "game_date": date,
        "team_a_key": "usc",
        "team_b_key": "opponent",
        "result_winner_team_key": "opponent",
        "game_type": "NCAA_TOURNAMENT",
        "postseason_round": round_name,
    }


class VerifiedHistoricalRoundCrosscheckTests(unittest.TestCase):
    def setUp(self):
        self.program = {
            "program_key": "usc",
            "history_start_season": "1906-1907",
            "history_scope_status": "OWNER_CONFIRMED",
            "history_scope_basis": "ALWAYS_TOP_LEVEL_FROM_INCEPTION",
        }

        self.games = [
            ncaa_game(
                "CBBG-FINAL-FOUR",
                "1953-1954",
                "1954-03-19",
                "Final Four",
            ),
            # Deliberately blank: represents an old NCAA format for which
            # the repository has no honest controlled-round mapping.
            ncaa_game(
                "CBBG-HISTORICAL-ROUND",
                "1959-1960",
                "1960-03-07",
                "",
            ),
        ]

        self.reference = {
            "program_key": "usc",
            "conference_regular_season_championships": "14",
            "conference_tournament_championships": "1",
            "ncaa_tournament_appearances": "2",
            "final_four_appearances": "1",
            "national_championships": "0",
            "best_finish_key": "FINAL_FOUR",
            "best_finish_year": "1954",
            "verification_status": "VERIFIED",
            "canonical_crosscheck_status": "MATCH",
        }

    def run_compare(self, reference=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = compare_program(
                self.program,
                reference or self.reference,
                self.games,
            )
        return result, output.getvalue()

    def test_verified_matching_reference_allows_diagnostic_round_gap(self):
        result, output = self.run_compare()

        self.assertTrue(result)
        self.assertIn("usc: MATCH", output)
        self.assertIn(
            "Historical NCAA round gaps remain diagnostic only",
            output,
        )
        self.assertIn(
            "1959-1960 has no resolved NCAA round",
            output,
        )

    def test_unverified_reference_with_same_round_gap_still_fails(self):
        reference = dict(self.reference)
        reference["verification_status"] = "OWNER_BASELINE_UNVERIFIED"

        result, output = self.run_compare(reference)

        self.assertFalse(result)
        self.assertIn("usc: INCOMPLETE", output)

    def test_nonmatching_stored_crosscheck_with_round_gap_still_fails(self):
        reference = dict(self.reference)
        reference["canonical_crosscheck_status"] = "NOT_CHECKED"

        result, output = self.run_compare(reference)

        self.assertFalse(result)
        self.assertIn("usc: INCOMPLETE", output)

    def test_real_aggregate_conflict_still_fails_verified_reference(self):
        reference = dict(self.reference)
        reference["final_four_appearances"] = "2"

        result, output = self.run_compare(reference)

        self.assertFalse(result)
        self.assertIn("usc: CONFLICT", output)
        self.assertIn(
            "final_four_appearances",
            output,
        )


if __name__ == "__main__":
    unittest.main()
