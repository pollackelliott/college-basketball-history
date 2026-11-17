"""Exact population proof for existing published-site debt in one-game corrections."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from correction_site_nonregression import (
    EXPANSION_MODE,
    digest,
    prove,
    prove_expansion,
    verify_current,
    verify_expansion_current,
)
from onboarding_plan import WorkflowError
from onboard_school import correction_gate_kwargs_from_manifest, pr_body


def report(*, gaps=("CBBG-1", "CBBG-2"), lost=1):
    return {
        "school_key": "tennessee", "history_start_season": "1908-1909",
        "source_validation_scope": {
            "mode": "CORRECTION_DELTA", "scoped_source_games": 1,
            "correction_source_games": 1,
        },
        "source_site_counts": {"source_site_rows": 1},
        "status": "FAIL",
        "counts": {
            "target_canonical_games": 2952,
            "unaccounted_public_gap": len(gaps),
            "target_source_location_lost": lost,
        },
        "examples": {
            "unaccounted_public_gap": list(gaps),
            "target_source_location_lost": (["CBBG-0020298"] if lost else []),
        },
        "errors": ["pre-existing publication debt"],
        "warnings": [],
    }


class CorrectionSiteNonregressionTests(unittest.TestCase):
    def test_existing_population_persists_without_becoming_a_general_gate_pass(self):
        before = report()
        after = report(lost=0)
        proof = prove(before, after, "CBBG-0020298")
        self.assertEqual(proof["baseline_site_status"], "FAIL")
        self.assertEqual(proof["corrected_site_status"], "FAIL")
        self.assertEqual(proof["removed_site_findings"], 1)
        self.assertTrue(proof["site_debt_remains"])
        self.assertEqual(proof["corrected_report_sha256"], digest(after))
        verify_current(after, proof, "tennessee")

    def test_same_count_but_new_game_fails(self):
        before, after = report(), report(gaps=("CBBG-1", "CBBG-3"))
        with self.assertRaisesRegex(WorkflowError, "introduced site failure"):
            prove(before, after, "CBBG-0020298")

    def test_missing_population_entries_fail_closed(self):
        before, after = report(), report()
        after["examples"]["unaccounted_public_gap"] = ["CBBG-1"]
        with self.assertRaisesRegex(WorkflowError, "complete failure population"):
            prove(before, after, "CBBG-0020298")

    def test_added_category_fails_even_when_other_category_improves(self):
        before, after = report(), report(lost=0)
        after["counts"]["reciprocal_location_unpropagated"] = 1
        after["examples"]["reciprocal_location_unpropagated"] = ["CBBG-99"]
        with self.assertRaisesRegex(WorkflowError, "introduced site failure"):
            prove(before, after, "CBBG-0020298")

    def test_modified_source_scope_or_canonical_universe_fails(self):
        before, after = report(), report()
        after["source_validation_scope"]["scoped_source_games"] = 2
        with self.assertRaisesRegex(WorkflowError, "trusted one-game scope"):
            prove(before, after, "CBBG-0020298")
        after = report()
        after["counts"]["target_canonical_games"] = 2953
        with self.assertRaisesRegex(WorkflowError, "canonical universe"):
            prove(before, after, "CBBG-0020298")
        after = report()
        after["source_site_counts"]["source_site_rows"] = 2
        with self.assertRaisesRegex(WorkflowError, "source-side Research debt"):
            prove(before, after, "CBBG-0020298")

    def test_release_gate_reuses_only_valid_one_game_proof(self):
        after = report(lost=0)
        proof = prove(report(), after, "CBBG-0020298")
        for transaction_kind in (
            "SINGLE_GAME_IDENTITY",
            "SINGLE_GAME_IDENTITY_SITE",
        ):
            with self.subTest(transaction_kind=transaction_kind):
                manifest = {
                    "school_key": "tennessee",
                    "summary": {
                        "correction_transaction_kind": transaction_kind,
                        "correction_source_game_id": "TENRAW-00136",
                        "correction_canonical_game_id": "CBBG-0020298",
                    },
                    "execution": {"correction_site_nonregression": proof},
                }
                kwargs = correction_gate_kwargs_from_manifest(manifest, "tennessee")
                self.assertEqual(kwargs["correction_source_id"], "TENRAW-00136")
                verify_current(after, kwargs["correction_site_proof"], "tennessee")
                corrupt = copy.deepcopy(manifest)
                corrupt["summary"]["correction_canonical_game_id"] = "CBBG-OTHER"
                with self.assertRaisesRegex(WorkflowError, "invalid sealed correction"):
                    correction_gate_kwargs_from_manifest(corrupt, "tennessee")
                with self.assertRaisesRegex(WorkflowError, "invalid sealed correction"):
                    correction_gate_kwargs_from_manifest(manifest, "georgetown")

    def test_expansion_nonregression_allows_inherited_debt_while_universe_grows(self):
        before = report()
        after = report()
        for value in (before, after):
            value["school_key"] = "houston"
            value["history_start_season"] = "1950-1951"
            value["source_validation_scope"] = {
                "mode": "FULL_SOURCE_PACKAGE",
                "scoped_source_games": 2394,
            }
            value["source_site_counts"] = {"material_gap_rows": 11}
        before["counts"]["target_canonical_games"] = 2296
        after["counts"]["target_canonical_games"] = 2395
        proof = prove_expansion(before, after)
        self.assertEqual(proof["mode"], EXPANSION_MODE)
        self.assertEqual(proof["added_target_canonical_games"], 99)
        self.assertTrue(proof["site_debt_remains"])
        verify_expansion_current(after, proof, "houston")


    def test_expansion_nonregression_allows_new_researched_nonblocking_categories(self):
        before = report(gaps=(), lost=0)
        after = report(gaps=(), lost=0)
        for value in (before, after):
            value["school_key"] = "ucf"
            value["history_start_season"] = "1984-1985"
            value["source_validation_scope"] = {
                "mode": "FULL_SOURCE_PACKAGE",
                "scoped_source_games": 1646,
            }
            value["source_site_counts"] = {
                "material_gap_rows": 76,
                "researched_unresolved_home_location_rows": 27,
            }
            value["status"] = "PASS"
            value["errors"] = []
            value["counts"]["target_canonical_games"] = 1273
        after["counts"]["target_canonical_games"] = 1646

        # These are real site findings, but not publication failures when the
        # permanent site report independently validates their research authority.
        accepted = {
            "home_missing_both": ["CBBG-HOME-1"],
            "home_missing_location": ["CBBG-HOME-1"],
            "home_missing_venue": ["CBBG-HOME-1", "CBBG-HOME-2"],
            "researched_unresolved_home_location": ["CBBG-HOME-1"],
            "researched_unresolved_home_venue": ["CBBG-HOME-2"],
            "neutral_missing_venue": ["CBBG-NEUTRAL"],
            "unknown_site_type": ["CBBG-UNKNOWN"],
        }
        for category, population in accepted.items():
            after["counts"][category] = len(population)
            after["examples"][category] = population

        proof = prove_expansion(before, after)
        self.assertEqual(proof["added_target_canonical_games"], 373)
        self.assertEqual(proof["expanded_site_status"], "PASS")
        self.assertFalse(proof["site_debt_remains"])

    def test_expansion_nonregression_still_rejects_new_blocking_population(self):
        before = report(gaps=(), lost=0)
        after = report(gaps=(), lost=0)
        for value in (before, after):
            value["school_key"] = "ucf"
            value["history_start_season"] = "1984-1985"
            value["source_validation_scope"] = {
                "mode": "FULL_SOURCE_PACKAGE",
                "scoped_source_games": 1646,
            }
            value["source_site_counts"] = {"material_gap_rows": 76}
            value["counts"]["target_canonical_games"] = 1273
            value["status"] = "PASS"
            value["errors"] = []
        after["counts"]["target_canonical_games"] = 1646
        after["counts"]["home_missing_both"] = 1
        after["examples"]["home_missing_both"] = ["CBBG-BLOCKED"]
        after["counts"]["strict_home_gap"] = 1
        after["examples"]["strict_home_gap"] = ["CBBG-BLOCKED"]
        after["status"] = "FAIL"
        after["errors"] = ["1 in-scope target HOME canonical game is missing authority"]
        with self.assertRaisesRegex(
            WorkflowError, "expansion introduced site failure strict_home_gap"
        ):
            prove_expansion(before, after)

    def test_expansion_nonregression_fails_closed_on_unclassified_new_report_error(self):
        before = report(gaps=(), lost=0)
        after = report(gaps=(), lost=0)
        for value in (before, after):
            value["school_key"] = "ucf"
            value["history_start_season"] = "1984-1985"
            value["source_validation_scope"] = {
                "mode": "FULL_SOURCE_PACKAGE",
                "scoped_source_games": 1646,
            }
            value["source_site_counts"] = {"material_gap_rows": 76}
            value["counts"]["target_canonical_games"] = 1273
            value["status"] = "PASS"
            value["errors"] = []
        after["counts"]["target_canonical_games"] = 1646
        after["status"] = "FAIL"
        after["errors"] = ["future implementation site failure category"]
        with self.assertRaisesRegex(
            WorkflowError, "expansion introduced site failure report-error"
        ):
            prove_expansion(before, after)

    def test_expansion_nonregression_rejects_new_site_failure(self):
        before = report(gaps=("CBBG-OLD",))
        after = report(gaps=("CBBG-OLD", "CBBG-NEW"))
        for value in (before, after):
            value["school_key"] = "houston"
            value["history_start_season"] = "1950-1951"
            value["source_validation_scope"] = {
                "mode": "FULL_SOURCE_PACKAGE",
                "scoped_source_games": 2394,
            }
            value["source_site_counts"] = {"material_gap_rows": 11}
        before["counts"]["target_canonical_games"] = 2296
        after["counts"]["target_canonical_games"] = 2395
        with self.assertRaisesRegex(WorkflowError, "expansion introduced site failure"):
            prove_expansion(before, after)

    def test_release_gate_carries_valid_expansion_proof(self):
        before = report()
        after = report()
        for value in (before, after):
            value["school_key"] = "houston"
            value["history_start_season"] = "1950-1951"
            value["source_validation_scope"] = {
                "mode": "FULL_SOURCE_PACKAGE",
                "scoped_source_games": 2394,
            }
            value["source_site_counts"] = {"material_gap_rows": 11}
        before["counts"]["target_canonical_games"] = 2296
        after["counts"]["target_canonical_games"] = 2395
        proof = prove_expansion(before, after)
        manifest = {
            "school_key": "houston",
            "summary": {"already_public": True},
            "execution": {"expansion_site_nonregression": proof},
        }
        kwargs = correction_gate_kwargs_from_manifest(manifest, "houston")
        self.assertEqual(kwargs["expansion_site_proof"]["mode"], EXPANSION_MODE)
        verify_expansion_current(after, kwargs["expansion_site_proof"], "houston")

    def test_expansion_pr_body_reports_nonregression(self):
        body = pr_body(
            {
                "school_key": "houston",
                "approved_plan_hash": "abc123",
                "summary": {
                    "already_public": True,
                    "source_rows": 2394,
                    "pre_cutoff_rows": 103,
                    "existing_game_matches": 2295,
                    "new_canonical_games": 99,
                },
                "decisions": [],
            },
            ["data/canonical/games.csv"],
            execution={"expansion_site_nonregression": {"mode": EXPANSION_MODE}},
        )
        self.assertIn("All-History expansion site nonregression — PASS", body)
        self.assertNotIn("implementation site completeness — PASS", body)

    def test_identity_only_pr_body_reports_correction_nonregression(self):
        body = pr_body(
            {
                "school_key": "vanderbilt",
                "approved_plan_hash": "abc123",
                "summary": {
                    "correction_transaction_kind": "SINGLE_GAME_IDENTITY",
                    "source_rows": 1,
                    "pre_cutoff_rows": 0,
                    "existing_game_matches": 1,
                    "new_canonical_games": 0,
                },
                "decisions": [],
            },
            ["data/canonical/games.csv"],
        )
        self.assertIn("correction-only site nonregression — PASS", body)
        self.assertNotIn("implementation site completeness — PASS", body)

    def test_current_report_must_match_exact_proved_after_state(self):
        after = report(lost=0)
        proof = prove(report(), after, "CBBG-0020298")
        drift = copy.deepcopy(after)
        drift["warnings"].append("unexpected detail")
        with self.assertRaisesRegex(WorkflowError, "does not match"):
            verify_current(drift, proof, "tennessee")
        with self.assertRaisesRegex(WorkflowError, "does not match"):
            verify_current(after, proof, "georgetown")
