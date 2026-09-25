import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import WorkflowError  # noqa: E402
from stage1_reference_reconciliation import (  # noqa: E402
    conference_reconciliation_inventory,
    load_conference_reconciliation,
    register_conferences,
)


FIELDS = [
    "source_program_key",
    "start_season",
    "end_season",
    "conference_key",
    "conference_name",
    "membership_type",
    "ongoing",
    "basis",
    "notes",
]


def write_history(path: Path, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class Stage1ReferenceReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.history = self.root / "conferences.csv"
        self.original = [
            {
                "source_program_key": "cincinnati",
                "start_season": "1901-1902",
                "end_season": "1924-1925",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "No",
                "basis": "frozen",
                "notes": "",
            },
            {
                "source_program_key": "cincinnati",
                "start_season": "1925-1926",
                "end_season": "1935-1936",
                "conference_key": "ohio-athletic",
                "conference_name": "Ohio Athletic Conference",
                "membership_type": "primary",
                "ongoing": "No",
                "basis": "frozen",
                "notes": "",
            },
        ]
        write_history(self.history, self.original)

    def make_spec(self):
        import hashlib

        expected = hashlib.sha256(self.history.read_bytes()).hexdigest()
        replacement = [
            {
                "source_program_key": "cincinnati",
                "start_season": "1901-1902",
                "end_season": "1909-1910",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "No",
                "basis": "owner correction",
                "notes": "",
            },
            {
                "source_program_key": "cincinnati",
                "start_season": "1910-1911",
                "end_season": "1924-1925",
                "conference_key": "ohio-athletic",
                "conference_name": "Ohio Athletic Conference",
                "membership_type": "primary",
                "ongoing": "No",
                "basis": "owner correction",
                "notes": "",
            },
        ]
        spec = {
            "schema_version": 1,
            "school_key": "cincinnati",
            "owner_approval_basis": "Owner approved institutional chronology correction.",
            "expected_conferences_sha256": expected,
            "replacement_history": replacement,
            "registrations": [
                {
                    "conference_key": "ohio-athletic",
                    "conference_name": "Ohio Athletic Conference",
                    "tournament_label": "Ohio Athletic Conference",
                    "status": "historical",
                    "notes": "Registration does not imply that a tournament existed.",
                }
            ],
        }
        path = self.root / "spec.json"
        path.write_text(json.dumps(spec), encoding="utf-8")
        return path

    def test_owner_correction_replaces_history_and_registers_missing_identity(self):
        spec = self.make_spec()
        replacement, registrations, meta = load_conference_reconciliation(
            spec,
            school_key="cincinnati",
            conferences_path=self.history,
            local_fields=FIELDS,
        )
        self.assertEqual(replacement[0]["end_season"], "1909-1910")
        self.assertEqual(replacement[1]["start_season"], "1910-1911")
        self.assertEqual(len(registrations), 1)
        self.assertEqual(meta["replacement_row_count"], 2)

        global_rows = [
            {
                "conference_key": "independent",
                "conference_name": "Independent",
                "tournament_label": "",
                "status": "nonconference",
                "notes": "",
            }
        ]
        inventory = conference_reconciliation_inventory(
            replacement,
            global_rows,
            registrations,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            inventory["classification_counts"],
            {"NEW_GLOBAL_IDENTITY": 1, "REUSE_CURRENT_IDENTITY": 1},
        )

        global_rows, mappings = register_conferences(global_rows, registrations)
        self.assertEqual(len(global_rows), 2)
        self.assertEqual(mappings[0]["resolution"], "NEW_GLOBAL_IDENTITY")

    def test_missing_registration_is_blocking(self):
        spec = self.make_spec()
        replacement, _registrations, _meta = load_conference_reconciliation(
            spec,
            school_key="cincinnati",
            conferences_path=self.history,
            local_fields=FIELDS,
        )
        inventory = conference_reconciliation_inventory(
            replacement,
            [
                {
                    "conference_key": "independent",
                    "conference_name": "Independent",
                    "tournament_label": "",
                    "status": "nonconference",
                    "notes": "",
                }
            ],
            [],
        )
        self.assertEqual(inventory["blocker_count"], 1)
        self.assertEqual(
            inventory["blockers"][0]["issues"],
            ["MISSING_GLOBAL_CONFERENCE_REGISTRATION"],
        )

    def test_hash_mismatch_rejects_stale_correction(self):
        spec = self.make_spec()
        self.history.write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(
            WorkflowError,
            "frozen conferences.csv hash mismatch",
        ):
            load_conference_reconciliation(
                spec,
                school_key="cincinnati",
                conferences_path=self.history,
                local_fields=FIELDS,
            )


if __name__ == "__main__":
    unittest.main()
