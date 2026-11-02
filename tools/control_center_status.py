#!/usr/bin/env python3
"""Read-only Control Center recovery snapshot.

This helper is intentionally conservative. It derives current Git ref facts and,
when the exact remote control commit is already present locally, reads the
global remote-Implementation control state. It never fetches, writes, checks
out, commits, pushes, or mutates tracked basketball/control state.

Branch names emitted by this tool are recovery locators only. They do not prove
Research Freeze, Implementation phase, or owner-gate authority.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

PROTECTED_MAIN_REF = "refs/heads/main"
CONTROL_BRANCH = "control/remote-implementation"
CONTROL_REF = f"refs/heads/{CONTROL_BRANCH}"
CONTROL_STATE_PATH = ".remote-implementation/control-state.json"

READ_ONLY_GIT_SUBCOMMANDS = frozenset(
    {
        "ls-remote",
        "rev-parse",
        "show",
        "status",
    }
)


class RecoveryError(RuntimeError):
    """Raised when a required read-only Git fact cannot be established."""


def _git(repo: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    if not args or args[0] not in READ_ONLY_GIT_SUBCOMMANDS:
        raise ValueError(f"Refusing non-read-only git subcommand: {args!r}")
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        detail = (result.stderr or result.stdout).strip()
        raise RecoveryError(
            f"git {' '.join(args)} failed with {result.returncode}: {detail}"
        )
    return result


def _parse_ls_remote(output: str) -> list[tuple[str, str]]:
    rows: list[tuple[str, str]] = []
    for raw in output.splitlines():
        raw = raw.strip()
        if not raw:
            continue
        parts = raw.split("\t", 1)
        if len(parts) != 2:
            raise RecoveryError(f"Unexpected git ls-remote row: {raw!r}")
        sha, ref = parts
        rows.append((sha, ref))
    return rows


def _remote_ref_sha(repo: Path, remote: str, ref: str) -> str:
    result = _git(repo, "ls-remote", "--refs", remote, ref)
    rows = _parse_ls_remote(result.stdout)
    exact = [sha for sha, candidate in rows if candidate == ref]
    if len(exact) != 1:
        raise RecoveryError(
            f"Expected exactly one remote ref for {ref}; found {len(exact)}"
        )
    return exact[0]


def _remote_branch_names(repo: Path, remote: str, pattern: str) -> list[str]:
    result = _git(repo, "ls-remote", "--heads", remote, pattern)
    prefix = "refs/heads/"
    names = []
    for _sha, ref in _parse_ls_remote(result.stdout):
        if ref.startswith(prefix):
            names.append(ref[len(prefix) :])
    return sorted(set(names))


def _cached_control_state(
    repo: Path,
    remote: str,
    remote_control_sha: str,
) -> tuple[dict[str, Any] | None, str | None]:
    candidates = (
        CONTROL_BRANCH,
        f"{remote}/{CONTROL_BRANCH}",
    )
    for ref in candidates:
        resolved = _git(repo, "rev-parse", "--verify", ref, check=False)
        if resolved.returncode != 0:
            continue
        if resolved.stdout.strip() != remote_control_sha:
            continue
        shown = _git(
            repo,
            "show",
            f"{ref}:{CONTROL_STATE_PATH}",
            check=False,
        )
        if shown.returncode != 0:
            continue
        try:
            payload = json.loads(shown.stdout)
        except json.JSONDecodeError as exc:
            raise RecoveryError(
                f"Exact cached control state at {ref} is not valid JSON"
            ) from exc
        if not isinstance(payload, dict):
            raise RecoveryError(
                f"Exact cached control state at {ref} is not a JSON object"
            )
        return payload, ref
    return None, None


def _control_summary(state: dict[str, Any]) -> dict[str, Any]:
    last = state.get("last_operation")
    if not isinstance(last, dict):
        last = {}
    return {
        "current_sequence": state.get("current_sequence"),
        "lifecycle_state": state.get("lifecycle_state"),
        "transaction_state": state.get("transaction_state"),
        "active_request_id": state.get("active_request_id"),
        "active_school_key": state.get("active_school_key"),
        "active_lock_owner": state.get("active_lock_owner"),
        "recovery_required": state.get("recovery_required"),
        "last_operation": {
            key: last.get(key)
            for key in (
                "operation",
                "request_id",
                "school_key",
                "protected_main_sha",
                "target_branch",
                "target_sha",
                "fresh_runner_verification",
                "stage2_status",
                "checkpoint_manifest_path",
                "checkpoint_manifest_sha256",
                "decision_universe_sha256",
            )
            if key in last
        },
    }


def build_snapshot(repo: Path, remote: str = "origin") -> dict[str, Any]:
    repo = repo.resolve()
    protected_main_sha = _remote_ref_sha(repo, remote, PROTECTED_MAIN_REF)
    control_branch_sha = _remote_ref_sha(repo, remote, CONTROL_REF)

    local_head = _git(repo, "rev-parse", "HEAD").stdout.strip()
    worktree = _git(repo, "status", "--porcelain=v1").stdout
    control_state, control_state_ref = _cached_control_state(
        repo,
        remote,
        control_branch_sha,
    )

    snapshot: dict[str, Any] = {
        "schema_version": 1,
        "kind": "CONTROL_CENTER_RECOVERY_SNAPSHOT",
        "repository": str(repo),
        "remote": remote,
        "protected_main_sha": protected_main_sha,
        "control_branch": CONTROL_BRANCH,
        "control_branch_sha": control_branch_sha,
        "local_head_sha": local_head,
        "worktree_clean": not bool(worktree.strip()),
        "control_state_source_ref": control_state_ref,
        "control_state_available_exactly": control_state is not None,
        "global_control": (
            _control_summary(control_state) if control_state is not None else None
        ),
        "branch_locators": {
            "onboarding": _remote_branch_names(
                repo,
                remote,
                "refs/heads/data/*-onboarding",
            ),
            "correction": _remote_branch_names(
                repo,
                remote,
                "refs/heads/data/*-correction",
            ),
            "research": _remote_branch_names(
                repo,
                remote,
                "refs/heads/research/*",
            ),
        },
        "authority_notes": [
            "Branch locators are not lifecycle authority.",
            "RESEARCH_FROZEN must be supported by an authoritative checkpoint/artifact.",
            "An IDLE global mutation lock does not authorize a second Implementation school.",
            "If exact control state is unavailable locally, read the exact remote control branch through the authenticated GitHub connection.",
        ],
    }
    return snapshot


def _human(snapshot: dict[str, Any]) -> str:
    lines = [
        "CONTROL CENTER RECOVERY",
        f"protected_main_sha: {snapshot['protected_main_sha']}",
        f"control_branch_sha: {snapshot['control_branch_sha']}",
        f"local_head_sha: {snapshot['local_head_sha']}",
        f"worktree_clean: {str(snapshot['worktree_clean']).lower()}",
    ]

    control = snapshot.get("global_control")
    if isinstance(control, dict):
        lines.extend(
            [
                f"control_sequence: {control.get('current_sequence')}",
                f"lifecycle_state: {control.get('lifecycle_state')}",
                f"transaction_state: {control.get('transaction_state')}",
                f"active_request_id: {control.get('active_request_id') or 'NONE'}",
                f"active_school_key: {control.get('active_school_key') or 'NONE'}",
                f"active_lock_owner: {control.get('active_lock_owner') or 'NONE'}",
                f"recovery_required: {str(bool(control.get('recovery_required'))).lower()}",
            ]
        )
        last = control.get("last_operation") or {}
        lines.extend(
            [
                f"last_operation: {last.get('operation') or 'NONE'}",
                f"last_operation_school: {last.get('school_key') or 'NONE'}",
                f"last_operation_request: {last.get('request_id') or 'NONE'}",
                f"fresh_runner_verification: {last.get('fresh_runner_verification') or 'UNKNOWN'}",
            ]
        )
    else:
        lines.append(
            "global_control: EXACT_REMOTE_STATE_NOT_CACHED_LOCALLY "
            "(read exact control branch through GitHub)"
        )

    locators = snapshot["branch_locators"]
    for key in ("onboarding", "correction", "research"):
        values = locators[key]
        lines.append(f"{key}_branch_locators: {', '.join(values) if values else 'NONE'}")

    lines.append(
        "NOTE: branch locators are recovery hints only; reconcile authoritative checkpoints before declaring lifecycle status."
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository checkout to inspect (default: repository root).",
    )
    parser.add_argument(
        "--remote",
        default="origin",
        help="Git remote to inspect (default: origin).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the recovery snapshot as JSON.",
    )
    args = parser.parse_args()

    try:
        snapshot = build_snapshot(args.repo, args.remote)
    except (OSError, RecoveryError, ValueError) as exc:
        print(f"STOP: {exc}")
        return 1

    if args.json:
        print(json.dumps(snapshot, indent=2, sort_keys=True))
    else:
        print(_human(snapshot), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
