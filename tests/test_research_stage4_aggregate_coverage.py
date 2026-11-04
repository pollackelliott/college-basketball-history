"""Stage 4 carries season-level coverage as evidence, never as game rows."""
import io
import json
import sys
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import research_stage4 as mod


class Stage4AggregateCoverageTests(unittest.TestCase):
    def setUp(self):
        self.entry = {
            "school_key": "example", "season": "1919-20",
            "research_base_sha": "a" * 40,
            "institutional_record": {"wins": 6, "losses": 10, "games": 16},
            "identified_record": {"wins": 3, "losses": 7, "games": 10},
            "unidentified_record": {"wins": 3, "losses": 3, "games": 6},
            "terminal_classification": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
            "audit_sha256": "b" * 64,
        }
        self.member = "stage4-authoring/season-coverage.json"
        self.manifest = {"files": {self.member: {"sha256": "present"}}}

    def inspect(self, payload=None, manifest=None):
        raw = json.dumps({"schema_version": 1,
                          "coverage": [self.entry]} if payload is None else payload).encode()
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, "w") as z:
            z.writestr(self.member, raw)
        buffer.seek(0)
        with zipfile.ZipFile(buffer) as z:
            return mod._aggregate_coverage_payload(
                z, "", self.manifest if manifest is None else manifest,
                school_key="example", research_base_sha="a" * 40
            )

    def test_valid_aggregate_is_season_only(self):
        payload, defects, summary = self.inspect()
        self.assertFalse(defects)
        self.assertEqual(summary["unidentified_games"], 6)
        self.assertEqual(summary["seasons"], ["1919-20"])
        self.assertEqual(len(payload["coverage"]), 1)


    def test_accounting_contradiction_allows_negative_diagnostic_delta(self):
        contradiction = {
            "school_key": "example", "season": "1903-04",
            "research_base_sha": "a" * 40,
            "institutional_record": {"wins": 0, "losses": 0, "games": 0},
            "identified_record": {"wins": 1, "losses": 0, "games": 1},
            "mechanical_delta": {"wins": -1, "losses": 0, "games": -1},
            "terminal_classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
            "audit_sha256": "c" * 64,
        }
        payload, defects, summary = self.inspect(payload={
            "schema_version": 1,
            "coverage": [self.entry],
            "accounting_contradictions": [contradiction],
        })
        self.assertFalse(defects)
        self.assertEqual(summary["accounting_contradiction_seasons"], ["1903-04"])
        self.assertEqual(payload["accounting_contradictions"][0]["mechanical_delta"]["games"], -1)

    def test_accounting_contradiction_cannot_be_arithmetic_fitted(self):
        contradiction = {
            "school_key": "example", "season": "1903-04",
            "research_base_sha": "a" * 40,
            "institutional_record": {"wins": 0, "losses": 0, "games": 0},
            "identified_record": {"wins": 1, "losses": 0, "games": 1},
            "mechanical_delta": {"wins": 0, "losses": 0, "games": 0},
            "terminal_classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
            "audit_sha256": "c" * 64,
        }
        _, defects, _ = self.inspect(payload={
            "schema_version": 1,
            "coverage": [self.entry],
            "accounting_contradictions": [contradiction],
        })
        self.assertIn("ACCOUNTING_CONTRADICTION_ARITHMETIC_INVALID",
                      {d["reason"] for d in defects})

    def test_nonmanifested_payload_fails(self):
        _, defects, _ = self.inspect(manifest={"files": {}})
        self.assertIn("AGGREGATE_COVERAGE_NOT_MANIFESTED",
                      {d["reason"] for d in defects})

    def test_false_aggregate_fails(self):
        self.entry["institutional_record"]["games"] = 15
        _, defects, _ = self.inspect()
        self.assertIn("AGGREGATE_COVERAGE_ARITHMETIC_INVALID",
                      {d["reason"] for d in defects})

    def test_forged_school_identity_fails(self):
        self.entry["school_key"] = "different-school"
        _, defects, _ = self.inspect()
        self.assertIn("AGGREGATE_COVERAGE_AUTHORITY_MISMATCH",
                      {d["reason"] for d in defects})

    def test_duplicate_season_fails(self):
        _, defects, _ = self.inspect(payload={
            "schema_version": 1, "coverage": [self.entry, self.entry]
        })
        self.assertIn("AGGREGATE_COVERAGE_DUPLICATE_SEASON",
                      {d["reason"] for d in defects})

    def test_invalid_payload_shape_fails_closed(self):
        _, defects, _ = self.inspect(payload=[])
        self.assertIn("AGGREGATE_COVERAGE_INVALID_STRUCTURE",
                      {d["reason"] for d in defects})


if __name__ == "__main__":
    unittest.main()
