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


class Stage4DurableOpponentSchemaCompatibilityTests(unittest.TestCase):
    @staticmethod
    def _gw_style_row():
        return {
            "research_game_id": "GW-DURABLE-OPPONENT",
            "source_program_key": "george-washington",
            "season_label": "2000-2001",
            "game_date": "2001-01-15",
            "source_opponent_literal": "Old College",
            "stage2_opponent_key": "old-college",
            "team_score": "70",
            "opponent_score": "60",
            "played_result": "W",
            "game_type": "REGULAR_SEASON",
            "site_type": "HOME",
        }

    def test_stage2_key_and_literal_source_label_project_exactly(self):
        row = self._gw_style_row()
        games, defects = mod._projection(
            [row],
            opponent_rows(),
            [],
            school_key="george-washington",
        )

        self.assertEqual(defects, [])
        self.assertEqual(len(games), 1)
        game = games[0]
        self.assertEqual(game["normalized_opponent_key"], "old-college")
        self.assertEqual(game["normalized_opponent_name"], "Old College")
        self.assertEqual(game["source_opponent_label"], "Old College")
        self.assertEqual(
            mod._mapping_defects(games, opponent_rows()),
            [],
        )

    def test_literal_label_key_pair_still_must_exist_in_opponents_capsule(self):
        row = self._gw_style_row()
        games, defects = mod._projection(
            [row],
            opponent_rows("Different Literal"),
            [],
            school_key="george-washington",
        )

        self.assertEqual(defects, [])
        mapping = mod._mapping_defects(
            games,
            opponent_rows("Different Literal"),
        )
        self.assertEqual(
            [item["reason"] for item in mapping],
            ["SOURCE_LABEL_OPPONENT_MAPPING_MISSING"],
        )
        self.assertEqual(mapping[0]["source_opponent_label"], "Old College")
        self.assertEqual(mapping[0]["canonical_opponent_key"], "old-college")

    def test_durable_opponent_aliases_are_in_semantic_anti_loss_guard(self):
        row = self._gw_style_row()
        games, defects = mod._projection(
            [row],
            opponent_rows(),
            [],
            school_key="george-washington",
        )
        self.assertEqual(defects, [])
        projected = dict(games[0])

        for field in ("source_opponent_label", "normalized_opponent_key"):
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


class Stage4LegacyBaseLabelOpponentCompatibilityTests(unittest.TestCase):
    @staticmethod
    def _opponent(label="Fordham", key="fordham", name="Fordham"):
        return {
            "source_program_key": "george-washington",
            "source_opponent_label": label,
            "canonical_opponent_key": key,
            "canonical_opponent_name": name,
            "current_d1": "Yes",
            "games_with_source_label": "10",
            "first_season": "1935-36",
            "last_season": "1945-46",
            "resolution_status": "RESOLVED",
            "resolution_method": "ACCEPTED_STAGE2_DURABLE_IDENTITY",
            "user_choice": "",
            "audit_note": "Literal source variants remain preserved on game rows.",
        }

    @staticmethod
    def _ledger(
        game_id,
        literal,
        *,
        season="1940-41",
        base="Fordham",
        stage2_key="fordham",
        normalized_key="",
    ):
        row = {
            "research_game_id": game_id,
            "source_program_key": "george-washington",
            "season_label": season,
            "game_date": "1941-01-01",
            "source_opponent_literal": literal,
            "stage2_opponent_base_label": base,
            "stage2_opponent_key": stage2_key,
            "team_score": "70",
            "opponent_score": "60",
            "played_result": "W",
            "game_type": "REGULAR_SEASON",
            "site_type": "HOME",
        }
        if normalized_key:
            row["normalized_opponent_key"] = normalized_key
        return row

    def test_decorated_literals_materialize_package_ready_mappings_without_rewriting_literal(self):
        ledger = [
            self._ledger("PREFIX", "at Fordham", season="1940-41"),
            self._ledger("SUFFIX-A", "Fordham*", season="1941-42"),
            self._ledger("SUFFIX-B", "Fordham*", season="1942-43"),
            self._ledger("BOTH", "vs. Fordham 2", season="1943-44"),
        ]
        opponents = [self._opponent()]
        games, projection_defects = mod._projection(
            ledger,
            opponents,
            [],
            school_key="george-washington",
        )
        self.assertEqual(projection_defects, [])

        package_opponents, defects, summary = mod._project_package_opponents(
            ledger,
            games,
            opponents,
        )
        self.assertEqual(defects, [])
        self.assertEqual(summary["authoring_opponent_rows"], 1)
        self.assertEqual(summary["package_opponent_rows"], 4)
        self.assertEqual(summary["legacy_literal_mapping_rows_added"], 3)
        self.assertEqual(mod._mapping_defects(games, package_opponents), [])

        games_by_id = {row["source_game_id"]: row for row in games}
        self.assertEqual(games_by_id["PREFIX"]["source_opponent_label"], "at Fordham")
        self.assertEqual(games_by_id["SUFFIX-A"]["source_opponent_label"], "Fordham*")
        self.assertEqual(games_by_id["BOTH"]["source_opponent_label"], "vs. Fordham 2")

        mappings = {
            (row["source_opponent_label"], row["canonical_opponent_key"]): row
            for row in package_opponents
        }
        self.assertEqual(mappings[("at Fordham", "fordham")]["canonical_opponent_name"], "Fordham")
        self.assertEqual(mappings[("at Fordham", "fordham")]["current_d1"], "Yes")
        self.assertEqual(
            mappings[("at Fordham", "fordham")]["resolution_method"],
            "ACCEPTED_STAGE2_DURABLE_IDENTITY",
        )
        suffix = mappings[("Fordham*", "fordham")]
        self.assertEqual(suffix["games_with_source_label"], "2")
        self.assertEqual(suffix["first_season"], "1941-42")
        self.assertEqual(suffix["last_season"], "1942-43")

    def test_exact_literal_mapping_is_not_duplicated(self):
        ledger = [self._ledger("EXACT", "Fordham")]
        opponents = [self._opponent()]
        games, projection_defects = mod._projection(
            ledger,
            opponents,
            [],
            school_key="george-washington",
        )
        self.assertEqual(projection_defects, [])
        package_opponents, defects, summary = mod._project_package_opponents(
            ledger,
            games,
            opponents,
        )
        self.assertEqual(defects, [])
        self.assertEqual(package_opponents, opponents)
        self.assertEqual(summary["legacy_literal_mapping_rows_added"], 0)

    def test_missing_base_mapping_fails_closed(self):
        ledger = [self._ledger("MISS", "at Fordham")]
        opponents = [self._opponent(label="Different")]
        games, projection_defects = mod._projection(
            ledger,
            opponents,
            [],
            school_key="george-washington",
        )
        self.assertEqual(projection_defects, [])
        _, defects, _ = mod._project_package_opponents(
            ledger,
            games,
            opponents,
        )
        self.assertIn(
            "LEGACY_STAGE2_BASE_LABEL_KEY_AMBIGUOUS",
            {item["reason"] for item in defects},
        )

    def test_base_label_mapping_ambiguous_across_keys_fails_closed(self):
        ledger = [self._ledger("AMB", "at Fordham")]
        opponents = [
            self._opponent(),
            self._opponent(label="Fordham", key="fordham-state", name="Fordham State"),
        ]
        games, projection_defects = mod._projection(
            ledger,
            opponents,
            [],
            school_key="george-washington",
        )
        self.assertEqual(projection_defects, [])
        _, defects, _ = mod._project_package_opponents(
            ledger,
            games,
            opponents,
        )
        self.assertIn(
            "LEGACY_STAGE2_BASE_LABEL_KEY_AMBIGUOUS",
            {item["reason"] for item in defects},
        )

    def test_stage2_key_conflict_with_projected_key_fails_closed(self):
        ledger = [
            self._ledger(
                "KEY-CONFLICT",
                "at Fordham",
                normalized_key="different-key",
            )
        ]
        opponents = [
            self._opponent(),
            self._opponent(label="Different", key="different-key", name="Different"),
        ]
        games, projection_defects = mod._projection(
            ledger,
            opponents,
            [],
            school_key="george-washington",
        )
        self.assertEqual(projection_defects, [])
        _, defects, _ = mod._project_package_opponents(
            ledger,
            games,
            opponents,
        )
        self.assertIn(
            "LEGACY_STAGE2_OPPONENT_KEY_CONFLICT",
            {item["reason"] for item in defects},
        )

    def test_current_schema_missing_literal_mapping_remains_fail_closed(self):
        ledger = [
            {
                "research_game_id": "CURRENT",
                "source_program_key": "test",
                "season_label": "2020-21",
                "game_date": "2021-01-01",
                "source_opponent_label": "Decorated Old College",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "game_type": "REGULAR_SEASON",
                "site_type": "HOME",
            }
        ]
        opponents = opponent_rows("Old College")
        games, projection_defects = mod._projection(
            ledger,
            opponents,
            [],
            school_key="test",
        )
        self.assertEqual(projection_defects, [])
        package_opponents, defects, summary = mod._project_package_opponents(
            ledger,
            games,
            opponents,
        )
        self.assertEqual(defects, [])
        self.assertEqual(summary["legacy_literal_mapping_rows_added"], 0)
        self.assertEqual(
            [item["reason"] for item in mod._mapping_defects(games, package_opponents)],
            ["SOURCE_LABEL_OPPONENT_MAPPING_MISSING"],
        )


if __name__ == "__main__":
    unittest.main()
