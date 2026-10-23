#!/usr/bin/env python3
"""Temporary pre-merge real-tool regression for remote Implementation productionization.

All mutation refs are published only to a local bare Git repository under /tmp.
Nothing in this script pushes a school branch to GitHub.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path.cwd()
ARCH_BRANCH = "tooling/remote-implementation-control-plane"
CONTROL_BRANCH = "control/remote-implementation"
MAIN_SHA = "e7d64d5971d02c5949a1a06539e3e3b641999190"
PROOF1_COMMIT = "c34ba9de312a97d03d910be40e8091c576080cfa"
PROOF6_COMMIT = "146812469962f8c5c4ddc3ed7d0fb30f2e6a5538"
RESEARCH_SHA = "c1e439ec668608271287bc41bde29453b22321e0d1d3d1a4a219e4c516ca60c2"
RESEARCH_BASE = "8aa88fb7e131aee333ba85ab0f3a52c8d1624c1e"
VENUE_SHA = "c07b06387f75c829188800404719f2aa897612008fea19f647de8fbb4ecd0d92"
CONFERENCE_SHA = "62271fed5e97cfd26d9056efd5c24bccb65944a4f17fe7aac695b81082d1722b"
PROOF6_TREE = "f53fbf5436ab4056232c6771b52105e52af9318c"
PROOF6_FREEZE_SHA = "a0db804501dc12f1e3ef060e60821c1971a4814e3fc8d3209513009cd6ac3e06"
SEMANTIC_SHA = "3e9c996db3cc0089c5e314c851309c818dbdbf0f04724676d9eaf28b649ee3d0"
TARGET = "data/long-island-university-onboarding"
VENUE_PROOF_PATH = (
    ".remote-implementation-poc/control6/inputs/proof6-liu-phase0-0002/"
    "venue-reconciliation.json"
)
CONFERENCE_PROOF_PATH = (
    ".remote-implementation-poc/control6/inputs/proof6-liu-phase0-0002/"
    "conference-reconciliation.json"
)
FREEZE_PROOF_PATH = (
    ".remote-implementation-poc/control6/writeahead/proof6-liu-phase0-0002/"
    "integration-freeze.json"
)
PREFIX = ".remote-implementation-poc/inputs/liu-research-frozen.zip.b64.part"
EXPECTED_CHANGED = [
    "data/reference/programs.csv",
    "data/reference/venue-names.csv",
    "data/reference/venues.csv",
    "schools/long-island-university/conferences.csv",
    "schools/long-island-university/notes.md",
    "schools/long-island-university/opponents.csv",
    "schools/long-island-university/source-games.csv",
    "schools/long-island-university/source-notes.md",
    "schools/long-island-university/venues.csv",
]


def run(cmd, cwd=None, env=None, check=True):
    cp = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if check and cp.returncode != 0:
        raise RuntimeError(
            "command failed (%s): %s\n%s"
            % (cp.returncode, " ".join(str(x) for x in cmd), cp.stdout)
        )
    return cp


def git(cwd, *args, check=True):
    return run(["git", *args], cwd=cwd, check=check)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_show(cwd, commit, path):
    cp = subprocess.run(
        ["git", "show", "%s:%s" % (commit, path)],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return cp.stdout


def configure(cwd):
    git(cwd, "config", "user.name", "Remote Regression")
    git(cwd, "config", "user.email", "remote-regression@example.com")


def clone(bare, dest):
    run(["git", "clone", str(bare), str(dest)])
    configure(dest)


def state_bytes(repo):
    return (repo / ".remote-implementation/control-state.json").read_bytes()


def request_base(repo, operation, request_id):
    predecessor = git(repo, "rev-parse", "HEAD").stdout.strip()
    return {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": request_id,
        "school_key": "long-island-university",
        "operation": operation,
        "previous_control_state_commit": predecessor,
        "previous_control_state_sha256": sha256(state_bytes(repo)),
        "expected_protected_main_sha": MAIN_SHA,
        "creation_provenance": {
            "origin": "productionization-real-tool-regression",
            "authorization": "Non-authoritative disposable LIU regression only.",
        },
        "authority": {
            "owner_gate_1": False,
            "owner_gate_2": False,
            "release": False,
            "phase0": operation == "PHASE0",
            "recovery": False,
        },
        "research_checkpoint": {
            "sha256": RESEARCH_SHA,
            "research_base_sha": RESEARCH_BASE,
            "transport": {
                "kind": "git_base64_parts",
                "commit_sha": PROOF1_COMMIT,
                "path_prefix": PREFIX,
                "part_count": 9,
            },
        },
        "venue_reconciliation": {
            "path": ".remote-implementation/payloads/liu/venue-reconciliation.json",
            "sha256": VENUE_SHA,
        },
        "conference_reconciliation": {
            "path": ".remote-implementation/payloads/liu/conference-reconciliation.json",
            "sha256": CONFERENCE_SHA,
        },
    }


def commit_request(repo, request, message):
    path = repo / ".remote-implementation/request.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(request, indent=2, sort_keys=True) + "\n")
    git(repo, "add", "--", ".remote-implementation")
    git(repo, "commit", "-m", message)
    commit = git(repo, "rev-parse", "HEAD").stdout.strip()
    git(repo, "push", "origin", "HEAD:refs/heads/%s" % CONTROL_BRANCH)
    return commit


def runner_env(commit, run_id):
    env = os.environ.copy()
    env.update(
        {
            "REMOTE_IMPLEMENTATION_CONTROL_BRANCH": CONTROL_BRANCH,
            "GITHUB_SHA": commit,
            "GITHUB_RUN_ID": str(run_id),
            "GITHUB_RUN_ATTEMPT": "1",
            "REMOTE_IMPLEMENTATION_DIAG": "/tmp/remote-implementation-regression-%s"
            % run_id,
        }
    )
    return env


def normalize_freeze(value):
    value = json.loads(json.dumps(value))
    for key in ("venue_reconciliation", "conference_reconciliation"):
        meta = value.get(key)
        if isinstance(meta, dict):
            meta.pop("spec_path", None)
    return value


def main():
    root = Path(tempfile.mkdtemp(prefix="remote-production-regression-"))
    bare = root / "origin.git"
    try:
        # Bring accepted experimental evidence into this checkout only as source refs.
        git(REPO, "fetch", "--no-tags", "origin", "experiment/remote-implementation-stage1")
        git(REPO, "fetch", "--no-tags", "origin", "experiment/remote-implementation-proof6")
        git(REPO, "branch", "-f", "regression-main-source", MAIN_SHA)
        git(REPO, "branch", "-f", "regression-proof1-source", PROOF1_COMMIT)
        git(REPO, "branch", "-f", "regression-proof6-source", PROOF6_COMMIT)

        run(["git", "clone", "--bare", str(REPO), str(bare)])
        git(bare, "update-ref", "refs/heads/main", MAIN_SHA)
        git(bare, "update-ref", "refs/heads/regression-proof1", PROOF1_COMMIT)
        git(bare, "update-ref", "refs/heads/regression-proof6", PROOF6_COMMIT)

        # Seed the production control branch from the candidate code with exact IDLE state.
        init = root / "init"
        clone(bare, init)
        git(init, "checkout", ARCH_BRANCH)
        git(init, "checkout", "-b", CONTROL_BRANCH)
        state_dir = init / ".remote-implementation"
        state_dir.mkdir()
        shutil.copyfile(
            init / "config/remote-implementation-control-state.initial.json",
            state_dir / "control-state.json",
        )
        git(init, "add", "--", ".remote-implementation/control-state.json")
        git(
            init,
            "commit",
            "-m",
            "[remote-implementation-internal] initialize regression control state",
        )
        git(init, "push", "-u", "origin", CONTROL_BRANCH)

        # Stage 1 request on a fresh runner clone.
        stage1 = root / "stage1"
        clone(bare, stage1)
        git(stage1, "checkout", CONTROL_BRANCH)
        payload_dir = stage1 / ".remote-implementation/payloads/liu"
        payload_dir.mkdir(parents=True, exist_ok=True)
        venue_bytes = git_show(stage1, PROOF6_COMMIT, VENUE_PROOF_PATH)
        conference_bytes = git_show(
            stage1, PROOF6_COMMIT, CONFERENCE_PROOF_PATH
        )
        assert sha256(venue_bytes) == VENUE_SHA
        assert sha256(conference_bytes) == CONFERENCE_SHA
        (payload_dir / "venue-reconciliation.json").write_bytes(venue_bytes)
        (payload_dir / "conference-reconciliation.json").write_bytes(
            conference_bytes
        )
        stage1_request = request_base(
            stage1, "STAGE1_INVENTORY", "production-regression-liu-stage1"
        )
        stage1_commit = commit_request(
            stage1,
            stage1_request,
            "Productionized remote Stage 1 LIU regression request",
        )
        cp = run(
            [sys.executable, "tools/remote_implementation_runner.py"],
            cwd=stage1,
            env=runner_env(stage1_commit, 92001),
            check=False,
        )
        print(cp.stdout)
        assert cp.returncode == 0, cp.stdout

        # Phase 0 request on a completely fresh runner clone.
        phase0 = root / "phase0"
        clone(bare, phase0)
        git(phase0, "checkout", CONTROL_BRANCH)
        state = json.loads(state_bytes(phase0))
        last = state["last_operation"]
        assert state["lifecycle_state"] == "IDLE"
        assert last["operation"] == "STAGE1_INVENTORY"
        assert last["stage1_status"] == "PASS"
        phase0_request = request_base(
            phase0, "PHASE0", "production-regression-liu-phase0"
        )
        phase0_request["target_branch"] = TARGET
        phase0_request["stage1_checkpoint"] = {
            "path": last["checkpoint_manifest_path"],
            "sha256": last["checkpoint_manifest_sha256"],
        }
        phase0_request["history_scope"] = {
            "start_season": "1928-1929",
            "basis": "TOP_LEVEL_INTERVALS",
            "intervals": "1928-29..1950-51|1968-69+",
            "notes": (
                "Owner-confirmed LIU top-level scope: 1928-29 through 1950-51 "
                "and 1968-69 onward; 1951-52 through 1967-68 excluded. "
                "Proof 6 disposable rehearsal only."
            ),
        }
        phase0_commit = commit_request(
            phase0,
            phase0_request,
            "Productionized remote Phase 0 LIU regression request",
        )
        cp = run(
            [sys.executable, "tools/remote_implementation_runner.py"],
            cwd=phase0,
            env=runner_env(phase0_commit, 92002),
            check=False,
        )
        print(cp.stdout)
        assert cp.returncode == 0, cp.stdout

        # Fresh verification from another destroyed-runner-equivalent clone.
        verify = root / "verify"
        clone(bare, verify)
        git(verify, "checkout", CONTROL_BRANCH)
        env = os.environ.copy()
        env["REMOTE_IMPLEMENTATION_CONTROL_BRANCH"] = CONTROL_BRANCH
        env["REMOTE_IMPLEMENTATION_DIAG"] = (
            "/tmp/remote-implementation-regression-verify"
        )
        cp = run(
            [sys.executable, "tools/remote_implementation_verify.py"],
            cwd=verify,
            env=env,
            check=False,
        )
        print(cp.stdout)
        assert cp.returncode == 0, cp.stdout

        # Durable final-state/equivalence assertions.
        final_control = (
            git(bare, "rev-parse", "refs/heads/%s" % CONTROL_BRANCH)
            .stdout.strip()
        )
        target = git(bare, "rev-parse", "refs/heads/%s" % TARGET).stdout.strip()
        main_sha = git(bare, "rev-parse", "refs/heads/main").stdout.strip()
        assert main_sha == MAIN_SHA

        state_doc = json.loads(
            git_show(bare, final_control, ".remote-implementation/control-state.json")
        )
        assert state_doc["lifecycle_state"] == "IDLE"
        assert state_doc["active_request_id"] is None
        assert state_doc["recovery_required"] is False
        final = state_doc["last_operation"]
        assert final["operation"] == "PHASE0"
        assert final["fresh_runner_verification"] == "PASS"
        assert final["remote_phase0_equivalence"] == "PASS"
        assert final["target_sha"] == target

        target_parent = git(bare, "rev-parse", "%s^" % target).stdout.strip()
        target_tree = git(
            bare, "rev-parse", "%s^{tree}" % target
        ).stdout.strip()
        assert target_parent == MAIN_SHA
        assert target_tree == PROOF6_TREE, (target_tree, PROOF6_TREE)

        changed = sorted(
            x
            for x in git(
                bare,
                "diff-tree",
                "--no-commit-id",
                "--name-only",
                "-r",
                target,
            ).stdout.splitlines()
            if x
        )
        assert changed == EXPECTED_CHANGED, changed

        wa_path = final["writeahead_manifest_path"]
        wa = json.loads(git_show(bare, final_control, wa_path))
        assert wa["semantic_snapshot_sha256"] == SEMANTIC_SHA
        assert wa["repository_validation"] == "PASS"
        assert wa["changed_paths"] == EXPECTED_CHANGED
        assert (
            wa["venue_reconciliation"]["spec_sha256"] == VENUE_SHA
        )
        assert (
            wa["conference_reconciliation"]["spec_sha256"]
            == CONFERENCE_SHA
        )
        assert (
            wa["history_scope"]["history_scope_intervals"]
            == "1928-29..1950-51|1968-69+"
        )

        new_freeze_path = (
            Path(wa_path).parent / "integration-freeze.json"
        ).as_posix()
        new_freeze_bytes = git_show(bare, final_control, new_freeze_path)
        accepted_freeze_bytes = git_show(
            bare, PROOF6_COMMIT, FREEZE_PROOF_PATH
        )
        accepted_freeze = json.loads(accepted_freeze_bytes)
        new_freeze = json.loads(new_freeze_bytes)
        assert normalize_freeze(new_freeze) == normalize_freeze(
            accepted_freeze
        )
        print(
            "ACCEPTED_PROOF6_INTEGRATION_FREEZE_SHA256=%s"
            % PROOF6_FREEZE_SHA
        )
        print(
            "PRODUCTIONIZED_REGRESSION_INTEGRATION_FREEZE_SHA256=%s"
            % sha256(new_freeze_bytes)
        )
        print("PRODUCTIONIZED_REMOTE_PHASE0_TREE=%s" % target_tree)
        print("PRODUCTIONIZED_REMOTE_PHASE0_TARGET=%s" % target)
        print("PRODUCTIONIZED_LIU_DISPOSABLE_EQUIVALENCE=PASS")
        print("PRODUCTIONIZED_CONTROL_FINAL_LIFECYCLE=IDLE")
        return 0
    finally:
        shutil.rmtree(root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
