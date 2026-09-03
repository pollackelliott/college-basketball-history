import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    WorkflowError,
    apply_reconciliation_decisions,
)


class ReconciliationLocationFinalStateTests(unittest.TestCase):
    def write_csv(self, path, fields, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def fixture(self, repo, include_site_decision):
        canonical = {
            field: "" for field in ingest_school.CANONICAL_FIELDS
        }
        canonical.update(
            {
                "canonical_game_id": "CBBG-1",
                "season_label": "1967-1968",
                "game_date": "1967-12-28",
                "date_precision": "EXACT",
                "team_a_key": "tennessee",
                "team_b_key": "usc",
                "team_a_score": "78",
                "team_b_score": "68",
                "result_winner_team_key": "tennessee",
                "overtime_periods": "0",
                "site_type": "NEUTRAL",
                "designated_home_team_key": "",
                "site_city": "Los Angeles",
                "site_state": "",
                "game_type": "REGULAR_SEASON",
                "canonical_status": "PROVISIONAL",
            }
        )

        source = {
            field: "" for field in ingest_school.ASSERTION_FIELDS
        }
        source.update(
            {
                "source_program_key": "usc",
                "source_game_id": "USC-1",
                "season_label": "1967-1968",
                "game_date": "1967-12-29",
                "normalized_opponent_key": "tennessee",
                "normalized_opponent_name": "Tennessee",
                "team_score": "68",
                "opponent_score": "78",
                "played_result": "L",
                "overtime_periods": "0",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "city": "Los Angeles",
                "state": "CA",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "USC vs Tennessee",
            }
        )

        assertion = dict(source)
        assertion.update(
            {
                "assertion_id": "ASRT-USC-1",
                "canonical_game_id": "CBBG-1",
                "match_status": "MATCHED",
                "match_method": "FIXTURE",
            }
        )

        date_disc = {
            field: "" for field in ingest_school.DISCREPANCY_FIELDS
        }
        date_disc.update(
            {
                "discrepancy_id": "DISC-1",
                "canonical_game_id": "CBBG-1",
                "field_name": "game_date",
                "source_a_program_key": "usc",
                "source_a_value": "1967-12-29",
                "canonical_value": "1967-12-28",
                "status": "UNDER_REVIEW",
            }
        )

        discrepancies = [date_disc]

        decisions = [
            {
                "decision_id": "DATE-1",
                "category": "discrepancy",
                "source_game_id": "USC-1",
                "canonical_game_id": "CBBG-1",
                "field_name": "game_date",
                "source_value": "1967-12-29",
                "canonical_value": "1967-12-28",
                "decision": "KEEP_CANONICAL",
                "resolution_basis": "Fixture keeps reciprocal date.",
                "canonical_patch": {},
                "source_patch": {},
            }
        ]

        if include_site_decision:
            site_disc = {
                field: "" for field in ingest_school.DISCREPANCY_FIELDS
            }
            site_disc.update(
                {
                    "discrepancy_id": "DISC-2",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "site_type",
                    "source_a_program_key": "usc",
                    "source_a_value": "TEAM_B_HOME",
                    "canonical_value": "NEUTRAL",
                    "status": "UNDER_REVIEW",
                }
            )
            discrepancies.append(site_disc)

            decisions.append(
                {
                    "decision_id": "SITE-1",
                    "category": "discrepancy",
                    "source_game_id": "USC-1",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "site_type",
                    "source_value": "TEAM_B_HOME",
                    "canonical_value": "NEUTRAL",
                    "decision": "USE_SOURCE",
                    "resolution_basis": "Fixture uses completed USC site evidence.",
                    "canonical_patch": {},
                    "source_patch": {},
                }
            )

        self.write_csv(
            repo / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS,
            [canonical],
        )
        self.write_csv(
            repo / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS,
            [assertion],
        )
        self.write_csv(
            repo / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            discrepancies,
        )
        self.write_csv(
            repo / "schools/usc/source-games.csv",
            ingest_school.ASSERTION_FIELDS,
            [source],
        )

        return {
            "school_key": "usc",
            "approved_plan_hash": "a" * 64,
            "decisions": decisions,
        }

    def read_one(self, path):
        with path.open(encoding="utf-8") as handle:
            return list(csv.DictReader(handle))[0]

    def test_later_site_decision_may_complete_intermediate_partial_location(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.fixture(
                repo,
                include_site_decision=True,
            )

            with patch(
                "onboarding_plan._venue_maps",
                return_value=({}, {}),
            ):
                counts = apply_reconciliation_decisions(
                    repo,
                    approved,
                )

            self.assertEqual(counts["processed"], 2)
            self.assertEqual(counts["canonical_changes"], 1)

            canonical = self.read_one(
                repo / "data/canonical/games.csv"
            )
            self.assertEqual(
                canonical["site_type"],
                "TEAM_B_HOME",
            )
            self.assertEqual(
                canonical["site_city"],
                "Los Angeles",
            )
            self.assertEqual(
                canonical["site_state"],
                "CA",
            )

    def test_final_partial_location_still_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.fixture(
                repo,
                include_site_decision=False,
            )

            with self.assertRaisesRegex(
                WorkflowError,
                "final reconciliation leaves partial canonical city/state",
            ):
                apply_reconciliation_decisions(
                    repo,
                    approved,
                )


if __name__ == "__main__":
    unittest.main()
