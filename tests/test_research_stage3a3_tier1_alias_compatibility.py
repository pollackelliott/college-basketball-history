import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "tools" / "research_stage3a3_tier1.py"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


class Stage3A3Tier1OpponentAliasCompatibilityTest(unittest.TestCase):
    def test_tier1_accepts_canonical_opponent_key_from_durable_ledger(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ledger = root / "ledger.csv"
            output = root / "out"

            write_csv(
                ledger,
                [
                    {
                        "research_game_id": "VT-ALIAS-001",
                        "season_label": "2024-2025",
                        "game_date": "2024-11-20",
                        "canonical_opponent_key": "virginia",
                        "site_type": "NEUTRAL",
                        "game_type": "REGULAR_SEASON",
                    }
                ],
            )

            write_csv(
                root / "schools" / "virginia" / "source-games.csv",
                [
                    {
                        "source_game_id": "VA-001",
                        "source_program_key": "virginia",
                        "game_date": "2024-11-20",
                        "normalized_opponent_key": "virginia-tech",
                        "curated_venue_name": "Test Arena",
                        "city": "Charlotte",
                        "state": "NC",
                    }
                ],
            )

            write_csv(
                root / "data" / "canonical" / "games.csv",
                [
                    {
                        "canonical_game_id": "OTHER",
                        "game_date": "2000-01-01",
                        "team_a_key": "a",
                        "team_b_key": "b",
                        "venue_name": "",
                        "city": "",
                        "state": "",
                    }
                ],
            )

            process = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "virginia-tech",
                    str(ledger),
                    "--repo-root",
                    str(root),
                    "--output-dir",
                    str(output),
                    "--main-sha",
                    "PINNED",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            status = json.loads((output / "stage3a3-tier1-status.json").read_text())
            self.assertEqual(status["status"], "COMPLETE")
            self.assertEqual(status["neutral_rows"], 1)
            self.assertEqual(status["accepted_count"], 1)
            self.assertEqual(status["accepted_complete_count"], 1)
            self.assertEqual(status["contradiction_count"], 0)
            self.assertEqual(status["unresolved_count"], 0)


if __name__ == "__main__":
    unittest.main()
