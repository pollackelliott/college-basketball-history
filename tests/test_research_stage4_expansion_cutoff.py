"""Expansion Stage 4: immutable Stage 3B completed-season declaration compatibility."""

import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from expansion_stage4_coverage import ExpansionStage4CoverageError
from research_stage4_closeout import _expansion_stage3b_required_cutoff


class ExpansionStage3BCoverageCompatibilityTests(unittest.TestCase):
    def setUp(self):
        # Reproduces the accepted VCU Stage 3B COMPLETE status topology.
        self.nested = {
            "workflow_kind": "ALL_HISTORY_EXPANSION",
            "school_key": "vcu",
            "status": "COMPLETE",
            "research_base_sha": "df73675852ec5a43dfac50da0ee06d8bcabf8832",
            "research_coverage": {
                "primary_source_historical_cutoff": "2025-2026",
                "required_completed_season_cutoff": "2025-2026",
            },
        }

    def test_manifest_authenticated_nested_status_reuses_cutoff(self):
        self.assertNotIn("required_completed_season_cutoff", self.nested)
        self.assertEqual(
            _expansion_stage3b_required_cutoff(self.nested, "2025-2026"),
            "2025-2026",
        )
        # Reading the nested value cannot rewrite the immutable parent status.
        self.assertNotIn("required_completed_season_cutoff", self.nested)

    def test_matching_nested_and_top_level_declarations(self):
        self.nested["required_completed_season_cutoff"] = "2025-2026"
        self.assertEqual(
            _expansion_stage3b_required_cutoff(self.nested, "2025-2026"),
            "2025-2026",
        )

    def test_accepted_legacy_top_level_declaration(self):
        self.nested.pop("research_coverage")
        self.nested["required_completed_season_cutoff"] = "2025-2026"
        self.assertEqual(
            _expansion_stage3b_required_cutoff(self.nested, "2025-2026"),
            "2025-2026",
        )

    def test_conflicting_durable_values_fail_closed(self):
        self.nested["required_completed_season_cutoff"] = "2024-2025"
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "conflicting.*declarations"
        ):
            _expansion_stage3b_required_cutoff(self.nested, "2025-2026")

    def test_nested_value_must_match_independent_package_coverage(self):
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "declaration changed"
        ):
            _expansion_stage3b_required_cutoff(self.nested, "2024-2025")

    def test_no_durable_declaration_is_not_acceptance(self):
        self.nested.pop("research_coverage")
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "declaration missing"
        ):
            _expansion_stage3b_required_cutoff(self.nested, "2025-2026")

    def test_explicit_blank_or_invalid_declarations_fail_closed(self):
        self.nested["required_completed_season_cutoff"] = ""
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "declaration missing"
        ):
            _expansion_stage3b_required_cutoff(self.nested, "2025-2026")
        self.nested.pop("required_completed_season_cutoff")
        self.nested["research_coverage"] = "not an object"
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "not an object"
        ):
            _expansion_stage3b_required_cutoff(self.nested, "2025-2026")


if __name__ == "__main__":
    unittest.main()
