import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboard_school import (  # noqa: E402
    annotate_reciprocal_only_unknown_site_provenance,
    backfill_reciprocal_only_home_chronology,
    backfill_resolved_target_home_chronology,
)


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
    "normalized_opponent_key",
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

GLOBAL_VENUE_FIELDS = [
    "venue_id",
    "venue_key",
    "display_name",
    "city",
    "state",
]

DISCREPANCY_FIELDS = [
    "discrepancy_id",
    "canonical_game_id",
    "field_name",
    "source_a_program_key",
    "source_a_value",
    "canonical_value",
    "status",
    "resolution_basis",
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

    def test_unknown_target_site_assertion_allows_deterministic_home_chronology_backfill(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)

            write_csv(
                repo / "data/canonical/games.csv",
                CANONICAL_FIELDS,
                [{
                    "canonical_game_id": "CBBG-0000004",
                    "season_label": "1935-1936",
                    "game_date": "1936-02-04",
                    "team_a_key": "north-carolina",
                    "team_b_key": "cincinnati",
                    "site_type": "TEAM_B_HOME",
                    "designated_home_team_key": "cincinnati",
                }],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ASSERTION_FIELDS,
                [
                    {
                        "canonical_game_id": "CBBG-0000004",
                        "source_program_key": "north-carolina",
                        "source_game_id": "UNC-1",
                        "curated_site_type": "OPPONENT_HOME",
                    },
                    {
                        "canonical_game_id": "CBBG-0000004",
                        "source_program_key": "cincinnati",
                        "source_game_id": "CIN-1",
                        "curated_site_type": "UNKNOWN",
                    },
                ],
            )
            write_csv(
                repo / "schools/cincinnati/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [{
                    "venue_id": "VEN-000684",
                    "venue_key": "schmidlapp-gym",
                    "canonical_name": "Schmidlapp Gym",
                    "city": "Cincinnati",
                    "state": "OH",
                    "relationship_type": "source_program_home",
                    "relationship_start": "1911-1912",
                    "relationship_end": "1953-1954",
                    "source_basis": "documented home chronology",
                }],
            )
            write_csv(
                repo / "data/reference/venues.csv",
                GLOBAL_VENUE_FIELDS,
                [{
                    "venue_id": "VEN-000684",
                    "venue_key": "schmidlapp-gym",
                    "display_name": "Schmidlapp Gym",
                    "city": "Cincinnati",
                    "state": "OH",
                }],
            )

            result = backfill_reciprocal_only_home_chronology(repo, "cincinnati")
            self.assertEqual(result["applied_games"], 1)

            row = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(row["venue_id"], "VEN-000684")
            self.assertEqual(row["site_city"], "Cincinnati")

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
                        "curated_site_type": "SOURCE_PROGRAM_HOME",
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


    def test_resolved_target_site_conflict_backfills_canonical_only_from_home_chronology(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)

            write_csv(
                repo / "data/canonical/games.csv",
                CANONICAL_FIELDS,
                [{
                    "canonical_game_id": "CBBG-0000006",
                    "season_label": "1967-1968",
                    "game_date": "1968-02-19",
                    "team_a_key": "alpha",
                    "team_b_key": "beta",
                    "site_type": "TEAM_A_HOME",
                    "designated_home_team_key": "alpha",
                }],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ASSERTION_FIELDS,
                [
                    {
                        "canonical_game_id": "CBBG-0000006",
                        "source_program_key": "alpha",
                        "source_game_id": "ALPHA-1",
                        "normalized_opponent_key": "beta",
                        "curated_site_type": "OPPONENT_HOME",
                    },
                    {
                        "canonical_game_id": "CBBG-0000006",
                        "source_program_key": "beta",
                        "source_game_id": "BETA-1",
                        "normalized_opponent_key": "alpha",
                        "curated_site_type": "OPPONENT_HOME",
                    },
                ],
            )
            write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                DISCREPANCY_FIELDS,
                [{
                    "discrepancy_id": "DISC-1",
                    "canonical_game_id": "CBBG-0000006",
                    "field_name": "site_type",
                    "source_a_program_key": "alpha",
                    "source_a_value": "TEAM_B_HOME",
                    "canonical_value": "TEAM_A_HOME",
                    "status": "RESOLVED",
                    "resolution_basis": "Owner-confirmed canonical HOME classification.",
                }],
            )
            write_csv(
                repo / "schools/alpha/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [{
                    "venue_id": "VEN-000437",
                    "venue_key": "alpha-field-house",
                    "canonical_name": "Alpha Field House",
                    "city": "Alpha City",
                    "state": "AA",
                    "relationship_type": "PRIMARY_HOME",
                    "relationship_start": "1951-12-15",
                    "relationship_end": "2002-03-02",
                    "source_basis": "documented home chronology",
                }],
            )
            write_csv(
                repo / "data/reference/venues.csv",
                GLOBAL_VENUE_FIELDS,
                [{
                    "venue_id": "VEN-000437",
                    "venue_key": "alpha-field-house",
                    "display_name": "Alpha Field House",
                    "city": "Alpha City",
                    "state": "AA",
                }],
            )

            result = backfill_resolved_target_home_chronology(repo, "alpha")

            self.assertEqual(result["applied_games"], 1)
            row = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(row["site_type"], "TEAM_A_HOME")
            self.assertEqual(row["venue_id"], "VEN-000437")
            self.assertEqual(row["venue_key"], "alpha-field-house")
            self.assertEqual(row["site_city"], "Alpha City")
            self.assertEqual(row["site_state"], "AA")
            self.assertIn(
                "RESOLVED_TARGET_HOME_CHRONOLOGY_BACKFILL",
                row["notes"],
            )

            assertions = read_csv(repo / "data/evidence/game-assertions.csv")
            target = next(
                item for item in assertions
                if item["source_program_key"] == "alpha"
            )
            self.assertEqual(target["curated_site_type"], "OPPONENT_HOME")
            self.assertEqual(target["curated_venue_name"], "")
            self.assertEqual(target["city"], "")
            self.assertEqual(target["state"], "")

    def test_resolved_target_home_backfill_requires_resolved_site_discrepancy(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)

            write_csv(
                repo / "data/canonical/games.csv",
                CANONICAL_FIELDS,
                [{
                    "canonical_game_id": "CBBG-0000007",
                    "season_label": "1967-1968",
                    "game_date": "1968-02-19",
                    "team_a_key": "alpha",
                    "team_b_key": "beta",
                    "site_type": "TEAM_A_HOME",
                    "designated_home_team_key": "alpha",
                }],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ASSERTION_FIELDS,
                [{
                    "canonical_game_id": "CBBG-0000007",
                    "source_program_key": "alpha",
                    "source_game_id": "ALPHA-2",
                    "normalized_opponent_key": "beta",
                    "curated_site_type": "OPPONENT_HOME",
                }],
            )
            write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                DISCREPANCY_FIELDS,
                [{
                    "discrepancy_id": "DISC-2",
                    "canonical_game_id": "CBBG-0000007",
                    "field_name": "site_type",
                    "source_a_program_key": "alpha",
                    "source_a_value": "TEAM_B_HOME",
                    "canonical_value": "TEAM_A_HOME",
                    "status": "UNDER_REVIEW",
                    "resolution_basis": "",
                }],
            )
            write_csv(
                repo / "schools/alpha/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [{
                    "venue_id": "VEN-000437",
                    "venue_key": "alpha-field-house",
                    "canonical_name": "Alpha Field House",
                    "city": "Alpha City",
                    "state": "AA",
                    "relationship_type": "PRIMARY_HOME",
                    "relationship_start": "1951-12-15",
                    "relationship_end": "2002-03-02",
                    "source_basis": "documented home chronology",
                }],
            )
            write_csv(
                repo / "data/reference/venues.csv",
                GLOBAL_VENUE_FIELDS,
                [{
                    "venue_id": "VEN-000437",
                    "venue_key": "alpha-field-house",
                    "display_name": "Alpha Field House",
                    "city": "Alpha City",
                    "state": "AA",
                }],
            )

            result = backfill_resolved_target_home_chronology(repo, "alpha")

            self.assertEqual(result["applied_games"], 0)
            self.assertEqual(result["skipped_no_resolved_site_conflict"], 1)
            row = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(row["venue_id"], "")
            self.assertEqual(row["site_city"], "")


    def test_annotates_reciprocal_only_unknown_site_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)

            write_csv(
                repo / "data/canonical/games.csv",
                CANONICAL_FIELDS,
                [{
                    "canonical_game_id": "CBBG-0000005",
                    "season_label": "1907-1908",
                    "game_date": "",
                    "team_a_key": "auburn",
                    "team_b_key": "cincinnati",
                    "site_type": "UNKNOWN",
                    "designated_home_team_key": "",
                }],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ASSERTION_FIELDS,
                [{
                    "canonical_game_id": "CBBG-0000005",
                    "source_program_key": "auburn",
                    "source_game_id": "AUBRAW-1",
                    "curated_site_type": "UNKNOWN",
                }],
            )

            result = annotate_reciprocal_only_unknown_site_provenance(
                repo,
                "cincinnati",
            )

            self.assertEqual(result["annotated_games"], 1)
            row = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertIn(
                "RECIPROCAL_ONLY_UNKNOWN_SITE_PROVENANCE "
                "target=cincinnati reciprocal=auburn/AUBRAW-1",
                row["notes"],
            )



if __name__ == "__main__":
    unittest.main()
