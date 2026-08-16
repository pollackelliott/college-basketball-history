import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
import onboard_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    WorkflowError,
    _record_reciprocal_discrepancies,
    approve_plan,
    apply_reconciliation_decisions,
    build_plan,
    date_label,
    render_report,
    set_canonical_field,
    validate_package,
)


def review_item(**changes):
    item = {
        "decision_id": "DISCREPANCY-EXAMPLE-GAME_DATE",
        "category": "discrepancy",
        "source_game_id": "EXAMPLE-1",
        "canonical_game_id": "CBBG-0000001",
        "season_label": "2020-2021",
        "source_game_date": "2020-12-30",
        "canonical_game_date": "2020-12-29",
        "matchup": "alpha vs beta",
        "field_name": "game_date",
        "source_value": "2020-12-30",
        "canonical_value": "2020-12-29",
        "relevant_evidence": "alpha 2020-12-30; beta 2020-12-29",
        "recommended_action": "LEAVE_UNRESOLVED",
        "allowed_actions": [
            "KEEP_CANONICAL",
            "LEAVE_UNRESOLVED",
            "NORMALIZE_SOURCE_TO_CANONICAL",
            "USE_SOURCE",
        ],
        "decision": "PENDING",
        "resolution_basis": "",
        "canonical_patch_json": "{}",
        "source_patch_json": "{}",
        "notes": "date conflict",
    }
    item.update(changes)
    return item


class DateCompleteReviewTests(unittest.TestCase):
    def test_same_date_is_still_printed(self):
        item = review_item(
            source_game_date="1959-02-21",
            canonical_game_date="1959-02-21",
        )
        self.assertEqual(date_label(item), "Date: 1959-02-21")

    def test_date_discrepancy_prints_both_dates(self):
        item = review_item()
        label = date_label(item)
        self.assertIn("source 2020-12-30", label)
        self.assertIn("canonical 2020-12-29", label)

    def test_unknown_date_is_never_silently_omitted(self):
        item = review_item(source_game_date="", canonical_game_date="2020-12-29")
        self.assertEqual(
            date_label(item),
            "Dates: source [unknown]; canonical 2020-12-29",
        )

    def test_markdown_report_preserves_disputed_dates(self):
        plan = {
            "school_key": "alpha",
            "created_at": "2026-08-14T00:00:00+00:00",
            "input_fingerprint": {"sha256": "abc"},
            "summary": {},
            "blockers": [],
            "warnings": [],
            "decisions": [review_item()],
        }
        report = render_report(plan)
        self.assertIn("Dates: source 2020-12-30; canonical 2020-12-29", report)


class ApprovalContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base_plan = build_plan(ROOT, "vanderbilt")

    def write_fixture(self, directory, decision="PENDING", basis=""):
        plan = dict(self.base_plan)
        item = {
            "decision_id": "PUBLICATION-TEST",
            "category": "publication",
            "source_game_id": "",
            "season_label": "",
            "source_game_date": "[unknown]",
            "canonical_game_date": "[unknown]",
            "matchup": "vanderbilt",
            "field_name": "public_page_enabled",
            "source_value": "No",
            "canonical_value": "Yes",
            "relevant_evidence": "fixture",
            "recommended_action": "ENABLE_PUBLIC_PAGE",
            "allowed_actions": ["ENABLE_PUBLIC_PAGE", "KEEP_DISABLED"],
            "decision": "PENDING",
            "resolution_basis": "",
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
            "notes": "fixture",
        }
        plan["decisions"] = [item]
        plan_path = Path(directory) / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        review_path = Path(directory) / "review.csv"
        fields = [
            "decision_id",
            "decision",
            "resolution_basis",
            "canonical_patch_json",
            "source_patch_json",
            "notes",
        ]
        with review_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerow(
                {
                    "decision_id": item["decision_id"],
                    "decision": decision,
                    "resolution_basis": basis,
                    "canonical_patch_json": "{}",
                    "source_patch_json": "{}",
                    "notes": "fixture",
                }
            )
        return plan_path, review_path

    def test_pending_decision_cannot_be_sealed(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path, review_path = self.write_fixture(directory)
            with self.assertRaisesRegex(WorkflowError, "still PENDING"):
                approve_plan(ROOT, plan_path, review_path, "owner")

    def test_resolution_basis_is_required(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path, review_path = self.write_fixture(
                directory,
                decision="ENABLE_PUBLIC_PAGE",
            )
            with self.assertRaisesRegex(WorkflowError, "resolution_basis is required"):
                approve_plan(ROOT, plan_path, review_path, "owner")

    def test_decision_change_changes_approved_hash(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_plan, first_review = self.write_fixture(
                first,
                decision="ENABLE_PUBLIC_PAGE",
                basis="Owner approved publication after preview-ready QA.",
            )
            second_plan, second_review = self.write_fixture(
                second,
                decision="KEEP_DISABLED",
                basis="Owner approved data-only ingestion pending further research.",
            )
            _, first_hash = approve_plan(ROOT, first_plan, first_review, "owner")
            _, second_hash = approve_plan(ROOT, second_plan, second_review, "owner")
            self.assertNotEqual(first_hash, second_hash)

    def test_raw_text_cannot_be_patched(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path, review_path = self.write_fixture(
                directory,
                decision="ENABLE_PUBLIC_PAGE",
                basis="Owner-approved fixture.",
            )
            with review_path.open(encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["source_patch_json"] = json.dumps({"raw_text": "rewrite"})
            with review_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(WorkflowError, "forbidden source patch fields"):
                approve_plan(ROOT, plan_path, review_path, "owner")

    def test_identity_choice_seals_only_its_conditional_discrepancies(self):
        with tempfile.TemporaryDirectory() as directory:
            plan = dict(self.base_plan)
            identity = {
                "decision_id": "IDENTITY-EXAMPLE",
                "category": "identity",
                "source_game_id": "EXAMPLE-1",
                "canonical_value": "CBBG-1;CBBG-2",
                "allowed_actions": [
                    "MATCH_CANONICAL:CBBG-1",
                    "MATCH_CANONICAL:CBBG-2",
                    "FORCE_NEW",
                ],
            }
            selected = review_item(
                decision_id="CONDITIONAL-1",
                category="conditional_discrepancy",
                source_game_id="EXAMPLE-1",
                canonical_game_id="CBBG-1",
                applies_if_identity_decision="MATCH_CANONICAL:CBBG-1",
                allowed_actions=[
                    "KEEP_CANONICAL",
                    "LEAVE_UNRESOLVED",
                    "NORMALIZE_SOURCE_TO_CANONICAL",
                    "NOT_APPLICABLE",
                    "USE_SOURCE",
                ],
            )
            unselected = dict(selected)
            unselected.update(
                {
                    "decision_id": "CONDITIONAL-2",
                    "canonical_game_id": "CBBG-2",
                    "applies_if_identity_decision": "MATCH_CANONICAL:CBBG-2",
                }
            )
            plan["decisions"] = [identity, selected, unselected]
            plan_path = Path(directory) / "plan.json"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            review_path = Path(directory) / "review.csv"
            fields = [
                "decision_id",
                "decision",
                "resolution_basis",
                "canonical_patch_json",
                "source_patch_json",
                "notes",
            ]
            with review_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(
                    [
                        {
                            "decision_id": "IDENTITY-EXAMPLE",
                            "decision": "MATCH_CANONICAL:CBBG-1",
                            "resolution_basis": "Owner matched the dated source row.",
                            "canonical_patch_json": "{}",
                            "source_patch_json": "{}",
                            "notes": "",
                        },
                        {
                            "decision_id": "CONDITIONAL-1",
                            "decision": "KEEP_CANONICAL",
                            "resolution_basis": "Reciprocal dated evidence controls.",
                            "canonical_patch_json": "{}",
                            "source_patch_json": "{}",
                            "notes": "",
                        },
                        {
                            "decision_id": "CONDITIONAL-2",
                            "decision": "PENDING",
                            "resolution_basis": "",
                            "canonical_patch_json": "{}",
                            "source_patch_json": "{}",
                            "notes": "",
                        },
                    ]
                )
            approved, _ = approve_plan(ROOT, plan_path, review_path, "owner")
            by_id = {item["decision_id"]: item for item in approved["decisions"]}
            self.assertEqual(by_id["CONDITIONAL-1"]["category"], "discrepancy")
            self.assertEqual(by_id["CONDITIONAL-1"]["decision"], "KEEP_CANONICAL")
            self.assertEqual(by_id["CONDITIONAL-2"]["decision"], "NOT_APPLICABLE")


class RegressionAndSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = build_plan(ROOT, "vanderbilt")

    def test_vanderbilt_complete_state_is_a_zero_decision_no_op(self):
        self.assertEqual(self.plan["blockers"], [])
        self.assertEqual(self.plan["decisions"], [])
        self.assertEqual(self.plan["summary"]["existing_game_matches"], 3006)
        self.assertEqual(self.plan["summary"]["new_canonical_games"], 0)
        self.assertEqual(self.plan["summary"]["discrepancies_to_add"], 0)

    def test_vanderbilt_package_contract_is_complete(self):
        result = validate_package(ROOT, "vanderbilt")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["counts"]["source_games"], 3006)

    def test_score_change_recomputes_canonical_winner(self):
        row = {
            "team_a_key": "alpha",
            "team_b_key": "beta",
            "team_a_score": "50",
            "team_b_score": "60",
            "result_winner_team_key": "beta",
        }
        set_canonical_field(row, "score", "70-60")
        self.assertEqual(row["team_a_score"], "70")
        self.assertEqual(row["team_b_score"], "60")
        self.assertEqual(row["result_winner_team_key"], "alpha")

    def test_sealed_identity_match_revalidates_pair_and_season(self):
        source = {
            "source_program_key": "alpha",
            "normalized_opponent_key": "beta",
            "season_label": "2020-2021",
        }
        canonical = {
            "canonical_game_id": "CBBG-1",
            "team_a_key": "alpha",
            "team_b_key": "gamma",
            "season_label": "2020-2021",
        }
        status, _, method = ingest_school.resolve_sealed_identity_decision(
            source,
            "MATCH_CANONICAL:CBBG-1",
            [canonical],
            {"CBBG-1": canonical},
        )
        self.assertEqual(status, ingest_school.REVIEW)
        self.assertIn("IDENTITY_MISMATCH", method)

    def test_transaction_allow_list_rejects_cross_program_source_edits(self):
        self.assertFalse(
            onboard_school.allowed_apply_path(
                "schools/tennessee/source-games.csv",
                "vanderbilt",
                "a" * 64,
            )
        )
        self.assertTrue(
            onboard_school.allowed_apply_path(
                "schools/vanderbilt/source-games.csv",
                "vanderbilt",
                "a" * 64,
            )
        )


class ReciprocalDiscrepancyLifecycleTests(unittest.TestCase):
    def test_owner_canonical_change_records_losing_existing_assertion(self):
        canonical = {
            "canonical_game_id": "CBBG-1",
            "team_a_key": "alpha",
            "team_b_key": "beta",
            "overtime_periods": "1",
        }
        assertions = [
            {
                "canonical_game_id": "CBBG-1",
                "source_program_key": "alpha",
                "source_game_id": "ALPHA-1",
                "normalized_opponent_key": "beta",
                "overtime_periods": "1",
            },
            {
                "canonical_game_id": "CBBG-1",
                "source_program_key": "beta",
                "source_game_id": "BETA-1",
                "normalized_opponent_key": "alpha",
                "overtime_periods": "0",
            },
        ]
        discrepancies = []

        counts = _record_reciprocal_discrepancies(
            "alpha",
            {("CBBG-1", "overtime_periods"): "Owner selected alpha after cross-source review."},
            {"CBBG-1": canonical},
            assertions,
            discrepancies,
        )

        self.assertEqual(counts["reciprocal_discrepancies_added"], 1)
        self.assertEqual(len(discrepancies), 1)
        row = discrepancies[0]
        self.assertEqual(row["source_a_program_key"], "beta")
        self.assertEqual(row["source_a_value"], "0")
        self.assertEqual(row["canonical_value"], "1")
        self.assertEqual(row["status"], "RESOLVED")
        self.assertIn("Owner selected alpha", row["resolution_basis"])


class GenericReconciliationTests(unittest.TestCase):
    def write_csv(self, path, fields, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def read_one(self, path):
        with path.open(encoding="utf-8") as handle:
            return list(csv.DictReader(handle))[0]

    def test_source_normalization_preserves_raw_text_and_original_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            canonical.update(
                {
                    "canonical_game_id": "CBBG-1",
                    "season_label": "2020-2021",
                    "game_date": "2020-12-29",
                    "date_precision": "EXACT",
                    "team_a_key": "alpha",
                    "team_b_key": "beta",
                    "team_a_score": "70",
                    "team_b_score": "60",
                    "result_winner_team_key": "alpha",
                    "site_type": "UNKNOWN",
                    "game_type": "REGULAR_SEASON",
                    "canonical_status": "PROVISIONAL",
                }
            )
            source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            source.update(
                {
                    "source_program_key": "alpha",
                    "source_game_id": "ALPHA-1",
                    "season_label": "2020-2021",
                    "game_date": "2020-12-30",
                    "normalized_opponent_key": "beta",
                    "normalized_opponent_name": "Beta",
                    "team_score": "70",
                    "opponent_score": "60",
                    "played_result": "W",
                    "overtime_periods": "0",
                    "curated_site_type": "UNKNOWN",
                    "curated_game_type": "REGULAR_SEASON",
                    "raw_text": "Dec. 30 Beta W 70-60",
                }
            )
            assertion = dict(source)
            assertion.update(
                {
                    "assertion_id": "ASRT-ALPHA-1",
                    "canonical_game_id": "CBBG-1",
                    "match_status": "MATCHED",
                    "match_method": "FIXTURE",
                }
            )
            discrepancy = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
            discrepancy.update(
                {
                    "discrepancy_id": "DISC-1",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "game_date",
                    "source_a_program_key": "alpha",
                    "source_a_value": "2020-12-30",
                    "canonical_value": "2020-12-29",
                    "status": "UNDER_REVIEW",
                }
            )
            self.write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )
            self.write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS,
                [assertion],
            )
            self.write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS,
                [discrepancy],
            )
            self.write_csv(
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [source],
            )
            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": "DATE-1",
                        "category": "discrepancy",
                        "source_game_id": "ALPHA-1",
                        "canonical_game_id": "CBBG-1",
                        "field_name": "game_date",
                        "source_value": "2020-12-30",
                        "canonical_value": "2020-12-29",
                        "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                        "resolution_basis": "Dated reciprocal official record controls.",
                        "canonical_patch": {},
                        "source_patch": {},
                    }
                ],
            }
            counts = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(counts["source_normalizations"], 1)
            normalized = self.read_one(repo / "schools/alpha/source-games.csv")
            synced = self.read_one(repo / "data/evidence/game-assertions.csv")
            resolved = self.read_one(
                repo / "data/reconciliation/discrepancies.csv"
            )
            self.assertEqual(normalized["game_date"], "2020-12-29")
            self.assertEqual(normalized["raw_text"], "Dec. 30 Beta W 70-60")
            self.assertEqual(synced["game_date"], "2020-12-29")
            self.assertEqual(resolved["source_a_value"], "2020-12-30")
            self.assertEqual(resolved["status"], "RESOLVED")


if __name__ == "__main__":
    unittest.main()
