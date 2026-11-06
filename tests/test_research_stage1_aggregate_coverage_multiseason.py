"""Multi-season early aggregate closeout remains exact, ledger-preserving, and fail-closed."""
from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import research_stage1_aggregate_coverage as mod


RESEARCH_BASE = "8" * 40
SCHOOL = "saint-joseph-s"
OWNER = "https://github.com/pollackelliott/college-basketball-history/issues/478"
SEASONS = [
    ("1911-12", (6, 22, 28), (5, 8, 13), (1, 14, 15)),
    ("1916-17", (18, 5, 23), (16, 5, 21), (2, 0, 2)),
    ("1924-25", (9, 9, 18), (7, 5, 12), (2, 4, 6)),
    ("1925-26", (4, 11, 15), (4, 5, 9), (0, 6, 6)),
    ("1926-27", (6, 11, 17), (5, 11, 16), (1, 0, 1)),
]

LEGACY_NONBLOCKING_COUNTS = {
    "1911-12": 23,
    "1916-17": 20,
    "1924-25": 4,
    "1925-26": 4,
    "1926-27": 12,
}


def jb(value):
    return mod.json_bytes(value)


def csv_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode()


def record(values):
    return {"wins": values[0], "losses": values[1], "games": values[2]}


def legacy_full_season(season):
    start = int(season[:4])
    return f"{start:04d}-{start + 1:04d}"


class MultiSeasonAggregateCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.parent = self.root / "parent.zip"
        self.audit_file = self.root / "audit.json"
        self.closeout_file = self.root / "closeout.zip"
        self.registry = self.root / "authorities.json"

        ledger = []
        census = []
        residuals = []
        game_no = 0
        for season, institutional, identified, unidentified in SEASONS:
            wins, losses, games = identified
            results = ["W"] * wins + ["L"] * losses
            self.assertEqual(len(results), games)
            for result in results:
                game_no += 1
                ledger.append({
                    "research_game_id": f"SJU-{game_no:04d}",
                    "season_label": season,
                    "opponent_literal": f"Documented Opponent {game_no}",
                    "game_type": "REGULAR_SEASON",
                    "game_universe_state": "ACCEPTED",
                    "game_inclusion": "INCLUDED",
                    "played_result": result,
                })
            census.append({
                "season_label": season,
                "source_aggregate_wins": str(institutional[0]),
                "source_aggregate_losses": str(institutional[1]),
                "source_aggregate_games": str(institutional[2]),
                "accepted_or_identified_rows": str(identified[2]),
                "known_played_wins": str(identified[0]),
                "known_played_losses": str(identified[1]),
            })
            residuals.append({
                "blocker_id": "SJU-" + season + "-AGGREGATE",
                "season": season,
                "class": "FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION",
                "research_state": "RESEARCH_EXHAUSTED_SOURCE_COVERAGE",
                "detail": {
                    "identified_game_rows": identified[2],
                    "unidentified_game_rows": unidentified[2],
                },
                "research_evidence_summary": (
                    "Target institutional aggregate and bounded reciprocal/archive "
                    "research exhausted; unidentified identities remain unsupported."
                ),
            })

        self.ledger_raw = csv_bytes(ledger)
        self.nonblocking_raw = jb([{
            "season": "1952-53",
            "class": "SOURCE_INTERNAL_AGGREGATE_CONFLICT",
            "blocking": False,
            "status": "PRESERVE_UNCHANGED",
        }])
        members = {
            "structured-stage1-ledger.csv": self.ledger_raw,
            "season-census.csv": csv_bytes(census),
            "blocking-residuals.json": jb(residuals),
            "nonblocking-residuals.json": self.nonblocking_raw,
            "stage1-status.json": jb({
                "school_key": SCHOOL,
                "status": "RESEARCH_BLOCKED_SOURCE_COVERAGE",
                "stage1_complete": False,
                "research_base_sha": RESEARCH_BASE,
                "total_candidate_game_rows": len(ledger),
                "blocking_residual_count": len(residuals),
            }),
            "research-log.md": b"Preserved source notes and 1952-53 nonblocking debt.\n",
        }
        manifest = {
            "game_rows": len(ledger),
            "research_base_sha": RESEARCH_BASE,
            "blocking_residuals": len(residuals),
            "members": {
                name: {"size": len(data), "sha256": mod.digest(data)}
                for name, data in members.items()
            },
        }
        members["stage1-manifest.json"] = jb(manifest)
        mod.serialize_zip(members, self.parent)
        self.parent_sha = mod.digest(self.parent.read_bytes())
        self.write_registry()

    def write_registry(self, *, drop_last=False, ledger_hash=None):
        cases = []
        source = SEASONS[:-1] if drop_last else SEASONS
        for season, institutional, identified, unidentified in source:
            cases.append({
                "school_key": SCHOOL,
                "season": season,
                "parent_checkpoint_sha256": self.parent_sha,
                "research_base_sha": RESEARCH_BASE,
                "owner_disposition": OWNER,
                "institutional_record": record(institutional),
                "identified_record": record(identified),
                "unidentified_record": record(unidentified),
                "maximum_eligible_season_start_year": 1930,
                "identified_ledger_sha256": (
                    ledger_hash if ledger_hash is not None else mod.digest(self.ledger_raw)
                ),
                "identified_rows": 71,
                "legacy_evidence_mode": mod.LEGACY_EVIDENCE_MODE,
            })
        self.registry.write_bytes(jb({
            "schema_version": 1,
            "authority_type": "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE",
            "cases": cases,
        }))

    def audit(self):
        return mod.audit_checkpoint(
            self.parent,
            expected_parent_sha256=self.parent_sha,
            registry=self.registry,
        )

    def test_five_approved_seasons_close_together_and_preserve_debt(self):
        report = self.audit()
        self.assertEqual(report["status"], mod.ELIGIBLE, report["defects"])
        self.assertEqual(report["identified_game_rows"], 71)
        self.assertEqual(report["identified_ledger_sha256"], mod.digest(self.ledger_raw))
        self.assertEqual(len(report["season_coverages"]), 5)
        self.assertNotIn("season_coverage", report)
        self.assertEqual(
            sum(item["unidentified_record"]["games"] for item in report["season_coverages"]),
            30,
        )

        self.audit_file.write_bytes(jb(report))
        audit_sha = mod.digest(self.audit_file.read_bytes())
        created = mod.closeout(
            self.parent,
            self.audit_file,
            self.closeout_file,
            parent_sha=self.parent_sha,
            audit_sha=audit_sha,
            registry=self.registry,
        )
        self.assertEqual(created["season_coverage_count"], 5)
        closeout_sha = mod.digest(self.closeout_file.read_bytes())
        verified = mod.verify_closeout(
            self.parent,
            self.closeout_file,
            self.audit_file,
            parent_sha=self.parent_sha,
            successor_sha=closeout_sha,
            audit_sha=audit_sha,
            registry=self.registry,
        )
        self.assertEqual(verified["status"], mod.VERIFIED, verified["defects"])
        self.assertEqual(len(verified["season_coverages"]), 5)

        original, _ = mod.read_zip(self.parent, self.parent_sha)
        successor, _ = mod.read_zip(self.closeout_file, closeout_sha)
        self.assertEqual(
            original["structured-stage1-ledger.csv"],
            successor["structured-stage1-ledger.csv"],
        )
        self.assertEqual(
            original["season-census.csv"],
            successor["season-census.csv"],
        )
        self.assertEqual(
            original["nonblocking-residuals.json"],
            successor["nonblocking-residuals.json"],
        )
        authoring = json.loads(successor[mod.AUTHORING_MEMBER])
        self.assertEqual(len(authoring["coverage"]), 5)
        self.assertTrue(all(
            item["terminal_classification"] == mod.TERMINAL
            for item in authoring["coverage"]
        ))
        self.assertEqual(json.loads(successor["blocking-residuals.json"]), [])

    def make_legacy_parent(
        self,
        *,
        duplicate_blocker=False,
        blocker_class="AGGREGATE_COVERAGE_AUTHORITY_REQUIRED",
    ):
        current, _ = mod.read_zip(self.parent, self.parent_sha)
        ledger = mod.as_csv(current["structured-stage1-ledger.csv"])
        legacy_ledger = []
        for row in ledger:
            legacy_ledger.append({
                "id": row["research_game_id"],
                "season": legacy_full_season(row["season_label"]),
                "source_opponent": row["opponent_literal"],
                "accepted_game_type": row["game_type"],
                "accepted_result": row["played_result"],
            })
        legacy_ledger_raw = csv_bytes(legacy_ledger)

        legacy_census = []
        for season, institutional, identified, _ in SEASONS:
            legacy_census.append({
                "season": legacy_full_season(season),
                "source_header_record": f"{institutional[0]}-{institutional[1]}",
                "expected_games": str(institutional[2]),
                "identified_competitive_games": str(identified[2]),
            })

        legacy_residuals = []
        nonblocking_no = 0
        for season, _, identified, unidentified in SEASONS:
            legacy_residuals.append({
                "residual_id": "SJU-" + season + "-AGGREGATE",
                "season": legacy_full_season(season),
                "residual_class": blocker_class,
                "state": "RESEARCH_EXHAUSTED_SOURCE_COVERAGE",
                "identified_competitive_games": str(identified[2]),
                "missing_games": str(unidentified[2]),
                "evidence_summary": "Legacy manifested bounded research exhaustion.",
                "blocking": "true",
            })
            if duplicate_blocker and season == SEASONS[0][0]:
                legacy_residuals.append({
                    "residual_id": "SJU-" + season + "-SECOND-BLOCKER",
                    "season": legacy_full_season(season),
                    "residual_class": blocker_class,
                    "state": "RESEARCH_EXHAUSTED_SOURCE_COVERAGE",
                    "identified_competitive_games": str(identified[2]),
                    "missing_games": str(unidentified[2]),
                    "evidence_summary": "Deliberate duplicate blocking residual.",
                    "blocking": "true",
                })
            for _ in range(LEGACY_NONBLOCKING_COUNTS[season]):
                nonblocking_no += 1
                legacy_residuals.append({
                    "residual_id": f"EXACT_DATE_UNKNOWN-SJU-R1-{nonblocking_no:05d}",
                    "season": legacy_full_season(season),
                    "residual_class": "EXACT_DATE_UNKNOWN",
                    "state": "PRESERVE_UNCHANGED",
                    "identified_competitive_games": "1",
                    "missing_games": "0",
                    "evidence_summary": "Identified game retained with nonblocking exact-date debt.",
                    "blocking": "false",
                })
        legacy_residuals.append({
            "residual_id": "SJU-1952-53-NONBLOCKING",
            "season": "1952-1953",
            "residual_class": "SOURCE_INTERNAL_AGGREGATE_CONFLICT",
            "state": "PRESERVE_UNCHANGED",
            "identified_competitive_games": "25",
            "missing_games": "0",
            "evidence_summary": "All game identities stable; aggregate conflict is nonblocking.",
            "blocking": "false",
        })

        members = {
            "stage1-ledger.csv": legacy_ledger_raw,
            "stage1-season-census.csv": csv_bytes(legacy_census),
            "stage1-residuals.csv": csv_bytes(legacy_residuals),
            "status.json": jb({
                "school": SCHOOL,
                "research_base_sha": RESEARCH_BASE,
                "stage1_complete": False,
            }),
            "research-log.md": b"Original legacy research log.\n",
        }
        manifest = {
            "research_base_sha": RESEARCH_BASE,
            "files": [
                {
                    "path": name,
                    "bytes": len(data),
                    "sha256": mod.digest(data),
                }
                for name, data in members.items()
            ],
        }
        members["manifest.json"] = jb(manifest)
        mod.serialize_zip(members, self.parent)
        self.parent_sha = mod.digest(self.parent.read_bytes())
        self.ledger_raw = legacy_ledger_raw
        self.nonblocking_raw = members["stage1-residuals.csv"]
        self.write_registry()

    def test_legacy_root_layout_closes_without_rewriting_parent_evidence(self):
        self.make_legacy_parent()
        original, _ = mod.read_zip(self.parent, self.parent_sha)
        report = self.audit()
        self.assertEqual(report["status"], mod.ELIGIBLE, report["defects"])
        self.assertTrue(report["legacy_parent_projection"])
        self.assertEqual(report["identified_ledger_sha256"], mod.digest(self.ledger_raw))
        self.assertEqual(len(report["season_coverages"]), 5)

        self.audit_file.write_bytes(jb(report))
        audit_sha = mod.digest(self.audit_file.read_bytes())
        created = mod.closeout(
            self.parent,
            self.audit_file,
            self.closeout_file,
            parent_sha=self.parent_sha,
            audit_sha=audit_sha,
            registry=self.registry,
        )
        self.assertEqual(created["season_coverage_count"], 5)
        closeout_sha = mod.digest(self.closeout_file.read_bytes())
        verified = mod.verify_closeout(
            self.parent,
            self.closeout_file,
            self.audit_file,
            parent_sha=self.parent_sha,
            successor_sha=closeout_sha,
            audit_sha=audit_sha,
            registry=self.registry,
        )
        self.assertEqual(verified["status"], mod.VERIFIED, verified["defects"])

        successor, _ = mod.read_zip(self.closeout_file, closeout_sha)
        for name, data in original.items():
            self.assertEqual(successor[name], data, name)
        self.assertEqual(successor["stage1-ledger.csv"], self.ledger_raw)
        self.assertEqual(successor["stage1-residuals.csv"], self.nonblocking_raw)
        self.assertIn("structured-stage1-ledger.csv", successor)
        self.assertIn("season-census.csv", successor)
        self.assertEqual(json.loads(successor["blocking-residuals.json"]), [])
        self.assertTrue(json.loads(successor["stage1-status.json"])["stage1_complete"])

    def test_second_blocking_residual_in_authority_season_still_fails_closed(self):
        self.make_legacy_parent(duplicate_blocker=True)
        report = self.audit()
        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(
            report["defects"],
            ["DUPLICATE_LEGACY_RESIDUAL_SEASON:1911-12"],
        )

    def test_unknown_authority_bound_blocker_class_still_fails_closed(self):
        self.make_legacy_parent(blocker_class="UNRECOGNIZED_LEGACY_BLOCKER_CLASS")
        report = self.audit()
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("UNRELATED_STAGE1_BLOCKER", report["defects"])
        self.assertIn("OWNER_AUTHORITY_POPULATION_MISMATCH", report["defects"])

    def test_legacy_season_label_normalization_is_fail_closed(self):
        self.assertEqual(mod._legacy_season_label("1911-1912"), "1911-12")
        self.assertEqual(mod._legacy_season_label("1999-2000"), "1999-00")
        self.assertEqual(mod._legacy_season_label("1911-1913"), "1911-1913")
        self.assertEqual(mod._legacy_season_label("1911-12"), "1911-12")
        self.assertEqual(mod._legacy_season_label("not-a-season"), "not-a-season")

    def test_exact_authority_population_is_required(self):
        self.write_registry(drop_last=True)
        report = self.audit()
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("NO_EXACT_OWNER_AUTHORITY", report["defects"])
        self.assertIn("OWNER_AUTHORITY_POPULATION_MISMATCH", report["defects"])

    def test_ledger_hash_binding_is_enforced(self):
        self.write_registry(ledger_hash="0" * 64)
        report = self.audit()
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("IDENTIFIED_LEDGER_HASH_MISMATCH", report["defects"])

    def test_legacy_evidence_mode_must_be_explicit(self):
        data = json.loads(self.registry.read_bytes())
        for case in data["cases"]:
            case.pop("legacy_evidence_mode", None)
        self.registry.write_bytes(jb(data))
        report = self.audit()
        self.assertEqual(report["status"], "FAIL")
        self.assertIn("MISSING_STRUCTURED_RESEARCH_EVIDENCE", report["defects"])


if __name__ == "__main__":
    unittest.main()
