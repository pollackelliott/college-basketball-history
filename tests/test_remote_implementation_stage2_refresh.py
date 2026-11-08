from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import remote_implementation_stage2_refresh as refresh  # noqa: E402
import remote_implementation_verify as verify  # noqa: E402
from remote_implementation_io import REQUIRED_PACKAGE_FILES, Stop  # noqa: E402


SCHOOL = "example-school"
BRANCH = "data/example-school-onboarding"


class CurrentMainRefreshTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> str:
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if cp.returncode:
            self.fail(cp.stdout)
        return cp.stdout.strip()

    def make_repo(self):
        root = Path(tempfile.mkdtemp(prefix="stage2-refresh-test-"))
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        bare = root / "origin.git"
        repo = root / "repo"
        self.git(root, "init", "--bare", str(bare))
        self.git(root, "init", str(repo))
        self.git(repo, "config", "user.name", "Test")
        self.git(repo, "config", "user.email", "test@example.com")

        school = repo / "schools" / SCHOOL
        school.mkdir(parents=True)
        for name in REQUIRED_PACKAGE_FILES:
            (school / name).write_text(name + " base\n", encoding="utf-8")
        (repo / "base.txt").write_text("base\n", encoding="utf-8")
        (repo / "tools").mkdir()
        (repo / "tools" / "validate_data.py").write_text(
            "raise SystemExit(0)\n", encoding="utf-8"
        )
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "base")
        base = self.git(repo, "rev-parse", "HEAD")
        self.git(repo, "branch", "-M", "main")

        self.git(repo, "checkout", "-b", BRANCH)
        (repo / "target-only.txt").write_text("target\n", encoding="utf-8")
        self.git(repo, "add", "target-only.txt")
        self.git(repo, "commit", "-m", "target")
        target = self.git(repo, "rev-parse", "HEAD")

        self.git(repo, "checkout", "main")
        (repo / "main-only.txt").write_text("main\n", encoding="utf-8")
        self.git(repo, "add", "main-only.txt")
        self.git(repo, "commit", "-m", "main advance")
        main = self.git(repo, "rev-parse", "HEAD")

        self.git(repo, "remote", "add", "origin", str(bare))
        self.git(repo, "push", "origin", "main")
        self.git(repo, "push", "origin", BRANCH)
        return repo, base, target, main

    def package_hashes(self, repo: Path, commit: str):
        result = {}
        for name in REQUIRED_PACKAGE_FILES:
            data = subprocess.run(
                ["git", "show", f"{commit}:schools/{SCHOOL}/{name}"],
                cwd=repo,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout
            result[name] = hashlib.sha256(data).hexdigest()
        return result

    def test_disjoint_refresh_prepares_exact_two_parent_merge(self):
        repo, base, target, main = self.make_repo()
        authority = {
            "prior_authority": {
                "freeze_bytes": b'{"status":"INTEGRATION_FROZEN"}\n',
                "target_authority_kind": "PHASE0_SUCCESSOR",
            },
            "merge_base_sha": base,
            "target_changed_paths": ["target-only.txt"],
            "main_changed_paths": ["main-only.txt"],
            "overlap_paths": [],
            "package_member_sha256": self.package_hashes(repo, target),
        }
        request = {
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": target,
            "integration_freeze_sha256": "a" * 64,
            "semantic_snapshot_sha256": "b" * 64,
        }
        with (
            patch.object(refresh, "restore_integration_freeze"),
            patch.object(
                refresh,
                "semantic_drift_report",
                return_value={"status": "PASS", "changes": []},
            ),
        ):
            result = refresh.prepare_current_main_refresh(
                request,
                authority,
                main,
                source_repo=repo,
                diag=repo.parent / "diag",
            )
        self.assertEqual(result["prepared_parents"], [target, main])
        self.assertEqual(result["changed_paths"], ["main-only.txt"])
        self.assertEqual(
            result["proof"]["package_member_sha256"],
            authority["package_member_sha256"],
        )
        parents = self.git(
            repo,
            "show",
            "-s",
            "--format=%P",
            result["prepared_commit_sha"],
        ).split()
        self.assertEqual(parents, [target, main])

    def test_authority_rejects_overlapping_target_and_main_paths(self):
        repo, base, target, main = self.make_repo()
        request = {
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": target,
            "expected_protected_main_sha": main,
        }
        prior = {
            "target_authority_kind": "PHASE0_SUCCESSOR",
            "phase0_protected_main_sha": base,
        }
        with (
            patch.object(refresh, "verify_phase0_authority", return_value=prior),
            patch.object(refresh, "_paths_between", side_effect=[
                ["shared.csv"], ["shared.csv"],
            ]),
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_REFRESH_PATH_OVERLAP_REQUIRES_RECONCILIATION",
            ):
                refresh.verify_current_main_refresh_authority(
                    request, "0" * 40, main, source_repo=repo
                )

    def test_refresh_verifier_accepts_linear_live_main_advance(self):
        repo, base, _target, main = self.make_repo()
        successor = {"protected_main_sha": base}
        with patch.object(verify, "ROOT", repo):
            refresh_main = verify._stage2_refresh_verification_main(
                successor,
                main,
            )
        self.assertEqual(refresh_main, base)

    def test_refresh_verifier_rejects_diverged_live_main(self):
        repo, _base, target, main = self.make_repo()
        successor = {"protected_main_sha": target}
        with patch.object(verify, "ROOT", repo):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_REFRESH_FRESH_MAIN_DIVERGED",
            ):
                verify._stage2_refresh_verification_main(
                    successor,
                    main,
                )

    def test_authority_rejects_current_main_target_school_change(self):
        repo, base, target, main = self.make_repo()
        request = {
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": target,
            "expected_protected_main_sha": main,
        }
        prior = {
            "target_authority_kind": "PHASE0_SUCCESSOR",
            "phase0_protected_main_sha": base,
        }
        with (
            patch.object(refresh, "verify_phase0_authority", return_value=prior),
            patch.object(refresh, "_paths_between", side_effect=[
                ["target-only.txt"],
                [f"schools/{SCHOOL}/notes.md"],
            ]),
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_REFRESH_CURRENT_MAIN_TOUCHED_TARGET_SCHOOL",
            ):
                refresh.verify_current_main_refresh_authority(
                    request, "0" * 40, main, source_repo=repo
                )


if __name__ == "__main__":
    unittest.main()
