"""Generic postseason-round reconciliation read/write schema regressions.

Neither test fixture nor repair selects historical basketball truth: the
approved review controls each action, and raw source evidence is preserved.
"""
from __future__ import annotations

import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    WorkflowError,
    _assertion_value,
    apply_reconciliation_decisions,
    set_source_field,
)


class PostseasonRoundReconciliationTests(unittest.TestCase):
    def _write(self, root: Path, path: str, fields: list[str], rows: list[dict[str, str]]) -> None:
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def _read(self, root: Path, path: str) -> list[dict[str, str]]:
        with (root / path).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    def _fixture(self, root: Path, *, tamper_assertion: bool = False) -> dict:
        cases = (
            ("ONE", "opponent-one", "1984-03-15", "R64", "Play-in",
             "USE_SOURCE", "74", "66"),
            ("TWO", "opponent-two", "1984-03-17", "R32", "R64",
             "NORMALIZE_SOURCE_TO_CANONICAL", "63", "59"),
        )
        canonicals, sources, assertions, discrepancies, decisions = [], [], [], [], []
        for suffix, opponent, date, source_round, canonical_round, action, score_a, score_b in cases:
            game_id = "CBBG-EXAMPLE-" + suffix
            source_id = "EXAMPLE-" + suffix
            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            canonical.update({
                "canonical_game_id": game_id,
                "season_label": "1983-1984",
                "game_date": date,
                "date_precision": "EXACT",
                "team_a_key": "example",
                "team_b_key": opponent,
                "team_a_score": score_a,
                "team_b_score": score_b,
                "result_winner_team_key": "example",
                "overtime_periods": "0",
                "site_type": "NEUTRAL",
                "game_type": "NCAA_TOURNAMENT",
                "postseason_round": canonical_round,
                "canonical_status": "PROVISIONAL",
            })
            source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            source.update({
                "source_game_id": source_id,
                "source_program_key": "example",
                "season_label": "1983-1984",
                "game_date": date,
                "normalized_opponent_key": opponent,
                "normalized_opponent_name": opponent.title(),
                "team_score": score_a,
                "opponent_score": score_b,
                "played_result": "W",
                "overtime_periods": "0",
                "curated_site_type": "NEUTRAL",
                "curated_game_type": "NCAA_TOURNAMENT",
                "curated_postseason_round": source_round,
                "raw_text": "Original institutional record: " + suffix + " / " + source_round,
            })
            assertion = dict(source)
            assertion.update({
                "assertion_id": "ASRT-" + suffix,
                "canonical_game_id": game_id,
                "match_status": "MATCHED",
                "match_method": "TEST_FIXTURE",
            })
            if tamper_assertion and suffix == "ONE":
                assertion["curated_postseason_round"] = "Sweet Sixteen"
            discrepancy = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
            discrepancy.update({
                "discrepancy_id": "DISC-" + suffix,
                "canonical_game_id": game_id,
                "field_name": "postseason_round",
                "source_a_program_key": "example",
                "source_a_value": source_round,
                "canonical_value": canonical_round,
                "status": "UNDER_REVIEW",
            })
            decisions.append({
                "decision_id": "ROUND-" + suffix,
                "category": "discrepancy",
                "source_game_id": source_id,
                "canonical_game_id": game_id,
                "field_name": "postseason_round",
                "source_value": source_round,
                "canonical_value": canonical_round,
                "decision": action,
                "resolution_basis": "Fixture owner-approved historical round selection.",
                "canonical_patch": {},
                "source_patch": {},
            })
            canonicals.append(canonical)
            sources.append(source)
            assertions.append(assertion)
            discrepancies.append(discrepancy)

        self._write(root, "data/canonical/games.csv", ingest_school.CANONICAL_FIELDS, canonicals)
        self._write(root, "data/evidence/game-assertions.csv", ingest_school.ASSERTION_FIELDS, assertions)
        self._write(root, "data/reconciliation/discrepancies.csv", ingest_school.DISCREPANCY_FIELDS, discrepancies)
        self._write(root, "schools/example/source-games.csv", ingest_school.ASSERTION_FIELDS, sources)
        return {"school_key": "example", "approved_plan_hash": "a" * 64, "decisions": decisions}

    def test_schema_read_uses_curated_postseason_round(self):
        row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
        row["curated_postseason_round"] = "R64"
        self.assertNotIn("postseason_round", ingest_school.ASSERTION_FIELDS)
        self.assertEqual(_assertion_value(row, {}, "postseason_round"), "R64")

    def test_schema_write_uses_curated_postseason_round(self):
        row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
        set_source_field(row, {}, "postseason_round", "R32")
        self.assertEqual(row["curated_postseason_round"], "R32")
        self.assertNotIn("postseason_round", row)

    def test_both_approved_actions_in_one_transaction(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            approved = self._fixture(root)
            before = self._read(root, "schools/example/source-games.csv")
            counts = apply_reconciliation_decisions(root, approved)
            self.assertEqual(counts["processed"], 2)
            self.assertEqual(counts["canonical_changes"], 1)
            self.assertEqual(counts["source_normalizations"], 1)

            games = {row["canonical_game_id"]: row
                     for row in self._read(root, "data/canonical/games.csv")}
            sources = {row["source_game_id"]: row
                       for row in self._read(root, "schools/example/source-games.csv")}
            assertions = {row["source_game_id"]: row
                          for row in self._read(root, "data/evidence/game-assertions.csv")}
            discrepancies = {row["discrepancy_id"]: row
                             for row in self._read(root, "data/reconciliation/discrepancies.csv")}

            # USE_SOURCE: canonical adopts the approved source R64; source evidence unchanged.
            self.assertEqual(games["CBBG-EXAMPLE-ONE"]["postseason_round"], "R64")
            self.assertEqual(sources["EXAMPLE-ONE"]["curated_postseason_round"], "R64")
            self.assertEqual(assertions["EXAMPLE-ONE"]["curated_postseason_round"], "R64")
            self.assertEqual(discrepancies["DISC-ONE"]["status"], "RESOLVED")

            # NORMALIZE_SOURCE_TO_CANONICAL: canonical R64 is retained; curated
            # source and assertion round are normalized, never to a phantom column.
            self.assertEqual(games["CBBG-EXAMPLE-TWO"]["postseason_round"], "R64")
            self.assertEqual(sources["EXAMPLE-TWO"]["curated_postseason_round"], "R64")
            self.assertEqual(assertions["EXAMPLE-TWO"]["curated_postseason_round"], "R64")
            self.assertNotIn("postseason_round", sources["EXAMPLE-TWO"])
            self.assertEqual(discrepancies["DISC-TWO"]["source_a_value"], "R32")
            self.assertEqual(discrepancies["DISC-TWO"]["status"], "RESOLVED")

            for original, updated in zip(before, sources.values()):
                self.assertEqual(updated["raw_text"], original["raw_text"])
                self.assertEqual(updated["curated_game_type"], "NCAA_TOURNAMENT")
                self.assertEqual(updated["curated_site_type"], "NEUTRAL")

    def test_drifted_assertion_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            approved = self._fixture(root, tamper_assertion=True)
            with self.assertRaisesRegex(WorkflowError, "ingested source assertion value changed"):
                apply_reconciliation_decisions(root, approved)


if __name__ == "__main__":
    unittest.main()
