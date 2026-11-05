"""Final-release merge packet binding tests."""
from __future__ import annotations

import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import remote_implementation_final_release as final_release  # noqa: E402
import remote_implementation_production as production  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402

SCHOOL = "example-school"
BRANCH = "data/example-school-onboarding"
GATE2_ID = "example-release-gate2-0001"
PRODUCTION_ID = "example-production-0001"
PR = 321
HEAD = "a" * 40
APPROVED_MAIN = "b" * 40
HASH = "c" * 64


def dump(value):
    return (json.dumps(value, sort_keys=True) + "\n").encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def fixture(*, packet_method="merge", production_request_id=PRODUCTION_ID):
    checkpoint_path = (
        f".remote-implementation/checkpoints/{SCHOOL}/{GATE2_ID}/"
        "checkpoint-manifest.json"
    )
    verification_path = (
        f".remote-implementation/verifications/{SCHOOL}/{GATE2_ID}/"
        "gate2-approval-verification.json"
    )
    gate2_request_path = (
        f".remote-implementation/checkpoints/{SCHOOL}/{GATE2_ID}/request.json"
    )
    packet_path = (
        f".remote-implementation/checkpoints/{SCHOOL}/{GATE2_ID}/"
        "gate2-merge-packet.json"
    )

    gate2_request = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": GATE2_ID,
        "operation": "RELEASE_GATE2_APPROVAL",
        "school_key": SCHOOL,
        "expected_protected_main_sha": APPROVED_MAIN,
        "target_branch": BRANCH,
        "target_sha": HEAD,
        "pr_number": PR,
        "final_release_continuation": {
            "kind": final_release.FINAL_RELEASE_CONTINUATION_KIND,
            "production_request_id": production_request_id,
        },
    }
    gate2_request_bytes = dump(gate2_request)

    packet = {
        "schema_version": 1,
        "kind": final_release.MERGE_PACKET_KIND,
        "gate2_request_id": GATE2_ID,
        "production_request_id": production_request_id,
        "school_key": SCHOOL,
        "pr_number": PR,
        "pr_head_sha": HEAD,
        "target_branch": BRANCH,
        "base_branch": "main",
        "approved_main_sha": APPROVED_MAIN,
        "merge_method": packet_method,
        "preview_deployment_id": 777,
        "preview_url": "https://example-preview.vercel.app",
        "owner_gate_2_approved": True,
        "merged": False,
        "production_proof": False,
    }
    packet_bytes = dump(packet)
    packet_hash = digest(packet_bytes)

    checkpoint = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVED_CHECKPOINT",
        "request_id": GATE2_ID,
        "request_sha256": digest(gate2_request_bytes),
        "school_key": SCHOOL,
        "status": "OWNER_GATE_2_APPROVED",
        "target_branch": BRANCH,
        "target_sha": HEAD,
        "pr_number": PR,
        "owner_gate_2_approved": True,
        "merged": False,
        "production_proof": False,
        "gate2_merge_packet_path": packet_path,
        "gate2_merge_packet_sha256": packet_hash,
        "production_request_id": production_request_id,
    }
    checkpoint_bytes = dump(checkpoint)

    verification = {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_OWNER_GATE_2_APPROVAL_VERIFICATION",
        "status": "PASS",
        "request_id": GATE2_ID,
        "school_key": SCHOOL,
        "checkpoint_sha256": digest(checkpoint_bytes),
        "pr_number": PR,
        "pr_head_sha": HEAD,
        "owner_gate_2_approved": True,
        "merged": False,
        "gate2_merge_packet_sha256": packet_hash,
        "production_request_id": production_request_id,
        "remote_gate2_approval_equivalence": "PASS",
    }
    verification_bytes = dump(verification)

    request = {
        "request_id": production_request_id,
        "school_key": SCHOOL,
        "target_branch": BRANCH,
        "target_sha": HEAD,
        "pr_number": PR,
        "owner_gate_2_checkpoint": {
            "path": checkpoint_path,
            "sha256": digest(checkpoint_bytes),
        },
        "owner_gate_2_verification": {
            "path": verification_path,
            "sha256": digest(verification_bytes),
        },
    }

    storage = {
        checkpoint_path: checkpoint_bytes,
        verification_path: verification_bytes,
        gate2_request_path: gate2_request_bytes,
        packet_path: packet_bytes,
    }
    return request, storage


class FinalReleaseVerifierImportTests(unittest.TestCase):
    def test_gate2_fresh_verifier_imports_merge_packet_builder(self):
        self.assertIs(
            verifier.build_gate2_merge_packet,
            production.build_gate2_merge_packet,
        )

    def test_production_fresh_verifier_imports_packet_binding(self):
        self.assertIs(
            verifier.verify_final_release_packet_binding,
            final_release.verify_final_release_packet_binding,
        )


class FinalReleasePacketTests(unittest.TestCase):
    def authenticate(self, request, storage):
        with patch.object(
            final_release,
            "git_show_bytes",
            side_effect=lambda _head, path, **_: storage[path],
        ):
            return final_release.verify_final_release_packet_binding(
                request,
                "d" * 40,
                repo=ROOT,
            )

    def test_exact_packet_is_accepted(self):
        request, storage = fixture()
        packet = self.authenticate(request, storage)
        self.assertEqual(packet["merge_method"], "merge")
        self.assertEqual(packet["approved_main_sha"], APPROVED_MAIN)
        self.assertEqual(packet["production_request_id"], PRODUCTION_ID)

    def test_wrong_production_request_id_is_refused(self):
        request, storage = fixture()
        request["request_id"] = "example-production-wrong"
        with self.assertRaisesRegex(
            final_release.Stop,
            "PRODUCTION_REQUEST_ID_MISMATCH",
        ):
            self.authenticate(request, storage)

    def test_wrong_merge_method_is_refused(self):
        request, storage = fixture(packet_method="squash")
        with self.assertRaisesRegex(
            final_release.Stop,
            "MERGE_PACKET_FIELD_MISMATCH:merge_method",
        ):
            self.authenticate(request, storage)

    def test_wrong_pr_head_is_refused(self):
        request, storage = fixture()
        request["target_sha"] = "e" * 40
        with self.assertRaisesRegex(
            final_release.Stop,
            "MERGE_PACKET_FIELD_MISMATCH:pr_head_sha",
        ):
            self.authenticate(request, storage)

    def test_legacy_gate2_without_packet_remains_supported(self):
        request, storage = fixture()
        checkpoint_path = request["owner_gate_2_checkpoint"]["path"]
        checkpoint = json.loads(storage[checkpoint_path])
        for key in (
            "production_request_id",
            "gate2_merge_packet_path",
            "gate2_merge_packet_sha256",
        ):
            checkpoint.pop(key, None)
        storage[checkpoint_path] = dump(checkpoint)
        request["owner_gate_2_checkpoint"]["sha256"] = digest(
            storage[checkpoint_path]
        )
        self.assertIsNone(self.authenticate(request, storage))


if __name__ == "__main__":
    unittest.main()
