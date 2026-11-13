#!/usr/bin/env python3
"""Fail-closed v2 All-History expansion Stage 1 parent/terminal accounting capability.

No source-game, historical conclusion, protected-main row, or authority registry is
modified. A terminal closeout requires a *separate* exact-parent owner authority in
protected-main data/reference/expansion-stage1-accounting-authorities.json.

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


def write_zip(path, members, metadata):
    if "manifest.json" in members:
        raise ValueError("MANIFEST_RESERVED")
    manifest = {**metadata, "member_sha256": {k: sha(v) for k, v in sorted(members.items())},
                "member_bytes": {k: len(v) for k, v in sorted(members.items())}}
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


def materialize(checkpoint, source_csv, checkpoint_sha, source_blob, output, *, accept=False):
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
              "unresolved_blocking_count": 6 + (0 if accept else 1),
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


def lookup(registry_path, school):
    path = Path(registry_path)
    if not path.is_file():
        return None
    data = json.loads(path.read_text())
    if data.get("schema_version") != 1 or data.get("authority_type") != "OWNER_APPROVED_EXPANSION_STAGE1_ACCOUNTING":
        raise ValueError("REGISTRY_SCHEMA_MISMATCH")
    matches = [c for c in data.get("cases", []) if c.get("school_key") == school]
    if len(matches) > 1:
        raise ValueError("DUPLICATE_OWNER_AUTHORITY")
    return matches[0] if matches else None


def protected_registry_authentication(registry, main_sha):
    """Prove that authority bytes are from the exact remote protected-main Git object."""
    if not re.fullmatch(r"[0-9a-f]{40}", main_sha or ""):
        raise ValueError("EXPECTED_PROTECTED_MAIN_SHA_REQUIRED")
    if Path(registry).resolve() != REGISTRY.resolve():
        raise ValueError("REGISTRY_OVERRIDE_NOT_ALLOWED_FOR_PRODUCTION")
    root = Path(__file__).resolve().parents[1]
    try:
        actual_main = subprocess.check_output(
            ["git", "-C", str(root), "rev-parse", "refs/remotes/origin/main"],
            stderr=subprocess.DEVNULL, text=True).strip()
        committed = subprocess.check_output(
            ["git", "-C", str(root), "show", f"{main_sha}:{REGISTRY_PATH}"],
            stderr=subprocess.DEVNULL)
    except (OSError, subprocess.CalledProcessError):
        raise ValueError("PROTECTED_MAIN_REGISTRY_GIT_OBJECT_UNAVAILABLE")
    if actual_main != main_sha:
        raise ValueError("PROTECTED_MAIN_SHA_CHANGED")
    if not REGISTRY.is_file() or REGISTRY.read_bytes() != committed:
        raise ValueError("AUTHORITY_REGISTRY_BYTES_NOT_PROTECTED_MAIN")


def audit(parent, parent_sha, registry=REGISTRY, main_sha=None):
    members, manifest = zip_read(parent, parent_sha)
    defects = []
    if manifest.get("kind") != "EXPANSION_STAGE1_PARENT_V1" or manifest.get("school_key") != SCHOOL:
        defects.append("INVALID_PARENT_KIND_OR_SCHOOL")
    status = json.loads(members["stage1-status.json"])
    proof = json.loads(members["materialization-proof.json"])
    if status.get("stage1_complete") is not False or status.get("research_base_sha") != BASE:
        defects.append("INVALID_PARENT_STAGE_OR_BASE")
    if status.get("accepted_inherited") != 469 or status.get("accepted_new_supplemental") != 10:
        defects.append("CANDIDATE_ACCEPTANCE_REQUIRED")
    if proof.get("candidate_acceptance_performed") is not True or proof.get("contested_source_representation_status") != "UNRESOLVED_WITHHELD":
        defects.append("UNVERIFIED_CANDIDATE_OR_CONTESTED_STATUS")
    ledger = read_csv(members["stage1-identified-game-ledger.csv"])
    census = read_csv(members["stage1-season-census.csv"])
    residuals = read_csv(members["stage1-residuals.csv"])
    expected_ids = {"ASU-S1-1916-17-AGG", "ASU-S1-1917-18-AGG", "ASU-S1-1919-20-AGG",
                    "ASU-S1-1943-44-AGG", "ASU-S1-1920-21-RECORD", "ASU-S1-1920-21-IDENTITY"}
    if len(ledger) != 479 or len({r["research_game_id"] for r in ledger}) != len(ledger):
        defects.append("GAME_LEDGER_POPULATION_INVALID")
    if len(census) != 39 or len({r["season"] for r in census}) != 39:
        defects.append("SEASON_CENSUS_INVALID")
    if {r["blocker_id"] for r in residuals} != expected_ids or len(residuals) != 6 or any(r["blocking"] != "YES" for r in residuals):
        defects.append("BLOCKING_POPULATION_UNEXPECTED")
    if any(r["research_game_id"].upper().startswith(("ANONYMOUS", "PLACEHOLDER")) for r in ledger):
        defects.append("FABRICATED_GAME_ROW")
    literal = read_csv(members["original-research-base-source-games.csv"])
    legacy = [r for r in literal if int(r["season_label"][:4]) < 1950]
    if blob(members["original-research-base-source-games.csv"]) != ORIGINAL_BLOB or len(legacy) != 469:
        defects.append("INHERITED_SOURCE_DRIFT")
    if {r["research_game_id"] for r in ledger if r["authority"] == "REUSE_INHERITED"} != {r["source_game_id"] for r in legacy}:
        defects.append("INHERITED_GAME_IDS_CHANGED")
    if any(r["source_opponent_label"] == "ASC" and r["team_score"] == "42" and r["opponent_score"] == "13"
           for r in ledger if r["season_label"] == "1920-1921"):
        defects.append("DISPUTED_ASC_ROW_INCLUDED")
    # The entire parent must be reproducible from exact embedded evidence, not
    # merely count-consistent or backed by a self-authored manifest/registry.
    import tempfile
    with tempfile.TemporaryDirectory() as root:
        checkpoint = Path(root) / "checkpoint.zip"
        source = Path(root) / "source.csv"
        expected = Path(root) / "replayed-parent.zip"
        checkpoint.write_bytes(members["original-recovery-checkpoint-0018.zip"])
        source.write_bytes(members["original-research-base-source-games.csv"])
        try:
            materialize(checkpoint, source, CHECKPOINT_0018, ORIGINAL_BLOB, expected,
                        accept=status.get("accepted_new_supplemental") == 10)
            if expected.read_bytes() != Path(parent).read_bytes():
                defects.append("PARENT_NOT_EXACT_DETERMINISTIC_REPLAY")
        except (ValueError, KeyError, TypeError, OSError) as exc:
            defects.append("PARENT_REPLAY_FAILED:" + str(exc))
    if main_sha is not None:
        protected_registry_authentication(registry, main_sha)
    elif Path(registry).resolve() == REGISTRY.resolve():
        defects.append("PROTECTED_MAIN_AUTHENTICATION_REQUIRED")
    authority = lookup(registry, SCHOOL)
    if authority is None:
        defects.append("NO_EXACT_OWNER_AUTHORITY")
    else:
        if authority.get("parent_sha256") != parent_sha or authority.get("research_base_sha") != BASE or \
           authority.get("identified_ledger_sha256") != sha(members["stage1-identified-game-ledger.csv"]) or \
           authority.get("census_sha256") != sha(members["stage1-season-census.csv"]) or \
           not str(authority.get("owner_disposition", "")).startswith("https://github.com/"):
            defects.append("EXACT_AUTHORITY_BINDING_MISMATCH")
        allowed = {x.get("season"): x for x in authority.get("aggregate_only_seasons", [])}
        if set(allowed) != set(AGGREGATES):
            defects.append("AGGREGATE_AUTHORITY_POPULATION_MISMATCH")
        for season, (w,l) in AGGREGATES.items():
            if allowed.get(season, {}).get("institutional_record") != {"wins": w, "losses": l, "games": w+l}:
                defects.append("AGGREGATE_AUTHORITY_RECORD_MISMATCH:" + season)
        if allowed.get("1943-1944", {}).get("exception_kind") != "EXACT_WARTIME_NONFOUNDING_1943_44":
            defects.append("WARTIME_EXCEPTION_NOT_EXPLICIT")
        if authority.get("accounting_contradiction") != {"season": "1920-1921", "official": {"wins": 11, "losses": 3, "games": 14},
            "identified": {"wins": 9, "losses": 2, "games": 11}, "arithmetic_only_difference": {"wins": 2, "losses": 1, "games": 3}}:
            defects.append("ACCOUNTING_CONTRADICTION_AUTHORITY_MISMATCH")
        if authority.get("contested_representation") != {"season": "1920-1921", "literal_assertion": "ASC W42-13",
              "inherited_game_id": "ASU-STG2-PRE1950-1920-21-001", "inherited_result": "Northern Arizona W45-13",
              "disposition": "TERMINAL_CONTESTED_SOURCE_REPRESENTATION__NOT_IDENTITY_RESOLVED__NO_ROW_ADDED"}:
            defects.append("CONTESTED_REPRESENTATION_OWNER_AUTHORITY_MISSING")
    return {"status": "ELIGIBLE_FOR_EXPANSION_STAGE1_ACCOUNTING_CLOSEOUT" if not defects else "BLOCKED",
            "defects": defects, "parent_sha256": parent_sha, "research_base_sha": BASE,
            "stage1_complete": False, "included_game_rows": len(ledger),
            "expected_terminal_residuals": sorted(expected_ids)}


def closeout(parent, report_path, parent_sha, audit_sha, registry, output, main_sha=None):
    report_raw = Path(report_path).read_bytes()
    if sha(report_raw) != audit_sha or json.loads(report_raw) != audit(parent, parent_sha, registry, main_sha):
        raise ValueError("AUDIT_HASH_OR_FRESHNESS_MISMATCH")
    report = json.loads(report_raw)
    if report["status"] != "ELIGIBLE_FOR_EXPANSION_STAGE1_ACCOUNTING_CLOSEOUT":
        raise ValueError("CLOSEOUT_NOT_AUTHORIZED")
    old, manifest = zip_read(parent, parent_sha)
    terminal = {
        "ASU-S1-1916-17-AGG": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
        "ASU-S1-1917-18-AGG": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
        "ASU-S1-1919-20-AGG": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
        "ASU-S1-1943-44-AGG": "WARTIME_INSTITUTIONAL_AGGREGATE_COVERAGE_GAP",
        "ASU-S1-1920-21-RECORD": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
        "ASU-S1-1920-21-IDENTITY": "CONTESTED_SOURCE_REPRESENTATION_PRESERVED",
    }
    original_residuals = read_csv(old["stage1-residuals.csv"])
    revised = []
    for row in original_residuals:
        if row["blocker_id"] not in terminal:
            raise ValueError("UNEXPECTED_BLOCKER_AT_CLOSEOUT")
        revised.append({**row, "class": terminal[row["blocker_id"]], "blocking": "NO",
                        "detail": "EXACT_OWNER_AUTHORIZED_TERMINAL_DEBT; REOPEN_ONLY_WITH_DIRECT_SOURCE_EVIDENCE"})
    status = json.loads(old["stage1-status.json"])
    status.update({"status": "CLOSEOUT_CANDIDATE_AWAITING_INDEPENDENT_VERIFICATION",
                   "stage1_complete": False, "blocking_residual_count": 0,
                   "closeout_requires_independent_verification": True})
    additions = {"terminal-accounting-records.json": jb({"parent_sha256": parent_sha, "audit_sha256": audit_sha,
         "terminal_classifications": terminal, "unidentified_season_aggregate_games": 41,
         "contested_source_still_unresolved": True, "source_record_disagreement_preserved": True,
         "inherited_game_rows_untouched": True}),
         "stage1-closeout-status.json": jb(status),
         "stage1-closeout-residuals.csv": write_csv(revised)}
    if any(name in old for name in additions):
        raise ValueError("CLOSEOUT_MEMBER_COLLISION")
    result = write_zip(output, {**{k: v for k,v in old.items() if k != "manifest.json"}, **additions},
                       {"kind": "EXPANSION_STAGE1_ACCOUNTING_CLOSEOUT_CANDIDATE_V1",
                        "parent_sha256": parent_sha, "audit_sha256": audit_sha,
                        "research_base_sha": BASE, "school_key": SCHOOL})
    return {"status": "CLOSEOUT_CANDIDATE_ONLY", "sha256": result, "stage1_complete": False}


def verify_closeout(parent, successor, audit_path, parent_sha, successor_sha, audit_sha, registry, main_sha=None):
    if sha(Path(audit_path).read_bytes()) != audit_sha:
        raise ValueError("AUDIT_HASH_MISMATCH")
    expected_report = audit(parent, parent_sha, registry, main_sha)
    if expected_report != json.loads(Path(audit_path).read_bytes()) or expected_report["status"] != "ELIGIBLE_FOR_EXPANSION_STAGE1_ACCOUNTING_CLOSEOUT":
        raise ValueError("FRESH_AUDIT_NOT_ELIGIBLE")
    old, _ = zip_read(parent, parent_sha)
    new, meta = zip_read(successor, successor_sha)
    if meta.get("parent_sha256") != parent_sha or meta.get("audit_sha256") != audit_sha:
        raise ValueError("CLOSEOUT_BOUND_AUTHORITY_MISMATCH")
    for key, data in old.items():
        if key != "manifest.json" and new.get(key) != data:
            raise ValueError("HISTORICAL_PARENT_MEMBER_DRIFT:" + key)
    # Bit-for-bit determinism: recreate the expected closeout in a temporary file.
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        candidate = Path(d) / "expected.zip"
        closeout(parent, audit_path, parent_sha, audit_sha, registry, candidate, main_sha)
        if candidate.read_bytes() != Path(successor).read_bytes():
            raise ValueError("CLOSEOUT_CONTENT_MISMATCH")
    return {"status": "VERIFIED_EXPANSION_STAGE1_ACCOUNTING_CLOSEOUT_CANDIDATE",
            "closeout_sha256": successor_sha, "stage1_complete": False,
            "no_historical_game_mutation": True}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("materialize")
    p.add_argument("checkpoint", type=Path)
    p.add_argument("source", type=Path)
    p.add_argument("--checkpoint-sha", required=True)
    p.add_argument("--source-blob", required=True)
    p.add_argument("--output", required=True, type=Path)
    p.add_argument("--accept-verified-candidates", action="store_true")
    p = sub.add_parser("audit")
    p.add_argument("parent", type=Path); p.add_argument("--parent-sha", required=True)
    p.add_argument("--registry", type=Path, default=REGISTRY); p.add_argument("--main-sha", required=True); p.add_argument("--output", type=Path)
    p = sub.add_parser("closeout")
    p.add_argument("parent", type=Path); p.add_argument("audit", type=Path)
    p.add_argument("--parent-sha", required=True); p.add_argument("--audit-sha", required=True)
    p.add_argument("--registry", type=Path, default=REGISTRY); p.add_argument("--main-sha", required=True); p.add_argument("--output", type=Path, required=True)
    p = sub.add_parser("verify-closeout")
    p.add_argument("parent", type=Path); p.add_argument("successor", type=Path); p.add_argument("audit", type=Path)
    p.add_argument("--parent-sha", required=True); p.add_argument("--successor-sha", required=True)
    p.add_argument("--audit-sha", required=True); p.add_argument("--registry", type=Path, default=REGISTRY); p.add_argument("--main-sha", required=True)
    a = ap.parse_args(argv)
    try:
        if a.command == "materialize":
            out = materialize(a.checkpoint, a.source, a.checkpoint_sha, a.source_blob, a.output,
                              accept=a.accept_verified_candidates)
        elif a.command == "audit":
            out = audit(a.parent, a.parent_sha, a.registry, a.main_sha)
            if a.output: a.output.write_bytes(jb(out))
        elif a.command == "closeout":
            out = closeout(a.parent, a.audit, a.parent_sha, a.audit_sha, a.registry, a.output, a.main_sha)
        else:
            out = verify_closeout(a.parent, a.successor, a.audit, a.parent_sha,
                                  a.successor_sha, a.audit_sha, a.registry, a.main_sha)
    except (ValueError, KeyError, IndexError, TypeError, OSError, zipfile.BadZipFile) as exc:
        print(jb({"status": "BLOCKED", "error": str(exc)}).decode(), end="")
        return 2
    print(jb(out).decode(), end="")
    return 0 if out.get("status") not in {"BLOCKED"} else 2


if __name__ == "__main__":
    sys.exit(main())
