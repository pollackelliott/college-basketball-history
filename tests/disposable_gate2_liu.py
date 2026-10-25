#!/usr/bin/env python3
"""ONE SHOT: read-only LIU Gate 2 authentication on real merged-main candidate.

Never creates a control request, approval record, PR, merge, or deployment.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_control import sha256_bytes
from remote_implementation_io import git_show_bytes
from remote_implementation_production import approve_exact_gate2

SCHOOL = "long-island-university"
PR = 367
HEAD = "38ad43f63fcc852bf927501338dc9d24f4ea2498"
MAIN = "b3cdaee2c8306fda1c51a4247028bf58c9e03531"
PLAN = "7ed1c916f96d5b01016b9b1df56e1a82f4c0505802ed9654c086289a605f6e5f"
RELEASE = "1d8ce94e1437b571a046b0497ecaedd47512cf5d33eb7ced49ea4e536fa5c3f0"
PREVIEW_ID = 7306788588
PREVIEW_URL = "https://college-basketball-history-bxrz17y4c-elliott-pollacks-projects.vercel.app"
SOURCE_ID = "liu-release-preview-verify-0001"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def main():
    git("fetch", "--no-tags", "origin",
        "+refs/heads/main:refs/remotes/origin/main",
        "+refs/heads/control/remote-implementation:refs/remotes/origin/remote-control",
        "+refs/heads/data/long-island-university-onboarding:refs/remotes/origin/remote-liu")
    assert git("rev-parse", "refs/remotes/origin/main") == MAIN
    assert git("rev-parse", "refs/remotes/origin/remote-liu") == HEAD
    control = git("rev-parse", "refs/remotes/origin/remote-control")
    state = json.loads(git_show_bytes(control, ".remote-implementation/control-state.json", cwd=ROOT))
    assert state["lifecycle_state"] == "IDLE" and state["transaction_state"] == "COMPLETE"
    assert state["recovery_required"] is False
    assert state["last_operation"]["operation"] == "RELEASE_PREVIEW_VERIFY"
    assert state["last_operation"]["remote_release_preview_equivalence"] == "PASS"
    prefix = f".remote-implementation/checkpoints/{SCHOOL}/{SOURCE_ID}"
    checkpoint = prefix + "/checkpoint-manifest.json"
    verification = f".remote-implementation/verifications/{SCHOOL}/{SOURCE_ID}/release-preview-verification.json"
    cb = git_show_bytes(control, checkpoint, cwd=ROOT)
    vb = git_show_bytes(control, verification, cwd=ROOT)
    request = {
        "school_key": SCHOOL,
        "target_branch": f"data/{SCHOOL}-onboarding",
        "target_sha": HEAD,
        "expected_protected_main_sha": MAIN,
        "pr_number": PR,
        "preview_deployment_id": PREVIEW_ID,
        "preview_url": PREVIEW_URL,
        "approved_plan_hash": PLAN,
        "release_manifest_sha256": RELEASE,
        "release_preview_checkpoint": {
            "path": checkpoint, "sha256": sha256_bytes(cb),
        },
        "release_preview_verification": {
            "path": verification, "sha256": sha256_bytes(vb),
        },
        # Synthetic in disposable test only; not a persisted owner approval.
        "owner_gate_2_approval": {
            "approved": True, "approval_basis": "DISPOSABLE TEST ONLY",
            "preview_checkpoint_sha256": sha256_bytes(cb),
            "preview_verification_sha256": sha256_bytes(vb),
            "pr_number": PR, "pr_head_sha": HEAD,
            "preview_deployment_id": PREVIEW_ID, "preview_url": PREVIEW_URL,
        },
    }
    result = approve_exact_gate2(request, control, repo=ROOT)
    assert result["pr_number"] == PR
    assert result["target_sha"] == HEAD
    assert result["preview_deployment_id"] == PREVIEW_ID
    assert result["merged"] is False
    assert result["production_proof"] is False
    assert git("rev-parse", "refs/remotes/origin/main") == MAIN
    assert git("rev-parse", "refs/remotes/origin/remote-liu") == HEAD
    print("DISPOSABLE_LIU_GATE2_CHAIN_PASS")
    print("PR_EXACT_HEAD=" + HEAD)
    print("PREVIEW_DEPLOYMENT_ID=" + str(PREVIEW_ID))


if __name__ == "__main__":
    main()
