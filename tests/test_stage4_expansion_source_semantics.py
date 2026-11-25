"""Fail-closed accepted Stage 3B expansion source-field preservation."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import research_stage4 as author
from research_stage4_closeout import accepted_source_date_iso, compare_parent_semantics


class ExpansionSourceFieldPreservationTests(unittest.TestCase):
    def source_row(self, **updates):
        row = {
            "research_game_id": "EXP-2003-04-001",
            "source_program_key": "uc-davis",
            "season_label": "2003-2004",
            "source_opponent_label": "Opp A",
            "stage2_opponent_key": "opp-a",
            "on_court_result": "W",
            "source_score_for": "73",
            "source_score_against": "65",
            "source_result_text": "W, 73-65",
            "source_date": "12/8/03",
            "overtime_text": "2OT",
            "source_postseason_text": "NCAA Division II",
            "stage3b_event_or_tournament": "NCAA Division II West Regional",
            "game_type": "POSTSEASON",
            "stage3b_site_type": "NEUTRAL",
            "stage3b_physical_venue_name": "Hall A",
            "stage3b_venue_city": "Town",
            "stage3b_venue_state": "CA",
        }
        row.update(updates)
        return row

    def project(self, source):
        opponents = [{"canonical_opponent_key": "opp-a",
                      "canonical_opponent_name": "Opp A"}]
        games, defects = author._projection([source], opponents, [],
                                            school_key="uc-davis")
        self.assertEqual(defects, [])
        return games[0]

    def test_accepted_expansion_source_fields_survive(self):
        source = self.source_row()
        game = self.project(source)
        self.assertEqual(game["game_date"], "2003-12-08")
        self.assertEqual((game["team_score"], game["opponent_score"]),
                         ("73", "65"))
        self.assertEqual(game["overtime_periods"], "2")
        self.assertEqual(game["raw_text"], "W, 73-65")
        self.assertEqual(game["event_or_tournament"],
                         "NCAA Division II West Regional")
        self.assertIn("NCAA Division II", game["notes"])
        self.assertEqual(compare_parent_semantics([source], [game], [],
                         school_key="uc-davis"), [])

    def test_parent_comparator_rejects_dropped_semantics(self):
        source = self.source_row()
        game = self.project(source)
        for key in ("game_date", "team_score", "opponent_score",
                    "overtime_periods", "raw_text"):
            damaged = dict(game)
            damaged[key] = ""
            mismatches = compare_parent_semantics([source], [damaged], [],
                                                  school_key="uc-davis")
            self.assertIn(key, {m.get("field") for m in mismatches}, key)

    def test_source_date_requires_explicit_matching_season_year(self):
        source = self.source_row(source_date="12/8/01")
        self.assertEqual(accepted_source_date_iso(source), "")
        game = self.project(source)
        self.assertEqual(game["game_date"], "")
        self.assertIn("source_date='12/8/01'", game["notes"])

    def test_source_date_century_boundary_and_prewar(self):
        self.assertEqual(accepted_source_date_iso(self.source_row(
            season_label="1999-2000", source_date="1/3/00")), "2000-01-03")
        self.assertEqual(accepted_source_date_iso(self.source_row(
            season_label="1936-1937", source_date="12/8/36")), "1936-12-08")

    def test_current_schema_populated_values_retain_precedence(self):
        source = self.source_row(team_score="73", opponent_score="65",
                                 game_date="2003-12-08",
                                 raw_text="full original source line",
                                 overtime_periods="2")
        game = self.project(source)
        self.assertEqual(game["raw_text"], "full original source line")
        self.assertEqual((game["team_score"], game["opponent_score"]),
                         ("73", "65"))
        self.assertEqual(game["game_date"], "2003-12-08")


if __name__ == "__main__":
    unittest.main()
