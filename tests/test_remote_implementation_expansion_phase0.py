"""Remote control-plane validation for guarded ALL_HISTORY_EXPANSION Phase 0."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
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
    _install_scope_generated_projection,
    _pin_stage1_control_authority,
    _require_repository_acceptance,
    _require_source_game_package_update,
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
        "stage1_control_authority_sha": "a" * 40,
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


class ExpansionOpponentDisplayRequestTests(unittest.TestCase):
    def test_optional_opponent_display_reconciliation_ref_is_validated(self):
        request = expansion_request()
        request["opponent_display_reconciliation"] = {
            "path": ".remote-implementation/payloads/example/display.json",
            "sha256": "b" * 64,
        }
        validate_request(request)

    def test_bad_opponent_display_reconciliation_hash_is_rejected(self):
        request = expansion_request()
        request["opponent_display_reconciliation"] = {
            "path": ".remote-implementation/payloads/example/display.json",
            "sha256": "bad",
        }
        with self.assertRaises(RemoteImplementationError):
            validate_request(request)


class ExpansionImplementationAcceptancePreflightTests(unittest.TestCase):
    def test_preflight_passes_and_preserves_json_proof(self):
        import json
        import tempfile

        payload = {
            "summary": {
                "status": "PASS",
                "curated_lifecycle_suite": "PASS",
            },
            "errors": [],
        }
        with tempfile.TemporaryDirectory() as temporary, patch(
            "remote_implementation_expansion_phase0.git",
            return_value=SimpleNamespace(stdout="3" * 40),
        ), patch(
            "remote_implementation_expansion_phase0.run",
            return_value=SimpleNamespace(
                returncode=0,
                stdout=json.dumps(payload),
            ),
        ):
            diag = Path(temporary)
            result = _require_repository_acceptance("3" * 40, diag)
            self.assertEqual(result["summary"]["status"], "PASS")
            self.assertEqual(
                json.loads(
                    (diag / "all-history-expansion-implementation-acceptance.json")
                    .read_text(encoding="utf-8")
                ),
                payload,
            )

    def test_preflight_fails_before_transaction_on_acceptance_failure(self):
        import json
        import tempfile

        payload = {
            "summary": {
                "status": "FAIL",
                "curated_lifecycle_suite": "FAIL",
            },
            "errors": ["known generic blocker"],
        }
        with tempfile.TemporaryDirectory() as temporary, patch(
            "remote_implementation_expansion_phase0.git",
            return_value=SimpleNamespace(stdout="3" * 40),
        ), patch(
            "remote_implementation_expansion_phase0.run",
            return_value=SimpleNamespace(
                returncode=1,
                stdout=json.dumps(payload),
            ),
        ):
            with self.assertRaisesRegex(
                Stop,
                "EXPANSION_IMPLEMENTATION_ACCEPTANCE_FAILED",
            ):
                _require_repository_acceptance("3" * 40, Path(temporary))

    def test_preflight_rejects_wrong_runtime_main(self):
        import tempfile

        with tempfile.TemporaryDirectory() as temporary, patch(
            "remote_implementation_expansion_phase0.git",
            return_value=SimpleNamespace(stdout="4" * 40),
        ):
            with self.assertRaisesRegex(
                Stop,
                "EXPANSION_IMPLEMENTATION_ACCEPTANCE_RUNTIME_MISMATCH",
            ):
                _require_repository_acceptance("3" * 40, Path(temporary))


class ExpansionZeroDeltaSourceUpdateTests(unittest.TestCase):
    def test_zero_delta_scope_only_change_does_not_require_source_games_diff(self):
        intent={
            "school_key":"example",
            "supplemental_source_game_count":0,
        }
        _require_source_game_package_update(
            intent,
            ["data/reference/programs.csv"],
        )

    def test_nonzero_expansion_still_requires_source_games_diff(self):
        intent={
            "school_key":"example",
            "supplemental_source_game_count":1,
        }
        with self.assertRaisesRegex(
            Stop,
            "EXPANSION_PHASE0_SOURCE_GAME_PACKAGE_NOT_UPDATED",
        ):
            _require_source_game_package_update(
                intent,
                ["data/reference/programs.csv"],
            )


class ExpansionScopeGeneratedProjectionTests(unittest.TestCase):
    def test_scope_projection_stages_only_target_generated_files(self):
        import tempfile

        expected = [
            "site/data/programs.json",
            "site/data/teams/example.json",
        ]
        authority = {"intent": {"scope_generated_paths": expected}}
        with tempfile.TemporaryDirectory() as temporary:
            worktree = Path(temporary) / "repo"
            diag = Path(temporary) / "diag"
            (worktree / "tools").mkdir(parents=True)
            for path in expected:
                target = worktree / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}\n", encoding="utf-8")

            def fake_run(*args, **kwargs):
                return SimpleNamespace(returncode=0, stdout="PASS\n")

            def fake_git(*args, **kwargs):
                if args[:4] == ("diff", "--name-only", "--", "site/data"):
                    return SimpleNamespace(stdout="\n".join(expected) + "\n")
                if args[:2] == ("add", "--"):
                    return SimpleNamespace(stdout="")
                raise AssertionError(f"unexpected git call: {args}")

            with patch(
                "remote_implementation_expansion_phase0.run",
                side_effect=fake_run,
            ) as run_mock, patch(
                "remote_implementation_expansion_phase0.git",
                side_effect=fake_git,
            ) as git_mock:
                observed = _install_scope_generated_projection(
                    worktree,
                    expansion_request(),
                    authority,
                    diag,
                )

            self.assertEqual(observed, expected)
            self.assertTrue(
                (diag / "expansion-phase0-build-site-data.log").is_file()
            )
            run_mock.assert_called_once()
            git_mock.assert_any_call(
                "add",
                "--",
                *expected,
                cwd=worktree,
            )

    def test_scope_projection_rejects_unrelated_generated_drift(self):
        import tempfile

        expected = [
            "site/data/programs.json",
            "site/data/teams/example.json",
        ]
        authority = {"intent": {"scope_generated_paths": expected}}
        with tempfile.TemporaryDirectory() as temporary:
            worktree = Path(temporary) / "repo"
            diag = Path(temporary) / "diag"
            (worktree / "tools").mkdir(parents=True)
            for path in expected:
                target = worktree / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("{}\n", encoding="utf-8")

            with patch(
                "remote_implementation_expansion_phase0.run",
                return_value=SimpleNamespace(returncode=0, stdout="PASS\n"),
            ), patch(
                "remote_implementation_expansion_phase0.git",
                return_value=SimpleNamespace(
                    stdout=(
                        "site/data/programs.json\n"
                        "site/data/teams/example.json\n"
                        "site/data/teams/other.json\n"
                    )
                ),
            ):
                with self.assertRaisesRegex(
                    Stop,
                    "EXPANSION_PHASE0_SCOPE_SITE_PROJECTION_OUTSIDE_TARGET",
                ):
                    _install_scope_generated_projection(
                        worktree,
                        expansion_request(),
                        authority,
                        diag,
                    )


class ExpansionPinnedControlAuthorityTests(unittest.TestCase):
    @staticmethod
    def _git(repo: Path, *args: str, check: bool = True):
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=check,
        )

    def test_pin_survives_later_control_commits(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            control_repo = root / "control"
            replay = root / "replay"
            control_repo.mkdir()
            replay.mkdir()

            for repo in (control_repo, replay):
                self._git(repo, "init")
                self._git(repo, "config", "user.email", "test@example.com")
                self._git(repo, "config", "user.name", "Test")

            (control_repo / "authority").write_text(
                "startup\n",
                encoding="utf-8",
            )
            self._git(control_repo, "add", "authority")
            self._git(control_repo, "commit", "-m", "startup authority")
            pinned = self._git(
                control_repo,
                "rev-parse",
                "HEAD",
            ).stdout.strip()

            (control_repo / "later").write_text(
                "lock\n",
                encoding="utf-8",
            )
            self._git(control_repo, "add", "later")
            self._git(control_repo, "commit", "-m", "later control")
            current = self._git(
                control_repo,
                "rev-parse",
                "HEAD",
            ).stdout.strip()

            previous = Path.cwd()
            os.chdir(control_repo)
            try:
                request = expansion_request()
                request["stage1_control_authority_sha"] = pinned
                observed = _pin_stage1_control_authority(
                    request,
                    current,
                    replay,
                )
            finally:
                os.chdir(previous)

            self.assertEqual(observed, pinned)
            self.assertEqual(
                self._git(
                    replay,
                    "rev-parse",
                    "refs/remotes/origin/remote-control",
                ).stdout.strip(),
                pinned,
            )

    def test_pin_rejects_nonancestor_control(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            control_repo = root / "control"
            replay = root / "replay"
            control_repo.mkdir()
            replay.mkdir()

            self._git(control_repo, "init")
            self._git(control_repo, "config", "user.email", "test@example.com")
            self._git(control_repo, "config", "user.name", "Test")
            self._git(replay, "init")
            self._git(replay, "config", "user.email", "test@example.com")
            self._git(replay, "config", "user.name", "Test")

            (control_repo / "main").write_text(
                "one\n",
                encoding="utf-8",
            )
            self._git(control_repo, "add", "main")
            self._git(control_repo, "commit", "-m", "one")
            current = self._git(
                control_repo,
                "rev-parse",
                "HEAD",
            ).stdout.strip()

            self._git(control_repo, "checkout", "--orphan", "other")
            self._git(control_repo, "rm", "-rf", ".")
            (control_repo / "other").write_text(
                "two\n",
                encoding="utf-8",
            )
            self._git(control_repo, "add", "other")
            self._git(control_repo, "commit", "-m", "two")
            pinned = self._git(
                control_repo,
                "rev-parse",
                "HEAD",
            ).stdout.strip()

            previous = Path.cwd()
            os.chdir(control_repo)
            try:
                request = expansion_request()
                request["stage1_control_authority_sha"] = pinned
                with self.assertRaisesRegex(
                    Stop,
                    "EXPANSION_PHASE0_STAGE1_CONTROL_AUTHORITY_NOT_ANCESTOR",
                ):
                    _pin_stage1_control_authority(
                        request,
                        current,
                        replay,
                    )
            finally:
                os.chdir(previous)


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

    def test_expansion_requires_pinned_stage1_control_authority(self):
        request = expansion_request()
        request.pop("stage1_control_authority_sha")
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_PHASE0_STAGE1_CONTROL_AUTHORITY_INVALID",
        ):
            validate_request(request)

        request = expansion_request()
        request["stage1_control_authority_sha"] = "not-a-sha"
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "EXPANSION_PHASE0_STAGE1_CONTROL_AUTHORITY_INVALID",
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
