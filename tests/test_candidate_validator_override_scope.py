import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import onboard_school  # noqa: E402


class CandidateValidatorOverrideScopeTests(unittest.TestCase):
    def child_value(self) -> str:
        return onboard_school.run(
            [
                sys.executable,
                "-c",
                (
                    "import os; "
                    "print(os.environ.get('CBB_VALIDATE_DATA_TOOL_OVERRIDE', 'ABSENT'))"
                ),
            ],
            cwd=ROOT,
            label="candidate validator override scope probe",
        ).strip()

    def test_nested_children_strip_candidate_validator_override_by_default(self):
        with patch.dict(
            os.environ,
            {"CBB_VALIDATE_DATA_TOOL_OVERRIDE": "/candidate/tools/validate_data.py"},
            clear=False,
        ):
            self.assertEqual(self.child_value(), "ABSENT")

    def test_ingestion_scope_can_preserve_candidate_validator_override(self):
        expected = "/candidate/tools/validate_data.py"
        with patch.dict(
            os.environ,
            {"CBB_VALIDATE_DATA_TOOL_OVERRIDE": expected},
            clear=False,
        ):
            with onboard_school._candidate_validator_override_for_ingestion():
                self.assertEqual(self.child_value(), expected)
            self.assertEqual(self.child_value(), "ABSENT")


if __name__ == "__main__":
    unittest.main()
