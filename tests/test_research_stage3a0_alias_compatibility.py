import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "tools" / "research_stage3a0.py"


def csv_text(rows):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


class Stage3A0Stage2AliasCompatibilityTest(unittest.TestCase):
    def test_structured_stage2_ledger_accepts_durable_alias_fields(self):
        rows = [
            {
                "research_game_id": "ALIAS-001",
                "season": "2024-25",
                "canonical_opponent_key": "duke",
                "curated_game_type": "REGULAR_SEASON",
                "site_type": "HOME",
            },
            {
                "research_game_id": "ALIAS-002",
                "season": "2024-25",
                "canonical_opponent_key": "north-carolina",
                "curated_game_type": "NCAA",
                "site_type": "NEUTRAL",
            },
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            checkpoint = root / "stage2-complete.zip"
            output = root / "stage3a0"

            with zipfile.ZipFile(checkpoint, "w") as archive:
                archive.writestr(
                    "nested/structured-stage2-ledger.csv",
                    csv_text(rows),
                )
                archive.writestr("manifest.json", "{}")

            process = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "alias-fixture",
                    str(checkpoint),
                    "--output-dir",
                    str(output),
                    "--main-sha",
                    "PINNED",
                ],
                text=True,
                capture_output=True,
            )

            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            status = json.loads((output / "stage3a0-status.json").read_text())
            self.assertEqual(status["status"], "COMPLETE")
            self.assertEqual(status["entry_mode"], "checkpoint_zip")
            self.assertEqual(
                status["input_checkpoint_member"],
                "nested/structured-stage2-ledger.csv",
            )
            self.assertEqual(
                status["partition"],
                {
                    "postseason": 1,
                    "regular_season": 1,
                    "unclassified": 0,
                },
            )

            with (output / "stage3a0-input-ledger.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                projected = list(csv.DictReader(handle))

            self.assertEqual(
                [row["canonical_opponent_key"] for row in projected],
                ["duke", "north-carolina"],
            )
            self.assertEqual(
                [row["curated_game_type"] for row in projected],
                ["REGULAR_SEASON", "NCAA"],
            )


if __name__ == "__main__":
    unittest.main()
