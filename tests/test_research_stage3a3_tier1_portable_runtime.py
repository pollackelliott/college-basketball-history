import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "research_stage3a3_tier1_portable.py"
PINNED = "1" * 40


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class Stage3A3Tier1PortableRuntimeTests(unittest.TestCase):
    def make_repo(self, root):
        repo = root / "repo"
        write(repo / "tools/research_stage3a3_tier1.py", "print('tier1')\n")
        write(repo / "tools/research_stage3a3_tier1_portable.py", SCRIPT.read_text())
        write_csv(repo / "data/canonical/games.csv", [{
            "canonical_game_id": "G1",
            "game_date": "2024-11-20",
            "team_a_key": "florida-state",
            "team_b_key": "virginia",
        }])
        write_csv(repo / "schools/virginia/source-games.csv", [{
            "source_game_id": "V1",
            "source_program_key": "virginia",
            "normalized_opponent_key": "florida-state",
        }])
        write_csv(repo / "schools/duke/source-games.csv", [{
            "source_game_id": "D1",
            "source_program_key": "duke",
            "normalized_opponent_key": "other",
        }])
        write(repo / "README.md", "not part of Tier-1 evidence\n")
        return repo

    def run_cmd(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), *map(str, args)],
            text=True,
            capture_output=True,
        )

    def test_build_contains_complete_tier1_surface_and_verifies(self):
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
                (snapshot / "research-stage3a3-tier1-state-manifest.json").read_text()
            )
            paths = {item["path"] for item in manifest["files"]}
            self.assertEqual(
                paths,
                {
                    "tools/research_stage3a3_tier1.py",
                    "tools/research_stage3a3_tier1_portable.py",
                    "data/canonical/games.csv",
                    "schools/duke/source-games.csv",
                    "schools/virginia/source-games.csv",
                },
            )
            self.assertNotIn("README.md", paths)
            verify = self.run_cmd("verify", snapshot, "--main-sha", PINNED)
            self.assertEqual(verify.returncode, 0, verify.stderr or verify.stdout)
            result = json.loads(verify.stdout)
            self.assertEqual(result["status"], "COMPLETE")
            self.assertEqual(result["published_reciprocal_file_count"], 2)

    def test_verify_fails_closed_on_missing_extra_or_modified_state(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repo = self.make_repo(root)
            snapshot = root / "snapshot"
            built = self.run_cmd(
                "build", "--repo-root", repo, "--output-dir", snapshot,
                "--main-sha", PINNED,
            )
            self.assertEqual(built.returncode, 0)
            (snapshot / "schools/duke/source-games.csv").unlink()
            write(snapshot / "unexpected.txt", "extra\n")
            with (snapshot / "data/canonical/games.csv").open(
                "a", encoding="utf-8"
            ) as handle:
                handle.write("tampered\n")
            verify = self.run_cmd("verify", snapshot, "--main-sha", PINNED)
            self.assertEqual(verify.returncode, 2)
            result = json.loads(verify.stdout)
            reasons = {d["reason"] for d in result["defects"]}
            self.assertIn("SNAPSHOT_FILE_SET_MISMATCH", reasons)
            self.assertIn("SNAPSHOT_FILE_HASH_MISMATCH", reasons)

    def test_workflow_publishes_exact_sha_artifact_on_main_push(self):
        workflow = (
            Path(__file__).parents[1]
            / ".github/workflows/research-stage3a3-tier1-portable.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("push:", workflow)
        self.assertIn("branches: [main]", workflow)
        self.assertIn("github.sha", workflow)
        self.assertIn("research_stage3a3_tier1_portable.py build", workflow)
        self.assertIn("research_stage3a3_tier1_portable.py verify", workflow)
        self.assertIn("actions/upload-artifact@v4", workflow)
        self.assertIn("retention-days: 7", workflow)


if __name__ == "__main__":
    unittest.main()
