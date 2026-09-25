import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import implementation_stage2 as stage2  # noqa: E402
from onboarding_plan import WorkflowError  # noqa: E402


class ImplementationStage2CoordinatorTests(unittest.TestCase):
    def sample_plan(self):
        return {
            "blockers": [],
            "warnings": [],
            "summary": {
                "existing_game_matches": 10,
                "new_canonical_games": 2,
                "discrepancies_to_add": 3,
                "conditional_discrepancies": 1,
            },
            "decisions": [
                {
                    "decision_id": "DISCREPANCY-2",
                    "category": "discrepancy",
                    "field_name": "score",
                },
                {
                    "decision_id": "IDENTITY-1",
                    "category": "identity",
                    "field_name": "game_identity",
                },
            ],
        }

    def base_status(self):
        return {
            "schema_version": 1,
            "school_key": "test",
            "stage": "IMPLEMENTATION_STAGE_2",
            "status": "RUNNING",
            "branch": "data/test-onboarding",
            "head_sha": "abc123",
            "research_base_sha": "research",
            "integration_base_sha": "mainbase",
            "origin_main_sha_at_integration_freeze": "mainbase",
            "integration_semantic_sha256": "semantic",
        }

    def fake_write_preflight(self, root: Path):
        def _write(plan, output_dir):
            output_dir.mkdir(parents=True, exist_ok=True)
            plan_path = output_dir / "plan.json"
            review_path = output_dir / "review.csv"
            report_path = output_dir / "preflight.md"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            review_path.write_text("decision_id\n", encoding="utf-8")
            report_path.write_text("# preflight\n", encoding="utf-8")
            return {
                "plan": plan_path,
                "review": review_path,
                "report": report_path,
            }

        return _write

    def common_patches(self, root: Path, plan):
        return [
            patch.object(stage2, "_base_status", return_value=self.base_status()),
            patch.object(stage2.onboard_school, "ensure_package_checkpoint"),
            patch.object(
                stage2,
                "semantic_drift_report",
                return_value={"status": "PASS", "changes": []},
            ),
            patch.object(stage2, "build_plan", return_value=plan),
            patch.object(
                stage2,
                "write_preflight_artifacts",
                side_effect=self.fake_write_preflight(root),
            ),
        ]

    def test_decision_universe_hash_is_order_independent(self):
        plan = self.sample_plan()
        reversed_plan = dict(plan)
        reversed_plan["decisions"] = list(reversed(plan["decisions"]))
        self.assertEqual(
            stage2._decision_universe_sha256(plan),
            stage2._decision_universe_sha256(reversed_plan),
        )

    def test_preflight_only_writes_recovery_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan = self.sample_plan()
            patches = self.common_patches(root, plan)
            with patches[0], patches[1], patches[2], patches[3], patches[4]:
                code, status, status_path = stage2.run_stage2(root, "test")

            self.assertEqual(code, 0)
            self.assertEqual(status["status"], "CAPABILITY_CENSUS_READY")
            self.assertEqual(status["preflight"]["decision_count"], 2)
            self.assertTrue(status["preflight"]["decision_universe_sha256"])
            self.assertEqual(
                status["capability_census"]["status"],
                "CENSUS_CAPTURED",
            )
            census_path = root / ".onboarding/test/implementation-stage2-capability-census.json"
            self.assertTrue(census_path.is_file())
            census = json.loads(census_path.read_text(encoding="utf-8"))
            self.assertEqual(census["status"], "CENSUS_CAPTURED")
            self.assertEqual(
                census["preflight"]["decision_categories"]["discrepancy"],
                1,
            )
            self.assertTrue(status_path.is_file())
            persisted = json.loads(status_path.read_text(encoding="utf-8"))
            self.assertEqual(persisted["status"], "CAPABILITY_CENSUS_READY")

    def test_validated_map_and_rehearsal_reach_owner_gate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan = self.sample_plan()
            mapping = root / "recommendations.json"
            mapping.write_text('{"decisions": {}}\n', encoding="utf-8")
            patches = self.common_patches(root, plan)
            validation = {
                "action_counts": {
                    "MATCH_CANONICAL:CBBG-0000001": 1,
                    "KEEP_CANONICAL": 1,
                },
                "decision_count": 2,
                "approved_plan_hash_preview": "preview-hash",
            }
            rehearsal = {
                "approved_plan_hash_preview": "preview-hash",
                "changed_paths": ["data/canonical/games.csv"],
                "action_counts": validation["action_counts"],
            }

            with (
                patches[0],
                patches[1],
                patches[2],
                patches[3],
                patches[4],
                patch.object(
                    stage2,
                    "validate_decision_map",
                    return_value=validation,
                ),
                patch.object(
                    stage2,
                    "rehearse_decision_map",
                    return_value=rehearsal,
                ),
                patch.object(stage2, "_site_diagnostic", return_value=None),
            ):
                code, status, _ = stage2.run_stage2(
                    root,
                    "test",
                    map_path=mapping,
                )

            self.assertEqual(code, 0)
            self.assertEqual(status["status"], "OWNER_GATE_1_READY")
            self.assertEqual(status["recommendation_map"]["decision_count"], 2)
            self.assertEqual(
                status["recommendation_map"]["action_counts"][
                    "MATCH_CANONICAL:CBBG-0000001"
                ],
                1,
            )
            self.assertEqual(
                status["proposal_rehearsal"]["approved_plan_hash_preview"],
                "preview-hash",
            )
            self.assertEqual(status["capability_census"]["status"], "PASS")

    def test_failed_rehearsal_preserves_site_diagnostic_in_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan = self.sample_plan()
            mapping = root / "recommendations.json"
            mapping.write_text('{"decisions": {}}\n', encoding="utf-8")
            patches = self.common_patches(root, plan)
            validation = {
                "action_counts": {"KEEP_CANONICAL": 2},
                "decision_count": 2,
                "approved_plan_hash_preview": "preview-hash",
            }
            diagnostic = {
                "path": ".onboarding/test/last-rehearsal-site-gate.json",
                "status": "FAIL",
                "counts": {"unaccounted_public_gap_rows": 3},
                "examples": {"unaccounted_public_gap": ["CBBG-1"]},
                "errors": ["3 public gaps are unaccounted."],
            }

            with (
                patches[0],
                patches[1],
                patches[2],
                patches[3],
                patches[4],
                patch.object(
                    stage2,
                    "validate_decision_map",
                    return_value=validation,
                ),
                patch.object(
                    stage2,
                    "rehearse_decision_map",
                    side_effect=WorkflowError("implementation site completeness failed"),
                ),
                patch.object(
                    stage2,
                    "_site_diagnostic",
                    return_value=diagnostic,
                ),
            ):
                code, status, status_path = stage2.run_stage2(
                    root,
                    "test",
                    map_path=mapping,
                )

            self.assertEqual(code, 1)
            self.assertEqual(status["status"], "BLOCKED")
            self.assertEqual(
                status["site_diagnostic"]["counts"]["unaccounted_public_gap_rows"],
                3,
            )
            self.assertEqual(
                status["capability_census"]["status"],
                "REPAIR_SCOPE_REQUIRED",
            )
            census_path = root / ".onboarding/test/implementation-stage2-capability-census.json"
            census = json.loads(census_path.read_text(encoding="utf-8"))
            topologies = {
                row["topology"]: row["count"]
                for row in census["topology_groups"]
            }
            self.assertEqual(topologies["unaccounted_public_gap_rows"], 3)
            self.assertIn("consolidated repair scope", status["next_action"])
            self.assertTrue(status_path.is_file())


if __name__ == "__main__":
    unittest.main()
