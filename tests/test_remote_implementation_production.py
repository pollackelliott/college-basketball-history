"""Generic remote Gate 2 approval and post-merge Production proof refusal tests."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import remote_implementation_production as prod  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_RELEASE_GATE2_APPROVAL, OP_RELEASE_PRODUCTION_PROOF,
    LIFECYCLE_READ_ONLY, RemoteImplementationError,
    begin_request, initial_control_state, validate_request,
)

SCHOOL = "example-school"
BRANCH = "data/example-school-onboarding"
PR = 321
HEAD = "a" * 40
MAIN = "b" * 40
MERGE = "c" * 40
HASH = "d" * 64
PREVIEW = "https://example-preview.vercel.app"


def req(operation):
    gate2 = operation == OP_RELEASE_GATE2_APPROVAL
    flags = {
        k: False for k in (
            "phase0", "recovery", "stage2_census",
            "stage2_opponent_display_normalize", "stage2_proposal_rehearsal",
            "stage2_gate1_fill", "stage2_preseal_rehearsal", "stage2_gate1_seal",
            "stage2_sealed_apply", "stage2_reconciliation_diagnostic",
            "release_readiness", "release_preview_verify", "release",
            "owner_gate_1", "owner_gate_2", "release_gate2_approval",
            "release_production_proof",
        )
    }
    flags["owner_gate_2"] = gate2
    flags["release_gate2_approval" if gate2 else "release_production_proof"] = True
    obj = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": "example-release-gate2-0001" if gate2 else "example-production-0001",
        "operation": operation,
        "school_key": SCHOOL,
        "previous_control_state_commit": MAIN,
        "previous_control_state_sha256": HASH,
        "expected_protected_main_sha": MAIN if gate2 else MERGE,
        "target_branch": BRANCH,
        "target_sha": HEAD,
        "pr_number": PR,
        "creation_provenance": {
            "origin": "Owner's school Implementation chat",
            "authorization": "Explicit exact PR-head Preview approval",
        },
        "authority": flags,
    }
    if gate2:
        obj.update({
            "approved_plan_hash": HASH,
            "release_manifest_sha256": HASH,
            "preview_deployment_id": 67890,
            "preview_url": PREVIEW,
            "release_preview_checkpoint": {
                "path": ".remote-implementation/checkpoints/example-school/preview/checkpoint-manifest.json",
                "sha256": HASH,
            },
            "release_preview_verification": {
                "path": ".remote-implementation/verifications/example-school/preview/release-preview-verification.json",
                "sha256": HASH,
            },
        })
        obj["owner_gate_2_approval"] = {
            "approved": True,
            "approval_basis": "Explicit owner approval of exact Preview",
            "preview_checkpoint_sha256": HASH,
            "preview_verification_sha256": HASH,
            "pr_number": PR,
            "pr_head_sha": HEAD,
            "preview_deployment_id": 67890,
            "preview_url": PREVIEW,
        }
    else:
        obj.update({
            "merge_sha": MERGE,
            "owner_gate_2_checkpoint": {
                "path": ".remote-implementation/checkpoints/example-school/gate2/checkpoint-manifest.json",
                "sha256": HASH,
            },
            "owner_gate_2_verification": {
                "path": ".remote-implementation/verifications/example-school/gate2/gate2-approval-verification.json",
                "sha256": HASH,
            },
        })
    return obj


class RemoteReleaseGate2ControlTests(unittest.TestCase):
    def test_explicit_gate2_request_valid_and_read_only(self):
        r = req(OP_RELEASE_GATE2_APPROVAL)
        validate_request(r)
        state = begin_request(
            initial_control_state(), r, HASH,
            run_id="100", run_attempt="1", request_commit=MAIN,
        )
        self.assertEqual(state["lifecycle_state"], LIFECYCLE_READ_ONLY)
        self.assertIsNone(state["active_lock_owner"])

    def test_production_request_valid_and_read_only(self):
        r = req(OP_RELEASE_PRODUCTION_PROOF)
        validate_request(r)
        state = begin_request(
            initial_control_state(), r, HASH,
            run_id="100", run_attempt="1", request_commit=MAIN,
        )
        self.assertEqual(state["lifecycle_state"], LIFECYCLE_READ_ONLY)
        self.assertIsNone(state["active_lock_owner"])

    def test_gate2_approval_needs_explicit_bounded_owner_evidence(self):
        cases = [
            ("owner_gate_2_approval", None),
            ("owner_gate_2_approval.approved", False),
            ("owner_gate_2_approval.pr_number", 888),
            ("owner_gate_2_approval.pr_head_sha", MERGE),
            ("owner_gate_2_approval.preview_deployment_id", 67891),
            ("owner_gate_2_approval.preview_checkpoint_sha256", "f"*64),
        ]
        for field, bad in cases:
            with self.subTest(field=field):
                r = req(OP_RELEASE_GATE2_APPROVAL)
                if "." in field:
                    outer, inner = field.split(".")
                    r[outer][inner] = bad
                else:
                    r[field] = bad
                with self.assertRaises(RemoteImplementationError):
                    validate_request(r)

    def test_production_cannot_claim_owner_approval_or_merge_authority(self):
        for k in ("owner_gate_2", "release", "release_gate2_approval", "stage2_sealed_apply"):
            with self.subTest(field=k):
                r = req(OP_RELEASE_PRODUCTION_PROOF)
                r["authority"][k] = True
                with self.assertRaises(RemoteImplementationError):
                    validate_request(r)

    def test_no_approval_reference_blocks_production(self):
        r = req(OP_RELEASE_PRODUCTION_PROOF)
        del r["owner_gate_2_verification"]
        with self.assertRaises(RemoteImplementationError):
            validate_request(r)


def merged_pr():
    return {
        "number": PR, "state": "MERGED",
        "mergedAt": "2026-10-25T10:00:00Z",
        "mergeCommit": {"oid": MERGE},
        "headRefOid": HEAD,
        "headRefName": BRANCH,
        "baseRefName": "main",
    }


class ExactMergedMainTests(unittest.TestCase):
    def check(self, *, pr=None, main=MERGE, parents=None, old_main=MAIN):
        if pr is None:
            pr = merged_pr()
        if parents is None:
            parents = f"{MERGE} {MAIN} {HEAD}"
        def git_command(_repo, *args):
            if args[0] == "ls-remote":
                return main + "\nrefs/heads/main"
            if args[0] == "rev-list":
                return parents
            raise AssertionError(args)
        authority = {"original_main_sha": old_main}
        with (
            patch.object(prod.release_school, "git", side_effect=git_command),
            patch.object(prod.release_school, "gh_json", return_value=pr),
        ):
            return prod.verify_exact_merge(
                req(OP_RELEASE_PRODUCTION_PROOF), authority, repo=ROOT
            )

    def test_exact_merge_is_accepted(self):
        result = self.check()
        self.assertEqual(result["merge_sha"], MERGE)

    def test_reject_wrong_main_sha(self):
        with self.assertRaisesRegex(prod.Stop, "MAIN_NOT_EXACT"):
            self.check(main="e" * 40)

    def test_reject_wrong_pr_merge_identity(self):
        for field, value in (
            ("headRefOid", "e" * 40),
            ("state", "OPEN"),
            ("mergeCommit", {"oid": "e"*40}),
            ("mergedAt", None),
        ):
            with self.subTest(field=field):
                with self.assertRaises(prod.Stop):
                    self.check(pr={**merged_pr(), field: value})

    def test_reject_squash_rebase_or_foreign_merge_parent(self):
        for parents in (
            f"{MERGE} {MAIN}",
            f"{MERGE} {MAIN} {'f'*40}",
            f"{MERGE} {'f'*40} {HEAD}",
        ):
            with self.subTest(parents=parents):
                with self.assertRaises(prod.Stop):
                    self.check(parents=parents)


class LiveProductionProofTests(unittest.TestCase):
    def test_owner_gate2_approval_never_claims_merge(self):
        request = req(OP_RELEASE_GATE2_APPROVAL)
        record = {
            "school_key": SCHOOL, "pr_number": PR,
            "target_sha": HEAD, "preview_deployment_id": 67890,
            "preview_url": PREVIEW, "preview_checkpoint_sha256": HASH,
            "preview_verification_sha256": HASH,
        }
        with patch.object(prod, "verify_gate2_ready_chain", return_value=record):
            out = prod.approve_exact_gate2(request, MAIN, repo=ROOT)
        self.assertTrue(out["owner_gate_2_approved"])
        self.assertFalse(out["merged"])
        self.assertFalse(out["production_proof"])

    def test_mismatched_preview_claim_is_refused(self):
        request = req(OP_RELEASE_GATE2_APPROVAL)
        with patch.object(prod, "verify_gate2_ready_chain", return_value={
            "school_key": SCHOOL, "pr_number": PR,
            "target_sha": HEAD, "preview_deployment_id": 67891,
            "preview_url": PREVIEW, "preview_checkpoint_sha256": HASH,
            "preview_verification_sha256": HASH,
        }):
            with self.assertRaises(prod.Stop):
                prod.approve_exact_gate2(request, MAIN, repo=ROOT)


if __name__ == "__main__":
    unittest.main()
