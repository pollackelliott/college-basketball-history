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

    def test_publication_branch_families_always_build(self):
        for ref in (
            "data/florida-state-onboarding",
            "maintenance/shared-reference-publication",
        ):
            self.assertFalse(
                gate.should_skip(
                    ref=ref,
                    parent_available=False,
                    site_diff_returncode=2,
                ),
                ref,
            )

    def test_non_publication_branch_families_always_skip(self):
        for ref in (
            "control/remote-implementation",
            "tooling/stage2-repair",
            "research/uc-davis-stage3a1",
            "control-center/vercel-repair",
            "transport/freeze-parts",
            "hardening/vercel-policy",
            "docs/policy-update",
            "feature/site-change",
        ):
            for parent_available, diff_rc in (
                (True, 0),
                (True, 1),
                (True, 2),
                (False, 2),
            ):
                self.assertTrue(
                    gate.should_skip(
                        ref=ref,
                        parent_available=parent_available,
                        site_diff_returncode=diff_rc,
                    ),
                    (ref, parent_available, diff_rc),
                )

    def test_vercel_config_is_exact_fail_closed_allow_list(self):
        config = json.loads((ROOT / "vercel.json").read_text())
        self.assertEqual(config["outputDirectory"], "site")
        deployment = config["git"]["deploymentEnabled"]
        self.assertEqual(
            deployment,
            {
                "**": False,
                "main": True,
                "data/**": True,
                "maintenance/**": True,
            },
        )


if __name__ == "__main__":
    unittest.main()
