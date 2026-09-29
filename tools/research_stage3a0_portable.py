#!/usr/bin/env python3
"""Build and verify the exact permanent-tool bundle used by Research Stage 3A-0."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

MANIFEST = "research-stage3a0-tool-manifest.json"
TOOL_PATHS = (
    "tools/research_stage3a0.py",
    "tools/research_stage3a0_portable.py",
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def required_paths(repo_root: Path) -> list[str]:
    missing = [rel for rel in TOOL_PATHS if not (repo_root / rel).is_file()]
    if missing:
        raise ValueError("missing required Stage 3A-0 tool files: " + ", ".join(missing))
    return list(TOOL_PATHS)


def build(repo_root: Path, output_dir: Path, main_sha: str) -> dict:
    if not SHA_RE.fullmatch(main_sha):
        raise ValueError("--main-sha must be a full 40-character lowercase commit SHA")
    repo_root = repo_root.resolve()
    output_dir = output_dir.resolve()
    if output_dir == repo_root or repo_root in output_dir.parents:
        raise ValueError("output directory must be outside the source repository")
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True)

    files = []
    for rel in required_paths(repo_root):
        src = repo_root / rel
        dst = output_dir / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        files.append({
            "path": rel,
            "sha256": sha256(dst),
            "size_bytes": dst.stat().st_size,
        })

    manifest = {
        "schema_version": 1,
        "protected_main_sha": main_sha,
        "stage3a0_tool_path": TOOL_PATHS[0],
        "portable_tool_path": TOOL_PATHS[1],
        "files": files,
    }
    (output_dir / MANIFEST).write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def verify(snapshot_dir: Path, main_sha: str) -> dict:
    if not SHA_RE.fullmatch(main_sha):
        raise ValueError("--main-sha must be a full 40-character lowercase commit SHA")
    snapshot_dir = snapshot_dir.resolve()
    manifest_path = snapshot_dir / MANIFEST
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    defects = []

    if manifest.get("protected_main_sha") != main_sha:
        defects.append({
            "reason": "PROTECTED_MAIN_SHA_MISMATCH",
            "expected": main_sha,
            "actual": manifest.get("protected_main_sha"),
        })

    listed = {
        item["path"]: item
        for item in manifest.get("files", [])
        if isinstance(item, dict) and item.get("path")
    }
    expected_paths = set(listed)
    actual_paths = {
        p.relative_to(snapshot_dir).as_posix()
        for p in snapshot_dir.rglob("*")
        if p.is_file() and p.name != MANIFEST
    }

    if actual_paths != expected_paths:
        defects.append({
            "reason": "SNAPSHOT_FILE_SET_MISMATCH",
            "missing": sorted(expected_paths - actual_paths),
            "extra": sorted(actual_paths - expected_paths),
        })

    required = set(TOOL_PATHS)
    if not required.issubset(expected_paths):
        defects.append({
            "reason": "SNAPSHOT_REQUIRED_PATH_MISSING",
            "paths": sorted(required - expected_paths),
        })

    for rel, item in listed.items():
        path = snapshot_dir / rel
        if not path.is_file():
            continue
        actual_sha = sha256(path)
        actual_size = path.stat().st_size
        if actual_sha != item.get("sha256") or actual_size != item.get("size_bytes"):
            defects.append({
                "reason": "SNAPSHOT_FILE_HASH_MISMATCH",
                "path": rel,
                "expected_sha256": item.get("sha256"),
                "actual_sha256": actual_sha,
                "expected_size_bytes": item.get("size_bytes"),
                "actual_size_bytes": actual_size,
            })

    return {
        "status": "COMPLETE" if not defects else "INVALID",
        "protected_main_sha": main_sha,
        "file_count": len(expected_paths),
        "defects": defects,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    build_p = sub.add_parser("build")
    build_p.add_argument("--repo-root", type=Path, default=Path("."))
    build_p.add_argument("--output-dir", type=Path, required=True)
    build_p.add_argument("--main-sha", required=True)

    verify_p = sub.add_parser("verify")
    verify_p.add_argument("snapshot_dir", type=Path)
    verify_p.add_argument("--main-sha", required=True)

    args = parser.parse_args()
    try:
        if args.command == "build":
            result = build(args.repo_root, args.output_dir, args.main_sha)
            print(json.dumps({
                "status": "COMPLETE",
                "protected_main_sha": result["protected_main_sha"],
                "file_count": len(result["files"]),
                "output_dir": str(args.output_dir),
            }, indent=2, sort_keys=True))
            return 0
        result = verify(args.snapshot_dir, args.main_sha)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["status"] == "COMPLETE" else 2
    except (OSError, ValueError, json.JSONDecodeError, KeyError) as exc:
        print(json.dumps(
            {"status": "INVALID", "error": str(exc)},
            indent=2,
            sort_keys=True,
        ))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
