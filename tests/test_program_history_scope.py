import csv
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import build_site_data  # noqa: E402
from program_history import (  # noqa: E402
    BEST_FINISH_LABELS,
    accomplishment_row_issues,
    derive_ncaa_accomplishments,
    history_scope_errors,
    partition_source_rows,
    scope_canonical_games,
    trim_conference_history,
)


def canonical_game(
    game_id,
    season,
    team_a="program-a",
    team_b="program-b",
    game_type="REGULAR_SEASON",
    round_name="",
    winner="program-a",
    game_date="",
):
    return {
        "canonical_game_id": game_id,
        "season_label": season,
        "game_date": game_date,
        "date_precision": "EXACT" if game_date else "SEASON",
        "team_a_key": team_a,
        "team_b_key": team_b,
        "team_a_score": "70",
        "team_b_score": "60",
        "result_winner_team_key": winner,
        "overtime_periods": "0",
        "site_type": "UNKNOWN",
        "designated_home_team_key": "",
        "venue_key": "",
        "site_city": "",
        "site_state": "",
        "game_type": game_type,
        "postseason_round": round_name,
        "administrative_status": "",
        "administrative_note": "",
    }


class ProgramHistoryScopeTests(unittest.TestCase):
    def test_owner_scope_is_required_before_target_ingestion(self):
        missing = {
            "history_start_season": "",
            "history_scope_status": "",
            "history_scope_basis": "",
        }
        self.assertTrue(history_scope_errors(missing, required=True))
        confirmed = {
            "history_start_season": "2000-2001",
            "history_scope_status": "OWNER_CONFIRMED",
            "history_scope_basis": "FIRST_TOP_LEVEL_SEASON",
        }
        self.assertEqual(history_scope_errors(confirmed, required=True), [])

    def test_one_game_can_be_out_of_scope_for_a_and_in_scope_for_b(self):
        game = canonical_game("CBBG-OLD", "1999-2000")
        self.assertEqual(
            scope_canonical_games([game], "program-a", "2000-2001"), []
        )
        self.assertEqual(
            scope_canonical_games([game], "program-b", "1990-1991"), [game]
        )

    def test_ingest_partition_preserves_pre_cutoff_source_evidence(self):
        old = {"season_label": "1999-2000", "raw_text": "preserve me"}
        current = {"season_label": "2000-2001", "raw_text": "in scope"}
        in_scope, pre_cutoff = partition_source_rows(
            [old, current], "2000-2001"
        )
        self.assertEqual(in_scope, [current])
        self.assertEqual(pre_cutoff, [old])
        self.assertEqual(old["raw_text"], "preserve me")

    def test_records_and_opponents_use_only_scoped_games(self):
        old = canonical_game("CBBG-OLD", "1999-2000", winner="program-b")
        current = canonical_game("CBBG-NEW", "2000-2001")
        scoped = scope_canonical_games(
            [old, current], "program-a", "2000-2001"
        )
        perspective = [
            build_site_data.perspective_game(
                game,
                "program-a",
                {"program-b": "Program B"},
                {},
                {},
            )
            for game in scoped
        ]
        self.assertEqual(build_site_data.record_from_games(perspective)["wins"], 1)
        self.assertEqual({game["opponent_key"] for game in perspective}, {"program-b"})
        self.assertEqual(len(perspective), 1)

    def test_public_conference_history_is_clipped_without_mutating_source(self):
        source = [
            {"start_season": "1990-1991", "end_season": "2004-2005", "conference_key": "old"},
            {"start_season": "2005-2006", "end_season": "", "conference_key": "new"},
        ]
        public = trim_conference_history(source, "2000-2001")
        self.assertEqual(public[0]["start_season"], "2000-2001")
        self.assertEqual(source[0]["start_season"], "1990-1991")

    def test_public_program_pre_scope_games_are_reciprocal_only(self):
        with (ROOT / "data/reference/programs.csv").open(
            encoding="utf-8-sig", newline=""
        ) as f:
            programs = {
                row["program_key"]: row for row in csv.DictReader(f)
            }
        with (ROOT / "data/canonical/games.csv").open(
            encoding="utf-8-sig", newline=""
        ) as f:
            games = list(csv.DictReader(f))
        with (ROOT / "data/evidence/game-assertions.csv").open(
            encoding="utf-8-sig", newline=""
        ) as f:
            assertions = list(csv.DictReader(f))

        assertion_sources = {}
        for assertion in assertions:
            assertion_sources.setdefault(
                assertion["canonical_game_id"], set()
            ).add(assertion["source_program_key"])

        public_keys = [
            key
            for key, row in programs.items()
            if row["public_page_enabled"] == "Yes"
        ]
        for key in public_keys:
            start = programs[key]["history_start_season"]
            all_games = [
                game
                for game in games
                if key in {game["team_a_key"], game["team_b_key"]}
            ]
            scoped = scope_canonical_games(all_games, key, start)
            scoped_ids = {game["canonical_game_id"] for game in scoped}
            excluded = [
                game
                for game in all_games
                if game["canonical_game_id"] not in scoped_ids
            ]
            for game in excluded:
                self.assertLess(game["season_label"], start, key)
                sources = assertion_sources.get(game["canonical_game_id"], set())
                self.assertNotIn(key, sources, game["canonical_game_id"])
                self.assertTrue(sources, game["canonical_game_id"])


class AccomplishmentTests(unittest.TestCase):
    def program(self, public=False):
        return {
            "history_start_season": "1990-1991",
            "public_page_enabled": "Yes" if public else "No",
        }

    def row(self, **changes):
        row = {
            "conference_regular_season_championships": "0",
            "conference_tournament_championships": "0",
            "ncaa_tournament_appearances": "0",
            "final_four_appearances": "0",
            "national_championships": "0",
            "best_finish_key": "",
            "best_finish_year": "",
            "verification_status": "OWNER_BASELINE_UNVERIFIED",
            "canonical_crosscheck_status": "NOT_CHECKED",
        }
        row.update(changes)
        return row

    def test_controlled_vocabulary(self):
        self.assertEqual(
            set(BEST_FINISH_LABELS),
            {
                "NATIONAL_CHAMPION",
                "NATIONAL_RUNNER_UP",
                "FINAL_FOUR",
                "ELITE_EIGHT",
                "SWEET_SIXTEEN",
                "ROUND_OF_32",
                "ROUND_OF_64",
                "PLAY_IN_ROUND",
            },
        )

    def test_zero_appearance_finish_rules(self):
        errors, _ = accomplishment_row_issues(
            self.row(best_finish_key="ROUND_OF_64"), self.program(), False
        )
        self.assertIn("zero NCAA appearances requires blank best_finish_key", errors)

    def test_disabled_under_review_missing_year_is_warning(self):
        errors, warnings = accomplishment_row_issues(
            self.row(
                ncaa_tournament_appearances="2",
                best_finish_key="ROUND_OF_64",
                verification_status="UNDER_REVIEW",
            ),
            self.program(),
            False,
        )
        self.assertEqual(errors, [])
        self.assertIn("positive NCAA appearances requires best_finish_year", warnings)

    def test_champion_and_runner_up_are_distinguished(self):
        runner = canonical_game(
            "CBBG-RUNNER",
            "2000-2001",
            game_type="NCAA_TOURNAMENT",
            round_name="Championship",
            winner="program-b",
            game_date="2001-04-02",
        )
        champion = canonical_game(
            "CBBG-CHAMPION",
            "2005-2006",
            game_type="NCAA_TOURNAMENT",
            round_name="Championship",
            winner="program-a",
            game_date="2006-04-03",
        )
        derived = derive_ncaa_accomplishments(
            [runner, champion], "program-a", "1990-1991"
        )
        self.assertEqual(derived["national_championships"], 1)
        self.assertEqual(derived["best_finish_key"], "NATIONAL_CHAMPION")

    def test_best_finish_year_is_most_recent_same_finish(self):
        games = [
            canonical_game(
                "CBBG-ONE",
                "2005-2006",
                game_type="NCAA_TOURNAMENT",
                round_name="Elite Eight",
                game_date="2006-03-25",
            ),
            canonical_game(
                "CBBG-TWO",
                "2010-2011",
                game_type="NCAA_TOURNAMENT",
                round_name="Elite Eight",
                game_date="2011-03-26",
            ),
        ]
        derived = derive_ncaa_accomplishments(
            games, "program-a", "1990-1991"
        )
        self.assertEqual(derived["best_finish_key"], "ELITE_EIGHT")
        self.assertEqual(derived["best_finish_year"], 2011)


if __name__ == "__main__":
    unittest.main()
