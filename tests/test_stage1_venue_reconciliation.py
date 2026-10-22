"""Regression tests for explicit, hash-bound Stage 1 venue identity reuse."""
import hashlib
import csv
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from onboarding_plan import WorkflowError  # noqa: E402
from stage1_venue_reconciliation import load_venue_reconciliation  # noqa: E402
from stage_research_portfolio import (  # noqa: E402
    build_stage1_reconciliation_inventory,
    rebase_venues,
    rebase_program_aliases,
    program_alias_inventory,
    venue_reconciliation_inventory,
)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class ExplicitVenueReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.package = self.root / "package.zip"
        venues_bytes = b"venue_key,canonical_name,city,state\nreitz-arena,Reitz Arena,Baltimore,MD\n"
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        self.local = {
            "source_program_key": "test-school",
            "venue_key": "reitz-arena", "venue_id": "",
            "canonical_name": "Reitz Arena", "aliases": "",
            "city": "Baltimore", "state": "MD",
            "known_opened": "", "known_closed": "", "venue_date_precision": "unknown",
            "first_assigned_game": "1985-03-02", "last_assigned_game": "1985-03-04",
            "notes": "Historical identity: RESOLVED. Global registration: PENDING_CURRENT_MAIN_REBASE.",
        }
        self.global_row = {
            "venue_id": "VEN-000925", "venue_key": "reitz-arena-loyola-maryland",
            "display_name": "Reitz Arena", "city": "Baltimore", "state": "MD",
            "opened": "", "closed": "", "identity_status": "TEST", "notes": "",
        }
        self.doc = {
            "schema_version": 1,
            "school_key": "test-school",
            "owner_approval_basis": "Control Center disposition: same physical venue",
            "expected_research_zip_sha256": sha(self.package.read_bytes()),
            "expected_venues_sha256": sha(venues_bytes),
            "mappings": [{
                "local_venue_key": "reitz-arena",
                "expected_local_name": "Reitz Arena",
                "expected_local_city": "Baltimore", "expected_local_state": "MD",
                "global_venue_id": "VEN-000925",
                "global_venue_key": "reitz-arena-loyola-maryland",
                "expected_global_city": "Baltimore", "expected_global_state": "MD",
                "resolution_basis": "Loyola reference + explicit owner authority",
            }],
        }
        self.spec = self.root / "reconciliation.json"
        self.save()

    def save(self):
        self.spec.write_text(json.dumps(self.doc), encoding="utf-8")

    def load(self):
        return load_venue_reconciliation(
            self.spec, school_key="test-school", package_path=self.package,
            local_venues=[dict(self.local)], global_venues=[dict(self.global_row)],
        )

    def test_inventory_and_rebase_share_explicit_identity(self):
        mapping, meta = self.load()
        result = venue_reconciliation_inventory(
            [dict(self.local)], [dict(self.global_row)], [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(result["blocker_count"], 0)
        item = result["rows"][0]
        self.assertEqual(item["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(item["target_venue_id"], "VEN-000925")
        self.assertEqual(item["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        whole = build_stage1_reconciliation_inventory(
            "test-school", [dict(self.local)], [dict(self.global_row)], [], [], [], [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(whole["status"], "PASS")
        locals_, globals_, _, outcomes = rebase_venues(
            "test-school", [dict(self.local)], [dict(self.global_row)], [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(locals_[0]["venue_key"], "reitz-arena-loyola-maryland")
        self.assertEqual(locals_[0]["venue_id"], "VEN-000925")
        self.assertEqual(len(globals_), 1)
        self.assertEqual(outcomes[0]["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        self.assertEqual(meta["frozen_venues_sha256"], self.doc["expected_venues_sha256"])

    def test_no_spec_keeps_ambiguous_stop(self):
        result = venue_reconciliation_inventory(
            [dict(self.local)], [dict(self.global_row)], []
        )
        self.assertEqual(result["blocker_count"], 1)

    def test_package_hash_mismatch_fails(self):
        self.doc["expected_research_zip_sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(WorkflowError, "package SHA-256 mismatch"):
            self.load()

    def test_member_hash_mismatch_fails(self):
        self.doc["expected_venues_sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(WorkflowError, "venues.csv SHA-256 mismatch"):
            self.load()

    def test_unknown_local_key_fails(self):
        self.doc["mappings"][0]["local_venue_key"] = "wrong-key"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "unknown local key"):
            self.load()

    def test_stale_global_id_fails(self):
        self.doc["mappings"][0]["global_venue_id"] = "VEN-111111"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "stale global venue ID/key"):
            self.load()

    def test_stale_global_key_fails(self):
        self.doc["mappings"][0]["global_venue_key"] = "wrong-key"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "stale global venue ID/key"):
            self.load()

    def test_global_geography_mismatch_fails(self):
        self.doc["mappings"][0]["expected_global_state"] = "NJ"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "global geography mismatch"):
            self.load()

    def test_local_identity_drift_fails(self):
        self.doc["mappings"][0]["expected_local_name"] = "Reitz Gym"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "frozen local identity drift"):
            self.load()

    def test_duplicate_key_fails(self):
        self.doc["mappings"].append(dict(self.doc["mappings"][0]))
        self.save()
        with self.assertRaisesRegex(WorkflowError, "repeats local key"):
            self.load()


class DaytonHistoricalNameBoundTests(unittest.TestCase):
    """Current verified predecessor name must not attach a 1986 opponent to Dayton."""

    def setUp(self):
        path = ROOT / "data/reference/program-names.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        matches = [r for r in rows
                   if r["program_key"] == "dayton"
                   and r["alias_name"] == "St. Mary's College"]
        self.assertEqual(len(matches), 1)
        self.alias = matches[0]
        self.programs = [{"program_key": "dayton", "program_name": "Dayton",
                          "display_name": "Dayton", "current_d1": "Yes"}]

    def opponent(self, season):
        return {
            "source_program_key": "test-school",
            "source_opponent_label": "St. Mary’s College",
            "canonical_opponent_key": "st-marys-college",
            "canonical_opponent_name": "St. Mary’s College",
            "current_d1": "FALSE",
            "games_with_source_label": "1",
            "first_season": season, "last_season": season,
        }

    def game(self, season):
        return {
            "source_game_id": "FDU-S1-000488" if season == "1986-1987" else "fixture-early",
            "source_program_key": "test-school", "season_label": season,
            "source_opponent_label": "St. Mary’s College",
            "normalized_opponent_key": "st-marys-college",
            "normalized_opponent_name": "St. Mary’s College",
            "raw_text": "W 86-54 St. Mary’s College",
            "opponent_current_d1": "FALSE",
        }

    def test_dayton_alias_is_bounded_at_1919_1920(self):
        self.assertEqual(self.alias["effective_end_season"], "1919-1920")
        self.assertEqual(self.alias["verification_status"], "VERIFIED")

    def test_early_dayton_usage_remains_eligible(self):
        opponents, games, mappings = rebase_program_aliases(
            self.programs, [self.alias], [self.opponent("1915-1916")],
            [self.game("1915-1916")],
        )
        self.assertEqual(opponents[0]["canonical_opponent_key"], "dayton")
        self.assertEqual(games[0]["normalized_opponent_key"], "dayton")
        self.assertEqual(len(mappings), 1)

    def test_1986_fdu_opponent_remains_non_d1_literal_identity(self):
        opponent = self.opponent("1986-1987")
        game = self.game("1986-1987")
        inventory = program_alias_inventory(self.programs, [self.alias], [opponent])
        self.assertEqual(inventory["classification_counts"], {"NO_CURRENT_VERIFIED_ALIAS": 1})
        opponents, games, mappings = rebase_program_aliases(
            self.programs, [self.alias], [opponent], [game],
        )
        self.assertEqual(opponents[0]["canonical_opponent_key"], "st-marys-college")
        self.assertEqual(opponents[0]["current_d1"], "FALSE")
        self.assertEqual(games[0]["normalized_opponent_key"], "st-marys-college")
        self.assertEqual(games[0]["opponent_current_d1"], "FALSE")
        self.assertEqual(games[0]["raw_text"], "W 86-54 St. Mary’s College")
        self.assertEqual(mappings, [])


if __name__ == "__main__":
    unittest.main()
