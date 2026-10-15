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
                "notes": "Accepted owner historical correction, source H/A/N preserved.",
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


if __name__ == "__main__":
    unittest.main()
