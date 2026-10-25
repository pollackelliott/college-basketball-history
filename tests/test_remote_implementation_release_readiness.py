"""Negative/positive authentication tests for read-only remote release readiness."""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import remote_implementation_release_readiness as ready  # noqa: E402

SCHOOL = "example-school"
BRANCH = "data/example-school-onboarding"
MAIN = "a" * 40
TARGET = "b" * 40
PREDECESSOR = "c" * 40
TREE = "d" * 40
APPROVED = "e" * 64
APPLY_ID = "example-sealed-apply-0001"


def canonical(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def hash_bytes(value):
    return hashlib.sha256(value).hexdigest()


def sample():
    prefix = f".remote-implementation/successors/{SCHOOL}/{APPLY_ID}"
    verify_prefix = f".remote-implementation/verifications/{SCHOOL}/{APPLY_ID}"
    writeahead_prefix = f".remote-implementation/writeahead/{SCHOOL}/{APPLY_ID}"
    paths = ["data/canonical/games.csv"]
    file_hashes = {paths[0]: "f" * 64}
    manifest = {
        "school_key": SCHOOL,
        "branch": BRANCH,
        "base_commit": PREDECESSOR,
        "approved_plan_hash": APPROVED,
        "changed_paths": paths,
    }
    approved_plan = {"school_key": SCHOOL, "approved_plan_hash": APPROVED}
    sidecars = {
        "approved-plan.json": canonical(approved_plan),
        "release-manifest.json": canonical(manifest),
        "pr-body.md": b"review\n",
        "visual-qa.md": b"visual\n",
        "integration-freeze.json": b"{}\n",
        "seal-checkpoint-manifest.json": b"{}\n",
        "seal-verification.json": b"{}\n",
        "current-main-preseal.json": b"{}\n",
    }
    release_hash = hash_bytes(sidecars["release-manifest.json"])
    common = {
        "school_key": SCHOOL,
        "target_branch": BRANCH,
        "protected_main_sha": MAIN,
        "approved_plan_hash": APPROVED,
        "release_manifest_sha256": release_hash,
    }
    successor = {
        "kind": ready.SUCCESSOR_KIND,
        "operation": "STAGE2_SEALED_APPLY",
        "request_id": APPLY_ID,
        "actual_published_target_sha": TARGET,
        "prepared_commit_sha": TARGET,
        "prepared_parent_sha": PREDECESSOR,
        "prepared_tree_sha": TREE,
        "expected_target_predecessor_sha": PREDECESSOR,
        "changed_paths": paths,
        "changed_file_sha256": file_hashes,
        "deleted_paths": [],
        "approved_plan_sha256": hash_bytes(sidecars["approved-plan.json"]),
        "writeahead_manifest_path": writeahead_prefix + "/writeahead-manifest.json",
        "repository_validation": "PASS",
        "final_transaction_state": "COMPLETE",
        **common,
    }
    verify = {
        "kind": ready.VERIFICATION_KIND,
        "request_id": APPLY_ID,
        "target_sha": TARGET,
        "target_predecessor_sha": PREDECESSOR,
        "target_tree_sha": TREE,
        "fresh_replayed_tree_sha": TREE,
        "changed_paths": paths,
        "changed_file_sha256": file_hashes,
        "deleted_paths": [],
        "tracked_stage2_mutation": "EXACT_SEALED_APPLY_SUCCESSOR",
        "remote_stage2_sealed_apply_equivalence": "PASS",
        **common,
    }
    writeahead = {
        "kind": ready.WRITEAHEAD_KIND,
        "operation": "STAGE2_SEALED_APPLY",
        "request_id": APPLY_ID,
        "prepared_commit_sha": TARGET,
        "prepared_tree_sha": TREE,
        "prepared_parent_sha": PREDECESSOR,
        "expected_target_predecessor_sha": PREDECESSOR,
        "changed_paths": paths,
        "changed_file_sha256": file_hashes,
        "deleted_paths": [],
        "sidecars": {k: hash_bytes(v) for k, v in sidecars.items()},
        **common,
    }
    successor["writeahead_manifest_sha256"] = hash_bytes(canonical(writeahead))
    storage = {
        prefix + "/successor-manifest.json": canonical(successor),
        verify_prefix + "/stage2-sealed-apply-verification.json": canonical(verify),
        writeahead_prefix + "/writeahead-manifest.json": canonical(writeahead),
    }
    for name, value in sidecars.items():
        storage[writeahead_prefix + "/" + name] = value
    request = {
        "school_key": SCHOOL,
        "target_branch": BRANCH,
        "target_sha": TARGET,
        "expected_protected_main_sha": MAIN,
        "approved_plan_hash": APPROVED,
        "release_manifest_sha256": release_hash,
        "stage2_apply_successor": {
            "path": prefix + "/successor-manifest.json",
            "sha256": hash_bytes(storage[prefix + "/successor-manifest.json"]),
        },
        "stage2_apply_verification": {
            "path": verify_prefix + "/stage2-sealed-apply-verification.json",
            "sha256": hash_bytes(storage[verify_prefix + "/stage2-sealed-apply-verification.json"]),
        },
    }
    return request, storage


class RemoteReleaseReadinessTests(unittest.TestCase):
    def authenticate(self, request, storage):
        with (
            patch.object(ready, "git_show_bytes", side_effect=lambda _commit, path, **_: storage[path]),
            patch.object(ready, "remote_head", return_value=TARGET),
            patch.object(
                ready, "verify_prepared_sealed_apply",
                return_value={"prepared_tree_sha": TREE},
            ) as verifier,
        ):
            result = ready.verify_release_readiness_authority(
                request, "0" * 40, source_repo=ROOT
            )
            self.assertEqual(verifier.call_count, 1)
            return result

    def test_accepts_exact_successor_and_fresh_verified_evidence(self):
        request, storage = sample()
        got = self.authenticate(request, storage)
        self.assertEqual(got["target_sha"], TARGET)
        self.assertEqual(got["changed_path_count"], 1)
        self.assertEqual(got["sidecars"]["pr-body.md"], b"review\n")

    def test_rejects_stale_or_tampered_successor_reference(self):
        request, storage = sample()
        request["stage2_apply_successor"]["sha256"] = "0" * 64
        with self.assertRaisesRegex(ready.Stop, "RELEASE_SUCCESSOR_HASH_MISMATCH"):
            self.authenticate(request, storage)

    def test_rejects_unverified_apply(self):
        request, storage = sample()
        path = request["stage2_apply_verification"]["path"]
        doc = json.loads(storage[path])
        doc["remote_stage2_sealed_apply_equivalence"] = "PENDING"
        storage[path] = canonical(doc)
        request["stage2_apply_verification"]["sha256"] = hash_bytes(storage[path])
        with self.assertRaisesRegex(ready.Stop, "RELEASE_VERIFICATION_REMOTE_STAGE2"):
            self.authenticate(request, storage)

    def test_rejects_target_head_drift(self):
        request, storage = sample()
        with (
            patch.object(ready, "git_show_bytes", side_effect=lambda _commit, path, **_: storage[path]),
            patch.object(ready, "remote_head", return_value="9" * 40),
        ):
            with self.assertRaisesRegex(ready.Stop, "RELEASE_TARGET_MOVED"):
                ready.verify_release_readiness_authority(request, "0" * 40, source_repo=ROOT)

    def test_rejects_wrong_release_manifest_sidecar(self):
        request, storage = sample()
        path = request["stage2_apply_successor"]["path"]
        doc = json.loads(storage[path])
        sidecar_path = doc["writeahead_manifest_path"].replace(
            "writeahead-manifest.json", "release-manifest.json"
        )
        storage[sidecar_path] = b'{"changed_paths":[]}\n'
        with self.assertRaisesRegex(ready.Stop, "RELEASE_SIDECAR_HASH_MISMATCH"):
            self.authenticate(request, storage)

    def test_rejects_forged_successor_parent_tree(self):
        request, storage = sample()
        path = request["stage2_apply_successor"]["path"]
        doc = json.loads(storage[path])
        doc["prepared_parent_sha"] = "8" * 40
        storage[path] = canonical(doc)
        request["stage2_apply_successor"]["sha256"] = hash_bytes(storage[path])
        with self.assertRaisesRegex(ready.Stop, "RELEASE_PREPARED_PARENT_MISMATCH"):
            self.authenticate(request, storage)

    @patch.object(ready.release_school, "run_gates")
    @patch.object(ready.release_school, "verify_committed_change_boundary", return_value=["data/canonical/games.csv"])
    @patch.object(ready, "git")
    def test_readiness_runs_permanent_gates_without_pr_or_merge(self, mock_git, mock_boundary, mock_gates):
        from tempfile import TemporaryDirectory
        mock_git.return_value.stdout = TARGET + "\n"
        request, storage = sample()
        authority = self.authenticate(request, storage)
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            report = ready.run_permanent_release_readiness(
                authority,
                worktree=root,
                artifact_dir=root / ".onboarding" / SCHOOL,
            )
            self.assertEqual(report["status"], "RELEASE_READINESS_PASS")
            self.assertFalse(report["pr_created"])
            self.assertFalse(report["owner_gate_2"])
            self.assertEqual(mock_boundary.call_count, 2)
            mock_gates.assert_called_once()


if __name__ == "__main__":
    unittest.main()
