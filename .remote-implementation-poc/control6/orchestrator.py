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
REQUEST_PATH = Path(".remote-implementation-poc/control6/request.json")
DIAG = Path("/tmp/proof6-diagnostics")
SCHOOL = "long-island-university"
EXPECTED_MAIN = "e7d64d5971d02c5949a1a06539e3e3b641999190"
RESEARCH_BASE = "8aa88fb7e131aee333ba85ab0f3a52c8d1624c1e"
RESEARCH_ZIP_SHA = "c1e439ec668608271287bc41bde29453b22321e0d1d3d1a4a219e4c516ca60c2"
ORIGINAL_STAGE1_BASE = "396ac80855a4d04c3b9a3f98f8c9a2516e9a1e97"
EXPECTED_VENUE_RECON_SHA = "c07b06387f75c829188800404719f2aa897612008fea19f647de8fbb4ecd0d92"
EXPECTED_CONFERENCE_RECON_SHA = "62271fed5e97cfd26d9056efd5c24bccb65944a4f17fe7aac695b81082d1722b"
PROOF1_COMMIT = "c34ba9de312a97d03d910be40e8091c576080cfa"
PROOF2_CHECKPOINT = "32f11c925f0b17b1840a58f06ec848b20a20cdd7"
PROOF2_STAGE1_PATH = ".remote-implementation-poc/checkpoints/long-island-university/proof1/stage1-reconciliation.json"
REQUIRED_FILES = [
    "conferences.csv",
    "notes.md",
    "opponents.csv",
    "source-games.csv",
    "source-notes.md",
    "venues.csv",
]
CONTRACT_ALLOWED = {
    "data/reference/programs.csv",
    "data/reference/venues.csv",
    "data/reference/venue-names.csv",
    "data/reference/conferences.csv",
    *{f"schools/{SCHOOL}/{name}" for name in REQUIRED_FILES},
}
VENUE_REUSE = {
    "liu-schwartz": ("VEN-000949", "schwartz-athletic-center"),
    "liu-wellness": ("VEN-000611", "steinberg-wellness-center"),
    "liu-barclays": ("VEN-000020", "barclays-center"),
    "uab-arena-bartow": ("VEN-000527", "bartow-arena"),
    "special-events-arena-hawaii": ("VEN-000194", "stan-sheriff-center"),
    "sun-dome-tampa": ("VEN-000238", "yuengling-center"),
    "wells-fargo-arena-asu": ("VEN-000056", "desert-financial-arena"),
    "ucf-arena": ("VEN-000038", "cfe-arena"),
    "liu-boston-garden": ("VEN-000313", "boston-garden"),
    "wagner-spiro-sports-center": ("VEN-000914", "spiro-sports-center"),
    "fdu-rothman-center": ("VEN-000916", "bogota-savings-bank-center"),
    "quinnipiac-td-bank-sports-center": ("VEN-000918", "m-t-bank-arena"),
    "robert-morris-upmc-events-center": ("VEN-000907", "upmc-events-center"),
    "saint-francis-pa-degol-arena": ("VEN-000911", "degol-arena"),
    "loyola-reitz-arena": ("VEN-000925", "reitz-arena-loyola-maryland"),
    "charlotte-coliseum-original": ("VEN-000040", "charlotte-coliseum-1955"),
    "time-warner-cable-arena-charlotte": ("VEN-000190", "spectrum-center"),
}


class Stop(Exception):
    pass


def run(cmd, *, cwd=None, check=True, env=None, text=True, input_data=None):
    cp = subprocess.run(
        cmd,
        cwd=cwd,
        text=text,
        input=input_data,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    if check and cp.returncode != 0:
        output = cp.stdout if text else cp.stdout.decode("utf-8", errors="replace")
        raise Stop(f"command failed ({cp.returncode}): {' '.join(map(str, cmd))}\n{output}")
    return cp


def git(*args, cwd=None, check=True, env=None, text=True):
    return run(["git", *args], cwd=cwd, check=check, env=env, text=text)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical(obj) -> bytes:
    return (json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(obj))


def git_show_text(commit: str, path: str) -> str:
    return git("show", f"{commit}:{path}").stdout


def git_show_bytes(commit: str, path: str, *, cwd=None) -> bytes:
    return git("show", f"{commit}:{path}", cwd=cwd, text=False).stdout


def remote_head(branch: str) -> str | None:
    cp = git("ls-remote", "--heads", "origin", f"refs/heads/{branch}")
    line = cp.stdout.strip()
    return line.split()[0] if line else None


def configure_git(cwd=None) -> None:
    git("config", "user.name", "github-actions[bot]", cwd=cwd)
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com", cwd=cwd)


def push_control(expected_remote: str) -> str:
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


def commit_control(expected_remote: str, message: str, paths: list[Path | str]) -> str:
    for path in paths:
        git("add", "--", str(path))
    git("commit", "-m", message)
    return push_control(expected_remote)


def clear_active(state: dict) -> None:
    for key in [
        "active_request_id", "active_request_sha256", "active_lock_owner",
        "active_lock_commit", "active_operation", "active_writeahead_commit",
        "active_writeahead_manifest_sha256", "active_prepared_commit_sha",
        "active_prepared_tree_sha", "active_integration_freeze_sha256",
        "active_venue_reconciliation_sha256", "active_conference_reconciliation_sha256",
        "active_stage1_reconciliation_sha256",
    ]:
        state[key] = None
    for key in ["lock_acquired_run_id", "lock_acquired_run_attempt", "lock_acquisition_request_commit"]:
        state.pop(key, None)
    state["lifecycle_state"] = "IDLE"
    state["recovery_required"] = False


def reconstruct_research_zip(out_path: Path) -> dict:
    git(
        "fetch", "--no-tags", "origin",
        "+refs/heads/experiment/remote-implementation-stage1:refs/remotes/origin/proof6-proof1"
    )
    prefix = ".remote-implementation-poc/inputs/liu-research-frozen.zip.b64.part"
    listing = git("ls-tree", "-r", "--name-only", PROOF1_COMMIT, ".remote-implementation-poc/inputs").stdout.splitlines()
    parts = sorted(p for p in listing if p.startswith(prefix))
    if len(parts) != 9:
        raise Stop(f"RESEARCH_FIXTURE_PART_COUNT_MISMATCH: {len(parts)}")
    encoded = "".join(git_show_text(PROOF1_COMMIT, p) for p in parts).encode("ascii")
    out_path.write_bytes(base64.b64decode(encoded))
    actual = sha256_file(out_path)
    if actual != RESEARCH_ZIP_SHA:
        raise Stop(f"RESEARCH_FREEZE_SHA_MISMATCH expected={RESEARCH_ZIP_SHA} actual={actual}")

    with zipfile.ZipFile(out_path) as zf:
        names = sorted(zf.namelist())
        if names != sorted(REQUIRED_FILES):
            raise Stop(f"RESEARCH_FREEZE_MEMBER_SET_MISMATCH: {names}")
        member_hashes = {name: sha256_bytes(zf.read(name)) for name in REQUIRED_FILES}
        source_rows = list(csv.DictReader(io.StringIO(zf.read("source-games.csv").decode("utf-8-sig"))))
        seasons = sorted({row.get("season_label", "").strip() for row in source_rows})
    expected_seasons = [f"{year:04d}-{year+1:04d}" for year in range(1928, 1951)]
    expected_seasons += [f"{year:04d}-{year+1:04d}" for year in range(1968, 2026)]
    if len(source_rows) != 2193:
        raise Stop(f"RESEARCH_FREEZE_GAME_COUNT_MISMATCH: {len(source_rows)}")
    if seasons != expected_seasons:
        missing = sorted(set(expected_seasons) - set(seasons))
        extra = sorted(set(seasons) - set(expected_seasons))
        raise Stop(f"RESEARCH_FREEZE_SEASON_SET_MISMATCH missing={missing} extra={extra}")
    return {
        "zip_sha256": actual,
        "member_sha256": member_hashes,
        "game_count": len(source_rows),
        "season_count": len(seasons),
        "first_season": seasons[0],
        "last_season": seasons[-1],
    }


def csv_rows_from_bytes(data: bytes) -> list[dict[str, str]]:
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"))))


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def build_reconciliation_specs(zip_path: Path, worktree: Path, scratch: Path) -> tuple[Path, Path, dict]:
    with zipfile.ZipFile(zip_path) as zf:
        venues_bytes = zf.read("venues.csv")
        conferences_bytes = zf.read("conferences.csv")
        frozen_venues = csv_rows_from_bytes(venues_bytes)
        frozen_conferences = csv_rows_from_bytes(conferences_bytes)

    local_by_key = {row["venue_key"].strip(): row for row in frozen_venues}
    global_venues = csv_rows(worktree / "data/reference/venues.csv")
    global_by_id = {row["venue_id"].strip(): row for row in global_venues}
    global_conferences = {row["conference_key"].strip(): row for row in csv_rows(worktree / "data/reference/conferences.csv")}

    original = json.loads(git_show_text(PROOF2_CHECKPOINT, PROOF2_STAGE1_PATH))
    if original.get("integration_base_sha") != ORIGINAL_STAGE1_BASE:
        raise Stop("ORIGINAL_STAGE1_CHECKPOINT_BASE_MISMATCH")
    original_ambiguous = {
        row["venue_key"] for row in original["venue"]["rows"]
        if row.get("classification") == "STOP_AMBIGUOUS"
    }
    if original_ambiguous != set(VENUE_REUSE):
        raise Stop(
            "VENUE_RECONCILIATION_POPULATION_MISMATCH "
            f"expected={sorted(original_ambiguous)} supplied={sorted(VENUE_REUSE)}"
        )
    original_new = sorted(
        row["venue_key"] for row in original["venue"]["rows"]
        if row.get("classification") == "NEW_GLOBAL_IDENTITY"
    )

    mappings = []
    for local_key in sorted(VENUE_REUSE):
        target_id, target_key = VENUE_REUSE[local_key]
        local = local_by_key.get(local_key)
        target = global_by_id.get(target_id)
        if local is None or target is None:
            raise Stop(f"VENUE_RECONCILIATION_IDENTITY_MISSING: {local_key}")
        if target.get("venue_key", "").strip() != target_key:
            raise Stop(f"VENUE_RECONCILIATION_TARGET_KEY_DRIFT: {local_key}")
        if local.get("city", "").strip().casefold() != target.get("city", "").strip().casefold():
            raise Stop(f"VENUE_RECONCILIATION_CITY_MISMATCH: {local_key}")
        if local.get("state", "").strip().upper() != target.get("state", "").strip().upper():
            raise Stop(f"VENUE_RECONCILIATION_STATE_MISMATCH: {local_key}")
        basis = (
            "Control Center-authorized Proof 6 current-main same-physical-venue "
            "reconciliation; post-merge read-only verification."
        )
        mappings.append({
            "local_venue_key": local_key,
            "expected_local_name": local.get("canonical_name", "").strip(),
            "expected_local_city": local.get("city", "").strip(),
            "expected_local_state": local.get("state", "").strip(),
            "global_venue_id": target_id,
            "global_venue_key": target_key,
            "expected_global_city": target.get("city", "").strip(),
            "expected_global_state": target.get("state", "").strip(),
            "resolution_basis": basis,
        })

    venue_spec = {
        "schema_version": 1,
        "school_key": SCHOOL,
        "owner_approval_basis": (
            "Control Center-authorized generic Stage 1 tooling repair post-merge "
            "read-only regression; LIU is a discovered fixture only."
        ),
        "expected_research_zip_sha256": RESEARCH_ZIP_SHA,
        "expected_venues_sha256": sha256_bytes(venues_bytes),
        "mappings": mappings,
    }
    venue_path = scratch / "liu-stage1-venue-reconciliation.json"
    write_json(venue_path, venue_spec)
    venue_sha = sha256_file(venue_path)
    if venue_sha != EXPECTED_VENUE_RECON_SHA:
        raise Stop(
            "VENUE_RECONCILIATION_SHA_MISMATCH "
            f"expected={EXPECTED_VENUE_RECON_SHA} actual={venue_sha}"
        )

    if "nec" not in global_conferences:
        raise Stop("GLOBAL_NEC_IDENTITY_MISSING")
    replacement = []
    ecac_rows = 0
    for row in frozen_conferences:
        copy = dict(row)
        if copy.get("conference_key", "").strip() == "ecac-metro-conference":
            ecac_rows += 1
            copy["conference_key"] = "nec"
        replacement.append(copy)
    if ecac_rows < 1:
        raise Stop("FROZEN_ECAC_METRO_ROW_MISSING")
    conference_spec = {
        "schema_version": 1,
        "school_key": SCHOOL,
        "owner_approval_basis": (
            "Control Center-authorized Proof 6 ECAC Metro to NEC reconciliation; "
            "post-merge read-only verification."
        ),
        "expected_conferences_sha256": sha256_bytes(conferences_bytes),
        "replacement_history": replacement,
        "registrations": [],
    }
    conference_path = scratch / "liu-stage1-conference-reconciliation.json"
    write_json(conference_path, conference_spec)
    conference_sha = sha256_file(conference_path)
    if conference_sha != EXPECTED_CONFERENCE_RECON_SHA:
        raise Stop(
            "CONFERENCE_RECONCILIATION_SHA_MISMATCH "
            f"expected={EXPECTED_CONFERENCE_RECON_SHA} actual={conference_sha}"
        )

    return venue_path, conference_path, {
        "venue_reconciliation_sha256": venue_sha,
        "conference_reconciliation_sha256": conference_sha,
        "frozen_venues_sha256": sha256_bytes(venues_bytes),
        "frozen_conferences_sha256": sha256_bytes(conferences_bytes),
        "original_new_global_venue_keys": original_new,
        "original_ambiguous_venue_keys": sorted(original_ambiguous),
        "ecac_metro_replacement_row_count": ecac_rows,
    }


def commit_file_hashes(worktree: Path, commit: str, paths: list[str]) -> dict[str, str]:
    return {path: sha256_bytes(git_show_bytes(commit, path, cwd=worktree)) for path in paths}


def main() -> int:
    DIAG.mkdir(parents=True, exist_ok=True)
    if not REQUEST_PATH.exists():
        print("Proof 6 infrastructure-only push; no request.")
        return 0

    configure_git()
    request = read_json(REQUEST_PATH)
    rid = request.get("request_id")
    run_id = int(os.environ["GITHUB_RUN_ID"])
    attempt = int(os.environ["GITHUB_RUN_ATTEMPT"])

    git(
        "fetch", "--no-tags", "origin",
        "+refs/heads/main:refs/remotes/origin/main",
        "+refs/heads/main:refs/remotes/origin/proof6-live-main",
        f"+refs/heads/{CONTROL_BRANCH}:refs/remotes/origin/proof6-control",
    )
    live_main = git("rev-parse", "refs/remotes/origin/proof6-live-main").stdout.strip()
    durable_head = git("rev-parse", "refs/remotes/origin/proof6-control").stdout.strip()

    if attempt > 1:
        durable_state = json.loads(git_show_text(durable_head, STATE_PATH.as_posix()))
        used = set(durable_state.get("accepted_request_ids") or []) | set(durable_state.get("consumed_request_ids") or [])
        if rid in used or rid == durable_state.get("active_request_id"):
            print(f"ACCEPTED_PHASE0_REQUEST_REPLAY: REJECTED — {rid} has durable prior acceptance")
            return 42
        raise Stop("RERUN_GUARD_UNEXPECTEDLY_CLEAR")

    prior_commit = git("rev-parse", f"{os.environ['GITHUB_SHA']}^").stdout.strip()
    state_bytes = git_show_bytes(prior_commit, STATE_PATH.as_posix())
    state = json.loads(state_bytes)
    if state.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF6_GLOBAL_CONTROL":
        raise Stop("CONTROL_KIND_MISMATCH")
    if state.get("lifecycle_state") != "IDLE" or state.get("active_request_id") is not None:
        raise Stop("IMPLEMENTATION_LOCK_OCCUPIED")
    if state.get("integration_frozen") is not False or state.get("phase0_authorized") is not False:
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if request.get("experiment_kind") != "REMOTE_IMPLEMENTATION_PROOF6_REQUEST":
        raise Stop("REQUEST_KIND_MISMATCH")
    authority = request.get("authority") or {}
    if authority.get("experimental_rehearsal_only") is not True:
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if any(authority.get(k) is not False for k in [
        "authoritative_integration_freeze", "real_phase0", "real_onboarding_branch",
        "stage2", "gate1", "release"
    ]):
        raise Stop("AUTHORITY_BOUNDARY_VIOLATION")
    if request.get("previous_control_state_commit") != prior_commit:
        raise Stop("STALE_CONTROL_STATE")
    if request.get("previous_control_state_sha256") != sha256_bytes(state_bytes):
        raise Stop("STALE_CONTROL_STATE_HASH")
    if request.get("expected_protected_main_sha") != EXPECTED_MAIN or live_main != EXPECTED_MAIN:
        raise Stop("MAIN_SHA_MISMATCH")
    if request.get("venue_reconciliation_sha256") != EXPECTED_VENUE_RECON_SHA:
        raise Stop("REQUEST_VENUE_RECONCILIATION_SHA_MISMATCH")
    if request.get("conference_reconciliation_sha256") != EXPECTED_CONFERENCE_RECON_SHA:
        raise Stop("REQUEST_CONFERENCE_RECONCILIATION_SHA_MISMATCH")
    if request.get("operation") != "REHEARSE_REAL_LIU_PHASE0":
        raise Stop("OPERATION_NOT_ALLOWED")
    if rid in set(state.get("accepted_request_ids") or []) | set(state.get("consumed_request_ids") or []):
        raise Stop("REQUEST_REPLAY")
    if remote_head(REAL_BRANCH) is not None:
        raise Stop("REAL_LIU_ONBOARDING_BRANCH_EXISTS")
    if remote_head(TARGET_BRANCH) is not None:
        raise Stop("DISPOSABLE_TARGET_ALREADY_EXISTS")

    request_sha = sha256_file(REQUEST_PATH)
    accepted = list(state.get("accepted_request_ids") or [])
    accepted.append(rid)
    state.update({
        "accepted_request_ids": accepted,
        "lifecycle_state": "ACTIVE",
        "transaction_state": "LOCKED",
        "active_request_id": rid,
        "active_operation": request["operation"],
        "active_lock_owner": f"github-actions:{run_id}:{attempt}",
        "active_request_sha256": request_sha,
        "recovery_required": True,
        "lock_acquired_run_id": run_id,
        "lock_acquired_run_attempt": attempt,
        "lock_acquisition_request_commit": os.environ["GITHUB_SHA"],
    })
    write_json(STATE_PATH, state)
    lock_commit = commit_control(
        os.environ["GITHUB_SHA"],
        f"[proof6-internal] acquire global rehearsal lock {rid}",
        [STATE_PATH],
    )
    state["active_lock_commit"] = lock_commit
    write_json(STATE_PATH, state)
    lock_bound = commit_control(
        lock_commit,
        f"[proof6-internal] bind rehearsal lock identity {rid}",
        [STATE_PATH],
    )
    print(f"GLOBAL LOCK: ACQUIRED {lock_commit}")

    scratch = Path(tempfile.mkdtemp(prefix="proof6-inputs-"))
    zip_path = scratch / "liu-research-frozen.zip"
    freeze_info = reconstruct_research_zip(zip_path)
    print(f"RESEARCH FREEZE: VERIFIED {freeze_info['zip_sha256']} games={freeze_info['game_count']} seasons={freeze_info['season_count']}")

    worktree = Path(tempfile.mkdtemp(prefix="proof6-phase0-worktree-"))
    shutil.rmtree(worktree)
    git("worktree", "add", "-b", REAL_BRANCH, str(worktree), live_main)
    configure_git(worktree)
    if git("rev-parse", "HEAD", cwd=worktree).stdout.strip() != live_main:
        raise Stop("WORKTREE_MAIN_MISMATCH")
    if git("rev-parse", "origin/main", cwd=worktree).stdout.strip() != live_main:
        raise Stop("WORKTREE_ORIGIN_MAIN_MISMATCH")

    venue_spec, conference_spec, reconciliation = build_reconciliation_specs(zip_path, worktree, scratch)
    stage1_cmd = [
        sys.executable,
        str(worktree / "tools/implementation_stage1_inventory.py"),
        SCHOOL,
        str(zip_path),
        "--expected-sha256", RESEARCH_ZIP_SHA,
        "--research-base", RESEARCH_BASE,
        "--venue-reconciliation", str(venue_spec),
        "--conference-reconciliation", str(conference_spec),
        "--repo", str(worktree),
    ]
    stage1_cp = run(stage1_cmd, cwd=worktree, check=False)
    (DIAG / "stage1-reconciled.log").write_text(stage1_cp.stdout, encoding="utf-8")
    if stage1_cp.returncode != 0:
        raise Stop("RECONCILED_STAGE1_COMMAND_FAILED\n" + stage1_cp.stdout[-6000:])
    stage1_path = worktree / ".onboarding" / SCHOOL / "stage1-reconciliation.json"
    stage1 = read_json(stage1_path)
    if (
        stage1.get("status") != "PASS"
        or int(stage1.get("blocker_count", -1)) != 0
        or int(stage1.get("ambiguous_stop_count", -1)) != 0
        or int(stage1.get("maintenance_required_count", -1)) != 0
    ):
        raise Stop(
            "RECONCILED_STAGE1_NOT_PASS\n"
            + json.dumps({
                "status": stage1.get("status"),
                "blockers": stage1.get("blocker_count"),
                "ambiguous": stage1.get("ambiguous_stop_count"),
                "maintenance": stage1.get("maintenance_required_count"),
                "venue_blockers": stage1.get("venue", {}).get("blockers"),
                "conference_blockers": stage1.get("conference", {}).get("blockers"),
            }, indent=2)
        )
    stage1_by_key = {row["venue_key"]: row for row in stage1["venue"]["rows"]}
    for key in reconciliation["original_new_global_venue_keys"]:
        if stage1_by_key.get(key, {}).get("classification") != "NEW_GLOBAL_IDENTITY":
            raise Stop(f"GENUINELY_NEW_VENUE_RECLASSIFIED: {key}")
    if stage1.get("conference", {}).get("blocker_count") != 0:
        raise Stop("CONFERENCE_RECONCILIATION_STILL_BLOCKED")
    expected_venue_counts = {
        "NEW_GLOBAL_IDENTITY": 20,
        "SAFE_REPRESENTATION_REUSE": 39,
    }
    if stage1.get("venue", {}).get("venue_count") != 59:
        raise Stop("RECONCILED_STAGE1_VENUE_COUNT_DRIFT")
    if stage1.get("venue", {}).get("classification_counts") != expected_venue_counts:
        raise Stop(
            "RECONCILED_STAGE1_VENUE_TOPOLOGY_DRIFT: "
            + json.dumps(stage1.get("venue", {}).get("classification_counts"), sort_keys=True)
        )
    if stage1.get("conference", {}).get("classification_counts") != {"REUSE_CURRENT_IDENTITY": 3}:
        raise Stop("RECONCILED_STAGE1_CONFERENCE_TOPOLOGY_DRIFT")
    if stage1.get("program_alias", {}).get("blocker_count") != 0:
        raise Stop("RECONCILED_STAGE1_PROGRAM_ALIAS_BLOCKED")
    if stage1.get("program_alias", {}).get("classification_counts") != {"NO_CURRENT_VERIFIED_ALIAS": 229}:
        raise Stop("RECONCILED_STAGE1_PROGRAM_ALIAS_TOPOLOGY_DRIFT")
    print("FINAL RECONCILED STAGE 1: PASS")

    input_dir = Path(f".remote-implementation-poc/control6/inputs/{rid}")
    input_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(venue_spec, input_dir / "venue-reconciliation.json")
    shutil.copyfile(conference_spec, input_dir / "conference-reconciliation.json")
    shutil.copyfile(stage1_path, input_dir / "stage1-reconciliation.json")
    input_verification = {
        "schema_version": 1,
        "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF6_INPUT_VERIFICATION",
        "request_id": rid,
        "protected_main_sha": live_main,
        "research_base_sha": RESEARCH_BASE,
        "research_freeze": freeze_info,
        **reconciliation,
        "venue_reconciliation_sha256": sha256_file(input_dir / "venue-reconciliation.json"),
        "conference_reconciliation_sha256": sha256_file(input_dir / "conference-reconciliation.json"),
        "stage1_reconciliation_sha256": sha256_file(input_dir / "stage1-reconciliation.json"),
        "stage1_status": stage1["status"],
        "stage1_blocker_count": stage1["blocker_count"],
        "known_scope_reference_debt": {
            "protected_main_row": "1947-48..1950-51|1968-69+",
            "accepted_owner_scope": "1928-29..1950-51|1968-69+",
            "classification": "SETTLED_SHARED_REFERENCE_MAINTENANCE_DEBT_NOT_MUTATED_BY_PROOF6",
        },
        "authority_statement": "Experimental Proof 6 input authority only; no real LIU Integration Freeze or Phase 0.",
    }
    write_json(input_dir / "input-verification.json", input_verification)
    state.update({
        "transaction_state": "INPUTS_VERIFIED",
        "active_venue_reconciliation_sha256": input_verification["venue_reconciliation_sha256"],
        "active_conference_reconciliation_sha256": input_verification["conference_reconciliation_sha256"],
        "active_stage1_reconciliation_sha256": input_verification["stage1_reconciliation_sha256"],
    })
    write_json(STATE_PATH, state)
    inputs_commit = commit_control(
        lock_bound,
        f"[proof6-internal] persist authenticated LIU rehearsal inputs {rid}",
        [STATE_PATH, input_dir],
    )
    print(f"INPUT AUTHORITY: DURABLE {inputs_commit}")

    phase0_cmd = [
        sys.executable,
        "tools/stage_research_portfolio.py",
        SCHOOL,
        str(zip_path),
        "--expected-sha256", RESEARCH_ZIP_SHA,
        "--research-base", RESEARCH_BASE,
        "--history-start-season", "1928-1929",
        "--history-scope-basis", "TOP_LEVEL_INTERVALS",
        "--history-scope-intervals", "1928-29..1950-51|1968-69+",
        "--history-scope-notes",
        "Owner-confirmed LIU top-level scope: 1928-29 through 1950-51 and 1968-69 onward; 1951-52 through 1967-68 excluded. Proof 6 disposable rehearsal only.",
        "--venue-reconciliation", str(venue_spec),
        "--conference-reconciliation", str(conference_spec),
        "--apply", "--commit",
    ]
    phase0_cp = run(phase0_cmd, cwd=worktree, check=False)
    (DIAG / "phase0.log").write_text(phase0_cp.stdout, encoding="utf-8")
    if phase0_cp.returncode != 0:
        raise Stop("PERMANENT_PHASE0_COMMAND_FAILED\n" + phase0_cp.stdout[-10000:])

    prepared = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
    parent = git("rev-parse", f"{prepared}^", cwd=worktree).stdout.strip()
    tree = git("rev-parse", f"{prepared}^{{tree}}", cwd=worktree).stdout.strip()
    message = git("log", "-1", "--format=%B", prepared, cwd=worktree).stdout.strip()
    if parent != live_main:
        raise Stop(f"PHASE0_PARENT_MISMATCH expected={live_main} actual={parent}")
    changed = sorted(
        line.strip()
        for line in git("diff-tree", "--no-commit-id", "--name-only", "-r", prepared, cwd=worktree).stdout.splitlines()
        if line.strip()
    )
    unexpected = sorted(set(changed) - CONTRACT_ALLOWED)
    if unexpected:
        raise Stop("PROOF 6: STOP — PHASE 0 DIFF OUTSIDE CONTRACT: " + ", ".join(unexpected))
    required_school_paths = {f"schools/{SCHOOL}/{name}" for name in REQUIRED_FILES}
    if not required_school_paths.issubset(changed):
        raise Stop("PHASE0_SIX_FILE_COMMIT_INCOMPLETE")
    if "data/reference/programs.csv" not in changed:
        raise Stop("PHASE0_PROGRAM_SCOPE_NOT_COMMITTED")

    freeze_path = worktree / ".onboarding" / SCHOOL / "integration-freeze.json"
    if not freeze_path.exists():
        raise Stop("INTEGRATION_FREEZE_MISSING")
    freeze_bytes = freeze_path.read_bytes()
    freeze_sha = sha256_bytes(freeze_bytes)
    integration = json.loads(freeze_bytes)
    if integration.get("status") != "INTEGRATION_FROZEN":
        raise Stop("INTEGRATION_FREEZE_STATUS_MISMATCH")
    if integration.get("integration_base_sha") != live_main or integration.get("origin_main_sha") != live_main:
        raise Stop("INTEGRATION_FREEZE_MAIN_BINDING_MISMATCH")
    if integration.get("research_zip_sha256") != RESEARCH_ZIP_SHA or integration.get("research_base_sha") != RESEARCH_BASE:
        raise Stop("INTEGRATION_FREEZE_RESEARCH_BINDING_MISMATCH")
    scope = integration.get("history_scope") or {}
    if (
        scope.get("history_start_season") != "1928-1929"
        or scope.get("history_scope_basis") != "TOP_LEVEL_INTERVALS"
        or scope.get("history_scope_intervals") != "1928-29..1950-51|1968-69+"
        or scope.get("history_scope_status") != "OWNER_CONFIRMED"
    ):
        raise Stop("INTEGRATION_FREEZE_SCOPE_MISMATCH")
    venue_meta = integration.get("venue_reconciliation") or {}
    conference_meta = integration.get("conference_reconciliation") or {}
    if venue_meta.get("spec_sha256") != EXPECTED_VENUE_RECON_SHA:
        raise Stop("INTEGRATION_FREEZE_VENUE_RECONCILIATION_HASH_MISMATCH")
    if conference_meta.get("spec_sha256") != EXPECTED_CONFERENCE_RECON_SHA:
        raise Stop("INTEGRATION_FREEZE_CONFERENCE_RECONCILIATION_HASH_MISMATCH")

    package_hashes = integration.get("package_member_sha256") or {}
    for name in REQUIRED_FILES:
        committed = git_show_bytes(prepared, f"schools/{SCHOOL}/{name}", cwd=worktree)
        if sha256_bytes(committed) != package_hashes.get(name):
            raise Stop(f"INTEGRATION_FREEZE_PACKAGE_HASH_MISMATCH: {name}")

    file_hashes = commit_file_hashes(worktree, prepared, changed)
    print(f"PERMANENT PHASE 0: PASS commit={prepared} tree={tree} parent={parent}")
    print(f"REPOSITORY VALIDATION: PASS via permanent command")
    print(f"INTEGRATION FREEZE CAPTURED: {freeze_sha}")

    wa_dir = Path(f".remote-implementation-poc/control6/writeahead/{rid}")
    wa_dir.mkdir(parents=True, exist_ok=True)
    (wa_dir / "integration-freeze.json").write_bytes(freeze_bytes)
    manifest = {
        "schema_version": 1,
        "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF6_WRITEAHEAD",
        "authority_statement": "Disposable real-tool LIU Phase 0 rehearsal only; no authoritative LIU status or real onboarding-branch authority.",
        "request_id": rid,
        "request_sha256": request_sha,
        "global_lock_commit": lock_commit,
        "protected_main_sha": live_main,
        "research_freeze_sha256": RESEARCH_ZIP_SHA,
        "research_base_sha": RESEARCH_BASE,
        "venue_reconciliation_sha256": input_verification["venue_reconciliation_sha256"],
        "conference_reconciliation_sha256": input_verification["conference_reconciliation_sha256"],
        "stage1_reconciliation_sha256": input_verification["stage1_reconciliation_sha256"],
        "stage1_status": "PASS",
        "target_branch": TARGET_BRANCH,
        "expected_target_predecessor": None,
        "expected_target_nonexistent": True,
        "prepared_phase0_commit_sha": prepared,
        "prepared_phase0_tree_sha": tree,
        "prepared_phase0_parent_sha": parent,
        "commit_message": message,
        "changed_paths": changed,
        "contract_allowed_paths": sorted(CONTRACT_ALLOWED),
        "changed_file_sha256": file_hashes,
        "integration_freeze_file": "integration-freeze.json",
        "integration_freeze_sha256": freeze_sha,
        "integration_freeze_package_member_sha256": package_hashes,
        "semantic_snapshot_sha256": integration.get("source_game_semantic_guard", {}).get("snapshot_sha256"),
        "venue_mapping": integration.get("venue_mapping"),
        "conference_mapping": integration.get("conference_mapping"),
        "program_alias_mapping": integration.get("program_alias_mapping"),
        "venue_reconciliation_metadata": venue_meta,
        "conference_reconciliation_metadata": conference_meta,
        "history_scope": scope,
        "known_scope_reference_debt": input_verification["known_scope_reference_debt"],
        "permanent_command": "python tools/stage_research_portfolio.py long-island-university <exact-research-freeze> --expected-sha256 <exact> --research-base <exact> --history-start-season 1928-1929 --history-scope-basis TOP_LEVEL_INTERVALS --history-scope-intervals 1928-29..1950-51|1968-69+ --history-scope-notes <owner-confirmed> --venue-reconciliation <exact> --conference-reconciliation <exact> --apply --commit",
        "permanent_command_exit_status": phase0_cp.returncode,
        "repository_validation": "PASS",
        "mutation_state": "PREPARED_NOT_PUBLISHED",
    }
    wa_path = wa_dir / "writeahead-manifest.json"
    write_json(wa_path, manifest)
    wa_sha = sha256_file(wa_path)
    (wa_dir / "writeahead-manifest.sha256").write_text(f"{wa_sha}  writeahead-manifest.json\n", encoding="utf-8")
    state.update({
        "transaction_state": "PREPARED_NOT_PUBLISHED",
        "active_prepared_commit_sha": prepared,
        "active_prepared_tree_sha": tree,
        "active_integration_freeze_sha256": freeze_sha,
        "active_writeahead_manifest_sha256": wa_sha,
    })
    write_json(STATE_PATH, state)
    wa_commit = commit_control(
        inputs_commit,
        f"[proof6-internal] publish real Phase 0 write-ahead authority {rid}",
        [STATE_PATH, wa_dir],
    )
    state["active_writeahead_commit"] = wa_commit
    write_json(STATE_PATH, state)
    wa_bound = commit_control(
        wa_commit,
        f"[proof6-internal] bind real Phase 0 write-ahead commit {rid}",
        [STATE_PATH],
    )
    print(f"WRITE-AHEAD: DURABLE commit={wa_commit} manifest_sha256={wa_sha}")

    if remote_head(TARGET_BRANCH) is not None:
        raise Stop("DISPOSABLE_TARGET_APPEARED_BEFORE_PUBLICATION")
    publish = git(
        "push",
        f"--force-with-lease=refs/heads/{TARGET_BRANCH}:",
        "origin",
        f"{prepared}:refs/heads/{TARGET_BRANCH}",
        check=False,
    )
    if publish.returncode != 0:
        raise Stop("DISPOSABLE_TARGET_CAS_PUBLICATION_FAILED\n" + publish.stdout)
    git(
        "fetch", "--no-tags", "origin",
        f"+refs/heads/{TARGET_BRANCH}:refs/remotes/origin/proof6-target",
    )
    actual_target = git("rev-parse", "refs/remotes/origin/proof6-target").stdout.strip()
    if actual_target != prepared:
        raise Stop("DISPOSABLE_TARGET_PUBLICATION_VERIFY_FAILED")
    if remote_head(REAL_BRANCH) is not None:
        raise Stop("REAL_LIU_ONBOARDING_BRANCH_CREATED_UNEXPECTEDLY")
    print(f"DISPOSABLE PUBLICATION: PASS {actual_target}")

    successor_dir = Path(f".remote-implementation-poc/control6/successors/{rid}")
    successor_dir.mkdir(parents=True, exist_ok=True)
    successor = {
        "schema_version": 1,
        "experiment_kind": "REMOTE_IMPLEMENTATION_PROOF6_SUCCESSOR",
        "authority_statement": "Disposable rehearsal successor only; LIU remains RESEARCH_FROZEN outside this experiment.",
        "predecessor_control_state_commit": request["previous_control_state_commit"],
        "request_id": rid,
        "request_sha256": request_sha,
        "global_lock_commit": lock_commit,
        "inputs_commit": inputs_commit,
        "venue_reconciliation_sha256": input_verification["venue_reconciliation_sha256"],
        "conference_reconciliation_sha256": input_verification["conference_reconciliation_sha256"],
        "stage1_reconciliation_sha256": input_verification["stage1_reconciliation_sha256"],
        "writeahead_commit": wa_commit,
        "writeahead_manifest_sha256": wa_sha,
        "protected_main_sha": live_main,
        "research_freeze_sha256": RESEARCH_ZIP_SHA,
        "research_base_sha": RESEARCH_BASE,
        "phase0_commit_sha": prepared,
        "phase0_tree_sha": tree,
        "phase0_parent_sha": parent,
        "changed_paths": changed,
        "changed_file_sha256": file_hashes,
        "integration_freeze_sha256": freeze_sha,
        "semantic_snapshot_sha256": manifest["semantic_snapshot_sha256"],
        "actual_published_target_sha": actual_target,
        "target_branch": TARGET_BRANCH,
        "publication_cas": "EXPECTED_NONEXISTENCE_CREATE_ONCE_PASS",
        "repository_validation": "PASS",
        "final_transaction_state": "COMPLETE",
        "final_global_lifecycle": "IDLE",
        "integration_frozen": False,
        "phase0_authorized": False,
        "real_onboarding_branch_created": False,
        "known_scope_reference_debt": input_verification["known_scope_reference_debt"],
        "original_action_run_id": run_id,
        "original_action_run_attempt": attempt,
    }
    successor_path = successor_dir / "successor-manifest.json"
    write_json(successor_path, successor)
    successor_sha = sha256_file(successor_path)
    (successor_dir / "successor-manifest.sha256").write_text(f"{successor_sha}  successor-manifest.json\n", encoding="utf-8")

    consumed = list(state.get("consumed_request_ids") or [])
    consumed.append(rid)
    state["consumed_request_ids"] = consumed
    state["current_sequence"] = int(state.get("current_sequence", 0)) + 1
    state["last_transaction"] = {
        "request_id": rid,
        "phase0_commit_sha": prepared,
        "phase0_tree_sha": tree,
        "target_sha": actual_target,
        "integration_freeze_sha256": freeze_sha,
        "writeahead_manifest_sha256": wa_sha,
        "successor_manifest_sha256": successor_sha,
        "successor_manifest_path": successor_path.as_posix(),
        "writeahead_manifest_path": wa_path.as_posix(),
        "inputs_path": input_dir.as_posix(),
        "repository_validation": "PASS",
        "remote_phase0_equivalence": "PENDING_FRESH_RUNNER_VERIFICATION",
        "basketball_authoritative_mutation": False,
    }
    clear_active(state)
    state["transaction_state"] = "COMPLETE"
    write_json(STATE_PATH, state)
    successor_commit = commit_control(
        wa_bound,
        f"[proof6-internal] finalize disposable real Phase 0 rehearsal {rid}",
        [STATE_PATH, successor_dir],
    )
    print(f"SUCCESSOR: DURABLE {successor_commit} sha256={successor_sha}")
    print("GLOBAL LOCK: RELEASED TO IDLE")
    return 0


if __name__ == "__main__":
    try:
        rc = main()
    except Stop as exc:
        DIAG.mkdir(parents=True, exist_ok=True)
        (DIAG / "stop.txt").write_text(str(exc) + "\n", encoding="utf-8")
        print(f"STOP: {exc}")
        rc = 1
    sys.exit(rc)
