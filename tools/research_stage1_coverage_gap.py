#!/usr/bin/env python3
"""Read-only audit of institutional source-acknowledged unidentified historical games.

Never creates games, changes a checkpoint, resolves historical results, or closes Stage 1.
An eligible audit permits a separately serialized, explicitly sourced Stage 1 successor.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

WORDS = dict(zip(
    ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"),
    range(1, 11),
))
ALLOWED = {"SOURCE_EXPLICIT_GAME_MISSING", "SEASON_OUTCOME_CENSUS_MISMATCH"}


def _j(data: bytes):
    return json.loads(data.decode("utf-8-sig"))


def _csv(data: bytes):
    return list(csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline="")))


def _count_missing(note: str) -> int | None:
    m = re.search(
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)"
        r"\s+games?\s+missing\b", note, re.IGNORECASE,
    )
    if not m:
        return None
    word = m.group(1).lower()
    n = int(word) if word.isdecimal() else WORDS[word]
    return n if 0 < n <= 10 else None


def audit_checkpoint(checkpoint: Path, *, evidence_member: str,
                     expected_sha256: str) -> dict:
    """Verify accepted game/census/source-gap separation without modifying input."""
    actual_sha = hashlib.sha256(checkpoint.read_bytes()).hexdigest()
    if not expected_sha256 or actual_sha != expected_sha256:
        return {"status": "FAIL", "checkpoint_sha256": actual_sha,
                "defects": ["CHECKPOINT_HASH_MISMATCH_OR_UNPINNED"]}
    defects: list[str] = []
    with zipfile.ZipFile(checkpoint) as z:
        if z.testzip():
            return {"status": "FAIL", "checkpoint_sha256": actual_sha,
                    "defects": ["INVALID_ARCHIVE_CRC"]}
        names = z.namelist()
        roots = {n.split("/", 1)[0] for n in names if "/" in n}
        if len(roots) != 1 or any("/" not in n for n in names):
            return {"status": "FAIL", "checkpoint_sha256": actual_sha,
                    "defects": ["UNEXPECTED_ARCHIVE_LAYOUT"]}
        prefix = next(iter(roots)) + "/"

        def read(name: str) -> bytes:
            if prefix + name not in names:
                defects.append("MISSING_" + name)
                return b""
            return z.read(prefix + name)

        manifest = _j(read("stage1-manifest.json"))
        tracked = manifest.get("members", {})
        if not isinstance(tracked, dict):
            return {"status": "FAIL", "checkpoint_sha256": actual_sha,
                    "defects": ["INVALID_MANIFEST_MEMBERS"]}
        for name, expected in tracked.items():
            data = read(name)
            if (len(data) != expected.get("size") or
                    hashlib.sha256(data).hexdigest() != expected.get("sha256")):
                defects.append("MANIFEST_MISMATCH:" + name)
        if set(tracked) != {
            n[len(prefix):] for n in names
            if n != prefix + "stage1-manifest.json"
        }:
            defects.append("MANIFEST_MEMBER_SET_MISMATCH")
        status = _j(read("stage1-status.json"))
        blockers = _j(read("blocking-residuals.json"))
        ledger = _csv(read("structured-stage1-ledger.csv"))
        census = _csv(read("season-census.csv"))
        evidence = _j(read(evidence_member))

    if not ledger or not isinstance(blockers, list) or not isinstance(evidence.get("seasons"), list):
        return {"status": "FAIL", "checkpoint_sha256": actual_sha,
                "defects": sorted(set(defects + ["MISSING_LEDGER_BLOCKERS_OR_EVIDENCE"]))}

    ids = [r.get("research_game_id", "").strip() for r in ledger]
    if not all(ids) or len(ids) != len(set(ids)):
        defects.append("BLANK_OR_DUPLICATE_GAME_IDS")
    if any(not r.get("opponent_literal", "").strip() or
           not r.get("game_type", "").strip() for r in ledger):
        defects.append("UNIDENTIFIED_OR_UNTYPED_LEDGER_GAME")
    if any("UNIDENTIFIED" in r.get("game_universe_state", "").upper() for r in ledger):
        defects.append("FABRICATED_UNIDENTIFIED_GAME_ROW")
    if (status.get("total_candidate_game_rows") != len(ledger) or
            manifest.get("game_rows") != len(ledger)):
        defects.append("LEDGER_COUNT_CONFLICT")
    if status.get("research_base_sha") != manifest.get("research_base_sha"):
        defects.append("RESEARCH_BASE_MISMATCH")
    if (len(blockers) != status.get("blocking_residual_count", -1) or
            len(blockers) != manifest.get("blocking_residuals", -1)):
        defects.append("BLOCKER_COUNT_CONFLICT")
    if evidence.get("policy_result") != "RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED":
        defects.append("RESEARCH_NOT_EXHAUSTED")
    if (evidence.get("rows_added") != 0 or
            evidence.get("accepted_game_rows_before") != len(ledger) or
            evidence.get("accepted_game_rows_after") != len(ledger)):
        defects.append("EVIDENCE_IMPLIED_LEDGER_MUTATION")

    census_by_season = {r.get("season"): r for r in census}
    row_counts = Counter(r.get("season_label") for r in ledger)
    evidence_by_season: dict[str, dict] = {}
    for ev in evidence["seasons"]:
        key = ev.get("season", "")
        if not key or key in evidence_by_season:
            defects.append("DUPLICATE_OR_BLANK_EVIDENCE_SEASON")
        evidence_by_season[key] = ev
    residual_seasons = [r.get("season", "") for r in blockers]
    if (len(set(residual_seasons)) != len(blockers) or
            set(residual_seasons) != set(evidence_by_season)):
        defects.append("BLOCKER_EVIDENCE_POPULATION_MISMATCH")

    gaps = []
    for residual in blockers:
        season = residual.get("season", "")
        kind = residual.get("class", "")
        ev = evidence_by_season.get(season, {})
        primary = ev.get("primary_source_state", {})
        count = _count_missing(primary.get("explicit_note", ""))
        if kind not in ALLOWED:
            defects.append("UNRELATED_BLOCKER:" + season)
        if count is None:
            defects.append("NO_EXPLICIT_INSTITUTIONAL_MISSING_COUNT:" + season)
            continue
        c = census_by_season.get(season)
        if c is None or int(c.get("observed_games", "-1")) != row_counts.get(season, -2):
            defects.append("SEASON_LEDGER_CENSUS_MISMATCH:" + season)
        if (primary.get("listed_game_rows") != row_counts.get(season) or
                int(c.get("observed_games", "-1")) != primary.get("listed_game_rows")):
            defects.append("SOURCE_LISTED_ROWS_MISMATCH:" + season)
        if not primary.get("heading") or not primary.get("listed_result_tally"):
            defects.append("MISSING_SOURCE_HEADING_OR_TALLY:" + season)
        if kind == "SOURCE_EXPLICIT_GAME_MISSING":
            note = residual.get("source_note", {})
            if note.get("text", "").strip() != primary.get("explicit_note", "").strip():
                defects.append("SOURCE_NOTE_MISMATCH:" + season)
            if not note.get("page"):
                defects.append("SOURCE_NOTE_PAGE_MISSING:" + season)
        if kind == "SEASON_OUTCOME_CENSUS_MISMATCH":
            detail = residual.get("detail", {})
            if (int(detail.get("expected_games", "-1")) -
                    int(detail.get("observed_games", "-1"))) != count:
                defects.append("SEASON_GAME_DELTA_CONFLICT:" + season)
            if int(detail.get("observed_games", "-1")) != row_counts.get(season):
                defects.append("BLOCKER_LISTED_ROWS_CONFLICT:" + season)
        sources = ev.get("systematic_evidence_checked", [])
        if (not isinstance(sources, list) or len(sources) < 2 or any(
            not r.get("source") or not r.get("finding") or not r.get("authority")
            for r in sources
        )):
            defects.append("INSUFFICIENT_BOUNDED_RESEARCH_EVIDENCE:" + season)
        if (ev.get("disposition") != "BLOCKING_RESEARCHED_UNRESOLVED" or
                residual.get("research_state") != "RESEARCHED_UNRESOLVED"):
            defects.append("NOT_EXPLICITLY_UNRESOLVED:" + season)
        research_summary = (
            residual.get("research_evidence_summary") or
            next((v for k, v in residual.items()
                  if k.endswith("_evidence_summary") and isinstance(v, str) and v.strip()), "")
        )
        if not research_summary or not ev.get("reason"):
            defects.append("MISSING_GAP_PROVENANCE:" + season)
        gaps.append({
            "season": season, "institutional_missing_count": count,
            "identified_game_rows": row_counts.get(season),
            "source_note": primary.get("explicit_note"),
            "source_heading": primary.get("heading"),
            "residual_class": kind,
        })
    if {r.get("season") for r in census if r.get("state") == "MISMATCH"} - set(evidence_by_season):
        defects.append("UNRELATED_UNRESOLVED_SEASON_CENSUS")
    gap_total = sum(g["institutional_missing_count"] for g in gaps)
    for label, value in (
        ("status", status.get("remaining_unknown_real_games")),
        ("manifest", manifest.get("unknown_real_games")),
        ("evidence", evidence.get("unknown_real_games_represented_by_blockers")),
    ):
        if value is not None and value != gap_total:
            defects.append("UNIDENTIFIED_COUNT_MISMATCH:" + label)
    return {
        "schema_version": 1,
        "status": "ELIGIBLE_FOR_SOURCE_ACKNOWLEDGED_COVERAGE_GAP"
                  if not defects and gaps else "FAIL",
        "checkpoint_sha256": actual_sha,
        "research_base_sha": status.get("research_base_sha"),
        "school": status.get("school"),
        "identified_competitive_games": len(ledger),
        "unidentified_games_not_added": gap_total,
        "source_coverage_gaps": sorted(gaps, key=lambda g: g["season"]),
        "defects": sorted(set(defects)),
        "stage1_complete": False,
        "next_action": (
            "Create one separately hashed Stage 1 closeout successor retaining this exact "
            "parent and unchanged identified-game ledger. Preserve all season-level "
            "coverage gaps; stop before Stage 2."
        ),
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("--expected-sha256", required=True)
    parser.add_argument("--evidence-member", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = audit_checkpoint(args.checkpoint, evidence_member=args.evidence_member,
                                  expected_sha256=args.expected_sha256)
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile,
            json.JSONDecodeError, csv.Error) as exc:
        report = {"status": "FAIL", "defects": ["INVALID_INPUT:" + type(exc).__name__]}
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if report["status"] == "ELIGIBLE_FOR_SOURCE_ACKNOWLEDGED_COVERAGE_GAP" else 2


if __name__ == "__main__":
    sys.exit(main())
