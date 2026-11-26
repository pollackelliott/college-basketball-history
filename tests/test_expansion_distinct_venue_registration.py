"""Generic exact-source tests for the keyed historical-venue split exception."""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from onboarding_plan import WorkflowError
from expansion_distinct_venue_registration import (
    ACTION, canonical, sha, validate_distinct_keyed_registration,
)
from stage1_venue_reconciliation import load_venue_reconciliation
from stage_research_portfolio import (
    rebase_venues, research_declares_registration_only_pending,
    venue_reconciliation_inventory,
)
from all_history_expansion_venue_guard import census as venue_guard_census


def csv_bytes(rows):
    fields = list(rows[0])
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


class DistinctKeyedPhysicalVenueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.local = {
            "source_program_key": "example",
            "venue_key": "historic-academic-hall",
            "venue_id": "",
            "canonical_name": "Old Academic Hall",
            "aliases": "Academic Hall",
            "city": "Testville", "state": "CA",
            "venue_type": "gymnasium",
            "known_opened": "1921", "known_closed": "1938",
            "venue_date_precision": "YEAR",
            "games_currently_assigned": "30",
            "first_assigned_game": "", "last_assigned_game": "",
            "relationship_type": "primary_home",
            "relationship_start": "1921-1922",
            "relationship_end": "1936-1937",
            "relationship_date_precision": "SEASON",
            "site_rule": "Only independently established HOME games",
            "source_basis": "https://example.edu/archive/old-hall",
            "notes": "Separate early campus hall completed 1921; current-day hall opened 1977.",
        }
        self.incumbent = {
            "venue_id": "VEN-000500",
            "venue_key": "new-academic-center",
            "display_name": "New Academic Center",
            "city": "Testville", "state": "CA",
            "opened": "1977", "closed": "",
            "date_precision": "YEAR", "identity_status": "RESEARCHED",
            "source_basis": "https://example.edu/modern-hall",
            "notes": "Separate 1977 physical building.",
        }
        self.aliases = [
            {
                "venue_id": self.incumbent["venue_id"],
                "venue_name": name,
                "normalized_name": normalized,
                "name_type": kind,
                "valid_from": "", "valid_to": "", "date_precision": "",
                "source_basis": "https://example.edu/modern-hall",
                "notes": "Existing published alias.",
            }
            for name, normalized, kind in [
                ("New Academic Center", "newacademiccenter", "PROJECT_DISPLAY"),
                ("Academic Hall", "academichall", "HISTORICAL_OR_ALIAS"),
            ]
        ]
        self.sources = [{
            "source_game_id": "S-1",
            "source_program_key": "example",
            "season_label": "1922-1923",
            "curated_venue_name": "Old Academic Hall",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "game_date": "1922-12-01",
        }]
        self.source_raw = csv_bytes(self.sources)
        self.support = {
            "support_id": "EXP-VEN-0001",
            "support_action": "NEW_SUPPLEMENTAL",
            "venue_key": self.local["venue_key"],
            "baseline_row_sha256": "",
            "changed_fields": "",
            "candidate_row_json": json.dumps(
                self.local, sort_keys=True, separators=(",", ":")
            ),
            "evidence_basis": "Accepted historical source and venue archaeology.",
        }
        self.venue_raw = csv_bytes([self.local])
        self.package = self.root / "research.zip"
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", self.venue_raw)
            z.writestr("source-games.csv", self.source_raw)
            z.writestr("expansion-venues.csv", csv_bytes([self.support]))
        self.spec = self.root / "venue.json"
        self.mapping = {
            "action": ACTION,
            "local_venue_key": self.local["venue_key"],
            "expected_local_name": self.local["canonical_name"],
            "expected_local_city": self.local["city"],
            "expected_local_state": self.local["state"],
            "resolution_basis": "Explicit approved Control Center venue separation",
            "new_global_venue_key": self.local["venue_key"],
            "source_support_id": self.support["support_id"],
            "source_support_row": self.support,
            "source_support_row_sha256": sha(self.support),
            "expected_local_row_sha256": sha(self.local),
            "expected_source_games_sha256": hashlib.sha256(self.source_raw).hexdigest(),
            "conflicting_global_venue_id": self.incumbent["venue_id"],
            "conflicting_global_venue_key": self.incumbent["venue_key"],
            "expected_conflicting_global_row_sha256": sha(self.incumbent),
            "expected_conflicting_global_name_rows_sha256": sha(sorted(
                self.aliases, key=canonical
            )),
            "expected_conflicting_global_opened": self.incumbent["opened"],
            "expected_conflicting_global_closed": self.incumbent["closed"],
            "physical_separation_basis": (
                "Institutional 1921 original building versus newly built 1977 hall"
            ),
            "excluded_global_alias_names": ["Academic Hall"],
        }
        self.doc = {
            "schema_version": 3,
            "school_key": "example",
            "owner_approval_basis": "https://github.com/example/repo/issues/722",
            "expected_research_zip_sha256": hashlib.sha256(
                self.package.read_bytes()
            ).hexdigest(),
            "expected_venues_sha256": hashlib.sha256(self.venue_raw).hexdigest(),
            "mappings": [self.mapping],
        }
        self.save()

    def save(self):
        self.spec.write_text(json.dumps(self.doc, indent=2) + "\n")

    def load(self, **kwargs):
        self.save()
        return load_venue_reconciliation(
            self.spec,
            school_key="example",
            package_path=self.package,
            local_venues=[self.local],
            global_venues=[self.incumbent],
            global_name_rows=self.aliases,
            **kwargs,
        )

    def test_full_exact_freeze_to_preview_to_registration(self):
        original = copy.deepcopy((self.local, self.incumbent, self.aliases))
        m, meta = self.load()
        self.assertEqual(m[self.local["venue_key"]]["action"], ACTION)
        self.assertEqual(meta["schema_version"], 3)
        inventory = venue_reconciliation_inventory(
            [self.local], [self.incumbent], self.aliases,
            venue_reconciliation=m,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(inventory["classification_counts"], {
            "NEW_GLOBAL_IDENTITY": 1
        })
        self.assertEqual(venue_guard_census(
            [self.local], [self.incumbent], self.aliases, m
        )["blocker_count"], 0)
        school, registry, names, mapping = rebase_venues(
            "example", [dict(self.local)], [dict(self.incumbent)],
            [dict(x) for x in self.aliases],
            venue_reconciliation=m, source_games=self.sources,
        )
        self.assertEqual(school[0]["venue_key"], self.local["venue_key"])
        self.assertEqual(school[0]["venue_id"], "VEN-000501")
        self.assertEqual(school[0]["aliases"], "Academic Hall")
        self.assertEqual(school[0]["relationship_start"], "1921-1922")
        self.assertEqual(school[0]["relationship_end"], "1936-1937")
        self.assertEqual(registry[0], self.incumbent)
        self.assertEqual(names[:len(self.aliases)], self.aliases)
        self.assertNotIn(
            ("VEN-000501", "academichall"),
            {(x["venue_id"], x["normalized_name"]) for x in names},
        )
        self.assertIn(
            ("VEN-000500", "academichall"),
            {(x["venue_id"], x["normalized_name"]) for x in names},
        )
        self.assertEqual(mapping[0]["resolution"], "NEW_GLOBAL_IDENTITY_DISTINCT_KEYED")
        self.assertEqual((self.local, self.incumbent, self.aliases), original)
        # Independent Phase 0 preview replays the exact same frozen spec and
        # projected source rows without a second research ZIP transport.
        preview, replay = load_venue_reconciliation(
            self.spec,
            school_key="example",
            package_path=None,
            expected_package_sha256=self.doc["expected_research_zip_sha256"],
            frozen_venues_bytes=self.venue_raw,
            source_games_bytes=self.source_raw,
            local_venues=[self.local], global_venues=[self.incumbent],
            global_name_rows=self.aliases,
        )
        self.assertEqual(m, preview)
        self.assertEqual(meta["mappings"], replay["mappings"])

    def test_without_explicit_authority_remains_blocked(self):
        result = venue_reconciliation_inventory(
            [self.local], [self.incumbent], self.aliases
        )
        self.assertEqual(result["blocker_count"], 1)
        self.assertEqual(result["blockers"][0]["classification"], "STOP_AMBIGUOUS")
        self.assertGreater(venue_guard_census(
            [self.local], [self.incumbent], self.aliases
        )["blocker_count"], 0)

    def test_hash_bound_integrity_and_owner_scope(self):
        for key, bad in (
            ("source_support_row_sha256", "0"*64),
            ("expected_local_row_sha256", "0"*64),
            ("expected_source_games_sha256", "0"*64),
            ("expected_conflicting_global_row_sha256", "0"*64),
            ("expected_conflicting_global_name_rows_sha256", "0"*64),
            ("new_global_venue_key", "new-academic-center"),
            ("conflicting_global_venue_id", "VEN-000001"),
            ("conflicting_global_venue_key", "other"),
            ("expected_conflicting_global_opened", "1960"),
            ("excluded_global_alias_names", ["Nonexistent Alias"]),
        ):
            original = self.doc["mappings"][0][key]
            self.doc["mappings"][0][key] = bad
            with self.subTest(key=key), self.assertRaises(WorkflowError):
                self.load()
            self.doc["mappings"][0][key] = original
        self.doc["mappings"][0]["unapproved_extra"] = "smuggled"
        with self.assertRaisesRegex(WorkflowError, "FIELD_SET_INVALID"):
            self.load()

    def test_modified_original_freeze_support_or_package_fails(self):
        self.doc["expected_research_zip_sha256"] = "0"*64
        with self.assertRaisesRegex(WorkflowError, "package SHA"):
            self.load()
        self.doc["expected_research_zip_sha256"] = hashlib.sha256(
            self.package.read_bytes()
        ).hexdigest()
        self.doc["mappings"][0]["source_support_row"]["evidence_basis"] = "tampered"
        with self.assertRaisesRegex(WorkflowError, "SUPPORT_ROW_HASH_MISMATCH"):
            self.load()

    def test_chronology_cannot_overlap_or_be_inferred(self):
        for change in ("1935", "", "1977", "2000"):
            original = self.incumbent["opened"]
            self.incumbent["opened"] = change
            self.mapping["expected_conflicting_global_opened"] = change
            self.mapping["expected_conflicting_global_row_sha256"] = sha(self.incumbent)
            with self.subTest(opened=change), self.assertRaises(WorkflowError):
                self.load()
            self.incumbent["opened"] = original
            self.mapping["expected_conflicting_global_opened"] = original
            self.mapping["expected_conflicting_global_row_sha256"] = sha(self.incumbent)

    def test_same_physical_building_cannot_register_twice(self):
        other = copy.deepcopy(self.local)
        with self.assertRaisesRegex(WorkflowError, "LOCAL_KEY_NOT_UNIQUE"):
            validate_distinct_keyed_registration(
                self.mapping, self.local, [self.local, other],
                [self.incumbent], self.aliases,
                frozen_support_rows=[self.support],
                source_games_sha256=hashlib.sha256(self.source_raw).hexdigest(),
                school_key="example",
            )

    def test_other_same_locality_match_is_not_silenced(self):
        extra = dict(
            self.incumbent, venue_id="VEN-000400",
            venue_key="another-campus-hall",
            display_name="Old Academic Hall",
        )
        with self.assertRaisesRegex(WorkflowError, "ADDITIONAL_PHYSICAL_MATCHES"):
            validate_distinct_keyed_registration(
                self.mapping, self.local, [self.local],
                [self.incumbent, extra], self.aliases,
                frozen_support_rows=[self.support],
                source_games_sha256=hashlib.sha256(self.source_raw).hexdigest(),
                school_key="example",
            )


class SettledPendingRegistrationsTests(unittest.TestCase):
    def setUp(self):
        self.local = {
            "source_program_key": "test-school",
            "venue_key": "test-opponent-gym",
            "venue_id": "", "canonical_name": "Opponent Gymnasium",
            "aliases": "Older Opponent Gym",
            "city": "Somewhere", "state": "CA",
            "source_basis": "https://example.edu/official-facility",
            "site_rule": "One accepted exact postseason opponent-host site",
            "relationship_type": "POSTSEASON_GAME_SITE",
            "relationship_date_precision": "EXACT_GAME_SET",
            "games_currently_assigned": "2",
            "notes": "Documented opponent gym; global venue registration pending current-main rebase.",
            "first_assigned_game": "1992-03-03",
            "last_assigned_game": "1992-03-07",
            "known_opened": "1967",
            "known_closed": "",
            "venue_date_precision": "YEAR",
            "relationship_start": "", "relationship_end": "",
            "venue_type": "gymnasium",
        }

    def test_documented_registration_only_does_not_require_magic_phrase(self):
        self.assertTrue(research_declares_registration_only_pending(self.local))
        inventory = venue_reconciliation_inventory([self.local], [], [])
        self.assertEqual(inventory["classification_counts"], {
            "NEW_GLOBAL_IDENTITY": 1,
        })
        final, global_rows, aliases, mapped = rebase_venues(
            "test-school", [dict(self.local)], [], []
        )
        self.assertEqual(final[0]["venue_id"], "VEN-000001")
        self.assertEqual(global_rows[0]["venue_key"], "test-opponent-gym")
        self.assertEqual(mapped[0]["resolution"], "NEW_GLOBAL_IDENTITY")

    def test_registration_ambiguity_or_insufficient_evidence_remains_blocked(self):
        for key, change in (
            ("source_basis", ""),
            ("relationship_date_precision", ""),
            ("relationship_type", ""),
            ("city", ""),
            ("venue_key", ""),
            ("games_currently_assigned", "0"),
            ("notes", "Global registration pending; but reuse decision remains"),
        ):
            candidate = dict(self.local, **{key:change})
            with self.subTest(key=key):
                self.assertFalse(research_declares_registration_only_pending(candidate))


if __name__ == "__main__":
    unittest.main()
