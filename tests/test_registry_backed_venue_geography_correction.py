import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402


def venue_map():
    return {
        "allstate arena": [
            {
                "venue_key": "allstate-arena",
                "venue_id": "VEN-000004",
                "city": "Rosemont",
                "state": "IL",
                "local_valid_from": "1980-12-01",
                "local_valid_to": "2017-03-04",
                "physical_opened": "",
                "physical_closed": "",
            }
        ]
    }


def source(city="Rosemont", state="IL"):
    return {
        "source_program_key": "depaul",
        "source_game_id": "DEPRAW-01374",
        "season_label": "1982-1983",
        "game_date": "1983-03-25",
        "normalized_opponent_key": "ole-miss",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_venue_name": "Allstate Arena",
        "city": city,
        "state": state,
    }


def canonical(city="Chicago", state="IL", venue_key="", venue_id=""):
    return {
        "canonical_game_id": "CBBG-0032919",
        "site_type": "TEAM_A_HOME",
        "team_a_key": "depaul",
        "team_b_key": "ole-miss",
        "venue_key": venue_key,
        "venue_id": venue_id,
        "site_city": city,
        "site_state": state,
        "notes": "",
    }


class RegistryBackedVenueGeographyCorrectionTests(unittest.TestCase):
    def test_specific_source_and_registry_may_correct_coarse_canonical_geography(self):
        src = source()
        can = canonical()

        correction = ingest_school.registry_backed_geography_correction(
            src, can, venue_map()
        )
        self.assertIsNotNone(correction)
        self.assertEqual(correction["registry_city"], "Rosemont")

        conflict = ingest_school.venue_geography_enrichment_conflict(
            src, can, venue_map()
        )
        self.assertIsNone(conflict)

        changes = dict(
            ingest_school.canonical_enrichment_candidates(
                src, can, venue_map()
            )
        )
        self.assertEqual(changes["venue_key"], "allstate-arena")
        self.assertEqual(changes["venue_id"], "VEN-000004")
        self.assertEqual(changes["site_city"], "Rosemont")
        self.assertEqual(changes["site_state"], "IL")

    def test_source_registry_disagreement_still_blocks(self):
        src = source(city="Chicago", state="IL")
        can = canonical()

        correction = ingest_school.registry_backed_geography_correction(
            src, can, venue_map()
        )
        self.assertIsNone(correction)

        conflict = ingest_school.venue_geography_enrichment_conflict(
            src, can, venue_map()
        )
        self.assertIsNotNone(conflict)
        self.assertEqual(conflict["canonical_city"], "Chicago")
        self.assertEqual(conflict["registry_city"], "Rosemont")

    def test_existing_canonical_venue_identity_is_not_replaced(self):
        src = source()
        can = canonical(
            venue_key="some-existing-venue",
            venue_id="VEN-999999",
        )

        correction = ingest_school.registry_backed_geography_correction(
            src, can, venue_map()
        )
        self.assertIsNone(correction)

    def test_source_assertion_is_not_mutated(self):
        src = source()
        before = dict(src)
        ingest_school.canonical_enrichment_candidates(
            src, canonical(), venue_map()
        )
        self.assertEqual(src, before)


if __name__ == "__main__":
    unittest.main()
