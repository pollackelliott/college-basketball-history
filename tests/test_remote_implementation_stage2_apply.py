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
import remote_implementation_stage2_apply as applymod  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_SEALED_APPLY,
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
SEAL_CHECKPOINT_SHA = "5" * 64
SEAL_VERIFICATION_SHA = "6" * 64
FILLED_REVIEW_SHA = "7" * 64
DECISION_ID_SHA = "8" * 64
OWNER_APPROVAL_SHA = "9" * 64
APPROVED_HASH = "e" * 64
SCHOOL = "example-school"
BRANCH = f"data/{SCHOOL}-onboarding"


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def request():
    checkpoint_path = (
        ".remote-implementation/checkpoints/example-school/"
        "seal-001/checkpoint-manifest.json"
    )
    verification_path = (
        ".remote-implementation/verifications/example-school/"
        "seal-001/stage2-gate1-seal-verification.json"
    )
    return {
        "schema_version": 1,
        "kind": REQUEST_KIND,
        "request_id": "apply-001",
        "school_key": SCHOOL,
        "operation": OP_STAGE2_SEALED_APPLY,
        "previous_control_state_commit": CONTROL,
        "previous_control_state_sha256": "f" * 64,
        "expected_protected_main_sha": MAIN,
        "creation_provenance": {
            "origin": "ChatGPT",
            "authorization": "bounded exact sealed apply",
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
            "stage2_gate1_seal": False,
            "stage2_sealed_apply": True,
            "stage2_reconciliation_diagnostic": False,
        },
        "target_branch": BRANCH,
        "target_sha": TARGET,
        "stage2_gate1_seal_checkpoint": {
            "path": checkpoint_path,
            "sha256": SEAL_CHECKPOINT_SHA,
        },
        "stage2_gate1_seal_verification": {
            "path": verification_path,
            "sha256": SEAL_VERIFICATION_SHA,
        },
        "approved_plan_hash": APPROVED_HASH,
        "approved_plan_sha256": "a" * 64,
        "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
        "integration_freeze_sha256": FREEZE_SHA,
        "semantic_snapshot_sha256": SEMANTIC_SHA,
        "decision_universe_sha256": DECISION_SHA,
        "recommendation_map_sha256": MAP_SHA,
        "filled_review_sha256": FILLED_REVIEW_SHA,
        "decision_id_set_sha256": DECISION_ID_SHA,
    }


def init_repo(root: Path) -> str:
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "test"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
    (root / ".gitignore").write_text(".onboarding/\n", encoding="utf-8")
    (root / "data").mkdir()
    (root / "data/test.txt").write_text("before\n", encoding="utf-8")
    subprocess.run(["git", "add", ".gitignore", "data/test.txt"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "-m", "base"], cwd=root, check=True)
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()


class RemoteStage2SealedApplyTests(unittest.TestCase):
    def authority_fixture(self):
        req = request()
        approved_bytes = b'{"approved_plan_hash":"' + APPROVED_HASH.encode() + b'"}\n'
        req["approved_plan_sha256"] = sha(approved_bytes)
        seal_request_bytes = (
            json.dumps({"request_id": "seal-001"}, sort_keys=True) + "\n"
        ).encode()
        checkpoint_path = req["stage2_gate1_seal_checkpoint"]["path"]
        directory = Path(checkpoint_path).parent
        approved_path = (directory / "approved-plan.json").as_posix()
        manifest = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_CHECKPOINT",
            "request_id": "seal-001",
            "request_sha256": sha(seal_request_bytes),
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "seal_status": "SEALED",
            "approved_plan_hash": APPROVED_HASH,
            "approved_plan_sha256": sha(approved_bytes),
            "approved_plan_checkpoint_path": approved_path,
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "approved_plan_hash_preview": "0" * 64,
            "current_main_preseal_changed_path_count": 1,
            "current_main_preseal_site_gate_normalized_sha256": "1" * 64,
            "decision_count": 97,
        }
        checkpoint_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        verification = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_GATE1_SEAL_VERIFICATION",
            "request_id": "seal-001",
            "school_key": SCHOOL,
            "target_sha": TARGET,
            "seal_status": "SEALED",
            "approved_plan_hash": APPROVED_HASH,
            "approved_plan_sha256": sha(approved_bytes),
            "owner_gate_1_approval_sha256": OWNER_APPROVAL_SHA,
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "filled_review_sha256": FILLED_REVIEW_SHA,
            "decision_id_set_sha256": DECISION_ID_SHA,
            "tracked_stage2_mutation": "NONE",
            "remote_stage2_gate1_seal_equivalence": "PASS",
        }
        verification_bytes = (
            json.dumps(verification, indent=2, sort_keys=True) + "\n"
        ).encode()
        req["stage2_gate1_seal_checkpoint"]["sha256"] = sha(checkpoint_bytes)
        req["stage2_gate1_seal_verification"]["sha256"] = sha(verification_bytes)
        mapping = {
            checkpoint_path: checkpoint_bytes,
            req["stage2_gate1_seal_verification"]["path"]: verification_bytes,
            (directory / "request.json").as_posix(): seal_request_bytes,
            approved_path: approved_bytes,
        }
        return req, manifest, mapping

    def test_control_accepts_mutating_sealed_apply(self):
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
        self.assertEqual(state["lifecycle_state"], "ACTIVE")
        self.assertEqual(state["transaction_state"], "LOCKED")
        self.assertIsNotNone(state["active_lock_owner"])
        self.assertEqual(state["active_target_branch"], BRANCH)

    def test_control_rejects_missing_or_leaked_apply_authority(self):
        req = request()
        req["authority"]["stage2_sealed_apply"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_SEALED_APPLY_REQUEST_AUTHORITY_REQUIRED",
        ):
            validate_request(req)

        req = request()
        req["operation"] = "STAGE2_GATE1_SEAL"
        req["authority"]["stage2_sealed_apply"] = True
        req["authority"]["stage2_gate1_seal"] = True
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "REQUEST_SEALED_APPLY_AUTHORITY_FORBIDDEN",
        ):
            validate_request(req)

    def test_fresh_verified_seal_authenticates(self):
        req, manifest, mapping = self.authority_fixture()
        with (
            patch.object(
                applymod,
                "git_show_bytes",
                side_effect=lambda commit, path, **kwargs: mapping[path],
            ),
            patch.object(
                applymod,
                "verify_stage2_gate1_seal_authority",
                return_value={
                    "freeze_bytes": b"freeze",
                    "plan_bytes": b"plan",
                    "filled_review_bytes": b"review",
                    "target_tree_sha": TREE,
                },
            ),
        ):
            result = applymod.verify_stage2_sealed_apply_authority(req, CONTROL)
        self.assertEqual(result["seal_manifest"], manifest)
        self.assertEqual(result["approved_plan_bytes"], mapping[manifest["approved_plan_checkpoint_path"]])
        self.assertEqual(result["expected_changed_path_count"], 1)

    def test_unverified_seal_is_refused(self):
        req, manifest, mapping = self.authority_fixture()
        path = req["stage2_gate1_seal_verification"]["path"]
        verification = json.loads(mapping[path])
        verification["remote_stage2_gate1_seal_equivalence"] = "PENDING"
        data = (json.dumps(verification, indent=2, sort_keys=True) + "\n").encode()
        mapping[path] = data
        req["stage2_gate1_seal_verification"]["sha256"] = sha(data)
        with patch.object(
            applymod,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_SEALED_APPLY_SEAL_EQUIVALENCE_NOT_PASS",
            ):
                applymod.verify_stage2_sealed_apply_authority(req, CONTROL)

    def test_transactional_apply_prepares_exact_manifest_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            predecessor = init_repo(root)
            authority = {
                "freeze_bytes": b"{}\n",
                "approved_plan_bytes": b"{}\n",
                "plan_bytes": b"plan",
                "filled_review_bytes": b"review",
                "seal_manifest": {"approved_plan_hash": APPROVED_HASH},
                "expected_changed_path_count": 1,
            }

            def fake_run(command, **kwargs):
                (root / "data/test.txt").write_text("after\n", encoding="utf-8")
                output = Path(command[command.index("--output-dir") + 1])
                output.mkdir(parents=True, exist_ok=True)
                release = {
                    "schema_version": 1,
                    "school_key": SCHOOL,
                    "approved_plan_hash": APPROVED_HASH,
                    "base_commit": predecessor,
                    "branch": "test",
                    "changed_paths": ["data/test.txt"],
                    "summary": {"x": 1},
                    "execution": {},
                    "copied_state_gates": {},
                }
                (output / "release-manifest.json").write_text(
                    json.dumps(release, indent=2) + "\n", encoding="utf-8"
                )
                (output / "pr-body.md").write_text("pr\n", encoding="utf-8")
                (output / "visual-qa.md").write_text("qa\n", encoding="utf-8")
                return subprocess.CompletedProcess(
                    command,
                    0,
                    stdout="PASS: sealed plan applied transactionally and every automated gate passed.\n",
                )

            with (
                patch.object(applymod, "restore_integration_freeze"),
                patch.object(
                    applymod,
                    "verify_sealed_plan_bytes",
                    return_value={"approved_plan_hash": APPROVED_HASH},
                ),
                patch.object(applymod, "run", side_effect=fake_run),
            ):
                result = applymod.run_sealed_apply_tool(
                    root,
                    SCHOOL,
                    predecessor,
                    authority=authority,
                    diag=Path(directory).parent / "sealed-apply-test-diag",
                    tool_repo=ROOT,
                    prepare_commit=True,
                )
            self.assertEqual(result["prepared_parent_sha"], predecessor)
            self.assertEqual(result["changed_paths"], ["data/test.txt"])
            self.assertEqual(result["deleted_paths"], [])
            self.assertEqual(len(result["changed_file_sha256"]), 1)
            self.assertEqual(
                subprocess.check_output(
                    ["git", "show", f"{result['prepared_commit_sha']}:data/test.txt"],
                    cwd=root,
                    text=True,
                ),
                "after\n",
            )

    def test_prepared_proof_supports_deletions(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            predecessor = init_repo(root)
            (root / "data/test.txt").unlink()
            subprocess.run(["git", "add", "--", "data/test.txt"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-q", "-m", "delete"], cwd=root, check=True)
            prepared = subprocess.check_output(
                ["git", "rev-parse", "HEAD"], cwd=root, text=True
            ).strip()
            proof = applymod.verify_prepared_sealed_apply(
                root,
                predecessor_sha=predecessor,
                prepared_sha=prepared,
                changed_paths=["data/test.txt"],
                changed_file_sha256={},
                deleted_paths=["data/test.txt"],
            )
            self.assertEqual(proof["deleted_paths"], ["data/test.txt"])

    def test_runner_refuses_changed_target_before_lock(self):
        req = request()
        with (
            patch.object(
                runner,
                "verify_stage2_sealed_apply_authority",
                return_value={"target_tree_sha": TREE},
            ),
            patch.object(runner, "remote_head", return_value="f" * 40),
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_SEALED_APPLY_TARGET_HEAD_MISMATCH",
            ):
                runner.run_stage2_sealed_apply(
                    initial_control_state(),
                    req,
                    b"{}",
                    "e" * 40,
                    CONTROL,
                    MAIN,
                )

    def test_fresh_verifier_dispatches_sealed_apply(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_SEALED_APPLY,
            "request_id": "apply-001",
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
                "verify_stage2_sealed_apply",
                return_value=0,
            ) as verify,
        ):
            self.assertEqual(verifier.main(), 0)
        verify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
