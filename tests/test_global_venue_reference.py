import copy
import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import backfill_venue_keys  # noqa: E402
import build_site_data  # noqa: E402
import venue_reference  # noqa: E402


def rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class GlobalVenueReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (
            cls.venues_by_id,
            cls.venues_by_key,
            cls.name_ids,
        ) = venue_reference.load_global_venue_reference(ROOT)

    def test_foundation_count_and_retired_id(self):
        self.assertGreaterEqual(len(self.venues_by_id), 237)
        self.assertNotIn("VEN-000075", self.venues_by_id)
        self.assertNotIn("VEN-000207", self.venues_by_id)
        self.assertNotIn("VEN-000407", self.venues_by_id)
        self.assertNotIn("VEN-000410", self.venues_by_id)
        self.assertNotIn("VEN-000680", self.venues_by_id)
        self.assertEqual(
            self.venues_by_id["VEN-000076"]["display_name"],
            "Greensboro Coliseum",
        )

    def test_owner_display_and_geography_rules(self):
        self.assertEqual(
            self.venues_by_key["state-farm-center"]["display_name"],
            "Assembly Hall",
        )
        self.assertEqual(
            self.venues_by_key["thompson-boling-arena"]["display_name"],
            "Thompson-Boling Arena",
        )
        for venue_key in (
            "mgm-grand-garden-arena",
            "michelob-ultra-arena",
            "t-mobile-arena",
            "orleans-arena",
            "thomas-and-mack-center",
        ):
            self.assertEqual(
                (
                    self.venues_by_key[venue_key]["city"],
                    self.venues_by_key[venue_key]["state"],
                ),
                ("Las Vegas", "NV"),
            )


    def test_documented_historical_alias_stays_local_across_distinct_buildings(self):
        # The generic physical-site topology behind UC Davis's accepted older
        # Recreation Hall versus the facility opened in 1977. No literal
        # school-specific exception and no second unqualified global alias.
        local = {
            "source_program_key": "fixture",
            "venue_key": "former-hall",
            "venue_id": "VEN-999970",
            "canonical_name": "Old Academic Hall",
            "aliases": "Academic Hall",
            "city": "College Town", "state": "CA",
            "known_opened": "", "known_closed": "1938",
            "relationship_start": "1921-1922",
            "relationship_end": "1936-1937",
            "site_rule": "Documented HOME facility for accepted early games",
            "source_basis": "https://example.edu/archive/early-building",
            "notes": "Former standalone building closed in 1938",
        }
        older = {
            "venue_id": "VEN-999970", "venue_key": "former-hall",
            "display_name": "Old Academic Hall",
            "city": "College Town", "state": "CA",
            "opened": "", "closed": "1938",
            "source_basis": "https://example.edu/archive/early-building",
        }
        newer = {
            "venue_id": "VEN-999971", "venue_key": "modern-hall",
            "display_name": "University Sports Center",
            "city": "College Town", "state": "CA",
            "opened": "1977", "closed": "",
            "source_basis": "https://example.edu/archive/modern-building",
        }
        distant = {
            "venue_id": "VEN-999972", "venue_key": "distant-hall",
            "display_name": "Academic Hall",
            "city": "Faraway", "state": "PA",
            "opened": "1900", "closed": "",
            "source_basis": "https://example.edu/archive/distant-building",
        }
        venue_rows = {r["venue_id"]: r for r in (older, newer, distant)}
        names = {
            "oldacademichall": {"VEN-999970"},
            "academic hall": set(),  # normalized key cannot create authority
            "academichall": {"VEN-999971", "VEN-999972"},
            "universitysportscenter": {"VEN-999971"},
        }

        def check(row=local, venues=venue_rows, labels=names):
            return venue_reference.school_venue_reference_errors(
                Path("schools/fixture/venues.csv"), [row], venues, labels,
            )

        self.assertEqual(check(), [])
        self.assertNotIn("VEN-999970", names["academichall"])
        self.assertEqual(
            check(dict(local, aliases="Academic Hall;Unregistered Other Alias")),
            ["line 2: name/alias 'Unregistered Other Alias' is not registered to VEN-999970"],
        )

        # Any evidence gap, chronology overlap, or changed physical key
        # restores the ordinary failure. Canonical names never receive
        # historical-alias treatment.
        for field, value in (
            ("source_basis", ""),
            ("site_rule", ""),
            ("notes", ""),
            ("known_closed", ""),
            ("known_closed", "1939"),
            ("relationship_end", ""),
            ("relationship_end", "1940-1941"),
            ("relationship_start", "1938-1939"),
            ("venue_key", "another-hall"),
            ("city", "Other City"),
            ("canonical_name", "Academic Hall"),
        ):
            with self.subTest(local_field=field, value=value):
                self.assertTrue(check(dict(local, **{field: value})))

        for field, value in (
            ("opened", ""), ("opened", "1937"),
            ("display_name", "Academic Hall"), ("source_basis", ""),
            ("city", "Other City"),
        ):
            with self.subTest(newer_field=field, value=value):
                changed = copy.deepcopy(venue_rows)
                changed["VEN-999971"][field] = value
                self.assertTrue(check(venues=changed))

        changed = copy.deepcopy(venue_rows)
        changed["VEN-999970"]["closed"] = ""
        self.assertTrue(check(venues=changed))
        changed = copy.deepcopy(venue_rows)
        changed["VEN-999970"]["venue_key"] = "different-key"
        self.assertTrue(check(venues=changed))

        without_newer = copy.deepcopy(names)
        without_newer["academichall"] = {"VEN-999972"}
        self.assertTrue(check(labels=without_newer))
        ambiguous = copy.deepcopy(venue_rows)
        ambiguous["VEN-999973"] = dict(
            newer, venue_id="VEN-999973", venue_key="another-modern-hall"
        )
        ambiguous_names = copy.deepcopy(names)
        ambiguous_names["academichall"].add("VEN-999973")
        self.assertTrue(check(venues=ambiguous, labels=ambiguous_names))

    def test_all_school_rows_reference_global_identity(self):
        total = 0
        for path in sorted((ROOT / "schools").glob("*/venues.csv")):
            school_rows = rows(path)
            problems = venue_reference.school_venue_reference_errors(
                path,
                school_rows,
                self.venues_by_id,
                self.name_ids,
            )
            self.assertEqual(problems, [], msg=f"{path}: {problems[:5]}")
            total += len(school_rows)
        self.assertGreaterEqual(total, 266)

    def test_existing_canonical_identity_parity(self):
        canonical = rows(ROOT / "data/canonical/games.csv")
        keyed = [row for row in canonical if row.get("venue_key", "").strip()]
        self.assertGreaterEqual(len(keyed), 18456)
        self.assertTrue(
            all(row.get("venue_id", "").strip() in self.venues_by_id for row in keyed)
        )
        self.assertTrue(
            all(
                bool(row.get("venue_key", "").strip())
                == bool(row.get("venue_id", "").strip())
                for row in canonical
            )
        )

    def test_all_canonical_venue_geography_matches_global_identity(self):
        canonical = rows(ROOT / "data/canonical/games.csv")
        self.assertEqual(
            venue_reference.canonical_venue_geography_errors(
                canonical,
                self.venues_by_id,
            ),
            [],
        )

    def test_global_geography_mismatch_is_fatal(self):
        fixture = {
            "canonical_game_id": "FIXTURE-GEO",
            "venue_id": "VEN-000048",
            "site_city": "Birmingham",
            "site_state": "AL",
        }
        problems = venue_reference.canonical_venue_geography_errors(
            [fixture],
            self.venues_by_id,
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("does not match", problems[0])

    def test_five_locked_global_geography_corrections(self):
        canonical = {
            row["canonical_game_id"]: row
            for row in rows(ROOT / "data/canonical/games.csv")
        }
        expected = {
            "CBBG-0002744": ("hp-field-house", "VEN-000084", "Kissimmee", "FL"),
            "CBBG-0002745": ("hp-field-house", "VEN-000084", "Kissimmee", "FL"),
            "CBBG-0002746": ("hp-field-house", "VEN-000084", "Kissimmee", "FL"),
            "CBBG-0029269": (
                "coleman-coliseum",
                "VEN-000048",
                "Tuscaloosa",
                "AL",
            ),
            "CBBG-0029681": (
                "legacy-arena",
                "VEN-000109",
                "Birmingham",
                "AL",
            ),
        }
        for game_id, values in expected.items():
            row = canonical[game_id]
            self.assertEqual(
                (
                    row["venue_key"],
                    row["venue_id"],
                    row["site_city"],
                    row["site_state"],
                ),
                values,
            )

    def test_backfill_same_physical_id_different_legacy_keys_is_not_conflict(self):
        resolved = backfill_venue_keys.resolve_candidate_identity(
            {
                ("alumni-gym", "VEN-000005"),
                ("alumni-gym-kentucky", "VEN-000005"),
            },
            self.venues_by_id,
        )
        self.assertEqual(
            resolved,
            (
                self.venues_by_id["VEN-000005"]["venue_key"],
                "VEN-000005",
            ),
        )

    def test_backfill_different_physical_ids_remains_unresolved(self):
        resolved = backfill_venue_keys.resolve_candidate_identity(
            {
                ("venue-a", "VEN-000005"),
                ("venue-b", "VEN-000006"),
            },
            self.venues_by_id,
        )
        self.assertIsNone(resolved)

    def test_builder_uses_global_project_display_name(self):
        names = build_site_data.load_venue_names(ROOT)
        assembly = self.venues_by_key["state-farm-center"]
        thompson = self.venues_by_key["thompson-boling-arena"]
        self.assertEqual(names[assembly["venue_id"]], "Assembly Hall")
        self.assertEqual(names[thompson["venue_id"]], "Thompson-Boling Arena")
        self.assertNotIn("state-farm-center", names)


if __name__ == "__main__":
    unittest.main()
