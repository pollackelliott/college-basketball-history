"""Guarded presentation refresh admission: no owner gate or release bypass."""
from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from remote_implementation_control import (  # noqa: E402
    OP_RELEASE_PRESENTATION_REFRESH, REQUEST_KIND,
    RemoteImplementationError, begin_request, initial_control_state,
    validate_request,
)


def request():
    return {
        "schema_version": 1,
        "kind": REQUEST_KIND,
        "request_id": "example-presentation-0001",
        "school_key": "example-school",
        "operation": OP_RELEASE_PRESENTATION_REFRESH,
        "previous_control_state_commit": "a" * 40,
        "previous_control_state_sha256": "f" * 64,
        "expected_protected_main_sha": "b" * 40,
        "creation_provenance": {
            "origin": "existing Implementation lane",
            "authorization": "Control Center Issue #602 technical repair",
        },
        "target_branch": "data/example-school-onboarding",
        "target_sha": "c" * 40,
        "sealed_tree_sha": "d" * 40,
        "repair_main_sha": "b" * 40,
        "accepted_asset_blob_sha": "e" * 40,
        "stage2_apply_successor": {
            "path": ".remote-implementation/successors/example-school/apply/successor-manifest.json",
            "sha256": "f" * 64,
        },
        "stage2_apply_verification": {
            "path": ".remote-implementation/verifications/example-school/apply/stage2-sealed-apply-verification.json",
            "sha256": "f" * 64,
        },
        "approved_plan_hash": "f" * 64,
        "release_manifest_sha256": "f" * 64,
        "authority": {
            "owner_gate_1": False,
            "owner_gate_2": False,
            "release": False,
            "release_presentation_refresh": True,
            "recovery": False,
        },
    }


class PresentationAdmissionTests(unittest.TestCase):
    def test_exact_request_acquires_serialized_mutation_lock(self):
        req = request()
        validate_request(req)
        locked = begin_request(
            initial_control_state(), req, "f" * 64,
            run_id="run-1", run_attempt="1", request_commit="a" * 40,
        )
        self.assertEqual(locked["lifecycle_state"], "ACTIVE")
        self.assertEqual(locked["transaction_state"], "LOCKED")
        self.assertEqual(locked["active_operation"], OP_RELEASE_PRESENTATION_REFRESH)
        self.assertEqual(locked["active_target_branch"], req["target_branch"])
        self.assertTrue(locked["recovery_required"])
        with self.assertRaises(RemoteImplementationError):
            begin_request(
                locked, req, "f" * 64,
                run_id="run-2", run_attempt="1", request_commit="a" * 40,
            )

    def test_wrong_main_blob_seal_scope_or_source_hash_fails(self):
        for key, bad in (
            ("repair_main_sha", "a" * 40),
            ("accepted_asset_blob_sha", "wrong"),
            ("sealed_tree_sha", ""),
            ("target_sha", None),
            ("target_branch", "data/other-school-onboarding"),
            ("stage2_apply_successor", None),
            ("stage2_apply_verification", None),
            ("approved_plan_hash", "bad"),
        ):
            with self.subTest(key=key):
                req = request()
                req[key] = bad
                with self.assertRaises(RemoteImplementationError):
                    validate_request(req)

    def test_owner_gate_and_other_operation_powers_forbidden(self):
        for key in (
            "owner_gate_1", "owner_gate_2", "phase0",
            "stage2_sealed_apply", "stage2_current_main_refresh",
            "release_readiness", "release_preview_verify",
            "release_gate2_approval", "release_production_proof",
            "venue_identity_maintenance",
        ):
            with self.subTest(key=key):
                req = request()
                req["authority"][key] = True
                with self.assertRaises(RemoteImplementationError):
                    validate_request(req)

    def test_unapproved_or_misrouted_request_is_rejected(self):
        req = request()
        req["authority"]["release_presentation_refresh"] = False
        with self.assertRaises(RemoteImplementationError):
            validate_request(req)
        req = request()
        req["operation"] = "RELEASE_READINESS"
        with self.assertRaises(RemoteImplementationError):
            validate_request(req)


if __name__ == "__main__":
    unittest.main()
