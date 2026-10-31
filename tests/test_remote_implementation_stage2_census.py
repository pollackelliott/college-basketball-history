import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remote_implementation_control import RemoteImplementationError, sha256_bytes  # noqa: E402
import remote_implementation_stage2_census as stage2_runtime  # noqa: E402
from remote_implementation_stage2_census import (  # noqa: E402
    STAGE2_ARTIFACT_NAMES,
    add_existing_onboarding_worktree,
    normalize_artifact_bytes,
    run_stage2_census_tool,
    verify_phase0_authority,
)


SCHOOL = "example-school"
SEMANTIC = "9" * 64
TARGET_BRANCH = "data/example-school-onboarding"


class RemoteStage2CensusTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> str:
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if cp.returncode:
            self.fail(cp.stdout)
        return cp.stdout.strip()

    def make_tool_repo(self, mode: str = "ready") -> Path:
        repo = Path(tempfile.mkdtemp(prefix="stage2-census-test-"))
        self.addCleanup(lambda: shutil.rmtree(repo, ignore_errors=True))
        previous_runtime_root = stage2_runtime.RUNTIME_ROOT
        stage2_runtime.RUNTIME_ROOT = repo
        self.addCleanup(
            lambda: setattr(stage2_runtime, "RUNTIME_ROOT", previous_runtime_root)
        )
        self.git(repo, "init")
        self.git(repo, "config", "user.name", "Test")
        self.git(repo, "config", "user.email", "test@example.com")
        (repo / ".gitignore").write_text(".onboarding/\n", encoding="utf-8")
        (repo / "tracked.txt").write_text("stable\n", encoding="utf-8")
        (repo / "mode.txt").write_text(mode + "\n", encoding="utf-8")
        tools = repo / "tools"
        tools.mkdir()
        script = r"""#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path

school = sys.argv[1]
repo = Path(sys.argv[sys.argv.index("--repo") + 1]).resolve()
mode = (repo / "mode.txt").read_text().strip()
out = repo / ".onboarding" / school
out.mkdir(parents=True, exist_ok=True)
decision_sha = "d" * 64
plan = {
    "blockers": ["synthetic blocker"] if mode == "blocked" else [],
    "warnings": ["synthetic warning"],
    "decisions": [{"decision_id": "D-1", "category": "identity", "field_name": "opponent"}],
    "summary": {"canonical_site_patch_reviews": 0},
    "runner_root": str(repo),
}
(out / "plan.json").write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n")
with (out / "review.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(["decision_id", "category"])
    writer.writerow(["D-1", "identity"])
(out / "review.md").write_text("# Synthetic review\n\n" + str(repo) + "\n")
census = {
    "schema_version": 1,
    "status": "PREFLIGHT_BLOCKED" if mode == "blocked" else "CENSUS_CAPTURED",
    "preflight": {
        "blocker_count": 1 if mode == "blocked" else 0,
        "warning_count": 1,
        "decision_count": 1,
        "decision_categories": {"identity": 1},
        "decision_fields": {"opponent": 1},
        "canonical_site_patch_reviews": 0,
    },
    "topology_groups": [{"topology": "synthetic", "count": 1}],
}
(out / "implementation-stage2-capability-census.json").write_text(
    json.dumps(census, indent=2, sort_keys=True) + "\n"
)
status_name = "BLOCKED" if mode == "blocked" else "CAPABILITY_CENSUS_READY"
status = {
    "schema_version": 1,
    "school_key": school,
    "stage": "IMPLEMENTATION_STAGE_2",
    "status": status_name,
    "branch": "synthetic",
    "head_sha": "a" * 40,
    "semantic_drift": {"status": "PASS", "change_count": 0},
    "preflight": {
        "blocker_count": 1 if mode == "blocked" else 0,
        "warning_count": 1,
        "decision_count": 1,
        "decision_categories": {"identity": 1},
        "decision_universe_sha256": decision_sha,
        "plan_path": ".onboarding/%s/plan.json" % school,
        "review_path": ".onboarding/%s/review.csv" % school,
    },
    "capability_census": {
        "path": ".onboarding/%s/implementation-stage2-capability-census.json" % school,
        "status": census["status"],
        "topology_group_count": 1,
    },
}
if mode == "semantic":
    status["status"] = "BLOCKED"
    status["last_error"] = "INTEGRATION_FROZEN semantic drift detected"
if mode == "mutate":
    (repo / "tracked.txt").write_text("mutated\n")
(out / "implementation-stage2-status.json").write_text(
    json.dumps(status, indent=2, sort_keys=True) + "\n"
)
raise SystemExit(1 if status["status"] == "BLOCKED" else 0)
"""
        (tools / "implementation_stage2.py").write_text(script, encoding="utf-8")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "fixture")
        return repo

    def test_runtime_tool_is_separate_from_target_snapshot(self):
        repo = self.make_tool_repo("ready")
        runtime = Path(tempfile.mkdtemp(prefix="stage2-runtime-tool-"))
        self.addCleanup(lambda: shutil.rmtree(runtime, ignore_errors=True))
        (runtime / "tools").mkdir(parents=True)
        shutil.copyfile(
            repo / "tools/implementation_stage2.py",
            runtime / "tools/implementation_stage2.py",
        )
        (repo / "tools/implementation_stage2.py").write_text(
            "raise SystemExit('STALE TARGET TOOL EXECUTED')\n",
            encoding="utf-8",
        )
        self.git(repo, "add", "tools/implementation_stage2.py")
        self.git(repo, "commit", "-m", "install stale target tool")
        result = run_stage2_census_tool(
            repo,
            SCHOOL,
            b'{"status":"INTEGRATION_FROZEN"}\n',
            repo.parent / "diag-runtime-boundary",
            tool_repo=runtime,
        )
        self.assertEqual(result["stage2_status"], "CAPABILITY_CENSUS_READY")
        self.assertEqual(result["exit_code"], 0)

    def test_capability_census_ready_checkpoint_surface(self):
        repo = self.make_tool_repo("ready")
        result = run_stage2_census_tool(
            repo,
            SCHOOL,
            b'{"status":"INTEGRATION_FROZEN"}\n',
            repo.parent / "diag-ready",
        )
        self.assertEqual(result["stage2_status"], "CAPABILITY_CENSUS_READY")
        self.assertEqual(result["exit_code"], 0)
        self.assertEqual(
            set(result["artifact_sha256"]),
            set(STAGE2_ARTIFACT_NAMES),
        )
        self.assertEqual(
            result["status"]["preflight"]["decision_universe_sha256"],
            "d" * 64,
        )
        self.assertEqual(
            result["tracked_mutation_proof"]["tracked_stage2_mutation"],
            "NONE",
        )

    def test_permanent_blocked_is_preserved_not_remote_failure(self):
        repo = self.make_tool_repo("blocked")
        result = run_stage2_census_tool(
            repo,
            SCHOOL,
            b'{"status":"INTEGRATION_FROZEN"}\n',
            repo.parent / "diag-blocked",
        )
        self.assertEqual(result["stage2_status"], "BLOCKED")
        self.assertEqual(result["exit_code"], 1)
        self.assertEqual(
            result["capability_census"]["status"],
            "PREFLIGHT_BLOCKED",
        )

    def test_semantic_drift_blocked_is_preserved(self):
        repo = self.make_tool_repo("semantic")
        result = run_stage2_census_tool(
            repo,
            SCHOOL,
            b'{"status":"INTEGRATION_FROZEN"}\n',
            repo.parent / "diag-semantic",
        )
        self.assertEqual(result["stage2_status"], "BLOCKED")
        self.assertIn("semantic drift", result["status"]["last_error"])

    def test_tracked_mutation_is_refused(self):
        repo = self.make_tool_repo("mutate")
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "TRACKED_STAGE2_MUTATION_DETECTED",
        ):
            run_stage2_census_tool(
                repo,
                SCHOOL,
                b'{"status":"INTEGRATION_FROZEN"}\n',
                repo.parent / "diag-mutate",
            )

    def test_path_normalization_is_explicit_and_bounded(self):
        repo = Path("/tmp/runner-one")
        raw = b'{"repo":"/tmp/runner-one","other":"/tmp/not-runner"}\n'
        normalized = normalize_artifact_bytes("implementation-stage2-status.json", raw, repo)
        self.assertIn(b"<REPO>", normalized)
        self.assertIn(b"/tmp/not-runner", normalized)

    def test_worktree_branch_normalization_is_explicit(self):
        repo = Path("/tmp/runner-one")
        one = (
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "CAPABILITY_CENSUS_READY",
                    "branch": "remote-stage2-census/example-aaaaaaaaaaaa",
                    "head_sha": "a" * 40,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode()
        two = (
            json.dumps(
                {
                    "schema_version": 1,
                    "status": "CAPABILITY_CENSUS_READY",
                    "branch": "remote-stage2-census/example-bbbbbbbbbbbb",
                    "head_sha": "a" * 40,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n"
        ).encode()
        self.assertEqual(
            normalize_artifact_bytes(
                "implementation-stage2-status.json", one, repo
            ),
            normalize_artifact_bytes(
                "implementation-stage2-status.json", two, repo
            ),
        )

    def test_generated_timestamp_normalization_is_explicit(self):
        repo = Path("/tmp/runner-one")
        plan_one = (
            json.dumps(
                {
                    "created_at": "2026-10-23T00:00:00+00:00",
                    "value": "same",
                },
                indent=2,
            )
            + "\n"
        ).encode()
        plan_two = (
            json.dumps(
                {
                    "created_at": "2026-10-23T00:01:00+00:00",
                    "value": "same",
                },
                indent=2,
            )
            + "\n"
        ).encode()
        self.assertEqual(
            normalize_artifact_bytes("plan.json", plan_one, repo),
            normalize_artifact_bytes("plan.json", plan_two, repo),
        )
        review_one = b"# Review\n\nGenerated: one\nStable\n"
        review_two = b"# Review\n\nGenerated: two\nStable\n"
        self.assertEqual(
            normalize_artifact_bytes("review.md", review_one, repo),
            normalize_artifact_bytes("review.md", review_two, repo),
        )


    def make_authority_repo(self):
        repo = Path(tempfile.mkdtemp(prefix="stage2-authority-test-"))
        self.addCleanup(lambda: shutil.rmtree(repo, ignore_errors=True))
        self.git(repo, "init")
        self.git(repo, "config", "user.name", "Test")
        self.git(repo, "config", "user.email", "test@example.com")
        package_hashes = {}
        school_dir = repo / "schools" / SCHOOL
        school_dir.mkdir(parents=True)
        for name in (
            "conferences.csv",
            "notes.md",
            "opponents.csv",
            "source-games.csv",
            "source-notes.md",
            "venues.csv",
        ):
            data = (name + "\n").encode()
            (school_dir / name).write_bytes(data)
            package_hashes[name] = hashlib.sha256(data).hexdigest()
        (repo / "base.txt").write_text("base\n")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "target")
        target_sha = self.git(repo, "rev-parse", "HEAD")

        freeze = {
            "status": "INTEGRATION_FROZEN",
            "school_key": SCHOOL,
            "package_member_sha256": package_hashes,
            "source_game_semantic_guard": {"snapshot_sha256": SEMANTIC},
        }
        freeze_bytes = (
            json.dumps(freeze, indent=2, sort_keys=True) + "\n"
        ).encode()
        freeze_sha = hashlib.sha256(freeze_bytes).hexdigest()
        writeahead_path = (
            ".remote-implementation/writeahead/example-school/phase0/"
            "writeahead-manifest.json"
        )
        freeze_path = str(Path(writeahead_path).parent / "integration-freeze.json")
        (repo / freeze_path).parent.mkdir(parents=True)
        (repo / freeze_path).write_bytes(freeze_bytes)
        writeahead = {
            "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "prepared_commit_sha": target_sha,
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": SEMANTIC,
            "sidecars": {"integration-freeze.json": freeze_sha},
        }
        writeahead_bytes = (
            json.dumps(writeahead, indent=2, sort_keys=True) + "\n"
        ).encode()
        (repo / writeahead_path).write_bytes(writeahead_bytes)
        writeahead_sha = hashlib.sha256(writeahead_bytes).hexdigest()
        successor_path = (
            ".remote-implementation/successors/example-school/phase0/"
            "successor-manifest.json"
        )
        successor = {
            "kind": "REMOTE_IMPLEMENTATION_SUCCESSOR",
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "actual_published_target_sha": target_sha,
            "prepared_commit_sha": target_sha,
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": SEMANTIC,
            "repository_validation": "PASS",
            "final_transaction_state": "COMPLETE",
            "protected_main_sha": "1" * 40,
            "writeahead_manifest_path": writeahead_path,
            "writeahead_manifest_sha256": writeahead_sha,
        }
        successor_bytes = (
            json.dumps(successor, indent=2, sort_keys=True) + "\n"
        ).encode()
        (repo / successor_path).parent.mkdir(parents=True)
        (repo / successor_path).write_bytes(successor_bytes)
        self.git(repo, "add", ".remote-implementation")
        self.git(repo, "commit", "-m", "control authority")
        control_sha = self.git(repo, "rev-parse", "HEAD")
        request = {
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "target_sha": target_sha,
            "phase0_successor": {
                "path": successor_path,
                "sha256": hashlib.sha256(successor_bytes).hexdigest(),
            },
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": SEMANTIC,
        }
        return repo, control_sha, request, freeze_path

    def add_verified_display_successor(
        self,
        repo: Path,
        request: dict,
        *,
        extra_school_change: bool = False,
        bad_predecessor: bool = False,
        verification_pass: bool = True,
    ):
        phase0_target = request["target_sha"]
        control_branch = self.git(repo, "branch", "--show-current")
        self.git(repo, "checkout", "-b", "display-target", phase0_target)
        school_dir = repo / "schools" / SCHOOL
        (school_dir / "opponents.csv").write_text("opponents.csv display\n")
        (school_dir / "source-games.csv").write_text("source-games.csv display\n")
        if extra_school_change:
            (school_dir / "notes.md").write_text("notes.md unrelated\n")
        self.git(repo, "add", "schools")
        self.git(repo, "commit", "-m", "display successor")
        display_sha = self.git(repo, "rev-parse", "HEAD")
        display_tree = self.git(repo, "rev-parse", "HEAD^{tree}")
        self.git(repo, "checkout", control_branch)

        allowed_paths = [
            f"schools/{SCHOOL}/opponents.csv",
            f"schools/{SCHOOL}/source-games.csv",
        ]
        changed_hashes = {}
        for changed_path in allowed_paths:
            data = subprocess.run(
                ["git", "show", f"{display_sha}:{changed_path}"],
                cwd=repo,
                stdout=subprocess.PIPE,
                check=True,
            ).stdout
            changed_hashes[changed_path] = hashlib.sha256(data).hexdigest()

        blocker_keys = ["alpha-academy"]
        proof = {
            "schema_version": 1,
            "school_key": SCHOOL,
            "allowed_paths": allowed_paths,
            "literal_evidence_changes": 0,
            "opponent_key_changes": 0,
            "source_game_non_name_field_changes": 0,
            "opponent_changed_keys": blocker_keys,
            "source_game_changed_keys": blocker_keys,
            "source_game_normalized_name_row_count": 1,
        }
        proof_bytes = (json.dumps(proof, indent=2, sort_keys=True) + "\n").encode()
        proof_sha = hashlib.sha256(proof_bytes).hexdigest()
        normalization_sha = "a" * 64
        display_request_id = "example-display-0001"
        writeahead_path = (
            f".remote-implementation/writeahead/{SCHOOL}/"
            f"{display_request_id}/writeahead-manifest.json"
        )
        writeahead_dir = repo / Path(writeahead_path).parent
        writeahead_dir.mkdir(parents=True, exist_ok=True)
        (writeahead_dir / "field-level-proof.json").write_bytes(proof_bytes)

        writeahead = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
            "operation": "STAGE2_OPPONENT_DISPLAY_NORMALIZE",
            "request_id": display_request_id,
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "expected_target_predecessor_sha": phase0_target,
            "prepared_parent_sha": phase0_target,
            "prepared_commit_sha": display_sha,
            "prepared_tree_sha": display_tree,
            "changed_paths": allowed_paths,
            "allowed_paths": allowed_paths,
            "changed_file_sha256": changed_hashes,
            "integration_freeze_sha256": request["integration_freeze_sha256"],
            "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
            "field_level_proof_sha256": proof_sha,
            "sidecars": {"field-level-proof.json": proof_sha},
        }
        writeahead_bytes = (json.dumps(writeahead, indent=2, sort_keys=True) + "\n").encode()
        (repo / writeahead_path).write_bytes(writeahead_bytes)
        writeahead_sha = hashlib.sha256(writeahead_bytes).hexdigest()

        drift = {
            "status": "PASS",
            "changes": [],
            "baseline_sha256": request["semantic_snapshot_sha256"],
            "current_sha256": request["semantic_snapshot_sha256"],
        }
        successor_path = (
            f".remote-implementation/successors/{SCHOOL}/"
            f"{display_request_id}/successor-manifest.json"
        )
        successor = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
            "operation": "STAGE2_OPPONENT_DISPLAY_NORMALIZE",
            "request_id": display_request_id,
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "expected_target_predecessor_sha": (
                "f" * 40 if bad_predecessor else phase0_target
            ),
            "prepared_parent_sha": phase0_target,
            "actual_published_target_sha": display_sha,
            "prepared_commit_sha": display_sha,
            "prepared_tree_sha": display_tree,
            "publication_cas": "EXISTING_REF_CAS_PASS",
            "repository_validation": "PASS",
            "final_transaction_state": "COMPLETE",
            "protected_main_sha": "1" * 40,
            "integration_freeze_sha256": request["integration_freeze_sha256"],
            "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
            "semantic_drift_before": drift,
            "semantic_drift_after": drift,
            "changed_paths": allowed_paths,
            "changed_file_sha256": changed_hashes,
            "expected_blocker_keys": blocker_keys,
            "field_level_proof_sha256": proof_sha,
            "normalization_report_sha256": normalization_sha,
            "source_game_normalized_name_row_count": 1,
            "writeahead_manifest_path": writeahead_path,
            "writeahead_manifest_sha256": writeahead_sha,
        }
        successor_bytes = (json.dumps(successor, indent=2, sort_keys=True) + "\n").encode()
        successor_file = repo / successor_path
        successor_file.parent.mkdir(parents=True, exist_ok=True)
        successor_file.write_bytes(successor_bytes)

        verification_path = (
            f".remote-implementation/verifications/{SCHOOL}/"
            f"{display_request_id}/stage2-opponent-display-verification.json"
        )
        verification = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_VERIFICATION",
            "request_id": display_request_id,
            "school_key": SCHOOL,
            "protected_main_sha": "1" * 40,
            "target_branch": TARGET_BRANCH,
            "target_predecessor_sha": phase0_target,
            "target_sha": display_sha,
            "target_tree_sha": display_tree,
            "integration_freeze_sha256": request["integration_freeze_sha256"],
            "semantic_snapshot_sha256": request["semantic_snapshot_sha256"],
            "field_level_proof_sha256": proof_sha,
            "normalization_report_sha256": normalization_sha,
            "changed_paths": allowed_paths,
            "expected_blocker_keys": blocker_keys,
            "semantic_drift": "PASS",
            "tracked_stage2_mutation": "NONE",
            "remote_stage2_opponent_display_equivalence": (
                "PASS" if verification_pass else "FAIL"
            ),
        }
        verification_file = repo / verification_path
        verification_file.parent.mkdir(parents=True, exist_ok=True)
        verification_file.write_text(json.dumps(verification, indent=2, sort_keys=True) + "\n")

        self.git(repo, "add", ".remote-implementation")
        self.git(repo, "commit", "-m", "display control authority")
        control_sha = self.git(repo, "rev-parse", "HEAD")
        request = dict(request)
        request["target_sha"] = display_sha
        request["stage2_opponent_display_successor"] = {
            "path": successor_path,
            "sha256": hashlib.sha256(successor_bytes).hexdigest(),
        }
        return control_sha, request

    def test_wrong_onboarding_sha_is_rejected_before_worktree(self):
        with patch(
            "remote_implementation_stage2_census.remote_head",
            return_value="a" * 40,
        ):
            with self.assertRaisesRegex(
                RemoteImplementationError,
                "STAGE2_ONBOARDING_HEAD_MISMATCH",
            ):
                add_existing_onboarding_worktree(
                    TARGET_BRANCH,
                    "b" * 40,
                    SCHOOL,
                    source_repo=Path("/tmp/not-used"),
                )

    def test_phase0_authority_and_freeze_are_authenticated(self):
        repo, control_sha, request, _ = self.make_authority_repo()
        authority = verify_phase0_authority(
            request,
            control_sha,
            source_repo=repo,
        )
        self.assertEqual(
            hashlib.sha256(authority["freeze_bytes"]).hexdigest(),
            request["integration_freeze_sha256"],
        )

    def test_tampered_integration_freeze_is_refused(self):
        repo, _, request, freeze_path = self.make_authority_repo()
        (repo / freeze_path).write_text('{"tampered":true}\n', encoding="utf-8")
        self.git(repo, "add", freeze_path)
        self.git(repo, "commit", "-m", "tamper")
        tampered_control = self.git(repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_PHASE0_FREEZE_BYTES_MISMATCH",
        ):
            verify_phase0_authority(
                request,
                tampered_control,
                source_repo=repo,
            )


if __name__ == "__main__":
    unittest.main()
