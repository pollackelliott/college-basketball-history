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


if __name__ == "__main__":
    unittest.main()
