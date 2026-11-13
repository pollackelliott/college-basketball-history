import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_io import Stop  # noqa: E402
from stage2_candidate_runtime_rehearsal import (  # noqa: E402
    candidate_census_decision_universe,
    classify_candidate_result,
    validate_candidate_scope,
)


class CandidateRuntimeScopeTests(unittest.TestCase):
    def test_generic_tooling_paths_are_allowed(self):
        validate_candidate_scope([
            "tools/onboarding_plan.py",
            "tests/test_example.py",
            "docs/implementation-efficiency-recovery.md",
            ".github/workflows/example.yml",
            "AGENTS.md",
        ])

    def test_basketball_data_path_is_rejected(self):
        with self.assertRaisesRegex(Stop, "NON_TOOLING_PATHS"):
            validate_candidate_scope([
                "tools/onboarding_plan.py",
                "schools/example/source-games.csv",
            ])

    def test_reference_data_path_is_rejected(self):
        with self.assertRaisesRegex(Stop, "NON_TOOLING_PATHS"):
            validate_candidate_scope([
                "data/reference/venues.csv",
            ])


class CandidateRuntimeDecisionUniverseTests(unittest.TestCase):
    def test_candidate_census_exposes_recomputed_decision_universe(self):
        value = "a" * 64
        self.assertEqual(
            candidate_census_decision_universe(
                {
                    "status": {
                        "preflight": {
                            "decision_universe_sha256": value,
                        }
                    }
                }
            ),
            value,
        )

    def test_candidate_census_requires_decision_universe_fingerprint(self):
        with self.assertRaisesRegex(
            Stop,
            "CANDIDATE_REHEARSAL_DECISION_UNIVERSE_MISSING",
        ):
            candidate_census_decision_universe(
                {"status": {"preflight": {}}}
            )


class CandidateRuntimeClassificationTests(unittest.TestCase):
    def test_gate1_ready_is_terminal_success(self):
        self.assertEqual(
            classify_candidate_result(
                {"last_error": "old blocker"},
                {"stage2_status": "OWNER_GATE_1_READY", "status": {}},
            ),
            "RESOLVED_TO_GATE1",
        )

    def test_different_blocker_is_material_progress(self):
        self.assertEqual(
            classify_candidate_result(
                {"last_error": "old blocker"},
                {
                    "stage2_status": "BLOCKED",
                    "status": {"last_error": "different blocker"},
                },
            ),
            "ADVANCED_TO_DIFFERENT_BLOCKER",
        )

    def test_same_coarse_site_error_with_reduced_blocker_population_advances(self):
        baseline_site = {
            "counts": {
                "strict_home_gap_rows": 13,
                "unaccounted_public_gap_rows": 5,
            },
            "examples": {
                "strict_home_gap_rows": ["HOME-1"],
                "unaccounted_public_gap_rows": [
                    "NEUTRAL-1",
                    "NEUTRAL-2",
                    "HOME-1",
                    "HOME-2",
                    "HOME-3",
                ],
            },
        }
        candidate_site = {
            "counts": {
                "strict_home_gap_rows": 13,
                "unaccounted_public_gap_rows": 3,
            },
            "examples": {
                "strict_home_gap_rows": ["HOME-1"],
                "unaccounted_public_gap_rows": [
                    "HOME-1",
                    "HOME-2",
                    "HOME-3",
                ],
            },
        }
        self.assertEqual(
            classify_candidate_result(
                {
                    "last_error": "site_completeness failed with exit code 1",
                    "site_diagnostic": baseline_site,
                },
                {
                    "stage2_status": "BLOCKED",
                    "status": {
                        "last_error": "site_completeness failed with exit code 1",
                    },
                    "site_diagnostic": candidate_site,
                },
            ),
            "ADVANCED_TO_DIFFERENT_BLOCKER",
        )

    def test_same_coarse_site_error_with_same_structured_blocker_is_no_progress(self):
        site = {
            "counts": {
                "strict_home_gap_rows": 13,
                "unaccounted_public_gap_rows": 5,
            },
            "examples": {
                "strict_home_gap_rows": ["HOME-1"],
                "unaccounted_public_gap_rows": ["NEUTRAL-1", "HOME-1"],
            },
        }
        self.assertEqual(
            classify_candidate_result(
                {
                    "last_error": "site_completeness failed with exit code 1",
                    "site_diagnostic": site,
                },
                {
                    "stage2_status": "BLOCKED",
                    "status": {
                        "last_error": "site_completeness failed with exit code 1",
                    },
                    "site_diagnostic": site,
                },
            ),
            "NO_PROGRESS_SAME_BLOCKER",
        )

    def test_same_blocker_is_no_progress(self):
        self.assertEqual(
            classify_candidate_result(
                {"last_error": "same blocker"},
                {
                    "stage2_status": "BLOCKED",
                    "status": {"last_error": "same blocker"},
                },
            ),
            "NO_PROGRESS_SAME_BLOCKER",
        )

    def test_missing_baseline_error_still_classifies_new_blocker(self):
        self.assertEqual(
            classify_candidate_result(
                {},
                {
                    "stage2_status": "BLOCKED",
                    "status": {"last_error": "candidate blocker"},
                },
            ),
            "ADVANCED_TO_DIFFERENT_BLOCKER",
        )


if __name__ == "__main__":
    unittest.main()
