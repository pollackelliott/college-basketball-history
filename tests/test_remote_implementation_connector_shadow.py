"""Stage A: deterministic shadow-only release handoff tests.

No GitHub App, workflow dispatch, PR create/merge, network write, or school
request publication is exercised. Tests use synthetic authority bytes and
a completed-UCF-shaped final control state, never real UCF replay.
"""
from __future__ import annotations

import copy
import hashlib
import hmac
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from remote_implementation_control import (  # noqa: E402
    initial_control_state, canonical_json_bytes, sha256_bytes,
)
import remote_implementation_connector_shadow as shadow  # noqa: E402


MAIN = "a" * 40
CONTROL = "b" * 40
TARGET = "c" * 40
SCHOOL = "ucf"
REPO = "pollackelliott/college-basketball-history"


def asbytes(value):
    return canonical_json_bytes(value)


class Fixture:
    def __init__(self, operation: str = shadow.REA):
        self.op = operation
        self.school = SCHOOL
        self.id = "synthetic-ucf-release-readiness-001" if operation == shadow.REA \
            else "synthetic-ucf-gate2-approval-001"
        self.base = f".remote-implementation/checkpoints/{self.school}/{self.id}"
        self.blobs = {}
        self.request = {
            "operation": operation,
            "school_key": self.school,
            "request_id": self.id,
            "expected_protected_main_sha": MAIN,
            "target_sha": TARGET,
        }
        self.checkpoint = {
            "school_key": self.school,
            "request_id": self.id,
            "target_branch": "data/ucf-onboarding",
            "target_sha": TARGET,
            "protected_main_sha": MAIN,
        }
        self.verification = {
            "request_id": self.id,
            "school_key": self.school,
        }
        self.packet = {}
        if operation == shadow.REA:
            self.configure_readiness()
        else:
            self.configure_gate2()

    def configure_readiness(self):
        body = b"Exact synthetic PR body\n"
        self.blobs[self.base + "/pr-body.md"] = body
        self.request["release_phase_continuation"] = {
            "kind": "RELEASE_READINESS_TO_PREVIEW_V1",
            "preview_request_id": "synthetic-ucf-release-preview-001",
        }
        self.checkpoint.update({
            "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_CHECKPOINT",
            "readiness_status": "RELEASE_READINESS_PASS",
            "owner_gate_2": False,
            "pr_created": False,
            "preview_verified": False,
            "tracked_mutation": "NONE",
            "preview_request_id": "synthetic-ucf-release-preview-001",
            "pr_body_checkpoint_path": self.base + "/pr-body.md",
            "pr_body_sha256": sha256_bytes(body),
            "release_pr_packet_path": self.base + "/release-pr-packet.json",
            "approved_plan_hash": "d" * 64,
            "release_manifest_sha256": "e" * 64,
        })
        self.packet = {
            "kind": "REMOTE_IMPLEMENTATION_RELEASE_PR_PACKET",
            "school_key": self.school,
            "readiness_request_id": self.id,
            "preview_request_id": self.checkpoint["preview_request_id"],
            "base_branch": "main",
            "head_branch": "data/ucf-onboarding",
            "head_sha": TARGET,
            "body_checkpoint_path": self.base + "/pr-body.md",
            "body_sha256": self.checkpoint["pr_body_sha256"],
            "approved_plan_hash": "d" * 64,
            "release_manifest_sha256": "e" * 64,
            "owner_gate_2": False,
            "pr_created_by_runner": False,
        }
        self.verification.update({
            "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_VERIFICATION",
            "remote_release_readiness_equivalence": "PASS",
            "preview_request_id": self.checkpoint["preview_request_id"],
            "pr_body_sha256": self.checkpoint["pr_body_sha256"],
            "target_sha": TARGET,
            "tracked_mutation": "NONE",
            "owner_gate_2": False,
            "pr_created": False,
        })
        self.packet_path = self.base + "/release-pr-packet.json"
        self.verification_path = (
            f".remote-implementation/verifications/{self.school}/{self.id}/"
            "release-readiness-verification.json"
        )

    def configure_gate2(self):
        self.request["final_release_continuation"] = {
            "kind": "RELEASE_GATE2_TO_PRODUCTION_V1",
            "production_request_id": "synthetic-ucf-prod-001",
        }
        self.request["owner_gate_2_approval"] = {"approved": True}
        self.checkpoint.update({
            "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVED_CHECKPOINT",
            "status": "OWNER_GATE_2_APPROVED",
            "owner_gate_2_approved": True,
            "merged": False,
            "production_proof": False,
            "production_request_id": "synthetic-ucf-prod-001",
            "pr_head_sha": TARGET,
            "pr_number": 636,
            "preview_deployment_id": 7857416801,
            "preview_url": "https://preview.example.invalid",
            "gate2_merge_packet_path": self.base + "/gate2-merge-packet.json",
        })
        self.packet = {
            "kind": "REMOTE_IMPLEMENTATION_GATE2_MERGE_PACKET",
            "school_key": self.school,
            "gate2_request_id": self.id,
            "production_request_id": "synthetic-ucf-prod-001",
            "pr_number": 636,
            "pr_head_sha": TARGET,
            "base_branch": "main",
            "target_branch": "data/ucf-onboarding",
            "merge_method": "merge",
            "approved_main_sha": MAIN,
            "preview_deployment_id": 7857416801,
            "preview_url": "https://preview.example.invalid",
            "owner_gate_2_approved": True,
            "merged": False,
            "production_proof": False,
        }
        self.verification.update({
            "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVAL_VERIFICATION",
            "remote_gate2_approval_equivalence": "PASS",
            "owner_gate_2_approved": True,
            "pr_head_sha": TARGET,
            "pr_number": 636,
            "preview_deployment_id": 7857416801,
            "preview_url": "https://preview.example.invalid",
            "production_request_id": "synthetic-ucf-prod-001",
            "merged": False,
        })
        self.packet_path = self.base + "/gate2-merge-packet.json"
        self.verification_path = (
            f".remote-implementation/verifications/{self.school}/{self.id}/"
            "gate2-approval-verification.json"
        )

    def finalize(self):
        # Reconstruct the immutable source bytes and *then* independently
        # bind the checkpoint, packet and fresh verifier to their exact hashes.
        self.blobs[self.base + "/request.json"] = asbytes(self.request)
        self.checkpoint["request_sha256"] = sha256_bytes(
            self.blobs[self.base + "/request.json"]
        )
        self.blobs[self.packet_path] = asbytes(self.packet)
        packet_sha = sha256_bytes(self.blobs[self.packet_path])
        if self.op == shadow.REA:
            self.checkpoint["release_pr_packet_sha256"] = packet_sha
            self.verification["release_pr_packet_sha256"] = packet_sha
        else:
            self.checkpoint["gate2_merge_packet_sha256"] = packet_sha
            self.verification["gate2_merge_packet_sha256"] = packet_sha
        checkpoint_bytes = asbytes(self.checkpoint)
        self.blobs[self.base + "/checkpoint-manifest.json"] = checkpoint_bytes
        checkpoint_sha = sha256_bytes(checkpoint_bytes)
        if self.op == shadow.REA:
            self.verification["checkpoint_manifest_sha256"] = checkpoint_sha
        else:
            self.verification["checkpoint_sha256"] = checkpoint_sha
        self.blobs[self.verification_path] = asbytes(self.verification)

        self.state = initial_control_state()
        self.state.update({
            "lifecycle_state": "IDLE",
            "transaction_state": "COMPLETE",
            "last_operation": {
                "school_key": self.school,
                "request_id": self.id,
                "operation": self.op,
                "fresh_runner_verification": "PASS",
                "checkpoint_manifest_path": self.base + "/checkpoint-manifest.json",
                "checkpoint_manifest_sha256": checkpoint_sha,
                "protected_main_sha": MAIN,
            },
        })
        return self

    def evaluate(self, *, main=MAIN, target=TARGET):
        return shadow.evaluate_shadow(
            repo_slug=REPO,
            control_head=CONTROL,
            state_bytes=asbytes(self.state),
            blobs=lambda path: self.blobs[path],
            main_sha=main,
            target_sha=target,
        )


class ReadinessShadowTests(unittest.TestCase):
    def setUp(self):
        self.f = Fixture().finalize()

    def test_authenticated_readiness_is_shadow_only(self):
        x = self.f.evaluate()
        self.assertEqual(x["status"], "AUTHENTICATED_PACKET_SHADOW_ONLY")
        self.assertEqual(x["candidate_action"],
                         "WOULD_CREATE_OR_REUSE_EXACT_PR_AFTER_LIVE_CHECKS")
        self.assertEqual(x["child_request_id"],
                         "synthetic-ucf-release-preview-001")
        self.assertEqual(x["actions_executed"], 0)
        self.assertFalse(x["execution_authorized_by_this_tool"])
        self.assertEqual(x["external_pr_ci_preview_preconditions"],
                         "NOT_CHECKED_BY_SHADOW")

    def test_repeated_observation_is_same_work_item_not_two_actions(self):
        first = self.f.evaluate()
        second = self.f.evaluate()
        self.assertEqual(first["work_item_sha256"], second["work_item_sha256"])
        self.assertEqual(first["actions_executed"] + second["actions_executed"], 0)

    def test_missing_fresh_verification_never_acts(self):
        self.f.state["last_operation"]["fresh_runner_verification"] = "PENDING"
        x = self.f.evaluate()
        self.assertEqual(x["status"], "NOT_READY")
        self.assertEqual(x["actions_executed"], 0)

    def test_verification_changed_from_pass_stops(self):
        self.f.verification["remote_release_readiness_equivalence"] = "FAIL"
        self.f.blobs[self.f.verification_path] = asbytes(self.f.verification)
        with self.assertRaisesRegex(shadow.ShadowStop, "EQUIVALENCE_MISMATCH"):
            self.f.evaluate()

    def test_pr_packet_tampering_stops(self):
        self.f.packet["head_sha"] = "f" * 40
        self.f.blobs[self.f.packet_path] = asbytes(self.f.packet)
        with self.assertRaisesRegex(shadow.ShadowStop, "PR_PACKET_HASH_MISMATCH"):
            self.f.evaluate()

    def test_pr_body_tampering_stops(self):
        self.f.blobs[self.f.base + "/pr-body.md"] = b"changed"
        with self.assertRaisesRegex(shadow.ShadowStop, "PR_BODY_HASH_MISMATCH"):
            self.f.evaluate()

    def test_source_request_tampering_stops(self):
        self.f.blobs[self.f.base + "/request.json"] = b'{"not":"authorized"}\n'
        with self.assertRaisesRegex(shadow.ShadowStop, "ORIGINAL_REQUEST_HASH_MISMATCH"):
            self.f.evaluate()

    def test_main_advanced_stops(self):
        with self.assertRaisesRegex(shadow.ShadowStop, "CURRENT_REFS_CHANGED"):
            self.f.evaluate(main="f" * 40)

    def test_target_advanced_stops(self):
        with self.assertRaisesRegex(shadow.ShadowStop, "CURRENT_REFS_CHANGED"):
            self.f.evaluate(target="f" * 40)

    def test_wrong_preview_child_id_stops(self):
        self.f.request["release_phase_continuation"]["preview_request_id"] = "other"
        self.f.finalize()
        with self.assertRaisesRegex(shadow.ShadowStop, "CHILD_ID_AUTHORITY_MISMATCH"):
            self.f.evaluate()

    def test_wrong_owner_gate2_flag_stops(self):
        self.f.packet["owner_gate_2"] = True
        self.f.finalize()
        with self.assertRaisesRegex(shadow.ShadowStop, "PR_PACKET_OWNER_GATE_2_MISMATCH"):
            self.f.evaluate()

    def test_active_mutation_lock_stops(self):
        self.f.state["lifecycle_state"] = "ACTIVE"
        self.f.state["active_request_id"] = "other-implementation"
        self.f.state["active_lock_commit"] = "d" * 40
        with self.assertRaisesRegex(shadow.ShadowStop, "CONTROL_NOT_SAFELY_IDLE"):
            self.f.evaluate()

    def test_wrong_checkpointer_hash_stops(self):
        self.f.state["last_operation"]["checkpoint_manifest_sha256"] = "f" * 64
        with self.assertRaisesRegex(shadow.ShadowStop, "CHECKPOINT_HASH_MISMATCH"):
            self.f.evaluate()


class Gate2ShadowTests(unittest.TestCase):
    def setUp(self):
        self.f = Fixture(shadow.GATE).finalize()

    def test_verified_explicit_gate2_yields_shadow_only_exact_merge_candidate(self):
        x = self.f.evaluate()
        self.assertEqual(x["status"], "AUTHENTICATED_PACKET_SHADOW_ONLY")
        self.assertEqual(x["candidate_action"],
                         "WOULD_MERGE_EXACT_APPROVED_PR_AFTER_LIVE_CHECKS")
        self.assertEqual(x["child_request_id"], "synthetic-ucf-prod-001")
        self.assertEqual(x["actions_executed"], 0)
        self.assertFalse(x["execution_authorized_by_this_tool"])

    def test_no_explicit_approval_stops(self):
        self.f.request["owner_gate_2_approval"]["approved"] = False
        self.f.finalize()
        with self.assertRaisesRegex(shadow.ShadowStop, "EXPLICIT_GATE2_APPROVAL_MISSING"):
            self.f.evaluate()

    def test_merge_packet_hash_tampering_stops(self):
        self.f.packet["merge_method"] = "squash"
        self.f.blobs[self.f.packet_path] = asbytes(self.f.packet)
        with self.assertRaisesRegex(shadow.ShadowStop, "MERGE_PACKET_HASH_MISMATCH"):
            self.f.evaluate()

    def test_squash_even_when_rehashed_stops(self):
        self.f.packet["merge_method"] = "squash"
        self.f.finalize()
        with self.assertRaisesRegex(shadow.ShadowStop, "MERGE_PACKET_MERGE_METHOD_MISMATCH"):
            self.f.evaluate()

    def test_changed_main_stops(self):
        with self.assertRaisesRegex(shadow.ShadowStop, "CURRENT_REFS_CHANGED"):
            self.f.evaluate(main="f" * 40)

    def test_changed_pr_head_stops(self):
        with self.assertRaisesRegex(shadow.ShadowStop, "CURRENT_REFS_CHANGED"):
            self.f.evaluate(target="f" * 40)

    def test_missing_fresh_gate2_proof_stops(self):
        self.f.verification["remote_gate2_approval_equivalence"] = "FAIL"
        self.f.blobs[self.f.verification_path] = asbytes(self.f.verification)
        with self.assertRaisesRegex(shadow.ShadowStop, "EQUIVALENCE_MISMATCH"):
            self.f.evaluate()

    def test_production_child_id_not_reinvented(self):
        self.f.request["final_release_continuation"]["production_request_id"] = "other"
        self.f.finalize()
        with self.assertRaisesRegex(shadow.ShadowStop,
                                    "PRODUCTION_CHILD_ID_AUTHORITY_MISMATCH"):
            self.f.evaluate()


class CompletionAndWebhookTests(unittest.TestCase):
    def test_completed_ucf_like_state_is_no_action_even_with_no_artifact_loader(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": "RELEASE_PRODUCTION_PROOF",
            "school_key": SCHOOL,
            "request_id": "ucf-expansion-release-production-proof-0001",
            "fresh_runner_verification": "PASS",
            "remote_production_proof_equivalence": "PASS",
            "merge_sha": "a950b261648d13fd77c88e7bf997b7dd8555eae1",
        }
        loader = Mock(side_effect=AssertionError("must not read old UCF packets"))
        x = shadow.evaluate_shadow(
            repo_slug=REPO,
            control_head=CONTROL,
            state_bytes=asbytes(state),
            blobs=loader,
            main_sha=MAIN,
            target_sha=None,
        )
        self.assertEqual(x["status"], "NO_ELIGIBLE_HANDOFF")
        self.assertEqual(x["actions_executed"], 0)
        loader.assert_not_called()

    def test_signed_completed_event_wakes_observer_but_grants_no_approval(self):
        secret = b"local-test-only"
        data = asbytes({
            "action": "completed",
            "workflow_run": {"id": 44130910737, "status": "completed"},
        })
        signature = "sha256=" + hmac.new(secret, data, hashlib.sha256).hexdigest()
        event = shadow.webhook_wakeup(data, signature, secret)
        self.assertEqual(event["wakeup_kind"], "WORKFLOW_RUN_COMPLETED")
        self.assertEqual(event["run_id"], "44130910737")
        self.assertNotIn("approval", event)

    def test_webhook_replayed_is_still_just_a_wakeup(self):
        secret = b"local-test-only"
        data = asbytes({
            "action": "completed",
            "workflow_run": {"id": 44130910737, "status": "completed"},
        })
        signature = "sha256=" + hmac.new(secret, data, hashlib.sha256).hexdigest()
        self.assertEqual(
            shadow.webhook_wakeup(data, signature, secret),
            shadow.webhook_wakeup(data, signature, secret),
        )

    def test_webhook_signature_tampering_stops(self):
        secret = b"local-test-only"
        data = asbytes({"action": "completed", "workflow_run": {"id": 1, "status": "completed"}})
        signature = "sha256=" + hmac.new(secret, data, hashlib.sha256).hexdigest()
        with self.assertRaisesRegex(shadow.ShadowStop, "SIGNATURE_INVALID"):
            shadow.webhook_wakeup(data + b" ", signature, secret)

    def test_noncompleted_event_stops(self):
        secret = b"local-test-only"
        data = asbytes({"action": "requested", "workflow_run": {"id": 1, "status": "queued"}})
        signature = "sha256=" + hmac.new(secret, data, hashlib.sha256).hexdigest()
        with self.assertRaisesRegex(shadow.ShadowStop, "NOT_COMPLETED"):
            shadow.webhook_wakeup(data, signature, secret)


if __name__ == "__main__":
    unittest.main()
