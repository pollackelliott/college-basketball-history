"""Real-Git adversarial proofs for G historical + C presentation release."""
from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from remote_implementation_io import Stop  # noqa: E402
from remote_implementation_presentation_refresh import (  # noqa: E402
    ASSET_PATH, git, presentation_refresh_tree_plan,
)
from remote_implementation_presentation_release_boundary import (  # noqa: E402
    BOUNDARY_KIND, verify_presentation_dual_release_boundary,
)


class PresentationDualReleaseBoundaryTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        subprocess.run(
            ["git", "init", "-q", str(self.repo)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        git(self.repo, "config", "user.name", "Example")
        git(self.repo, "config", "user.email", "example@example.invalid")
        self.write(ASSET_PATH, "old series selection\n")
        self.write("data/canonical/games.csv", "g1,5\n")
        self.write("site/data/teams/example-school.json", '{"games":86}\n')
        self.write("data/reference/programs.csv", "program\nexample-school\n")
        self.base = self.commit("baseline")
        git(self.repo, "checkout", "-qb", "sealed")
        self.write("data/canonical/games.csv", "g1,5\ng2,9\n")
        self.write("site/data/teams/example-school.json", '{"games":102}\n')
        self.sealed = self.commit("historical sealed apply")
        self.sealed_tree = git(self.repo, "rev-parse", self.sealed + "^{tree}")
        self.old_paths = [
            "data/canonical/games.csv", "site/data/teams/example-school.json",
        ]
        self.old_hashes = {
            path: hashlib.sha256(
                subprocess.run(
                    ["git", "show", f"{self.sealed}:{path}"],
                    cwd=self.repo, check=True, stdout=subprocess.PIPE,
                ).stdout
            ).hexdigest()
            for path in self.old_paths
        }
        git(self.repo, "checkout", "-qb", "main", self.base)
        self.write(ASSET_PATH, "fixed published-history series\n")
        self.main = self.commit("generic website fix")
        self.site_blob = git(self.repo, "rev-parse", self.main + ":" + ASSET_PATH)
        git(self.repo, "checkout", "-q", "sealed")
        plan = presentation_refresh_tree_plan(
            self.repo,
            sealed_commit_sha=self.sealed,
            repair_main_sha=self.main,
            expected_sealed_tree_sha=self.sealed_tree,
            expected_asset_blob_sha=self.site_blob,
        )
        self.successor = git(
            self.repo, "commit-tree", str(plan["candidate_tree_sha"]),
            "-p", self.sealed, "-m", "presentation-only successor",
        )
        git(self.repo, "checkout", "-qb", "release", self.successor)
        self.plan = plan
        self.release_manifest = {
            "school_key": "example-school",
            "base_commit": self.base,
            "approved_plan_hash": "f" * 64,
            "changed_paths": self.old_paths[:],
        }

    def write(self, path: str, content: str):
        target = self.repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def commit(self, msg: str):
        git(self.repo, "add", "--all")
        git(self.repo, "commit", "-qm", msg)
        return git(self.repo, "rev-parse", "HEAD")

    def verify(self, **overrides):
        args = {
            "school_key": "example-school",
            "original_release_manifest": self.release_manifest,
            "approved_plan_hash": "f" * 64,
            "original_apply_base_sha": self.base,
            "original_sealed_sha": self.sealed,
            "original_sealed_tree_sha": self.sealed_tree,
            "original_changed_paths": self.old_paths[:],
            "original_changed_file_sha256": self.old_hashes,
            "original_deleted_paths": [],
            "presentation_successor_sha": self.successor,
            "source_protected_main_sha": self.main,
            "accepted_site_blob_sha": self.site_blob,
        }
        args.update(overrides)
        return verify_presentation_dual_release_boundary(
            self.repo, **args,
        )

    def test_two_separate_boundaries_with_no_historical_mutation(self):
        x = self.verify()
        self.assertEqual(x["kind"], BOUNDARY_KIND)
        self.assertEqual(x["original_apply_path_hash_equivalence"], "PASS")
        self.assertEqual(x["presentation_tree_equivalence"], "PASS")
        self.assertEqual(x["original_release_changed_path_count"], 2)
        self.assertEqual(x["presentation_changed_paths"], [ASSET_PATH])
        self.assertEqual(
            x["full_rehearsal_changed_paths"], sorted(self.old_paths + [ASSET_PATH]),
        )
        self.assertEqual(x["tracked_basketball_mutation_after_seal"], "NONE")
        self.assertFalse(x["original_manifest_modified"])
        self.assertFalse(x["owner_gate_2_approved"])
        for path in self.old_paths + ["data/reference/programs.csv"]:
            self.assertEqual(
                git(self.repo, "rev-parse", self.sealed + ":" + path),
                git(self.repo, "rev-parse", self.successor + ":" + path),
            )
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), self.successor)

    def test_wrong_original_approval_manifest_and_file_sha_fail(self):
        for key, val in (
            ("school_key", "wrong-school"),
            ("base_commit", self.main),
            ("approved_plan_hash", "0" * 64),
            ("changed_paths", [ASSET_PATH]),
        ):
            with self.subTest(key=key):
                other = dict(self.release_manifest)
                other[key] = val
                with self.assertRaisesRegex(Stop, "ORIGINAL_MANIFEST_MISMATCH"):
                    self.verify(original_release_manifest=other)
        wrong_hashes = dict(self.old_hashes)
        wrong_hashes[self.old_paths[0]] = "a" * 64
        with self.assertRaises(Stop):
            self.verify(original_changed_file_sha256=wrong_hashes)

    def test_wrong_original_sealed_tree_and_path_populations_fail(self):
        with self.assertRaises(Stop):
            self.verify(original_sealed_tree_sha=self.main)
        with self.assertRaisesRegex(Stop, "ORIGINAL_PATH_SCOPE_INVALID"):
            self.verify(
                original_release_manifest={
                    **self.release_manifest,
                    "changed_paths": self.old_paths + [ASSET_PATH],
                },
                original_changed_paths=self.old_paths + [ASSET_PATH],
            )
        with self.assertRaisesRegex(Stop, "ORIGINAL_HASH_SCOPE_MISMATCH"):
            self.verify(original_changed_file_sha256={self.old_paths[0]: "0" * 64})

    def test_unapproved_main_blob_and_changed_site_payload_fail(self):
        with self.assertRaisesRegex(Stop, "PRESENTATION_DUAL_PRESENTATION_BOUNDARY"):
            self.verify(accepted_site_blob_sha="0" * 40)
        git(self.repo, "checkout", "-q", "-b", "unapproved", self.sealed)
        self.write(ASSET_PATH, "unapproved website change\n")
        other = self.commit("wrong website change")
        with self.assertRaisesRegex(Stop, "PRESENTATION_DUAL_PRESENTATION_BOUNDARY"):
            self.verify(presentation_successor_sha=other)

    def test_rejects_candidate_with_extra_canonical_mutation(self):
        git(self.repo, "checkout", "-q", "-b", "data-tamper", self.sealed)
        self.write(ASSET_PATH, "fixed published-history series\n")
        self.write("data/canonical/games.csv", "g1,5\ng2,9\ng3,666\n")
        tamper = self.commit("wrong extra basketball mutation")
        with self.assertRaisesRegex(Stop, "PRESENTATION_DUAL_PRESENTATION_BOUNDARY"):
            self.verify(presentation_successor_sha=tamper)

    def test_rejects_wrong_presentation_parent_with_correct_tree(self):
        wrong_parent = git(
            self.repo, "commit-tree", str(self.plan["candidate_tree_sha"]),
            "-p", self.base, "-m", "wrong parent",
        )
        git(self.repo, "checkout", "-q", "-b", "wrong-parent", wrong_parent)
        with self.assertRaisesRegex(Stop, "PRESENTATION_DUAL_PRESENTATION_BOUNDARY"):
            self.verify(presentation_successor_sha=wrong_parent)

    def test_dirty_worktree_and_wrong_head_fail_closed(self):
        with self.assertRaisesRegex(Stop, "TARGET_HEAD_MISMATCH"):
            self.verify(presentation_successor_sha=self.sealed)
        self.write("UNAPPROVED.txt", "new untracked content\n")
        with self.assertRaisesRegex(Stop, "WORKTREE_NOT_CLEAN"):
            self.verify()


if __name__ == "__main__":
    unittest.main()
