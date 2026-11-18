"""Fail-closed synthetic regression for resuming a blocked post-Gate-1 chain.

This is a disposable authority fixture, not a live UCF publication operation.
"""
from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import remote_implementation_stage2_continuation as resume  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    LIFECYCLE_IDLE,
    OP_STAGE2_GATE1_FILL,
    initial_control_state,
    OP_STAGE2_GATE1_SEAL,
    OP_STAGE2_PRESEAL_REHEARSAL,
    STAGE2_POST_GATE1_CONTINUATION_KIND,
    TX_COMPLETE,
    validate_request,
    validate_stage2_phase_continuation,
)
from remote_implementation_io import Stop  # noqa: E402


class VerifiedPresealReplacementTests(unittest.TestCase):
    FILL = "school-stage2-fill-0001"
    FIRST = "school-stage2-preseal-0001"
    REPLACEMENT = "school-stage2-preseal-0002"
    CONTROL = "c" * 40

    def setUp(self):
        self.authorized = {
            "kind": STAGE2_POST_GATE1_CONTINUATION_KIND,
            "preseal_request_id": self.FIRST,
            "seal_request_id": "school-stage2-seal-0001",
            "apply_request_id": "school-stage2-apply-0001",
        }
        self.identity = {
            "school_key": "school",
            "target_branch": "data/school-onboarding",
            "target_sha": "1" * 40,
            "target_tree_sha": "a" * 40,
            "integration_freeze_sha256": "2" * 64,
            "semantic_snapshot_sha256": "3" * 64,
            "decision_universe_sha256": "4" * 64,
            "recommendation_map_sha256": "5" * 64,
            "approved_plan_hash_preview": "6" * 64,
            "filled_review_sha256": "7" * 64,
            "decision_id_set_sha256": "8" * 64,
            "owner_gate_1_approval_sha256": "9" * 64,
        }
        self.fill_request = {
            "school_key": "school",
            "operation": OP_STAGE2_GATE1_FILL,
            "request_id": self.FILL,
            "authority": {"owner_gate_1": True},
            "phase_continuation": copy.deepcopy(self.authorized),
        }
        self.first_request = {
            "school_key": "school",
            "operation": OP_STAGE2_PRESEAL_REHEARSAL,
            "request_id": self.FIRST,
            "phase_continuation": copy.deepcopy(self.authorized),
        }
        self.fill = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT",
            "request_id": self.FILL,
            "gate1_fill_status": "FILLED",
            "owner_gate_1_approval": {"approved": True},
            "request_sha256": resume.sha256_bytes(self.bytes(self.fill_request)),
        }
        self.fill_verification = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_VERIFICATION",
            "request_id": self.FILL,
            "remote_stage2_gate1_fill_equivalence": "PASS",
            "tracked_stage2_mutation": "NONE",
        }
        self.first = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": self.FIRST,
            "request_sha256": resume.sha256_bytes(self.bytes(self.first_request)),
            "preseal_status": "BLOCKED",
        }
        self.first_verification = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_VERIFICATION",
            "request_id": self.FIRST,
            "preseal_status": "BLOCKED",
            "remote_stage2_preseal_equivalence": "PASS",
            "tracked_stage2_mutation": "NONE",
        }
        self.fill_path = (
            f".remote-implementation/checkpoints/school/{self.FILL}/"
            "checkpoint-manifest.json"
        )
        self.fill_verification_path = (
            f".remote-implementation/verifications/school/{self.FILL}/"
            "stage2-gate1-fill-verification.json"
        )
        self.first_path = (
            f".remote-implementation/checkpoints/school/{self.FIRST}/"
            "checkpoint-manifest.json"
        )
        self.first_verification_path = (
            f".remote-implementation/verifications/school/{self.FIRST}/"
            "stage2-preseal-rehearsal-verification.json"
        )
        self.parent = {
            **self.identity,
            "operation": OP_STAGE2_PRESEAL_REHEARSAL,
            "request_id": self.REPLACEMENT,
        }
        self.manifest = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": self.REPLACEMENT,
            "preseal_status": "READY_TO_SEAL",
            "source_gate1_fill_request_id": self.FILL,
            "stage2_gate1_fill_checkpoint_path": self.fill_path,
            "stage2_gate1_fill_verification_path": self.fill_verification_path,
        }
        self.state = {
            "lifecycle_state": LIFECYCLE_IDLE,
            "transaction_state": TX_COMPLETE,
            "recovery_required": False,
            "active_request_id": None,
            "active_lock_commit": None,
            "accepted_request_ids": [],
            "consumed_request_ids": [],
            "abandoned_request_ids": [],
            "used": {self.FIRST},
        }
        self.extra_archives = {}
        self.extra_files = {}
        self.prior_states = {}
        self.last = {
            "fresh_runner_verification": "PASS",
            "request_id": self.REPLACEMENT,
        }

    @staticmethod
    def bytes(value):
        return (json.dumps(value, sort_keys=True) + "\n").encode()

    def prepare(self):
        self.files = {
            self.fill_path: self.bytes(self.fill),
            self.fill_verification_path: self.bytes(self.fill_verification),
            self.first_path: self.bytes(self.first),
            self.first_verification_path: self.bytes(self.first_verification),
        }
        self.fill_ref = {
            "path": self.fill_path,
            "sha256": resume.sha256_bytes(self.files[self.fill_path]),
        }
        self.fill_verification_ref = {
            "path": self.fill_verification_path,
            "sha256": resume.sha256_bytes(self.files[self.fill_verification_path]),
        }
        self.parent["stage2_gate1_fill_checkpoint"] = copy.deepcopy(self.fill_ref)
        self.parent["stage2_gate1_fill_verification"] = copy.deepcopy(
            self.fill_verification_ref
        )
        self.first_request["stage2_gate1_fill_checkpoint"] = copy.deepcopy(
            self.fill_ref
        )
        self.first_request["stage2_gate1_fill_verification"] = copy.deepcopy(
            self.fill_verification_ref
        )
        # The archived first request hash binds the complete request including
        # its original fill references.
        self.first["request_sha256"] = resume.sha256_bytes(
            self.bytes(self.first_request)
        )
        self.files[self.first_path] = self.bytes(self.first)
        self.manifest["stage2_gate1_fill_checkpoint_sha256"] = self.fill_ref["sha256"]
        self.manifest["stage2_gate1_fill_verification_sha256"] = (
            self.fill_verification_ref["sha256"]
        )

    def after_prepare(self):
        pass

    def call(self):
        self.prepare()
        self.after_prepare()

        def archive(control_head, request_id):
            self.assertEqual(control_head, self.CONTROL)
            request = (
                self.fill_request if request_id == self.FILL
                else self.first_request if request_id == self.FIRST
                else self.extra_archives.get(request_id)
            )
            if request is None:
                raise AssertionError("unexpected archived request " + request_id)
            return copy.deepcopy(request), self.bytes(request)

        def show(control_head, path):
            self.assertEqual(control_head, self.CONTROL)
            files = {**self.files, **self.extra_files}
            return files[path]

        def show_json(control_head, path):
            if path == ".remote-implementation/control-state.json":
                if control_head not in self.prior_states:
                    raise AssertionError("unexpected prior state " + control_head)
                return copy.deepcopy(self.prior_states[control_head])
            self.assertEqual(control_head, self.CONTROL)
            return {"request_id": self.REPLACEMENT}

        with (
            patch.object(resume, "_load_archived_request", side_effect=archive),
            patch.object(resume, "git_show_bytes", side_effect=show),
            patch.object(
                resume, "request_used",
                side_effect=lambda state, rid: rid in state["used"],
            ),
            patch.object(
                resume, "git_show_json",
                side_effect=show_json,
            ),
        ):
            return resume._resume_post_gate1_from_verified_replacement(
                self.parent,
                self.manifest,
                control_head=self.CONTROL,
                state=self.state,
                last=self.last,
            )

    def test_verified_blocked_predecessor_resumes_with_fresh_single_use_ids(self):
        spec = self.call()
        self.assertEqual(spec["preseal_request_id"], self.REPLACEMENT)
        self.assertEqual(spec["seal_request_id"], self.REPLACEMENT + "-seal")
        self.assertEqual(spec["apply_request_id"], self.REPLACEMENT + "-apply")
        validate_stage2_phase_continuation(
            OP_STAGE2_PRESEAL_REHEARSAL, self.REPLACEMENT, spec
        )

    def test_cannot_invent_continuation_without_original_approval(self):
        self.fill_request.pop("phase_continuation")
        self.fill["request_sha256"] = resume.sha256_bytes(
            self.bytes(self.fill_request)
        )
        self.assertIsNone(self.call())

    def test_changed_historical_decision_universe_fails(self):
        self.manifest["decision_universe_sha256"] = "f" * 64
        with self.assertRaisesRegex(Stop, "HISTORICAL_AUTHORITY_CHANGED"):
            self.call()

    def test_changed_target_fails(self):
        self.manifest["target_sha"] = "f" * 40
        with self.assertRaisesRegex(Stop, "HISTORICAL_AUTHORITY_CHANGED"):
            self.call()

    def test_changed_owner_gate1_approval_fails(self):
        self.manifest["owner_gate_1_approval_sha256"] = "f" * 64
        with self.assertRaisesRegex(Stop, "HISTORICAL_AUTHORITY_CHANGED"):
            self.call()

    def test_fill_requires_explicit_historical_owner_approval(self):
        self.fill["owner_gate_1_approval"]["approved"] = False
        with self.assertRaisesRegex(Stop, "FILL_AUTHORITY_NOT_VERIFIED"):
            self.call()

    def test_fill_requires_fresh_equivalence(self):
        self.fill_verification["remote_stage2_gate1_fill_equivalence"] = "FAIL"
        with self.assertRaisesRegex(Stop, "FILL_AUTHORITY_NOT_VERIFIED"):
            self.call()

    def test_earlier_preseal_must_be_blocked(self):
        self.first["preseal_status"] = "READY_TO_SEAL"
        with self.assertRaisesRegex(Stop, "NOT_VERIFIED_BLOCKED"):
            self.call()

    def test_earlier_preseal_must_be_independently_verified(self):
        self.first_verification["remote_stage2_preseal_equivalence"] = "FAIL"
        with self.assertRaisesRegex(Stop, "NOT_VERIFIED_BLOCKED"):
            self.call()

    def test_original_preseal_must_have_been_consumed(self):
        self.state["used"].clear()
        with self.assertRaisesRegex(Stop, "ORIGINAL_PRESEAL_LINEAGE_INVALID"):
            self.call()

    def test_original_seal_or_apply_cannot_have_run(self):
        self.state["used"].add(self.authorized["seal_request_id"])
        with self.assertRaisesRegex(Stop, "ORIGINAL_CHILD_ALREADY_CONSUMED"):
            self.call()

    def test_replacement_seal_id_cannot_be_reused(self):
        self.state["used"].add(self.REPLACEMENT + "-seal")
        with self.assertRaisesRegex(Stop, "REPLACEMENT_CHILD_ALREADY_USED"):
            self.call()

    def test_active_lock_stops_resumption(self):
        self.state["active_lock_commit"] = "f" * 40
        with self.assertRaisesRegex(Stop, "CONTROL_OR_PRESEAL_AUTHORITY_UNSAFE"):
            self.call()

    def test_unsafe_recovery_stops_resumption(self):
        self.state["recovery_required"] = True
        with self.assertRaisesRegex(Stop, "CONTROL_OR_PRESEAL_AUTHORITY_UNSAFE"):
            self.call()

    def test_changed_original_fill_target_tree_fails(self):
        self.fill["target_tree_sha"] = "f" * 40
        with self.assertRaisesRegex(Stop, "HISTORICAL_AUTHORITY_CHANGED"):
            self.call()

    def test_verified_replacement_queues_seal_without_an_owner_relay(self):
        spec = {
            "kind": STAGE2_POST_GATE1_CONTINUATION_KIND,
            "preseal_request_id": self.REPLACEMENT,
            "seal_request_id": self.REPLACEMENT + "-seal",
            "apply_request_id": self.REPLACEMENT + "-apply",
        }
        self.manifest["equivalence_sha256"] = "e" * 64
        self.manifest["request_sha256"] = resume.sha256_bytes(
            self.bytes(self.parent)
        )
        captured = {}
        with (
            patch.object(
                resume, "_load_archived_request",
                return_value=(self.parent, self.bytes(self.parent)),
            ),
            patch.object(
                resume, "_checkpoint_manifest",
                return_value=(
                    self.manifest,
                    {"path": "preseal-manifest.json", "sha256": "b" * 64},
                ),
            ),
            patch.object(
                resume, "_resume_post_gate1_from_verified_replacement",
                return_value=spec,
            ),
            patch.object(
                resume, "_verification_ref",
                return_value={"path": "preseal-verify.json", "sha256": "c" * 64},
            ),
            patch.object(
                resume, "_queue_request",
                side_effect=lambda request, **kwargs: captured.setdefault(
                    "request", request
                ),
            ),
        ):
            resume.queue_after_preseal(
                live_main="d" * 40,
                control_head="e" * 40,
                state=self.state,
                state_bytes=b"{}",
                last=self.last,
            )
        request = captured["request"]
        self.assertEqual(request["operation"], OP_STAGE2_GATE1_SEAL)
        self.assertEqual(request["request_id"], spec["seal_request_id"])
        self.assertEqual(request["phase_continuation"], spec)
        self.assertEqual(request["owner_gate_1_approval_sha256"], "9" * 64)
        self.assertEqual(request["equivalence_sha256"], "e" * 64)
        validate_request(request)


class AbandonedApplyResumeTests(VerifiedPresealReplacementTests):
    BLOCKED = "school-stage2-preseal-0002"
    REPLACEMENT = "school-stage2-preseal-0003"
    PRIOR = "d" * 40

    def after_prepare(self):
        self.first["preseal_status"] = "READY_TO_SEAL"
        self.first_verification["preseal_status"] = "READY_TO_SEAL"
        self.files[self.first_path] = self.bytes(self.first)
        self.files[self.first_verification_path] = self.bytes(self.first_verification)

        first_ref = {
            "path": self.first_path,
            "sha256": resume.sha256_bytes(self.files[self.first_path]),
        }
        first_verification_ref = {
            "path": self.first_verification_path,
            "sha256": resume.sha256_bytes(self.files[self.first_verification_path]),
        }

        seal_id = self.authorized["seal_request_id"]
        apply_id = self.authorized["apply_request_id"]
        seal_request = {
            "school_key": "school",
            "operation": OP_STAGE2_GATE1_SEAL,
            "request_id": seal_id,
            "phase_continuation": copy.deepcopy(self.authorized),
            "stage2_preseal_checkpoint": first_ref,
            "stage2_preseal_verification": first_verification_ref,
        }
        seal_path = (
            f".remote-implementation/checkpoints/school/{seal_id}/"
            "checkpoint-manifest.json"
        )
        seal_verification_path = (
            f".remote-implementation/verifications/school/{seal_id}/"
            "stage2-gate1-seal-verification.json"
        )
        seal = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT",
            "request_id": seal_id,
            "request_sha256": resume.sha256_bytes(self.bytes(seal_request)),
            "seal_status": "SEALED",
            "source_preseal_request_id": self.FIRST,
        }
        seal_verification = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_VERIFICATION",
            "request_id": seal_id,
            "seal_status": "SEALED",
            "remote_stage2_gate1_seal_equivalence": "PASS",
            "tracked_stage2_mutation": "NONE",
        }
        self.extra_files[seal_path] = self.bytes(seal)
        self.extra_files[seal_verification_path] = self.bytes(seal_verification)
        seal_ref = {
            "path": seal_path,
            "sha256": resume.sha256_bytes(self.extra_files[seal_path]),
        }
        seal_verification_ref = {
            "path": seal_verification_path,
            "sha256": resume.sha256_bytes(self.extra_files[seal_verification_path]),
        }
        apply_request = {
            "school_key": "school",
            "operation": "STAGE2_SEALED_APPLY",
            "request_id": apply_id,
            "stage2_gate1_seal_checkpoint": seal_ref,
            "stage2_gate1_seal_verification": seal_verification_ref,
        }
        writeahead_path = (
            f".remote-implementation/writeahead/school/{apply_id}/"
            "writeahead-manifest.json"
        )
        writeahead = {
            **{
                key: self.identity[key]
                for key in (
                    "integration_freeze_sha256",
                    "semantic_snapshot_sha256",
                    "decision_universe_sha256",
                    "recommendation_map_sha256",
                    "filled_review_sha256",
                    "decision_id_set_sha256",
                    "owner_gate_1_approval_sha256",
                )
            },
            "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
            "operation": "STAGE2_SEALED_APPLY",
            "request_id": apply_id,
            "request_sha256": resume.sha256_bytes(self.bytes(apply_request)),
            "mutation_state": "PREPARED_NOT_PUBLISHED",
            "target_branch": self.identity["target_branch"],
            "expected_target_predecessor_sha": self.identity["target_sha"],
            "prepared_parent_sha": self.identity["target_sha"],
        }
        self.extra_files[writeahead_path] = self.bytes(writeahead)
        self.extra_archives[seal_id] = seal_request
        self.extra_archives[apply_id] = apply_request

        blocked_request = {
            "school_key": "school",
            "operation": OP_STAGE2_PRESEAL_REHEARSAL,
            "request_id": self.BLOCKED,
            "target_branch": self.identity["target_branch"],
            "target_sha": self.identity["target_sha"],
            "stage2_gate1_fill_checkpoint": copy.deepcopy(self.fill_ref),
            "stage2_gate1_fill_verification": copy.deepcopy(self.fill_verification_ref),
        }
        blocked_path = (
            f".remote-implementation/checkpoints/school/{self.BLOCKED}/"
            "checkpoint-manifest.json"
        )
        blocked_verification_path = (
            f".remote-implementation/verifications/school/{self.BLOCKED}/"
            "stage2-preseal-rehearsal-verification.json"
        )
        blocked = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": self.BLOCKED,
            "request_sha256": resume.sha256_bytes(self.bytes(blocked_request)),
            "preseal_status": "BLOCKED",
        }
        blocked_verification = {
            **self.identity,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_VERIFICATION",
            "request_id": self.BLOCKED,
            "preseal_status": "BLOCKED",
            "remote_stage2_preseal_equivalence": "PASS",
            "tracked_stage2_mutation": "NONE",
        }
        self.extra_archives[self.BLOCKED] = blocked_request
        self.extra_files[blocked_path] = self.bytes(blocked)
        self.extra_files[blocked_verification_path] = self.bytes(blocked_verification)

        prior = initial_control_state()
        prior["transaction_state"] = TX_COMPLETE
        prior["accepted_request_ids"] = [self.FIRST, seal_id, apply_id, self.BLOCKED]
        prior["consumed_request_ids"] = [self.FIRST, seal_id, self.BLOCKED]
        prior["abandoned_request_ids"] = [apply_id]
        prior["last_operation"] = {
            "operation": OP_STAGE2_PRESEAL_REHEARSAL,
            "request_id": self.BLOCKED,
            "school_key": "school",
            "target_branch": self.identity["target_branch"],
            "target_sha": self.identity["target_sha"],
            "preseal_status": "BLOCKED",
            "fresh_runner_verification": "PASS",
            "checkpoint_manifest_path": blocked_path,
            "checkpoint_manifest_sha256": resume.sha256_bytes(
                self.extra_files[blocked_path]
            ),
        }
        self.prior_states[self.PRIOR] = prior
        self.parent["previous_control_state_commit"] = self.PRIOR

        self.state["accepted_request_ids"] = [self.FIRST, seal_id, apply_id, self.BLOCKED]
        self.state["consumed_request_ids"] = [self.FIRST, seal_id, self.BLOCKED]
        self.state["abandoned_request_ids"] = [apply_id]
        self.state["used"].update({seal_id, apply_id, self.BLOCKED})

    def test_abandoned_unpublished_apply_can_resume_from_exact_blocked_predecessor(self):
        spec = self.call()
        self.assertEqual(spec["preseal_request_id"], self.REPLACEMENT)
        self.assertEqual(spec["seal_request_id"], self.REPLACEMENT + "-seal")
        self.assertEqual(spec["apply_request_id"], self.REPLACEMENT + "-apply")

    def test_abandoned_apply_must_be_recorded(self):
        self.after_prepare = self._after_prepare_without_abandonment
        with self.assertRaisesRegex(Stop, "ORIGINAL_CHILD_RECOVERY_INVALID"):
            self.call()

    def _after_prepare_without_abandonment(self):
        AbandonedApplyResumeTests.after_prepare(self)
        self.state["abandoned_request_ids"].clear()

    def test_prior_control_state_must_be_verified_blocked_preseal(self):
        self.after_prepare = self._after_prepare_with_ready_prior
        with self.assertRaisesRegex(Stop, "BLOCKED_PREDECESSOR_STATE_INVALID"):
            self.call()

    def _after_prepare_with_ready_prior(self):
        AbandonedApplyResumeTests.after_prepare(self)
        self.prior_states[self.PRIOR]["last_operation"]["preseal_status"] = "READY_TO_SEAL"


if __name__ == "__main__":
    unittest.main()
