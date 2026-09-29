import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "research_stage3a0_portable.py"
PINNED = "2" * 40


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class Stage3A0PortableRuntimeTests(unittest.TestCase):
    def make_repo(self, root):
        repo = root / "repo"
        write(repo / "tools/research_stage3a0.py", "print('stage3a0')\n")
        write(repo / "tools/research_stage3a0_portable.py", SCRIPT.read_text())
        write(repo / "README.md", "not part of Stage 3A-0 portable tool state\n")
        return repo

    def run_cmd(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
        )

    def test_build_contains_only_exact_stage3a0_tool_surface_and_verifies(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = self.make_repo(root)
            snapshot = root / "snapshot"
            proc = self.run_cmd(
                "build", "--repo-root", repo, "--output-dir", snapshot,
                "--main-sha", PINNED,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            manifest = json.loads(
                (snapshot / "research-stage3a0-tool-manifest.json").read_text()
            )
            paths = {item["path"] for item in manifest["files"]}
            self.assertEqual(
                paths,
                {
                    "tools/research_stage3a0.py",
                    "tools/research_stage3a0_portable.py",
                },
            )
            self.assertNotIn("README.md", paths)
            verify = self.run_cmd("verify", snapshot, "--main-sha", PINNED)
            self.assertEqual(verify.returncode, 0, verify.stderr or verify.stdout)
            result = json.loads(verify.stdout)
            self.assertEqual(result["status"], "COMPLETE")
            self.assertEqual(result["file_count"], 2)

    def test_verify_fails_closed_on_missing_extra_modified_or_wrong_sha(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = self.make_repo(root)
            snapshot = root / "snapshot"
            built = self.run_cmd(
                "build", "--repo-root", repo, "--output-dir", snapshot,
                "--main-sha", PINNED,
            )
            self.assertEqual(built.returncode, 0)
            (snapshot / "tools/research_stage3a0.py").write_text(
                "print('tampered')\n", encoding="utf-8"
            )
            write(snapshot / "unexpected.txt", "extra\n")
            verify = self.run_cmd("verify", snapshot, "--main-sha", "3" * 40)
            self.assertEqual(verify.returncode, 2)
            result = json.loads(verify.stdout)
            reasons = {item["reason"] for item in result["defects"]}
            self.assertIn("PROTECTED_MAIN_SHA_MISMATCH", reasons)
            self.assertIn("SNAPSHOT_FILE_SET_MISMATCH", reasons)
            self.assertIn("SNAPSHOT_FILE_HASH_MISMATCH", reasons)

    def test_workflow_publishes_exact_sha_artifact_on_main_push(self):
        workflow = (
            Path(__file__).parents[1]
            / ".github/workflows/research-stage3a0-portable.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("push:", workflow)
        self.assertIn("branches: [main]", workflow)
        self.assertIn("github.sha", workflow)
        self.assertIn("research_stage3a0_portable.py build", workflow)
        self.assertIn("research_stage3a0_portable.py verify", workflow)
        self.assertIn("actions/upload-artifact@v4", workflow)
        self.assertIn("research-stage3a0-tool-", workflow)
        self.assertIn("retention-days: 7", workflow)


if __name__ == "__main__":
    unittest.main()
