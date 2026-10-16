"""Regression tests for the exact C1 row-scope apply safety boundary."""
import csv
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from apply_c1_home_batch1 import Stop, patch, FIELDS


def write_csv(path, names, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=names)
        writer.writeheader()
        writer.writerows(rows)


class C1HomeBatchSafetyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.game_id = "CBBG-TEST-1"
        self.source_id = "ALA-S1"
        self.can = dict(canonical_game_id=self.game_id, game_date="1955-01-03", game_type="REGULAR_SEASON",
                        team_a_key="alabama", team_b_key="auburn", site_type="TEAM_A_HOME",
                        venue_id="", venue_key="", site_city="", site_state="", notes="")
        self.src = dict(source_game_id=self.source_id, source_program_key="alabama",
                        curated_site_type="UNKNOWN", curated_venue_name="", city="", state="")
        self.mine = dict(canonical_game_id=self.game_id, source_program_key="alabama",
                         source_game_id=self.source_id, normalized_opponent_key="auburn",
                         curated_site_type="UNKNOWN", curated_venue_name="", city="", state="")
        self.recip = dict(canonical_game_id=self.game_id, source_program_key="auburn",
                          source_game_id="AUB-S1", normalized_opponent_key="alabama",
                          curated_site_type="OPPONENT_HOME", curated_venue_name="", city="", state="")
        self.row = dict(program="alabama", canonical_game_id=self.game_id, source_game_id=self.source_id,
                        game_date="1955-01-03", part="B", authority="reciprocal_participant_HOME_assertion",
                        reciprocal_home_assertions=["AUB-S1"], venue_key="foster-auditorium",
                        patches={"canonical": {"venue_id": "VEN-000067", "venue_key": "foster-auditorium",
                                               "site_city": "Tuscaloosa", "site_state": "AL"},
                                 "source": {}, "assertion": {}},
                        preimage={"canonical": {"venue_id": "", "venue_key": "", "site_city": "", "site_state": ""},
                                  "source": {}, "assertion": {}})
        self.write()

    def write(self):
        write_csv(self.root / "data/canonical/games.csv", list(self.can), [self.can])
        write_csv(self.root / "data/evidence/game-assertions.csv", list(self.mine), [self.mine, self.recip])
        write_csv(self.root / "data/reconciliation/discrepancies.csv",
                  ["canonical_game_id", "field_name", "status", "resolution_basis"], [])
        for school in ("alabama", "auburn", "duke", "purdue", "wisconsin"):
            rows = [self.src] if school == "alabama" else []
            write_csv(self.root / f"schools/{school}/source-games.csv", list(self.src), rows)

    def test_canonical_only_backfill_preserves_unknown_source(self):
        before = (self.root / "schools/alabama/source-games.csv").read_bytes()
        diff = patch(self.root, [self.row], apply=False)
        self.assertEqual(diff["canonical"], 4)
        self.assertEqual(diff["source"], 0)
        self.assertEqual((self.root / "schools/alabama/source-games.csv").read_bytes(), before)
        self.assertEqual(FIELDS["canonical"], {"venue_id", "venue_key", "site_city", "site_state"})

    def test_does_not_override_nonblank_canonical_location(self):
        self.can["site_city"] = "Birmingham"
        self.write()
        with self.assertRaisesRegex(Stop, "preimage drift"):
            patch(self.root, [self.row], apply=False)

    def test_disallows_unauthorized_source_han_rewrite(self):
        self.row["patches"]["source"] = {"curated_site_type": "SOURCE_PROGRAM_HOME"}
        self.row["preimage"]["source"] = {"curated_site_type": "UNKNOWN"}
        with self.assertRaisesRegex(Stop, "Part B must not alter"):
            patch(self.root, [self.row], apply=False)

    def test_requires_real_reciprocal_home_evidence(self):
        self.recip["curated_site_type"] = "NEUTRAL"
        self.write()
        with self.assertRaisesRegex(Stop, "reciprocal HOME evidence changed"):
            patch(self.root, [self.row], apply=False)

    def test_refuses_unadjudicated_conflicting_site(self):
        third = dict(self.recip, source_game_id="AUB-S2", curated_site_type="NEUTRAL")
        write_csv(self.root / "data/evidence/game-assertions.csv", list(self.mine), [self.mine, self.recip, third])
        with self.assertRaisesRegex(Stop, "unadjudicated contradictory"):
            patch(self.root, [self.row], apply=False)


if __name__ == "__main__":
    unittest.main()
