import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remote_implementation_expansion_rebootstrap import (  # noqa: E402
    PRE_GATE1_OPERATIONS,
    SUCCESSOR_KIND_DISPLAY,
    SUCCESSOR_KIND_PHASE0,
    SUCCESSOR_KIND_REFRESH,
    create_superseded_bundle,
    require_pre_gate_control_boundary,
    successor_verification_contract,
    verify_superseded_bundle,
)
from remote_implementation_control import (  # noqa: E402
    OP_EXPANSION_PHASE0,
    OP_STAGE2_CURRENT_MAIN_REFRESH,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_STAGE2_PROPOSAL_REHEARSAL,
    RemoteImplementationError,
    initial_control_state,
)


class ExpansionRebootstrapTests(unittest.TestCase):
    def test_successor_verification_contracts_are_exact(self):
        self.assertEqual(
            successor_verification_contract(SUCCESSOR_KIND_PHASE0),
            (
                OP_EXPANSION_PHASE0,
                "REMOTE_IMPLEMENTATION_FRESH_VERIFICATION",
                "remote_phase0_equivalence",
            ),
        )
        self.assertEqual(
            successor_verification_contract(SUCCESSOR_KIND_DISPLAY),
            (
                OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
                "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_VERIFICATION",
                "remote_stage2_opponent_display_equivalence",
            ),
        )
        self.assertEqual(
            successor_verification_contract(SUCCESSOR_KIND_REFRESH),
            (
                OP_STAGE2_CURRENT_MAIN_REFRESH,
                "REMOTE_IMPLEMENTATION_STAGE2_CURRENT_MAIN_REFRESH_VERIFICATION",
                "remote_stage2_current_main_refresh_equivalence",
            ),
        )
        with self.assertRaises(RemoteImplementationError):
            successor_verification_contract("UNKNOWN_SUCCESSOR")

    def test_gate1_and_later_are_not_rebootstrap_boundaries(self):
        self.assertIn(OP_STAGE2_PROPOSAL_REHEARSAL, PRE_GATE1_OPERATIONS)
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": "STAGE2_GATE1_FILL",
            "fresh_runner_verification": "PASS",
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "target_sha": "b" * 40,
            "protected_main_sha": "a" * 40,
        }
        request = {
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "target_sha": "b" * 40,
        }
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_REBOOTSTRAP_NOT_PRE_GATE1",
        ):
            require_pre_gate_control_boundary(
                state,
                request,
                "a" * 40,
            )

    def test_requires_fresh_verified_same_school_target(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_PROPOSAL_REHEARSAL,
            "fresh_runner_verification": "PASS",
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "target_sha": "b" * 40,
            "protected_main_sha": "a" * 40,
        }
        request = {
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "target_sha": "b" * 40,
        }
        self.assertEqual(
            require_pre_gate_control_boundary(
                state,
                request,
                "a" * 40,
            )["operation"],
            OP_STAGE2_PROPOSAL_REHEARSAL,
        )
        state["last_operation"]["fresh_runner_verification"] = "PENDING"
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "PREDECESSOR_NOT_FRESH_VERIFIED",
        ):
            require_pre_gate_control_boundary(
                state,
                request,
                "a" * 40,
            )

    def test_bundle_preserves_target_only_commit(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "test"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "test@example.com"],
                check=True,
            )
            (repo / "base.txt").write_text("base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "base.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-q", "-m", "base"],
                check=True,
            )
            main = subprocess.check_output(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                text=True,
            ).strip()
            subprocess.run(
                ["git", "-C", str(repo), "switch", "-q", "-c", "target"],
                check=True,
            )
            (repo / "target.txt").write_text("target\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "target.txt"], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-q", "-m", "target"],
                check=True,
            )
            target = subprocess.check_output(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                text=True,
            ).strip()

            bundle_path = Path(temporary) / "superseded.bundle"
            proof = create_superseded_bundle(
                repo=repo,
                school_key="example-school",
                target_sha=target,
                protected_main_sha=main,
                bundle_path=bundle_path,
            )
            self.assertEqual(proof["target_sha"], target)
            self.assertEqual(proof["merge_base_sha"], main)
            self.assertTrue(bundle_path.is_file())
            self.assertEqual(
                verify_superseded_bundle(
                    bundle_path,
                    expected_sha256=proof["bundle_sha256"],
                    expected_target_sha=target,
                    expected_ref=proof["bundle_ref"],
                    expected_merge_base_sha=main,
                    repo=repo,
                )["target_sha"],
                target,
            )


if __name__ == "__main__":
    unittest.main()
