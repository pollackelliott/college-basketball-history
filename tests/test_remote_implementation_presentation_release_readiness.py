"""Strict G-only and G+C release readiness authentication/integration."""
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

from remote_implementation_io import Stop  # noqa: E402
from remote_implementation_presentation_refresh import (  # noqa: E402
    ASSET_PATH, git, presentation_refresh_tree_plan,
)
from remote_implementation_release_readiness import (  # noqa: E402
    verify_release_readiness_authority,
    run_permanent_release_readiness,
)


def json_bytes(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


class PresentationReleaseReadinessTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name) / "repo"
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        git(self.repo, "config", "user.name", "Test")
        git(self.repo, "config", "user.email", "test@example.invalid")
        self.write(".gitignore", ".onboarding/\n")
        self.write(ASSET_PATH, "old top-level-only matchup code\n")
        self.write("data/canonical/games.csv", "g1,71\n")
        self.write("site/data/teams/example.json", '{"games":86}\n')
        self.base = self.commit("base")
        git(self.repo, "checkout", "-qb", "sealed")
        self.write("data/canonical/games.csv", "g1,71\ng2,92\n")
        self.write("site/data/teams/example.json", '{"games":102}\n')
        self.sealed = self.commit("original historical apply")
        self.sealed_tree = git(self.repo, "rev-parse", self.sealed + "^{tree}")
        self.old_paths = [
            "data/canonical/games.csv", "site/data/teams/example.json",
        ]
        self.old_hashes = {
            path: hashlib.sha256(subprocess.run(
                ["git", "show", f"{self.sealed}:{path}"],
                cwd=self.repo, stdout=subprocess.PIPE, check=True,
            ).stdout).hexdigest() for path in self.old_paths
        }
        git(self.repo, "checkout", "-qb", "main", self.base)
        self.write(ASSET_PATH, "fixed series code using publication history\n")
        self.main = self.commit("accepted site fix")
        self.site_blob = git(self.repo, "rev-parse", self.main + ":" + ASSET_PATH)
        self.plan = presentation_refresh_tree_plan(
            self.repo,
            sealed_commit_sha=self.sealed,
            repair_main_sha=self.main,
            expected_sealed_tree_sha=self.sealed_tree,
            expected_asset_blob_sha=self.site_blob,
        )
        self.candidate = git(
            self.repo, "commit-tree", str(self.plan["candidate_tree_sha"]),
            "-p", self.sealed, "-m", "website only",
        )
        self.manifest = {
            "school_key": "example",
            "base_commit": self.base,
            "approved_plan_hash": "f" * 64,
            "changed_paths": list(self.old_paths),
        }
        self.successor = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_SUCCESSOR",
            "operation": "RELEASE_PRESENTATION_REFRESH",
            "request_id": "example-presentation-0001",
            "school_key": "example",
            "target_branch": "data/example-onboarding",
            "protected_main_sha": self.main,
            "expected_target_predecessor_sha": self.sealed,
            "prepared_parent_sha": self.sealed,
            "prepared_commit_sha": self.candidate,
            "prepared_tree_sha": self.plan["candidate_tree_sha"],
            "actual_published_target_sha": self.candidate,
            "changed_paths": [ASSET_PATH],
            "deleted_paths": [],
            "approved_plan_hash": "f" * 64,
            "release_manifest_sha256": "e" * 64,
            "stage2_apply_successor": {"path": "control/apply.json", "sha256": "a" * 64},
            "stage2_apply_verification": {"path": "control/apply-verified.json", "sha256": "b" * 64},
            "repair_main_sha": self.main,
            "sealed_tree_sha": self.sealed_tree,
            "accepted_asset_blob_sha": self.site_blob,
            "repository_validation": "PASS",
            "tracked_basketball_mutation": "NONE",
            "owner_gate_2_approved": False,
            "final_transaction_state": "COMPLETE",
        }
        self.fresh = {
            "kind": "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_FRESH_PROOF",
            "request_id": self.successor["request_id"],
            "school_key": "example",
            "original_sealed_sha": self.sealed,
            "successor_sha": self.candidate,
            "successor_tree_sha": self.plan["candidate_tree_sha"],
            "protected_main_sha": self.main,
            "accepted_asset_blob_sha": self.site_blob,
            "changed_paths": [ASSET_PATH],
            "original_sealed_apply_equivalence": "PASS",
            "fresh_presentation_tree_equivalence": "PASS",
            "branch_published_exact": True,
            "owner_gate_2_approved": False,
        }
        self.succ_path = (
            ".remote-implementation/successors/example/example-presentation-0001/"
            "successor-manifest.json"
        )
        self.fresh_path = (
            ".remote-implementation/verifications/example/example-presentation-0001/"
            "presentation-refresh-verification.json"
        )
        git(self.repo, "checkout", "-qb", "control", self.base)
        (self.repo / self.succ_path).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / self.fresh_path).parent.mkdir(parents=True, exist_ok=True)
        (self.repo / self.succ_path).write_bytes(json_bytes(self.successor))
        (self.repo / self.fresh_path).write_bytes(json_bytes(self.fresh))
        self.control = self.commit("archived signed presentation proof")
        self.request = {
            "school_key": "example",
            "target_branch": "data/example-onboarding",
            "target_sha": self.candidate,
            "expected_protected_main_sha": self.main,
            "approved_plan_hash": "f" * 64,
            "release_manifest_sha256": "e" * 64,
            "stage2_apply_successor": self.successor["stage2_apply_successor"],
            "stage2_apply_verification": self.successor["stage2_apply_verification"],
            "presentation_refresh_successor": {
                "path": self.succ_path,
                "sha256": hashlib.sha256(json_bytes(self.successor)).hexdigest(),
            },
            "presentation_refresh_verification": {
                "path": self.fresh_path,
                "sha256": hashlib.sha256(json_bytes(self.fresh)).hexdigest(),
            },
        }
        self.original_authority = {
            "school_key": "example",
            "target_branch": "data/example-onboarding",
            "target_sha": self.sealed,
            "protected_main_sha": self.main,
            "apply_protected_main_sha": self.base,
            "apply_request_id": "original-seal",
            "successor_sha256": "a" * 64,
            "verification_sha256": "b" * 64,
            "writeahead_sha256": "c" * 64,
            "approved_plan_hash": "f" * 64,
            "release_manifest_sha256": "e" * 64,
            "changed_path_count": len(self.old_paths),
            "changed_paths": list(self.old_paths),
            "sidecars": {
                "release-manifest.json": json_bytes(self.manifest),
                "approved-plan.json": b'{"approved":true}',
                "pr-body.md": b"Approved school history",
                "visual-qa.md": b"review",
                "integration-freeze.json": b'{}',
            },
            "manifest": self.manifest,
            "approved": {"school_key": "example"},
        }

    def write(self, path, value):
        f = self.repo / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(value, encoding="utf-8")

    def commit(self, message):
        git(self.repo, "add", "--all")
        git(self.repo, "commit", "-qm", message)
        return git(self.repo, "rev-parse", "HEAD")

    def authenticate(self, request=None):
        from remote_implementation_release_readiness import _verify_sealed_release_readiness_authority
        with patch(
            "remote_implementation_release_readiness._verify_sealed_release_readiness_authority",
            return_value=dict(self.original_authority),
        ) as old, patch(
            "remote_implementation_release_readiness.remote_head",
            return_value=self.candidate,
        ):
            proof = verify_release_readiness_authority(
                request or self.request, self.control, source_repo=self.repo,
            )
            return proof, old

    def test_g_plus_c_authentic_and_distinct(self):
        proof, old = self.authenticate()
        self.assertEqual(proof["target_sha"], self.candidate)
        self.assertEqual(proof["changed_path_count"], 3)
        self.assertEqual(proof["changed_paths"], sorted(self.old_paths + [ASSET_PATH]))
        self.assertEqual(proof["presentation_refresh"]["original_sealed_sha"], self.sealed)
        self.assertFalse(proof["presentation_refresh"]["owner_gate_2_approved"])
        self.assertEqual(old.call_args.kwargs["published_head_sha"], self.candidate)
        self.assertEqual(old.call_args.args[0]["target_sha"], self.sealed)

    def test_new_readiness_uses_dual_boundary_and_never_legacy_boundary(self):
        proof, _ = self.authenticate()
        detached = Path(self.repo.parent) / "candidate"
        git(self.repo, "worktree", "add", "--detach", str(detached), self.candidate)
        with patch(
            "remote_implementation_release_readiness.release_school.verify_committed_change_boundary",
        ) as old, patch(
            "remote_implementation_release_readiness.release_school.run_gates",
        ) as gates:
            result = run_permanent_release_readiness(
                proof,
                worktree=detached,
                artifact_dir=detached / ".onboarding/example",
            )
        self.assertEqual(result["target_sha"], self.candidate)
        self.assertEqual(result["changed_path_count"], 3)
        self.assertEqual(result["presentation_dual_boundary"]["presentation_tree_equivalence"], "PASS")
        self.assertFalse(result["owner_gate_2"])
        old.assert_not_called()
        self.assertEqual(gates.call_args.args[2], sorted(self.old_paths + [ASSET_PATH]))

    def test_missing_mismatched_verification_or_original_seal_rejected(self):
        for label, update in (
            ("missing_verification", {"presentation_refresh_verification": None}),
            ("wrong_successor_sha", {"target_sha": self.sealed}),
            ("different_main", {"expected_protected_main_sha": self.base}),
            ("wrong_original_apply", {"stage2_apply_successor": {"path": "bad", "sha256": "a" * 64}}),
            ("wrong_confirmation_digest", {"presentation_refresh_verification": {
                "path": self.fresh_path, "sha256": "0" * 64,
            }}),
        ):
            with self.subTest(label=label):
                req = {**self.request, **update}
                with self.assertRaises(Stop):
                    self.authenticate(req)

    def test_g_only_release_keeps_original_authenticator_and_original_output(self):
        req = dict(self.request)
        req.pop("presentation_refresh_successor")
        req.pop("presentation_refresh_verification")
        result, old = self.authenticate(req)
        old.assert_called_once()
        self.assertEqual(result["target_sha"], self.sealed)
        self.assertEqual(result["changed_path_count"], 2)
        self.assertNotIn("presentation_refresh", result)
        self.assertNotIn("presentation_dual_boundary", result)


if __name__ == "__main__":
    unittest.main()
