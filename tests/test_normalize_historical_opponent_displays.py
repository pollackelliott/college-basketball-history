import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import normalize_historical_opponent_displays as normalizer


OPPONENT_FIELDS = [
    "source_opponent_label",
    "canonical_opponent_key",
    "canonical_opponent_name",
]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_programs(repo: Path, keys: list[str]) -> None:
    write_csv(
        repo / "data/reference/programs.csv",
        ["program_key"],
        [{"program_key": key} for key in keys],
    )


def write_opponents(repo: Path, school: str, rows: list[dict[str, str]]) -> None:
    write_csv(repo / "schools" / school / "opponents.csv", OPPONENT_FIELDS, rows)


class HistoricalOpponentDisplayNormalizerTests(unittest.TestCase):
    def test_normalizes_divergent_target_name_to_existing_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_programs(repo, [])
            write_opponents(
                repo,
                "alpha",
                [{
                    "source_opponent_label": "Beloit College",
                    "canonical_opponent_key": "beloit",
                    "canonical_opponent_name": "Beloit College",
                }],
            )
            write_opponents(
                repo,
                "beta",
                [{
                    "source_opponent_label": "Beloit",
                    "canonical_opponent_key": "beloit",
                    "canonical_opponent_name": "Beloit",
                }],
            )

            plan = normalizer.build_normalization_plan(repo, "alpha")

            self.assertEqual(plan["status"], "PASS")
            self.assertEqual(plan["change_key_count"], 1)
            self.assertEqual(plan["change_row_count"], 1)
            self.assertEqual(
                plan["rows"][0]["canonical_opponent_name"],
                "Beloit",
            )

    def test_punctuation_equivalent_authority_uses_deterministic_preferred_display(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_programs(repo, [])
            write_opponents(
                repo,
                "alpha",
                [{
                    "source_opponent_label": "Hardin-Simmons University",
                    "canonical_opponent_key": "hardin-simmons",
                    "canonical_opponent_name": "Hardin-Simmons University",
                }],
            )
            write_opponents(
                repo,
                "beta",
                [{
                    "source_opponent_label": "Hardin Simmons",
                    "canonical_opponent_key": "hardin-simmons",
                    "canonical_opponent_name": "Hardin Simmons",
                }],
            )
            write_opponents(
                repo,
                "gamma",
                [{
                    "source_opponent_label": "Hardin-Simmons",
                    "canonical_opponent_key": "hardin-simmons",
                    "canonical_opponent_name": "Hardin-Simmons",
                }],
            )

            plan = normalizer.build_normalization_plan(repo, "alpha")

            self.assertEqual(plan["status"], "PASS")
            self.assertEqual(plan["ambiguous_key_count"], 0)
            self.assertEqual(plan["change_key_count"], 1)
            self.assertEqual(
                plan["changes"][0]["authority_names"],
                ["Hardin Simmons", "Hardin-Simmons"],
            )
            self.assertEqual(
                plan["rows"][0]["canonical_opponent_name"],
                "Hardin Simmons",
            )

    def test_multiple_authority_signatures_fail_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_programs(repo, [])
            write_opponents(
                repo,
                "alpha",
                [{
                    "source_opponent_label": "Beloit University",
                    "canonical_opponent_key": "beloit",
                    "canonical_opponent_name": "Beloit University",
                }],
            )
            write_opponents(
                repo,
                "beta",
                [{
                    "source_opponent_label": "Beloit",
                    "canonical_opponent_key": "beloit",
                    "canonical_opponent_name": "Beloit",
                }],
            )
            write_opponents(
                repo,
                "gamma",
                [{
                    "source_opponent_label": "Beloit College",
                    "canonical_opponent_key": "beloit",
                    "canonical_opponent_name": "Beloit College",
                }],
            )

            plan = normalizer.build_normalization_plan(repo, "alpha")

            self.assertEqual(plan["status"], "BLOCKED")
            self.assertEqual(plan["change_key_count"], 0)
            self.assertEqual(plan["ambiguous_key_count"], 1)

    def test_registered_program_key_is_not_rewritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_programs(repo, ["registered"])
            write_opponents(
                repo,
                "alpha",
                [{
                    "source_opponent_label": "Old Registered Label",
                    "canonical_opponent_key": "registered",
                    "canonical_opponent_name": "Old Registered Label",
                }],
            )
            write_opponents(
                repo,
                "beta",
                [{
                    "source_opponent_label": "Registered Program",
                    "canonical_opponent_key": "registered",
                    "canonical_opponent_name": "Registered Program",
                }],
            )

            plan = normalizer.build_normalization_plan(repo, "alpha")

            self.assertEqual(plan["status"], "PASS")
            self.assertEqual(plan["change_key_count"], 0)
            self.assertEqual(plan["change_row_count"], 0)


if __name__ == "__main__":
    unittest.main()
