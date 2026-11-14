"""Adversarial Git-blob regression tests for post-seal presentation-only scope."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from remote_implementation_presentation_refresh import (  # noqa: E402
    PLAN_KIND, PresentationRefreshStop, git,
    presentation_refresh_tree_plan, verify_presentation_successor,
)


class PresentationRefreshTreeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name)
        subprocess.run(
            ["git", "init", "-q", str(self.repo)], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        git(self.repo, "config", "user.name", "Test Author")
        git(self.repo, "config", "user.email", "test@example.invalid")
        for path, value in (
            ("site/index.html", "bad top-level-only series filter\n"),
            ("data/canonical/games.csv", "game_key,score\nold,71\n"),
            ("site/data/teams/george-mason.json", '{"games":86}\n'),
            ("data/reference/programs.csv", "program_key\ngeorge-mason\n"),
        ):
            self.write(path, value)
        self.base = self.commit("base")
        git(self.repo, "checkout", "-qb", "sealed")
        self.write("data/canonical/games.csv", "game_key,score\nold,71\nnew,81\n")
        self.write("site/data/teams/george-mason.json", '{"games":102}\n')
        self.sealed = self.commit("sealed historical apply")
        self.sealed_tree = git(self.repo, "rev-parse", self.sealed + "^{tree}")
        git(self.repo, "checkout", "-q", "-b", "main", self.base)
        self.write("site/index.html", "corrected publication-scoped series\n")
        self.main = self.commit("accepted generic presentation repair")
        self.accepted_blob = git(self.repo, "rev-parse", self.main + ":site/index.html")
        git(self.repo, "checkout", "-q", "sealed")

    def write(self, path: str, value: str):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(value, encoding="utf-8")

    def commit(self, msg: str) -> str:
        git(self.repo, "add", "--all")
        git(self.repo, "commit", "-qm", msg)
        return git(self.repo, "rev-parse", "HEAD")

    def plan(self, **overrides):
        kwargs = {
            "sealed_commit_sha": self.sealed,
            "repair_main_sha": self.main,
            "expected_sealed_tree_sha": self.sealed_tree,
            "expected_asset_blob_sha": self.accepted_blob,
        }
        kwargs.update(overrides)
        return presentation_refresh_tree_plan(self.repo, **kwargs)

    def successor(self, *, tree=None, parent=None):
        plan = self.plan()
        return git(
            self.repo, "commit-tree", tree or str(plan["candidate_tree_sha"]),
            "-p", parent or self.sealed, "-m", "guarded presentation successor",
        )

    def verify(self, candidate, **overrides):
        kwargs = {
            "sealed_commit_sha": self.sealed,
            "successor_sha": candidate,
            "repair_main_sha": self.main,
            "expected_sealed_tree_sha": self.sealed_tree,
            "expected_asset_blob_sha": self.accepted_blob,
        }
        kwargs.update(overrides)
        return verify_presentation_successor(self.repo, **kwargs)

    def test_exact_one_asset_successor_and_independent_proof(self):
        old_head = git(self.repo, "rev-parse", "HEAD")
        prior_status = git(self.repo, "status", "--porcelain")
        plan = self.plan()
        self.assertEqual(plan["kind"], PLAN_KIND)
        self.assertEqual(plan["allowed_changed_paths"], ["site/index.html"])
        self.assertEqual(plan["tracked_basketball_mutation"], "NONE")
        self.assertFalse(plan["branch_published"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), old_head)
        self.assertEqual(git(self.repo, "status", "--porcelain"), prior_status)
        candidate = self.successor()
        proof = self.verify(candidate)
        self.assertEqual(proof["fresh_tree_equivalence"], "PASS")
        self.assertEqual(proof["sealed_parent"], self.sealed)
        self.assertEqual(
            git(self.repo, "rev-parse", candidate + ":data/canonical/games.csv"),
            git(self.repo, "rev-parse", self.sealed + ":data/canonical/games.csv"),
        )
        self.assertEqual(
            git(self.repo, "rev-parse", candidate + ":site/data/teams/george-mason.json"),
            git(self.repo, "rev-parse", self.sealed + ":site/data/teams/george-mason.json"),
        )

    def test_rejects_changed_basketball_data_and_additional_paths(self):
        # A second tracked change must be rejected even if the accepted site
        # blob is exactly right.
        git(self.repo, "checkout", "-q", "-b", "tamper", self.sealed)
        self.write("site/index.html", "corrected publication-scoped series\n")
        self.write("data/canonical/games.csv", "game_key,score\nunexpected,900\n")
        bad = self.commit("extra data mutation")
        with self.assertRaisesRegex(
            PresentationRefreshStop, "PRESENTATION_SUCCESSOR_TREE_MISMATCH"
        ):
            self.verify(bad)
        self.assertNotEqual(
            git(self.repo, "rev-parse", bad + ":data/canonical/games.csv"),
            git(self.repo, "rev-parse", self.sealed + ":data/canonical/games.csv"),
        )

    def test_rejects_wrong_parent_even_with_identical_candidate_tree(self):
        same_tree = self.plan()["candidate_tree_sha"]
        wrong_parent = git(self.repo, "commit-tree", str(same_tree),
                           "-p", self.base, "-m", "wrong parent")
        with self.assertRaisesRegex(
            PresentationRefreshStop, "PRESENTATION_SUCCESSOR_PARENT_MISMATCH"
        ):
            self.verify(wrong_parent)

    def test_rejects_wrong_current_main_blob_and_sealed_tree(self):
        with self.assertRaisesRegex(
            PresentationRefreshStop, "PRESENTATION_REPAIR_SOURCE_BLOB_MISMATCH"
        ):
            self.plan(expected_asset_blob_sha="f" * 40)
        with self.assertRaisesRegex(
            PresentationRefreshStop, "PRESENTATION_SEALED_TREE_MISMATCH"
        ):
            self.plan(expected_sealed_tree_sha="a" * 40)

    def test_rejects_no_effective_change_and_invalid_source(self):
        with self.assertRaisesRegex(
            PresentationRefreshStop, "PRESENTATION_NO_EFFECTIVE_CHANGE"
        ):
            self.plan(repair_main_sha=self.base,
                      expected_asset_blob_sha=git(
                          self.repo, "rev-parse", self.base + ":site/index.html"))
        with self.assertRaisesRegex(
            PresentationRefreshStop, "PRESENTATION_COMMIT_ID_INVALID"
        ):
            self.plan(sealed_commit_sha="not-a-commit")

    def test_rejects_deletion_and_wrong_asset_blob(self):
        # Deleting the asset or replacing it with an unaccepted blob can never
        # validate as a presentation-only refresh.
        git(self.repo, "checkout", "-q", "-b", "deletion", self.sealed)
        (self.repo / "site/index.html").unlink()
        deleted = self.commit("delete site")
        with self.assertRaises(PresentationRefreshStop):
            self.verify(deleted)
        git(self.repo, "checkout", "-q", "sealed")
        git(self.repo, "checkout", "-q", "-b", "wrong-asset")
        self.write("site/index.html", "different unreviewed site content\n")
        altered = self.commit("wrong asset")
        with self.assertRaisesRegex(
            PresentationRefreshStop, "PRESENTATION_SUCCESSOR_TREE_MISMATCH"
        ):
            self.verify(altered)


if __name__ == "__main__":
    unittest.main()
