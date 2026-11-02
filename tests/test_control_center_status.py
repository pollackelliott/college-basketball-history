import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import control_center_status as status  # noqa: E402


class ControlCenterStatusTests(unittest.TestCase):
    def test_parse_ls_remote(self):
        rows = status._parse_ls_remote(
            "abc123\trefs/heads/main\n"
            "def456\trefs/heads/control/remote-implementation\n"
        )
        self.assertEqual(
            rows,
            [
                ("abc123", "refs/heads/main"),
                ("def456", "refs/heads/control/remote-implementation"),
            ],
        )

    def test_git_wrapper_refuses_mutating_subcommands_before_execution(self):
        with patch.object(status.subprocess, "run") as run:
            with self.assertRaisesRegex(ValueError, "Refusing non-read-only"):
                status._git(ROOT, "fetch", "origin", "main")
            run.assert_not_called()

    def test_control_summary_is_compact_and_preserves_authority_fields(self):
        summary = status._control_summary(
            {
                "current_sequence": 225,
                "lifecycle_state": "IDLE",
                "transaction_state": "COMPLETE",
                "active_request_id": None,
                "active_school_key": None,
                "active_lock_owner": None,
                "recovery_required": False,
                "last_operation": {
                    "operation": "STAGE2_CENSUS",
                    "request_id": "dayton-stage2-census-0003",
                    "school_key": "dayton",
                    "protected_main_sha": "main-sha",
                    "target_branch": "data/dayton-onboarding",
                    "target_sha": "target-sha",
                    "fresh_runner_verification": "PASS",
                    "stage2_status": "CAPABILITY_CENSUS_READY",
                    "checkpoint_manifest_path": "checkpoint.json",
                    "checkpoint_manifest_sha256": "manifest-sha",
                    "decision_universe_sha256": "universe-sha",
                    "irrelevant_large_field": ["do", "not", "copy"],
                },
            }
        )
        self.assertEqual(summary["current_sequence"], 225)
        self.assertEqual(summary["lifecycle_state"], "IDLE")
        self.assertFalse(summary["recovery_required"])
        self.assertEqual(
            summary["last_operation"]["request_id"],
            "dayton-stage2-census-0003",
        )
        self.assertNotIn("irrelevant_large_field", summary["last_operation"])

    @patch.object(status, "_remote_branch_names")
    @patch.object(status, "_cached_control_state")
    @patch.object(status, "_git")
    @patch.object(status, "_remote_ref_sha")
    def test_build_snapshot_does_not_promote_branch_names_to_status(
        self,
        remote_ref_sha,
        git,
        cached_control_state,
        remote_branch_names,
    ):
        remote_ref_sha.side_effect = ["main-sha", "control-sha"]
        git.side_effect = [
            Mock(stdout="local-head\n"),
            Mock(stdout=""),
        ]
        cached_control_state.return_value = (
            {
                "current_sequence": 5,
                "lifecycle_state": "IDLE",
                "transaction_state": "COMPLETE",
                "active_request_id": None,
                "active_school_key": None,
                "active_lock_owner": None,
                "recovery_required": False,
                "last_operation": {
                    "operation": "STAGE2_CENSUS",
                    "school_key": "example",
                },
            },
            "origin/control/remote-implementation",
        )
        remote_branch_names.side_effect = [
            ["data/example-onboarding"],
            [],
            ["research/example-stage3-checkpoint"],
        ]

        snapshot = status.build_snapshot(ROOT)

        self.assertEqual(snapshot["protected_main_sha"], "main-sha")
        self.assertEqual(snapshot["control_branch_sha"], "control-sha")
        self.assertEqual(
            snapshot["branch_locators"]["research"],
            ["research/example-stage3-checkpoint"],
        )
        self.assertNotIn("research_status", snapshot)
        self.assertIn(
            "Branch locators are not lifecycle authority.",
            snapshot["authority_notes"],
        )

    def test_human_output_marks_missing_exact_control_state(self):
        snapshot = {
            "protected_main_sha": "main",
            "control_branch_sha": "control",
            "local_head_sha": "local",
            "worktree_clean": True,
            "global_control": None,
            "branch_locators": {
                "onboarding": [],
                "correction": [],
                "research": [],
            },
        }
        rendered = status._human(snapshot)
        self.assertIn("EXACT_REMOTE_STATE_NOT_CACHED_LOCALLY", rendered)
        self.assertIn("branch locators are recovery hints only", rendered)


if __name__ == "__main__":
    unittest.main()
