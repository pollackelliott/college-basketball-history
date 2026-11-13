"""Pre-publication presentation-refresh authority/commit regression tests."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_io import Stop, git_show_bytes as actual_show  # noqa: E402
from remote_implementation_presentation_refresh import git  # noqa: E402
from remote_implementation_presentation_transaction import (  # noqa: E402
    PREPARED_KIND, prepare_presentation_successor,
)


class PresentationPreflightTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        git(self.repo, "config", "user.name", "Example")
        git(self.repo, "config", "user.email", "example@example.invalid")
        self.write("site/index.html", "old top-level filter\n")
        self.write("data/canonical/games.csv", "old,71\n")
        self.write("site/data/teams/example.json", '{"games":86}\n')
        base = self.commit("base")
        git(self.repo, "checkout", "-qb", "sealed")
        self.write("data/canonical/games.csv", "old,71\nnew,82\n")
        self.write("site/data/teams/example.json", '{"games":102}\n')
        self.sealed = self.commit("sealed")
        self.sealed_tree = git(self.repo, "rev-parse", self.sealed + "^{tree}")
        git(self.repo, "checkout", "-qb", "main", base)
        self.write("site/index.html", "fixed published history series\n")
        self.main = self.commit("main with website fix")
        self.accepted = git(self.repo, "rev-parse", self.main + ":site/index.html")
        git(self.repo, "checkout", "-q", "sealed")

        self.successor = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_SUCCESSOR",
            "actual_published_target_sha": self.sealed,
            "prepared_tree_sha": self.sealed_tree,
            "approved_plan_hash": "f" * 64,
            "release_manifest_sha256": "e" * 64,
        }
        self.successor_bytes = (json.dumps(self.successor) + "\n").encode()
        self.successor_path = ".remote-implementation/successors/example/seal/successor-manifest.json"
        self.request = {
            "operation": "RELEASE_PRESENTATION_REFRESH",
            "school_key": "example",
            "target_branch": "data/example-onboarding",
            "target_sha": self.sealed,
            "sealed_tree_sha": self.sealed_tree,
            "repair_main_sha": self.main,
            "expected_protected_main_sha": self.main,
            "accepted_asset_blob_sha": self.accepted,
            "stage2_apply_successor": {
                "path": self.successor_path,
                "sha256": hashlib.sha256(self.successor_bytes).hexdigest(),
            },
            "stage2_apply_verification": {
                "path": ".remote-implementation/verifications/example/seal/verification.json",
                "sha256": "d" * 64,
            },
            "approved_plan_hash": "f" * 64,
            "release_manifest_sha256": "e" * 64,
        }

    def write(self, path, content):
        dest = self.repo / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")

    def commit(self, name):
        git(self.repo, "add", "--all")
        git(self.repo, "commit", "-qm", name)
        return git(self.repo, "rev-parse", "HEAD")

    def prepared(self):
        def read(commit, path, *, cwd):
            if path == self.successor_path:
                return self.successor_bytes
            return actual_show(commit, path, cwd=cwd)

        with patch(
            "remote_implementation_presentation_transaction.verify_release_readiness_authority",
            return_value={"target_sha": self.sealed},
        ), patch(
            "remote_implementation_presentation_transaction.git_show_bytes",
            side_effect=read,
        ):
            return prepare_presentation_successor(
                self.request, "a" * 40, repo=self.repo,
            )

    def test_authenticated_preparation_is_unreferenced_one_asset_change(self):
        original = git(self.repo, "rev-parse", "HEAD")
        state = git(self.repo, "status", "--porcelain")
        result = self.prepared()
        self.assertEqual(result["kind"], PREPARED_KIND)
        self.assertEqual(result["prepared_parent_sha"], self.sealed)
        self.assertEqual(result["changed_paths"], ["site/index.html"])
        self.assertEqual(result["tracked_basketball_mutation"], "NONE")
        self.assertFalse(result["branch_published"])
        self.assertFalse(result["owner_gate_2_approved"])
        self.assertEqual(git(self.repo, "rev-parse", "HEAD"), original)
        self.assertEqual(git(self.repo, "status", "--porcelain"), state)
        for name in ("data/canonical/games.csv", "site/data/teams/example.json"):
            self.assertEqual(
                git(self.repo, "rev-parse", result["prepared_commit_sha"] + ":" + name),
                git(self.repo, "rev-parse", self.sealed + ":" + name),
            )
        self.assertEqual(
            git(self.repo, "rev-list", "--parents", "-n", "1", result["prepared_commit_sha"]).split(),
            [result["prepared_commit_sha"], self.sealed],
        )

    def test_rejects_wrong_original_manifest_and_source(self):
        self.request["stage2_apply_successor"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(Stop, "SUCCESSOR_HASH_MISMATCH"):
            self.prepared()
        self.request["stage2_apply_successor"]["sha256"] = hashlib.sha256(
            self.successor_bytes
        ).hexdigest()
        self.request["repair_main_sha"] = self.sealed
        with self.assertRaisesRegex(Stop, "SOURCE_MAIN_MISMATCH"):
            self.prepared()

    def test_rejects_original_seal_mismatch_and_wrong_main_asset(self):
        self.request["sealed_tree_sha"] = self.main
        with self.assertRaisesRegex(Stop, "ORIGINAL_SEAL_MISMATCH"):
            self.prepared()
        self.request["sealed_tree_sha"] = self.sealed_tree
        self.request["accepted_asset_blob_sha"] = "0" * 40
        with self.assertRaises(ValueError):
            self.prepared()

    def test_rejects_nonrefresh_operation_before_committing(self):
        self.request["operation"] = "RELEASE_GATE2_APPROVAL"
        with self.assertRaisesRegex(Stop, "OPERATION_INVALID"):
            self.prepared()


if __name__ == "__main__":
    unittest.main()
