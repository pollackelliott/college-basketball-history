import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import release_school  # noqa: E402


class ProtectedMainMergeTests(unittest.TestCase):
    def test_owner_admin_merge_is_exact_sha_pinned(self):
        head_sha = "a" * 40
        args = release_school.protected_merge_args(
            "14",
            "pollackelliott",
            "data/auburn-onboarding",
            "Auburn",
            head_sha,
        )

        self.assertEqual(args[:4], ["pr", "merge", "14", "--merge"])
        self.assertIn("--admin", args)
        self.assertNotIn("--auto", args)

        match_index = args.index("--match-head-commit")
        self.assertEqual(args[match_index + 1], head_sha)

        subject_index = args.index("--subject")
        self.assertEqual(
            args[subject_index + 1],
            "Merge pull request #14 from pollackelliott/data/auburn-onboarding",
        )

    def test_merge_body_remains_school_specific(self):
        args = release_school.protected_merge_args(
            "99",
            "owner",
            "data/example-onboarding",
            "Example State",
            "b" * 40,
        )
        body_index = args.index("--body")
        self.assertEqual(
            args[body_index + 1],
            "Ingest and publish Example State history",
        )


if __name__ == "__main__":
    unittest.main()
