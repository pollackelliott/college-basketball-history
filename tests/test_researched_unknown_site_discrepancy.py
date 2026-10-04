import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402


class ResearchedUnknownSiteDiscrepancyTests(unittest.TestCase):
    def source(self, **changes):
        row = {
            "source_program_key": "pittsburgh",
            "normalized_opponent_key": "west-virginia",
            "game_date": "",
            "team_score": "",
            "opponent_score": "",
            "played_result": "",
            "overtime_periods": "",
            "curated_site_type": "UNKNOWN",
            "curated_game_type": "",
            "curated_postseason_round": "",
            "site_research_status": "",
            "site_research_basis": "",
        }
        row.update(changes)
        return row

    def canonical(self, **changes):
        row = {
            "game_date": "",
            "team_a_key": "pittsburgh",
            "team_b_key": "west-virginia",
            "team_a_score": "",
            "team_b_score": "",
            "result_winner_team_key": "",
            "overtime_periods": "",
            "site_type": "TEAM_A_HOME",
            "game_type": "",
            "postseason_round": "",
        }
        row.update(changes)
        return row

    def test_researched_unresolved_unknown_competes_with_known_canonical_site(self):
        source = self.source(
            site_research_status="RESEARCHED_UNRESOLVED",
            site_research_basis=(
                "Target and reciprocal institutional evidence conflict on H/A/N; "
                "bounded research could not resolve the classification."
            ),
        )

        self.assertEqual(
            ingest_school.discrepancy_candidates(source, self.canonical()),
            [("site_type", "UNKNOWN", "TEAM_A_HOME")],
        )

    def test_ordinary_unknown_remains_non_authoritative(self):
        self.assertEqual(
            ingest_school.discrepancy_candidates(self.source(), self.canonical()),
            [],
        )

    def test_incomplete_research_metadata_does_not_gain_authority(self):
        for changes in (
            {"site_research_status": "RESEARCHED_UNRESOLVED"},
            {
                "site_research_basis": (
                    "Evidence was reviewed, but the controlled research status is absent."
                )
            },
            {
                "site_research_status": "RESEARCHED_PARTIAL",
                "site_research_basis": "Only locality research remains incomplete.",
            },
        ):
            with self.subTest(changes=changes):
                self.assertEqual(
                    ingest_school.discrepancy_candidates(
                        self.source(**changes),
                        self.canonical(),
                    ),
                    [],
                )

    def test_researched_unknown_does_not_conflict_with_unknown_canonical_site(self):
        source = self.source(
            site_research_status="RESEARCHED_UNRESOLVED",
            site_research_basis="H/A/N remains unresolved after bounded research.",
        )

        self.assertEqual(
            ingest_school.discrepancy_candidates(
                source,
                self.canonical(site_type="UNKNOWN"),
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
