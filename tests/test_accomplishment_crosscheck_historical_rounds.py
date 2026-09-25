import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    _accomplishment_conflicts,
    _accomplishment_crosscheck_game,
)


def ncaa_game(
    game_id,
    season,
    game_date,
    round_name,
    *,
    opponent="opponent",
    winner="opponent",
):
    return {
        "canonical_game_id": game_id,
        "season_label": season,
        "game_date": game_date,
        "date_precision": "EXACT",
        "team_a_key": "usc",
        "team_b_key": opponent,
        "team_a_score": "60",
        "team_b_score": "70",
        "result_winner_team_key": winner,
        "overtime_periods": "0",
        "site_type": "NEUTRAL",
        "designated_home_team_key": "",
        "venue_key": "",
        "venue_id": "",
        "site_city": "",
        "site_state": "",
        "game_type": "NCAA_TOURNAMENT",
        "postseason_round": round_name,
        "administrative_status": "",
        "administrative_note": "",
        "canonical_status": "PROVISIONAL",
        "notes": "",
    }


class HistoricalRoundAccomplishmentCrosscheckTests(unittest.TestCase):
    def setUp(self):
        self.program = {
            "program_key": "usc",
            "history_start_season": "1906-1907",
        }
        self.reference = {
            "ncaa_tournament_appearances": "2",
            "final_four_appearances": "1",
            "national_championships": "0",
            "best_finish_key": "FINAL_FOUR",
            "best_finish_year": "1954",
        }
        self.games = [
            ncaa_game(
                "CBBG-FF",
                "1953-1954",
                "1954-03-19",
                "Final Four",
            ),
            # Deliberately blank: an old tournament format with no honest
            # controlled-vocabulary equivalent.
            ncaa_game(
                "CBBG-OLD-FORMAT",
                "1959-1960",
                "1960-03-07",
                "",
            ),
        ]

    def test_confident_blank_source_round_inherits_known_canonical_round(self):
        source = {
            "source_program_key": "usc",
            "source_game_id": "USC-2010-FF",
            "season_label": "2009-2010",
            "game_date": "2010-04-03",
            "normalized_opponent_key": "duke",
            "team_score": "57",
            "opponent_score": "78",
            "played_result": "L",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "Indianapolis",
            "state": "IN",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "",
        }
        canonical = ncaa_game(
            "CBBG-2010-FF",
            "2009-2010",
            "2010-04-03",
            "Final Four",
            opponent="duke",
            winner="duke",
        )

        predicted = _accomplishment_crosscheck_game(
            source,
            ingest_school.CONFIDENT,
            "CBBG-2010-FF",
            {"CBBG-2010-FF": canonical},
            {},
            {},
            "PREFLIGHT-USC-2010-FF",
        )

        self.assertEqual(predicted["postseason_round"], "Final Four")
        self.assertEqual(source["curated_postseason_round"], "")

    def test_nonblank_source_round_is_not_overwritten_by_canonical_fallback(self):
        source = {
            "source_program_key": "usc",
            "source_game_id": "USC-ROUND-CONFLICT",
            "season_label": "2009-2010",
            "game_date": "2010-03-21",
            "normalized_opponent_key": "duke",
            "team_score": "70",
            "opponent_score": "68",
            "played_result": "W",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "Indianapolis",
            "state": "IN",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "R32",
        }
        canonical = ncaa_game(
            "CBBG-ROUND-CONFLICT",
            "2009-2010",
            "2010-03-21",
            "Final Four",
            opponent="duke",
            winner="usc",
        )

        predicted = _accomplishment_crosscheck_game(
            source,
            ingest_school.CONFIDENT,
            "CBBG-ROUND-CONFLICT",
            {"CBBG-ROUND-CONFLICT": canonical},
            {},
            {},
            "PREFLIGHT-USC-ROUND-CONFLICT",
        )

        self.assertEqual(predicted["postseason_round"], "R32")

    def test_honest_blank_round_does_not_block_matching_aggregates(self):
        derived, conflicts = _accomplishment_conflicts(
            self.program,
            self.reference,
            self.games,
        )

        self.assertEqual(
            derived["ncaa_tournament_appearances"],
            2,
        )
        self.assertIn(
            "1959-1960 has no resolved NCAA round",
            derived["incomplete_reasons"],
        )
        self.assertEqual(conflicts, [])

    def test_blank_round_diagnostic_remains_when_aggregates_conflict(self):
        reference = dict(self.reference)
        reference["final_four_appearances"] = "2"

        _, conflicts = _accomplishment_conflicts(
            self.program,
            reference,
            self.games,
        )

        self.assertTrue(
            any(
                item.startswith("final_four_appearances:")
                for item in conflicts
            )
        )
        self.assertIn(
            "1959-1960 has no resolved NCAA round",
            conflicts,
        )


if __name__ == "__main__":
    unittest.main()
