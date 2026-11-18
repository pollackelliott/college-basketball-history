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
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import remote_implementation_runner as runner  # noqa: E402
import remote_implementation_stage2_preseal as preseal  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402
import stage2_candidate_runtime_rehearsal as candidate_rehearsal  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_PRESEAL_REHEARSAL,
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
FILL_CHECKPOINT_SHA = "5" * 64
FILL_VERIFICATION_SHA = "6" * 64
PLAN_PREVIEW = "7" * 64
FILLED_REVIEW_SHA = "8" * 64
DECISION_ID_SHA = "9" * 64
OWNER_APPROVAL_SHA = "e" * 64
SCHOOL = "example-school"
BRANCH = f"data/{SCHOOL}-onboarding"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def request():
    checkpoint_path = (
        ".remote-implementation/checkpoints/example-school/"
        "gate1-fill-001/checkpoint-manifest.json"
    )
    verification_path = (
        ".remote-implementation/verifications/example-school/"
        "gate1-fill-001/stage2-gate1-fill-verification.json"
    )
    return {
        "schema_version": 1,
        "kind": REQUEST_KIND,
        "request_id": "preseal-001",
        "school_key": SCHOOL,
        "operation": OP_STAGE2_PRESEAL_REHEARSAL,
        "previous_control_state_commit": CONTROL,
        "previous_control_state_sha256": "f" * 64,
        "expected_protected_main_sha": MAIN,
        "creation_provenance": {
            "origin": "ChatGPT",
            "authorization": "bounded owner-authorized pre-seal rehearsal",
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
            "stage2_preseal_rehearsal": True,
            "stage2_reconciliation_diagnostic": False,
        },
        "target_branch": BRANCH,
        "target_sha": TARGET,
        "stage2_gate1_fill_checkpoint": {
            "path": checkpoint_path,
            "sha256": FILL_CHECKPOINT_SHA,
        },
        "stage2_gate1_fill_verification": {
            "path": verification_path,
            "sha256": FILL_VERIFICATION_SHA,
        },
        "integration_freeze_sha256": FREEZE_SHA,
        "semantic_snapshot_sha256": SEMANTIC_SHA,
        "decision_universe_sha256": DECISION_SHA,
        "recommendation_map_sha256": MAP_SHA,
        "approved_plan_hash_preview": PLAN_PREVIEW,
        "filled_review_sha256": FILLED_REVIEW_SHA,
        "decision_id_set_sha256": DECISION_ID_SHA,
    }


class RemoteStage2PresealTests(unittest.TestCase):
    def authority_fixture(self):
        req = request()
        fill_request_bytes = (
            json.dumps({"request_id": "gate1-fill-001"}, sort_keys=True) + "\n"
        ).encode()
        plan_bytes = b'{"decisions":[]}\n'
        review_bytes = (
            b"decision_id,category,decision,resolution_basis\n"
            b"D-1,publication,ENABLE_PUBLIC_PAGE,Owner approved\n"
        )
        checkpoint_path = req["stage2_gate1_fill_checkpoint"]["path"]
        directory = Path(checkpoint_path).parent
        plan_path = (directory / "plan.json").as_posix()
        review_path = (directory / "filled-review.csv").as_posix()
        manifest = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_CHECKPOINT",
            "request_id": "gate1-fill-001",
            "request_sha256": sha(fill_request_bytes),
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "gate1_fill_status": "FILLED",
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "filled_review_checkpoint_path": review_path,
            "filled_review_sha256": sha(review_bytes),
            "plan_checkpoint_path": plan_path,
            "plan_sha256": sha(plan_bytes),
            "decision_id_set_sha256": DECISION_ID_SHA,
        }
        checkpoint_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        verification = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_FILL_VERIFICATION",
            "request_id": "gate1-fill-001",
            "school_key": SCHOOL,
            "target_sha": TARGET,
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": sha(review_bytes),
            "decision_id_set_sha256": DECISION_ID_SHA,
            "tracked_stage2_mutation": "NONE",
            "remote_stage2_gate1_fill_equivalence": "PASS",
        }
        verification_bytes = (
            json.dumps(verification, indent=2, sort_keys=True) + "\n"
        ).encode()
        req["stage2_gate1_fill_checkpoint"]["sha256"] = sha(checkpoint_bytes)
        req["stage2_gate1_fill_verification"]["sha256"] = sha(
            verification_bytes
        )
        req["filled_review_sha256"] = sha(review_bytes)
        mapping = {
            checkpoint_path: checkpoint_bytes,
            req["stage2_gate1_fill_verification"]["path"]: verification_bytes,
            (directory / "request.json").as_posix(): fill_request_bytes,
            plan_path: plan_bytes,
            review_path: review_bytes,
        }
        return req, manifest, verification, mapping

    def test_control_accepts_read_only_preseal_request(self):
        req = request()
        validate_request(req)
        state = begin_request(
            initial_control_state(),
            req,
            "a" * 64,
            run_id="100",
            run_attempt="1",
            request_commit="b" * 40,
        )
        self.assertEqual(state["lifecycle_state"], "READ_ONLY_ACTIVE")
        self.assertEqual(
            state["transaction_state"],
            "STAGE2_PRESEAL_REHEARSAL_RUNNING",
        )
        self.assertIsNone(state["active_lock_commit"])

    def test_control_rejects_missing_or_leaked_preseal_authority(self):
        req = request()
        req["authority"]["stage2_preseal_rehearsal"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_PRESEAL_REQUEST_AUTHORITY_REQUIRED",
        ):
            validate_request(req)

        req = request()
        req["operation"] = "STAGE2_GATE1_FILL"
        req["authority"]["stage2_preseal_rehearsal"] = True
        req["authority"]["owner_gate_1"] = True
        req["authority"]["stage2_gate1_fill"] = True
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "REQUEST_PRESEAL_AUTHORITY_FORBIDDEN",
        ):
            validate_request(req)

    def test_exact_fill_checkpoint_and_verification_authenticate(self):
        req, manifest, verification, mapping = self.authority_fixture()

        with (
            patch.object(
                preseal,
                "git_show_bytes",
                side_effect=lambda commit, path, **kwargs: mapping[path],
            ),
            patch.object(
                preseal,
                "verify_stage2_gate1_fill_authority",
                return_value={
                    "freeze_bytes": b"freeze",
                    "venue_reconciliation_bytes": b"venue-sidecar",
                },
            ),
        ):
            result = preseal.verify_stage2_preseal_authority(req, CONTROL)

        self.assertEqual(
            result["venue_reconciliation_bytes"],
            b"venue-sidecar",
        )
        self.assertEqual(result["gate1_fill_manifest"], manifest)
        self.assertEqual(result["gate1_fill_verification"], verification)
        self.assertEqual(result["target_tree_sha"], TREE)
        self.assertEqual(result["freeze_bytes"], b"freeze")
        self.assertEqual(result["owner_gate_1_approval_sha256"], OWNER_APPROVAL_SHA)

    def test_unverified_fill_is_refused(self):
        req, manifest, verification, mapping = self.authority_fixture()
        verification["remote_stage2_gate1_fill_equivalence"] = "PENDING"
        verification_bytes = (
            json.dumps(verification, indent=2, sort_keys=True) + "\n"
        ).encode()
        mapping[req["stage2_gate1_fill_verification"]["path"]] = (
            verification_bytes
        )
        req["stage2_gate1_fill_verification"]["sha256"] = sha(
            verification_bytes
        )
        with patch.object(
            preseal,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_PRESEAL_GATE1_FILL_EQUIVALENCE_NOT_PASS",
            ):
                preseal.verify_stage2_preseal_authority(req, CONTROL)

    def test_log_normalization_removes_temp_roots_and_test_timing(self):
        repo = Path("/work/target")
        first = (
            "Repository: /work/target\n"
            "/tmp/tmps6yu3v7v/schools/alpha/source-games.csv\n"
            "/tmp/display-recovery-test-c4ppztya/schools/example/opponents.csv\n"
            "/tmp/onboard-example-zydzz45i/repository\n"
            "Ran 865 tests in 65.220s\n"
        )
        second = (
            "Repository: /work/target\n"
            "/tmp/tmp8a1bcdef/schools/alpha/source-games.csv\n"
            "/tmp/display-recovery-test-z9y8x7w6/schools/example/opponents.csv\n"
            "/tmp/onboard-example-a1b2c3d4/repository\n"
            "Ran 865 tests in 60.033s\n"
        )
        self.assertEqual(
            preseal._normalize_text(first, repo=repo),
            preseal._normalize_text(second, repo=repo),
        )
        normalized = preseal._normalize_text(first, repo=repo)
        self.assertIn("<TARGET_REPO>", normalized)
        self.assertIn("<TMPDIR>/schools/alpha/source-games.csv", normalized)
        self.assertIn("Ran 865 tests in <ELAPSED>s", normalized)

    def test_expansion_venue_reconciliation_is_restored_exactly(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            sidecar_bytes = b'{"schema_version":1}\n'
            freeze_bytes = (
                json.dumps(
                    {
                        "kind": "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
                        "venue_reconciliation": {"spec_sha256": sha(sidecar_bytes)},
                        "venue_reconciliation_sha256": sha(sidecar_bytes),
                    }
                )
                + "\n"
            ).encode()
            restored = preseal.restore_expansion_venue_reconciliation(
                root,
                SCHOOL,
                freeze_bytes,
                sidecar_bytes,
            )
            self.assertIsNotNone(restored)
            self.assertEqual(restored.read_bytes(), sidecar_bytes)

            with self.assertRaisesRegex(
                Stop,
                "STAGE2_GATE1_VENUE_RECONCILIATION_BYTES_MISMATCH",
            ):
                preseal.restore_expansion_venue_reconciliation(
                    root,
                    SCHOOL,
                    freeze_bytes,
                    b"wrong",
                )

    def test_permanent_rehearsal_restores_bound_venue_reconciliation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            sidecar_bytes = b'{"schema_version":1}\n'
            freeze_bytes = (
                json.dumps(
                    {
                        "kind": "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
                        "venue_reconciliation": {"spec_sha256": sha(sidecar_bytes)},
                        "venue_reconciliation_sha256": sha(sidecar_bytes),
                    }
                )
                + "\n"
            ).encode()
            log = (
                "TECHNICAL READINESS PASSED\n"
                f"Preview approved-plan hash: {PLAN_PREVIEW}\n"
                "Changed paths: 12\n"
            )
            with (
                patch.object(
                    preseal,
                    "tracked_worktree_state",
                    side_effect=[clean, clean],
                ),
                patch.object(
                    preseal,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, stdout=log),
                ),
            ):
                result = preseal.run_stage2_preseal_rehearsal_tool(
                    root,
                    SCHOOL,
                    freeze_bytes=freeze_bytes,
                    plan_bytes=b"{}\n",
                    filled_review_bytes=b"decision_id\n",
                    venue_reconciliation_bytes=sidecar_bytes,
                    expected_approved_plan_hash_preview=PLAN_PREVIEW,
                    diag=root / "diag",
                    tool_repo=ROOT,
                )

            restored = (
                root / ".onboarding" / SCHOOL / "venue-reconciliation.json"
            )
            self.assertEqual(restored.read_bytes(), sidecar_bytes)
            self.assertEqual(result["preseal_status"], "READY_TO_SEAL")

    def test_permanent_rehearsal_success_is_ready_to_seal(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            log = (
                "Rehearsing filled review in /tmp/preseal-example-abc/repository\n"
                "TECHNICAL READINESS PASSED\n"
                f"Preview approved-plan hash: {PLAN_PREVIEW}\n"
                "Changed paths: 12\n"
            )
            with (
                patch.object(preseal, "restore_integration_freeze"),
                patch.object(
                    preseal,
                    "tracked_worktree_state",
                    side_effect=[clean, clean],
                ),
                patch.object(
                    preseal,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, stdout=log),
                ),
            ):
                result = preseal.run_stage2_preseal_rehearsal_tool(
                    root,
                    SCHOOL,
                    freeze_bytes=b"freeze",
                    plan_bytes=b"{}\n",
                    filled_review_bytes=b"decision_id\n",
                    expected_approved_plan_hash_preview=PLAN_PREVIEW,
                    diag=root / "diag",
                    tool_repo=ROOT,
                )

            self.assertEqual(result["preseal_status"], "READY_TO_SEAL")
            self.assertEqual(result["approved_plan_hash_preview"], PLAN_PREVIEW)
            self.assertEqual(result["changed_path_count"], 12)
            self.assertRegex(result["raw_log_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(result["normalized_log_sha256"], r"^[0-9a-f]{64}$")
            self.assertRegex(result["equivalence_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(
                result["tracked_mutation_proof"]["tracked_stage2_mutation"],
                "NONE",
            )

    def test_permanent_rehearsal_binds_runtime_validator_only_for_subprocess(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            log = (
                "TECHNICAL READINESS PASSED\n"
                f"Preview approved-plan hash: {PLAN_PREVIEW}\n"
                "Changed paths: 12\n"
            )
            observed = {}

            def fake_run(*args, **kwargs):
                observed["override"] = os.environ.get(
                    "CBB_VALIDATE_DATA_TOOL_OVERRIDE"
                )
                return subprocess.CompletedProcess([], 0, stdout=log)

            with (
                patch.dict(
                    os.environ,
                    {"CBB_VALIDATE_DATA_TOOL_OVERRIDE": "prior-validator"},
                ),
                patch.object(preseal, "restore_integration_freeze"),
                patch.object(
                    preseal,
                    "tracked_worktree_state",
                    side_effect=[clean, clean],
                ),
                patch.object(preseal, "run", side_effect=fake_run),
            ):
                result = preseal.run_stage2_preseal_rehearsal_tool(
                    root,
                    SCHOOL,
                    freeze_bytes=b"freeze",
                    plan_bytes=b"{}\n",
                    filled_review_bytes=b"decision_id\n",
                    expected_approved_plan_hash_preview=PLAN_PREVIEW,
                    diag=root / "diag",
                    tool_repo=ROOT,
                )
                self.assertEqual(
                    os.environ["CBB_VALIDATE_DATA_TOOL_OVERRIDE"],
                    "prior-validator",
                )

            self.assertEqual(result["preseal_status"], "READY_TO_SEAL")
            self.assertEqual(
                observed["override"],
                str(ROOT / "tools/validate_data.py"),
            )

    def test_permanent_rehearsal_failure_is_durable_blocked_result(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            with (
                patch.object(preseal, "restore_integration_freeze"),
                patch.object(
                    preseal,
                    "tracked_worktree_state",
                    side_effect=[clean, clean],
                ),
                patch.object(
                    preseal,
                    "run",
                    return_value=subprocess.CompletedProcess(
                        [], 1, stdout="FAIL: site gate failed\n"
                    ),
                ),
            ):
                result = preseal.run_stage2_preseal_rehearsal_tool(
                    root,
                    SCHOOL,
                    freeze_bytes=b"freeze",
                    plan_bytes=b"{}\n",
                    filled_review_bytes=b"decision_id\n",
                    expected_approved_plan_hash_preview=PLAN_PREVIEW,
                    diag=root / "diag",
                    tool_repo=ROOT,
                )

            self.assertEqual(result["preseal_status"], "BLOCKED")
            self.assertEqual(result["exit_code"], 1)
            self.assertIsNone(result["changed_path_count"])

    def test_permanent_rehearsal_refuses_tracked_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            dirty = {
                "head_sha": TARGET,
                "tree_sha": TREE,
                "status": " M data/canonical/games.csv\n",
            }
            with (
                patch.object(preseal, "restore_integration_freeze"),
                patch.object(
                    preseal,
                    "tracked_worktree_state",
                    side_effect=[clean, dirty],
                ),
                patch.object(
                    preseal,
                    "run",
                    return_value=subprocess.CompletedProcess(
                        [], 0, stdout=""
                    ),
                ),
            ):
                with self.assertRaisesRegex(
                    Stop,
                    "STAGE2_PRESEAL_TRACKED_MUTATION_DETECTED",
                ):
                    preseal.run_stage2_preseal_rehearsal_tool(
                        root,
                        SCHOOL,
                        freeze_bytes=b"freeze",
                        plan_bytes=b"{}\n",
                        filled_review_bytes=b"decision_id\n",
                        expected_approved_plan_hash_preview=PLAN_PREVIEW,
                        diag=root / "diag",
                        tool_repo=ROOT,
                    )

    def test_runner_refuses_changed_target_before_acceptance(self):
        req = request()
        with (
            patch.object(
                runner,
                "verify_stage2_preseal_authority",
                return_value={"target_tree_sha": TREE},
            ),
            patch.object(runner, "remote_head", return_value="f" * 40),
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_PRESEAL_TARGET_HEAD_MISMATCH",
            ):
                runner.run_read_only_stage2_preseal_rehearsal(
                    initial_control_state(),
                    req,
                    b"{}",
                    "e" * 40,
                    CONTROL,
                    MAIN,
                )

    def test_fresh_verifier_replays_same_preseal_result(self):
        request_bytes = b'{"request_id":"preseal-001"}\n'
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": "preseal-001",
            "request_sha256": sha(request_bytes),
            "school_key": SCHOOL,
            "protected_main_sha": MAIN,
            "runtime_tool_sha256": {
                "tools/onboarding_hardening.py": "x",
                "tools/onboard_school.py": "y",
            },
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "stage2_gate1_fill_checkpoint_sha256": FILL_CHECKPOINT_SHA,
            "stage2_gate1_fill_verification_sha256": FILL_VERIFICATION_SHA,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "preseal_status": "READY_TO_SEAL",
            "command_exit_code": 0,
            "rehearsal_approved_plan_hash_preview": PLAN_PREVIEW,
            "changed_path_count": 12,
            "normalized_log_sha256": "a" * 64,
            "site_gate_normalized_sha256": "b" * 64,
            "tracked_mutation_proof": {
                "tracked_stage2_mutation": "NONE",
            },
        }
        manifest_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        checkpoint_path = (
            ".remote-implementation/checkpoints/example-school/"
            "preseal-001/checkpoint-manifest.json"
        )
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_PRESEAL_REHEARSAL,
            "request_id": "preseal-001",
            "checkpoint_manifest_path": checkpoint_path,
            "checkpoint_manifest_sha256": sha(manifest_bytes),
            "target_sha": TARGET,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "preseal_status": "READY_TO_SEAL",
            "changed_path_count": 12,
            "normalized_log_sha256": "a" * 64,
            "site_gate_normalized_sha256": "b" * 64,
            "fresh_runner_verification": "PENDING",
        }
        mapping = {
            checkpoint_path: manifest_bytes,
            (Path(checkpoint_path).parent / "request.json").as_posix(): (
                request_bytes
            ),
        }
        expected_equivalence = preseal.preseal_equivalence_sha256(
            preseal_status="READY_TO_SEAL",
            exit_code=0,
            approved_plan_hash_preview=PLAN_PREVIEW,
            changed_path_count=12,
            site_gate_normalized_sha256="b" * 64,
            runtime_tool_sha256=manifest["runtime_tool_sha256"],
            target_tree_sha=TREE,
            tracked_stage2_mutation="NONE",
        )
        result = {
            "runtime_tool_sha256": manifest["runtime_tool_sha256"],
            "preseal_status": "READY_TO_SEAL",
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "changed_path_count": 12,
            "raw_log_sha256": "c" * 64,
            # Deliberately different from the durable checkpoint. Diagnostic
            # log hash inequality must not block semantic fresh equivalence.
            "normalized_log_sha256": "d" * 64,
            "equivalence_sha256": expected_equivalence,
            "site_gate_normalized_sha256": "b" * 64,
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
                    "verify_stage2_preseal_authority",
                    return_value={
                        "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
                        "freeze_bytes": b"freeze",
                        "plan_bytes": b"plan",
                        "filled_review_bytes": b"review",
                        "target_tree_sha": TREE,
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
                    return_value=result,
                ),
                patch.object(verifier, "read_json", return_value=state),
                patch.object(verifier, "validate_control_state"),
                patch.object(verifier, "write_json"),
                patch.object(verifier, "commit_control", return_value="e" * 40),
            ):
                self.assertEqual(
                    verifier.verify_stage2_preseal_rehearsal(
                        MAIN, CONTROL, state
                    ),
                    0,
                )

    def test_structured_equivalence_hash_changes_on_stable_result_drift(self):
        baseline = preseal.preseal_equivalence_sha256(
            preseal_status="READY_TO_SEAL",
            exit_code=0,
            approved_plan_hash_preview=PLAN_PREVIEW,
            changed_path_count=87,
            site_gate_normalized_sha256="b" * 64,
            runtime_tool_sha256={
                "tools/onboarding_hardening.py": "x",
                "tools/onboard_school.py": "y",
            },
            target_tree_sha=TREE,
            tracked_stage2_mutation="NONE",
        )
        changed = preseal.preseal_equivalence_sha256(
            preseal_status="READY_TO_SEAL",
            exit_code=0,
            approved_plan_hash_preview=PLAN_PREVIEW,
            changed_path_count=88,
            site_gate_normalized_sha256="b" * 64,
            runtime_tool_sha256={
                "tools/onboarding_hardening.py": "x",
                "tools/onboard_school.py": "y",
            },
            target_tree_sha=TREE,
            tracked_stage2_mutation="NONE",
        )
        self.assertNotEqual(baseline, changed)


    def test_candidate_preseal_replays_exact_blocked_authority_with_sidecar(self):
        req = request()
        req["request_id"] = "preseal-001"
        request_bytes = (json.dumps(req, sort_keys=True) + "\n").encode()
        checkpoint_path = (
            ".remote-implementation/checkpoints/example-school/"
            "preseal-001/checkpoint-manifest.json"
        )
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": "preseal-001",
            "request_sha256": sha(request_bytes),
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "integration_freeze_sha256": FREEZE_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "preseal_status": "BLOCKED",
            "tracked_mutation_proof": {"tracked_stage2_mutation": "NONE"},
        }
        authority = {
            "freeze_bytes": b"freeze",
            "plan_bytes": b"plan",
            "filled_review_bytes": b"review",
            "venue_reconciliation_bytes": b"venue-sidecar",
            "target_tree_sha": TREE,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
        }
        result = {
            "preseal_status": "READY_TO_SEAL",
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "tracked_mutation_proof": {"tracked_stage2_mutation": "NONE"},
        }
        cp_head = subprocess.CompletedProcess([], 0, stdout=("f" * 40) + "\n")
        cp_tree = subprocess.CompletedProcess([], 0, stdout=TREE + "\n")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            diag = target / "diag"
            with (
                patch.object(
                    candidate_rehearsal,
                    "_run_git",
                    side_effect=[cp_head, cp_tree],
                ),
                patch.object(
                    candidate_rehearsal,
                    "_load_json_at",
                    side_effect=[(manifest, b"manifest"), (req, request_bytes)],
                ),
                patch.object(
                    candidate_rehearsal,
                    "candidate_changed_paths",
                    return_value=(
                        ["tools/remote_implementation_stage2_preseal.py"],
                        MAIN,
                    ),
                ),
                patch.object(candidate_rehearsal, "validate_candidate_scope"),
                patch.object(
                    candidate_rehearsal,
                    "verify_stage2_preseal_authority",
                    return_value=authority,
                ),
                patch.object(
                    candidate_rehearsal,
                    "add_existing_onboarding_worktree",
                    return_value=target,
                ),
                patch.object(
                    candidate_rehearsal,
                    "run_stage2_preseal_rehearsal_tool",
                    return_value=result,
                ) as replay,
            ):
                summary = candidate_rehearsal.run_candidate_preseal_rehearsal(
                    source_repo=ROOT,
                    candidate_runtime=ROOT,
                    candidate_sha="f" * 40,
                    control_commit=CONTROL,
                    preseal_checkpoint_path=checkpoint_path,
                    diag=diag,
                )

        self.assertEqual(
            summary["classification"],
            "RESOLVED_TO_READY_TO_SEAL",
        )
        self.assertEqual(summary["decision_universe_sha256"], DECISION_SHA)
        self.assertEqual(summary["recommendation_map_sha256"], MAP_SHA)
        self.assertEqual(
            summary["owner_gate_1_approval_sha256"],
            OWNER_APPROVAL_SHA,
        )
        self.assertEqual(
            replay.call_args.kwargs["venue_reconciliation_bytes"],
            b"venue-sidecar",
        )

    def test_candidate_preseal_fails_closed_when_candidate_remains_blocked(self):
        req = request()
        req["request_id"] = "preseal-001"
        request_bytes = (json.dumps(req, sort_keys=True) + "\n").encode()
        checkpoint_path = (
            ".remote-implementation/checkpoints/example-school/"
            "preseal-001/checkpoint-manifest.json"
        )
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PRESEAL_REHEARSAL_CHECKPOINT",
            "request_id": "preseal-001",
            "request_sha256": sha(request_bytes),
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "approved_plan_hash_preview": PLAN_PREVIEW,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "preseal_status": "BLOCKED",
            "tracked_mutation_proof": {"tracked_stage2_mutation": "NONE"},
        }
        authority = {
            "freeze_bytes": b"freeze",
            "plan_bytes": b"plan",
            "filled_review_bytes": b"review",
            "venue_reconciliation_bytes": b"venue-sidecar",
            "target_tree_sha": TREE,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
        }
        cp_head = subprocess.CompletedProcess([], 0, stdout=("f" * 40) + "\n")
        cp_tree = subprocess.CompletedProcess([], 0, stdout=TREE + "\n")
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory)
            with (
                patch.object(
                    candidate_rehearsal,
                    "_run_git",
                    side_effect=[cp_head, cp_tree],
                ),
                patch.object(
                    candidate_rehearsal,
                    "_load_json_at",
                    side_effect=[(manifest, b"manifest"), (req, request_bytes)],
                ),
                patch.object(
                    candidate_rehearsal,
                    "candidate_changed_paths",
                    return_value=(["tools/example.py"], MAIN),
                ),
                patch.object(candidate_rehearsal, "validate_candidate_scope"),
                patch.object(
                    candidate_rehearsal,
                    "verify_stage2_preseal_authority",
                    return_value=authority,
                ),
                patch.object(
                    candidate_rehearsal,
                    "add_existing_onboarding_worktree",
                    return_value=target,
                ),
                patch.object(
                    candidate_rehearsal,
                    "run_stage2_preseal_rehearsal_tool",
                    return_value={
                        "preseal_status": "BLOCKED",
                        "tracked_mutation_proof": {
                            "tracked_stage2_mutation": "NONE"
                        },
                    },
                ),
            ):
                with self.assertRaisesRegex(
                    Stop,
                    "CANDIDATE_PRESEAL_NOT_READY:BLOCKED",
                ):
                    candidate_rehearsal.run_candidate_preseal_rehearsal(
                        source_repo=ROOT,
                        candidate_runtime=ROOT,
                        candidate_sha="f" * 40,
                        control_commit=CONTROL,
                        preseal_checkpoint_path=checkpoint_path,
                        diag=target / "diag",
                    )

    def test_fresh_verifier_dispatches_preseal_operation(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_PRESEAL_REHEARSAL,
            "request_id": "preseal-001",
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
                "verify_stage2_preseal_rehearsal",
                return_value=0,
            ) as verify,
        ):
            self.assertEqual(verifier.main(), 0)
        verify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
