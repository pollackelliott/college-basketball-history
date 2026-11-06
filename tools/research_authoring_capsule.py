#!/usr/bin/env python3
"""Generic Stage 4 authoring-capsule carry-forward and continuity guards.

Research checkpoints may carry package-authoring authority under
stage4-authoring/.  Later research substages must preserve inherited members
byte-for-byte unless the current substage explicitly owns and updates that
member.  This module provides the permanent, school-agnostic mechanics for
that invariant and a fail-closed continuity audit for legacy checkpoint chains.

It never reconstructs missing historical authority from current registries,
conversation state, or web research.  If bytes are gone, the only safe result
is a precise missing-authority defect.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

AUTHORING_DIR = "stage4-authoring"
AUTHORING_BASENAMES = frozenset(
    {
        "opponents.csv",
        "venues.csv",
        "conferences.csv",
        "early-history-uncertainty.json",
        "season-coverage.json",
    }
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _basename(member: str) -> str:
    return Path(member).name.lower()


def discover_authoring_members(
    archive: zipfile.ZipFile,
) -> dict[str, dict[str, Any]]:
    """Return unique authoring members keyed by normalized basename.

    A checkpoint with two candidate members for the same logical authoring file
    is ambiguous and therefore invalid for deterministic carry-forward.
    """

    by_basename: dict[str, list[str]] = {}
    for name in archive.namelist():
        if name.endswith("/") or "/stage4-authoring/" not in "/" + name:
            continue
        basename = _basename(name)
        if basename not in AUTHORING_BASENAMES:
            continue
        by_basename.setdefault(basename, []).append(name)

    result: dict[str, dict[str, Any]] = {}
    for basename, members in sorted(by_basename.items()):
        if len(members) != 1:
            raise ValueError(
                "AMBIGUOUS_STAGE4_AUTHORING_MEMBER: "
                + basename
                + ":"
                + ",".join(sorted(members))
            )
        member = members[0]
        data = archive.read(member)
        result[basename] = {
            "member": member,
            "sha256": sha256_bytes(data),
            "bytes": data,
        }
    return result


def carry_authoring_capsule(
    archive: zipfile.ZipFile,
    out: Path,
    *,
    owned_updates: set[str] | frozenset[str] = frozenset(),
) -> dict[str, dict[str, str]]:
    """Carry inherited authoring members to out without silent mutation.

    Members named in owned_updates may be replaced later by the current
    substage and are therefore not copied.  Every other inherited member is
    written byte-for-byte.  If an already-existing output differs, fail closed.
    """

    unknown_owned = set(owned_updates) - AUTHORING_BASENAMES
    if unknown_owned:
        raise ValueError(
            "UNKNOWN_STAGE4_AUTHORING_OWNED_MEMBER: "
            + ",".join(sorted(unknown_owned))
        )

    carried: dict[str, dict[str, str]] = {}
    for basename, metadata in discover_authoring_members(archive).items():
        if basename in owned_updates:
            continue
        data = metadata["bytes"]
        target = out / AUTHORING_DIR / basename
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and target.read_bytes() != data:
            raise ValueError(
                "STAGE4_AUTHORING_INHERITED_MEMBER_CHANGED: " + basename
            )
        target.write_bytes(data)
        carried[basename] = {
            "input_member": str(metadata["member"]),
            "sha256": str(metadata["sha256"]),
            "output_path": str(target),
        }
    return carried


def _declared_carried_hashes_from_payload(
    payload: Any,
) -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    if not isinstance(payload, dict):
        return found
    carried = payload.get("stage4_authoring_carried")
    if not isinstance(carried, dict):
        return found
    for basename, metadata in carried.items():
        normalized = str(basename).strip().lower()
        if normalized not in AUTHORING_BASENAMES or not isinstance(metadata, dict):
            continue
        digest = str(metadata.get("sha256", "")).strip().lower()
        if len(digest) == 64 and all(ch in "0123456789abcdef" for ch in digest):
            found.setdefault(normalized, set()).add(digest)
    return found


def historical_carry_claims(
    archive: zipfile.ZipFile,
) -> dict[str, list[dict[str, str]]]:
    """Collect prior hash-bound carry claims serialized inside a checkpoint.

    This intentionally consumes only the checkpoint's own JSON artifacts.  It
    does not look at current repository registries or external state.
    """

    claims: dict[str, list[dict[str, str]]] = {}
    for member in sorted(archive.namelist()):
        if member.endswith("/") or not member.lower().endswith(".json"):
            continue
        try:
            payload = json.loads(archive.read(member))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for basename, hashes in _declared_carried_hashes_from_payload(payload).items():
            for digest in sorted(hashes):
                claims.setdefault(basename, []).append(
                    {
                        "sha256": digest,
                        "source_member": member,
                    }
                )
    return claims


def checkpoint_continuity_defects(
    archive: zipfile.ZipFile,
) -> list[dict[str, Any]]:
    """Report inherited authoring authority that disappeared from a checkpoint.

    Missing bytes are never reconstructed.  Multiple historical hashes for one
    basename are surfaced as an ambiguity instead of choosing one.
    """

    actual = discover_authoring_members(archive)
    claims = historical_carry_claims(archive)
    defects: list[dict[str, Any]] = []
    for basename, records in sorted(claims.items()):
        hashes = sorted({record["sha256"] for record in records})
        if len(hashes) > 1:
            defects.append(
                {
                    "reason": "AMBIGUOUS_INHERITED_AUTHORING_AUTHORITY",
                    "name": AUTHORING_DIR + "/" + basename,
                    "expected_sha256": hashes,
                    "provenance_members": sorted(
                        {record["source_member"] for record in records}
                    ),
                }
            )
            continue
        if basename not in actual:
            defects.append(
                {
                    "reason": "DROPPED_INHERITED_AUTHORING_MEMBER",
                    "name": AUTHORING_DIR + "/" + basename,
                    "expected_sha256": hashes[0],
                    "provenance_members": sorted(
                        {record["source_member"] for record in records}
                    ),
                }
            )
    return defects


def compare_parent_child(
    parent: zipfile.ZipFile,
    child: zipfile.ZipFile,
    *,
    owned_updates: set[str] | frozenset[str] = frozenset(),
) -> list[dict[str, Any]]:
    """Enforce exact-byte inheritance from one checkpoint to its successor."""

    parent_members = discover_authoring_members(parent)
    child_members = discover_authoring_members(child)
    defects: list[dict[str, Any]] = []
    for basename, metadata in sorted(parent_members.items()):
        if basename in owned_updates:
            continue
        child_meta = child_members.get(basename)
        if child_meta is None:
            defects.append(
                {
                    "reason": "DROPPED_INHERITED_AUTHORING_MEMBER",
                    "name": AUTHORING_DIR + "/" + basename,
                    "expected_sha256": metadata["sha256"],
                }
            )
        elif child_meta["sha256"] != metadata["sha256"]:
            defects.append(
                {
                    "reason": "CHANGED_INHERITED_AUTHORING_MEMBER",
                    "name": AUTHORING_DIR + "/" + basename,
                    "expected_sha256": metadata["sha256"],
                    "actual_sha256": child_meta["sha256"],
                }
            )
    return defects


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit or carry durable Stage 4 authoring-capsule members."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit")
    audit.add_argument("checkpoint", type=Path)
    audit.add_argument("--parent", type=Path)
    audit.add_argument("--owned", action="append", default=[])

    carry = sub.add_parser("carry")
    carry.add_argument("parent", type=Path)
    carry.add_argument("output_dir", type=Path)
    carry.add_argument("--owned", action="append", default=[])

    args = parser.parse_args()
    try:
        owned = {value.strip().lower() for value in args.owned if value.strip()}
        if args.command == "carry":
            with zipfile.ZipFile(args.parent) as parent:
                carried = carry_authoring_capsule(
                    parent, args.output_dir, owned_updates=owned
                )
            print(json.dumps({"status": "PASS", "carried": carried}, indent=2))
            return 0

        with zipfile.ZipFile(args.checkpoint) as child:
            defects = checkpoint_continuity_defects(child)
            if args.parent:
                with zipfile.ZipFile(args.parent) as parent:
                    defects.extend(
                        compare_parent_child(parent, child, owned_updates=owned)
                    )
        result = {"status": "PASS" if not defects else "INVALID", "defects": defects}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if not defects else 2
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({"status": "INVALID", "error": str(exc)}, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
