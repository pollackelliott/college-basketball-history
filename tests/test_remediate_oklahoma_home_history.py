import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remediate_oklahoma_home_history import (  # noqa: E402
    facility_key_for,
    oklahoma_home,
    site_patch,
)


class OklahomaHomeChronologyTests(unittest.TestCase):
    def test_primary_era_boundaries(self):
        self.assertEqual(
            facility_key_for({"season_label": "1907-1908", "game_date": ""}),
            ("ou-gymnasium", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1919-1920", "game_date": ""}),
            ("ou-rotc-armory", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1928-1929", "game_date": ""}),
            ("mccasland-field-house", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1974-1975", "game_date": ""}),
            ("mccasland-field-house", None),
        )

    def test_1928_transition_is_date_aware(self):
        self.assertEqual(
            facility_key_for({"season_label": "1927-1928", "game_date": "1928-01-12"}),
            ("ou-rotc-armory", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1927-1928", "game_date": "1928-01-13"}),
            ("mccasland-field-house", None),
        )
        key, reason = facility_key_for({"season_label": "1927-1928", "game_date": ""})
        self.assertIsNone(key)
        self.assertEqual(reason, "1927-28_transition_missing_date")

    def test_1975_transition_is_date_aware(self):
        self.assertEqual(
            facility_key_for({"season_label": "1975-1976", "game_date": "1975-11-30"}),
            ("mccasland-field-house", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1975-1976", "game_date": "1975-12-01"}),
            ("lloyd-noble-center", None),
        )
        key, reason = facility_key_for({"season_label": "1975-1976", "game_date": ""})
        self.assertIsNone(key)
        self.assertEqual(reason, "1975-76_transition_missing_date")

    def test_modern_blank_is_not_blanket_lloyd_noble(self):
        key, reason = facility_key_for({"season_label": "2012-2013", "game_date": "2012-12-31"})
        self.assertIsNone(key)
        self.assertEqual(reason, "post_1975_primary_history_not_sufficient")

    def test_oklahoma_home_requires_independent_site_classification(self):
        self.assertTrue(
            oklahoma_home(
                {"site_type": "TEAM_A_HOME", "team_a_key": "oklahoma", "team_b_key": "texas"}
            )
        )
        self.assertFalse(
            oklahoma_home(
                {"site_type": "UNKNOWN", "team_a_key": "oklahoma", "team_b_key": "texas"}
            )
        )

    def test_site_patch_fills_blanks_but_refuses_conflicts(self):
        facility = {
            "venue_key": "ou-gymnasium",
            "venue_id": "VEN-000341",
            "display_name": "OU Gymnasium",
            "city": "Norman",
            "state": "OK",
        }
        patch, conflict = site_patch(
            {"venue_key": "", "venue_id": "", "site_city": "", "site_state": ""},
            facility,
            canonical=True,
        )
        self.assertIsNone(conflict)
        self.assertEqual(patch["venue_key"], "ou-gymnasium")
        self.assertEqual(patch["venue_id"], "VEN-000341")
        self.assertEqual((patch["site_city"], patch["site_state"]), ("Norman", "OK"))

        patch, conflict = site_patch(
            {"venue_key": "other-arena", "venue_id": "VEN-999999", "site_city": "Norman", "site_state": "OK"},
            facility,
            canonical=True,
        )
        self.assertEqual(patch, {})
        self.assertTrue(conflict.startswith("existing_canonical_venue_key:"))


if __name__ == "__main__":
    unittest.main()
