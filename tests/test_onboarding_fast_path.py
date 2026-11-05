import csv
import hashlib
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
    _planned_venue_geography_errors,
    _record_reciprocal_discrepancies,
    approve_plan,
    apply_reconciliation_decisions,
    build_plan,
    date_label,
    exhibition_warning_required,
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


class PlannedVenueGeographySafetyTests(unittest.TestCase):
    def test_source_and_registry_corrobated_venue_clears_coarse_geography_block(self):
        source = {
            "source_program_key": "new-school",
            "source_game_id": "NEW-0001",
            "normalized_opponent_key": "opponent",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "Example Arena",
            "city": "Atlanta",
            "state": "GA",
        }
        canonical = {
            "canonical_game_id": "CBBG-TEST",
            "site_type": "NEUTRAL",
            "venue_key": "",
            "venue_id": "",
            "site_city": "Nashville",
            "site_state": "TN",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "venue_id": "VEN-EXAMPLE",
                "city": "Atlanta",
                "state": "GA",
            }
        }

        errors = _planned_venue_geography_errors(
            source,
            ingest_school.CONFIDENT,
            "CBBG-TEST",
            {"CBBG-TEST": canonical},
            metadata,
        )

        # Source and permanent venue registry independently agree on Atlanta,
        # while the canonical row has no physical venue identity. Under the
        # project invariant, canonical geography follows the resolved physical
        # venue and the older Nashville assertion remains preserved separately.
        self.assertEqual(errors, [])


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

    def test_markdown_report_states_public_scope_consequence_plainly(self):
        plan = {
            "school_key": "alpha",
            "created_at": "2026-08-14T00:00:00+00:00",
            "input_fingerprint": {"sha256": "abc"},
            "summary": {
                "source_rows": 100,
                "in_scope_source_rows": 80,
                "pre_cutoff_rows": 20,
                "history_start_season": "1950-1951",
                "pre_cutoff_first_season": "1911-1912",
                "pre_cutoff_last_season": "1949-1950",
                "affected_public_programs": [],
            },
            "blockers": [],
            "warnings": [],
            "decisions": [],
        }
        report = render_report(plan)
        self.assertIn("PUBLIC SCOPE", report)
        self.assertIn("20 researched rows", report)
        self.assertIn("1911-1912 through 1949-1950", report)
        self.assertIn("will not appear on the public page", report)


class ExhibitionWarningTests(unittest.TestCase):
    def test_true_exhibition_wording_still_warns(self):
        self.assertTrue(
            exhibition_warning_required(
                "10/25/2025 Example State — Exhibition",
                "",
                "",
            )
        )

    def test_excluded_preseason_exhibitions_note_does_not_warn(self):
        self.assertFalse(
            exhibition_warning_required(
                "11/3/2025 Western Carolina W 94-63",
                "",
                (
                    "2025-26 competitive game from official Cincinnati schedule; "
                    "preseason exhibitions excluded from Stage 1 competitive universe."
                ),
            )
        )

    def test_exhibition_complex_venue_name_does_not_warn(self):
        self.assertFalse(
            exhibition_warning_required(
                "18 Hofstra W 79-65 A - -",
                "National Invitation Tournament",
                (
                    "Hofstra official box score identifies the game at "
                    "David S. Mack Sports and Exhibition Complex, Hempstead, New York."
                ),
            )
        )


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

    def write_shared_score_fixture(self, repo):
        canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
        canonical.update(
            {
                "canonical_game_id": "CBBG-1",
                "season_label": "1930-1931",
                "game_date": "1931-02-14",
                "date_precision": "EXACT",
                "team_a_key": "alpha",
                "team_b_key": "beta",
                "team_a_score": "16",
                "team_b_score": "24",
                "result_winner_team_key": "beta",
                "site_type": "UNKNOWN",
                "game_type": "REGULAR_SEASON",
                "canonical_status": "PROVISIONAL",
            }
        )

        sources = []
        assertions = []
        for source_game_id, team_score, opponent_score in (
            ("ALPHA-1", "21", "26"),
            ("ALPHA-2", "18", "22"),
        ):
            source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            source.update(
                {
                    "source_program_key": "alpha",
                    "source_game_id": source_game_id,
                    "season_label": "1930-1931",
                    "normalized_opponent_key": "beta",
                    "normalized_opponent_name": "Beta",
                    "team_score": team_score,
                    "opponent_score": opponent_score,
                    "played_result": "L",
                    "overtime_periods": "0",
                    "curated_site_type": "UNKNOWN",
                    "curated_game_type": "REGULAR_SEASON",
                    "raw_text": f"{source_game_id} Beta L {team_score}-{opponent_score}",
                }
            )
            sources.append(source)
            assertion = dict(source)
            assertion.update(
                {
                    "assertion_id": f"ASRT-{source_game_id}",
                    "canonical_game_id": "CBBG-1",
                    "match_status": "MATCHED",
                    "match_method": "FIXTURE",
                }
            )
            assertions.append(assertion)

        discrepancy = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
        discrepancy.update(
            {
                "discrepancy_id": "DISC-1",
                "canonical_game_id": "CBBG-1",
                "field_name": "score",
                "source_a_program_key": "alpha",
                "source_a_value": "21-26",
                "canonical_value": "16-24",
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
            assertions,
        )
        self.write_csv(
            repo / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            [discrepancy],
        )
        self.write_csv(
            repo / "schools/alpha/source-games.csv",
            ingest_school.ASSERTION_FIELDS,
            sources,
        )

    def shared_score_approved(self, second_decision="KEEP_CANONICAL"):
        return {
            "school_key": "alpha",
            "approved_plan_hash": "a" * 64,
            "decisions": [
                {
                    "decision_id": "SCORE-ALPHA-1",
                    "category": "discrepancy",
                    "source_game_id": "ALPHA-1",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "score",
                    "source_value": "21-26",
                    "canonical_value": "16-24",
                    "decision": "KEEP_CANONICAL",
                    "resolution_basis": "Reciprocal canonical score controls ALPHA-1.",
                    "canonical_patch": {},
                    "source_patch": {},
                },
                {
                    "decision_id": "SCORE-ALPHA-2",
                    "category": "discrepancy",
                    "source_game_id": "ALPHA-2",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "score",
                    "source_value": "18-22",
                    "canonical_value": "16-24",
                    "decision": second_decision,
                    "resolution_basis": "Reviewed ALPHA-2 against the same real game.",
                    "canonical_patch": {},
                    "source_patch": {},
                },
            ],
        }

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

    def test_reconciliation_authenticates_mid_phase_before_any_source_normalization(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            school_key = "alpha"

            split_source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            split_source.update({
                "source_program_key": school_key,
                "source_game_id": "SPLIT-1",
                "season_label": "1960-1961",
                "game_date": "1961-01-15",
                "normalized_opponent_key": "gamma",
                "normalized_opponent_name": "Gamma",
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Frozen Arena",
                "city": "Frozen City",
                "state": "FC",
                "curated_game_type": "REGULAR_SEASON",
            })
            site_source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            site_source.update({
                "source_program_key": school_key,
                "source_game_id": "ALPHA-SITE",
                "season_label": "2010-2011",
                "game_date": "2011-03-16",
                "normalized_opponent_key": "beta",
                "normalized_opponent_name": "Beta",
                "team_score": "65",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "curated_site_type": "OPPONENT_HOME",
                "curated_venue_name": "",
                "city": "",
                "state": "",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "Beta postseason fixture",
            })
            later_source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            later_source.update({
                "source_program_key": school_key,
                "source_game_id": "ALPHA-LATER",
                "season_label": "2019-2020",
                "game_date": "2020-01-02",
                "normalized_opponent_key": "delta",
                "normalized_opponent_name": "Delta",
                "team_score": "70",
                "opponent_score": "68",
                "played_result": "W",
                "overtime_periods": "0",
                "curated_site_type": "NEUTRAL",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "Delta date fixture",
            })
            self.write_csv(
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [split_source, site_source, later_source],
            )

            site_canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            site_canonical.update({
                "canonical_game_id": "CBBG-SITE",
                "season_label": "2010-2011",
                "game_date": "2011-03-16",
                "date_precision": "EXACT",
                "team_a_key": school_key,
                "team_b_key": "beta",
                "team_a_score": "65",
                "team_b_score": "60",
                "result_winner_team_key": school_key,
                "site_type": "TEAM_B_HOME",
                "game_type": "NIT",
                "canonical_status": "PROVISIONAL",
            })
            later_canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            later_canonical.update({
                "canonical_game_id": "CBBG-LATER",
                "season_label": "2019-2020",
                "game_date": "2020-01-03",
                "date_precision": "EXACT",
                "team_a_key": school_key,
                "team_b_key": "delta",
                "team_a_score": "70",
                "team_b_score": "68",
                "result_winner_team_key": school_key,
                "site_type": "NEUTRAL",
                "game_type": "REGULAR_SEASON",
                "canonical_status": "PROVISIONAL",
            })
            self.write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [site_canonical, later_canonical],
            )

            assertions = []
            for source, game_id in (
                (site_source, "CBBG-SITE"),
                (later_source, "CBBG-LATER"),
            ):
                assertion = dict(source)
                assertion.update({
                    "assertion_id": f"ASRT-{source['source_game_id']}",
                    "canonical_game_id": game_id,
                    "match_status": "MATCHED",
                    "match_method": "FIXTURE",
                })
                assertions.append(assertion)
            self.write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS,
                assertions,
            )

            site_discrepancy = {
                field: "" for field in ingest_school.DISCREPANCY_FIELDS
            }
            site_discrepancy.update({
                "discrepancy_id": "DISC-SITE",
                "canonical_game_id": "CBBG-SITE",
                "field_name": "game_type",
                "source_a_program_key": school_key,
                "source_a_value": "REGULAR_SEASON",
                "canonical_value": "NIT",
                "status": "UNDER_REVIEW",
            })
            later_discrepancy = {
                field: "" for field in ingest_school.DISCREPANCY_FIELDS
            }
            later_discrepancy.update({
                "discrepancy_id": "DISC-LATER",
                "canonical_game_id": "CBBG-LATER",
                "field_name": "game_date",
                "source_a_program_key": school_key,
                "source_a_value": "2020-01-02",
                "canonical_value": "2020-01-03",
                "status": "UNDER_REVIEW",
            })
            self.write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS,
                [site_discrepancy, later_discrepancy],
            )

            global_venue_fields = [
                "venue_id", "venue_key", "display_name", "city", "state",
                "opened", "closed", "date_precision", "identity_status",
                "source_basis", "notes",
            ]
            self.write_csv(
                repo / "data/reference/venues.csv",
                global_venue_fields,
                [
                    {
                        "venue_id": "VEN-000901",
                        "venue_key": "frozen-arena",
                        "display_name": "Frozen Arena",
                        "city": "Frozen City",
                        "state": "FC",
                        "opened": "",
                        "closed": "",
                        "date_precision": "",
                        "identity_status": "VERIFIED",
                        "source_basis": "fixture",
                        "notes": "",
                    },
                    {
                        "venue_id": "VEN-000902",
                        "venue_key": "example-arena",
                        "display_name": "Example Arena",
                        "city": "Example City",
                        "state": "EX",
                        "opened": "2000",
                        "closed": "",
                        "date_precision": "YEAR",
                        "identity_status": "VERIFIED",
                        "source_basis": "fixture",
                        "notes": "",
                    },
                ],
            )
            self.write_csv(
                repo / "data/reference/venue-names.csv",
                [
                    "venue_id", "venue_name", "normalized_name", "name_type",
                    "valid_from", "valid_to", "date_precision", "source_basis",
                    "notes",
                ],
                [
                    {
                        "venue_id": "VEN-000901",
                        "venue_name": "Frozen Arena",
                        "normalized_name": "frozenarena",
                        "name_type": "PROJECT_DISPLAY",
                        "valid_from": "",
                        "valid_to": "",
                        "date_precision": "",
                        "source_basis": "fixture",
                        "notes": "",
                    },
                    {
                        "venue_id": "VEN-000902",
                        "venue_name": "Example Arena",
                        "normalized_name": "examplearena",
                        "name_type": "PROJECT_DISPLAY",
                        "valid_from": "",
                        "valid_to": "",
                        "date_precision": "",
                        "source_basis": "fixture",
                        "notes": "",
                    },
                    {
                        "venue_id": "VEN-000902",
                        "venue_name": "Historic Example Arena",
                        "normalized_name": "historicexamplearena",
                        "name_type": "HISTORICAL",
                        "valid_from": "",
                        "valid_to": "",
                        "date_precision": "",
                        "source_basis": "fixture",
                        "notes": "",
                    },
                ],
            )

            venue_fields = [
                "source_program_key", "venue_key", "venue_id", "canonical_name",
                "aliases", "city", "state", "venue_type", "known_opened",
                "known_closed", "venue_date_precision", "games_currently_assigned",
                "first_assigned_game", "last_assigned_game", "relationship_type",
                "relationship_start", "relationship_end",
                "relationship_date_precision", "site_rule", "source_basis", "notes",
            ]
            frozen_venue = {field: "" for field in venue_fields}
            frozen_venue.update({
                "source_program_key": school_key,
                "venue_key": "frozen-arena",
                "venue_id": "VEN-000901",
                "canonical_name": "Frozen Arena",
                "city": "Frozen City",
                "state": "FC",
                "games_currently_assigned": "1",
                "first_assigned_game": "1961-01-15",
                "last_assigned_game": "1961-01-15",
                "relationship_type": "GAME_SITE",
                "site_rule": "fixture",
                "source_basis": "fixture",
                "notes": "fixture",
            })
            local_venue_path = repo / "schools/alpha/venues.csv"
            self.write_csv(local_venue_path, venue_fields, [frozen_venue])
            frozen_venue_hash = hashlib.sha256(
                local_venue_path.read_bytes()
            ).hexdigest()

            snapshot_fields = [
                "season_label",
                "game_date",
                "curated_venue_name",
                "city",
                "state",
                "curated_site_type",
                "curated_game_type",
            ]
            source_rows = [split_source, site_source, later_source]
            snapshot = {
                "schema_version": 1,
                "fields": snapshot_fields,
                "rows": {
                    row["source_game_id"]: {
                        field: row.get(field, "")
                        for field in snapshot_fields
                    }
                    for row in source_rows
                },
            }
            onboarding = repo / ".onboarding" / school_key
            onboarding.mkdir(parents=True)
            (onboarding / "integration-freeze.json").write_text(
                json.dumps({
                    "schema_version": 2,
                    "school_key": school_key,
                    "status": "INTEGRATION_FROZEN",
                    "package_member_sha256": {
                        "venues.csv": frozen_venue_hash,
                    },
                    "source_game_semantic_guard": {
                        "schema_version": 1,
                        "snapshot_sha256": hashlib.sha256(
                            json.dumps(
                                snapshot,
                                ensure_ascii=False,
                                sort_keys=True,
                                separators=(",", ":"),
                            ).encode("utf-8")
                        ).hexdigest(),
                        "snapshot": snapshot,
                    },
                    "venue_reconciliation": {
                        "schema_version": 2,
                        "mappings": [{
                            "action": "SPLIT_LOCAL_ROW_BY_CUTOVER",
                            "expected_local_name": "Frozen Arena",
                            "expected_local_city": "Frozen City",
                            "expected_local_state": "FC",
                            "cutover_date": "1960-01-01",
                            "split_source_game_count": "1",
                            "split_targets": [{
                                "side": "AFTER",
                                "global_venue_id": "VEN-000901",
                                "global_venue_key": "frozen-arena",
                                "games_currently_assigned": "1",
                                "source_game_ids": ["SPLIT-1"],
                            }],
                        }],
                    },
                }),
                encoding="utf-8",
            )

            approved = {
                "school_key": school_key,
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": "SITE-GAME-TYPE",
                        "category": "discrepancy",
                        "source_game_id": "ALPHA-SITE",
                        "source_game_date": "2011-03-16",
                        "canonical_game_id": "CBBG-SITE",
                        "field_name": "game_type",
                        "source_value": "REGULAR_SEASON",
                        "canonical_value": "NIT",
                        "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                        "resolution_basis": "Official host source identifies exact site.",
                        "canonical_patch": {},
                        "source_patch": {
                            "curated_venue_name": "Historic Example Arena",
                            "city": "Example City",
                            "state": "EX",
                        },
                        "venue_relationship_patch": {
                            "venue_id": "VEN-000902",
                            "venue_key": "example-arena",
                        },
                    },
                    {
                        "decision_id": "LATER-DATE",
                        "category": "discrepancy",
                        "source_game_id": "ALPHA-LATER",
                        "source_game_date": "2020-01-02",
                        "canonical_game_id": "CBBG-LATER",
                        "field_name": "game_date",
                        "source_value": "2020-01-02",
                        "canonical_value": "2020-01-03",
                        "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                        "resolution_basis": "Exact dated reciprocal source controls.",
                        "canonical_patch": {},
                        "source_patch": {},
                    },
                ],
            }

            counts = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(counts["venue_relationship_patches"], 1)
            self.assertEqual(counts["source_normalizations"], 2)

            with (repo / "schools/alpha/source-games.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                final_sources = {
                    row["source_game_id"]: row for row in csv.DictReader(handle)
                }
            self.assertEqual(
                final_sources["ALPHA-SITE"]["curated_game_type"],
                "NIT",
            )
            self.assertEqual(
                final_sources["ALPHA-SITE"]["curated_venue_name"],
                "Historic Example Arena",
            )
            self.assertEqual(
                final_sources["ALPHA-LATER"]["game_date"],
                "2020-01-03",
            )
            with local_venue_path.open(
                encoding="utf-8", newline=""
            ) as handle:
                final_venues = list(csv.DictReader(handle))
            self.assertEqual(len(final_venues), 2)
            self.assertEqual(final_venues[1]["relationship_type"], "GAME_SITE")
            self.assertEqual(final_venues[1]["venue_id"], "VEN-000902")

    def test_shared_program_discrepancy_accepts_distinct_source_values_when_outcome_agrees(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.write_shared_score_fixture(repo)

            counts = apply_reconciliation_decisions(
                repo,
                self.shared_score_approved(),
            )

            self.assertEqual(counts["canonical_retentions"], 2)
            self.assertEqual(counts["processed"], 2)
            canonical = self.read_one(repo / "data/canonical/games.csv")
            self.assertEqual(
                (canonical["team_a_score"], canonical["team_b_score"]),
                ("16", "24"),
            )
            resolved = self.read_one(
                repo / "data/reconciliation/discrepancies.csv"
            )
            self.assertEqual(resolved["source_a_value"], "21-26")
            self.assertEqual(resolved["canonical_value"], "16-24")
            self.assertEqual(resolved["status"], "RESOLVED")
            self.assertIn("ALPHA-1", resolved["resolution_basis"])
            self.assertIn("ALPHA-2", resolved["resolution_basis"])
            self.assertIn("ALPHA-1", resolved["notes"])
            self.assertIn("ALPHA-2", resolved["notes"])

    def test_shared_program_discrepancy_rejects_conflicting_final_canonical_values(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            self.write_shared_score_fixture(repo)

            with self.assertRaisesRegex(
                WorkflowError,
                "must converge on one final canonical value",
            ):
                apply_reconciliation_decisions(
                    repo,
                    self.shared_score_approved(second_decision="USE_SOURCE"),
                )

    def test_normalized_home_site_patch_propagates_through_full_transaction(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            canonical.update(
                {
                    "canonical_game_id": "CBBG-1",
                    "season_label": "1945-1946",
                    "game_date": "1946-02-01",
                    "date_precision": "EXACT",
                    "team_a_key": "alpha",
                    "team_b_key": "beta",
                    "team_a_score": "34",
                    "team_b_score": "31",
                    "result_winner_team_key": "alpha",
                    "site_type": "TEAM_B_HOME",
                    "designated_home_team_key": "beta",
                    "game_type": "REGULAR_SEASON",
                    "canonical_status": "PROVISIONAL",
                    "venue_key": "",
                    "venue_id": "",
                    "site_city": "",
                    "site_state": "",
                }
            )
            source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            source.update(
                {
                    "source_program_key": "beta",
                    "source_game_id": "BETA-1",
                    "season_label": "1945-1946",
                    "game_date": "1946-02-01",
                    "normalized_opponent_key": "alpha",
                    "normalized_opponent_name": "Alpha",
                    "team_score": "31",
                    "opponent_score": "34",
                    "played_result": "L",
                    "overtime_periods": "0",
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                    "curated_game_type": "REGULAR_SEASON",
                    "raw_text": "Alpha 34, Beta 31",
                }
            )
            assertion = dict(source)
            assertion.update(
                {
                    "assertion_id": "ASRT-BETA-1",
                    "canonical_game_id": "CBBG-1",
                    "match_status": "MATCHED",
                    "match_method": "FIXTURE",
                }
            )
            discrepancy = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
            discrepancy.update(
                {
                    "discrepancy_id": "DISC-SITE-1",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "site_type",
                    "source_a_program_key": "beta",
                    "source_a_value": "TEAM_A_HOME",
                    "canonical_value": "TEAM_B_HOME",
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
                repo / "schools/beta/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [source],
            )
            self.write_csv(
                repo / "data/reference/venues.csv",
                [
                    "venue_id", "venue_key", "display_name", "city", "state",
                    "opened", "closed", "date_precision", "identity_status",
                    "source_basis", "notes",
                ],
                [
                    {
                        "venue_id": "VEN-999999",
                        "venue_key": "example-fieldhouse",
                        "display_name": "Example Fieldhouse",
                        "city": "Example City",
                        "state": "EX",
                        "opened": "1940",
                        "closed": "1970",
                        "date_precision": "year",
                        "identity_status": "CURATED_SEED",
                        "source_basis": "Regression fixture.",
                        "notes": "",
                    }
                ],
            )
            self.write_csv(
                repo / "data/reference/venue-names.csv",
                [
                    "venue_id", "venue_name", "normalized_name", "name_type",
                    "valid_from", "valid_to", "date_precision", "source_basis",
                    "notes",
                ],
                [
                    {
                        "venue_id": "VEN-999999",
                        "venue_name": "Example Fieldhouse",
                        "normalized_name": "examplefieldhouse",
                        "name_type": "PROJECT_DISPLAY",
                        "valid_from": "",
                        "valid_to": "",
                        "date_precision": "",
                        "source_basis": "Regression fixture.",
                        "notes": "",
                    }
                ],
            )
            self.write_csv(
                repo / "schools/beta/venues.csv",
                [
                    "source_program_key", "venue_key", "venue_id",
                    "canonical_name", "aliases", "city", "state", "venue_type",
                    "known_opened", "known_closed", "venue_date_precision",
                    "games_currently_assigned", "first_assigned_game",
                    "last_assigned_game", "relationship_type",
                    "relationship_start", "relationship_end",
                    "relationship_date_precision", "site_rule", "source_basis",
                    "notes",
                ],
                [
                    {
                        "source_program_key": "beta",
                        "venue_key": "example-fieldhouse",
                        "venue_id": "VEN-999999",
                        "canonical_name": "Example Fieldhouse",
                        "aliases": "",
                        "city": "Example City",
                        "state": "EX",
                        "venue_type": "arena",
                        "known_opened": "1940",
                        "known_closed": "1970",
                        "venue_date_precision": "year",
                        "games_currently_assigned": "1",
                        "first_assigned_game": "1940-01-01",
                        "last_assigned_game": "1970-12-31",
                        "relationship_type": "HOME",
                        "relationship_start": "1940-01-01",
                        "relationship_end": "1970-12-31",
                        "relationship_date_precision": "day",
                        "site_rule": "HOME only after independent H/A/N classification.",
                        "source_basis": "Regression fixture.",
                        "notes": "",
                    }
                ],
            )

            approved = {
                "school_key": "beta",
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": "SITE-1",
                        "category": "discrepancy",
                        "source_game_id": "BETA-1",
                        "canonical_game_id": "CBBG-1",
                        "field_name": "site_type",
                        "source_value": "TEAM_A_HOME",
                        "canonical_value": "TEAM_B_HOME",
                        "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                        "resolution_basis": "Owner-approved regression fixture.",
                        "canonical_patch": {},
                        "source_patch": {
                            "curated_venue_name": "Example Fieldhouse",
                            "city": "Example City",
                            "state": "EX",
                        },
                    }
                ],
            }

            counts = apply_reconciliation_decisions(repo, approved)
            normalized = self.read_one(repo / "schools/beta/source-games.csv")
            synced = self.read_one(repo / "data/evidence/game-assertions.csv")
            final = self.read_one(repo / "data/canonical/games.csv")

            self.assertEqual(counts["source_normalizations"], 1)
            self.assertEqual(normalized["curated_site_type"], "SOURCE_PROGRAM_HOME")
            self.assertEqual(normalized["curated_venue_name"], "Example Fieldhouse")
            self.assertEqual(normalized["city"], "Example City")
            self.assertEqual(normalized["state"], "EX")
            self.assertEqual(synced["curated_site_type"], "SOURCE_PROGRAM_HOME")
            self.assertEqual(synced["curated_venue_name"], "Example Fieldhouse")
            self.assertEqual(synced["city"], "Example City")
            self.assertEqual(synced["state"], "EX")
            self.assertEqual(final["site_type"], "TEAM_B_HOME")
            self.assertEqual(final["venue_key"], "example-fieldhouse")
            self.assertEqual(final["venue_id"], "VEN-999999")
            self.assertEqual(final["site_city"], "Example City")
            self.assertEqual(final["site_state"], "EX")


if __name__ == "__main__":
    unittest.main()
