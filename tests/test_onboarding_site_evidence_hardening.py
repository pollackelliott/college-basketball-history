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


    def test_matched_home_exception_does_not_mark_known_canonical_venue(self):
        source = {
            "source_program_key": "south-carolina",
            "source_game_id": "TEST-3",
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
            "site_research_status": "RESEARCHED_UNRESOLVED_HOME_VENUE",
            "site_research_basis": (
                "HOME and Columbia established; exact building unrecoverable."
            ),
        }
        canonical = {
            "canonical_game_id": "CBBG-TEST",
            "season_label": "1908-1909",
            "game_date": "1908-10-30",
            "date_precision": "EXACT",
            "team_a_key": "furman",
            "team_b_key": "south-carolina",
            "team_a_score": "21",
            "team_b_score": "19",
            "result_winner_team_key": "furman",
            "overtime_periods": "0",
            "site_type": "TEAM_B_HOME",
            "designated_home_team_key": "south-carolina",
            "venue_key": "known-arena",
            "venue_id": "VEN-999999",
            "site_city": "Columbia",
            "site_state": "SC",
            "game_type": "REGULAR_SEASON",
            "postseason_round": "",
            "notes": "[EXISTING_VENUE_PROVENANCE]",
        }

        candidates = ingest_school.canonical_enrichment_candidates(
            source,
            canonical,
            {},
        )
        note_values = [
            value for field, value in candidates if field == "notes"
        ]
        self.assertFalse(
            any(
                "RESEARCHED_UNRESOLVED_HOME_VENUE" in value
                for value in note_values
            )
        )



if __name__ == "__main__":
    unittest.main()
