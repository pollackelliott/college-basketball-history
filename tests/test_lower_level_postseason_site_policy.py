"""Adversarial tests for the lower-level generic POSTSEASON site-policy classifier."""

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from site_completeness import (  # noqa: E402
    LOWER_LEVEL_POSTSEASON_MODERN_START,
    lower_level_postseason_site_disposition,
)


def row(
    season,
    game_type="POSTSEASON",
    *,
    venue="",
    city="",
    state="",
):
    return {
        "season_label": season,
        "curated_game_type": game_type,
        "curated_venue_name": venue,
        "city": city,
        "state": state,
    }


class LowerLevelPostseasonSitePolicyTests(unittest.TestCase):
    def classify(
        self,
        value,
        *,
        target_top_level=False,
        target_home=False,
        research_accounted=True,
        shared_top_level_obligation=False,
    ):
        return lower_level_postseason_site_disposition(
            value,
            target_top_level=target_top_level,
            target_home=target_home,
            research_accounted=research_accounted,
            shared_top_level_obligation=shared_top_level_obligation,
        )

    def test_historical_locality_known_blank_venue_researched_is_nonblocking(self):
        result = self.classify(
            row("1995-1996", city="Springfield", state="MO")
        )
        self.assertTrue(result["applies"])
        self.assertEqual(
            result["era"],
            "HISTORICAL_1995_96_OR_EARLIER",
        )
        self.assertTrue(result["venue_missing"])
        self.assertFalse(result["locality_missing"])
        self.assertTrue(result["nonblocking"])

    def test_modern_blank_venue_requires_explicit_research_accounting(self):
        value = row("1996-1997", city="Springfield", state="MO")
        researched = self.classify(value, research_accounted=True)
        unresearched = self.classify(value, research_accounted=False)
        self.assertEqual(researched["era"], "MODERN_1996_97_PLUS")
        self.assertTrue(researched["nonblocking"])
        self.assertFalse(unresearched["nonblocking"])

    def test_unresolved_locality_can_be_nonblocking_only_when_researched(self):
        value = row("2001-2002", venue="Example Arena")
        researched = self.classify(value, research_accounted=True)
        unresearched = self.classify(value, research_accounted=False)
        self.assertTrue(researched["locality_missing"])
        self.assertTrue(researched["material_gap"])
        self.assertTrue(researched["nonblocking"])
        self.assertFalse(unresearched["nonblocking"])

    def test_same_unresolved_row_without_research_accounting_remains_blocking(self):
        result = self.classify(
            row("1994-1995"),
            research_accounted=False,
        )
        self.assertTrue(result["applies"])
        self.assertTrue(result["material_gap"])
        self.assertFalse(result["research_accounted"])
        self.assertFalse(result["nonblocking"])

    def test_ncaa_tournament_never_receives_relaxation(self):
        result = self.classify(row("2005-2006", "NCAA_TOURNAMENT"))
        self.assertFalse(result["applies"])
        self.assertFalse(result["nonblocking"])

    def test_nit_never_receives_relaxation(self):
        result = self.classify(row("2005-2006", "NIT"))
        self.assertFalse(result["applies"])
        self.assertFalse(result["nonblocking"])

    def test_conference_tournament_never_receives_relaxation(self):
        result = self.classify(row("2005-2006", "CONFERENCE_TOURNAMENT"))
        self.assertFalse(result["applies"])
        self.assertFalse(result["nonblocking"])

    def test_top_level_postseason_never_receives_relaxation(self):
        result = self.classify(
            row("2005-2006"),
            target_top_level=True,
        )
        self.assertFalse(result["applies"])
        self.assertFalse(result["nonblocking"])

    def test_target_home_never_receives_relaxation(self):
        result = self.classify(
            row("2005-2006"),
            target_home=True,
        )
        self.assertFalse(result["applies"])
        self.assertFalse(result["nonblocking"])

    def test_regular_season_neutral_never_receives_relaxation(self):
        value = row("2005-2006", "REGULAR_SEASON")
        value["curated_site_type"] = "NEUTRAL"
        result = self.classify(value)
        self.assertFalse(result["applies"])
        self.assertFalse(result["nonblocking"])

    def test_shared_top_level_obligation_disables_relaxation(self):
        result = self.classify(
            row("2005-2006"),
            shared_top_level_obligation=True,
        )
        self.assertFalse(result["applies"])
        self.assertFalse(result["nonblocking"])

    def test_era_boundary_is_exact(self):
        self.assertEqual(LOWER_LEVEL_POSTSEASON_MODERN_START, "1996-1997")
        historical = self.classify(row("1995-1996"))
        modern = self.classify(row("1996-1997"))
        self.assertEqual(
            historical["era"],
            "HISTORICAL_1995_96_OR_EARLIER",
        )
        self.assertEqual(modern["era"], "MODERN_1996_97_PLUS")

    def test_canonical_and_source_venue_representations_are_recognized(self):
        for key in ("venue_key", "venue_id", "source_venue_name"):
            with self.subTest(field=key):
                value = row("2000-2001", city="Springfield", state="MO")
                value["curated_venue_name"] = ""
                value[key] = "known"
                result = self.classify(value)
                self.assertFalse(result["venue_missing"])
                self.assertFalse(result["material_gap"])
                self.assertFalse(result["nonblocking"])

    def test_canonical_locality_representation_is_recognized(self):
        value = row("2000-2001", venue="Example Arena")
        value["site_city"] = "Springfield"
        value["site_state"] = "MO"
        result = self.classify(value)
        self.assertFalse(result["locality_missing"])
        self.assertFalse(result["material_gap"])
        self.assertFalse(result["nonblocking"])


if __name__ == "__main__":
    unittest.main()
