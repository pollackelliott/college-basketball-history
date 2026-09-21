#!/usr/bin/env python3
"""Durable Stage 3A research-state helpers.

Commands:
  check           validate the full row-level Stage 3A ledger against Stage 1
  neutral-lookup  surface read-only exact-game canonical site candidates
  apply-updates   fold accepted sparse updates into the full Stage 3A ledger
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

REGULAR = "REGULAR_SEASON"
POSTSEASON = "POSTSEASON_HANDOFF"
TERMINAL_ACTIONS = {"NONE", "NO_SOURCE_SCHOOL_VENUE_RESEARCH", POSTSEASON}
HOME_EXCEPTION = "RESEARCHED_UNRESOLVED_HOME_VENUE"
NEUTRAL_DEBT = {"RESEARCHED_PARTIAL", "RESEARCHED_UNRESOLVED"}
CLEAR = "__CLEAR__"
REQUIRED = {
    "research_game_id", "source_program_key", "season_label", "game_date",
    "normalized_opponent_key", "stage3a_disposition", "stage3a_han",
    "stage3a_venue_name", "stage3a_city", "stage3a_state",
    "stage3a_site_research_status", "stage3a_site_research_basis",
    "stage3a_boundary_correction", "stage3a_next_action",
}


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields: list[str], rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _year(season: str) -> int | None:
    match = re.fullmatch(r"(\d{4})-(\d{2}|\d{4})", season.strip())
    if not match:
        return None
    start = int(match.group(1))
    end_text = match.group(2)
    if len(end_text) == 2:
        return start if int(end_text) == (start + 1) % 100 else None
    return start if int(end_text) == start + 1 else None


def _ids(rows: Iterable[dict[str, str]]) -> Counter[str]:
    return Counter(row.get("research_game_id", "").strip() for row in rows)


def _examples(values: list[str]) -> str:
    return ", ".join(values[:12])


def stage3a_state_report(
    universe_fields: Iterable[str],
    universe: list[dict[str, str]],
    ledger_fields: Iterable[str],
    ledger: list[dict[str, str]],
    *,
    handoff_fields: Iterable[str] | None = None,
    handoff: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if "research_game_id" not in set(universe_fields):
        errors.append("Stage 1 universe missing research_game_id")
    missing_fields = sorted(REQUIRED - set(ledger_fields))
    if missing_fields:
        errors.append("Stage 3A ledger missing columns: " + ", ".join(missing_fields))
    if errors:
        return {"complete": False, "errors": errors, "warnings": warnings, "counts": {}}

    uc, lc = _ids(universe), _ids(ledger)
    ublank, lblank = uc.pop("", 0), lc.pop("", 0)
    udupes = sorted(k for k, v in uc.items() if v > 1)
    ldupes = sorted(k for k, v in lc.items() if v > 1)
    if ublank or udupes:
        errors.append("Stage 1 universe has blank/duplicate research_game_id values")
    if lblank or ldupes:
        errors.append("Stage 3A ledger has blank/duplicate research_game_id values")
    missing_ids, extra_ids = sorted(set(uc) - set(lc)), sorted(set(lc) - set(uc))
    if missing_ids:
        errors.append(f"Stage 3A ledger missing {len(missing_ids)} Stage 1 IDs: {_examples(missing_ids)}")
    if extra_ids:
        errors.append(f"Stage 3A ledger has {len(extra_ids)} extra IDs: {_examples(extra_ids)}")

    disp, han, actions = Counter(), Counter(), Counter()
    bad: dict[str, list[str]] = {k: [] for k in [
        "identity", "season", "disposition", "han", "action", "postseason_action",
        "unknown_terminal", "status_basis", "home", "away", "neutral",
    ]}
    counts = Counter()
    postseason_ids: set[str] = set()

    for row in ledger:
        gid = row["research_game_id"].strip()
        if not gid:
            continue
        source = row["source_program_key"].strip()
        opponent = row["normalized_opponent_key"].strip()
        season = row["season_label"].strip()
        year = _year(season)
        if not source or not opponent or not season:
            bad["identity"].append(gid)
        if year is None:
            bad["season"].append(gid)

        disposition = row["stage3a_disposition"].strip().upper()
        action = row["stage3a_next_action"].strip().upper()
        status = row["stage3a_site_research_status"].strip().upper()
        basis = row["stage3a_site_research_basis"].strip()
        disp[disposition] += 1
        if disposition not in {REGULAR, POSTSEASON}:
            bad["disposition"].append(gid)
            continue
        if not action:
            bad["action"].append(gid)
        elif action not in TERMINAL_ACTIONS:
            actions[action] += 1
        if bool(status) != bool(basis):
            bad["status_basis"].append(gid)

        if disposition == POSTSEASON:
            postseason_ids.add(gid)
            if action != POSTSEASON:
                bad["postseason_action"].append(gid)
            continue

        site = row["stage3a_han"].strip().upper()
        han[site] += 1
        if site not in {"HOME", "OPPONENT_HOME", "NEUTRAL", "UNKNOWN"}:
            bad["han"].append(gid)
            continue
        if site == "UNKNOWN":
            counts["unknown_han_rows"] += 1
            if action in TERMINAL_ACTIONS:
                bad["unknown_terminal"].append(gid)
            continue

        venue = row["stage3a_venue_name"].strip()
        city = row["stage3a_city"].strip()
        state = row["stage3a_state"].strip()

        if site == "HOME":
            counts["home_rows"] += 1
            if venue and city and state:
                counts["home_exact_rows"] += 1
            elif not venue and city and state and status == HOME_EXCEPTION and basis:
                counts["home_researched_unresolved_venue_rows"] += 1
            elif action in TERMINAL_ACTIONS:
                bad["home"].append(gid)

        elif site == "OPPONENT_HOME":
            counts["opponent_home_rows"] += 1
            if not venue:
                counts["opponent_home_blank_rows"] += 1
                if action == "NO_SOURCE_SCHOOL_VENUE_RESEARCH":
                    counts["opponent_home_no_research_rows"] += 1
                else:
                    bad["away"].append(gid)
            elif not city or not state:
                bad["away"].append(gid)

        else:
            counts["neutral_rows"] += 1
            if venue and city and state:
                counts["neutral_exact_rows"] += 1
            else:
                modern = year is not None and year >= 1984
                counts["modern_neutral_unresolved_rows" if modern else "historical_neutral_unresolved_rows"] += 1
                accounted = status in NEUTRAL_DEBT and bool(basis)
                if not accounted and action in TERMINAL_ACTIONS:
                    bad["neutral"].append(gid)

    labels = {
        "identity": "missing source/opponent/season identity fields",
        "season": "invalid season_label",
        "disposition": "invalid stage3a_disposition",
        "han": "invalid stage3a_han",
        "action": "blank stage3a_next_action",
        "postseason_action": "postseason row not marked POSTSEASON_HANDOFF action",
        "unknown_terminal": "UNKNOWN H/A/N incorrectly marked terminal",
        "status_basis": "site research status/basis not paired",
        "home": "HOME row lacks exact site or valid HOME exception",
        "away": "OPPONENT_HOME row violates source-school responsibility accounting",
        "neutral": "NEUTRAL gap lacks researched-debt accounting",
    }
    for key, values in bad.items():
        if values:
            errors.append(f"{labels[key]}: {len(values)} row(s); examples: {_examples(values)}")

    if handoff is not None:
        if "research_game_id" not in set(handoff_fields or []):
            errors.append("postseason handoff missing research_game_id")
        else:
            hc = _ids(handoff)
            hblank = hc.pop("", 0)
            hdupes = [k for k, v in hc.items() if v > 1]
            if hblank or hdupes:
                errors.append("postseason handoff has blank/duplicate IDs")
            if set(hc) != postseason_ids:
                errors.append(
                    "postseason handoff ID set differs from Stage 3A disposition: "
                    f"missing={len(postseason_ids-set(hc))}, extra={len(set(hc)-postseason_ids)}"
                )

    if counts["modern_neutral_unresolved_rows"]:
        warnings.append(
            f"{counts['modern_neutral_unresolved_rows']} modern NEUTRAL row(s) remain without exact site; "
            "document the 1984-85+ strong-completeness pass before completion"
        )

    active = sum(actions.values())
    result_counts: dict[str, Any] = {
        "stage1_rows": len(universe), "stage1_unique_ids": len(uc),
        "stage3a_rows": len(ledger), "stage3a_unique_ids": len(lc),
        "regular_season_rows": disp[REGULAR], "postseason_handoff_rows": disp[POSTSEASON],
        "han": dict(sorted(han.items())), "active_action_rows": active,
        "active_actions": dict(sorted(actions.items())), **dict(sorted(counts.items())),
    }
    return {"complete": not errors and active == 0, "errors": errors, "warnings": warnings, "counts": result_counts}


def _canonical_han(row: dict[str, str], source: str) -> str:
    site = row.get("site_type", "").strip().upper()
    a, b = row.get("team_a_key", "").strip(), row.get("team_b_key", "").strip()
    if site == "NEUTRAL":
        return "NEUTRAL"
    if site == "TEAM_A_HOME":
        return "HOME" if source == a else "OPPONENT_HOME" if source == b else "UNKNOWN"
    if site == "TEAM_B_HOME":
        return "HOME" if source == b else "OPPONENT_HOME" if source == a else "UNKNOWN"
    return "UNKNOWN"


def canonical_neutral_lookup(
    ledger: list[dict[str, str]], canonical: Iterable[dict[str, str]], venues: Iterable[dict[str, str]], *, only_missing: bool = True
) -> list[dict[str, str]]:
    targets = [r for r in ledger if r.get("stage3a_disposition", "").upper() == REGULAR and r.get("stage3a_han", "").upper() == "NEUTRAL" and (not only_missing or not r.get("stage3a_venue_name", "").strip())]
    wanted: dict[tuple[str, tuple[str, str]], list[str]] = {}
    by_id = {r["research_game_id"].strip(): r for r in targets}
    for r in targets:
        date, source, opp = r.get("game_date", "").strip(), r.get("source_program_key", "").strip(), r.get("normalized_opponent_key", "").strip()
        if date and source and opp:
            wanted.setdefault((date, tuple(sorted((source, opp)))), []).append(r["research_game_id"].strip())
    matches = {gid: [] for gid in by_id}
    for c in canonical:
        key = (c.get("game_date", "").strip(), tuple(sorted((c.get("team_a_key", "").strip(), c.get("team_b_key", "").strip()))))
        for gid in wanted.get(key, []):
            matches[gid].append(c)
    venue_id = {v.get("venue_id", "").strip(): v for v in venues if v.get("venue_id", "").strip()}
    venue_key = {v.get("venue_key", "").strip(): v for v in venues if v.get("venue_key", "").strip()}
    out = []
    for gid, r in by_id.items():
        base = {"research_game_id": gid, "season_label": r.get("season_label", ""), "game_date": r.get("game_date", ""), "source_program_key": r.get("source_program_key", ""), "normalized_opponent_key": r.get("normalized_opponent_key", ""), "lookup_status": "", "canonical_game_id": "", "canonical_han_for_source": "", "canonical_site_type": "", "canonical_venue_key": "", "canonical_venue_id": "", "canonical_venue_name": "", "canonical_site_city": "", "canonical_site_state": "", "canonical_status": "", "canonical_notes": "", "provenance": ""}
        date, source, opp = base["game_date"].strip(), base["source_program_key"].strip(), base["normalized_opponent_key"].strip()
        found = matches[gid]
        if not date or not source or not opp:
            base["lookup_status"] = "INSUFFICIENT_INPUT"
        elif not found:
            base["lookup_status"] = "NO_MATCH"
        elif len(found) > 1:
            base["lookup_status"] = f"AMBIGUOUS_{len(found)}_MATCHES"
            base["canonical_game_id"] = "|".join(sorted(c.get("canonical_game_id", "") for c in found))
        else:
            c = found[0]
            vid, vkey = c.get("venue_id", "").strip(), c.get("venue_key", "").strip()
            v = venue_id.get(vid) or venue_key.get(vkey) or {}
            chan = _canonical_han(c, source)
            name = v.get("display_name", "").strip()
            city = c.get("site_city", "").strip() or v.get("city", "").strip()
            state = c.get("site_state", "").strip() or v.get("state", "").strip()
            complete_site = bool(vid or vkey or name) and bool(city and state)
            status = "H_A_N_CONTRADICTION" if chan not in {"NEUTRAL", "UNKNOWN"} else "EXACT_VENUE_CANDIDATE" if complete_site else "EXACT_GAME_SITE_INCOMPLETE"
            base.update({"lookup_status": status, "canonical_game_id": c.get("canonical_game_id", ""), "canonical_han_for_source": chan, "canonical_site_type": c.get("site_type", ""), "canonical_venue_key": vkey, "canonical_venue_id": vid, "canonical_venue_name": name, "canonical_site_city": city, "canonical_site_state": state, "canonical_status": c.get("canonical_status", ""), "canonical_notes": c.get("notes", ""), "provenance": f"data/canonical/games.csv:{c.get('canonical_game_id','')}" + (f";data/reference/venues.csv:{vid}" if vid else "")})
        out.append(base)
    return out


def apply_sparse_updates(fields: list[str], rows: list[dict[str, str]], update_fields: list[str], updates: list[dict[str, str]]) -> tuple[list[dict[str, str]], dict[str, Any]]:
    if "research_game_id" not in fields or "research_game_id" not in update_fields:
        raise ValueError("ledger and updates both require research_game_id")
    extra = sorted(set(update_fields) - set(fields))
    if extra:
        raise ValueError("updates contain fields absent from ledger: " + ", ".join(extra))
    by_id = {r.get("research_game_id", "").strip(): r for r in rows}
    if "" in by_id or len(by_id) != len(rows):
        raise ValueError("ledger has blank or duplicate research_game_id")
    seen, changed, changed_fields = set(), set(), Counter()
    for u in updates:
        gid = u.get("research_game_id", "").strip()
        if not gid or gid in seen:
            raise ValueError("updates have blank or duplicate research_game_id")
        seen.add(gid)
        if gid not in by_id:
            raise ValueError(f"update ID absent from ledger: {gid}")
        for field in update_fields:
            if field == "research_game_id" or u.get(field, "") == "":
                continue
            value = "" if u[field] == CLEAR else u[field]
            if by_id[gid].get(field, "") != value:
                by_id[gid][field] = value
                changed.add(gid)
                changed_fields[field] += 1
    return rows, {"updated_input_rows": len(updates), "changed_rows": len(changed), "changed_fields": dict(sorted(changed_fields.items()))}


def _dump(payload: dict[str, Any], path: Path | None = None) -> None:
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stage 3A durable-state helpers")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("check")
    check.add_argument("--universe", type=Path, required=True)
    check.add_argument("--ledger", type=Path, required=True)
    check.add_argument("--handoff", type=Path)
    check.add_argument("--report", type=Path)
    check.add_argument("--require-complete", action="store_true")
    lookup = sub.add_parser("neutral-lookup")
    lookup.add_argument("--ledger", type=Path, required=True)
    lookup.add_argument("--output", type=Path, required=True)
    lookup.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    lookup.add_argument("--all-neutral", action="store_true")
    apply_cmd = sub.add_parser("apply-updates")
    apply_cmd.add_argument("--ledger", type=Path, required=True)
    apply_cmd.add_argument("--updates", type=Path, required=True)
    apply_cmd.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "check":
        uf, universe = read_csv(args.universe)
        lf, ledger = read_csv(args.ledger)
        hf = handoff = None
        if args.handoff:
            hf, handoff = read_csv(args.handoff)
        report = stage3a_state_report(uf, universe, lf, ledger, handoff_fields=hf, handoff=handoff)
        report["sha256"] = {"universe": sha256_file(args.universe), "ledger": sha256_file(args.ledger), **({"handoff": sha256_file(args.handoff)} if args.handoff else {})}
        _dump(report, args.report)
        return 1 if report["errors"] or (args.require_complete and not report["complete"]) else 0
    if args.command == "neutral-lookup":
        lf, ledger = read_csv(args.ledger)
        missing = sorted(REQUIRED - set(lf))
        if missing:
            raise SystemExit("Stage 3A ledger missing columns: " + ", ".join(missing))
        _, canonical = read_csv(args.repo / "data/canonical/games.csv")
        _, venues = read_csv(args.repo / "data/reference/venues.csv")
        out = canonical_neutral_lookup(ledger, canonical, venues, only_missing=not args.all_neutral)
        fields = ["research_game_id", "season_label", "game_date", "source_program_key", "normalized_opponent_key", "lookup_status", "canonical_game_id", "canonical_han_for_source", "canonical_site_type", "canonical_venue_key", "canonical_venue_id", "canonical_venue_name", "canonical_site_city", "canonical_site_state", "canonical_status", "canonical_notes", "provenance"]
        write_csv(args.output, fields, out)
        _dump({"rows": len(out), "lookup_status": dict(sorted(Counter(r["lookup_status"] for r in out).items())), "output": str(args.output), "output_sha256": sha256_file(args.output), "note": "read-only evidence candidates; no Stage 3A row was mutated"})
        return 0
    lf, ledger = read_csv(args.ledger)
    uf, updates = read_csv(args.updates)
    try:
        rows, report = apply_sparse_updates(lf, ledger, uf, updates)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    write_csv(args.output, lf, rows)
    report.update({"output": str(args.output), "output_rows": len(rows), "output_sha256": sha256_file(args.output)})
    _dump(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
