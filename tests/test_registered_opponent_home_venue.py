"""Fail-closed identity tests for preexisting global opponent-host facilities.

School-local venues.csv is the target school's relationships, not a complete
catalogue of every away opponent's registered physical buildings.
"""
from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
from venue_reference import (  # noqa: E402
    load_global_venue_reference,
    registered_opponent_home_venue,
)


def csv_rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class RegisteredOpponentHomeVenueTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.by_id, _, cls.names = load_global_venue_reference(ROOT)
        cls.local_path = ROOT / "schools" / "uc-davis" / "venues.csv"
        cls.local = csv_rows(cls.local_path)
        cls.source = {
            "source_game_id": "TEST-REGISTERED-OPPONENT-HOME",
            "source_program_key": "uc-davis",
            "normalized_opponent_key": "dayton",
            "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": "University of Dayton Fieldhouse",
            "city": "Dayton",
            "state": "OH",
            "game_date": "1963-12-04",
            "season_label": "1963-1964",
            "team_score": "48",
            "opponent_score": "74",
            "played_result": "L",
            "curated_game_type": "REGULAR_SEASON",
        }

    def test_real_authorized_dayton_venue_is_a_global_registered_identity(self):
        # The actual published protected-main registry contains this settled
        # physical identity, not a name/latitude guess or a new venue ID.
        self.assertNotIn(
            "University of Dayton Fieldhouse",
            [r.get("canonical_name") for r in self.local],
        )
        result = registered_opponent_home_venue(
            self.source, self.local, self.by_id, self.names
        )
        self.assertIsNotNone(result)
        self.assertEqual(
            (result["venue_id"], result["venue_key"], result["city"], result["state"]),
            ("VEN-001043", "university-of-dayton-fieldhouse", "Dayton", "OH"),
        )

    def test_canonical_runtime_uses_same_registered_identity_without_local_edit(self):
        venue_map = ingest_school.load_venue_metadata_map_with_name_periods(
            ROOT, self.local_path, self.by_id,
        )
        resolved = ingest_school.resolve_venue_metadata(self.source, venue_map)
        self.assertEqual(resolved["venue_id"], "VEN-001043")
        self.assertEqual(resolved["venue_key"], "university-of-dayton-fieldhouse")
        game = ingest_school.build_new_canonical(
            self.source, "CBBG-TEST-REGISTERED-HOST", {}, venue_map
        )
        self.assertEqual(game["venue_id"], "VEN-001043")
        self.assertEqual(game["venue_key"], "university-of-dayton-fieldhouse")
        self.assertEqual(game["designated_home_team_key"], "dayton")
        self.assertEqual((game["site_city"], game["site_state"]), ("Dayton", "OH"))
        # No normalization or source mutation is permitted.
        self.assertEqual(self.source["curated_venue_name"], "University of Dayton Fieldhouse")

    def test_non_host_or_incomplete_source_authority_fails_closed(self):
        for field, value in (
            ("curated_site_type", "SOURCE_PROGRAM_HOME"),
            ("curated_site_type", "NEUTRAL"),
            ("curated_site_type", "UNKNOWN"),
            ("curated_venue_name", ""),
            ("curated_venue_name", "Unregistered Dayton Hall"),
            ("city", ""),
            ("city", "Davis"),
            ("state", ""),
            ("state", "CA"),
            ("game_date", ""),
            ("game_date", "not-a-date"),
            ("normalized_opponent_key", ""),
            ("normalized_opponent_key", "uc-davis"),
        ):
            with self.subTest(field=field, value=value):
                source = dict(self.source, **{field: value})
                self.assertIsNone(
                    registered_opponent_home_venue(
                        source, self.local, self.by_id, self.names
                    )
                )

    def test_local_conflict_or_ambiguous_global_match_fails_closed(self):
        conflicting_local = self.local + [
            {"venue_key": "other-venue", "canonical_name": "Other Facility",
             "aliases": "University of Dayton Fieldhouse"}
        ]
        self.assertIsNone(registered_opponent_home_venue(
            self.source, conflicting_local, self.by_id, self.names
        ))
        missing_names = dict(self.names)
        missing_names["universityofdaytonfieldhouse"] = set()
        self.assertIsNone(registered_opponent_home_venue(
            self.source, self.local, self.by_id, missing_names
        ))
        extra = dict(self.by_id)
        extra["VEN-999991"] = dict(
            self.by_id["VEN-001043"],
            venue_id="VEN-999991",
            venue_key="another-physical-dayton-fieldhouse",
        )
        duplicated = dict(self.names)
        duplicated["universityofdaytonfieldhouse"] = {
            "VEN-001043", "VEN-999991"
        }
        self.assertIsNone(registered_opponent_home_venue(
            self.source, self.local, extra, duplicated
        ))

    def test_stated_physical_chronology_cannot_be_contradicted(self):
        for field, value in (
            ("opened", "1964"), ("opened", "1964-01"),
            ("closed", "1962"), ("closed", "1962-12-31"),
            ("opened", "not-a-date"),
            ("closed", "not-a-date"),
        ):
            with self.subTest(field=field, value=value):
                changed = dict(self.by_id)
                changed["VEN-001043"] = dict(changed["VEN-001043"], **{field: value})
                self.assertIsNone(registered_opponent_home_venue(
                    self.source, self.local, changed, self.names
                ))


if __name__ == "__main__":
    unittest.main()
