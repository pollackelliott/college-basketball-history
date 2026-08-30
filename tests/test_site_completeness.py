import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from site_completeness import source_site_completeness_report  # noqa: E402


FIELDS = [
    "source_game_id",
    "season_label",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "site_research_status",
    "site_research_basis",
]


def row(**overrides):
    value = {
        "source_game_id": "TESTRAW-00001",
        "season_label": "2025-2026",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_venue_name": "Example Arena",
        "city": "Example City",
        "state": "EX",
        "curated_game_type": "REGULAR_SEASON",
        "site_research_status": "",
        "site_research_basis": "",
    }
    value.update(overrides)
    return value


class SourceSiteCompletenessTests(unittest.TestCase):
    def test_complete_home_row_has_no_material_gap(self):
        report = source_site_completeness_report(FIELDS, [row()])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["material_gap_rows"], 0)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 0)

    def test_unaccounted_home_blank_blocks(self):
        report = source_site_completeness_report(
            FIELDS,
            [row(curated_venue_name="", city="", state="")],
        )
        self.assertEqual(report["counts"]["material_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 1)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)
        self.assertEqual(report["counts"]["home_missing_venue"], 1)
        self.assertEqual(report["counts"]["home_missing_location"], 1)
        self.assertEqual(report["counts"]["home_missing_both"], 1)
        self.assertTrue(any("material site-gap" in error for error in report["errors"]))
        self.assertTrue(any("non-waivable" in error for error in report["errors"]))

    def test_researched_unresolved_home_blank_still_blocks_freeze(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    city="",
                    state="",
                    site_research_status="RESEARCHED_UNRESOLVED",
                    site_research_basis=(
                        "Primary ledger and facility chronology checked; exact site unsupported."
                    ),
                )
            ],
        )
        self.assertEqual(report["counts"]["researched_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)
        self.assertTrue(any("non-waivable" in error for error in report["errors"]))

    def test_partial_home_gap_still_blocks_freeze(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    site_research_status="RESEARCHED_PARTIAL",
                    site_research_basis=(
                        "Official schedule establishes Norman, Oklahoma; exact building unresolved."
                    ),
                )
            ],
        )
        self.assertEqual(report["counts"]["home_missing_venue"], 1)
        self.assertNotIn("home_missing_location", report["counts"])
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)
        self.assertTrue(any("non-waivable" in error for error in report["errors"]))

    def test_unknown_site_type_requires_accounting(self):
        report = source_site_completeness_report(
            FIELDS,
            [row(curated_site_type="UNKNOWN")],
        )
        self.assertEqual(report["counts"]["unknown_site_type"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 1)

    def test_away_regular_season_blank_is_not_a_research_freeze_gap(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="OPPONENT_HOME",
                    curated_venue_name="",
                    city="",
                    state="",
                )
            ],
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["material_gap_rows"], 0)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 0)

    def test_non_ncaa_neutral_and_postseason_gaps_are_counted(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="NEUTRAL",
                    curated_venue_name="",
                    city="",
                    state="",
                    curated_game_type="NIT",
                    site_research_status="RESEARCHED_UNRESOLVED",
                    site_research_basis="NIT site sources checked; exact historical site unsupported.",
                )
            ],
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["neutral_missing_venue"], 1)
        self.assertEqual(report["counts"]["neutral_missing_location"], 1)
        self.assertEqual(report["counts"]["postseason_missing_venue"], 1)
        self.assertEqual(report["counts"]["postseason_missing_location"], 1)
        self.assertEqual(report["counts"]["material_gap_rows"], 1)

    def test_ncaa_neutral_blank_is_not_waivable_here(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="NEUTRAL",
                    curated_venue_name="",
                    city="",
                    state="",
                    curated_game_type="NCAA_TOURNAMENT",
                    site_research_status="RESEARCHED_UNRESOLVED",
                    site_research_basis="This marker must not substitute for the strict NCAA gate.",
                )
            ],
        )
        # NCAA completeness is deliberately enforced by onboarding_hardening's existing
        # strict gate, not by this waivable accounting layer.
        self.assertEqual(report["counts"]["material_gap_rows"], 0)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)
        self.assertEqual(len(report["warnings"]), 1)

    def test_status_and_basis_must_be_paired(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    site_research_status="RESEARCHED_PARTIAL",
                    site_research_basis="",
                )
            ],
        )
        self.assertTrue(any("site_research_basis is required" in error for error in report["errors"]))
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 1)

    def test_decade_breakdown_exposes_chronology_holes(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    source_game_id="A",
                    season_label="1907-1908",
                    curated_venue_name="",
                    city="",
                    state="",
                ),
                row(
                    source_game_id="B",
                    season_label="1975-1976",
                    curated_venue_name="",
                    city="",
                    state="",
                ),
            ],
        )
        self.assertEqual(report["by_decade"]["home_missing_both"]["1900s"], 1)
        self.assertEqual(report["by_decade"]["home_missing_both"]["1970s"], 1)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 2)


if __name__ == "__main__":
    unittest.main()
