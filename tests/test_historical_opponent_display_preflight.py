import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import build_site_data


def write_opponents(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["canonical_opponent_key", "canonical_opponent_name"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


class HistoricalOpponentDisplayPreflightTests(unittest.TestCase):
    def test_true_historical_collision_is_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_opponents(
                repo / "schools" / "alpha" / "opponents.csv",
                [
                    {
                        "canonical_opponent_key": "beloit",
                        "canonical_opponent_name": "Beloit",
                    }
                ],
            )
            write_opponents(
                repo / "schools" / "beta" / "opponents.csv",
                [
                    {
                        "canonical_opponent_key": "beloit",
                        "canonical_opponent_name": "Beloit College",
                    }
                ],
            )

            self.assertEqual(
                build_site_data.historical_opponent_display_conflicts(repo, {}),
                {"beloit": ["Beloit", "Beloit College"]},
            )

    def test_punctuation_only_variants_are_not_conflicts(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_opponents(
                repo / "schools" / "alpha" / "opponents.csv",
                [
                    {
                        "canonical_opponent_key": "st-johns-historical",
                        "canonical_opponent_name": "St. Johns",
                    },
                    {
                        "canonical_opponent_key": "st-johns-historical",
                        "canonical_opponent_name": "St Johns",
                    },
                ],
            )

            self.assertEqual(
                build_site_data.historical_opponent_display_conflicts(repo, {}),
                {},
            )

    def test_program_registry_remains_display_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_opponents(
                repo / "schools" / "alpha" / "opponents.csv",
                [
                    {
                        "canonical_opponent_key": "registered",
                        "canonical_opponent_name": "Old Registered Label",
                    }
                ],
            )
            programs = {
                "registered": {
                    "program_name": "Registered Program",
                }
            }

            self.assertEqual(
                build_site_data.historical_opponent_display_conflicts(
                    repo,
                    programs,
                ),
                {},
            )
            self.assertEqual(
                build_site_data.load_opponent_names(repo, programs)["registered"],
                "Registered Program",
            )


if __name__ == "__main__":
    unittest.main()
