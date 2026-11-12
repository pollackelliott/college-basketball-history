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
    derive_top_level_ncaa_accomplishments,
    history_coverage_errors,
    publication_conference_timeline,
    publication_history_games,
    publication_history_start,
    season_is_published_history,
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


class AllHistoryUniverseTopLevelAccomplishmentTests(unittest.TestCase):
    def test_publication_can_include_pre_d1_while_accomplishments_exclude_it(self):
        games = [
            game(
                "CBBG-EARLY-NCAA",
                "1930-1931",
                game_type="NCAA_TOURNAMENT",
                round_name="Championship",
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
            "history_scope_intervals": "",
        }
        self.assertEqual(
            [row["canonical_game_id"] for row in publication_history_games(
                games, "program-a", program
            )],
            ["CBBG-EARLY-NCAA", "CBBG-TOP-NCAA"],
        )
        derived = derive_top_level_ncaa_accomplishments(
            games,
            "program-a",
            program["history_start_season"],
            program["history_scope_intervals"],
        )
        self.assertEqual(derived["ncaa_game_count"], 1)
        self.assertEqual(derived["ncaa_tournament_appearances"], 1)
        self.assertEqual(derived["best_finish_key"], "ROUND_OF_32")

    def test_pre_d1_ncaa_row_cannot_create_top_level_accomplishments(self):
        derived = derive_top_level_ncaa_accomplishments(
            [
                game(
                    "CBBG-EARLY-CHAMPION",
                    "1930-1931",
                    game_type="NCAA_TOURNAMENT",
                    round_name="Championship",
                )
            ],
            "program-a",
            "1950-1951",
        )
        self.assertEqual(derived["ncaa_tournament_appearances"], 0)
        self.assertEqual(derived["final_four_appearances"], 0)
        self.assertEqual(derived["national_championships"], 0)
        self.assertIsNone(derived["best_finish_key"])
        self.assertIsNone(derived["best_finish_year"])

    def test_pre_d1_tournament_row_does_not_change_valid_top_level_result(self):
        top_level = game(
            "CBBG-TOP-R32",
            "1950-1951",
            game_type="NCAA_TOURNAMENT",
            round_name="R32",
        )
        pre_d1 = game(
            "CBBG-EARLY-CHAMPION",
            "1930-1931",
            game_type="NCAA_TOURNAMENT",
            round_name="Championship",
        )
        expected = derive_top_level_ncaa_accomplishments(
            [top_level],
            "program-a",
            "1950-1951",
        )
        actual = derive_top_level_ncaa_accomplishments(
            [pre_d1, top_level],
            "program-a",
            "1950-1951",
        )
        self.assertEqual(actual, expected)

    def test_interrupted_top_level_intervals_exclude_gap_tournament_rows(self):
        intervals = "1940-41..1941-42|1944-45+"
        first_stint = game(
            "CBBG-FIRST-STINT",
            "1940-1941",
            game_type="NCAA_TOURNAMENT",
            round_name="R64",
        )
        gap_champion = game(
            "CBBG-GAP-CHAMPION",
            "1942-1943",
            game_type="NCAA_TOURNAMENT",
            round_name="Championship",
        )
        current_stint = game(
            "CBBG-CURRENT-STINT",
            "1944-1945",
            game_type="NCAA_TOURNAMENT",
            round_name="R32",
        )
        expected = derive_top_level_ncaa_accomplishments(
            [first_stint, current_stint],
            "program-a",
            "1940-1941",
            intervals,
        )
        actual = derive_top_level_ncaa_accomplishments(
            [first_stint, gap_champion, current_stint],
            "program-a",
            "1940-1941",
            intervals,
        )
        self.assertEqual(actual, expected)
        self.assertEqual(actual["ncaa_tournament_appearances"], 2)
        self.assertEqual(actual["national_championships"], 0)
        self.assertEqual(actual["best_finish_key"], "ROUND_OF_32")

    def test_compatibility_wrapper_matches_explicit_top_level_helper(self):
        games = [
            game(
                "CBBG-EARLY",
                "1930-1931",
                game_type="NCAA_TOURNAMENT",
                round_name="Championship",
            ),
            game(
                "CBBG-TOP",
                "1950-1951",
                game_type="NCAA_TOURNAMENT",
                round_name="R32",
            ),
        ]
        explicit = derive_top_level_ncaa_accomplishments(
            games,
            "program-a",
            "1950-1951",
        )
        compatibility = derive_ncaa_accomplishments(
            games,
            "program-a",
            "1950-1951",
        )
        self.assertEqual(compatibility, explicit)

    def test_explicit_helper_uses_top_level_authority_not_publication_history(self):
        source = (ROOT / "tools/program_history.py").read_text(encoding="utf-8")
        helper = source.split(
            "def derive_top_level_ncaa_accomplishments(", 1
        )[1].split("\ndef ", 1)[0]
        self.assertIn("top_level_canonical_games(", helper)
        self.assertNotIn("scope_canonical_games(", helper)
        self.assertNotIn("publication_history_games(", helper)
        self.assertIn(
            "accepted top-level/D-I-equivalent intervals",
            helper,
        )

    def test_direct_accomplishment_consumers_use_explicit_top_level_helper(self):
        for relative_path in (
            "tools/verify_program_accomplishments.py",
            "tools/onboarding_plan.py",
        ):
            with self.subTest(path=relative_path):
                source = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn("derive_top_level_ncaa_accomplishments", source)
                self.assertNotIn("derive_ncaa_accomplishments", source)
                self.assertIn("history_scope_intervals", source)

    def test_accomplishment_reference_and_generated_payloads_are_unchanged(self):
        reference = {
            row["program_key"]: row
            for row in read_csv(
                ROOT / "data/reference/program-accomplishments.csv"
            )
        }
        manifest = json.loads(
            (ROOT / "site/data/programs.json").read_text(encoding="utf-8")
        )["programs"]
        integer_fields = (
            "conference_regular_season_championships",
            "conference_tournament_championships",
            "ncaa_tournament_appearances",
            "final_four_appearances",
            "national_championships",
            "best_finish_year",
        )
        scalar_fields = ("best_finish_key",)

        self.assertEqual(
            {program["program_key"] for program in manifest},
            set(reference),
        )
        for program in manifest:
            key = program["program_key"]
            row = reference[key]
            for field in integer_fields:
                expected = int(row[field]) if row[field].strip() else None
                self.assertEqual(program[field], expected, (key, field))
            for field in scalar_fields:
                self.assertEqual(
                    program[field],
                    row[field].strip() or None,
                    (key, field),
                )

            if program["public_page_enabled"]:
                team = json.loads(
                    (ROOT / "site/data/teams" / f"{key}.json").read_text(
                        encoding="utf-8"
                    )
                )["program"]
                for field in (*integer_fields, *scalar_fields):
                    self.assertEqual(team[field], program[field], (key, field))


class AllHistoryUniverseConferenceProjectionTests(unittest.TestCase):
    @staticmethod
    def complete_program(
        *,
        inception="1930-1931",
        top_level_start="1950-1951",
        intervals="",
    ):
        return {
            "history_coverage_status": "COMPLETE_INSTITUTIONAL",
            "program_inception_season": inception,
            "history_start_season": top_level_start,
            "history_scope_intervals": intervals,
        }

    @staticmethod
    def real_row(start="1950-1951", end=""):
        return {
            "start_season": start,
            "end_season": end,
            "conference_key": "example-conference",
            "conference_name": "Example Conference",
            "membership_type": "full",
        }

    def test_complete_institutional_synthesizes_active_pre_d1_block(self):
        program = self.complete_program()
        timeline = publication_conference_timeline(
            [self.real_row()],
            program,
            ["1930-1931", "1931-1932", "1950-1951"],
        )
        self.assertEqual(
            timeline[0],
            {
                "start_season": "1930-1931",
                "end_season": "1931-1932",
                "conference_key": "",
                "conference_name": "Non-D1",
                "membership_type": "classification",
                "classification": "NON_D1_CLASSIFICATION",
            },
        )
        self.assertTrue(season_is_published_history("1930-1931", program))
        self.assertFalse(season_is_top_level("1930-1931", "1950-1951"))

    def test_dormant_season_gap_is_not_manufactured(self):
        timeline = publication_conference_timeline(
            [self.real_row()],
            self.complete_program(),
            ["1930-1931", "1932-1933", "1950-1951"],
        )
        synthetic = [
            row for row in timeline
            if row.get("classification") == "NON_D1_CLASSIFICATION"
        ]
        self.assertEqual(
            [(row["start_season"], row["end_season"]) for row in synthetic],
            [
                ("1930-1931", "1930-1931"),
                ("1932-1933", "1932-1933"),
            ],
        )

    def test_interrupted_d1_non_d1_d1_history(self):
        program = self.complete_program(
            inception="1940-1941",
            top_level_start="1940-1941",
            intervals="1940-41..1941-42|1944-45+",
        )
        history = [
            self.real_row("1940-1941", "1941-1942"),
            {
                **self.real_row("1944-1945", ""),
                "conference_key": "later-conference",
                "conference_name": "Later Conference",
            },
        ]
        timeline = publication_conference_timeline(
            history,
            program,
            [
                "1940-1941",
                "1941-1942",
                "1942-1943",
                "1943-1944",
                "1944-1945",
            ],
        )
        self.assertEqual(
            [row["conference_name"] for row in timeline],
            ["Example Conference", "Non-D1", "Later Conference"],
        )
        synthetic = timeline[1]
        self.assertEqual(synthetic["start_season"], "1942-1943")
        self.assertEqual(synthetic["end_season"], "1943-1944")

    def test_legacy_does_not_synthesize_unpublished_pre_scope_history(self):
        program = {
            "history_coverage_status": "LEGACY_TOP_LEVEL_ONLY",
            "program_inception_season": "",
            "history_start_season": "1950-1951",
            "history_scope_intervals": "",
        }
        timeline = publication_conference_timeline(
            [self.real_row()],
            program,
            ["1930-1931", "1950-1951"],
        )
        self.assertEqual(timeline, [self.real_row()])
        self.assertFalse(season_is_published_history("1930-1931", program))
        self.assertTrue(season_is_published_history("1950-1951", program))

    def test_real_conference_rows_keep_existing_public_shape(self):
        source = self.real_row()
        timeline = publication_conference_timeline(
            [source],
            self.complete_program(),
            ["1950-1951"],
        )
        self.assertEqual(timeline, [source])
        self.assertNotIn("classification", timeline[0])

    def test_current_published_portfolio_has_zero_synthetic_non_d1_rows(self):
        programs = read_csv(ROOT / "data/reference/programs.csv")
        published = [
            row for row in programs
            if row["public_page_enabled"] == "Yes"
        ]
        self.assertEqual(len(published), 113)

        synthetic = []
        for program in published:
            key = program["program_key"]
            history = read_csv(ROOT / "schools" / key / "conferences.csv")
            team = json.loads(
                (ROOT / "site/data/teams" / f"{key}.json").read_text(
                    encoding="utf-8"
                )
            )
            active_seasons = {
                row["season_label"] for row in team.get("seasons", [])
            }
            timeline = publication_conference_timeline(
                history,
                program,
                active_seasons,
            )
            synthetic.extend(
                (key, row)
                for row in timeline
                if row.get("classification") == "NON_D1_CLASSIFICATION"
            )

        self.assertEqual(synthetic, [])

    def test_publication_season_unknown_coverage_fails_closed(self):
        with self.assertRaises(ValueError):
            season_is_published_history(
                "2000-2001",
                {"history_coverage_status": "MYSTERY"},
            )


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


class AllHistoryUniverseBuilderSourceTests(unittest.TestCase):
    def test_builder_uses_publication_history_helper_and_metadata_contract(self):
        source = (ROOT / "tools/build_site_data.py").read_text(encoding="utf-8")
        self.assertIn("publication_history_games(", source)
        self.assertNotIn("scope_canonical_games(", source)
        self.assertIn("publication_history_start(", source)
        self.assertIn("current_top_level_stint_start(", source)
        self.assertIn("publication_conference_timeline(", source)
        self.assertNotIn("trim_conference_history(", source)
        self.assertIn('"classification": row.get("classification", "").strip()', source)
        for field in (
            "published_history_start_season",
            "d1_since_season",
            "history_coverage_status",
        ):
            self.assertGreaterEqual(source.count(f'"{field}"'), 2, field)
        self.assertGreaterEqual(source.count('"history_start_season"'), 2)


if __name__ == "__main__":
    unittest.main()
