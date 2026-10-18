"""Exact population proof for existing published-site debt in one-game corrections."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from correction_site_nonregression import prove, digest, verify_current
from onboarding_plan import WorkflowError
from onboard_school import correction_gate_kwargs_from_manifest


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
        manifest = {
            "school_key": "tennessee",
            "summary": {
                "correction_transaction_kind": "SINGLE_GAME_IDENTITY_SITE",
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

    def test_current_report_must_match_exact_proved_after_state(self):
        after = report(lost=0)
        proof = prove(report(), after, "CBBG-0020298")
        drift = copy.deepcopy(after)
        drift["warnings"].append("unexpected detail")
        with self.assertRaisesRegex(WorkflowError, "does not match"):
            verify_current(drift, proof, "tennessee")
        with self.assertRaisesRegex(WorkflowError, "does not match"):
            verify_current(after, proof, "georgetown")
