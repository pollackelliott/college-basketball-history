import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import onboarding_plan  # noqa: E402
from location_safety import registry_fallback_marker  # noqa: E402


class ReconciliationSiteMetadataResolutionTests(unittest.TestCase):
    def test_reused_venue_name_is_date_resolved_during_use_source(self):
        source = {
            "source_program_key": "depaul",
            "source_game_id": "TEST-CHARLOTTE",
            "season_label": "1991-1992",
            "game_date": "1991-12-07",
            "curated_venue_name": "Charlotte Coliseum",
            "city": "Charlotte",
            "state": "NC",
        }
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        venue_map = {
            "charlotte coliseum": [
                {
                    "venue_key": "charlotte-coliseum-1955",
                    "venue_id": "VEN-000040",
                    "city": "Charlotte",
                    "state": "NC",
                    "local_valid_from": "1976-03-13",
                    "local_valid_to": "1976-03-13",
                    "physical_opened": "1955",
                    "physical_closed": "1988",
                },
                {
                    "venue_key": "charlotte-coliseum-1988",
                    "venue_id": "VEN-000041",
                    "city": "Charlotte",
                    "state": "NC",
                    "local_valid_from": "1991-12-07",
                    "local_valid_to": "1991-12-07",
                    "physical_opened": "1988",
                    "physical_closed": "2005",
                },
            ]
        }

        onboarding_plan._sync_site_metadata_from_source(
            source,
            canonical,
            venue_map,
        )

        self.assertEqual(canonical["venue_key"], "charlotte-coliseum-1988")
        self.assertEqual(canonical["venue_id"], "VEN-000041")

    def test_resolved_physical_venue_registry_owns_canonical_geography(self):
        source = {
            "source_program_key": "depaul",
            "source_game_id": "TEST-ALLSTATE",
            "season_label": "2006-2007",
            "game_date": "2006-12-02",
            "curated_venue_name": "Allstate Arena",
            "city": "Chicago",
            "state": "IL",
        }
        canonical = {
            "site_type": "TEAM_A_HOME",
            "venue_key": "",
            "venue_id": "",
            "site_city": "Chicago",
            "site_state": "IL",
            "notes": "",
        }
        venue_map = {
            "allstate arena": [
                {
                    "venue_key": "allstate-arena",
                    "venue_id": "VEN-000004",
                    "city": "Rosemont",
                    "state": "IL",
                    "local_valid_from": "1980-12-01",
                    "local_valid_to": "2017-03-04",
                    "physical_opened": "1980",
                    "physical_closed": "",
                }
            ]
        }

        onboarding_plan._sync_site_metadata_from_source(
            source,
            canonical,
            venue_map,
        )

        self.assertEqual(canonical["venue_key"], "allstate-arena")
        self.assertEqual(canonical["venue_id"], "VEN-000004")
        self.assertEqual(canonical["site_city"], "Rosemont")
        self.assertEqual(canonical["site_state"], "IL")
        self.assertEqual(source["city"], "Chicago")

    def test_third_outcome_can_clear_temporary_venue_pair_and_old_marker(self):
        old_marker = registry_fallback_marker(
            "depaul",
            "DEPRAW-01277",
            "hearnes-center",
            "TEAM_B_HOME",
            ("venue_key", "venue_id", "site_city", "site_state"),
        )
        canonical = {
            "site_type": "TEAM_B_HOME",
            "designated_home_team_key": "missouri",
            "venue_key": "hearnes-center",
            "venue_id": "VEN-000077",
            "site_city": "Columbia",
            "site_state": "MO",
            "notes": old_marker,
        }

        retired = onboarding_plan._apply_canonical_patch(
            canonical,
            {
                "site_type": "NEUTRAL",
                "designated_home_team_key": "",
                "venue_key": "",
                "site_city": "Kansas City",
                "site_state": "MO",
            },
        )

        self.assertEqual(retired, 1)
        self.assertEqual(canonical["venue_key"], "")
        self.assertEqual(canonical["venue_id"], "")
        self.assertEqual(canonical["site_type"], "NEUTRAL")
        self.assertEqual(canonical["site_city"], "Kansas City")
        self.assertEqual(canonical["site_state"], "MO")
        self.assertNotIn("VENUE_REGISTRY_FALLBACK", canonical["notes"])

    def test_nonblank_patch_cannot_silently_change_physical_venue(self):
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "old-arena",
            "venue_id": "VEN-OLD",
            "site_city": "Old City",
            "site_state": "IL",
            "notes": "",
        }
        with self.assertRaises(onboarding_plan.WorkflowError):
            onboarding_plan._apply_canonical_patch(
                canonical,
                {"venue_key": "different-arena"},
            )


if __name__ == "__main__":
    unittest.main()
