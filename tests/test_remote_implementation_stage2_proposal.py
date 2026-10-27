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
import remote_implementation_stage2_proposal as proposal  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_PROPOSAL_REHEARSAL,
    canonical_json_bytes,
    initial_control_state,
)
from remote_implementation_io import Stop  # noqa: E402


SCHOOL = "example-school"
BRANCH = "data/example-school-onboarding"
TARGET = "a" * 40
TREE = "b" * 40
MAIN = "c" * 40
DECISION_SHA = proposal._decision_universe_sha256([{"decision_id": "SYNTHETIC-1"}])
SEMANTIC_SHA = "e" * 64


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class RemoteStage2ProposalTests(unittest.TestCase):
    def authority_fixture(self):
        freeze = canonical_json_bytes(
            {
                "status": "INTEGRATION_FROZEN",
                "school_key": SCHOOL,
                "source_game_semantic_guard": {
                    "snapshot_sha256": SEMANTIC_SHA,
                },
            }
        )
        freeze_sha = sha(freeze)
        writeahead_path = (
            ".remote-implementation/writeahead/example-school/repair/"
            "writeahead-manifest.json"
        )
        writeahead = canonical_json_bytes(
            {
                "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
                "school_key": SCHOOL,
                "target_branch": BRANCH,
                "integration_freeze_sha256": freeze_sha,
                "semantic_snapshot_sha256": SEMANTIC_SHA,
                "sidecars": {"integration-freeze.json": freeze_sha},
            }
        )
        successor = canonical_json_bytes(
            {
                "kind": "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
                "school_key": SCHOOL,
                "target_branch": BRANCH,
                "actual_published_target_sha": TARGET,
                "prepared_tree_sha": TREE,
                "integration_freeze_sha256": freeze_sha,
                "semantic_snapshot_sha256": SEMANTIC_SHA,
                "writeahead_manifest_path": writeahead_path,
                "writeahead_manifest_sha256": sha(writeahead),
                "post_repair_stage2": {
                    "stage2_status": "CAPABILITY_CENSUS_READY",
                    "blocker_count": 0,
                    "warning_count": 0,
                    "decision_universe_sha256": DECISION_SHA,
                },
            }
        )
        authority_path = (
            ".remote-implementation/successors/example-school/repair/"
            "successor-manifest.json"
        )
        request = {
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "stage2_authority": {
                "path": authority_path,
                "sha256": sha(successor),
            },
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": SEMANTIC_SHA,
            "decision_universe_sha256": DECISION_SHA,
        }
        freeze_path = (
            Path(writeahead_path).parent / "integration-freeze.json"
        ).as_posix()
        mapping = {
            authority_path: successor,
            writeahead_path: writeahead,
            freeze_path: freeze,
        }
        return request, mapping

    def test_exact_post_repair_authority_authenticates(self):
        request, mapping = self.authority_fixture()

        def fake_show(commit, path, **kwargs):
            return mapping[path]

        with patch.object(proposal, "git_show_bytes", side_effect=fake_show):
            result = proposal.verify_stage2_proposal_authority(
                request,
                "f" * 40,
            )
        self.assertEqual(
            result["authority_kind"],
            "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
        )
        self.assertEqual(result["target_tree_sha"], TREE)
        self.assertEqual(sha(result["freeze_bytes"]), request["integration_freeze_sha256"])

    def test_stale_decision_universe_is_refused(self):
        request, mapping = self.authority_fixture()
        request["decision_universe_sha256"] = "0" * 64

        with patch.object(
            proposal,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_PROPOSAL_AUTHORITY_DECISION_UNIVERSE_MISMATCH",
            ):
                proposal.verify_stage2_proposal_authority(request, "f" * 40)

    def test_tampered_integration_freeze_is_refused(self):
        request, mapping = self.authority_fixture()
        freeze_path = next(path for path in mapping if path.endswith("integration-freeze.json"))
        mapping[freeze_path] = b'{"tampered":true}\n'

        with patch.object(
            proposal,
            "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            with self.assertRaisesRegex(
                Stop,
                "STAGE2_PROPOSAL_FREEZE_BYTES_MISMATCH",
            ):
                proposal.verify_stage2_proposal_authority(request, "f" * 40)

    def _run_fixture(self, *, status_name, exit_code, last_error=None, site=None):
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        map_path = root / "map.json"
        map_path.write_text(
            json.dumps({"decisions": {"SYNTHETIC-1": "KEEP_CANONICAL"}}) + "\n",
            encoding="utf-8",
        )
        output = root / ".onboarding" / SCHOOL
        output.mkdir(parents=True)
        permanent_status = {
            "status": status_name,
            "preflight": {
                "decision_count": 1,
                "decision_universe_sha256": DECISION_SHA,
            },
            "capability_census": {
                "path": f".onboarding/{SCHOOL}/implementation-stage2-capability-census.json",
                "status": "PASS" if status_name == "OWNER_GATE_1_READY" else "CENSUS_CAPTURED",
            },
        }
        if status_name == "OWNER_GATE_1_READY":
            permanent_status["recommendation_map"] = {
                "path": str(map_path),
                "sha256": sha(map_path.read_bytes()),
                "decision_count": 1,
                "action_counts": {"KEEP_CANONICAL": 1},
                "approved_plan_hash_preview": "preview-hash",
            }
            permanent_status["proposal_rehearsal"] = {
                "approved_plan_hash_preview": "preview-hash",
                "changed_path_count": 2,
                "action_counts": {"KEEP_CANONICAL": 1},
            }
        if last_error:
            permanent_status["last_error"] = last_error
        (output / "implementation-stage2-status.json").write_text(
            json.dumps(permanent_status) + "\n",
            encoding="utf-8",
        )
        (output / "implementation-stage2-capability-census.json").write_text(
            json.dumps(
                {
                    "status": permanent_status["capability_census"]["status"],
                    "topology_groups": (
                        [{"topology": "synthetic", "count": 1}]
                        if status_name == "BLOCKED"
                        else []
                    ),
                }
            )
            + "\n",
            encoding="utf-8",
        )
        (output / "plan.json").write_text(
            json.dumps({"decisions": [{"decision_id": "SYNTHETIC-1"}]}) + "\n",
            encoding="utf-8",
        )
        (output / "review.csv").write_text("decision_id\nSYNTHETIC-1\n", encoding="utf-8")
        (output / "review.md").write_text("# synthetic review\n", encoding="utf-8")
        if site is not None:
            (output / "last-rehearsal-site-gate.json").write_text(
                json.dumps(site) + "\n",
                encoding="utf-8",
            )
        clean = {"head_sha": TARGET, "tree_sha": TREE, "status": ""}
        cp = subprocess.CompletedProcess([], exit_code, stdout="synthetic")
        return temporary, root, map_path, clean, cp

    def test_successful_permanent_rehearsal_reaches_owner_gate_ready(self):
        temporary, root, map_path, clean, cp = self._run_fixture(
            status_name="OWNER_GATE_1_READY",
            exit_code=0,
        )
        self.addCleanup(temporary.cleanup)
        with (
            patch.object(proposal, "restore_integration_freeze"),
            patch.object(
                proposal,
                "tracked_worktree_state",
                side_effect=[clean, clean],
            ),
            patch.object(proposal, "run", return_value=cp),
        ):
            result = proposal.run_stage2_proposal_tool(
                root,
                SCHOOL,
                b"freeze",
                map_path,
                DECISION_SHA,
                root / "diag",
                tool_repo=ROOT,
            )
        self.assertEqual(result["stage2_status"], "OWNER_GATE_1_READY")
        self.assertEqual(
            result["status"]["proposal_rehearsal"]["approved_plan_hash_preview"],
            "preview-hash",
        )
        self.assertEqual(
            result["tracked_mutation_proof"]["tracked_stage2_mutation"],
            "NONE",
        )

    def test_accomplishment_action_vocabulary_bridge_is_exact(self):
        legacy = [
            {
                "decision_id": "ACCOMPLISHMENTS-EXAMPLE",
                "category": "accomplishments",
                "source_value": "{\"conference_regular_season_championships\":\"13\"}",
                "allowed_actions": [
                    "KEEP_UNDER_REVIEW",
                    "VERIFY_REFERENCE_VALUES",
                ],
            },
            {
                "decision_id": "PUBLICATION-EXAMPLE",
                "category": "publication",
                "source_value": "No",
                "allowed_actions": ["ENABLE_PUBLIC_PAGE", "KEEP_DISABLED"],
            },
        ]
        current = json.loads(json.dumps(legacy))
        current[0]["allowed_actions"].insert(0, "APPLY_ACCOMPLISHMENT_PATCH")
        legacy_sha = proposal._decision_universe_sha256(legacy)
        current_sha = proposal._decision_universe_sha256(current)

        result = proposal.accomplishment_action_compatibility(
            {"decisions": current},
            legacy_sha,
            current_sha,
        )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(
            result["kind"],
            "ACCOMPLISHMENT_ACTION_VOCABULARY_ADDITION",
        )
        self.assertEqual(result["legacy_compatible_sha256"], legacy_sha)
        self.assertEqual(result["runtime_decision_universe_sha256"], current_sha)

    def test_accomplishment_bridge_refuses_any_substantive_row_change(self):
        legacy = [
            {
                "decision_id": "ACCOMPLISHMENTS-EXAMPLE",
                "category": "accomplishments",
                "source_value": "{\"conference_regular_season_championships\":\"13\"}",
                "allowed_actions": [
                    "KEEP_UNDER_REVIEW",
                    "VERIFY_REFERENCE_VALUES",
                ],
            }
        ]
        current = json.loads(json.dumps(legacy))
        current[0]["allowed_actions"].insert(0, "APPLY_ACCOMPLISHMENT_PATCH")
        current[0]["source_value"] = (
            "{\"conference_regular_season_championships\":\"12\"}"
        )
        with self.assertRaisesRegex(
            Stop,
            "STAGE2_PROPOSAL_DECISION_UNIVERSE_MISMATCH",
        ):
            proposal.accomplishment_action_compatibility(
                {"decisions": current},
                proposal._decision_universe_sha256(legacy),
                proposal._decision_universe_sha256(current),
            )

    def test_permanent_rehearsal_accepts_only_accomplishment_action_hash_bridge(self):
        temporary, root, map_path, clean, cp = self._run_fixture(
            status_name="OWNER_GATE_1_READY",
            exit_code=0,
        )
        self.addCleanup(temporary.cleanup)
        legacy = [
            {
                "decision_id": "ACCOMPLISHMENTS-EXAMPLE",
                "category": "accomplishments",
                "source_value": "{\"conference_regular_season_championships\":\"13\"}",
                "allowed_actions": [
                    "KEEP_UNDER_REVIEW",
                    "VERIFY_REFERENCE_VALUES",
                ],
            }
        ]
        current = json.loads(json.dumps(legacy))
        current[0]["allowed_actions"].insert(0, "APPLY_ACCOMPLISHMENT_PATCH")
        legacy_sha = proposal._decision_universe_sha256(legacy)
        current_sha = proposal._decision_universe_sha256(current)
        output = root / ".onboarding" / SCHOOL
        status_path = output / "implementation-stage2-status.json"
        status = json.loads(status_path.read_text(encoding="utf-8"))
        status["preflight"]["decision_universe_sha256"] = current_sha
        status_path.write_text(json.dumps(status) + "\n", encoding="utf-8")
        (output / "plan.json").write_text(
            json.dumps({"decisions": current}) + "\n",
            encoding="utf-8",
        )

        with (
            patch.object(proposal, "restore_integration_freeze"),
            patch.object(
                proposal,
                "tracked_worktree_state",
                side_effect=[clean, clean],
            ),
            patch.object(proposal, "run", return_value=cp),
        ):
            result = proposal.run_stage2_proposal_tool(
                root,
                SCHOOL,
                b"freeze",
                map_path,
                legacy_sha,
                root / "diag",
                tool_repo=ROOT,
            )
        self.assertEqual(
            result["decision_universe_compatibility"]["kind"],
            "ACCOMPLISHMENT_ACTION_VOCABULARY_ADDITION",
        )
        self.assertEqual(
            result["decision_universe_compatibility"][
                "runtime_decision_universe_sha256"
            ],
            current_sha,
        )

    def test_incomplete_map_blocked_result_is_preserved(self):
        temporary, root, map_path, clean, cp = self._run_fixture(
            status_name="BLOCKED",
            exit_code=1,
            last_error="recommendation map is missing decision SYNTHETIC-1",
        )
        self.addCleanup(temporary.cleanup)
        with (
            patch.object(proposal, "restore_integration_freeze"),
            patch.object(
                proposal,
                "tracked_worktree_state",
                side_effect=[clean, clean],
            ),
            patch.object(proposal, "run", return_value=cp),
        ):
            result = proposal.run_stage2_proposal_tool(
                root,
                SCHOOL,
                b"freeze",
                map_path,
                DECISION_SHA,
                root / "diag",
                tool_repo=ROOT,
            )
        self.assertEqual(result["stage2_status"], "BLOCKED")
        self.assertIn("missing decision", result["status"]["last_error"])

    def test_invalid_action_blocked_result_is_preserved(self):
        temporary, root, map_path, clean, cp = self._run_fixture(
            status_name="BLOCKED",
            exit_code=1,
            last_error="invalid action for SYNTHETIC-1",
        )
        self.addCleanup(temporary.cleanup)
        with (
            patch.object(proposal, "restore_integration_freeze"),
            patch.object(
                proposal,
                "tracked_worktree_state",
                side_effect=[clean, clean],
            ),
            patch.object(proposal, "run", return_value=cp),
        ):
            result = proposal.run_stage2_proposal_tool(
                root,
                SCHOOL,
                b"freeze",
                map_path,
                DECISION_SHA,
                root / "diag",
                tool_repo=ROOT,
            )
        self.assertEqual(result["stage2_status"], "BLOCKED")
        self.assertIn("invalid action", result["status"]["last_error"])

    def test_site_diagnostic_is_captured(self):
        site = {
            "status": "FAIL",
            "counts": {"unaccounted_public_gap_rows": 2},
            "examples": {"unaccounted_public_gap_rows": ["SYNTHETIC-1"]},
        }
        temporary, root, map_path, clean, cp = self._run_fixture(
            status_name="BLOCKED",
            exit_code=1,
            last_error="implementation site completeness failed",
            site=site,
        )
        self.addCleanup(temporary.cleanup)
        with (
            patch.object(proposal, "restore_integration_freeze"),
            patch.object(
                proposal,
                "tracked_worktree_state",
                side_effect=[clean, clean],
            ),
            patch.object(proposal, "run", return_value=cp),
        ):
            result = proposal.run_stage2_proposal_tool(
                root,
                SCHOOL,
                b"freeze",
                map_path,
                DECISION_SHA,
                root / "diag",
                tool_repo=ROOT,
            )
        self.assertEqual(result["site_diagnostic"], site)

    def test_tracked_mutation_is_refused(self):
        temporary, root, map_path, clean, cp = self._run_fixture(
            status_name="OWNER_GATE_1_READY",
            exit_code=0,
        )
        self.addCleanup(temporary.cleanup)
        dirty = dict(clean)
        dirty["status"] = " M schools/example/source-games.csv\n"
        with (
            patch.object(proposal, "restore_integration_freeze"),
            patch.object(
                proposal,
                "tracked_worktree_state",
                side_effect=[clean, dirty],
            ),
            patch.object(proposal, "run", return_value=cp),
        ):
            with self.assertRaisesRegex(Stop, "TRACKED_STAGE2_MUTATION_DETECTED"):
                proposal.run_stage2_proposal_tool(
                    root,
                    SCHOOL,
                    b"freeze",
                    map_path,
                    DECISION_SHA,
                    root / "diag",
                    tool_repo=ROOT,
                )

    def test_changed_onboarding_sha_is_refused_before_acceptance(self):
        request = {
            "request_id": "proposal-001",
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
        }
        with (
            patch.object(
                runner,
                "verify_stage2_proposal_authority",
                return_value={"freeze_bytes": b"x", "target_tree_sha": TREE},
            ),
            patch.object(runner, "remote_head", return_value="f" * 40),
        ):
            with self.assertRaisesRegex(Stop, "STAGE2_PROPOSAL_TARGET_HEAD_MISMATCH"):
                runner.run_read_only_stage2_proposal(
                    initial_control_state(),
                    request,
                    b"{}",
                    "1" * 40,
                    "2" * 40,
                    MAIN,
                )

    def test_runner_passes_authenticated_main_runtime_to_proposal(self):
        request = {
            "request_id": "proposal-001",
            "school_key": SCHOOL,
            "operation": OP_STAGE2_PROPOSAL_REHEARSAL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "recommendation_map": {"path": "map.json", "sha256": "9" * 64},
            "decision_universe_sha256": DECISION_SHA,
        }
        authority = {"freeze_bytes": b"x", "target_tree_sha": TREE}
        result = {
            "stage2_status": "BLOCKED",
            "tracked_mutation_proof": {"after_tree_sha": TREE},
        }
        cp = subprocess.CompletedProcess([], 0, stdout=TREE + "\n")
        with tempfile.TemporaryDirectory() as directory:
            worktree = Path(directory)
            map_path = worktree / "recommendation-map.json"
            map_path.write_bytes(b"{}\n")
            with (
                patch.object(
                    runner,
                    "verify_stage2_proposal_authority",
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
                patch.object(runner, "commit_control", return_value="3" * 40),
                patch.object(
                    runner,
                    "materialize_payload",
                    return_value=map_path,
                ),
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
                    "run_stage2_proposal_tool",
                    return_value=result,
                ) as run_tool,
                patch.object(runner, "assert_protected_main_unchanged"),
                patch.object(
                    runner,
                    "persist_stage2_proposal_checkpoint",
                    return_value="4" * 40,
                ),
            ):
                runner.run_read_only_stage2_proposal(
                    initial_control_state(),
                    request,
                    b"{}",
                    "1" * 40,
                    "2" * 40,
                    MAIN,
                )
        runtime_selector.assert_called_once_with(MAIN)
        self.assertEqual(run_tool.call_args.kwargs["tool_repo"], worktree / "runtime")

    def test_map_sha_mismatch_stops_at_payload_transport(self):
        request = {
            "request_id": "proposal-001",
            "school_key": SCHOOL,
            "operation": OP_STAGE2_PROPOSAL_REHEARSAL,
            "target_branch": BRANCH,
            "target_sha": TARGET,
            "recommendation_map": {"path": "map.json", "sha256": "0" * 64},
        }
        authority = {"freeze_bytes": b"x", "target_tree_sha": TREE}
        with (
            patch.object(
                runner,
                "verify_stage2_proposal_authority",
                return_value=authority,
            ),
            patch.object(runner, "remote_head", return_value=TARGET),
            patch.object(runner, "begin_request", return_value=initial_control_state()),
            patch.object(runner, "write_json"),
            patch.object(runner, "archive_request", return_value=Path("archive")),
            patch.object(runner, "commit_control", return_value="3" * 40),
            patch.object(
                runner,
                "materialize_payload",
                side_effect=Stop("REQUEST_PAYLOAD_HASH_MISMATCH"),
            ),
        ):
            with self.assertRaisesRegex(Stop, "REQUEST_PAYLOAD_HASH_MISMATCH"):
                runner.run_read_only_stage2_proposal(
                    initial_control_state(),
                    request,
                    b"{}",
                    "1" * 40,
                    "2" * 40,
                    MAIN,
                )

    def test_fresh_verifier_dispatches_proposal_operation(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_PROPOSAL_REHEARSAL,
            "request_id": "proposal-001",
        }
        with (
            patch.object(verifier, "configure_git"),
            patch.object(
                verifier,
                "fetch_operational_refs",
                return_value=(MAIN, "3" * 40),
            ),
            patch.object(verifier, "git_show_json", return_value=state),
            patch.object(
                verifier,
                "verify_stage2_proposal_rehearsal",
                return_value=0,
            ) as verify,
        ):
            self.assertEqual(verifier.main(), 0)
        verify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
