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


def _manifested_members(archive: zipfile.ZipFile) -> set[str]:
    """Return the authoritative checkpoint-manifest member population when present."""

    candidates = [
        name
        for name in archive.namelist()
        if Path(name).name.lower() in {"manifest.json", "checkpoint-manifest.json"}
    ]
    if not candidates:
        return set()
    if len(candidates) > 1:
        root = [name for name in candidates if "/" not in name.strip("/")]
        if len(root) == 1:
            candidates = root
        else:
            return set()
    try:
        payload = json.loads(archive.read(candidates[0]))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return set()
    files = payload.get("files", {})
    if isinstance(files, list):
        return {
            str(item.get("name", ""))
            for item in files
            if isinstance(item, dict) and item.get("name")
        }
    if isinstance(files, dict):
        return {str(name) for name in files}
    return set()


def _valid_sha256(value: str) -> bool:
    value = str(value or "").strip().lower()
    return len(value) == 64 and all(ch in "0123456789abcdef" for ch in value)


def _replacement_records_from_payload(
    payload: Any,
    *,
    source_member: str,
) -> list[dict[str, Any]]:
    """Extract generic and accepted legacy authoring-replacement records."""

    if not isinstance(payload, dict):
        return []

    records: list[dict[str, Any]] = []
    generic = payload.get("stage4_authoring_replacements")
    generic_items: list[dict[str, Any]] = []
    if isinstance(generic, list):
        generic_items = [item for item in generic if isinstance(item, dict)]
    elif isinstance(generic, dict):
        for name, metadata in generic.items():
            if not isinstance(metadata, dict):
                continue
            item = dict(metadata)
            item.setdefault("member", AUTHORING_DIR + "/" + str(name))
            generic_items.append(item)
    for item in generic_items:
        records.append(
            {
                "source_member": source_member,
                "member": str(item.get("member", "")).strip(),
                "old_sha256": str(
                    item.get("old_sha256", item.get("old_inherited_sha256", ""))
                ).strip().lower(),
                "new_sha256": str(
                    item.get("new_sha256", item.get("new_authorized_sha256", ""))
                ).strip().lower(),
                "old_claim_member": str(item.get("old_claim_member", "")).strip(),
                "new_claim_member": str(item.get("new_claim_member", "")).strip(),
                "historical_authority_changed": item.get(
                    "historical_authority_changed"
                ),
            }
        )

    legacy = payload.get("authoring_provenance_population")
    if (
        isinstance(legacy, dict)
        and str(legacy.get("classification", "")).strip()
        == "AUTHORIZED_STAGE3B_CAPSULE_REPLACEMENT_VS_INHERITED_STAGE3A4_BYTE_PRESERVATION_CLAIM"
    ):
        records.append(
            {
                "source_member": source_member,
                "member": str(legacy.get("member", "")).strip(),
                "old_sha256": str(
                    legacy.get("old_inherited_sha256", "")
                ).strip().lower(),
                "new_sha256": str(
                    legacy.get("new_authorized_sha256", "")
                ).strip().lower(),
                "old_claim_member": str(
                    legacy.get("old_claim_member", "")
                ).strip(),
                "new_claim_member": str(
                    legacy.get("new_claim_member", "")
                ).strip(),
                "historical_authority_changed": legacy.get(
                    "historical_authority_changed"
                ),
            }
        )
    return records


def authorized_authoring_replacements(
    archive: zipfile.ZipFile,
) -> tuple[dict[str, list[dict[str, Any]]], list[dict[str, Any]]]:
    """Validate manifested, hash-bound authoring-member replacement claims.

    This is provenance reconciliation only. It never supplies missing bytes or
    changes historical authority. Invalid replacement records remain explicit
    defects and cannot suppress ordinary continuity checks.
    """

    manifested = _manifested_members(archive)
    replacements: dict[str, list[dict[str, Any]]] = {}
    defects: list[dict[str, Any]] = []

    for source_member in sorted(archive.namelist()):
        if source_member.endswith("/") or not source_member.lower().endswith(".json"):
            continue
        try:
            payload = json.loads(archive.read(source_member))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        for record in _replacement_records_from_payload(
            payload, source_member=source_member
        ):
            member = record["member"]
            basename = _basename(member)
            reason: str | None = None
            if source_member not in manifested:
                reason = "AUTHORIZING_RECORD_NOT_MANIFESTED"
            elif (
                basename not in AUTHORING_BASENAMES
                or member.replace("\\", "/").rstrip("/")
                != AUTHORING_DIR + "/" + basename
            ):
                reason = "UNKNOWN_AUTHORIZED_AUTHORING_MEMBER"
            elif not _valid_sha256(record["old_sha256"]) or not _valid_sha256(
                record["new_sha256"]
            ):
                reason = "INVALID_AUTHORIZED_AUTHORING_REPLACEMENT_HASH"
            elif record["old_sha256"] == record["new_sha256"]:
                reason = "NOOP_AUTHORIZED_AUTHORING_REPLACEMENT"
            elif record["historical_authority_changed"] is not False:
                reason = "AUTHORIZED_REPLACEMENT_CHANGED_HISTORICAL_AUTHORITY"
            elif (
                not record["old_claim_member"]
                or not record["new_claim_member"]
                or record["old_claim_member"] not in archive.namelist()
                or record["new_claim_member"] not in archive.namelist()
            ):
                reason = "AUTHORIZED_REPLACEMENT_CLAIM_MEMBER_MISSING"
            elif (
                record["old_claim_member"] not in manifested
                or record["new_claim_member"] not in manifested
            ):
                reason = "AUTHORIZED_REPLACEMENT_CLAIM_MEMBER_NOT_MANIFESTED"
            else:
                old_payload = json.loads(archive.read(record["old_claim_member"]))
                new_payload = json.loads(archive.read(record["new_claim_member"]))
                old_claims = _declared_carried_hashes_from_payload(old_payload)
                new_claims = _declared_carried_hashes_from_payload(new_payload)
                if record["old_sha256"] not in old_claims.get(basename, set()):
                    reason = "AUTHORIZED_REPLACEMENT_OLD_CLAIM_MISMATCH"
                elif record["new_sha256"] not in new_claims.get(basename, set()):
                    reason = "AUTHORIZED_REPLACEMENT_NEW_CLAIM_MISMATCH"

            if reason:
                defects.append(
                    {
                        "reason": reason,
                        "name": member or AUTHORING_DIR + "/" + basename,
                        "authorization_member": source_member,
                    }
                )
                continue
            replacements.setdefault(basename, []).append(record)
    return replacements, defects


def _replacement_chain_explains_hashes(
    hashes: set[str],
    replacements: list[dict[str, Any]],
    *,
    actual_sha256: str,
) -> bool:
    if len(hashes) <= 1:
        return True
    edges = {(r["old_sha256"], r["new_sha256"]) for r in replacements}
    if len(edges) != len(replacements):
        return False
    sources = {old for old, _ in edges}
    targets = {new for _, new in edges}
    nodes = sources | targets
    if nodes != hashes or len(edges) != len(hashes) - 1:
        return False
    if any(sum(1 for old, _ in edges if old == node) > 1 for node in nodes):
        return False
    if any(sum(1 for _, new in edges if new == node) > 1 for node in nodes):
        return False
    starts = hashes - targets
    ends = hashes - sources
    if len(starts) != 1 or ends != {actual_sha256}:
        return False
    current = next(iter(starts))
    visited = {current}
    while current != actual_sha256:
        next_values = [new for old, new in edges if old == current]
        if len(next_values) != 1 or next_values[0] in visited:
            return False
        current = next_values[0]
        visited.add(current)
    return visited == hashes


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

    Missing bytes are never reconstructed. Multiple historical hashes remain
    ambiguous unless one exact manifested, hash-bound, no-historical-change
    replacement chain explains every observed hash and terminates at the
    current authoring bytes.
    """

    actual = discover_authoring_members(archive)
    claims = historical_carry_claims(archive)
    replacements, replacement_defects = authorized_authoring_replacements(archive)
    defects: list[dict[str, Any]] = list(replacement_defects)
    for basename, records in sorted(claims.items()):
        hashes = sorted({record["sha256"] for record in records})
        if len(hashes) > 1:
            actual_hash = str(actual.get(basename, {}).get("sha256", ""))
            if (
                actual_hash
                and not replacement_defects
                and _replacement_chain_explains_hashes(
                    set(hashes),
                    replacements.get(basename, []),
                    actual_sha256=actual_hash,
                )
            ):
                continue
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
