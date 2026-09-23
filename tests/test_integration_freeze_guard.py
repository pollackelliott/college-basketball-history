import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from integration_freeze_guard import (  # noqa: E402
    assert_no_unapproved_semantic_drift,
    build_source_game_semantic_snapshot,
    semantic_drift_report,
    semantic_snapshot_sha256,
)
from onboarding_plan import WorkflowError  # noqa: E402


FIELDS = [
    "source_game_id",
    "source_program_key",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_key",
    "normalized_opponent_name",
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
    "raw_text",
]


def write_games(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def base_row() -> dict[str, str]:
    return {
        "source_game_id": "TEST-0001",
        "source_program_key": "test",
        "season_label": "1976-1977",
        "game_date": "1977-02-12",
        "source_opponent_label": "USC",
        "normalized_opponent_key": "usc-old",
        "normalized_opponent_name": "Southern California",
        "team_score": "72",
        "opponent_score": "55",
        "played_result": "W",
        "overtime_periods": "0",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_venue_name": "Example Arena",
        "city": "Example City",
        "state": "EX",
        "event_or_tournament": "",
        "curated_game_type": "REGULAR_SEASON",
        "curated_postseason_round": "",
        "raw_text": "F 12 USC W 72-55",
    }


class IntegrationFreezeGuardTests(unittest.TestCase):
    def make_repo(self, root: Path) -> tuple[Path, dict[str, str]]:
        row = base_row()
        source = root / "schools" / "test" / "source-games.csv"
        write_games(source, [row])
        snapshot = build_source_game_semantic_snapshot(source)
        manifest_dir = root / ".onboarding" / "test"
        manifest_dir.mkdir(parents=True)
        (manifest_dir / "integration-freeze.json").write_text(
            json.dumps(
                {
                    "schema_version": 2,
                    "school_key": "test",
                    "status": "INTEGRATION_FROZEN",
                    "integration_base_sha": "abc123",
                    "source_game_semantic_guard": {
                        "schema_version": 1,
                        "snapshot_sha256": semantic_snapshot_sha256(snapshot),
                        "snapshot": snapshot,
                    },
                }
            ),
            encoding="utf-8",
        )
        return source, row

    def test_representation_only_opponent_normalization_is_allowed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, row = self.make_repo(root)
            changed = dict(row)
            changed["normalized_opponent_key"] = "usc"
            changed["normalized_opponent_name"] = "USC"
            write_games(source, [changed])

            report = semantic_drift_report(root, "test")

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["changes"], [])

    def test_substantive_date_score_ot_and_site_drift_is_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, row = self.make_repo(root)
            changed = dict(row)
            changed["game_date"] = "1977-02-10"
            changed["team_score"] = "70"
            changed["overtime_periods"] = "1"
            changed["curated_site_type"] = "NEUTRAL"
            write_games(source, [changed])

            report = semantic_drift_report(root, "test")

            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(
                report["category_counts"],
                {"DATE": 1, "OVERTIME": 1, "SCORE": 1, "SITE_TYPE": 1},
            )
            with self.assertRaisesRegex(
                WorkflowError,
                "carry the proposed correction to Owner Gate 1",
            ):
                assert_no_unapproved_semantic_drift(root, "test")

    def test_frozen_raw_evidence_cannot_be_rewritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, row = self.make_repo(root)
            changed = dict(row)
            changed["raw_text"] = "F 10 USC W 72-55"
            write_games(source, [changed])

            report = semantic_drift_report(root, "test")

            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(
                report["category_counts"],
                {"FROZEN_SOURCE_EVIDENCE": 1},
            )

    def test_added_or_removed_source_rows_are_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source, row = self.make_repo(root)
            added = dict(row)
            added["source_game_id"] = "TEST-0002"
            write_games(source, [added])

            report = semantic_drift_report(root, "test")

            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(
                report["category_counts"],
                {"ROW_ADDED": 1, "ROW_REMOVED": 1},
            )

    def test_manifest_without_semantic_snapshot_is_not_accepted(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "schools" / "test" / "source-games.csv"
            write_games(source, [base_row()])
            manifest_dir = root / ".onboarding" / "test"
            manifest_dir.mkdir(parents=True)
            (manifest_dir / "integration-freeze.json").write_text(
                json.dumps({"schema_version": 1, "school_key": "test"}),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                WorkflowError,
                "predates the semantic-drift guard",
            ):
                semantic_drift_report(root, "test")


if __name__ == "__main__":
    unittest.main()
