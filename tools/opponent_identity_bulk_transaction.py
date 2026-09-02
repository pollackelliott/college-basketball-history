#!/usr/bin/env python3
"""Sealed bulk transaction for reviewed opponent-identity cleanup.

This complements opponent_identity_transaction.py.  The first transaction engine was
purpose-built for a reciprocal-duplicate batch in which every stale canonical row was
absorbed into a counterpart.  A broad owner-reviewed cleanup also needs to support:

* in-place canonical key remaps when no duplicate exists;
* reciprocal duplicate absorption when a key remap exposes one real game twice;
* explicit retention of genuinely distinct undated games whose mapped signatures are
  indistinguishable; and
* owner-reviewed non-D1 rekeys without pretending the target is current D1.

Literal source labels/raw text remain evidence and are never rewritten.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

import opponent_identity_collision_audit as collision_audit
import opponent_identity_remediation as remediation
import opponent_identity_transaction as tx


class BulkTransactionError(RuntimeError):
    pass


MANIFEST_FIELDS = [
    "source_program_key",
    "source_opponent_label",
    "from_program_key",
    "to_program_key",
    "to_program_name",
    "target_current_d1",
    "decision",
    "evidence_basis",
    "evidence_url",
]
SUPPORTED_DECISIONS = {"MERGE_TO_PROGRAM", "REKEY_DISTINCT_NON_D1"}
PAIR_KINDS = {"EXPLICIT_RECONCILIATION", "EXPLICIT_COUNTERPART", "SAME_DATE_IDENTITY_CONFLICT", "EXACT_CORE_MATCH"}


def clean(value: Any) -> str:
    return "" if value is None else str(value).strip()


def stable(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    return tx.read_csv(path)


def manifest_id(row: dict[str, str]) -> str:
    payload = "|".join(clean(row.get(field)) for field in MANIFEST_FIELDS[:7])
    return "OIB-" + sha_text(payload)[:16].upper()


def load_manifest(repo: Path, path: Path) -> tuple[list[dict[str, Any]], dict[str, str], list[str]]:
    fields, rows = read_csv(path)
    missing = [field for field in MANIFEST_FIELDS if field not in fields]
    if missing:
        raise BulkTransactionError("manifest missing fields: " + ", ".join(missing))

    programs, current_d1, _ = remediation.load_programs(repo)
    blockers: list[str] = []
    items: list[dict[str, Any]] = []
    key_map: dict[str, str] = {}
    d1_map: dict[str, str] = {}

    for raw in rows:
        row = {k: clean(raw.get(k)) for k in MANIFEST_FIELDS}
        mid = manifest_id(row)
        source = row["source_program_key"]
        label = row["source_opponent_label"]
        old = row["from_program_key"]
        new = row["to_program_key"]
        name = row["to_program_name"]
        action = row["decision"].upper()
        current = row["target_current_d1"].title()
        basis = row["evidence_basis"]

        if source not in programs:
            blockers.append(f"{mid}: unknown source program {source!r}")
        if action not in SUPPORTED_DECISIONS:
            blockers.append(f"{mid}: unsupported decision {action!r}")
        if not all((label, old, new, name, basis)) or old == new:
            blockers.append(f"{mid}: incomplete or no-op identity decision")
        if current not in {"Yes", "No"}:
            blockers.append(f"{mid}: target_current_d1 must be Yes or No")

        if action == "MERGE_TO_PROGRAM":
            if new not in programs:
                blockers.append(f"{mid}: current-D1 target {new!r} absent from registry")
            elif new not in current_d1:
                blockers.append(f"{mid}: MERGE_TO_PROGRAM target {new!r} is not current D1")
            if current != "Yes":
                blockers.append(f"{mid}: MERGE_TO_PROGRAM requires target_current_d1=Yes")
        elif action == "REKEY_DISTINCT_NON_D1":
            if current != "No":
                blockers.append(f"{mid}: non-D1 rekey requires target_current_d1=No")
            if new in current_d1:
                blockers.append(f"{mid}: non-D1 rekey points at current-D1 registry key {new!r}")

        prior = key_map.get(old)
        if prior and prior != new:
            blockers.append(f"{mid}: global key {old!r} maps inconsistently to {prior!r} and {new!r}")
        key_map[old] = new
        prior_d1 = d1_map.get(old)
        if prior_d1 and prior_d1 != current:
            blockers.append(f"{mid}: inconsistent target_current_d1 for {old!r}")
        d1_map[old] = current

        opponents = repo / "schools" / source / "opponents.csv"
        source_games = repo / "schools" / source / "source-games.csv"
        if not opponents.exists() or not source_games.exists():
            blockers.append(f"{mid}: source package files missing")
            items.append({**row, "manifest_id": mid, "source_game_ids": []})
            continue
        _, opponent_rows = read_csv(opponents)
        matches = [
            r for r in opponent_rows
            if clean(r.get("source_opponent_label")) == label
            and clean(r.get("canonical_opponent_key")) == old
        ]
        if len(matches) != 1:
            blockers.append(f"{mid}: expected exactly one opponents.csv row, found {len(matches)}")
        expected = None
        if matches:
            try:
                expected = int(clean(matches[0].get("games_with_source_label")))
            except ValueError:
                blockers.append(f"{mid}: invalid games_with_source_label")

        _, game_rows = read_csv(source_games)
        game_matches = [
            r for r in game_rows
            if clean(r.get("source_opponent_label")) == label
            and clean(r.get("normalized_opponent_key")) == old
        ]
        if expected is not None and len(game_matches) != expected:
            blockers.append(f"{mid}: source-game count {len(game_matches)} != opponents.csv count {expected}")
        if not game_matches:
            blockers.append(f"{mid}: no matching source-games.csv rows")
        items.append({**row, "manifest_id": mid, "source_game_ids": sorted(clean(r.get("source_game_id")) for r in game_matches)})

    return sorted(items, key=lambda x: x["manifest_id"]), key_map, sorted(set(blockers))


def load_resolutions(path: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    doc = json.loads(path.read_text(encoding="utf-8"))
    if doc.get("schema_version") != 2:
        raise BulkTransactionError("resolution schema must be version 2")
    pair_doc = {"schema_version": 1, "resolutions": doc.get("resolutions") or []}
    temp = path.with_suffix(path.suffix + ".pairs.tmp")
    temp.write_text(json.dumps(pair_doc), encoding="utf-8")
    try:
        pairs = tx.load_resolutions(temp)
    finally:
        temp.unlink(missing_ok=True)

    distinct: list[dict[str, Any]] = []
    seen: set[str] = set()
    for raw in doc.get("retain_distinct") or []:
        rid = clean(raw.get("resolution_id"))
        ids = sorted({clean(x) for x in raw.get("canonical_game_ids") or [] if clean(x)})
        basis = clean(raw.get("resolution_basis"))
        if not rid or rid in seen or len(ids) < 2 or not basis:
            raise BulkTransactionError("each retain_distinct item requires unique id, 2+ canonical ids, and basis")
        seen.add(rid)
        distinct.append({
            "resolution_id": rid,
            "canonical_game_ids": ids,
            "resolution_basis": basis,
            "evidence_urls": sorted(clean(x) for x in raw.get("evidence_urls") or [] if clean(x)),
        })
    return pairs, sorted(distinct, key=lambda x: x["resolution_id"])


def _mapped_unknown_groups(rows: list[dict[str, str]], key_map: dict[str, str], affected: set[str]) -> list[dict[str, Any]]:
    groups: dict[tuple[str, ...], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if clean(row.get("game_date")):
            continue
        mapped = collision_audit.mapped_view(row, key_map)
        signature = (
            mapped["season_label"], mapped["team_a_key"], mapped["team_b_key"],
            mapped["team_a_score"], mapped["team_b_score"], mapped["overtime_periods"],
        )
        groups[signature].append(mapped)
    out = []
    for signature, members in groups.items():
        ids = sorted(clean(r.get("canonical_game_id")) for r in members)
        touched = sorted(set(ids) & affected)
        if touched and len(ids) > 1:
            out.append({"signature": list(signature), "canonical_game_ids": ids, "affected_canonical_game_ids": touched})
    return sorted(out, key=lambda x: (x["signature"], x["canonical_game_ids"]))


def _notes_for_in_place(row: dict[str, str], key_map: dict[str, str]) -> str:
    old = [k for k in (clean(row.get("team_a_key")), clean(row.get("team_b_key"))) if k in key_map]
    marker = "[OPPONENT_IDENTITY_RECONCILIATION in_place_remap=" + ",".join(f"{k}->{key_map[k]}" for k in old) + "]"
    notes = clean(row.get("notes"))
    return (notes + " | " + marker).strip(" |") if notes else marker


def build_plan(repo: Path, manifest_path: Path, resolutions_path: Path) -> dict[str, Any]:
    repo = repo.resolve()
    items, key_map, blockers = load_manifest(repo, manifest_path.resolve())
    pair_resolutions, distinct_resolutions = load_resolutions(resolutions_path.resolve())
    _, canonical_rows = read_csv(repo / "data/canonical/games.csv")
    _, discrepancy_rows = read_csv(repo / "data/reconciliation/discrepancies.csv")

    affected_by_map: dict[str, list[str]] = defaultdict(list)
    affected: set[str] = set()
    for row in canonical_rows:
        gid = clean(row.get("canonical_game_id"))
        old_keys = {clean(row.get("team_a_key")), clean(row.get("team_b_key"))} & set(key_map)
        for old in sorted(old_keys):
            affected_by_map[f"{old}->{key_map[old]}"].append(gid)
            affected.add(gid)
        mapped = tx.maprow(row, key_map)
        if clean(mapped.get("team_a_key")) == clean(mapped.get("team_b_key")):
            blockers.append(f"{gid}: key replacement creates self-game")

    synthetic = {
        "plan_sha256": "bulk-preplan",
        "global_key_map": key_map,
        "affected_canonical_game_ids": {k: sorted(v) for k, v in affected_by_map.items()},
    }
    audit = collision_audit.audit_rows(synthetic, canonical_rows)
    unknown_groups = _mapped_unknown_groups(canonical_rows, key_map, affected)
    byid = {clean(r.get("canonical_game_id")): r for r in canonical_rows}

    pair_lookup = {(r["survivor"], r["absorbed"]): r for r in pair_resolutions}
    pair_by_ids: dict[frozenset[str], dict[str, Any]] = {frozenset((r["survivor"], r["absorbed"])): r for r in pair_resolutions}
    distinct_by_ids = {frozenset(r["canonical_game_ids"]): r for r in distinct_resolutions}
    used_pair_resolutions: set[str] = set()
    used_distinct: set[str] = set()
    pairs: list[dict[str, Any]] = []
    absorbed: set[str] = set()
    pair_survivors: set[str] = set()

    def make_pair(sid: str, aid: str, kind: str, resolution: dict[str, Any] | None) -> None:
        label = f"{sid}->{aid}"
        s = byid.get(sid)
        a = byid.get(aid)
        if not s or not a:
            blockers.append(f"{label}: missing canonical row")
            return
        if aid in absorbed or sid in pair_survivors:
            blockers.append(f"{label}: canonical row paired twice")
            return
        sm, am = tx.maprow(s, key_map), tx.maprow(a, key_map)
        if (clean(sm.get("team_a_key")), clean(sm.get("team_b_key"))) != (clean(am.get("team_a_key")), clean(am.get("team_b_key"))):
            blockers.append(f"{label}: mapped participants mismatch")
        if clean(sm.get("season_label")) != clean(am.get("season_label")):
            blockers.append(f"{label}: season mismatch")
        explicit = dict((resolution or {}).get("canonical_values") or {})
        clear = set((resolution or {}).get("canonical_clear_fields") or [])
        final = {"team_a_key": clean(sm.get("team_a_key")), "team_b_key": clean(sm.get("team_b_key"))}
        for field in [x for x in tx.MERGE_FIELDS if x in s]:
            value, error = tx.mergefield(field, sm.get(field, ""), am.get(field, ""), explicit, clear, label)
            final[field] = value
            if error:
                blockers.append(error)
        notes = []
        for text in [clean(sm.get("notes")), clean(am.get("notes")), f"[OPPONENT_IDENTITY_RECONCILIATION absorbed={aid}; preserved={sid}; one real game / one canonical game]"]:
            if text and text not in notes:
                notes.append(text)
        final["notes"] = " | ".join(notes)
        pairs.append({
            "kind": kind,
            "survivor_canonical_game_id": sid,
            "absorbed_canonical_game_id": aid,
            "resolution_id": clean((resolution or {}).get("resolution_id")),
            "final_canonical_values": final,
            "discrepancies": (resolution or {}).get("discrepancies") or [],
        })
        absorbed.add(aid)
        pair_survivors.add(sid)
        if resolution:
            used_pair_resolutions.add(resolution["resolution_id"])

    for group in audit.get("collision_groups") or []:
        ids = list(group.get("canonical_game_ids") or [])
        idset = frozenset(ids)
        if idset in distinct_by_ids:
            used_distinct.add(distinct_by_ids[idset]["resolution_id"])
            continue
        explicit_pair = pair_by_ids.get(idset)
        if explicit_pair:
            make_pair(explicit_pair["survivor"], explicit_pair["absorbed"], clean(group.get("kind")) or "EXPLICIT_RECONCILIATION", explicit_pair)
            continue
        touched = [gid for gid in ids if gid in affected]
        untouched = [gid for gid in ids if gid not in affected]
        if len(ids) == 2 and len(touched) == 1 and len(untouched) == 1:
            if clean(group.get("kind")) == "SAME_DATE_IDENTITY_CONFLICT":
                blockers.append(f"{touched[0]}->{untouched[0]}: material same-date conflict requires explicit resolution")
                continue
            make_pair(touched[0], untouched[0], clean(group.get("kind")) or "EXACT_CORE_MATCH", None)
        else:
            blockers.append("collision group requires explicit reconciliation: " + ",".join(ids))

    for group in unknown_groups:
        idset = frozenset(group["canonical_game_ids"])
        if idset in distinct_by_ids:
            used_distinct.add(distinct_by_ids[idset]["resolution_id"])
            continue
        explicit_pair = pair_by_ids.get(idset)
        if explicit_pair:
            make_pair(explicit_pair["survivor"], explicit_pair["absorbed"], "UNKNOWN_DATE_EXPLICIT_COUNTERPART", explicit_pair)
            continue
        blockers.append("unknown-date collision requires explicit retain-distinct or counterpart ruling: " + ",".join(group["canonical_game_ids"]))

    # Explicit counterpart resolutions may intentionally bridge rows that the
    # date-based collision audit cannot pair (for example, two source histories
    # disagree on the exact game date).  They are still guarded: the stale-key
    # survivor must be affected by this transaction and the resolution kind must
    # explicitly authorize a non-standard counterpart.
    for resolution in pair_resolutions:
        if resolution["resolution_id"] in used_pair_resolutions:
            continue
        if resolution["kind"] not in {"EXPLICIT_COUNTERPART", "EXPLICIT_RECONCILIATION"}:
            continue
        if resolution["survivor"] not in affected:
            blockers.append(
                f"{resolution['resolution_id']}: explicit counterpart survivor is not an affected stale-key row"
            )
            continue
        make_pair(
            resolution["survivor"],
            resolution["absorbed"],
            "EXPLICIT_COUNTERPART",
            resolution,
        )

    unused_pairs = [r["resolution_id"] for r in pair_resolutions if r["resolution_id"] not in used_pair_resolutions]
    unused_distinct = [r["resolution_id"] for r in distinct_resolutions if r["resolution_id"] not in used_distinct]
    if unused_pairs:
        blockers.append("unused pair resolutions: " + ",".join(unused_pairs))
    if unused_distinct:
        blockers.append("unused retain-distinct resolutions: " + ",".join(unused_distinct))

    remap_only = sorted(affected - absorbed - pair_survivors)
    retained_distinct_ids = sorted({gid for r in distinct_resolutions if r["resolution_id"] in used_distinct for gid in r["canonical_game_ids"]})

    specs: list[dict[str, str]] = []
    for pair in sorted(pairs, key=lambda x: x["survivor_canonical_game_id"]):
        for d in pair["discrepancies"]:
            specs.append({**d, "canonical_game_id": pair["survivor_canonical_game_id"]})
    for did, spec in zip(tx.next_disc_ids(discrepancy_rows, len(specs)), specs):
        spec["discrepancy_id"] = did

    fingerprints = {
        "canonical-games.csv": sha_file(repo / "data/canonical/games.csv"),
        "game-assertions.csv": sha_file(repo / "data/evidence/game-assertions.csv"),
        "discrepancies.csv": sha_file(repo / "data/reconciliation/discrepancies.csv"),
        "manifest.csv": sha_file(manifest_path.resolve()),
        "resolutions.json": sha_file(resolutions_path.resolve()),
    }
    for source in sorted({item["source_program_key"] for item in items}):
        fingerprints[source + "/opponents.csv"] = sha_file(repo / "schools" / source / "opponents.csv")
        fingerprints[source + "/source-games.csv"] = sha_file(repo / "schools" / source / "source-games.csv")

    core = {
        "schema_version": 1,
        "git_head": tx.git_head(repo),
        "global_key_map": key_map,
        "manifest_items": items,
        "affected_canonical_game_count": len(affected),
        "remap_only_canonical_game_ids": remap_only,
        "canonical_pairs": sorted(pairs, key=lambda x: x["survivor_canonical_game_id"]),
        "absorbed_canonical_game_ids": sorted(absorbed),
        "retained_distinct_canonical_game_ids": retained_distinct_ids,
        "retain_distinct_resolutions": [r for r in distinct_resolutions if r["resolution_id"] in used_distinct],
        "new_discrepancies": sorted(specs, key=lambda x: x["discrepancy_id"]),
        "collision_audit_sha256": audit.get("audit_sha256", ""),
        "same_date_collision_group_count": audit.get("same_date_collision_group_count", 0),
        "unknown_date_collision_group_count": len(unknown_groups),
        "blockers": sorted(set(blockers)),
        "fingerprints": fingerprints,
    }
    accounted = set(remap_only) | (pair_survivors & affected) | (absorbed & affected)
    if accounted != affected:
        core["blockers"].append("affected canonical accounting mismatch")
        core["blockers"] = sorted(set(core["blockers"]))
    core["plan_sha256"] = sha_text(stable(core))
    return core


def assert_ready(plan: dict[str, Any]) -> None:
    if plan["blockers"]:
        raise BulkTransactionError("plan blockers: " + " | ".join(plan["blockers"][:10]))


def _run_validation(repo: Path) -> None:
    if subprocess.run([sys.executable, "tools/validate_data.py"], cwd=repo).returncode:
        raise BulkTransactionError("validate_data failed")


def apply(repo: Path, manifest_path: Path, resolutions_path: Path, expected_sha: str, run_validation: bool = True) -> dict[str, Any]:
    repo = repo.resolve()
    plan = build_plan(repo, manifest_path, resolutions_path)
    assert_ready(plan)
    if clean(expected_sha) != plan["plan_sha256"]:
        raise BulkTransactionError(f"sealed plan hash mismatch: expected {expected_sha}, actual {plan['plan_sha256']}")

    paths = [
        repo / "data/canonical/games.csv",
        repo / "data/evidence/game-assertions.csv",
        repo / "data/reconciliation/discrepancies.csv",
    ]
    for item in plan["manifest_items"]:
        paths.extend([
            repo / "schools" / item["source_program_key"] / "opponents.csv",
            repo / "schools" / item["source_program_key"] / "source-games.csv",
        ])
    paths = list(dict.fromkeys(paths))
    originals = {path: path.read_bytes() for path in paths}

    try:
        loaded: dict[Path, tuple[list[str], list[dict[str, str]]]] = {}
        opponent_updates = source_updates = 0
        for item in plan["manifest_items"]:
            op = repo / "schools" / item["source_program_key"] / "opponents.csv"
            sp = repo / "schools" / item["source_program_key"] / "source-games.csv"
            loaded.setdefault(op, read_csv(op))
            loaded.setdefault(sp, read_csv(sp))
            _, opponent_rows = loaded[op]
            _, source_rows = loaded[sp]
            matches = [
                r for r in opponent_rows
                if clean(r.get("source_opponent_label")) == item["source_opponent_label"]
                and clean(r.get("canonical_opponent_key")) == item["from_program_key"]
            ]
            if len(matches) != 1:
                raise BulkTransactionError(item["manifest_id"] + ": opponents row changed")
            matches[0]["canonical_opponent_key"] = item["to_program_key"]
            matches[0]["canonical_opponent_name"] = item["to_program_name"]
            matches[0]["current_d1"] = item["target_current_d1"]
            opponent_updates += 1

            ids = set(item["source_game_ids"])
            source_matches = [r for r in source_rows if clean(r.get("source_game_id")) in ids]
            if {clean(r.get("source_game_id")) for r in source_matches} != ids:
                raise BulkTransactionError(item["manifest_id"] + ": source game set changed")
            for row in source_matches:
                if clean(row.get("normalized_opponent_key")) != item["from_program_key"]:
                    raise BulkTransactionError(item["manifest_id"] + ": source opponent key changed")
                row["normalized_opponent_key"] = item["to_program_key"]
                row["opponent_current_d1"] = item["target_current_d1"]
                source_updates += 1

        cf, cr = read_csv(repo / "data/canonical/games.csv")
        af, ar = read_csv(repo / "data/evidence/game-assertions.csv")
        df, dr = read_csv(repo / "data/reconciliation/discrepancies.csv")
        byid = {clean(r.get("canonical_game_id")): r for r in cr}
        key_map = plan["global_key_map"]

        for gid in plan["remap_only_canonical_game_ids"]:
            row = byid.get(gid)
            if not row:
                raise BulkTransactionError(gid + ": canonical row disappeared")
            mapped = tx.maprow(row, key_map)
            mapped["notes"] = _notes_for_in_place(row, key_map)
            row.update(mapped)

        redirect: dict[str, str] = {}
        for pair in plan["canonical_pairs"]:
            sid = pair["survivor_canonical_game_id"]
            aid = pair["absorbed_canonical_game_id"]
            survivor = byid.get(sid)
            if not survivor or aid not in byid:
                raise BulkTransactionError("canonical pair disappeared")
            for field, value in pair["final_canonical_values"].items():
                if field not in cf:
                    raise BulkTransactionError("canonical schema changed: " + field)
                survivor[field] = clean(value)
            redirect[aid] = sid
        cr = [r for r in cr if clean(r.get("canonical_game_id")) not in redirect]

        redirected = 0
        for row in ar:
            gid = clean(row.get("canonical_game_id"))
            if gid in redirect:
                row["canonical_game_id"] = redirect[gid]
                redirected += 1
            old = clean(row.get("normalized_opponent_key"))
            if old in key_map:
                row["normalized_opponent_key"] = key_map[old]

        for row in dr:
            gid = clean(row.get("canonical_game_id"))
            if gid in redirect:
                row["canonical_game_id"] = redirect[gid]
        existing = {clean(r.get("discrepancy_id")) for r in dr}
        for spec in plan["new_discrepancies"]:
            if spec["discrepancy_id"] in existing:
                raise BulkTransactionError("discrepancy id collision")
            dr.append({field: clean(spec.get(field)) for field in tx.DISC_FIELDS})

        for path, (fields, rows) in loaded.items():
            tx.write_csv(path, fields, rows)
        tx.write_csv(repo / "data/canonical/games.csv", cf, cr)
        tx.write_csv(repo / "data/evidence/game-assertions.csv", af, ar)
        tx.write_csv(repo / "data/reconciliation/discrepancies.csv", df, dr)

        _, cr2 = read_csv(repo / "data/canonical/games.csv")
        _, ar2 = read_csv(repo / "data/evidence/game-assertions.csv")
        old_keys = set(key_map)
        absorbed = set(plan["absorbed_canonical_game_ids"])
        if any(clean(r.get("canonical_game_id")) in absorbed for r in cr2):
            raise BulkTransactionError("postcondition: absorbed canonical row remains")
        if any(clean(r.get("team_a_key")) in old_keys or clean(r.get("team_b_key")) in old_keys for r in cr2):
            raise BulkTransactionError("postcondition: stale canonical key remains")
        if any(clean(r.get("canonical_game_id")) in absorbed or clean(r.get("normalized_opponent_key")) in old_keys for r in ar2):
            raise BulkTransactionError("postcondition: stale assertion mapping remains")
        retained = set(plan["retained_distinct_canonical_game_ids"])
        if retained and not retained.issubset({clean(r.get("canonical_game_id")) for r in cr2}):
            raise BulkTransactionError("postcondition: retain-distinct row was lost")
        if run_validation:
            _run_validation(repo)
    except Exception:
        for path, data in originals.items():
            path.write_bytes(data)
        raise

    return {
        "plan_sha256": plan["plan_sha256"],
        "canonical_games_remapped_in_place": len(plan["remap_only_canonical_game_ids"]),
        "canonical_games_absorbed": len(plan["absorbed_canonical_game_ids"]),
        "retained_distinct_games": len(plan["retained_distinct_canonical_game_ids"]),
        "assertions_redirected": redirected,
        "opponents_rows_updated": opponent_updates,
        "source_game_rows_updated": source_updates,
        "discrepancies_added": len(plan["new_discrepancies"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    sub = parser.add_subparsers(dest="cmd", required=True)
    plan_cmd = sub.add_parser("plan")
    plan_cmd.add_argument("manifest", type=Path)
    plan_cmd.add_argument("resolutions", type=Path)
    plan_cmd.add_argument("--output", type=Path)
    plan_cmd.add_argument("--json", action="store_true")
    apply_cmd = sub.add_parser("apply")
    apply_cmd.add_argument("manifest", type=Path)
    apply_cmd.add_argument("resolutions", type=Path)
    apply_cmd.add_argument("--expected-plan-sha256", required=True)
    apply_cmd.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        if args.cmd == "plan":
            plan = build_plan(args.repo, args.manifest, args.resolutions)
            payload = json.dumps(plan, indent=2, sort_keys=True) + "\n"
            if args.output:
                args.output.write_text(payload, encoding="utf-8")
            if args.json:
                print(payload, end="")
            else:
                print(
                    "BULK OPPONENT IDENTITY PLAN\n"
                    f"affected={plan['affected_canonical_game_count']} "
                    f"in_place={len(plan['remap_only_canonical_game_ids'])} "
                    f"pairs={len(plan['canonical_pairs'])} "
                    f"absorbed={len(plan['absorbed_canonical_game_ids'])} "
                    f"retained_distinct={len(plan['retained_distinct_canonical_game_ids'])} "
                    f"blockers={len(plan['blockers'])}\n"
                    f"plan sha256: {plan['plan_sha256']}"
                )
            return 2 if plan["blockers"] else 0
        if not args.apply:
            raise BulkTransactionError("apply command requires explicit --apply")
        result = apply(args.repo, args.manifest, args.resolutions, args.expected_plan_sha256)
        print("PASS: " + stable(result))
        return 0
    except (BulkTransactionError, FileNotFoundError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print("FAIL:", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
