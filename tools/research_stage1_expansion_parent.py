#!/usr/bin/env python3
"""Fail-closed exact-source expansion Stage 1 parent materialization adapter.

No source-game, historical conclusion, protected-main row, or authority registry is
modified. A terminal closeout is separately gated by the permanent generic owner-authority registry.

Commands:
  materialize CHECKPOINT SOURCE --checkpoint-sha SHA --source-blob SHA --output PARENT [--accept-verified-candidates]
  audit PARENT --parent-sha SHA [--registry JSON] [--output REPORT]
  closeout PARENT AUDIT --parent-sha SHA --audit-sha SHA [--registry JSON] --output ZIP
  verify-closeout PARENT SUCCESSOR AUDIT --parent-sha SHA --successor-sha SHA --audit-sha SHA [--registry JSON]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

REGISTRY_PATH = "data/reference/expansion-stage1-accounting-authorities.json"
REGISTRY = Path(__file__).resolve().parents[1] / REGISTRY_PATH
BASE = "df73675852ec5a43dfac50da0ee06d8bcabf8832"
SCHOOL = "arizona-state"
ORIGINAL_BLOB = "bb2e5ddb63e2caab96c2f3eb33d4d231bf75c875"
CHECKPOINT_0018 = "f3391cca078e25f4e3a737b632026aa5636d0723519b3b95805688c7dbe6e10d"
TRANSPORT_SHA = "3118188075b1ce4f028bf25653f979c64e83a63714c674344c26b7e16208f63f"
AGGREGATES = {"1916-1917": (0, 1), "1917-1918": (14, 4),
              "1919-1920": (5, 3), "1943-1944": (12, 2)}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(raw):
    return hashlib.sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest()


def jb(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode()


def read_csv(raw):
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def write_csv(rows, fields=None):
    fields = fields or (list(rows[0]) if rows else [])
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode()


def zip_read(path, pin):
    raw = Path(path).read_bytes()
    if not re.fullmatch("[a-f0-9]{64}", pin or "") or sha(raw) != pin:
        raise ValueError("EXACT_ZIP_HASH_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if z.testzip():
            raise ValueError("ZIP_CRC_INVALID")
        names = z.namelist()
        if len(names) != len(set(names)) or not names or any(
                n.startswith("/") or ".." in Path(n).parts or n.endswith("/") for n in names):
            raise ValueError("UNSAFE_ZIP_ENTRIES")
        members = {n: z.read(n) for n in names}
    if "manifest.json" not in members:
        raise ValueError("MISSING_MANIFEST")
    manifest = json.loads(members["manifest.json"])
    if "member_sha256" in manifest:
        expected = manifest["member_sha256"]
        if set(expected) != set(members) - {"manifest.json"}:
            raise ValueError("MANIFEST_MEMBER_SET_MISMATCH")
        for name, digest in expected.items():
            if sha(members[name]) != digest or len(members[name]) != manifest["member_bytes"][name]:
                raise ValueError("MANIFEST_MEMBER_MISMATCH:" + name)
    elif "files" in manifest and isinstance(manifest["files"], list):
        expected = {v["path"]: v for v in manifest["files"]}
        if set(expected) != set(members) - {"manifest.json"}:
            raise ValueError("MANIFEST_MEMBER_SET_MISMATCH")
        for name, info in expected.items():
            if sha(members[name]) != info["sha256"] or len(members[name]) != info["size"]:
                raise ValueError("MANIFEST_MEMBER_MISMATCH:" + name)
    else:
        raise ValueError("UNKNOWN_MANIFEST_CONTRACT")
    return members, manifest


def write_zip(path, members, metadata, *, modern=False):
    if "manifest.json" in members:
        raise ValueError("MANIFEST_RESERVED")
    manifest = {**metadata, "member_sha256": {k: sha(v) for k, v in sorted(members.items())},
                "member_bytes": {k: len(v) for k, v in sorted(members.items())},
                "files": [{"path": k, "size": len(v), "sha256": sha(v)} for k, v in sorted(members.items())]}
    if modern:
        manifest.pop("member_sha256", None)
        manifest.pop("member_bytes", None)
    contents = {**members, "manifest.json": jb(manifest)}
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, value in sorted(contents.items()):
            info = zipfile.ZipInfo(name, date_time=(2020, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, value)
    return sha(Path(path).read_bytes())


def original_literal_results(transport):
    """Authenticate nested original 0002 directly; no conversational evidence joins."""
    with zipfile.ZipFile(io.BytesIO(transport)) as top:
        manifest = json.loads(top.read("transport-manifest.json"))
        nested = "originals/arizona-state-early-universe-partial-0002.zip"
        orig = top.read(nested)
        # Different transport manifests may key by basename; require an explicit exact match.
        if not any(v == sha(orig) for v in _all_string_values(manifest)):
            raise ValueError("ORIGINAL_0002_NOT_MANIFEST_AUTHENTICATED")
    with zipfile.ZipFile(io.BytesIO(orig)) as z:
        rows = read_csv(z.read("official-1920-21-literal-results.csv"))
        local_manifest = json.loads(z.read("manifest.json"))
        # Independently verify 0002's own simple manifest by filename or path keys.
        if not any(v == sha(z.read("official-1920-21-literal-results.csv"))
                   for v in _all_string_values(local_manifest)):
            raise ValueError("ORIGINAL_0002_LITERAL_HASH_MISMATCH")
    return rows


def _all_string_values(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from _all_string_values(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _all_string_values(v)


def key(op, result, team, opp):
    return (" ".join(op.casefold().split()), result.upper(), int(team), int(opp))


def _materialize_source_checked(checkpoint, source_csv, checkpoint_sha, source_blob, output, *, accept=False):
    if checkpoint_sha != CHECKPOINT_0018 or source_blob != ORIGINAL_BLOB:
        raise ValueError("UNAPPROVED_INPUT_IDENTITY")
    source = Path(source_csv).read_bytes()
    if blob(source) != source_blob:
        raise ValueError("IMMUTABLE_SOURCE_BLOB_MISMATCH")
    srcrows = read_csv(source)
    if len(srcrows) != 2680 or len({r["source_game_id"] for r in srcrows}) != 2680:
        raise ValueError("INHERITED_SOURCE_POPULATION_MISMATCH")
    inherited = [r for r in srcrows if 1911 <= int(r["season_label"][:4]) < 1950]
    if len(inherited) != 469 or Counter(r["played_result"] for r in inherited) != Counter({"W": 215, "L": 254}):
        raise ValueError("INHERITED_POPULATION_OR_WL_DRIFT")
    if any(r["curated_game_type"] not in {"REGULAR_SEASON", "POSTSEASON", "CONFERENCE_TOURNAMENT"}
           for r in inherited):
        raise ValueError("INHERITED_GAME_TYPE_INVALID")
    members, manifest = zip_read(checkpoint, checkpoint_sha)
    if manifest.get("research_base_sha") != BASE or manifest.get("checkpoint_number") != 18:
        raise ValueError("CHECKPOINT_BASE_OR_STAGE_MISMATCH")
    if sha(members["inputs/original-checkpoints-0001-0006-transport.zip"]) != TRANSPORT_SHA:
        raise ValueError("ORIGINAL_TRANSPORT_IDENTITY_MISMATCH")
    preserved = read_csv(members["stage1/complete-mechanical-season-census.csv"])
    candidates = read_csv(members["stage1/retained-1920-21-provisional-candidates.csv"])
    residuals = read_csv(members["stage1/exact-remaining-source-blockers-and-acceptance-prerequisites.csv"])
    expected_seasons = {f"{y}-{y+1}" for y in range(1911, 1950)}
    if len(preserved) != 39 or {r["season_label"] for r in preserved} != expected_seasons:
        raise ValueError("INCOMPLETE_SEASON_CENSUS")
    for row in preserved:
        season = row["season_label"]
        if season in AGGREGATES:
            w, l = AGGREGATES[season]
            if (row["source_institutional_aggregate_wins"],
                row["source_institutional_aggregate_losses"],
                row["source_institutional_aggregate_games"],
                row["inherited_accepted_rows"]) != (str(w), str(l), str(w + l), "0"):
                raise ValueError("SOURCE_AGGREGATE_COUNT_MISMATCH:" + season)
        if season == "1920-1921" and (
            row["source_institutional_aggregate_wins"],
            row["source_institutional_aggregate_losses"],
            row["source_institutional_aggregate_games"],
            row["inherited_accepted_rows"],
            row["new_supplemental_provisional_rows"]
        ) != ("11", "3", "14", "1", "10"):
            raise ValueError("1920_21_RECORD_OR_PROVISIONAL_COUNT_MISMATCH")
        if season == "1915-1916" and row["activity"] != "NO_TEAM":
            raise ValueError("NO_TEAM_RECLASSIFICATION")
    byseason = defaultdict(list)
    for r in inherited:
        byseason[r["season_label"]].append(r)
    if sum(len(v) for v in byseason.values()) != 469 or len(byseason) != 34:
        raise ValueError("INVALID_INHERITED_SEASON_POPULATION")
    for r in preserved:
        s = r["season_label"]
        matching = byseason[s]
        if len(matching) != int(r["inherited_accepted_rows"]):
            raise ValueError("SEASON_INHERITED_COUNT_DRIFT:" + s)
        for result, field in (("W", "inherited_accepted_wins"), ("L", "inherited_accepted_losses")):
            if sum(x["played_result"] == result for x in matching) != int(r[field]):
                raise ValueError("SEASON_INHERITED_RESULT_DRIFT:" + s)
        if r["activity"] == "NO_TEAM" and (matching or s != "1915-1916"):
            raise ValueError("NO_TEAM_POPULATION_DRIFT")
    if len(candidates) != 10 or len({r["research_candidate_id"] for r in candidates}) != 10:
        raise ValueError("PROVISIONAL_CANDIDATE_COUNT_DRIFT")
    literal = original_literal_results(members["inputs/original-checkpoints-0001-0006-transport.zip"])
    if len(literal) != 11 or Counter(x["result"] for x in literal) != {"W": 9, "L": 2}:
        raise ValueError("HISTORICAL_DETAILED_SOURCE_DRIFT")
    literal_keys = Counter(key(x["literal_opponent"], x["result"], x["asu_score"], x["opponent_score"])
                           for x in literal)
    if literal_keys[key("ASC", "W", 42, 13)] != 1:
        raise ValueError("CONTESTED_ASC_ASSERTION_MISSING")
    provisional_keys = [key(x["source_literal_opponent"], x["source_result"], x["asu_score"], x["opponent_score"])
                        for x in candidates]
    inherited_keys = {key(x["source_opponent_label"], x["played_result"], x["team_score"], x["opponent_score"])
                      for x in inherited if x["season_label"] == "1920-1921"}
    if len(set(provisional_keys)) != 10 or set(provisional_keys) & inherited_keys:
        raise ValueError("PROVISIONAL_DUPLICATE_IN_SUPPLEMENTAL_OR_INHERITED")
    if Counter(provisional_keys) != literal_keys - Counter({key("ASC", "W", 42, 13): 1}):
        raise ValueError("CANDIDATES_NOT_EXACT_SOURCE_DETAILED_SUBSET")
    if Counter(x["source_result"] for x in candidates) != {"W": 8, "L": 2}:
        raise ValueError("PROVISIONAL_RESULT_DRIFT")
    if any(x["season_label"] != "1920-1921" or x["status"] != "PROVISIONAL_SUPPLEMENTAL_IDENTITY"
           or x["game_date"] or x["site_type"] != "UNKNOWN" for x in candidates):
        raise ValueError("PROVISIONAL_HISTORICAL_ASSERTION_DRIFT")
    issue_ids = {r["issue_id"] for r in residuals}
    required_issues = {"ASU-S1-1916-17-AGG", "ASU-S1-1917-18-AGG", "ASU-S1-1919-20-AGG",
                       "ASU-S1-1943-44-AGG", "ASU-S1-1920-21-RECORD", "ASU-S1-1920-21-IDENTITY",
                       "ASU-S1-1920-21-PROVISIONAL-INCLUSION"}
    if issue_ids != required_issues:
        raise ValueError("CHECKPOINT_BLOCKER_UNIVERSE_DRIFT")
    if len(inherited_keys) != 1 or key("Northern Arizona / Flagstaff", "W", 45, 13) not in inherited_keys:
        raise ValueError("INHERITED_NAU_IDENTITY_MISMATCH")
    # Do not infer ASC and NAU share a game, or insert ASC as an additional row.
    ledger = []
    for row in inherited:
        ledger.append({"research_game_id": row["source_game_id"], "season_label": row["season_label"],
                       "authority": "REUSE_INHERITED", "source_game_id": row["source_game_id"],
                       "source_opponent_label": row["source_opponent_label"], "played_result": row["played_result"],
                       "team_score": row["team_score"], "opponent_score": row["opponent_score"],
                       "game_type": row["curated_game_type"], "literal_raw_text": row["raw_text"],
                       "source_locator": row["source_page"]})
    if accept:
        for row in candidates:
            ledger.append({"research_game_id": row["research_candidate_id"], "season_label": row["season_label"],
                           "authority": "NEW_SUPPLEMENTAL_SOURCE_VERIFIED", "source_game_id": row["research_candidate_id"],
                           "source_opponent_label": row["source_literal_opponent"], "played_result": row["source_result"],
                           "team_score": row["asu_score"], "opponent_score": row["opponent_score"],
                           "game_type": "REGULAR_SEASON", "literal_raw_text": "", "source_locator":
                           "ASU All-Time Scores PDF page " + row["source_page"]})
    if len({x["research_game_id"] for x in ledger}) != len(ledger):
        raise ValueError("IDENTIFIED_GAME_ID_DUPLICATE")
    status = {"stage": "STAGE_1", "stage1_complete": False, "school_key": SCHOOL,
              "research_base_sha": BASE, "materialization_source_checkpoint_sha256": checkpoint_sha,
              "original_source_git_blob_sha": source_blob, "accepted_inherited": 469,
              "accepted_new_supplemental": 10 if accept else 0,
              "unaccepted_provisional_candidates": 0 if accept else 10,
              "contested_ASC_42_13_in_ledger": False, "unidentified_aggregate_games_not_in_ledger": 41,
              "unresolved_blocking_count": 2 + (0 if accept else 1),
              "result": "PARENT_MATERIALIZED__ACCOUNTING_AUTHORITY_REQUIRED"}
    census = []
    for item in preserved:
        season = item["season_label"]
        base_rows = byseason[season]
        extra_rows = [x for x in ledger if x["season_label"] == season and x["authority"] != "REUSE_INHERITED"]
        w = sum(x["played_result"] == "W" for x in base_rows) + sum(x["played_result"] == "W" for x in extra_rows)
        l = sum(x["played_result"] == "L" for x in base_rows) + sum(x["played_result"] == "L" for x in extra_rows)
        census.append({"season": season, "activity": item["activity"],
                       "accepted_inherited": len(base_rows), "accepted_supplemental": len(extra_rows),
                       "identified_w": w, "identified_l": l, "identified_games": w + l,
                       "official_w": item["source_institutional_aggregate_wins"],
                       "official_l": item["source_institutional_aggregate_losses"],
                       "official_games": item["source_institutional_aggregate_games"],
                       "census_class": item["census_class"]})
    residual_records = [{"blocker_id": r["issue_id"], "season": r["season"],
                         "class": r["issue_class"], "blocking": "YES", "detail": r["authority_state"]}
                        for r in residuals if r["issue_id"] != "ASU-S1-1920-21-PROVISIONAL-INCLUSION" or not accept]
    package = {"stage1-status.json": jb(status),
               "stage1-identified-game-ledger.csv": write_csv(ledger),
               "stage1-season-census.csv": write_csv(census),
               "stage1-residuals.csv": write_csv(residual_records),
               "source-explicit-aggregate-only-seasons.csv": write_csv([
                   {"season": s, "wins": w, "losses": l, "games": w+l, "identified": 0,
                    "research_status": "BOUNDED_ACCESSIBLE_SOURCES_EXHAUSTED"}
                   for s, (w,l) in AGGREGATES.items()]),
               "early-period-season-accounting.csv": write_csv([{"season": "1920-1921", "official_w": 11,
                   "official_l": 3, "official_games": 14, "identified_w": 9 if accept else 1,
                   "identified_l": 2 if accept else 0, "identified_games": 11 if accept else 1,
                   "arithmetic_not_game_identities": "YES"}]),
               "separate-source-questions.csv": members["stage1/unaligned-and-separate-research-issues-preserved.csv"],
               "provisional-candidates-source.csv": members["stage1/retained-1920-21-provisional-candidates.csv"],
               "original-recovery-checkpoint-0018.zip": Path(checkpoint).read_bytes(),
               "original-research-base-source-games.csv": source,
               "materialization-proof.json": jb({"input_checkpoint_sha": checkpoint_sha,
                   "research_base_sha": BASE, "inherited_git_blob_sha": source_blob,
                   "inherited_count": 469, "provisional_count": 10,
                   "source_literal_line_count": len(literal), "unique_candidate_identity_keys": 10,
                   "candidate_acceptance_performed": accept,
                   "contested_source_representation_status": "UNRESOLVED_WITHHELD", "no_anonymous_games": True})}
    result = write_zip(output, package, {"schema_version": 1, "kind": "EXPANSION_STAGE1_PARENT_V1",
               "school_key": SCHOOL, "research_base_sha": BASE})
    return {"status": "PARENT_MATERIALIZED", "sha256": result, "identified_count": len(ledger),
            "inherited": 469, "new_supplemental": 10 if accept else 0, "blocking": len(residual_records)}


# Only a representation adapter is new: current-main generic closeout remains the
# sole accounting auditor, successor author, and independent verifier.
GENERIC_CONCLUSION = (
    "SIMPLE_UNION_RECONCILIATION_REJECTED. Aggregate structures cannot be "
    "converted into anonymous or inferred game rows. String-similar opponent "
    "labels are review triggers only, not same-game authority."
)


def materialize(checkpoint, source_csv, checkpoint_sha, source_blob, output, *, accept=False):
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        provisional = Path(tmp) / "source-checked-parent.zip"
        result = _materialize_source_checked(
            checkpoint, source_csv, checkpoint_sha, source_blob, provisional, accept=accept
        )
        if not accept:
            raise ValueError("ONLY_VERIFIED_AND_OWNER_PERMITTED_CANDIDATES_CAN_CLOSE_STAGE1")
        members, old_manifest = zip_read(provisional, result["sha256"])
        ledger = read_csv(members["stage1-identified-game-ledger.csv"])
        orig = original_literal_results(
            zip_read(checkpoint, checkpoint_sha)[0]["inputs/original-checkpoints-0001-0006-transport.zip"]
        )
        literal_candidates = {
            key(r["literal_opponent"], r["result"], r["asu_score"], r["opponent_score"]): r
            for r in orig if r["literal_opponent"] != "ASC"
        }
        if len(literal_candidates) != 10:
            raise ValueError("LITERAL_SOURCE_UNIQUENESS_VIOLATION")
        for row in ledger:
            if row["authority"] != "NEW_SUPPLEMENTAL_SOURCE_VERIFIED":
                continue
            literal_key = key(row["source_opponent_label"], row["played_result"],
                              row["team_score"], row["opponent_score"])
            source = literal_candidates.get(literal_key)
            if not source:
                raise ValueError("MISSING_ACCEPTED_LITERAL_PROVENANCE")
            row["literal_raw_text"] = json.dumps(source, sort_keys=True, separators=(",", ":"))
        members["stage1-identified-game-ledger.csv"] = write_csv(ledger)
        census = read_csv(members["stage1-season-census.csv"])
        if (len(census) != 39 or
            next(x for x in census if x["season"] == "1920-1921")["identified_games"] != "11"):
            raise ValueError("INCOMPLETE_1920_21_CENSUS")
        # Preserve all six distinct source blockers and the provisional-acceptance
        # precondition in their original manifest-hashed 0018 member. The generic
        # tool expects two coherent accounting *families*, not six individual rows.
        members["original-six-source-blockers-and-provisional-precondition.csv"] = members["original-recovery-checkpoint-0018.zip"] and zip_read(
            checkpoint, checkpoint_sha
        )[0]["stage1/exact-remaining-source-blockers-and-acceptance-prerequisites.csv"]
        original_residuals = read_csv(members["stage1-residuals.csv"])
        if len(original_residuals) != 6:
            raise ValueError("ORIGINAL_SIX_BLOCKER_POPULATION_MISMATCH")
        merged = [
            {"blocker_id": "ASU-EXACT-4-SEASON-AGGREGATE-FAMILY",
             "season": "1916-17;1917-18;1919-20;1943-44",
             "residual_class": "EARLY_SOURCE_EXPLICIT_AGGREGATE_ONLY_GAME_IDENTITIES_UNKNOWN",
             "blocking": "YES",
             "detail": "Four owner-authorized season records, 41 unidentified games; exact original source blockers embedded unchanged. The 1943-44 case is a narrowly owner-approved wartime exception.",
             "next_evidence_family": "OWNER_APPROVED_ACCOUNTING_CLOSEOUT_ONLY"},
            {"blocker_id": "ASU-EXACT-1920-21-ACCOUNTING-AND-CONTESTED-SOURCE",
             "season": "1920-21",
             "residual_class": "EARLY_DETAILED_VS_OVERALL_CLUB_ACCOUNTING_CONTRADICTION",
             "blocking": "YES",
             "detail": "Official 11-3 vs accepted detailed 9-2 is arithmetic-only; separately recorded ASC W42-13 assertion is TERMINAL CONTESTED, not an accepted game and not identified with inherited NAU W45-13. Original six blocker rows preserved.",
             "next_evidence_family": "OWNER_APPROVED_ACCOUNTING_CLOSEOUT_ONLY"},
        ]
        members["stage1-residuals.csv"] = write_csv(merged)
        records = []
        for season, (wins, losses) in sorted(AGGREGATES.items()):
            old = next(x for x in census if x["season"] == season)
            if (old["identified_games"], old["identified_w"], old["identified_l"]) != ("0", "0", "0"):
                raise ValueError("AGGREGATE_ONLY_SEASON_HAS_IDENTIFIED_GAMES")
            records.append({
                "season": season, "official_w": wins, "official_l": losses,
                "official_games": wins + losses, "individual_game_rows_in_guide": 0,
                "source_note": "ASU official historical season aggregate; game identities not recoverable in bounded research. "
                               + ("Explicit narrow wartime exception approved for 1943-44. " if season == "1943-1944" else "")
                               + "No anonymous rows or aggregate W/L allocations."
            })
        members["source-explicit-aggregate-only-seasons.csv"] = write_csv(records)
        account = [{
            "season": "1920-1921", "source_status": "DETAILED", "official_w": 11,
            "official_l": 3, "official_games": 14, "identified_w": 9,
            "identified_l": 2, "identified_rows": 11,
            "source_note": "1920-21 accepted detailed 9-2, official 11-3; ASC W42-13 is a separate contested source representation, not another accepted game."
        }]
        members["early-period-season-accounting.csv"] = write_csv(account)
        members["early-reconciliation-summary.json"] = jb({
            "official_season_aggregate": {"wins": 11, "losses": 3, "games": 14},
            "chronological_detail": {"wins": 9, "losses": 2, "rows": 11},
            "club_high_school_aggregate": None,
            "simple_union_implied_overlap_games": None,
            "conclusion": GENERIC_CONCLUSION,
            "direct_candidate_result_conflicts": [{
                "season": "1920-21", "literal_source_assertion": "ASC W42-13",
                "inherited_original_source_game_id": "ASU-STG2-PRE1950-1920-21-001",
                "inherited_source_assertion": "Northern Arizona / Flagstaff W45-13",
                "identity_relationship": "NOT_ESTABLISHED; neither duplicate nor additional game inferred",
                "terminal_disposition": "TERMINAL_CONTESTED_SOURCE_REPRESENTATION__NO_ROW_ADDED"
            }],
            "separate_1917_18_contemporary_15_4": "UNALIGNED; NOT A NINETEENTH GAME",
            "separate_1943_44_championship": "UNRESOLVED OUTSIDE STAGE1 GAME UNIVERSE",
        })
        members["terminal-contested-source-representation.json"] = jb({
            "season": "1920-21", "classification": "TERMINAL_CONTESTED_SOURCE_REPRESENTATION",
            "source_assertion": {"opponent": "ASC", "result": "W", "team_score": 42, "opponent_score": 13},
            "inherited_source_assertion": {"source_game_id": "ASU-STG2-PRE1950-1920-21-001",
                                            "opponent": "Northern Arizona / Flagstaff",
                                            "result": "W", "team_score": 45, "opponent_score": 13},
            "same_game_identity_proven": False, "additional_game_identity_proven": False,
            "new_rows_created_from_ASC_assertion": 0,
            "reopen_only_with_independent_direct_game_evidence": True,
            "owner_approval": "Accepted Arizona State historical-accounting resolution; captured in conversation; exact GitHub provenance recorded in owner authority case."
        })
        status = json.loads(members["stage1-status.json"])
        status.pop("unresolved_blocking_count", None)
        status.update({
            "state": "BLOCKED_OWNER_APPROVED_ACCOUNTING_CLOSEOUT_REQUIRES_REGISTRY",
            "status": "BLOCKED", "blocking_residual_count": 2,
            "original_evidenced_source_blockers": 6,
            "anonymous_games_manufactured": 0,
            "early_archive_pass": {"new_game_identities_recovered": 0,
                                   "source_explicit_aggregate_only_games": 41},
            "early_spalding_pass": {"new_game_identities_recovered": 0},
            "candidate_acceptance": "VERIFIED_EXACT_LITERAL_AND_DUPLICATE_CHECKS",
            "contested_representation": "TERMINAL_CONTESTED_SOURCE_REPRESENTATION_NOT_RESOLVED",
        })
        members["stage1-status.json"] = jb(status)
        # Exact working evidence retained from all predecessors, plus the pinned
        # immutable Research-base source. Never silently change original member bytes.
        members.pop("manifest.json", None)
        final_hash = write_zip(output, members, {
            "schema_version": 1, "school_key": SCHOOL, "research_base_sha": BASE,
            "kind": "ASU_SOURCE_PINNED_GENERIC_EARLY_ACCOUNTING_PARENT",
            "original_recovery_checkpoint_sha256": checkpoint_sha,
            "original_source_git_blob_sha": source_blob,
            "original_evidenced_blocker_count": 6,
            "generic_accounting_blocker_family_count": 2,
        }, modern=True)
        return {"status": "BLOCKED_PARENT_MATERIALIZED", "sha256": final_hash,
                "inherited_identified": 469, "accepted_supplemental": 10,
                "contested_assertion_new_rows": 0, "aggregate_unidentified": 41,
                "owner_registry_required": True}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", type=Path)
    parser.add_argument("source", type=Path)
    parser.add_argument("--checkpoint-sha", required=True)
    parser.add_argument("--source-blob", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        result = materialize(args.checkpoint, args.source, args.checkpoint_sha,
                             args.source_blob, args.output, accept=True)
    except (ValueError, KeyError, TypeError, OSError, zipfile.BadZipFile) as e:
        print(jb({"status": "BLOCKED", "error": str(e)}).decode(), end="")
        return 2
    print(jb(result).decode(), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
