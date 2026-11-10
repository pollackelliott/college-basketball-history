#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

SITE_GAMES = [
    "CBBG-0008338",
    "CBBG-0019677",
    "CBBG-0020092",
    "CBBG-0031705",
    "CBBG-0034875",
    "CBBG-0035026",
    "CBBG-0035260",
    "CBBG-0039580",
    "CBBG-0042461",
    "CBBG-0051583",
    "CBBG-0053518",
    "CBBG-0058536",
    "CBBG-0058602",
]
SCHOOL = "richmond"
CONTROL_COMMIT = "41fb2d14ef35eb751a59012002ddd911c9e9f97e"
CHECKPOINT_DIR = ".remote-implementation/checkpoints/richmond/richmond-stage2-proposal-0001"
EXPECTED = {
    "main": "802006f8f30ec9fc2e7b7a528d482bd343dc8e3b",
    "target": "2350ec65bbc6bf066dff29c356b6855e1d9fc980",
    "candidate": "9d8822325f2d049cbf23a828e7346a835e6a0a7b",
    "freeze": "170bacc15fd117aacef9e9303d2bf88c46daf931c20b8c11b5c7447c4c90c916",
    "semantic": "383dfc3cf1d4411534fa0f17de2252114392eed43791a2e4a9fdccc7bc770f9d",
    "universe": "f10f646c6a808f5d5ff77b1ecf3f8b4626d6bcecd6f0055d5c127b7e238a23a8",
    "map": "352232cf27ba3fa88f0214ac8ee49efc0897756a6f1a53994033cd349a8be218",
}


def run(cmd, *, cwd: Path, env=None, check=True):
    cp = subprocess.run(
        cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, check=False
    )
    if check and cp.returncode:
        raise RuntimeError("$ " + " ".join(map(str, cmd)) + "\n" + cp.stdout[-12000:])
    return cp


def git_show(repo: Path, commit: str, path: str) -> bytes:
    cp = subprocess.run(
        ["git", "show", f"{commit}:{path}"], cwd=repo,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False
    )
    if cp.returncode:
        raise RuntimeError(cp.stderr.decode("utf-8", errors="replace"))
    return cp.stdout


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def canonical_map(repo: Path) -> dict[str, dict[str, str]]:
    return {
        row.get("canonical_game_id", "").strip(): row
        for row in read_csv(repo / "data/canonical/games.csv")
        if row.get("canonical_game_id", "").strip()
    }


def primitive_gaps(row: dict[str, str]) -> list[str]:
    gaps = []
    if not (row.get("venue_key", "").strip() or row.get("venue_id", "").strip()):
        gaps.append("venue")
    city = row.get("site_city", "").strip()
    state = row.get("site_state", "").strip()
    if not city and not state:
        gaps.append("location")
    elif bool(city) != bool(state):
        gaps.append("partial_location")
    return sorted(gaps)


def state(row: dict[str, str] | None) -> dict[str, Any]:
    if row is None:
        return {"missing": True}
    return {
        "site_type": row.get("site_type", "").strip(),
        "venue_key": row.get("venue_key", "").strip(),
        "venue_id": row.get("venue_id", "").strip(),
        "city": row.get("site_city", "").strip(),
        "state": row.get("site_state", "").strip(),
        "game_date": row.get("game_date", "").strip(),
        "game_type": row.get("game_type", "").strip(),
        "team_a_key": row.get("team_a_key", "").strip(),
        "team_b_key": row.get("team_b_key", "").strip(),
        "gaps": primitive_gaps(row),
    }


def snapshot(repo: Path) -> dict[str, dict[str, Any]]:
    games = canonical_map(repo)
    return {gid: state(games.get(gid)) for gid in SITE_GAMES}


def assertions_by_game(repo: Path) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(repo / "data/evidence/game-assertions.csv"):
        gid = row.get("canonical_game_id", "").strip()
        if gid in SITE_GAMES:
            result[gid].append(row)
    return result


def target_assertion_summary(repo: Path) -> dict[str, list[dict[str, str]]]:
    result = {}
    source_by_id = {
        row.get("source_game_id", "").strip(): row
        for row in read_csv(repo / f"schools/{SCHOOL}/source-games.csv")
        if row.get("source_game_id", "").strip()
    }
    for gid, rows in assertions_by_game(repo).items():
        vals = []
        for row in rows:
            if row.get("source_program_key", "").strip() != SCHOOL:
                continue
            sid = row.get("source_game_id", "").strip()
            src = source_by_id.get(sid, {})
            vals.append({
                "source_game_id": sid,
                "game_date": row.get("game_date", "").strip(),
                "match_method": row.get("match_method", "").strip(),
                "curated_site_type": row.get("curated_site_type", "").strip(),
                "curated_venue_name": row.get("curated_venue_name", "").strip(),
                "city": row.get("city", "").strip(),
                "state": row.get("state", "").strip(),
                "source_research_status": src.get("research_status", "").strip(),
                "source_site_research_status": src.get("site_research_status", "").strip(),
                "source_site_research_basis": src.get("site_research_basis", "").strip(),
                "source_raw_text": src.get("raw_text", "").strip(),
            })
        result[gid] = vals
    return result


def classify_transition(pre: dict[str, Any], post: dict[str, Any], origin: dict[str, Any]) -> str:
    pg = set(pre.get("gaps", []))
    qg = set(post.get("gaps", []))
    identity_changed = any(
        pre.get(k) != post.get(k) for k in ("team_a_key", "team_b_key", "game_date")
    )
    if identity_changed:
        return "GAP_CHANGED_BY_IDENTITY_RECONCILIATION"
    if pg == qg:
        return "UNCHANGED_GAP_SET"
    if qg < pg:
        if not qg:
            return "GAP_ELIMINATED_BY_SUPPORTED_ENRICHMENT" if origin.get("supported") else "GAP_CHANGED_BY_UNSUPPORTED_OR_SUSPICIOUS_MUTATION"
        return "GAP_REDUCED_BY_SUPPORTED_ENRICHMENT" if origin.get("supported") else "GAP_CHANGED_BY_UNSUPPORTED_OR_SUSPICIOUS_MUTATION"
    if origin.get("supported"):
        return "OTHER"
    return "GAP_CHANGED_BY_UNSUPPORTED_OR_SUSPICIOUS_MUTATION"


def explain_origin(
    pre: dict[str, Any],
    post_ingest: dict[str, Any],
    post_recon: dict[str, Any],
    target_assertions: list[dict[str, str]],
    approved: dict[str, Any],
    gid: str,
) -> dict[str, Any]:
    changes = []
    supported = True
    for field, state_key in [
        ("location", ("city", "state")),
        ("venue", ("venue_key", "venue_id")),
    ]:
        before = tuple(pre.get(k, "") for k in state_key)
        after_ingest = tuple(post_ingest.get(k, "") for k in state_key)
        after_recon = tuple(post_recon.get(k, "") for k in state_key)
        if before != after_ingest:
            matching = []
            for a in target_assertions:
                if field == "location":
                    if (a.get("city", ""), a.get("state", "")) == after_ingest:
                        matching.append(a)
                else:
                    if a.get("curated_venue_name", ""):
                        matching.append(a)
            if matching:
                changes.append({
                    "field": field,
                    "phase": "INGESTION_CANONICAL_ENRICHMENT",
                    "permanent_path": "tools/ingest_school.py -> apply_canonical_enrichment_candidates()",
                    "originating_target_assertions": matching,
                    "accepted_authority": True,
                    "historical_choice_made": False,
                })
            else:
                changes.append({
                    "field": field,
                    "phase": "INGESTION_CANONICAL_ENRICHMENT",
                    "permanent_path": "tools/ingest_school.py -> apply_canonical_enrichment_candidates()",
                    "originating_target_assertions": target_assertions,
                    "accepted_authority": False,
                    "historical_choice_made": False,
                    "explanation": "No matching target assertion value found; requires scrutiny.",
                })
                supported = False
        if after_ingest != after_recon:
            decisions = [
                item for item in approved.get("decisions", [])
                if item.get("canonical_game_id", "") == gid
            ]
            changes.append({
                "field": field,
                "phase": "GENERIC_RECONCILIATION",
                "permanent_path": "tools/onboarding_plan.py -> apply_reconciliation_decisions()",
                "decisions": decisions,
                "accepted_authority": bool(decisions),
                "historical_choice_made": bool(decisions),
            })
            if not decisions:
                supported = False
    return {"supported": supported, "changes": changes}


def repo_provenance_census(repo: Path) -> dict[str, Any]:
    canonical = canonical_map(repo)
    grouped: dict[str, set[str]] = defaultdict(set)
    rows = []
    marker = "Sealed non-substantive reciprocal-only site-gap provenance;"
    for row in read_csv(repo / "data/reconciliation/discrepancies.csv"):
        if marker not in row.get("notes", ""):
            continue
        gid = row.get("canonical_game_id", "").strip()
        field = row.get("field_name", "").strip()
        grouped[gid].add(field)
        rows.append({
            "discrepancy_id": row.get("discrepancy_id", "").strip(),
            "canonical_game_id": gid,
            "field_name": field,
            "source_program_key": row.get("source_a_program_key", "").strip(),
            "status": row.get("status", "").strip(),
            "resolution_basis": row.get("resolution_basis", "").strip(),
        })
    combos = Counter(tuple(sorted(fields)) for fields in grouped.values())
    mismatch = []
    for gid, fields in sorted(grouped.items()):
        current = set(primitive_gaps(canonical.get(gid, {})))
        if "partial_location" in current:
            current.remove("partial_location")
            current.add("location")
        if fields != current:
            mismatch.append({
                "canonical_game_id": gid,
                "provenance_fields": sorted(fields),
                "current_primitive_gaps": sorted(current),
            })

    archived = []
    root = repo / "data/reconciliation/onboarding-decisions"
    if root.exists():
        for path in root.rglob("*.json"):
            try:
                doc = json.loads(path.read_text(encoding="utf-8"))
            except Exception:
                continue
            if isinstance(doc, dict) and doc.get("site_gap_provenance"):
                archived.append({
                    "path": path.relative_to(repo).as_posix(),
                    "entry_count": len(doc.get("site_gap_provenance") or []),
                })
    return {
        "discrepancy_row_count": len(rows),
        "canonical_game_count": len(grouped),
        "field_combinations": {
            "+".join(k): v for k, v in sorted(combos.items(), key=lambda kv: kv[0])
        },
        "current_gap_mismatch_count": len(mismatch),
        "current_gap_mismatches": mismatch,
        "archived_plan_count": len(archived),
        "archived_plans": archived,
        "validator_semantics": {
            "implementation_site_gate": "Requires provenance for every current primitive gap but tolerates extra resolved discrepancy rows.",
            "repository_validation": "Does not reinterpret reciprocal-only site-gap discrepancy semantics; apply-time lifecycle validator is stricter.",
        },
    }


def write_checkpoint_inputs(control: Path, target: Path, control_commit: str):
    odir = target / ".onboarding" / SCHOOL
    odir.mkdir(parents=True, exist_ok=True)
    plan = git_show(control, control_commit, f"{CHECKPOINT_DIR}/plan.json")
    review = git_show(control, control_commit, f"{CHECKPOINT_DIR}/review.csv")
    recmap = git_show(control, control_commit, f"{CHECKPOINT_DIR}/recommendation-map.json")
    (odir / "plan.json").write_bytes(plan)
    (odir / "review.csv").write_bytes(review)
    map_path = odir / "assessment-recommendation-map.json"
    map_path.write_bytes(recmap)
    return odir / "plan.json", odir / "review.csv", map_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", type=Path, required=True)
    ap.add_argument("--target", type=Path, required=True)
    ap.add_argument("--control", type=Path, required=True)
    ap.add_argument("--control-commit", default=CONTROL_COMMIT)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()

    candidate = args.candidate.resolve()
    target = args.target.resolve()
    control = args.control.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    candidate_sha = run(["git", "rev-parse", "HEAD"], cwd=candidate).stdout.strip()
    target_sha = run(["git", "rev-parse", "HEAD"], cwd=target).stdout.strip()
    if candidate_sha != EXPECTED["candidate"]:
        raise SystemExit(f"candidate mismatch {candidate_sha}")
    if target_sha != EXPECTED["target"]:
        raise SystemExit(f"target mismatch {target_sha}")
    run(["git", "cat-file", "-e", f"{args.control_commit}^{{commit}}"], cwd=control)

    sys.path.insert(0, str(candidate / "tools"))
    import onboarding_hardening
    import onboarding_plan
    import onboard_school
    import implementation_site_gate
    from remote_implementation_stage2_proposal import verify_stage2_proposal_authority

    request = json.loads(git_show(control, args.control_commit, f"{CHECKPOINT_DIR}/request.json"))
    authority = verify_stage2_proposal_authority(
        request, args.control_commit, source_repo=control
    )
    freeze_bytes = authority["freeze_bytes"]
    if sha256(freeze_bytes) != EXPECTED["freeze"]:
        raise SystemExit("Integration Freeze mismatch")
    if request["decision_universe_sha256"] != EXPECTED["universe"]:
        raise SystemExit("decision universe mismatch")

    plan_path, review_path, map_path = write_checkpoint_inputs(
        control, target, args.control_commit
    )
    if sha256(map_path.read_bytes()) != EXPECTED["map"]:
        raise SystemExit("recommendation map mismatch")
    freeze_path = target / ".onboarding" / SCHOOL / "integration-freeze.json"
    freeze_path.write_bytes(freeze_bytes)

    filled_review = target / ".onboarding" / SCHOOL / "assessment-filled-review.csv"
    filled_review.write_bytes(review_path.read_bytes())
    action_counts = onboarding_hardening.fill_review_from_map(filled_review, map_path)
    approved, approved_hash = onboarding_hardening.approve_plan(
        target,
        plan_path,
        filled_review,
        onboarding_hardening.TECHNICAL_PREVIEW_APPROVED_BY,
        approved_at=onboarding_hardening.TECHNICAL_PREVIEW_APPROVED_AT,
    )
    if len(approved.get("decisions", [])) != 137:
        raise SystemExit("approved decision count drift")
    provenance = list(approved.get("site_gap_provenance", []))
    if len(provenance) != 13:
        raise SystemExit(f"expected 13 provenance entries, found {len(provenance)}")
    if {e["canonical_game_id"] for e in provenance} != set(SITE_GAMES):
        raise SystemExit("provenance game population drift")

    base_tree = run(["git", "rev-parse", "HEAD^{tree}"], cwd=target).stdout.strip()
    target_status_before = run(["git", "status", "--porcelain"], cwd=target).stdout

    assessment_repo = Path(tempfile.mkdtemp(prefix="richmond-stage2-assessment-")) / "repo"
    onboard_school.copy_repository(target, assessment_repo, school_key=SCHOOL)
    pre = snapshot(assessment_repo)
    pre_assertions = target_assertion_summary(assessment_repo)

    onboarding_plan.apply_pre_ingest_correction_identity_patches(assessment_repo, approved)
    onboarding_plan.apply_pre_ingest_source_patches(assessment_repo, approved)
    ingest_plan = onboard_school.write_plan_for_ingest(assessment_repo, approved)
    env = os.environ.copy()
    env["CBB_VALIDATE_DATA_TOOL_OVERRIDE"] = str(candidate / "tools/validate_data.py")
    ingest = run(
        [
            sys.executable,
            str(candidate / "tools/ingest_school.py"),
            SCHOOL,
            "--apply",
            "--identity-decisions",
            str(ingest_plan),
            "--repo",
            str(assessment_repo),
        ],
        cwd=candidate,
        env=env,
        check=False,
    )
    if ingest.returncode:
        (output / "assessment-ingest.log").write_text(ingest.stdout, encoding="utf-8")
        raise SystemExit("assessment ingestion failed; see log")

    post_ingest = snapshot(assessment_repo)
    post_ingest_assertions = target_assertion_summary(assessment_repo)

    captured_before_provenance: dict[str, dict[str, Any]] = {}
    original_recorder = onboarding_plan._record_reciprocal_only_site_gap_provenance

    def capture_noop(
        school_key, approved_plan, canonical_rows, assertion_rows, source_rows, discrepancy_rows
    ):
        by_id = {
            row.get("canonical_game_id", "").strip(): row for row in canonical_rows
        }
        captured_before_provenance.update(
            {gid: state(by_id.get(gid)) for gid in SITE_GAMES}
        )
        return {}

    onboarding_plan._record_reciprocal_only_site_gap_provenance = capture_noop
    try:
        reconciliation_counts = onboarding_plan.apply_reconciliation_decisions(
            assessment_repo, approved
        )
    finally:
        onboarding_plan._record_reciprocal_only_site_gap_provenance = original_recorder

    post_recon = snapshot(assessment_repo)
    post_recon_assertions = target_assertion_summary(assessment_repo)
    if captured_before_provenance != post_recon:
        raise SystemExit("canonical state changed after provenance-recording boundary")

    canonical_after = canonical_map(assessment_repo)
    gate_categories = {
        gid: implementation_site_gate._canonical_gap_categories(
            canonical_after[gid], SCHOOL
        )
        for gid in SITE_GAMES
    }
    site_report_without_provenance = implementation_site_gate.implementation_site_report(
        assessment_repo, SCHOOL, example_limit=50
    )

    validator = run(
        [sys.executable, str(candidate / "tools/validate_data.py"), str(assessment_repo)],
        cwd=candidate, env=env, check=False
    )
    (output / "assessment-validate-data.log").write_text(validator.stdout, encoding="utf-8")

    prov_by_id = {e["canonical_game_id"]: e for e in provenance}
    rows = []
    for gid in SITE_GAMES:
        origin = explain_origin(
            pre[gid], post_ingest[gid], post_recon[gid],
            post_recon_assertions.get(gid, []), approved, gid
        )
        rows.append({
            "canonical_game_id": gid,
            "pre_apply": pre[gid],
            "discovered_provenance_fields": prov_by_id[gid]["fields"],
            "named_reciprocal": {
                "source_program_key": prov_by_id[gid]["reciprocal_source_program_key"],
                "source_game_id": prov_by_id[gid]["reciprocal_source_game_id"],
            },
            "pre_apply_target_assertions": pre_assertions.get(gid, []),
            "after_ingestion": post_ingest[gid],
            "after_ingestion_target_assertions": post_ingest_assertions.get(gid, []),
            "after_site_geography_enrichment": post_ingest[gid],
            "after_generic_reconciliation": post_recon[gid],
            "immediately_before_provenance_recording": captured_before_provenance[gid],
            "repository_validation_state": post_recon[gid],
            "site_gate_validation_state": {
                **post_recon[gid],
                "gap_categories": gate_categories[gid],
            },
            "origin_explanation": origin,
            "classification": classify_transition(pre[gid], post_recon[gid], origin),
        })

    # Read-only diagnostic continuation. This emulates coherent lifecycle semantics
    # only inside a fresh disposable copy: fields legitimately resolved before
    # materialization retire; if ingestion created a target assertion, reciprocal-
    # only provenance retires entirely and ordinary source/site accounting must
    # carry the surviving state. The original approved plan hash is preserved.
    adaptive_repo = Path(tempfile.mkdtemp(prefix="richmond-stage2-adaptive-")) / "repo"
    onboard_school.copy_repository(target, adaptive_repo, school_key=SCHOOL)
    original_recorder2 = onboarding_plan._record_reciprocal_only_site_gap_provenance
    adaptive_events = []

    def adaptive_recorder(
        school_key, approved_plan, canonical_rows, assertion_rows, source_rows, discrepancy_rows
    ):
        by_id = {
            row.get("canonical_game_id", "").strip(): row for row in canonical_rows
        }
        assertions_by_gid: dict[str, list[dict[str, str]]] = defaultdict(list)
        for a in assertion_rows:
            assertions_by_gid[a.get("canonical_game_id", "").strip()].append(a)
        adjusted = []
        for entry in approved_plan.get("site_gap_provenance", []):
            gid = entry["canonical_game_id"]
            current = primitive_gaps(by_id[gid])
            current = [f for f in current if f in {"venue", "location"}]
            target_assertions = [
                a for a in assertions_by_gid.get(gid, [])
                if a.get("source_program_key", "").strip() == school_key
            ]
            event = {
                "canonical_game_id": gid,
                "discovery_fields": list(entry["fields"]),
                "materialization_fields": current,
                "target_assertion_count": len(target_assertions),
            }
            if target_assertions:
                event["action"] = "RETIRE_RECIPROCAL_ONLY_TO_ORDINARY_SOURCE_ACCOUNTING"
                adaptive_events.append(event)
                continue
            if not current:
                event["action"] = "RETIRE_FULLY_RESOLVED"
                adaptive_events.append(event)
                continue
            new_entry = copy.deepcopy(entry)
            new_entry["fields"] = current
            event["action"] = (
                "PRESERVE" if current == entry["fields"] else "RETIRE_RESOLVED_FIELDS"
            )
            adaptive_events.append(event)
            adjusted.append(new_entry)
        temp = copy.deepcopy(approved_plan)
        temp["site_gap_provenance"] = adjusted
        return original_recorder2(
            school_key, temp, canonical_rows, assertion_rows, source_rows, discrepancy_rows
        )

    onboarding_plan._record_reciprocal_only_site_gap_provenance = adaptive_recorder
    adaptive_error = None
    adaptive_execution = None
    adaptive_gates = None
    try:
        old_override = os.environ.get("CBB_VALIDATE_DATA_TOOL_OVERRIDE")
        os.environ["CBB_VALIDATE_DATA_TOOL_OVERRIDE"] = str(candidate / "tools/validate_data.py")
        try:
            adaptive_execution = onboard_school.execute_approved_in_place(
                adaptive_repo, approved
            )
        finally:
            if old_override is None:
                os.environ.pop("CBB_VALIDATE_DATA_TOOL_OVERRIDE", None)
            else:
                os.environ["CBB_VALIDATE_DATA_TOOL_OVERRIDE"] = old_override
        before_hashes = onboard_school.tree_hashes(target)
        after_hashes = onboard_school.tree_hashes(adaptive_repo)
        changed = onboard_school.changed_paths(before_hashes, after_hashes)
        adaptive_gates = onboard_school.run_gates(
            adaptive_repo,
            SCHOOL,
            changed,
            include_tests=False,
            approved_plan=approved,
        )
    except Exception as exc:
        adaptive_error = f"{type(exc).__name__}: {exc}"
    finally:
        onboarding_plan._record_reciprocal_only_site_gap_provenance = original_recorder2

    main_provenance = repo_provenance_census(candidate)

    target_status_after = run(["git", "status", "--porcelain"], cwd=target).stdout
    target_tree_after = run(["git", "rev-parse", "HEAD^{tree}"], cwd=target).stdout.strip()
    tracked_unchanged = (
        target_status_before == target_status_after == ""
        and base_tree == target_tree_after
        and run(["git", "rev-parse", "HEAD"], cwd=target).stdout.strip() == EXPECTED["target"]
    )

    assessment = {
        "schema_version": 1,
        "kind": "RICHMOND_STAGE2_SYSTEMIC_PRE_GATE1_ASSESSMENT",
        "authority": {
            "protected_main_sha": EXPECTED["main"],
            "target_sha": EXPECTED["target"],
            "control_commit": args.control_commit,
            "candidate_sha": EXPECTED["candidate"],
            "integration_freeze_sha256": EXPECTED["freeze"],
            "semantic_snapshot_sha256": EXPECTED["semantic"],
            "decision_count": 137,
            "decision_universe_sha256": EXPECTED["universe"],
            "recommendation_map_sha256": EXPECTED["map"],
            "approved_plan_hash_preview": approved_hash,
            "map_action_counts": dict(sorted(action_counts.items())),
        },
        "site_gap_population": rows,
        "site_gap_population_summary": {
            "pre_apply_field_combinations": dict(Counter(
                "+".join(sorted(e["fields"])) for e in provenance
            )),
            "transition_classifications": dict(Counter(r["classification"] for r in rows)),
            "post_reconciliation_gap_combinations": dict(Counter(
                "+".join(r["after_generic_reconciliation"]["gaps"]) or "NONE"
                for r in rows
            )),
            "post_ingestion_target_assertion_counts": {
                gid: len(post_ingest_assertions.get(gid, [])) for gid in SITE_GAMES
            },
        },
        "lifecycle_semantics": {
            "discovery": "Pre-apply snapshot generated by _discover_reciprocal_only_site_gap_provenance().",
            "review_serialization": "site_gap_provenance_json rides the publication review row and is copied into the approved plan; it is outside the 137 owner decision-map payload.",
            "ingestion": "Permanent ingestion may add a target assertion and deterministic canonical enrichment before generic reconciliation.",
            "materialization": "_record_reciprocal_only_site_gap_provenance() currently revalidates the immutable discovery-time field set against the post-ingestion/post-reconciliation canonical state.",
            "site_gate": "_review_accounts_for_gap() asks only whether every current primitive gap has field-specific provenance; extra resolved discrepancy rows are not required for current-gap accounting.",
            "semantic_model_assessed": "Discovery-time fields are a conservative superset. At materialization, only still-unresolved legitimate primitive gaps may survive; entries whose topology becomes ordinary target-source accounting or fully resolved must retire rather than remain stale.",
        },
        "repository_existing_provenance_census": main_provenance,
        "assessment_runtime": {
            "ingestion_returncode": ingest.returncode,
            "reconciliation_counts_without_provenance": reconciliation_counts,
            "validate_data_returncode_without_provenance": validator.returncode,
            "site_gate_without_provenance": site_report_without_provenance,
            "adaptive_lifecycle_events": adaptive_events,
            "adaptive_execution_error": adaptive_error,
            "adaptive_execution": adaptive_execution,
            "adaptive_gates": adaptive_gates,
        },
        "detected_generic_families": [
            {
                "family": "VENUE_NAME_PERIOD_EXECUTION_VALIDATION",
                "classification": "OTHER_GENERIC_PRE_GATE1_TECHNICAL_FAMILY",
                "status": "CANDIDATE_REPAIR_ADVANCES_PAST_PRIOR_BLOCKER",
            },
            {
                "family": "RECIPROCAL_ONLY_SITE_GAP_PROVENANCE_LIFECYCLE",
                "classification": "SAME_SITE_GAP_PROVENANCE_FAMILY",
                "status": "ASSESSMENT_TARGET",
            },
        ] + ([] if adaptive_error is None else [{
            "family": "NEXT_CURRENTLY_EXERCISABLE_BLOCKER",
            "classification": "UNCLASSIFIED_PENDING_DIAGNOSTIC_REVIEW",
            "status": adaptive_error,
        }]),
        "richmond_tracked_state_unchanged": tracked_unchanged,
    }
    (output / "richmond-stage2-systemic-assessment.json").write_text(
        json.dumps(assessment, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (output / "assessment-summary.txt").write_text(
        json.dumps({
            "transition_classifications": assessment["site_gap_population_summary"]["transition_classifications"],
            "post_gap_combinations": assessment["site_gap_population_summary"]["post_reconciliation_gap_combinations"],
            "existing_provenance": main_provenance,
            "adaptive_error": adaptive_error,
            "tracked_unchanged": tracked_unchanged,
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "transition_classifications": assessment["site_gap_population_summary"]["transition_classifications"],
        "post_gap_combinations": assessment["site_gap_population_summary"]["post_reconciliation_gap_combinations"],
        "adaptive_error": adaptive_error,
        "tracked_unchanged": tracked_unchanged,
    }, indent=2, sort_keys=True))
    if not tracked_unchanged:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
