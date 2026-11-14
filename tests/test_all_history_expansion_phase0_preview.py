"""Fail-closed tests for disposable expansion Phase 0 representation projection."""
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from all_history_expansion_integration import (
    MANIFEST_NAME, PACKAGE_FILES, STAGE1_REPORT, IntegrationAuthorityError,
    canonical_bytes, sha256,
)
from all_history_expansion_freeze import canonical_row_sha256
from all_history_expansion_phase0_preview import preview_phase0


def csv_encoded(rows, fields=None):
    fields=fields or list(rows[0])
    s=io.StringIO(newline="")
    w=csv.DictWriter(s,fieldnames=fields,lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return s.getvalue().encode()


class ExpansionPhase0PreviewTests(unittest.TestCase):
    def fixture(self,root):
        frozen=root/"frozen"
        frozen.mkdir()
        source={"source_game_id":"NEW-1","source_program_key":"sample",
                "season_label":"1966-1967"}
        venue={"source_program_key":"sample","venue_key":"gym",
               "venue_id":"","canonical_name":"Sample Gym",
               "city":"Sampleville","state":"VA"}
        program={"program_key":"sample","history_start_season":"1978-1979",
                 "history_coverage_status":"LEGACY_TOP_LEVEL_ONLY",
                 "program_inception_season":"","public_page_enabled":"Yes"}
        target=dict(program,history_coverage_status="COMPLETE_INSTITUTIONAL",
                    program_inception_season="1966-1967")
        artifacts={
            "source-games.csv":csv_encoded([source]),
            "opponents.csv":csv_encoded([{"source_opponent_label":"Opp","canonical_opponent_key":"opp"}]),
            "venues.csv":csv_encoded([venue]),
            "conferences.csv":b"conference_key\n",
            "notes.md":b"Original notes",
            "source-notes.md":b"Source notes",
            STAGE1_REPORT:canonical_bytes({"global_venue_reconciliation":{
                "counts":{"NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED":1}}}),
        }
        for name,raw in artifacts.items():
            (frozen/name).write_bytes(raw)
        inherited=dict(artifacts)
        inherited["source-games.csv"]=csv_encoded([], list(source))
        inherited["opponents.csv"]=csv_encoded([], ["source_opponent_label","canonical_opponent_key"])
        inherited["venues.csv"]=csv_encoded([], list(venue))
        baseline={k:sha256(inherited[k]) for k in PACKAGE_FILES}
        manifest={
            "kind":"ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
            "status":"INTEGRATION_FROZEN",
            "school_key":"sample","protected_main_sha":"a"*40,"research_base_sha":"b"*40,
            "candidate_member_sha256":{k:sha256(artifacts[k]) for k in PACKAGE_FILES},
            "stage1_report_sha256":sha256(artifacts[STAGE1_REPORT]),
            "baseline_package_member_sha256":baseline,
            "baseline_program_row_sha256":canonical_row_sha256(program),
            "opponent_support_actions":{"NEW_SUPPLEMENTAL":1,"EXTEND_INHERITED":0,"REUSE_INHERITED":0},
            "venue_support_actions":{"NEW_SUPPLEMENTAL":1,"EXTEND_INHERITED":0,"REUSE_INHERITED":0},
            "source_preservation":{"combined_count":1,"inherited_count":0,
                                   "supplemental_count":1},
            "frozen_program_projection":target,
            "tracked_mutation":"NONE","release_authority":False,
            "required_phase0_guards":["GLOBAL_IMPLEMENTATION_MUTATION_LOCK",
                 "EXPECTED_PREDECESSOR_CAS","DURABLE_WRITEAHEAD_BEFORE_PUBLICATION"],
            "manifest_self_fingerprint_sha256":"",
        }
        manifest["manifest_self_fingerprint_sha256"]=sha256(canonical_bytes(manifest))
        (frozen/MANIFEST_NAME).write_bytes(canonical_bytes(manifest))
        global_venue={"venue_id":"VEN-000001","venue_key":"older-gym",
                      "display_name":"Older Gym","city":"Elsewhere","state":"VA"}
        new_global={"venue_id":"VEN-000002","venue_key":"gym",
                      "display_name":"Sample Gym","city":"Sampleville","state":"VA"}
        fake_git={}
        for n in PACKAGE_FILES:
            fake_git["schools/sample/"+n]=inherited[n]
        fake_git["data/reference/programs.csv"]=csv_encoded([program])
        fake_git["data/reference/venues.csv"]=csv_encoded([global_venue])
        fake_git["data/reference/venue-names.csv"]=b"venue_id,venue_name\n"
        fake_git["data/reference/program-names.csv"]=b"program_key,alias_name\n"
        return frozen, fake_git, source, venue, global_venue, new_global

    def evaluate(self,root,*,main="a"*40,alter_source=False,register_extra=False,
                 duplicate_inherited_venue=False,
                 accepted_predecessor_rebase=False):
        frozen,files,source,venue,global_old,global_new=self.fixture(root)
        if accepted_predecessor_rebase:
            manifest=json.loads((frozen/MANIFEST_NAME).read_bytes())
            manifest["accepted_predecessor_package_member_sha256"]={
                name:sha256(files["schools/sample/"+name])
                for name in PACKAGE_FILES
            }
            manifest["baseline_package_member_sha256"]=dict(
                manifest["baseline_package_member_sha256"]
            )
            manifest["baseline_package_member_sha256"]["source-games.csv"]="0"*64
            manifest["manifest_self_fingerprint_sha256"]=""
            manifest["manifest_self_fingerprint_sha256"]=sha256(
                canonical_bytes(manifest)
            )
            (frozen/MANIFEST_NAME).write_bytes(canonical_bytes(manifest))
        if duplicate_inherited_venue:
            # Two frozen legacy relationship rows may share a physical venue key;
            # they are inherited authority, not two new venue registrations.
            first=dict(venue,venue_key="legacy-gym",venue_id="VEN-000001",
                       canonical_name="Legacy Gym",relationship_start="1960-1961")
            second=dict(first,relationship_start="1964-1965")
            supplement=dict(venue,relationship_start="")
            fields=list(first)
            original_rows=[first,second]
            files["schools/sample/venues.csv"]=csv_encoded(original_rows,fields)
            (frozen/"venues.csv").write_bytes(csv_encoded(original_rows+[supplement],fields))
            manifest=json.loads((frozen/MANIFEST_NAME).read_bytes())
            manifest["baseline_package_member_sha256"]["venues.csv"]=sha256(
                files["schools/sample/venues.csv"])
            manifest["candidate_member_sha256"]["venues.csv"]=sha256(
                (frozen/"venues.csv").read_bytes())
            manifest["manifest_self_fingerprint_sha256"]=""
            manifest["manifest_self_fingerprint_sha256"]=sha256(canonical_bytes(manifest))
            (frozen/MANIFEST_NAME).write_bytes(canonical_bytes(manifest))
        def rebase(programs,aliases,opp,sources):
            return opp, ([dict(sources[0],season_label="1999-2000")]
                         if alter_source else sources),[]
        def venues(*_args,**_kwargs):
            # The permanent helper mutates its global registry input in place.
            # Exercise that exact topology; the production preview must snapshot
            # the authenticated original list before rebase.
            after=_args[2]
            after.append(global_new)
            if register_extra:
                after.append(dict(global_new,venue_id="VEN-000003",venue_key="third-gym"))
            return [venue],after,_args[3],[{"venue_key":"gym"}]
        with patch("all_history_expansion_phase0_preview.git_revision",return_value=main), \
             patch("all_history_expansion_phase0_preview.git_bytes",side_effect=lambda repo,commit,path:files[path]), \
             patch("all_history_expansion_phase0_preview.load_existing_school_venues",return_value=[]), \
             patch("all_history_expansion_phase0_preview.rebase_program_aliases",side_effect=rebase), \
             patch("all_history_expansion_phase0_preview.rebase_venues",side_effect=venues):
            return preview_phase0(root,frozen,root.parent/"outside-preview")

    def test_disposable_preview_preserves_program_scope_and_source_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"repo";repo.mkdir()
            result=self.evaluate(repo)
            self.assertEqual(result["status"],"DISPOSABLE_ONLY_NOT_PUBLISHED")
            self.assertEqual(result["global_venue_registration_count"],1)
            self.assertFalse(result["lock_acquired"])
            self.assertFalse(result["branch_published"])
            self.assertFalse(result["authorized_live_mutation"])
            self.assertEqual(result["source_game_count"],1)
            self.assertFalse((repo/"schools").exists())

    def test_accepted_current_main_predecessor_can_differ_from_research_base(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"repo";repo.mkdir()
            result=self.evaluate(repo,accepted_predecessor_rebase=True)
            self.assertEqual(result["status"],"DISPOSABLE_ONLY_NOT_PUBLISHED")
            self.assertEqual(result["source_game_count"],1)

    def test_multiple_inherited_venue_relationship_rows_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"repo";repo.mkdir()
            result=self.evaluate(repo,duplicate_inherited_venue=True)
            self.assertEqual(result["inherited_venue_rows_preserved_without_rebase"],2)
            self.assertEqual(result["supplemental_venue_rows_rebased"],1)
            self.assertEqual(result["global_venue_registration_count"],1)

    def test_current_main_drift_stops_without_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"repo";repo.mkdir()
            with self.assertRaisesRegex(IntegrationAuthorityError,"CURRENT_MAIN_CHANGED"):
                self.evaluate(repo,main="d"*40)

    def test_semantic_redistribution_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"repo";repo.mkdir()
            with self.assertRaisesRegex(IntegrationAuthorityError,"SOURCE_SEMANTIC_REBASE"):
                self.evaluate(repo,alter_source=True)

    def test_extra_global_registration_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"repo";repo.mkdir()
            with self.assertRaisesRegex(IntegrationAuthorityError,"REGISTRATION_COUNT_CHANGED"):
                self.evaluate(repo,register_extra=True)


if __name__=="__main__":
    unittest.main()
