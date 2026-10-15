"""Issue #310: correction-only canonical site Gate 1 regression tests."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import onboarding_plan as plan  # noqa: E402


class CorrectionSiteDecisionTests(unittest.TestCase):
    def fixture(self):
        ids = ["ARIZ-1942A", "ARIZ-1942B", "ARIZ-1954", "ARIZ-1959"]
        sources = []
        assertions_by_source = {}
        assertions_by_game = {}
        canon = {}
        pre, post = {}, {}
        for i, sid in enumerate(ids):
            game_id = f"CBBG-{i+1:07d}"
            venue = "Phoenix Union High School Gymnasium" if i < 2 else ""
            old_venue = "" if i < 2 else venue
            site = "NEUTRAL" if i < 2 else "OPPONENT_HOME"
            source = {
                "source_game_id": sid, "source_program_key": "arizona",
                "curated_site_type": site, "curated_venue_name": venue,
                "season_label": "1941-1942" if i < 2 else "1954-1955",
                "game_date": "" if i < 2 else "1954-12-21",
                "notes": ("Owner approved canonical Stanford HOME correction; source preserved."
                          if i >= 2 else "Phoenix venue site correction; source preserved."),
            }
            assertion = dict(source, curated_venue_name=old_venue)
            sources.append(source)
            assertions_by_source[("arizona", sid)] = [assertion]
            assertion["canonical_game_id"] = game_id
            assertions_by_game[game_id] = [assertion]
            canon[game_id] = {
                "canonical_game_id": game_id, "season_label": source["season_label"],
                "game_date": source["game_date"],
                "team_a_key": "arizona",
                "team_b_key": "stanford",
                "site_type": "TEAM_A_HOME",
                "venue_key": "", "venue_id": "",
                "site_city": "", "site_state": "",
            }
            pre[sid] = {
                "curated_site_type": site, "curated_venue_name": old_venue
            }
            post[sid] = {
                "curated_site_type": site, "curated_venue_name": venue
            }
        context = {
            "correction_source_game_ids": set(ids),
            "fields": ["curated_site_type", "curated_venue_name"],
            "pre_rows": pre, "post_rows": post,
        }
        return sources, assertions_by_source, assertions_by_game, canon, context

    def generate(self, context):
        sources, linked, by_game, canonical, _ = self.fixture()
        with (
            patch.object(plan, "_correction_assertion_reconciliation_context",
                         return_value=context),
            patch.object(plan, "assertion_drift", return_value={}),
        ):
            return plan._post_publication_site_review_decisions(
                Path("/not-used"), "arizona", sources, canonical, linked, by_game,
            )

    def test_four_corrected_published_games_become_four_gate_one_reviews(self):
        context = self.fixture()[-1]
        rows = self.generate(context)
        self.assertEqual(len(rows), 4)
        self.assertEqual({r["source_game_id"] for r in rows},
                         context["correction_source_game_ids"])
        self.assertEqual({r["category"] for r in rows},
                         {"correction_site_patch"})
        for item in rows:
            self.assertEqual(item["allowed_actions"], ["APPLY_CANONICAL_PATCH"])
            self.assertEqual(item["canonical_patch_json"], "{}")
            self.assertEqual(item["decision"], "PENDING")

    def test_standard_new_school_has_no_correction_site_decisions(self):
        self.assertEqual(self.generate(None), [])

    def test_non_site_correction_does_not_create_site_review(self):
        sources, linked, by_game, canon, context = self.fixture()
        for i, source in enumerate(sources):
            source["curated_venue_name"] = ""
            source["notes"] = "Approved score correction only."
            context["post_rows"][source["source_game_id"]]["curated_venue_name"] = ""
            context["pre_rows"][source["source_game_id"]]["curated_venue_name"] = ""
        with (
            patch.object(plan, "_correction_assertion_reconciliation_context",
                         return_value=context),
            patch.object(plan, "assertion_drift", return_value={}),
        ):
            rows = plan._post_publication_site_review_decisions(
                Path("/not-used"), "arizona", sources, canon, linked, by_game,
            )
        self.assertEqual(rows, [])

    def test_out_of_scope_source_id_fails_closed(self):
        context = self.fixture()[-1]
        context["correction_source_game_ids"].add("FORGED")
        with self.assertRaisesRegex(plan.WorkflowError, "not in published source scope"):
            self.generate(context)

    def test_unauthorized_source_assertion_drift_blocks(self):
        sources, linked, by_game, canon, context = self.fixture()
        with (
            patch.object(plan, "_correction_assertion_reconciliation_context",
                         return_value=context),
            patch.object(plan, "assertion_drift",
                         return_value={"curated_site_type": ("NEUTRAL", "OPPONENT_HOME")}),
            patch.object(plan, "_is_authorized_correction_assertion_drift",
                         return_value=False),
        ):
            with self.assertRaisesRegex(plan.WorkflowError, "unauthorized assertion drift"):
                plan._post_publication_site_review_decisions(
                    Path("/not-used"), "arizona", sources, canon, linked, by_game,
                )


class CorrectionSiteApprovalTests(unittest.TestCase):
    def review(self, candidate, source_patch=None, decision="APPLY_CANONICAL_PATCH"):
        old = {"site_type": "TEAM_A_HOME", "venue_key": "", "venue_id": "",
               "site_city": "", "site_state": ""}
        item = {
            "decision_id": "CORRECTION-SITE-X",
            "category": "correction_site_patch",
            "allowed_actions": ["APPLY_CANONICAL_PATCH"],
            "source_game_id": "X",
            "canonical_game_id": "CBBG-0000001",
            "canonical_site_expected": old,
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan_path = root / "plan.json"
            review_path = root / "review.csv"
            plan_path.write_text(json.dumps({
                "school_key": "example",
                "input_fingerprint": {"sha256": "fixed"},
                "blockers": [],
                "decisions": [item],
                "summary": {},
            }))
            with review_path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=[
                    "decision_id", "decision", "resolution_basis",
                    "canonical_patch_json", "source_patch_json", "notes"
                ])
                writer.writeheader()
                writer.writerow({
                    "decision_id": "CORRECTION-SITE-X",
                    "decision": decision,
                    "resolution_basis": "Owner-approved institutional site correction",
                    "canonical_patch_json": json.dumps(candidate),
                    "source_patch_json": json.dumps(source_patch or {}),
                    "notes": "",
                })
            with patch.object(plan, "input_fingerprint",
                              return_value={"sha256": "fixed"}):
                return plan.approve_plan(root, plan_path, review_path, "project-owner")

    def test_corrected_site_is_sealed_with_explicit_five_fields(self):
        result, digest = self.review({
            "site_type": "TEAM_B_HOME",
            "venue_key": "", "venue_id": "",
            "site_city": "Stanford", "site_state": "CA",
        })
        self.assertEqual(result["decisions"][0]["canonical_patch"]["site_type"],
                         "TEAM_B_HOME")
        self.assertEqual(len(digest), 64)

    def test_missing_han_is_rejected(self):
        with self.assertRaisesRegex(plan.WorkflowError, "all five canonical site"):
            self.review({
                "venue_key": "", "venue_id": "",
                "site_city": "Stanford", "site_state": "CA",
            })

    def test_source_han_cannot_be_rewritten(self):
        with self.assertRaisesRegex(plan.WorkflowError, "forbids source patches"):
            self.review({
                "site_type": "TEAM_B_HOME",
                "venue_key": "", "venue_id": "",
                "site_city": "Stanford", "site_state": "CA",
            }, source_patch={"curated_site_type": "SOURCE_PROGRAM_HOME"})

    def test_noop_does_not_count_as_implemented_correction(self):
        with self.assertRaisesRegex(plan.WorkflowError, "no-op"):
            self.review({
                "site_type": "TEAM_A_HOME",
                "venue_key": "", "venue_id": "",
                "site_city": "", "site_state": "",
            })

    def test_site_review_cannot_be_skipped(self):
        with self.assertRaisesRegex(plan.WorkflowError, "unsupported decision"):
            self.review({}, decision="LEAVE_UNRESOLVED")


class CorrectionSiteApplyTests(unittest.TestCase):
    """A sealed Phoenix site patch must preserve source H/A/N and discrepancy history."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.school = getattr(self, "school", "arizona")

        def write(relative, fields, rows):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)

        self.source = {"source_game_id": "PHOENIX-1",
                       "source_program_key": self.school,
                       "curated_site_type": "NEUTRAL",
                       "curated_venue_name": "Phoenix Union High School Gymnasium",
                       "notes": "Owner approved physical venue; source NEUTRAL preserved"}
        self.canonical = {
            "canonical_game_id": "CBBG-0000001",
            "team_a_key": self.school,
            "team_b_key": "arizona" if self.school == "stanford" else "stanford",
            "site_type": "TEAM_A_HOME",
            "designated_home_team_key": self.school,
            "venue_key": "", "venue_id": "", "site_city": "", "site_state": "",
            "notes": "",
        }
        write(f"schools/{self.school}/source-games.csv", list(self.source), [self.source])
        write("data/canonical/games.csv", list(self.canonical), [self.canonical])
        write("data/evidence/game-assertions.csv", [
            "assertion_id", "canonical_game_id", "source_program_key",
            "source_game_id", "curated_site_type", "curated_venue_name", "notes",
        ], [{
            "assertion_id": "ASSERT-1", "canonical_game_id": "CBBG-0000001",
            "source_program_key": self.school, "source_game_id": "PHOENIX-1",
            "curated_site_type": "NEUTRAL", "curated_venue_name": "",
            "notes": "Owner approved physical venue; source NEUTRAL preserved",
        }])
        write("data/reconciliation/discrepancies.csv", [
            "discrepancy_id", "canonical_game_id", "field_name",
            "source_a_program_key", "source_a_value", "source_b_program_key",
            "source_b_value", "canonical_value", "status", "resolution_basis", "notes",
        ], [{
            "discrepancy_id": "DISC-000001", "canonical_game_id": "CBBG-0000001",
            "field_name": "site_type", "source_a_program_key": self.school,
            "source_a_value": "NEUTRAL", "source_b_program_key": "",
            "source_b_value": "", "canonical_value": "TEAM_A_HOME",
            "status": "RESOLVED", "resolution_basis": "Original Gate 1 decision",
            "notes": "Original history retained",
        }])
        write("data/reference/venues.csv", ["venue_id", "venue_key", "city", "state"], [
            {"venue_id": "VEN-000866",
             "venue_key": "phoenix-union-high-school-gymnasium",
             "city": "Phoenix", "state": "AZ"}
        ])
        self.patch = {
            "site_type": "TEAM_A_HOME",
            "venue_id": "VEN-000866",
            "venue_key": "phoenix-union-high-school-gymnasium",
            "site_city": "Phoenix", "site_state": "AZ",
        }
        self.context = {
            "correction_source_game_ids": {"PHOENIX-1"},
            "fields": ["curated_site_type", "curated_venue_name"],
            "post_rows": {"PHOENIX-1": {
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Phoenix Union High School Gymnasium"}},
        }

    def read(self, name):
        with (self.root / name).open(newline="", encoding="utf-8") as stream:
            return list(csv.DictReader(stream))

    def rewrite(self, name, rows):
        with (self.root / name).open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    def apply(self, patch_values=None, authorized_drift=True):
        approved = {
            "school_key": self.school, "approved_plan_hash": "0" * 64,
            "decisions": [{
                "category": "correction_site_patch",
                "decision_id": "CORRECTION-SITE-PHOENIX-1",
                "source_game_id": "PHOENIX-1",
                "canonical_game_id": "CBBG-0000001",
                "decision": "APPLY_CANONICAL_PATCH",
                "canonical_site_expected": {
                    k: self.canonical.get(k, "") for k in plan.CORRECTION_SITE_PATCH_FIELDS
                },
                "canonical_patch": patch_values if patch_values is not None else self.patch,
                "source_patch": {},
                "resolution_basis": "Accepted institutional and owner 1942 Phoenix decision",
            }],
        }
        with (
            patch.object(plan, "_correction_assertion_reconciliation_context",
                         return_value=self.context),
            patch.object(plan, "SOURCE_ASSERTION_COPY_FIELDS",
                         ("curated_site_type", "curated_venue_name", "notes")),
            patch.object(plan, "assertion_drift",
                         return_value={"curated_venue_name": (
                             "Phoenix Union High School Gymnasium", "")}),
            patch.object(plan, "_is_authorized_correction_assertion_drift",
                         return_value=authorized_drift),
            patch.object(plan, "_record_dependent_site_gap_discrepancies",
                         return_value={}),
            patch.object(plan, "_record_reconciled_unresolved_home_venue_markers",
                         return_value={}),
            patch.object(plan, "_record_reciprocal_discrepancies",
                         return_value={}),
        ):
            return plan.apply_reconciliation_decisions(self.root, approved)

    def test_phoenix_sealed_apply_patches_canonical_and_assertion_only(self):
        counts = self.apply()
        self.assertEqual(counts["correction_site_patches"], 1)
        canonical = self.read("data/canonical/games.csv")[0]
        self.assertEqual(canonical["site_type"], "TEAM_A_HOME")
        self.assertEqual(canonical["designated_home_team_key"], self.school)
        self.assertEqual(canonical["venue_id"], "VEN-000866")
        self.assertEqual((canonical["site_city"], canonical["site_state"]),
                         ("Phoenix", "AZ"))
        source = self.read(f"schools/{self.school}/source-games.csv")[0]
        assertion = self.read("data/evidence/game-assertions.csv")[0]
        self.assertEqual(source["curated_site_type"], "NEUTRAL")
        self.assertEqual(assertion["curated_site_type"], "NEUTRAL")
        self.assertEqual(assertion["curated_venue_name"],
                         "Phoenix Union High School Gymnasium")
        self.assertEqual(source["notes"], assertion["notes"])
        self.assertIn("OWNER GATE 1 SUPERSEDING CANONICAL SITE", source["notes"])
        discrepancy = self.read("data/reconciliation/discrepancies.csv")[0]
        self.assertIn("Original Gate 1 decision", discrepancy["notes"])
        self.assertEqual(discrepancy["source_a_value"], "NEUTRAL")
        self.assertEqual(discrepancy["status"], "RESOLVED")

    def test_unregistered_physical_identity_fails_closed(self):
        proposed = dict(self.patch, venue_id="VEN-NOT-REGISTERED")
        with self.assertRaisesRegex(plan.WorkflowError, "not globally registered"):
            self.apply(proposed)

    def test_injected_assertion_drift_fails_closed(self):
        with self.assertRaisesRegex(plan.WorkflowError, "unapproved global assertion drift"):
            self.apply(authorized_drift=False)




    def test_registered_venue_geography_must_match(self):
        wrong = dict(self.patch, site_city="Stanford", site_state="CA")
        with self.assertRaisesRegex(plan.WorkflowError, "venue geography mismatch"):
            self.apply(wrong)

    def test_existing_venue_cannot_be_erased(self):
        row = dict(self.canonical,
                   venue_id="VEN-000866",
                   venue_key="phoenix-union-high-school-gymnasium",
                   site_city="Phoenix", site_state="AZ")
        self.canonical = row
        self.rewrite("data/canonical/games.csv", [row])
        blank = {"site_type": "TEAM_B_HOME", "venue_id": "", "venue_key": "",
                 "site_city": "Stanford", "site_state": "CA"}
        with self.assertRaisesRegex(plan.WorkflowError,
                                    "established canonical venue cannot be erased"):
            self.apply(blank)

    def test_superseded_claim_is_preserved_and_marked_overridden(self):
        name = f"schools/{self.school}/source-games.csv"
        row = self.read(name)[0]
        claim = "Prior notes claimed owner-approved OPPONENT HOME."
        row["notes"] = claim
        self.rewrite(name, [row])
        self.apply()
        updated = self.read(name)[0]
        assertion = self.read("data/evidence/game-assertions.csv")[0]
        self.assertIn(claim, updated["notes"])
        self.assertIn("OWNER GATE 1 SUPERSEDING CANONICAL SITE", updated["notes"])
        self.assertIn("home=" + self.school, updated["notes"])
        self.assertIn("venue_id=VEN-000866", updated["notes"])
        self.assertEqual(updated["notes"], assertion["notes"])
        self.assertEqual(updated["curated_site_type"], "NEUTRAL")


class NonArizonaResolvedSiteTests(CorrectionSiteApplyTests):
    """An existing RESOLVED site conflict outside Arizona is still reviewable."""

    school = "stanford"

    def test_non_arizona_prior_resolved_discrepancy_and_venue(self):
        self.rewrite("data/reference/venues.csv", [{
            "venue_id": "VEN-000422", "venue_key": "stanford-pavilion",
            "city": "Stanford", "state": "CA",
        }])
        proposed = {"site_type": "TEAM_A_HOME",
                    "venue_id": "VEN-000422", "venue_key": "stanford-pavilion",
                    "site_city": "Stanford", "site_state": "CA"}
        counts = self.apply(proposed)
        self.assertEqual(counts["correction_site_patches"], 1)
        canonical = self.read("data/canonical/games.csv")[0]
        self.assertEqual(canonical["designated_home_team_key"], "stanford")
        self.assertEqual(canonical["venue_id"], "VEN-000422")
        discrepancy = self.read("data/reconciliation/discrepancies.csv")[0]
        self.assertEqual(discrepancy["status"], "RESOLVED")
        self.assertIn("Original Gate 1 decision", discrepancy["notes"])
        self.assertEqual(
            self.read("schools/stanford/source-games.csv")[0]["curated_site_type"],
            "NEUTRAL",
        )


class CorrectionAuthorityManifestTests(unittest.TestCase):
    def test_missing_manifest_snapshot_digest_is_rejected(self):
        snapshot = {"fields": list(plan.SOURCE_ASSERTION_SYNC_FIELDS),
                    "rows": {"CORRECTION-1": {}}}
        self._check_bad_manifest(snapshot, snapshot, "")

    def test_tampered_manifest_snapshot_is_rejected(self):
        snapshot = {"fields": list(plan.SOURCE_ASSERTION_SYNC_FIELDS),
                    "rows": {"CORRECTION-1": {}}}
        altered = {"fields": snapshot["fields"],
                   "rows": {"CORRECTION-1": {"curated_site_type": "FORGED"}}}
        good = plan.sha256_text(plan.canonical_json(snapshot))
        self._check_bad_manifest(snapshot, altered, good)

    def _check_bad_manifest(self, pre, post, post_digest):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            folder = repo / ".onboarding" / "arizona"
            folder.mkdir(parents=True)
            manifest = {
                "school_key": "arizona",
                "status": "INTEGRATION_FROZEN",
                "workflow_kind": plan.CORRECTION_WORKFLOW_KIND,
                "correction_source_game_ids": ["CORRECTION-1"],
                "pre_correction_source_semantic_guard": {
                    "snapshot": pre,
                    "snapshot_sha256": plan.sha256_text(plan.canonical_json(pre)),
                },
                "source_game_semantic_guard": {
                    "snapshot": post, "snapshot_sha256": post_digest,
                },
            }
            (folder / "integration-freeze.json").write_text(json.dumps(manifest))
            with self.assertRaisesRegex(plan.WorkflowError, "snapshot hash mismatch"):
                plan._correction_assertion_reconciliation_context(repo, "arizona")

if __name__ == "__main__":
    unittest.main()
