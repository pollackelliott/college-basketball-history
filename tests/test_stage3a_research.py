import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from stage3a_research import (  # noqa: E402
    canonical_neutral_lookup,
    validate_stage3a_state,
)


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


STAGE3A_FIELDS = [
    "research_game_id",
    "season_label",
    "game_date",
    "normalized_opponent_key",
    "stage3a_disposition",
    "stage3a_han",
    "stage3a_han_basis",
    "stage3a_venue",
    "stage3a_city",
    "stage3a_state",
    "site_research_status",
    "site_research_basis",
    "stage3a_next_action",
]


class Stage3AStateValidationTests(unittest.TestCase):
    def make_stage1(self, root: Path):
        write_csv(
            root / "stage1.csv",
            ["research_game_id"],
            [{"research_game_id": f"TEST-{i}"} for i in range(1, 6)],
        )

    def make_ledger(self, root: Path):
        rows = [
            {
                "research_game_id": "TEST-1",
                "season_label": "1932-1933",
                "game_date": "1933-01-10",
                "normalized_opponent_key": "alpha",
                "stage3a_disposition": "REGULAR_SEASON",
                "stage3a_han": "HOME",
                "stage3a_han_basis": "institutional schedule",
                "stage3a_venue": "Home Gym",
                "stage3a_city": "Testville",
                "stage3a_state": "TX",
                "site_research_status": "RESEARCHED",
                "site_research_basis": "facility chronology",
                "stage3a_next_action": "COMPLETE",
            },
            {
                "research_game_id": "TEST-2",
                "season_label": "1932-1933",
                "game_date": "1933-02-10",
                "normalized_opponent_key": "beta",
                "stage3a_disposition": "REGULAR_SEASON",
                "stage3a_han": "HOME",
                "stage3a_han_basis": "institutional schedule",
                "stage3a_venue": "",
                "stage3a_city": "Testville",
                "stage3a_state": "TX",
                "site_research_status": "RESEARCHED_UNRESOLVED_HOME_VENUE",
                "site_research_basis": "institutional and archival evidence exhausted",
                "stage3a_next_action": "TERMINAL_RESEARCHED_DEBT",
            },
            {
                "research_game_id": "TEST-3",
                "season_label": "2025-2026",
                "game_date": "2025-12-20",
                "normalized_opponent_key": "gamma",
                "stage3a_disposition": "REGULAR_SEASON",
                "stage3a_han": "NEUTRAL",
                "stage3a_han_basis": "event record",
                "stage3a_venue": "Neutral Arena",
                "stage3a_city": "Neutral City",
                "stage3a_state": "NC",
                "site_research_status": "RESEARCHED",
                "site_research_basis": "official event site",
                "stage3a_next_action": "COMPLETE",
            },
            {
                "research_game_id": "TEST-4",
                "season_label": "2025-2026",
                "game_date": "2026-01-10",
                "normalized_opponent_key": "delta",
                "stage3a_disposition": "REGULAR_SEASON",
                "stage3a_han": "OPPONENT_HOME",
                "stage3a_han_basis": "source at-marker",
                "stage3a_venue": "",
                "stage3a_city": "",
                "stage3a_state": "",
                "site_research_status": "",
                "site_research_basis": "",
                "stage3a_next_action": "NO_SOURCE_SCHOOL_VENUE_RESEARCH",
            },
            {
                "research_game_id": "TEST-5",
                "season_label": "2025-2026",
                "game_date": "2026-03-20",
                "normalized_opponent_key": "epsilon",
                "stage3a_disposition": "POSTSEASON_HANDOFF",
                "stage3a_han": "",
                "stage3a_han_basis": "",
                "stage3a_venue": "",
                "stage3a_city": "",
                "stage3a_state": "",
                "site_research_status": "",
                "site_research_basis": "",
                "stage3a_next_action": "POSTSEASON_HANDOFF",
            },
        ]
        write_csv(root / "stage3a.csv", STAGE3A_FIELDS, rows)

    def test_complete_stage3a_state_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_stage1(root)
            self.make_ledger(root)
            write_csv(
                root / "postseason.csv",
                ["research_game_id"],
                [{"research_game_id": "TEST-5"}],
            )

            report = validate_stage3a_state(
                root / "stage3a.csv",
                stage1_path=root / "stage1.csv",
                postseason_path=root / "postseason.csv",
                phase="complete",
            )

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["regular_season_rows"], 4)
            self.assertEqual(report["counts"]["postseason_handoff_rows"], 1)
            self.assertEqual(
                report["counts"]["han"],
                {"HOME": 2, "NEUTRAL": 1, "OPPONENT_HOME": 1},
            )
            self.assertEqual(report["counts"]["home_terminal_debt_rows"], 1)

    def test_active_action_blocks_completion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_stage1(root)
            self.make_ledger(root)
            rows = list(csv.DictReader((root / "stage3a.csv").open()))
            rows[2]["stage3a_next_action"] = "RESEARCH_MODERN_NEUTRAL"
            write_csv(root / "stage3a.csv", STAGE3A_FIELDS, rows)

            report = validate_stage3a_state(
                root / "stage3a.csv",
                stage1_path=root / "stage1.csv",
                phase="complete",
            )

            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(
                any(
                    "active/nonterminal next actions" in error
                    or "completed NEUTRAL row has nonterminal" in error
                    for error in report["errors"]
                )
            )

    def test_unaccounted_neutral_gap_blocks_completion(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_stage1(root)
            self.make_ledger(root)
            rows = list(csv.DictReader((root / "stage3a.csv").open()))
            rows[2]["stage3a_venue"] = ""
            rows[2]["stage3a_city"] = ""
            rows[2]["stage3a_state"] = ""
            rows[2]["site_research_status"] = ""
            rows[2]["site_research_basis"] = ""
            rows[2]["stage3a_next_action"] = "TERMINAL_RESEARCHED_DEBT"
            write_csv(root / "stage3a.csv", STAGE3A_FIELDS, rows)

            report = validate_stage3a_state(
                root / "stage3a.csv",
                stage1_path=root / "stage1.csv",
                phase="complete",
            )

            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(
                any(
                    "blank NEUTRAL venue requires" in error
                    for error in report["errors"]
                )
            )

    def test_postseason_set_must_match_exactly(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_stage1(root)
            self.make_ledger(root)
            write_csv(
                root / "postseason.csv",
                ["research_game_id"],
                [{"research_game_id": "TEST-4"}],
            )

            report = validate_stage3a_state(
                root / "stage3a.csv",
                stage1_path=root / "stage1.csv",
                postseason_path=root / "postseason.csv",
                phase="complete",
            )

            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(
                any("does not exactly equal" in error for error in report["errors"])
            )


class CanonicalNeutralLookupTests(unittest.TestCase):
    def test_lookup_surfaces_venue_and_han_contradiction_without_applying(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_csv(
                root / "ledger.csv",
                STAGE3A_FIELDS,
                [
                    {
                        "research_game_id": "TEST-1",
                        "season_label": "1994-1995",
                        "game_date": "1994-12-20",
                        "normalized_opponent_key": "opponent",
                        "stage3a_disposition": "REGULAR_SEASON",
                        "stage3a_han": "NEUTRAL",
                        "stage3a_han_basis": "source ledger",
                        "stage3a_venue": "",
                        "stage3a_city": "",
                        "stage3a_state": "",
                        "site_research_status": "",
                        "site_research_basis": "",
                        "stage3a_next_action": "RESEARCH_MODERN_NEUTRAL",
                    }
                ],
            )
            write_csv(
                root / "games.csv",
                [
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
                ],
                [
                    {
                        "canonical_game_id": "CBBG-1",
                        "season_label": "1994-1995",
                        "game_date": "1994-12-20",
                        "team_a_key": "test",
                        "team_b_key": "opponent",
                        "site_type": "TEAM_A_HOME",
                        "designated_home_team_key": "test",
                        "venue_key": "example-arena",
                        "venue_id": "VEN-1",
                        "site_city": "Example City",
                        "site_state": "EX",
                    }
                ],
            )
            write_csv(
                root / "venues.csv",
                ["venue_id", "venue_key", "display_name", "city", "state"],
                [
                    {
                        "venue_id": "VEN-1",
                        "venue_key": "example-arena",
                        "display_name": "Example Arena",
                        "city": "Example City",
                        "state": "EX",
                    }
                ],
            )
            write_csv(
                root / "assertions.csv",
                [
                    "canonical_game_id",
                    "source_program_key",
                    "source_game_id",
                    "curated_site_type",
                    "source_site_candidate",
                    "curated_venue_name",
                    "source_venue_name",
                    "city",
                    "state",
                ],
                [
                    {
                        "canonical_game_id": "CBBG-1",
                        "source_program_key": "opponent",
                        "source_game_id": "OPP-1",
                        "curated_site_type": "OPPONENT_HOME",
                        "source_site_candidate": "",
                        "curated_venue_name": "Example Arena",
                        "source_venue_name": "",
                        "city": "Example City",
                        "state": "EX",
                    }
                ],
            )

            report = canonical_neutral_lookup(
                root / "ledger.csv",
                source_program_key="test",
                output_path=root / "lookup.csv",
                canonical_games_path=root / "games.csv",
                assertions_path=root / "assertions.csv",
                venues_path=root / "venues.csv",
            )

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(
                report["lookup_status_counts"],
                {"EXACT_GAME_HAN_CONTRADICTION": 1},
            )
            row = next(csv.DictReader((root / "lookup.csv").open()))
            self.assertEqual(row["canonical_venue_names"], "Example Arena")
            self.assertEqual(row["canonical_target_han"], "HOME")
            reciprocal = json.loads(row["reciprocal_venue_candidates"])
            self.assertEqual(reciprocal[0]["source_program_key"], "opponent")


if __name__ == "__main__":
    unittest.main()
