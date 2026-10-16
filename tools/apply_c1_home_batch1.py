#!/usr/bin/env python3
"""Sealed, row-scoped C1 HOME-site maintenance on a dedicated branch.

Only the 145 previously evidence-rehearsed canonical IDs may change. Source H/A/N,
raw evidence, scores, game identities, and already populated site fields stay intact.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from apply_home_chronology_remediation import (
    _patch_blanks,
    _read_csv,
    _write_csv_preserving_format,
    _marker,
)
from location_safety import append_note
from site_remediation_audit import canonical_site_from_assertion, reconciliation_state

BASE = "2a18d454cc6a8a41057c61a7a6fcecda918dd0cf"
PLAN = "97129db0151861c693acf20853d34a79028399037be5b32900922e5d6805111d"
MANIFEST = "63632d835557a74e7e4b7aad7b63f678cd7c30d3c0072bc7f3bb9de5bf931350"
BRANCH = "maintenance/c1-home-batch1"
SCHOOLS = {"alabama": 129, "auburn": 1, "duke": 4, "purdue": 10, "wisconsin": 1}
MANIFEST_PATH = Path(".onboarding/objective-c1/batch1-exact-evidence-rehearsal/exact-eligible-manifest-NOT-APPROVED.json")
PLAN_PATH = Path(".onboarding/objective-c1/home-chronology-plan.json")
ARCHIVE_PATH = Path("data/reconciliation/maintenance/c1-home-batch1-evidence-manifest.json")
FIELDS = {
    "canonical": {"venue_id", "venue_key", "site_city", "site_state"},
    "source": {"curated_venue_name", "city", "state"},
    "assertion": {"curated_venue_name", "city", "state"},
}

class Stop(RuntimeError):
    pass

def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()

def preflight(root: Path, manifest_path: Path, plan_path: Path):
    if git(root, "branch", "--show-current") != BRANCH:
        raise Stop(f"must run on dedicated {BRANCH} branch")
    if git(root, "status", "--porcelain", "--untracked-files=no"):
        raise Stop("tracked worktree is not clean")
    if subprocess.run(["git", "merge-base", "--is-ancestor", BASE, "HEAD"], cwd=root).returncode:
        raise Stop("reviewed protected-main baseline is not an ancestor")
    raw = manifest_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != MANIFEST:
        raise Stop("exact 145-row manifest fingerprint differs from reviewed rehearsal")
    doc = json.loads(raw)
    candidates = doc["candidates"]
    if len(candidates) != 145 or Counter(c["program"] for c in candidates) != SCHOOLS:
        raise Stop("eligible population or school counts changed")
    if len({c["canonical_game_id"] for c in candidates}) != 145:
        raise Stop("duplicate canonical IDs in manifest")
    plan = json.loads(plan_path.read_text())
    if plan.get("sha256") != PLAN or plan.get("payload", {}).get("git_head") != BASE:
        raise Stop("frozen HOME-chronology plan has changed")
    for path, expected in plan["payload"]["inputs"].items():
        actual = hashlib.sha256((root / path).read_bytes()).hexdigest()
        if actual != expected:
            raise Stop(f"frozen input changed: {path}")
    return raw, candidates

def patch(root: Path, candidates: list[dict], *, apply: bool):
    paths = {"canonical": root / "data/canonical/games.csv", "assertion": root / "data/evidence/game-assertions.csv"}
    for school in SCHOOLS:
        paths["source:" + school] = root / f"schools/{school}/source-games.csv"
    loaded = {key: _read_csv(path) for key, path in paths.items()}
    canonical = {r["canonical_game_id"]: r for r in loaded["canonical"][1]}
    if len(canonical) != len(loaded["canonical"][1]):
        raise Stop("duplicate canonical game IDs")
    assertions = defaultdict(list)
    for r in loaded["assertion"][1]:
        assertions[r.get("canonical_game_id", "")].append(r)
    sources = {}
    for school in SCHOOLS:
        rows = loaded["source:" + school][1]
        sources[school] = {r["source_game_id"]: r for r in rows}
        if len(sources[school]) != len(rows):
            raise Stop(f"duplicate source IDs: {school}")
    _, disputes = _read_csv(root / "data/reconciliation/discrepancies.csv")
    reviews = defaultdict(list)
    for r in disputes:
        reviews[r.get("canonical_game_id", "")].append(r)
    changed = Counter()
    for c in candidates:
        game_id, school, source_id = c["canonical_game_id"], c["program"], c["source_game_id"]
        game = canonical.get(game_id)
        source = sources[school].get(source_id)
        if game is None or source is None:
            raise Stop(f"missing canonical/source mapping: {game_id}/{source_id}")
        if game.get("game_date", "").strip() != c["game_date"]:
            raise Stop(f"date drift: {game_id}")
        if game.get("game_type", "").strip() != "REGULAR_SEASON":
            raise Stop(f"not a regular-season game: {game_id}")
        site = game.get("site_type", "").strip()
        home = game.get("team_a_key") if site == "TEAM_A_HOME" else game.get("team_b_key") if site == "TEAM_B_HOME" else ""
        if home != school:
            raise Stop(f"canonical HOME authority changed: {game_id}")
        if source.get("source_game_id") != source_id or source.get("source_program_key") != school:
            raise Stop(f"source identity drift: {game_id}")
        mine = [a for a in assertions[game_id] if a.get("source_program_key") == school and a.get("source_game_id") == source_id]
        if len(mine) != 1:
            raise Stop(f"ambiguous source assertion: {game_id}")
        mine = mine[0]
        matching = {a.get("source_game_id") for a in assertions[game_id]
                    if a.get("source_program_key") != school and canonical_site_from_assertion(a) == site}
        declared = set(c.get("reciprocal_home_assertions", []))
        if not declared.issubset(matching):
            raise Stop(f"reciprocal HOME evidence changed: {game_id}")
        if c["part"] == "A":
            if c["authority"] != "source_self_HOME" or source.get("curated_site_type", "").strip() != "SOURCE_PROGRAM_HOME":
                raise Stop(f"source HOME authority drift: {game_id}")
        elif c["part"] == "B":
            if c["authority"] != "reciprocal_participant_HOME_assertion" or source.get("curated_site_type", "").strip() != "UNKNOWN" or not declared:
                raise Stop(f"source UNKNOWN/reciprocal authority drift: {game_id}")
            if c["patches"].get("source") or c["patches"].get("assertion"):
                raise Stop(f"Part B must not alter source assertions: {game_id}")
        else:
            raise Stop(f"unexpected batch part: {game_id}")
        if any(reconciliation_state(reviews[game_id], k) == "UNDER_REVIEW" for k in ("site_type", "venue", "location")):
            raise Stop(f"unresolved site/venue/location dispute: {game_id}")
        conflicting = [a for a in assertions[game_id]
                       if canonical_site_from_assertion(a) not in {site, "UNKNOWN"}]
        if conflicting and reconciliation_state(reviews[game_id], "site_type") != "RESOLVED":
            raise Stop(f"unadjudicated contradictory site assertion: {game_id}")
        rows = {"canonical": game, "source": source, "assertion": mine}
        for kind, row in rows.items():
            patch_fields = c["patches"].get(kind, {})
            expected = c["preimage"].get(kind, {})
            if set(patch_fields) != set(expected) or not set(patch_fields).issubset(FIELDS[kind]):
                raise Stop(f"invalid patch field set: {game_id}/{kind}")
            for field, before in expected.items():
                if row.get(field) != before:
                    raise Stop(f"preimage drift: {game_id}/{kind}/{field}")
            changed[kind] += _patch_blanks(row, patch_fields, label=f"{game_id}/{kind}")
        before = game.get("notes", "")
        game["notes"] = append_note(before, _marker({"program": school, "source_game_id": source_id, "venue": {"venue_key": c["venue_key"]}}))
        changed["notes"] += int(game["notes"] != before)
    if not apply:
        return changed
    originals = {path: path.read_bytes() for path in paths.values()}
    try:
        for key, path in paths.items():
            fields, rows = loaded[key]
            _write_csv_preserving_format(path, fields, rows)
        check = subprocess.run([sys.executable, "tools/validate_data.py"], cwd=root, capture_output=True, text=True)
        if check.returncode:
            raise Stop("validation failed; rolled back: " + (check.stdout + check.stderr)[-1400:])
        census = subprocess.run([sys.executable, "tools/published_site_completeness_census.py", "--json"], cwd=root, capture_output=True, text=True)
        if census.returncode:
            raise Stop("published site census failed; rolled back: " + (census.stdout + census.stderr)[-1400:])
        count = json.loads(census.stdout)["home"]["hard_blockers"]
        if count != 788:
            raise Stop(f"C1 hard-blocker postcondition was {count}, not 788; rolled back")
    except BaseException:
        for path, data in originals.items():
            path.write_bytes(data)
        raise
    return changed

def main():
    args = argparse.ArgumentParser()
    args.add_argument("--apply", action="store_true")
    options = args.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        raw, candidates = preflight(root, root / MANIFEST_PATH, root / PLAN_PATH)
        dest = root / ARCHIVE_PATH
        if dest.exists() and dest.read_bytes() != raw:
            raise Stop("archived exact manifest collision")
        count = patch(root, candidates, apply=options.apply)
        if options.apply:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(raw)
        print(f"PASS: C1 Batch 1 {'APPLIED' if options.apply else 'READ-ONLY'}; "
              f"games={len(candidates)} changed_fields={dict(count)} "
              f"manifest_sha256={MANIFEST}")
        if options.apply:
            print("NEXT: build deterministic site JSON and review staged exact diff; do not merge without Preview approval")
    except (Stop, KeyError, ValueError, OSError, subprocess.CalledProcessError) as exc:
        print("STOP:", exc)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
