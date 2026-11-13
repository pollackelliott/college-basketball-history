import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import all_history_expansion_implementation_acceptance as acceptance  # noqa: E402


def legacy_program(key: str) -> dict[str, str]:
    return {
        "program_key": key,
        "program_name": key.title(),
        "display_name": key.title(),
        "public_page_enabled": "Yes",
        "program_inception_season": "",
        "history_coverage_status": "LEGACY_TOP_LEVEL_ONLY",
        "history_start_season": "1970-1971",
        "history_scope_status": "OWNER_CONFIRMED",
        "history_scope_basis": "FIRST_TOP_LEVEL_SEASON",
        "history_scope_notes": "Accepted top-level history.",
        "history_scope_intervals": "",
    }


def complete_program(key: str) -> dict[str, str]:
    row = legacy_program(key)
    row["program_inception_season"] = "1960-1961"
    row["history_coverage_status"] = "COMPLETE_INSTITUTIONAL"
    return row


class AllHistoryExpansionImplementationAcceptanceTests(unittest.TestCase):
    def test_current_repository_passes_acceptance_gate(self):
        errors, summary = acceptance.evaluate_repository(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(summary["status"], "PASS")

    def test_successive_expansion_transitions_are_count_agnostic(self):
        rows = [
            legacy_program("alpha"),
            legacy_program("beta"),
            complete_program("gamma"),
        ]
        errors, summary = acceptance.portfolio_errors(rows)
        self.assertEqual(errors, [])
        self.assertEqual(summary["legacy"], 2)
        self.assertEqual(summary["complete"], 1)
        self.assertEqual(summary["eligible"], 2)

        transitioned = copy.deepcopy(rows)
        transitioned[0]["program_inception_season"] = "1965-1966"
        transitioned[0]["history_coverage_status"] = "COMPLETE_INSTITUTIONAL"
        errors, summary = acceptance.portfolio_errors(transitioned)
        self.assertEqual(errors, [])
        self.assertEqual(summary["legacy"], 1)
        self.assertEqual(summary["complete"], 2)
        self.assertEqual(summary["eligible"], 1)

    def test_complete_institutional_start_must_equal_inception(self):
        row = complete_program("alpha")
        row["program_inception_season"] = ""
        errors, _ = acceptance.portfolio_errors([row])
        self.assertTrue(any("missing inception" in error or "requires valid" in error
                            for error in errors))

    def test_curated_suite_includes_all_owner_phase_boundaries(self):
        patterns = set(acceptance.ACCEPTANCE_TEST_PATTERNS)
        required = {
            "test_all_history_expansion_integration.py",
            "test_all_history_expansion_venue_guard.py",
            "test_remote_implementation_expansion_phase0.py",
            "test_implementation_stage2.py",
            "test_remote_implementation_stage2_gate1_fill.py",
            "test_remote_implementation_stage2_preseal.py",
            "test_remote_implementation_stage2_seal.py",
            "test_remote_implementation_stage2_apply.py",
            "test_remote_implementation_stage2_continuation.py",
            "test_remote_implementation_release_readiness.py",
            "test_remote_implementation_release_preview.py",
            "test_remote_implementation_final_release.py",
            "test_remote_implementation_production.py",
            "test_all_history_expansion_implementation_composition.py",
        }
        self.assertTrue(required <= patterns)


if __name__ == "__main__":
    unittest.main()
