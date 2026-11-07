"""Historical season coverage must never create fictional games or distort series."""
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from build_site_data import (
    normalize_scope_season,
    validated_historical_accounting,
    validated_historical_coverage,
)


class HistoricalCoverageBuildTests(unittest.TestCase):
    def setUp(self):
        self.authority = {
            ("example", "1919-20"): {
                "institutional_record": {"wins": 6, "losses": 10, "games": 16},
                "identified_record": {"wins": 3, "losses": 7, "games": 10},
                "unidentified_record": {"wins": 3, "losses": 3, "games": 6},
                "owner_disposition": "https://github.com/example/history/issues/1",
            }
        }
        self.seasons = {"1919-1920": [{"result": "W"}] * 3 + [{"result": "L"}] * 7}
        self.row = {
            "program_key": "example", "season_label": "1919-20",
            "official_wins": "6", "official_losses": "10", "official_games": "16",
            "documented_wins": "3", "documented_losses": "7", "documented_games": "10",
            "unidentified_wins": "3", "unidentified_losses": "3", "unidentified_games": "6",
            "source_label": "Example institutional record book",
            "owner_disposition": "https://github.com/example/history/issues/1",
            "stage1_audit_sha256": "f" * 64,
            "public_note": "",
        }

    def build(self, rows=None, seasons=None, authority=None):
        return validated_historical_coverage(
            [self.row] if rows is None else rows,
            "example",
            self.seasons if seasons is None else seasons,
            self.authority if authority is None else authority,
        )

    def test_official_and_documented_records_remain_distinct(self):
        before = {key: list(value) for key, value in self.seasons.items()}
        result = self.build()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["season_label"], "1919-1920")
        self.assertEqual(result[0]["unidentified_record"]["games"], 6)
        self.assertEqual(result[0]["official_record"]["wins"], 6)
        self.assertIn("10 individual game results", result[0]["note"])
        self.assertIn("six", result[0]["note"].lower().replace("6", "six"))
        self.assertEqual(self.seasons, before)

    def test_no_coverage_row_preserves_current_build(self):
        self.assertEqual(self.build(rows=[]), [])

    def test_canonical_result_drift_is_rejected(self):
        games = {"1919-1920": [{"result": "W"}] * 4 + [{"result": "L"}] * 6}
        with self.assertRaisesRegex(ValueError, "arithmetic/canonical discrepancy"):
            self.build(seasons=games)

    def test_unauthorized_season_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "lacks owner authority"):
            self.build(authority={})

    def test_missing_closeout_hash_is_rejected(self):
        self.row["stage1_audit_sha256"] = ""
        with self.assertRaisesRegex(ValueError, "audit SHA-256 required"):
            self.build()

    def test_changed_source_aggregate_is_rejected(self):
        self.row["official_wins"] = "7"
        with self.assertRaisesRegex(ValueError, "arithmetic/canonical discrepancy"):
            self.build()

    def test_duplicate_coverage_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.build(rows=[self.row, dict(self.row)])

    def test_missing_or_phantom_canonical_games_rejected(self):
        with self.assertRaisesRegex(ValueError, "arithmetic/canonical discrepancy"):
            self.build(seasons={})

    def test_zero_documented_coverage_season_is_allowed(self):
        authority = {
            ("example", "1909-10"): {
                "institutional_record": {"wins": 2, "losses": 0, "games": 2},
                "identified_record": {"wins": 0, "losses": 0, "games": 0},
                "unidentified_record": {"wins": 2, "losses": 0, "games": 2},
                "owner_disposition": "https://github.com/example/history/issues/2",
            }
        }
        row = {
            "program_key": "example",
            "season_label": "1909-10",
            "official_wins": "2",
            "official_losses": "0",
            "official_games": "2",
            "documented_wins": "0",
            "documented_losses": "0",
            "documented_games": "0",
            "unidentified_wins": "2",
            "unidentified_losses": "0",
            "unidentified_games": "2",
            "source_label": "Institutional aggregate",
            "owner_disposition": "https://github.com/example/history/issues/2",
            "stage1_audit_sha256": "e" * 64,
            "public_note": "",
        }
        result = validated_historical_coverage(
            [row],
            "example",
            {},
            authority,
        )
        self.assertEqual(result[0]["season_label"], "1909-1910")
        self.assertEqual(result[0]["documented_record"]["games"], 0)
        self.assertEqual(result[0]["official_record"]["games"], 2)

    def test_accounting_contradiction_preserves_negative_delta(self):
        authority = {
            ("example", "1903-04"): {
                "institutional_record": {"wins": 0, "losses": 0, "games": 0},
                "identified_record": {"wins": 1, "losses": 0, "games": 1},
                "mechanical_delta": {"wins": -1, "losses": 0, "games": -1},
                "owner_disposition": "https://github.com/example/history/issues/2",
            }
        }
        rows = [
            {
                "program_key": "example",
                "season_label": "1903-04",
                "official_wins": "0",
                "official_losses": "0",
                "official_games": "0",
                "documented_wins": "1",
                "documented_losses": "0",
                "documented_games": "1",
                "delta_wins": "-1",
                "delta_losses": "0",
                "delta_games": "-1",
                "classification":
                    "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
                "source_label": "Conflicting institutional structures",
                "owner_disposition": "https://github.com/example/history/issues/2",
                "stage1_audit_sha256": "e" * 64,
                "public_note": "Diagnostic only",
            }
        ]
        seasons = {"1903-1904": [{"result": "W"}]}
        result = validated_historical_accounting(
            rows,
            "example",
            seasons,
            authority,
        )
        self.assertEqual(result[0]["season_label"], "1903-1904")
        self.assertEqual(result[0]["mechanical_delta"]["games"], -1)
        self.assertEqual(seasons["1903-1904"], [{"result": "W"}])

    def test_accounting_contradiction_ignores_reciprocal_canonical_union_drift(self):
        authority = {
            ("example", "1903-04"): {
                "institutional_record": {"wins": 0, "losses": 0, "games": 0},
                "identified_record": {"wins": 1, "losses": 0, "games": 1},
                "mechanical_delta": {"wins": -1, "losses": 0, "games": -1},
                "owner_disposition": "https://github.com/example/history/issues/2",
            }
        }
        row = {
            "program_key": "example",
            "season_label": "1903-04",
            "official_wins": "0",
            "official_losses": "0",
            "official_games": "0",
            "documented_wins": "1",
            "documented_losses": "0",
            "documented_games": "1",
            "delta_wins": "-1",
            "delta_losses": "0",
            "delta_games": "-1",
            "classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
            "source_label": "Conflicting institutional structures",
            "owner_disposition": "https://github.com/example/history/issues/2",
            "stage1_audit_sha256": "e" * 64,
            "public_note": "Diagnostic only",
        }
        canonical_union = {
            "1903-1904": [
                {"result": "W"},
                {"result": "W"},
                {"result": "L"},
                {"result": "T"},
            ]
        }
        before = {key: list(value) for key, value in canonical_union.items()}
        result = validated_historical_accounting(
            [row],
            "example",
            canonical_union,
            authority,
        )
        self.assertEqual(result[0]["documented_record"], {
            "wins": 1, "losses": 0, "games": 1,
        })
        self.assertEqual(result[0]["mechanical_delta"]["games"], -1)
        self.assertEqual(canonical_union, before)

    def test_accounting_contradiction_source_arithmetic_still_fails_closed(self):
        authority = {
            ("example", "1903-04"): {
                "institutional_record": {"wins": 0, "losses": 0, "games": 0},
                "identified_record": {"wins": 1, "losses": 0, "games": 1},
                "mechanical_delta": {"wins": -1, "losses": 0, "games": -1},
                "owner_disposition": "https://github.com/example/history/issues/2",
            }
        }
        row = {
            "program_key": "example",
            "season_label": "1903-04",
            "official_wins": "0",
            "official_losses": "0",
            "official_games": "0",
            "documented_wins": "1",
            "documented_losses": "0",
            "documented_games": "1",
            "delta_wins": "0",
            "delta_losses": "0",
            "delta_games": "-1",
            "classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
            "source_label": "Conflicting institutional structures",
            "owner_disposition": "https://github.com/example/history/issues/2",
            "stage1_audit_sha256": "e" * 64,
            "public_note": "Diagnostic only",
        }
        with self.assertRaisesRegex(ValueError, "arithmetic/authority discrepancy"):
            validated_historical_accounting(
                [row],
                "example",
                {"1903-1904": [{"result": "W"}, {"result": "T"}]},
                authority,
            )

    def test_accounting_contradiction_still_requires_owner_authority_and_canonical_season(self):
        authority = {
            ("example", "1903-04"): {
                "institutional_record": {"wins": 0, "losses": 0, "games": 0},
                "identified_record": {"wins": 1, "losses": 0, "games": 1},
                "mechanical_delta": {"wins": -1, "losses": 0, "games": -1},
                "owner_disposition": "https://github.com/example/history/issues/2",
            }
        }
        row = {
            "program_key": "example",
            "season_label": "1903-04",
            "official_wins": "0",
            "official_losses": "0",
            "official_games": "0",
            "documented_wins": "1",
            "documented_losses": "0",
            "documented_games": "1",
            "delta_wins": "-1",
            "delta_losses": "0",
            "delta_games": "-1",
            "classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
            "source_label": "Conflicting institutional structures",
            "owner_disposition": "https://github.com/example/history/issues/2",
            "stage1_audit_sha256": "e" * 64,
            "public_note": "Diagnostic only",
        }
        with self.assertRaisesRegex(ValueError, "lacks owner authority"):
            validated_historical_accounting(
                [row], "example", {"1903-1904": [{"result": "W"}]}, {}
            )
        with self.assertRaisesRegex(ValueError, "has no documented canonical games"):
            validated_historical_accounting(
                [row], "example", {}, authority
            )

    def test_fordham_all_17_accounting_contradictions_allow_enriched_canonical_union(self):
        repo = Path(__file__).resolve().parents[1]
        registry = json.loads(
            (repo / "data/reference/early-history-accounting-authorities.json")
            .read_text(encoding="utf-8")
        )
        case = next(
            item for item in registry["cases"]
            if item.get("school_key") == "fordham"
        )
        contradictions = case["accounting_contradiction_seasons"]
        self.assertEqual(len(contradictions), 17)

        authority = {}
        rows = []
        seasons = {}
        for item in contradictions:
            season = item["season"]
            authority[("fordham", season)] = {
                "institutional_record": dict(item["institutional_record"]),
                "identified_record": dict(item["identified_record"]),
                "mechanical_delta": dict(item["mechanical_delta"]),
                "owner_disposition": case["owner_disposition"],
            }
            rows.append({
                "program_key": "fordham",
                "season_label": season,
                "official_wins": str(item["institutional_record"]["wins"]),
                "official_losses": str(item["institutional_record"]["losses"]),
                "official_games": str(item["institutional_record"]["games"]),
                "documented_wins": str(item["identified_record"]["wins"]),
                "documented_losses": str(item["identified_record"]["losses"]),
                "documented_games": str(item["identified_record"]["games"]),
                "delta_wins": str(item["mechanical_delta"]["wins"]),
                "delta_losses": str(item["mechanical_delta"]["losses"]),
                "delta_games": str(item["mechanical_delta"]["games"]),
                "classification": "EARLY_HISTORY_SOURCE_ACCOUNTING_CONTRADICTION",
                "source_label": "Fordham institutional early-history accounting",
                "owner_disposition": case["owner_disposition"],
                "stage1_audit_sha256": "a" * 64,
                "public_note": "Diagnostic only",
            })
            identified = item["identified_record"]
            seasons[normalize_scope_season(season)] = (
                [{"result": "W"}] * (identified["wins"] + 1)
                + [{"result": "L"}] * identified["losses"]
                + [{"result": "T"}]
            )

        before = {key: list(value) for key, value in seasons.items()}
        result = validated_historical_accounting(
            rows,
            "fordham",
            seasons,
            authority,
        )
        self.assertEqual(len(result), 17)
        self.assertEqual(
            {item["season_label"] for item in result},
            {normalize_scope_season(item["season"]) for item in contradictions},
        )
        self.assertEqual(seasons, before)

    def test_short_and_full_equivalent_coverage_rows_are_duplicate(self):
        duplicate = dict(self.row)
        duplicate["season_label"] = "1919-1920"
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            self.build(rows=[self.row, duplicate])

    def test_short_and_full_equivalent_authority_keys_are_duplicate(self):
        authority = dict(self.authority)
        authority[("example", "1919-1920")] = dict(
            self.authority[("example", "1919-20")]
        )
        with self.assertRaisesRegex(ValueError, "duplicated after season normalization"):
            self.build(authority=authority)

    def test_invalid_coverage_season_fails_closed(self):
        self.row["season_label"] = "1919-21"
        with self.assertRaisesRegex(ValueError, "season invalid"):
            self.build()


if __name__ == "__main__":
    unittest.main()
