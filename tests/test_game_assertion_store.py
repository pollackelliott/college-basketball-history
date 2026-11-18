import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import game_assertion_store as store  # noqa: E402
import onboard_school  # noqa: E402


FIELDS = [
    "assertion_id",
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
]


def write_table(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class GameAssertionStoreTests(unittest.TestCase):
    def test_small_legacy_append_preserves_legacy_behavior(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            legacy = repo / store.LEGACY_RELATIVE_PATH
            write_table(legacy, [{
                "assertion_id": "A1",
                "canonical_game_id": "G1",
                "source_program_key": "alpha",
                "source_game_id": "S1",
            }])
            changed = store.append_game_assertions(repo, FIELDS, [{
                "assertion_id": "A2",
                "canonical_game_id": "G2",
                "source_program_key": "beta",
                "source_game_id": "S2",
            }])
            self.assertEqual(changed, [legacy])
            self.assertEqual(list(legacy.parent.glob("game-assertions-*.csv")), [])
            fields, rows = store.read_game_assertions(repo)
            self.assertEqual(fields, FIELDS)
            self.assertEqual([row["assertion_id"] for row in rows], ["A1", "A2"])

    def test_over_limit_legacy_spills_only_new_rows_to_numbered_shard(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            legacy = repo / store.LEGACY_RELATIVE_PATH
            write_table(legacy, [{
                "assertion_id": "A1",
                "canonical_game_id": "G1",
                "source_program_key": "alpha",
                "source_game_id": "S1",
            }])
            original = legacy.read_bytes()
            changed = store.append_game_assertions(
                repo,
                FIELDS,
                [{
                    "assertion_id": "A2",
                    "canonical_game_id": "G2",
                    "source_program_key": "beta",
                    "source_game_id": "S2",
                }],
                legacy_append_limit_bytes=1,
                shard_target_bytes=4096,
            )
            shard = repo / "data/evidence/game-assertions-0002.csv"
            self.assertEqual(changed, [shard])
            self.assertEqual(legacy.read_bytes(), original)
            self.assertTrue(shard.is_file())
            _, rows = store.read_game_assertions(repo)
            self.assertEqual([row["assertion_id"] for row in rows], ["A1", "A2"])

    def test_union_rejects_duplicate_assertion_ids_across_files(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            write_table(repo / store.LEGACY_RELATIVE_PATH, [{
                "assertion_id": "A1",
                "canonical_game_id": "G1",
                "source_program_key": "alpha",
                "source_game_id": "S1",
            }])
            write_table(repo / "data/evidence/game-assertions-0002.csv", [{
                "assertion_id": "A1",
                "canonical_game_id": "G2",
                "source_program_key": "beta",
                "source_game_id": "S2",
            }])
            with self.assertRaisesRegex(ValueError, "duplicate assertion_id"):
                store.read_game_assertions(repo)

    def test_git_reader_includes_numbered_shards(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
            write_table(repo / store.LEGACY_RELATIVE_PATH, [{
                "assertion_id": "A1",
                "canonical_game_id": "G1",
                "source_program_key": "alpha",
                "source_game_id": "S1",
            }])
            write_table(repo / "data/evidence/game-assertions-0002.csv", [{
                "assertion_id": "A2",
                "canonical_game_id": "G2",
                "source_program_key": "beta",
                "source_game_id": "S2",
            }])
            subprocess.run(["git", "add", "."], cwd=repo, check=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=repo, check=True, capture_output=True)
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=repo, check=True,
                capture_output=True, text=True,
            ).stdout.strip()

            def reader(root: Path, sha: str, path: str):
                raw = subprocess.run(
                    ["git", "show", f"{sha}:{path}"], cwd=root, check=True,
                    capture_output=True, text=True,
                ).stdout
                return list(csv.DictReader(raw.splitlines()))

            rows = store.read_game_assertions_at_git(repo, commit, reader)
            self.assertEqual([row["assertion_id"] for row in rows], ["A1", "A2"])

    def test_onboarding_apply_allowlist_accepts_numbered_assertion_shard(self):
        self.assertTrue(onboard_school.allowed_apply_path(
            "data/evidence/game-assertions-0002.csv", "wyoming", "a" * 64,
        ))
        self.assertFalse(onboard_school.allowed_apply_path(
            "data/evidence/game-assertions-not-a-shard.txt", "wyoming", "a" * 64,
        ))


if __name__ == "__main__":
    unittest.main()
