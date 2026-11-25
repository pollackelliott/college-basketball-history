"""Generic regressions for frozen expansion Stage 1 identity reconciliation.

The synthetic score/date topologies reproduce the bounded Hawai‘i intake
blocker. These tests never change Research Freeze or canonical basketball data.
"""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from expansion_implementation_stage1 import reconcile_canonical


def source(game_id, season, date, opponent, team, opp, site="SOURCE_PROGRAM_HOME"):
    return {
        "source_game_id": game_id,
        "source_program_key": "island",
        "season_label": season,
        "normalized_opponent_key": opponent,
        "game_date": date,
        "team_score": str(team),
        "opponent_score": str(opp),
        "curated_site_type": site,
        "curated_game_type": "REGULAR_SEASON",
        "played_result": "W" if team > opp else "L",
    }


def canonical(game_id, season, date, opponent, team, opp, home):
    # All synthetic opponent keys sort after "island".
    return {
        "canonical_game_id": game_id,
        "season_label": season,
        "team_a_key": "island",
        "team_b_key": opponent,
        "team_a_score": str(team),
        "team_b_score": str(opp),
        "game_date": date,
        "date_precision": "EXACT" if date else "SEASON",
        "site_type": "TEAM_A_HOME" if home == "island" else "TEAM_B_HOME",
        "designated_home_team_key": home,
        "game_type": "REGULAR_SEASON",
    }


class ExpansionStage1IdentityTiebreakTests(unittest.TestCase):
    def test_two_games_one_day_source_shift_do_not_reuse_one_canonical(self):
        src = [
            source("S-1", "1959-1960", "1960-02-10", "north", 62, 64),
            source("S-2", "1959-1960", "1960-02-12", "north", 64, 74),
        ]
        can = [
            canonical("C-1", "1959-1960", "1960-02-12", "north", 62, 64, "island"),
            canonical("C-2", "1959-1960", "1960-02-13", "north", 64, 74, "island"),
        ]
        result = reconcile_canonical("island", src, can)
        self.assertEqual(result["counts"]["REUSE_CANONICAL"], 2)
        self.assertEqual(result["duplicate_canonical_reuse"], {})
        self.assertEqual([r["canonical_game_id"] for r in result["game_rows"]], ["C-1", "C-2"])
        self.assertEqual(result["game_rows"][1]["match_method"],
                         "UNIQUE_PAIR_SEASON_SCORE_OVERRIDES_CONFLICTING_EXACT_DATE")
        self.assertEqual(result["game_rows"][0]["field_disagreements"], ["date"])
        self.assertEqual(result["game_rows"][1]["field_disagreements"], ["date"])

    def test_unique_partial_score_plus_same_explicit_home_preserves_conflict(self):
        specimens = [
            (
                source("OLD-1", "1937-1938", "", "north", 24, 76),
                [canonical("N-1", "1937-1938", "", "north", 25, 76, "island")],
                "N-1",
            ),
            (
                source("OLD-2", "1952-1953", "1953-01-24", "west", 70, 59),
                [canonical("W-1", "1952-1953", "", "west", 70, 58, "island")],
                "W-1",
            ),
            (
                source("OLD-3", "1954-1955", "", "west", 58, 85, "OPPONENT_HOME"),
                [
                    canonical("W-2", "1954-1955", "", "west", 55, 85, "west"),
                    canonical("W-3", "1954-1955", "", "west", 51, 71, "island"),
                    canonical("W-4", "1954-1955", "", "west", 51, 58, "island"),
                ],
                "W-2",
            ),
        ]
        for src, can, expected in specimens:
            with self.subTest(source_game_id=src["source_game_id"]):
                result = reconcile_canonical("island", [src], can)
                row = result["game_rows"][0]
                self.assertEqual(row["classification"], "REUSE_CANONICAL")
                self.assertEqual(row["canonical_game_id"], expected)
                self.assertIn("score", row["field_disagreements"])
                self.assertEqual(row["match_method"], "UNIQUE_PAIR_SEASON_PARTIAL_SCORE_AND_HOME")

    def test_later_home_series_is_not_confused_with_earlier_away_series(self):
        src = [
            source("U-1", "1958-1959", "1959-01-28", "west", 60, 56),
            source("U-2", "1958-1959", "1959-01-30", "west", 74, 87),
            source("U-3", "1959-1960", "1960-01-27", "west", 61, 69),
            source("U-4", "1959-1960", "1960-01-29", "west", 59, 69),
        ]
        can = [
            canonical("W-1", "1958-1959", "1958-12-16", "west", 56, 76, "west"),
            canonical("W-2", "1958-1959", "1958-12-17", "west", 42, 72, "west"),
            canonical("W-3", "1959-1960", "1959-12-22", "west", 43, 91, "west"),
            canonical("W-4", "1959-1960", "1959-12-23", "west", 49, 73, "west"),
        ]
        result = reconcile_canonical("island", src, can)
        self.assertEqual(result["counts"]["PROVISIONAL_NEW_CANONICAL"], 4)
        self.assertEqual(result["counts"]["IDENTITY_REVIEW_BLOCKER"], 0)
        for row in result["game_rows"]:
            self.assertEqual(row["match_method"], "DISTINCT_EXACT_DATES_HOME_SIDES_AND_SCORES")
            self.assertEqual(row["canonical_game_id"], "")

    def test_no_inference_when_site_unknown_date_near_or_partial_score_nonunique(self):
        src = source("S-1", "1958-1959", "1959-01-28", "west", 60, 56)
        near = canonical("C-NEAR", "1958-1959", "1959-01-26", "west", 42, 72, "west")
        same_site = canonical("C-SAME", "1958-1959", "1958-12-16", "west", 42, 72, "island")
        unknown = {**same_site, "canonical_game_id": "C-UNKNOWN", "site_type": "UNKNOWN",
                   "designated_home_team_key": ""}
        for candidates in ([near], [same_site], [unknown]):
            with self.subTest(candidates=candidates):
                result = reconcile_canonical("island", [src], candidates)
                self.assertEqual(result["counts"]["IDENTITY_REVIEW_BLOCKER"], 1)
        partial = source("S-2", "1954-1955", "", "west", 58, 85, "OPPONENT_HOME")
        double = [
            canonical("C-1", "1954-1955", "", "west", 55, 85, "west"),
            canonical("C-2", "1954-1955", "", "west", 54, 85, "west"),
        ]
        result = reconcile_canonical("island", [partial], double)
        self.assertEqual(result["counts"]["IDENTITY_REVIEW_BLOCKER"], 1)


if __name__ == "__main__":
    unittest.main()
