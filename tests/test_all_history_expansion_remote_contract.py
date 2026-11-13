"""Acceptance/rejection and no-publication model for expansion transaction contract."""
from __future__ import annotations
import json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))

from all_history_expansion_integration import (
    MANIFEST_NAME,PACKAGE_FILES,STAGE1_REPORT,canonical_bytes,sha256,
    IntegrationAuthorityError,
)
from all_history_expansion_remote_contract import (
    OP_EXPANSION_PHASE0,authenticate_intent,prove_lock_contract,
    inspect_recovery,check_cas,verify_exact_prepared,exact_paths,
)
from remote_implementation_control import initial_control_state


class ExpansionTransactionModelTests(unittest.TestCase):
    def setUp(self):
        self.main="a"*40
        self.target="b"*40
        self.prepared="c"*40
        self.integration_sha=""
        self.research_sha="d"*64
        self.proof_sha="e"*64
        self.school="example"
        self.request={
            "operation":OP_EXPANSION_PHASE0,
            "school_key":self.school,
            "target_branch":"data/example-onboarding",
            "target_sha":self.target,
            "expected_protected_main_sha":self.main,
            "research_freeze_sha256":self.research_sha,
            "stage1_independent_proof_sha256":self.proof_sha,
            "authority":{"expansion_phase0":True,"phase0":False,
                "stage2_census":False,"stage2_sealed_apply":False,
                "owner_gate_1":False,"owner_gate_2":False,
                "recovery":False,"release":False},
        }

    def fixture(self,root):
        freeze=root/"freeze";freeze.mkdir()
        preview=root/"preview";preview.mkdir()
        p={name:(b"candidate-"+name.encode()) for name in PACKAGE_FILES}
        for name,contents in p.items():
            (freeze/name).write_bytes(contents)
            (preview/name).write_bytes(contents)
        (freeze/STAGE1_REPORT).write_bytes(b"{}\n")
        manifest={
            "schema_version":1,"kind":"ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
            "status":"INTEGRATION_FROZEN","tracked_mutation":"NONE",
            "release_authority":False,
            "school_key":self.school,
            "protected_main_sha":self.main,
            "research_freeze_zip_sha256":self.research_sha,
            "independent_stage1_proof_sha256":self.proof_sha,
            "canonical_identity_counts":{"IDENTITY_REVIEW_BLOCKER":0,
                "PROVISIONAL_NEW_CANONICAL":1,"REUSE_CANONICAL":0},
            "global_venue_reconciliation":{
                "GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER":0,
                "NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED":1},
            "venue_support_actions":{"NEW_SUPPLEMENTAL":1},
            "source_preservation":{"inherited_count":1,
                "supplemental_count":1,"combined_count":2},
            "candidate_member_sha256":{name:sha256(contents) for name,contents in p.items()},
            "stage1_report_sha256":sha256(b"{}\n"),
            "manifest_self_fingerprint_sha256":"",
        }
        manifest["manifest_self_fingerprint_sha256"]=sha256(canonical_bytes(manifest))
        raw=canonical_bytes(manifest)
        (freeze/MANIFEST_NAME).write_bytes(raw)
        self.integration_sha=sha256(raw)
        self.request["integration_freeze_sha256"]=self.integration_sha
        globals_={
            "data/reference/programs.csv":b"programs\n",
            "data/reference/venues.csv":b"venues\n",
            "data/reference/venue-names.csv":b"names\n",
        }
        (preview/"references").mkdir()
        for name,contents in globals_.items():
            (preview/"references"/Path(name).name).write_bytes(contents)
        preview_doc={
            "status":"DISPOSABLE_ONLY_NOT_PUBLISHED",
            "integration_freeze_sha256":self.integration_sha,
            "school_key":self.school,
            "protected_main_sha":self.main,
            "source_game_count":2,"inherited_source_game_count":1,
            "supplemental_source_game_count":1,
            "global_venue_registration_count":1,
            "authorized_live_mutation":False,"branch_published":False,
            "lock_acquired":False,
            "venue_identity_census":{"status":"PASS","blocker_count":0,
                "new_support_count":1,"blockers":[]},
            "permitted_new_coverage_status":"COMPLETE_INSTITUTIONAL",
            "protected_top_level_and_accomplishments":"UNCHANGED",
            "six_file_preview_sha256":{k:sha256(v) for k,v in p.items()},
            "global_reference_preview_sha256":{k:sha256(v) for k,v in globals_.items()},
        }
        (preview/"phase0-preview.json").write_bytes(canonical_bytes(preview_doc))
        return freeze,preview,preview_doc

    def authenticate(self,freeze,preview,**kwargs):
        return authenticate_intent(
            request=self.request,current_main=kwargs.get("main",self.main),
            current_target=kwargs.get("target",self.target),
            target_is_ancestor_of_main=kwargs.get("ancestor",True),
            freeze=freeze,phase0_preview=preview,
            original_research_sha256=self.research_sha,
            accepted_stage1_proof_sha256=self.proof_sha,
            exact_freeze_manifest_sha256=self.integration_sha)

    def test_accepted_exact_intent_no_live_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            result=self.authenticate(freeze,preview)
            self.assertEqual(result["status"],"RECONCILED_PREPARATION_ONLY")
            self.assertFalse(result["live_mutation_authority"])
            self.assertEqual(result["expected_target_predecessor_sha"],self.target)
            self.assertEqual(len(result["projected_package_sha256"]),6)

    def test_changed_main_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            with self.assertRaisesRegex(IntegrationAuthorityError,"CURRENT_MAIN_MOVED"):
                self.authenticate(freeze,preview,main="f"*40)

    def test_changed_target_cas_predecessor_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            with self.assertRaisesRegex(IntegrationAuthorityError,"TARGET_PREDECESSOR_CHANGED"):
                self.authenticate(freeze,preview,target="f"*40)

    def test_existing_branch_not_ancestor_of_accepted_main_stops(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            with self.assertRaisesRegex(IntegrationAuthorityError,"PREDECESSOR_NOT_ACCEPTED"):
                self.authenticate(freeze,preview,ancestor=False)

    def test_research_freeze_or_integration_hash_tamper_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            self.request["research_freeze_sha256"]="f"*64
            with self.assertRaisesRegex(IntegrationAuthorityError,"ORIGINAL_RESEARCH"):
                self.authenticate(freeze,preview)
            self.request["research_freeze_sha256"]=self.research_sha
            self.request["integration_freeze_sha256"]="f"*64
            with self.assertRaisesRegex(IntegrationAuthorityError,"INTEGRATION_FREEZE_SHA"):
                self.authenticate(freeze,preview)

    def test_original_stage1_proof_changed_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            self.request["stage1_independent_proof_sha256"]="f"*64
            with self.assertRaisesRegex(IntegrationAuthorityError,"STAGE1_PROOF_CHANGED"):
                self.authenticate(freeze,preview)

    def test_tampered_phase0_candidate_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            (preview/"source-games.csv").write_text("forged source-game")
            with self.assertRaisesRegex(IntegrationAuthorityError,"CANDIDATE_TAMPERED"):
                self.authenticate(freeze,preview)

    def test_historical_venue_identity_blocked(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,view=self.fixture(Path(temp))
            view["venue_identity_census"]={
                "status":"BLOCKED_VENUE_IDENTITY_RECONCILIATION",
                "blocker_count":1,"new_support_count":1,
                "blockers":[{"venue_key":"umbc-fieldhouse",
                             "class":"VENUE_POTENTIAL_EXISTING_PHYSICAL_IDENTITY",
                             "global_venue_id":"VEN-000934"}]}
            (preview/"phase0-preview.json").write_bytes(canonical_bytes(view))
            with self.assertRaisesRegex(ValueError,"VENUE_IDENTITY_RECONCILIATION"):
                self.authenticate(freeze,preview)

    def test_no_owner_gate_stage2_or_release_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            freeze,preview,_=self.fixture(Path(temp))
            self.request["authority"]["owner_gate_1"]=True
            with self.assertRaisesRegex(IntegrationAuthorityError,"UNRELATED_OPERATION"):
                self.authenticate(freeze,preview)

    def test_mutation_lock_owned_and_concurrent_attempt_rejected(self):
        request=dict(self.request,request_id="expansion-test-001")
        state=initial_control_state()
        active=prove_lock_contract(state,request,b"request-bytes","1"*40,"2"*40)
        self.assertEqual(active["active_lock_commit"],"2"*40)
        with self.assertRaisesRegex(IntegrationAuthorityError,"GLOBAL_LOCK_OCCUPIED"):
            prove_lock_contract(active,request,b"request-bytes","1"*40,"3"*40)

    def test_recovery_before_writeahead_classifies_not_attempted(self):
        classification=inspect_recovery(
            expected_target_predecessor=self.target,actual_target=self.target,
            writeahead=None)
        self.assertEqual(classification["safe_next_action"],"ABANDON_WITHOUT_PUBLICATION")

    def test_interrupted_prepared_without_publication_abandoned(self):
        wa={"expected_target_predecessor_sha":self.target,
            "prepared_commit_sha":self.prepared}
        result=inspect_recovery(expected_target_predecessor=self.target,
                                actual_target=self.target,writeahead=wa)
        self.assertEqual(result["safe_next_action"],"ABANDON_PREPARED_UNPUBLISHED")

    def test_published_without_finalization_requires_replay(self):
        wa={"expected_target_predecessor_sha":self.target,
            "prepared_commit_sha":self.prepared}
        result=inspect_recovery(expected_target_predecessor=self.target,
                                actual_target=self.prepared,writeahead=wa)
        self.assertEqual(result["safe_next_action"],
                         "ADOPT_ONLY_AFTER_EXACT_PREPARED_TREE_REPLAY")

    def test_exact_completed_publication_cannot_be_reapplied(self):
        wa={"expected_target_predecessor_sha":self.target,
            "prepared_commit_sha":self.prepared}
        succ={"prepared_commit_sha":self.prepared,
              "actual_published_target_sha":self.prepared,
              "final_transaction_state":"COMPLETE"}
        result=inspect_recovery(expected_target_predecessor=self.target,
                                actual_target=self.prepared,writeahead=wa,successor=succ)
        self.assertEqual(result["safe_next_action"],"NO_REAPPLICATION_PERMITTED")

    def test_concurrent_cas_and_already_published_refused(self):
        check_cas(predecessor=self.target,observed=self.target,prepared=self.prepared)
        for observed in (self.prepared,"f"*40):
            with self.assertRaisesRegex(IntegrationAuthorityError,"CAS_REFUSED"):
                check_cas(predecessor=self.target,observed=observed,prepared=self.prepared)

    def test_diverged_recovery_fail_closed(self):
        with self.assertRaisesRegex(IntegrationAuthorityError,"DIVERGED"):
            inspect_recovery(expected_target_predecessor=self.target,
                             actual_target="f"*40,writeahead=None)

    def test_exact_tree_acceptance_and_rejection(self):
        with tempfile.TemporaryDirectory() as temp:
            frozen,preview,_=self.fixture(Path(temp))
            intent=self.authenticate(frozen,preview)
            expected={
                f"schools/{self.school}/{k}":v
                for k,v in intent["projected_package_sha256"].items()}
            expected.update(intent["projected_global_sha256"])
            paths=sorted({
                f"schools/{self.school}/source-games.csv",
                "data/reference/programs.csv",
            })
            args=dict(intent=intent,prepared_parent_sha=self.main,
                prepared_tree_sha="1"*40,replay_tree_sha="1"*40,
                changed_paths=paths,committed_files_sha256=expected,
                inherited_rows_preserved=True,semantic_guard_hash="2"*64)
            result=verify_exact_prepared(**args)
            self.assertEqual(result["status"],"INDEPENDENT_DISPOSABLE_PREPARED_TREE_EQUIVALENCE")
            self.assertFalse(result["publish_authority"])
            with self.assertRaisesRegex(IntegrationAuthorityError,"TREE_MISMATCH"):
                verify_exact_prepared(**dict(args,replay_tree_sha="3"*40))
            with self.assertRaisesRegex(IntegrationAuthorityError,"INHERITED_ROWS_CHANGED"):
                verify_exact_prepared(**dict(args,inherited_rows_preserved=False))
            with self.assertRaisesRegex(IntegrationAuthorityError,"OUTSIDE_ALLOWLIST"):
                verify_exact_prepared(**dict(args,changed_paths=paths+["data/canonical/games.csv"]))
            with self.assertRaisesRegex(IntegrationAuthorityError,"BLOB_HASH_MISMATCH"):
                verify_exact_prepared(**dict(args,committed_files_sha256={}))

if __name__=="__main__":
    unittest.main()
