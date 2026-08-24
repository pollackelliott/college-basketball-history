import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_hardening import research_portfolio_report  # noqa: E402


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ResearchRoundPolicyTests(unittest.TestCase):
    def make_package(self, root: Path, *, round_name: str, raw_text: str):
        write_csv(
            root / "source-games.csv",
            [
                "source_game_id",
                "source_program_key",
                "season_label",
                "game_date",
                "source_opponent_label",
                "normalized_opponent_key",
                "team_score",
                "opponent_score",
                "played_result",
                "curated_site_type",
                "curated_venue_name",
                "city",
                "state",
                "event_or_tournament",
                "source_round",
                "curated_game_type",
                "curated_postseason_round",
                "raw_text",
                "notes",
            ],
            [
                {
                    "source_game_id": "TESTRAW-00001",
                    "source_program_key": "test",
                    "season_label": "1960-1961",
                    "game_date": "1961-03-25",
                    "source_opponent_label": "Example",
                    "normalized_opponent_key": "example",
                    "team_score": "70",
                    "opponent_score": "60",
                    "played_result": "W",
                    "curated_site_type": "NEUTRAL",
                    "curated_venue_name": "Example Arena",
                    "city": "Example City",
                    "state": "EX",
                    "event_or_tournament": "NCAA Tournament",
                    "source_round": "",
                    "curated_game_type": "NCAA_TOURNAMENT",
                    "curated_postseason_round": round_name,
                    "raw_text": raw_text,
                    "notes": "",
                }
            ],
        )
        write_csv(
            root / "opponents.csv",
            ["source_program_key", "canonical_opponent_key"],
            [{"source_program_key": "test", "canonical_opponent_key": "example"}],
        )
        write_csv(
            root / "venues.csv",
            [
                "source_program_key",
                "venue_key",
                "venue_id",
                "canonical_name",
                "aliases",
                "city",
                "state",
            ],
            [
                {
                    "source_program_key": "test",
                    "venue_key": "example-arena",
                    "venue_id": "VEN-999999",
                    "canonical_name": "Example Arena",
                    "aliases": "",
                    "city": "Example City",
                    "state": "EX",
                }
            ],
        )
        write_csv(
            root / "conferences.csv",
            ["source_program_key"],
            [{"source_program_key": "test"}],
        )
        (root / "notes.md").write_text("# notes\n", encoding="utf-8")
        (root / "source-notes.md").write_text("# source notes\n", encoding="utf-8")

    def test_blank_round_is_allowed_for_explicit_third_place_game(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_package(
                root,
                round_name="",
                raw_text="NCAA Tournament third-place game",
            )
            report = research_portfolio_report(root, school_key="test")
            self.assertEqual(report["status"], "PASS", report["errors"])

    def test_blank_round_blocks_ordinary_ncaa_game(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_package(
                root,
                round_name="",
                raw_text="NCAA Tournament game",
            )
            report = research_portfolio_report(root, school_key="test")
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(
                any(
                    "requires a curated postseason round" in error
                    for error in report["errors"]
                )
            )


if __name__ == "__main__":
    unittest.main()
