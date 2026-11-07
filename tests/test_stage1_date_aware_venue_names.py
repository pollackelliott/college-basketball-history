import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from stage_research_portfolio import rebase_venues, venue_reconciliation_inventory  # noqa: E402


def global_venue(venue_id: str, venue_key: str, name: str):
    return {
        "venue_id": venue_id,
        "venue_key": venue_key,
        "display_name": name,
        "city": "Orlando",
        "state": "FL",
        "opened": "",
        "closed": "",
        "date_precision": "",
        "identity_status": "TEST",
        "source_basis": "test",
        "notes": "",
    }


def local_ucf_arena(date: str):
    return {
        "source_program_key": "test-school",
        "venue_key": "ucf-arena",
        "venue_id": "",
        "canonical_name": "UCF Arena",
        "aliases": "",
        "city": "Orlando",
        "state": "FL",
        "venue_type": "",
        "known_opened": "",
        "known_closed": "",
        "venue_date_precision": "unknown",
        "games_currently_assigned": "1",
        "first_assigned_game": date,
        "last_assigned_game": date,
        "relationship_type": "",
        "relationship_start": "",
        "relationship_end": "",
        "relationship_date_precision": "",
        "site_rule": "",
        "source_basis": "accepted target-school venue authority",
        "notes": "",
    }


def name_row(venue_id: str, valid_from: str, valid_to: str):
    return {
        "venue_id": venue_id,
        "venue_name": "UCF Arena",
        "normalized_name": "ucfarena",
        "name_type": "OFFICIAL_NAMING_PERIOD",
        "valid_from": valid_from,
        "valid_to": valid_to,
        "date_precision": "EXACT",
        "source_basis": "accepted UCF venue chronology",
        "notes": "",
    }


def reconciliation():
    return {
        "ucf-arena": {
            "action": "REUSE_CURRENT_IDENTITY",
            "global_venue_id": "VEN-000694",
            "global_venue_key": "the-venue-at-ucf",
        }
    }


class DateAwareVenueNameReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.old = global_venue(
            "VEN-000694", "the-venue-at-ucf", "The Venue at UCF"
        )
        self.new = global_venue(
            "VEN-000038", "cfe-arena", "Addition Financial Arena"
        )
        self.old_name = name_row("VEN-000694", "", "2007-03-03")
        self.new_name = name_row(
            "VEN-000038", "2007-09-08", "2013-05-22"
        )

    def test_exact_2004_assignment_uses_old_ucf_arena_without_unbounded_alias(self):
        local = local_ucf_arena("2004-12-28")
        names = [dict(self.old_name), dict(self.new_name)]

        inventory = venue_reconciliation_inventory(
            [dict(local)],
            [dict(self.old), dict(self.new)],
            [dict(row) for row in names],
            venue_reconciliation=reconciliation(),
        )
        self.assertEqual(inventory["blocker_count"], 0)
        row = inventory["rows"][0]
        self.assertEqual(row["target_venue_id"], "VEN-000694")
        self.assertEqual(row["missing_registered_names"], [])
        self.assertNotIn("CONFLICTING_REGISTERED_NAME_IDENTITIES", row["issues"])
        self.assertNotIn("GLOBAL_NAME_REGISTRATION_DURING_PHASE0", row["issues"])
        self.assertIn(
            "DATE_BOUNDED_REGISTERED_NAME_DISAMBIGUATION",
            row["issues"],
        )

        staged, _globals, staged_names, mappings = rebase_venues(
            "test-school",
            [dict(local)],
            [dict(self.old), dict(self.new)],
            [dict(row) for row in names],
            venue_reconciliation=reconciliation(),
        )
        self.assertEqual(staged[0]["venue_id"], "VEN-000694")
        self.assertEqual(
            mappings[0]["resolution"], "REUSE_EXPLICIT_RECONCILIATION"
        )
        old_ucf_rows = [
            row
            for row in staged_names
            if row["venue_id"] == "VEN-000694"
            and row["normalized_name"] == "ucfarena"
        ]
        self.assertEqual(len(old_ucf_rows), 1)
        self.assertEqual(old_ucf_rows[0]["valid_to"], "2007-03-03")
        self.assertFalse(
            any(
                row["venue_id"] == "VEN-000694"
                and row["normalized_name"] == "ucfarena"
                and not row.get("valid_from", "").strip()
                and not row.get("valid_to", "").strip()
                for row in staged_names
            )
        )

    def test_exact_fordham_2004_ucf_topology_against_repository_reference(self):
        def read_csv(path):
            with path.open(encoding="utf-8-sig", newline="") as handle:
                return list(csv.DictReader(handle))

        globals_ = read_csv(ROOT / "data/reference/venues.csv")
        names = read_csv(ROOT / "data/reference/venue-names.csv")
        old = next(row for row in globals_ if row["venue_id"] == "VEN-000694")
        new = next(row for row in globals_ if row["venue_id"] == "VEN-000038")
        old_names = [
            row
            for row in names
            if row["venue_id"] == "VEN-000694"
            and row["normalized_name"] == "ucfarena"
        ]
        new_names = [
            row
            for row in names
            if row["venue_id"] == "VEN-000038"
            and row["normalized_name"] == "ucfarena"
        ]

        self.assertEqual(len(old_names), 1)
        self.assertEqual(old_names[0]["name_type"], "HISTORICAL_OR_ALIAS")
        self.assertEqual(old_names[0]["valid_from"], "")
        self.assertEqual(old_names[0]["valid_to"], "2007-03-03")
        self.assertEqual(len(new_names), 1)
        self.assertEqual(new_names[0]["valid_from"], "2007-09-08")

        fordham = local_ucf_arena("2004-12-28")
        fordham["source_program_key"] = "fordham"
        fordham["source_basis"] = (
            "Fordham immutable Research Freeze; FORDHAM-2004-05-009"
        )

        inventory = venue_reconciliation_inventory(
            [dict(fordham)],
            globals_,
            names,
            school_key="fordham",
            venue_reconciliation=reconciliation(),
        )
        self.assertEqual(inventory["blocker_count"], 0)
        row = inventory["rows"][0]
        self.assertEqual(row["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(row["target_venue_id"], "VEN-000694")
        self.assertIn(
            "DATE_BOUNDED_REGISTERED_NAME_DISAMBIGUATION",
            row["issues"],
        )
        self.assertNotIn("CONFLICTING_REGISTERED_NAME_IDENTITIES", row["issues"])
        self.assertNotIn("GLOBAL_NAME_REGISTRATION_DURING_PHASE0", row["issues"])

        staged, staged_globals, staged_names, mappings = rebase_venues(
            "fordham",
            [dict(fordham)],
            globals_,
            names,
            venue_reconciliation=reconciliation(),
        )
        self.assertEqual(staged[0]["venue_id"], "VEN-000694")
        self.assertEqual(mappings[0]["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        self.assertEqual(
            next(row for row in staged_globals if row["venue_id"] == "VEN-000038"),
            new,
        )
        self.assertFalse(
            any(
                row["venue_id"] == "VEN-000694"
                and row["normalized_name"] == "ucfarena"
                and not row.get("valid_from", "").strip()
                and not row.get("valid_to", "").strip()
                for row in staged_names
            )
        )

    def test_assignment_in_new_arena_period_does_not_resolve_to_old_identity(self):
        inventory = venue_reconciliation_inventory(
            [local_ucf_arena("2011-03-16")],
            [dict(self.old), dict(self.new)],
            [dict(self.old_name), dict(self.new_name)],
            venue_reconciliation=reconciliation(),
        )
        self.assertEqual(inventory["blocker_count"], 1)
        self.assertIn(
            "CONFLICTING_REGISTERED_NAME_IDENTITIES",
            inventory["rows"][0]["issues"],
        )

    def test_overlapping_registered_periods_remain_blocked(self):
        overlapping_new = name_row(
            "VEN-000038", "2007-01-01", "2013-05-22"
        )
        old_overlap = name_row("VEN-000694", "", "2008-12-31")
        inventory = venue_reconciliation_inventory(
            [local_ucf_arena("2008-01-01")],
            [dict(self.old), dict(self.new)],
            [old_overlap, overlapping_new],
            venue_reconciliation=reconciliation(),
        )
        self.assertEqual(inventory["blocker_count"], 1)
        self.assertIn(
            "CONFLICTING_REGISTERED_NAME_IDENTITIES",
            inventory["rows"][0]["issues"],
        )

    def test_undated_assignment_remains_blocked(self):
        inventory = venue_reconciliation_inventory(
            [local_ucf_arena("")],
            [dict(self.old), dict(self.new)],
            [dict(self.old_name), dict(self.new_name)],
            venue_reconciliation=reconciliation(),
        )
        self.assertEqual(inventory["blocker_count"], 1)
        self.assertIn(
            "CONFLICTING_REGISTERED_NAME_IDENTITIES",
            inventory["rows"][0]["issues"],
        )


if __name__ == "__main__":
    unittest.main()
