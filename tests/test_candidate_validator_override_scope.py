import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import onboard_school  # noqa: E402


class CandidateValidatorOverrideScopeTests(unittest.TestCase):
    def child_value(self, *, preserve: bool) -> str:
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
            preserve_candidate_validator_override=preserve,
        ).strip()

    def test_nested_children_strip_candidate_validator_override_by_default(self):
        with patch.dict(
            os.environ,
            {"CBB_VALIDATE_DATA_TOOL_OVERRIDE": "/candidate/tools/validate_data.py"},
            clear=False,
        ):
            self.assertEqual(self.child_value(preserve=False), "ABSENT")

    def test_ingestion_apply_can_explicitly_preserve_candidate_validator_override(self):
        expected = "/candidate/tools/validate_data.py"
        with patch.dict(
            os.environ,
            {"CBB_VALIDATE_DATA_TOOL_OVERRIDE": expected},
            clear=False,
        ):
            self.assertEqual(self.child_value(preserve=True), expected)


if __name__ == "__main__":
    unittest.main()
