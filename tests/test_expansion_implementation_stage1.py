"""Fail-closed Stage 1 adapter tests. Synthetic authority is never published."""
import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from expansion_implementation_stage1 import (
    Stage1Stop, build_candidate, csv_rows, materialize_support,
    prepare_current_main_identity_rebase, reconcile_canonical, render_csv,
    sha256, stage1,
)
from all_history_expansion_freeze import canonical_row_sha256, OPPONENT_EXTENSION_FIELDS


def support(action, candidate, original=None, changed="", identity_label="A"):
    return {"support_id": "support-" + identity_label, "support_action": action,
            "source_opponent_label": candidate["source_opponent_label"],
            "canonical_opponent_key": candidate["canonical_opponent_key"],
            "baseline_row_sha256": canonical_row_sha256(original) if original is not None else "",
            "changed_fields": changed, "candidate_row_json": json.dumps(candidate),
            "evidence_basis": "mock fixture"}


class Stage1FoundationTests(unittest.TestCase):
    def setUp(self):
        self.original = {"source_program_key":"sample", "source_opponent_label":"Team A",
                         "canonical_opponent_key":"a", "audit_note":"old", "games_currently_assigned":"1"}
        self.opp_fields = list(self.original)
        self.source1 = {"source_game_id":"OLD-1", "source_program_key":"sample",
                        "season_label":"1978-1979", "normalized_opponent_key":"a", "game_date":"1978-12-01",
                        "team_score":"60", "opponent_score":"40"}
        self.source2 = {**self.source1, "source_game_id":"NEW-1", "season_label":"1966-1967"}
        self.venue = {"venue_key":"hall", "source_program_key":"sample", "notes":"old",
                      "games_currently_assigned":"1"}

    def test_reuse_inherited_is_nonmutating(self):
        original = self.original.copy()
        rows, counts, _ = materialize_support([original], self.opp_fields,
            [support("REUSE_INHERITED", original, original)],
            ("source_opponent_label", "canonical_opponent_key"), OPPONENT_EXTENSION_FIELDS,"opponent")
        self.assertEqual(rows, [original])
        self.assertEqual(counts["REUSE_INHERITED"],1)
        self.assertEqual(self.original, original)

    def test_allowed_extension_is_additive_and_does_not_touch_baseline(self):
        original = self.original.copy()
        extension = {**original,"audit_note":"old; new evidence"}
        rows, counts, _ = materialize_support([original],self.opp_fields,
            [support("EXTEND_INHERITED", extension, original, "audit_note")],
            ("source_opponent_label", "canonical_opponent_key"), OPPONENT_EXTENSION_FIELDS,"opponent")
        self.assertEqual(rows,[extension]);self.assertEqual(original,self.original)
        self.assertEqual(counts["EXTEND_INHERITED"],1)

    def test_changed_baseline_rejected(self):
        candidate={**self.original,"audit_note":"new"}
        item=support("EXTEND_INHERITED",candidate,self.original,"audit_note")
        item["baseline_row_sha256"]="0"*64
        with self.assertRaisesRegex(Stage1Stop,"hash changed"):
            materialize_support([self.original],self.opp_fields,[item],
                ("source_opponent_label","canonical_opponent_key"),OPPONENT_EXTENSION_FIELDS,"opponent")

    def test_unsupported_extension_rejected(self):
        item=support("EXTEND_INHERITED",{**self.original,"canonical_opponent_key":"renamed"},self.original,"canonical_opponent_key")
        with self.assertRaises(Stage1Stop):
            materialize_support([self.original],self.opp_fields,[item],
                ("source_opponent_label","canonical_opponent_key"),OPPONENT_EXTENSION_FIELDS,"opponent")

    def test_new_support_collision_and_duplicate_identity_refused(self):
        item=support("NEW_SUPPLEMENTAL",self.original)
        with self.assertRaisesRegex(Stage1Stop,"collides"):
            materialize_support([self.original],self.opp_fields,[item],
                ("source_opponent_label","canonical_opponent_key"),OPPONENT_EXTENSION_FIELDS,"opponent")
        distinct={**self.original,"source_opponent_label":"Team B"}
        two=[support("NEW_SUPPLEMENTAL",distinct,identity_label="1"),support("NEW_SUPPLEMENTAL",distinct,identity_label="2")]
        with self.assertRaisesRegex(Stage1Stop,"duplicate"):
            materialize_support([self.original],self.opp_fields,two,
                ("source_opponent_label","canonical_opponent_key"),OPPONENT_EXTENSION_FIELDS,"opponent")

    def fixture(self):
        b={"source_fields":list(self.source1),"source_rows":[self.source1],
            "opponent_fields":self.opp_fields,"opponent_rows":[self.original],
            "venue_fields":list(self.venue),"venue_rows":[self.venue]}
        b["package_bytes"]={"source-games.csv":render_csv(b["source_fields"],b["source_rows"]),
             "opponents.csv":render_csv(self.opp_fields,[self.original]),
             "venues.csv":render_csv(list(self.venue),[self.venue]),
             "conferences.csv":b"school,conference\nsample,Independent\n",
             "notes.md":b"Original notes\n", "source-notes.md":b"Original source notes\n"}
        new_opp={**self.original,"source_opponent_label":"Team B","canonical_opponent_key":"b"}
        v={"source_game_id":"NEW-1", "source_program_key":"sample", "season_label":"1966-1967",
           "normalized_opponent_key":"b", "game_date":"1966-12-01", "team_score":"60", "opponent_score":"40"}
        validated={"source_rows":[v],"opponent_support_rows":[support("NEW_SUPPLEMENTAL",new_opp)],
                   "venue_support_rows":[], "season_accounting_rows":[],"non_d1_scan_rows":[],"residual_rows":[]}
        payload={"expansion-notes.md":b"Additional historical notes\n",
                 "expansion-source-notes.md":b"Additional source notes\n"}
        return b,validated,payload

    def test_complete_candidate_preserves_inherited_ids_and_conference(self):
        base,valid,payload=self.fixture()
        candidate,census=build_candidate(base,payload,valid)
        _,sources=csv_rows(candidate["source-games.csv"],"candidate")
        self.assertEqual([r["source_game_id"] for r in sources],["OLD-1","NEW-1"])
        self.assertEqual(sources[0],self.source1)
        self.assertEqual(candidate["conferences.csv"],base["package_bytes"]["conferences.csv"])
        self.assertTrue(candidate["notes.md"].startswith(base["package_bytes"]["notes.md"]))
        self.assertEqual(census["opponent_support_actions"]["NEW_SUPPLEMENTAL"],1)

    def test_duplicate_source_game_id_rejected(self):
        base,valid,payload=self.fixture()
        valid["source_rows"][0]["source_game_id"]="OLD-1"
        with self.assertRaisesRegex(Stage1Stop,"Duplicate"):
            build_candidate(base,payload,valid)

    def test_existing_canonical_reuse_and_ambiguity(self):
        src={**self.source2, "normalized_opponent_key":"a"}
        can={"canonical_game_id":"CB-1","season_label":"1966-1967","team_a_key":"a","team_b_key":"sample",
             "team_a_score":"40","team_b_score":"60","game_date":"1978-12-01"}
        src["game_date"]="1978-12-01"
        match=reconcile_canonical("sample",[src],[can])
        self.assertEqual(match["counts"]["REUSE_CANONICAL"],1)
        self.assertEqual(match["game_rows"][0]["canonical_game_id"],"CB-1")
        multiple=reconcile_canonical("sample",[src],[can,{**can,"canonical_game_id":"CB-2"}])
        self.assertEqual(multiple["counts"]["IDENTITY_REVIEW_BLOCKER"],1)

    def test_new_game_is_provisional_not_published(self):
        match=reconcile_canonical("sample",[self.source2],[])
        self.assertEqual(match["counts"]["PROVISIONAL_NEW_CANONICAL"],1)
        self.assertEqual(match["game_rows"][0]["canonical_game_id"],"")

    def test_no_output_under_repository_or_over_existing_output(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            with self.assertRaisesRegex(Stage1Stop,"outside"):
                stage1(root,"sample",root/"artifact.zip","", "", "",root/"inside")
            with self.assertRaisesRegex(Stage1Stop,"already exists"):
                stage1(root,"sample",root/"artifact.zip","", "", "",root.parent)

    def test_reject_modified_or_unauthenticated_freeze_before_projection(self):
        from unittest.mock import patch
        from expansion_implementation_stage1 import stage1
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp)
            artifact=root/"freeze.zip";artifact.write_bytes(b"tampered")
            with patch("expansion_implementation_stage1.git_revision",return_value="a"*40):
                with self.assertRaisesRegex(Stage1Stop,"SHA-256 mismatch"):
                    stage1(root,"sample",artifact,"0"*64,"b"*40,"a"*40,root.parent/"new-expansion-test-output")
        

class CurrentMainIdentityRebaseTests(unittest.TestCase):
    def test_resolved_external_identity_correction_is_preserved_and_extended(self):
        from unittest.mock import patch

        source_fields = [
            "source_game_id", "source_program_key", "season_label",
            "source_opponent_label", "normalized_opponent_key",
            "normalized_opponent_name",
        ]
        old_source = {
            "source_game_id": "OLD-1",
            "source_program_key": "sample",
            "season_label": "1978-1979",
            "source_opponent_label": "SOUTHEASTERN",
            "normalized_opponent_key": "old-key",
            "normalized_opponent_name": "Old Identity",
        }
        current_source = dict(
            old_source,
            normalized_opponent_key="new-key",
            normalized_opponent_name="New Identity",
        )
        opponent_fields = [
            "source_program_key", "source_opponent_label",
            "canonical_opponent_key", "canonical_opponent_name", "current_d1",
            "games_with_source_label", "first_season", "last_season",
            "resolution_status", "resolution_method", "user_choice", "audit_note",
        ]
        old_opponent = {
            "source_program_key": "sample",
            "source_opponent_label": "SOUTHEASTERN",
            "canonical_opponent_key": "old-key",
            "canonical_opponent_name": "Old Identity",
            "current_d1": "Yes",
            "games_with_source_label": "4",
            "first_season": "1973-74",
            "last_season": "1978-79",
            "resolution_status": "RESOLVED_PROJECT_AUTHORITY",
            "resolution_method": "OLD_METHOD",
            "user_choice": "",
            "audit_note": "old authority",
        }
        current_opponent = dict(
            old_opponent,
            canonical_opponent_key="new-key",
            canonical_opponent_name="New Identity",
            current_d1="No",
            resolution_status="RESOLVED_RESEARCHED_IDENTITY",
            resolution_method="LIVE_CORRECTION",
            audit_note="accepted live correction",
        )
        supplemental_opponent = dict(
            current_opponent,
            games_with_source_label="6",
            first_season="1968-69",
            last_season="1972-73",
            resolution_method="EXPANSION_RESEARCH",
            audit_note="frozen expansion evidence",
        )

        package = {
            "source-games.csv": render_csv(source_fields, [old_source]),
            "opponents.csv": render_csv(opponent_fields, [old_opponent]),
            "venues.csv": b"venue_key\n",
            "conferences.csv": b"school,conference\nsample,Independent\n",
            "notes.md": b"notes\n",
            "source-notes.md": b"source notes\n",
        }
        current_package = dict(package)
        current_package["source-games.csv"] = render_csv(
            source_fields, [current_source]
        )
        current_package["opponents.csv"] = render_csv(
            opponent_fields, [current_opponent]
        )
        baseline = {
            "package_bytes": package,
            "source_fields": source_fields,
            "source_rows": [old_source],
            "source_ids": ["OLD-1"],
            "source_game_count": 1,
            "opponent_fields": opponent_fields,
            "opponent_rows": [old_opponent],
            "venue_fields": ["venue_key"],
            "venue_rows": [],
        }
        validated = {
            "opponent_support_rows": [{
                "support_id": "SUP-1",
                "support_action": "NEW_SUPPLEMENTAL",
                "source_opponent_label": "SOUTHEASTERN",
                "canonical_opponent_key": "new-key",
                "baseline_row_sha256": "",
                "changed_fields": "",
                "candidate_row_json": json.dumps(supplemental_opponent),
                "evidence_basis": "frozen evidence",
            }],
            "correction_question_rows": [{
                "inherited_source_game_id": "OLD-1",
                "expansion_impact": "NO_EXPANSION_IMPACT",
                "disposition": "RESOLVED_EXTERNALLY: accepted correction is already live",
            }],
        }

        def git_show(_repo, _sha, path):
            return current_package[path.rsplit("/", 1)[-1]]

        with patch(
            "expansion_implementation_stage1.git_bytes",
            side_effect=git_show,
        ):
            rebased, adjusted, metadata, blockers = (
                prepare_current_main_identity_rebase(
                    Path("/tmp/repo"),
                    "sample",
                    "a" * 40,
                    baseline,
                    validated,
                )
            )

        self.assertEqual(blockers, [])
        self.assertEqual(
            metadata["status"],
            "APPLIED_RESOLVED_EXTERNAL_IDENTITY_CORRECTION",
        )
        self.assertEqual(metadata["changed_source_game_ids"], ["OLD-1"])
        self.assertEqual(rebased["source_rows"], [current_source])
        rewritten = adjusted["opponent_support_rows"][0]
        self.assertEqual(rewritten["support_action"], "EXTEND_INHERITED")
        merged = json.loads(rewritten["candidate_row_json"])
        self.assertEqual(merged["games_with_source_label"], "10")
        self.assertEqual(merged["first_season"], "1968-69")
        self.assertEqual(merged["last_season"], "1978-79")
        self.assertEqual(merged["resolution_method"], "LIVE_CORRECTION")
        self.assertIn("accepted live correction", merged["audit_note"])
        self.assertIn("frozen expansion evidence", merged["audit_note"])



class Stage1AuthenticatedWorkflowTests(unittest.TestCase):
    """Synthetic Git and verifier surfaces test Stage 1 stop boundaries."""

    def _invoke(self, *, drift=False, verify_error=None, accounting_error=None):
        import zipfile
        from unittest.mock import patch
        fixture = Stage1FoundationTests()
        fixture.setUp()
        baseline, validated, payload = fixture.fixture()
        baseline.update({
            "program": {"program_key": "sample"},
            "scope_row": {"school": "Sample"},
            "accomplishment_row": None,
            "published_canonical_ids": [],
            "package_member_sha256": {k: sha256(v) for k, v in baseline["package_bytes"].items()},
        })
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            repo = root / "checkout"
            repo.mkdir()
            artifact = root / "accepted.zip"
            with zipfile.ZipFile(artifact, "w") as archive:
                archive.writestr("expansion-freeze.json", json.dumps({
                    "researched_inception_season": "1966-1967", "schema_version": 1,
                }))
                for name, raw in payload.items():
                    archive.writestr(name, raw)
            main = "a" * 40
            base = "b" * 40
            expected = sha256(artifact.read_bytes())
            output = root / "rehearsal"

            def git_show(_repo, commit, path):
                name = path.rsplit("/", 1)[-1]
                if name in baseline["package_bytes"]:
                    content = baseline["package_bytes"][name]
                    if drift and commit == main and name == "source-games.csv":
                        return content + b"current-main-drift"
                    return content
                raise AssertionError(path)

            def read_rows(_repo, _sha, path):
                if path.endswith("programs.csv"):
                    return [baseline["program"]]
                if path.endswith("program-top-level-scope.csv"):
                    return [baseline["scope_row"]]
                return []

            def verification(_repo, _artifact):
                if verify_error:
                    raise ValueError(verify_error)
                return {"status": "VERIFIED_EXPANSION_RESEARCH_FROZEN",
                        "school_key": "sample", "research_base_sha": base}

            def validated_delta(*_args):
                if accounting_error:
                    raise ValueError(accounting_error)
                return validated

            with patch("expansion_implementation_stage1.git_revision", return_value=main), \
                 patch("expansion_implementation_stage1.git_bytes", side_effect=git_show), \
                 patch("expansion_implementation_stage1.read_csv_at_git", side_effect=read_rows), \
                 patch("expansion_implementation_stage1.verify_expansion", side_effect=verification), \
                 patch("expansion_implementation_stage1.authenticate_baseline", return_value=baseline), \
                 patch("expansion_implementation_stage1.validate_delta_payload", side_effect=validated_delta):
                if verify_error or accounting_error:
                    with self.assertRaisesRegex(ValueError, verify_error or accounting_error):
                        stage1(repo, "sample", artifact, expected, base, main, output)
                    self.assertFalse(output.exists(), "Rejected inputs cannot materialize candidate")
                    return None
                result = stage1(repo, "sample", artifact, expected, base, main, output)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertEqual(result["write_authority"], "NONE_REHEARSAL_ONLY")
                self.assertFalse((repo / "schools").exists())
                self.assertTrue((output / "expansion-stage1-reconciliation.json").exists())
                return result

    def test_changed_inherited_package_is_explicit_blocker(self):
        result = self._invoke(drift=True)
        self.assertIn("CURRENT_MAIN_INHERITED_PACKAGE_DRIFT",
                      [b["class"] for b in result["blockers"]])

    def test_modified_member_fails_permanent_freeze_verification(self):
        self._invoke(verify_error="frozen payload member SHA-256 map mismatch")

    def test_missing_season_accounting_fails_before_projection(self):
        self._invoke(accounting_error="season accounting mismatch")

    def test_unblocked_source_projection_still_cannot_publish(self):
        result = self._invoke()
        self.assertEqual([b["class"] for b in result["blockers"]], [
            "DOWNSTREAM_EXPANSION_INTEGRATION_FREEZE_AND_GUARDED_PHASE0_MISSING"])


class GlobalVenueReconciliationTests(unittest.TestCase):
    def row(self, key="town-hall", name="Town Hall", city="Midtown", state="VA", vid=""):
        return {"support_id": "venue-1", "support_action": "NEW_SUPPLEMENTAL",
                "venue_key": key,
                "candidate_row_json": json.dumps({
                    "venue_key": key, "venue_id": vid,
                    "canonical_name": name, "city": city, "state": state})}

    def global_row(self, key="town-hall", name="Town Hall", city="Midtown", state="VA", vid="VEN-000001"):
        return {"venue_key": key, "venue_id": vid, "display_name": name,
                "city": city, "state": state}

    def run_census(self, supp, global_rows):
        from expansion_implementation_stage1 import reconcile_global_venues
        return reconcile_global_venues(supp, global_rows)

    def test_registered_physical_identity_reused_with_blank_candidate_id(self):
        result = self.run_census([self.row()], [self.global_row()])
        self.assertEqual(result["counts"]["REUSE_REGISTERED_GLOBAL_VENUE"], 1)
        self.assertEqual(result["rows"][0]["existing_global_venue_id"], "VEN-000001")
        self.assertEqual(result["blockers"], [])

    def test_new_school_venue_requires_future_global_registration(self):
        result = self.run_census([self.row()], [])
        self.assertEqual(result["counts"]["NEW_GLOBAL_VENUE_REGISTRATION_REQUIRED"], 1)
        self.assertEqual(result["rows"][0]["existing_global_venue_id"], "")
        self.assertFalse(result["blockers"])

    def test_conflicting_geography_is_not_silent_reuse(self):
        result = self.run_census([self.row(city="Elsewhere")], [self.global_row()])
        self.assertEqual(result["counts"]["GLOBAL_VENUE_IDENTITY_REVIEW_BLOCKER"], 1)
        self.assertIn("REGISTERED_VENUE_GEOGRAPHY_REVIEW", [b["class"] for b in result["blockers"]])

    def test_conflicting_global_id_is_not_reassigned(self):
        result = self.run_census([self.row(vid="VEN-999999")], [self.global_row()])
        self.assertIn("REGISTERED_VENUE_ID_CONFLICT", [b["class"] for b in result["blockers"]])

    def test_conflicting_canonical_name_requires_review(self):
        result = self.run_census([self.row(name="Another Building")], [self.global_row()])
        self.assertIn("REGISTERED_VENUE_NAME_REVIEW", [b["class"] for b in result["blockers"]])

    def test_duplicate_registered_global_venue_keys_are_rejected(self):
        result = self.run_census([self.row()], [self.global_row(), self.global_row(vid="VEN-000002")])
        self.assertIn("DUPLICATE_GLOBAL_VENUE_KEY", [b["class"] for b in result["blockers"]])

    def test_new_candidate_cannot_reuse_id_of_different_venue(self):
        result = self.run_census([self.row(vid="VEN-000001")],
                                 [self.global_row(key="other-key")])
        self.assertIn("GLOBAL_VENUE_ID_USED_BY_DIFFERENT_KEY",
                      [b["class"] for b in result["blockers"]])

if __name__=="__main__":
    unittest.main()
