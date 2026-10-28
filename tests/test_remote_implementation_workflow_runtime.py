import subprocess
import sys
import tempfile
import unittest
from contextlib import chdir
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/remote-implementation.yml"
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import remote_implementation_io  # noqa: E402
from remote_implementation_control import publish_ref_cas, remote_head  # noqa: E402


class RemoteImplementationWorkflowRuntimeAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_request_processing_authenticates_and_executes_exact_main_runner(self):
        text = self.workflow
        self.assertIn(
            "protected_main_sha: ${{ steps.detect.outputs.protected_main_sha }}",
            text,
        )
        self.assertIn(
            'print("protected_main_sha="+str(request.get("expected_protected_main_sha","")))',
            text,
        )
        self.assertIn(
            'git fetch --no-tags origin "+refs/heads/main:refs/remotes/origin/main"',
            text,
        )
        self.assertIn(
            'actual_main="$(git rev-parse refs/remotes/origin/main)"',
            text,
        )
        self.assertIn(
            'if [[ "$actual_main" != "$expected_main" ]]; then',
            text,
        )
        self.assertIn(
            "ref: ${{ steps.detect.outputs.protected_main_sha }}\n"
            "          path: runtime",
            text,
        )
        self.assertIn(
            'working-directory: control\n'
            "        env:\n"
            "          GH_TOKEN: ${{ github.token }}\n"
            '        run: python "$GITHUB_WORKSPACE/runtime/tools/remote_implementation_runner.py"',
            text,
        )

    def test_stale_control_runner_and_verifier_copies_are_not_executable_paths(self):
        text = self.workflow
        self.assertNotIn("run: python tools/remote_implementation_runner.py", text)
        self.assertNotIn("run: python tools/remote_implementation_verify.py", text)
        self.assertEqual(
            text.count(
                'run: python "$GITHUB_WORKSPACE/runtime/tools/remote_implementation_runner.py"'
            ),
            1,
        )
        verifier_count = text.count(
            'run: python "$GITHUB_WORKSPACE/runtime/tools/remote_implementation_verify.py"'
        )
        self.assertGreater(verifier_count, 0)
        self.assertEqual(
            text.count(
                "ref: ${{ needs.process-request.outputs.protected_main_sha }}\n"
                "          path: runtime"
            ),
            verifier_count,
        )

    def test_control_checkout_remains_state_authority(self):
        text = self.workflow
        self.assertIn(
            "ref: ${{ github.sha }}\n"
            "          path: control",
            text,
        )
        self.assertIn(
            "ref: control/remote-implementation\n"
            "          path: control",
            text,
        )
        process = text.split(
            "  fresh-owner-gate2-approval-verification:", 1
        )[0]
        self.assertIn("working-directory: control", process)
        self.assertNotIn("working-directory: runtime", process)


class RemoteImplementationPhase0ObjectStoreTests(unittest.TestCase):
    def git(self, repo, *args, check=True):
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if check and cp.returncode != 0:
            self.fail(cp.stdout)
        return cp

    def test_phase0_prepared_commit_is_owned_and_publishable_from_runtime(self):
        # Match Actions: independent Git checkouts, process cwd=control,
        # authenticated executable ROOT=runtime, and one remote origin.
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bare = root / "origin.git"
            seed = root / "seed"
            control = root / "control"
            runtime = root / "runtime"
            self.git(root, "init", "--bare", str(bare))
            self.git(root, "init", str(seed))
            self.git(seed, "config", "user.name", "Test")
            self.git(seed, "config", "user.email", "test@example.com")
            (seed / "state.txt").write_text("initial\n", encoding="utf-8")
            self.git(seed, "add", "state.txt")
            self.git(seed, "commit", "-m", "initial")
            self.git(seed, "branch", "-M", "main")
            self.git(seed, "remote", "add", "origin", str(bare))
            self.git(seed, "push", "origin", "main")
            self.git(root, "clone", "--branch", "main", str(bare), str(control))
            self.git(root, "clone", "--branch", "main", str(bare), str(runtime))
            main_sha = self.git(runtime, "rev-parse", "HEAD").stdout.strip()

            # With the old implicit-cwd helper, the resulting linked worktree
            # belongs to control; its new commit is missing from runtime.
            worktree = None
            with chdir(control), patch.object(remote_implementation_io, "ROOT", runtime):
                try:
                    worktree = remote_implementation_io.add_isolated_worktree(
                        main_sha, "example-school"
                    )
                    (worktree / "state.txt").write_text(
                        "prepared Phase 0\n", encoding="utf-8"
                    )
                    self.git(worktree, "add", "state.txt")
                    self.git(worktree, "commit", "-m", "prepared Phase 0")
                    prepared = self.git(worktree, "rev-parse", "HEAD").stdout.strip()

                    common_dir = Path(
                        self.git(worktree, "rev-parse", "--git-common-dir").stdout.strip()
                    ).resolve()
                    self.assertEqual(common_dir, (runtime / ".git").resolve())
                    self.assertEqual(
                        self.git(runtime, "cat-file", "-t", prepared).stdout.strip(),
                        "commit",
                    )
                    self.assertNotEqual(
                        self.git(control, "cat-file", "-e", prepared, check=False).returncode,
                        0,
                    )

                    # Use the unchanged create-once production CAS, not a direct
                    # push or a manually reconstructed publication mechanism.
                    publish_ref_cas(
                        runtime,
                        branch="data/example-school-onboarding",
                        prepared_commit=prepared,
                        expected_predecessor=None,
                    )
                    self.assertEqual(
                        remote_head(runtime, "data/example-school-onboarding"),
                        prepared,
                    )
                    self.assertEqual(
                        self.git(runtime, "rev-parse", "HEAD").stdout.strip(),
                        main_sha,
                    )
                    self.assertEqual(
                        self.git(control, "rev-parse", "HEAD").stdout.strip(),
                        main_sha,
                    )
                finally:
                    if worktree is not None:
                        self.git(
                            runtime, "worktree", "remove", "--force", str(worktree),
                            check=False,
                        )
                        if worktree.exists():
                            self.git(
                                control, "worktree", "remove", "--force", str(worktree),
                                check=False,
                            )




if __name__ == "__main__":
    unittest.main()
