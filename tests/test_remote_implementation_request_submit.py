"""Exact control-state request submission and CAS regression tests.

The Git integration tests use a temporary local bare remote only. They never
submit a real school request, touch the operational control branch, or require
GitHub credentials.
"""
from __future__ import annotations

import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_control import (  # noqa: E402
    OP_RECOVER,
    initial_control_state,
    RemoteImplementationError,
    sha256_bytes,
    validate_request,
)
from remote_implementation_io import Stop  # noqa: E402
import remote_implementation_request_submit as submit  # noqa: E402


MAIN = "b" * 40
CONTROL = "a" * 40


def template():
    return {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": "school-stage2-census-0091",
        "school_key": "school",
        "operation": "STAGE2_CENSUS",
        "expected_protected_main_sha": MAIN,
        "target_branch": "data/school-onboarding",
        "target_sha": "c" * 40,
        "phase0_successor": {
            "path": ".remote-implementation/successors/school/phase0.json",
            "sha256": "d" * 64,
        },
        "integration_freeze_sha256": "e" * 64,
        "semantic_snapshot_sha256": "f" * 64,
        "creation_provenance": {
            "origin": "test exact prior owner authorization",
            "authorization": "pre-existing school Stage 2 authority",
        },
        "authority": {
            "owner_gate_1": False,
            "owner_gate_2": False,
            "phase0": False,
            "recovery": False,
            "release": False,
            "stage2_census": True,
            "stage2_opponent_display_normalize": False,
            "stage2_proposal_rehearsal": False,
            "stage2_reconciliation_diagnostic": False,
        },
    }


def noncanonical_state():
    return (json.dumps(initial_control_state(), indent=3) + "\n").encode()


class ExactEnvelopeTests(unittest.TestCase):
    def setUp(self):
        self.state = initial_control_state()
        self.raw = noncanonical_state()
        self.body = template()

    def bind(self, *, prior_id="previous-unrelated-request-0001"):
        return submit.prepare_exact_request(
            self.body,
            state=self.state,
            state_bytes=self.raw,
            control_head=CONTROL,
            live_main=MAIN,
            last_request_id=prior_id,
        )

    def test_valid_request_uses_raw_control_bytes_and_single_exact_parent(self):
        req = self.bind()
        validate_request(req)
        self.assertEqual(req["previous_control_state_commit"], CONTROL)
        self.assertEqual(
            req["previous_control_state_sha256"],
            hashlib.sha256(self.raw).hexdigest(),
        )
        normalized = json.dumps(self.state, sort_keys=True).encode()
        self.assertNotEqual(hashlib.sha256(normalized).hexdigest(),
                            req["previous_control_state_sha256"])
        self.assertNotIn("previous_control_state_commit", self.body)
        self.assertNotIn("previous_control_state_sha256", self.body)
        self.assertEqual(req["authority"], self.body["authority"])
        self.assertEqual(req["creation_provenance"], self.body["creation_provenance"])

    def test_cannot_supply_stale_control_commit(self):
        self.body["previous_control_state_commit"] = "f" * 40
        with self.assertRaisesRegex(Stop, "TEMPLATE_CONTAINS_PREDECESSOR"):
            self.bind()

    def test_cannot_supply_wrong_state_hash_even_with_right_commit(self):
        self.body["previous_control_state_sha256"] = "0" * 64
        with self.assertRaisesRegex(Stop, "TEMPLATE_CONTAINS_PREDECESSOR"):
            self.bind()

    def test_even_matching_envelope_must_be_omitted(self):
        self.body["previous_control_state_commit"] = CONTROL
        self.body["previous_control_state_sha256"] = sha256_bytes(self.raw)
        with self.assertRaisesRegex(Stop, "TEMPLATE_CONTAINS_PREDECESSOR"):
            self.bind()

    def test_protected_main_change_stops_without_rebinding(self):
        self.body["expected_protected_main_sha"] = "0" * 40
        with self.assertRaisesRegex(Stop, "EXPECTED_MAIN_CHANGED"):
            self.bind()

    def test_current_unaccepted_request_id_must_not_be_reissued(self):
        with self.assertRaisesRegex(Stop, "REQUEST_ID_ALREADY_USED"):
            self.bind(prior_id=self.body["request_id"])

    def test_accepted_request_id_must_not_be_replayed(self):
        self.state["accepted_request_ids"].append(self.body["request_id"])
        with self.assertRaisesRegex(Stop, "REQUEST_ID_ALREADY_USED"):
            self.bind()

    def test_active_lock_stops_submission(self):
        self.state["lifecycle_state"] = "ACTIVE"
        self.state["transaction_state"] = "LOCKED"
        self.state["active_request_id"] = "other-school-apply"
        self.state["active_lock_commit"] = "f" * 40
        with self.assertRaisesRegex(Stop, "CONTROL_NOT_SAFELY_IDLE"):
            self.bind()

    def test_recovery_required_cannot_be_ignored(self):
        self.state["recovery_required"] = True
        with self.assertRaisesRegex(
            RemoteImplementationError, "IDLE_CONTROL_REQUIRES_RECOVERY"
        ):
            self.bind()

    def test_diverged_control_state_refused(self):
        self.state["transaction_state"] = "DIVERGED_STOP"
        with self.assertRaisesRegex(Stop, "CONTROL_NOT_SAFELY_IDLE"):
            self.bind()

    def test_recovery_operation_requires_other_explicit_path(self):
        self.body["operation"] = OP_RECOVER
        with self.assertRaisesRegex(Stop, "RECOVERY_REQUIRES_EXPLICIT_PATH"):
            self.bind()

    def test_invalid_operation_authority_remains_rejected(self):
        self.body["authority"]["stage2_census"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError, "STAGE2_CENSUS_REQUEST_AUTHORITY_REQUIRED"
        ):
            self.bind()

    def test_missing_gate_provenance_not_generated(self):
        self.body.pop("creation_provenance")
        with self.assertRaisesRegex(
            RemoteImplementationError, "REQUEST_PROVENANCE_MISSING"
        ):
            self.bind()


def git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if result.returncode:
        raise AssertionError(f"git {args} failed:\n{result.stdout}")
    return result.stdout.strip()


class LocalControlCASIntegrationTests(unittest.TestCase):
    def setUp(self):
        self._temp = tempfile.TemporaryDirectory()
        self.addCleanup(self._temp.cleanup)
        work = Path(self._temp.name)
        self.origin = work / "origin.git"
        self.repo = work / "client"
        git(work, "init", "--bare", str(self.origin))
        git(work, "init", "-b", "main", str(self.repo))
        git(self.repo, "config", "user.name", "Request Test")
        git(self.repo, "config", "user.email", "request-test@example.invalid")
        git(self.repo, "remote", "add", "origin", str(self.origin))
        (self.repo / "README.md").write_text("read-only test repository\n")
        git(self.repo, "add", "README.md")
        git(self.repo, "commit", "-m", "main base")
        git(self.repo, "push", "origin", "HEAD:refs/heads/main")
        git(self.repo, "checkout", "-b", "control/remote-implementation")
        control = self.repo / ".remote-implementation"
        control.mkdir()
        (control / "control-state.json").write_bytes(noncanonical_state())
        (control / "request.json").write_text(
            json.dumps({"request_id": "previous-request-0001"}) + "\n"
        )
        git(self.repo, "add", "--", ".remote-implementation")
        git(self.repo, "commit", "-m", "initial independent control state")
        git(
            self.repo,
            "push",
            "origin",
            "HEAD:refs/heads/control/remote-implementation",
        )
        git(self.repo, "checkout", "main")
        self.live_main, self.control_head = submit.fetch_exact_heads(self.repo)

    def body(self):
        body = template()
        body["expected_protected_main_sha"] = self.live_main
        return body

    def remote_request(self):
        submit.fetch_exact_heads(self.repo)
        body = git(
            self.repo,
            "show",
            "refs/remotes/origin/remote-control:.remote-implementation/request.json",
        )
        return json.loads(body)

    def test_validated_only_never_publishes(self):
        result = submit.submit_request(self.repo, self.body(), submit=False)
        self.assertEqual(result["status"], "VALIDATED_ONLY")
        _, head = submit.fetch_exact_heads(self.repo)
        self.assertEqual(head, self.control_head)

    def test_publishes_one_exact_parent_commit_and_no_other_control_files(self):
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}):
            result = submit.submit_request(self.repo, self.body(), submit=True)
        self.assertEqual(result["status"], "PUBLISHED_REQUEST_NOT_YET_ACCEPTED")
        self.assertEqual(
            git(
                self.repo, "rev-list", "-n", "1",
                f"{result['request_commit_sha']}^",
            ),
            self.control_head,
        )
        req = self.remote_request()
        self.assertEqual(
            req["previous_control_state_commit"], self.control_head
        )
        self.assertEqual(
            req["previous_control_state_sha256"],
            sha256_bytes(noncanonical_state()),
        )
        self.assertEqual(req["expected_protected_main_sha"], self.live_main)
        changed = git(
            self.repo, "diff-tree", "--no-commit-id", "--name-only", "-r",
            result["request_commit_sha"],
        ).splitlines()
        self.assertEqual(changed, [".remote-implementation/request.json"])
        self.assertEqual(
            req["request_id"], self.body()["request_id"]
        )

    def test_repeat_submit_refuses_same_unaccepted_request_id(self):
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}):
            submit.submit_request(self.repo, self.body(), submit=True)
        with self.assertRaisesRegex(Stop, "REQUEST_ID_ALREADY_USED"):
            submit.submit_request(self.repo, self.body(), submit=False)

    def test_live_main_moving_before_publication_fails_closed(self):
        original = submit.fetch_exact_heads
        def changed_second_fetch(repo):
            changed_second_fetch.calls += 1
            main, control = original(repo)
            return (("f" * 40 if changed_second_fetch.calls > 1 else main), control)
        changed_second_fetch.calls = 0
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}), patch.object(
            submit, "fetch_exact_heads", side_effect=changed_second_fetch
        ):
            with self.assertRaisesRegex(Stop, "REFS_MOVED_BEFORE_CAS"):
                submit.submit_request(self.repo, self.body(), submit=True)
        _, head = original(self.repo)
        self.assertEqual(head, self.control_head)

    def test_actions_token_cannot_publish_silent_nontriggering_push(self):
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}):
            with self.assertRaisesRegex(Stop, "ACTIONS_TOKEN"):
                submit.submit_request(self.repo, self.body(), submit=True)
        _, head = submit.fetch_exact_heads(self.repo)
        self.assertEqual(head, self.control_head)

    def test_stale_body_main_will_never_publish(self):
        body = self.body()
        body["expected_protected_main_sha"] = "0" * 40
        with patch.dict(os.environ, {"GITHUB_ACTIONS": "false"}):
            with self.assertRaisesRegex(Stop, "EXPECTED_MAIN_CHANGED"):
                submit.submit_request(self.repo, body, submit=True)
        _, head = submit.fetch_exact_heads(self.repo)
        self.assertEqual(head, self.control_head)


if __name__ == "__main__":
    unittest.main()
