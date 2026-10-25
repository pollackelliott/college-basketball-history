"""Control-plane scope tests for release readiness (never PR/Gate2 authority)."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_control import (  # noqa: E402
    OP_RELEASE_READINESS,
    OP_RELEASE_PREVIEW_VERIFY,
    LIFECYCLE_READ_ONLY,
    TX_RELEASE_READINESS_RUNNING,
    RemoteImplementationError,
    begin_request,
    initial_control_state,
    validate_request,
)

SHA = "a" * 40
HASH = "b" * 64
SCHOOL = "example-school"


def request():
    flags = {
        key: False
        for key in (
            "phase0", "recovery", "stage2_census", "stage2_opponent_display_normalize",
            "stage2_proposal_rehearsal", "stage2_gate1_fill",
            "stage2_preseal_rehearsal", "stage2_gate1_seal",
            "stage2_sealed_apply", "stage2_reconciliation_diagnostic",
            "owner_gate_1", "owner_gate_2", "release",
        )
    }
    flags["release_readiness"] = True
    return {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": "example-release-readiness-0001",
        "school_key": SCHOOL,
        "operation": OP_RELEASE_READINESS,
        "previous_control_state_commit": SHA,
        "previous_control_state_sha256": HASH,
        "expected_protected_main_sha": SHA,
        "target_branch": f"data/{SCHOOL}-onboarding",
        "target_sha": SHA,
        "stage2_apply_successor": {
            "path": f".remote-implementation/successors/{SCHOOL}/apply/successor-manifest.json",
            "sha256": HASH,
        },
        "stage2_apply_verification": {
            "path": f".remote-implementation/verifications/{SCHOOL}/apply/stage2-sealed-apply-verification.json",
            "sha256": HASH,
        },
        "approved_plan_hash": HASH,
        "release_manifest_sha256": HASH,
        "creation_provenance": {"origin": "Test", "authorization": "Bounded read-only gate"},
        "authority": flags,
    }


class ReleaseReadinessControlTests(unittest.TestCase):
    def test_exact_read_only_request_is_accepted(self):
        validate_request(request())

    def test_readiness_acquires_read_only_lifecycle_not_mutation_lock(self):
        r = request()
        state = begin_request(
            initial_control_state(), r, HASH,
            run_id="1", run_attempt="1", request_commit=SHA,
        )
        self.assertEqual(state["lifecycle_state"], LIFECYCLE_READ_ONLY)
        self.assertEqual(state["transaction_state"], TX_RELEASE_READINESS_RUNNING)
        self.assertIsNone(state["active_lock_owner"])

    def test_owner_gate_2_is_refused(self):
        r = request()
        r["authority"]["owner_gate_2"] = True
        with self.assertRaisesRegex(RemoteImplementationError, "GATE2_AUTHORITY_FORBIDDEN"):
            validate_request(r)

    def test_pr_release_authority_is_refused(self):
        r = request()
        r["authority"]["release"] = True
        with self.assertRaisesRegex(RemoteImplementationError, "RELEASE_AUTHORITY_FORBIDDEN"):
            validate_request(r)

    def test_sealed_apply_mutation_authority_is_refused(self):
        r = request()
        r["authority"]["stage2_sealed_apply"] = True
        with self.assertRaisesRegex(RemoteImplementationError, "SEALED_APPLY"):
            validate_request(r)

    def test_missing_fresh_apply_verification_is_refused(self):
        r = request()
        del r["stage2_apply_verification"]
        with self.assertRaisesRegex(RemoteImplementationError, "STAGE2_APPLY_VERIFICATION"):
            validate_request(r)

    def test_no_release_readiness_authority_is_refused(self):
        r = request()
        r["authority"]["release_readiness"] = False
        with self.assertRaisesRegex(RemoteImplementationError, "RELEASE_READINESS_AUTHORITY_REQUIRED"):
            validate_request(r)


def preview_request():
    r = request()
    r["operation"] = OP_RELEASE_PREVIEW_VERIFY
    r["request_id"] = "example-preview-verify-0001"
    r["authority"]["release_readiness"] = False
    r["authority"]["release_preview_verify"] = True
    r["release_readiness_checkpoint"] = {
        "path": ".remote-implementation/checkpoints/example-school/readiness/checkpoint-manifest.json",
        "sha256": HASH,
    }
    r["release_readiness_verification"] = {
        "path": ".remote-implementation/verifications/example-school/readiness/release-readiness-verification.json",
        "sha256": HASH,
    }
    r["pr_number"] = 123
    return r


class ReleasePreviewControlTests(unittest.TestCase):
    def test_exact_preview_check_is_valid_and_read_only(self):
        r = preview_request()
        validate_request(r)
        state = begin_request(
            initial_control_state(), r, HASH,
            run_id="1", run_attempt="1", request_commit=SHA,
        )
        self.assertEqual(state["lifecycle_state"], LIFECYCLE_READ_ONLY)
        self.assertIsNone(state["active_lock_owner"])

    def test_gate2_claim_refused(self):
        r = preview_request()
        r["authority"]["owner_gate_2"] = True
        with self.assertRaisesRegex(RemoteImplementationError, "GATE2_AUTHORITY_FORBIDDEN"):
            validate_request(r)

    def test_release_or_apply_authority_refused(self):
        for field in ("release", "stage2_sealed_apply", "release_readiness"):
            with self.subTest(field=field):
                r = preview_request()
                r["authority"][field] = True
                with self.assertRaises(RemoteImplementationError):
                    validate_request(r)

    def test_missing_preview_prior_verification_refused(self):
        r = preview_request()
        r.pop("release_readiness_verification")
        with self.assertRaisesRegex(RemoteImplementationError, "RELEASE_READINESS_VERIFICATION"):
            validate_request(r)

    def test_pr_number_must_be_integer(self):
        for number in ("123", 0, -1, None, 1.5):
            with self.subTest(number=number):
                r = preview_request()
                r["pr_number"] = number
                with self.assertRaisesRegex(RemoteImplementationError, "PR_NUMBER_INVALID"):
                    validate_request(r)



if __name__ == "__main__":
    unittest.main()
