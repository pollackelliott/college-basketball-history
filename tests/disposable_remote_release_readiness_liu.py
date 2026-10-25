#!/usr/bin/env python3
"""Single-use disposable LIU regression for generic remote release readiness.

Never writes target/control refs or opens a PR. Delete this test after proof
has been captured durably; it is not a school-specific production dependency.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_control import sha256_bytes
from remote_implementation_io import git_show_bytes
from remote_implementation_release_readiness import (
    run_permanent_release_readiness, verify_release_readiness_authority
)
from remote_implementation_stage2_census import add_existing_onboarding_worktree

SCHOOL = "long-island-university"
REQUEST_ID = "liu-stage2-sealed-apply-0001"
BRANCH = "data/long-island-university-onboarding"
MAIN = "802de9cbe0b779da0bad55c71969d3337fa62e82"
TARGET = "38ad43f63fcc852bf927501338dc9d24f4ea2498"
TREE = "5ca3666d2078e1aaf64bd147e3127d90a031efdd"
APPROVED = "7ed1c916f96d5b01016b9b1df56e1a82f4c0505802ed9654c086289a605f6e5f"
MANIFEST_HASH = "1d8ce94e1437b571a046b0497ecaedd47512cf5d33eb7ced49ea4e536fa5c3f0"


def execute(*args):
    result = subprocess.run(["git", *args], cwd=ROOT, check=True,
                            text=True, capture_output=True)
    return result.stdout.strip()


def main():
    execute("fetch", "--no-tags", "origin",
            "+refs/heads/main:refs/remotes/origin/main",
            "+refs/heads/control/remote-implementation:refs/remotes/origin/remote-control",
            "+refs/heads/data/long-island-university-onboarding:refs/remotes/origin/remote-target")
    assert execute("rev-parse", "refs/remotes/origin/main") == MAIN, "protected main drift"
    assert execute("rev-parse", "refs/remotes/origin/remote-target") == TARGET, "LIU ref drift"
    control = execute("rev-parse", "refs/remotes/origin/remote-control")
    state = json.loads(git_show_bytes(control, ".remote-implementation/control-state.json", cwd=ROOT))
    assert state["lifecycle_state"] == "IDLE"
    assert state["transaction_state"] == "COMPLETE"
    assert state["recovery_required"] is False
    last = state.get("last_operation", {})
    assert last["operation"] == "STAGE2_SEALED_APPLY"
    assert last["request_id"] == REQUEST_ID
    assert last["fresh_runner_verification"] == "PASS"
    assert last["remote_stage2_sealed_apply_equivalence"] == "PASS"
    assert last["target_sha"] == TARGET

    sp = f".remote-implementation/successors/{SCHOOL}/{REQUEST_ID}/successor-manifest.json"
    vp = f".remote-implementation/verifications/{SCHOOL}/{REQUEST_ID}/stage2-sealed-apply-verification.json"
    sb = git_show_bytes(control, sp, cwd=ROOT)
    vb = git_show_bytes(control, vp, cwd=ROOT)
    request = {
        "school_key": SCHOOL,
        "target_branch": BRANCH,
        "target_sha": TARGET,
        "expected_protected_main_sha": MAIN,
        "approved_plan_hash": APPROVED,
        "release_manifest_sha256": MANIFEST_HASH,
        "stage2_apply_successor": {"path": sp, "sha256": sha256_bytes(sb)},
        "stage2_apply_verification": {"path": vp, "sha256": sha256_bytes(vb)},
    }
    authority = verify_release_readiness_authority(request, control, source_repo=ROOT)
    assert authority["changed_path_count"] == 87
    wt = add_existing_onboarding_worktree(BRANCH, TARGET, SCHOOL, source_repo=ROOT)
    try:
        report = run_permanent_release_readiness(
            authority, worktree=wt, artifact_dir=wt / ".onboarding" / SCHOOL
        )
        assert report["status"] == "RELEASE_READINESS_PASS"
        assert report["tracked_mutation"] == "NONE"
        assert report["pr_created"] is False
        assert report["preview_verified"] is False
        assert report["owner_gate_2"] is False
        assert execute("rev-parse", "refs/remotes/origin/remote-target") == TARGET
        assert execute("rev-parse", "refs/remotes/origin/main") == MAIN
        print("DISPOSABLE_LIU_RELEASE_READINESS_PASS")
        print("APPLY_SUCCESSOR=" + TARGET)
        print("MAIN=" + MAIN)
        print("CHANGED_PATHS=" + str(report["changed_path_count"]))
        print("APPROVED_PLAN_HASH=" + APPROVED)
    finally:
        subprocess.run(["git", "worktree", "remove", "--force", str(wt)],
                       cwd=ROOT, text=True, capture_output=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
