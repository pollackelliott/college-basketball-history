"""Tests for owner-curated visual labels and responsive header wiring.

This reference is website presentation, not a canonical identity mapping.
"""
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_site_data import public_program_display_labels, read_csv  # noqa: E402

SITE = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
REFERENCE = ROOT / "data" / "reference" / "program-display-labels.csv"


class ProgramDisplayLabelTests(unittest.TestCase):
    def test_every_registered_program_has_one_visual_label(self):
        programs = read_csv(ROOT / "data" / "reference" / "programs.csv")
        rows = read_csv(REFERENCE)
        self.assertEqual(len(programs), 365)
        self.assertEqual(len(rows), len(programs))
        rendered = public_program_display_labels(programs, rows)
        self.assertEqual(set(rendered["programs"]), {p["program_key"] for p in programs})
        self.assertEqual(rendered["programs"]["miami"],
                         {"header_short": "MIAMI", "badge_initialism": "M"})
        self.assertEqual(rendered["programs"]["north-carolina"],
                         {"header_short": "UNC", "badge_initialism": "UNC"})
        self.assertEqual(rendered["programs"]["new-orleans"],
                         {"header_short": "UNO", "badge_initialism": "LSUN"})
        self.assertEqual(rendered["programs"]["west-florida"],
                         {"header_short": "WFLA", "badge_initialism": "WF"})
        self.assertNotIn("saint-francis", rendered["programs"])

    def test_published_json_matches_reference_exactly(self):
        payload = public_program_display_labels(
            read_csv(ROOT / "data" / "reference" / "programs.csv"), read_csv(REFERENCE)
        )
        actual = json.loads(
            (ROOT / "site" / "data" / "program-display-labels.json").read_text(encoding="utf-8")
        )
        self.assertEqual(actual, payload)
        manifest = json.loads(
            (ROOT / "site" / "data" / "manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            manifest["files"]["display_labels"], "program-display-labels.json"
        )

    def test_bad_or_incomplete_reference_is_rejected(self):
        rows = [
            {"program_key": "miami", "header_short": "MIAMI", "badge_initialism": "M"}
        ]
        programs = [{"program_key": "miami"}, {"program_key": "north-carolina"}]
        with self.assertRaisesRegex(ValueError, "cover current programs exactly"):
            public_program_display_labels(programs, rows)
        with self.assertRaisesRegex(ValueError, "Missing/duplicate"):
            public_program_display_labels([{"program_key": "miami"}], rows + rows)
        with self.assertRaisesRegex(ValueError, "empty field"):
            public_program_display_labels(
                [{"program_key": "miami"}],
                [{"program_key": "miami", "header_short": "", "badge_initialism": "M"}],
            )

    def test_badges_use_curated_initialism_and_fit_after_render(self):
        self.assertIn('badgeInitialism: DB.displayLabels[program.program_key]', SITE)
        self.assertIn('const initialism = team.badgeInitialism || initials(team.name);', SITE)
        self.assertIn('aria-label="${esc(team.name)}"', SITE)
        self.assertIn('function fitLogoBadgeText()', SITE)
        self.assertIn('fitLogoBadgeText();', SITE)
        self.assertIn('document.fonts?.ready', SITE)

    def test_sticky_navigation_restores_full_name_and_falls_back_on_overflow(self):
        self.assertIn('function fitTeamContextTitle()', SITE)
        self.assertIn('title.dataset.shortName = team.headerShort || team.name;', SITE)
        self.assertIn('if (overflowed() && title.dataset.shortName', SITE)
        self.assertIn('function fitSeriesContextTitle()', SITE)
        self.assertIn('badgeA.dataset.fullName = teamA.name;', SITE)
        self.assertIn('badgeB.dataset.shortName = teamB.headerShort || teamB.name;', SITE)
        self.assertIn('badge.dataset.fullName || badge.textContent', SITE)
        self.assertIn('badge.dataset.shortName || badge.dataset.fullName', SITE)
        # Full team titles and full historical names in games remain unmodified.
        self.assertIn('id="teamPageTitle">${esc(team.name)} ${esc(team.nickname)}', SITE)
        self.assertIn('aria-label="Open ${esc(program.name)} team history"', SITE)


if __name__ == "__main__":
    unittest.main()
