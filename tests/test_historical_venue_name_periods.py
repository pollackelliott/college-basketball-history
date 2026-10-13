"""Audited physical-venue naming periods: exact Illinois pilot and UI behavior."""
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


class HistoricalVenueNamingTests(unittest.TestCase):
    def test_exact_periods_published_from_existing_reference(self):
        expected = {
            "schema_version": 1,
            "venues": {
                "VEN-000196": [
                    {
                        "venue_name": "Assembly Hall",
                        "valid_from": "1963-03-02",
                        "valid_to": "2013-04-28",
                    },
                    {
                        "venue_name": "State Farm Center",
                        "valid_from": "2013-04-29",
                        "valid_to": "",
                    },
                ]
            },
        }
        self.assertEqual(official_venue_name_periods(ROOT), expected)
        self.assertEqual(json.loads(PERIODS_PATH.read_text(encoding="utf-8")), expected)
        manifest = json.loads((ROOT / "site/data/manifest.json").read_text())
        self.assertEqual(
            manifest["files"]["venue_name_periods"], "venue-name-periods.json"
        )
        with CSV_PATH.open(encoding="utf-8", newline="") as fp:
            rows = list(csv.DictReader(fp))
        official = [r for r in rows if r["name_type"] == "OFFICIAL_NAMING_PERIOD"]
        self.assertEqual(len(official), 2)
        self.assertEqual({r["venue_id"] for r in official}, {"VEN-000196"})
        self.assertEqual(
            {r["venue_name"] for r in official},
            {"Assembly Hall", "State Farm Center"},
        )
        self.assertTrue(all(r["source_basis"].startswith("https://") for r in official))
        self.assertEqual(
            [r["venue_name"] for r in rows if r["venue_id"] == "VEN-000186"
             and r["name_type"] == "PROJECT_DISPLAY"],
            ["Assembly Hall"],
        )

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
        self.assertEqual(check([dict(row, name_type="HISTORICAL_OR_ALIAS")]),
                         {"schema_version": 1, "venues": {}})

    def test_frontend_uses_identity_and_exact_game_date_not_alias_guesswork(self):
        # These checks execute the actual production JS functions in Node, if
        # available. The Python site checks remain useful on lean environments.
        self.assertIn("game.venue_id, game.game_date, game.date_precision", INDEX)
        self.assertIn("venueId: game.venue_id || null", INDEX)
        self.assertIn("venueNamePeriods: {}", INDEX)
        self.assertIn("DB.venueNamePeriods = namingDocument.venues;", INDEX)
        self.assertIn("venueOptionMatchesGame(state.venueQuery", INDEX)
        self.assertIn("aggregateVenueLabel,", INDEX)
        self.assertIn("(game) => game.venueId || game.venueKey", INDEX)
        if not shutil.which("node"):
            self.skipTest("Node is not installed; source/period validation still ran")
        def section(start, end):
            begin = INDEX.index("function " + start + "(")
            finish = INDEX.index("\nfunction " + end + "(", begin)
            return INDEX[begin:finish]

        source = [
            "const assert = require('node:assert/strict');",
            "const DB = {venueNamePeriods: " +
                json.dumps(official_venue_name_periods(ROOT)["venues"]) + "};",
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
assert.equal(show("VEN-000196","2025-01-01"),"State Farm Center");
assert.equal(show("VEN-000186","2013-04-29"),"Project fallback");
assert.equal(show("VEN-000196","2013","YEAR"),"Project fallback");
assert.equal(show("VEN-000196","2013-04-29","YEAR"),"Project fallback");
assert.equal(show("VEN-000196",null,""),"Project fallback");
const opts = venueOptionsForGames([old,modern,different]);
assert.equal(venueOptionMatchesGame("State Farm Center",old,opts),true);
assert.equal(venueOptionMatchesGame("Assembly Hall",modern,opts),true);
assert.equal(venueOptionMatchesGame("State Farm Center",different,opts),false);
assert.equal(venueOptionMatchesGame("Bloomington",old,opts),false);
const summaries = bucket([old,modern],"illinois","opponent",aggregateVenueLabel,
  game => game.venueId || game.venueKey);
assert.equal(summaries.length,1);
assert.equal(summaries[0].games,2);
assert.equal(summaries[0].wins,1);
assert.equal(summaries[0].losses,1);
assert.equal(summaries[0].label,"Assembly Hall / State Farm Center");
""",
        ]
        result = subprocess.run(
            ["node", "-"], input="\n".join(source),
            text=True, capture_output=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
