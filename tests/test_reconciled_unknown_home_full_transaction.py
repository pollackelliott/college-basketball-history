import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
from implementation_site_gate import implementation_site_report  # noqa: E402
from onboard_school import backfill_reciprocal_only_home_chronology  # noqa: E402
from onboarding_plan import apply_reconciliation_decisions, read_csv_table  # noqa: E402


SOURCE_FIELDS = [
    "source_game_id",
    "source_program_key",
    "season_label",
    "game_date",
    "normalized_opponent_key",
    "normalized_opponent_name",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "site_research_status",
    "site_research_basis",
    "raw_text",
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
    "venue_type",
    "known_opened",
    "known_closed",
    "venue_date_precision",
    "games_currently_assigned",
    "first_assigned_game",
    "last_assigned_game",
    "relationship_type",
    "relationship_start",
    "relationship_end",
    "relationship_date_precision",
    "site_rule",
    "source_basis",
    "notes",
]


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_row(source_game_id: str, *, opponent: str = "other"):
    return {
        "source_game_id": source_game_id,
        "source_program_key": "test",
        "season_label": "1909-1910",
        "game_date": "1910-02-01",
        "normalized_opponent_key": opponent,
        "normalized_opponent_name": "Other",
        "team_score": "20",
        "opponent_score": "40",
        "played_result": "L",
        "overtime_periods": "0",
        "curated_site_type": "UNKNOWN",
        "curated_venue_name": "",
        "city": "",
        "state": "",
        "curated_game_type": "REGULAR_SEASON",
        "site_research_status": "RESEARCHED_UNRESOLVED",
        "site_research_basis": "Bounded H/A/N research remains unresolved.",
        "raw_text": "Historical score line.",
        "notes": "",
    }


def assertion_from_source(source: dict[str, str], game_id: str, assertion_id: str):
    row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
    for field in ingest_school.ASSERTION_FIELDS:
        if field in source:
            row[field] = source[field]
    row.update(
        {
            "assertion_id": assertion_id,
            "canonical_game_id": game_id,
            "match_status": "MATCHED",
            "match_method": "FIXTURE",
        }
    )
    return row


def reciprocal_assertion(
    game_id: str,
    source_game_id: str,
    *,
    source_program: str = "other",
):
    row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
    row.update(
        {
            "assertion_id": f"ASRT-{source_game_id}",
            "canonical_game_id": game_id,
            "source_program_key": source_program,
            "source_game_id": source_game_id,
            "season_label": "1909-1910",
            "game_date": "1910-02-01",
            "normalized_opponent_key": "test",
            "normalized_opponent_name": "Test",
            "team_score": "40",
            "opponent_score": "20",
            "played_result": "W",
            "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": "",
            "city": "",
            "state": "",
            "curated_game_type": "REGULAR_SEASON",
            "match_status": "MATCHED",
            "match_method": "FIXTURE",
        }
    )
    return row


def canonical_row(
    game_id: str,
    *,
    team_a: str,
    team_b: str,
    site_type: str,
    game_date: str = "1910-02-01",
):
    row = {field: "" for field in ingest_school.CANONICAL_FIELDS}
    row.update(
        {
            "canonical_game_id": game_id,
            "season_label": "1909-1910",
            "game_date": game_date,
            "date_precision": "EXACT",
            "team_a_key": team_a,
            "team_b_key": team_b,
            "team_a_score": "40",
            "team_b_score": "20",
            "result_winner_team_key": "other",
            "overtime_periods": "0",
            "site_type": site_type,
            "designated_home_team_key": "test",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "game_type": "REGULAR_SEASON",
            "canonical_status": "PROVISIONAL",
            "notes": "",
        }
    )
    return row


def discrepancy(game_id: str, decision_id: str, canonical_site: str):
    row = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
    row.update(
        {
            "discrepancy_id": decision_id,
            "canonical_game_id": game_id,
            "field_name": "site_type",
            "source_a_program_key": "test",
            "source_a_value": "UNKNOWN",
            "canonical_value": canonical_site,
            "status": "UNDER_REVIEW",
        }
    )
    return row


class ReconciledUnknownHomeFullTransactionTests(unittest.TestCase):
    def test_markers_survive_full_reconciliation_and_site_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)

            ordinary = source_row("TEST-ORDINARY")
            conditional = source_row("TEST-CONDITIONAL", opponent="zeta")
            canonical = [
                canonical_row(
                    "CBBG-ORDINARY",
                    team_a="other",
                    team_b="test",
                    site_type="TEAM_B_HOME",
                ),
                canonical_row(
                    "CBBG-CONDITIONAL",
                    team_a="test",
                    team_b="zeta",
                    site_type="TEAM_A_HOME",
                ),
                canonical_row(
                    "CBBG-BACKFILL",
                    team_a="other",
                    team_b="test",
                    site_type="TEAM_B_HOME",
                    game_date="1950-01-15",
                ),
            ]
            assertions = [
                assertion_from_source(ordinary, "CBBG-ORDINARY", "ASRT-TEST-ORDINARY"),
                reciprocal_assertion("CBBG-ORDINARY", "OTHER-ORDINARY"),
                assertion_from_source(
                    conditional, "CBBG-CONDITIONAL", "ASRT-TEST-CONDITIONAL"
                ),
                reciprocal_assertion(
                    "CBBG-CONDITIONAL", "ZETA-CONDITIONAL", source_program="zeta"
                ),
                reciprocal_assertion("CBBG-BACKFILL", "OTHER-BACKFILL"),
            ]
            discrepancies = [
                discrepancy("CBBG-ORDINARY", "DISC-ORDINARY", "TEAM_B_HOME"),
                discrepancy("CBBG-CONDITIONAL", "DISC-CONDITIONAL", "TEAM_A_HOME"),
            ]

            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                canonical,
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS,
                assertions,
            )
            write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS,
                discrepancies,
            )
            write_csv(
                repo / "schools/test/source-games.csv",
                SOURCE_FIELDS,
                [ordinary, conditional],
            )
            write_csv(
                repo / "schools/other/source-games.csv",
                SOURCE_FIELDS,
                [
                    {
                        **source_row("OTHER-ORDINARY", opponent="test"),
                        "source_program_key": "other",
                        "curated_site_type": "OPPONENT_HOME",
                        "site_research_status": "",
                        "site_research_basis": "",
                    },
                    {
                    {
                        **source_row("OTHER-BACKFILL", opponent="test"),
                        "source_program_key": "other",
                        "game_date": "1950-01-15",
                        "season_label": "1949-1950",
                        "curated_site_type": "OPPONENT_HOME",
                        "site_research_status": "",
                        "site_research_basis": "",
                    },
                ],
            )
            write_csv(
                repo / "schools/zeta/source-games.csv",
                SOURCE_FIELDS,
                [
                    {
                        **source_row("ZETA-CONDITIONAL", opponent="test"),
                        "source_program_key": "zeta",
                        "curated_site_type": "OPPONENT_HOME",
                        "site_research_status": "",
                        "site_research_basis": "",
                    }
                ],
            )
            write_csv(
                repo / "data/reference/programs.csv",
                ["program_key", "history_start_season", "history_scope_intervals"],
                [
                    {
                        "program_key": "test",
                        "history_start_season": "1900-1901",
                        "history_scope_intervals": "",
                    }
                ],
            )
            write_csv(
                repo / "schools/test/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [
                    {
                        "source_program_key": "test",
                        "venue_key": "example-fieldhouse",
                        "venue_id": "VEN-999999",
                        "canonical_name": "Example Fieldhouse",
                        "aliases": "",
                        "city": "Example City",
                        "state": "EX",
                        "venue_type": "arena",
                        "known_opened": "1940",
                        "known_closed": "1960",
                        "venue_date_precision": "year",
                        "games_currently_assigned": "1",
                        "first_assigned_game": "1950-01-15",
                        "last_assigned_game": "1950-01-15",
                        "relationship_type": "HOME",
                        "relationship_start": "1940-01-01",
                        "relationship_end": "1960-12-31",
                        "relationship_date_precision": "day",
                        "site_rule": "HOME only after independent H/A/N classification.",
                        "source_basis": "Regression fixture.",
                        "notes": "",
                    }
                ],
            )
            write_csv(
                repo / "data/reference/venues.csv",
                ["venue_id", "venue_key", "display_name", "city", "state"],
                [
                    {
                        "venue_id": "VEN-999999",
                        "venue_key": "example-fieldhouse",
                        "display_name": "Example Fieldhouse",
                        "city": "Example City",
                        "state": "EX",
                    }
                ],
            )

            approved = {
                "school_key": "test",
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": "SITE-ORDINARY",
                        "category": "discrepancy",
                        "source_game_id": "TEST-ORDINARY",
                        "canonical_game_id": "CBBG-ORDINARY",
                        "field_name": "site_type",
                        "source_value": "UNKNOWN",
                        "canonical_value": "TEAM_B_HOME",
                        "decision": "KEEP_CANONICAL",
                        "resolution_basis": "Reciprocal source establishes canonical HOME.",
                        "canonical_patch": {
                            "site_city": "Example City",
                            "site_state": "EX",
                        },
                        "source_patch": {},
                    },
                    {
                        "decision_id": "SITE-CONDITIONAL",
                        "category": "discrepancy",
                        "conditional_identity_satisfied": True,
                        "source_game_id": "TEST-CONDITIONAL",
                        "canonical_game_id": "CBBG-CONDITIONAL",
                        "field_name": "site_type",
                        "source_value": "UNKNOWN",
                        "canonical_value": "TEAM_A_HOME",
                        "decision": "KEEP_CANONICAL",
                        "resolution_basis": "Selected identity reciprocal source establishes HOME.",
                        "canonical_patch": {
                            "site_city": "Example City",
                            "site_state": "EX",
                        },
                        "source_patch": {},
                    },
                ],
            }

            first = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(
                first["reconciled_unknown_site_home_venue_markers_added"],
                2,
            )

            _, first_rows = read_csv_table(repo / "data/canonical/games.csv")
            by_id = {row["canonical_game_id"]: row for row in first_rows}
            for game_id, source_id, reciprocal_id in (
                ("CBBG-ORDINARY", "TEST-ORDINARY", "OTHER-ORDINARY"),
                ("CBBG-CONDITIONAL", "TEST-CONDITIONAL", "ZETA-CONDITIONAL"),
            ):
                marker = (
                    "[RECONCILED_UNKNOWN_SITE_HOME_VENUE "
                    f"source=test/{source_id} reciprocal={'zeta' if 'CONDITIONAL' in game_id else 'other'}/{reciprocal_id}]"
                )
                row = by_id[game_id]
                self.assertEqual(row["venue_key"], "")
                self.assertEqual(row["venue_id"], "")
                self.assertEqual(row["site_city"], "Example City")
                self.assertEqual(row["site_state"], "EX")
                self.assertEqual(row["notes"].count(marker), 1)

            second = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(
                second["reconciled_unknown_site_home_venue_markers_existing"],
                2,
            )

            rewrite = backfill_reciprocal_only_home_chronology(repo, "test")
            self.assertEqual(rewrite["applied_games"], 1)

            _, rewritten_rows = read_csv_table(repo / "data/canonical/games.csv")
            rewritten = {row["canonical_game_id"]: row for row in rewritten_rows}
            for game_id, source_id, reciprocal_id in (
                ("CBBG-ORDINARY", "TEST-ORDINARY", "OTHER-ORDINARY"),
                ("CBBG-CONDITIONAL", "TEST-CONDITIONAL", "OTHER-CONDITIONAL"),
            ):
                marker = (
                    "[RECONCILED_UNKNOWN_SITE_HOME_VENUE "
                    f"source=test/{source_id} reciprocal=other/{reciprocal_id}]"
                )
                self.assertEqual(rewritten[game_id]["notes"].count(marker), 1)

            self.assertEqual(
                rewritten["CBBG-BACKFILL"]["venue_key"],
                "example-fieldhouse",
            )
            self.assertEqual(
                rewritten["CBBG-BACKFILL"]["venue_id"],
                "VEN-999999",
            )

            report = implementation_site_report(repo, "test")
            self.assertEqual(report["status"], "PASS", report)
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 0)
            self.assertEqual(
                report["counts"][
                    "reconciled_unknown_site_unresolved_home_venue"
                ],
                2,
            )


if __name__ == "__main__":
    unittest.main()
