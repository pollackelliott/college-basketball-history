import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from correction_lifecycle import source_game_diff, validate_correction_candidate  # noqa: E402
import onboarding_plan  # noqa: E402
from implementation_site_gate import _correction_source_validation_scope  # noqa: E402


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


FIELDS = [
    "source_game_id",
    "source_program_key",
    "source_era",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_key",
    "normalized_opponent_name",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "source_site_candidate",
    "curated_site_type",
    "source_venue_name",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "source_round",
    "curated_game_type",
    "curated_postseason_round",
    "source_page",
    "raw_text",
    "normalization_status",
    "administrative_status",
    "administrative_note",
    "notes",
    "site_research_status",
    "site_research_basis",
]


def row(source_id, **overrides):
    value = {field: "" for field in FIELDS}
    value.update(
        {
            "source_game_id": source_id,
            "source_program_key": "example",
            "season_label": "2025-2026",
            "game_date": "2026-01-01",
            "source_opponent_label": "Opponent",
            "normalized_opponent_key": "opponent",
            "normalized_opponent_name": "Opponent",
            "team_score": "70",
            "opponent_score": "60",
            "played_result": "W",
            "overtime_periods": "0",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "source_venue_name": "Example Arena",
            "curated_venue_name": "Example Arena",
            "city": "Example City",
            "state": "EX",
            "curated_game_type": "REGULAR_SEASON",
            "raw_text": "Opponent W 70-60",
        }
    )
    value.update(overrides)
    return value


def csv_bytes(rows):
    import io

    handle = io.StringIO(newline="")
    writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return handle.getvalue().encode()


class CorrectionDiffTests(unittest.TestCase):
    def test_exact_source_diff_reports_add_and_field_patch(self):
        before = [row("G1")]
        after = [
            row("G1", curated_site_type="OPPONENT_HOME"),
            row("G2", game_date="2026-01-02"),
        ]
        diff = source_game_diff(csv_bytes(before), csv_bytes(after))
        self.assertEqual(diff["added_count"], 1)
        self.assertEqual(diff["modified_count"], 1)
        self.assertEqual(diff["added"][0]["source_game_id"], "G2")
        self.assertEqual(
            diff["modified"][0]["fields"]["curated_site_type"],
            {"before": "SOURCE_PROGRAM_HOME", "after": "OPPONENT_HOME"},
        )

    def test_source_deletion_is_not_supported(self):
        with self.assertRaisesRegex(Exception, "does not support deleting"):
            source_game_diff(csv_bytes([row("G1")]), csv_bytes([]))

    def test_scoped_acceptance_ignores_unchanged_legacy_debt(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            legacy = row(
                "OLD",
                curated_site_type="OPPONENT_HOME",
                source_venue_name="Old Gym",
                curated_venue_name="",
                city="",
                state="",
            )
            changed = row("NEW")
            write_csv(root / "source-games.csv", FIELDS, [legacy, changed])
            write_csv(
                root / "opponents.csv",
                ["source_program_key", "source_opponent_label", "canonical_opponent_key"],
                [{
                    "source_program_key": "example",
                    "source_opponent_label": "Opponent",
                    "canonical_opponent_key": "opponent",
                }],
            )
            write_csv(
                root / "venues.csv",
                [
                    "source_program_key",
                    "venue_key",
                    "venue_id",
                    "canonical_name",
                    "aliases",
                    "city",
                    "state",
                    "relationship_type",
                    "relationship_start",
                    "relationship_end",
                ],
                [{
                    "source_program_key": "example",
                    "venue_key": "example-arena",
                    "venue_id": "VEN-000001",
                    "canonical_name": "Example Arena",
                    "aliases": "",
                    "city": "Example City",
                    "state": "EX",
                    "relationship_type": "PRIMARY_HOME",
                    "relationship_start": "2020-01-01",
                    "relationship_end": "",
                }],
            )
            report = validate_correction_candidate(
                root, school_key="example", changed_source_game_ids=["NEW"]
            )
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["changed_source_games"], 1)


class CorrectionStage2LegacyPackageScopeTests(unittest.TestCase):
    def git(self, repo, *args):
        return subprocess.check_output(
            ["git", *args],
            cwd=repo,
            text=True,
            stderr=subprocess.STDOUT,
        ).strip()

    def write_package(self, repo, rows):
        school = repo / "schools" / "example"
        write_csv(school / "source-games.csv", FIELDS, rows)
        write_csv(
            school / "opponents.csv",
            [
                "source_program_key",
                "source_opponent_label",
                "canonical_opponent_key",
            ],
            [{
                "source_program_key": "example",
                "source_opponent_label": "Opponent",
                "canonical_opponent_key": "opponent",
            }],
        )
        write_csv(
            school / "venues.csv",
            [
                "source_program_key",
                "venue_key",
                "venue_id",
                "canonical_name",
                "aliases",
                "city",
                "state",
                "relationship_type",
                "relationship_start",
                "relationship_end",
            ],
            [{
                "source_program_key": "example",
                "venue_key": "example-arena",
                "venue_id": "VEN-000001",
                "canonical_name": "Example Arena",
                "aliases": "",
                "city": "Example City",
                "state": "EX",
                "relationship_type": "PRIMARY_HOME",
                "relationship_start": "2020-01-01",
                "relationship_end": "",
            }],
        )
        write_csv(
            school / "conferences.csv",
            ["source_program_key", "conference_key", "start_season", "end_season"],
            [],
        )
        (school / "notes.md").write_text("fixture\n", encoding="utf-8")
        (school / "source-notes.md").write_text("fixture\n", encoding="utf-8")

    def validate(self, repo):
        with (
            patch.object(onboarding_plan, "current_d1_opponent_key_errors", return_value=[]),
            patch.object(onboarding_plan, "historical_opponent_display_conflicts", return_value={}),
            patch.object(onboarding_plan, "history_scope_errors", return_value=[]),
            patch.object(onboarding_plan, "history_errors", return_value=[]),
        ):
            return onboarding_plan.validate_package(repo, "example")

    def make_repo(self, root):
        self.git(root, "init")
        self.git(root, "config", "user.email", "fixture@example.com")
        self.git(root, "config", "user.name", "Fixture")
        (root / "data/reference").mkdir(parents=True)
        write_csv(
            root / "data/reference/programs.csv",
            ["program_key"],
            [{"program_key": "example"}],
        )
        write_csv(
            root / "data/reference/conferences.csv",
            ["conference_key"],
            [],
        )
        legacy = row(
            "OLD",
            season_label="1922-1923",
            game_date="1923-01-06",
            played_result="L",
            team_score="15",
            opponent_score="32",
            curated_site_type="OPPONENT_HOME",
            source_venue_name="Old Armory",
            curated_venue_name="Old Armory",
            city="State College",
            state="PA",
        )
        self.write_package(root, [legacy])
        self.git(root, "add", "schools/example", "data/reference")
        self.git(root, "commit", "-m", "published baseline")
        return self.git(root, "rev-parse", "HEAD"), legacy

    def write_manifest(self, root, base_sha, correction_ids):
        onboard = root / ".onboarding" / "example"
        onboard.mkdir(parents=True, exist_ok=True)
        (onboard / "integration-freeze.json").write_text(
            json.dumps(
                {
                    "workflow_kind": "POST_PUBLICATION_CORRECTION",
                    "status": "INTEGRATION_FROZEN",
                    "school_key": "example",
                    "research_base_sha": base_sha,
                    "correction_source_game_ids": correction_ids,
                }
            ),
            encoding="utf-8",
        )

    def test_unchanged_published_missing_venue_is_warning_only_for_correction(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_sha, legacy = self.make_repo(root)
            changed = row("NEW", curated_venue_name="Example Arena")
            self.write_package(root, [legacy, changed])
            self.write_manifest(root, base_sha, ["NEW"])

            report = self.validate(root)

            self.assertEqual(report["errors"], [])
            self.assertTrue(
                any(
                    "OLD: curated venue 'Old Armory' absent from venues.csv" in warning
                    and "unchanged published legacy debt outside this correction" in warning
                    for warning in report["warnings"]
                )
            )
            self.assertEqual(
                report["counts"]["correction_unchanged_published_rows"],
                1,
            )

    def test_correction_or_modified_legacy_missing_venue_still_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base_sha, legacy = self.make_repo(root)
            modified_legacy = dict(legacy)
            modified_legacy["curated_venue_name"] = "Changed Armory"
            correction = row("NEW", curated_venue_name="Missing Correction Arena")
            self.write_package(root, [modified_legacy, correction])
            self.write_manifest(root, base_sha, ["NEW"])

            report = self.validate(root)

            self.assertIn(
                "OLD: curated venue 'Changed Armory' absent from venues.csv",
                report["errors"],
            )
            self.assertIn(
                "NEW: curated venue 'Missing Correction Arena' absent from venues.csv",
                report["errors"],
            )
            self.assertEqual(
                report["counts"]["correction_unchanged_published_rows"],
                0,
            )

    def test_standard_workflow_missing_venue_still_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _, legacy = self.make_repo(root)
            self.write_package(root, [legacy])

            report = self.validate(root)

            self.assertIn(
                "OLD: curated venue 'Old Armory' absent from venues.csv",
                report["errors"],
            )
            self.assertEqual(
                report["counts"]["correction_unchanged_published_rows"],
                0,
            )


class CorrectionStage2AssertionDriftScopeTests(unittest.TestCase):
    semantic_fields = [
        "season_label",
        "game_date",
        "team_score",
        "opponent_score",
        "played_result",
        "overtime_periods",
        "curated_site_type",
        "curated_venue_name",
        "city",
        "state",
        "event_or_tournament",
        "curated_game_type",
        "curated_postseason_round",
        "source_opponent_label",
        "raw_text",
    ]

    def snapshot(self, rows):
        return {
            "schema_version": 1,
            "fields": list(self.semantic_fields),
            "rows": {
                item["source_game_id"]: {
                    field: item.get(field, "")
                    for field in self.semantic_fields
                }
                for item in rows
            },
        }

    def guard(self, snapshot):
        return {
            "schema_version": 1,
            "snapshot_sha256": onboarding_plan.sha256_text(
                onboarding_plan.canonical_json(snapshot)
            ),
            "snapshot": snapshot,
        }

    def write_manifest(self, repo, before, after, correction_ids):
        pre = self.snapshot(before)
        post = self.snapshot(after)
        onboard = repo / ".onboarding" / "example"
        onboard.mkdir(parents=True, exist_ok=True)
        (onboard / "integration-freeze.json").write_text(
            json.dumps(
                {
                    "workflow_kind": "POST_PUBLICATION_CORRECTION",
                    "status": "INTEGRATION_FROZEN",
                    "school_key": "example",
                    "research_base_sha": "a" * 40,
                    "correction_source_game_ids": correction_ids,
                    "pre_correction_source_semantic_guard": self.guard(pre),
                    "source_game_semantic_guard": self.guard(post),
                }
            ),
            encoding="utf-8",
        )

    def issues(self, repo, sources, assertions):
        by_source = {
            ("example", item["source_game_id"]): [item]
            for item in assertions
        }
        return onboarding_plan._source_assertion_sync_issues(
            repo,
            "example",
            sources,
            by_source,
        )

    def test_exact_27_row_site_correction_drift_reaches_reconciliation(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            before = [
                row(f"ND-STG1-{index:05d}")
                for index in range(1, 28)
            ]
            after = []
            for index, item in enumerate(before):
                updated = dict(item)
                updated["curated_site_type"] = (
                    "NEUTRAL" if index < 6 else "OPPONENT_HOME"
                )
                after.append(updated)

            ids = [item["source_game_id"] for item in after]
            self.write_manifest(repo, before, after, ids)
            errors, warnings = self.issues(repo, after, before)

            self.assertEqual(errors, [])
            self.assertEqual(len(warnings), 27)
            self.assertEqual(
                sum("curated_site_type" in warning for warning in warnings),
                27,
            )
            self.assertEqual(
                sum(item["curated_site_type"] == "NEUTRAL" for item in after),
                6,
            )
            self.assertEqual(
                sum(item["curated_site_type"] == "OPPONENT_HOME" for item in after),
                21,
            )
            self.assertTrue(
                all(
                    "authorized correction delta pending sealed reconciliation"
                    in warning
                    for warning in warnings
                )
            )

    def test_standard_workflow_assertion_drift_still_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            before = row("G1")
            after = row("G1", curated_site_type="OPPONENT_HOME")

            errors, warnings = self.issues(repo, [after], [before])

            self.assertEqual(warnings, [])
            self.assertEqual(
                errors,
                ["G1: global assertion differs in curated_site_type"],
            )

    def test_out_of_scope_correction_assertion_drift_still_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            correction_before = row("C1")
            correction_after = row("C1", curated_site_type="OPPONENT_HOME")
            other_before = row("OTHER")
            other_after = row("OTHER", curated_site_type="NEUTRAL")
            self.write_manifest(
                repo,
                [correction_before, other_before],
                [correction_after, other_after],
                ["C1"],
            )

            errors, warnings = self.issues(
                repo,
                [correction_after, other_after],
                [correction_before, other_before],
            )

            self.assertEqual(len(warnings), 1)
            self.assertEqual(
                errors,
                ["OTHER: global assertion differs in curated_site_type"],
            )

    def test_wrong_original_assertion_value_still_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            before = row("G1")
            after = row("G1", curated_site_type="OPPONENT_HOME")
            wrong_assertion = row("G1", curated_site_type="NEUTRAL")
            self.write_manifest(repo, [before], [after], ["G1"])

            errors, warnings = self.issues(
                repo,
                [after],
                [wrong_assertion],
            )

            self.assertEqual(warnings, [])
            self.assertEqual(
                errors,
                ["G1: global assertion differs in curated_site_type"],
            )

    def test_extra_assertion_drift_field_not_in_correction_delta_still_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            before = row("G1")
            after = row("G1", curated_site_type="OPPONENT_HOME")
            assertion = dict(before)
            assertion["raw_text"] = "unrelated global assertion drift"
            self.write_manifest(repo, [before], [after], ["G1"])

            errors, warnings = self.issues(repo, [after], [assertion])

            self.assertEqual(warnings, [])
            self.assertEqual(
                errors,
                ["G1: global assertion differs in curated_site_type, raw_text"],
            )

    def test_staged_source_must_match_frozen_post_correction_snapshot(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            before = row("G1")
            frozen = row("G1", curated_site_type="OPPONENT_HOME")
            drifted_source = row("G1", curated_site_type="NEUTRAL")
            self.write_manifest(repo, [before], [frozen], ["G1"])

            errors, warnings = self.issues(
                repo,
                [drifted_source],
                [before],
            )

            self.assertEqual(warnings, [])
            self.assertEqual(
                errors,
                ["G1: global assertion differs in curated_site_type"],
            )

    def test_multiple_global_assertions_still_block_in_correction_mode(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            before = row("G1")
            after = row("G1", curated_site_type="OPPONENT_HOME")
            self.write_manifest(repo, [before], [after], ["G1"])
            assertions = {
                ("example", "G1"): [dict(before), dict(before)],
            }

            errors, warnings = onboarding_plan._source_assertion_sync_issues(
                repo,
                "example",
                [after],
                assertions,
            )

            self.assertEqual(warnings, [])
            self.assertEqual(errors, ["G1: multiple global assertions exist"])

    def test_untrusted_correction_snapshot_hash_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            before = row("G1")
            after = row("G1", curated_site_type="OPPONENT_HOME")
            self.write_manifest(repo, [before], [after], ["G1"])
            manifest_path = repo / ".onboarding/example/integration-freeze.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["source_game_semantic_guard"]["snapshot_sha256"] = "bad"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

            with self.assertRaisesRegex(
                onboarding_plan.WorkflowError,
                "snapshot hash mismatch",
            ):
                self.issues(repo, [after], [before])


class CorrectionSiteScopeTests(unittest.TestCase):
    def test_standard_manifest_keeps_full_source_scope(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            rows = [row("A"), row("B")]
            scoped, meta = _correction_source_validation_scope(repo, "example", rows)
            self.assertEqual([r["source_game_id"] for r in scoped], ["A", "B"])
            self.assertEqual(meta["mode"], "FULL_SOURCE_PACKAGE")

    def test_correction_manifest_scopes_legacy_source_debt(self):
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            onboard = repo / ".onboarding" / "example"
            onboard.mkdir(parents=True)
            baseline_a = row("A")
            baseline_b = row("B")
            fields = [
                "season_label",
                "game_date",
                "team_score",
                "opponent_score",
                "played_result",
                "overtime_periods",
                "curated_site_type",
                "curated_venue_name",
                "city",
                "state",
                "event_or_tournament",
                "curated_game_type",
                "curated_postseason_round",
                "source_opponent_label",
                "raw_text",
            ]
            snapshot = {
                "schema_version": 1,
                "fields": fields,
                "rows": {
                    r["source_game_id"]: {f: r.get(f, "") for f in fields}
                    for r in [baseline_a, baseline_b]
                },
            }
            (onboard / "integration-freeze.json").write_text(
                json.dumps(
                    {
                        "workflow_kind": "POST_PUBLICATION_CORRECTION",
                        "correction_source_game_ids": ["B"],
                        "pre_correction_source_semantic_guard": {"snapshot": snapshot},
                    }
                ),
                encoding="utf-8",
            )
            current = [baseline_a, row("B", curated_site_type="OPPONENT_HOME")]
            scoped, meta = _correction_source_validation_scope(
                repo, "example", current
            )
            self.assertEqual([r["source_game_id"] for r in scoped], ["B"])
            self.assertEqual(meta["mode"], "CORRECTION_DELTA")
            self.assertEqual(meta["scoped_source_games"], 1)


if __name__ == "__main__":
    unittest.main()