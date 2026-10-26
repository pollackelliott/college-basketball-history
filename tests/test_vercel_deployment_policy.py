import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import vercel_deployment_gate as gate


class VercelDeploymentGateTests(unittest.TestCase):
    def test_main_always_builds(self):
        self.assertFalse(
            gate.should_skip(ref="main", parent_available=True, site_diff_returncode=0)
        )

    def test_control_branch_always_skips(self):
        self.assertTrue(
            gate.should_skip(
                ref="control/remote-implementation",
                parent_available=True,
                site_diff_returncode=1,
            )
        )

    def test_non_main_branch_skips_without_site_or_config_change(self):
        self.assertTrue(
            gate.should_skip(
                ref="hardening/docs-only",
                parent_available=True,
                site_diff_returncode=0,
            )
        )

    def test_non_main_branch_builds_when_site_or_config_changes(self):
        self.assertFalse(
            gate.should_skip(
                ref="maintenance/forum",
                parent_available=True,
                site_diff_returncode=1,
            )
        )

    def test_missing_parent_fails_open(self):
        self.assertFalse(
            gate.should_skip(
                ref="hardening/initial",
                parent_available=False,
                site_diff_returncode=2,
            )
        )

    def test_git_diff_error_fails_open(self):
        self.assertFalse(
            gate.should_skip(
                ref="hardening/tooling",
                parent_available=True,
                site_diff_returncode=2,
            )
        )

    def test_vercel_config_disables_control_branch(self):
        config = json.loads((ROOT / "vercel.json").read_text())
        self.assertEqual(config["outputDirectory"], "site")
        self.assertIs(
            config["git"]["deploymentEnabled"]["control/remote-implementation"],
            False,
        )


if __name__ == "__main__":
    unittest.main()
