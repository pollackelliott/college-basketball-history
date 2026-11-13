"""Regression: head-to-head series honor published history, not top-level scope.

The generated per-team game list is already publication-scoped. The browser
must not apply a second top-level-only filter to the matchup page.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
sys.path.insert(0, str(ROOT / "tools"))
from program_history import (  # noqa: E402
    publication_history_games,
    top_level_canonical_games,
)


def series_source() -> str:
    start = "function seriesGamesFor(teamKey, opponentKey) {"
    return start + SITE.split(start, 1)[1].split("\nfunction ", 1)[0]


def synthetic_games() -> list[dict[str, str]]:
    # Exact shape of the George Mason/JMU discrepancy: 16 pre-D1 and 86 D1.
    early = [
        {"canonical_game_id": f"EARLY-{index:03d}",
         "season_label": "1967-1968",
         "team_a_key": "expanded", "team_b_key": "legacy"}
        for index in range(16)
    ]
    later = [
        {"canonical_game_id": f"LATER-{index:03d}",
         "season_label": "1978-1979",
         "team_a_key": "expanded", "team_b_key": "legacy"}
        for index in range(86)
    ]
    return early + later


def published_game_rows():
    rows = synthetic_games()
    expanded = {
        "history_coverage_status": "COMPLETE_INSTITUTIONAL",
        "program_inception_season": "1966-1967",
        "history_start_season": "1978-1979",
        "history_scope_intervals": "",
    }
    legacy = {
        "history_coverage_status": "LEGACY_TOP_LEVEL_ONLY",
        "history_start_season": "1978-1979",
        "history_scope_intervals": "",
    }
    return (
        publication_history_games(rows, "expanded", expanded),
        publication_history_games(rows, "legacy", legacy),
        top_level_canonical_games(rows, "expanded", "1978-1979"),
    )


def browser_perspective(rows, *, viewer: str, opponent: str):
    games = [
        {
            "canonicalGameId": row["canonical_game_id"],
            "opponentKey": opponent,
            "season": row["season_label"],
            "date": "",
            "datePrecision": "",
            "teamScore": 71,
            "oppScore": 70,
            "result": "W",
            "scoreKnown": True,
            "site": "NEUTRAL",
        }
        for row in rows
    ]
    # The unrelated opponent must not leak into the matchup.
    games.append({
        "canonicalGameId": "UNRELATED",
        "opponentKey": "unrelated",
        "season": "1978-1979",
        "date": "",
        "datePrecision": "",
        "teamScore": 60,
        "oppScore": 65,
        "result": "L",
        "scoreKnown": True,
        "site": "NEUTRAL",
    })
    return {
        "teams": {
            viewer: {"name": viewer, "historyStartSeason": "1978-1979",
                     "publishedHistoryStartSeason": (
                         "1966-1967" if viewer == "expanded" else "1978-1979"
                     )},
        },
        "games": {viewer: games},
    }


class MatchupPublicationHistoryTests(unittest.TestCase):
    def test_series_uses_only_generated_published_team_games(self):
        block = series_source()
        self.assertIn("DB.games[teamKey]", block)
        self.assertIn("game.opponentKey === opponentKey", block)
        self.assertNotIn("gameInProgramScope", block)
        self.assertNotIn("historyStartSeason", block)
        self.assertNotIn("publishedHistoryStartSeason", block)
        # No remaining second-stage top-level filter elsewhere in the page.
        self.assertNotIn("function gameInProgramScope(", SITE)

    def test_site_generated_publication_and_top_level_scopes_remain_distinct(self):
        complete, legacy, top_level = published_game_rows()
        self.assertEqual(len(complete), 102)
        self.assertEqual(len(legacy), 86)
        self.assertEqual(len(top_level), 86)
        self.assertEqual(
            {row["canonical_game_id"] for row in complete}
            - {row["canonical_game_id"] for row in top_level},
            {f"EARLY-{index:03d}" for index in range(16)},
        )

    @unittest.skipUnless(shutil.which("node"), "Node.js unavailable for browser function execution")
    def test_actual_browser_function_respects_both_publication_modes(self):
        complete, legacy, _ = published_game_rows()
        browser_js = (
            "const DB = JSON.parse(process.argv[1]);\n"
            "function opponentProfile(_key, opponentKey) {return {name: opponentKey};}\n"
            "function oppositeResult(result) {return result === 'W' ? 'L' : result === 'L' ? 'W' : result;}\n"
            + series_source() + "\n"
            "process.stdout.write(JSON.stringify(seriesGamesFor(process.argv[2], process.argv[3])));\n"
        )
        for viewer, opponent, rows, expected in (
            ("expanded", "legacy", complete, 102),
            ("legacy", "expanded", legacy, 86),
        ):
            with self.subTest(viewer=viewer):
                fixture = browser_perspective(rows, viewer=viewer, opponent=opponent)
                result = subprocess.run(
                    ["node", "-e", browser_js, json.dumps(fixture), viewer, opponent],
                    capture_output=True, text=True, check=True, timeout=15,
                )
                selected = json.loads(result.stdout)
                self.assertEqual(len(selected), expected)
                self.assertEqual(
                    len({row["canonicalGameId"] for row in selected}), expected
                )
                self.assertNotIn(
                    "UNRELATED", {row["canonicalGameId"] for row in selected}
                )

    def test_matchup_routes_consume_the_same_series_selector(self):
        self.assertIn(
            "if (seriesGamesFor(teamA, teamB).length) navigateRoute(", SITE
        )
        self.assertIn(
            "const allGames = seriesGamesFor(teamA, teamB);", SITE
        )
        self.assertIn(
            "const games = seriesGamesFor(teamA, teamB);", SITE
        )


if __name__ == "__main__":
    unittest.main()
