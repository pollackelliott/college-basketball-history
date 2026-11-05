"""Exact-head PR/Preview authorization tests; never create PR/merge."""
import hashlib
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import remote_implementation_release_preview as preview  # noqa: E402
from remote_implementation_io import Stop  # noqa: E402

BRANCH = "data/example-school-onboarding"
SHA = "a" * 40
BODY = "## Summary\nApproved plan bound to exact sealed apply\n"
BODY_SHA = hashlib.sha256(BODY.encode()).hexdigest()
PR_NO = 123


def valid_pr():
    return {
        "number": PR_NO, "url": "https://github.com/example/repo/pull/123",
        "state": "OPEN", "isDraft": False, "headRefOid": SHA,
        "headRefName": BRANCH, "baseRefName": "main", "body": BODY,
        "headRepositoryOwner": {"login": "example"},
        "headRepository": {"name": "repo"},
    }


class ExactPreviewVerificationTests(unittest.TestCase):
    @patch.object(preview.release_school, "repository_slug", return_value="example/repo")
    @patch.object(preview.release_school, "gh_json")
    @patch.object(preview, "remote_head", return_value=SHA)
    def test_pr_identity_valid(self, _remote, gh, _slug):
        gh.return_value = valid_pr()
        result = preview.check_pr_identity(
            ROOT, pr_number=PR_NO, target_branch=BRANCH,
            target_sha=SHA, exact_pr_body_sha256=BODY_SHA,
        )
        self.assertEqual(result["target_sha"], SHA)

    def test_reject_modified_or_draft_head_and_body(self):
        for key, value in (
            ("state", "CLOSED"),
            ("isDraft", True),
            ("headRefOid", "b" * 40),
            ("headRefName", "wrong-branch"),
            ("baseRefName", "other"),
            ("body", "changed"),
        ):
            with self.subTest(key=key):
                with patch.object(preview.release_school, "gh_json") as gh:
                    with patch.object(preview.release_school, "repository_slug", return_value="example/repo"):
                        with patch.object(preview, "remote_head", return_value=SHA):
                            gh.return_value = {**valid_pr(), key: value}
                            with self.assertRaises(Stop):
                                preview.check_pr_identity(
                                    ROOT, pr_number=PR_NO, target_branch=BRANCH,
                                    target_sha=SHA, exact_pr_body_sha256=BODY_SHA,
                                )

    @patch.object(preview.release_school, "repository_slug", return_value="example/repo")
    @patch.object(preview.release_school, "gh_json")
    @patch.object(preview, "remote_head", return_value=SHA)
    def test_foreign_pr_head_repo_refused(self, _remote, gh, _slug):
        for key, value in (
            ("headRepositoryOwner", {"login": "unauthorized"}),
            ("headRepository", {"name": "foreign-fork"}),
        ):
            with self.subTest(key=key):
                gh.return_value = {**valid_pr(), key: value}
                with self.assertRaisesRegex(Stop, "PREVIEW_PR_FOREIGN_HEAD_REPOSITORY"):
                    preview.check_pr_identity(
                        ROOT, pr_number=PR_NO, target_branch=BRANCH,
                        target_sha=SHA, exact_pr_body_sha256=BODY_SHA,
                    )

    @patch.object(preview.release_school, "gh_json")
    @patch.object(preview, "remote_head", return_value="c" * 40)
    def test_ref_move_refused_before_pr_lookup(self, _remote, gh):
        with self.assertRaisesRegex(Stop, "PREVIEW_TARGET_REF_MOVED"):
            preview.check_pr_identity(
                ROOT, pr_number=PR_NO, target_branch=BRANCH,
                target_sha=SHA, exact_pr_body_sha256=BODY_SHA,
            )
        gh.assert_not_called()

    @patch.object(preview.release_school, "repository_slug", return_value="example/repo")
    @patch.object(preview.release_school, "wait_for_deployment")
    @patch.object(preview.release_school, "wait_for_pr_mergeable")
    @patch.object(preview.release_school, "gh")
    @patch.object(preview.release_school, "gh_json", return_value=valid_pr())
    @patch.object(preview, "remote_head", return_value=SHA)
    def test_successful_exact_preview_stops_before_gate2(
        self, _remote, _gh_json, gh, mergeable, deployment, _slug
    ):
        mergeable.return_value = {"headRefOid": SHA, "mergeable": "MERGEABLE"}
        deployment.return_value = {
            "deployment_id": 5, "sha": SHA, "state": "success",
            "environment": "Preview", "environment_url": "https://example.vercel.app",
        }
        result = preview.verify_pr_checks_and_preview(
            ROOT, pr_number=PR_NO, target_branch=BRANCH,
            target_sha=SHA, exact_pr_body_sha256=BODY_SHA,
        )
        self.assertEqual(result["status"], "OWNER_GATE_2_READY")
        self.assertFalse(result["owner_gate_2_approved"])
        self.assertFalse(result["merged"])
        self.assertFalse(result["production_proof"])
        gh.assert_called_once()

    @patch.object(preview.release_school, "repository_slug", return_value="example/repo")
    @patch.object(preview.release_school, "wait_for_deployment")
    @patch.object(preview.release_school, "wait_for_pr_mergeable")
    @patch.object(preview.release_school, "gh")
    @patch.object(preview.release_school, "gh_json", return_value=valid_pr())
    @patch.object(preview, "remote_head", return_value=SHA)
    def test_fails_preview_wrong_sha_or_missing_url(
        self, _remote, _gh_json, _gh, mergeable, deployment, _slug
    ):
        mergeable.return_value = {"headRefOid": SHA}
        for record in (
            {"deployment_id": 5, "sha": "0" * 40, "state": "success",
             "environment": "Preview", "environment_url": "https://example.vercel.app"},
            {"deployment_id": 5, "sha": SHA, "state": "success",
             "environment": "Preview", "environment_url": None},
            {"deployment_id": 5, "sha": SHA, "state": "success",
             "environment": "Production", "environment_url": "https://example.vercel.app"},
        ):
            with self.subTest(record=record):
                deployment.return_value = record
                with self.assertRaises(Stop):
                    preview.verify_pr_checks_and_preview(
                        ROOT, pr_number=PR_NO, target_branch=BRANCH,
                        target_sha=SHA, exact_pr_body_sha256=BODY_SHA,
                    )


class PriorReadinessAuthorityTests(unittest.TestCase):
    def setup_storage(self, branch=BRANCH):
        import json
        rid = "example-release-readiness-0001"
        school = "example-school"
        ckpt = (
            ".remote-implementation/checkpoints/"
            + school + "/" + rid + "/checkpoint-manifest.json"
        )
        verify = (
            ".remote-implementation/verifications/"
            + school + "/" + rid + "/release-readiness-verification.json"
        )
        prior_path = (
            ".remote-implementation/checkpoints/"
            + school + "/" + rid + "/request.json"
        )
        prior = {"request_id": rid, "operation": "RELEASE_READINESS"}
        prior_bytes = (json.dumps(prior, sort_keys=True)).encode()
        base = {
            "request_id": rid, "school_key": school, "target_branch": branch,
            "target_sha": SHA, "approved_plan_hash": "e" * 64,
            "release_manifest_sha256": "f" * 64,
        }
        check = {
            **base,
            "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_CHECKPOINT",
            "request_sha256": hashlib.sha256(prior_bytes).hexdigest(),
            "protected_main_sha": "0" * 40,
            "readiness_status": "RELEASE_READINESS_PASS",
            "tracked_mutation": "NONE", "pr_created": False, "owner_gate_2": False,
        }
        ckpt_bytes = (json.dumps(check, sort_keys=True)).encode()
        ver = {
            **base,
            "kind": "REMOTE_IMPLEMENTATION_RELEASE_READINESS_VERIFICATION",
            "checkpoint_manifest_sha256": hashlib.sha256(ckpt_bytes).hexdigest(),
            "remote_release_readiness_equivalence": "PASS",
            "tracked_mutation": "NONE", "pr_created": False, "owner_gate_2": False,
        }
        ver_bytes = (json.dumps(ver, sort_keys=True)).encode()
        request = {
            "school_key": school, "target_branch": branch, "target_sha": SHA,
            "expected_protected_main_sha": "1" * 40,
            "approved_plan_hash": "e" * 64,
            "release_manifest_sha256": "f" * 64,
            "release_readiness_checkpoint": {
                "path": ckpt, "sha256": hashlib.sha256(ckpt_bytes).hexdigest(),
            },
            "release_readiness_verification": {
                "path": verify, "sha256": hashlib.sha256(ver_bytes).hexdigest(),
            },
        }
        return request, {ckpt: ckpt_bytes, verify: ver_bytes, prior_path: prior_bytes}

    def bind_release_packet(
        self,
        request,
        storage,
        *,
        preview_request_id="example-preview-verify-0001",
    ):
        import json
        checkpoint_path = request["release_readiness_checkpoint"]["path"]
        verification_path = request["release_readiness_verification"]["path"]
        checkpoint = json.loads(storage[checkpoint_path])
        checkpoint["preview_request_id"] = preview_request_id
        checkpoint["pr_body_sha256"] = BODY_SHA
        checkpoint["release_pr_packet_sha256"] = "a" * 64
        storage[checkpoint_path] = (
            json.dumps(checkpoint, sort_keys=True)
        ).encode()
        request["release_readiness_checkpoint"]["sha256"] = hashlib.sha256(
            storage[checkpoint_path]
        ).hexdigest()

        verification = json.loads(storage[verification_path])
        verification["checkpoint_manifest_sha256"] = request[
            "release_readiness_checkpoint"
        ]["sha256"]
        verification["preview_request_id"] = preview_request_id
        verification["pr_body_sha256"] = BODY_SHA
        verification["release_pr_packet_sha256"] = "a" * 64
        storage[verification_path] = (
            json.dumps(verification, sort_keys=True)
        ).encode()
        request["release_readiness_verification"]["sha256"] = hashlib.sha256(
            storage[verification_path]
        ).hexdigest()
        request["request_id"] = preview_request_id
        return request, storage

    def authenticate(self, request, storage, *, ancestry=0):
        with patch.object(
            preview, "git_show_bytes",
            side_effect=lambda _commit, path, **_: storage[path],
        ):
            with patch.object(preview, "git") as git:
                with patch.object(preview, "remote_head", return_value=SHA):
                    with patch.object(
                        preview, "verify_release_readiness_authority",
                    ) as earlier:
                        git.return_value.returncode = ancestry
                        earlier.return_value = {
                            "target_sha": SHA,
                            "approved_plan_hash": "e" * 64,
                            "release_manifest_sha256": "f" * 64,
                            "sidecars": {"pr-body.md": BODY.encode()},
                        }
                        return preview.verify_release_preview_authority(
                            request, "2" * 40, source_repo=ROOT,
                        )

    def test_exact_fresh_readiness_chain(self):
        request, store = self.setup_storage()
        result = self.authenticate(request, store)
        self.assertEqual(result["pr_body_sha256"], BODY_SHA)
        self.assertEqual(result["readiness_request_id"], "example-release-readiness-0001")

    def test_exact_fresh_readiness_chain_honors_release_packet(self):
        request, store = self.setup_storage()
        request, store = self.bind_release_packet(request, store)
        result = self.authenticate(request, store)
        self.assertEqual(
            result["preview_request_id"],
            "example-preview-verify-0001",
        )
        self.assertEqual(
            result["release_pr_packet_sha256"],
            "a" * 64,
        )

    def test_release_packet_rejects_wrong_preview_request_id(self):
        request, store = self.setup_storage()
        request, store = self.bind_release_packet(request, store)
        request["request_id"] = "example-preview-verify-wrong"
        with self.assertRaisesRegex(
            Stop,
            "PREVIEW_REQUEST_ID_CONTINUATION_MISMATCH",
        ):
            self.authenticate(request, store)

    def test_release_packet_rejects_body_hash_drift(self):
        import json
        request, store = self.setup_storage()
        request, store = self.bind_release_packet(request, store)
        path = request["release_readiness_checkpoint"]["path"]
        checkpoint = json.loads(store[path])
        checkpoint["pr_body_sha256"] = "b" * 64
        store[path] = json.dumps(checkpoint, sort_keys=True).encode()
        request["release_readiness_checkpoint"]["sha256"] = hashlib.sha256(
            store[path]
        ).hexdigest()
        verify_path = request["release_readiness_verification"]["path"]
        verification = json.loads(store[verify_path])
        verification["checkpoint_manifest_sha256"] = request[
            "release_readiness_checkpoint"
        ]["sha256"]
        store[verify_path] = json.dumps(verification, sort_keys=True).encode()
        request["release_readiness_verification"]["sha256"] = hashlib.sha256(
            store[verify_path]
        ).hexdigest()
        with self.assertRaisesRegex(
            Stop,
            "PREVIEW_PR_BODY_CONTINUATION_HASH_MISMATCH",
        ):
            self.authenticate(request, store)

    def test_exact_fresh_readiness_chain_accepts_correction_branch(self):
        branch = "data/example-school-correction"
        request, store = self.setup_storage(branch)
        result = self.authenticate(request, store)
        self.assertEqual(result["target_branch"], branch)
        self.assertEqual(result["target_sha"], SHA)

    def test_reject_tampered_checkpoint(self):
        request, store = self.setup_storage()
        path = request["release_readiness_checkpoint"]["path"]
        store[path] += b"tampered"
        with self.assertRaisesRegex(Stop, "CHECKPOINT_HASH_MISMATCH"):
            self.authenticate(request, store)

    def test_reject_incomplete_fresh_equivalence(self):
        import json
        request, store = self.setup_storage()
        path = request["release_readiness_verification"]["path"]
        doc = json.loads(store[path])
        doc["remote_release_readiness_equivalence"] = "PENDING"
        store[path] = (json.dumps(doc, sort_keys=True)).encode()
        request["release_readiness_verification"]["sha256"] = hashlib.sha256(store[path]).hexdigest()
        with self.assertRaisesRegex(Stop, "EQUIVALENCE_MISMATCH"):
            self.authenticate(request, store)

    def test_reject_unrelated_current_main(self):
        request, store = self.setup_storage()
        with self.assertRaisesRegex(Stop, "NOT_DESCENDANT"):
            self.authenticate(request, store, ancestry=1)


if __name__ == "__main__":
    unittest.main()
