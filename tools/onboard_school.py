#!/usr/bin/env python3
"""Permanent two-gate onboarding workflow for one school.

Examples:
    python tools/onboard_school.py vanderbilt --preflight
    python tools/onboard_school.py vanderbilt --approve --approved-by Elliott
    python tools/onboard_school.py vanderbilt --apply --approved-plan <sha256>
    python tools/onboard_school.py vanderbilt --verify

``--preflight`` and ``--approve`` never alter tracked repository data.
``--apply`` rehearses the complete mutation and verification in a disposable
copy, then copies only the allow-listed, already-validated files into the real
working tree.  A failure leaves the real working tree untouched.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from onboarding_plan import (
    WorkflowError,
    approve_plan,
    apply_publication_decisions,
    apply_reconciliation_decisions,
    archive_approved_plan,
    build_plan,
    verify_approved_plan,
    write_approved_plan,
    write_preflight_artifacts,
)


TEXT_SUFFIXES = {".csv", ".py", ".html", ".json", ".md", ".txt"}


def run(
    command: list[str],
    *,
    cwd: Path,
    label: str,
    echo: bool = True,
) -> str:
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
    )
    output = result.stdout.rstrip()
    if echo and output:
        print(output)
    if result.returncode:
        raise WorkflowError(
            f"{label} failed with exit code {result.returncode}"
            + (f"\n{output}" if not echo and output else "")
        )
    return output


def git(repo: Path, *args: str, echo: bool = False) -> str:
    return run(["git", *args], cwd=repo, label="git " + " ".join(args), echo=echo)


def ensure_clean_worktree(repo: Path) -> None:
    status = git(repo, "status", "--porcelain", "--untracked-files=all")
    if status.strip():
        raise WorkflowError(
            "--apply requires a clean tracked working tree. Commit the six-file "
            "package checkpoint first; leave .onboarding artifacts ignored.\n" + status
        )
    branch = git(repo, "branch", "--show-current").strip()
    if branch in {"", "main", "master"}:
        raise WorkflowError("--apply must run on a dedicated onboarding branch, never main")


def ensure_package_checkpoint(repo: Path) -> None:
    """Preflight/approval begin only from the committed six-file checkpoint."""
    branch = git(repo, "branch", "--show-current").strip()
    if branch in {"", "main", "master"}:
        raise WorkflowError(
            "preflight and approval must run on data/<school>-onboarding, never main"
        )
    status = git(repo, "status", "--porcelain", "--untracked-files=all")
    if status.strip():
        raise WorkflowError(
            "commit the complete six-file package and approved scope metadata before "
            "preflight/approval; tracked worktree changes remain:\n" + status
        )


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_hashes(root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if any(part in {".git", ".onboarding", "__pycache__"} for part in relative.parts):
            continue
        if path.suffix == ".pyc":
            continue
        result[relative.as_posix()] = file_sha(path)
    return result


def site_hashes(repo: Path) -> dict[str, str]:
    root = repo / "site/data"
    return {
        path.relative_to(repo).as_posix(): file_sha(path)
        for path in sorted(root.rglob("*.json"))
    }


def changed_paths(before: dict[str, str], after: dict[str, str]) -> list[str]:
    return sorted(
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    )


def allowed_apply_path(path: str, school_key: str, approved_hash: str) -> bool:
    exact = {
        "data/canonical/games.csv",
        "data/evidence/game-assertions.csv",
        "data/reconciliation/discrepancies.csv",
        "data/reference/programs.csv",
        "data/reference/program-accomplishments.csv",
        f"schools/{school_key}/source-games.csv",
        f"data/reconciliation/onboarding-decisions/{school_key}-{approved_hash[:12]}.json",
    }
    return path in exact or path.startswith("site/data/")


def whitespace_errors(repo: Path, paths: list[str]) -> list[str]:
    errors: list[str] = []
    for relative in paths:
        path = repo / relative
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        for line_number, line in enumerate(path.read_bytes().splitlines(), start=1):
            if line.endswith((b" ", b"\t")):
                errors.append(f"{relative}:{line_number}")
    return errors


def run_gates(
    repo: Path,
    school_key: str,
    changed: list[str] | None = None,
    *,
    include_tests: bool = True,
) -> dict[str, str]:
    python = sys.executable
    outputs: dict[str, str] = {}
    commands = [
        (
            "validation",
            [python, str(repo / "tools/validate_data.py"), str(repo)],
        ),
        (
            "target_no_op",
            [
                python,
                str(repo / "tools/ingest_school.py"),
                school_key,
                "--check-package",
                "--repo",
                str(repo),
            ],
        ),
        (
            "accomplishments",
            [
                python,
                str(repo / "tools/verify_program_accomplishments.py"),
                school_key,
                "--repo",
                str(repo),
            ],
        ),
        (
            "site_dry_run",
            [python, str(repo / "tools/build_site_data.py"), str(repo)],
        ),
    ]
    if include_tests:
        commands.append(
            (
                "unit_tests",
                [
                    python,
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    "tests",
                    "-p",
                    "test_*.py",
                ],
            )
        )
    for label, command in commands:
        print(f"\n=== {label} ===")
        outputs[label] = run(command, cwd=repo, label=label)
    if changed is not None:
        bad = whitespace_errors(repo, changed)
        if bad:
            raise WorkflowError(
                "genuine trailing spaces/tabs in changed text files:\n  "
                + "\n  ".join(bad[:50])
            )
        outputs["whitespace"] = "PASS: no genuine trailing spaces/tabs in changed text files."
        print("\n" + outputs["whitespace"])
    return outputs


def write_plan_for_ingest(repo: Path, approved: dict[str, Any]) -> Path:
    path = repo / ".approved-onboarding-plan.json"
    path.write_text(json.dumps(approved, indent=2) + "\n", encoding="utf-8")
    return path


def execute_approved_in_place(
    repo: Path,
    approved: dict[str, Any],
) -> dict[str, Any]:
    school_key = approved["school_key"]
    plan_path = write_plan_for_ingest(repo, approved)
    try:
        print("\n=== ingestion apply ===")
        ingestion_output = run(
            [
                sys.executable,
                str(repo / "tools/ingest_school.py"),
                school_key,
                "--apply",
                "--identity-decisions",
                str(plan_path),
                "--repo",
                str(repo),
            ],
            cwd=repo,
            label="ingestion apply",
        )
    finally:
        plan_path.unlink(missing_ok=True)

    print("\n=== generic reconciliation ===")
    reconciliation = apply_reconciliation_decisions(repo, approved)
    print(json.dumps(reconciliation, sort_keys=True))
    print("\n=== publication metadata ===")
    publication = apply_publication_decisions(repo, approved)
    print(json.dumps(publication, sort_keys=True))

    archive = archive_approved_plan(repo, approved)
    print(f"Archived sealed decisions: {archive.relative_to(repo)}")

    print("\n=== deterministic site build ===")
    site_output = run(
        [sys.executable, str(repo / "tools/build_site_data.py"), str(repo), "--apply"],
        cwd=repo,
        label="site build apply",
    )
    first_site_hashes = site_hashes(repo)
    run(
        [sys.executable, str(repo / "tools/build_site_data.py"), str(repo), "--apply"],
        cwd=repo,
        label="site build determinism replay",
        echo=False,
    )
    second_site_hashes = site_hashes(repo)
    if first_site_hashes != second_site_hashes:
        raise WorkflowError("site/data changed during the deterministic replay")
    print("PASS: repeated site build produced identical JSON hashes.")
    return {
        "ingestion_output": ingestion_output,
        "reconciliation": reconciliation,
        "publication": publication,
        "site_output": site_output,
        "archive": archive.relative_to(repo).as_posix(),
    }


def copy_repository(source: Path, destination: Path) -> None:
    def ignore(_directory: str, names: list[str]) -> set[str]:
        return {
            name
            for name in names
            if name in {".git", ".onboarding", "__pycache__"} or name.endswith(".pyc")
        }

    shutil.copytree(source, destination, ignore=ignore)


def copy_validated_changes(
    rehearsal: Path,
    repo: Path,
    after: dict[str, str],
    paths: list[str],
) -> None:
    for relative in paths:
        source = rehearsal / relative
        destination = repo / relative
        if relative not in after:
            if not relative.startswith("site/data/teams/"):
                raise WorkflowError(f"refusing unexpected deletion outside site teams: {relative}")
            destination.unlink(missing_ok=True)
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def visual_qa_markdown(repo: Path, school_key: str) -> str:
    payload_path = repo / "site/data/teams" / f"{school_key}.json"
    if not payload_path.is_file():
        return (
            f"# {school_key} visual QA\n\nThe page remains disabled by the approved plan.\n"
        )
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    games = payload.get("games", [])
    samples: list[dict[str, Any]] = []
    selectors = [
        lambda game: True,
        lambda game: game.get("overtime_periods", 0) > 0,
        lambda game: game.get("game_type") != "REGULAR_SEASON",
        lambda game: game.get("site") == "NEUTRAL",
    ]
    for selector in selectors:
        match = next((game for game in games if selector(game)), None)
        if match and match not in samples:
            samples.append(match)
    if games and games[-1] not in samples:
        samples.append(games[-1])
    summary = payload.get("summary", {})
    lines = [
        f"# {school_key} preview QA",
        "",
        "Approve merge only after checking the PR preview, not a local or production URL.",
        "",
        "## Expected headline",
        "",
        f"- Games: {summary.get('games', 0):,}",
        f"- Record: {summary.get('wins', 0):,}-{summary.get('losses', 0):,}"
        + (f"-{summary.get('ties', 0):,}" if summary.get("ties") else ""),
        f"- Opponents: {summary.get('opponents', 0):,}",
        f"- Seasons: {summary.get('first_season')} through {summary.get('last_season')}",
        "",
        "## Representative filters",
        "",
    ]
    for game in samples:
        lines.append(
            "- "
            + f"{game.get('game_date') or game.get('season_label')} vs. "
            + f"{game.get('opponent_name')}: {game.get('result')} "
            + f"{game.get('team_score')}-{game.get('opponent_score')}, "
            + f"{game.get('site')}, {game.get('venue_name') or '[venue unknown]'}"
        )
    lines.extend(
        [
            "",
            "## Existing-page smoke test",
            "",
            "Open every existing public program listed as affected in review.md, plus one unaffected page.",
            "Confirm routing, record totals, opponent links, and any approved reciprocal change.",
        ]
    )
    return "\n".join(lines) + "\n"


def pr_body(approved: dict[str, Any], changed: list[str]) -> str:
    summary = approved.get("summary", {})
    decisions = approved.get("decisions", [])
    discrepancy_decisions = [item for item in decisions if item["category"] == "discrepancy"]
    identity_decisions = [item for item in decisions if item["category"] == "identity"]
    dispositions = {}
    for item in discrepancy_decisions:
        dispositions[item["decision"]] = dispositions.get(item["decision"], 0) + 1
    lines = [
        "## Summary",
        "",
        f"- onboards `{approved['school_key']}` through the permanent sealed-plan workflow",
        f"- preserves {summary.get('source_rows', 0):,} source rows ({summary.get('pre_cutoff_rows', 0):,} pre-cutoff)",
        f"- matches {summary.get('existing_game_matches', 0):,} existing games and creates {summary.get('new_canonical_games', 0):,}",
        f"- applies {len(identity_decisions):,} owner-approved identity decisions",
        f"- records {len(discrepancy_decisions):,} dated discrepancy decisions",
        f"- approved plan `{approved['approved_plan_hash']}`",
    ]
    if dispositions:
        lines.append(
            "- discrepancy dispositions: "
            + ", ".join(f"{key}={value}" for key, value in sorted(dispositions.items()))
        )
    lines.extend(
        [
            "",
            "## Validation",
            "",
            "- repository validation — PASS",
            "- target package no-op — PASS",
            "- accomplishment cross-check — PASS",
            "- deterministic site build — PASS",
            "- unit tests — PASS",
            "- changed-file whitespace check — PASS",
            "",
            "## Change boundary",
            "",
        ]
    )
    lines.extend(f"- `{path}`" for path in changed)
    return "\n".join(lines) + "\n"


def transactional_apply(
    repo: Path,
    approved: dict[str, Any],
    output_dir: Path,
) -> dict[str, Any]:
    ensure_clean_worktree(repo)
    before = tree_hashes(repo)
    with tempfile.TemporaryDirectory(prefix=f"onboard-{approved['school_key']}-") as temporary:
        rehearsal = Path(temporary) / "repository"
        print(f"Rehearsing the sealed plan in {rehearsal}")
        copy_repository(repo, rehearsal)
        execution = execute_approved_in_place(rehearsal, approved)
        after = tree_hashes(rehearsal)
        changed = changed_paths(before, after)
        forbidden = [
            path
            for path in changed
            if not allowed_apply_path(path, approved["school_key"], approved["approved_plan_hash"])
        ]
        if forbidden:
            raise WorkflowError(
                "sealed apply attempted files outside the allow-list:\n  "
                + "\n  ".join(forbidden)
            )
        run_gates(rehearsal, approved["school_key"], changed, include_tests=True)
        copy_validated_changes(rehearsal, repo, after, changed)

    print("\n=== copied-state verification ===")
    copied_outputs = run_gates(
        repo,
        approved["school_key"],
        changed,
        include_tests=False,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "schema_version": 1,
        "school_key": approved["school_key"],
        "approved_plan_hash": approved["approved_plan_hash"],
        "base_commit": git(repo, "rev-parse", "HEAD").strip(),
        "branch": git(repo, "branch", "--show-current").strip(),
        "changed_paths": changed,
        "summary": approved.get("summary", {}),
        "execution": execution,
        "copied_state_gates": copied_outputs,
    }
    (output_dir / "release-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (output_dir / "pr-body.md").write_text(
        pr_body(approved, changed),
        encoding="utf-8",
    )
    (output_dir / "visual-qa.md").write_text(
        visual_qa_markdown(repo, approved["school_key"]),
        encoding="utf-8",
    )
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preflight, approve, transactionally apply, or verify one school onboarding."
    )
    parser.add_argument("school_key")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--preflight", action="store_true")
    mode.add_argument("--approve", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--approved-by", default="project-owner")
    parser.add_argument(
        "--approved-plan",
        default="",
        help="Exact SHA-256 emitted by --approve; required by --apply.",
    )
    parser.add_argument("--plan-file", type=Path, default=None)
    parser.add_argument("--review-file", type=Path, default=None)
    parser.add_argument("--approved-plan-file", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    output_dir = (
        args.output_dir.resolve()
        if args.output_dir
        else repo / ".onboarding" / args.school_key
    )
    plan_path = args.plan_file.resolve() if args.plan_file else output_dir / "plan.json"
    review_path = args.review_file.resolve() if args.review_file else output_dir / "review.csv"
    approved_path = (
        args.approved_plan_file.resolve()
        if args.approved_plan_file
        else output_dir / "approved-plan.json"
    )

    try:
        if args.preflight:
            ensure_package_checkpoint(repo)
            plan = build_plan(repo, args.school_key)
            paths = write_preflight_artifacts(plan, output_dir)
            summary = plan.get("summary", {})
            print("College Basketball History — sealed onboarding preflight")
            print(f"School:      {args.school_key}")
            print(f"Blockers:    {len(plan.get('blockers', [])):,}")
            print(f"Warnings:    {len(plan.get('warnings', [])):,}")
            print(f"Decisions:   {len(plan.get('decisions', [])):,}")
            if summary:
                print(
                    "Prediction:  "
                    f"{summary.get('existing_game_matches', 0):,} matches, "
                    f"{summary.get('new_canonical_games', 0):,} new, "
                    f"{summary.get('discrepancies_to_add', 0):,} definite / "
                    f"{summary.get('conditional_discrepancies', 0):,} conditional discrepancies"
                )
            print(f"Review:      {paths['report']}")
            print(f"Decision CSV:{paths['review']}")
            if plan.get("blockers"):
                print("\nSTOP: clear every blocker, then rerun --preflight.")
                return 1
            if plan.get("decisions"):
                print(
                    "\nOWNER GATE 1: fill decision and resolution_basis in review.csv, "
                    "then run --approve."
                )
            else:
                print("\nPASS: no owner decisions are pending for this already-complete state.")
            return 0

        if args.approve:
            ensure_package_checkpoint(repo)
            approved, approved_hash = approve_plan(
                repo,
                plan_path,
                review_path,
                args.approved_by,
            )
            path = write_approved_plan(approved, output_dir)
            print("OWNER GATE 1 SEALED")
            print(f"Approved plan: {approved_hash}")
            print(f"File:          {path}")
            print(
                "Apply exactly this reviewed state with:\n"
                f"python tools/onboard_school.py {args.school_key} --apply "
                f"--approved-plan {approved_hash}"
            )
            return 0

        if args.apply:
            if not approved_path.is_file():
                raise WorkflowError(f"approved plan file not found: {approved_path}")
            approved = json.loads(approved_path.read_text(encoding="utf-8"))
            verify_approved_plan(repo, approved, args.approved_plan)
            manifest = transactional_apply(repo, approved, output_dir)
            print("\nPASS: sealed plan applied transactionally and every automated gate passed.")
            print(f"Changed files: {len(manifest['changed_paths']):,}")
            print(f"Release manifest: {output_dir / 'release-manifest.json'}")
            print(
                "Next: python tools/release_school.py "
                f"{args.school_key} --prepare"
            )
            return 0

        changed = [
            line.strip()
            for line in git(repo, "diff", "--name-only", "HEAD").splitlines()
            if line.strip()
        ]
        run_gates(repo, args.school_key, changed, include_tests=True)
        print("\nPASS: verification suite completed.")
        return 0
    except (WorkflowError, FileNotFoundError, KeyError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
