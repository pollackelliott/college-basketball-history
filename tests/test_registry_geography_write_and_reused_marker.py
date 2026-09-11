import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
import validate_data  # noqa: E402


class RegistryGeographyWriteTests(unittest.TestCase):
    def test_proven_registry_geography_replaces_coarse_nonblank_canonical_location(self):
        source = {
            "source_program_key": "depaul",
            "source_game_id": "DEPRAW-01374",
            "season_label": "1982-1983",
            "game_date": "1983-03-25",
            "normalized_opponent_key": "ole-miss",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "Allstate Arena",
            "city": "Rosemont",
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
        metadata = {
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

        applied = dict(
            ingest_school.apply_canonical_enrichment_candidates(
                source,
                canonical,
                metadata,
            )
        )
        self.assertEqual(applied["venue_key"], "allstate-arena")
        self.assertEqual(applied["venue_id"], "VEN-000004")
        self.assertEqual(applied["site_city"], "Rosemont")
        self.assertEqual(applied["site_state"], "IL")
        self.assertEqual(canonical["site_city"], "Rosemont")
        self.assertEqual(canonical["site_state"], "IL")


class ReusedVenueMarkerValidationTests(unittest.TestCase):
    def metadata(self):
        return {
            "madison square garden": [
                {
                    "venue_key": "madison-square-garden-1925",
                    "venue_id": "VEN-000123",
                    "city": "New York",
                    "state": "NY",
                    "local_valid_from": "1930-01-01",
                    "local_valid_to": "1967-12-31",
                    "physical_opened": "1925",
                    "physical_closed": "1968",
                },
                {
                    "venue_key": "madison-square-garden-1968",
                    "venue_id": "VEN-000124",
                    "city": "New York",
                    "state": "NY",
                    "local_valid_from": "1968-02-11",
                    "local_valid_to": "2026-03-11",
                    "physical_opened": "1968-02-11",
                    "physical_closed": "",
                },
            ]
        }

    def test_undated_1935_assertion_validates_as_msg_iii(self):
        assertion = {
            "source_game_id": "DEPRAW-00201",
            "season_label": "1935-1936",
            "game_date": "",
            "curated_venue_name": "Madison Square Garden",
        }
        self.assertEqual(
            validate_data.resolved_assertion_venue_key(
                assertion,
                self.metadata(),
            ),
            "madison-square-garden-1925",
        )

    def test_1970_assertion_validates_as_msg_iv(self):
        assertion = {
            "source_game_id": "LATE",
            "season_label": "1970-1971",
            "game_date": "1970-12-01",
            "curated_venue_name": "Madison Square Garden",
        }
        self.assertEqual(
            validate_data.resolved_assertion_venue_key(
                assertion,
                self.metadata(),
            ),
            "madison-square-garden-1968",
        )

    def test_transition_ambiguity_still_stops(self):
        assertion = {
            "source_game_id": "TRANSITION",
            "season_label": "1967-1968",
            "game_date": "",
            "curated_venue_name": "Madison Square Garden",
        }
        with self.assertRaises(ValueError):
            validate_data.resolved_assertion_venue_key(
                assertion,
                self.metadata(),
            )


if __name__ == "__main__":
    unittest.main()
