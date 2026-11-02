"""Read-only real-repository census plus controlled classification regression."""
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from canonical_partial_location_census import scan


class CanonicalPartialLocationCensusTests(unittest.TestCase):
    def test_census_classification_on_isolated_fixture(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def write(rel, fields, rows):
                target = root / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("w", newline="", encoding="utf-8") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
                    writer.writeheader()
                    writer.writerows(rows)
            write("data/canonical/games.csv",
                  ["canonical_game_id", "season_label", "game_date", "team_a_key", "team_b_key",
                   "site_type", "site_city", "site_state", "venue_id", "venue_key", "canonical_status"],
                  [
                      {"canonical_game_id": "A", "site_city": "Maui",
                       "site_type": "NEUTRAL", "team_a_key": "a", "team_b_key": "b"},
                      {"canonical_game_id": "B", "site_city": "Athens", "site_state": "GA"},
                      {"canonical_game_id": "C", "site_state": "HI", "site_type": "NEUTRAL"},
                      {"canonical_game_id": "D", "site_city": "Example City",
                       "site_type": "TEAM_A_HOME", "venue_id": "VEN-001"},
                  ])
            write("data/evidence/game-assertions.csv",
                  ["canonical_game_id", "source_program_key", "source_game_id",
                   "city", "state", "curated_site_type", "raw_text"],
                  [
                      {"canonical_game_id": "A", "source_program_key": "b",
                       "source_game_id": "B-1", "city": "Maui", "state": "HI",
                       "raw_text": "Maui, Hawai'i"},
                      {"canonical_game_id": "C", "source_program_key": "c",
                       "source_game_id": "C-1", "city": "", "state": "HI",
                       "raw_text": "Hawai'i"},
                  ])
            write("data/reference/venues.csv",
                  ["venue_id", "venue_key", "display_name", "city", "state"],
                  [{"venue_id": "VEN-001", "venue_key": "example",
                    "display_name": "Example", "city": "Example City", "state": "EX"}])
            result = scan(root)
            self.assertEqual(result["partial_canonical_count"], 3)
            self.assertEqual(result["by_evidence_classification"], {
                "ONLY_PARTIAL_OR_EMPTY_ASSERTIONS": 1,
                "REGISTERED_VENUE_GEO_AVAILABLE": 1,
                "SAME_CITY_COMPLETE_ASSERTION": 1,
            })
            self.assertEqual([x["canonical_game_id"] for x in result["records"]],
                             ["A", "C", "D"])

    def test_real_repository_exact_population_and_evidence(self):
        result = scan(ROOT)
        self.assertGreater(result["canonical_game_count"], 1000)
        self.assertEqual(result["partial_canonical_count"], len(result["records"]))
        self.assertEqual(sum(result["by_evidence_classification"].values()),
                         result["partial_canonical_count"])
        self.assertEqual(sum(result["by_site_type"].values()),
                         result["partial_canonical_count"])
        print("PARTIAL_CENSUS_SUMMARY=" + json.dumps({
            k: v for k, v in result.items() if k != "records"
        }, sort_keys=True, ensure_ascii=False), flush=True)
        for row in result["records"]:
            print("PARTIAL_CENSUS_ROW=" + json.dumps(row, sort_keys=True,
                                                     ensure_ascii=False, separators=(",", ":")),
                  flush=True)


if __name__ == "__main__":
    unittest.main()
