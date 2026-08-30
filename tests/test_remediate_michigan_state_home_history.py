from __future__ import annotations

import sys
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import remediate_michigan_state_home_history as msu


class MichiganStateHomeHistoryTests(unittest.TestCase):
    def test_armory_boundary(self):
        self.assertEqual(msu.facility_for_season("1898-1899"), ("michigan-state-armory", None))
        self.assertEqual(msu.facility_for_season("1917-1918"), ("michigan-state-armory", None))

    def test_im_circle_boundary(self):
        self.assertEqual(msu.facility_for_season("1918-1919"), ("michigan-state-im-circle-gymnasium", None))
        self.assertEqual(msu.facility_for_season("1928-1929"), ("michigan-state-im-circle-gymnasium", None))

    def test_outside_verified_early_chronology_is_held(self):
        self.assertEqual(msu.facility_for_season("1929-1930"), (None, "outside_verified_early_chronology"))
        self.assertEqual(msu.facility_for_season("1940-1941"), (None, "outside_verified_early_chronology"))

    def test_invalid_season_is_held(self):
        self.assertEqual(msu.facility_for_season("1918"), (None, "invalid_season"))
        self.assertEqual(msu.facility_for_season("1918-1920"), (None, "invalid_season"))

    def test_home_predicate(self):
        self.assertTrue(msu.michigan_state_home({"site_type": "TEAM_A_HOME", "team_a_key": "michigan-state", "team_b_key": "x"}))
        self.assertTrue(msu.michigan_state_home({"site_type": "TEAM_B_HOME", "team_a_key": "x", "team_b_key": "michigan-state"}))
        self.assertFalse(msu.michigan_state_home({"site_type": "NEUTRAL", "team_a_key": "michigan-state", "team_b_key": "x"}))
        self.assertFalse(msu.michigan_state_home({"site_type": "TEAM_A_HOME", "team_a_key": "x", "team_b_key": "michigan-state"}))

    def test_expected_facility_universe_is_fixed(self):
        self.assertEqual(
            msu.EXPECTED_FACILITY_COUNTS,
            {
                "michigan-state-armory": 120,
                "michigan-state-im-circle-gymnasium": 133,
            },
        )
        self.assertEqual(sum(msu.EXPECTED_FACILITY_COUNTS.values()), 253)

    def test_blank_or_expected_allows_blank_and_matching(self):
        msu.require_blank_or_expected({"city": ""}, "city", "East Lansing", "row")
        msu.require_blank_or_expected({"city": "East Lansing"}, "city", "East Lansing", "row")

    def test_blank_or_expected_rejects_conflict(self):
        with self.assertRaises(msu.MichiganStateHomeError):
            msu.require_blank_or_expected({"city": "Detroit"}, "city", "East Lansing", "row")

    def test_provenance_note_is_idempotent(self):
        marker = "[HOME_VENUE_CHRONOLOGY source=michigan-state/X]"
        self.assertEqual(msu.append_note("", marker), marker)
        self.assertEqual(msu.append_note(marker, marker), marker)
        self.assertEqual(msu.append_note("prior", marker), f"prior {marker}")


if __name__ == "__main__":
    unittest.main()
