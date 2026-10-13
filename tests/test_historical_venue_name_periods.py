"""Audited physical-venue naming periods and date-aware website behavior."""
import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_site_data import official_venue_name_periods  # noqa: E402

INDEX = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
CSV_PATH = ROOT / "data/reference/venue-names.csv"
PERIODS_PATH = ROOT / "site/data/venue-name-periods.json"

EXPECTED = {
    "schema_version": 1,
    "venues": {
        "VEN-000052": [
            {"venue_name": "CU Events/Conference Center", "valid_from": "1979-08-08", "valid_to": "1990-09-19"},
            {"venue_name": "Coors Events Center", "valid_from": "1990-09-20", "valid_to": "2018-06-30"},
            {"venue_name": "CU Events Center", "valid_from": "2018-07-01", "valid_to": ""},
        ],
        "VEN-000096": [
            {"venue_name": "Carrier Dome", "valid_from": "1980-09-20", "valid_to": "2022-05-18"},
            {"venue_name": "JMA Wireless Dome", "valid_from": "2022-05-19", "valid_to": ""},
        ],
        "VEN-000196": [
            {"venue_name": "Assembly Hall", "valid_from": "1963-03-02", "valid_to": "2013-04-28"},
            {"venue_name": "State Farm Center", "valid_from": "2013-04-29", "valid_to": ""},
        ],
    },
}


class HistoricalVenueNamingTests(unittest.TestCase):
    def test_exact_periods_published_from_existing_reference(self):
        self.assertEqual(official_venue_name_periods(ROOT), EXPECTED)
        self.assertEqual(json.loads(PERIODS_PATH.read_text(encoding="utf-8")), EXPECTED)
        manifest = json.loads((ROOT / "site/data/manifest.json").read_text())
        self.assertEqual(manifest["files"]["venue_name_periods"], "venue-name-periods.json")
        with CSV_PATH.open(encoding="utf-8", newline="") as fp:
            rows = list(csv.DictReader(fp))
        official = [r for r in rows if r["name_type"] == "OFFICIAL_NAMING_PERIOD"]
        self.assertEqual(len(official), 7)
        self.assertEqual(
            {r["venue_id"] for r in official},
            {"VEN-000052", "VEN-000096", "VEN-000196"},
        )
        self.assertTrue(all(r["source_basis"].startswith("https://") for r in official))

    def test_reject_ambiguous_overlaps_and_unsupported_exact_dates(self):
        fields = [
            "venue_id", "venue_name", "normalized_name", "name_type",
            "valid_from", "valid_to", "date_precision", "source_basis", "notes",
        ]
        row = {
            "venue_id": "VEN-TEST", "venue_name": "Test Gym",
            "normalized_name": "testgym", "name_type": "OFFICIAL_NAMING_PERIOD",
            "valid_from": "1990-01-01", "valid_to": "2000-12-31",
            "date_precision": "EXACT", "source_basis": "Test official announcement",
            "notes": "",
        }

        def check(rows):
            with tempfile.TemporaryDirectory() as temp:
                path = Path(temp) / "data/reference/venue-names.csv"
                path.parent.mkdir(parents=True)
                with path.open("w", encoding="utf-8", newline="") as handle:
                    writer = csv.DictWriter(handle, fieldnames=fields)
                    writer.writeheader()
                    writer.writerows(rows)
                return official_venue_name_periods(Path(temp))

        with self.assertRaisesRegex(ValueError, "overlapping official"):
            check([row, dict(row, venue_name="Second Gym",
                             valid_from="2000-12-31", valid_to="")])
        with self.assertRaisesRegex(ValueError, "EXACT precision"):
            check([dict(row, date_precision="YEAR")])
        with self.assertRaisesRegex(ValueError, "invalid exact naming date"):
            check([dict(row, valid_from="1990-02-30")])
        with self.assertRaisesRegex(ValueError, "ends before start"):
            check([dict(row, valid_to="1989-12-31")])
        with self.assertRaisesRegex(ValueError, "expected exact ISO"):
            check([dict(row, valid_from="1990")])

    def test_frontend_uses_identity_dates_and_current_name_fallback(self):
        self.assertIn("game.venue_id, game.game_date, game.date_precision", INDEX)
        self.assertIn("periods[periods.length - 1].venue_name", INDEX)
        self.assertIn("venueOptionMatchesGame(state.venueQuery", INDEX)
        self.assertIn("(game) => game.venueId || game.venueKey", INDEX)
        if not shutil.which("node"):
            self.skipTest("Node is not installed; source/period validation still ran")

        def section(start, end):
            begin = INDEX.index("function " + start + "(")
            finish = INDEX.index("\nfunction " + end + "(", begin)
            return INDEX[begin:finish]

        source = [
            "const assert = require('node:assert/strict');",
            "const DB = {venueNamePeriods: " + json.dumps(EXPECTED["venues"]) + "};",
            "function canonicalWinnerKey(game) { return game.winner; }",
            section("historicalVenueName", "normalizeGame"),
            section("venueFilterValue", "locationFilterValue"),
            section("bucket", "miniPanel"),
            r"""
const old = {venueId:"VEN-000196",venueKey:"state-farm-center",
             venue:"Assembly Hall",location:"Champaign, IL",winner:"illinois"};
const modern = {...old, venue:"State Farm Center",winner:"opponent"};
const different = {venueId:"VEN-000186",venueKey:"simon-skjodt-assembly-hall",
                   venue:"Assembly Hall",location:"Bloomington, IN",winner:"illinois"};
const show = (id, when, precision="EXACT") =>
  historicalVenueName(id,when,precision,"Project fallback");

assert.equal(show("VEN-000196","1985-01-01"),"Assembly Hall");
assert.equal(show("VEN-000196","2013-04-28"),"Assembly Hall");
assert.equal(show("VEN-000196","2013-04-29"),"State Farm Center");
assert.equal(show("VEN-000196","2013","YEAR"),"State Farm Center");
assert.equal(show("VEN-000196",null,""),"State Farm Center");

assert.equal(show("VEN-000096","2020-01-01"),"Carrier Dome");
assert.equal(show("VEN-000096","2022-05-19"),"JMA Wireless Dome");
assert.equal(show("VEN-000096","2022","SEASON"),"JMA Wireless Dome");

assert.equal(show("VEN-000052","1985-01-01"),"CU Events/Conference Center");
assert.equal(show("VEN-000052","1995-01-01"),"Coors Events Center");
assert.equal(show("VEN-000052","2020-01-01"),"CU Events Center");
assert.equal(show("VEN-000052",null,""),"CU Events Center");

assert.equal(show("VEN-000186","2013-04-29"),"Project fallback");
assert.equal(show("VEN-999999",null,""),"Project fallback");

const opts = venueOptionsForGames([old,modern,different]);
assert.equal(venueOptionMatchesGame("State Farm Center",old,opts),true);
assert.equal(venueOptionMatchesGame("Assembly Hall",modern,opts),true);
assert.equal(venueOptionMatchesGame("State Farm Center",different,opts),false);
const summaries = bucket([old,modern],"illinois","opponent",aggregateVenueLabel,
  game => game.venueId || game.venueKey);
assert.equal(summaries.length,1);
assert.equal(summaries[0].games,2);
assert.equal(summaries[0].label,"Assembly Hall / State Farm Center");
""",
        ]
        result = subprocess.run(
            ["node", "-"], input="\n".join(source),
            text=True, capture_output=True, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
