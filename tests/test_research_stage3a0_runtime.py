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


def legacy_rows():
    return [
        {
            "research_game_id": "CREI-S1-00001",
            "season": "1911-1912",
            "game_date": "1912-01-10",
            "source_opponent_field": "Omaha YMCA",
            "source_site_token": "@",
            "source_opponent_label": "Omaha YMCA",
            "game_type": "REGULAR_SEASON",
        },
        {
            "research_game_id": "CREI-S1-00002",
            "season": "1911-1912",
            "game_date": "1912-02-10",
            "source_opponent_field": "Drake",
            "source_site_token": "N",
            "source_opponent_label": "Drake",
            "game_type": "REGULAR_SEASON",
        },
    ]


def census_rows(first_count="1"):
    return [
        {
            "source_opponent_label": "Omaha YMCA",
            "game_count": first_count,
            "proposed_program_key": "omaha-ymca",
        },
        {
            "source_opponent_label": "Drake",
            "game_count": "1",
            "proposed_program_key": "drake",
        },
    ]


class Stage3A0RuntimeTests(unittest.TestCase):
    def run_checkpoint(self, checkpoint):
        out = checkpoint.parent / "out"
        proc = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "creighton",
                str(checkpoint),
                "--output-dir",
                str(out),
                "--main-sha",
                "PINNED",
            ],
            text=True,
            capture_output=True,
        )
        status_path = out / "stage3a0-status.json"
        status = json.loads(status_path.read_text()) if status_path.exists() else None
        return proc, status, out

    def test_creighton_shaped_legacy_checkpoint_completes(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checkpoint = root / "stage2.zip"
            with zipfile.ZipFile(checkpoint, "w") as archive:
                archive.writestr(
                    "creighton_stage1_working_ledger.csv", csv_text(legacy_rows())
                )
                archive.writestr(
                    "creighton_stage2_opponent_census.csv", csv_text(census_rows())
                )
            proc, status, out = self.run_checkpoint(checkpoint)
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            self.assertEqual(status["status"], "COMPLETE")
            self.assertEqual(status["entry_mode"], "legacy_stage2_materialized")
            self.assertEqual(status["legacy_opponent_mapping_coverage"], "COMPLETE")
            self.assertEqual(status["site_type_defaulted_to_unknown_count"], 2)
            with (out / "stage3a0-input-ledger.csv").open(
                newline="", encoding="utf-8"
            ) as handle:
                materialized = list(csv.DictReader(handle))
            self.assertEqual(
                [row["opponent_key"] for row in materialized],
                ["omaha-ymca", "drake"],
            )
            self.assertEqual(
                [row["site_type"] for row in materialized],
                ["UNKNOWN", "UNKNOWN"],
            )
            self.assertEqual(
                [row["source_site_token"] for row in materialized],
                ["@", "N"],
            )

    def test_current_checkpoint_accepts_ncaa_tournament_as_postseason(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checkpoint = root / "stage2-current.zip"
            rows = [
                {
                    "research_game_id": "FSU-STG1-00001",
                    "season": "2025-2026",
                    "game_date": "2025-11-10",
                    "opponent_key": "florida",
                    "site_type": "UNKNOWN",
                    "game_type": "REGULAR_SEASON",
                },
                {
                    "research_game_id": "FSU-STG1-00002",
                    "season": "2025-2026",
                    "game_date": "2026-03-20",
                    "opponent_key": "duke",
                    "site_type": "UNKNOWN",
                    "game_type": "NCAA_TOURNAMENT",
                },
            ]
            with zipfile.ZipFile(checkpoint, "w") as archive:
                archive.writestr("structured-stage2-ledger.csv", csv_text(rows))

            proc, status, out = self.run_checkpoint(checkpoint)
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            self.assertEqual(status["status"], "COMPLETE")
            self.assertEqual(
                status["partition"],
                {
                    "postseason": 1,
                    "regular_season": 1,
                    "unclassified": 0,
                },
            )
            handoff = json.loads((out / "stage3b-postseason-handoff.json").read_text())
            self.assertEqual(
                [row["research_game_id"] for row in handoff],
                ["FSU-STG1-00002"],
            )
            self.assertEqual(handoff[0]["game_type"], "NCAA_TOURNAMENT")

    def test_bad_mapping_count_fails_closed_with_status(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checkpoint = root / "stage2.zip"
            with zipfile.ZipFile(checkpoint, "w") as archive:
                archive.writestr(
                    "creighton_stage1_working_ledger.csv", csv_text(legacy_rows())
                )
                archive.writestr(
                    "creighton_stage2_opponent_census.csv",
                    csv_text(census_rows(first_count="2")),
                )
            proc, status, _ = self.run_checkpoint(checkpoint)
            self.assertEqual(proc.returncode, 2)
            self.assertEqual(status["status"], "STAGE_3A0_ENTRY_NOT_READY")
            self.assertTrue(
                status["entry_error"].startswith(
                    "NO_COMPLETE_LEGACY_STAGE2_OPPONENT_MAPPING"
                )
            )


if __name__ == "__main__":
    unittest.main()
