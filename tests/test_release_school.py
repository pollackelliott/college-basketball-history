import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import release_school  # noqa: E402
import onboard_school  # noqa: E402


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


class PullRequestBodyTests(unittest.TestCase):
    def test_pr_body_distinguishes_apply_boundary_from_full_pr_diff(self):
        approved = {
            "school_key": "example",
            "approved_plan_hash": "a" * 64,
            "summary": {
                "source_rows": 10,
                "pre_cutoff_rows": 0,
                "existing_game_matches": 4,
                "new_canonical_games": 6,
            },
            "decisions": [],
        }

        body = onboard_school.pr_body(
            approved,
            ["data/canonical/games.csv"],
        )

        self.assertIn("## Sealed apply boundary", body)
        self.assertIn(
            "full PR diff also includes committed Phase 0 package/reference changes",
            body,
        )
        self.assertIn("`data/canonical/games.csv`", body)
        self.assertNotIn("## Change boundary", body)


class ProductionProofCheckoutTests(unittest.TestCase):
    def git(self, repo, *args):
        return subprocess.check_output(
            ["git", *args], cwd=repo, text=True
        ).strip()

    def test_detached_proof_does_not_require_local_main_branch(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source"
            main_owner = root / "main-owner"
            proof = root / "proof"
            source.mkdir()
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
            (source / "tracked.txt").write_text("merged\n", encoding="utf-8")
            subprocess.run(["git", "add", "tracked.txt"], cwd=source, check=True)
            subprocess.run(
                [
                    "git", "-c", "user.name=Regression",
                    "-c", "user.email=regression@example.test",
                    "commit", "-qm", "base",
                ],
                cwd=source,
                check=True,
            )
            merge_sha = self.git(source, "rev-parse", "HEAD")
            subprocess.run(
                ["git", "branch", "data/example-onboarding"],
                cwd=source,
                check=True,
            )
            subprocess.run(
                ["git", "switch", "-q", "data/example-onboarding"],
                cwd=source,
                check=True,
            )
            subprocess.run(
                ["git", "worktree", "add", "-q", str(main_owner), "main"],
                cwd=source,
                check=True,
            )

            release_school.create_production_proof_repository(
                source,
                proof,
                merge_sha,
                school_key="example",
                correction_freeze=None,
            )

            self.assertEqual(self.git(proof, "rev-parse", "HEAD"), merge_sha)
            self.assertEqual(
                self.git(source, "branch", "--show-current"),
                "data/example-onboarding",
            )
            self.assertEqual((proof / "tracked.txt").read_text(), "merged\n")

    def test_detached_proof_transfers_only_exact_correction_freeze(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = root / "source"
            proof = root / "proof"
            source.mkdir()
            subprocess.run(["git", "init", "-q", "-b", "main"], cwd=source, check=True)
            (source / ".gitignore").write_text(".onboarding/\n", encoding="utf-8")
            (source / "tracked.txt").write_text("merged\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=source, check=True)
            subprocess.run(
                [
                    "git", "-c", "user.name=Regression",
                    "-c", "user.email=regression@example.test",
                    "commit", "-qm", "base",
                ],
                cwd=source,
                check=True,
            )
            merge_sha = self.git(source, "rev-parse", "HEAD")
            payload = b'{"status":"INTEGRATION_FROZEN"}\n'

            release_school.create_production_proof_repository(
                source,
                proof,
                merge_sha,
                school_key="example",
                correction_freeze=payload,
            )

            target = proof / ".onboarding/example/integration-freeze.json"
            self.assertEqual(target.read_bytes(), payload)
            self.assertFalse((proof / ".onboarding/example/other.json").exists())


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


class CommittedRemoteSuccessorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q", "-b", "main"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "Regression"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "regression@example.test"], cwd=self.repo, check=True)
        (self.repo / "stable.txt").write_text("stable\\n", encoding="utf-8")
        subprocess.run(["git", "add", "stable.txt"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "baseline"], cwd=self.repo, check=True)
        self.base = self.git("rev-parse", "HEAD")
        subprocess.run(["git", "switch", "-q", "-c", "data/example-onboarding"], cwd=self.repo, check=True)
        (self.repo / "accepted.txt").write_text("approved\\n", encoding="utf-8")
        subprocess.run(["git", "add", "accepted.txt"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", "sealed apply"], cwd=self.repo, check=True)
        self.head = self.git("rev-parse", "HEAD")
        self.manifest = {"base_commit": self.base, "changed_paths": ["accepted.txt"]}

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.repo, text=True).strip()

    def test_accept_exact_clean_committed_successor(self):
        paths = release_school.verify_committed_change_boundary(
            self.repo, self.manifest, self.head
        )
        self.assertEqual(paths, ["accepted.txt"])
        self.assertEqual(self.git("rev-parse", "HEAD"), self.head)

    def test_reject_wrong_authenticated_successor(self):
        with self.assertRaisesRegex(release_school.WorkflowError, "HEAD does not match"):
            release_school.verify_committed_change_boundary(
                self.repo, self.manifest, self.base
            )

    def test_reject_wrong_predecessor(self):
        self.manifest["base_commit"] = "a" * 40
        with self.assertRaisesRegex(release_school.WorkflowError, "parent differs"):
            release_school.verify_committed_change_boundary(
                self.repo, self.manifest, self.head
            )

    def test_reject_unrelated_committed_change(self):
        self.manifest["changed_paths"] = ["stable.txt"]
        with self.assertRaisesRegex(release_school.WorkflowError, "diff differs"):
            release_school.verify_committed_change_boundary(
                self.repo, self.manifest, self.head
            )

    def test_reject_dirty_or_untracked_worktree(self):
        (self.repo / "unexpected.txt").write_text("not approved\\n", encoding="utf-8")
        with self.assertRaisesRegex(release_school.WorkflowError, "not clean"):
            release_school.verify_committed_change_boundary(
                self.repo, self.manifest, self.head
            )


if __name__ == "__main__":
    unittest.main()
