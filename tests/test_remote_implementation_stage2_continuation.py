import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_CENSUS,
    OP_STAGE2_CURRENT_MAIN_REFRESH,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    STAGE2_PHASE_CONTINUATION_KIND,
    RemoteImplementationError,
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


if __name__ == "__main__":
    unittest.main()
