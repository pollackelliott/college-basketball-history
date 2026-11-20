import csv
import io
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from all_history_expansion_display_successor_guard import (  # noqa: E402
    _opponent_representation_changes,
)


FIELDS = [
    "canonical_opponent_key",
    "canonical_opponent_name",
    "current_d1",
    "notes",
]


def csv_bytes(row):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    writer.writerow(row)
    return out.getvalue().encode("utf-8")


class ExpansionDisplaySuccessorCurrentD1Tests(unittest.TestCase):
    def base(self):
        return {
            "canonical_opponent_key": "example",
            "canonical_opponent_name": "Example",
            "current_d1": "",
            "notes": "unchanged",
        }

    def test_current_d1_only_change_is_representation_compatible(self):
        before = self.base()
        after = dict(before, current_d1="Yes")
        changes = _opponent_representation_changes(
            csv_bytes(before), csv_bytes(after)
        )
        self.assertIsNotNone(changes)
        self.assertEqual(len(changes), 1)

    def test_name_only_change_remains_representation_compatible(self):
        before = self.base()
        after = dict(before, canonical_opponent_name="Example University")
        changes = _opponent_representation_changes(
            csv_bytes(before), csv_bytes(after)
        )
        self.assertIsNotNone(changes)
        self.assertEqual(len(changes), 1)

    def test_invalid_current_d1_value_is_rejected(self):
        before = self.base()
        after = dict(before, current_d1="Maybe")
        self.assertIsNone(
            _opponent_representation_changes(csv_bytes(before), csv_bytes(after))
        )

    def test_unrelated_opponent_field_change_is_rejected(self):
        before = self.base()
        after = dict(before, notes="changed")
        self.assertIsNone(
            _opponent_representation_changes(csv_bytes(before), csv_bytes(after))
        )


if __name__ == "__main__":
    unittest.main()
