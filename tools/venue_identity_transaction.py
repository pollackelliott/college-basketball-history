#!/usr/bin/env python3
"""Sealed transaction for merging duplicate global physical-venue identities."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path


class TransactionError(RuntimeError):
    pass


def clean(value):
    return "" if value is None else str(value).strip()


def stable(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def htext(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def hfile(path: Path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head(repo: Path):
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=repo,
        text=True,
        capture_output=True,
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields, rows):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    encoding = "utf-8-sig" if bom else "utf-8"
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding=encoding, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=newline)
        writer.writeheader()
        writer.writerows({field: row.get(field, "") for field in fields} for row in rows)
    temporary.replace(path)


def merge_text(left: str, right: str) -> str:
    parts = []
    for value in (left, right):
        for part in clean(value).split(" | "):
            part = part.strip()
            if part and part not in parts:
                parts.append(part)
    return " | ".join(parts)


def registry_marker_token(venue_key: str) -> str:
    return f";venue_key={venue_key};"


def rewrite_registry_marker_keys(notes: str, absorbed_key: str, survivor_key: str):
    old = registry_marker_token(absorbed_key)
    new = registry_marker_token(survivor_key)
    count = (notes or "").count(old)
    return (notes or "").replace(old, new), count


def load_spec(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("schema_version") != 1 or not isinstance(doc.get("merges"), list):
        raise TransactionError("spec must be schema_version 1 with a merges list")
    merges = []
    used_absorbed = set()
    for raw in doc["merges"]:
        survivor = clean(raw.get("survivor_venue_id"))
        absorbed = clean(raw.get("absorbed_venue_id"))
        basis = clean(raw.get("resolution_basis"))
        if not survivor or not absorbed or survivor == absorbed or not basis:
            raise TransactionError("each merge requires survivor, absorbed, and resolution_basis")
        if absorbed in used_absorbed:
            raise TransactionError(f"absorbed venue listed twice: {absorbed}")
        used_absorbed.add(absorbed)
        merges.append(
            {
                "survivor_venue_id": survivor,
                "absorbed_venue_id": absorbed,
                "resolution_basis": basis,
                "expected_canonical_rows": raw.get("expected_canonical_rows"),
                "expected_school_rows": raw.get("expected_school_rows"),
            }
        )
    return merges


def structured_school_paths(repo: Path):
    return sorted((repo / "schools").glob("*/venues.csv"))


def _assert_expected(label: str, expected, actual: int, blockers: list[str]):
    if expected is None:
        return
    try:
        expected_int = int(expected)
    except (TypeError, ValueError):
        blockers.append(f"{label}: invalid expected count {expected!r}")
        return
    if expected_int != actual:
        blockers.append(f"{label}: expected {expected_int}, found {actual}")


def build_plan(repo: Path, spec_path: Path):
    repo = repo.resolve()
    spec_path = spec_path.resolve()
    merges = load_spec(spec_path)

    venue_path = repo / "data/reference/venues.csv"
    names_path = repo / "data/reference/venue-names.csv"
    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"

    _, venues = read_csv(venue_path)
    _, names = read_csv(names_path)
    cfields, canonical = read_csv(canonical_path)
    if assertions_path.exists():
        afields, assertions = read_csv(assertions_path)
    else:
        afields, assertions = [], []

    by_id = {clean(row.get("venue_id")): row for row in venues}
    blockers = []
    rows = []
    touched_school_paths = set()

    for merge in merges:
        survivor_id = merge["survivor_venue_id"]
        absorbed_id = merge["absorbed_venue_id"]
        survivor = by_id.get(survivor_id)
        absorbed = by_id.get(absorbed_id)
        if survivor is None or absorbed is None:
            blockers.append(
                f"{survivor_id}<-{absorbed_id}: survivor or absorbed venue missing"
            )
            continue
        if (
            clean(survivor.get("city")).casefold() != clean(absorbed.get("city")).casefold()
            or clean(survivor.get("state")).upper() != clean(absorbed.get("state")).upper()
        ):
            blockers.append(
                f"{survivor_id}<-{absorbed_id}: geography differs; not a mechanical duplicate"
            )

        canonical_count = sum(
            1 for row in canonical if clean(row.get("venue_id")) == absorbed_id
        )
        provenance_marker_count = sum(
            clean(row.get("notes")).count(registry_marker_token(clean(absorbed.get("venue_key"))))
            for row in canonical
            if clean(row.get("venue_id")) == absorbed_id
        )
        assertion_count = sum(
            1
            for row in assertions
            if clean(row.get("venue_id")) == absorbed_id
            or clean(row.get("venue_key")) == clean(absorbed.get("venue_key"))
        )
        school_refs = []
        for path in structured_school_paths(repo):
            _, school_rows = read_csv(path)
            count = sum(
                1 for row in school_rows if clean(row.get("venue_id")) == absorbed_id
            )
            if count:
                touched_school_paths.add(path)
                school_refs.append(
                    {"path": str(path.relative_to(repo)), "row_count": count}
                )
        school_count = sum(item["row_count"] for item in school_refs)
        name_count = sum(
            1 for row in names if clean(row.get("venue_id")) == absorbed_id
        )

        _assert_expected(
            f"{survivor_id}<-{absorbed_id} canonical rows",
            merge.get("expected_canonical_rows"),
            canonical_count,
            blockers,
        )
        _assert_expected(
            f"{survivor_id}<-{absorbed_id} school venue rows",
            merge.get("expected_school_rows"),
            school_count,
            blockers,
        )

        rows.append(
            {
                **merge,
                "survivor_venue_key": clean(survivor.get("venue_key")),
                "absorbed_venue_key": clean(absorbed.get("venue_key")),
                "city": clean(survivor.get("city")),
                "state": clean(survivor.get("state")),
                "canonical_rows": canonical_count,
                "provenance_markers": provenance_marker_count,
                "assertion_rows": assertion_count,
                "school_rows": school_count,
                "school_files": school_refs,
                "venue_name_rows": name_count,
            }
        )

    fingerprint_paths = [
        venue_path,
        names_path,
        canonical_path,
        spec_path,
    ]
    if assertions_path.exists():
        fingerprint_paths.append(assertions_path)
    fingerprint_paths.extend(sorted(touched_school_paths))
    fingerprints = {
        str(path.relative_to(repo)) if path.is_relative_to(repo) else str(path): hfile(path)
        for path in fingerprint_paths
    }

    core = {
        "schema_version": 1,
        "git_head": git_head(repo),
        "spec": str(spec_path.relative_to(repo)) if spec_path.is_relative_to(repo) else str(spec_path),
        "merges": rows,
        "blockers": sorted(set(blockers)),
        "fingerprints": fingerprints,
    }
    core["plan_sha256"] = htext(stable(core))
    return core


def assert_ready(plan):
    if plan["blockers"]:
        raise TransactionError("plan blockers: " + " | ".join(plan["blockers"][:8]))


def _dedupe_names(rows):
    output = []
    seen = {}
    key_fields = (
        "venue_id",
        "normalized_name",
        "name_type",
        "valid_from",
        "valid_to",
        "date_precision",
    )
    for row in rows:
        key = tuple(clean(row.get(field)) for field in key_fields)
        prior = seen.get(key)
        if prior is None:
            copy = dict(row)
            seen[key] = copy
            output.append(copy)
            continue
        prior["source_basis"] = merge_text(prior.get("source_basis", ""), row.get("source_basis", ""))
        prior["notes"] = merge_text(prior.get("notes", ""), row.get("notes", ""))
    return output


def _run_validation(repo: Path):
    result = subprocess.run([sys.executable, "tools/validate_data.py"], cwd=repo)
    if result.returncode:
        raise TransactionError("validate_data failed")


def apply_transaction(
    repo: Path,
    spec_path: Path,
    expected_plan_sha256: str,
    *,
    run_validation: bool = True,
):
    repo = repo.resolve()
    spec_path = spec_path.resolve()
    plan = build_plan(repo, spec_path)
    assert_ready(plan)
    if clean(expected_plan_sha256) != plan["plan_sha256"]:
        raise TransactionError(
            "sealed plan hash mismatch: "
            f"expected {expected_plan_sha256}, actual {plan['plan_sha256']}"
        )

    venue_path = repo / "data/reference/venues.csv"
    names_path = repo / "data/reference/venue-names.csv"
    canonical_path = repo / "data/canonical/games.csv"
    assertions_path = repo / "data/evidence/game-assertions.csv"

    paths = {venue_path, names_path, canonical_path}
    if assertions_path.exists():
        paths.add(assertions_path)
    for merge in plan["merges"]:
        for item in merge["school_files"]:
            paths.add(repo / item["path"])

    originals = {path: path.read_bytes() for path in paths}

    try:
        vfields, venues = read_csv(venue_path)
        nfields, names = read_csv(names_path)
        cfields, canonical = read_csv(canonical_path)
        if assertions_path.exists():
            afields, assertions = read_csv(assertions_path)
        else:
            afields, assertions = [], []

        canonical_updates = 0
        provenance_marker_updates = 0
        assertion_updates = 0
        school_updates = 0
        names_reassigned = 0

        for merge in plan["merges"]:
            survivor_id = merge["survivor_venue_id"]
            absorbed_id = merge["absorbed_venue_id"]
            by_id = {clean(row.get("venue_id")): row for row in venues}
            survivor = by_id[survivor_id]
            absorbed = by_id[absorbed_id]
            survivor_key = clean(survivor.get("venue_key"))
            absorbed_key = clean(absorbed.get("venue_key"))

            retirement_note = (
                f"{absorbed_id} retired during shared-reference reconciliation after "
                f"determining {clean(absorbed.get('display_name'))} and "
                f"{clean(survivor.get('display_name'))} are the same physical venue; "
                f"{absorbed_id} must not be reused."
            )
            survivor["source_basis"] = merge_text(
                survivor.get("source_basis", ""), absorbed.get("source_basis", "")
            )
            survivor["notes"] = merge_text(
                survivor.get("notes", ""), retirement_note
            )
            venues = [
                row for row in venues if clean(row.get("venue_id")) != absorbed_id
            ]

            for row in names:
                if clean(row.get("venue_id")) != absorbed_id:
                    continue
                row["venue_id"] = survivor_id
                if clean(row.get("name_type")) == "PROJECT_DISPLAY":
                    row["name_type"] = "HISTORICAL_OR_ALIAS"
                row["notes"] = merge_text(
                    row.get("notes", ""),
                    f"Reassigned from retired {absorbed_id} to {survivor_id}.",
                )
                names_reassigned += 1
            names = _dedupe_names(names)

            for row in canonical:
                if clean(row.get("venue_id")) != absorbed_id:
                    continue
                row["venue_id"] = survivor_id
                if "venue_key" in cfields:
                    row["venue_key"] = survivor_key
                if "site_city" in cfields:
                    row["site_city"] = clean(survivor.get("city"))
                if "site_state" in cfields:
                    row["site_state"] = clean(survivor.get("state"))
                if "notes" in cfields:
                    rewritten, marker_count = rewrite_registry_marker_keys(
                        row.get("notes", ""),
                        absorbed_key,
                        survivor_key,
                    )
                    row["notes"] = rewritten
                    provenance_marker_updates += marker_count
                canonical_updates += 1

            for row in assertions:
                matched = False
                if "venue_id" in afields and clean(row.get("venue_id")) == absorbed_id:
                    row["venue_id"] = survivor_id
                    matched = True
                if "venue_key" in afields and clean(row.get("venue_key")) == absorbed_key:
                    row["venue_key"] = survivor_key
                    matched = True
                if matched:
                    if "site_city" in afields:
                        row["site_city"] = clean(survivor.get("city"))
                    if "site_state" in afields:
                        row["site_state"] = clean(survivor.get("state"))
                    assertion_updates += 1

            for item in merge["school_files"]:
                path = repo / item["path"]
                fields, rows = read_csv(path)
                changed = 0
                for row in rows:
                    if clean(row.get("venue_id")) != absorbed_id:
                        continue
                    row["venue_id"] = survivor_id
                    if "venue_key" in fields:
                        row["venue_key"] = survivor_key
                    if "city" in fields:
                        row["city"] = clean(survivor.get("city"))
                    if "state" in fields:
                        row["state"] = clean(survivor.get("state"))
                    if "notes" in fields:
                        row["notes"] = merge_text(
                            row.get("notes", ""),
                            f"Shared-reference reconciliation remapped retired "
                            f"{absorbed_id} to {survivor_id}.",
                        )
                    changed += 1
                if changed != item["row_count"]:
                    raise TransactionError(
                        f"{item['path']}: planned {item['row_count']} updates, found {changed}"
                    )
                write_csv(path, fields, rows)
                school_updates += changed

        write_csv(venue_path, vfields, venues)
        write_csv(names_path, nfields, names)
        write_csv(canonical_path, cfields, canonical)
        if assertions_path.exists():
            write_csv(assertions_path, afields, assertions)

        absorbed_ids = {merge["absorbed_venue_id"] for merge in plan["merges"]}
        _, venues_check = read_csv(venue_path)
        _, names_check = read_csv(names_path)
        _, canonical_check = read_csv(canonical_path)
        if any(clean(row.get("venue_id")) in absorbed_ids for row in venues_check):
            raise TransactionError("postcondition: absorbed venue remains in venues.csv")
        if any(clean(row.get("venue_id")) in absorbed_ids for row in names_check):
            raise TransactionError("postcondition: absorbed venue remains in venue-names.csv")
        if any(clean(row.get("venue_id")) in absorbed_ids for row in canonical_check):
            raise TransactionError("postcondition: absorbed venue remains in canonical games")
        absorbed_keys = {
            merge["absorbed_venue_key"]
            for merge in plan["merges"]
        }
        if any(
            registry_marker_token(key) in clean(row.get("notes"))
            for row in canonical_check
            for key in absorbed_keys
        ):
            raise TransactionError(
                "postcondition: absorbed venue_key remains in canonical provenance marker"
            )
        for path in structured_school_paths(repo):
            _, rows = read_csv(path)
            if any(clean(row.get("venue_id")) in absorbed_ids for row in rows):
                raise TransactionError(
                    f"postcondition: absorbed venue remains active in {path.relative_to(repo)}"
                )
        if assertions_path.exists():
            _, assertion_check = read_csv(assertions_path)
            if "venue_id" in afields and any(
                clean(row.get("venue_id")) in absorbed_ids for row in assertion_check
            ):
                raise TransactionError("postcondition: absorbed venue remains in assertions")

        if run_validation:
            _run_validation(repo)

    except Exception:
        for path, data in originals.items():
            path.write_bytes(data)
        raise

    return {
        "plan_sha256": plan["plan_sha256"],
        "canonical_rows_updated": canonical_updates,
        "provenance_markers_updated": provenance_marker_updates,
        "assertion_rows_updated": assertion_updates,
        "school_rows_updated": school_updates,
        "venue_name_rows_reassigned": names_reassigned,
        "venues_retired": len(plan["merges"]),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Plan/apply duplicate global physical-venue identity reconciliation."
    )
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    sub = parser.add_subparsers(dest="command", required=True)

    plan_parser = sub.add_parser("plan")
    plan_parser.add_argument("spec", type=Path)
    plan_parser.add_argument("--output", type=Path)
    plan_parser.add_argument("--json", action="store_true")

    apply_parser = sub.add_parser("apply")
    apply_parser.add_argument("spec", type=Path)
    apply_parser.add_argument("--expected-plan-sha256", required=True)
    apply_parser.add_argument("--apply", action="store_true")

    args = parser.parse_args()
    repo = args.repo.resolve()

    try:
        if args.command == "plan":
            plan = build_plan(repo, args.spec)
            if args.output:
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(
                    json.dumps(plan, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8",
                )
            if args.json:
                print(json.dumps(plan, indent=2, sort_keys=True))
            else:
                print("VENUE IDENTITY TRANSACTION PLAN")
                for merge in plan["merges"]:
                    print(
                        f"{merge['survivor_venue_id']} <- {merge['absorbed_venue_id']}: "
                        f"canonical={merge['canonical_rows']} "
                        f"markers={merge['provenance_markers']} "
                        f"assertions={merge['assertion_rows']} "
                        f"school={merge['school_rows']} names={merge['venue_name_rows']}"
                    )
                print(f"blockers={len(plan['blockers'])}")
                print(f"plan sha256: {plan['plan_sha256']}")
            return 2 if plan["blockers"] else 0

        if not args.apply:
            raise TransactionError("apply command requires explicit --apply")
        result = apply_transaction(
            repo,
            args.spec,
            args.expected_plan_sha256,
        )
        print("PASS: " + stable(result))
        return 0
    except (
        TransactionError,
        FileNotFoundError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
    ) as exc:
        print("FAIL:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
