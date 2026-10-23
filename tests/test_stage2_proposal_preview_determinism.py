import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

import sys
sys.path.insert(0, str(TOOLS))

import onboarding_hardening  # noqa: E402
import onboarding_plan  # noqa: E402


class Stage2ProposalPreviewDeterminismTests(unittest.TestCase):
    def write_empty_plan_and_review(self, root: Path):
        plan = root / "plan.json"
        review = root / "review.csv"
        plan.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workflow_version": 1,
                    "school_key": "example-school",
                    "input_fingerprint": {"sha256": "fixture-input"},
                    "blockers": [],
                    "warnings": [],
                    "summary": {},
                    "decisions": [],
                }
            )
            + "\n",
            encoding="utf-8",
        )
        review.write_text("decision_id\n", encoding="utf-8")
        return plan, review

    def test_explicit_approval_timestamp_stabilizes_preview_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan, review = self.write_empty_plan_and_review(root)
            with patch(
                "onboarding_plan.input_fingerprint",
                return_value={"sha256": "fixture-input"},
            ):
                first, first_hash = onboarding_plan.approve_plan(
                    root,
                    plan,
                    review,
                    "technical-readiness-preview",
                    approved_at="1970-01-01T00:00:00+00:00",
                )
                second, second_hash = onboarding_plan.approve_plan(
                    root,
                    plan,
                    review,
                    "technical-readiness-preview",
                    approved_at="1970-01-01T00:00:00+00:00",
                )
                changed, changed_hash = onboarding_plan.approve_plan(
                    root,
                    plan,
                    review,
                    "technical-readiness-preview",
                    approved_at="1970-01-01T00:00:01+00:00",
                )

            self.assertEqual(first_hash, second_hash)
            self.assertEqual(first["approval"], second["approval"])
            self.assertEqual(
                first["approval"]["approved_at"],
                onboarding_hardening.TECHNICAL_PREVIEW_APPROVED_AT,
            )
            self.assertNotEqual(first_hash, changed_hash)
            self.assertNotEqual(
                first["approval"]["approved_at"],
                changed["approval"]["approved_at"],
            )

    def test_validate_decision_map_preview_hash_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan, review = self.write_empty_plan_and_review(root)
            map_path = root / "map.json"
            map_path.write_text("{}\n", encoding="utf-8")

            with (
                patch("onboarding_hardening.onboard_school.ensure_package_checkpoint"),
                patch("onboarding_hardening.assert_no_unapproved_semantic_drift"),
                patch(
                    "onboarding_plan.input_fingerprint",
                    return_value={"sha256": "fixture-input"},
                ),
            ):
                first = onboarding_hardening.validate_decision_map(
                    root,
                    "example-school",
                    plan_path=plan,
                    review_path=review,
                    map_path=map_path,
                )
                second = onboarding_hardening.validate_decision_map(
                    root,
                    "example-school",
                    plan_path=plan,
                    review_path=review,
                    map_path=map_path,
                )

            self.assertEqual(
                first["approved_plan_hash_preview"],
                second["approved_plan_hash_preview"],
            )

    def test_rehearsal_uses_deterministic_preview_approval_metadata(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            plan, review = self.write_empty_plan_and_review(root)

            def fake_copy_repository(repo, rehearsal, *, school_key=None):
                rehearsal.mkdir(parents=True, exist_ok=True)

            with (
                patch("onboarding_hardening.onboard_school.ensure_package_checkpoint"),
                patch("onboarding_hardening.assert_no_unapproved_semantic_drift"),
                patch(
                    "onboarding_hardening.approve_plan",
                    return_value=({"school_key": "example-school"}, "preview-hash"),
                ) as approve,
                patch(
                    "onboarding_hardening.onboard_school.tree_hashes",
                    side_effect=[{}, {}],
                ),
                patch(
                    "onboarding_hardening.onboard_school.copy_repository",
                    side_effect=fake_copy_repository,
                ),
                patch(
                    "onboarding_hardening.onboard_school.execute_approved_in_place",
                    return_value={},
                ),
                patch(
                    "onboarding_hardening.onboard_school.changed_paths",
                    return_value=[],
                ),
                patch(
                    "onboarding_hardening.onboard_school.run_gates",
                    return_value={},
                ),
            ):
                result = onboarding_hardening.rehearse_review(
                    root,
                    "example-school",
                    plan_path=plan,
                    review_path=review,
                )

            self.assertEqual(result["approved_plan_hash_preview"], "preview-hash")
            approve.assert_called_once_with(
                root,
                plan,
                review,
                onboarding_hardening.TECHNICAL_PREVIEW_APPROVED_BY,
                approved_at=onboarding_hardening.TECHNICAL_PREVIEW_APPROVED_AT,
            )


if __name__ == "__main__":
    unittest.main()
