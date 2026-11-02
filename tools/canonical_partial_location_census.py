#!/usr/bin/env python3
"""Read-only complete canonical one-sided city/state census with reciprocal evidence.

Never changes protected data. Each canonical ID is counted once, with all matched
source assertions retained for evidentiary classification. A missing normalized
state alone does not authorize a historical or geographic inference.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

def scan(repo: Path) -> dict:
    path = repo / "data/canonical/games.csv"
    raw_sha = hashlib.sha256(path.read_bytes()).hexdigest()
    partial: dict[str, dict] = {}
    total = 0
    with path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            total += 1
            city = row.get("site_city", "").strip()
            state = row.get("site_state", "").strip()
            if bool(city) == bool(state):
                continue
            gid = row.get("canonical_game_id", "").strip()
            if not gid or gid in partial:
                raise ValueError("Duplicate or blank canonical game ID in partial population")
            partial[gid] = {
                "canonical_game_id": gid,
                "season": row.get("season_label", ""),
                "date": row.get("game_date", ""),
                "teams": [row.get("team_a_key", ""), row.get("team_b_key", "")],
                "site_type": row.get("site_type", ""),
                "city": city,
                "state": state,
                "venue_id": row.get("venue_id", ""),
                "venue_key": row.get("venue_key", ""),
                "canonical_status": row.get("canonical_status", ""),
                "source_assertions": [],
            }
    assertions_path = repo / "data/evidence/game-assertions.csv"
    assertion_sha = hashlib.sha256(assertions_path.read_bytes()).hexdigest()
    assertion_count = 0
    with assertions_path.open(newline="", encoding="utf-8-sig") as handle:
        for assertion in csv.DictReader(handle):
            gid = assertion.get("canonical_game_id", "").strip()
            if gid not in partial:
                continue
            assertion_count += 1
            partial[gid]["source_assertions"].append({
                "source_program_key": assertion.get("source_program_key", ""),
                "source_game_id": assertion.get("source_game_id", ""),
                "city": assertion.get("city", "").strip(),
                "state": assertion.get("state", "").strip(),
                "curated_site_type": assertion.get("curated_site_type", ""),
                "source_venue_name": assertion.get("source_venue_name", ""),
                "curated_venue_name": assertion.get("curated_venue_name", ""),
                "raw_text": assertion.get("raw_text", "")[:360],
            })
    venue_path = repo / "data/reference/venues.csv"
    by_id = {}
    with venue_path.open(newline="", encoding="utf-8-sig") as handle:
        for venue in csv.DictReader(handle):
            vid = venue.get("venue_id", "").strip()
            if vid:
                by_id[vid] = venue
    types = Counter()
    classes = Counter()
    records = []
    for game in sorted(partial.values(), key=lambda g: g["canonical_game_id"]):
        game["source_assertions"].sort(key=lambda x: (x["source_program_key"], x["source_game_id"]))
        types[game["site_type"]] += 1
        venue = by_id.get(game["venue_id"])
        evidence = game["source_assertions"]
        same_city_complete = [
            a for a in evidence
            if a["city"].casefold() == game["city"].casefold()
            and a["city"] and a["state"]
        ]
        any_complete = [a for a in evidence if a["city"] and a["state"]]
        if game["venue_id"] and venue and venue.get("city") and venue.get("state"):
            category = "REGISTERED_VENUE_GEO_AVAILABLE"
        elif same_city_complete:
            category = "SAME_CITY_COMPLETE_ASSERTION"
        elif any_complete:
            category = "DIFFERENT_CITY_COMPLETE_ASSERTION_REVIEW"
        elif evidence:
            category = "ONLY_PARTIAL_OR_EMPTY_ASSERTIONS"
        else:
            category = "NO_SOURCE_ASSERTIONS"
        game["evidence_classification"] = category
        if venue:
            game["registered_venue"] = {
                key: venue.get(key, "") for key in ("venue_id", "venue_key", "display_name", "city", "state")
            }
        classes[category] += 1
        records.append(game)
    payload = {
        "schema_version": 1,
        "canonical_sha256": raw_sha,
        "assertions_sha256": assertion_sha,
        "canonical_game_count": total,
        "partial_canonical_count": len(records),
        "affected_assertion_count": assertion_count,
        "by_site_type": dict(sorted(types.items())),
        "by_evidence_classification": dict(sorted(classes.items())),
        "records": records,
    }
    payload["census_sha256"] = hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()
    return payload

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--output", type=Path)
    args = p.parse_args()
    report = scan(args.repo)
    value = json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(value, encoding="utf-8")
    print(value, end="")

if __name__ == "__main__":
    main()
