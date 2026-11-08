import json
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_CENSUS,
    OP_STAGE2_CURRENT_MAIN_REFRESH,
    OP_STAGE2_GATE1_FILL,
    OP_STAGE2_PRESEAL_REHEARSAL,
    OP_STAGE2_GATE1_SEAL,
    OP_STAGE2_SEALED_APPLY,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    STAGE2_PHASE_CONTINUATION_KIND,
    STAGE2_POST_GATE1_CONTINUATION_KIND,
    RemoteImplementationError,
    validate_request,
    validate_stage2_phase_continuation,
)
from remote_implementation_io import Stop  # noqa: E402
import remote_implementation_stage2_continuation as continuation  # noqa: E402


def continuation_spec():
    return {
        "kind": STAGE2_PHASE_CONTINUATION_KIND,
        "census_request_id": "school-stage2-census-next",
        "proposal_request_id": "school-stage2-proposal-next",
        "expected_decision_universe_sha256": "d" * 64,
        "recommendation_map": {
            "path": ".remote-implementation/payloads/school/map.json",
            "sha256": "m" * 64,
        },
    }


class ContinuationValidationTests(unittest.TestCase):
    def test_refresh_continuation_is_valid(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        validate_stage2_phase_continuation(
            OP_STAGE2_CURRENT_MAIN_REFRESH,
            "school-stage2-refresh-next",
            spec,
        )

    def test_census_carries_same_census_identity(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        validate_stage2_phase_continuation(
            OP_STAGE2_CENSUS,
            spec["census_request_id"],
            spec,
        )

    def test_census_parent_mismatch_rejected(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        with self.assertRaisesRegex(RemoteImplementationError, "CENSUS_PARENT_MISMATCH"):
            validate_stage2_phase_continuation(
                OP_STAGE2_CENSUS,
                "different-census-id",
                spec,
            )

    def test_other_operation_cannot_carry_continuation(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        with self.assertRaisesRegex(RemoteImplementationError, "CONTINUATION_FORBIDDEN"):
            validate_stage2_phase_continuation(
                OP_STAGE2_PROPOSAL_REHEARSAL,
                "school-stage2-proposal-old",
                spec,
            )

    def test_child_ids_must_be_distinct_from_refresh_parent(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        spec["census_request_id"] = "school-stage2-refresh-next"
        with self.assertRaisesRegex(RemoteImplementationError, "REQUEST_IDS_NOT_DISTINCT"):
            validate_stage2_phase_continuation(
                OP_STAGE2_CURRENT_MAIN_REFRESH,
                "school-stage2-refresh-next",
                spec,
            )


class ContinuationPayloadBindingTests(unittest.TestCase):
    def test_refresh_payloads_bind_to_supplied_request_commit(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        request = {
            "request_id": "school-stage2-refresh-next",
            "operation": OP_STAGE2_CURRENT_MAIN_REFRESH,
            "phase_continuation": spec,
        }
        with patch.object(
            continuation,
            "_verify_payload_ref",
            return_value=b"payload",
        ) as verifier:
            continuation.verify_phase_continuation_payloads(
                request,
                "f" * 40,
            )
        verifier.assert_called_once_with(
            "f" * 40,
            spec["recommendation_map"],
            "RECOMMENDATION_MAP",
        )


class ContinuationDispatchTests(unittest.TestCase):
    def test_actions_authored_queue_explicitly_dispatches_control_workflow(self):
        completed = SimpleNamespace(returncode=0, stdout="")
        with patch.dict(
            os.environ,
            {
                "GITHUB_ACTIONS": "true",
                "GITHUB_REPOSITORY": "owner/repo",
                "GH_TOKEN": "token",
            },
            clear=True,
        ), patch.object(continuation, "run", return_value=completed) as runner:
            continuation._dispatch_child_workflow_if_actions("a" * 40)

        runner.assert_called_once_with(
            [
                "gh",
                "api",
                "--method",
                "POST",
                "repos/owner/repo/actions/workflows/remote-implementation.yml/dispatches",
                "-f",
                "ref=control/remote-implementation",
            ],
            check=False,
        )

    def test_external_queue_relies_on_push_and_does_not_dispatch(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(
            continuation, "run"
        ) as runner:
            continuation._dispatch_child_workflow_if_actions("a" * 40)
        runner.assert_not_called()

    def test_actions_dispatch_failure_is_fail_closed(self):
        completed = SimpleNamespace(returncode=1, stdout="dispatch denied")
        with patch.dict(
            os.environ,
            {
                "GITHUB_ACTIONS": "true",
                "GITHUB_REPOSITORY": "owner/repo",
                "GH_TOKEN": "token",
            },
            clear=True,
        ), patch.object(continuation, "run", return_value=completed):
            with self.assertRaisesRegex(
                Stop, "STAGE2_CONTINUATION_WORKFLOW_DISPATCH_FAILED"
            ):
                continuation._dispatch_child_workflow_if_actions("a" * 40)

    def test_queue_dispatches_only_after_successful_control_push(self):
        request = {
            "request_id": "school-stage2-census-next",
            "operation": OP_STAGE2_CENSUS,
        }
        with patch.object(
            continuation, "_already_queued", return_value=False
        ), patch.object(
            continuation, "validate_request"
        ), patch.object(
            continuation, "write_json"
        ), patch.object(
            continuation,
            "git",
            return_value=SimpleNamespace(stdout="1" * 40 + "\n"),
        ), patch.object(
            continuation, "push_control", return_value="2" * 40
        ) as push, patch.object(
            continuation, "_dispatch_child_workflow_if_actions"
        ) as dispatch:
            result = continuation._queue_request(
                request,
                expected_control_head="1" * 40,
                state={},
            )

        self.assertEqual(result, "2" * 40)
        push.assert_called_once_with("1" * 40)
        dispatch.assert_called_once_with("2" * 40)

    def test_already_queued_request_does_not_dispatch_again(self):
        with patch.object(
            continuation, "_already_queued", return_value=True
        ), patch.object(
            continuation, "_dispatch_child_workflow_if_actions"
        ) as dispatch:
            result = continuation._queue_request(
                {
                    "request_id": "school-stage2-census-next",
                    "operation": OP_STAGE2_CENSUS,
                },
                expected_control_head="1" * 40,
                state={},
            )
        self.assertEqual(result, "1" * 40)
        dispatch.assert_not_called()

    def test_control_workflow_exposes_dispatch_and_actions_write(self):
        workflow = (
            ROOT / ".github/workflows/remote-implementation.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("actions: write", workflow)
        self.assertIn("github.event_name == 'workflow_dispatch'", workflow)


class ContinuationMainAdvanceTests(unittest.TestCase):
    def test_verified_refresh_with_newer_live_main_does_not_queue_stale_census(self):
        state = {
            "lifecycle_state": "IDLE",
            "last_operation": {
                "operation": OP_STAGE2_CURRENT_MAIN_REFRESH,
                "fresh_runner_verification": "PASS",
                "protected_main_sha": "a" * 40,
            },
        }
        with patch.object(
            continuation, "configure_git"
        ), patch.object(
            continuation,
            "fetch_operational_refs",
            return_value=("b" * 40, "c" * 40),
        ), patch.object(
            continuation,
            "git_show_bytes",
            return_value=json.dumps(state).encode(),
        ), patch.object(
            continuation, "validate_control_state"
        ), patch.object(
            continuation, "queue_after_refresh"
        ) as queue:
            code = continuation.main()
        self.assertEqual(code, 0)
        queue.assert_not_called()


class QueueAfterRefreshTests(unittest.TestCase):
    def parent(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        return {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_REQUEST",
            "request_id": "school-stage2-refresh-next",
            "school_key": "school",
            "operation": OP_STAGE2_CURRENT_MAIN_REFRESH,
            "target_branch": "data/school-onboarding",
            "target_sha": "1" * 40,
            "phase0_successor": {
                "path": ".remote-implementation/successors/school/phase0.json",
                "sha256": "2" * 64,
            },
            "integration_freeze_sha256": "3" * 64,
            "semantic_snapshot_sha256": "4" * 64,
            "phase_continuation": spec,
        }

    def test_queues_census_against_refreshed_target(self):
        parent = self.parent()
        successor = {
            "actual_published_target_sha": "5" * 40,
        }
        captured = {}

        def fake_verify(_head, ref, label):
            if label == "REFRESH_SUCCESSOR":
                return json.dumps(successor).encode()
            return b"payload"

        def fake_queue(request, **kwargs):
            captured["request"] = request
            return "queued"

        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ), patch.object(
            continuation, "_verify_payload_ref", side_effect=fake_verify
        ), patch.object(
            continuation, "_queue_request", side_effect=fake_queue
        ):
            code = continuation.queue_after_refresh(
                live_main="6" * 40,
                control_head="7" * 40,
                state={"accepted_request_ids": [], "consumed_request_ids": [], "abandoned_request_ids": []},
                state_bytes=b"{}",
                last={
                    "request_id": parent["request_id"],
                    "successor_manifest_path": ".remote-implementation/successors/school/refresh.json",
                    "successor_manifest_sha256": "8" * 64,
                    "target_sha": "5" * 40,
                },
            )

        self.assertEqual(code, 0)
        request = captured["request"]
        self.assertEqual(request["operation"], OP_STAGE2_CENSUS)
        self.assertEqual(
            request["request_id"],
            parent["phase_continuation"]["census_request_id"],
        )
        self.assertEqual(request["target_sha"], "5" * 40)
        self.assertTrue(request["authority"]["stage2_census"])
        self.assertEqual(
            request["stage2_current_main_refresh_successor"]["sha256"],
            "8" * 64,
        )
        self.assertEqual(
            request["phase_continuation"],
            parent["phase_continuation"],
        )


class QueueAfterCensusTests(unittest.TestCase):
    def parent(self):
        spec = continuation_spec()
        spec["recommendation_map"]["sha256"] = "a" * 64
        return {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_REQUEST",
            "request_id": spec["census_request_id"],
            "school_key": "school",
            "operation": OP_STAGE2_CENSUS,
            "target_branch": "data/school-onboarding",
            "target_sha": "5" * 40,
            "integration_freeze_sha256": "3" * 64,
            "semantic_snapshot_sha256": "4" * 64,
            "phase_continuation": spec,
        }

    def test_queues_proposal_only_after_exact_universe(self):
        parent = self.parent()
        captured = {}

        def fake_queue(request, **kwargs):
            captured["request"] = request
            return "queued"

        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ), patch.object(
            continuation, "_verify_payload_ref", return_value=b"payload"
        ), patch.object(
            continuation, "_queue_request", side_effect=fake_queue
        ):
            code = continuation.queue_after_census(
                live_main="6" * 40,
                control_head="7" * 40,
                state={"accepted_request_ids": [], "consumed_request_ids": [], "abandoned_request_ids": []},
                state_bytes=b"{}",
                last={
                    "request_id": parent["request_id"],
                    "stage2_status": "CAPABILITY_CENSUS_READY",
                    "decision_universe_sha256": parent["phase_continuation"][
                        "expected_decision_universe_sha256"
                    ],
                    "checkpoint_manifest_path": ".remote-implementation/checkpoints/school/census/checkpoint-manifest.json",
                    "checkpoint_manifest_sha256": "8" * 64,
                },
            )

        self.assertEqual(code, 0)
        request = captured["request"]
        self.assertEqual(request["operation"], OP_STAGE2_PROPOSAL_REHEARSAL)
        self.assertEqual(
            request["request_id"],
            parent["phase_continuation"]["proposal_request_id"],
        )
        self.assertEqual(
            request["decision_universe_sha256"],
            parent["phase_continuation"]["expected_decision_universe_sha256"],
        )
        self.assertTrue(request["authority"]["stage2_proposal_rehearsal"])
        self.assertNotIn("phase_continuation", request)

    def test_changed_decision_universe_stops_chain(self):
        parent = self.parent()
        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ):
            with self.assertRaisesRegex(Stop, "DECISION_UNIVERSE_CHANGED"):
                continuation.queue_after_census(
                    live_main="6" * 40,
                    control_head="7" * 40,
                    state={"accepted_request_ids": [], "consumed_request_ids": [], "abandoned_request_ids": []},
                    state_bytes=b"{}",
                    last={
                        "request_id": parent["request_id"],
                        "stage2_status": "CAPABILITY_CENSUS_READY",
                        "decision_universe_sha256": "e" * 64,
                        "checkpoint_manifest_path": ".remote-implementation/checkpoints/school/census/checkpoint-manifest.json",
                        "checkpoint_manifest_sha256": "8" * 64,
                    },
                )

    def test_blocked_census_stops_chain(self):
        parent = self.parent()
        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ):
            with self.assertRaisesRegex(Stop, "CENSUS_NOT_READY"):
                continuation.queue_after_census(
                    live_main="6" * 40,
                    control_head="7" * 40,
                    state={"accepted_request_ids": [], "consumed_request_ids": [], "abandoned_request_ids": []},
                    state_bytes=b"{}",
                    last={
                        "request_id": parent["request_id"],
                        "stage2_status": "BLOCKED",
                        "decision_universe_sha256": parent["phase_continuation"][
                            "expected_decision_universe_sha256"
                        ],
                    },
                )


def post_gate1_spec():
    return {
        "kind": STAGE2_POST_GATE1_CONTINUATION_KIND,
        "preseal_request_id": "school-stage2-preseal-next",
        "seal_request_id": "school-stage2-seal-next",
        "apply_request_id": "school-stage2-apply-next",
    }


class PostGate1ContinuationValidationTests(unittest.TestCase):
    def test_fill_can_start_post_gate1_chain(self):
        validate_stage2_phase_continuation(
            OP_STAGE2_GATE1_FILL,
            "school-stage2-fill-approved",
            post_gate1_spec(),
        )

    def test_preseal_and_seal_must_carry_exact_child_identity(self):
        spec = post_gate1_spec()
        validate_stage2_phase_continuation(
            OP_STAGE2_PRESEAL_REHEARSAL,
            spec["preseal_request_id"],
            spec,
        )
        validate_stage2_phase_continuation(
            OP_STAGE2_GATE1_SEAL,
            spec["seal_request_id"],
            spec,
        )

    def test_post_gate1_chain_cannot_start_before_owner_gate(self):
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "POST_GATE1_CONTINUATION_FORBIDDEN",
        ):
            validate_stage2_phase_continuation(
                OP_STAGE2_PROPOSAL_REHEARSAL,
                "school-stage2-proposal",
                post_gate1_spec(),
            )

    def test_apply_is_terminal_and_cannot_carry_continuation(self):
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "POST_GATE1_CONTINUATION_FORBIDDEN",
        ):
            validate_stage2_phase_continuation(
                OP_STAGE2_SEALED_APPLY,
                "school-stage2-apply-next",
                post_gate1_spec(),
            )


def _post_gate_parent(operation, request_id):
    return {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": request_id,
        "school_key": "school",
        "operation": operation,
        "target_branch": "data/school-onboarding",
        "target_sha": "1" * 40,
        "phase_continuation": post_gate1_spec(),
    }


class QueueAfterGate1FillTests(unittest.TestCase):
    def test_fill_queues_preseal_from_fresh_checkpoint(self):
        parent = _post_gate_parent(
            OP_STAGE2_GATE1_FILL,
            "school-stage2-fill-approved",
        )
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT",
            "request_id": parent["request_id"],
            "school_key": "school",
            "target_branch": parent["target_branch"],
            "target_sha": parent["target_sha"],
            "gate1_fill_status": "FILLED",
            "integration_freeze_sha256": "2" * 64,
            "semantic_snapshot_sha256": "3" * 64,
            "decision_universe_sha256": "4" * 64,
            "recommendation_map_sha256": "5" * 64,
            "approved_plan_hash_preview": "6" * 64,
            "filled_review_sha256": "7" * 64,
            "decision_id_set_sha256": "8" * 64,
        }
        captured = {}
        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ), patch.object(
            continuation,
            "_checkpoint_manifest",
            return_value=(
                manifest,
                {"path": "fill.json", "sha256": "9" * 64},
            ),
        ), patch.object(
            continuation,
            "_verification_ref",
            return_value={"path": "fill-verification.json", "sha256": "a" * 64},
        ), patch.object(
            continuation,
            "_queue_request",
            side_effect=lambda request, **kwargs: captured.setdefault("request", request),
        ):
            continuation.queue_after_gate1_fill(
                live_main="b" * 40,
                control_head="c" * 40,
                state={},
                state_bytes=b"{}",
                last={"request_id": parent["request_id"]},
            )
        request = captured["request"]
        self.assertEqual(request["operation"], OP_STAGE2_PRESEAL_REHEARSAL)
        self.assertEqual(
            request["request_id"],
            parent["phase_continuation"]["preseal_request_id"],
        )
        self.assertTrue(request["authority"]["stage2_preseal_rehearsal"])
        self.assertEqual(request["phase_continuation"], parent["phase_continuation"])
        validate_request(request)


class QueueAfterPresealTests(unittest.TestCase):
    def test_ready_preseal_queues_seal(self):
        spec = post_gate1_spec()
        parent = _post_gate_parent(OP_STAGE2_PRESEAL_REHEARSAL, spec["preseal_request_id"])
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": parent["request_id"],
            "school_key": "school",
            "target_branch": parent["target_branch"],
            "target_sha": parent["target_sha"],
            "preseal_status": "READY_TO_SEAL",
            "integration_freeze_sha256": "2" * 64,
            "semantic_snapshot_sha256": "3" * 64,
            "decision_universe_sha256": "4" * 64,
            "recommendation_map_sha256": "5" * 64,
            "approved_plan_hash_preview": "6" * 64,
            "filled_review_sha256": "7" * 64,
            "decision_id_set_sha256": "8" * 64,
            "owner_gate_1_approval_sha256": "9" * 64,
            "equivalence_sha256": "a" * 64,
        }
        captured = {}
        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ), patch.object(
            continuation,
            "_checkpoint_manifest",
            return_value=(manifest, {"path": "preseal.json", "sha256": "b" * 64}),
        ), patch.object(
            continuation,
            "_verification_ref",
            return_value={"path": "preseal-verification.json", "sha256": "c" * 64},
        ), patch.object(
            continuation,
            "_queue_request",
            side_effect=lambda request, **kwargs: captured.setdefault("request", request),
        ):
            continuation.queue_after_preseal(
                live_main="d" * 40,
                control_head="e" * 40,
                state={},
                state_bytes=b"{}",
                last={"request_id": parent["request_id"]},
            )
        request = captured["request"]
        self.assertEqual(request["operation"], OP_STAGE2_GATE1_SEAL)
        self.assertTrue(request["authority"]["stage2_gate1_seal"])
        self.assertEqual(request["equivalence_sha256"], "a" * 64)
        validate_request(request)

    def test_blocked_preseal_stops_before_seal(self):
        spec = post_gate1_spec()
        parent = _post_gate_parent(OP_STAGE2_PRESEAL_REHEARSAL, spec["preseal_request_id"])
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "preseal_status": "BLOCKED",
        }
        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ), patch.object(
            continuation,
            "_checkpoint_manifest",
            return_value=(manifest, {"path": "preseal.json", "sha256": "b" * 64}),
        ):
            with self.assertRaisesRegex(Stop, "PRESEAL_NOT_READY"):
                continuation.queue_after_preseal(
                    live_main="d" * 40,
                    control_head="e" * 40,
                    state={},
                    state_bytes=b"{}",
                    last={"request_id": parent["request_id"]},
                )


class QueueAfterGate1SealTests(unittest.TestCase):
    def test_fresh_seal_queues_apply(self):
        spec = post_gate1_spec()
        parent = _post_gate_parent(OP_STAGE2_GATE1_SEAL, spec["seal_request_id"])
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT",
            "request_id": parent["request_id"],
            "school_key": "school",
            "target_branch": parent["target_branch"],
            "target_sha": parent["target_sha"],
            "seal_status": "SEALED",
            "approved_plan_hash": "2" * 64,
            "approved_plan_sha256": "3" * 64,
            "owner_gate_1_approval_sha256": "4" * 64,
            "integration_freeze_sha256": "5" * 64,
            "semantic_snapshot_sha256": "6" * 64,
            "decision_universe_sha256": "7" * 64,
            "recommendation_map_sha256": "8" * 64,
            "filled_review_sha256": "9" * 64,
            "decision_id_set_sha256": "a" * 64,
        }
        captured = {}
        with patch.object(
            continuation, "_load_archived_request", return_value=(parent, b"{}")
        ), patch.object(
            continuation,
            "_checkpoint_manifest",
            return_value=(manifest, {"path": "seal.json", "sha256": "b" * 64}),
        ), patch.object(
            continuation,
            "_verification_ref",
            return_value={"path": "seal-verification.json", "sha256": "c" * 64},
        ), patch.object(
            continuation,
            "_queue_request",
            side_effect=lambda request, **kwargs: captured.setdefault("request", request),
        ):
            continuation.queue_after_gate1_seal(
                live_main="d" * 40,
                control_head="e" * 40,
                state={},
                state_bytes=b"{}",
                last={"request_id": parent["request_id"]},
            )
        request = captured["request"]
        self.assertEqual(request["operation"], OP_STAGE2_SEALED_APPLY)
        self.assertEqual(request["request_id"], spec["apply_request_id"])
        self.assertTrue(request["authority"]["stage2_sealed_apply"])
        self.assertNotIn("phase_continuation", request)
        self.assertEqual(request["approved_plan_hash"], "2" * 64)
        validate_request(request)


if __name__ == "__main__":
    unittest.main()
