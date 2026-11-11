import csv
import json
import sys
import unittest
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from program_history import (  # noqa: E402
    current_top_level_stint_start,
    derive_ncaa_accomplishments,
    history_coverage_errors,
    publication_history_games,
    publication_history_start,
    season_is_top_level,
    top_level_canonical_games,
)


LEGACY_PUBLISHED_KEYS = {
    "arizona-state",
    "boise-state",
    "central-connecticut",
    "chicago-state",
    "fairleigh-dickinson",
    "florida-state",
    "fresno-state",
    "george-mason",
    "gonzaga",
    "hawai-i",
    "houston",
    "kentucky",
    "le-moyne",
    "long-island-university",
    "mercyhurst",
    "miami",
    "new-haven",
    "san-diego-state",
    "stonehill",
    "texas-state",
    "uc-davis",
    "ucf",
    "vcu",
    "wagner",
}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def game(game_id, season, game_type="REGULAR_SEASON", round_name=""):
    return {
        "canonical_game_id": game_id,
        "season_label": season,
        "team_a_key": "program-a",
        "team_b_key": "program-b",
        "game_type": game_type,
        "postseason_round": round_name,
        "result_winner_team_key": "program-a",
        "game_date": "",
    }


class AllHistoryUniverseSemanticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.programs = read_csv(ROOT / "data/reference/programs.csv")
        cls.scope_rows = read_csv(
            ROOT / "data/reference/program-top-level-scope.csv"
        )
        cls.scope_by_school = {
            row["school"]: row["top_level_scope"] for row in cls.scope_rows
        }

    def scope_for(self, program):
        scope = self.scope_by_school.get(program["program_name"])
        if scope is None and program["program_key"] == "miami":
            scope = self.scope_by_school.get("Miami")
        self.assertIsNotNone(scope, program["program_key"])
        return scope

    def test_current_published_cohort_is_classified_deterministically(self):
        published = [
            row for row in self.programs
            if row["public_page_enabled"] == "Yes"
        ]
        unpublished = [
            row for row in self.programs
            if row["current_d1"] == "Yes"
            and row["public_page_enabled"] != "Yes"
        ]

        self.assertEqual(len(published), 113)
        complete = [
            row for row in published
            if row["history_coverage_status"] == "COMPLETE_INSTITUTIONAL"
        ]
        legacy = [
            row for row in published
            if row["history_coverage_status"] == "LEGACY_TOP_LEVEL_ONLY"
        ]
        self.assertEqual(len(complete), 89)
        self.assertEqual(len(legacy), 24)
        self.assertEqual(
            {row["program_key"] for row in legacy},
            LEGACY_PUBLISHED_KEYS,
        )
        self.assertEqual(len(unpublished), 252)
        self.assertTrue(
            all(row["history_coverage_status"] == "UNMIGRATED"
                for row in unpublished)
        )

        for row in published:
            expected = (
                "COMPLETE_INSTITUTIONAL"
                if self.scope_for(row) == "INCEPTION+"
                else "LEGACY_TOP_LEVEL_ONLY"
            )
            self.assertEqual(row["history_coverage_status"], expected)
            if expected == "COMPLETE_INSTITUTIONAL":
                self.assertEqual(
                    row["program_inception_season"],
                    row["history_start_season"],
                )
                self.assertEqual(
                    row["history_scope_basis"],
                    "ALWAYS_TOP_LEVEL_FROM_INCEPTION",
                )
            else:
                self.assertEqual(row["program_inception_season"], "")

        self.assertTrue(
            all(row["program_inception_season"] == "" for row in unpublished)
        )

    def test_registry_coverage_metadata_validates_independently(self):
        for row in self.programs:
            self.assertEqual(
                history_coverage_errors(
                    row,
                    public=row["public_page_enabled"] == "Yes",
                ),
                [],
                row["program_key"],
            )

    def test_top_level_membership_remains_interval_driven(self):
        intervals = "1948-49..1952-53|1954-55..1970-71|1985-86+"
        self.assertTrue(
            season_is_top_level("1952-1953", "1948-1949", intervals)
        )
        self.assertFalse(
            season_is_top_level("1953-1954", "1948-1949", intervals)
        )
        self.assertFalse(
            season_is_top_level("1979-1980", "1948-1949", intervals)
        )
        self.assertTrue(
            season_is_top_level("1985-1986", "1948-1949", intervals)
        )
        self.assertEqual(
            current_top_level_stint_start("1948-1949", intervals),
            "1985-1986",
        )

    def test_complete_institutional_publication_is_distinct_from_top_level(self):
        games = [
            game("CBBG-EARLY", "1930-1931"),
            game("CBBG-TOP", "1950-1951"),
        ]
        program = {
            "history_coverage_status": "COMPLETE_INSTITUTIONAL",
            "program_inception_season": "1930-1931",
            "history_start_season": "1950-1951",
            "history_scope_intervals": "",
        }
        self.assertEqual(
            [g["canonical_game_id"] for g in publication_history_games(
                games, "program-a", program
            )],
            ["CBBG-EARLY", "CBBG-TOP"],
        )
        self.assertEqual(
            [g["canonical_game_id"] for g in top_level_canonical_games(
                games, "program-a", "1950-1951"
            )],
            ["CBBG-TOP"],
        )
        self.assertEqual(publication_history_start(program), "1930-1931")

    def test_legacy_publication_preserves_existing_scope_selection(self):
        games = [
            game("CBBG-RECIPROCAL-EARLY", "1930-1931"),
            game("CBBG-LEGACY", "1950-1951"),
        ]
        program = {
            "history_coverage_status": "LEGACY_TOP_LEVEL_ONLY",
            "program_inception_season": "",
            "history_start_season": "1950-1951",
            "history_scope_intervals": "",
        }
        selected = publication_history_games(games, "program-a", program)
        self.assertEqual(
            [g["canonical_game_id"] for g in selected],
            ["CBBG-LEGACY"],
        )
        self.assertEqual(publication_history_start(program), "1950-1951")

    def test_unmigrated_and_unknown_statuses_fail_closed(self):
        self.assertEqual(
            publication_history_games(
                [game("CBBG-X", "2000-2001")],
                "program-a",
                {
                    "history_coverage_status": "UNMIGRATED",
                    "program_inception_season": "",
                },
            ),
            [],
        )
        problems = history_coverage_errors(
            {
                "history_coverage_status": "MYSTERY",
                "program_inception_season": "",
            },
            public=False,
        )
        self.assertIn("unknown history_coverage_status 'MYSTERY'", problems)
        with self.assertRaises(ValueError):
            publication_history_games(
                [],
                "program-a",
                {
                    "history_coverage_status": "MYSTERY",
                    "program_inception_season": "",
                },
            )

    def test_new_metadata_does_not_redefine_accomplishment_scope(self):
        games = [
            game(
                "CBBG-EARLY-NCAA",
                "1930-1931",
                game_type="NCAA_TOURNAMENT",
                round_name="R32",
            ),
            game(
                "CBBG-TOP-NCAA",
                "1950-1951",
                game_type="NCAA_TOURNAMENT",
                round_name="R32",
            ),
        ]
        program = {
            "history_coverage_status": "COMPLETE_INSTITUTIONAL",
            "program_inception_season": "1930-1931",
            "history_start_season": "1950-1951",
        }
        self.assertEqual(
            len(publication_history_games(games, "program-a", program)),
            2,
        )
        derived = derive_ncaa_accomplishments(
            games,
            "program-a",
            "1950-1951",
        )
        self.assertEqual(derived["ncaa_tournament_appearances"], 1)


class AllHistoryUniversePublicNonregressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.programs = read_csv(ROOT / "data/reference/programs.csv")
        with (ROOT / "data/canonical/games.csv").open(
            encoding="utf-8-sig", newline=""
        ) as handle:
            cls.canonical_games = list(csv.DictReader(handle))
        cls.games_by_program = defaultdict(list)
        for row in cls.canonical_games:
            cls.games_by_program[row["team_a_key"]].append(row)
            cls.games_by_program[row["team_b_key"]].append(row)

    def test_exact_public_canonical_game_id_population_is_unchanged(self):
        published = [
            row for row in self.programs
            if row["public_page_enabled"] == "Yes"
        ]
        self.assertEqual(len(published), 113)

        selector_union = set()
        frozen_site_union = set()
        for program in published:
            key = program["program_key"]
            selected_ids = {
                row["canonical_game_id"]
                for row in publication_history_games(
                    self.games_by_program[key],
                    key,
                    program,
                )
            }
            team_path = ROOT / "site/data/teams" / f"{key}.json"
            team = json.loads(team_path.read_text(encoding="utf-8"))
            frozen_ids = {
                row["canonical_game_id"] for row in team.get("games", [])
            }
            self.assertEqual(
                selected_ids,
                frozen_ids,
                (
                    f"{key}: Unit 1 publication selector changed the frozen "
                    "public canonical-game-ID population"
                ),
            )
            selector_union.update(selected_ids)
            frozen_site_union.update(frozen_ids)

        self.assertEqual(selector_union, frozen_site_union)

    def test_no_legacy_reciprocal_prescope_game_leaks(self):
        programs = {
            row["program_key"]: row for row in self.programs
        }
        for key in sorted(LEGACY_PUBLISHED_KEYS):
            program = programs[key]
            selected_ids = {
                row["canonical_game_id"]
                for row in publication_history_games(
                    self.games_by_program[key],
                    key,
                    program,
                )
            }
            team = json.loads(
                (ROOT / "site/data/teams" / f"{key}.json").read_text(
                    encoding="utf-8"
                )
            )
            frozen_ids = {
                row["canonical_game_id"] for row in team.get("games", [])
            }
            self.assertEqual(selected_ids, frozen_ids, key)


if __name__ == "__main__":
    unittest.main()
