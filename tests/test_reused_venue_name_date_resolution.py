import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import ingest_school

FIELDS = [
    "source_program_key","venue_key","venue_id","canonical_name","aliases",
    "city","state","venue_type","known_opened","known_closed","venue_date_precision",
    "games_currently_assigned","first_assigned_game","last_assigned_game",
    "relationship_type","relationship_start","relationship_end","relationship_date_precision",
    "site_rule","source_basis","notes",
]


def venue_row(key, vid, first, last):
    return {
        "source_program_key":"depaul","venue_key":key,"venue_id":vid,
        "canonical_name":"Charlotte Coliseum","aliases":"","city":"Charlotte","state":"NC",
        "venue_type":"arena","known_opened":"","known_closed":"","venue_date_precision":"",
        "games_currently_assigned":"1","first_assigned_game":first,"last_assigned_game":last,
        "relationship_type":"","relationship_start":"","relationship_end":"",
        "relationship_date_precision":"","site_rule":"","source_basis":"fixture","notes":"",
    }


class ReusedVenueNameDateResolutionTests(unittest.TestCase):
    def make_map(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "venues.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow(venue_row("charlotte-coliseum-1955","VEN-000040","1976-03-13","1976-03-13"))
            writer.writerow(venue_row("charlotte-coliseum-1988","VEN-000041","1991-12-07","1991-12-07"))
        globals_by_id = {
            "VEN-000040":{"venue_id":"VEN-000040","city":"Charlotte","state":"NC","opened":"1955","closed":""},
            "VEN-000041":{"venue_id":"VEN-000041","city":"Charlotte","state":"NC","opened":"1988","closed":"2005"},
        }
        return ingest_school.load_venue_metadata_map(path, globals_by_id)

    def test_1976_resolves_original(self):
        result = ingest_school.resolve_venue_metadata(
            {"source_game_id":"DEPRAW-01178","game_date":"1976-03-13","curated_venue_name":"Charlotte Coliseum"},
            self.make_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000040")
        self.assertEqual(result["venue_key"], "charlotte-coliseum-1955")

    def test_1991_resolves_new_building(self):
        result = ingest_school.resolve_venue_metadata(
            {"source_game_id":"DEPRAW-01659","game_date":"1991-12-07","curated_venue_name":"Charlotte Coliseum"},
            self.make_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000041")
        self.assertEqual(result["venue_key"], "charlotte-coliseum-1988")

    def test_undated_reused_name_without_season_stops(self):
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id":"UNDATED",
                    "game_date":"",
                    "season_label":"",
                    "curated_venue_name":"Charlotte Coliseum",
                },
                self.make_map(),
            )

    def test_ambiguous_exact_date_stops(self):
        with self.assertRaisesRegex(ValueError, "does not resolve exactly one candidate"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id":"OTHER",
                    "game_date":"1989-01-01",
                    "season_label":"1988-1989",
                    "curated_venue_name":"Charlotte Coliseum",
                },
                self.make_map(),
            )

    def make_msg_map(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "venues.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            old = venue_row(
                "madison-square-garden-1925",
                "VEN-000123",
                "1937-02-24",
                "1966-03-10",
            )
            old["canonical_name"] = "Madison Square Garden"
            new = venue_row(
                "madison-square-garden-1968",
                "VEN-000124",
                "1983-02-20",
                "2026-03-11",
            )
            new["canonical_name"] = "Madison Square Garden"
            writer.writerow(old)
            writer.writerow(new)
        globals_by_id = {
            "VEN-000123":{
                "venue_id":"VEN-000123",
                "city":"New York",
                "state":"NY",
                "opened":"1925",
                "closed":"1968",
            },
            "VEN-000124":{
                "venue_id":"VEN-000124",
                "city":"New York",
                "state":"NY",
                "opened":"1968-02-11",
                "closed":"",
            },
        }
        return ingest_school.load_venue_metadata_map(path, globals_by_id)

    def test_undated_1935_36_msg_resolves_msg_iii_by_season(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id":"DEPRAW-00201",
                "game_date":"",
                "season_label":"1935-1936",
                "curated_venue_name":"Madison Square Garden",
            },
            self.make_msg_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000123")

    def test_undated_1937_38_msg_resolves_msg_iii_by_season(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id":"DEPRAW-00235",
                "game_date":"",
                "season_label":"1937-1938",
                "curated_venue_name":"Madison Square Garden",
            },
            self.make_msg_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000123")

    def test_msg_transition_season_stops(self):
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id":"TRANSITION",
                    "game_date":"",
                    "season_label":"1967-1968",
                    "curated_venue_name":"Madison Square Garden",
                },
                self.make_msg_map(),
            )

if __name__ == "__main__":
    unittest.main()
