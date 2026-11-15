"""Generic expansion Integration Freeze and guarded Phase 0 preparation tests."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1] / "tools"))
from all_history_expansion_integration import (
    IntegrationAuthorityError, MANIFEST_NAME, PACKAGE_FILES, PROPOSAL_NAME,
    SCOPE_REFERENCE_PATH, STAGE1_REPORT, authenticate_proof, canonical_bytes,
    freeze_authority, metadata_projection, phase0_packet, sha256,
    source_preservation, verify_manifest_bytes,
)


class ExpansionIntegrationAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.source_fields = ["source_game_id","season_label","source_program_key"]
        self.old = {"source_game_id":"OLD-1","season_label":"1978-1979",
                    "source_program_key":"sample"}
        self.new = {"source_game_id":"NEW-1","season_label":"1966-1967",
                    "source_program_key":"sample"}
        self.baseline={"source_fields":self.source_fields,"source_rows":[self.old]}
        self.report={
            "census":{"inherited_source_game_count":1,
                      "supplemental_new_source_game_count":1,
                      "combined_source_game_count":2,
                      "opponent_support_actions":{"NEW_SUPPLEMENTAL":1,
                           "EXTEND_INHERITED":0,"REUSE_INHERITED":0},
                      "venue_support_actions":{"NEW_SUPPLEMENTAL":0,
                           "EXTEND_INHERITED":1,"REUSE_INHERITED":0}},
            "canonical_identity_census":{"counts":{"REUSE_CANONICAL":0,
                  "PROVISIONAL_NEW_CANONICAL":1,"IDENTITY_REVIEW_BLOCKER":0}},
            "global_venue_reconciliation":{"counts":{
                  "REUSE_REGISTERED_GLOBAL_VENUE":1,
                  "NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED":0,
                  "GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER":0}},
            "blockers":[{"class":"DOWNSTREAM_EXPANSION_INTEGRATION_FREEZE_AND_GUARDED_PHASE0_MISSING"}]
        }
        self.sha1 = "a"*40
        self.sha2 = "b"*40
        self.sha3 = "c"*64

    def csv_sources(self, rows):
        stream=io.StringIO(newline="")
        writer=csv.DictWriter(stream,fieldnames=self.source_fields,lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        return stream.getvalue().encode()

    def test_preserves_inherited_rows_and_all_source_ids(self):
        guard=source_preservation(self.baseline,self.csv_sources([self.old,self.new]),
                                  self.report,{})
        self.assertEqual(guard["inherited_count"],1)
        self.assertEqual(guard["combined_count"],2)
        self.assertEqual(guard["inherited_rows_sha256"],sha256(canonical_bytes([self.old])))

    def test_refuses_rewritten_inherited_rows(self):
        changed=dict(self.old,season_label="1969-1970")
        with self.assertRaisesRegex(IntegrationAuthorityError,"INHERITED_SOURCE_ROWS_CHANGED"):
            source_preservation(self.baseline,self.csv_sources([changed,self.new]),
                                self.report,{})

    def test_refuses_duplicate_inherited_id(self):
        with self.assertRaisesRegex(IntegrationAuthorityError,"COMBINED_SOURCE_ID_COLLISION"):
            source_preservation(self.baseline,self.csv_sources([self.old,dict(self.new,source_game_id="OLD-1")]),
                                self.report,{})

    def test_refuses_missing_source(self):
        with self.assertRaisesRegex(IntegrationAuthorityError,"SUPPLEMENTAL_SOURCE_COUNT_DRIFT"):
            source_preservation(self.baseline,self.csv_sources([self.old]),self.report,{})

    def good_proof(self):
        return {
            "status":"INDEPENDENTLY_REPRODUCED_READ_ONLY_STAGE1",
            "protected_main_sha":self.sha1,
            "research_base_sha":self.sha2,
            "freeze_zip_sha256":self.sha3,
            "candidate_sha256":{"source-games.csv":"9"*64},
            "identity_counts":self.report["canonical_identity_census"]["counts"],
            "global_venue_counts":self.report["global_venue_reconciliation"]["counts"],
            "support_opponents":self.report["census"]["opponent_support_actions"],
            "support_venues":self.report["census"]["venue_support_actions"],
            "blockers":self.report["blockers"],
            "integration_freeze_authorized":False
        }

    def authenticate(self,proof):
        authenticate_proof(proof,self.report,{"source-games.csv":"9"*64},
                           self.sha1,self.sha2,self.sha3)

    def test_exact_independent_proof_accepted(self):
        self.authenticate(self.good_proof())

    def test_proof_hash_mismatch_refused(self):
        proof=self.good_proof()
        proof["candidate_sha256"]["source-games.csv"]="e"*64
        with self.assertRaisesRegex(IntegrationAuthorityError,"HASH_MISMATCH"):
            self.authenticate(proof)

    def test_proof_current_main_drift_refused(self):
        proof=self.good_proof()
        proof["protected_main_sha"]="d"*40
        with self.assertRaisesRegex(IntegrationAuthorityError,"PROOF_BINDING"):
            self.authenticate(proof)

    def test_canonical_reuse_or_ambiguity_count_drift_refused(self):
        proof=self.good_proof()
        proof["identity_counts"]=dict(proof["identity_counts"], REUSE_CANONICAL=1)
        with self.assertRaisesRegex(IntegrationAuthorityError,"PROOF_COUNTS"):
            self.authenticate(proof)

    def test_unapproved_mutation_claim_refused(self):
        proof=self.good_proof()
        proof["integration_freeze_authorized"]=True
        with self.assertRaisesRegex(IntegrationAuthorityError,"PREAUTHORIZE"):
            self.authenticate(proof)

    def projection_baseline(self):
        program={
            "program_key":"sample",
            "program_inception_season":"",
            "history_coverage_status":"LEGACY_TOP_LEVEL_ONLY",
            "history_start_season":"1978-1979",
            "history_scope_intervals":"",
            "history_scope_status":"OWNER_CONFIRMED",
            "history_scope_basis":"FIRST_TOP_LEVEL_SEASON",
            "history_scope_notes":"Baseline scope",
        }
        return {
            "program":program,
            "scope_row":{"school":"Sample","top_level_scope":"1978-79+"},
        }

    def test_v1_metadata_projection_preserves_scope(self):
        baseline=self.projection_baseline()
        report={
            "researched_inception_season":"1966-1967",
            "research_freeze_schema_version":1,
            "scope_authority":None,
        }
        program,scope,changed=metadata_projection(baseline,report)
        self.assertEqual(program["program_inception_season"],"1966-1967")
        self.assertEqual(program["history_coverage_status"],"COMPLETE_INSTITUTIONAL")
        self.assertEqual(program["history_start_season"],"1978-1979")
        self.assertEqual(scope,baseline["scope_row"])
        self.assertFalse(changed)

    def test_v2_metadata_projection_applies_only_frozen_target_scope(self):
        baseline=self.projection_baseline()
        target_fields={
            "history_start_season":"1966-1967",
            "history_scope_intervals":"",
            "history_scope_status":"OWNER_CONFIRMED",
            "history_scope_basis":"ALWAYS_TOP_LEVEL_FROM_INCEPTION",
            "history_scope_notes":"Owner accepted INCEPTION+",
        }
        report={
            "researched_inception_season":"1966-1967",
            "research_freeze_schema_version":2,
            "scope_authority":{
                "baseline_scope":"1978-79+",
                "accepted_scope":"INCEPTION+",
                "target_program_scope_fields":target_fields,
            },
        }
        program,scope,changed=metadata_projection(baseline,report)
        self.assertTrue(changed)
        self.assertEqual(scope,{"school":"Sample","top_level_scope":"INCEPTION+"})
        for key,value in target_fields.items():
            self.assertEqual(program[key],value)
        self.assertEqual(program["history_coverage_status"],"COMPLETE_INSTITUTIONAL")

    def test_v2_metadata_projection_requires_authenticated_scope_authority(self):
        baseline=self.projection_baseline()
        with self.assertRaisesRegex(
            IntegrationAuthorityError,"FREEZE_V2_SCOPE_AUTHORITY_MISSING"
        ):
            metadata_projection(baseline,{
                "researched_inception_season":"1966-1967",
                "research_freeze_schema_version":2,
                "scope_authority":None,
            })

    def test_v2_metadata_projection_rejects_unbound_program_scope_fields(self):
        baseline=self.projection_baseline()
        with self.assertRaisesRegex(
            IntegrationAuthorityError,"SCOPE_PROGRAM_PROJECTION_FIELDS_INVALID"
        ):
            metadata_projection(baseline,{
                "researched_inception_season":"1966-1967",
                "research_freeze_schema_version":2,
                "scope_authority":{
                    "baseline_scope":"1978-79+",
                    "accepted_scope":"INCEPTION+",
                    "target_program_scope_fields":{"history_start_season":"1966-1967"},
                },
            })

    def make_manifest(self,root):
        root.mkdir()
        for member in PACKAGE_FILES:
            (root/member).write_bytes(b"some deterministic candidate bytes\n")
        (root/STAGE1_REPORT).write_bytes(b"{}\n")
        manifest={
            "kind":"ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
            "status":"INTEGRATION_FROZEN","school_key":"sample",
            "protected_main_sha":self.sha1,"research_base_sha":self.sha2,
            "tracked_mutation":"NONE","release_authority":False,
            "required_phase0_guards":["GLOBAL_IMPLEMENTATION_MUTATION_LOCK",
                    "CURRENT_MAIN_SHA_MATCH","EXPECTED_PREDECESSOR_CAS",
                    "DURABLE_WRITEAHEAD_BEFORE_PUBLICATION",
                    "INDEPENDENT_EXACT_TREE_REPLAY"],
            "candidate_member_sha256":{
                n:sha256((root/n).read_bytes()) for n in PACKAGE_FILES
            },
            "stage1_report_sha256":sha256((root/STAGE1_REPORT).read_bytes()),
            "manifest_self_fingerprint_sha256":"",
        }
        manifest["manifest_self_fingerprint_sha256"]=sha256(canonical_bytes(manifest))
        (root/MANIFEST_NAME).write_bytes(canonical_bytes(manifest))
        return manifest

    def test_manifest_verification_accepts_unchanged_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"f"
            original=self.make_manifest(path)
            actual=verify_manifest_bytes((path/MANIFEST_NAME).read_bytes(),path)
            self.assertEqual(actual,original)

    def test_manifest_modification_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"f"
            self.make_manifest(path)
            m=json.loads((path/MANIFEST_NAME).read_bytes())
            m["release_authority"]=True
            with self.assertRaisesRegex(IntegrationAuthorityError,"SELF_FINGERPRINT"):
                verify_manifest_bytes(canonical_bytes(m),path)

    def test_manifest_binds_exact_venue_reconciliation_sidecar(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"f"
            manifest=self.make_manifest(path)
            sidecar=b'{"schema_version":2,"school_key":"sample"}\n'
            sidecar_sha=sha256(sidecar)
            (path/"venue-reconciliation.json").write_bytes(sidecar)
            manifest["venue_reconciliation"]={
                "schema_version":2,
                "spec_path":"venue-reconciliation.json",
                "spec_sha256":sidecar_sha,
                "owner_approval_basis":"durable resolution",
                "research_zip_sha256":"f"*64,
                "frozen_venues_sha256":"e"*64,
                "mappings":[],
            }
            manifest["venue_reconciliation_sha256"]=sidecar_sha
            manifest["venue_reconciliation_census"]={
                "schema_version":1,"venue_count":0,
                "classification_counts":{},"blocker_count":0,
                "blockers":[],"rows":[],
            }
            manifest["manifest_self_fingerprint_sha256"]=""
            manifest["manifest_self_fingerprint_sha256"]=sha256(canonical_bytes(manifest))
            raw=canonical_bytes(manifest)
            self.assertEqual(
                verify_manifest_bytes(raw,path)["venue_reconciliation_sha256"],
                sidecar_sha,
            )
            (path/"venue-reconciliation.json").write_bytes(b"tampered")
            with self.assertRaisesRegex(
                IntegrationAuthorityError,
                "VENUE_RECONCILIATION_CHANGED",
            ):
                verify_manifest_bytes(raw,path)

    def test_candidate_content_modification_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"f"
            self.make_manifest(path)
            (path/"source-games.csv").write_text("tampered")
            with self.assertRaisesRegex(IntegrationAuthorityError,"CANDIDATE_CHANGED"):
                verify_manifest_bytes((path/MANIFEST_NAME).read_bytes(),path)

    def test_report_modification_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/"f"
            self.make_manifest(path)
            (path/STAGE1_REPORT).write_text('{"tampered":true}')
            with self.assertRaisesRegex(IntegrationAuthorityError,"STAGE1_REPORT_CHANGED"):
                verify_manifest_bytes((path/MANIFEST_NAME).read_bytes(),path)

    def test_phase0_packet_cannot_apply_or_bypass_lock(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/"f"
            self.make_manifest(folder)
            packet=phase0_packet(folder,Path(tmp)/"packet.json")
            self.assertEqual(packet["mutation_authority"],"NONE")
            self.assertEqual(packet["status"],"PREPARATION_ONLY")
            self.assertFalse(packet["phase0_executed"])
            self.assertEqual(packet["terminal_blocker"],"GUARDED_EXPANSION_PHASE0_RUNNER_NOT_ACTIVATED")
            self.assertIn("GLOBAL_IMPLEMENTATION_MUTATION_LOCK",
                          packet["required_transaction_guards"])
            self.assertIn("EXPECTED_PREDECESSOR_CAS",
                          packet["required_transaction_guards"])
            self.assertIn("DURABLE_WRITEAHEAD_BEFORE_PUBLICATION",
                          packet["required_transaction_guards"])

    def test_phase0_packet_includes_scope_path_only_when_frozen(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/"f"
            manifest=self.make_manifest(folder)
            manifest["scope_mutation_authorized"]=True
            manifest["manifest_self_fingerprint_sha256"]=""
            manifest["manifest_self_fingerprint_sha256"]=sha256(canonical_bytes(manifest))
            (folder/MANIFEST_NAME).write_bytes(canonical_bytes(manifest))
            packet=phase0_packet(folder,Path(tmp)/"packet.json")
            self.assertIn(SCOPE_REFERENCE_PATH,packet["allowed_changed_paths"])

    def test_phase0_packet_refuses_overwriting_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/"f"
            self.make_manifest(folder)
            out=Path(tmp)/"packet.json"
            out.write_text("prior")
            with self.assertRaisesRegex(IntegrationAuthorityError,"REFUSE_OVERWRITE"):
                phase0_packet(folder,out)

    def test_phase0_packet_refuses_bad_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder=Path(tmp)/"f"
            self.make_manifest(folder)
            (folder/"notes.md").write_text("corrupted")
            with self.assertRaisesRegex(IntegrationAuthorityError,"CANDIDATE_CHANGED"):
                phase0_packet(folder,Path(tmp)/"packet.json")

    def test_output_must_be_outside_repo(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp)/"repo"
            repo.mkdir()
            with self.assertRaisesRegex(IntegrationAuthorityError,"MUST_BE_EXTERNAL"):
                freeze_authority(repo,"sample",repo/"fake.zip",self.sha3,
                    self.sha2,self.sha1,repo/"proof.json",self.sha3,repo/"inside")

    def test_proof_sha_checked_before_any_repository_work(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            proof=root/"proof.json"
            proof.write_text("{}")
            artifact=root/"freeze.zip"
            artifact.write_bytes(b"does not matter")
            with self.assertRaisesRegex(IntegrationAuthorityError,"PROOF_SHA256_MISMATCH"):
                freeze_authority(root,"sample",artifact,self.sha3,
                    self.sha2,self.sha1,proof,self.sha3,root.parent/"unmade-freeze-test")


if __name__=="__main__":
    unittest.main()
