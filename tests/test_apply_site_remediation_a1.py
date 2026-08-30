import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from apply_site_remediation_a1 import (  # noqa: E402
    A1ApplyError,
    apply_a1_plan,
    build_a1_plan,
)


CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "game_type",
    "notes",
]
ASSERTION_FIELDS = [
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
]
DISCREPANCY_FIELDS = [
    "canonical_game_id",
    "field_name",
    "status",
    "resolution_basis",
]
GLOBAL_VENUE_FIELDS = [
    "venue_id",
    "venue_key",
    "display_name",
    "city",
    "state",
]
VENUE_NAME_FIELDS = [
    "venue_id",
    "venue_name",
    "normalized_name",
    "name_type",
    "valid_from",
    "valid_to",
    "date_precision",
    "source_basis",
    "notes",
]
SCHOOL_VENUE_FIELDS = [
    "source_program_key",
    "venue_key",
    "venue_id",
    "canonical_name",
    "aliases",
    "city",
    "state",
]


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class ApplySiteRemediationA1Tests(unittest.TestCase):
    def make_repo(self, root: Path, *, include_a2=False):
        games = [
            {
                "canonical_game_id": "CBBG-0000001",
                "season_label": "2000-2001",
                "game_date": "2001-01-01",
                "team_a_key": "alpha",
                "team_b_key": "beta",
                "site_type": "NEUTRAL",
                "designated_home_team_key": "",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "game_type": "REGULAR_SEASON",
                "notes": "",
            }
        ]
        assertions = [
            {
                "canonical_game_id": "CBBG-0000001",
                "source_program_key": "alpha",
                "source_game_id": "ARAW-1",
                "normalized_opponent_key": "beta",
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Example Arena",
                "city": "Alpha City",
                "state": "AA",
            },
            {
                "canonical_game_id": "CBBG-0000001",
                "source_program_key": "beta",
                "source_game_id": "BRAW-1",
                "normalized_opponent_key": "alpha",
                "curated_site_type": "UNKNOWN",
                "curated_venue_name": "",
                "city": "",
                "state": "",
            },
        ]

        if include_a2:
            games.append(
                {
                    "canonical_game_id": "CBBG-0000002",
                    "season_label": "2000-2001",
                    "game_date": "2001-02-01",
                    "team_a_key": "alpha",
                    "team_b_key": "beta",
                    "site_type": "UNKNOWN",
                    "designated_home_team_key": "",
                    "venue_key": "",
                    "venue_id": "",
                    "site_city": "",
                    "site_state": "",
                    "game_type": "REGULAR_SEASON",
                    "notes": "",
                }
            )
            assertions.extend(
                [
                    {
                        "canonical_game_id": "CBBG-0000002",
                        "source_program_key": "alpha",
                        "source_game_id": "ARAW-2",
                        "normalized_opponent_key": "beta",
                        "curated_site_type": "SOURCE_PROGRAM_HOME",
                        "curated_venue_name": "Example Arena",
                        "city": "Alpha City",
                        "state": "AA",
                    },
                    {
                        "canonical_game_id": "CBBG-0000002",
                        "source_program_key": "beta",
                        "source_game_id": "BRAW-2",
                        "normalized_opponent_key": "alpha",
                        "curated_site_type": "UNKNOWN",
                        "curated_venue_name": "",
                        "city": "",
                        "state": "",
                    },
                ]
            )

        write_csv(root / "data/canonical/games.csv", CANONICAL_FIELDS, games)
        write_csv(root / "data/evidence/game-assertions.csv", ASSERTION_FIELDS, assertions)
        write_csv(root / "data/reconciliation/discrepancies.csv", DISCREPANCY_FIELDS, [])
        write_csv(
            root / "data/reference/venues.csv",
            GLOBAL_VENUE_FIELDS,
            [
                {
                    "venue_id": "VEN-000001",
                    "venue_key": "example-arena",
                    "display_name": "Example Arena",
                    "city": "Alpha City",
                    "state": "AA",
                }
            ],
        )
        write_csv(
            root / "data/reference/venue-names.csv",
            VENUE_NAME_FIELDS,
            [
                {
                    "venue_id": "VEN-000001",
                    "venue_name": "Example Arena",
                    "normalized_name": "examplearena",
                    "name_type": "PROJECT_DISPLAY",
                }
            ],
        )
        for program in ("alpha", "beta"):
            write_csv(
                root / f"schools/{program}/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [
                    {
                        "source_program_key": program,
                        "venue_key": "example-arena",
                        "venue_id": "VEN-000001",
                        "canonical_name": "Example Arena",
                        "aliases": "",
                        "city": "Alpha City",
                        "state": "AA",
                    }
                ],
            )

        # Guarded tool files only need stable bytes in the synthetic repository.
        for relative in (
            "tools/site_remediation_audit.py",
            "tools/site_remediation_tier_report.py",
            "tools/apply_site_remediation_a1.py",
        ):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(relative + "\n", encoding="utf-8")

    def test_plan_contains_only_existing_site_propagation(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo, include_a2=True)
            plan = build_a1_plan(repo)
            self.assertEqual(plan["payload"]["candidate_count"], 1)
            candidate = plan["payload"]["candidates"][0]
            self.assertEqual(candidate["canonical_game_id"], "CBBG-0000001")
            self.assertEqual(candidate["current_site_type"], "NEUTRAL")
            self.assertNotIn("site_type", candidate["patch"])
            self.assertEqual(candidate["patch"]["venue_id"], "VEN-000001")
            self.assertEqual(candidate["patch"]["site_city"], "Alpha City")

    def test_apply_requires_exact_sealed_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            with self.assertRaises(A1ApplyError):
                apply_a1_plan(repo, "not-the-plan", run_validation=False)
            row = read_rows(repo / "data/canonical/games.csv")[0]
            self.assertEqual(row["venue_id"], "")

    def test_apply_fills_only_blank_a1_fields_and_leaves_a2_site_unknown(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo, include_a2=True)
            plan = build_a1_plan(repo)
            result = apply_a1_plan(repo, plan["sha256"], run_validation=False)
            self.assertEqual(result["applied_games"], 1)
            rows = {row["canonical_game_id"]: row for row in read_rows(repo / "data/canonical/games.csv")}
            a1 = rows["CBBG-0000001"]
            self.assertEqual(a1["site_type"], "NEUTRAL")
            self.assertEqual(a1["venue_id"], "VEN-000001")
            self.assertEqual(a1["venue_key"], "example-arena")
            self.assertEqual((a1["site_city"], a1["site_state"]), ("Alpha City", "AA"))
            self.assertIn("VENUE_REGISTRY_FALLBACK", a1["notes"])
            a2 = rows["CBBG-0000002"]
            self.assertEqual(a2["site_type"], "UNKNOWN")
            self.assertEqual(a2["venue_id"], "")

    def test_second_plan_after_apply_has_no_a1_candidates(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            plan = build_a1_plan(repo)
            apply_a1_plan(repo, plan["sha256"], run_validation=False)
            post = build_a1_plan(repo)
            self.assertEqual(post["payload"]["candidate_count"], 0)


if __name__ == "__main__":
    unittest.main()
