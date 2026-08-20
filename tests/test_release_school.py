import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import release_school  # noqa: E402


class ReleasePreparationHardeningTests(unittest.TestCase):
    @patch.object(release_school, "gh")
    @patch.object(release_school, "pr_for_branch")
    def test_reused_open_pr_refreshes_current_body(self, mock_pr_for_branch, mock_gh):
        repo = Path("/repo")
        body_path = repo / ".onboarding/example/pr-body.md"
        existing = {
            "number": 20,
            "url": "https://github.com/example/repo/pull/20",
            "state": "OPEN",
        }
        mock_pr_for_branch.side_effect = [existing, existing]

        result = release_school.create_or_reuse_pr(
            repo,
            "data/example-onboarding",
            "example",
            body_path,
        )

        self.assertEqual(result, existing)
        mock_gh.assert_called_once_with(
            repo,
            "pr",
            "edit",
            "20",
            "--body-file",
            str(body_path),
        )

    @patch.object(release_school.time, "sleep")
    @patch.object(release_school, "gh_json")
    def test_unknown_mergeability_is_polled_until_mergeable(self, mock_gh_json, mock_sleep):
        head_sha = "c" * 40
        unknown = {
            "number": 20,
            "url": "https://github.com/example/repo/pull/20",
            "state": "OPEN",
            "mergeable": "UNKNOWN",
            "mergeStateStatus": "UNKNOWN",
            "headRefOid": head_sha,
        }
        mergeable = {
            **unknown,
            "mergeable": "MERGEABLE",
            "mergeStateStatus": "BLOCKED",
        }
        mock_gh_json.side_effect = [unknown, mergeable]

        result = release_school.wait_for_pr_mergeable(
            Path("/repo"),
            "20",
            expected_head_sha=head_sha,
            timeout_seconds=10,
            poll_seconds=0,
        )

        self.assertEqual(result, mergeable)
        self.assertEqual(mock_gh_json.call_count, 2)
        mock_sleep.assert_called_once_with(0)

    @patch.object(release_school, "gh_json")
    def test_mergeability_polling_rejects_changed_head(self, mock_gh_json):
        mock_gh_json.return_value = {
            "number": 20,
            "state": "OPEN",
            "mergeable": "UNKNOWN",
            "headRefOid": "d" * 40,
        }

        with self.assertRaisesRegex(release_school.WorkflowError, "head changed"):
            release_school.wait_for_pr_mergeable(
                Path("/repo"),
                "20",
                expected_head_sha="e" * 40,
                timeout_seconds=10,
                poll_seconds=0,
            )


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
