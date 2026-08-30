import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from published_site_standard import published_site_standard_report  # noqa: E402


PROGRAM_FIELDS = ["program_key", "public_page_enabled"]
GAME_FIELDS = [
    "canonical_game_id",
    "team_a_key",
    "team_b_key",
    "site_type",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
]


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def game(game_id, team_a, team_b, site_type, *, venue="", city="", state=""):
    return {
        "canonical_game_id": game_id,
        "team_a_key": team_a,
        "team_b_key": team_b,
        "site_type": site_type,
        "venue_key": venue,
        "venue_id": "VEN-1" if venue else "",
        "site_city": city,
        "site_state": state,
    }


class PublishedSiteStandardTests(unittest.TestCase):
    def make_repo(self, root: Path, games):
        write_csv(
            root / "data/reference/programs.csv",
            PROGRAM_FIELDS,
            [
                {"program_key": "alpha", "public_page_enabled": "Yes"},
                {"program_key": "beta", "public_page_enabled": "Yes"},
                {"program_key": "gamma", "public_page_enabled": "No"},
            ],
        )
        write_csv(root / "data/canonical/games.csv", GAME_FIELDS, games)

    def test_published_home_gap_is_hard_blocker(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                [game("CBBG-1", "alpha", "gamma", "TEAM_A_HOME")],
            )
            report = published_site_standard_report(root)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["hard_published_home_blocker_games"], 1)
            self.assertEqual(report["counts"]["published_home_missing_venue"], 1)
            self.assertEqual(report["counts"]["published_home_missing_location"], 1)

    def test_away_at_unpublished_gap_is_expected_debt_not_blocker(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                [game("CBBG-2", "alpha", "gamma", "TEAM_B_HOME")],
            )
            report = published_site_standard_report(root)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["hard_published_home_blocker_games"], 0)
            self.assertEqual(report["counts"]["expected_away_at_unpublished_debt_games"], 1)
            self.assertEqual(report["counts"]["published_away_at_unpublished_missing_venue"], 1)
            self.assertEqual(report["counts"]["published_away_at_unpublished_missing_location"], 1)

    def test_away_at_published_home_gap_is_hard_home_blocker(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                [game("CBBG-3", "alpha", "beta", "TEAM_B_HOME")],
            )
            report = published_site_standard_report(root)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["hard_published_home_blocker_games"], 1)
            self.assertEqual(report["counts"]["published_home_missing_venue"], 1)
            self.assertEqual(report["counts"]["published_home_missing_location"], 1)

    def test_neutral_missing_location_is_reported_and_heightened_when_both_published(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                [
                    game("CBBG-4", "alpha", "gamma", "NEUTRAL", venue="arena"),
                    game("CBBG-5", "alpha", "beta", "NEUTRAL", venue="arena"),
                ],
            )
            report = published_site_standard_report(root)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["published_neutral_missing_location"], 2)
            self.assertEqual(
                report["counts"]["published_vs_published_neutral_missing_location"], 1
            )
            self.assertEqual(
                report["counts"]["heightened_published_vs_published_neutral_games"], 1
            )

    def test_unknown_site_is_heightened_when_both_participants_published(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                [
                    game("CBBG-6", "alpha", "gamma", "UNKNOWN"),
                    game("CBBG-7", "alpha", "beta", "UNKNOWN"),
                ],
            )
            report = published_site_standard_report(root)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["published_unknown_site_type"], 2)
            self.assertEqual(report["counts"]["published_vs_published_unknown_site_type"], 1)
            self.assertEqual(
                report["counts"]["heightened_published_vs_published_unknown_site_games"], 1
            )

    def test_complete_published_home_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                [
                    game(
                        "CBBG-8",
                        "alpha",
                        "beta",
                        "TEAM_A_HOME",
                        venue="alpha-arena",
                        city="Alpha City",
                        state="AA",
                    )
                ],
            )
            report = published_site_standard_report(root)
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["hard_published_home_blocker_games"], 0)


if __name__ == "__main__":
    unittest.main()
