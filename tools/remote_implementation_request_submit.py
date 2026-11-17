#!/usr/bin/env python3
"""Construct and publish one exact-bound remote Implementation request.

A complete owner-authorized request template must deliberately OMIT the two
previous_control_state_* envelope keys. The exact protected-main SHA must
already be present. This tool binds the raw control-state bytes and immediate
control commit, invokes the permanent request/predecessor validators, and
optionally creates one Git control-branch commit by expected-predecessor CAS.

The tool NEVER creates owner approval, repairs a failed request, or retries CAS.
It is not an alternative remote runner or a recovery mechanism.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import tempfile
from typing import Any

from remote_implementation_control import (
    LIFECYCLE_IDLE,
    OP_RECOVER,
    TX_IDLE,
    TX_COMPLETE,
    TX_ABANDONED_NOT_ATTEMPTED,
    TX_ABANDONED_PREPARED,
    canonical_json_bytes,
    request_used,
    sha256_bytes,
    validate_control_state,
    verify_request_predecessor,
)
from remote_implementation_io import (
    CONTROL_BRANCH,
    REQUEST_PATH,
    STATE_PATH,
    ROOT,
    Stop,
    git,
    git_show_bytes,
)


def fetch_exact_heads(repo: Path) -> tuple[str, str]:
    """Fetch both authoritative refs afresh, never using cached conversation SHAs."""
    git(
        "fetch",
        "--no-tags",
        "origin",
        "+refs/heads/main:refs/remotes/origin/main",
        f"+refs/heads/{CONTROL_BRANCH}:refs/remotes/origin/remote-control",
        cwd=repo,
    )
    main = git("rev-parse", "refs/remotes/origin/main", cwd=repo).stdout.strip()
    control = git(
        "rev-parse", "refs/remotes/origin/remote-control", cwd=repo
    ).stdout.strip()
    return main, control


def read_control_snapshot(
    repo: Path, control_head: str
) -> tuple[dict[str, Any], bytes, str | None]:
    """Use exact Git blob bytes; never hash a JSON reserialization."""
    state_bytes = git_show_bytes(
        control_head, STATE_PATH.as_posix(), cwd=repo
    )
    try:
        state = json.loads(state_bytes)
    except (ValueError, TypeError) as exc:
        raise Stop("REQUEST_SUBMISSION_CONTROL_JSON_INVALID") from exc
    validate_control_state(state)

    # This file normally exists. An initial empty control branch may omit it.
    old = git(
        "show",
        f"{control_head}:{REQUEST_PATH.as_posix()}",
        cwd=repo,
        check=False,
        text=False,
    )
    if old.returncode:
        old_id = None
    else:
        try:
            old_doc = json.loads(old.stdout)
            old_id = old_doc.get("request_id")
        except (ValueError, TypeError, AttributeError) as exc:
            raise Stop("REQUEST_SUBMISSION_PREVIOUS_REQUEST_INVALID") from exc
    return state, state_bytes, old_id


def prepare_exact_request(
    template: dict[str, Any],
    *,
    state: dict[str, Any],
    state_bytes: bytes,
    control_head: str,
    live_main: str,
    last_request_id: str | None,
) -> dict[str, Any]:
    """Bind both predecessor fields from ONE authenticated control snapshot."""
    if not isinstance(template, dict):
        raise Stop("REQUEST_SUBMISSION_TEMPLATE_NOT_OBJECT")
    if any(
        field in template
        for field in (
            "previous_control_state_commit",
            "previous_control_state_sha256",
        )
    ):
        raise Stop("REQUEST_SUBMISSION_TEMPLATE_CONTAINS_PREDECESSOR")
    if template.get("operation") == OP_RECOVER:
        raise Stop("REQUEST_SUBMISSION_RECOVERY_REQUIRES_EXPLICIT_PATH")

    validate_control_state(state)
    if (
        state.get("lifecycle_state") != LIFECYCLE_IDLE
        or state.get("transaction_state")
        not in (
            TX_IDLE,
            TX_COMPLETE,
            TX_ABANDONED_NOT_ATTEMPTED,
            TX_ABANDONED_PREPARED,
        )
        or state.get("recovery_required") is not False
        or state.get("active_request_id") is not None
        or state.get("active_lock_commit") is not None
    ):
        raise Stop("REQUEST_SUBMISSION_CONTROL_NOT_SAFELY_IDLE")
    if template.get("expected_protected_main_sha") != live_main:
        raise Stop("REQUEST_SUBMISSION_EXPECTED_MAIN_CHANGED")

    request_id = template.get("request_id")
    if request_id == last_request_id or (
        isinstance(request_id, str) and request_used(state, request_id)
    ):
        raise Stop("REQUEST_SUBMISSION_REQUEST_ID_ALREADY_USED")

    request = copy.deepcopy(template)
    request["previous_control_state_commit"] = control_head
    request["previous_control_state_sha256"] = sha256_bytes(state_bytes)

    # This unchanged permanent validator checks the complete operation,
    # authority/gate fields, exact predecessor, main, and replay boundary.
    verify_request_predecessor(
        state, state_bytes, control_head, request, live_main
    )
    return request


def submit_request(
    repo: Path,
    template: dict[str, Any],
    *,
    submit: bool = False,
) -> dict[str, str]:
    """One bounded publication. Any moved ref, CAS error, or unsafe state stops."""
    repo = repo.resolve()
    main, control_head = fetch_exact_heads(repo)
    state, state_bytes, prior_id = read_control_snapshot(repo, control_head)
    request = prepare_exact_request(
        template,
        state=state,
        state_bytes=state_bytes,
        control_head=control_head,
        live_main=main,
        last_request_id=prior_id,
    )
    result = {
        "request_id": request["request_id"],
        "operation": request["operation"],
        "protected_main_sha": main,
        "previous_control_state_commit": control_head,
        "previous_control_state_sha256": sha256_bytes(state_bytes),
        "request_sha256": sha256_bytes(canonical_json_bytes(request)),
        "status": "VALIDATED_ONLY",
    }
    if not submit:
        return result
    if os.environ.get("GITHUB_ACTIONS", "").lower() == "true":
        raise Stop("REQUEST_SUBMISSION_ACTIONS_TOKEN_CANNOT_TRIGGER_PUSH_WORKFLOW")

    with tempfile.TemporaryDirectory(prefix="remote-implementation-request-") as tmp:
        worktree = Path(tmp) / "control"
        git("worktree", "add", "--detach", str(worktree), control_head, cwd=repo)
        try:
            path = worktree / REQUEST_PATH
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(canonical_json_bytes(request))
            git("add", "--", REQUEST_PATH.as_posix(), cwd=worktree)
            changed = git(
                "diff", "--cached", "--name-only", cwd=worktree
            ).stdout.splitlines()
            if changed != [REQUEST_PATH.as_posix()]:
                raise Stop("REQUEST_SUBMISSION_CHANGED_PATH_SCOPE_INVALID")
            git("config", "user.name", "remote-implementation-request", cwd=worktree)
            git(
                "config",
                "user.email",
                "41898282+github-actions[bot]@users.noreply.github.com",
                cwd=worktree,
            )
            git(
                "commit",
                "-m",
                f"Submit exact-bound remote Implementation request {request['request_id']}",
                cwd=worktree,
            )
            successor = git("rev-parse", "HEAD", cwd=worktree).stdout.strip()
            parent = git("rev-parse", "HEAD^", cwd=worktree).stdout.strip()
            if parent != control_head:
                raise Stop("REQUEST_SUBMISSION_COMMIT_PARENT_CHANGED")

            # Recheck both live authorities immediately before the single CAS.
            fresh_main, fresh_control = fetch_exact_heads(repo)
            if fresh_main != main or fresh_control != control_head:
                raise Stop("REQUEST_SUBMISSION_REFS_MOVED_BEFORE_CAS")

            push = git(
                "push",
                f"--force-with-lease=refs/heads/{CONTROL_BRANCH}:{control_head}",
                "origin",
                f"HEAD:refs/heads/{CONTROL_BRANCH}",
                cwd=worktree,
                check=False,
            )
            if push.returncode != 0:
                raise Stop("REQUEST_SUBMISSION_CONTROL_REF_CAS_FAILED\n" + push.stdout)
            result["status"] = "PUBLISHED_REQUEST_NOT_YET_ACCEPTED"
            result["request_commit_sha"] = successor
        finally:
            git(
                "worktree",
                "remove",
                "--force",
                str(worktree),
                cwd=repo,
                check=False,
            )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template",
        required=True,
        type=Path,
        help="Complete authorized request JSON without predecessor envelope keys",
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=ROOT,
        help="Existing repository checkout (default: current tool's repository)",
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Publish exactly one request; without this flag validate only",
    )
    args = parser.parse_args()
    try:
        template = json.loads(args.template.read_bytes())
    except (OSError, ValueError) as exc:
        raise Stop("REQUEST_SUBMISSION_TEMPLATE_UNREADABLE_OR_INVALID") from exc
    result = submit_request(args.repo, template, submit=args.submit)
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Stop as exc:
        print(f"FAIL: {exc}")
        raise SystemExit(1)
