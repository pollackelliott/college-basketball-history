import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import onboard_school  # noqa: E402


class SiteCompletenessWiringTests(unittest.TestCase):
    def test_permanent_gate_chain_includes_implementation_site_completeness(self):
        labels = []

        def fake_run(command, *, cwd, label, echo=True):
            labels.append(label)
            if label == "site_completeness":
                self.assertIn("implementation_site_gate.py", " ".join(command))
                self.assertIn("example-school", command)
            return "PASS"

        with tempfile.TemporaryDirectory() as temporary:
            with patch.object(onboard_school, "run", side_effect=fake_run):
                outputs = onboard_school.run_gates(
                    Path(temporary),
                    "example-school",
                    changed=None,
                    include_tests=False,
                )

        self.assertEqual(
            labels,
            [
                "validation",
                "target_no_op",
                "site_completeness",
                "accomplishments",
                "site_dry_run",
            ],
        )
        self.assertEqual(outputs["site_completeness"], "PASS")


if __name__ == "__main__":
    unittest.main()
