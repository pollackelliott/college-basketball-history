"""Exact-owner historical coverage publication is safe and idempotent."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from publish_historical_season_coverage import integrate_approved_coverage


class PublishHistoricalSeasonCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name)
        self.school = "example"
        self.season = "1919-20"
        self.notes = self.repo / "schools" / self.school / "source-notes.md"
        self.notes.parent.mkdir(parents=True)
        base = self.repo / "data" / "reference"
        base.mkdir(parents=True)
        self.csv = base / "historical-season-coverage.csv"
        self.csv.write_text(
            "program_key,season_label,official_wins,official_losses,official_games,"
            "documented_wins,documented_losses,documented_games,"
            "unidentified_wins,unidentified_losses,unidentified_games,"
            "source_label,owner_disposition,stage1_audit_sha256,public_note\n",
            encoding="utf-8",
        )
        self.case = {
            "school_key": self.school, "season": self.season,
            "parent_checkpoint_sha256": "c" * 64,
            "research_base_sha": "a" * 40,
            "owner_disposition": "https://github.com/example/history/issues/1",
            "institutional_record": {"wins": 6, "losses": 10, "games": 16},
            "identified_record": {"wins": 3, "losses": 7, "games": 10},
            "unidentified_record": {"wins": 3, "losses": 3, "games": 6},
        }
        (base / "early-aggregate-coverage-authorities.json").write_text(
            json.dumps({"authority_type": "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE",
                        "cases": [self.case]}), encoding="utf-8"
        )
        self.entry = {
            **self.case, "terminal_classification": "EARLY_HISTORY_AGGREGATE_RECONCILED_GAP",
            "audit_sha256": "d" * 64, "source_description": "Institutional record book",
        }
        self.write_notes()

    def write_notes(self):
        value = {"schema_version": 1, "coverage": [self.entry]}
        self.notes.write_text(
            "# Original source notes\n\n"
            "## Research-exhausted institutional aggregate coverage gap\n\n"
            "This describes season-level debt, not games.\n\n"
            + chr(96) * 3 + "json\n"
            + json.dumps(value, indent=2) + "\n" + chr(96) * 3
            + "\n\n## Other authoritative sources\n\nPreserved.\n",
            encoding="utf-8"
        )

    def read_rows(self):
        with self.csv.open(newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))

    def test_add_exact_season_note_and_repeat_idempotently(self):
        result = integrate_approved_coverage(self.repo, self.school)
        self.assertEqual(result["status"], "ADDED_VERIFIED_SEASON_COVERAGE")
        self.assertEqual(len(self.read_rows()), 1)
        self.assertEqual(self.read_rows()[0]["unidentified_games"], "6")
        self.assertEqual(self.read_rows()[0]["stage1_audit_sha256"], "d" * 64)
        self.assertEqual(integrate_approved_coverage(self.repo, self.school)["status"],
                         "EXACT_ALREADY_PRESENT")
        self.assertEqual(len(self.read_rows()), 1)

    def test_no_metadata_is_exact_noop(self):
        self.notes.unlink()
        self.assertEqual(integrate_approved_coverage(self.repo, self.school)["status"],
                         "NO_AGGREGATE_COVERAGE")
        self.assertEqual(self.read_rows(), [])

    def test_different_owner_disposition_cannot_publish(self):
        self.entry["owner_disposition"] = "https://github.com/example/history/issues/2"
        self.write_notes()
        with self.assertRaisesRegex(ValueError, "OWNER_AUTHORITY_MISMATCH"):
            integrate_approved_coverage(self.repo, self.school)

    def test_unapproved_school_cannot_publish(self):
        self.entry["school_key"] = "unapproved"
        self.write_notes()
        with self.assertRaisesRegex(ValueError, "SCHOOL_IDENTITY_MISMATCH"):
            integrate_approved_coverage(self.repo, self.school)

    def test_inferred_game_count_not_allocated(self):
        self.entry["unidentified_record"]["wins"] = 4
        self.write_notes()
        with self.assertRaisesRegex(ValueError, "RECORD_AUTHORITY_MISMATCH"):
            integrate_approved_coverage(self.repo, self.school)

    def test_reject_conflicting_existing_public_entry(self):
        self.csv.write_text(self.csv.read_text(encoding="utf-8")
                            + "example,1919-20,0,0,0,0,0,0,0,0,0,s,x,"
                            + "0" * 64 + ",\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "EXISTING_ROW_CONFLICT"):
            integrate_approved_coverage(self.repo, self.school)


if __name__ == "__main__":
    unittest.main()
