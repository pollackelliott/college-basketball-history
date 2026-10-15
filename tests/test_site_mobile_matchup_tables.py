"""Regression contract for responsive matchup summary tables (Issue #296)."""

import re
import unittest
from pathlib import Path


SITE = (Path(__file__).resolve().parents[1] / "site" / "index.html").read_text(
    encoding="utf-8"
)


def mini_panel_renderer():
    return SITE.split("function miniPanel(title, rows, teamA) {", 1)[1].split(
        "\nfunction matchupTeamName(", 1
    )[0]


class MobileMatchupTableTests(unittest.TestCase):
    def test_shared_renderer_preserves_labels_and_omits_visual_group_header(self):
        renderer = mini_panel_renderer()
        self.assertIn('<table class="mini-table">', renderer)
        self.assertIn("<td>${esc(row.label)}</td>", renderer)
        self.assertIn(
            '<th scope="col"><span class="sr-only">Category</span></th>',
            renderer,
        )
        self.assertNotIn("<th>Group</th>", renderer)
        for title in ("Record by Site", "Record by Decade", "Most-Used Venues"):
            with self.subTest(title=title):
                self.assertIn(f'miniPanel("{title}",', SITE)

    def test_all_viewports_wrap_label_column_and_keep_numeric_columns(self):
        css = SITE.split(
            "/* Keep full matchup summary labels readable inside each desktop or mobile panel. */",
            1,
        )[1].split("@media(max-width:720px){", 1)[0]
        self.assertIn(".subgrid .mini-table{table-layout:fixed}", css)
        self.assertIn(
            ".subgrid .mini-table th:first-child,.subgrid .mini-table td:first-child{",
            css,
        )
        self.assertIn("width:50%;white-space:normal;overflow-wrap:anywhere", css)
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
        proportions = [int(value) for value in re.findall(r"width:(\d+)%", css)]
        self.assertEqual(proportions, [50, 36, 14])
        self.assertEqual(sum(proportions), 100)

    def test_mobile_only_centers_labels_and_compacts_padding(self):
        css = SITE.split(
            "/* Keep full matchup summary labels readable inside each desktop or mobile panel. */",
            1,
        )[1].split("@media(max-width:720px){", 1)[1].split("\n}", 1)[0]
        self.assertIn(
            ".subgrid .mini-table th,.subgrid .mini-table td{padding:8px 5px}",
            css,
        )
        self.assertIn(
            ".subgrid .mini-table th:first-child,"
            ".subgrid .mini-table td:first-child{text-align:center}",
            css,
        )

    def test_game_history_layouts_remain_independent(self):
        self.assertIn(
            ".subgrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr))",
            SITE,
        )
        self.assertIn(".matchup-history-table{min-width:790px}", SITE)
        self.assertIn(".desktop-history{display:block}", SITE)
        self.assertIn(".mobile-history{display:none}", SITE)


if __name__ == "__main__":
    unittest.main()
