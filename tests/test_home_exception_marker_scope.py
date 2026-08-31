import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from implementation_site_gate import implementation_site_report  # noqa: E402


SOURCE_FIELDS = [
    "source_game_id",
    "source_program_key",
    "season_label",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "site_research_status",
    "site_research_basis",
]
CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "team_a_key",
    "team_b_key",
    "site_type",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "game_type",
    "notes",
]
ASSERTION_FIELDS = [
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
]
DISCREPANCY_FIELDS = [
    "canonical_game_id",
    "field_name",
    "status",
    "resolution_basis",
]


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class HomeExceptionMarkerScopeTests(unittest.TestCase):
    def make_repo(self, root: Path, marker_school: str):
        write_csv(
            root / "schools/beta/source-games.csv",
            SOURCE_FIELDS,
            [
                {
                    "source_game_id": "BRAW-1",
                    "source_program_key": "beta",
                    "season_label": "2025-2026",
                    "normalized_opponent_key": "alpha",
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                    "curated_game_type": "REGULAR_SEASON",
                    "site_research_status": "",
                    "site_research_basis": "",
                }
            ],
        )
        write_csv(
            root / "data/reference/programs.csv",
            ["program_key", "history_start_season"],
            [{"program_key": "beta", "history_start_season": "1900-1901"}],
        )
        write_csv(
            root / "data/canonical/games.csv",
            CANONICAL_FIELDS,
            [
                {
                    "canonical_game_id": "CBBG-1",
                    "season_label": "2025-2026",
                    "team_a_key": "alpha",
                    "team_b_key": "beta",
                    "site_type": "TEAM_A_HOME",
                    "venue_key": "",
                    "venue_id": "",
                    "site_city": "Alpha City",
                    "site_state": "AA",
                    "game_type": "REGULAR_SEASON",
                    "notes": (
                        "[RESEARCHED_UNRESOLVED_HOME_VENUE "
                        f"source={marker_school}/ARAW-1]"
                    ),
                }
            ],
        )
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ASSERTION_FIELDS,
            [
                {
                    "canonical_game_id": "CBBG-1",
                    "source_program_key": "beta",
                    "source_game_id": "BRAW-1",
                    "normalized_opponent_key": "alpha",
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                }
            ],
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            DISCREPANCY_FIELDS,
            [],
        )

    def test_opponent_marker_is_ignored(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, marker_school="alpha")
            report = implementation_site_report(root, "beta")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(
                report["counts"]["invalid_home_venue_exception_marker_rows"], 0
            )

    def test_target_marker_on_away_game_is_still_invalid(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, marker_school="beta")
            report = implementation_site_report(root, "beta")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(
                report["counts"]["invalid_home_venue_exception_marker_rows"], 1
            )


if __name__ == "__main__":
    unittest.main()
