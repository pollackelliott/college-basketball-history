import unittest

import research_stage4_closeout as mod


def legacy_parent(team, opponent, result, raw_text):
    return {
        "research_game_id": "G1",
        "season": "2000-01",
        "team_score": str(team),
        "opponent_score": str(opponent),
        "played_result": result,
        "raw_text": raw_text,
        "opponent_key": "old-college",
        "game_type": "REGULAR_SEASON",
        "stage3a_final_han": "UNKNOWN",
    }


def current_parent(team, opponent, result, raw_text):
    return {
        "research_game_id": "G1",
        "source_program_key": "test",
        "season_label": "2000-2001",
        "team_score": str(team),
        "opponent_score": str(opponent),
        "played_result": result,
        "raw_text": raw_text,
        "opponent_key": "old-college",
        "game_type": "REGULAR_SEASON",
        "stage3a_final_han": "UNKNOWN",
    }


def package_row(team, opponent, result, raw_text):
    return {
        "source_game_id": "G1",
        "source_program_key": "test",
        "season_label": "2000-2001",
        "game_date": "",
        "normalized_opponent_key": "old-college",
        "team_score": str(team),
        "opponent_score": str(opponent),
        "played_result": result,
        "overtime_periods": "",
        "curated_site_type": "UNKNOWN",
        "curated_venue_name": "",
        "city": "",
        "state": "",
        "country": "",
        "curated_game_type": "REGULAR_SEASON",
        "raw_text": raw_text,
    }


class Stage4CloseoutLegacyScoreCompatibilityTests(unittest.TestCase):
    def test_deterministic_legacy_win_orientation_is_semantically_equivalent(self):
        parent = [legacy_parent(60, 70, "W", "Old College 60 70 W")]
        package = [package_row(70, 60, "W", "Old College 60 70 W")]
        self.assertEqual(
            mod.compare_parent_semantics(parent, package, [], school_key="test"),
            [],
        )

    def test_deterministic_legacy_loss_orientation_is_semantically_equivalent(self):
        parent = [legacy_parent(74, 61, "L", "Old College 74 61 L")]
        package = [package_row(61, 74, "L", "Old College 74 61 L")]
        self.assertEqual(
            mod.compare_parent_semantics(parent, package, [], school_key="test"),
            [],
        )

    def test_already_correct_orientation_remains_noop(self):
        parent = [legacy_parent(70, 60, "W", "Old College 70 60 W")]
        package = [package_row(70, 60, "W", "Old College 70 60 W")]
        self.assertEqual(
            mod.compare_parent_semantics(parent, package, [], school_key="test"),
            [],
        )

    def test_ambiguous_literal_fails_closed(self):
        parent = [legacy_parent(74, 61, "L", "Old College score unavailable L")]
        package = [package_row(61, 74, "L", "Old College score unavailable L")]
        mismatches = mod.compare_parent_semantics(
            parent, package, [], school_key="test"
        )
        self.assertEqual(
            {item["field"] for item in mismatches},
            {"team_score", "opponent_score"},
        )

    def test_current_schema_conflict_fails_closed(self):
        parent = [current_parent(74, 61, "L", "Old College 74 61 L")]
        package = [package_row(61, 74, "L", "Old College 74 61 L")]
        mismatches = mod.compare_parent_semantics(
            parent, package, [], school_key="test"
        )
        self.assertEqual(
            {item["field"] for item in mismatches},
            {"team_score", "opponent_score"},
        )

    def test_changed_numeric_pair_fails_closed(self):
        parent = [legacy_parent(74, 61, "L", "Old College 74 61 L")]
        package = [package_row(61, 75, "L", "Old College 74 61 L")]
        mismatches = mod.compare_parent_semantics(
            parent, package, [], school_key="test"
        )
        self.assertEqual(
            {item["field"] for item in mismatches},
            {"team_score", "opponent_score"},
        )

    def test_changed_result_remains_strict(self):
        parent = [legacy_parent(74, 61, "L", "Old College 74 61 L")]
        package = [package_row(61, 74, "W", "Old College 74 61 L")]
        mismatches = mod.compare_parent_semantics(
            parent, package, [], school_key="test"
        )
        self.assertEqual(
            {item["field"] for item in mismatches},
            {"team_score", "opponent_score", "played_result"},
        )


def durable_parent(
    points_for="58",
    points_against="65",
    result="L",
):
    return {
        "research_game_id": "DURABLE",
        "source_program_key": "test",
        "season_label": "2012-2013",
        "game_date": "2012-11-24",
        "opponent_key": "old-college",
        "source_points_for": points_for,
        "source_points_against": points_against,
        "played_result": result,
        "source_overtime_token": "2OT",
        "source_venue_token": "RC",
        "source_entry_literal": "Nov. 24 vs Old College& L 65-58 2OT",
        "game_type": "REGULAR_SEASON",
        "stage3a_final_han": "NEUTRAL",
    }


def durable_package(
    team="58",
    opponent="65",
    result="L",
    *,
    overtime="2",
    source_venue_name="RC",
    raw_text="Nov. 24 vs Old College& L 65-58 2OT",
):
    row = package_row(team, opponent, result, raw_text)
    row.update(
        {
            "source_game_id": "DURABLE",
            "season_label": "2012-2013",
            "game_date": "2012-11-24",
            "overtime_periods": overtime,
            "source_venue_name": source_venue_name,
            "curated_site_type": "NEUTRAL",
        }
    )
    return row


class Stage4CloseoutDurableSchemaCompatibilityTests(unittest.TestCase):
    def test_durable_parent_aliases_are_semantically_preserved(self):
        self.assertEqual(
            mod.compare_parent_semantics(
                [durable_parent()],
                [durable_package()],
                [],
                school_key="test",
            ),
            [],
        )

    def test_durable_parent_alias_losses_are_all_detected(self):
        cases = {
            "team_score": durable_package(team=""),
            "opponent_score": durable_package(opponent=""),
            "overtime_periods": durable_package(overtime=""),
            "source_venue_name": durable_package(source_venue_name=""),
            "raw_text": durable_package(raw_text=""),
        }
        for field, package in cases.items():
            with self.subTest(field=field):
                mismatches = mod.compare_parent_semantics(
                    [durable_parent()],
                    [package],
                    [],
                    school_key="test",
                )
                self.assertIn(field, {item["field"] for item in mismatches})

    def test_current_schema_inconsistent_score_is_not_legacy_equivalent(self):
        parent = durable_parent(points_for="65", points_against="58", result="L")
        package = durable_package(team="58", opponent="65", result="L")
        mismatches = mod.compare_parent_semantics(
            [parent],
            [package],
            [],
            school_key="test",
        )
        self.assertEqual(
            {item["field"] for item in mismatches},
            {"team_score", "opponent_score"},
        )

    def test_corrected_current_schema_score_is_semantically_exact(self):
        self.assertEqual(
            mod.compare_parent_semantics(
                [durable_parent(points_for="58", points_against="65", result="L")],
                [durable_package(team="58", opponent="65", result="L")],
                [],
                school_key="test",
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
