"""Integration regression: correction authority must survive disposable copies."""

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import onboard_school  # noqa: E402
import onboarding_hardening  # noqa: E402
from implementation_site_gate import _correction_source_validation_scope  # noqa: E402
from integration_freeze_guard import SEMANTIC_SOURCE_GAME_FIELDS, semantic_snapshot_sha256  # noqa: E402
from site_completeness import source_site_completeness_report  # noqa: E402

FIELDS = list(dict.fromkeys(["source_game_id", "source_program_key",
    "normalized_opponent_key", "site_research_status", "site_research_basis",
    *SEMANTIC_SOURCE_GAME_FIELDS]))


def game(game_id, **changes):
    result = dict.fromkeys(FIELDS, "")
    result.update(source_game_id=game_id, source_program_key="example",
        normalized_opponent_key="opponent", season_label="2025-2026",
        game_date="2026-01-01", played_result="W", team_score="70",
        opponent_score="60", curated_site_type="SOURCE_PROGRAM_HOME",
        curated_venue_name="Example Arena", city="Example City", state="EX",
        curated_game_type="REGULAR_SEASON", raw_text="Opponent W 70-60")
    result.update(changes)
    return result


def write_games(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def freeze_guard(rows):
    snapshot = {"schema_version": 1, "fields": list(SEMANTIC_SOURCE_GAME_FIELDS),
        "rows": {r["source_game_id"]:
            {f: r.get(f, "") for f in SEMANTIC_SOURCE_GAME_FIELDS} for r in rows}}
    return {"schema_version": 1, "snapshot_sha256": semantic_snapshot_sha256(snapshot),
        "snapshot": snapshot}


class CorrectionRehearsalCopyTests(unittest.TestCase):
    def fixture(self, repo):
        before = [game("LEGACY", curated_venue_name="", city="", state=""),
            game("CORRECTION"), game("SAFE")]
        after = [dict(r) for r in before]
        after[1]["curated_site_type"] = "OPPONENT_HOME"
        source = repo / "schools/example/source-games.csv"
        write_games(source, after)
        manifest = {"schema_version": 2, "workflow_kind": "POST_PUBLICATION_CORRECTION",
            "status": "INTEGRATION_FROZEN", "school_key": "example",
            "correction_source_game_ids": ["CORRECTION"],
            "pre_correction_source_semantic_guard": freeze_guard(before),
            "source_game_semantic_guard": freeze_guard(after),
            "package_member_sha256": {"source-games.csv": onboard_school.file_sha(source)}}
        path = repo / ".onboarding/example/integration-freeze.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(manifest), encoding="utf-8")
        (path.parent / "other.json").write_text("ignored\n", encoding="utf-8")
        return path, after

    def scoped_gate(self, repo, rows):
        scoped, meta = _correction_source_validation_scope(repo, "example", rows)
        report = source_site_completeness_report(FIELDS, scoped)
        return meta["mode"], [r["source_game_id"] for r in scoped], report["errors"]

    def test_exact_manifest_transferred_but_not_other_onboarding_files(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / "original", Path(temp) / "copy"
            path, rows = self.fixture(src)
            onboard_school.copy_repository(src, dst, school_key="example")
            self.assertEqual((dst / ".onboarding/example/integration-freeze.json").read_bytes(),
                path.read_bytes())
            self.assertFalse((dst / ".onboarding/example/other.json").exists())
            self.assertEqual(self.scoped_gate(dst, rows),
                ("CORRECTION_DELTA", ["CORRECTION"], []))

    def test_modifying_unchanged_row_introduces_blocking_gap(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / "original", Path(temp) / "copy"
            _, rows = self.fixture(src)
            onboard_school.copy_repository(src, dst, school_key="example")
            rows[2].update(curated_venue_name="", city="", state="")
            mode, selected, errors = self.scoped_gate(dst, rows)
            self.assertEqual((mode, selected),
                ("CORRECTION_DELTA", ["CORRECTION", "SAFE"]))
            self.assertTrue(errors)

    def test_standard_workflow_stays_full_source(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / "original", Path(temp) / "copy"
            path, rows = self.fixture(src)
            manifest = json.loads(path.read_text())
            manifest["workflow_kind"] = "NEW_SCHOOL"
            path.write_text(json.dumps(manifest))
            onboard_school.copy_repository(src, dst, school_key="example")
            self.assertFalse((dst / ".onboarding").exists())
            mode, selected, errors = self.scoped_gate(dst, rows)
            self.assertEqual((mode, selected), ("FULL_SOURCE_PACKAGE",
                ["LEGACY", "CORRECTION", "SAFE"]))
            self.assertTrue(errors)

    def test_invalid_correction_authority_fails_closed(self):
        for variant in ("school", "status", "hash", "scope", "source"):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as temp:
                src, dst = Path(temp) / "original", Path(temp) / "copy"
                path, rows = self.fixture(src)
                manifest = json.loads(path.read_text())
                if variant == "school":
                    manifest["school_key"] = "wrong-school"
                elif variant == "status":
                    manifest["status"] = "PENDING"
                elif variant == "hash":
                    manifest["pre_correction_source_semantic_guard"]["snapshot_sha256"] = "bad"
                elif variant == "scope":
                    manifest["correction_source_game_ids"] = ["SAFE"]
                elif variant == "source":
                    rows[1]["curated_site_type"] = "NEUTRAL"
                    write_games(src / "schools/example/source-games.csv", rows)
                path.write_text(json.dumps(manifest))
                with self.assertRaises(onboard_school.WorkflowError):
                    onboard_school.copy_repository(src, dst, school_key="example")

    def test_rehearsal_and_sealed_apply_use_correction_scope(self):
        with tempfile.TemporaryDirectory() as temp:
            repo = Path(temp) / "repo"
            self.fixture(repo)
            plan, review = repo / "plan.json", repo / "review.csv"
            plan.write_text("{}\n")
            review.write_text("decision_id\n")
            observations = []

            def gate(checkout, school_key, changed, include_tests=True):
                with (checkout / "schools/example/source-games.csv").open(
                    encoding="utf-8", newline=""
                ) as stream:
                    rows = list(csv.DictReader(stream))
                mode, selected, errors = self.scoped_gate(checkout, rows)
                observations.append((mode, selected, include_tests))
                if errors:
                    raise AssertionError(errors)
                return {"site_completeness": "PASS"}

            with (
                patch("onboarding_hardening.onboard_school.ensure_package_checkpoint"),
                patch("onboarding_hardening.assert_no_unapproved_semantic_drift"),
                patch("onboarding_hardening.approve_plan",
                    return_value=({"school_key": "example"}, "approved-hash")),
                patch("onboarding_hardening.onboard_school.execute_approved_in_place",
                    return_value={}),
                patch("onboarding_hardening.onboard_school.run_gates", side_effect=gate),
            ):
                result = onboarding_hardening.rehearse_review(
                    repo, "example", plan_path=plan, review_path=review)
                self.assertEqual(result["gates"]["site_completeness"], "PASS")
            with (
                patch("onboard_school.ensure_clean_worktree"),
                patch("onboard_school.execute_approved_in_place", return_value={}),
                patch("onboard_school.run_gates", side_effect=gate),
                patch("onboard_school.git", return_value="maintenance-branch"),
            ):
                result = onboard_school.transactional_apply(repo,
                    {"school_key": "example", "approved_plan_hash": "approved-hash"},
                    repo / ".onboarding/example")
                self.assertEqual(result["copied_state_gates"]["site_completeness"], "PASS")
            self.assertEqual(observations, [
                ("CORRECTION_DELTA", ["CORRECTION"], True),
                ("CORRECTION_DELTA", ["CORRECTION"], True),
                ("CORRECTION_DELTA", ["CORRECTION"], False)])


if __name__ == "__main__":
    unittest.main()
