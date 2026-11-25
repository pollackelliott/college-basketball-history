"""Narrow acceptance of documented nonmaterial opponent-home scope annotations."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from site_completeness import source_site_completeness_report


class OpponentHomeMetadataWarningTests(unittest.TestCase):
    def row(self, **changes):
        row = {
            "source_game_id": "TEST-1",
            "season_label": "1949-1950",
            "curated_site_type": "OPPONENT_HOME",
            "curated_game_type": "REGULAR_SEASON",
            "source_venue_name": "",
            "curated_venue_name": "",
            "city": "",
            "state": "",
            "site_research_status": "RESEARCHED_PARTIAL",
            "site_research_basis": (
                "Exact opponent-home building research is outside the "
                "source school's Stage 3A responsibility."
            ),
        }
        row.update(changes)
        return row

    def check(self, **changes):
        row = self.row(**changes)
        return source_site_completeness_report(row.keys(), [row])

    def test_documented_regular_season_opponent_home_is_not_warning(self):
        report = self.check()
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["warnings"], [])
        self.assertEqual(report["counts"]["material_gap_rows"], 0)

    def test_separately_sourced_exact_away_venue_preserves_annotation(self):
        report = self.check(curated_venue_name="The Nest", city="Sacramento", state="CA")
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["warnings"], [])

    def test_original_source_venue_with_complete_curated_venue_still_warns(self):
        report = self.check(
            source_venue_name="Original Gym",
            curated_venue_name="Original Gym",
            city="Other",
            state="CA",
        )
        self.assertTrue(report["warnings"])

    def test_home_with_venue_still_warns(self):
        report = self.check(
            curated_site_type="SOURCE_PROGRAM_HOME",
            curated_venue_name="Home Gym",
            city="Home City",
            state="CA",
        )
        self.assertTrue(report["warnings"])

    def test_other_research_status_still_warns(self):
        report = self.check(site_research_status="RESEARCHED_UNRESOLVED")
        self.assertTrue(report["warnings"])

    def test_orphaned_status_still_errors(self):
        report = self.check(site_research_basis="")
        self.assertTrue(report["errors"])

    def test_postseason_complete_site_still_warns(self):
        report = self.check(
            curated_game_type="POSTSEASON",
            curated_venue_name="Arena",
            city="Site",
            state="CA",
        )
        self.assertTrue(report["warnings"])

    def test_missing_source_venue_with_no_research_status_still_blocks(self):
        report = self.check(
            source_venue_name="Source Gym",
            site_research_status="",
            site_research_basis="",
        )
        self.assertTrue(report["errors"])


if __name__ == "__main__":
    unittest.main()
