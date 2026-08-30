import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from plan_home_chronology_remediation import build_plan  # noqa: E402


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


if __name__ == "__main__":
    unittest.main()
