import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ingest_school


class SiteEvidenceHardeningTests(unittest.TestCase):

    def test_known_source_site_vs_unknown_canonical_is_discrepancy(self):
        source = {
            "source_program_key": "south-carolina",
            "source_game_id": "TEST-1",
            "normalized_opponent_key": "alabama",
            "curated_site_type": "OPPONENT_HOME",
            "game_date": "2022-02-26",
            "team_score": "",
            "opponent_score": "",
            "played_result": "",
            "overtime_periods": "",
            "curated_game_type": "REGULAR_SEASON",
            "curated_postseason_round": "",
        }
        canonical = {
            "game_date": "2022-02-26",
            "team_a_key": "alabama",
            "team_b_key": "south-carolina",
            "team_a_score": "",
            "team_b_score": "",
            "result_winner_team_key": "",
            "overtime_periods": "",
            "site_type": "UNKNOWN",
            "game_type": "REGULAR_SEASON",
            "postseason_round": "",
        }
        self.assertIn(
            ("site_type", "TEAM_A_HOME", "UNKNOWN"),
            ingest_school.discrepancy_candidates(source, canonical),
        )

    def test_new_home_exception_gets_canonical_marker(self):
        source = {
            "source_program_key": "south-carolina",
            "source_game_id": "TEST-2",
            "normalized_opponent_key": "furman",
            "season_label": "1908-1909",
            "game_date": "1908-10-30",
            "team_score": "19",
            "opponent_score": "21",
            "played_result": "L",
            "overtime_periods": "0",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "",
            "city": "Columbia",
            "state": "SC",
            "curated_game_type": "REGULAR_SEASON",
            "curated_postseason_round": "",
            "administrative_status": "",
            "administrative_note": "",
            "site_research_status": "RESEARCHED_UNRESOLVED_HOME_VENUE",
            "site_research_basis": "HOME and Columbia established; exact building unrecoverable.",
        }
        game = ingest_school.build_new_canonical(
            source, "CBBG-TEST", {}, {}
        )
        self.assertIn(
            "[RESEARCHED_UNRESOLVED_HOME_VENUE "
            "source=south-carolina/TEST-2]",
            game["notes"],
        )
        self.assertEqual((game["site_city"], game["site_state"]), ("Columbia", "SC"))
        self.assertFalse(game["venue_id"])


if __name__ == "__main__":
    unittest.main()
