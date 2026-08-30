import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remediate_mississippi_state_home_history import (  # noqa: E402
    EXCEPTION_STATUS,
    MISSISSIPPI_COLISEUM,
    classify_source_gap,
    marker,
    next_discrepancy_id,
    primary_for_date,
)


class MississippiStateHomeRemediationTests(unittest.TestCase):
    def source(self, **overrides):
        row = {
            "source_game_id": "MSURAW-X",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "",
            "city": "Starkville",
            "state": "MS",
            "game_date": "1915-01-01",
        }
        row.update(overrides)
        return row

    def test_pre_tin_starkville_is_researched_unresolved_not_fabricated(self):
        action, facility, basis = classify_source_gap(self.source())
        self.assertEqual(action, "UNRESOLVED_HOME_VENUE")
        self.assertIsNone(facility)
        self.assertIn("does not safely identify the exact physical home venue", basis)

    def test_pre_1962_jackson_is_researched_unresolved(self):
        action, facility, basis = classify_source_gap(
            self.source(city="Jackson", game_date="1960-01-01")
        )
        self.assertEqual(action, "UNRESOLVED_HOME_VENUE")
        self.assertIsNone(facility)
        self.assertIn("pre-1962", basis)

    def test_mississippi_coliseum_relationship_begins_1962_12_15(self):
        before = classify_source_gap(
            self.source(city="Jackson", game_date="1962-12-14")
        )
        opener = classify_source_gap(
            self.source(city="Jackson", game_date="1962-12-15")
        )
        self.assertEqual(before[0], "UNRESOLVED_HOME_VENUE")
        self.assertEqual(opener[0], "ASSIGN_VENUE")
        self.assertEqual(opener[1], MISSISSIPPI_COLISEUM)

    def test_primary_home_boundaries(self):
        self.assertIsNone(primary_for_date("1932-01-24"))
        self.assertEqual(primary_for_date("1932-01-25")["venue_key"], "tin-gym")
        self.assertEqual(primary_for_date("1950-12-14")["venue_key"], "tin-gym")
        self.assertEqual(
            primary_for_date("1950-12-15")["venue_key"], "mccarthy-gymnasium"
        )
        self.assertEqual(
            primary_for_date("1975-11-30")["venue_key"], "mccarthy-gymnasium"
        )
        self.assertEqual(
            primary_for_date("1975-12-01")["venue_key"], "humphrey-coliseum"
        )

    def test_exception_marker_is_source_specific(self):
        self.assertEqual(
            marker("MSURAW-00001"),
            "[RESEARCHED_UNRESOLVED_HOME_VENUE source=mississippi-state/MSURAW-00001]",
        )
        self.assertEqual(EXCEPTION_STATUS, "RESEARCHED_UNRESOLVED_HOME_VENUE")

    def test_next_discrepancy_id(self):
        rows = [
            {"discrepancy_id": "DISC-000007"},
            {"discrepancy_id": "DISC-001976"},
            {"discrepancy_id": "legacy-other"},
        ]
        self.assertEqual(next_discrepancy_id(rows), "DISC-001977")


if __name__ == "__main__":
    unittest.main()
