import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import remote_implementation_runner as runner  # noqa: E402
import remote_implementation_verify as verifier  # noqa: E402
from remote_implementation_control import (  # noqa: E402
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    canonical_json_bytes,
    initial_control_state,
    sha256_bytes,
)
from remote_implementation_io import Stop  # noqa: E402
from remote_implementation_stage2_opponent_display import (  # noqa: E402
    verify_prepared_commit_field_boundary,
)


SCHOOL = "example-school"
BRANCH = "data/example-school-onboarding"
MAIN = "a" * 40
LOCK = "b" * 40


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class RemoteStage2OpponentDisplayRecoveryTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> str:
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if cp.returncode:
            self.fail(cp.stdout)
        return cp.stdout.strip()

    def make_commits(self):
        repo = Path(tempfile.mkdtemp(prefix="display-recovery-test-"))
        self.addCleanup(lambda: shutil.rmtree(repo, ignore_errors=True))
        self.git(repo, "init")
        self.git(repo, "config", "user.name", "Test")
        self.git(repo, "config", "user.email", "test@example.com")
        write_csv(
            repo / "schools" / SCHOOL / "opponents.csv",
            [
                "source_opponent_label",
                "canonical_opponent_key",
                "canonical_opponent_name",
            ],
            [{
                "source_opponent_label": "Old literal",
                "canonical_opponent_key": "alpha-academy",
                "canonical_opponent_name": "Old",
            }],
        )
        write_csv(
            repo / "schools" / SCHOOL / "source-games.csv",
            [
                "source_game_id",
                "normalized_opponent_key",
                "normalized_opponent_name",
                "source_opponent_label",
                "raw_text",
            ],
            [{
                "source_game_id": "E-1",
                "normalized_opponent_key": "alpha-academy",
                "normalized_opponent_name": "Old",
                "source_opponent_label": "Old literal",
                "raw_text": "at Old literal",
            }],
        )
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "predecessor")
        predecessor = self.git(repo, "rev-parse", "HEAD")

        opp = repo / "schools" / SCHOOL / "opponents.csv"
        rows = list(csv.DictReader(opp.open(newline="", encoding="utf-8")))
        rows[0]["canonical_opponent_name"] = "Authority"
        write_csv(opp, list(rows[0]), rows)
        source = repo / "schools" / SCHOOL / "source-games.csv"
        rows = list(csv.DictReader(source.open(newline="", encoding="utf-8")))
        rows[0]["normalized_opponent_name"] = "Authority"
        write_csv(source, list(rows[0]), rows)
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "prepared")
        prepared = self.git(repo, "rev-parse", "HEAD")
        tree = self.git(repo, "rev-parse", "HEAD^{tree}")
        changed = self.git(
            repo,
            "diff-tree",
            "--no-commit-id",
            "--name-only",
            "-r",
            prepared,
        ).splitlines()
        hashes = {}
        for path in changed:
            data = subprocess.check_output(
                ["git", "show", f"{prepared}:{path}"],
                cwd=repo,
            )
            hashes[path] = hashlib.sha256(data).hexdigest()
        proof = verify_prepared_commit_field_boundary(
            repo,
            school_key=SCHOOL,
            predecessor_sha=predecessor,
            prepared_sha=prepared,
            expected_blocker_keys=["alpha-academy"],
        )
        return repo, predecessor, prepared, tree, sorted(changed), hashes, proof

    def make_state_and_request(
        self,
        *,
        predecessor: str,
        prepared: str,
        tree: str,
        changed: list[str],
        hashes: dict[str, str],
        proof: dict,
    ):
        original_request = {
            "request_id": "display-001",
            "school_key": SCHOOL,
            "target_branch": BRANCH,
            "target_sha": predecessor,
        }
        original_bytes = canonical_json_bytes(original_request)
        freeze = b'{"status":"INTEGRATION_FROZEN"}\n'
        manifest = {
            "operation": OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
            "protected_main_sha": MAIN,
            "expected_target_predecessor_sha": predecessor,
            "prepared_commit_sha": prepared,
            "prepared_tree_sha": tree,
            "prepared_parent_sha": predecessor,
            "changed_paths": changed,
            "changed_file_sha256": hashes,
            "integration_freeze_sha256": hashlib.sha256(freeze).hexdigest(),
            "semantic_snapshot_sha256": "c" * 64,
            "expected_blocker_keys": ["alpha-academy"],
            "repository_validation": "PASS",
        }
        state = initial_control_state()
        state.update({
            "lifecycle_state": "ACTIVE",
            "transaction_state": "PREPARED_NOT_PUBLISHED",
            "active_request_id": "display-001",
            "active_request_sha256": sha256_bytes(original_bytes),
            "active_school_key": SCHOOL,
            "active_operation": OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
            "active_expected_main_sha": MAIN,
            "active_lock_owner": "github-actions:test",
            "active_lock_commit": LOCK,
            "active_writeahead_path": ".remote-implementation/writeahead/example-school/display-001/writeahead-manifest.json",
            "active_writeahead_sha256": "d" * 64,
            "active_writeahead_commit": "e" * 40,
            "active_prepared_commit_sha": prepared,
            "active_prepared_tree_sha": tree,
            "active_target_branch": BRANCH,
            "recovery_required": True,
            "accepted_request_ids": ["display-001"],
        })
        recovery = {
            "request_id": "recovery-001",
            "school_key": SCHOOL,
            "recovery": {
                "abandoned_request_id": "display-001",
                "lock_commit": LOCK,
                "target_branch": BRANCH,
            },
        }
        return state, recovery, manifest, original_bytes, freeze

    def test_published_not_finalized_routes_to_exact_repair_adoption(self):
        (
            repo,
            predecessor,
            prepared,
            tree,
            changed,
            hashes,
            proof,
        ) = self.make_commits()
        state, recovery, manifest, original_bytes, freeze = (
            self.make_state_and_request(
                predecessor=predecessor,
                prepared=prepared,
                tree=tree,
                changed=changed,
                hashes=hashes,
                proof=proof,
            )
        )
        control_parent = "f" * 40
        prefix = Path(state["active_writeahead_path"]).parent

        def fake_git(*args, **kwargs):
            cp = subprocess.run(
                ["git", *args],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
            )
            if cp.returncode:
                raise AssertionError(cp.stdout)
            return cp

        def fake_show(commit, path, **kwargs):
            if commit == control_parent:
                if path == (prefix / "integration-freeze.json").as_posix():
                    return freeze
                if path == ".remote-implementation/requests/display-001/request.json":
                    return original_bytes
                if path == (prefix / "field-level-proof.json").as_posix():
                    return canonical_json_bytes(proof)
                raise AssertionError(path)
            return subprocess.check_output(
                ["git", "show", f"{commit}:{path}"],
                cwd=repo,
            )

        old_cwd = os.getcwd()
        with tempfile.TemporaryDirectory() as tmp, patch.object(
            runner, "ROOT", repo
        ), patch.object(
            runner, "load_writeahead", return_value=manifest
        ), patch.object(
            runner, "remote_head", return_value=prepared
        ), patch.object(
            runner, "git", side_effect=fake_git
        ), patch.object(
            runner, "git_show_bytes", side_effect=fake_show
        ), patch.object(
            runner,
            "finalize_stage2_opponent_display_successor",
            return_value="1" * 40,
        ) as finalize:
            os.chdir(tmp)
            try:
                runner.run_recovery(
                    state,
                    recovery,
                    "2" * 40,
                    control_parent,
                    MAIN,
                )
            finally:
                os.chdir(old_cwd)
        finalize.assert_called_once()
        kwargs = finalize.call_args.kwargs
        self.assertEqual(
            kwargs["publication_cas"],
            "RECOVERY_ADOPTION_EXACT_MATCH",
        )
        self.assertEqual(kwargs["recovery_classification"], "PUBLISHED_NOT_FINALIZED")
        self.assertEqual(kwargs["original_request"]["request_id"], "display-001")

    def test_diverged_target_is_hard_stop(self):
        (
            repo,
            predecessor,
            prepared,
            tree,
            changed,
            hashes,
            proof,
        ) = self.make_commits()
        state, recovery, manifest, _, _ = self.make_state_and_request(
            predecessor=predecessor,
            prepared=prepared,
            tree=tree,
            changed=changed,
            hashes=hashes,
            proof=proof,
        )
        with patch.object(
            runner, "load_writeahead", return_value=manifest
        ), patch.object(
            runner, "remote_head", return_value="9" * 40
        ):
            with self.assertRaisesRegex(Stop, "RECOVERY_DIVERGED_STOP"):
                runner.run_recovery(
                    state,
                    recovery,
                    "2" * 40,
                    "f" * 40,
                    MAIN,
                )

    def test_fresh_verifier_dispatches_repair_operation(self):
        state = initial_control_state()
        state["transaction_state"] = "COMPLETE"
        state["last_operation"] = {
            "operation": OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
            "request_id": "display-001",
        }
        with patch.object(
            verifier,
            "configure_git",
        ), patch.object(
            verifier,
            "fetch_operational_refs",
            return_value=(MAIN, "3" * 40),
        ), patch.object(
            verifier,
            "git_show_json",
            return_value=state,
        ), patch.object(
            verifier,
            "verify_stage2_opponent_display_normalization",
            return_value=0,
        ) as verify:
            self.assertEqual(verifier.main(), 0)
        verify.assert_called_once()


if __name__ == "__main__":
    unittest.main()
