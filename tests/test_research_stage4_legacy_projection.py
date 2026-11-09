import unittest

import research_stage4 as mod
from research_stage4_closeout import normalize_game_type


def opponent_rows(label="Old College"):
    return [
        {
            "source_program_key": "test",
            "source_opponent_label": label,
            "canonical_opponent_key": "old-college",
            "canonical_opponent_name": "Old College",
            "current_d1": "No",
            "games_with_source_label": "1",
            "first_season": "2000-2001",
            "last_season": "2000-2001",
            "resolution_status": "RESOLVED",
            "resolution_method": "ACCEPTED_STAGE2_DURABLE_IDENTITY",
            "user_choice": "",
            "audit_note": "accepted",
        }
    ]


def legacy_score_row(game_id, team, opponent, result, raw_text):
    return {
        "research_game_id": game_id,
        "season": "2000-01",
        "source_opponent_label": "Old College",
        "opponent_key": "old-college",
        "team_score": str(team),
        "opponent_score": str(opponent),
        "played_result": result,
        "raw_text": raw_text,
        "game_type": "REGULAR_SEASON",
        "site_type": "UNKNOWN",
    }


class Stage4LegacyProjectionCompatibilityTests(unittest.TestCase):
    def test_deterministic_w_reorients_unordered_accepted_pair(self):
        row = legacy_score_row("W", 60, 70, "W", "Old College 60 70 W")
        games, defects = mod._projection([row], opponent_rows(), [], school_key="test")
        self.assertEqual(defects, [])
        game = games[0]
        self.assertEqual((game["team_score"], game["opponent_score"]), ("70", "60"))
        self.assertEqual(game["played_result"], "W")
        self.assertEqual(
            sorted(map(int, (game["team_score"], game["opponent_score"]))),
            [60, 70],
        )
        self.assertIn("legacy score-orientation compatibility", game["notes"])

    def test_deterministic_l_reorients_unordered_accepted_pair(self):
        row = legacy_score_row("L", 74, 61, "L", "Old College 74 61 L")
        games, defects = mod._projection([row], opponent_rows(), [], school_key="test")
        self.assertEqual(defects, [])
        game = games[0]
        self.assertEqual((game["team_score"], game["opponent_score"]), ("61", "74"))
        self.assertEqual(game["played_result"], "L")
        self.assertEqual(
            sorted(map(int, (game["team_score"], game["opponent_score"]))),
            [61, 74],
        )

    def test_already_oriented_score_is_noop(self):
        row = legacy_score_row("NOOP", 70, 60, "W", "Old College 70 60 W")
        games, defects = mod._projection([row], opponent_rows(), [], school_key="test")
        self.assertEqual(defects, [])
        self.assertEqual(
            (games[0]["team_score"], games[0]["opponent_score"]),
            ("70", "60"),
        )
        self.assertNotIn("legacy score-orientation compatibility", games[0]["notes"])

    def test_ambiguous_or_current_schema_score_fails_closed(self):
        ambiguous = legacy_score_row(
            "AMB", 74, 61, "L", "Old College score unavailable L"
        )
        current = {
            **legacy_score_row("CURRENT", 74, 61, "L", "Old College 74 61 L"),
            "season": "",
            "season_label": "2000-2001",
            "source_program_key": "test",
        }
        games, defects = mod._projection(
            [ambiguous, current], opponent_rows(), [], school_key="test"
        )
        self.assertEqual(
            [d["reason"] for d in defects].count(
                "LEGACY_SCORE_ORIENTATION_AMBIGUOUS"
            ),
            2,
        )
        self.assertEqual(
            [(g["team_score"], g["opponent_score"]) for g in games],
            [("74", "61"), ("74", "61")],
        )
        self.assertTrue(all(g["played_result"] == "L" for g in games))

    def test_legacy_site_debt_maps_only_terminal_regular_season_shapes(self):
        cases = (
            (
                {
                    "site_type": "UNKNOWN",
                    "game_type": "REGULAR_SEASON",
                    "site_research_status":
                        "STAGE3A1_RESEARCHED_UNRESOLVED_OPPONENT_INSTITUTIONAL_0042",
                    "site_research_basis": "EXHAUSTED",
                },
                ("RESEARCHED_UNRESOLVED", "EXHAUSTED"),
            ),
            (
                {
                    "season": "1907-08",
                    "site_type": "NEUTRAL",
                    "game_type": "REGULAR_SEASON",
                    "venue_research_status":
                        "RESEARCHED_UNRESOLVED_STAGE3A3_HISTORICAL_LOCALITY",
                    "venue_research_basis": "HISTORICAL_LOCATION_PATH_EXHAUSTED",
                },
                ("RESEARCHED_UNRESOLVED", "HISTORICAL_LOCATION_PATH_EXHAUSTED"),
            ),
            (
                {
                    "season": "1998-99",
                    "site_type": "NEUTRAL",
                    "game_type": "REGULAR_SEASON",
                    "venue_city": "Hartford",
                    "venue_state": "CT",
                    "venue_research_status":
                        "RESEARCHED_UNRESOLVED_STAGE3A3_MODERN_ONEOFF_EXACT_VENUE",
                    "venue_research_basis": "MODERN_PATHS_EXHAUSTED",
                },
                ("RESEARCHED_UNRESOLVED", "MODERN_PATHS_EXHAUSTED"),
            ),
        )
        for row, expected in cases:
            with self.subTest(row=row):
                self.assertEqual(mod._research_accounting(row), expected)

        fail_closed = (
            {
                "site_type": "UNKNOWN",
                "game_type": "REGULAR_SEASON",
                "site_research_status": "STAGE3A1_ACTIVE_QUEUE_0042",
                "site_research_basis": "pending",
            },
            {
                "site_type": "UNKNOWN",
                "game_type": "NIT",
                "site_research_status": "STAGE3A1_RESEARCHED_UNRESOLVED_X",
                "site_research_basis": "EXHAUSTED",
            },
            {
                "season": "1998-99",
                "site_type": "NEUTRAL",
                "game_type": "REGULAR_SEASON",
                "venue_research_status":
                    "RESEARCHED_UNRESOLVED_STAGE3A3_MODERN_ONEOFF_EXACT_VENUE",
                "venue_research_basis": "EXHAUSTED",
            },
        )
        for row in fail_closed:
            with self.subTest(row=row):
                self.assertEqual(mod._research_accounting(row), ("", ""))

    def test_cit_projects_to_postseason_and_preserves_literal_evidence(self):
        self.assertEqual(normalize_game_type("CIT"), "POSTSEASON")
        row = {
            **legacy_score_row(
                "CIT", 66, 69, "L", "Boston University(CIT) 66 69 L"
            ),
            "source_opponent_label": "Boston University(CIT)",
            "opponent_key": "old-college",
            "game_type": "CIT",
        }
        games, defects = mod._projection(
            [row], opponent_rows("Boston University(CIT)"), [], school_key="test"
        )
        self.assertEqual(defects, [])
        game = games[0]
        self.assertEqual(game["curated_game_type"], "POSTSEASON")
        self.assertIn("CIT", game["raw_text"])
        self.assertIn("CIT", game["source_opponent_label"])
        self.assertEqual(game["played_result"], "L")


def durable_stage3b_row(
    game_id="DURABLE",
    *,
    points_for="58",
    points_against="65",
    result="L",
):
    return {
        "research_game_id": game_id,
        "source_program_key": "test",
        "season_label": "2012-2013",
        "game_date": "2012-11-24",
        "source_opponent_label": "Old College",
        "opponent_key": "old-college",
        "source_points_for": points_for,
        "source_points_against": points_against,
        "played_result": result,
        "source_overtime_token": "2OT",
        "source_venue_token": "RC",
        "source_entry_literal": "Nov. 24 vs Old College& L 65-58 2OT",
        "game_type": "REGULAR_SEASON",
        "site_type": "NEUTRAL",
    }


class Stage4DurableStage3BSchemaCompatibilityTests(unittest.TestCase):
    def test_current_durable_aliases_project_without_semantic_loss(self):
        row = durable_stage3b_row()
        games, defects = mod._projection(
            [row],
            opponent_rows(),
            [],
            school_key="test",
        )

        self.assertEqual(defects, [])
        self.assertEqual(len(games), 1)
        game = games[0]
        self.assertEqual(game["team_score"], "58")
        self.assertEqual(game["opponent_score"], "65")
        self.assertEqual(game["played_result"], "L")
        self.assertEqual(game["overtime_periods"], "2")
        self.assertEqual(game["source_venue_name"], "RC")
        self.assertEqual(
            game["raw_text"],
            "Nov. 24 vs Old College& L 65-58 2OT",
        )
        self.assertEqual(game["curated_venue_name"], "")

    def test_preflight_anti_loss_checks_current_durable_aliases(self):
        row = durable_stage3b_row()
        games, defects = mod._projection(
            [row],
            opponent_rows(),
            [],
            school_key="test",
        )
        self.assertEqual(defects, [])
        projected = dict(games[0])

        expected_fields = {
            "team_score",
            "opponent_score",
            "overtime_periods",
            "source_venue_name",
            "raw_text",
        }
        for field in expected_fields:
            with self.subTest(field=field):
                candidate = dict(projected)
                candidate[field] = ""
                losses = mod._semantic_projection_defects(row, candidate)
                self.assertIn(
                    field,
                    {
                        item["field"]
                        for item in losses
                        if item["reason"] == "ACCEPTED_SOURCE_FIELD_LOST"
                    },
                )

    def test_current_schema_score_result_inconsistency_fails_closed(self):
        row = durable_stage3b_row(
            game_id="BAD-CURRENT",
            points_for="65",
            points_against="58",
            result="L",
        )
        games, defects = mod._projection(
            [row],
            opponent_rows(),
            [],
            school_key="test",
        )

        self.assertEqual(
            [item["reason"] for item in defects],
            ["LEGACY_SCORE_ORIENTATION_AMBIGUOUS"],
        )
        self.assertEqual(
            (games[0]["team_score"], games[0]["opponent_score"]),
            ("65", "58"),
        )
        self.assertEqual(games[0]["played_result"], "L")

    def test_corrected_current_schema_score_result_projects_normally(self):
        row = durable_stage3b_row(
            game_id="CORRECTED-CURRENT",
            points_for="58",
            points_against="65",
            result="L",
        )
        games, defects = mod._projection(
            [row],
            opponent_rows(),
            [],
            school_key="test",
        )

        self.assertEqual(defects, [])
        self.assertEqual(
            (games[0]["team_score"], games[0]["opponent_score"]),
            ("58", "65"),
        )
        self.assertEqual(games[0]["played_result"], "L")


if __name__ == "__main__":
    unittest.main()
