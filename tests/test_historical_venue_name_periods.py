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
        "VEN-000015": [
            {
                "venue_name": "Cowboys Stadium",
                "valid_from": "2009-05-13",
                "valid_to": "2013-07-24"
            },
            {
                "venue_name": "AT&T Stadium",
                "valid_from": "2013-07-25",
                "valid_to": ""
            }
        ],
        "VEN-000052": [
            {
                "venue_name": "CU Events/Conference Center",
                "valid_from": "1979-08-08",
                "valid_to": "1990-09-19"
            },
            {
                "venue_name": "Coors Events Center",
                "valid_from": "1990-09-20",
                "valid_to": "2018-06-30"
            },
            {
                "venue_name": "CU Events Center",
                "valid_from": "2018-07-01",
                "valid_to": ""
            }
        ],
        "VEN-000096": [
            {
                "venue_name": "Carrier Dome",
                "valid_from": "1980-09-20",
                "valid_to": "2022-05-18"
            },
            {
                "venue_name": "JMA Wireless Dome",
                "valid_from": "2022-05-19",
                "valid_to": ""
            }
        ],
        "VEN-000135": [
            {
                "venue_name": "Mandalay Bay Events Center",
                "valid_from": "1999-04-10",
                "valid_to": "2021-02-10"
            },
            {
                "venue_name": "Michelob ULTRA Arena",
                "valid_from": "2021-02-11",
                "valid_to": ""
            }
        ],
        "VEN-000196": [
            {
                "venue_name": "Assembly Hall",
                "valid_from": "1963-03-02",
                "valid_to": "2013-04-28"
            },
            {
                "venue_name": "State Farm Center",
                "valid_from": "2013-04-29",
                "valid_to": ""
            }
        ],
        "VEN-000228": [
            {
                "venue_name": "Wells Fargo Arena",
                "valid_from": "2005-07-12",
                "valid_to": "2025-06-30"
            },
            {
                "venue_name": "Casey's Center",
                "valid_from": "2025-07-01",
                "valid_to": ""
            }
        ],
        "VEN-000686": [
            {
                "venue_name": "Special Events Arena",
                "valid_from": "1994-10-21",
                "valid_to": "1998-02-19"
            },
            {
                "venue_name": "Stan Sheriff Center",
                "valid_from": "1998-02-20",
                "valid_to": "2020-11-11"
            },
            {
                "venue_name": "SimpliFi Arena at Stan Sheriff Center",
                "valid_from": "2020-11-12",
                "valid_to": "2025-08-25"
            },
            {
                "venue_name": "Bankoh Arena at Stan Sheriff Center",
                "valid_from": "2025-08-26",
                "valid_to": ""
            }
        ],
        "VEN-000698": [
            {
                "venue_name": "American Bank Center Arena",
                "valid_from": "2004-05-20",
                "valid_to": "2025-08-31"
            },
            {
                "venue_name": "Hilliard Center Arena",
                "valid_from": "2025-09-01",
                "valid_to": ""
            }
        ],
        "VEN-000714": [
            {
                "venue_name": "Coliseum Arena",
                "valid_from": "1922-04-04",
                "valid_to": "2003-10-31"
            },
            {
                "venue_name": "Ricoh Coliseum",
                "valid_from": "2003-11-01",
                "valid_to": "2018-07-10"
            },
            {
                "venue_name": "Coca-Cola Coliseum",
                "valid_from": "2018-07-11",
                "valid_to": ""
            }
        ]
    }
}


class HistoricalVenueNamingTests(unittest.TestCase):
    def test_exact_periods_published_from_existing_reference(self):
        expected = json.loads(json.dumps(EXPECTED))
        current = official_venue_name_periods(ROOT)
        if "VEN-000433" in current["venues"]:
            expected["venues"]["VEN-000433"] = [
                {
                    "venue_name": "Atlantic City Convention Hall",
                    "valid_from": "1929-05-31",
                    "valid_to": "2001-10-10",
                },
                {
                    "venue_name": "Boardwalk Hall",
                    "valid_from": "2001-10-11",
                    "valid_to": "2018-01-15",
                },
                {
                    "venue_name": "Jim Whelan Boardwalk Hall",
                    "valid_from": "2018-01-16",
                    "valid_to": "",
                },
            ]
        self.assertEqual(current, expected)
        self.assertEqual(json.loads(PERIODS_PATH.read_text(encoding="utf-8")), expected)
        manifest = json.loads((ROOT / "site/data/manifest.json").read_text())
        self.assertEqual(manifest["files"]["venue_name_periods"], "venue-name-periods.json")
        with CSV_PATH.open(encoding="utf-8", newline="") as fp:
            rows = list(csv.DictReader(fp))
        official = [r for r in rows if r["name_type"] == "OFFICIAL_NAMING_PERIOD"]
        self.assertEqual(len(official), sum(len(v) for v in expected["venues"].values()))
        self.assertEqual(
            {r["venue_id"] for r in official},
            set(expected["venues"]),
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
        self.assertIn("venueCanonical: game.venue_name || humanizeKey(game.venue_key)", INDEX)
        self.assertIn("venueCanonical: game.venueCanonical", INDEX)
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
             venue:"Assembly Hall",venueCanonical:"Assembly Hall",
             location:"Champaign, IL",winner:"illinois"};
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

assert.equal(show("VEN-000015","2010-01-01"),"Cowboys Stadium");
assert.equal(show("VEN-000015","2013-07-25"),"AT&T Stadium");
assert.equal(show("VEN-000135","2020-01-01"),"Mandalay Bay Events Center");
assert.equal(show("VEN-000135","2021-02-11"),"Michelob ULTRA Arena");
assert.equal(show("VEN-000228","2025-06-30"),"Wells Fargo Arena");
assert.equal(show("VEN-000228","2025-07-01"),"Casey's Center");
assert.equal(show("VEN-000686","1997-01-01"),"Special Events Arena");
assert.equal(show("VEN-000686","1998-02-20"),"Stan Sheriff Center");
assert.equal(show("VEN-000686","2020-11-12"),"SimpliFi Arena at Stan Sheriff Center");
assert.equal(show("VEN-000686","2025-08-26"),"Bankoh Arena at Stan Sheriff Center");
assert.equal(show("VEN-000698","2025-08-31"),"American Bank Center Arena");
assert.equal(show("VEN-000698","2025-09-01"),"Hilliard Center Arena");
assert.equal(show("VEN-000714","2000-01-01"),"Coliseum Arena");
assert.equal(show("VEN-000714","2003-11-01"),"Ricoh Coliseum");
assert.equal(show("VEN-000714","2018-07-11"),"Coca-Cola Coliseum");

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
assert.equal(summaries[0].label,"State Farm Center");

const syracuse = {venueId:"VEN-000096",venueKey:"jma-wireless-dome",
                  venue:"Carrier Dome",venueCanonical:"Carrier Dome",
                  location:"Syracuse, NY",winner:"syracuse"};
assert.equal(aggregateVenueLabel(syracuse),"JMA Wireless Dome");

DB.venueNamePeriods["VEN-CLOSED"] = [
  {venue_name:"Old Closed Name",valid_from:"1980-01-01",valid_to:"1990-12-31"},
  {venue_name:"Last Closed Name",valid_from:"1991-01-01",valid_to:"2000-12-31"},
];
const closed = {venueId:"VEN-CLOSED",venue:"Old Closed Name",
                venueCanonical:"Canonical Closed Venue",location:"Somewhere"};
assert.equal(aggregateVenueLabel(closed),"Canonical Closed Venue");
""",
        ]
        result = subprocess.run(
            ["node", "-"], input="\n".join(source),
            text=True, capture_output=True, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
