#!/usr/bin/env python3
"""Sealed intent-constrained transaction for non-merge global venue corrections."""
from __future__ import annotations

import argparse
import csv
import fnmatch
import hashlib
import json
import re
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
    d = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            d.update(chunk)
    return d.hexdigest()


def git_head(repo: Path):
    result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def git_changed_paths(repo: Path):
    result = subprocess.run(["git", "diff", "--name-only"], cwd=repo, text=True, capture_output=True)
    if result.returncode:
        raise TransactionError("unable to read git diff")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields, rows):
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    enc = "utf-8-sig" if bom else "utf-8"
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding=enc, newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator=newline)
        writer.writeheader()
        writer.writerows({f: row.get(f, "") for f in fields} for row in rows)
    tmp.replace(path)


def load_spec(path: Path):
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("schema_version") != 1:
        raise TransactionError("spec schema_version must be 1")
    if not clean(doc.get("expected_base_sha")):
        raise TransactionError("spec requires expected_base_sha")
    return doc


def row_matches(row, match):
    match = match or {}
    for field, value in match.get("eq", {}).items():
        if clean(row.get(field)) != clean(value):
            return False
    for field, values in match.get("in", {}).items():
        if clean(row.get(field)) not in {clean(v) for v in values}:
            return False
    for field, pattern in match.get("regex", {}).items():
        if re.search(pattern, row.get(field, "") or "") is None:
            return False
    for field, pattern in match.get("not_regex", {}).items():
        if re.search(pattern, row.get(field, "") or "") is not None:
            return False
    for op, func in (
        ("gt", lambda a, b: a > b),
        ("gte", lambda a, b: a >= b),
        ("lt", lambda a, b: a < b),
        ("lte", lambda a, b: a <= b),
    ):
        for field, value in match.get(op, {}).items():
            actual = clean(row.get(field))
            expected = clean(value)
            if not actual or not func(actual, expected):
                return False
    return True


def expect_partial(row, expected, label, blockers):
    for field, value in (expected or {}).items():
        if clean(row.get(field)) != clean(value):
            blockers.append(
                f"{label}: expected {field}={value!r}, found {row.get(field, '')!r}"
            )


def assert_expected_count(label, expected, actual, blockers):
    if int(expected) != int(actual):
        blockers.append(f"{label}: expected {expected}, found {actual}")


def venue_num(venue_id):
    m = re.fullmatch(r"VEN-(\d{6})", clean(venue_id))
    return int(m.group(1)) if m else -1


def structured_paths(repo: Path, spec):
    paths = {
        repo / "data/reference/venues.csv",
        repo / "data/reference/venue-names.csv",
        repo / "data/canonical/games.csv",
        repo / "data/evidence/game-assertions.csv",
        repo / "data/evidence/ncaa-tournament-sites.csv",
    }
    for section in ("school_venue_updates", "school_venue_deletes", "school_venue_additions", "source_game_rules"):
        for item in spec.get(section, []):
            paths.add(repo / item["path"])
    return sorted(p for p in paths if p.exists())


def dependent_counts(repo: Path, venue_id: str, old_key: str):
    out = {}
    for label, rel in (
        ("canonical", "data/canonical/games.csv"),
        ("assertions", "data/evidence/game-assertions.csv"),
        ("ncaa", "data/evidence/ncaa-tournament-sites.csv"),
    ):
        path = repo / rel
        if not path.exists():
            out[label] = 0
            continue
        fields, rows = read_csv(path)
        count = 0
        for row in rows:
            id_match = "venue_id" in fields and clean(row.get("venue_id")) == venue_id
            key_match = "venue_key" in fields and clean(row.get("venue_key")) == old_key
            if id_match or key_match:
                count += 1
        out[label] = count
    return out


def build_plan(repo: Path, spec_path: Path):
    repo = repo.resolve()
    spec_path = spec_path.resolve()
    spec = load_spec(spec_path)
    blockers = []
    head = git_head(repo)
    base = clean(spec["expected_base_sha"])
    ancestry = subprocess.run(["git", "merge-base", "--is-ancestor", base, "HEAD"], cwd=repo)
    if ancestry.returncode != 0:
        blockers.append(f"protected-main base {base} is not an ancestor of HEAD {head}")

    venue_path = repo / "data/reference/venues.csv"
    names_path = repo / "data/reference/venue-names.csv"
    vfields, venues = read_csv(venue_path)
    nfields, names = read_csv(names_path)
    by_id = {clean(row.get("venue_id")): row for row in venues}
    by_key = {clean(row.get("venue_key")): row for row in venues}
    detail = {"venue_updates": [], "venue_additions": [], "name_ops": [], "school_ops": [], "source_game_rules": []}

    for item in spec.get("venue_updates", []):
        vid = clean(item.get("venue_id"))
        row = by_id.get(vid)
        if row is None:
            blockers.append(f"venue update {vid}: missing venue")
            continue
        expect_partial(row, item.get("expected"), f"venue update {vid}", blockers)
        new_key = clean(item.get("set", {}).get("venue_key", row.get("venue_key")))
        if new_key != clean(row.get("venue_key")) and new_key in by_key and clean(by_key[new_key].get("venue_id")) != vid:
            blockers.append(f"venue update {vid}: key collision {new_key}")
        counts = dependent_counts(repo, vid, clean(row.get("venue_key")))
        for label, field in (("canonical", "expected_canonical_rows"), ("assertions", "expected_assertion_rows"), ("ncaa", "expected_ncaa_rows")):
            if field in item:
                assert_expected_count(f"venue update {vid} {label} rows", item[field], counts[label], blockers)
        detail["venue_updates"].append({"venue_id": vid, "old_key": clean(row.get("venue_key")), "new_key": new_key, **counts})

    existing_nums = [venue_num(row.get("venue_id")) for row in venues if venue_num(row.get("venue_id")) >= 0]
    next_id = f"VEN-{max(existing_nums) + 1:06d}" if existing_nums else "VEN-000001"
    for item in spec.get("venue_additions", []):
        row = item.get("row", {})
        vid = clean(row.get("venue_id")); key = clean(row.get("venue_key"))
        if vid in by_id:
            blockers.append(f"venue addition {vid}: venue_id already exists")
        if key in by_key:
            blockers.append(f"venue addition {vid}: venue_key already exists: {key}")
        if item.get("require_next_numeric_id") and vid != next_id:
            blockers.append(f"venue addition {vid}: expected next numeric ID {next_id}")
        missing = [f for f in vfields if f not in row]
        if missing:
            blockers.append(f"venue addition {vid}: missing columns {missing}")
        detail["venue_additions"].append({"venue_id": vid, "venue_key": key})

    for section in ("venue_name_updates", "venue_name_deletes"):
        for item in spec.get(section, []):
            matched = [row for row in names if row_matches(row, item.get("match"))]
            assert_expected_count(section, item.get("expected_count", 1), len(matched), blockers)
            for row in matched:
                expect_partial(row, item.get("expected"), section, blockers)
            detail["name_ops"].append({"kind": section, "count": len(matched), "match": item.get("match", {})})
    for item in spec.get("venue_name_additions", []):
        row = item.get("row", {})
        missing = [f for f in nfields if f not in row]
        if missing:
            blockers.append(f"venue name addition missing columns {missing}")
        dup = [x for x in names if all(clean(x.get(k)) == clean(v) for k, v in row.items())]
        if dup:
            blockers.append(f"venue name addition already exists: {row.get('venue_id')} {row.get('venue_name')}")
        detail["name_ops"].append({"kind": "venue_name_additions", "count": 1, "match": {"venue_id": row.get("venue_id"), "venue_name": row.get("venue_name")}})

    for section in ("school_venue_updates", "school_venue_deletes"):
        for item in spec.get(section, []):
            path = repo / item["path"]
            fields, rows = read_csv(path)
            matched = [row for row in rows if row_matches(row, item.get("match"))]
            assert_expected_count(f"{section} {item['path']}", item.get("expected_count", 1), len(matched), blockers)
            for row in matched:
                expect_partial(row, item.get("expected"), f"{section} {item['path']}", blockers)
            detail["school_ops"].append({"kind": section, "path": item["path"], "count": len(matched)})
    for item in spec.get("school_venue_additions", []):
        path = repo / item["path"]
        fields, rows = read_csv(path)
        row = item.get("row", {})
        missing = [f for f in fields if f not in row]
        if missing:
            blockers.append(f"school venue addition {item['path']}: missing columns {missing}")
        if any(row_matches(x, item.get("unique_match", {"eq": {"venue_id": row.get("venue_id")}})) for x in rows):
            blockers.append(f"school venue addition {item['path']}: unique match already exists")
        detail["school_ops"].append({"kind": "school_venue_additions", "path": item["path"], "count": 1})

    seen_source_rows = set()
    for idx, item in enumerate(spec.get("source_game_rules", []), start=1):
        path = repo / item["path"]
        fields, rows = read_csv(path)
        forbidden = sorted(set(item.get("set", {})) - {"curated_venue_name", "city", "state"})
        if forbidden:
            blockers.append(f"source rule {idx}: forbidden mutable fields {forbidden}")
        matched_indexes = [i for i, row in enumerate(rows) if row_matches(row, item.get("match"))]
        assert_expected_count(f"source rule {idx} {item['path']}", item["expected_count"], len(matched_indexes), blockers)
        for row_index in matched_indexes:
            key = (item["path"], row_index)
            if key in seen_source_rows:
                blockers.append(f"source rule {idx}: overlaps another rule at {item['path']} row {row_index + 2}")
            seen_source_rows.add(key)
        detail["source_game_rules"].append({"path": item["path"], "rule": idx, "count": len(matched_indexes), "description": item.get("description", "")})

    fingerprints = {}
    for path in structured_paths(repo, spec):
        fingerprints[str(path.relative_to(repo))] = hfile(path)
    fingerprints[str(spec_path.relative_to(repo)) if spec_path.is_relative_to(repo) else str(spec_path)] = hfile(spec_path)

    core = {
        "schema_version": 1,
        "git_head": head,
        "spec": str(spec_path.relative_to(repo)) if spec_path.is_relative_to(repo) else str(spec_path),
        "blockers": sorted(set(blockers)),
        "detail": detail,
        "fingerprints": fingerprints,
    }
    core["plan_sha256"] = htext(stable(core))
    return core


def assert_ready(plan):
    if plan["blockers"]:
        raise TransactionError("plan blockers: " + " | ".join(plan["blockers"][:12]))


def remove_aliases(value, removals):
    remove = {clean(x).casefold() for x in removals}
    parts = [p.strip() for p in (value or "").split(";") if p.strip()]
    return ";".join(p for p in parts if p.casefold() not in remove)


def rewrite_dependents(repo: Path, venue_id: str, old_key: str, new_key: str):
    changed = {"canonical": 0, "assertions": 0, "ncaa": 0}
    if old_key == new_key:
        return changed
    for label, rel in (("canonical", "data/canonical/games.csv"), ("assertions", "data/evidence/game-assertions.csv"), ("ncaa", "data/evidence/ncaa-tournament-sites.csv")):
        path = repo / rel
        if not path.exists():
            continue
        fields, rows = read_csv(path)
        n = 0
        for row in rows:
            id_match = "venue_id" in fields and clean(row.get("venue_id")) == venue_id
            key_match = "venue_key" in fields and clean(row.get("venue_key")) == old_key
            if not (id_match or key_match):
                continue
            if "venue_id" in fields and clean(row.get("venue_id")) not in ("", venue_id):
                raise TransactionError(f"{rel}: old key {old_key} belongs to unexpected venue_id {row.get('venue_id')}")
            if "venue_key" in fields:
                row["venue_key"] = new_key
            n += 1
        if n:
            write_csv(path, fields, rows)
        changed[label] = n
    return changed


def _site_json_paths(repo: Path):
    root = repo / "site/data"
    return set(root.rglob("*.json")) if root.exists() else set()


def snapshot_site(repo: Path):
    return {p: p.read_bytes() for p in _site_json_paths(repo) if p.is_file()}


def restore_site(repo: Path, snap):
    before = set(snap)
    for p in _site_json_paths(repo) - before:
        if p.is_file():
            p.unlink()
    for p, data in snap.items():
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(data)


def run_validation(repo: Path, tests):
    commands = [
        [sys.executable, "tools/validate_data.py"],
        [sys.executable, "tools/build_site_data.py", "--apply"],
        [sys.executable, "tools/check_site_data_freshness.py"],
    ]
    if tests:
        commands.append([sys.executable, "-m", "unittest", *tests, "-v"])
    for command in commands:
        result = subprocess.run(command, cwd=repo)
        if result.returncode:
            raise TransactionError("validation failed: " + " ".join(command[1:]))


def check_changed_paths(repo: Path, patterns):
    changed = git_changed_paths(repo)
    bad = [p for p in changed if not any(fnmatch.fnmatch(p, pat) for pat in patterns)]
    if bad:
        raise TransactionError("undeclared changed paths: " + ", ".join(bad[:20]))
    return changed


def check_postconditions(repo: Path, conditions):
    for i, item in enumerate(conditions, start=1):
        path = repo / item["path"]
        _, rows = read_csv(path)
        matched = [row for row in rows if row_matches(row, item.get("match"))]
        expected = int(item.get("expected_count", 1))
        if len(matched) != expected:
            raise TransactionError(f"postcondition {i} {item['path']}: expected {expected}, found {len(matched)}")
        for row in matched:
            for field, value in item.get("expected", {}).items():
                if clean(row.get(field)) != clean(value):
                    raise TransactionError(f"postcondition {i} {item['path']}: {field} expected {value!r}, found {row.get(field,'')!r}")


def apply_transaction(repo: Path, spec_path: Path, expected_plan_sha256: str, *, run_checks=True):
    repo = repo.resolve(); spec_path = spec_path.resolve(); spec = load_spec(spec_path)
    plan = build_plan(repo, spec_path); assert_ready(plan)
    if clean(expected_plan_sha256) != plan["plan_sha256"]:
        raise TransactionError(f"sealed plan hash mismatch: expected {expected_plan_sha256}, actual {plan['plan_sha256']}")

    paths = set(structured_paths(repo, spec))
    originals = {p: p.read_bytes() for p in paths}
    site_originals = snapshot_site(repo) if run_checks else {}
    counts = {"venue_updates":0,"venue_additions":0,"venue_name_updates":0,"venue_name_deletes":0,"venue_name_additions":0,"school_updates":0,"school_deletes":0,"school_additions":0,"source_game_updates":0,"dependent_updates":0}
    try:
        venue_path = repo / "data/reference/venues.csv"
        names_path = repo / "data/reference/venue-names.csv"
        vfields, venues = read_csv(venue_path)
        nfields, names = read_csv(names_path)

        for item in spec.get("venue_updates", []):
            vid = clean(item["venue_id"])
            row = next(row for row in venues if clean(row.get("venue_id")) == vid)
            old_key = clean(row.get("venue_key"))
            for field, value in item.get("set", {}).items(): row[field] = clean(value)
            new_key = clean(row.get("venue_key"))
            dep = rewrite_dependents(repo, vid, old_key, new_key)
            counts["dependent_updates"] += sum(dep.values())
            counts["venue_updates"] += 1

        for item in spec.get("venue_additions", []):
            row = {f: clean(item["row"].get(f)) for f in vfields}
            venues.append(row); counts["venue_additions"] += 1
        write_csv(venue_path, vfields, venues)

        for item in spec.get("venue_name_updates", []):
            matched = [row for row in names if row_matches(row, item.get("match"))]
            for row in matched:
                for field, value in item.get("set", {}).items(): row[field] = clean(value)
                counts["venue_name_updates"] += 1
        for item in spec.get("venue_name_deletes", []):
            keep=[]
            for row in names:
                if row_matches(row, item.get("match")):
                    counts["venue_name_deletes"] += 1
                else: keep.append(row)
            names=keep
        for item in spec.get("venue_name_additions", []):
            names.append({f: clean(item["row"].get(f)) for f in nfields}); counts["venue_name_additions"] += 1
        write_csv(names_path, nfields, names)

        by_path = {}
        for section in ("school_venue_updates", "school_venue_deletes", "school_venue_additions"):
            for item in spec.get(section, []): by_path.setdefault(item["path"], []).append((section,item))
        for rel, ops in by_path.items():
            path=repo/rel; fields, rows=read_csv(path)
            for section,item in ops:
                if section=="school_venue_updates":
                    for row in rows:
                        if not row_matches(row,item.get("match")): continue
                        for field,value in item.get("set",{}).items(): row[field]=clean(value)
                        if "aliases" in fields and item.get("remove_aliases"):
                            row["aliases"]=remove_aliases(row.get("aliases",""),item["remove_aliases"])
                        counts["school_updates"]+=1
                elif section=="school_venue_deletes":
                    keep=[]
                    for row in rows:
                        if row_matches(row,item.get("match")): counts["school_deletes"]+=1
                        else: keep.append(row)
                    rows=keep
                else:
                    rows.append({f: clean(item["row"].get(f)) for f in fields}); counts["school_additions"]+=1
            write_csv(path,fields,rows)

        source_by_path={}
        for item in spec.get("source_game_rules",[]): source_by_path.setdefault(item["path"],[]).append(item)
        for rel,rules in source_by_path.items():
            path=repo/rel; fields,rows=read_csv(path)
            for item in rules:
                for row in rows:
                    if not row_matches(row,item.get("match")): continue
                    for field,value in item.get("set",{}).items(): row[field]=clean(value)
                    counts["source_game_updates"]+=1
            write_csv(path,fields,rows)

        check_postconditions(repo,spec.get("postconditions",[]))
        if run_checks:
            run_validation(repo,spec.get("validation_tests",[]))
            check_postconditions(repo,spec.get("postconditions",[]))
            changed=check_changed_paths(repo,spec.get("allowed_changed_paths",[]))
        else:
            changed=git_changed_paths(repo) if (repo/".git").exists() else []
    except Exception:
        for p,data in originals.items(): p.write_bytes(data)
        if run_checks: restore_site(repo,site_originals)
        raise
    return {"plan_sha256":plan["plan_sha256"],**counts,"changed_paths":changed}


def main():
    parser=argparse.ArgumentParser(description="Plan/apply sealed non-merge venue structural corrections.")
    parser.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[1])
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("plan"); p.add_argument("spec",type=Path); p.add_argument("--output",type=Path); p.add_argument("--json",action="store_true")
    a=sub.add_parser("apply"); a.add_argument("spec",type=Path); a.add_argument("--expected-plan-sha256",required=True); a.add_argument("--apply",action="store_true")
    args=parser.parse_args(); repo=args.repo.resolve()
    try:
        if args.command=="plan":
            plan=build_plan(repo,args.spec)
            if args.output:
                args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(plan,indent=2,sort_keys=True)+"\n",encoding="utf-8")
            print(json.dumps(plan,indent=2,sort_keys=True) if args.json else f"VENUE STRUCTURAL TRANSACTION PLAN\nblockers={len(plan['blockers'])}\nplan sha256: {plan['plan_sha256']}")
            return 2 if plan["blockers"] else 0
        if not args.apply: raise TransactionError("apply command requires explicit --apply")
        result=apply_transaction(repo,args.spec,args.expected_plan_sha256)
        print("PASS: "+stable(result)); return 0
    except (TransactionError,FileNotFoundError,ValueError,KeyError,json.JSONDecodeError) as exc:
        print("FAIL:",exc); return 1


if __name__=="__main__": raise SystemExit(main())