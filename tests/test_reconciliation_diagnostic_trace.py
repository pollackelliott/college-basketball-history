import csv
import json
import shutil
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
import onboard_school  # noqa: E402
import onboarding_hardening  # noqa: E402
from onboarding_plan import WorkflowError, apply_reconciliation_decisions  # noqa: E402
from reconciliation_trace import ReconciliationTrace  # noqa: E402


class ReconciliationDiagnosticTraceTests(unittest.TestCase):
    def write_csv(self, path, fields, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def fixture(self, repo, *, include_site_decision):
        canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
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

        source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
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

        date_disc = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
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
        discrepancies = [date_disc]

        if include_site_decision:
            site_disc = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
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

    def test_trace_records_actual_decision_order_and_site_sync_branch(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.fixture(repo, include_site_decision=True)
            tracer = ReconciliationTrace("CBBG-1")

            with patch("onboarding_plan._venue_maps", return_value=({}, {})):
                with tracer:
                    counts = apply_reconciliation_decisions(repo, approved)

            self.assertEqual(counts["processed"], 2)
            self.assertEqual(
                [row["decision_id"] for row in tracer.document["decision_order"]],
                ["DATE-1", "SITE-1"],
            )
            self.assertEqual(len(tracer.document["site_sync_events"]), 1)
            self.assertEqual(
                tracer.document["site_sync_events"][0]["branch"],
                "SOURCE_LOCATION",
            )
            self.assertEqual(
                tracer.document["site_sync_events"][0]["canonical_after"]["site_state"],
                "CA",
            )
            self.assertEqual(
                tracer.document["partial_location_classification"],
                "FINAL_LOCATION_NOT_PARTIAL",
            )

    def test_trace_survives_final_partial_location_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.fixture(repo, include_site_decision=False)
            tracer = ReconciliationTrace("CBBG-1")

            with self.assertRaisesRegex(
                WorkflowError,
                "final reconciliation leaves partial canonical city/state",
            ):
                with tracer:
                    apply_reconciliation_decisions(repo, approved)

            self.assertEqual(
                tracer.document["integrity"]["status"],
                "FAIL",
            )
            self.assertEqual(
                tracer.document["partial_location_classification"],
                "PREEXISTING_PERSISTED",
            )
            self.assertEqual(
                tracer.document["canonical_last_observed"]["site_city"],
                "Los Angeles",
            )
            self.assertEqual(
                tracer.document["canonical_last_observed"]["site_state"],
                "",
            )

    def test_non_diagnostic_reconciliation_behavior_is_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.fixture(repo, include_site_decision=True)

            with patch("onboarding_plan._venue_maps", return_value=({}, {})):
                counts = apply_reconciliation_decisions(repo, approved)

            self.assertEqual(counts["processed"], 2)
            with (repo / "data/canonical/games.csv").open(encoding="utf-8") as handle:
                canonical = list(csv.DictReader(handle))[0]
            self.assertEqual(canonical["site_type"], "TEAM_B_HOME")
            self.assertEqual(canonical["site_city"], "Los Angeles")
            self.assertEqual(canonical["site_state"], "CA")

    def test_diagnostic_command_persists_trace_without_real_tracked_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / "repo"
            repo.mkdir()
            approved = self.fixture(repo, include_site_decision=False)
            output = repo / ".onboarding/usc"
            output.mkdir(parents=True)
            plan_path = output / "plan.json"
            review_path = output / "review.csv"
            map_path = repo / "recommendation-map.json"
            plan_path.write_text("{}\n", encoding="utf-8")
            review_path.write_text("decision_id,decision\n", encoding="utf-8")
            map_path.write_text("{}\n", encoding="utf-8")

            before = onboard_school.tree_hashes(repo)

            def copy_repository(source, target, *, school_key):
                self.assertEqual(school_key, "usc")
                shutil.copytree(source, target, dirs_exist_ok=True)

            def execute(rehearsal, sealed):
                self.assertEqual(sealed, approved)
                return {
                    "reconciliation": onboard_school.apply_reconciliation_decisions(
                        rehearsal, sealed
                    )
                }

            with (
                patch.object(onboard_school, "ensure_package_checkpoint"),
                patch.object(onboarding_hardening, "assert_no_unapproved_semantic_drift"),
                patch.object(
                    onboarding_hardening,
                    "fill_review_from_map",
                    return_value=Counter({"KEEP_CANONICAL": 1}),
                ),
                patch.object(
                    onboarding_hardening,
                    "approve_plan",
                    return_value=(approved, "b" * 64),
                ),
                patch.object(onboard_school, "git", return_value="deadbeef\n"),
                patch.object(onboard_school, "copy_repository", side_effect=copy_repository),
                patch.object(onboard_school, "execute_approved_in_place", side_effect=execute),
            ):
                result = onboarding_hardening.diagnose_reconciliation(
                    repo,
                    "usc",
                    plan_path=plan_path,
                    review_path=review_path,
                    map_path=map_path,
                    canonical_game_id="CBBG-1",
                )

            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["execution_status"], "RECONCILIATION_BLOCKED")
            self.assertTrue(result["real_tracked_repository_unchanged"])
            self.assertEqual(onboard_school.tree_hashes(repo), before)

            artifact = output / "last-rehearsal-reconciliation-trace.json"
            self.assertTrue(artifact.is_file())
            trace = json.loads(artifact.read_text(encoding="utf-8"))
            self.assertEqual(trace["diagnostic_status"], "PASS")
            self.assertEqual(
                trace["partial_location_classification"],
                "PREEXISTING_PERSISTED",
            )
            self.assertIn(
                "final reconciliation leaves partial canonical city/state",
                trace["execution_error"],
            )


if __name__ == "__main__":
    unittest.main()
