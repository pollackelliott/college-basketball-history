import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboard_school import backfill_reciprocal_only_home_chronology  # noqa: E402


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "site_type",
    "designated_home_team_key",
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

GLOBAL_VENUE_FIELDS = [
    "venue_id",
    "venue_key",
    "display_name",
    "city",
    "state",
]


class ReciprocalOnlyHomeChronologyTests(unittest.TestCase):
    def test_backfills_exact_date_and_season_only_reciprocal_home_games(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)

            write_csv(
                repo / "data/canonical/games.csv",
                CANONICAL_FIELDS,
                [
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "season_label": "2002-2003",
                        "game_date": "2003-02-09",
                        "team_a_key": "cincinnati",
                        "team_b_key": "oklahoma-state",
                        "site_type": "TEAM_A_HOME",
                        "designated_home_team_key": "cincinnati",
                    },
                    {
                        "canonical_game_id": "CBBG-0000002",
                        "season_label": "1901-1902",
                        "game_date": "",
                        "team_a_key": "cincinnati",
                        "team_b_key": "purdue",
                        "site_type": "TEAM_A_HOME",
                        "designated_home_team_key": "cincinnati",
                    },
                ],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ASSERTION_FIELDS,
                [
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "source_program_key": "oklahoma-state",
                        "source_game_id": "OKSTRAW-1",
                    },
                    {
                        "canonical_game_id": "CBBG-0000002",
                        "source_program_key": "purdue",
                        "source_game_id": "PURRAW-1",
                    },
                ],
            )
            write_csv(
                repo / "schools/cincinnati/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [
                    {
                        "venue_id": "VEN-000350",
                        "venue_key": "fifth-third-arena",
                        "canonical_name": "Fifth Third Arena",
                        "city": "Cincinnati",
                        "state": "OH",
                        "relationship_type": "source_program_home",
                        "relationship_start": "1989-1990",
                        "relationship_end": "2025-2026",
                        "source_basis": "documented modern home chronology",
                    },
                    {
                        "venue_id": "VEN-000681",
                        "venue_key": "mcmicken-gym",
                        "canonical_name": "McMicken Gym",
                        "city": "Cincinnati",
                        "state": "OH",
                        "relationship_type": "source_program_home",
                        "relationship_start": "1901-1902",
                        "relationship_end": "1910-1911",
                        "source_basis": "documented early home chronology",
                    },
                ],
            )
            write_csv(
                repo / "data/reference/venues.csv",
                GLOBAL_VENUE_FIELDS,
                [
                    {
                        "venue_id": "VEN-000350",
                        "venue_key": "fifth-third-arena",
                        "display_name": "Fifth Third Arena",
                        "city": "Cincinnati",
                        "state": "OH",
                    },
                    {
                        "venue_id": "VEN-000681",
                        "venue_key": "mcmicken-gym",
                        "display_name": "McMicken Gym",
                        "city": "Cincinnati",
                        "state": "OH",
                    },
                ],
            )

            result = backfill_reciprocal_only_home_chronology(repo, "cincinnati")

            self.assertEqual(result["applied_games"], 2)
            self.assertEqual(result["exact_date_matches"], 1)
            self.assertEqual(result["season_only_matches"], 1)

            rows = {
                row["canonical_game_id"]: row
                for row in read_csv(repo / "data/canonical/games.csv")
            }

            modern = rows["CBBG-0000001"]
            self.assertEqual(modern["venue_id"], "VEN-000350")
            self.assertEqual(modern["venue_key"], "fifth-third-arena")
            self.assertEqual(modern["site_city"], "Cincinnati")
            self.assertEqual(modern["site_state"], "OH")
            self.assertIn(
                "RECIPROCAL_ONLY_HOME_CHRONOLOGY_BACKFILL",
                modern["notes"],
            )

            early = rows["CBBG-0000002"]
            self.assertEqual(early["venue_id"], "VEN-000681")
            self.assertEqual(early["venue_key"], "mcmicken-gym")
            self.assertEqual(early["site_city"], "Cincinnati")
            self.assertEqual(early["site_state"], "OH")

    def test_target_school_assertion_prevents_reciprocal_only_backfill(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)

            write_csv(
                repo / "data/canonical/games.csv",
                CANONICAL_FIELDS,
                [
                    {
                        "canonical_game_id": "CBBG-0000003",
                        "season_label": "1922-1923",
                        "game_date": "1923-02-05",
                        "team_a_key": "cincinnati",
                        "team_b_key": "kentucky",
                        "site_type": "TEAM_A_HOME",
                        "designated_home_team_key": "cincinnati",
                    },
                ],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ASSERTION_FIELDS,
                [
                    {
                        "canonical_game_id": "CBBG-0000003",
                        "source_program_key": "kentucky",
                        "source_game_id": "KYRAW-1",
                    },
                    {
                        "canonical_game_id": "CBBG-0000003",
                        "source_program_key": "cincinnati",
                        "source_game_id": "CIN-STG1-1",
                    },
                ],
            )
            write_csv(
                repo / "schools/cincinnati/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [
                    {
                        "venue_id": "VEN-000684",
                        "venue_key": "schmidlapp-gym",
                        "canonical_name": "Schmidlapp Gym",
                        "city": "Cincinnati",
                        "state": "OH",
                        "relationship_type": "source_program_home",
                        "relationship_start": "1911-1912",
                        "relationship_end": "1953-1954",
                        "source_basis": "documented home chronology",
                    },
                ],
            )
            write_csv(
                repo / "data/reference/venues.csv",
                GLOBAL_VENUE_FIELDS,
                [
                    {
                        "venue_id": "VEN-000684",
                        "venue_key": "schmidlapp-gym",
                        "display_name": "Schmidlapp Gym",
                        "city": "Cincinnati",
                        "state": "OH",
                    },
                ],
            )

            result = backfill_reciprocal_only_home_chronology(repo, "cincinnati")
            self.assertEqual(result["applied_games"], 0)

            row = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(row["venue_id"], "")
            self.assertEqual(row["site_city"], "")


if __name__ == "__main__":
    unittest.main()
