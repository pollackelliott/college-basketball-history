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


    def test_sync_uses_reconciled_historical_table_and_preserves_source_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_programs(repo, ["florida"])
            write_opponents(repo, "alpha", [
                {"source_opponent_label": "Western Maryland",
                 "canonical_opponent_key": "mcdaniel", "canonical_opponent_name": "McDaniel"},
                {"source_opponent_label": "Florida",
                 "canonical_opponent_key": "florida", "canonical_opponent_name": "Florida"},
            ])
            write_opponents(repo, "beta", [
                {"source_opponent_label": "McDaniel",
                 "canonical_opponent_key": "mcdaniel", "canonical_opponent_name": "McDaniel"},
            ])
            source = repo / "schools" / "alpha" / "source-games.csv"
            fields = ["source_game_id", "normalized_opponent_key", "normalized_opponent_name",
                      "source_opponent_label", "raw_text", "game_date", "team_score", "opponent_score"]
            write_csv(source, fields, [
                {"source_game_id": "A-1", "normalized_opponent_key": "mcdaniel",
                 "normalized_opponent_name": "McDaniel College (formerly Western Maryland College)",
                 "source_opponent_label": "Western Maryland", "raw_text": "at Western Maryland",
                 "game_date": "1938-02-03", "team_score": "38", "opponent_score": "29"},
                {"source_game_id": "A-2", "normalized_opponent_key": "florida",
                 "normalized_opponent_name": "Historical Florida label",
                 "source_opponent_label": "Gators", "raw_text": "Florida",
                 "game_date": "1938-02-04", "team_score": "30", "opponent_score": "40"},
            ])
            before = list(csv.DictReader(source.open(encoding="utf-8", newline="")))
            opponent_plan = normalizer.build_normalization_plan(repo, "alpha")
            self.assertEqual(opponent_plan["change_row_count"], 0)
            plan = normalizer.build_source_display_plan(repo, "alpha", opponent_plan)
            self.assertEqual((plan["change_row_count"], plan["change_key_count"]), (1, 1))
            normalizer.write_csv_preserving(
                plan["path"], plan["fields"], plan["rows"], plan["encoding"], plan["line_ending"],
            )
            after = list(csv.DictReader(source.open(encoding="utf-8", newline="")))
            self.assertEqual(after[0]["normalized_opponent_name"], "McDaniel")
            self.assertEqual(after[1], before[1])  # current-D1 identity not touched
            for field in fields:
                if field != "normalized_opponent_name":
                    self.assertEqual(after[0][field], before[0][field])
            again = normalizer.build_source_display_plan(repo, "alpha", opponent_plan)
            self.assertEqual(again["change_row_count"], 0)

    def test_sync_rejects_ambiguous_project_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_programs(repo, [])
            for school, name in (("alpha", "Beloit"), ("beta", "Beloit"),
                                 ("gamma", "Beloit College")):
                write_opponents(repo, school, [
                    {"source_opponent_label": name, "canonical_opponent_key": "beloit",
                     "canonical_opponent_name": name},
                ])
            write_csv(repo / "schools" / "alpha" / "source-games.csv",
                ["source_game_id", "normalized_opponent_key", "normalized_opponent_name"],
                [{"source_game_id": "A-1", "normalized_opponent_key": "beloit",
                  "normalized_opponent_name": "Beloit College"}])
            opponent_plan = normalizer.build_normalization_plan(repo, "alpha")
            self.assertEqual(opponent_plan["status"], "BLOCKED")
            with self.assertRaisesRegex(ValueError, "ambiguous"):
                normalizer.build_source_display_plan(repo, "alpha", opponent_plan)



if __name__ == "__main__":
    unittest.main()
