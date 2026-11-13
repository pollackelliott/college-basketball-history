#!/usr/bin/env python3
"""Expansion Phase 0 disposable current-main representation rehearsal.

Use the exact frozen six-file candidate and existing permanent venue/alias
rebasing functions. Output stays outside the repository; this code NEVER
acquires a global lock, prepares a commit, writes a Git ref or executes Phase 0.
Those operations remain exclusively in the guarded remote Implementation lane.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

from all_history_expansion_integration import (
    MANIFEST_NAME, PACKAGE_FILES, STAGE1_REPORT, IntegrationAuthorityError,
    canonical_bytes, csv_rows, git_bytes, git_revision, require,
    sha256, verify_manifest_bytes,
)
from stage_research_portfolio import (
    WorkflowError, load_existing_school_venues, rebase_venues,
    rebase_program_aliases,
)
from expansion_implementation_stage1 import render_csv


def preview_phase0(repo: Path, frozen: Path, output: Path) -> dict:
    repo, frozen, output = repo.resolve(), frozen.resolve(), output.resolve()
    require(repo != output and repo not in output.parents,
            "PHASE0_PREVIEW_OUTPUT_INSIDE_REPOSITORY")
    require(not output.exists(), "PHASE0_PREVIEW_REFUSES_OVERWRITE")
    manifest = verify_manifest_bytes((frozen / MANIFEST_NAME).read_bytes(),frozen)
    main = manifest["protected_main_sha"]
    school = manifest["school_key"]
    require(git_revision(repo,"refs/remotes/origin/main") == main,
            "PHASE0_PREVIEW_CURRENT_MAIN_CHANGED")
    require(git_revision(repo,main+"^{commit}") == main,
            "PHASE0_PREVIEW_MAIN_OBJECT_MISSING")
    school_bytes={name:git_bytes(repo,main,f"schools/{school}/{name}") for name in PACKAGE_FILES}
    baseline_hashes=manifest["baseline_package_member_sha256"]
    require({name:sha256(raw) for name,raw in school_bytes.items()} == baseline_hashes,
            "PHASE0_PREVIEW_INHERITED_SCHOOL_DRIFT")
    globals_paths={
        "programs":"data/reference/programs.csv",
        "venues":"data/reference/venues.csv",
        "venue-names":"data/reference/venue-names.csv",
        "program-names":"data/reference/program-names.csv",
    }
    original={key:git_bytes(repo,main,path) for key,path in globals_paths.items()}
    program_fields,program_rows=csv_rows(original["programs"],"programs.csv")
    global_venue_fields,global_venues=csv_rows(original["venues"],"venues.csv")
    global_name_fields,global_names=csv_rows(original["venue-names"],"venue-names.csv")
    _, aliases=csv_rows(original["program-names"],"program-names.csv")
    source_fields,sources=csv_rows((frozen/"source-games.csv").read_bytes(),"candidate source games")
    opponent_fields,opponents=csv_rows((frozen/"opponents.csv").read_bytes(),"candidate opponents")
    venue_fields,venues=csv_rows((frozen/"venues.csv").read_bytes(),"candidate venues")
    require(len(sources)==manifest["source_preservation"]["combined_count"],
            "PHASE0_PREVIEW_SOURCE_COUNT_CHANGED")
    require(manifest["frozen_program_projection"] is not None,
            "PHASE0_PREVIEW_MISSING_METADATA_PROJECTION")
    before=[p for p in program_rows if p["program_key"]==school]
    require(len(before)==1 and
            sha256(canonical_bytes(before[0])) ==
            sha256(canonical_bytes(before[0])), "PHASE0_PREVIEW_PROGRAM_MISSING")
    # The exact canonical-row hash is stored from original Research; it is
    # intentionally not compared to JSON serialization of the raw registry.
    from all_history_expansion_freeze import canonical_row_sha256
    require(canonical_row_sha256(before[0]) == manifest["baseline_program_row_sha256"],
            "PHASE0_PREVIEW_BASELINE_PROGRAM_DRIFT")
    projected=manifest["frozen_program_projection"]
    require(set(projected)==set(program_fields),
            "PHASE0_PREVIEW_PROGRAM_SCHEMA_CHANGED")
    protected_fields=set(program_fields)-{
        "program_inception_season","history_coverage_status"}
    require(all(projected[k]==before[0][k] for k in protected_fields),
            "PHASE0_PREVIEW_PROTECTED_METADATA_CHANGED")
    require(projected["history_coverage_status"]=="COMPLETE_INSTITUTIONAL",
            "PHASE0_PREVIEW_COVERAGE_NOT_COMPLETE")
    post_programs=[dict(projected) if r["program_key"]==school else dict(r)
                   for r in program_rows]

    # Alias rebase is representation-only. It must not silently rewrite
    # source-game semantics; any proposed source change stops this preflight.
    _, rebased_sources, alias_actions = rebase_program_aliases(
        program_rows, aliases, opponents, sources)
    require(rebased_sources==sources,
            "PHASE0_PREVIEW_SOURCE_SEMANTIC_REBASE_REQUIRES_GUARDED_REVIEW")
    # Any existing opponent support changes need explicit representation
    # reconciliation in later locked Phase 0. Preserve the frozen rows now.
    existing_other_venues=load_existing_school_venues(repo,exclude_school_key=school)
    rebased_local,rebased_global,rebased_names,venue_mappings = rebase_venues(
        school,venues,global_venues,global_names,
        existing_school_venues=existing_other_venues,
        source_games=sources,
    )
    require(len(rebased_local)==len(venues),
            "PHASE0_PREVIEW_SCHOOL_VENUE_POPULATION_CHANGED")
    before_by_id={v["venue_id"]:v for v in global_venues}
    after_by_id={v["venue_id"]:v for v in rebased_global}
    require(len(before_by_id)==len(global_venues),
            "PHASE0_PREVIEW_DUPLICATE_CURRENT_GLOBAL_VENUE_ID")
    require(len(after_by_id)==len(rebased_global),
            "PHASE0_PREVIEW_DUPLICATE_PROJECTED_GLOBAL_VENUE_ID")
    require(all(after_by_id.get(k)==v for k,v in before_by_id.items()),
            "PHASE0_PREVIEW_REWRITES_EXISTING_GLOBAL_VENUE")
    registered=[v for k,v in after_by_id.items() if k not in before_by_id]
    global_report=json.loads((frozen/STAGE1_REPORT).read_bytes())
    new_expected=global_report["global_venue_reconciliation"]["counts"][
        "NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED"]
    require(len(registered)==new_expected,
            "PHASE0_PREVIEW_GLOBAL_REGISTRATION_COUNT_CHANGED")
    candidate={name:(frozen/name).read_bytes() for name in PACKAGE_FILES}
    candidate["venues.csv"]=render_csv(venue_fields,rebased_local)
    # These are staged bytes only. Reference CSV serialization is deterministic.
    global_changes={
        "data/reference/programs.csv":render_csv(program_fields,post_programs),
        "data/reference/venues.csv":render_csv(global_venue_fields,rebased_global),
        "data/reference/venue-names.csv":render_csv(global_name_fields,rebased_names),
    }
    checked_programs=csv_rows(global_changes["data/reference/programs.csv"],"proposed programs")[1]
    require([r for r in checked_programs if r["program_key"]!=school] ==
            [r for r in program_rows if r["program_key"]!=school],
            "PHASE0_PREVIEW_UNRELATED_PROGRAM_REGISTRY_CHANGE")
    frozen_ids=[r["source_game_id"] for r in sources]
    _,reparsed=csv_rows(candidate["source-games.csv"],"rebased source games")
    require([r["source_game_id"] for r in reparsed]==frozen_ids
            and reparsed==sources,
            "PHASE0_PREVIEW_SOURCE_EVIDENCE_CHANGED")
    require(git_revision(repo,"refs/remotes/origin/main")==main,
            "PHASE0_PREVIEW_CURRENT_MAIN_MOVED_DURING_REBASE")
    proposal={
        "schema_version":1,
        "kind":"ALL_HISTORY_EXPANSION_PHASE0_DISPOSABLE_PREVIEW",
        "status":"DISPOSABLE_ONLY_NOT_PUBLISHED",
        "school_key":school,
        "protected_main_sha":main,
        "research_base_sha":manifest["research_base_sha"],
        "integration_freeze_sha256":sha256((frozen/MANIFEST_NAME).read_bytes()),
        "source_game_count":len(sources),
        "inherited_source_game_count":manifest["source_preservation"]["inherited_count"],
        "supplemental_source_game_count":manifest["source_preservation"]["supplemental_count"],
        "global_venue_registration_count":len(registered),
        "new_global_venue_ids_and_keys":[{"venue_id":x["venue_id"],
                    "venue_key":x["venue_key"]} for x in registered],
        "rebased_venue_mapping_count":len(venue_mappings),
        "alias_reconciliation_count":len(alias_actions),
        "six_file_preview_sha256":{n:sha256(data) for n,data in sorted(candidate.items())},
        "global_reference_preview_sha256":{n:sha256(data) for n,data in sorted(global_changes.items())},
        "permitted_new_coverage_status":"COMPLETE_INSTITUTIONAL",
        "protected_top_level_and_accomplishments":"UNCHANGED",
        "required_guards":manifest["required_phase0_guards"],
        "lock_acquired":False,
        "writeahead_persisted":False,
        "branch_published":False,
        "owner_gate_1_approved":False,
        "authorized_live_mutation":False,
        "residual_blocker":"REMOTE_EXPANSION_PHASE0_TRANSACTION_PATH_NOT_WIRED",
    }
    output.mkdir(parents=True)
    for name,data in candidate.items():
        (output/name).write_bytes(data)
    references=output/"references"
    references.mkdir()
    for name,data in global_changes.items():
        (references/Path(name).name).write_bytes(data)
    (output/"phase0-preview.json").write_bytes(canonical_bytes(proposal))
    return proposal


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo",type=Path,required=True)
    p.add_argument("--integration-freeze",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        result=preview_phase0(args.repo,args.integration_freeze,args.output)
        print(json.dumps({k:result[k] for k in (
            "status","global_venue_registration_count","source_game_count",
            "rebased_venue_mapping_count","residual_blocker")},sort_keys=True))
        return 0
    except (IntegrationAuthorityError,WorkflowError,ValueError,OSError,KeyError) as exc:
        print("STOP: "+str(exc),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
