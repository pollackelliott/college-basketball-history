#!/usr/bin/env python3
from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

REPO = os.environ.get("GITHUB_REPOSITORY", "pollackelliott/college-basketball-history")
CONTROL_BRANCH = "experiment/remote-implementation-proof6"
TARGET_BRANCH = "experiment/remote-implementation-proof6-liu-phase0"
REAL_BRANCH = "data/long-island-university-onboarding"
STATE_PATH = Path(".remote-implementation-poc/control6/control-state.json")
SCHOOL = "long-island-university"
EXPECTED_MAIN = "396ac80855a4d04c3b9a3f98f8c9a2516e9a1e97"
RESEARCH_BASE = "8aa88fb7e131aee333ba85ab0f3a52c8d1624c1e"
RESEARCH_ZIP_SHA = "c1e439ec668608271287bc41bde29453b22321e0d1d3d1a4a219e4c516ca60c2"
PROOF1_COMMIT = "c34ba9de312a97d03d910be40e8091c576080cfa"
DIAG = Path("/tmp/proof6-fresh-verify")
REQUIRED_FILES = ["conferences.csv","notes.md","opponents.csv","source-games.csv","source-notes.md","venues.csv"]


class Stop(Exception):
    pass


def run(cmd, *, cwd=None, check=True, text=True):
    cp = subprocess.run(cmd, cwd=cwd, text=text, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if check and cp.returncode != 0:
        output = cp.stdout if text else cp.stdout.decode("utf-8", errors="replace")
        raise Stop(f"command failed ({cp.returncode}): {' '.join(map(str,cmd))}\n{output}")
    return cp


def git(*args, cwd=None, check=True, text=True):
    return run(["git", *args], cwd=cwd, check=check, text=text)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical(obj) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(obj))


def remote_head(branch: str) -> str | None:
    cp = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    line = cp.stdout.strip()
    return line.split()[0] if line else None


def reconstruct_zip(out_path: Path) -> str:
    git("fetch", "--no-tags", "origin", "+refs/heads/experiment/remote-implementation-stage1:refs/remotes/origin/proof6-proof1")
    prefix = ".remote-implementation-poc/inputs/liu-research-frozen.zip.b64.part"
    parts = sorted(
        p for p in git("ls-tree","-r","--name-only",PROOF1_COMMIT,".remote-implementation-poc/inputs").stdout.splitlines()
        if p.startswith(prefix)
    )
    encoded = "".join(git("show",f"{PROOF1_COMMIT}:{p}").stdout for p in parts).encode("ascii")
    out_path.write_bytes(base64.b64decode(encoded))
    return sha256_file(out_path)


def main() -> int:
    DIAG.mkdir(parents=True, exist_ok=True)
    git("fetch","--no-tags","origin",
        "+refs/heads/main:refs/remotes/origin/proof6-live-main",
        f"+refs/heads/{CONTROL_BRANCH}:refs/remotes/origin/proof6-control",
        f"+refs/heads/{TARGET_BRANCH}:refs/remotes/origin/proof6-target")
    live_main = git("rev-parse","refs/remotes/origin/proof6-live-main").stdout.strip()
    control_head = git("rev-parse","refs/remotes/origin/proof6-control").stdout.strip()
    target_head = git("rev-parse","refs/remotes/origin/proof6-target").stdout.strip()
    if live_main != EXPECTED_MAIN:
        raise Stop("FRESH_VERIFY_MAIN_SHA_MISMATCH")
    if remote_head(REAL_BRANCH) is not None:
        raise Stop("FRESH_VERIFY_REAL_ONBOARDING_BRANCH_EXISTS")

    state = json.loads(git("show",f"{control_head}:{STATE_PATH.as_posix()}").stdout)
    if state.get("lifecycle_state") != "IDLE" or state.get("transaction_state") != "COMPLETE":
        raise Stop("FRESH_VERIFY_CONTROL_NOT_COMPLETE_IDLE")
    tx = state.get("last_transaction") or {}
    if tx.get("target_sha") != target_head or tx.get("phase0_commit_sha") != target_head:
        raise Stop("FRESH_VERIFY_TARGET_LINEAGE_MISMATCH")

    successor_path = tx["successor_manifest_path"]
    writeahead_path = tx["writeahead_manifest_path"]
    inputs_path = tx["inputs_path"]
    successor_bytes = git("show",f"{control_head}:{successor_path}",text=False).stdout
    successor = json.loads(successor_bytes)
    wa_bytes = git("show",f"{control_head}:{writeahead_path}",text=False).stdout
    wa = json.loads(wa_bytes)
    freeze_path = str(Path(writeahead_path).parent / "integration-freeze.json")
    freeze_bytes = git("show",f"{control_head}:{freeze_path}",text=False).stdout
    if sha256_bytes(freeze_bytes) != wa["integration_freeze_sha256"]:
        raise Stop("FRESH_VERIFY_INTEGRATION_FREEZE_HASH_MISMATCH")
    integration = json.loads(freeze_bytes)

    for name, expected in [
        ("venue-reconciliation.json", wa["venue_reconciliation_sha256"]),
        ("conference-reconciliation.json", wa["conference_reconciliation_sha256"]),
        ("stage1-reconciliation.json", wa["stage1_reconciliation_sha256"]),
    ]:
        data = git("show",f"{control_head}:{inputs_path}/{name}",text=False).stdout
        if sha256_bytes(data) != expected:
            raise Stop(f"FRESH_VERIFY_INPUT_HASH_MISMATCH: {name}")
    stage1 = json.loads(git("show",f"{control_head}:{inputs_path}/stage1-reconciliation.json").stdout)
    if stage1.get("status") != "PASS" or stage1.get("blocker_count") != 0:
        raise Stop("FRESH_VERIFY_STAGE1_NOT_PASS")

    prepared = wa["prepared_phase0_commit_sha"]
    if target_head != prepared or successor.get("phase0_commit_sha") != prepared:
        raise Stop("FRESH_VERIFY_PUBLISHED_COMMIT_MISMATCH")
    parent = git("rev-parse",f"{prepared}^").stdout.strip()
    tree = git("rev-parse",f"{prepared}^{{tree}}").stdout.strip()
    if parent != wa["prepared_phase0_parent_sha"] or tree != wa["prepared_phase0_tree_sha"]:
        raise Stop("FRESH_VERIFY_COMMIT_STRUCTURE_MISMATCH")
    changed = sorted(
        x.strip() for x in git("diff-tree","--no-commit-id","--name-only","-r",prepared).stdout.splitlines()
        if x.strip()
    )
    if changed != sorted(wa["changed_paths"]):
        raise Stop("FRESH_VERIFY_CHANGED_PATH_MISMATCH")
    for path, expected in wa["changed_file_sha256"].items():
        data = git("show",f"{prepared}:{path}",text=False).stdout
        if sha256_bytes(data) != expected:
            raise Stop(f"FRESH_VERIFY_CHANGED_FILE_HASH_MISMATCH: {path}")

    if integration.get("integration_base_sha") != live_main or integration.get("origin_main_sha") != live_main:
        raise Stop("FRESH_VERIFY_INTEGRATION_BASE_MISMATCH")
    if integration.get("research_zip_sha256") != RESEARCH_ZIP_SHA or integration.get("research_base_sha") != RESEARCH_BASE:
        raise Stop("FRESH_VERIFY_RESEARCH_BINDING_MISMATCH")
    scope = integration.get("history_scope") or {}
    if scope.get("history_scope_intervals") != "1928-29..1950-51|1968-69+":
        raise Stop("FRESH_VERIFY_SCOPE_MISMATCH")

    zip_path = Path(tempfile.mkdtemp(prefix="proof6-fresh-zip-")) / "liu-research-frozen.zip"
    if reconstruct_zip(zip_path) != RESEARCH_ZIP_SHA:
        raise Stop("FRESH_VERIFY_RESEARCH_FREEZE_SHA_MISMATCH")

    verify_tree = Path(tempfile.mkdtemp(prefix="proof6-fresh-target-"))
    shutil.rmtree(verify_tree)
    git("worktree","add","--detach",str(verify_tree),prepared)
    validate = run([sys.executable,"tools/validate_data.py"],cwd=verify_tree,check=False)
    (DIAG / "validate-data.log").write_text(validate.stdout,encoding="utf-8")
    if validate.returncode != 0:
        raise Stop("FRESH_VERIFY_REPOSITORY_VALIDATION_FAILED\n"+validate.stdout[-8000:])

    package_hashes = integration.get("package_member_sha256") or {}
    for name in REQUIRED_FILES:
        data = (verify_tree / "schools" / SCHOOL / name).read_bytes()
        if sha256_bytes(data) != package_hashes.get(name):
            raise Stop(f"FRESH_VERIFY_PACKAGE_MEMBER_HASH_MISMATCH: {name}")

    sem_script = """
import json, sys
from pathlib import Path
root=Path(sys.argv[1])
sys.path.insert(0,str(root/'tools'))
from integration_freeze_guard import build_source_game_semantic_snapshot, semantic_snapshot_sha256
snap=build_source_game_semantic_snapshot(root/'schools'/'long-island-university'/'source-games.csv')
print(json.dumps({'hash':semantic_snapshot_sha256(snap),'snapshot':snap},sort_keys=True))
"""
    sem = run([sys.executable,"-c",sem_script,str(verify_tree)])
    sem_obj = json.loads(sem.stdout)
    guard = integration.get("source_game_semantic_guard") or {}
    if sem_obj["hash"] != guard.get("snapshot_sha256") or sem_obj["snapshot"] != guard.get("snapshot"):
        raise Stop("FRESH_VERIFY_SEMANTIC_SNAPSHOT_MISMATCH")

    programs = list(csv.DictReader((verify_tree/"data/reference/programs.csv").open(encoding="utf-8-sig",newline="")))
    prog = next(row for row in programs if row.get("program_key") == SCHOOL)
    if (
        prog.get("history_start_season") != "1928-1929"
        or prog.get("history_scope_status") != "OWNER_CONFIRMED"
        or prog.get("history_scope_basis") != "TOP_LEVEL_INTERVALS"
        or prog.get("history_scope_intervals") != "1928-29..1950-51|1968-69+"
    ):
        raise Stop("FRESH_VERIFY_PROGRAM_SCOPE_MISMATCH")
    scope_rows = list(csv.DictReader((verify_tree/"data/reference/program-top-level-scope.csv").open(encoding="utf-8-sig",newline="")))
    top = next(row for row in scope_rows if row.get("school") == "Long Island University")
    if top.get("top_level_scope") != "1947-48..1950-51|1968-69+":
        raise Stop("FRESH_VERIFY_SCOPE_REFERENCE_DEBT_CHANGED_UNEXPECTEDLY")

    if sha256_bytes(successor_bytes) != tx.get("successor_manifest_sha256"):
        raise Stop("FRESH_VERIFY_SUCCESSOR_HASH_MISMATCH")
    if sha256_bytes(wa_bytes) != tx.get("writeahead_manifest_sha256"):
        raise Stop("FRESH_VERIFY_WRITEAHEAD_HASH_MISMATCH")

    verification = {
        "schema_version": 1,
        "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF6_FRESH_RUNNER_VERIFICATION",
        "request_id": tx["request_id"],
        "protected_main_sha": live_main,
        "target_branch": TARGET_BRANCH,
        "target_sha": target_head,
        "phase0_commit_sha": prepared,
        "phase0_tree_sha": tree,
        "phase0_parent_sha": parent,
        "changed_paths": changed,
        "integration_freeze_sha256": wa["integration_freeze_sha256"],
        "research_freeze_sha256": RESEARCH_ZIP_SHA,
        "venue_reconciliation_sha256": wa["venue_reconciliation_sha256"],
        "conference_reconciliation_sha256": wa["conference_reconciliation_sha256"],
        "stage1_status": "PASS",
        "repository_validation": "PASS",
        "semantic_snapshot_sha256": guard["snapshot_sha256"],
        "package_member_hashes_verified": True,
        "exact_integration_freeze_bytes_reconstructed": True,
        "scope_reference_debt_preserved_not_mutated": True,
        "real_onboarding_branch_exists": False,
        "global_lifecycle": "IDLE",
        "remote_phase0_equivalence": "PASS",
        "equivalence_basis": (
            "Exact protected-main base, exact Research Freeze, exact hash-bound reconciliation inputs, "
            "unchanged permanent stage_research_portfolio.py --apply --commit, permanent validation, "
            "Phase 0 changed-path contract, exact ignored Integration Freeze bytes, and fresh-runner "
            "reconstruction all match repository acceptance invariants. Commit author/timestamp metadata "
            "is execution-environment provenance and does not alter the accepted tree or Integration Freeze semantics."
        ),
        "authority_statement": "Disposable rehearsal evidence only; no authoritative LIU Integration Freeze or real Phase 0.",
    }

    verify_dir = Path(f".remote-implementation-poc/control6/verification/{tx['request_id']}")
    write_json(verify_dir/"fresh-verification.json",verification)
    summary = {
        "schema_version": 1,
        "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF6_SUMMARY",
        "result": "REMOTE IMPLEMENTATION PROOF 6: PASS",
        "protected_main_sha": live_main,
        "control_branch": CONTROL_BRANCH,
        "disposable_target_branch": TARGET_BRANCH,
        "request_id": tx["request_id"],
        "global_lock_result": "ACQUIRED_THROUGH_FINALIZATION_RELEASED_IDLE",
        "research_freeze_sha256": RESEARCH_ZIP_SHA,
        "venue_reconciliation_sha256": wa["venue_reconciliation_sha256"],
        "conference_reconciliation_sha256": wa["conference_reconciliation_sha256"],
        "final_reconciled_stage1_status": "PASS",
        "permanent_phase0_command": wa["permanent_command"],
        "phase0_commit_sha": prepared,
        "phase0_tree_sha": tree,
        "phase0_parent_sha": parent,
        "changed_paths": changed,
        "repository_validation": "PASS",
        "integration_freeze_sha256": wa["integration_freeze_sha256"],
        "writeahead_manifest_sha256": tx["writeahead_manifest_sha256"],
        "successor_manifest_sha256": tx["successor_manifest_sha256"],
        "fresh_runner_reconstruction": "PASS",
        "remote_phase0_equivalence": "PASS",
        "global_final_lifecycle": "IDLE",
        "protected_main_mutated": False,
        "real_liu_onboarding_branch_exists": False,
        "owner_desktop_interaction_required": False,
        "owner_github_ui_interaction_required": False,
        "architecture_ready_for_real_liu_remote_phase0": True,
        "remaining_safety_gap": (
            "No architecture-level remote-transaction gap remains. Real LIU execution still requires the ordinary "
            "repository/Control Center authority to resolve the settled stale program-top-level-scope reference debt "
            "at the policy-required real integration boundary and explicit authorization to begin the real Implementation mutation."
        ),
    }
    write_json(Path(".remote-implementation-poc/control6/proof6-summary.json"),summary)

    git("config","user.name","github-actions[bot]")
    git("config","user.email","41898282+github-actions[bot]@users.noreply.github.com")
    git("add","--",str(verify_dir),".remote-implementation-poc/control6/proof6-summary.json")
    git("commit","-m",f"[proof6-internal] persist fresh-runner equivalence proof {tx['request_id']}")
    new_head=git("rev-parse","HEAD").stdout.strip()
    push=git(
        "push",
        f"--force-with-lease=refs/heads/{CONTROL_BRANCH}:{control_head}",
        "origin",
        f"{new_head}:refs/heads/{CONTROL_BRANCH}",
        check=False,
    )
    if push.returncode != 0:
        raise Stop("FRESH_VERIFY_CONTROL_CAS_FAILED\n"+push.stdout)

    print("FRESH RUNNER RECONSTRUCTION: PASS")
    print("REMOTE PHASE 0 EQUIVALENCE: PASS")
    print(f"FINAL VERIFICATION COMMIT: {new_head}")
    return 0


if __name__ == "__main__":
    try:
        rc=main()
    except Stop as exc:
        DIAG.mkdir(parents=True,exist_ok=True)
        (DIAG/"stop.txt").write_text(str(exc)+"\n",encoding="utf-8")
        print(f"STOP: {exc}")
        rc=1
    sys.exit(rc)
