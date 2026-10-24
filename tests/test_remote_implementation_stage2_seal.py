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
import remote_implementation_stage2_seal as seal  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_GATE1_SEAL,
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
PRESEAL_CHECKPOINT_SHA = "5" * 64
PRESEAL_VERIFICATION_SHA = "6" * 64
PLAN_PREVIEW = "7" * 64
FILLED_REVIEW_SHA = "8" * 64
DECISION_ID_SHA = "9" * 64
OWNER_APPROVAL_SHA = "e" * 64
PRESEAL_EQ_SHA = "f" * 64
SITE_SHA = "0" * 64
SCHOOL = "example-school"
BRANCH = f"data/{SCHOOL}-onboarding"


def sha(data: bytes) -> str:
    import hashlib
    return hashlib.sha256(data).hexdigest()


def request():
    checkpoint_path = (
        ".remote-implementation/checkpoints/example-school/"
        "preseal-001/checkpoint-manifest.json"
    )
    verification_path = (
        ".remote-implementation/verifications/example-school/"
        "preseal-001/stage2-preseal-rehearsal-verification.json"
    )
    return {
        "schema_version": 1,
        "kind": REQUEST_KIND,
        "request_id": "seal-001",
        "school_key": SCHOOL,
        "operation": OP_STAGE2_GATE1_SEAL,
        "previous_control_state_commit": CONTROL,
        "previous_control_state_sha256": "a" * 64,
        "expected_protected_main_sha": MAIN,
        "creation_provenance": {
            "origin": "ChatGPT",
            "authorization": "bounded cryptographic Gate 1 seal",
        },
        "authority": {
            "owner_gate_1": False,
            "owner_gate_2": False,
            "release": False,
            "phase0": False,
            "recovery": False,
            "stage2_census": False,
            "stage2_opponent_display_normalize": False,
            "stage2_proposal_rehearsal": False,
            "stage2_gate1_fill": False,
            "stage2_preseal_rehearsal": False,
            "stage2_gate1_seal": True,
            "stage2_reconciliation_diagnostic": False,
        },
        "target_branch": BRANCH,
        "target_sha": TARGET,
        "stage2_preseal_checkpoint": {
            "path": checkpoint_path,
            "sha256": PRESEAL_CHECKPOINT_SHA,
        },
        "stage2_preseal_verification": {
            "path": verification_path,
            "sha256": PRESEAL_VERIFICATION_SHA,
        },
        "integration_freeze_sha256": FREEZE_SHA,
        "semantic_snapshot_sha256": SEMANTIC_SHA,
        "decision_universe_sha256": DECISION_SHA,
        "recommendation_map_sha256": MAP_SHA,
        "approved_plan_hash_preview": PLAN_PREVIEW,
        "filled_review_sha256": FILLED_REVIEW_SHA,
        "decision_id_set_sha256": DECISION_ID_SHA,
        "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
        "equivalence_sha256": PRESEAL_EQ_SHA,
    }


class RemoteStage2Gate1SealTests(unittest.TestCase):
    def authority_fixture(self):
        req = request()
        preseal_request_bytes = (
            json.dumps({"request_id": "preseal-001"}, sort_keys=True) + "\n"
        ).encode()
        checkpoint_path = req["stage2_preseal_checkpoint"]["path"]
        directory = Path(checkpoint_path).parent
        manifest = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": "preseal-001",
            "request_sha256": sha(preseal_request_bytes),
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "preseal_status": "READY_TO_SEAL",
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "equivalence_sha256": PRESEAL_EQ_SHA,
            "changed_path_count": 12,
            "site_gate_normalized_sha256": SITE_SHA,
        }
        checkpoint_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        verification = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_VERIFICATION",
            "request_id": "preseal-001",
            "school_key": SCHOOL,
            "target_sha": TARGET,
            "preseal_status": "READY_TO_SEAL",
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "equivalence_sha256": PRESEAL_EQ_SHA,
            "tracked_stage2_mutation": "NONE",
            "remote_stage2_preseal_equivalence": "PASS",
        }
        verification_bytes = (
            json.dumps(verification, indent=2, sort_keys=True) + "\n"
        ).encode()
        req["stage2_preseal_checkpoint"]["sha256"] = sha(checkpoint_bytes)
        req["stage2_preseal_verification"]["sha256"] = sha(verification_bytes)
        mapping = {
            checkpoint_path: checkpoint_bytes,
            req["stage2_preseal_verification"]["path"]: verification_bytes,
            (directory / "request.json").as_posix(): preseal_request_bytes,
        }
        return req, manifest, verification, mapping

    def test_control_accepts_read_only_gate1_seal(self):
        req = request()
        validate_request(req)
        state = begin_request(
            initial_control_state(),
            req,
            "b" * 64,
            run_id="100",
            run_attempt="1",
            request_commit="c" * 40,
        )
        self.assertEqual(state["lifecycle_state"], "READ_ONLY_ACTIVE")
        self.assertEqual(state["transaction_state"], "STAGE2_GATE1_SEAL_RUNNING")
        self.assertIsNone(state["active_lock_commit"])

    def test_control_rejects_missing_or_leaked_seal_authority(self):
        req = request()
        req["authority"]["stage2_gate1_seal"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_GATE1_SEAL_REQUEST_AUTHORITY_REQUIRED",
        ):
            validate_request(req)

        req = request()
        req["operation"] = "STAGE2_PRESEAL_REHEARSAL"
        req["authority"]["stage2_gate1_seal"] = True
        req["authority"]["stage2_preseal_rehearsal"] = True
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "REQUEST_GATE1_SEAL_AUTHORITY_FORBIDDEN",
        ):
            validate_request(req)

    def test_ready_fresh_verified_preseal_authenticates(self):
        req, manifest, verification, mapping = self.authority_fixture()
        with (
            patch.object(
                seal,
                "git_show_bytes",
                side_effect=lambda commit, path, **kwargs: mapping[path],
            ),
            patch.object(
                seal,
                "verify_stage2_preseal_authority",
                return_value={
                    "freeze_bytes": b"freeze",
                    "plan_bytes": b"plan",
                    "filled_review_bytes": b"review",
                    "target_tree_sha": TREE,
                    "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
                    "gate1_fill_manifest": {"decision_count": 97},
                },
            ),
        ):
            result = seal.verify_stage2_gate1_seal_authority(req, CONTROL)
        self.assertEqual(result["preseal_manifest"], manifest)
        self.assertEqual(result["preseal_verification"], verification)
        self.assertEqual(result["expected_changed_path_count"], 12)
        self.assertEqual(result["expected_decision_count"], 97)

    def test_unverified_preseal_is_refused(self):
        req, manifest, verification, mapping = self.authority_fixture()
        verification["remote_stage2_preseal_equivalence"] = "PENDING"
        verification_bytes = (
            json.dumps(verification, indent=2, sort_keys=True) + "\n"
        ).encode()
        mapping[req["stage2_preseal_verification"]["path"]] = verification_bytes
        req["stage2_preseal_verification"]["sha256"] = sha(verification_bytes)
        with patch.object(
            seal,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_GATE1_SEAL_PRESEAL_EQUIVALENCE_NOT_PASS",
            ):
                seal.verify_stage2_gate1_seal_authority(req, CONTROL)

    def test_sealed_plan_reconstruction_uses_exact_timestamp(self):
        approved = {
            "school_key": SCHOOL,
            "decisions": [{"decision_id": "D-1"}],
            "approval": {
                "approved_by": seal.APPROVED_BY,
                "approved_at": "2026-10-24T12:34:56+00:00",
            },
            "approved_plan_hash": "a" * 64,
        }
        approved_bytes = (
            json.dumps(approved, indent=2, ensure_ascii=False) + "\n"
        ).encode()
        with (
            patch.object(seal, "verify_approved_plan"),
            patch.object(
                seal,
                "approve_plan",
                return_value=(approved, "a" * 64),
            ) as approve,
            patch.object(seal, "render_report", return_value="sealed review\n"),
        ):
            result = seal.verify_sealed_plan_bytes(
                Path("/tmp/repo"),
                plan_bytes=b"plan",
                filled_review_bytes=b"review",
                approved_plan_bytes=approved_bytes,
            )
        self.assertEqual(result["approved_plan_hash"], "a" * 64)
        self.assertEqual(result["approved_at"], "2026-10-24T12:34:56+00:00")
        self.assertEqual(result["expected_approved_review_bytes"], b"sealed review\n")
        self.assertEqual(
            approve.call_args.kwargs["approved_at"],
            "2026-10-24T12:34:56+00:00",
        )

    def test_sealed_plan_rejects_wrong_approved_by(self):
        approved = {
            "school_key": SCHOOL,
            "decisions": [],
            "approval": {
                "approved_by": "someone-else",
                "approved_at": "2026-10-24T12:34:56+00:00",
            },
            "approved_plan_hash": "a" * 64,
        }
        approved_bytes = (
            json.dumps(approved, indent=2, ensure_ascii=False) + "\n"
        ).encode()
        with self.assertRaisesRegex(
            Stop,
            "STAGE2_GATE1_SEAL_APPROVED_BY_MISMATCH",
        ):
            seal.verify_sealed_plan_bytes(
                Path("/tmp/repo"),
                plan_bytes=b"plan",
                filled_review_bytes=b"review",
                approved_plan_bytes=approved_bytes,
            )

    def test_permanent_seal_writes_only_ignored_authority(self):
        approved_bytes = b'{"approved_plan_hash":"' + b"a" * 64 + b'"}\n'
        review_bytes = b"approved review\n"
        clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def fake_run(command, **kwargs):
                output = Path(command[command.index("--output-dir") + 1])
                output.mkdir(parents=True, exist_ok=True)
                (output / seal.APPROVED_PLAN_NAME).write_bytes(approved_bytes)
                (output / seal.APPROVED_REVIEW_NAME).write_bytes(review_bytes)
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout=(
                        "OWNER GATE 1 SEALED\n"
                        f"Approved plan: {'a' * 64}\n"
                    ),
                )

            with (
                patch.object(seal, "restore_integration_freeze"),
                patch.object(
                    seal,
                    "tracked_worktree_state",
                    side_effect=[clean, clean],
                ),
                patch.object(seal, "run", side_effect=fake_run),
                patch.object(
                    seal,
                    "verify_sealed_plan_bytes",
                    return_value={
                        "approved_plan_hash": "a" * 64,
                        "approved_plan_sha256": sha(approved_bytes),
                        "expected_approved_review_bytes": review_bytes,
                        "expected_approved_review_sha256": sha(review_bytes),
                        "approved_by": seal.APPROVED_BY,
                        "approved_at": "2026-10-24T12:34:56+00:00",
                        "decision_count": 97,
                    },
                ),
            ):
                result = seal.run_stage2_gate1_seal_tool(
                    root,
                    SCHOOL,
                    freeze_bytes=b"freeze",
                    plan_bytes=b"plan",
                    filled_review_bytes=b"review",
                    diag=root / "diag",
                    tool_repo=ROOT,
                )

        self.assertEqual(result["approved_plan_hash"], "a" * 64)
        self.assertEqual(result["decision_count"], 97)
        self.assertEqual(
            result["tracked_mutation_proof"]["tracked_stage2_mutation"],
            "NONE",
        )

    def test_permanent_seal_refuses_tracked_mutation(self):
        clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
        dirty = {
            "head_sha": TARGET,
            "tree_sha": TREE,
            "status": " M data/canonical/games.csv\n",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with (
                patch.object(seal, "restore_integration_freeze"),
                patch.object(
                    seal,
                    "tracked_worktree_state",
                    side_effect=[clean, dirty],
                ),
                patch.object(
                    seal,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, stdout=""),
                ),
            ):
                with self.assertRaisesRegex(
                    Stop,
                    "STAGE2_GATE1_SEAL_TRACKED_MUTATION_DETECTED",
                ):
                    seal.run_stage2_gate1_seal_tool(
                        root,
                        SCHOOL,
                        freeze_bytes=b"freeze",
                        plan_bytes=b"plan",
                        filled_review_bytes=b"review",
                        diag=root / "diag",
                        tool_repo=ROOT,
                    )

    def test_runner_replays_current_main_preseal_before_sealing(self):
        req = request()
        authority = {
            "target_tree_sha": TREE,
            "freeze_bytes": b"freeze",
            "plan_bytes": b"plan",
            "filled_review_bytes": b"review",
            "expected_changed_path_count": 12,
            "expected_site_gate_normalized_sha256": SITE_SHA,
            "expected_decision_count": 97,
        }
        preseal_result = {
            "preseal_status": "READY_TO_SEAL",
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "changed_path_count": 12,
            "site_gate_normalized_sha256": SITE_SHA,
            "equivalence_sha256": PRESEAL_EQ_SHA,
            "runtime_tool_sha256": {},
            "tracked_mutation_proof": {"tracked_stage2_mutation": "NONE"},
        }
        seal_result = {
            "approved_plan_hash": "a" * 64,
            "decision_count": 97,
            "tracked_mutation_proof": {"after_tree_sha": TREE},
        }
        cp = subprocess.CompletedProcess([], 0, stdout=TREE + "\n")
        with tempfile.TemporaryDirectory() as directory:
            worktree = Path(directory)
            with (
                patch.object(
                    runner,
                    "verify_stage2_gate1_seal_authority",
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
                    "run_stage2_preseal_rehearsal_tool",
                    return_value=preseal_result,
                ) as preseal_run,
                patch.object(
                    runner,
                    "run_stage2_gate1_seal_tool",
                    return_value=seal_result,
                ) as seal_run,
                patch.object(runner, "assert_protected_main_unchanged"),
                patch.object(
                    runner,
                    "persist_stage2_gate1_seal_checkpoint",
                    return_value="2" * 40,
                ) as persist,
            ):
                runner.run_read_only_stage2_gate1_seal(
                    initial_control_state(),
                    req,
                    b"{}",
                    "e" * 40,
                    CONTROL,
                    MAIN,
                )
        preseal_run.assert_called_once()
        seal_run.assert_called_once()
        persist.assert_called_once()

    def test_fresh_verifier_reconstructs_exact_seal(self):
        request_bytes = b'{"request_id":"seal-001"}\n'
        approved_plan_bytes = b'{"sealed":true}\n'
        approved_review_bytes = b"sealed review\n"
        checkpoint_path = (
            ".remote-implementation/checkpoints/example-school/"
            "seal-001/checkpoint-manifest.json"
        )
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT",
            "request_id": "seal-001",
            "request_sha256": sha(request_bytes),
            "school_key": SCHOOL,
            "protected_main_sha": MAIN,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "source_preseal_request_id": "preseal-001",
            "stage2_preseal_checkpoint_sha256": PRESEAL_CHECKPOINT_SHA,
            "stage2_preseal_verification_sha256": PRESEAL_VERIFICATION_SHA,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "source_preseal_equivalence_sha256": PRESEAL_EQ_SHA,
            "current_main_preseal_approved_plan_hash_preview": PLAN_PREVIEW,
            "current_main_preseal_changed_path_count": 12,
            "current_main_preseal_site_gate_normalized_sha256": SITE_SHA,
            "current_main_preseal_equivalence_sha256": PRESEAL_EQ_SHA,
            "current_main_preseal_runtime_tool_sha256": {"x": "y"},
            "seal_runtime_tool_sha256": {
                "tools/onboard_school.py": "onboard",
                "tools/onboarding_plan.py": "plan",
            },
            "approved_plan_hash": "a" * 64,
            "approved_plan_checkpoint_path": (
                ".remote-implementation/checkpoints/example-school/"
                "seal-001/approved-plan.json"
            ),
            "approved_plan_sha256": sha(approved_plan_bytes),
            "approved_review_checkpoint_path": (
                ".remote-implementation/checkpoints/example-school/"
                "seal-001/approved-review.md"
            ),
            "approved_review_sha256": sha(approved_review_bytes),
            "approved_by": seal.APPROVED_BY,
            "approved_at": "2026-10-24T12:34:56+00:00",
            "decision_count": 97,
            "seal_status": "SEALED",
        }
        manifest_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_GATE1_SEAL,
            "request_id": "seal-001",
            "checkpoint_manifest_path": checkpoint_path,
            "checkpoint_manifest_sha256": sha(manifest_bytes),
            "target_sha": TARGET,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "source_preseal_equivalence_sha256": PRESEAL_EQ_SHA,
            "current_main_preseal_equivalence_sha256": PRESEAL_EQ_SHA,
            "approved_plan_hash": "a" * 64,
            "approved_plan_sha256": sha(approved_plan_bytes),
            "approved_by": seal.APPROVED_BY,
            "approved_at": "2026-10-24T12:34:56+00:00",
            "seal_status": "SEALED",
            "fresh_runner_verification": "PENDING",
        }
        mapping = {
            checkpoint_path: manifest_bytes,
            (Path(checkpoint_path).parent / "request.json").as_posix(): request_bytes,
            manifest["approved_plan_checkpoint_path"]: approved_plan_bytes,
            manifest["approved_review_checkpoint_path"]: approved_review_bytes,
        }
        preseal_result = {
            "preseal_status": "READY_TO_SEAL",
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "changed_path_count": 12,
            "site_gate_normalized_sha256": SITE_SHA,
            "equivalence_sha256": PRESEAL_EQ_SHA,
            "runtime_tool_sha256": {"x": "y"},
            "tracked_mutation_proof": {"tracked_stage2_mutation": "NONE"},
        }
        seal_summary = {
            "approved_plan_hash": "a" * 64,
            "approved_plan_sha256": sha(approved_plan_bytes),
            "expected_approved_review_bytes": approved_review_bytes,
            "expected_approved_review_sha256": sha(approved_review_bytes),
            "approved_by": seal.APPROVED_BY,
            "approved_at": "2026-10-24T12:34:56+00:00",
            "decision_count": 97,
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
                    "verify_stage2_gate1_seal_authority",
                    return_value={
                        "target_tree_sha": TREE,
                        "freeze_bytes": b"freeze",
                        "plan_bytes": b"plan",
                        "filled_review_bytes": b"review",
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
                    "run_stage2_preseal_rehearsal_tool",
                    return_value=preseal_result,
                ),
                patch.object(
                    verifier,
                    "sha256_file",
                    side_effect=lambda path: (
                        "onboard"
                        if str(path).endswith("onboard_school.py")
                        else "plan"
                    ),
                ),
                patch.object(
                    verifier,
                    "verify_sealed_plan_bytes",
                    return_value=seal_summary,
                ),
                patch.object(verifier, "read_json", return_value=state),
                patch.object(verifier, "validate_control_state"),
                patch.object(verifier, "write_json"),
                patch.object(verifier, "commit_control", return_value="e" * 40),
            ):
                self.assertEqual(
                    verifier.verify_stage2_gate1_seal(MAIN, CONTROL, state),
                    0,
                )

    def test_fresh_verifier_dispatches_gate1_seal(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_GATE1_SEAL,
            "request_id": "seal-001",
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
                "verify_stage2_gate1_seal",
                return_value=0,
            ) as verify,
        ):
            self.assertEqual(verifier.main(), 0)
        verify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
