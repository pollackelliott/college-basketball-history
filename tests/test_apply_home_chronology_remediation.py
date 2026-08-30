import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from apply_home_chronology_remediation import (  # noqa: E402
    HomeChronologyApplyError,
    apply_plan,
)
from plan_home_chronology_remediation import build_plan  # noqa: E402


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


class HomeChronologyApplyTests(unittest.TestCase):
    def make_repo(self, root: Path, *, source_site="SOURCE_PROGRAM_HOME"):
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
                    "site_type": "TEAM_A_HOME",
                    "venue_id": "",
                    "venue_key": "",
                    "site_city": "",
                    "site_state": "",
                    "notes": "existing note",
                }
            ],
        )
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ASSERTION_FIELDS,
            [
                {
                    "canonical_game_id": "CBBG-1",
                    "source_program_key": "alpha",
                    "source_game_id": "ALPHA-1",
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                }
            ],
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
                }
            ],
        )
        write_csv(
            root / "schools/alpha/source-games.csv",
            SOURCE_FIELDS,
            [
                {
                    "source_game_id": "ALPHA-1",
                    "curated_site_type": source_site,
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                }
            ],
        )
        write_csv(
            root / "schools/alpha/venues.csv",
            SCHOOL_VENUE_FIELDS,
            [
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
            ],
        )

    def test_apply_updates_three_layers_without_changing_home_classification(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            plan = build_plan(root, ["alpha"])

            result = apply_plan(
                root,
                ["alpha"],
                plan["sha256"],
                run_validation=False,
            )

            self.assertEqual(result["applied_games"], 1)

            canonical = read_rows(root / "data/canonical/games.csv")[0]
            source = read_rows(root / "schools/alpha/source-games.csv")[0]
            assertion = read_rows(root / "data/evidence/game-assertions.csv")[0]

            self.assertEqual(canonical["site_type"], "TEAM_A_HOME")
            self.assertEqual(canonical["venue_id"], "VEN-1")
            self.assertEqual(canonical["venue_key"], "alpha-gym")
            self.assertEqual(canonical["site_city"], "Alpha City")
            self.assertEqual(canonical["site_state"], "AA")
            self.assertIn("HOME_CHRONOLOGY_BACKFILL", canonical["notes"])
            self.assertIn("existing note", canonical["notes"])

            self.assertEqual(source["curated_site_type"], "SOURCE_PROGRAM_HOME")
            self.assertEqual(source["curated_venue_name"], "Alpha Gym")
            self.assertEqual(source["city"], "Alpha City")
            self.assertEqual(source["state"], "AA")
            self.assertEqual(assertion["curated_venue_name"], "Alpha Gym")
            self.assertEqual(assertion["city"], "Alpha City")
            self.assertEqual(assertion["state"], "AA")

            post = build_plan(root, ["alpha"])["payload"]
            self.assertEqual(post["candidate_count"], 0)
            self.assertEqual(post["review_count"], 0)
            self.assertEqual(post["summary_by_program"]["alpha"].get("hard_blocker", 0), 0)

    def test_hash_mismatch_refuses_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            before = (root / "data/canonical/games.csv").read_bytes()

            with self.assertRaises(HomeChronologyApplyError):
                apply_plan(
                    root,
                    ["alpha"],
                    "0" * 64,
                    run_validation=False,
                )

            self.assertEqual((root / "data/canonical/games.csv").read_bytes(), before)

    def test_review_bearing_program_refuses_without_writes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, source_site="UNKNOWN")
            plan = build_plan(root, ["alpha"])
            self.assertEqual(plan["payload"]["review_count"], 1)
            before = (root / "data/canonical/games.csv").read_bytes()

            with self.assertRaises(HomeChronologyApplyError):
                apply_plan(
                    root,
                    ["alpha"],
                    plan["sha256"],
                    run_validation=False,
                )

            self.assertEqual((root / "data/canonical/games.csv").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
