"""Regression matrix for hash-bound supplemental Stage 4 coverage acceptance."""
import csv
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import test_all_history_expansion_freeze as fixture
from expansion_stage4_coverage import (
    ExpansionStage4CoverageError,
    prove_expansion_stage4_coverage,
    reconcile_stage4_research_report,
)
from onboarding_hardening import _research_coverage_report


class ExpansionStage4CoverageTests(unittest.TestCase):
    def setUp(self):
        self.baseline = fixture.ExpansionFreezeTests(
            "test_01_valid_simple_expansion_freezes_and_verifies"
        )
        self.baseline.setUp()
        self.repo = self.baseline.repo

    def tearDown(self):
        self.baseline.tearDown()

    def _rows(self):
        return [
            fixture.source_row("EXP-1", "1968-1969"),
            fixture.source_row("EXP-2", "1969-1970"),
        ]

    def _prove(self, *, rows=None, cutoff="1971-1972", school="legacy", base=None):
        return prove_expansion_stage4_coverage(
            repo=self.repo,
            school_key=school,
            research_base_sha=base if base is not None else self.baseline.base,
            required_completed_season_cutoff=cutoff,
            supplemental_rows=rows if rows is not None else self._rows(),
        )

    def _read_table(self, path):
        with path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def _write_table(self, path, fields, rows):
        fixture.write_csv(path, fields, rows)
        self.baseline._recommit_baseline()

    def test_01_authenticated_legacy_baseline_publishes_completed_season(self):
        proof = self._prove()
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["workflow_kind"], "ALL_HISTORY_EXPANSION")
        self.assertEqual(proof["research_base_sha"], self.baseline.base)
        self.assertEqual(proof["inherited_required_season_source_rows"], 1)
        self.assertEqual(proof["inherited_required_season_published_canonical_rows"], 1)
        self.assertEqual(proof["supplemental_game_count"], 2)
        self.assertEqual(proof["supplemental_first_season"], "1968-1969")
        self.assertEqual(proof["supplemental_last_season"], "1969-1970")

    def test_02_only_proved_cutoff_error_can_be_removed(self):
        proof = self._prove()
        error = (
            "research package declares required completed-season cutoff 1971-1972 "
            "but contains zero competitive target-school rows for that season"
        )
        report = {
            "status": "FAIL", "errors": [error], "warnings": [],
            "counts": {"coverage": {
                "required_completed_season_cutoff": "1971-1972",
                "required_season_rows": 0,
            }},
        }
        adjusted = reconcile_stage4_research_report(report, proof)
        self.assertEqual(adjusted["status"], "PASS")
        self.assertEqual(adjusted["errors"], [])
        self.assertEqual(report["status"], "FAIL")  # no mutation of raw report
        self.assertEqual(adjusted["counts"]["coverage"]["acceptance_scope"],
                         "ALL_HISTORY_EXPANSION_SUPPLEMENTAL")
        self.assertEqual(adjusted["counts"]["coverage"][
            "inherited_published_required_season_source_rows"], 1)

    def test_03_remaining_independent_research_error_fails(self):
        proof = self._prove()
        report = {
            "status": "FAIL", "errors": [
                "research package declares required completed-season cutoff 1971-1972 "
                "but contains zero competitive target-school rows for that season",
                "UNKNOWN site was not researched",
            ], "warnings": [],
            "counts": {"coverage": {
                "required_completed_season_cutoff": "1971-1972",
                "required_season_rows": 0,
            }},
        }
        adjusted = reconcile_stage4_research_report(report, proof)
        self.assertEqual(adjusted["status"], "FAIL")
        self.assertEqual(adjusted["errors"], ["UNKNOWN site was not researched"])

    def test_04_ordinary_new_school_still_requires_cutoff_game(self):
        notes = (
            "- Primary-source historical results cutoff: 1969-1970\n"
            "- Required completed-season cutoff: 1971-1972\n"
        )
        report = _research_coverage_report(notes, self._rows())
        self.assertIn(
            "research package declares required completed-season cutoff 1971-1972 "
            "but contains zero competitive target-school rows for that season",
            report["errors"],
        )

    def test_05_wrong_or_absent_immutable_base_rejected(self):
        for base in ("0" * 40, "", "not-a-sha"):
            with self.subTest(base=base), self.assertRaises(
                ExpansionStage4CoverageError
            ):
                self._prove(base=base)

    def test_06_wrong_school_rejected(self):
        with self.assertRaises(ExpansionStage4CoverageError):
            self._prove(school="not-legacy")

    def test_07_unpublished_or_absent_final_season_rejected(self):
        for cutoff in ("1969-1970", "1972-1973", "bad"):
            with self.subTest(cutoff=cutoff), self.assertRaises(
                ExpansionStage4CoverageError
            ):
                self._prove(cutoff=cutoff)

    def test_08_rejects_published_season_in_supplement(self):
        rows = self._rows() + [fixture.source_row("EXP-3", "1970-1971")]
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "inherited published history"
        ):
            self._prove(rows=rows)

    def test_09_rejects_inherited_id_reused_with_changed_content(self):
        rows = self._rows()
        rows[0]["source_game_id"] = "BASE-1"
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "non-identical inherited source"
        ):
            self._prove(rows=rows)

    def test_10_rejects_inconsistent_reference_vs_program_scope(self):
        path = self.repo / "data/reference/program-top-level-scope.csv"
        fixture.write_csv(path, ["school", "top_level_scope"], [
            {"school": "Legacy University", "top_level_scope": "1969-70+"}
        ])
        self.baseline._recommit_baseline()
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "disagree"
        ):
            self._prove()

    def test_11_rejects_completed_season_missing_from_inherited_source(self):
        path = self.repo / "schools/legacy/source-games.csv"
        rows = [row for row in self._read_table(path)
                if row["season_label"] != "1971-1972"]
        self._write_table(path, fixture.SOURCE_FIELDS, rows)
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "inherited source package has no"
        ):
            self._prove()

    def test_12_rejects_completed_season_missing_from_published_canonical(self):
        path = self.repo / "data/canonical/games.csv"
        rows = [row for row in self._read_table(path)
                if row["season_label"] != "1971-1972"]
        self._write_table(path, fixture.CANONICAL_FIELDS, rows)
        with self.assertRaisesRegex(
            ExpansionStage4CoverageError, "canonical population has no"
        ):
            self._prove()

    def test_13_rejects_missing_or_forged_cutoff_claim(self):
        proof = self._prove()
        for report in (
            {"status": "FAIL", "errors": [], "warnings": [],
             "counts": {"coverage": {
                 "required_completed_season_cutoff": "1971-1972",
                 "required_season_rows": 0}}},
            {"status": "FAIL", "errors": ["wrong"], "warnings": [],
             "counts": {"coverage": {
                 "required_completed_season_cutoff": "1971-1972",
                 "required_season_rows": 0}}},
            {"status": "FAIL", "errors": ["wrong"], "warnings": [],
             "counts": {"coverage": {
                 "required_completed_season_cutoff": "1970-1971",
                 "required_season_rows": 0}}},
        ):
            with self.assertRaises(ExpansionStage4CoverageError):
                reconcile_stage4_research_report(report, proof)

    def test_14_duplicates_and_wrong_source_school_rejected(self):
        dup = self._rows()
        dup[1]["source_game_id"] = dup[0]["source_game_id"]
        with self.assertRaises(ExpansionStage4CoverageError):
            self._prove(rows=dup)
        bad = self._rows()
        bad[0]["source_program_key"] = "another-school"
        with self.assertRaises(ExpansionStage4CoverageError):
            self._prove(rows=bad)

    def test_15_baseline_fingerprints_remain_unchanged_by_proof(self):
        before = fixture.git(self.repo, "status", "--porcelain")
        proof = self._prove()
        self.assertEqual(before, fixture.git(self.repo, "status", "--porcelain"))
        self.assertEqual(proof["publication_mutation"], False)
        self.assertTrue(proof["baseline_program_row_sha256"])
        self.assertTrue(proof["baseline_scope_row_sha256"])



class Stage4ExpansionCloseoutIntegrationTests(unittest.TestCase):
    """Stage 4 wiring: only verified immutable checkpoint mode may clear one error."""

    @staticmethod
    def _parent(path: Path, *, expansion: bool, bad_manifest_base: bool = False):
        import io
        import zipfile
        import test_research_stage4_closeout as stage4_fixture
        import research_stage4_closeout as stage4
        stage4_fixture.make_parent(path, ("G1",))
        with zipfile.ZipFile(path) as archive:
            members = {name: archive.read(name) for name in archive.namelist()}
        status = json.loads(members["stage3b-status.json"])
        manifest = json.loads(members["checkpoint-manifest.json"])
        if expansion:
            status["workflow_kind"] = "ALL_HISTORY_EXPANSION"
            status["required_completed_season_cutoff"] = "2001-2002"
        if bad_manifest_base:
            manifest["research_base_sha"] = "b" * 40
        members["stage3b-status.json"] = (
            json.dumps(status, sort_keys=True) + "\n"
        ).encode("utf-8")
        for entry in manifest["files"]:
            if entry["name"] == "stage3b-status.json":
                entry["sha256"] = stage4.sha256_bytes(
                    members["stage3b-status.json"]
                )
                entry["bytes"] = len(members["stage3b-status.json"])
        members["checkpoint-manifest.json"] = (
            json.dumps(manifest, sort_keys=True) + "\n"
        ).encode("utf-8")
        stage4.write_deterministic_zip(path, members)

    @staticmethod
    def _failed_report(package, *, school_key, expected_sha256=""):
        import test_research_stage4_closeout as stage4_fixture
        report = stage4_fixture.fake_report(
            package, school_key=school_key, expected_sha256=expected_sha256
        )
        report["status"] = "FAIL"
        report["errors"] = [
            "research package declares required completed-season cutoff 2001-2002 "
            "but contains zero competitive target-school rows for that season"
        ]
        report["counts"]["coverage"] = {
            "required_completed_season_cutoff": "2001-2002",
            "required_season_rows": 0,
        }
        return report

    @staticmethod
    def _proof():
        return {
            "status": "PASS",
            "workflow_kind": "ALL_HISTORY_EXPANSION",
            "required_completed_season_cutoff": "2001-2002",
            "research_base_sha": "a" * 40,
            "inherited_required_season_source_rows": 2,
            "inherited_required_season_published_canonical_rows": 2,
        }

    def test_16_verified_expansion_parent_preserves_proof_in_closeout(self):
        import test_research_stage4_closeout as stage4_fixture
        import research_stage4_closeout as stage4
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            package = root / "package"
            stage4_fixture.make_package(package)
            parent = root / "parent.zip"
            self._parent(parent, expansion=True)
            with patch.object(stage4, "research_portfolio_report",
                              side_effect=self._failed_report), patch.object(
                                  stage4, "prove_expansion_stage4_coverage",
                                  return_value=self._proof(),
                              ) as proof_mock:
                status = stage4.closeout(
                    "test", package, parent, "c" * 40, root / "output"
                )
            self.assertEqual(
                status["status"], "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY"
            )
            self.assertEqual(status["workflow_kind"], "ALL_HISTORY_EXPANSION")
            self.assertEqual(status["expansion_coverage_proof"], "PASS")
            proof_mock.assert_called_once()
            with zipfile.ZipFile(root / "output" / "test-stage4-complete-checkpoint.zip") as z:
                self.assertIn("stage4-expansion-coverage-proof.json",
                              z.namelist())

    def test_17_package_notes_cannot_claim_expansion_mode(self):
        import test_research_stage4_closeout as stage4_fixture
        import research_stage4_closeout as stage4
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            package = root / "package"
            stage4_fixture.make_package(package)
            (package / "source-notes.md").write_text(
                "ALL_HISTORY_EXPANSION\n", encoding="utf-8"
            )
            parent = root / "parent.zip"
            self._parent(parent, expansion=False)
            with patch.object(stage4, "research_portfolio_report",
                              side_effect=self._failed_report), patch.object(
                                  stage4, "prove_expansion_stage4_coverage",
                                  side_effect=AssertionError("not authorized"),
                              ):
                with self.assertRaisesRegex(ValueError, "research acceptance failed"):
                    stage4.closeout(
                        "test", package, parent, "c" * 40, root / "output"
                    )

    def test_18_mismatched_parent_manifest_base_cannot_claim_exception(self):
        import test_research_stage4_closeout as stage4_fixture
        import research_stage4_closeout as stage4
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            package = root / "package"
            stage4_fixture.make_package(package)
            parent = root / "parent.zip"
            self._parent(parent, expansion=True, bad_manifest_base=True)
            with patch.object(stage4, "research_portfolio_report",
                              side_effect=self._failed_report), patch.object(
                                  stage4, "prove_expansion_stage4_coverage",
                                  side_effect=AssertionError("must not be called"),
                              ):
                with self.assertRaisesRegex(
                    ValueError, "research_base_sha/manifest mismatch"
                ):
                    stage4.closeout(
                        "test", package, parent, "c" * 40, root / "output"
                    )



if __name__ == "__main__":
    unittest.main()
