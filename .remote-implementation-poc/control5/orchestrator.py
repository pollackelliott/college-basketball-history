#!/usr/bin/env python3
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = os.environ.get("GITHUB_REPOSITORY", "pollackelliott/college-basketball-history")
CONTROL_BRANCH = "experiment/remote-implementation-proof5"
TARGET_BRANCH = "experiment/remote-implementation-proof5-target"
STATE_PATH = Path(".remote-implementation-poc/control5/control-state.json")
REQUEST_PATH = Path(".remote-implementation-poc/control5/request.json")
CLASSIFIER = Path(".remote-implementation-poc/control5/classify_mutation.py")
DIAG = Path("/tmp/proof5-diagnostics")
TARGET_PATH = ".remote-implementation-poc/proof5-target/state.json"
EXPECTED_MAIN = "396ac80855a4d04c3b9a3f98f8c9a2516e9a1e97"


class Stop(Exception):
    pass


def run(cmd, *, check=True, env=None, input_text=None):
    cp = subprocess.run(
        cmd,
        text=True,
        input=input_text,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    if check and cp.returncode != 0:
        raise Stop(f"command failed ({cp.returncode}): {' '.join(cmd)}\n{cp.stdout}")
    return cp


def git(*args, check=True, env=None, input_text=None):
    return run(["git", *args], check=check, env=env, input_text=input_text)


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def sha256_file(path):
    return sha256_bytes(Path(path).read_bytes())


def canonical(obj):
    return (json.dumps(obj, indent=2, sort_keys=True) + "\n").encode("utf-8")


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, obj):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_bytes(canonical(obj))


def git_show(commit, path):
    cp = git("show", f"{commit}:{path}")
    return cp.stdout


def remote_head(branch):
    cp = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    line = cp.stdout.strip()
    if not line:
        return None
    return line.split()[0]


def configure_git():
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")


def push_control(expected_remote):
    new_head = git("rev-parse", "HEAD").stdout.strip()
    cp = git(
        "push",
        f"--force-with-lease=refs/heads/{CONTROL_BRANCH}:{expected_remote}",
        "origin",
        f"{new_head}:refs/heads/{CONTROL_BRANCH}",
        check=False,
    )
    if cp.returncode != 0:
        raise Stop("CONTROL_REF_CAS_FAILED\n" + cp.stdout)
    return new_head


def commit_control(expected_remote, message, paths):
    for path in paths:
        git("add", "--", str(path))
    git("commit", "-m", message)
    return push_control(expected_remote)


def load_state_at(commit):
    return json.loads(git_show(commit, STATE_PATH.as_posix()))


def verify_common(state, state_commit, state_bytes, request, live_main):
    if state.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF5_GLOBAL_CONTROL":
        raise Stop("CONTROL_KIND_MISMATCH")
    if state.get("global_lock_scope") != "ONE_ACTIVE_IMPLEMENTATION_PROJECT_WIDE":
        raise Stop("CONTROL_SCOPE_MISMATCH")
    if state.get("integration_frozen") is not False or state.get("phase0_authorized") is not False:
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if request.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF5_REQUEST":
        raise Stop("REQUEST_KIND_MISMATCH")
    authority = request.get("authority") or {}
    if authority.get("experimental_control_only") is not True:
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if authority.get("basketball_mutation_authorized") is not False:
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if authority.get("integration_freeze_authorized") is not False:
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if authority.get("phase0_authorized") is not False:
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if request.get("previous_control_state_commit") != state_commit:
        raise Stop("STALE_CONTROL_STATE")
    if request.get("previous_control_state_sha256") != sha256_bytes(state_bytes):
        raise Stop("STALE_CONTROL_STATE_HASH")
    if request.get("expected_protected_main_sha") != state.get("expected_protected_main_sha"):
        raise Stop("MAIN_SHA_MISMATCH")
    if live_main != request.get("expected_protected_main_sha"):
        raise Stop("MAIN_SHA_MISMATCH")


def request_used(state, request_id):
    return (
        request_id == state.get("active_request_id")
        or request_id in set(state.get("accepted_request_ids") or [])
        or request_id in set(state.get("abandoned_request_ids") or [])
        or request_id in set(state.get("consumed_request_ids") or [])
    )


def bind_lock(state, request, request_sha, run_id, attempt):
    rid = request["request_id"]
    accepted = list(state.get("accepted_request_ids") or [])
    accepted.append(rid)
    state.update({
        "accepted_request_ids": accepted,
        "lifecycle_state": "ACTIVE",
        "transaction_state": "LOCKED",
        "active_request_id": rid,
        "active_fixture_id": request["fixture_id"],
        "active_operation": request["operation"],
        "active_boundary": request["boundary"],
        "active_lock_owner": f"github-actions:{run_id}:{attempt}",
        "active_request_sha256": request_sha,
        "active_target_predecessor_sha": request["expected_target_predecessor_sha"],
        "recovery_required": True,
        "lock_acquired_run_id": int(run_id),
        "lock_acquired_run_attempt": int(attempt),
        "lock_acquisition_request_commit": os.environ["GITHUB_SHA"],
    })


def make_prepared(request):
    pred = request["expected_target_predecessor_sha"]
    target_bytes = canonical(request["target_payload"])
    sidecar_bytes = canonical(request["sidecar_payload"])
    tmp = Path(tempfile.mkdtemp(prefix="proof5-prepare-"))
    target_file = tmp / "target-state.json"
    sidecar_file = tmp / "synthetic-integration-authority.json"
    target_file.write_bytes(target_bytes)
    sidecar_file.write_bytes(sidecar_bytes)

    index = tmp / "index"
    env_index = os.environ.copy()
    env_index["GIT_INDEX_FILE"] = str(index)
    git("read-tree", f"{pred}^{{tree}}", env=env_index)
    blob = git("hash-object", "-w", str(target_file)).stdout.strip()
    git("update-index", "--add", "--cacheinfo", f"100644,{blob},{TARGET_PATH}", env=env_index)
    tree = git("write-tree", env=env_index).stdout.strip()

    commit_env = os.environ.copy()
    meta = request["commit_metadata"]
    commit_env.update({
        "GIT_AUTHOR_NAME": meta["author_name"],
        "GIT_AUTHOR_EMAIL": meta["author_email"],
        "GIT_AUTHOR_DATE": meta["timestamp"],
        "GIT_COMMITTER_NAME": meta["committer_name"],
        "GIT_COMMITTER_EMAIL": meta["committer_email"],
        "GIT_COMMITTER_DATE": meta["timestamp"],
    })
    commit = git(
        "commit-tree", tree, "-p", pred, "-m", request["commit_message"],
        env=commit_env,
    ).stdout.strip()
    return {
        "tmp": tmp,
        "target_file": target_file,
        "sidecar_file": sidecar_file,
        "target_bytes": target_bytes,
        "sidecar_bytes": sidecar_bytes,
        "target_sha256": sha256_bytes(target_bytes),
        "sidecar_sha256": sha256_bytes(sidecar_bytes),
        "target_blob_sha": blob,
        "tree_sha": tree,
        "commit_sha": commit,
    }


def reconstruct_prepared(manifest, bundle):
    target_file = bundle / manifest["target_payload_file"]
    pred = manifest["expected_target_predecessor_sha"]
    tmp = Path(tempfile.mkdtemp(prefix="proof5-reconstruct-"))
    index = tmp / "index"
    env_index = os.environ.copy()
    env_index["GIT_INDEX_FILE"] = str(index)
    git("read-tree", f"{pred}^{{tree}}", env=env_index)
    blob = git("hash-object", "-w", str(target_file)).stdout.strip()
    git("update-index", "--add", "--cacheinfo", f"100644,{blob},{TARGET_PATH}", env=env_index)
    tree = git("write-tree", env=env_index).stdout.strip()
    meta = manifest["commit_metadata"]
    env_commit = os.environ.copy()
    env_commit.update({
        "GIT_AUTHOR_NAME": meta["author_name"],
        "GIT_AUTHOR_EMAIL": meta["author_email"],
        "GIT_AUTHOR_DATE": meta["timestamp"],
        "GIT_COMMITTER_NAME": meta["committer_name"],
        "GIT_COMMITTER_EMAIL": meta["committer_email"],
        "GIT_COMMITTER_DATE": meta["timestamp"],
    })
    commit = git(
        "commit-tree", tree, "-p", pred, "-m", manifest["commit_message"],
        env=env_commit,
    ).stdout.strip()
    if tree != manifest["prepared_tree_sha"] or commit != manifest["prepared_commit_sha"]:
        raise Stop("PREPARED_COMMIT_RECONSTRUCTION_MISMATCH")
    return tree, commit


def classify(expected_pred, actual_target, manifest_path=None, successor_path=None):
    cmd = [
        sys.executable, CLASSIFIER.as_posix(),
        "--expected-predecessor", expected_pred,
        "--actual-target", actual_target,
    ]
    if manifest_path:
        cmd += ["--manifest", str(manifest_path)]
    if successor_path:
        cmd += ["--successor", str(successor_path)]
    return run(cmd).stdout.strip().splitlines()[-1]


def verify_failed_run(run_id, attempt):
    cp = run([
        "gh", "api",
        f"repos/{REPO}/actions/runs/{run_id}/attempts/{attempt}",
    ])
    data = json.loads(cp.stdout)
    if data.get("status") != "completed" or data.get("conclusion") != "failure":
        raise Stop("FAILED_RUN_NOT_COMPLETED_FAILURE")


def clear_active(state):
    for key in [
        "active_request_id", "active_fixture_id", "active_operation", "active_boundary",
        "active_lock_owner", "active_request_sha256", "active_target_predecessor_sha",
        "active_prepared_commit_sha", "active_prepared_tree_sha",
        "active_target_payload_sha256", "active_sidecar_sha256",
        "active_writeahead_commit", "active_writeahead_manifest_path",
        "active_writeahead_manifest_sha256", "active_lock_commit",
    ]:
        state[key] = None
    for key in [
        "lock_acquired_run_id", "lock_acquired_run_attempt",
        "lock_acquisition_request_commit"
    ]:
        state.pop(key, None)
    state["recovery_required"] = False
    state["lifecycle_state"] = "IDLE"


def main():
    DIAG.mkdir(parents=True, exist_ok=True)
    if not REQUEST_PATH.exists():
        print("Proof 5 infrastructure-only push; no request.")
        return 0

    configure_git()
    request = read_json(REQUEST_PATH)
    rid = request["request_id"]
    run_id = int(os.environ["GITHUB_RUN_ID"])
    attempt = int(os.environ["GITHUB_RUN_ATTEMPT"])

    git("fetch", "--no-tags", "origin",
        "+refs/heads/main:refs/remotes/origin/proof5-live-main",
        f"+refs/heads/{CONTROL_BRANCH}:refs/remotes/origin/proof5-control",
        f"+refs/heads/{TARGET_BRANCH}:refs/remotes/origin/proof5-target")
    live_main = git("rev-parse", "refs/remotes/origin/proof5-live-main").stdout.strip()
    durable_head = git("rev-parse", "refs/remotes/origin/proof5-control").stdout.strip()

    if attempt > 1:
        durable_state = load_state_at(durable_head)
        if request_used(durable_state, rid):
            msg = f"ACCEPTED_MUTATION_REQUEST_REPLAY: REJECTED — {rid} has durable prior acceptance"
            print(msg)
            (DIAG / "rerun-guard.txt").write_text(msg + "\n")
            return 42
        raise Stop("RERUN_GUARD_UNEXPECTEDLY_CLEAR")

    prior_commit = git("rev-parse", f"{os.environ['GITHUB_SHA']}^").stdout.strip()
    state_bytes = git_show(prior_commit, STATE_PATH.as_posix()).encode("utf-8")
    state = json.loads(state_bytes)
    verify_common(state, prior_commit, state_bytes, request, live_main)

    operation = request["operation"]
    request_sha = sha256_file(REQUEST_PATH)

    if operation.startswith("FAIL_BOUNDARY_"):
        if state.get("lifecycle_state") != "IDLE" or state.get("active_request_id") is not None:
            raise Stop("IMPLEMENTATION_LOCK_OCCUPIED")
        if request_used(state, rid):
            raise Stop("ACCEPTED_MUTATION_REQUEST_REPLAY")
        actual_target = remote_head(TARGET_BRANCH)
        if actual_target != request["expected_target_predecessor_sha"]:
            raise Stop("TARGET_PREDECESSOR_MISMATCH")

        bind_lock(state, request, request_sha, run_id, attempt)
        write_json(STATE_PATH, state)
        lock_commit = commit_control(
            os.environ["GITHUB_SHA"],
            f"[proof5-internal] acquire global mutation lock {rid}",
            [STATE_PATH],
        )

        state["active_lock_commit"] = lock_commit
        write_json(STATE_PATH, state)
        lock_bound_commit = commit_control(
            lock_commit,
            f"[proof5-internal] bind mutation lock identity {rid}",
            [STATE_PATH],
        )
        print(f"PASS: durable global lock acquired {lock_commit}")
        print(f"PASS: active lock state bound {lock_bound_commit}")

        boundary = request["boundary"]
        if boundary == "A":
            print("INTENTIONAL PROOF 5 FAILURE A: before preparation/write-ahead publication")
            return 41

        prepared = make_prepared(request)
        wa_dir = Path(f".remote-implementation-poc/control5/writeahead/{rid}")
        wa_dir.mkdir(parents=True, exist_ok=True)
        target_copy = wa_dir / "target-state.json"
        sidecar_copy = wa_dir / "synthetic-integration-authority.json"
        shutil.copyfile(prepared["target_file"], target_copy)
        shutil.copyfile(prepared["sidecar_file"], sidecar_copy)

        manifest = {
            "schema_version": 1,
            "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF5_WRITEAHEAD",
            "request_id": rid,
            "request_sha256": request_sha,
            "fixture_id": request["fixture_id"],
            "operation": operation,
            "boundary": boundary,
            "global_lock_commit": lock_commit,
            "protected_main_sha": live_main,
            "target_branch": TARGET_BRANCH,
            "expected_target_predecessor_sha": request["expected_target_predecessor_sha"],
            "isolated_preparation_base_sha": request["expected_target_predecessor_sha"],
            "allowed_changed_paths": [TARGET_PATH],
            "target_payload_file": target_copy.name,
            "target_payload_sha256": prepared["target_sha256"],
            "target_payload_git_blob_sha": prepared["target_blob_sha"],
            "sidecar_authority_file": sidecar_copy.name,
            "sidecar_authority_sha256": prepared["sidecar_sha256"],
            "prepared_commit_sha": prepared["commit_sha"],
            "prepared_tree_sha": prepared["tree_sha"],
            "commit_message": request["commit_message"],
            "commit_metadata": request["commit_metadata"],
            "mutation_state": "PREPARED_NOT_PUBLISHED",
            "authority_statement": "Experimental synthetic mutation only; no basketball or real Implementation mutation authorized."
        }
        manifest_path = wa_dir / "writeahead-manifest.json"
        write_json(manifest_path, manifest)
        manifest_sha = sha256_file(manifest_path)
        (wa_dir / "writeahead-manifest.sha256").write_text(
            f"{manifest_sha}  writeahead-manifest.json\n"
        )

        state.update({
            "transaction_state": "PREPARED_NOT_PUBLISHED",
            "active_prepared_commit_sha": prepared["commit_sha"],
            "active_prepared_tree_sha": prepared["tree_sha"],
            "active_target_payload_sha256": prepared["target_sha256"],
            "active_sidecar_sha256": prepared["sidecar_sha256"],
            "active_writeahead_manifest_path": manifest_path.as_posix(),
            "active_writeahead_manifest_sha256": manifest_sha,
        })
        write_json(STATE_PATH, state)
        writeahead_commit = commit_control(
            lock_bound_commit,
            f"[proof5-internal] publish write-ahead authority {rid}",
            [STATE_PATH, wa_dir],
        )
        state["active_writeahead_commit"] = writeahead_commit
        write_json(STATE_PATH, state)
        writeahead_bound_commit = commit_control(
            writeahead_commit,
            f"[proof5-internal] bind write-ahead commit {rid}",
            [STATE_PATH],
        )
        print(f"PASS: write-ahead durable before target publication: {writeahead_commit}")
        print(f"prepared_commit={prepared['commit_sha']}")
        print(f"prepared_tree={prepared['tree_sha']}")
        print(f"writeahead_manifest_sha256={manifest_sha}")

        if boundary == "B":
            print("INTENTIONAL PROOF 5 FAILURE B: prepared/write-ahead durable, target not published")
            return 42

        if boundary != "C":
            raise Stop("UNKNOWN_FAILURE_BOUNDARY")

        publish = git(
            "push",
            f"--force-with-lease=refs/heads/{TARGET_BRANCH}:{request['expected_target_predecessor_sha']}",
            "origin",
            f"{prepared['commit_sha']}:refs/heads/{TARGET_BRANCH}",
            check=False,
        )
        if publish.returncode != 0:
            raise Stop("TARGET_PUBLICATION_CAS_FAILED\n" + publish.stdout)
        git("fetch", "--no-tags", "origin",
            f"+refs/heads/{TARGET_BRANCH}:refs/remotes/origin/proof5-target")
        actual = git("rev-parse", "refs/remotes/origin/proof5-target").stdout.strip()
        if actual != prepared["commit_sha"]:
            raise Stop("TARGET_PUBLICATION_VERIFY_FAILED")
        print(f"PASS: exact prepared commit atomically published {actual}")

        # Deliberately do not update the control branch after target publication.
        # Recovery must discover publication by comparing the target ref with write-ahead authority.
        print("INTENTIONAL PROOF 5 FAILURE C: target published, no successor/final checkpoint")
        return 43

    if operation == "RECOVER_MUTATION_TRANSACTION":
        if state.get("lifecycle_state") != "ACTIVE":
            raise Stop("RECOVERY_PREDECESSOR_STALE")
        if request["original_request_id"] != state.get("active_request_id"):
            raise Stop("RECOVERY_AUTHORITY_MISMATCH")
        if request["active_lock_commit"] != state.get("active_lock_commit"):
            raise Stop("RECOVERY_AUTHORITY_MISMATCH")
        if int(request["failed_action_run_id"]) != int(state.get("lock_acquired_run_id", -1)):
            raise Stop("RECOVERY_AUTHORITY_MISMATCH")
        if int(request["failed_action_run_attempt"]) != int(state.get("lock_acquired_run_attempt", -1)):
            raise Stop("RECOVERY_AUTHORITY_MISMATCH")
        verify_failed_run(request["failed_action_run_id"], request["failed_action_run_attempt"])

        actual_target = remote_head(TARGET_BRANCH)
        expected_pred = state["active_target_predecessor_sha"]
        manifest_path = Path(state["active_writeahead_manifest_path"]) if state.get("active_writeahead_manifest_path") else None
        manifest = None
        if manifest_path:
            if not manifest_path.exists():
                raise Stop("WRITEAHEAD_MANIFEST_MISSING")
            if sha256_file(manifest_path) != state["active_writeahead_manifest_sha256"]:
                raise Stop("WRITEAHEAD_MANIFEST_HASH_MISMATCH")
            manifest = read_json(manifest_path)
            bundle = manifest_path.parent
            if sha256_file(bundle / manifest["target_payload_file"]) != manifest["target_payload_sha256"]:
                raise Stop("WRITEAHEAD_PAYLOAD_HASH_MISMATCH")
            if sha256_file(bundle / manifest["sidecar_authority_file"]) != manifest["sidecar_authority_sha256"]:
                raise Stop("WRITEAHEAD_SIDECAR_HASH_MISMATCH")
            reconstruct_prepared(manifest, bundle)

        classification = classify(expected_pred, actual_target, manifest_path)
        print(f"MUTATION_STATE: {classification}")
        if classification != request["expected_classification"]:
            raise Stop(f"RECOVERY_CLASSIFICATION_MISMATCH expected={request['expected_classification']} actual={classification}")

        recovery_dir = Path(f".remote-implementation-poc/control5/recoveries/{request['request_id']}")
        recovery_dir.mkdir(parents=True, exist_ok=True)

        if classification in ("NOT_ATTEMPTED", "PREPARED_NOT_PUBLISHED"):
            if actual_target != expected_pred:
                raise Stop("RECOVERY_TARGET_NOT_AT_PREDECESSOR")
            disposition = (
                "ABANDON_NOT_ATTEMPTED"
                if classification == "NOT_ATTEMPTED"
                else "ABANDON_PREPARED_NOT_PUBLISHED"
            )
            abandoned = list(state.get("abandoned_request_ids") or [])
            abandoned.append(state["active_request_id"])
            consumed = list(state.get("consumed_request_ids") or [])
            consumed.append(request["request_id"])
            original = state["active_request_id"]
            state["abandoned_request_ids"] = abandoned
            state["consumed_request_ids"] = consumed
            state["current_sequence"] = int(state.get("current_sequence", 0)) + 1
            state["last_transaction"] = {
                "original_request_id": original,
                "classification": classification,
                "recovery_request_id": request["request_id"],
                "recovery_disposition": disposition,
                "target_sha": actual_target,
                "basketball_data_mutation": False
            }
            clear_active(state)
            state["transaction_state"] = "IDLE"
            recovery_manifest = {
                "schema_version": 1,
                "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF5_RECOVERY",
                "original_request_id": original,
                "recovery_request_id": request["request_id"],
                "classification": classification,
                "recovery_disposition": disposition,
                "target_sha": actual_target,
                "expected_target_predecessor_sha": expected_pred,
                "writeahead_manifest_sha256": manifest and sha256_file(manifest_path),
                "failed_action_run_id": request["failed_action_run_id"],
                "failed_action_run_attempt": request["failed_action_run_attempt"],
                "recovery_action_run_id": run_id,
                "recovery_action_run_attempt": attempt,
                "basketball_data_mutation": False,
                "final_global_lifecycle": "IDLE"
            }
            write_json(recovery_dir / "recovery-manifest.json", recovery_manifest)
            write_json(STATE_PATH, state)
            recovery_commit = commit_control(
                os.environ["GITHUB_SHA"],
                f"[proof5-internal] recover {classification.lower()} {original}",
                [STATE_PATH, recovery_dir],
            )
            print(f"RECOVERY_DISPOSITION: {disposition}")
            print(f"PASS: recovery returned global lifecycle to IDLE at {recovery_commit}")
            return 0

        if classification != "PUBLISHED_NOT_FINALIZED":
            raise Stop("RECOVERY_REFUSES_DIVERGED_TARGET")

        prepared = manifest["prepared_commit_sha"]
        if actual_target != prepared:
            raise Stop("PUBLISHED_TARGET_NOT_EXACT_PREPARED_COMMIT")
        parent = git("rev-parse", f"{prepared}^").stdout.strip()
        tree = git("rev-parse", f"{prepared}^{{tree}}").stdout.strip()
        if parent != expected_pred or tree != manifest["prepared_tree_sha"]:
            raise Stop("PUBLISHED_COMMIT_STRUCTURE_MISMATCH")
        changed = [
            x for x in git("diff-tree", "--no-commit-id", "--name-only", "-r", prepared).stdout.splitlines()
            if x.strip()
        ]
        if changed != manifest["allowed_changed_paths"]:
            raise Stop("PUBLISHED_CHANGED_PATH_ALLOWLIST_MISMATCH")

        divergence = classify(expected_pred, "1111111111111111111111111111111111111111", manifest_path)
        if divergence != "DIVERGED_STOP":
            raise Stop("DIVERGENCE_NEGATIVE_TEST_FAILED")
        print("MUTATION_TARGET_DIVERGED: STOP — synthetic negative classification PASS")

        # Demonstrate stale target writer rejection using the old predecessor lease.
        stale_payload = canonical({"proof": 5, "state": "STALE_WRITER_SHOULD_NOT_WIN"})
        tmp = Path(tempfile.mkdtemp(prefix="proof5-stale-writer-"))
        stale_file = tmp / "state.json"
        stale_file.write_bytes(stale_payload)
        idx = tmp / "index"
        env_idx = os.environ.copy()
        env_idx["GIT_INDEX_FILE"] = str(idx)
        git("read-tree", f"{expected_pred}^{{tree}}", env=env_idx)
        stale_blob = git("hash-object", "-w", str(stale_file)).stdout.strip()
        git("update-index", "--add", "--cacheinfo", f"100644,{stale_blob},{TARGET_PATH}", env=env_idx)
        stale_tree = git("write-tree", env=env_idx).stdout.strip()
        meta = manifest["commit_metadata"]
        env_commit = os.environ.copy()
        env_commit.update({
            "GIT_AUTHOR_NAME": meta["author_name"],
            "GIT_AUTHOR_EMAIL": meta["author_email"],
            "GIT_AUTHOR_DATE": meta["timestamp"],
            "GIT_COMMITTER_NAME": meta["committer_name"],
            "GIT_COMMITTER_EMAIL": meta["committer_email"],
            "GIT_COMMITTER_DATE": meta["timestamp"],
        })
        stale_commit = git(
            "commit-tree", stale_tree, "-p", expected_pred,
            "-m", "Proof 5 stale target writer candidate",
            env=env_commit,
        ).stdout.strip()
        cas = git(
            "push",
            f"--force-with-lease=refs/heads/{TARGET_BRANCH}:{expected_pred}",
            "origin",
            f"{stale_commit}:refs/heads/{TARGET_BRANCH}",
            check=False,
        )
        if cas.returncode == 0:
            raise Stop("TARGET_REF_CAS_FAILED_TO_REJECT_STALE_WRITER")
        print("TARGET_REF_CAS: PASS")

        original = state["active_request_id"]
        successor_dir = Path(f".remote-implementation-poc/control5/successors/{original}")
        successor_dir.mkdir(parents=True, exist_ok=True)
        successor = {
            "schema_version": 1,
            "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF5_SUCCESSOR",
            "predecessor_control_state_commit": request["previous_control_state_commit"],
            "original_mutation_request_id": original,
            "original_mutation_request_sha256": state["active_request_sha256"],
            "original_lock_commit": state["active_lock_commit"],
            "writeahead_commit": state["active_writeahead_commit"],
            "writeahead_manifest_sha256": state["active_writeahead_manifest_sha256"],
            "prepared_commit_sha": manifest["prepared_commit_sha"],
            "prepared_tree_sha": manifest["prepared_tree_sha"],
            "actual_published_target_sha": actual_target,
            "expected_target_predecessor_sha": expected_pred,
            "allowed_changed_paths": manifest["allowed_changed_paths"],
            "target_payload_sha256": manifest["target_payload_sha256"],
            "sidecar_authority_sha256": manifest["sidecar_authority_sha256"],
            "failed_action_run_id": request["failed_action_run_id"],
            "failed_action_run_attempt": request["failed_action_run_attempt"],
            "recovery_request_id": request["request_id"],
            "recovery_request_commit": os.environ["GITHUB_SHA"],
            "recovery_action_run_id": run_id,
            "recovery_action_run_attempt": attempt,
            "recovery_disposition": "ADOPT_EXACT_PUBLISHED_MUTATION",
            "divergence_test": "DIVERGED_STOP",
            "target_ref_cas": "PASS",
            "final_transaction_state": "COMPLETE",
            "final_global_lifecycle": "IDLE",
            "basketball_data_mutation": False,
            "integration_frozen": False,
            "phase0_authorized": False
        }
        successor_path = successor_dir / "successor-manifest.json"
        write_json(successor_path, successor)
        successor_sha = sha256_file(successor_path)
        (successor_dir / "successor-manifest.sha256").write_text(
            f"{successor_sha}  successor-manifest.json\n"
        )
        complete_class = classify(expected_pred, actual_target, manifest_path, successor_path)
        if complete_class != "COMPLETE":
            raise Stop("COMPLETE_CLASSIFIER_FAILED")
        print("MUTATION_STATE: COMPLETE")

        consumed = list(state.get("consumed_request_ids") or [])
        consumed.extend([original, request["request_id"]])
        state["consumed_request_ids"] = consumed
        state["current_sequence"] = int(state.get("current_sequence", 0)) + 1
        state["last_transaction"] = {
            "original_request_id": original,
            "classification_before_recovery": classification,
            "recovery_request_id": request["request_id"],
            "recovery_disposition": "ADOPT_EXACT_PUBLISHED_MUTATION",
            "prepared_commit_sha": prepared,
            "successor_manifest_sha256": successor_sha,
            "target_sha": actual_target,
            "basketball_data_mutation": False
        }
        clear_active(state)
        state["transaction_state"] = "COMPLETE"
        write_json(STATE_PATH, state)

        recovery_manifest = {
            "schema_version": 1,
            "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF5_RECOVERY",
            "classification": classification,
            "recovery_disposition": "ADOPT_EXACT_PUBLISHED_MUTATION",
            "original_request_id": original,
            "recovery_request_id": request["request_id"],
            "prepared_commit_sha": prepared,
            "actual_target_sha": actual_target,
            "successor_manifest_sha256": successor_sha,
            "failed_action_run_id": request["failed_action_run_id"],
            "failed_action_run_attempt": request["failed_action_run_attempt"],
            "recovery_action_run_id": run_id,
            "target_ref_cas": "PASS",
            "divergence_test": "DIVERGED_STOP",
            "basketball_data_mutation": False
        }
        write_json(recovery_dir / "recovery-manifest.json", recovery_manifest)
        recovery_commit = commit_control(
            os.environ["GITHUB_SHA"],
            f"[proof5-internal] adopt exact published mutation {original}",
            [STATE_PATH, successor_dir, recovery_dir],
        )
        print("RECOVERY_DISPOSITION: ADOPT_EXACT_PUBLISHED_MUTATION")
        print(f"PASS: durable successor checkpoint committed at {recovery_commit}")
        return 0

    raise Stop(f"OPERATION_NOT_ALLOWED: {operation}")


if __name__ == "__main__":
    try:
        rc = main()
    except Stop as exc:
        DIAG.mkdir(parents=True, exist_ok=True)
        (DIAG / "stop.txt").write_text(str(exc) + "\n")
        print(f"STOP: {exc}")
        rc = 1
    sys.exit(rc)
