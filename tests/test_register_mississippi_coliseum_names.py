import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from register_mississippi_coliseum_names import (  # noqa: E402
    ALIAS,
    DISPLAY_NAME,
    VENUE_ID,
    register,
)


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


VENUE_FIELDS = [
    "venue_id",
    "venue_key",
    "display_name",
    "city",
    "state",
    "opened",
    "closed",
    "date_precision",
    "identity_status",
    "source_basis",
    "notes",
]
NAME_FIELDS = [
    "venue_id",
    "venue_name",
    "normalized_name",
    "name_type",
    "valid_from",
    "valid_to",
    "date_precision",
    "source_basis",
    "notes",
]


class MississippiColiseumNameRegistrationTests(unittest.TestCase):
    def make_repo(self, root: Path, *, venue_key="mississippi-coliseum"):
        write_csv(
            root / "data/reference/venues.csv",
            VENUE_FIELDS,
            [
                {
                    "venue_id": VENUE_ID,
                    "venue_key": venue_key,
                    "display_name": DISPLAY_NAME,
                    "city": "Jackson",
                    "state": "MS",
                    "opened": "1962",
                    "closed": "",
                    "date_precision": "YEAR",
                    "identity_status": "RESEARCHED_OFFICIAL",
                    "source_basis": "test",
                    "notes": "test",
                }
            ],
        )
        write_csv(root / "data/reference/venue-names.csv", NAME_FIELDS, [])

    def test_apply_registers_display_and_alias_and_validates(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)

            result = register(root, apply=True)

            self.assertEqual(result["added_rows"], 2)
            with (root / "data/reference/venue-names.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(len(rows), 2)
            by_name = {row["venue_name"]: row for row in rows}
            self.assertEqual(by_name[DISPLAY_NAME]["name_type"], "PROJECT_DISPLAY")
            self.assertEqual(by_name[ALIAS]["name_type"], "HISTORICAL_OR_ALIAS")

    def test_registration_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)

            register(root, apply=True)
            second = register(root, apply=True)

            self.assertEqual(second["added_rows"], 0)
            with (root / "data/reference/venue-names.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 2)

    def test_identity_drift_is_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, venue_key="wrong-key")

            with self.assertRaises(Exception):
                register(root, apply=True)


if __name__ == "__main__":
    unittest.main()
