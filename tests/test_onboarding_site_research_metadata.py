import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import _sync_site_metadata_to_source  # noqa: E402


class OnboardingSiteResearchMetadataTests(unittest.TestCase):
    def test_resolved_site_gap_clears_stale_research_metadata(self):
        source = {
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "",
            "city": "Indianapolis",
            "state": "IN",
            "curated_game_type": "REGULAR_SEASON",
            "site_research_status":
                "RESEARCHED_UNRESOLVED_HOME_VENUE",
            "site_research_basis":
                "Venue remained unresolved during research.",
        }

        canonical = {
            "venue_key": "hinkle-fieldhouse",
            "site_city": "Indianapolis",
            "site_state": "IN",
        }

        _sync_site_metadata_to_source(
            source,
            canonical,
            {"hinkle-fieldhouse": "Hinkle Fieldhouse"},
        )

        self.assertEqual(
            source["curated_venue_name"],
            "Hinkle Fieldhouse",
        )
        self.assertEqual(source["city"], "Indianapolis")
        self.assertEqual(source["state"], "IN")
        self.assertEqual(source["site_research_status"], "")
        self.assertEqual(source["site_research_basis"], "")

    def test_unresolved_site_gap_retains_research_metadata(self):
        source = {
            "curated_site_type": "UNKNOWN",
            "curated_venue_name": "",
            "city": "",
            "state": "",
            "curated_game_type": "REGULAR_SEASON",
            "site_research_status": "RESEARCHED_UNRESOLVED",
            "site_research_basis":
                "H/A/N remains historically unresolved.",
        }

        canonical = {
            "venue_key": "",
            "site_city": "",
            "site_state": "",
        }

        _sync_site_metadata_to_source(
            source,
            canonical,
            {},
        )

        self.assertEqual(
            source["site_research_status"],
            "RESEARCHED_UNRESOLVED",
        )
        self.assertEqual(
            source["site_research_basis"],
            "H/A/N remains historically unresolved.",
        )


if __name__ == "__main__":
    unittest.main()
