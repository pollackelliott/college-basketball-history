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


class Stage3A3Tier1DurableSchemaCompatibilityTest(unittest.TestCase):
    def _run_case(self, ledger_row, evidence_rows):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ledger = root / "ledger.csv"
            output = root / "out"

            write_csv(ledger, [ledger_row])
            write_csv(root / "schools" / "virginia" / "source-games.csv", evidence_rows)
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
                    "clemson",
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
            status = json.loads((output / "stage3a3-tier1-status.json").read_text())
            accepted_path = output / "accepted-project-evidence.json"
            unresolved_path = output / "tier1-unresolved.json"
            accepted = json.loads(accepted_path.read_text()) if accepted_path.exists() else []
            unresolved = json.loads(unresolved_path.read_text()) if unresolved_path.exists() else []
            return process, status, accepted, unresolved

    @staticmethod
    def _ledger_row(
        research_game_id,
        *,
        season_label="2024-25",
        source_date_literal="",
        game_date="",
    ):
        return {
            "research_game_id": research_game_id,
            "season_label": season_label,
            "game_date": game_date,
            "source_date_literal": source_date_literal,
            "stage2_opponent_key": "virginia",
            "site_type": "NEUTRAL",
            "game_type": "REGULAR_SEASON",
        }

    @staticmethod
    def _evidence(source_game_id, game_date):
        return [
            {
                "source_game_id": source_game_id,
                "source_program_key": "virginia",
                "game_date": game_date,
                "normalized_opponent_key": "clemson",
                "curated_venue_name": "Arena A",
                "city": "Atlanta",
                "state": "GA",
            }
        ]

    def test_stage2_opponent_key_and_fall_source_date_match_reciprocal_evidence(self):
        process, status, accepted, unresolved = self._run_case(
            self._ledger_row(
                "C-DURABLE-FALL",
                source_date_literal="11/20",
            ),
            self._evidence("V-FALL", "2024-11-20"),
        )

        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(status["status"], "COMPLETE")
        self.assertEqual(status["accepted_count"], 1)
        self.assertEqual(unresolved, [])
        self.assertEqual(accepted[0]["game_date"], "2024-11-20")
        self.assertEqual(accepted[0]["opponent_key"], "virginia")

    def test_second_half_source_date_projects_to_season_end_year(self):
        process, status, accepted, _unresolved = self._run_case(
            self._ledger_row(
                "C-DURABLE-JAN",
                source_date_literal="1/15",
            ),
            self._evidence("V-JAN", "2025-01-15"),
        )

        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(status["accepted_count"], 1)
        self.assertEqual(accepted[0]["game_date"], "2025-01-15")

    def test_two_digit_season_rollover_projects_into_next_century(self):
        process, status, accepted, _unresolved = self._run_case(
            self._ledger_row(
                "C-DURABLE-2000",
                season_label="1999-00",
                source_date_literal="1/15",
            ),
            self._evidence("V-2000", "2000-01-15"),
        )

        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(status["accepted_count"], 1)
        self.assertEqual(accepted[0]["game_date"], "2000-01-15")

    def test_explicit_game_date_precedes_source_date_literal(self):
        process, status, accepted, _unresolved = self._run_case(
            self._ledger_row(
                "C-DURABLE-EXPLICIT",
                source_date_literal="1/15",
                game_date="2024-11-20",
            ),
            self._evidence("V-EXPLICIT", "2024-11-20"),
        )

        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(status["accepted_count"], 1)
        self.assertEqual(accepted[0]["game_date"], "2024-11-20")

    def test_blank_source_date_remains_no_exact_date_residual(self):
        process, status, accepted, unresolved = self._run_case(
            self._ledger_row("C-DURABLE-BLANK"),
            self._evidence("V-BLANK", "2024-11-20"),
        )

        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertEqual(status["status"], "COMPLETE")
        self.assertEqual(status["accepted_count"], 0)
        self.assertEqual(status["unresolved_count"], 1)
        self.assertEqual(accepted, [])
        self.assertEqual(
            unresolved,
            [
                {
                    "research_game_id": "C-DURABLE-BLANK",
                    "game_date": "",
                    "opponent_key": "virginia",
                    "reason": "NO_EXACT_DATE_FOR_TIER1_MATCH",
                }
            ],
        )

    def test_malformed_impossible_and_nonconsecutive_source_dates_remain_unresolved(self):
        cases = [
            ("C-DURABLE-BAD-TEXT", "2024-25", "Nov 20"),
            ("C-DURABLE-BAD-DATE", "2024-25", "2/30"),
            ("C-DURABLE-BAD-SEASON", "2024-26", "11/20"),
        ]
        for research_game_id, season_label, source_date_literal in cases:
            with self.subTest(
                research_game_id=research_game_id,
                season_label=season_label,
                source_date_literal=source_date_literal,
            ):
                process, status, accepted, unresolved = self._run_case(
                    self._ledger_row(
                        research_game_id,
                        season_label=season_label,
                        source_date_literal=source_date_literal,
                    ),
                    self._evidence("V-BAD", "2024-11-20"),
                )

                self.assertEqual(
                    process.returncode,
                    0,
                    process.stdout + process.stderr,
                )
                self.assertEqual(status["status"], "COMPLETE")
                self.assertEqual(status["accepted_count"], 0)
                self.assertEqual(status["unresolved_count"], 1)
                self.assertEqual(accepted, [])
                self.assertEqual(unresolved[0]["game_date"], "")
                self.assertEqual(
                    unresolved[0]["reason"],
                    "NO_EXACT_DATE_FOR_TIER1_MATCH",
                )


if __name__ == "__main__":
    unittest.main()
