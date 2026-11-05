import csv
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import onboarding_plan  # noqa: E402
from location_safety import (  # noqa: E402
    parse_registry_fallback_markers,
    registry_fallback_marker,
    retire_registry_fallbacks,
)


class ReconciliationSiteMetadataResolutionTests(unittest.TestCase):
    def test_reused_venue_name_is_date_resolved_during_use_source(self):
        source = {
            "source_program_key": "depaul",
            "source_game_id": "TEST-CHARLOTTE",
            "season_label": "1991-1992",
            "game_date": "1991-12-07",
            "curated_venue_name": "Charlotte Coliseum",
            "city": "Charlotte",
            "state": "NC",
        }
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        venue_map = {
            "charlotte coliseum": [
                {
                    "venue_key": "charlotte-coliseum-1955",
                    "venue_id": "VEN-000040",
                    "city": "Charlotte",
                    "state": "NC",
                    "local_valid_from": "1976-03-13",
                    "local_valid_to": "1976-03-13",
                    "physical_opened": "1955",
                    "physical_closed": "1988",
                },
                {
                    "venue_key": "charlotte-coliseum-1988",
                    "venue_id": "VEN-000041",
                    "city": "Charlotte",
                    "state": "NC",
                    "local_valid_from": "1991-12-07",
                    "local_valid_to": "1991-12-07",
                    "physical_opened": "1988",
                    "physical_closed": "2005",
                },
            ]
        }

        onboarding_plan._sync_site_metadata_from_source(
            source,
            canonical,
            venue_map,
        )

        self.assertEqual(canonical["venue_key"], "charlotte-coliseum-1988")
        self.assertEqual(canonical["venue_id"], "VEN-000041")

    def test_resolved_physical_venue_registry_owns_canonical_geography(self):
        source = {
            "source_program_key": "depaul",
            "source_game_id": "TEST-ALLSTATE",
            "season_label": "2006-2007",
            "game_date": "2006-12-02",
            "curated_venue_name": "Allstate Arena",
            "city": "Chicago",
            "state": "IL",
        }
        canonical = {
            "site_type": "TEAM_A_HOME",
            "venue_key": "",
            "venue_id": "",
            "site_city": "Chicago",
            "site_state": "IL",
            "notes": "",
        }
        venue_map = {
            "allstate arena": [
                {
                    "venue_key": "allstate-arena",
                    "venue_id": "VEN-000004",
                    "city": "Rosemont",
                    "state": "IL",
                    "local_valid_from": "1980-12-01",
                    "local_valid_to": "2017-03-04",
                    "physical_opened": "1980",
                    "physical_closed": "",
                }
            ]
        }

        onboarding_plan._sync_site_metadata_from_source(
            source,
            canonical,
            venue_map,
        )

        self.assertEqual(canonical["venue_key"], "allstate-arena")
        self.assertEqual(canonical["venue_id"], "VEN-000004")
        self.assertEqual(canonical["site_city"], "Rosemont")
        self.assertEqual(canonical["site_state"], "IL")
        self.assertEqual(source["city"], "Chicago")

    def test_third_outcome_can_clear_temporary_venue_pair_and_old_marker(self):
        old_marker = registry_fallback_marker(
            "depaul",
            "DEPRAW-01277",
            "hearnes-center",
            "TEAM_B_HOME",
            ("venue_key", "venue_id", "site_city", "site_state"),
        )
        canonical = {
            "site_type": "TEAM_B_HOME",
            "designated_home_team_key": "missouri",
            "venue_key": "hearnes-center",
            "venue_id": "VEN-000077",
            "site_city": "Columbia",
            "site_state": "MO",
            "notes": old_marker,
        }

        retired = onboarding_plan._apply_canonical_patch(
            canonical,
            {
                "site_type": "NEUTRAL",
                "designated_home_team_key": "",
                "venue_key": "",
                "site_city": "Kansas City",
                "site_state": "MO",
            },
        )

        self.assertEqual(retired, 1)
        self.assertEqual(canonical["venue_key"], "")
        self.assertEqual(canonical["venue_id"], "")
        self.assertEqual(canonical["site_type"], "NEUTRAL")
        self.assertEqual(canonical["site_city"], "Kansas City")
        self.assertEqual(canonical["site_state"], "MO")
        self.assertNotIn("VENUE_REGISTRY_FALLBACK", canonical["notes"])

    def _fallback_fixture(self):
        marker = registry_fallback_marker(
            "test",
            "TESTRAW-1",
            "old-arena",
            "NEUTRAL",
            ("venue_key", "venue_id", "site_city", "site_state"),
        )
        canonical = {
            "canonical_game_id": "CBBG-1",
            "team_a_key": "other",
            "team_b_key": "test",
            "site_type": "NEUTRAL",
            "venue_key": "old-arena",
            "venue_id": "VEN-OLD",
            "site_city": "Old City",
            "site_state": "OS",
            "notes": marker,
        }
        assertion = {
            "canonical_game_id": "CBBG-1",
            "source_program_key": "test",
            "source_game_id": "TESTRAW-1",
            "normalized_opponent_key": "other",
            "game_date": "1940-01-01",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "Old Arena",
        }
        venue_metadata = {
            "old arena": [
                {
                    "venue_key": "old-arena",
                    "venue_id": "VEN-OLD",
                    "city": "Old City",
                    "state": "OS",
                    "local_valid_from": "",
                    "local_valid_to": "",
                    "physical_opened": "",
                    "physical_closed": "",
                }
            ],
        }
        return marker, canonical, assertion, venue_metadata

    def _marker_supported(self, canonical, assertion, venue_metadata):
        marker = parse_registry_fallback_markers(canonical["notes"])[0]
        return onboarding_plan._registry_fallback_marker_supported(
            canonical,
            marker,
            assertion,
            venue_metadata,
        )

    def _retire_if_unsupported(self, canonical, assertion, venue_metadata):
        cleaned, retired = retire_registry_fallbacks(
            canonical["notes"],
            lambda marker: not onboarding_plan._registry_fallback_marker_supported(
                canonical, marker, assertion, venue_metadata
            ),
        )
        canonical["notes"] = cleaned
        return retired

    def test_same_site_venue_clearing_retires_old_registry_fallback(self):
        _, canonical, assertion, venue_metadata = self._fallback_fixture()
        canonical["venue_key"] = ""
        canonical["venue_id"] = ""

        self.assertFalse(self._marker_supported(canonical, assertion, venue_metadata))
        self.assertEqual(
            self._retire_if_unsupported(canonical, assertion, venue_metadata),
            1,
        )
        self.assertNotIn("VENUE_REGISTRY_FALLBACK", canonical["notes"])

    def test_same_site_venue_replacement_retires_old_registry_fallback(self):
        _, canonical, assertion, venue_metadata = self._fallback_fixture()
        canonical["venue_key"] = "new-arena"
        canonical["venue_id"] = "VEN-NEW"
        canonical["site_city"] = "New City"
        canonical["site_state"] = "NS"

        self.assertFalse(self._marker_supported(canonical, assertion, venue_metadata))
        self.assertEqual(
            self._retire_if_unsupported(canonical, assertion, venue_metadata),
            1,
        )

    def test_same_site_location_replacement_or_clearing_retires_marker(self):
        for city, state in (("New City", "NS"), ("", "")):
            with self.subTest(city=city, state=state):
                _, canonical, assertion, venue_metadata = self._fallback_fixture()
                canonical["site_city"] = city
                canonical["site_state"] = state

                self.assertFalse(
                    self._marker_supported(canonical, assertion, venue_metadata)
                )
                self.assertEqual(
                    self._retire_if_unsupported(
                        canonical, assertion, venue_metadata
                    ),
                    1,
                )

    def test_still_valid_matching_registry_fallback_is_preserved(self):
        marker, canonical, assertion, venue_metadata = self._fallback_fixture()

        self.assertTrue(self._marker_supported(canonical, assertion, venue_metadata))
        self.assertEqual(
            self._retire_if_unsupported(canonical, assertion, venue_metadata),
            0,
        )
        self.assertEqual(canonical["notes"], marker)

    def test_exact_four_error_topology_is_retired_before_validation(self):
        _, canonical, assertion, venue_metadata = self._fallback_fixture()
        # This is the rehearsal failure shape: same H/A/N, but the approved
        # source/canonical patches clear the assertion venue and all four
        # registry-derived canonical fields while the old marker still claims them.
        assertion["curated_venue_name"] = ""
        canonical["venue_key"] = ""
        canonical["venue_id"] = ""
        canonical["site_city"] = ""
        canonical["site_state"] = ""
        marker = parse_registry_fallback_markers(canonical["notes"])[0]

        self.assertFalse(assertion["curated_venue_name"])
        self.assertNotEqual(canonical["venue_key"], marker["venue_key"])
        self.assertNotEqual(canonical["venue_id"], "VEN-OLD")
        self.assertNotEqual(
            (canonical["site_city"], canonical["site_state"]),
            ("Old City", "OS"),
        )
        self.assertFalse(self._marker_supported(canonical, assertion, venue_metadata))
        self.assertEqual(
            self._retire_if_unsupported(canonical, assertion, venue_metadata),
            1,
        )
        self.assertNotIn("VENUE_REGISTRY_FALLBACK", canonical["notes"])
    def test_nonblank_patch_cannot_silently_change_physical_venue(self):
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "old-arena",
            "venue_id": "VEN-OLD",
            "site_city": "Old City",
            "site_state": "IL",
            "notes": "",
        }
        with self.assertRaises(onboarding_plan.WorkflowError):
            onboarding_plan._apply_canonical_patch(
                canonical,
                {"venue_key": "different-arena"},
            )


class SealedGameSiteVenueRelationshipTests(unittest.TestCase):
    VENUE_FIELDS = [
        "source_program_key",
        "venue_key",
        "venue_id",
        "canonical_name",
        "aliases",
        "city",
        "state",
        "venue_type",
        "known_opened",
        "known_closed",
        "venue_date_precision",
        "games_currently_assigned",
        "first_assigned_game",
        "last_assigned_game",
        "relationship_type",
        "relationship_start",
        "relationship_end",
        "relationship_date_precision",
        "site_rule",
        "source_basis",
        "notes",
    ]

    def _write_csv(self, path, fieldnames, rows):
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _repo(self, root):
        self._write_csv(
            root / "data/reference/venues.csv",
            [
                "venue_id",
                "venue_key",
                "display_name",
                "city",
                "state",
                "opened",
                "closed",
                "date_precision",
                "identity_status",
                "source_basis",
                "notes",
            ],
            [
                {
                    "venue_id": "VEN-000999",
                    "venue_key": "example-arena",
                    "display_name": "Example Arena",
                    "city": "Example City",
                    "state": "EX",
                    "opened": "2007-09-08",
                    "closed": "",
                    "date_precision": "EXACT",
                    "identity_status": "CURATED_SEED",
                    "source_basis": "test",
                    "notes": "",
                }
            ],
        )
        self._write_csv(
            root / "data/reference/venue-names.csv",
            [
                "venue_id",
                "venue_name",
                "normalized_name",
                "name_type",
                "valid_from",
                "valid_to",
                "date_precision",
                "source_basis",
                "notes",
            ],
            [
                {
                    "venue_id": "VEN-000999",
                    "venue_name": "Example Arena",
                    "normalized_name": "additionfinancialarena",
                    "name_type": "PROJECT_DISPLAY",
                    "valid_from": "",
                    "valid_to": "",
                    "date_precision": "",
                    "source_basis": "test",
                    "notes": "",
                },
                {
                    "venue_id": "VEN-000999",
                    "venue_name": "Historic Example Arena",
                    "normalized_name": "ucfarena",
                    "name_type": "OFFICIAL_NAMING_PERIOD",
                    "valid_from": "2007-09-08",
                    "valid_to": "2013-05-22",
                    "date_precision": "EXACT",
                    "source_basis": "test",
                    "notes": "",
                },
            ],
        )
        self._write_csv(
            root / "schools/test/venues.csv",
            self.VENUE_FIELDS,
            [],
        )
        return root

    def _item(self):
        return {
            "decision_id": "DISCREPANCY-TEST-1-GAME_TYPE",
            "category": "discrepancy",
            "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
            "source_game_id": "TEST-1",
            "source_game_date": "2011-03-16",
            "resolution_basis": "Official host source identifies exact postseason site.",
            "source_patch": {
                "curated_venue_name": "Historic Example Arena",
                "city": "Example City",
                "state": "EX",
            },
            "venue_relationship_patch": {
                "venue_id": "VEN-000999",
                "venue_key": "example-arena",
            },
        }

    def test_sealed_game_site_relationship_enables_real_source_venue_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(Path(directory))
            item = self._item()
            approved = {"school_key": "test", "decisions": [item]}

            count = onboarding_plan._apply_sealed_game_site_venue_relationship_patches(
                repo,
                approved,
            )
            self.assertEqual(count, 1)

            with (repo / "schools/test/venues.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 1)
            row = rows[0]
            self.assertEqual(row["venue_id"], "VEN-000999")
            self.assertEqual(row["venue_key"], "example-arena")
            self.assertEqual(row["relationship_type"], "GAME_SITE")
            self.assertEqual(row["games_currently_assigned"], "1")
            self.assertEqual(row["first_assigned_game"], "2011-03-16")
            self.assertEqual(row["last_assigned_game"], "2011-03-16")
            self.assertEqual(row["aliases"], "Historic Example Arena")

            global_by_id, _, _ = onboarding_plan.load_global_venue_reference(repo)
            venue_map = onboarding_plan.ingest_school.load_venue_metadata_map(
                repo / "schools/test/venues.csv",
                global_by_id,
            )
            source = {
                "source_game_id": "TEST-1",
                "season_label": "2010-2011",
                "game_date": "2011-03-16",
                "curated_venue_name": "Historic Example Arena",
                "city": "Example City",
                "state": "EX",
            }
            resolved = onboarding_plan.ingest_school.resolve_venue_metadata(
                source,
                venue_map,
            )
            self.assertEqual(resolved["venue_id"], "VEN-000999")
            self.assertEqual(resolved["venue_key"], "example-arena")

    def test_relationship_patch_rejects_unknown_or_mismatched_global_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(Path(directory))
            item = self._item()
            item["venue_relationship_patch"] = {
                "venue_id": "VEN-999999",
                "venue_key": "example-arena",
            }
            with self.assertRaisesRegex(
                onboarding_plan.WorkflowError,
                "existing global venue_id/venue_key pair",
            ):
                onboarding_plan._validate_game_site_venue_relationship_patch(
                    repo,
                    "test",
                    item,
                    item["source_patch"],
                    item["venue_relationship_patch"],
                )

    def test_relationship_patch_rejects_unregistered_name_and_locality_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(Path(directory))
            item = self._item()
            bad_name = dict(item["source_patch"], curated_venue_name="Unknown Arena")
            with self.assertRaisesRegex(
                onboarding_plan.WorkflowError,
                "does not resolve uniquely",
            ):
                onboarding_plan._validate_game_site_venue_relationship_patch(
                    repo,
                    "test",
                    item,
                    bad_name,
                    item["venue_relationship_patch"],
                )

            bad_location = dict(item["source_patch"], city="Tampa")
            with self.assertRaisesRegex(
                onboarding_plan.WorkflowError,
                "locality does not match",
            ):
                onboarding_plan._validate_game_site_venue_relationship_patch(
                    repo,
                    "test",
                    item,
                    bad_location,
                    item["venue_relationship_patch"],
                )

    def test_relationship_patch_rejects_redundant_target_identity(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = self._repo(Path(directory))
            item = self._item()
            onboarding_plan._apply_sealed_game_site_venue_relationship_patches(
                repo,
                {"school_key": "test", "decisions": [item]},
            )
            with self.assertRaisesRegex(
                onboarding_plan.WorkflowError,
                "redundant",
            ):
                onboarding_plan._validate_game_site_venue_relationship_patch(
                    repo,
                    "test",
                    item,
                    item["source_patch"],
                    item["venue_relationship_patch"],
                )


if __name__ == "__main__":
    unittest.main()
