import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import remote_implementation_runner as runner  # noqa: E402
import remote_implementation_stage2_gate1_fill as gate1  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_GATE1_FILL,
    REQUEST_KIND,
    RemoteImplementationError,
    begin_request,
    initial_control_state,
    validate_request,
)
from remote_implementation_io import Stop  # noqa: E402

MAIN = "a" * 40
CONTROL = "b" * 40
TARGET = "c" * 40
TREE = "d" * 40
FREEZE_SHA = "1" * 64
SEMANTIC_SHA = "2" * 64
DECISION_SHA = "3" * 64
MAP_SHA = "4" * 64
CHECKPOINT_SHA = "5" * 64
VERIFICATION_SHA = "6" * 64
PLAN_PREVIEW = "7" * 64
SCHOOL = "example-school"
BRANCH = f"data/{SCHOOL}-onboarding"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def request():
    checkpoint_path = (
        ".remote-implementation/checkpoints/example-school/"
        "proposal-001/checkpoint-manifest.json"
    )
    verification_path = (
        ".remote-implementation/verifications/example-school/"
        "proposal-001/stage2-proposal-rehearsal-verification.json"
    )
    return {
        "schema_version": 1,
        "kind": REQUEST_KIND,
        "request_id": "gate1-fill-001",
        "school_key": SCHOOL,
        "operation": OP_STAGE2_GATE1_FILL,
        "previous_control_state_commit": CONTROL,
        "previous_control_state_sha256": "8" * 64,
        "expected_protected_main_sha": MAIN,
        "creation_provenance": {
            "origin": "ChatGPT",
            "authorization": "Owner explicitly approved exact Gate 1 proposal.",
        },
        "authority": {
            "owner_gate_1": True,
            "owner_gate_2": False,
            "release": False,
            "phase0": False,
            "recovery": False,
            "stage2_census": False,
            "stage2_opponent_display_normalize": False,
            "stage2_proposal_rehearsal": False,
            "stage2_reconciliation_diagnostic": False,
            "stage2_gate1_fill": True,
        },
        "target_branch": BRANCH,
        "target_sha": TARGET,
        "stage2_proposal_checkpoint": {
            "path": checkpoint_path,
            "sha256": CHECKPOINT_SHA,
        },
        "stage2_proposal_verification": {
            "path": verification_path,
            "sha256": VERIFICATION_SHA,
        },
        "integration_freeze_sha256": FREEZE_SHA,
        "semantic_snapshot_sha256": SEMANTIC_SHA,
        "decision_universe_sha256": DECISION_SHA,
        "recommendation_map_sha256": MAP_SHA,
        "approved_plan_hash_preview": PLAN_PREVIEW,
        "owner_gate_1_approval": {
            "approved": True,
            "approval_basis": "Explicit owner approval in ChatGPT.",
            "proposal_checkpoint_sha256": CHECKPOINT_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
        },
    }


class RemoteStage2Gate1FillTests(unittest.TestCase):
    def authority_fixture(self):
        req = request()
        proposal_request_bytes = (
            json.dumps({"request_id": "proposal-001"}, sort_keys=True) + "\n"
        ).encode()
        map_bytes = b'{"decisions":{}}\n'
        plan_bytes = b'{"decisions":[]}\n'
        review_bytes = (
            b"decision_id,category,decision,resolution_basis\n"
            b"D-1,publication,,\n"
        )
        checkpoint_path = req["stage2_proposal_checkpoint"]["path"]
        directory = Path(checkpoint_path).parent
        map_path = (directory / "recommendation-map.json").as_posix()
        manifest = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT",
            "request_id": "proposal-001",
            "request_sha256": sha(proposal_request_bytes),
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "stage2_status": "OWNER_GATE_1_READY",
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_checkpoint_path": map_path,
            "recommendation_map_sha256": sha(map_bytes),
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "action_counts": {"ENABLE_PUBLIC_PAGE": 1},
            "preflight": {"decision_count": 1},
            "artifact_sha256": {
                "plan.json": sha(plan_bytes),
                "review.csv": sha(review_bytes),
            },
        }
        checkpoint_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        verification = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_VERIFICATION",
            "request_id": "proposal-001",
            "school_key": SCHOOL,
            "target_sha": TARGET,
            "stage2_status": "OWNER_GATE_1_READY",
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": sha(map_bytes),
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "tracked_stage2_mutation": "NONE",
            "remote_stage2_proposal_equivalence": "PASS",
        }
        verification_bytes = (
            json.dumps(verification, indent=2, sort_keys=True) + "\n"
        ).encode()
        req["stage2_proposal_checkpoint"]["sha256"] = sha(checkpoint_bytes)
        req["stage2_proposal_verification"]["sha256"] = sha(verification_bytes)
        req["recommendation_map_sha256"] = sha(map_bytes)
        req["owner_gate_1_approval"]["proposal_checkpoint_sha256"] = sha(
            checkpoint_bytes
        )
        req["owner_gate_1_approval"]["recommendation_map_sha256"] = sha(map_bytes)
        mapping = {
            checkpoint_path: checkpoint_bytes,
            req["stage2_proposal_verification"]["path"]: verification_bytes,
            (directory / "request.json").as_posix(): proposal_request_bytes,
            map_path: map_bytes,
            (directory / "plan.json").as_posix(): plan_bytes,
            (directory / "review.csv").as_posix(): review_bytes,
        }
        return req, manifest, verification, mapping

    def test_control_accepts_exact_gate1_fill_authority(self):
        req = request()
        validate_request(req)
        state = begin_request(
            initial_control_state(),
            req,
            "9" * 64,
            run_id="100",
            run_attempt="1",
            request_commit="e" * 40,
        )
        self.assertEqual(state["lifecycle_state"], "READ_ONLY_ACTIVE")
        self.assertEqual(state["transaction_state"], "STAGE2_GATE1_FILL_RUNNING")
        self.assertIsNone(state["active_lock_commit"])
        self.assertTrue(state["recovery_required"])

    def test_control_rejects_missing_owner_approval_or_binding_drift(self):
        req = request()
        req["authority"]["owner_gate_1"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_GATE1_FILL_OWNER_GATE1_AUTHORITY_REQUIRED",
        ):
            validate_request(req)

        req = request()
        req["owner_gate_1_approval"]["recommendation_map_sha256"] = "f" * 64
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_GATE1_FILL_OWNER_APPROVAL_BINDING_MISMATCH",
        ):
            validate_request(req)

    def test_non_gate1_operation_still_rejects_gate1_fill_authority(self):
        req = request()
        req["operation"] = "STAGE2_PROPOSAL_REHEARSAL"
        req["authority"]["owner_gate_1"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "REQUEST_GATE1_FILL_AUTHORITY_FORBIDDEN",
        ):
            validate_request(req)

    def test_ready_proposal_and_fresh_verification_authenticate(self):
        req, manifest, verification, mapping = self.authority_fixture()

        with (
            patch.object(
                gate1,
                "git_show_bytes",
                side_effect=lambda commit, path, **kwargs: mapping[path],
            ),
            patch.object(
                gate1,
                "verify_stage2_proposal_authority",
                return_value={"freeze_bytes": b"freeze"},
            ),
        ):
            result = gate1.verify_stage2_gate1_fill_authority(req, CONTROL)

        self.assertEqual(result["proposal_manifest"], manifest)
        self.assertEqual(result["proposal_verification"], verification)
        self.assertEqual(result["target_tree_sha"], TREE)
        self.assertEqual(result["expected_action_counts"], {"ENABLE_PUBLIC_PAGE": 1})
        self.assertEqual(result["expected_decision_count"], 1)

    def test_nonready_or_unverified_proposal_is_refused(self):
        req, manifest, verification, mapping = self.authority_fixture()
        checkpoint_path = req["stage2_proposal_checkpoint"]["path"]
        manifest["stage2_status"] = "BLOCKED"
        checkpoint_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        mapping[checkpoint_path] = checkpoint_bytes
        req["stage2_proposal_checkpoint"]["sha256"] = sha(checkpoint_bytes)

        with patch.object(
            gate1,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_GATE1_FILL_PROPOSAL_NOT_READY",
            ):
                gate1.verify_stage2_gate1_fill_authority(req, CONTROL)

        req, manifest, verification, mapping = self.authority_fixture()
        verification_path = req["stage2_proposal_verification"]["path"]
        verification["remote_stage2_proposal_equivalence"] = "PENDING"
        verification_bytes = (
            json.dumps(verification, indent=2, sort_keys=True) + "\n"
        ).encode()
        mapping[verification_path] = verification_bytes
        req["stage2_proposal_verification"]["sha256"] = sha(verification_bytes)
        with patch.object(
            gate1,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_GATE1_FILL_PROPOSAL_EQUIVALENCE_NOT_PASS",
            ):
                gate1.verify_stage2_gate1_fill_authority(req, CONTROL)

    def test_permanent_fill_proves_exact_actions_and_no_tracked_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            review = (
                "decision_id,category,decision,resolution_basis\n"
                "D-1,publication,ENABLE_PUBLIC_PAGE,Owner approved\n"
            ).encode()

            def fake_run(command, **kwargs):
                review_path = (
                    root / ".onboarding" / SCHOOL / gate1.SOURCE_REVIEW
                )
                review_path.write_bytes(review)
                return subprocess.CompletedProcess(command, 0, stdout="PASS\n")

            with (
                patch.object(gate1, "restore_integration_freeze"),
                patch.object(
                    gate1,
                    "tracked_worktree_state",
                    side_effect=[clean, clean],
                ),
                patch.object(gate1, "run", side_effect=fake_run),
            ):
                result = gate1.run_stage2_gate1_fill_tool(
                    root,
                    SCHOOL,
                    freeze_bytes=b"freeze",
                    map_bytes=b"{}\n",
                    plan_bytes=b"{}\n",
                    review_bytes=(
                        b"decision_id,category,decision,resolution_basis\n"
                        b"D-1,publication,,\n"
                    ),
                    expected_action_counts={"ENABLE_PUBLIC_PAGE": 1},
                    expected_decision_count=1,
                    diag=root / "diag",
                    tool_repo=ROOT,
                )

            self.assertEqual(result["decision_count"], 1)
            self.assertEqual(
                result["action_counts"],
                {"ENABLE_PUBLIC_PAGE": 1},
            )
            self.assertEqual(
                result["tracked_mutation_proof"]["tracked_stage2_mutation"],
                "NONE",
            )

    def test_permanent_fill_refuses_tracked_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            dirty = {
                "head_sha": TARGET,
                "tree_sha": TREE,
                "status": " M schools/example/source-games.csv\n",
            }
            with (
                patch.object(gate1, "restore_integration_freeze"),
                patch.object(
                    gate1,
                    "tracked_worktree_state",
                    side_effect=[clean, dirty],
                ),
                patch.object(
                    gate1,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, stdout=""),
                ),
            ):
                with self.assertRaisesRegex(
                    Stop,
                    "STAGE2_GATE1_FILL_TRACKED_MUTATION_DETECTED",
                ):
                    gate1.run_stage2_gate1_fill_tool(
                        root,
                        SCHOOL,
                        freeze_bytes=b"freeze",
                        map_bytes=b"{}\n",
                        plan_bytes=b"{}\n",
                        review_bytes=b"decision_id,decision,resolution_basis\n",
                        expected_action_counts={},
                        expected_decision_count=0,
                        diag=root / "diag",
                        tool_repo=ROOT,
                    )

    def test_runner_refuses_changed_target_before_acceptance(self):
        req = request()
        with (
            patch.object(
                runner,
                "verify_stage2_gate1_fill_authority",
                return_value={"target_tree_sha": TREE},
            ),
            patch.object(runner, "remote_head", return_value="f" * 40),
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_GATE1_FILL_TARGET_HEAD_MISMATCH",
            ):
                runner.run_read_only_stage2_gate1_fill(
                    initial_control_state(),
                    req,
                    b"{}",
                    "e" * 40,
                    CONTROL,
                    MAIN,
                )

    def test_runner_executes_and_checkpoints_gate1_fill(self):
        req = request()
        authority = {
            "target_tree_sha": TREE,
            "freeze_bytes": b"freeze",
            "map_bytes": b"map",
            "plan_bytes": b"plan",
            "review_bytes": b"review",
            "expected_action_counts": {"ENABLE_PUBLIC_PAGE": 1},
            "expected_decision_count": 1,
        }
        result = {
            "filled_review_bytes": b"filled",
            "filled_review_sha256": sha(b"filled"),
            "tracked_mutation_proof": {"after_tree_sha": TREE},
        }
        cp = subprocess.CompletedProcess([], 0, stdout=TREE + "\n")
        with tempfile.TemporaryDirectory() as directory:
            worktree = Path(directory)
            with (
                patch.object(
                    runner,
                    "verify_stage2_gate1_fill_authority",
                    return_value=authority,
                ),
                patch.object(runner, "remote_head", side_effect=[TARGET, TARGET]),
                patch.object(
                    runner,
                    "begin_request",
                    return_value=initial_control_state(),
                ),
                patch.object(runner, "write_json"),
                patch.object(runner, "archive_request", return_value=Path("archive")),
                patch.object(runner, "commit_control", return_value="1" * 40),
                patch.object(
                    runner,
                    "add_existing_onboarding_worktree",
                    return_value=worktree,
                ),
                patch.object(runner, "git", return_value=cp),
                patch.object(
                    runner,
                    "run_stage2_gate1_fill_tool",
                    return_value=result,
                ) as run_tool,
                patch.object(runner, "assert_protected_main_unchanged"),
                patch.object(
                    runner,
                    "persist_stage2_gate1_fill_checkpoint",
                    return_value="2" * 40,
                ) as persist,
            ):
                runner.run_read_only_stage2_gate1_fill(
                    initial_control_state(),
                    req,
                    b"{}",
                    "e" * 40,
                    CONTROL,
                    MAIN,
                )
        run_tool.assert_called_once()
        persist.assert_called_once()

    def test_fresh_verifier_replays_exact_fill_and_marks_equivalence(self):
        request_bytes = b'{"request_id":"gate1-fill-001"}\n'
        filled = b"decision_id,decision,resolution_basis\nD-1,X,basis\n"
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT",
            "request_id": "gate1-fill-001",
            "request_sha256": sha(request_bytes),
            "school_key": SCHOOL,
            "protected_main_sha": MAIN,
            "runtime_tool_sha256": "toolhash",
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "stage2_proposal_checkpoint_sha256": CHECKPOINT_SHA,
            "stage2_proposal_verification_sha256": VERIFICATION_SHA,
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "owner_gate_1_approval_sha256": "a" * 64,
            "source_review_sha256": "b" * 64,
            "filled_review_checkpoint_path": (
                ".remote-implementation/checkpoints/example-school/"
                "gate1-fill-001/filled-review.csv"
            ),
            "filled_review_sha256": sha(filled),
            "plan_sha256": "c" * 64,
            "decision_count": 1,
            "action_counts": {"X": 1},
            "decision_id_set_sha256": "d" * 64,
        }
        manifest_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        checkpoint_path = (
            ".remote-implementation/checkpoints/example-school/"
            "gate1-fill-001/checkpoint-manifest.json"
        )
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_GATE1_FILL,
            "request_id": "gate1-fill-001",
            "checkpoint_manifest_path": checkpoint_path,
            "checkpoint_manifest_sha256": sha(manifest_bytes),
            "target_sha": TARGET,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "owner_gate_1_approval_sha256": "a" * 64,
            "filled_review_sha256": sha(filled),
            "decision_id_set_sha256": "d" * 64,
            "fresh_runner_verification": "PENDING",
        }
        mapping = {
            checkpoint_path: manifest_bytes,
            (Path(checkpoint_path).parent / "request.json").as_posix(): request_bytes,
            manifest["filled_review_checkpoint_path"]: filled,
        }
        result = {
            "runtime_tool_sha256": "toolhash",
            "source_review_sha256": "b" * 64,
            "filled_review_sha256": sha(filled),
            "plan_sha256": "c" * 64,
            "recommendation_map_sha256": MAP_SHA,
            "decision_count": 1,
            "action_counts": {"X": 1},
            "decision_id_set_sha256": "d" * 64,
            "tracked_mutation_proof": {"tracked_stage2_mutation": "NONE"},
        }
        cp = subprocess.CompletedProcess([], 0, stdout=TREE + "\n")
        with tempfile.TemporaryDirectory() as directory:
            worktree = Path(directory)
            with (
                patch.object(
                    verifier,
                    "git_show_bytes",
                    side_effect=lambda commit, path: mapping[path],
                ),
                patch.object(
                    verifier,
                    "verify_stage2_gate1_fill_authority",
                    return_value={
                        "owner_gate_1_approval_sha256": "a" * 64,
                        "freeze_bytes": b"freeze",
                        "map_bytes": b"map",
                        "plan_bytes": b"plan",
                        "review_bytes": b"review",
                        "target_tree_sha": TREE,
                        "expected_action_counts": {"X": 1},
                        "expected_decision_count": 1,
                    },
                ),
                patch.object(verifier, "remote_head", return_value=TARGET),
                patch.object(
                    verifier,
                    "add_existing_onboarding_worktree",
                    return_value=worktree,
                ),
                patch.object(verifier, "git", return_value=cp),
                patch.object(
                    verifier,
                    "run_stage2_gate1_fill_tool",
                    return_value=result,
                ),
                patch.object(verifier, "read_json", return_value=state),
                patch.object(verifier, "validate_control_state"),
                patch.object(verifier, "write_json"),
                patch.object(verifier, "commit_control", return_value="e" * 40),
            ):
                self.assertEqual(
                    verifier.verify_stage2_gate1_fill(MAIN, CONTROL, state),
                    0,
                )

    def test_fresh_verifier_dispatches_gate1_fill_operation(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_GATE1_FILL,
            "request_id": "gate1-fill-001",
        }
        with (
            patch.object(verifier, "configure_git"),
            patch.object(
                verifier,
                "fetch_operational_refs",
                return_value=(MAIN, CONTROL),
            ),
            patch.object(verifier, "git_show_json", return_value=state),
            patch.object(
                verifier,
                "verify_stage2_gate1_fill",
                return_value=0,
            ) as verify,
        ):
            self.assertEqual(verifier.main(), 0)
        verify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
