"""Adversarial real-Git checks for post-seal presentation publication boundaries."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_control import (  # noqa: E402
    OP_RELEASE_PRESENTATION_REFRESH,
    MUTATION_COMPLETE, MUTATION_DIVERGED, MUTATION_PREPARED,
    MUTATION_PUBLISHED, begin_request, classify_mutation,
    initial_control_state,
)
from remote_implementation_io import Stop  # noqa: E402
from remote_implementation_presentation_refresh import (  # noqa: E402
    ASSET_PATH, git, presentation_refresh_tree_plan,
)
from remote_implementation_presentation_publish import (  # noqa: E402
    writeahead_contents, validate_presentation_intent,
    finalize_presentation_refresh_successor,
)
from remote_implementation_presentation_transaction import PREPARED_KIND  # noqa: E402
from remote_implementation_presentation_verify import (  # noqa: E402
    inspect_presentation_checkpoint,
)

def payload(obj):
    return (json.dumps(obj, sort_keys=True, indent=2) + "\n").encode("utf-8")


class GuardedPublicationFixture(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.repo = Path(tmp.name)
        subprocess.run(
            ["git", "init", "-q", str(self.repo)],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        git(self.repo, "config", "user.name", "Regression")
        git(self.repo, "config", "user.email", "regression@example.invalid")
        self.write("site/index.html", "bad top-level filter\n")
        self.write("data/canonical/games.csv", "old,67\n")
        self.write("site/data/teams/example.json", '{"games":86}\n')
        self.base = self.commit("base")
        git(self.repo, "checkout", "-qb", "sealed")
        self.write("data/canonical/games.csv", "old,67\nnew,92\n")
        self.write("site/data/teams/example.json", '{"games":102}\n')
        self.sealed = self.commit("sealed")
        self.sealed_tree = git(self.repo, "rev-parse", self.sealed + "^{tree}")
        git(self.repo, "checkout", "-qb", "main", self.base)
        self.write("site/index.html", "correct published-series selection\n")
        self.main = self.commit("accepted main fix")
        self.site_blob = git(self.repo, "rev-parse", self.main + ":site/index.html")
        git(self.repo, "checkout", "-q", "sealed")
        self.plan = presentation_refresh_tree_plan(
            self.repo,
            sealed_commit_sha=self.sealed,
            repair_main_sha=self.main,
            expected_sealed_tree_sha=self.sealed_tree,
            expected_asset_blob_sha=self.site_blob,
        )
        self.successor = git(
            self.repo, "commit-tree", str(self.plan["candidate_tree_sha"]),
            "-p", self.sealed, "-m", "presentation only",
        )
        self.asset_content = subprocess.run(
            ["git", "show", f"{self.successor}:{ASSET_PATH}"],
            cwd=self.repo, check=True, stdout=subprocess.PIPE,
        ).stdout
        self.original_paths = [
            "data/canonical/games.csv", "site/data/teams/example.json",
        ]
        # Use actual Git object bytes for hash calculation to avoid text stripping.
        self.original_hashes = {
            path: hashlib.sha256(subprocess.run(
                ["git", "show", f"{self.sealed}:{path}"],
                cwd=self.repo, check=True, stdout=subprocess.PIPE,
            ).stdout).hexdigest()
            for path in self.original_paths
        }
        self.orig_apply = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_SEALED_APPLY_SUCCESSOR",
            "actual_published_target_sha": self.sealed,
            "prepared_tree_sha": self.sealed_tree,
            "expected_target_predecessor_sha": self.base,
            "changed_paths": self.original_paths,
            "changed_file_sha256": self.original_hashes,
            "deleted_paths": [],
            "approved_plan_hash": "f" * 64,
            "release_manifest_sha256": "e" * 64,
            "final_transaction_state": "COMPLETE",
        }
        self.orig_verify = {
            "remote_stage2_sealed_apply_equivalence": "PASS",
            "target_sha": self.sealed,
            "target_tree_sha": self.sealed_tree,
        }
        self.request_id = "presentation-test-0001"
        self.request = {
            "operation": OP_RELEASE_PRESENTATION_REFRESH,
            "request_id": self.request_id,
            "school_key": "example",
            "target_branch": "data/example-onboarding",
            "expected_protected_main_sha": self.main,
            "repair_main_sha": self.main,
            "accepted_asset_blob_sha": self.site_blob,
            "target_sha": self.sealed,
            "sealed_tree_sha": self.sealed_tree,
            "approved_plan_hash": "f" * 64,
            "release_manifest_sha256": "e" * 64,
            "stage2_apply_successor": {
                "path": "original/apply/successor.json",
                "sha256": hashlib.sha256(payload(self.orig_apply)).hexdigest(),
            },
            "stage2_apply_verification": {
                "path": "original/apply/verification.json",
                "sha256": hashlib.sha256(payload(self.orig_verify)).hexdigest(),
            },
        }
        self.prepared = {
            "kind": PREPARED_KIND,
            "expected_target_predecessor_sha": self.sealed,
            "prepared_parent_sha": self.sealed,
            "prepared_commit_sha": self.successor,
            "prepared_tree_sha": self.plan["candidate_tree_sha"],
            "changed_paths": [ASSET_PATH],
            "changed_file_sha256": {
                ASSET_PATH: hashlib.sha256(self.asset_content).hexdigest(),
            },
            "deleted_paths": [],
            "repair_main_sha": self.main,
            "accepted_asset_blob_sha": self.site_blob,
            "tracked_basketball_mutation": "NONE",
            "branch_published": False,
            "owner_gate_2_approved": False,
        }
        self.request_bytes = payload(self.request)
        self.lock_commit = "a" * 40
        self.wa = writeahead_contents(
            request=self.request, request_bytes=self.request_bytes,
            prepared=self.prepared, global_lock_commit=self.lock_commit,
            protected_main_sha=self.main,
            proof_sha256=hashlib.sha256(payload(self.prepared)).hexdigest(),
        )
        self.wa_bytes = payload(self.wa)
        self.wa_path = ".remote-implementation/writeahead/example/presentation-test-0001/writeahead-manifest.json"
        self.proof_path = ".remote-implementation/writeahead/example/presentation-test-0001/prepared-proof.json"
        self.successor_path = ".remote-implementation/successors/example/presentation-test-0001/successor-manifest.json"

    def write(self, path, content):
        location = self.repo / path
        location.parent.mkdir(parents=True, exist_ok=True)
        location.write_text(content, encoding="utf-8")

    def commit(self, msg):
        git(self.repo, "add", "--all")
        git(self.repo, "commit", "-qm", msg)
        return git(self.repo, "rev-parse", "HEAD")


class PublicationGuardTests(GuardedPublicationFixture):
    def test_positive_writeahead_validation_and_safe_classification(self):
        proof = validate_presentation_intent(self.request, self.wa, repo=self.repo)
        self.assertEqual(proof["fresh_tree_equivalence"], "PASS")
        self.assertEqual(proof["sealed_parent"], self.sealed)
        self.assertEqual(self.wa["changed_paths"], [ASSET_PATH])
        self.assertEqual(self.wa["deleted_paths"], [])
        self.assertEqual(self.wa["owner_gate_2_approved"], False)
        self.assertEqual(
            classify_mutation(self.sealed, self.sealed, manifest=self.wa),
            MUTATION_PREPARED,
        )
        self.assertEqual(
            classify_mutation(self.sealed, self.successor, manifest=self.wa),
            MUTATION_PUBLISHED,
        )
        self.assertEqual(
            classify_mutation(self.sealed, self.base, manifest=self.wa),
            MUTATION_DIVERGED,
        )

    def test_reject_tampered_writeahead_authority(self):
        changes = (
            ("target_branch", "data/other-onboarding"),
            ("expected_target_predecessor_sha", self.base),
            ("prepared_parent_sha", self.base),
            ("prepared_tree_sha", self.sealed_tree),
            ("prepared_commit_sha", self.sealed),
            ("changed_paths", [ASSET_PATH, "data/canonical/games.csv"]),
            ("deleted_paths", [ASSET_PATH]),
            ("approved_plan_hash", "0" * 64),
            ("accepted_asset_blob_sha", "0" * 40),
            ("repository_validation", "FAIL"),
            ("owner_gate_2_approved", True),
        )
        for field, value in changes:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.wa)
                changed[field] = value
                with self.assertRaises(Stop):
                    validate_presentation_intent(self.request, changed, repo=self.repo)
        changed = copy.deepcopy(self.wa)
        changed["changed_file_sha256"] = {ASSET_PATH: "0" * 64}
        with self.assertRaisesRegex(Stop, "ASSET_HASH_MISMATCH"):
            validate_presentation_intent(self.request, changed, repo=self.repo)

    def test_finalize_success_requires_exact_published_ref(self):
        state = initial_control_state()
        req = {
            **self.request,
            "authority": {
                "owner_gate_1": False, "owner_gate_2": False,
                "release": False, "release_presentation_refresh": True,
            },
        }
        # This test exercises the finalizer's durable control and ref boundary
        # without creating a branch or contacting GitHub.
        active = begin_request(
            state, req, hashlib.sha256(payload(req)).hexdigest(),
            run_id="test", run_attempt="1", request_commit="b" * 40,
        )
        active["active_lock_commit"] = self.lock_commit
        oldcwd = Path.cwd()
        try:
            os.chdir(self.repo)
            with patch(
                "remote_implementation_presentation_publish.remote_head",
                return_value=self.sealed,
            ):
                with self.assertRaisesRegex(Stop, "TARGET_NOT_EXACT_PREPARED"):
                    finalize_presentation_refresh_successor(
                        active=active, request=self.request,
                        request_sha256=hashlib.sha256(self.request_bytes).hexdigest(),
                        live_main=self.main, writeahead=self.wa,
                        writeahead_path=self.wa_path,
                        writeahead_sha256=hashlib.sha256(self.wa_bytes).hexdigest(),
                        writeahead_commit="f" * 40,
                        expected_remote="c" * 40,
                        publication_cas="EXISTING_REF_CAS_PASS", repo=self.repo,
                    )
            with patch(
                "remote_implementation_presentation_publish.remote_head",
                return_value=self.successor,
            ), patch(
                "remote_implementation_presentation_publish.commit_control",
                return_value="d" * 40,
            ) as fake:
                result = finalize_presentation_refresh_successor(
                    active=active, request=self.request,
                    request_sha256=hashlib.sha256(self.request_bytes).hexdigest(),
                    live_main=self.main, writeahead=self.wa,
                    writeahead_path=self.wa_path,
                    writeahead_sha256=hashlib.sha256(self.wa_bytes).hexdigest(),
                    writeahead_commit="f" * 40,
                    expected_remote="c" * 40,
                    publication_cas="EXISTING_REF_CAS_PASS", repo=self.repo,
                )
                self.assertEqual(result, "d" * 40)
                fake.assert_called_once()
                last = json.loads((self.repo / ".remote-implementation/control-state.json").read_text())["last_operation"]
                self.assertEqual(last["target_sha"], self.successor)
                self.assertEqual(last["original_sealed_sha"], self.sealed)
                self.assertEqual(last["fresh_runner_verification"], "PENDING")
                self.assertFalse(last["owner_gate_2_approved"])
        finally:
            os.chdir(oldcwd)


class FreshProofTests(GuardedPublicationFixture):
    def test_fresh_proof_recovers_original_and_presentation_trees(self):
        successor = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_PRESENTATION_REFRESH_SUCCESSOR",
            "operation": OP_RELEASE_PRESENTATION_REFRESH,
            "request_id": self.request_id,
            "request_sha256": hashlib.sha256(self.request_bytes).hexdigest(),
            "school_key": self.request["school_key"],
            "target_branch": self.request["target_branch"],
            "protected_main_sha": self.main,
            "global_lock_commit": self.lock_commit,
            "writeahead_manifest_path": self.wa_path,
            "writeahead_manifest_sha256": hashlib.sha256(self.wa_bytes).hexdigest(),
            "expected_target_predecessor_sha": self.sealed,
            "prepared_commit_sha": self.successor,
            "prepared_tree_sha": self.plan["candidate_tree_sha"],
            "actual_published_target_sha": self.successor,
            "changed_paths": [ASSET_PATH],
            "changed_file_sha256": self.wa["changed_file_sha256"],
            "sealed_tree_sha": self.sealed_tree,
            "accepted_asset_blob_sha": self.site_blob,
            "stage2_apply_successor": self.request["stage2_apply_successor"],
            "stage2_apply_verification": self.request["stage2_apply_verification"],
            "approved_plan_hash": self.request["approved_plan_hash"],
            "release_manifest_sha256": self.request["release_manifest_sha256"],
            "owner_gate_2_approved": False,
            "tracked_basketball_mutation": "NONE",
            "repository_validation": "PASS",
            "final_transaction_state": "COMPLETE",
        }
        source = {
            self.successor_path: payload(successor),
            self.wa_path: self.wa_bytes,
            self.proof_path: payload(self.prepared),
            self.request["stage2_apply_successor"]["path"]: payload(self.orig_apply),
            self.request["stage2_apply_verification"]["path"]: payload(self.orig_verify),
            f".remote-implementation/requests/{self.request_id}/request.json": self.request_bytes,
        }
        last = {
            "operation": OP_RELEASE_PRESENTATION_REFRESH,
            "request_id": self.request_id,
            "target_branch": self.request["target_branch"],
            "target_sha": self.successor,
            "prepared_tree_sha": self.plan["candidate_tree_sha"],
            "original_sealed_sha": self.sealed,
            "successor_manifest_path": self.successor_path,
            "successor_manifest_sha256": hashlib.sha256(source[self.successor_path]).hexdigest(),
            "fresh_runner_verification": "PENDING",
        }

        def read(control,path,*,cwd):
            if path in source:
                return source[path]
            return subprocess.run(
                ["git", "show", f"{control}:{path}"],
                cwd=cwd, stdout=subprocess.PIPE, check=True,
            ).stdout

        from types import SimpleNamespace

        def fake_verifier_git(*args, **kwargs):
            if args[0] == "fetch":
                return SimpleNamespace(stdout="")
            if args[0] == "rev-parse":
                return SimpleNamespace(stdout=self.successor + "\n")
            raise AssertionError("Unexpected verification Git invocation: %s" % (args,))

        with patch(
            "remote_implementation_presentation_verify.git_show_bytes", side_effect=read,
        ), patch(
            "remote_implementation_presentation_verify.remote_head",
            return_value=self.successor,
        ), patch(
            "remote_implementation_presentation_verify.git",
            side_effect=fake_verifier_git,
        ):
            result = inspect_presentation_checkpoint(
                self.main, "0" * 40, {"last_operation": last}, repo=self.repo,
            )
            self.assertEqual(result["original_sealed_apply_equivalence"], "PASS")
            self.assertEqual(result["fresh_presentation_tree_equivalence"], "PASS")
            self.assertFalse(result["owner_gate_2_approved"])

            source[self.proof_path] = b'{"tampered":true}\n'
            with self.assertRaisesRegex(Stop, "PREPARED_PROOF_HASH_MISMATCH"):
                inspect_presentation_checkpoint(
                    self.main, "0" * 40, {"last_operation": last}, repo=self.repo,
                )


if __name__ == "__main__":
    unittest.main()
