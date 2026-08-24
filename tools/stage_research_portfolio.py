#!/usr/bin/env python3
"""Guarded RESEARCH_FROZEN -> INTEGRATION_FROZEN / Phase 0 staging.

Normal use from a clean ``data/<school>-onboarding`` branch created from current
``origin/main``:

    python tools/stage_research_portfolio.py <school> <research.zip> \
      --expected-sha256 <zip-sha> \
      --research-base <research_base_sha> \
      --history-start-season YYYY-YYYY \
      --history-scope-basis ALWAYS_TOP_LEVEL_FROM_INCEPTION \
      --history-scope-notes "Owner-confirmed scope..." \
      --apply --commit

The command verifies the immutable transport artifact, runs the permanent
research acceptance checks, rebases local venue identities against current
global references, registers only mechanically safe aliases/new identities,
installs the exact six-file package, applies the owner-confirmed history scope,
validates the repository, writes an ignored integration-freeze manifest, and
optionally creates the stable Phase 0 checkpoint commit.

Ambiguous physical venue identity is a STOP, never a guess.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from onboarding_hardening import research_portfolio_report
from onboarding_plan import (
    REQUIRED_PACKAGE_FILES,
    WorkflowError,
    write_csv_preserving_format,
)


def run(command: list[str], *, cwd: Path, echo: bool = False) -> str:
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    output = result.stdout.rstrip()
    if echo and output:
        print(output)
    if result.returncode:
        raise WorkflowError(f"command failed ({' '.join(command)}):\n{output}")
    return output


def git(repo: Path, *args: str, echo: bool = False) -> str:
    return run(["git", *args], cwd=repo, echo=echo)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_name(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").casefold())


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def copy_package(package: Path, destination: Path) -> None:
    if package.is_dir():
        names = sorted(p.name for p in package.iterdir() if p.is_file())
        if names != sorted(REQUIRED_PACKAGE_FILES):
            raise WorkflowError(
                "package directory must contain exactly the six required files"
            )
        for name in REQUIRED_PACKAGE_FILES:
            shutil.copy2(package / name, destination / name)
        return

    with zipfile.ZipFile(package) as archive:
        names = archive.namelist()
        if sorted(names) != sorted(REQUIRED_PACKAGE_FILES):
            raise WorkflowError(
                "research ZIP must contain exactly the six required flat files"
            )
        if any("/" in name or "\\" in name for name in names):
            raise WorkflowError("research ZIP members must be flat")
        archive.extractall(destination)


def venue_number(value: str) -> int | None:
    match = re.fullmatch(r"VEN-(\d{6})", value or "")
    return int(match.group(1)) if match else None


def next_venue_id(used: set[str]) -> str:
    numbers = [venue_number(value) for value in used]
    high = max((number for number in numbers if number is not None), default=0)
    while True:
        high += 1
        candidate = f"VEN-{high:06d}"
        if candidate not in used:
            return candidate


def geography_compatible(
    local: dict[str, str],
    global_row: dict[str, str],
) -> bool:
    lcity = local.get("city", "").strip().casefold()
    lstate = local.get("state", "").strip().upper()
    gcity = global_row.get("city", "").strip().casefold()
    gstate = global_row.get("state", "").strip().upper()
    if lcity and gcity and lcity != gcity:
        return False
    if lstate and gstate and lstate != gstate:
        return False
    return True


def rebase_venues(
    school_key: str,
    local_rows: list[dict[str, str]],
    global_rows: list[dict[str, str]],
    name_rows: list[dict[str, str]],
) -> tuple[
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, Any]],
]:
    global_by_key = {
        row.get("venue_key", "").strip(): row
        for row in global_rows
        if row.get("venue_key", "").strip()
    }
    global_by_id = {
        row.get("venue_id", "").strip(): row
        for row in global_rows
        if row.get("venue_id", "").strip()
    }

    ids_by_name: dict[str, set[str]] = {}
    for row in global_rows:
        normalized = normalize_name(row.get("display_name", ""))
        if normalized:
            ids_by_name.setdefault(normalized, set()).add(row["venue_id"])
    for row in name_rows:
        normalized = row.get("normalized_name", "").strip() or normalize_name(
            row.get("venue_name", "")
        )
        if normalized:
            ids_by_name.setdefault(normalized, set()).add(row["venue_id"])

    registered_names_by_id: dict[str, set[str]] = {}
    for row in name_rows:
        registered_names_by_id.setdefault(row["venue_id"], set()).add(
            row.get("normalized_name", "").strip()
            or normalize_name(row.get("venue_name", ""))
        )

    used_ids = set(global_by_id)
    mappings: list[dict[str, Any]] = []

    for local in local_rows:
        key = local.get("venue_key", "").strip()
        name = local.get("canonical_name", "").strip()
        research_id = local.get("venue_id", "").strip()
        proposed_id = research_id
        normalized = normalize_name(name)

        chosen: dict[str, str] | None = None
        reason = ""

        if key and key in global_by_key:
            candidate = global_by_key[key]
            if not geography_compatible(local, candidate):
                raise WorkflowError(
                    f"venue key {key!r} exists globally but geography conflicts: "
                    f"local={local.get('city','')},{local.get('state','')} "
                    f"global={candidate.get('city','')},{candidate.get('state','')}"
                )
            chosen = candidate
            reason = "REUSE_EXACT_KEY"

        if chosen is None and normalized:
            candidate_ids = {
                venue_id
                for venue_id in ids_by_name.get(normalized, set())
                if geography_compatible(local, global_by_id[venue_id])
            }
            if candidate_ids:
                raise WorkflowError(
                    f"venue {name!r} has a possible physical venue match "
                    f"({', '.join(sorted(candidate_ids))}) by name/geography, "
                    f"but venue_key {key!r} does not exactly match current main; "
                    "resolve physical identity explicitly before Phase 0"
                )

        # Research-time numeric venue IDs are provisional. A collision with
        # current main is never evidence that the physical venue is identical.
        if chosen is None and proposed_id in global_by_id:
            proposed_id = ""

        if chosen is None:
            final_id = (
                proposed_id
                if proposed_id and proposed_id not in used_ids
                else ""
            )
            if venue_number(final_id) is None:
                final_id = next_venue_id(used_ids)
            used_ids.add(final_id)

            chosen = {
                "venue_id": final_id,
                "venue_key": key,
                "display_name": name,
                "city": local.get("city", "").strip(),
                "state": local.get("state", "").strip(),
                "opened": local.get("known_opened", "").strip(),
                "closed": local.get("known_closed", "").strip(),
                "date_precision": (
                    local.get("venue_date_precision", "").strip().upper()
                    if local.get("venue_date_precision", "").strip().lower()
                    != "unknown"
                    else ""
                ),
                "identity_status": (
                    f"RESEARCHED_{school_key.upper().replace('-', '_')}_ONBOARDING"
                ),
                "source_basis": local.get("source_basis", "").strip(),
                "notes": (
                    f"Integrated from {school_key} research portfolio after "
                    "current-main physical-identity rebase."
                ),
            }
            if not chosen["venue_key"] or not chosen["display_name"]:
                raise WorkflowError(
                    "new venue identity requires venue_key and canonical_name: "
                    f"{local}"
                )
            global_rows.append(chosen)
            global_by_key[chosen["venue_key"]] = chosen
            global_by_id[chosen["venue_id"]] = chosen
            ids_by_name.setdefault(normalize_name(chosen["display_name"]), set()).add(
                chosen["venue_id"]
            )
            reason = "NEW_GLOBAL_IDENTITY"

        final_id = chosen["venue_id"]
        local["venue_id"] = final_id
        local_notes = local.get("notes", "").strip()
        integration_note = f"Integration rebase resolved final global venue ID {final_id}."
        local["notes"] = local_notes + (" " if local_notes else "") + integration_note

        candidate_names = [
            (
                name,
                "PROJECT_DISPLAY"
                if reason == "NEW_GLOBAL_IDENTITY"
                else "HISTORICAL_OR_ALIAS",
            )
        ]
        for alias in local.get("aliases", "").split(";"):
            alias = alias.strip()
            if alias:
                candidate_names.append((alias, "HISTORICAL_OR_ALIAS"))

        for candidate_name, name_type in candidate_names:
            normalized_candidate = normalize_name(candidate_name)
            if not normalized_candidate:
                continue
            if normalized_candidate in registered_names_by_id.get(final_id, set()):
                continue
            name_rows.append(
                {
                    "venue_id": final_id,
                    "venue_name": candidate_name,
                    "normalized_name": normalized_candidate,
                    "name_type": name_type,
                    "valid_from": "",
                    "valid_to": "",
                    "date_precision": "",
                    "source_basis": local.get("source_basis", "").strip(),
                    "notes": (
                        f"Registered during {school_key} onboarding current-main rebase."
                    ),
                }
            )
            registered_names_by_id.setdefault(final_id, set()).add(normalized_candidate)

        mappings.append(
            {
                "venue_key": key,
                "canonical_name": name,
                "research_venue_id": research_id,
                "final_venue_id": final_id,
                "resolution": reason,
            }
        )

    return local_rows, global_rows, name_rows, mappings


def update_program_scope(
    programs: list[dict[str, str]],
    school_key: str,
    *,
    start_season: str,
    basis: str,
    notes: str,
) -> None:
    targets = [row for row in programs if row.get("program_key") == school_key]
    if len(targets) != 1:
        raise WorkflowError(
            f"expected exactly one programs.csv row for {school_key}; found {len(targets)}"
        )
    row = targets[0]
    row["history_start_season"] = start_season
    row["history_scope_status"] = "OWNER_CONFIRMED"
    row["history_scope_basis"] = basis
    row["history_scope_notes"] = notes


def package_hashes(root: Path) -> dict[str, str]:
    return {name: sha256_file(root / name) for name in REQUIRED_PACKAGE_FILES}


def ensure_phase0_state(
    repo: Path,
    school_key: str,
    research_base: str,
) -> tuple[str, str]:
    branch = git(repo, "branch", "--show-current").strip()
    if branch != f"data/{school_key}-onboarding":
        raise WorkflowError(
            f"Phase 0 requires branch data/{school_key}-onboarding; "
            f"current={branch or '[detached]'}"
        )
    if git(repo, "status", "--porcelain", "--untracked-files=all").strip():
        raise WorkflowError("Phase 0 requires a clean working tree")
    head = git(repo, "rev-parse", "HEAD").strip()
    origin_main = git(repo, "rev-parse", "origin/main").strip()
    if head != origin_main:
        raise WorkflowError(
            "Phase 0 branch must still point exactly at current origin/main before staging; "
            f"HEAD={head}, origin/main={origin_main}"
        )
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", research_base, head],
        cwd=repo,
    )
    if result.returncode != 0:
        raise WorkflowError(
            f"research_base_sha {research_base} is not an ancestor of current main {head}"
        )
    return head, origin_main


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Guarded current-main staging of one RESEARCH_FROZEN portfolio."
    )
    parser.add_argument("school_key")
    parser.add_argument("package", type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--research-base", required=True)
    parser.add_argument("--history-start-season", required=True)
    parser.add_argument("--history-scope-basis", required=True)
    parser.add_argument("--history-scope-notes", required=True)
    parser.add_argument("--repo", type=Path, default=None)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--commit", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    package = args.package.resolve()

    try:
        if args.commit and not args.apply:
            raise WorkflowError("--commit requires --apply")

        actual_sha = sha256_file(package)
        if actual_sha.lower() != args.expected_sha256.lower():
            raise WorkflowError(
                f"research ZIP SHA-256 mismatch: expected {args.expected_sha256}, "
                f"found {actual_sha}"
            )

        current_head, origin_main = ensure_phase0_state(
            repo,
            args.school_key,
            args.research_base,
        )

        acceptance = research_portfolio_report(
            package,
            school_key=args.school_key,
            expected_sha256=args.expected_sha256,
        )
        if acceptance["status"] != "PASS":
            for error in acceptance["errors"]:
                print("  - " + error)
            raise WorkflowError(
                "research portfolio acceptance failed with "
                f"{len(acceptance['errors'])} error(s)"
            )

        if (repo / "schools" / args.school_key).exists():
            raise WorkflowError(
                f"schools/{args.school_key} already exists; Phase 0 will not overwrite it"
            )

        with tempfile.TemporaryDirectory(prefix=f"stage-{args.school_key}-") as temporary:
            temp_root = Path(temporary)
            package_root = temp_root / "package"
            package_root.mkdir()
            copy_package(package, package_root)

            local_fields, local_venues = load_csv(package_root / "venues.csv")
            global_fields, global_venues = load_csv(repo / "data/reference/venues.csv")
            name_fields, venue_names = load_csv(repo / "data/reference/venue-names.csv")
            program_fields, programs = load_csv(repo / "data/reference/programs.csv")

            (
                local_venues,
                global_venues,
                venue_names,
                mappings,
            ) = rebase_venues(
                args.school_key,
                local_venues,
                global_venues,
                venue_names,
            )

            update_program_scope(
                programs,
                args.school_key,
                start_season=args.history_start_season,
                basis=args.history_scope_basis,
                notes=args.history_scope_notes,
            )

            write_csv_preserving_format(
                package_root / "venues.csv",
                local_fields,
                local_venues,
            )
            notes_path = package_root / "notes.md"
            notes = notes_path.read_text(encoding="utf-8")
            if not notes.endswith("\n"):
                notes += "\n"
            notes += (
                "\n## Integration staging\n\n"
                "Current-main shared-reference rebase completed against "
                f"`integration_base_sha={current_head}` from "
                f"`research_base_sha={args.research_base}`. "
                "The authoritative final venue-ID mapping is recorded in the ignored "
                "`.onboarding/<school>/integration-freeze.json` manifest. "
                "Status: **INTEGRATION_FROZEN**.\n"
            )
            notes_path.write_text(notes, encoding="utf-8")

            staged_hashes = {
                name: sha256_file(package_root / name)
                for name in REQUIRED_PACKAGE_FILES
            }
            manifest = {
                "schema_version": 1,
                "school_key": args.school_key,
                "status": "INTEGRATION_FROZEN",
                "research_base_sha": args.research_base,
                "integration_base_sha": current_head,
                "origin_main_sha": origin_main,
                "research_zip_sha256": actual_sha,
                "package_member_sha256": staged_hashes,
                "venue_mapping": mappings,
                "history_scope": {
                    "history_start_season": args.history_start_season,
                    "history_scope_status": "OWNER_CONFIRMED",
                    "history_scope_basis": args.history_scope_basis,
                    "history_scope_notes": args.history_scope_notes,
                },
            }

            print("College Basketball History — Phase 0 staging")
            print(f"School:                {args.school_key}")
            print(f"Research base:         {args.research_base}")
            print(f"Integration base:      {current_head}")
            print(f"Research ZIP SHA-256:  {actual_sha}")
            print(f"Venue rows rebased:    {len(mappings)}")
            print("Venue outcomes:")
            for key, count in sorted(
                {
                    value: sum(
                        1 for row in mappings if row["resolution"] == value
                    )
                    for value in {row["resolution"] for row in mappings}
                }.items()
            ):
                print(f"  {key}: {count}")

            if not args.apply:
                print(
                    "\nDRY RUN COMPLETE: no repository files changed. "
                    "Rerun with --apply (and normally --commit) after reviewing the mapping."
                )
                return 0

            school_dir = repo / "schools" / args.school_key
            school_dir.mkdir()
            for name in REQUIRED_PACKAGE_FILES:
                shutil.copy2(package_root / name, school_dir / name)

            write_csv_preserving_format(
                repo / "data/reference/programs.csv",
                program_fields,
                programs,
            )
            write_csv_preserving_format(
                repo / "data/reference/venues.csv",
                global_fields,
                global_venues,
            )
            write_csv_preserving_format(
                repo / "data/reference/venue-names.csv",
                name_fields,
                venue_names,
            )

            output_dir = repo / ".onboarding" / args.school_key
            output_dir.mkdir(parents=True, exist_ok=True)
            manifest_path = output_dir / "integration-freeze.json"
            manifest_path.write_text(
                json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

        run(
            [sys.executable, str(repo / "tools/validate_data.py")],
            cwd=repo,
            echo=True,
        )

        expected_paths = [
            "data/reference/programs.csv",
            "data/reference/venues.csv",
            "data/reference/venue-names.csv",
            *[
                f"schools/{args.school_key}/{name}"
                for name in REQUIRED_PACKAGE_FILES
            ],
        ]
        print("\nPASS: Phase 0 files installed and repository validation passed.")
        print(
            "Integration manifest: "
            f"{repo / '.onboarding' / args.school_key / 'integration-freeze.json'}"
        )

        if args.commit:
            git(repo, "add", *expected_paths)
            staged = [
                line.strip()
                for line in git(repo, "diff", "--cached", "--name-only").splitlines()
                if line.strip()
            ]
            unexpected = sorted(set(staged) - set(expected_paths))
            if unexpected:
                raise WorkflowError(
                    "refusing Phase 0 commit with unexpected staged paths: "
                    + ", ".join(unexpected)
                )
            if not staged:
                raise WorkflowError("Phase 0 produced no staged files")
            message = (
                f"Add {args.school_key.replace('-', ' ').title()} onboarding source package"
            )
            git(repo, "commit", "-m", message, echo=True)
            print("\nPHASE 0 CHECKPOINT CREATED")
            print("HEAD: " + git(repo, "rev-parse", "HEAD").strip())
            if git(repo, "status", "--porcelain").strip():
                raise WorkflowError(
                    "Phase 0 checkpoint created but worktree is not clean"
                )
            print("Worktree: clean")
            print(
                f"Next: python tools/onboard_school.py {args.school_key} --preflight"
            )
        else:
            print(
                "Next: explicitly stage and commit the Phase 0 paths before preflight, "
                "or rerun with --commit in a fresh checkout."
            )
        return 0

    except (
        WorkflowError,
        FileNotFoundError,
        KeyError,
        ValueError,
        zipfile.BadZipFile,
    ) as exc:
        print(f"FAIL: {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
