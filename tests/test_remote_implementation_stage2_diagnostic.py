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

import remote_implementation_io as remote_io  # noqa: E402
import remote_implementation_runner as runner  # noqa: E402
import remote_implementation_stage2_diagnostic as diagnostic  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
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
SCHOOL = "example-school"
BRANCH = f"data/{SCHOOL}-onboarding"
GAME = "CBBG-1234567"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def request():
    return {
        "schema_version": 1,
        "kind": REQUEST_KIND,
        "request_id": "diagnostic-001",
        "school_key": SCHOOL,
        "operation": OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
        "previous_control_state_commit": CONTROL,
        "previous_control_state_sha256": "6" * 64,
        "expected_protected_main_sha": MAIN,
        "creation_provenance": {
            "origin": "ChatGPT",
            "authorization": "bounded owner-authorized diagnostic",
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
            "stage2_reconciliation_diagnostic": True,
        },
        "target_branch": BRANCH,
        "target_sha": TARGET,
        "stage2_proposal_checkpoint": {
            "path": (
                ".remote-implementation/checkpoints/example-school/"
                "proposal-001/checkpoint-manifest.json"
            ),
            "sha256": CHECKPOINT_SHA,
        },
        "integration_freeze_sha256": FREEZE_SHA,
        "semantic_snapshot_sha256": SEMANTIC_SHA,
        "decision_universe_sha256": DECISION_SHA,
        "recommendation_map_sha256": MAP_SHA,
        "canonical_game_id": GAME,
    }


class RemoteStage2ReconciliationDiagnosticTests(unittest.TestCase):
    def test_exact_main_runtime_executes_changed_transitive_reconciliation_tooling(self):
        with tempfile.TemporaryDirectory() as directory:
            source_repo = Path(directory) / "source"
            source_repo.mkdir()
            subprocess.run(["git", "init"], cwd=source_repo, check=True, capture_output=True)
            subprocess.run(
                ["git", "config", "user.email", "runtime@example.invalid"],
                cwd=source_repo,
                check=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Runtime Regression"],
                cwd=source_repo,
                check=True,
            )
            tools = source_repo / "tools"
            tools.mkdir()
            hardening = tools / "onboarding_hardening.py"
            hardening.write_text(
                "import json, sys\n"
                "from pathlib import Path\n"
                "import onboarding_plan\n"
                "school=sys.argv[2]\n"
                "repo=Path(sys.argv[sys.argv.index('--repo')+1])\n"
                "game=sys.argv[sys.argv.index('--canonical-game-id')+1]\n"
                "out=repo/'.onboarding'/school/'last-rehearsal-reconciliation-trace.json'\n"
                "out.parent.mkdir(parents=True, exist_ok=True)\n"
                "doc={'kind':'IMPLEMENTATION_RECONCILIATION_TRACE','school_key':school,"
                "'canonical_game_id':game,'diagnostic_status':'PASS',"
                "'execution_status':onboarding_plan.RUNTIME_MARKER,'execution_error':'',"
                "'partial_location_classification':'FINAL_LOCATION_NOT_PARTIAL',"
                "'real_tracked_repository_unchanged':True,'decision_order':[],"
                "'mutations':[],'site_sync_events':[],'integrity':{'status':'PASS'}}\n"
                "out.write_text(json.dumps(doc, sort_keys=True)+'\\n', encoding='utf-8')\n",
                encoding="utf-8",
            )
            (tools / "reconciliation_trace.py").write_text("# fixture\n", encoding="utf-8")
            (tools / "onboard_school.py").write_text("# fixture\n", encoding="utf-8")
            plan = tools / "onboarding_plan.py"
            plan.write_text("RUNTIME_MARKER = 'STALE_CONTROL'\n", encoding="utf-8")
            subprocess.run(["git", "add", "tools"], cwd=source_repo, check=True)
            subprocess.run(
                ["git", "commit", "-m", "stale control runtime"],
                cwd=source_repo,
                check=True,
                capture_output=True,
            )
            stale = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=source_repo,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()

            plan.write_text("RUNTIME_MARKER = 'FRESH_MAIN'\n", encoding="utf-8")
            subprocess.run(["git", "add", "tools/onboarding_plan.py"], cwd=source_repo, check=True)
            subprocess.run(
                ["git", "commit", "-m", "fresh main reconciliation"],
                cwd=source_repo,
                check=True,
                capture_output=True,
            )
            live_main = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=source_repo,
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            subprocess.run(
                ["git", "update-ref", "refs/remotes/origin/main", live_main],
                cwd=source_repo,
                check=True,
            )
            subprocess.run(
                ["git", "checkout", "--detach", stale],
                cwd=source_repo,
                check=True,
                capture_output=True,
            )

            runtime_repo = remote_io.add_exact_protected_main_runtime_worktree(
                live_main,
                source_repo=source_repo,
            )
            self.assertEqual(
                (source_repo / "tools/onboarding_plan.py").read_text(encoding="utf-8"),
                "RUNTIME_MARKER = 'STALE_CONTROL'\n",
            )
            self.assertEqual(
                (runtime_repo / "tools/onboarding_plan.py").read_text(encoding="utf-8"),
                "RUNTIME_MARKER = 'FRESH_MAIN'\n",
            )

            target = Path(directory) / "target"
            target.mkdir()
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            with patch.object(
                diagnostic,
                "tracked_worktree_state",
                side_effect=[clean, clean],
            ):
                result = diagnostic.run_stage2_reconciliation_diagnostic_tool(
                    target,
                    SCHOOL,
                    freeze_bytes=b"{}\n",
                    map_bytes=b"{}\n",
                    plan_bytes=b"{}\n",
                    review_bytes=b"decision_id\n",
                    canonical_game_id=GAME,
                    diag=target / "diag",
                    tool_repo=runtime_repo,
                )

            self.assertEqual(result["trace"]["execution_status"], "FRESH_MAIN")
            self.assertEqual(
                set(remote_io.STAGE2_TRANSITIVE_RUNTIME_TOOL_PATHS),
                set(result["runtime_tool_manifest_sha256"]),
            )

    def authority_fixture(self):
        proposal_request_bytes = (
            json.dumps({"request_id": "proposal-001"}, sort_keys=True) + "\n"
        ).encode()
        map_bytes = b'{"decisions":{}}\n'
        plan_bytes = b'{"decisions":[]}\n'
        review_bytes = b"decision_id,decision\n"
        checkpoint_path = request()["stage2_proposal_checkpoint"]["path"]
        directory = Path(checkpoint_path).parent
        map_path = (directory / "recommendation-map.json").as_posix()
        manifest = {
            "schema_version": 1,
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_PROPOSAL_REHEARSAL_CHECKPOINT",
            "request_id": "proposal-001",
            "request_sha256": sha(proposal_request_bytes),
            "school_key": SCHOOL,
            "protected_main_sha": "0" * 40,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "stage2_status": "BLOCKED",
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_checkpoint_path": map_path,
            "recommendation_map_sha256": sha(map_bytes),
            "artifact_sha256": {
                "plan.json": sha(plan_bytes),
                "review.csv": sha(review_bytes),
            },
        }
        checkpoint_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        req = request()
        req["stage2_proposal_checkpoint"]["sha256"] = sha(checkpoint_bytes)
        req["recommendation_map_sha256"] = sha(map_bytes)
        mapping = {
            checkpoint_path: checkpoint_bytes,
            (directory / "request.json").as_posix(): proposal_request_bytes,
            map_path: map_bytes,
            (directory / "plan.json").as_posix(): plan_bytes,
            (directory / "review.csv").as_posix(): review_bytes,
        }
        return req, manifest, mapping

    def test_control_accepts_bounded_read_only_diagnostic_request(self):
        req = request()
        validate_request(req)
        state = begin_request(
            initial_control_state(),
            req,
            "7" * 64,
            run_id="100",
            run_attempt="1",
            request_commit="8" * 40,
        )
        self.assertEqual(state["lifecycle_state"], "READ_ONLY_ACTIVE")
        self.assertEqual(
            state["transaction_state"],
            "STAGE2_RECONCILIATION_DIAGNOSTIC_RUNNING",
        )
        self.assertIsNone(state["active_lock_commit"])
        self.assertTrue(state["recovery_required"])

    def test_control_rejects_invalid_game_or_extra_proposal_authority(self):
        req = request()
        req["canonical_game_id"] = "Tennessee-1941"
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_DIAGNOSTIC_CANONICAL_GAME_ID_INVALID",
        ):
            validate_request(req)

        req = request()
        req["authority"]["stage2_proposal_rehearsal"] = True
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_DIAGNOSTIC_PROPOSAL_AUTHORITY_FORBIDDEN",
        ):
            validate_request(req)

    def test_exact_blocked_proposal_checkpoint_authenticates(self):
        req, manifest, mapping = self.authority_fixture()

        def fake_show(commit, path, **kwargs):
            return mapping[path]

        with (
            patch.object(diagnostic, "git_show_bytes", side_effect=fake_show),
            patch.object(
                diagnostic,
                "verify_stage2_proposal_authority",
                return_value={"freeze_bytes": b"freeze"},
            ),
        ):
            result = diagnostic.verify_stage2_diagnostic_authority(
                req,
                CONTROL,
            )

        self.assertEqual(result["proposal_manifest"], manifest)
        self.assertEqual(result["target_tree_sha"], TREE)
        self.assertEqual(result["freeze_bytes"], b"freeze")
        self.assertEqual(result["map_bytes"], mapping[manifest["recommendation_map_checkpoint_path"]])
        self.assertEqual(result["plan_bytes"], mapping[(Path(req["stage2_proposal_checkpoint"]["path"]).parent / "plan.json").as_posix()])

    def test_nonblocked_proposal_checkpoint_is_refused(self):
        req, manifest, mapping = self.authority_fixture()
        checkpoint_path = req["stage2_proposal_checkpoint"]["path"]
        manifest["stage2_status"] = "OWNER_GATE_1_READY"
        checkpoint_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        mapping[checkpoint_path] = checkpoint_bytes
        req["stage2_proposal_checkpoint"]["sha256"] = sha(checkpoint_bytes)

        with patch.object(
            diagnostic,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_DIAGNOSTIC_PROPOSAL_CHECKPOINT_NOT_BLOCKED",
            ):
                diagnostic.verify_stage2_diagnostic_authority(req, CONTROL)

    def test_permanent_diagnostic_proves_no_tracked_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / ".onboarding" / SCHOOL
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            trace = {
                "schema_version": 1,
                "kind": "IMPLEMENTATION_RECONCILIATION_TRACE",
                "school_key": SCHOOL,
                "canonical_game_id": GAME,
                "diagnostic_status": "PASS",
                "execution_status": "RECONCILIATION_BLOCKED",
                "execution_error": (
                    "CBBG-1234567: final reconciliation leaves partial canonical city/state"
                ),
                "partial_location_classification": "PREEXISTING_PERSISTED",
                "real_tracked_repository_unchanged": True,
                "decision_order": [],
                "mutations": [],
                "site_sync_events": [],
                "integrity": {"status": "FAIL"},
            }

            def fake_run(command, **kwargs):
                output.mkdir(parents=True, exist_ok=True)
                (output / diagnostic.TRACE_NAME).write_text(
                    json.dumps(trace, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
                return subprocess.CompletedProcess(command, 0, stdout="PASS\n")

            with (
                patch.object(diagnostic, "restore_integration_freeze"),
                patch.object(
                    diagnostic,
                    "tracked_worktree_state",
                    side_effect=[clean, clean],
                ),
                patch.object(diagnostic, "run", side_effect=fake_run),
            ):
                result = diagnostic.run_stage2_reconciliation_diagnostic_tool(
                    root,
                    SCHOOL,
                    freeze_bytes=b"freeze",
                    map_bytes=b"{}\n",
                    plan_bytes=b"{}\n",
                    review_bytes=b"decision_id\n",
                    canonical_game_id=GAME,
                    diag=root / "diag",
                    tool_repo=ROOT,
                )

            self.assertEqual(
                result["tracked_mutation_proof"]["tracked_stage2_mutation"],
                "NONE",
            )
            self.assertEqual(
                result["trace"]["partial_location_classification"],
                "PREEXISTING_PERSISTED",
            )

    def test_permanent_diagnostic_refuses_tracked_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
            dirty = {
                "head_sha": TARGET,
                "tree_sha": TREE,
                "status": " M data/canonical/games.csv\n",
            }
            with (
                patch.object(diagnostic, "restore_integration_freeze"),
                patch.object(
                    diagnostic,
                    "tracked_worktree_state",
                    side_effect=[clean, dirty],
                ),
                patch.object(
                    diagnostic,
                    "run",
                    return_value=subprocess.CompletedProcess([], 0, stdout=""),
                ),
            ):
                with self.assertRaisesRegex(
                    Stop,
                    "STAGE2_DIAGNOSTIC_TRACKED_MUTATION_DETECTED",
                ):
                    diagnostic.run_stage2_reconciliation_diagnostic_tool(
                        root,
                        SCHOOL,
                        freeze_bytes=b"freeze",
                        map_bytes=b"{}\n",
                        plan_bytes=b"{}\n",
                        review_bytes=b"decision_id\n",
                        canonical_game_id=GAME,
                        diag=root / "diag",
                        tool_repo=ROOT,
                    )

    def test_runner_refuses_changed_target_before_acceptance(self):
        req = request()
        with (
            patch.object(
                runner,
                "verify_stage2_diagnostic_authority",
                return_value={"target_tree_sha": TREE},
            ),
            patch.object(runner, "remote_head", return_value="f" * 40),
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_DIAGNOSTIC_TARGET_HEAD_MISMATCH",
            ):
                runner.run_read_only_stage2_reconciliation_diagnostic(
                    initial_control_state(),
                    req,
                    b"{}",
                    "1" * 40,
                    CONTROL,
                    MAIN,
                )

    def test_runner_executes_and_checkpoints_read_only_diagnostic(self):
        req = request()
        authority = {
            "target_tree_sha": TREE,
            "freeze_bytes": b"freeze",
            "map_bytes": b"map",
            "plan_bytes": b"plan",
            "review_bytes": b"review",
        }
        result = {
            "trace": {"partial_location_classification": "PREEXISTING_PERSISTED"},
            "trace_bytes": b"{}\n",
            "trace_sha256": sha(b"{}\n"),
            "tracked_mutation_proof": {"after_tree_sha": TREE},
        }
        cp = subprocess.CompletedProcess([], 0, stdout=TREE + "\n")
        with tempfile.TemporaryDirectory() as directory:
            worktree = Path(directory)
            with (
                patch.object(
                    runner,
                    "verify_stage2_diagnostic_authority",
                    return_value=authority,
                ),
                patch.object(
                    runner,
                    "remote_head",
                    side_effect=[TARGET, TARGET],
                ),
                patch.object(
                    runner,
                    "begin_request",
                    return_value=initial_control_state(),
                ),
                patch.object(runner, "write_json"),
                patch.object(runner, "archive_request", return_value=Path("archive")),
                patch.object(runner, "commit_control", return_value="2" * 40),
                patch.object(
                    runner,
                    "add_existing_onboarding_worktree",
                    return_value=worktree,
                ),
                patch.object(runner, "git", return_value=cp),
                patch.object(
                    runner,
                    "add_exact_protected_main_runtime_worktree",
                    return_value=worktree / "runtime",
                ) as runtime_selector,
                patch.object(
                    runner,
                    "run_stage2_reconciliation_diagnostic_tool",
                    return_value=result,
                ) as run_tool,
                patch.object(runner, "assert_protected_main_unchanged"),
                patch.object(
                    runner,
                    "persist_stage2_reconciliation_diagnostic_checkpoint",
                    return_value="3" * 40,
                ) as persist,
            ):
                runner.run_read_only_stage2_reconciliation_diagnostic(
                    initial_control_state(),
                    req,
                    b"{}",
                    "1" * 40,
                    CONTROL,
                    MAIN,
                )
        run_tool.assert_called_once()
        runtime_selector.assert_called_once_with(MAIN)
        self.assertEqual(run_tool.call_args.kwargs["tool_repo"], worktree / "runtime")
        persist.assert_called_once()

    def test_fresh_verifier_replays_exact_trace_and_marks_equivalence(self):
        trace = {
            "diagnostic_status": "PASS",
            "execution_status": "RECONCILIATION_BLOCKED",
            "execution_error": "partial",
            "partial_location_classification": "PREEXISTING_PERSISTED",
            "integrity": {"status": "FAIL"},
            "decision_order": [{"decision_id": "SITE-1"}],
            "mutations": [],
            "site_sync_events": [],
        }
        result = {
            "runtime_tool_sha256": {"tool": "hash"},
            "trace_sha256": "9" * 64,
            "trace": trace,
            "tracked_mutation_proof": {"tracked_stage2_mutation": "NONE"},
        }
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_RECONCILIATION_DIAGNOSTIC_CHECKPOINT",
            "request_id": "diagnostic-001",
            "request_sha256": "",
            "school_key": SCHOOL,
            "protected_main_sha": MAIN,
            "runtime_tool_sha256": {"tool": "hash"},
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "target_tree_sha": TREE,
            "stage2_proposal_checkpoint_sha256": CHECKPOINT_SHA,
            "integration_freeze_sha256": FREEZE_SHA,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
            "recommendation_map_sha256": MAP_SHA,
            "canonical_game_id": GAME,
            "trace_sha256": "9" * 64,
            "diagnostic_status": "PASS",
            "execution_status": "RECONCILIATION_BLOCKED",
            "execution_error": "partial",
            "partial_location_classification": "PREEXISTING_PERSISTED",
            "integrity": {"status": "FAIL"},
            "decision_count": 1,
            "mutation_count": 0,
            "site_sync_count": 0,
        }
        request_bytes = b'{"request_id":"diagnostic-001"}\n'
        manifest["request_sha256"] = sha(request_bytes)
        manifest_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        checkpoint_path = (
            ".remote-implementation/checkpoints/example-school/"
            "diagnostic-001/checkpoint-manifest.json"
        )
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
            "request_id": "diagnostic-001",
            "checkpoint_manifest_path": checkpoint_path,
            "checkpoint_manifest_sha256": sha(manifest_bytes),
            "target_sha": TARGET,
            "canonical_game_id": GAME,
            "trace_sha256": "9" * 64,
            "fresh_runner_verification": "PENDING",
        }
        mapping = {
            checkpoint_path: manifest_bytes,
            (
                Path(checkpoint_path).parent / "request.json"
            ).as_posix(): request_bytes,
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
                    "verify_stage2_diagnostic_authority",
                    return_value={
                        "freeze_bytes": b"freeze",
                        "map_bytes": b"map",
                        "plan_bytes": b"plan",
                        "review_bytes": b"review",
                        "target_tree_sha": TREE,
                    },
                ),
                patch.object(verifier, "remote_head", return_value=TARGET),
                patch.object(
                    verifier,
                    "add_existing_onboarding_worktree",
                    return_value=worktree,
                ),
                patch.object(
                    verifier,
                    "add_exact_protected_main_runtime_worktree",
                    return_value=worktree / "runtime",
                ),
                patch.object(verifier, "git", return_value=cp),
                patch.object(
                    verifier,
                    "run_stage2_reconciliation_diagnostic_tool",
                    return_value=result,
                ),
                patch.object(verifier, "read_json", return_value=state),
                patch.object(verifier, "validate_control_state"),
                patch.object(verifier, "write_json"),
                patch.object(verifier, "commit_control", return_value="e" * 40),
            ):
                self.assertEqual(
                    verifier.verify_stage2_reconciliation_diagnostic(
                        MAIN,
                        CONTROL,
                        state,
                    ),
                    0,
                )

    def test_fresh_verifier_dispatches_diagnostic_operation(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_RECONCILIATION_DIAGNOSTIC,
            "request_id": "diagnostic-001",
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
                "verify_stage2_reconciliation_diagnostic",
                return_value=0,
            ) as verify,
        ):
            self.assertEqual(verifier.main(), 0)
        verify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
