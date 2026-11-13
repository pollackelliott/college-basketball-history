"""Fail-closed object/transport tests; no basketbalI or baseline authentication mocked."""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import research_stage4_git_transport as stage4_transport

BASE = "f" * 40


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args], stderr=subprocess.STDOUT, text=True).strip()


class GitTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "config", "user.name", "Stage 4 Transport Test")
        git(self.repo, "config", "user.email", "stage4-test@example.invalid")
        (self.repo / "tools").mkdir()
        for name in ("research_stage4.py", "research_stage4_closeout.py", "expansion_stage4_coverage.py"):
            (self.repo / "tools" / name).write_text(
                "import sys\nraise SystemExit(0 if sys.argv[1] == 'author' else 2)\n"
                if name == "research_stage4.py" else "# permanent test source\n"
            )
        git(self.repo, "add", "tools")
        git(self.repo, "commit", "-qm", "immutable research base")
        self.base = git(self.repo, "rev-parse", "HEAD")
        (self.repo / "README.md").write_text("current main runtime\n")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-qm", "main")
        self.main = git(self.repo, "rev-parse", "HEAD")
        git(self.repo, "branch", "-M", "main")
        self.remote = self.root / "remote.git"
        subprocess.run(["git", "clone", "-q", "--bare", str(self.repo), str(self.remote)], check=True)
        git(self.repo, "remote", "add", "origin", str(self.remote))
        self.chk = self.root / "real-stage3b.zip"
        self.chk.write_bytes(b"immutable checkpoint fixture")
        self.sha = hashlib.sha256(self.chk.read_bytes()).hexdigest()
        self.artifact = self.root / "artifact"
        self.out = self.root / "out"

    def _build(self):
        return stage4_transport.build(repo=self.repo, output=self.artifact,
            main_sha=self.main, base_sha=self.base, school="vcu",
            checkpoint_sha=self.sha)

    def _run(self, **overrides):
        kw = dict(artifact=self.artifact, checkpoint=self.chk, output=self.out,
            main_sha=self.main, base_sha=self.base, school="vcu", checkpoint_sha=self.sha)
        kw.update(overrides)
        return stage4_transport.run(**kw)

    def test_genuine_git_bundle_replays_permanent_author(self):
        self._build()
        self.assertEqual(self._run()["status"], "PERMANENT_STAGE4_COMMAND_SUCCEEDED")
        self.assertTrue((self.out / "stage4-git-transport-execution.json").exists())

    def test_build_rejects_wrong_or_stale_protected_main(self):
        with self.assertRaisesRegex(stage4_transport.GitTransportError,"protected main moved"):
            stage4_transport.build(repo=self.repo, output=self.artifact,
                main_sha=self.base, base_sha=self.base, school="vcu", checkpoint_sha=self.sha)

    def test_missing_base_and_wrong_base_fail(self):
        with self.assertRaisesRegex(stage4_transport.GitTransportError,"research-base SHA.*missing"):
            stage4_transport.build(repo=self.repo, output=self.artifact,
                main_sha=self.main, base_sha=BASE, school="vcu", checkpoint_sha=self.sha)
        self._build()
        with self.assertRaisesRegex(stage4_transport.GitTransportError,"manifest mismatch: research_base_sha"):
            self._run(base_sha=self.main)

    def test_changed_checkpoint_fails_before_git_execution(self):
        self._build()
        self.chk.write_bytes(b"tampered")
        with self.assertRaisesRegex(stage4_transport.GitTransportError,"changed Stage 3B"):
            self._run()

    def test_changed_artifact_fails_before_git_execution(self):
        self._build()
        with (self.artifact / stage4_transport.BUNDLE_FILE).open("ab") as f:
            f.write(b"corruption")
        with self.assertRaisesRegex(stage4_transport.GitTransportError,"corrupt genuine Git bundle"):
            self._run()

    def test_mismatched_tool_runtime_fails_closed(self):
        self._build()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "clone", "-q", "--no-checkout",
                            str(self.artifact / stage4_transport.BUNDLE_FILE), str(root / "checkout")], check=True)
            clone = root / "checkout"
            git(clone, "checkout", "--detach", self.main)
            (clone / "tools" / "research_stage4.py").write_text("tampered")
            with self.assertRaisesRegex(stage4_transport.GitTransportError,"tracked edits"):
                stage4_transport._auth_checkout(clone, self.main, self.base)

    def test_non_git_directory_is_not_baseline_proof(self):
        with self.assertRaises(stage4_transport.GitTransportError):
            stage4_transport._auth_checkout(self.root, self.main, self.base)

    def test_permanent_stage4_failure_remains_failure(self):
        self._build()
        # Build a second, genuinely committed test runtime whose permanent tool
        # deliberately fails, not a mocked or bypassed acceptance gate.
        (self.repo / "tools" / "research_stage4.py").write_text("import sys\nraise SystemExit(2)\n")
        git(self.repo,"add","tools/research_stage4.py")
        git(self.repo,"commit","-qm","explicit permanent acceptance failure")
        new_main=git(self.repo,"rev-parse","HEAD")
        git(self.repo,"push","-q","origin","main")
        new_artifact=self.root / "failed-artifact"
        stage4_transport.build(repo=self.repo, output=new_artifact,
            main_sha=new_main, base_sha=self.base, school="vcu", checkpoint_sha=self.sha)
        with self.assertRaisesRegex(stage4_transport.GitTransportError,"permanent Stage 4 author failed"):
            self._run(artifact=new_artifact, main_sha=new_main)
        self.assertEqual(json.loads((self.out / "stage4-git-transport-execution.json").read_text())["status"],
                         "PERMANENT_STAGE4_ACCEPTANCE_FAILED")


if __name__ == "__main__":
    unittest.main()
