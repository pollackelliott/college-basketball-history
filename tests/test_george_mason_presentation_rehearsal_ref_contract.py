import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/rehearse_george_mason_presentation.py"


class GeorgeMasonPresentationRehearsalRefContractTests(unittest.TestCase):
    def test_regression_uses_only_immutable_commits(self):
        source = SCRIPT.read_text(encoding="utf-8")

        self.assertIn(
            'SEALED_G = "0fe86b37405bc5322bec5639a28c1819bb97d5f7"',
            source,
        )
        self.assertIn(
            'REVIEWED_FIX = "fc42631af872e2ae6573efcbb15b93f668360fb2"',
            source,
        )
        self.assertIn(
            'GUARDED_C = "9db724322351dc2facdaf2934248b8c34912c3a3"',
            source,
        )

        # Generic CI must not depend on mutable historical PR refs.
        self.assertNotIn("refs/pull/597", source)
        self.assertNotIn("refs/pull/607", source)
        self.assertNotIn("exact-gmu-release", source)
        self.assertNotIn("exact-site-fix-source", source)

        # The accepted guarded C remains a direct child of sealed G, while its
        # tree is reproduced by the permanent presentation-refresh planner.
        self.assertIn(
            'git("rev-parse", f"{GUARDED_C}^") == SEALED_G',
            source,
        )
        self.assertIn('"GUARDED_C_PARENT_MISMATCH"', source)
        self.assertIn('"GUARDED_C_TREE_NOT_REPRODUCED"', source)
        self.assertIn("successor_sha=GUARDED_C", source)

        # The regression no longer synthesizes a commit, so Git identity is
        # irrelevant to future generic validation.
        self.assertNotIn('"commit-tree"', source)


if __name__ == "__main__":
    unittest.main()
