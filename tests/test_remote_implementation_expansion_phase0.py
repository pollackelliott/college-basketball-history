"""Remote control-plane validation for guarded ALL_HISTORY_EXPANSION Phase 0."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from remote_implementation_control import (
    OP_EXPANSION_PHASE0,
    RemoteImplementationError,
    validate_request,
)
from remote_implementation_expansion_phase0 import (
    Stop,
    _target_predecessor_authority,
    _verification_bound_main,
)


def expansion_request() -> dict:
    false_flags = {
        "owner_gate_1": False,
        "owner_gate_2": False,
        "phase0": False,
        "phase0_scope_supersession": False,
        "recovery": False,
        "release": False,
        "release_gate2_approval": False,
        "release_preview_verify": False,
        "release_production_proof": False,
        "release_readiness": False,
        "stage2_census": False,
        "stage2_current_main_refresh": False,
        "stage2_gate1_fill": False,
        "stage2_gate1_seal": False,
        "stage2_opponent_display_normalize": False,
        "stage2_preseal_rehearsal": False,
        "stage2_proposal_rehearsal": False,
        "stage2_reconciliation_diagnostic": False,
        "stage2_sealed_apply": False,
        "venue_identity_maintenance": False,
    }
    false_flags["expansion_phase0"] = True
    research_sha = "4" * 64
    proof_sha = "5" * 64
    return {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": "example-expansion-phase0-0001",
        "school_key": "example",
        "operation": OP_EXPANSION_PHASE0,
        "previous_control_state_commit": "1" * 40,
        "previous_control_state_sha256": "2" * 64,
        "expected_protected_main_sha": "3" * 40,
        "target_branch": "data/example-onboarding",
        "target_sha": "6" * 40,
        "research_freeze_sha256": research_sha,
        "stage1_independent_proof_sha256": proof_sha,
        "integration_freeze_sha256": "7" * 64,
        "expansion_research_checkpoint": {
            "sha256": research_sha,
            "research_base_sha": "8" * 40,
            "transport": {
                "kind": "git_base64_parts",
                "commit_sha": "9" * 40,
                "path_prefix": ".transport/example-expansion/",
                "part_count": 3,
            },
        },
        "stage1_independent_proof": {
            "path": ".remote-implementation/payloads/example/stage1-proof.json",
            "sha256": proof_sha,
        },
        "creation_provenance": {
            "origin": "unit test",
            "authorization": "bounded generic expansion Phase 0 tooling test",
        },
        "authority": false_flags,
    }


class ExpansionFreshVerificationRegressionTests(unittest.TestCase):
    def test_live_predecessor_movement_still_fails_closed(self):
        request = expansion_request()
        with patch(
            "remote_implementation_expansion_phase0.remote_head",
            return_value="a" * 40,
        ):
            with self.assertRaisesRegex(
                Stop,
                "EXPANSION_PHASE0_TARGET_PREDECESSOR_CHANGED",
            ):
                _target_predecessor_authority(
                    request,
                    request["expected_protected_main_sha"],
                )

    def test_published_successor_authenticates_ref_but_reconstructs_predecessor(self):
        request = expansion_request()
        successor = "a" * 40
        with patch(
            "remote_implementation_expansion_phase0.remote_head",
            return_value=successor,
        ), patch(
            "remote_implementation_expansion_phase0.git",
            return_value=SimpleNamespace(returncode=0),
        ) as git_mock:
            target, ancestor = _target_predecessor_authority(
                request,
                request["expected_protected_main_sha"],
                authenticated_published_target_sha=successor,
            )
        self.assertEqual(target, request["target_sha"])
        self.assertTrue(ancestor)
        git_mock.assert_called_once_with(
            "merge-base",
            "--is-ancestor",
            request["target_sha"],
            request["expected_protected_main_sha"],
            cwd=git_mock.call_args.kwargs["cwd"],
            check=False,
        )

    def test_wrong_published_successor_still_fails_closed(self):
        request = expansion_request()
        with patch(
            "remote_implementation_expansion_phase0.remote_head",
            return_value="b" * 40,
        ):
            with self.assertRaisesRegex(
                Stop,
                "EXPANSION_PHASE0_PUBLISHED_TARGET_CHANGED",
            ):
                _target_predecessor_authority(
                    request,
                    request["expected_protected_main_sha"],
                    authenticated_published_target_sha="a" * 40,
                )

    def test_verification_preserves_bound_main_after_linear_runtime_advance(self):
        bound = "3" * 40
        observed = "4" * 40
        with patch(
            "remote_implementation_expansion_phase0.git",
            return_value=SimpleNamespace(returncode=0),
        ):
            self.assertEqual(
                _verification_bound_main(
                    {"protected_main_sha": bound},
                    observed,
                ),
                bound,
            )

    def test_verification_rejects_nonancestor_runtime_advance(self):
        with patch(
            "remote_implementation_expansion_phase0.git",
            return_value=SimpleNamespace(returncode=1),
        ):
            with self.assertRaisesRegex(
                Stop,
                "EXPANSION_PHASE0_FRESH_BOUND_MAIN_NOT_ANCESTOR",
            ):
                _verification_bound_main(
                    {"protected_main_sha": "3" * 40},
                    "4" * 40,
                )


class ExpansionRemoteRequestValidationTests(unittest.TestCase):
    def test_exact_expansion_request_is_supported(self):
        validate_request(expansion_request())

    def test_expansion_accepts_hash_bound_venue_reconciliation_payload(self):
        request = expansion_request()
        request["venue_reconciliation"] = {
            "path": ".remote-implementation/payloads/example/venue-reconciliation.json",
            "sha256": "a" * 64,
        }
        validate_request(request)

    def test_expansion_rejects_malformed_venue_reconciliation_payload(self):
        request = expansion_request()
        request["venue_reconciliation"] = {
            "path": ".remote-implementation/payloads/example/venue-reconciliation.json",
            "sha256": "not-a-sha",
        }
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "REQUEST_VENUE_RECONCILIATION_SHA_INVALID",
        ):
            validate_request(request)

    def test_expansion_requires_explicit_expansion_authority(self):
        request = expansion_request()
        request["authority"]["expansion_phase0"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_PHASE0_REQUEST_AUTHORITY_REQUIRED",
        ):
            validate_request(request)

    def test_expansion_forbids_ordinary_phase0_authority(self):
        request = expansion_request()
        request["authority"]["phase0"] = True
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_PHASE0_ORDINARY_PHASE0_AUTHORITY_FORBIDDEN",
        ):
            validate_request(request)

    def test_expansion_requires_existing_target_predecessor_binding(self):
        request = expansion_request()
        request["target_sha"] = ""
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_PHASE0_TARGET_SHA_INVALID",
        ):
            validate_request(request)

    def test_expansion_research_and_proof_hashes_are_bound(self):
        request = expansion_request()
        request["research_freeze_sha256"] = "a" * 64
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_PHASE0_RESEARCH_FREEZE_BINDING_MISMATCH",
        ):
            validate_request(request)
        request = expansion_request()
        request["stage1_independent_proof_sha256"] = "b" * 64
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_PHASE0_STAGE1_PROOF_BINDING_MISMATCH",
        ):
            validate_request(request)

    def test_expansion_cannot_smuggle_gate_or_stage2_authority(self):
        for flag in ("owner_gate_1", "stage2_census", "release"):
            request = expansion_request()
            request["authority"][flag] = True
            with self.subTest(flag=flag):
                with self.assertRaises(RemoteImplementationError):
                    validate_request(request)


if __name__ == "__main__":
    unittest.main()
