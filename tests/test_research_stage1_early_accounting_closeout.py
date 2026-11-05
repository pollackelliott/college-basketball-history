import csv
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "research_stage1_early_accounting_closeout",
    ROOT / "tools" / "research_stage1_early_accounting_closeout.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)


class EarlyAccountingCloseoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.parent = self.root / "parent.zip"
        self.registry = self.root / "registry.json"
        self._write_parent()
        self.parent_sha = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        self.ledger_sha = self._member_sha("stage1-identified-game-ledger.csv")
        self._write_registry()

    def _csv(self, fields, rows):
        out = io.StringIO(newline="")
        writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        return out.getvalue().encode()

    def _write_parent(self, *, extra_blocker=False, aggregate_games=2, anon=False):
        ledger = self._csv(
            ["research_game_id", "season", "source_opponent_label", "source_opponent_raw",
             "played_result", "game_type", "inclusion_status", "notes"],
            [
                {"research_game_id": "G1", "season": "1902-03",
                 "source_opponent_label": "Alpha" if not anon else "ANONYMOUS GAME",
                 "source_opponent_raw": "Alpha", "played_result": "W",
                 "game_type": "REGULAR_SEASON", "inclusion_status": "INCLUDED", "notes": ""},
                {"research_game_id": "G2", "season": "1902-03",
                 "source_opponent_label": "Beta", "source_opponent_raw": "Beta",
                 "played_result": "L", "game_type": "REGULAR_SEASON",
                 "inclusion_status": "INCLUDED", "notes": ""},
                {"research_game_id": "G3", "season": "1903-04",
                 "source_opponent_label": "Gamma", "source_opponent_raw": "Gamma",
                 "played_result": "W", "game_type": "REGULAR_SEASON",
                 "inclusion_status": "INCLUDED", "notes": ""},
            ],
        )
        residual_rows = [
            {"residual_class": "EARLY_SOURCE_EXPLICIT_AGGREGATE_ONLY_GAME_IDENTITIES_UNKNOWN",
             "season": "1904-05", "count": "2", "detail": "aggregate",
             "blocking": "YES", "next_evidence_family": "CONVERGED"},
            {"residual_class": "EARLY_DETAILED_VS_OVERALL_CLUB_ACCOUNTING_CONTRADICTION",
             "season": "1902-03|1903-04", "count": "2", "detail": "accounting",
             "blocking": "YES", "next_evidence_family": "CONVERGED"},
            {"residual_class": "IDENTIFIED_GAME_SCORE_UNKNOWN", "season": "1903-04",
             "count": "1", "detail": "score", "blocking": "NO",
             "next_evidence_family": "NONE"},
        ]
        if extra_blocker:
            residual_rows.append(
                {"residual_class": "OTHER", "season": "1905-06", "count": "1",
                 "detail": "x", "blocking": "YES", "next_evidence_family": "x"}
            )
        residuals = self._csv(
            ["residual_class", "season", "count", "detail", "blocking", "next_evidence_family"],
            residual_rows,
        )
        accounting = self._csv(
            ["season", "source_status", "official_w", "official_l", "identified_rows",
             "identified_w", "identified_l", "provisional_included_rows",
             "provisional_included_w", "provisional_included_l", "mechanical_w_delta",
             "mechanical_l_delta", "source_page", "official_games", "detail_games",
             "games_delta_official_minus_detail", "season_state"],
            [
                {"season": "1902-03", "source_status": "DETAILED", "official_w": "1",
                 "official_l": "1", "identified_rows": "2", "identified_w": "1",
                 "identified_l": "1", "provisional_included_rows": "2",
                 "provisional_included_w": "1", "provisional_included_l": "1",
                 "mechanical_w_delta": "0", "mechanical_l_delta": "0", "source_page": "1",
                 "official_games": "2", "detail_games": "2",
                 "games_delta_official_minus_detail": "0",
                 "season_state": "DETAIL_SHORT_OF_OFFICIAL_OR_EQUAL"},
                {"season": "1903-04", "source_status": "DETAILED", "official_w": "0",
                 "official_l": "0", "identified_rows": "1", "identified_w": "1",
                 "identified_l": "0", "provisional_included_rows": "1",
                 "provisional_included_w": "1", "provisional_included_l": "0",
                 "mechanical_w_delta": "-1", "mechanical_l_delta": "0", "source_page": "1",
                 "official_games": "0", "detail_games": "1",
                 "games_delta_official_minus_detail": "-1",
                 "season_state": "DETAIL_EXCEEDS_OFFICIAL_IN_AT_LEAST_ONE_RESULT"},
                {"season": "1904-05", "source_status": "AGGREGATE_ONLY", "official_w": "2",
                 "official_l": "0", "identified_rows": "0", "identified_w": "0",
                 "identified_l": "0", "provisional_included_rows": "0",
                 "provisional_included_w": "0", "provisional_included_l": "0",
                 "mechanical_w_delta": "2", "mechanical_l_delta": "0", "source_page": "1",
                 "official_games": str(aggregate_games), "detail_games": "0",
                 "games_delta_official_minus_detail": str(aggregate_games),
                 "season_state": "AGGREGATE_ONLY"},
            ],
        )
        aggregate = self._csv(
            ["season", "official_w", "official_l", "official_games",
             "source_page", "source_note", "individual_game_rows_in_guide"],
            [{"season": "1904-05", "official_w": "2", "official_l": "0",
              "official_games": str(aggregate_games), "source_page": "1",
              "source_note": "All games against club teams",
              "individual_game_rows_in_guide": "0"}],
        )
        census = self._csv(
            ["season", "source_status", "official_w", "official_l",
             "identified_rows", "identified_w", "identified_l"],
            [
                {"season": "1902-03", "source_status": "DETAILED", "official_w": "1",
                 "official_l": "1", "identified_rows": "2", "identified_w": "1",
                 "identified_l": "1"},
                {"season": "1903-04", "source_status": "DETAILED", "official_w": "0",
                 "official_l": "0", "identified_rows": "1", "identified_w": "1",
                 "identified_l": "0"},
                {"season": "1904-05", "source_status": "AGGREGATE_ONLY", "official_w": "2",
                 "official_l": "0", "identified_rows": "0", "identified_w": "0",
                 "identified_l": "0"},
            ],
        )
        summary = {
            "official_season_aggregate": {"wins": 3, "losses": 1, "games": 4},
            "chronological_detail": {"wins": 2, "losses": 1, "rows": 3},
            "club_high_school_aggregate": {"wins": 2, "losses": 0, "games": 2,
                                           "distinct_labels": 1},
            "simple_union_implied_overlap_games": 1,
            "direct_candidate_result_conflicts": [
                {"aggregate_opponent_label": "X", "aggregate_record": "1-0",
                 "candidate_detail_record": "0-1"}
            ],
            "conclusion": (
                "SIMPLE_UNION_RECONCILIATION_REJECTED. Aggregate structures cannot be "
                "converted into anonymous or inferred game rows. String-similar opponent "
                "labels are review triggers only, not same-game authority."
            ),
        }
        status = {
            "school_key": "example", "stage": "STAGE_1", "state": "BLOCKED",
            "stage1_complete": False, "research_base_sha": "a" * 40,
            "anonymous_games_manufactured": 0,
            "early_archive_pass": {
                "new_game_identities_recovered": 0,
                "source_explicit_aggregate_only_games": aggregate_games,
            },
            "early_spalding_pass": {"new_game_identities_recovered": 0},
        }
        members = {
            "stage1-status.json": mod.json_bytes(status),
            "stage1-residuals.csv": residuals,
            "stage1-identified-game-ledger.csv": ledger,
            "stage1-season-census.csv": census,
            "source-explicit-aggregate-only-seasons.csv": aggregate,
            "early-period-season-accounting.csv": accounting,
            "early-reconciliation-summary.json": mod.json_bytes(summary),
        }
        manifest = {
            "school_key": "example", "stage": "STAGE_1", "state": "BLOCKED",
            "research_base_sha": "a" * 40,
            "files": [
                {"path": name, "size": len(data), "sha256": mod.digest(data)}
                for name, data in sorted(members.items())
            ],
        }
        members["manifest.json"] = mod.json_bytes(manifest)
        mod.serialize_zip(members, self.parent)

    def _member_sha(self, name):
        members, _ = mod.read_zip(
            self.parent, hashlib.sha256(self.parent.read_bytes()).hexdigest()
        )
        return mod.digest(members[name])

    def _write_registry(self):
        registry = {
            "schema_version": 1,
            "authority_type": "OWNER_APPROVED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT",
            "cases": [{
                "school_key": "example",
                "parent_checkpoint_sha256": self.parent_sha,
                "research_base_sha": "a" * 40,
                "owner_disposition": "https://github.com/example/repo/issues/1",
                "identified_ledger_sha256": self.ledger_sha,
                "identified_rows": 3,
                "aggregate_only_seasons": [{
                    "season": "1904-05",
                    "institutional_record": {"wins": 2, "losses": 0, "games": 2},
                    "identified_record": {"wins": 0, "losses": 0, "games": 0},
                    "source_note": "All games against club teams",
                }],
                "accounting_contradiction_seasons": [
                    {"season": "1902-03",
                     "institutional_record": {"wins": 1, "losses": 1, "games": 2},
                     "identified_record": {"wins": 1, "losses": 1, "games": 2},
                     "mechanical_delta": {"wins": 0, "losses": 0, "games": 0}},
                    {"season": "1903-04",
                     "institutional_record": {"wins": 0, "losses": 0, "games": 0},
                     "identified_record": {"wins": 1, "losses": 0, "games": 1},
                     "mechanical_delta": {"wins": -1, "losses": 0, "games": -1}},
                ],
                "accounting_summary": {
                    "official_season_aggregate": {"wins": 3, "losses": 1, "games": 4},
                    "chronological_detail": {"wins": 2, "losses": 1, "rows": 3},
                    "club_high_school_aggregate": {
                        "wins": 2, "losses": 0, "games": 2, "distinct_labels": 1
                    },
                    "simple_union_implied_overlap_games": 1,
                },
                "minimum_direct_result_conflicts": 1,
            }],
        }
        self.registry.write_text(json.dumps(registry), encoding="utf-8")

    def audit(self):
        return mod.audit_checkpoint(
            self.parent,
            expected_parent_sha256=self.parent_sha,
            registry=self.registry,
        )

    def test_valid_mixed_population_closes_without_ledger_drift(self):
        report = self.audit()
        self.assertEqual(report["status"], mod.ELIGIBLE)
        self.assertFalse(report["defects"])
        self.assertEqual(report["aggregate_unidentified_games"], 2)
        self.assertEqual(
            report["accounting_contradictions"][1]["mechanical_delta"]["games"], -1
        )
        audit = self.root / "audit.json"
        audit.write_bytes(mod.json_bytes(report))
        audit_sha = hashlib.sha256(audit.read_bytes()).hexdigest()
        close = self.root / "close.zip"
        created = mod.closeout(
            self.parent, audit, close, parent_sha=self.parent_sha,
            audit_sha=audit_sha, registry=self.registry
        )
        verified = mod.verify_closeout(
            self.parent, close, audit, parent_sha=self.parent_sha,
            successor_sha=created["closeout_sha256"], audit_sha=audit_sha,
            registry=self.registry,
        )
        self.assertEqual(verified["status"], mod.VERIFIED)
        self.assertTrue(verified["stage1_complete"])

    def test_missing_owner_authority_fails(self):
        self.registry.write_text(
            json.dumps({
                "schema_version": 1,
                "authority_type": "OWNER_APPROVED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT",
                "cases": [],
            }),
            encoding="utf-8",
        )
        self.assertIn("NO_EXACT_OWNER_AUTHORITY", self.audit()["defects"])

    def test_extra_blocker_fails(self):
        self._write_parent(extra_blocker=True)
        self.parent_sha = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        self.ledger_sha = self._member_sha("stage1-identified-game-ledger.csv")
        self._write_registry()
        self.assertIn("UNRELATED_OR_MISSING_STAGE1_BLOCKER", self.audit()["defects"])

    def test_aggregate_drift_fails(self):
        self._write_parent(aggregate_games=3)
        self.parent_sha = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        self.ledger_sha = self._member_sha("stage1-identified-game-ledger.csv")
        self._write_registry()
        self.assertTrue(any(
            defect.startswith("AGGREGATE_RECORD_AUTHORITY_MISMATCH")
            for defect in self.audit()["defects"]
        ))

    def test_anonymous_game_fails(self):
        self._write_parent(anon=True)
        self.parent_sha = hashlib.sha256(self.parent.read_bytes()).hexdigest()
        self.ledger_sha = self._member_sha("stage1-identified-game-ledger.csv")
        self._write_registry()
        self.assertIn("FABRICATED_GAME_ROW", self.audit()["defects"])

    def test_tampered_successor_fails(self):
        report = self.audit()
        audit = self.root / "audit.json"
        audit.write_bytes(mod.json_bytes(report))
        audit_sha = hashlib.sha256(audit.read_bytes()).hexdigest()
        close = self.root / "close.zip"
        created = mod.closeout(
            self.parent, audit, close, parent_sha=self.parent_sha,
            audit_sha=audit_sha, registry=self.registry
        )
        members, _ = mod.read_zip(close, created["closeout_sha256"])
        members["stage1-identified-game-ledger.csv"] += b"tamper\n"
        mod.serialize_zip(members, close)
        verified = mod.verify_closeout(
            self.parent, close, audit, parent_sha=self.parent_sha,
            successor_sha=hashlib.sha256(close.read_bytes()).hexdigest(),
            audit_sha=audit_sha, registry=self.registry,
        )
        self.assertEqual(verified["status"], "FAIL")


if __name__ == "__main__":
    unittest.main()
