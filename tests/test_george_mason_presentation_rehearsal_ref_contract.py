import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/rehearse_george_mason_presentation.py"


class GeorgeMasonPresentationRehearsalRefContractTests(unittest.TestCase):
    def test_release_pr_may_advance_from_g_to_guarded_c(self):
        source = SCRIPT.read_text(encoding="utf-8")

        # The exact sealed historical commit remains immutable authority.
        self.assertIn(
            'SEALED_G = "0fe86b37405bc5322bec5639a28c1819bb97d5f7"',
            source,
        )
        self.assertIn(
            'git("rev-parse", f"{SEALED_G}^{tree}") == SEALED_G_TREE'
                .replace("{tree}", "{{tree}}"),
            source,
        )

        # PR #597 is a moving release locator: once guarded presentation
        # successor C is published, its head must not be required to equal G.
        self.assertNotIn('"G_REF_DRIFT"', source)
        self.assertNotIn(
            'git("rev-parse", "refs/remotes/origin/exact-gmu-sealed")',
            source,
        )
        self.assertIn(
            'git("merge-base", SEALED_G, gmu_release_head) == SEALED_G',
            source,
        )
        self.assertIn(
            '"SEALED_G_NOT_ANCESTOR_OF_RELEASE_HEAD"',
            source,
        )

        # The reviewed site-fix commit is likewise pinned by immutable commit
        # ancestry rather than by assuming a mutable PR head never advances.
        self.assertNotIn('"FIX_REF_DRIFT"', source)
        self.assertIn(
            'git("merge-base", REVIEWED_FIX, site_fix_head) == REVIEWED_FIX',
            source,
        )
        self.assertIn(
            '"REVIEWED_FIX_NOT_ANCESTOR_OF_SOURCE_HEAD"',
            source,
        )


if __name__ == "__main__":
    unittest.main()
