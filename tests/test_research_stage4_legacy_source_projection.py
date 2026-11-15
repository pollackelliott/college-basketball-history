#!/usr/bin/env python3
"""Regressions for fail-closed Stage 4 legacy-source and venue identity projection."""
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from onboarding_hardening import refresh_venue_assignment_summaries
from onboarding_plan import WorkflowError
from research_stage4 import _legacy_score_projection, _legacy_date_projection, _projection
from research_stage4_closeout import (
    _accepted_legacy_literal_enrichment_equivalent,
    effective_parent_game_type,
    compare_parent_semantics,
)


class Stage4LegacySourceRegression(unittest.TestCase):
    def test_split_physical_venues_use_explicit_parent_keys(self):
        venues = [
            dict(venue_key="garden-old", canonical_name="Garden", city="Metro", state="NY", aliases="", games_currently_assigned="9"),
            dict(venue_key="garden-new", canonical_name="Garden", city="Metro", state="NY", aliases="", games_currently_assigned="9"),
        ]
        games = [
            dict(source_game_id="one", curated_venue_name="Garden", city="Metro", state="NY", game_date="1930-01-02"),
            dict(source_game_id="two", curated_venue_name="Garden", city="Metro", state="NY", game_date="1980-02-03"),
        ]
        refreshed, report = refresh_venue_assignment_summaries(
            games, venues, accepted_venue_keys_by_game={"one": "garden-old", "two": "garden-new"},
        )
        self.assertEqual([x["games_currently_assigned"] for x in refreshed], ["1", "1"])
        self.assertEqual([x["first_assigned_game"] for x in refreshed], ["1930-01-02", "1980-02-03"])
        self.assertEqual(report["status"], "PASS")
        self.assertEqual([x["venue_key"] for x in refreshed], ["garden-old", "garden-new"])

    def test_same_name_missing_key_stops(self):
        venues = [dict(venue_key=k, canonical_name="Garden", city="Metro", state="NY", aliases="") for k in ("one", "two")]
        games = [dict(source_game_id="row", curated_venue_name="Garden", city="Metro", state="NY")]
        with self.assertRaises(WorkflowError):
            refresh_venue_assignment_summaries(games, venues, accepted_venue_keys_by_game={})

    def test_cbi_is_controlled_postseason_type_without_erasing_label(self):
        self.assertEqual(effective_parent_game_type({"game_type": "CBI"}), "POSTSEASON")
        self.assertEqual(effective_parent_game_type({"postseason_type": "CBI", "game_type": "POSTSEASON"}), "POSTSEASON")

    def test_loss_winner_first_and_literal_are_proved(self):
        row = {"source_score_raw": "96-49", "source_line_raw": "N 13 AT TECH L 96-49", "played_result": "L"}
        self.assertEqual(_legacy_score_projection(row, game_id="x")[:2], ("49", "96"))
        package = {"team_score": "49", "opponent_score": "96", "played_result": "L"}
        for field in ("team_score", "opponent_score"):
            self.assertTrue(_accepted_legacy_literal_enrichment_equivalent(row, package, field))
        self.assertFalse(_accepted_legacy_literal_enrichment_equivalent(row, {**package,"team_score":"96"}, "team_score"))

    def test_supplement_literal_with_trailing_round_is_accepted(self):
        row = {"source_score_raw": "70-74", "source_line_raw": "2026-03-17 at Wichita State L 70-74 NIT First Round", "played_result": "L"}
        self.assertEqual(_legacy_score_projection(row, game_id="x")[:2], ("70", "74"))

    def test_ambiguous_scores_rejected(self):
        row = {"source_score_raw": "80-50", "source_line_raw": "TEAM W 81-50", "played_result": "W"}
        self.assertTrue(_legacy_score_projection(row, game_id="x")[3])

    def test_exact_date_only_and_source_line_preserved(self):
        row = {"source_date_raw": "F 3", "season": "2025-26"}
        self.assertEqual(_legacy_date_projection(row, "x")[0], "2026-02-03")
        self.assertEqual(_legacy_date_projection({"source_date_raw":"D", "season":"2025-26"}, "x")[0], "")
        raw = {"source_line_raw": "F 3 AT TEAM W 40-31"}
        self.assertTrue(_accepted_legacy_literal_enrichment_equivalent(raw,{"raw_text":"F 3 AT TEAM W 40-31"},"raw_text"))
        self.assertFalse(_accepted_legacy_literal_enrichment_equivalent(raw,{"raw_text":"F 3 AT TEAM W 40-32"},"raw_text"))

    def test_contested_state_is_preserved_not_inferred(self):
        row = dict(season="1948-49", source_date_raw="D10",source_line_raw="D10 vs. Team W 78-43",
                   stage3a_final_venue_state="UT", stage3a_site_research_status="RESEARCHED_PARTIAL",
                   stage3a_site_research_basis="Guide says Logan; reciprocal says Salt Lake City; city contested")
        package = dict(city="", state="",notes="Accepted incomplete US locality: state='UT'; city remains contested; source evidence="+row["stage3a_site_research_basis"])
        self.assertTrue(_accepted_legacy_literal_enrichment_equivalent(row,package,"state"))
        self.assertFalse(_accepted_legacy_literal_enrichment_equivalent(row,{**package,"notes":""},"state"))
        self.assertFalse(_accepted_legacy_literal_enrichment_equivalent({**row,"stage3a_site_research_status":"UNRESOLVED"},package,"state"))


if __name__ == "__main__":
    unittest.main()
