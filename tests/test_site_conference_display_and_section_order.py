"""Presentation-only regression checks for conference labels and team section order."""
import csv
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site" / "index.html").read_text(encoding="utf-8")


def conference_label_overrides():
    match = re.search(
        r"const CONFERENCE_DISPLAY_ABBREVIATIONS = Object\.freeze\(\{(.*?)\}\);",
        SITE, re.DOTALL,
    )
    if not match:
        raise AssertionError("Missing website-only conference display override map")
    return dict(re.findall(r'"([^"]+)": "([^"]+)"', match.group(1)))


class SitePresentationTests(unittest.TestCase):
    def test_historical_conference_abbreviations_are_explicitly_keyed(self):
        expected = {
            "siaa": "SIAA",
            "eastern-intercollegiate-conference": "EIC",
            "eastern-collegiate-basketball-league": "ECBL",
            "aawu": "AAWU",
            "kiac": "KIAC",
            "midwestern-city": "MCC",
            "midwestern-collegiate": "MCC",
        }
        self.assertEqual(conference_label_overrides(), expected)
        with (ROOT / "data" / "reference" / "conferences.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            registry = {row["conference_key"]: row for row in csv.DictReader(handle)}
        for key, abbreviation in expected.items():
            with self.subTest(conference=key):
                self.assertIn(key, registry)
                self.assertEqual(registry[key]["tournament_label"], abbreviation)
        # Historical conference identity and full-name provenance remain in data.
        self.assertEqual(
            registry["siaa"]["conference_name"],
            "Southern Intercollegiate Athletic Association",
        )

    def test_display_override_is_used_across_web_sections(self):
        self.assertIn(
            "return displayConferenceName(conference?.conference_key, conference?.conference_name);",
            SITE,
        )
        for part in (
            "function conferenceName(conference)",
            "function fullConferenceTournamentLabel(game, teamKey)",
            "function mobileConferenceTournamentLabel(game, teamKey)",
            "function conferenceTimelineDisplayName(key, membership)",
        ):
            self.assertIn(part, SITE)
        full = SITE.split("function fullConferenceTournamentLabel(", 1)[1].split(
            "\nfunction ", 1
        )[0]
        mobile = SITE.split("function mobileConferenceTournamentLabel(", 1)[1].split(
            "\nfunction ", 1
        )[0]
        timeline = SITE.split("function conferenceTimelineDisplayName(", 1)[1].split(
            "\nfunction ", 1
        )[0]
        for block in (full, mobile, timeline):
            self.assertIn("displayConferenceName(", block)

    def test_opponent_record_appears_before_complete_game_history(self):
        team = SITE.split("function teamView(key) {", 1)[1].split(
            "\nfunction toggleTeamFilters(", 1
        )[0]
        self.assertEqual(team.count('<div class="panel opponent-breakdown">'), 1)
        self.assertEqual(team.count('<div class="panel history-panel">'), 1)
        self.assertLess(
            team.index('<div class="panel opponent-breakdown">'),
            team.index('<div class="panel history-panel">'),
        )
        self.assertLess(
            team.index('id="opponentBreakdownBody"'),
            team.index('id="teamGamesTable"'),
        )
        self.assertIn("conferenceHistoryMarkup(key)", team)


if __name__ == "__main__":
    unittest.main()
