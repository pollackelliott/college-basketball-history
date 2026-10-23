import csv
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from plan_home_chronology_remediation import (  # noqa: E402
    HomeChronologyPlanError,
    build_plan,
    parse_boundary,
)


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


PROGRAM_FIELDS = ["program_key", "public_page_enabled"]
CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "site_type",
    "venue_id",
    "venue_key",
    "site_city",
    "site_state",
    "notes",
]
ASSERTION_FIELDS = [
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "curated_venue_name",
    "city",
    "state",
]
GLOBAL_VENUE_FIELDS = ["venue_id", "venue_key", "display_name", "city", "state"]
SOURCE_FIELDS = [
    "source_game_id",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
]
SCHOOL_VENUE_FIELDS = [
    "venue_id",
    "venue_key",
    "canonical_name",
    "city",
    "state",
    "relationship_type",
    "relationship_start",
    "relationship_end",
    "source_basis",
]


class HomeChronologyPlannerTests(unittest.TestCase):
    def make_repo(
        self,
        root: Path,
        *,
        canonical_site="TEAM_A_HOME",
        canonical_city="",
        canonical_state="",
        include_assertion=True,
        second_relationship=False,
    ):
        write_csv(
            root / "data/reference/programs.csv",
            PROGRAM_FIELDS,
            [{"program_key": "alpha", "public_page_enabled": "yes"}],
        )
        write_csv(
            root / "data/canonical/games.csv",
            CANONICAL_FIELDS,
            [
                {
                    "canonical_game_id": "CBBG-1",
                    "season_label": "1924-1925",
                    "game_date": "1924-12-23",
                    "team_a_key": "alpha",
                    "team_b_key": "beta",
                    "site_type": canonical_site,
                    "venue_id": "",
                    "venue_key": "",
                    "site_city": canonical_city,
                    "site_state": canonical_state,
                    "notes": "",
                }
            ],
        )
        assertions = []
        if include_assertion:
            assertions.append(
                {
                    "canonical_game_id": "CBBG-1",
                    "source_program_key": "alpha",
                    "source_game_id": "ALPHA-1",
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                }
            )
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ASSERTION_FIELDS,
            assertions,
        )
        write_csv(
            root / "data/reference/venues.csv",
            GLOBAL_VENUE_FIELDS,
            [
                {
                    "venue_id": "VEN-1",
                    "venue_key": "alpha-gym",
                    "display_name": "Alpha Gym",
                    "city": "Alpha City",
                    "state": "AA",
                },
                {
                    "venue_id": "VEN-2",
                    "venue_key": "alpha-annex",
                    "display_name": "Alpha Annex",
                    "city": "Alpha City",
                    "state": "AA",
                },
            ],
        )
        write_csv(
            root / "schools/alpha/source-games.csv",
            SOURCE_FIELDS,
            [
                {
                    "source_game_id": "ALPHA-1",
                    "curated_site_type": "SOURCE_PROGRAM_HOME",
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                }
            ],
        )
        relationships = [
            {
                "venue_id": "VEN-1",
                "venue_key": "alpha-gym",
                "canonical_name": "Alpha Gym",
                "city": "Alpha City",
                "state": "AA",
                "relationship_type": "primary_home",
                "relationship_start": "1924-1925",
                "relationship_end": "1924-1925",
                "source_basis": "official venue chronology",
            }
        ]
        if second_relationship:
            relationships.append(
                {
                    "venue_id": "VEN-2",
                    "venue_key": "alpha-annex",
                    "canonical_name": "Alpha Annex",
                    "city": "Alpha City",
                    "state": "AA",
                    "relationship_type": "alternate_home",
                    "relationship_start": "1924-01-01",
                    "relationship_end": "1925-01-01",
                    "source_basis": "official alternate-site history",
                }
            )
        write_csv(
            root / "schools/alpha/venues.csv",
            SCHOOL_VENUE_FIELDS,
            relationships,
        )

    def test_unique_season_chronology_produces_three_layer_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)

            plan = build_plan(root, ["alpha"])["payload"]

            self.assertEqual(plan["candidate_count"], 1)
            self.assertEqual(plan["review_count"], 0)
            candidate = plan["candidates"][0]
            self.assertEqual(candidate["venue"]["venue_key"], "alpha-gym")
            self.assertEqual(
                candidate["patches"]["canonical"],
                {
                    "venue_id": "VEN-1",
                    "venue_key": "alpha-gym",
                    "site_city": "Alpha City",
                    "site_state": "AA",
                },
            )
            self.assertEqual(
                candidate["patches"]["source"],
                {
                    "curated_venue_name": "Alpha Gym",
                    "city": "Alpha City",
                    "state": "AA",
                },
            )
            self.assertEqual(candidate["patches"]["assertion"], candidate["patches"]["source"])

    def test_planner_never_infers_home_from_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, canonical_site="UNKNOWN")

            plan = build_plan(root, ["alpha"])["payload"]

            self.assertEqual(plan["candidate_count"], 0)
            self.assertEqual(plan["review_count"], 0)
            self.assertEqual(plan["summary_by_program"]["alpha"].get("hard_blocker", 0), 0)

    def test_retained_canonical_geography_conflict_is_review_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, canonical_city="Other City", canonical_state="AA")

            plan = build_plan(root, ["alpha"])["payload"]

            self.assertEqual(plan["candidate_count"], 0)
            self.assertEqual(plan["review_count"], 1)
            self.assertEqual(plan["reviews"][0]["reason"], "retained_value_conflict")
            self.assertIn("canonical.site_city", plan["reviews"][0]["detail"])

    def test_missing_home_assertion_is_review_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, include_assertion=False)

            plan = build_plan(root, ["alpha"])["payload"]

            self.assertEqual(plan["candidate_count"], 0)
            self.assertEqual(plan["review_count"], 1)
            self.assertEqual(plan["reviews"][0]["reason"], "missing_home_assertion")

    def test_overlapping_distinct_home_relationships_are_review_only(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, second_relationship=True)

            plan = build_plan(root, ["alpha"])["payload"]

            self.assertEqual(plan["candidate_count"], 0)
            self.assertEqual(plan["review_count"], 1)
            self.assertEqual(plan["reviews"][0]["reason"], "ambiguous_home_chronology")



    def test_existing_human_readable_boundaries_preserve_precision(self):
        pairs = [
            ("January 1930", date(1930, 1, 1), date(1930, 1, 31)),
            ("1971-1972 season", date(1971, 7, 1), date(1972, 6, 30)),
            ("2004-2005 season", date(2004, 7, 1), date(2005, 6, 30)),
        ]
        for text, expected_start, expected_end in pairs:
            with self.subTest(boundary=text):
                self.assertEqual(parse_boundary(text, end=False), expected_start)
                self.assertEqual(parse_boundary(text, end=True), expected_end)
        self.assertIsNone(parse_boundary("program beginning", end=False))
        self.assertIsNone(parse_boundary("present", end=True))

    def test_compact_basketball_seasons_preserve_season_semantics(self):
        pairs = [
            ("1931-32", date(1931, 7, 1), date(1932, 6, 30)),
            ("2011-12", date(2011, 7, 1), date(2012, 6, 30)),
        ]
        for text, expected_start, expected_end in pairs:
            with self.subTest(boundary=text):
                self.assertEqual(parse_boundary(text, end=False), expected_start)
                self.assertEqual(parse_boundary(text, end=True), expected_end)
        self.assertEqual(parse_boundary("2011-06", end=False), date(2011, 6, 1))
        self.assertEqual(parse_boundary("2011-06", end=True), date(2011, 6, 30))

    def test_unbounded_markers_do_not_reverse_meaning(self):
        with self.assertRaises(HomeChronologyPlanError):
            parse_boundary("program beginning", end=True)
        with self.assertRaises(HomeChronologyPlanError):
            parse_boundary("present", end=False)
        with self.assertRaises(HomeChronologyPlanError):
            parse_boundary("NotAMonth 1930", end=False)

    def test_human_readable_single_home_chronology_is_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            path = root / "schools/alpha/venues.csv"
            with path.open(encoding="utf-8", newline="") as handle:
                relationships = list(csv.DictReader(handle))
            relationships[0]["relationship_start"] = "program beginning"
            relationships[0]["relationship_end"] = "December 1924"
            write_csv(path, SCHOOL_VENUE_FIELDS, relationships)
            plan = build_plan(root, ["alpha"])["payload"]
            self.assertEqual(plan["candidate_count"], 1)
            self.assertEqual(plan["review_count"], 0)

    def test_named_month_transition_overlap_stops_for_review(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, second_relationship=True)
            game_path = root / "data/canonical/games.csv"
            with game_path.open(encoding="utf-8", newline="") as handle:
                games = list(csv.DictReader(handle))
            games[0]["game_date"] = "1925-01-15"
            write_csv(game_path, CANONICAL_FIELDS, games)
            venue_path = root / "schools/alpha/venues.csv"
            with venue_path.open(encoding="utf-8", newline="") as handle:
                relationships = list(csv.DictReader(handle))
            relationships[0]["relationship_end"] = "January 1925"
            relationships[1]["relationship_start"] = "January 1925"
            relationships[1]["relationship_end"] = "present"
            write_csv(venue_path, SCHOOL_VENUE_FIELDS, relationships)
            plan = build_plan(root, ["alpha"])["payload"]
            self.assertEqual(plan["candidate_count"], 0)
            self.assertEqual(plan["review_count"], 1)
            self.assertEqual(plan["reviews"][0]["reason"], "ambiguous_home_chronology")

if __name__ == "__main__":
    unittest.main()
