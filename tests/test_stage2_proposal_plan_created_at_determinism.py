import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"

import sys
sys.path.insert(0, str(TOOLS))

import onboarding_plan  # noqa: E402


class Stage2ProposalPlanCreatedAtDeterminismTests(unittest.TestCase):
    def write_plan_and_review(self, root: Path, created_at: str):
        root.mkdir(parents=True, exist_ok=True)
        plan = root / "plan.json"
        review = root / "review.csv"
        plan.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "workflow_version": 1,
                    "school_key": "example-school",
                    "created_at": created_at,
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

    def test_technical_preview_hash_ignores_preflight_created_at(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first_plan, first_review = self.write_plan_and_review(
                root / "first",
                "2026-10-24T01:26:20.598620+00:00",
            )
            second_plan, second_review = self.write_plan_and_review(
                root / "second",
                "2026-10-24T01:27:40.123456+00:00",
            )
            with patch(
                "onboarding_plan.input_fingerprint",
                return_value={"sha256": "fixture-input"},
            ):
                first, first_hash = onboarding_plan.approve_plan(
                    root,
                    first_plan,
                    first_review,
                    "technical-readiness-preview",
                    approved_at="1970-01-01T00:00:00+00:00",
                )
                second, second_hash = onboarding_plan.approve_plan(
                    root,
                    second_plan,
                    second_review,
                    "technical-readiness-preview",
                    approved_at="1970-01-01T00:00:00+00:00",
                )

            self.assertEqual(first_hash, second_hash)
            self.assertEqual(
                first["created_at"],
                "1970-01-01T00:00:00+00:00",
            )
            self.assertEqual(first["created_at"], second["created_at"])

    def test_owner_approval_preserves_plan_created_at(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first_plan, first_review = self.write_plan_and_review(
                root / "first",
                "2026-10-24T01:26:20.598620+00:00",
            )
            second_plan, second_review = self.write_plan_and_review(
                root / "second",
                "2026-10-24T01:27:40.123456+00:00",
            )
            with patch(
                "onboarding_plan.input_fingerprint",
                return_value={"sha256": "fixture-input"},
            ):
                first, first_hash = onboarding_plan.approve_plan(
                    root,
                    first_plan,
                    first_review,
                    "Elliott",
                    approved_at="2026-10-24T02:00:00+00:00",
                )
                second, second_hash = onboarding_plan.approve_plan(
                    root,
                    second_plan,
                    second_review,
                    "Elliott",
                    approved_at="2026-10-24T02:00:00+00:00",
                )

            self.assertNotEqual(first_hash, second_hash)
            self.assertEqual(
                first["created_at"],
                "2026-10-24T01:26:20.598620+00:00",
            )
            self.assertEqual(
                second["created_at"],
                "2026-10-24T01:27:40.123456+00:00",
            )


if __name__ == "__main__":
    unittest.main()
