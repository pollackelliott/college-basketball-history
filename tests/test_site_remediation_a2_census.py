import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from site_remediation_a2_census import (  # noqa: E402
    _raw_indicator_state,
    _unknown_side,
    build_census,
)


class SiteRemediationA2CensusTests(unittest.TestCase):
    def test_unknown_side_is_participant_without_support(self):
        row = {
            "team_a_key": "alabama",
            "team_b_key": "lsu",
            "supporting_programs": "lsu",
        }
        self.assertEqual(_unknown_side(row), "alabama")

    def test_raw_indicator_recognizes_explicit_tokens(self):
        self.assertEqual(
            _raw_indicator_state({"source_site_candidates": "H"}),
            "EXPLICIT_RAW_HAN_TOKEN",
        )
        self.assertEqual(
            _raw_indicator_state({"source_site_candidates": "Neutral Site"}),
            "EXPLICIT_RAW_HAN_TEXT",
        )

    def test_raw_indicator_distinguishes_missing_and_other_values(self):
        self.assertEqual(
            _raw_indicator_state({"source_site_candidates": ""}),
            "NO_RAW_SITE_CANDIDATE",
        )
        self.assertEqual(
            _raw_indicator_state({"source_site_candidates": "Atlanta, GA"}),
            "OTHER_RAW_SITE_CANDIDATE",
        )

    def test_build_census_counts_unknown_side_and_site_only_risk(self):
        rows = [
            {
                "canonical_game_id": "CBBG-1",
                "season_label": "1950-1951",
                "team_a_key": "alabama",
                "team_b_key": "lsu",
                "proposed_site_type": "TEAM_B_HOME",
                "evidence_profile": "SITE_ASSERTION_ONLY",
                "review_bucket": "ONE_SIDED_SITE_ASSERTION_ONLY",
                "supporting_programs": "lsu",
                "supporting_assertion_count": "1",
                "source_site_forms": "SOURCE_PROGRAM_HOME",
                "source_site_candidates": "H",
                "match_methods": "EXISTING_SOURCE_ASSERTION",
                "raw_text_excerpt": "H LSU",
            },
            {
                "canonical_game_id": "CBBG-2",
                "season_label": "1960-1961",
                "team_a_key": "alabama",
                "team_b_key": "georgia",
                "proposed_site_type": "NEUTRAL",
                "evidence_profile": "VENUE_AND_LOCATION",
                "review_bucket": "ONE_SIDED_WITH_PHYSICAL_SUPPORT",
                "supporting_programs": "georgia",
                "supporting_assertion_count": "1",
                "source_site_forms": "NEUTRAL",
                "source_site_candidates": "N",
                "match_methods": "EXISTING_SOURCE_ASSERTION",
                "raw_text_excerpt": "N Atlanta",
            },
            {
                "canonical_game_id": "CBBG-3",
                "season_label": "1970-1971",
                "team_a_key": "texas",
                "team_b_key": "purdue",
                "proposed_site_type": "TEAM_A_HOME",
                "evidence_profile": "SITE_ASSERTION_ONLY",
                "review_bucket": "ONE_SIDED_SITE_ASSERTION_ONLY",
                "supporting_programs": "texas",
                "supporting_assertion_count": "1",
                "source_site_forms": "SOURCE_PROGRAM_HOME",
                "source_site_candidates": "Austin",
                "match_methods": "EXISTING_SOURCE_ASSERTION",
                "raw_text_excerpt": "Texas vs Purdue",
            },
        ]
        fake = {"summary": {"status": "PASS"}, "rows": rows}
        with tempfile.TemporaryDirectory() as temporary, patch(
            "site_remediation_a2_census.build_a2_review",
            return_value=fake,
        ):
            census = build_census(Path(temporary))

        self.assertEqual(census["candidate_games"], 3)
        self.assertEqual(census["counts"]["unknown_side_program"]["alabama"], 2)
        self.assertEqual(census["counts"]["unknown_side_program"]["purdue"], 1)
        self.assertEqual(census["counts"]["raw_indicator_state"]["EXPLICIT_RAW_HAN_TOKEN"], 2)
        self.assertEqual(census["counts"]["raw_indicator_state"]["OTHER_RAW_SITE_CANDIDATE"], 1)
        self.assertEqual(census["site_only_without_explicit_raw_count"], 1)
        self.assertEqual(len(census["non_alabama_unknown_side"]), 1)
        self.assertEqual(
            census["non_alabama_unknown_side"][0]["canonical_game_id"],
            "CBBG-3",
        )


if __name__ == "__main__":
    unittest.main()
