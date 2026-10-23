import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remote_implementation_control import (  # noqa: E402
    CONTROL_KIND,
    LIFECYCLE_ACTIVE,
    LIFECYCLE_IDLE,
    MUTATION_COMPLETE,
    MUTATION_DIVERGED,
    MUTATION_NOT_ATTEMPTED,
    MUTATION_PREPARED,
    MUTATION_PUBLISHED,
    OP_PHASE0,
    OP_RECOVER,
    OP_STAGE1,
    OP_STAGE2_CENSUS,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    REQUEST_KIND,
    RemoteImplementationError,
    abandon_active,
    begin_request,
    bind_lock_commit,
    canonical_json_bytes,
    classify_mutation,
    initial_control_state,
    publish_ref_cas,
    remote_head,
    sha256_bytes,
    sha256_file,
    validate_control_state,
    validate_request,
    verify_request_predecessor,
    verify_sidecar_hashes,
)


MAIN = "a" * 40
PRED = "b" * 40
LOCK = "c" * 40
PREPARED = "d" * 40
TREE = "e" * 40
HASH = "f" * 64


def request(operation=OP_STAGE1, request_id="request-001"):
    base = {
        "schema_version": 1,
        "kind": REQUEST_KIND,
        "request_id": request_id,
        "school_key": "example-school",
        "operation": operation,
        "previous_control_state_commit": PRED,
        "previous_control_state_sha256": HASH,
        "expected_protected_main_sha": MAIN,
        "creation_provenance": {
            "origin": "ChatGPT",
            "authorization": "bounded owner-authorized operation",
        },
        "authority": {
            "owner_gate_1": False,
            "owner_gate_2": False,
            "release": False,
            "phase0": operation == OP_PHASE0,
            "stage2_census": operation == OP_STAGE2_CENSUS,
            "stage2_opponent_display_normalize": (
                operation == OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE
            ),
            "recovery": operation == OP_RECOVER,
        },
    }
    if operation in {OP_STAGE1, OP_PHASE0}:
        base["research_checkpoint"] = {
            "sha256": "1" * 64,
            "research_base_sha": "2" * 40,
            "transport": {
                "kind": "git_base64_parts",
                "commit_sha": "3" * 40,
                "path_prefix": "checkpoints/example.zip.part",
                "part_count": 2,
            },
        }
        base["venue_reconciliation"] = None
        base["conference_reconciliation"] = None
    if operation == OP_STAGE2_CENSUS:
        base["target_branch"] = "data/example-school-onboarding"
        base["target_sha"] = "6" * 40
        base["phase0_successor"] = {
            "path": ".remote-implementation/successors/example-school/phase0/successor-manifest.json",
            "sha256": "7" * 64,
        }
        base["integration_freeze_sha256"] = "8" * 64
        base["semantic_snapshot_sha256"] = "9" * 64
    if operation == OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE:
        base["target_branch"] = "data/example-school-onboarding"
        base["target_sha"] = "6" * 40
        base["stage2_census_checkpoint"] = {
            "path": ".remote-implementation/checkpoints/example-school/stage2/checkpoint-manifest.json",
            "sha256": "7" * 64,
        }
        base["integration_freeze_sha256"] = "8" * 64
        base["semantic_snapshot_sha256"] = "9" * 64
    if operation == OP_PHASE0:
        base["target_branch"] = "data/example-school-onboarding"
        base["stage1_checkpoint"] = {
            "path": ".remote-implementation/checkpoints/example-school/stage1/checkpoint-manifest.json",
            "sha256": "4" * 64,
        }
        base["history_scope"] = {
            "start_season": "2000-2001",
            "basis": "TOP_LEVEL_INTERVALS",
            "intervals": "2000-01+",
            "notes": "Owner-confirmed scope.",
        }
    if operation == OP_RECOVER:
        base["recovery"] = {
            "abandoned_request_id": "request-old",
            "lock_commit": LOCK,
            "target_branch": "data/example-school-onboarding",
        }
    return base


class RemoteImplementationControlTests(unittest.TestCase):
    def state_and_bytes(self):
        state = initial_control_state()
        data = canonical_json_bytes(state)
        return state, data

    def test_initial_state_is_valid_idle(self):
        state = initial_control_state()
        validate_control_state(state)
        self.assertEqual(state["kind"], CONTROL_KIND)
        self.assertEqual(state["lifecycle_state"], LIFECYCLE_IDLE)
        self.assertFalse(state["recovery_required"])

    def test_valid_bounded_stage1_request(self):
        validate_request(request(OP_STAGE1))

    def test_valid_bounded_phase0_request(self):
        validate_request(request(OP_PHASE0))

    def test_valid_bounded_stage2_census_request(self):
        validate_request(request(OP_STAGE2_CENSUS))

    def test_valid_stage2_opponent_display_request(self):
        validate_request(request(OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE))

    def test_stage2_opponent_display_requires_exact_census_checkpoint(self):
        req = request(OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE)
        req["stage2_census_checkpoint"]["sha256"] = "bad"
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_CENSUS_CHECKPOINT_SHA_INVALID",
        ):
            validate_request(req)

    def test_stage2_opponent_display_uses_global_mutation_lock(self):
        state = begin_request(
            initial_control_state(),
            request(
                OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
                "stage2-display-001",
            ),
            "7" * 64,
            run_id="205",
            run_attempt="1",
            request_commit="8" * 40,
        )
        self.assertEqual(state["lifecycle_state"], LIFECYCLE_ACTIVE)
        self.assertEqual(state["transaction_state"], "LOCKED")
        state = bind_lock_commit(state, LOCK)
        self.assertEqual(state["active_lock_commit"], LOCK)
        self.assertTrue(state["recovery_required"])

    def test_stage2_opponent_display_recovery_requires_exact_target_and_lock(self):
        state = begin_request(
            initial_control_state(),
            request(
                OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
                "stage2-display-old",
            ),
            "7" * 64,
            run_id="206",
            run_attempt="1",
            request_commit="8" * 40,
        )
        state = bind_lock_commit(state, LOCK)
        data = canonical_json_bytes(state)
        recovery = request(OP_RECOVER, "stage2-display-recovery")
        recovery["previous_control_state_sha256"] = sha256_bytes(data)
        recovery["recovery"] = {
            "abandoned_request_id": "stage2-display-old",
            "lock_commit": LOCK,
            "target_branch": "data/example-school-onboarding",
        }
        verify_request_predecessor(
            state,
            data,
            PRED,
            recovery,
            MAIN,
            allow_active_recovery=True,
        )

    def test_stage2_census_requires_exact_target_branch(self):
        req = request(OP_STAGE2_CENSUS)
        req["target_branch"] = "data/other-school-onboarding"
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_CENSUS_TARGET_BRANCH_INVALID",
        ):
            validate_request(req)

    def test_stage2_census_requires_target_sha(self):
        req = request(OP_STAGE2_CENSUS)
        req["target_sha"] = "not-a-sha"
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "STAGE2_CENSUS_TARGET_SHA_INVALID",
        ):
            validate_request(req)

    def test_stage2_census_is_read_only_serialized(self):
        state = begin_request(
            initial_control_state(),
            request(OP_STAGE2_CENSUS, "stage2-census-001"),
            "7" * 64,
            run_id="202",
            run_attempt="1",
            request_commit="8" * 40,
        )
        self.assertEqual(state["lifecycle_state"], "READ_ONLY_ACTIVE")
        self.assertEqual(
            state["transaction_state"],
            "STAGE2_CENSUS_RUNNING",
        )
        self.assertIsNone(state["active_lock_commit"])
        self.assertTrue(state["recovery_required"])

    def test_stale_predecessor_refused(self):
        state, data = self.state_and_bytes()
        req = request()
        req["previous_control_state_commit"] = "9" * 40
        req["previous_control_state_sha256"] = sha256_bytes(data)
        with self.assertRaisesRegex(RemoteImplementationError, "STALE_CONTROL_PREDECESSOR"):
            verify_request_predecessor(state, data, PRED, req, MAIN)

    def test_changed_main_refused(self):
        state, data = self.state_and_bytes()
        req = request()
        req["previous_control_state_sha256"] = sha256_bytes(data)
        with self.assertRaisesRegex(RemoteImplementationError, "CHANGED_PROTECTED_MAIN"):
            verify_request_predecessor(state, data, PRED, req, "8" * 40)

    def test_replayed_request_refused(self):
        state, data = self.state_and_bytes()
        state["consumed_request_ids"].append("request-001")
        data = canonical_json_bytes(state)
        req = request()
        req["previous_control_state_sha256"] = sha256_bytes(data)
        with self.assertRaisesRegex(RemoteImplementationError, "REQUEST_REPLAY_REFUSED"):
            verify_request_predecessor(state, data, PRED, req, MAIN)

    def test_global_lock_excludes_another_request(self):
        state, _ = self.state_and_bytes()
        first = request(OP_PHASE0, "request-first")
        active = begin_request(
            state,
            first,
            "5" * 64,
            run_id="100",
            run_attempt="1",
            request_commit="6" * 40,
        )
        active = bind_lock_commit(active, LOCK)
        data = canonical_json_bytes(active)
        second = request(OP_STAGE1, "request-second")
        second["previous_control_state_commit"] = PRED
        second["previous_control_state_sha256"] = sha256_bytes(data)
        with self.assertRaisesRegex(RemoteImplementationError, "GLOBAL_IMPLEMENTATION_LOCK_OCCUPIED"):
            verify_request_predecessor(active, data, PRED, second, MAIN)

    def test_stage2_census_blocks_another_implementation_transition(self):
        state = begin_request(
            initial_control_state(),
            request(OP_STAGE2_CENSUS, "stage2-active"),
            "7" * 64,
            run_id="203",
            run_attempt="1",
            request_commit="8" * 40,
        )
        data = canonical_json_bytes(state)
        second = request(OP_PHASE0, "phase0-second")
        second["previous_control_state_sha256"] = sha256_bytes(data)
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "GLOBAL_IMPLEMENTATION_LOCK_OCCUPIED",
        ):
            verify_request_predecessor(
                state,
                data,
                PRED,
                second,
                MAIN,
            )

    def test_stage2_census_read_only_recovery_is_exact(self):
        state = begin_request(
            initial_control_state(),
            request(OP_STAGE2_CENSUS, "stage2-old"),
            "7" * 64,
            run_id="204",
            run_attempt="1",
            request_commit="8" * 40,
        )
        data = canonical_json_bytes(state)
        recovery = request(OP_RECOVER, "stage2-recovery")
        recovery["previous_control_state_sha256"] = sha256_bytes(data)
        recovery["recovery"] = {
            "abandoned_request_id": "stage2-old",
            "lock_commit": None,
            "target_branch": None,
        }
        verify_request_predecessor(
            state,
            data,
            PRED,
            recovery,
            MAIN,
            allow_active_recovery=True,
        )

    def test_active_lock_persists_recovery_required(self):
        state = initial_control_state()
        active = begin_request(
            state,
            request(OP_PHASE0, "request-phase0"),
            "7" * 64,
            run_id="101",
            run_attempt="2",
            request_commit="8" * 40,
        )
        active = bind_lock_commit(active, LOCK)
        self.assertEqual(active["lifecycle_state"], LIFECYCLE_ACTIVE)
        self.assertTrue(active["recovery_required"])
        self.assertEqual(active["active_lock_commit"], LOCK)
        self.assertEqual(active["active_lock_owner"], "github-actions:101:2")

    def test_explicit_recovery_matches_exact_active_lock(self):
        state = begin_request(
            initial_control_state(),
            request(OP_PHASE0, "request-old"),
            "7" * 64,
            run_id="101",
            run_attempt="1",
            request_commit="8" * 40,
        )
        state = bind_lock_commit(state, LOCK)
        data = canonical_json_bytes(state)
        recovery = request(OP_RECOVER, "recovery-001")
        recovery["previous_control_state_sha256"] = sha256_bytes(data)
        verify_request_predecessor(
            state,
            data,
            PRED,
            recovery,
            MAIN,
            allow_active_recovery=True,
        )

    def test_read_only_stage1_recovery_uses_no_lock_or_target(self):
        state = begin_request(
            initial_control_state(),
            request(OP_STAGE1, "request-old"),
            "7" * 64,
            run_id="101",
            run_attempt="1",
            request_commit="8" * 40,
        )
        data = canonical_json_bytes(state)
        recovery = request(OP_RECOVER, "recovery-read-only")
        recovery["recovery"]["lock_commit"] = None
        recovery["recovery"]["target_branch"] = None
        recovery["previous_control_state_sha256"] = sha256_bytes(data)
        verify_request_predecessor(
            state,
            data,
            PRED,
            recovery,
            MAIN,
            allow_active_recovery=True,
        )

    def test_stale_recovery_lock_refused(self):
        state = begin_request(
            initial_control_state(),
            request(OP_PHASE0, "request-old"),
            "7" * 64,
            run_id="101",
            run_attempt="1",
            request_commit="8" * 40,
        )
        state = bind_lock_commit(state, LOCK)
        data = canonical_json_bytes(state)
        recovery = request(OP_RECOVER, "recovery-001")
        recovery["recovery"]["lock_commit"] = "9" * 40
        recovery["previous_control_state_sha256"] = sha256_bytes(data)
        with self.assertRaisesRegex(RemoteImplementationError, "STALE_RECOVERY_LOCK_MISMATCH"):
            verify_request_predecessor(
                state,
                data,
                PRED,
                recovery,
                MAIN,
                allow_active_recovery=True,
            )

    def test_recovery_abandon_returns_idle(self):
        state = begin_request(
            initial_control_state(),
            request(OP_PHASE0, "request-old"),
            "7" * 64,
            run_id="101",
            run_attempt="1",
            request_commit="8" * 40,
        )
        state = bind_lock_commit(state, LOCK)
        recovered = abandon_active(
            state,
            recovery_request_id="recovery-001",
            disposition="ABANDONED_PREPARED_NOT_PUBLISHED",
            recovery_manifest={"classification": MUTATION_PREPARED},
        )
        self.assertEqual(recovered["lifecycle_state"], LIFECYCLE_IDLE)
        self.assertIn("request-old", recovered["abandoned_request_ids"])
        self.assertIn("recovery-001", recovered["consumed_request_ids"])
        self.assertFalse(recovered["recovery_required"])

    def test_mutation_classification_not_attempted(self):
        self.assertEqual(
            classify_mutation(None, None),
            MUTATION_NOT_ATTEMPTED,
        )

    def test_mutation_classification_prepared_not_published(self):
        manifest = {
            "expected_target_predecessor_sha": None,
            "prepared_commit_sha": PREPARED,
        }
        self.assertEqual(
            classify_mutation(None, None, manifest=manifest),
            MUTATION_PREPARED,
        )

    def test_mutation_classification_published_not_finalized(self):
        manifest = {
            "expected_target_predecessor_sha": None,
            "prepared_commit_sha": PREPARED,
        }
        self.assertEqual(
            classify_mutation(None, PREPARED, manifest=manifest),
            MUTATION_PUBLISHED,
        )

    def test_mutation_classification_complete(self):
        manifest = {
            "expected_target_predecessor_sha": None,
            "prepared_commit_sha": PREPARED,
        }
        successor = {
            "prepared_commit_sha": PREPARED,
            "actual_published_target_sha": PREPARED,
            "final_transaction_state": "COMPLETE",
        }
        self.assertEqual(
            classify_mutation(
                None,
                PREPARED,
                manifest=manifest,
                successor=successor,
            ),
            MUTATION_COMPLETE,
        )

    def test_mutation_classification_divergence(self):
        manifest = {
            "expected_target_predecessor_sha": None,
            "prepared_commit_sha": PREPARED,
        }
        self.assertEqual(
            classify_mutation(
                None,
                "9" * 40,
                manifest=manifest,
            ),
            MUTATION_DIVERGED,
        )

    def test_exact_sidecar_hash_verification(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = root / "integration-freeze.json"
            payload.write_text('{"ok": true}\n', encoding="utf-8")
            manifest = {
                "sidecars": {
                    "integration-freeze.json": sha256_file(payload),
                }
            }
            verify_sidecar_hashes(manifest, root)

    def test_sidecar_hash_mismatch_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            payload = root / "integration-freeze.json"
            payload.write_text('{"ok": true}\n', encoding="utf-8")
            manifest = {
                "sidecars": {
                    "integration-freeze.json": "0" * 64,
                }
            }
            with self.assertRaisesRegex(RemoteImplementationError, "WRITEAHEAD_SIDECAR_HASH_MISMATCH"):
                verify_sidecar_hashes(manifest, root)

    def test_phase0_target_must_be_exact_school_branch(self):
        req = request(OP_PHASE0)
        req["target_branch"] = "data/other-school-onboarding"
        with self.assertRaisesRegex(RemoteImplementationError, "PHASE0_TARGET_BRANCH_INVALID"):
            validate_request(req)

    def test_stage1_cannot_carry_phase0_authority(self):
        req = request(OP_STAGE1)
        req["authority"]["phase0"] = True
        with self.assertRaisesRegex(RemoteImplementationError, "STAGE1_REQUEST_PHASE0_AUTHORITY_FORBIDDEN"):
            validate_request(req)


class RemoteImplementationGitCASTests(unittest.TestCase):
    def git(self, repo, *args, check=True):
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if check and cp.returncode != 0:
            self.fail(cp.stdout)
        return cp

    def make_repo(self):
        root = Path(tempfile.mkdtemp())
        bare = root / "origin.git"
        work = root / "work"
        self.git(root, "init", "--bare", str(bare))
        self.git(root, "init", str(work))
        self.git(work, "config", "user.name", "Test")
        self.git(work, "config", "user.email", "test@example.com")
        (work / "state.txt").write_text("one\n")
        self.git(work, "add", "state.txt")
        self.git(work, "commit", "-m", "one")
        self.git(work, "branch", "-M", "main")
        self.git(work, "remote", "add", "origin", str(bare))
        self.git(work, "push", "-u", "origin", "main")
        (work / "state.txt").write_text("two\n")
        self.git(work, "commit", "-am", "two")
        second = self.git(work, "rev-parse", "HEAD").stdout.strip()
        return root, bare, work, second

    def test_create_once_onboarding_branch(self):
        root, bare, work, prepared = self.make_repo()
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        publish_ref_cas(
            work,
            branch="data/example-school-onboarding",
            prepared_commit=prepared,
            expected_predecessor=None,
        )
        self.assertEqual(
            remote_head(work, "data/example-school-onboarding"),
            prepared,
        )

    def test_existing_ref_cas_success(self):
        root, bare, work, prepared = self.make_repo()
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        predecessor = self.git(
            work, "rev-parse", "origin/main"
        ).stdout.strip()
        publish_ref_cas(
            work,
            branch="main",
            prepared_commit=prepared,
            expected_predecessor=predecessor,
        )
        self.assertEqual(remote_head(work, "main"), prepared)

    def test_existing_ref_cas_stale_writer_refused(self):
        root, bare, work, prepared = self.make_repo()
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        stale = "1" * 40
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "TARGET_PUBLICATION_CAS_PRECONDITION_FAILED",
        ):
            publish_ref_cas(
                work,
                branch="main",
                prepared_commit=prepared,
                expected_predecessor=stale,
            )

    def test_existing_ref_mutation_classification(self):
        predecessor = "1" * 40
        manifest = {
            "expected_target_predecessor_sha": predecessor,
            "prepared_commit_sha": PREPARED,
        }
        self.assertEqual(
            classify_mutation(
                predecessor,
                predecessor,
                manifest=manifest,
            ),
            MUTATION_PREPARED,
        )
        self.assertEqual(
            classify_mutation(
                predecessor,
                PREPARED,
                manifest=manifest,
            ),
            MUTATION_PUBLISHED,
        )
        self.assertEqual(
            classify_mutation(
                predecessor,
                "9" * 40,
                manifest=manifest,
            ),
            MUTATION_DIVERGED,
        )

    def test_create_once_cas_race_refused(self):
        root, bare, work, prepared = self.make_repo()
        self.addCleanup(lambda: __import__("shutil").rmtree(root))
        publish_ref_cas(
            work,
            branch="data/example-school-onboarding",
            prepared_commit=prepared,
            expected_predecessor=None,
        )
        (work / "state.txt").write_text("three\n")
        self.git(work, "commit", "-am", "three")
        third = self.git(work, "rev-parse", "HEAD").stdout.strip()
        with self.assertRaisesRegex(RemoteImplementationError, "TARGET_PUBLICATION_CAS_PRECONDITION_FAILED"):
            publish_ref_cas(
                work,
                branch="data/example-school-onboarding",
                prepared_commit=third,
                expected_predecessor=None,
            )
        self.assertEqual(
            remote_head(work, "data/example-school-onboarding"),
            prepared,
        )


if __name__ == "__main__":
    unittest.main()
