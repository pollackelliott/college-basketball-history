#!/usr/bin/env python3
"""Freeze and stage bounded corrections to already-published schools.

This is an additive path.  New-school onboarding continues to use the existing
research-check / stage_research_portfolio workflow unchanged.
"""
from __future__ import annotations

import argparse
import csv
import difflib
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from integration_freeze_guard import build_source_game_semantic_snapshot, semantic_snapshot_sha256
from onboarding_plan import REQUIRED_PACKAGE_FILES, WorkflowError
from site_completeness import source_home_chronology_report, source_site_completeness_report

WORKFLOW_KIND = "POST_PUBLICATION_CORRECTION"


def run(cmd: list[str], repo: Path, *, echo: bool = False) -> str:
    p = subprocess.run(cmd, cwd=repo, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = p.stdout.rstrip()
    if echo and out:
        print(out)
    if p.returncode:
        raise WorkflowError(f"command failed ({' '.join(cmd)}):\n{out}")
    return out


def git(repo: Path, *args: str) -> str:
    return run(["git", *args], repo)


def git_bytes(repo: Path, *args: str) -> bytes:
    p = subprocess.run(["git", *args], cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode:
        raise WorkflowError(p.stderr.decode("utf-8", "replace").strip())
    return p.stdout


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    return sha_bytes(path.read_bytes())


def sha_json(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return sha_bytes(raw)


def csv_bytes(data: bytes) -> tuple[list[str], list[dict[str, str]]]:
    r = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""))
    return list(r.fieldnames or []), list(r)


def csv_file(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return csv_bytes(path.read_bytes())


def extract_flat_six(path: Path) -> tuple[tempfile.TemporaryDirectory[str], Path]:
    temp = tempfile.TemporaryDirectory(prefix="correction-package-")
    root = Path(temp.name)
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        if sorted(names) != sorted(REQUIRED_PACKAGE_FILES) or any("/" in n or "\\" in n for n in names):
            temp.cleanup()
            raise WorkflowError(f"candidate ZIP must contain exactly six flat package files; found {names}")
        z.extractall(root)
    return temp, root


def baseline(repo: Path, school: str, base_sha: str) -> dict[str, bytes]:
    git(repo, "cat-file", "-e", f"{base_sha}^{{commit}}")
    out: dict[str, bytes] = {}
    for name in REQUIRED_PACKAGE_FILES:
        out[name] = git_bytes(repo, "show", f"{base_sha}:schools/{school}/{name}")
    return out


def by_id(fields: list[str], rows: list[dict[str, str]], label: str) -> dict[str, dict[str, str]]:
    if "source_game_id" not in fields:
        raise WorkflowError(f"{label} source-games.csv lacks source_game_id")
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        key = row.get("source_game_id", "").strip()
        if not key or key in out:
            raise WorkflowError(f"{label} source-games.csv has blank/duplicate source_game_id {key!r}")
        out[key] = row
    return out


def source_game_diff(before: bytes, after: bytes) -> dict[str, Any]:
    bf, br = csv_bytes(before)
    af, ar = csv_bytes(after)
    if bf != af:
        raise WorkflowError("correction must preserve source-games.csv header")
    b, a = by_id(bf, br, "baseline"), by_id(af, ar, "candidate")
    deleted = sorted(set(b) - set(a))
    if deleted:
        raise WorkflowError("correction lifecycle does not support deleting published source games: " + ", ".join(deleted[:20]))
    added = [a[k] for k in sorted(set(a) - set(b))]
    modified = []
    for key in sorted(set(a) & set(b)):
        fields = {f: {"before": b[key].get(f, ""), "after": a[key].get(f, "")}
                  for f in bf if b[key].get(f, "") != a[key].get(f, "")}
        if fields:
            modified.append({"source_game_id": key, "fields": fields})
    ids = [r["source_game_id"] for r in added] + [r["source_game_id"] for r in modified]
    return {"added": added, "modified": modified, "deleted": [],\n            "added_count": len(added), "modified_count": len(modified), "deleted_count": 0,\n            "changed_source_game_ids": ids}


def exact_diff(base: dict[str, bytes], root: Path) -> dict[str, Any]:
    members = {}
    for name in REQUIRED_PACKAGE_FILES:
        before, after = base[name], (root / name).read_bytes()
        unified = ""
        if before != after and name != "source-games.csv":
            unified = "".join(difflib.unified_diff(
                before.decode("utf-8-sig").splitlines(keepends=True),
                after.decode("utf-8-sig").splitlines(keepends=True),
                fromfile=f"baseline/{name}", tofile=f"candidate/{name}"))
        members[name] = {"baseline_sha256": sha_bytes(before), "candidate_sha256": sha_bytes(after),
                         "changed": before != after, "unified_diff": unified}
    return {"schema_version": 1, "members": members,
            "source_games": source_game_diff(base["source-games.csv"], (root / "source-games.csv").read_bytes())}


def validate_correction_candidate(root: Path, school_key: str, changed_source_game_ids: list[str]) -> dict[str, Any]:
    fields, games = csv_file(root / "source-games.csv")
    _, opponents = csv_file(root / "opponents.csv")
    _, venues = csv_file(root / "venues.csv")
    rows = by_id(fields, games, "candidate")
    ids = list(changed_source_game_ids)\n    school = school_key\n    missing = sorted(set(ids) - set(rows))
    errors = ["missing correction source IDs: " + ", ".join(missing)] if missing else []
    changed = [rows[k] for k in ids if k in rows]
    opp_keys = {r.get("canonical_opponent_key", "").strip() for r in opponents}
    venue_names = set()
    for v in venues:
        venue_names.add(v.get("canonical_name", "").strip().casefold())
        venue_names.update(x.strip().casefold() for x in v.get("aliases", "").split(";") if x.strip())
    for r in changed:
        sid = r.get("source_game_id", "")
        if r.get("source_program_key", "").strip() != school:
            errors.append(f"{sid}: wrong source_program_key")
        if r.get("normalized_opponent_key", "").strip() not in opp_keys:
            errors.append(f"{sid}: normalized opponent absent from opponents.csv")
        venue = r.get("curated_venue_name", "").strip()
        if venue and venue.casefold() not in venue_names:
            errors.append(f"{sid}: curated venue {venue!r} absent from venues.csv")
    site = source_site_completeness_report(fields, changed)
    home = source_home_chronology_report(changed, venues, school_key=school)
    errors.extend(site["errors"]); errors.extend(home["errors"])
    return {"status": "PASS" if not errors else "FAIL", "errors": errors,
            "warnings": [*site["warnings"], *home["warnings"]],
            "counts": {"changed_source_games": len(changed), "site": site["counts"], "home": home["counts"]}}


def write_freeze(path: Path, manifest: dict[str, Any], root: Path) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("correction-freeze.json", json.dumps(manifest, indent=2, sort_keys=True) + "\n")
        for name in REQUIRED_PACKAGE_FILES:
            z.write(root / name, f"package/{name}")


def freeze(args: argparse.Namespace, repo: Path) -> int:
    base = baseline(repo, args.school_key, args.research_base)
    temp, root = extract_flat_six(args.candidate_zip.resolve())
    try:
        diff = exact_diff(base, root)
        diff_sha = sha_json(diff)
        ids = diff["source_games"]["changed_source_game_ids"]
        if not ids:
            raise WorkflowError("candidate changes no source-game rows")
        acceptance = validate_correction_candidate(root, args.school_key, ids)
        report = {"school_key": args.school_key, "research_base_sha": args.research_base,
                  "scope": args.scope, "research_authority_ref": args.research_authority_ref,
                  "research_authority_digest": args.research_authority_digest,
                  "correction_diff_sha256": diff_sha, "correction_diff": diff,
                  "scoped_acceptance": acceptance}
        print(json.dumps(report, indent=2, sort_keys=True))
        if args.report_json:
            args.report_json.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
        if acceptance["status"] != "PASS":
            raise WorkflowError("candidate failed scoped correction acceptance")
        if not args.expected_diff_sha256:
            print("\nCORRECTION DIFF REVIEW REQUIRED; rerun with --expected-diff-sha256 " + diff_sha)
            return 0
        if args.expected_diff_sha256.lower() != diff_sha.lower():
            raise WorkflowError(f"correction diff SHA mismatch: expected {args.expected_diff_sha256}, found {diff_sha}")
        if args.scope == "season-supplement" and not args.required_completed_season_cutoff:
            raise WorkflowError("season-supplement requires --required-completed-season-cutoff")
        if not args.output:
            raise WorkflowError("--output is required to freeze an acknowledged diff")
        manifest = {"schema_version": 1, "workflow_kind": WORKFLOW_KIND,
                    "status": "CORRECTION_RESEARCH_FROZEN", "school_key": args.school_key,
                    "research_base_sha": args.research_base, "scope": args.scope,
                    "research_authority": {"ref": args.research_authority_ref, "digest": args.research_authority_digest},
                    "required_completed_season_cutoff": args.required_completed_season_cutoff,
                    "baseline_package_sha256": {n: sha_bytes(v) for n, v in base.items()},
                    "candidate_package_sha256": {n: sha_file(root / n) for n in REQUIRED_PACKAGE_FILES},
                    "correction_diff_sha256": diff_sha, "correction_diff": diff,
                    "correction_source_game_ids": ids, "scoped_acceptance": acceptance}
        write_freeze(args.output.resolve(), manifest, root)
        print("\nCORRECTION_RESEARCH_FROZEN: YES")
        print(f"SHA-256: {sha_file(args.output.resolve())}")
        return 0
    finally:
        temp.cleanup()


def extract_freeze(path: Path, expected_sha: str):
    actual = sha_file(path)
    if actual.lower() != expected_sha.lower():
        raise WorkflowError(f"correction freeze SHA mismatch: expected {expected_sha}, found {actual}")
    temp = tempfile.TemporaryDirectory(prefix="correction-freeze-")
    root = Path(temp.name)
    with zipfile.ZipFile(path) as z:
        expected = sorted(["correction-freeze.json", *[f"package/{n}" for n in REQUIRED_PACKAGE_FILES]])
        if sorted(z.namelist()) != expected:
            temp.cleanup(); raise WorkflowError("invalid correction freeze ZIP members")
        z.extractall(root)
    manifest = json.loads((root / "correction-freeze.json").read_text())
    if manifest.get("workflow_kind") != WORKFLOW_KIND or manifest.get("status") != "CORRECTION_RESEARCH_FROZEN":
        temp.cleanup(); raise WorkflowError("invalid correction freeze manifest")
    return temp, root / "package", manifest, actual


def validate_registered_venues(repo: Path, root: Path, ids: list[str]) -> None:
    fields, games = csv_file(root / "source-games.csv")
    _, venues = csv_file(root / "venues.csv")
    _, global_venues = csv_file(repo / "data/reference/venues.csv")
    rows = by_id(fields, games, "frozen")
    global_pairs = {(r.get("venue_key", "").strip(), r.get("venue_id", "").strip()) for r in global_venues}
    names: dict[str, list[dict[str, str]]] = {}
    for v in venues:
        for name in [v.get("canonical_name", ""), *v.get("aliases", "").split(";")]:
            if name.strip(): names.setdefault(name.strip().casefold(), []).append(v)
    for sid in ids:
        venue = rows[sid].get("curated_venue_name", "").strip()
        if not venue: continue
        candidates = names.get(venue.casefold(), [])
        if not any((v.get("venue_key", "").strip(), v.get("venue_id", "").strip()) in global_pairs for v in candidates):
            raise WorkflowError(f"{sid}: venue {venue!r} is not already registered on current main")


def stage(args: argparse.Namespace, repo: Path) -> int:
    temp, root, frozen, freeze_sha = extract_freeze(args.freeze_zip.resolve(), args.expected_sha256)
    try:
        school = args.school_key
        if frozen.get("school_key") != school: raise WorkflowError("freeze belongs to another school")
        branch = git(repo, "branch", "--show-current").strip()
        if branch != f"data/{school}-correction": raise WorkflowError(f"requires branch data/{school}-correction; current={branch}")
        if git(repo, "status", "--porcelain", "--untracked-files=all").strip(): raise WorkflowError("requires clean working tree")
        run(["git", "fetch", "origin", "main"], repo)
        head, origin = git(repo, "rev-parse", "HEAD").strip(), git(repo, "rev-parse", "origin/main").strip()
        if head != origin: raise WorkflowError("correction branch must point exactly at current origin/main")
        git(repo, "merge-base", "--is-ancestor", frozen["research_base_sha"], origin)
        school_dir = repo / "schools" / school
        current = {n: sha_file(school_dir / n) for n in REQUIRED_PACKAGE_FILES}
        drift = [n for n in REQUIRED_PACKAGE_FILES if current[n] != frozen["baseline_package_sha256"][n]]
        if drift: raise WorkflowError("target package changed since correction Research: " + ", ".join(drift))
        ids = list(frozen["correction_source_game_ids"])
        acceptance = validate_correction_candidate(root, school, ids)
        if acceptance["status"] != "PASS": raise WorkflowError("frozen candidate no longer passes scoped acceptance")
        validate_registered_venues(repo, root, ids)
        pre = build_source_game_semantic_snapshot(school_dir / "source-games.csv")
        post = build_source_game_semantic_snapshot(root / "source-games.csv")
        _, programs = csv_file(repo / "data/reference/programs.csv")
        program = next((r for r in programs if r.get("program_key") == school), None)
        if not program: raise WorkflowError(f"program registry has no row for {school}")
        manifest = {"schema_version": 2, "workflow_kind": WORKFLOW_KIND, "status": "INTEGRATION_FROZEN",
                    "school_key": school, "research_base_sha": frozen["research_base_sha"],
                    "integration_base_sha": head, "origin_main_sha": origin,
                    "research_zip_sha256": freeze_sha, "correction_freeze_sha256": freeze_sha,
                    "correction_diff_sha256": frozen["correction_diff_sha256"],
                    "correction_source_game_ids": ids,
                    "package_member_sha256": {n: sha_file(root / n) for n in REQUIRED_PACKAGE_FILES},
                    "pre_correction_source_semantic_guard": {"schema_version": 1, "snapshot_sha256": semantic_snapshot_sha256(pre), "snapshot": pre},
                    "source_game_semantic_guard": {"schema_version": 1, "snapshot_sha256": semantic_snapshot_sha256(post), "snapshot": post},
                    "venue_mapping": [], "program_alias_mapping": [], "conference_mapping": [], "conference_reconciliation": None,
                    "history_scope": {"history_start_season": program.get("history_start_season", ""),
                                      "history_scope_intervals": program.get("history_scope_intervals", ""),
                                      "history_scope_status": "INHERITED_PUBLISHED",
                                      "history_scope_basis": "Published protected-main scope; correction does not alter scope.",
                                      "history_scope_notes": "Post-publication bounded correction."}}
        print(f"School: {school}\nIntegration base: {head}\nCorrection freeze: {freeze_sha}\nCorrection source IDs: {len(ids)}")
        if not args.apply:
            print("DRY RUN COMPLETE: no repository files changed."); return 0
        onboard = repo / ".onboarding" / school; onboard.mkdir(parents=True, exist_ok=True)
        manifest_path = onboard / "integration-freeze.json"
        old = {n: (school_dir / n).read_bytes() for n in REQUIRED_PACKAGE_FILES}
        old_manifest = manifest_path.read_bytes() if manifest_path.exists() else None
        try:
            for n in REQUIRED_PACKAGE_FILES: shutil.copy2(root / n, school_dir / n)
            manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
            run([sys.executable, str(repo / "tools/validate_data.py")], repo, echo=True)
        except Exception:
            for n, data in old.items(): (school_dir / n).write_bytes(data)
            if old_manifest is None: manifest_path.unlink(missing_ok=True)
            else: manifest_path.write_bytes(old_manifest)
            raise
        expected = [f"schools/{school}/{n}" for n in REQUIRED_PACKAGE_FILES]
        print("PASS: correction package installed and repository validation passed.")
        if args.commit:
            run(["git", "add", *expected], repo)
            staged = [x for x in git(repo, "diff", "--cached", "--name-only").splitlines() if x]
            if set(staged) - set(expected): raise WorkflowError("unexpected staged paths")
            if not staged: raise WorkflowError("correction staging produced no tracked changes")
            run(["git", "commit", "-m", f"Stage {school.replace('-', ' ').title()} correction package"], repo, echo=True)
        return 0
    finally:
        temp.cleanup()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    f = sub.add_parser("freeze"); f.add_argument("school_key"); f.add_argument("candidate_zip", type=Path)
    f.add_argument("--research-base", required=True); f.add_argument("--scope", choices=("season-supplement", "field-correction"), required=True)
    f.add_argument("--research-authority-ref", required=True); f.add_argument("--research-authority-digest", required=True)
    f.add_argument("--required-completed-season-cutoff", default=""); f.add_argument("--expected-diff-sha256", default="")
    f.add_argument("--report-json", type=Path); f.add_argument("--output", type=Path); f.add_argument("--repo", type=Path)
    s = sub.add_parser("stage"); s.add_argument("school_key"); s.add_argument("freeze_zip", type=Path); s.add_argument("--expected-sha256", required=True)
    s.add_argument("--apply", action="store_true"); s.add_argument("--commit", action="store_true"); s.add_argument("--repo", type=Path)
    return p.parse_args()


def main() -> int:
    args = parse_args(); repo = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[1]
    try:
        if args.command == "freeze": return freeze(args, repo)
        if args.commit and not args.apply: raise WorkflowError("--commit requires --apply")
        return stage(args, repo)
    except (WorkflowError, FileNotFoundError, KeyError, ValueError, zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}"); return 1


if __name__ == "__main__":
    raise SystemExit(main())