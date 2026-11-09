import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import research_stage4 as author
from onboarding_hardening import refresh_venue_assignment_summaries
from onboarding_plan import WorkflowError
from research_stage4_closeout import (
    compare_parent_semantics,
    project_administrative_status,
)


class Stage4HawaiiLegacyCompatibilityTests(unittest.TestCase):
    def legacy_row(self, **overrides):
        row = {
            "research_game_id": "hawai-i-test-001",
            "season": "1973-74",
            "game_date": "1973-12-29",
            "source_opponent_literal": "Purdue(forfeit)!",
            "stage2_opponent_key": "purdue",
            "stage2_opponent_name": "Purdue",
            "score_for": "76",
            "score_against": "67",
            "on_court_result": "W",
            "source_raw_line": "D 29 Purdue(forfeit)! W 76-67",
            "site_type": "HOME",
            "game_type": "REGULAR_SEASON",
            "stage3a_final_site_type": "SOURCE_PROGRAM_HOME",
            "stage3a_final_physical_venue_name": "Test Arena",
            "stage3a_final_city": "Honolulu",
            "stage3a_final_state": "HI",
            "administrative_status": "",
        }
        row.update(overrides)
        return row

    def opponents(self):
        return [{
            "source_opponent_label": "Purdue(forfeit)!",
            "canonical_opponent_key": "purdue",
            "canonical_opponent_name": "Purdue",
            "current_d1": "Yes",
        }]

    def test_hawaii_aliases_project_without_loss(self):
        row = self.legacy_row()
        games, defects = author._projection(
            [row], self.opponents(), [], school_key="hawai-i"
        )
        self.assertEqual(defects, [])
        game = games[0]
        self.assertEqual(game["team_score"], "76")
        self.assertEqual(game["opponent_score"], "67")
        self.assertEqual(game["raw_text"], row["source_raw_line"])
        self.assertEqual(
            compare_parent_semantics([row], games, [], school_key="hawai-i"),
            [],
        )

    def test_current_schema_fields_keep_precedence(self):
        row = self.legacy_row(
            source_game_id="CURRENT-1",
            source_program_key="hawai-i",
            season_label="1973-1974",
            team_score="80",
            opponent_score="70",
            raw_text="CURRENT LITERAL",
            score_for="76",
            score_against="67",
            source_raw_line="LEGACY LITERAL",
        )
        games, defects = author._projection(
            [row], self.opponents(), [], school_key="hawai-i"
        )
        self.assertEqual(defects, [])
        self.assertEqual(games[0]["team_score"], "80")
        self.assertEqual(games[0]["opponent_score"], "70")
        self.assertEqual(games[0]["raw_text"], "CURRENT LITERAL")

    def test_hawaii_forfeited_after_play_projects_to_forfeit_with_score_note(self):
        row = self.legacy_row(administrative_status="FORFEITED_AFTER_PLAY")
        status, note = project_administrative_status(row)
        self.assertEqual(status, "FORFEIT")
        self.assertIn("played_result=W", note)
        self.assertIn("score=76-67", note)
        games, defects = author._projection(
            [row], self.opponents(), [], school_key="hawai-i"
        )
        self.assertEqual(defects, [])
        self.assertEqual(games[0]["administrative_status"], "FORFEIT")
        self.assertIn("76-67", games[0]["administrative_note"])
        self.assertEqual(games[0]["team_score"], "76")
        self.assertEqual(games[0]["opponent_score"], "67")
        self.assertEqual(games[0]["played_result"], "W")
        self.assertEqual(
            compare_parent_semantics([row], games, [], school_key="hawai-i"),
            [],
        )

    def test_legacy_vacated_win_gets_deterministic_note_only_for_legacy_shape(self):
        row = self.legacy_row(administrative_status="VACATED_WIN")
        status, note = project_administrative_status(row)
        self.assertEqual(status, "VACATED_WIN")
        self.assertIn("accepted legacy administrative_status VACATED_WIN retained", note)
        self.assertIn("played_result=W", note)

        current = dict(row)
        current.update(
            source_game_id="CURRENT-2",
            source_program_key="hawai-i",
            season_label="1973-1974",
        )
        current.pop("research_game_id", None)
        current.pop("season", None)
        self.assertEqual(
            project_administrative_status(current),
            ("VACATED_WIN", ""),
        )

    def test_venue_summary_refresh_changes_only_derived_fields(self):
        venues = [{
            "source_program_key": "hawai-i",
            "venue_key": "test-arena",
            "venue_id": "",
            "canonical_name": "Test Arena",
            "aliases": "Old Test Arena",
            "city": "Honolulu",
            "state": "HI",
            "venue_type": "arena",
            "known_opened": "1970",
            "known_closed": "",
            "venue_date_precision": "YEAR",
            "games_currently_assigned": "1",
            "first_assigned_game": "2000-01-02",
            "last_assigned_game": "2000-01-02",
            "relationship_type": "HOME",
            "relationship_start": "1970-01-01",
            "relationship_end": "",
            "relationship_date_precision": "DAY",
            "site_rule": "test",
            "source_basis": "accepted basis",
            "notes": "accepted notes",
        }]
        games = [
            {
                "source_game_id": "G1",
                "curated_venue_name": "Test Arena",
                "city": "Honolulu",
                "state": "HI",
                "game_date": "1999-12-01",
                "curated_site_type": "NEUTRAL",
            },
            {
                "source_game_id": "G2",
                "curated_venue_name": "Old Test Arena",
                "city": "Honolulu",
                "state": "HI",
                "game_date": "2001-03-02",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
            },
        ]
        refreshed, report = refresh_venue_assignment_summaries(games, venues)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(refreshed[0]["games_currently_assigned"], "2")
        self.assertEqual(refreshed[0]["first_assigned_game"], "1999-12-01")
        self.assertEqual(refreshed[0]["last_assigned_game"], "2001-03-02")
        derived = {
            "games_currently_assigned",
            "first_assigned_game",
            "last_assigned_game",
        }
        for key, value in venues[0].items():
            if key not in derived:
                self.assertEqual(refreshed[0][key], value)

    def test_venue_summary_refresh_fails_closed_on_ambiguous_local_alias(self):
        venues = [
            {
                "venue_key": "arena-a",
                "canonical_name": "Arena A",
                "aliases": "Shared Arena",
                "city": "Example",
                "state": "TX",
                "games_currently_assigned": "0",
                "first_assigned_game": "",
                "last_assigned_game": "",
            },
            {
                "venue_key": "arena-b",
                "canonical_name": "Arena B",
                "aliases": "Shared Arena",
                "city": "Example",
                "state": "TX",
                "games_currently_assigned": "0",
                "first_assigned_game": "",
                "last_assigned_game": "",
            },
        ]
        games = [{
            "source_game_id": "G1",
            "curated_venue_name": "Shared Arena",
            "city": "Example",
            "state": "TX",
            "game_date": "2000-01-01",
        }]
        with self.assertRaisesRegex(WorkflowError, "ambiguous venue/locality"):
            refresh_venue_assignment_summaries(games, venues)


if __name__ == "__main__":
    unittest.main()
