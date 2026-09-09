import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import _sync_site_metadata_from_source  # noqa: E402


class ReconciliationHomeExceptionPropagationTests(unittest.TestCase):
    def test_use_source_home_sync_propagates_researched_unresolved_marker(self):
        source = {
            "source_program_key": "kansas-state",
            "source_game_id": "KSTATE-1",
            "normalized_opponent_key": "nebraska",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "",
            "city": "Manhattan",
            "state": "KS",
            "curated_game_type": "REGULAR_SEASON",
            "site_research_status": "RESEARCHED_UNRESOLVED_HOME_VENUE",
            "site_research_basis": (
                "Exhaustive historical research established Manhattan home "
                "status but not the exact physical building."
            ),
        }

        canonical = {
            "team_a_key": "kansas-state",
            "team_b_key": "nebraska",
            "site_type": "TEAM_A_HOME",
            "designated_home_team_key": "kansas-state",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }

        _sync_site_metadata_from_source(
            source,
            canonical,
            {},
        )

        marker = (
            "[RESEARCHED_UNRESOLVED_HOME_VENUE "
            "source=kansas-state/KSTATE-1]"
        )

        self.assertEqual(canonical["venue_key"], "")
        self.assertEqual(canonical["venue_id"], "")
        self.assertEqual(canonical["site_city"], "Manhattan")
        self.assertEqual(canonical["site_state"], "KS")
        self.assertIn(marker, canonical["notes"])

        # Repeating reconciliation must remain idempotent.
        _sync_site_metadata_from_source(
            source,
            canonical,
            {},
        )
        self.assertEqual(canonical["notes"].count(marker), 1)


if __name__ == "__main__":
    unittest.main()
