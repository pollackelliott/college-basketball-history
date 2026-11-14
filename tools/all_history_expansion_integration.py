#!/usr/bin/env python3
"""Generic, read-only expansion Integration Freeze authority and Phase 0 packet.

This module never writes tracked basketball state, creates a branch, or
publishes anything. The Phase 0 packet is NOT a mutation/merge authorization;
the existing serialized remote Implementation control plane must separately
validate and execute it with global lock, write-ahead, CAS, and fresh replay.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from all_history_expansion_freeze import (
    authenticate_baseline, canonical_row_sha256, verify_expansion,
)
from all_history_expansion_research import (
    project_complete_institutional_program_row,
)
from expansion_implementation_stage1 import (
    PACKAGE_FILES, Stage1Stop, canonical_bytes, csv_rows,
    git_bytes, git_revision, sha256, stage1,
)
from integration_freeze_guard import (
    build_source_game_semantic_snapshot,
    semantic_snapshot_sha256,
)
from stage1_venue_reconciliation import load_venue_reconciliation
from stage_research_portfolio import (
    load_existing_school_venues,
    venue_reconciliation_inventory,
)

MANIFEST_NAME = "expansion-integration-freeze.json"
PROPOSAL_NAME = "expansion-phase0-transaction-proposal.json"
STAGE1_REPORT = "expansion-stage1-reconciliation.json"
KNOWN_STAGE1_BLOCKER = "DOWNSTREAM_EXPANSION_INTEGRATION_FREEZE_AND_GUARDED_PHASE0_MISSING"
SHA40 = re.compile(r"[0-9a-f]{40}\Z")
SHA64 = re.compile(r"[0-9a-f]{64}\Z")


class IntegrationAuthorityError(Stage1Stop):
    """Authenticated authority drift or forbidden mutation surface."""


def require(condition: Any, reason: str) -> None:
    if not condition:
        raise IntegrationAuthorityError(reason)


def check_sha(value: str, count: int) -> None:
    require(isinstance(value, str) and bool(
        (SHA40 if count == 40 else SHA64).fullmatch(value)
    ), "EXACT_SHA_REQUIRED")


def read_json(path: Path) -> dict[str, Any]:
    result = json.loads(path.read_bytes())
    require(isinstance(result, dict), "JSON_OBJECT_REQUIRED")
    return result


def authenticate_proof(
    proof: dict[str, Any], report: dict[str, Any],
    actual_files: dict[str, str],
    expected_main: str, expected_base: str, expected_zip: str,
) -> None:
    require(proof.get("status") == "INDEPENDENTLY_REPRODUCED_READ_ONLY_STAGE1",
            "STAGE1_INDEPENDENT_PROOF_STATUS_MISMATCH")
    for label, value in (
        ("protected_main_sha", expected_main),
        ("research_base_sha", expected_base),
        ("freeze_zip_sha256", expected_zip),
    ):
        require(proof.get(label) == value, "STAGE1_INDEPENDENT_PROOF_BINDING:" + label)
    require(proof.get("candidate_sha256") == actual_files,
            "STAGE1_INDEPENDENT_PROOF_CANDIDATE_HASH_MISMATCH")
    for key, name in (
        ("identity_counts", "canonical_identity_census"),
        ("global_venue_counts", "global_venue_reconciliation"),
    ):
        require(proof.get(key) == report[name]["counts"], "STAGE1_PROOF_COUNTS:" + key)
    for kind, item in (("opponents", "opponent_support_actions"),
                       ("venues", "venue_support_actions")):
        require(proof.get("support_" + kind) == report["census"][item],
                "STAGE1_PROOF_SUPPORT_ACTIONS:" + kind)
    require(proof.get("blockers") == report["blockers"], "STAGE1_PROOF_BLOCKERS_MISMATCH")
    require(proof.get("integration_freeze_authorized") is False,
            "STAGE1_PROOF_CANNOT_PREAUTHORIZE_INTEGRATION")


def source_preservation(
    baseline: dict[str, Any], combined_raw: bytes,
    report: dict[str, Any], manifest: dict[str, Any],
) -> dict[str, Any]:
    fields, combined = csv_rows(combined_raw, "candidate source games")
    require(fields == baseline["source_fields"], "INHERITED_SOURCE_SCHEMA_DRIFT")
    inherited = baseline["source_rows"]
    require(combined[:len(inherited)] == inherited, "INHERITED_SOURCE_ROWS_CHANGED")
    supplemental = combined[len(inherited):]
    ids = [x.get("source_game_id", "").strip() for x in combined]
    require(all(ids) and len(ids) == len(set(ids)), "COMBINED_SOURCE_ID_COLLISION")
    require(report["census"]["inherited_source_game_count"] == len(inherited),
            "INHERITED_SOURCE_COUNT_DRIFT")
    require(report["census"]["supplemental_new_source_game_count"] == len(supplemental),
            "SUPPLEMENTAL_SOURCE_COUNT_DRIFT")
    require(report["census"]["combined_source_game_count"] == len(combined),
            "COMBINED_SOURCE_COUNT_DRIFT")
    return {"inherited_count": len(inherited), "supplemental_count": len(supplemental),
            "combined_count": len(combined), "inherited_source_ids_sha256": sha256(
                canonical_bytes([x["source_game_id"] for x in inherited])),
            "combined_source_ids_sha256": sha256(canonical_bytes(ids)),
            "supplemental_source_ids_sha256": sha256(canonical_bytes(
                [x["source_game_id"] for x in supplemental])),
            "inherited_rows_sha256": sha256(canonical_bytes(inherited))}


def freeze_authority(
    repo: Path, school: str, artifact: Path, zip_sha: str,
    research_base: str, main_sha: str, proof_path: Path, proof_sha: str,
    output: Path, *, retain: bool = True,
    venue_reconciliation_path: Path | None = None,
) -> dict[str, Any]:
    """Fresh-verifies accepted frozen evidence and independently replays Stage 1."""
    repo, artifact, proof_path, output = (
        repo.resolve(), artifact.resolve(), proof_path.resolve(), output.resolve()
    )
    if venue_reconciliation_path is not None:
        venue_reconciliation_path = venue_reconciliation_path.resolve()
    for digest in (zip_sha, proof_sha):
        check_sha(digest, 64)
    for digest in (research_base, main_sha):
        check_sha(digest, 40)
    require(output != repo and repo not in output.parents,
            "INTEGRATION_FREEZE_OUTPUT_MUST_BE_EXTERNAL")
    require(not output.exists(), "REFUSE_OVERWRITE_EXISTING_FREEZE")
    require(sha256(proof_path.read_bytes()) == proof_sha,
            "STAGE1_INDEPENDENT_PROOF_SHA256_MISMATCH")
    require(sha256(artifact.read_bytes()) == zip_sha,
            "RESEARCH_FREEZE_ZIP_SHA256_MISMATCH")
    require(git_revision(repo, "refs/remotes/origin/main") == main_sha,
            "PROTECTED_MAIN_CHANGED")
    require(git_revision(repo, main_sha + "^{commit}") == main_sha,
            "CURRENT_MAIN_GIT_COMMIT_MISSING")
    verified = verify_expansion(repo, artifact)
    require(verified["status"] == "VERIFIED_EXPANSION_RESEARCH_FROZEN",
            "PERMANENT_RESEARCH_FREEZE_VERIFIER_FAILED")
    require((verified["school_key"], verified["research_base_sha"],
             verified["zip_sha256"]) == (school, research_base, zip_sha),
            "FROZEN_RESEARCH_IDENTITY_MISMATCH")
    baseline = authenticate_baseline(repo, school, research_base)
    proof = read_json(proof_path)
    with tempfile.TemporaryDirectory(prefix="expansion-integration-freeze-") as tmp:
        root = Path(tmp)
        candidate = root / "candidate"
        report = stage1(repo, school, artifact, zip_sha, research_base,
                        main_sha, candidate)
        require(report.get("write_authority") == "NONE_REHEARSAL_ONLY",
                "STAGE1_REHEARSAL_WRITE_AUTHORITY_INVALID")
        require([x["class"] for x in report["blockers"]] == [KNOWN_STAGE1_BLOCKER],
                "STAGE1_RECONCILIATION_NOT_UNAMBIGUOUS")
        counts = report["canonical_identity_census"]["counts"]
        require(counts["IDENTITY_REVIEW_BLOCKER"] == 0, "CANONICAL_IDENTITY_UNRESOLVED")
        require(not report["canonical_identity_census"]["duplicate_canonical_reuse"],
                "DUPLICATE_CANONICAL_REUSE")
        require(not report["canonical_identity_census"]["possible_duplicate_supplemental_rows"],
                "DUPLICATE_SUPPLEMENTAL_GAMES")
        require(report["global_venue_reconciliation"]["counts"][
            "GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER"] == 0,
            "VENUE_IDENTITY_UNRESOLVED")

        venue_reconciliation: dict[str, dict[str, Any]] = {}
        venue_reconciliation_meta: dict[str, Any] | None = None
        venue_reconciliation_census: dict[str, Any] | None = None
        if venue_reconciliation_path is not None:
            candidate_venues_raw = (candidate / "venues.csv").read_bytes()
            _, candidate_venues = csv_rows(
                candidate_venues_raw, "expansion candidate venues"
            )
            _, global_venues = csv_rows(
                git_bytes(repo, main_sha, "data/reference/venues.csv"),
                "current global venues",
            )
            _, global_names = csv_rows(
                git_bytes(repo, main_sha, "data/reference/venue-names.csv"),
                "current global venue names",
            )
            venue_reconciliation, venue_reconciliation_meta = (
                load_venue_reconciliation(
                    venue_reconciliation_path,
                    school_key=school,
                    package_path=artifact,
                    local_venues=candidate_venues,
                    global_venues=global_venues,
                    frozen_venues_bytes=candidate_venues_raw,
                    source_games_bytes=(candidate / "source-games.csv").read_bytes(),
                )
            )
            venue_reconciliation_meta = dict(venue_reconciliation_meta)
            venue_reconciliation_meta["spec_path"] = "venue-reconciliation.json"
            require(
                all(
                    item.get("action") == "REUSE_CURRENT_IDENTITY"
                    for item in venue_reconciliation.values()
                ),
                "EXPANSION_VENUE_RECONCILIATION_ACTION_UNSUPPORTED",
            )
            inherited_venue_count = len(baseline["venue_rows"])
            new_venues = candidate_venues[inherited_venue_count:]
            new_keys = {
                row.get("venue_key", "").strip()
                for row in new_venues
                if row.get("venue_key", "").strip()
            }
            require(
                all(
                    item.get("local_venue_key", "") in new_keys
                    for item in venue_reconciliation.values()
                ),
                "EXPANSION_VENUE_RECONCILIATION_NOT_NEW_SUPPORT",
            )
            venue_reconciliation_census = venue_reconciliation_inventory(
                new_venues,
                global_venues,
                global_names,
                school_key=school,
                existing_school_venues=load_existing_school_venues(
                    repo, exclude_school_key=school
                ),
                venue_reconciliation=venue_reconciliation,
            )
            require(
                venue_reconciliation_census["blocker_count"] == 0,
                "EXPANSION_VENUE_RECONCILIATION_STILL_BLOCKED",
            )
        hashes = {name: sha256((candidate / name).read_bytes())
                  for name in (*PACKAGE_FILES, STAGE1_REPORT)}
        require(report["candidate_member_sha256"] == {
            name: hashes[name] for name in PACKAGE_FILES
        }, "CANDIDATE_SHA_MAP_CHANGED")
        authenticate_proof(proof, report, hashes, main_sha, research_base, zip_sha)
        preservation_baseline = baseline
        if report.get("current_main_reconciliation", {}).get("status") == (
            "APPLIED_RESOLVED_EXTERNAL_IDENTITY_CORRECTION"
        ):
            current_source_fields, current_source_rows = csv_rows(
                git_bytes(repo, main_sha, f"schools/{school}/source-games.csv"),
                "current-main inherited source games",
            )
            require(
                current_source_fields == baseline["source_fields"],
                "CURRENT_MAIN_REBASE_SOURCE_SCHEMA_DRIFT",
            )
            preservation_baseline = dict(
                baseline,
                source_rows=current_source_rows,
            )
        guard = source_preservation(
            preservation_baseline,
            (candidate / "source-games.csv").read_bytes(),
            report,
            {},
        )
        # Only historical publication metadata may transition, never top-level scope.
        expected = project_complete_institutional_program_row(
            baseline["program"], report["researched_inception_season"])
        require(set(expected) == set(baseline["program"]), "PROGRAM_SCHEMA_DRIFT")
        differences = {k for k in expected
                       if baseline["program"][k] != expected[k]}
        require(differences <= {
            "program_inception_season", "history_coverage_status"
        }, "TOP_LEVEL_SCOPE_OR_ACCOMPLISHMENT_MUTATION_FORBIDDEN")
        current_program_rows = csv_rows(git_bytes(repo, main_sha,
            "data/reference/programs.csv"), "current programs")[1]
        current = [x for x in current_program_rows if x["program_key"] == school]
        require(len(current) == 1 and current[0] == baseline["program"],
                "CURRENT_MAIN_PROGRAM_AUTHORITY_DRIFT")
        for path, key, identity, expected_row in (
            ("data/reference/program-top-level-scope.csv", "school",
             baseline["scope_row"]["school"], baseline["scope_row"]),
            ("data/reference/program-accomplishments.csv", "program_key",
             school, baseline["accomplishment_row"]),
        ):
            rows = csv_rows(git_bytes(repo, main_sha, path), path)[1]
            hits = [x for x in rows if x.get(key) == identity]
            require(hits == ([expected_row] if expected_row is not None else []),
                    "CURRENT_MAIN_ACCEPTED_SCOPE_OR_ACCOMPLISHMENT_DRIFT:" + path)
        # Reuse IDs are audit facts only; not an ungated canonical write map.
        reuse = sorted(
            [{"source_game_id":x["source_game_id"],
              "canonical_game_id":x["canonical_game_id"],
              "match_method":x["match_method"]}
             for x in report["canonical_identity_census"]["game_rows"]
             if x["classification"] == "REUSE_CANONICAL"],
            key=lambda x:x["source_game_id"]
        )
        semantic_snapshot = build_source_game_semantic_snapshot(
            candidate / "source-games.csv"
        )
        semantic_sha = semantic_snapshot_sha256(semantic_snapshot)
        package_hashes = {k: hashes[k] for k in PACKAGE_FILES}
        predecessor_package_hashes = dict(baseline["package_member_sha256"])
        if report.get("current_main_reconciliation", {}).get("status") == (
            "APPLIED_RESOLVED_EXTERNAL_IDENTITY_CORRECTION"
        ):
            predecessor_package_hashes = dict(
                report["current_main_reconciliation"][
                    "current_package_member_sha256"
                ]
            )
            require(
                set(predecessor_package_hashes) == set(PACKAGE_FILES),
                "CURRENT_MAIN_REBASE_PREDECESSOR_HASH_SET_INVALID",
            )
        manifest = {
            "schema_version": 1,
            "kind": "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
            "status": "INTEGRATION_FROZEN",
            "release_authority": False,
            "tracked_mutation": "NONE",
            "school_key": school,
            "research_base_sha": research_base,
            "protected_main_sha": main_sha,
            "integration_base_sha": main_sha,
            "origin_main_sha": main_sha,
            "research_freeze_zip_sha256": zip_sha,
            "research_zip_sha256": zip_sha,
            "independent_stage1_proof_sha256": proof_sha,
            "stage1_report_sha256": hashes[STAGE1_REPORT],
            "candidate_member_sha256": package_hashes,
            "package_member_sha256": package_hashes,
            "source_game_semantic_guard": {
                "snapshot": semantic_snapshot,
                "snapshot_sha256": semantic_sha,
            },
            "source_preservation": guard,
            "current_main_reconciliation": report.get(
                "current_main_reconciliation", {}
            ),
            "canonical_identity_counts": counts,
            "canonical_reuses": reuse,
            "opponent_support_actions": report["census"]["opponent_support_actions"],
            "venue_support_actions": report["census"]["venue_support_actions"],
            "global_venue_reconciliation": report["global_venue_reconciliation"]["counts"],
            "venue_reconciliation": venue_reconciliation_meta,
            "venue_reconciliation_sha256": (
                venue_reconciliation_meta["spec_sha256"]
                if venue_reconciliation_meta is not None else ""
            ),
            "venue_reconciliation_census": venue_reconciliation_census,
            "baseline_package_member_sha256": baseline["package_member_sha256"],
            "accepted_predecessor_package_member_sha256": predecessor_package_hashes,
            "baseline_program_row_sha256": canonical_row_sha256(baseline["program"]),
            "frozen_program_projection_sha256": canonical_row_sha256(expected),
            "frozen_program_projection": expected,
            "top_level_scope_row_sha256": baseline["scope_row_sha256"],
            "accomplishment_status": baseline["accomplishment_status"],
            "accomplishment_row_sha256": baseline["accomplishment_row_sha256"],
            "unresolved_history_decisions": 0,
            "required_phase0_guards": [
                "GLOBAL_IMPLEMENTATION_MUTATION_LOCK",
                "CURRENT_MAIN_SHA_MATCH",
                "EXPECTED_PREDECESSOR_CAS",
                "DURABLE_WRITEAHEAD_BEFORE_PUBLICATION",
                "EXACT_SCHOOL_AND_GLOBAL_CHANGED_PATH_ALLOWLIST",
                "INDEPENDENT_EXACT_TREE_REPLAY",
                "NO_OWNER_GATE_OR_RELEASE_AUTHORITY",
            ],
            "manifest_self_fingerprint_sha256": "",
        }
        manifest["manifest_self_fingerprint_sha256"] = sha256(canonical_bytes(manifest))
        require(git_revision(repo,"refs/remotes/origin/main") == main_sha,
                "PROTECTED_MAIN_CHANGED_DURING_FREEZE")
        if retain:
            output.mkdir(parents=True)
            for name in (*PACKAGE_FILES, STAGE1_REPORT):
                shutil.copyfile(candidate / name, output / name)
            if venue_reconciliation_path is not None:
                shutil.copyfile(
                    venue_reconciliation_path,
                    output / "venue-reconciliation.json",
                )
            (output / MANIFEST_NAME).write_bytes(canonical_bytes(manifest))
        return manifest


def verify_manifest_bytes(manifest_bytes: bytes, candidate: Path) -> dict[str, Any]:
    """Independent hash verifier; this never trusts a stored self-fingerprint."""
    manifest = json.loads(manifest_bytes)
    require(manifest.get("kind") == "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE"
            and manifest.get("status") == "INTEGRATION_FROZEN",
            "INTEGRATION_FREEZE_KIND_OR_STATUS_INVALID")
    fingerprint = manifest.get("manifest_self_fingerprint_sha256")
    check_sha(fingerprint, 64)
    view = dict(manifest, manifest_self_fingerprint_sha256="")
    require(sha256(canonical_bytes(view)) == fingerprint,
            "INTEGRATION_FREEZE_SELF_FINGERPRINT_MISMATCH")
    for name, digest in manifest["candidate_member_sha256"].items():
        require(name in PACKAGE_FILES and sha256((candidate / name).read_bytes()) == digest,
                "INTEGRATION_FREEZE_CANDIDATE_CHANGED:" + name)
    require(set(manifest["candidate_member_sha256"]) == set(PACKAGE_FILES),
            "INTEGRATION_FREEZE_MEMBER_SET_CHANGED")
    require(sha256((candidate / STAGE1_REPORT).read_bytes()) ==
            manifest["stage1_report_sha256"],
            "INTEGRATION_FREEZE_STAGE1_REPORT_CHANGED")
    reconciliation = manifest.get("venue_reconciliation")
    reconciliation_sha = str(manifest.get("venue_reconciliation_sha256") or "")
    if reconciliation is not None:
        require(isinstance(reconciliation, dict),
                "INTEGRATION_FREEZE_VENUE_RECONCILIATION_INVALID")
        require(reconciliation_sha == reconciliation.get("spec_sha256"),
                "INTEGRATION_FREEZE_VENUE_RECONCILIATION_HASH_BINDING")
        sidecar = candidate / "venue-reconciliation.json"
        require(sidecar.is_file(),
                "INTEGRATION_FREEZE_VENUE_RECONCILIATION_MISSING")
        require(sha256(sidecar.read_bytes()) == reconciliation_sha,
                "INTEGRATION_FREEZE_VENUE_RECONCILIATION_CHANGED")
    else:
        require(reconciliation_sha == "",
                "INTEGRATION_FREEZE_UNEXPECTED_VENUE_RECONCILIATION_HASH")
    require(manifest["tracked_mutation"] == "NONE"
            and manifest["release_authority"] is False,
            "INTEGRATION_FREEZE_CANNOT_AUTHORIZE_MUTATION")
    return manifest


def phase0_packet(frozen: Path, output: Path) -> dict[str, Any]:
    """Read-only request prerequisite. Not a substitute for guarded Phase 0."""
    require(not output.exists(), "REFUSE_OVERWRITE_PHASE0_PACKET")
    manifest = verify_manifest_bytes(
        (frozen / MANIFEST_NAME).read_bytes(), frozen
    )
    school = manifest["school_key"]
    paths = sorted({
        *(f"schools/{school}/{name}" for name in PACKAGE_FILES),
        "data/reference/programs.csv", "data/reference/venues.csv",
        "data/reference/venue-names.csv", "data/reference/conferences.csv",
    })
    packet = {
        "schema_version": 1,
        "kind": "ALL_HISTORY_EXPANSION_PHASE0_GUARDED_PRECONDITIONS",
        "status": "PREPARATION_ONLY",
        "school_key": school,
        "expected_main_sha": manifest["protected_main_sha"],
        "research_base_sha": manifest["research_base_sha"],
        "freeze_manifest_sha256": sha256((frozen / MANIFEST_NAME).read_bytes()),
        "candidate_member_sha256": manifest["candidate_member_sha256"],
        "allowed_changed_paths": paths,
        "required_transaction_guards": manifest["required_phase0_guards"],
        "registered_identity_changes_allowed_only_under_guard": True,
        "semantic_approval": False,
        "mutation_authority": "NONE",
        "phase0_executed": False,
        "terminal_blocker": "GUARDED_EXPANSION_PHASE0_RUNNER_NOT_ACTIVATED",
    }
    output.write_bytes(canonical_bytes(packet))
    return packet


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    freeze = sub.add_parser("freeze")
    freeze.add_argument("school_key")
    freeze.add_argument("freeze_zip", type=Path)
    freeze.add_argument("--expected-sha256", required=True)
    freeze.add_argument("--research-base", required=True)
    freeze.add_argument("--main-sha", required=True)
    freeze.add_argument("--independent-proof", required=True, type=Path)
    freeze.add_argument("--independent-proof-sha256", required=True)
    freeze.add_argument("--repo", type=Path, required=True)
    freeze.add_argument("--output", type=Path, required=True)
    freeze.add_argument("--venue-reconciliation", type=Path)
    verify = sub.add_parser("verify")
    verify.add_argument("candidate", type=Path)
    prepare = sub.add_parser("prepare-phase0")
    prepare.add_argument("candidate", type=Path)
    prepare.add_argument("--output", type=Path, required=True)
    args = p.parse_args(argv)
    try:
        if args.command == "freeze":
            result = freeze_authority(
                args.repo,args.school_key,args.freeze_zip,args.expected_sha256,
                args.research_base,args.main_sha,args.independent_proof,
                args.independent_proof_sha256,args.output,
                venue_reconciliation_path=args.venue_reconciliation,
            )
        elif args.command == "verify":
            result = verify_manifest_bytes(
                (args.candidate / MANIFEST_NAME).read_bytes(),args.candidate)
        else:
            result = phase0_packet(args.candidate,args.output)
        print(json.dumps({
            "status":result["status"],
            "school_key":result["school_key"],
            "mutated":False,
            "downstream_phase0_executed":False,
        },sort_keys=True))
        return 0
    except (IntegrationAuthorityError,OSError,ValueError,KeyError) as exc:
        print("STOP: "+str(exc),file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
