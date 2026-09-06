import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import onboarding_plan
import opponent_identity_remediation


class CurrentD1OpponentKeyGuardTests(unittest.TestCase):
    def setUp(self):
        self.programs = [
            {
                "program_key": "uconn",
                "current_d1": "Yes",
            },
            {
                "program_key": "historical-program",
                "current_d1": "No",
            },
        ]

    def test_true_package_key_must_exist_in_current_d1_registry(self):
        opponents = [
            {
                "canonical_opponent_key": "connecticut",
                "current_d1": "TRUE",
            }
        ]

        errors = onboarding_plan.current_d1_opponent_key_errors(
            self.programs,
            opponents,
        )

        self.assertEqual(len(errors), 1)
        self.assertIn("absent from programs.csv", errors[0])

    def test_registry_current_d1_key_requires_package_current_flag(self):
        opponents = [
            {
                "canonical_opponent_key": "uconn",
                "current_d1": "FALSE",
            }
        ]

        errors = onboarding_plan.current_d1_opponent_key_errors(
            self.programs,
            opponents,
        )

        self.assertEqual(len(errors), 1)
        self.assertIn("current D1 in programs.csv", errors[0])

    def test_true_false_and_yes_no_are_both_supported(self):
        self.assertTrue(opponent_identity_remediation.yes("TRUE"))
        self.assertTrue(opponent_identity_remediation.yes("Yes"))
        self.assertFalse(opponent_identity_remediation.yes("FALSE"))
        self.assertFalse(opponent_identity_remediation.yes("No"))

        opponents = [
            {
                "canonical_opponent_key": "uconn",
                "current_d1": "TRUE",
            },
            {
                "canonical_opponent_key": "historical-program",
                "current_d1": "FALSE",
            },
            {
                "canonical_opponent_key": "non-d1-local-key",
                "current_d1": "FALSE",
            },
        ]

        self.assertEqual(
            onboarding_plan.current_d1_opponent_key_errors(
                self.programs,
                opponents,
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
