"""Regression contract for responsive matchup summary tables (Issue #296)."""

import re
import unittest
from pathlib import Path


SITE = (Path(__file__).resolve().parents[1] / "site" / "index.html").read_text(
    encoding="utf-8"
)


class MobileMatchupTableTests(unittest.TestCase):
    def test_shared_summary_renderer_keeps_full_labels(self):
        self.assertIn('<table class="mini-table">', SITE)
        self.assertIn("<td>${esc(row.label)}</td>", SITE)
        for title in ("Record by Site", "Record by Decade", "Most-Used Venues"):
            with self.subTest(title=title):
                self.assertIn(f'miniPanel("{title}",', SITE)

    def test_only_mobile_matchup_summary_tables_get_fixed_columns(self):
        match = re.search(
            r"@media\(max-width:720px\)\{\s*"
            r"\.subgrid \.mini-table\{table-layout:fixed\}(.*?)\n\}",
            SITE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match, "Missing mobile-only fixed matchup table layout")
        css = match.group(1)
        self.assertIn(
            ".subgrid .mini-table th:first-child,.subgrid .mini-table td:first-child{",
            css,
        )
        self.assertRegex(
            css,
            r"width:50%;text-align:left;white-space:normal;overflow-wrap:anywhere",
        )
        self.assertIn(
            ".subgrid .mini-table th:nth-child(2),"
            ".subgrid .mini-table td:nth-child(2){width:36%}",
            css,
        )
        self.assertIn(
            ".subgrid .mini-table th:last-child,"
            ".subgrid .mini-table td:last-child{width:14%}",
            css,
        )
        percentages = [int(value) for value in re.findall(r"width:(\d+)%", css)]
        self.assertEqual(percentages, [50, 36, 14])
        self.assertEqual(sum(percentages), 100)

    def test_desktop_and_game_history_layouts_remain_separate(self):
        self.assertIn(".subgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))", SITE)
        self.assertIn(".matchup-history-table{min-width:790px}", SITE)
        self.assertIn(".desktop-history{display:block}", SITE)
        self.assertIn(".mobile-history{display:none}", SITE)


if __name__ == "__main__":
    unittest.main()
