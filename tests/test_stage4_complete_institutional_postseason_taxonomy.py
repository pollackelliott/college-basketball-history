import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from research_stage4_closeout import effective_parent_game_type


class CompleteInstitutionalPostseasonTaxonomyTests(unittest.TestCase):
    def test_outside_top_level_generic_postseason_is_not_promoted_by_subtype(self):
        row = {
            "research_game_id": "school-1964-65-001",
            "season": "1964-65",
            "game_type": "POSTSEASON",
            "postseason_type": "NCAA_TOURNAMENT",
            "top_level_classification": "OUTSIDE_ACCEPTED_TOP_LEVEL_SCOPE",
        }
        self.assertEqual(effective_parent_game_type(row), "POSTSEASON")

    def test_existing_legacy_subtype_refinement_is_unchanged_without_scope_marker(self):
        row = {
            "research_game_id": "school-2025-26-001",
            "season": "2025-26",
            "game_type": "POSTSEASON",
            "postseason_type": "NCAA_TOURNAMENT",
        }
        self.assertEqual(effective_parent_game_type(row), "NCAA_TOURNAMENT")


if __name__ == "__main__":
    unittest.main()
