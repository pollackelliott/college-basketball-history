import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from correction_lifecycle import source_game_diff, validate_correction_candidate  # noqa: E402
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