import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from site_remediation_audit import VenueResolver  # noqa: E402


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


class VenueResolutionSafetyTests(unittest.TestCase):
    def test_known_name_with_conflicting_assertion_geography_does_not_resolve(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            write_csv(
                repo / "data/reference/venues.csv",
                ["venue_id", "venue_key", "display_name", "city", "state"],
                [{
                    "venue_id": "VEN-000001",
                    "venue_key": "example-arena",
                    "display_name": "Example Arena",
                    "city": "Alpha City",
                    "state": "AA",
                }],
            )
            write_csv(
                repo / "data/reference/venue-names.csv",
                ["venue_id", "venue_name", "normalized_name"],
                [{
                    "venue_id": "VEN-000001",
                    "venue_name": "Example Arena",
                    "normalized_name": "examplearena",
                }],
            )
            write_csv(
                repo / "schools/alpha/venues.csv",
                [
                    "source_program_key",
                    "venue_key",
                    "venue_id",
                    "canonical_name",
                    "aliases",
                    "city",
                    "state",
                ],
                [{
                    "source_program_key": "alpha",
                    "venue_key": "example-arena",
                    "venue_id": "VEN-000001",
                    "canonical_name": "Example Arena",
                    "aliases": "",
                    "city": "Alpha City",
                    "state": "AA",
                }],
            )
            resolver = VenueResolver(repo)
            venue_id, basis = resolver.resolve({
                "source_program_key": "alpha",
                "curated_venue_name": "Example Arena",
                "city": "Wrong City",
                "state": "ZZ",
            })
            self.assertEqual(venue_id, "")
            self.assertIn("conflicts with assertion location", basis)


if __name__ == "__main__":
    unittest.main()
