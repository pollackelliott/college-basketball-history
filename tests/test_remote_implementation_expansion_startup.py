"""Regression coverage for repository-owned All-History expansion startup."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from all_history_expansion_integration import PACKAGE_FILES, STAGE1_REPORT  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    initial_control_state,
    validate_request,
)
from remote_implementation_expansion_startup import (  # noqa: E402
    STARTUP_KIND,
    Stop,
    build_phase0_request,
    build_stage1_proof,
    preserve_preintegration_diagnostics,
    require_startup_idle_control,
    validate_startup_intent,
)


def startup_intent() -> dict:
    freeze = "1" * 64
    return {
        "schema_version": 1,
        "kind": STARTUP_KIND,
        "startup_id": "example-expansion-startup-0001",
        "phase0_request_id": "example-expansion-phase0-0001",
        "school_key": "example",
        "expected_protected_main_sha": "2" * 40,
        "target_branch": "data/example-onboarding",
        "target_sha": "3" * 40,
        "research_freeze_sha256": freeze,
        "expansion_research_checkpoint": {
            "sha256": freeze,
            "research_base_sha": "4" * 40,
            "transport": {
                "kind": "git_base64_parts",
                "commit_sha": "5" * 40,
                "path_prefix": (
                    ".remote-implementation/transports/"
                    "example/expansion-startup-0001/"
                ),
                "part_count": 3,
            },
        },
        "creation_provenance": {
            "origin": "unit test",
            "authorization": (
                "Owner Proceed authorizes the initial expansion "
                "Implementation phase."
            ),
        },
    }


def recovered_idle_state(disposition: str) -> dict:
    state = initial_control_state()
    failed_request = "example-expansion-phase0-failed"
    recovery_request = "example-expansion-phase0-recover"
    classification = {
        "ABANDONED_NOT_ATTEMPTED": "NOT_ATTEMPTED",
        "ABANDONED_PREPARED_NOT_PUBLISHED": "PREPARED_NOT_PUBLISHED",
    }[disposition]
    state["transaction_state"] = disposition
    state["abandoned_request_ids"] = [failed_request]
    state["consumed_request_ids"] = [recovery_request]
    state["last_operation"] = {
        "operation": "RECOVER",
        "recovered_request_id": failed_request,
        "disposition": disposition,
        "recovery_manifest": {
            "mutation_classification": classification,
            "recovered_request_id": failed_request,
            "request_id": recovery_request,
        },
    }
    return state


class ExpansionStartupIdleControlTests(unittest.TestCase):
    def test_initial_idle_control_is_eligible(self):
        require_startup_idle_control(initial_control_state())

    def test_not_attempted_recovery_terminal_is_eligible(self):
        require_startup_idle_control(
            recovered_idle_state("ABANDONED_NOT_ATTEMPTED")
        )

    def test_prepared_unpublished_recovery_terminal_is_eligible(self):
        require_startup_idle_control(
            recovered_idle_state("ABANDONED_PREPARED_NOT_PUBLISHED")
        )


class ExpansionStartupIntentTests(unittest.TestCase):
    def test_valid_intent_is_school_agnostic(self):
        result = validate_startup_intent(startup_intent())
        self.assertEqual(result["school_key"], "example")
        self.assertEqual(
            result["phase0_request_id"],
            "example-expansion-phase0-0001",
        )

    def test_target_branch_is_exact_school_onboarding_predecessor(self):
        value = startup_intent()
        value["target_branch"] = "data/other-onboarding"
        with self.assertRaisesRegex(
            Stop,
            "EXPANSION_STARTUP_TARGET_BRANCH_INVALID",
        ):
            validate_startup_intent(value)

    def test_freeze_transport_is_hash_bound(self):
        value = startup_intent()
        value["expansion_research_checkpoint"]["sha256"] = "9" * 64
        with self.assertRaisesRegex(
            Stop,
            "EXPANSION_STARTUP_FREEZE_BINDING_MISMATCH",
        ):
            validate_startup_intent(value)


class ExpansionStartupProofTests(unittest.TestCase):
    def test_stage1_proof_uses_generic_permanent_contract(self):
        report = {
            "canonical_identity_census": {
                "counts": {
                    "REUSE_CANONICAL": 8,
                    "PROVISIONAL_NEW": 101,
                    "IDENTITY_REVIEW_BLOCKER": 0,
                },
            },
            "global_venue_reconciliation": {
                "counts": {
                    "GLOBAL_VENUE_REUSE": 2,
                    "GLOBAL_VENUE_PROVISIONAL_NEW": 0,
                    "GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER": 0,
                },
            },
            "census": {
                "opponent_support_actions": {
                    "NEW_SUPPLEMENTAL": 1,
                    "REUSE_INHERITED": 2,
                    "EXTEND_INHERITED": 3,
                },
                "venue_support_actions": {
                    "NEW_SUPPLEMENTAL": 0,
                    "REUSE_INHERITED": 1,
                    "EXTEND_INHERITED": 1,
                },
            },
            "blockers": [
                {
                    "class": (
                        "DOWNSTREAM_EXPANSION_INTEGRATION_FREEZE_"
                        "AND_GUARDED_PHASE0_MISSING"
                    ),
                },
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for index, name in enumerate((*PACKAGE_FILES, STAGE1_REPORT)):
                (root / name).write_text(
                    f"{name}:{index}\n",
                    encoding="utf-8",
                )
            proof = build_stage1_proof(
                report,
                root,
                protected_main_sha="2" * 40,
                research_base_sha="4" * 40,
                freeze_zip_sha256="1" * 64,
            )
        self.assertEqual(
            proof["status"],
            "INDEPENDENTLY_REPRODUCED_READ_ONLY_STAGE1",
        )
        self.assertEqual(
            set(proof["candidate_sha256"]),
            set((*PACKAGE_FILES, STAGE1_REPORT)),
        )
        self.assertFalse(proof["integration_freeze_authorized"])
        self.assertEqual(
            proof["identity_counts"]["PROVISIONAL_NEW"],
            101,
        )

    def test_child_request_is_ordinary_guarded_expansion_phase0(self):
        intent = startup_intent()
        request = build_phase0_request(
            intent,
            predecessor_commit="6" * 40,
            predecessor_state_sha256="7" * 64,
            proof_path=(
                ".remote-implementation/startups/example/"
                "example-expansion-startup-0001/"
                "stage1-independent-proof.json"
            ),
            proof_sha256="8" * 64,
            integration_freeze_sha256="9" * 64,
            venue_reconciliation_ref=None,
        )
        validate_request(request)
        self.assertEqual(request["operation"], "EXPANSION_PHASE0")
        self.assertTrue(request["authority"]["expansion_phase0"])
        self.assertFalse(request["authority"]["phase0"])
        self.assertFalse(request["authority"]["owner_gate_1"])
        self.assertFalse(request["authority"]["owner_gate_2"])

    def test_optional_venue_reconciliation_is_carried_not_invented(self):
        intent = startup_intent()
        request = build_phase0_request(
            intent,
            predecessor_commit="6" * 40,
            predecessor_state_sha256="7" * 64,
            proof_path=".remote-implementation/startups/example/proof.json",
            proof_sha256="8" * 64,
            integration_freeze_sha256="9" * 64,
            venue_reconciliation_ref={
                "path": (
                    ".remote-implementation/startups/example/"
                    "venue-reconciliation.json"
                ),
                "sha256": "a" * 64,
            },
        )
        validate_request(request)
        self.assertEqual(
            request["venue_reconciliation"]["sha256"],
            "a" * 64,
        )


class ExpansionStartupDiagnosticTests(unittest.TestCase):
    def test_stage1_diagnostics_survive_later_integration_failure(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            stage1 = root / "stage1"
            stage1.mkdir()
            report = stage1 / STAGE1_REPORT
            report.write_text(
                '{"blockers":[{"class":"EXAMPLE_BLOCKER"}]}\n',
                encoding="utf-8",
            )
            proof = root / "stage1-independent-proof.json"
            proof.write_text(
                '{"status":"INDEPENDENTLY_REPRODUCED_READ_ONLY_STAGE1"}\n',
                encoding="utf-8",
            )
            diag = root / "diag"
            with patch(
                "remote_implementation_expansion_startup.DIAG",
                diag,
            ):
                preserve_preintegration_diagnostics(stage1, proof)

            self.assertEqual(
                (diag / "stage1-reconciliation.json").read_bytes(),
                report.read_bytes(),
            )
            self.assertEqual(
                (diag / "stage1-independent-proof.json").read_bytes(),
                proof.read_bytes(),
            )

    def test_diagnostics_are_preserved_before_integration_freeze(self):
        tool = (
            ROOT
            / "tools"
            / "remote_implementation_expansion_startup.py"
        ).read_text(encoding="utf-8")
        preserve_call = (
            "preserve_preintegration_diagnostics(stage1_b, proof_path)"
        )
        integration_call = (
            'str(\n'
            '            ROOT\n'
            '            / "tools"\n'
            '            / "all_history_expansion_integration.py"\n'
            '        )'
        )
        self.assertIn(preserve_call, tool)
        self.assertIn(integration_call, tool)
        self.assertLess(
            tool.index(preserve_call),
            tool.index(integration_call),
        )


class ExpansionStartupWorkflowContractTests(unittest.TestCase):
    def test_control_workflow_detects_and_runs_generic_startup(self):
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "remote-implementation.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("has_expansion_startup", workflow)
        self.assertIn(
            "remote_implementation_expansion_startup.py",
            workflow,
        )
        self.assertIn(
            ".remote-implementation/expansion-startup.json",
            workflow,
        )

    def test_permanent_startup_surface_is_not_vcu_specific(self):
        tool = (
            ROOT
            / "tools"
            / "remote_implementation_expansion_startup.py"
        ).read_text(encoding="utf-8").lower()
        workflow = (
            ROOT
            / ".github"
            / "workflows"
            / "remote-implementation.yml"
        ).read_text(encoding="utf-8").lower()
        self.assertNotIn("vcu", tool)
        self.assertNotIn("vcu-expansion-phase0-prepare", workflow)


if __name__ == "__main__":
    unittest.main()
