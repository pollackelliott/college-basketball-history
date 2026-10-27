import sys
import unittest
from unittest import mock
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import (  # noqa: E402
    _record_reconciled_unresolved_home_venue_markers,
    _sync_explicit_source_site_patch_to_canonical,
    _sync_site_metadata_from_source,
)


class ReconciliationHomeExceptionPropagationTests(unittest.TestCase):
    def test_use_source_home_sync_propagates_researched_unresolved_marker(self):
        source = {
            "source_program_key": "kansas-state",
            "source_game_id": "KSTATE-1",
            "normalized_opponent_key": "nebraska",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "",
            "city": "Manhattan",
            "state": "KS",
            "curated_game_type": "REGULAR_SEASON",
            "site_research_status": "RESEARCHED_UNRESOLVED_HOME_VENUE",
            "site_research_basis": (
                "Exhaustive historical research established Manhattan home "
                "status but not the exact physical building."
            ),
        }

        canonical = {
            "team_a_key": "kansas-state",
            "team_b_key": "nebraska",
            "site_type": "TEAM_A_HOME",
            "designated_home_team_key": "kansas-state",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }

        _sync_site_metadata_from_source(
            source,
            canonical,
            {},
        )

        marker = (
            "[RESEARCHED_UNRESOLVED_HOME_VENUE "
            "source=kansas-state/KSTATE-1]"
        )

        self.assertEqual(canonical["venue_key"], "")
        self.assertEqual(canonical["venue_id"], "")
        self.assertEqual(canonical["site_city"], "Manhattan")
        self.assertEqual(canonical["site_state"], "KS")
        self.assertIn(marker, canonical["notes"])

        # Repeating reconciliation must remain idempotent.
        _sync_site_metadata_from_source(
            source,
            canonical,
            {},
        )
        self.assertEqual(canonical["notes"].count(marker), 1)


    def test_explicit_source_site_patch_propagates_to_canonical(self):
        source = {
            "source_program_key": "test",
            "source_game_id": "TEST-1",
            "normalized_opponent_key": "other",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "Example Fieldhouse",
            "city": "Example City",
            "state": "EX",
        }
        canonical = {
            "team_a_key": "other",
            "team_b_key": "test",
            "site_type": "TEAM_B_HOME",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        venue_map = {
            "example fieldhouse": {
                "venue_key": "example-fieldhouse",
                "venue_id": "VEN-1",
                "city": "Example City",
                "state": "EX",
            }
        }
        _sync_explicit_source_site_patch_to_canonical(
            source,
            canonical,
            venue_map,
            {"curated_venue_name", "city", "state"},
        )
        self.assertEqual(canonical["venue_key"], "example-fieldhouse")
        self.assertEqual(canonical["venue_id"], "VEN-1")
        self.assertEqual(canonical["site_city"], "Example City")
        self.assertEqual(canonical["site_state"], "EX")

    def test_normalized_site_patch_bypasses_redundant_agreement_recheck(self):
        source = {
            "source_program_key": "test",
            "source_game_id": "TEST-1",
            "normalized_opponent_key": "other",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "Example Fieldhouse",
            "city": "Example City",
            "state": "EX",
            "game_date": "1946-02-01",
        }
        canonical = {
            "team_a_key": "other",
            "team_b_key": "test",
            "site_type": "TEAM_B_HOME",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        venue_map = {
            "example fieldhouse": {
                "venue_key": "example-fieldhouse",
                "venue_id": "VEN-1",
                "city": "Example City",
                "state": "EX",
            }
        }

        # The site_type NORMALIZE_SOURCE_TO_CANONICAL decision has already
        # established agreement. A later redundant orientation re-check must
        # not suppress the explicit owner-approved venue/locality patch.
        with mock.patch(
            "onboarding_plan._assertion_site_to_canonical",
            return_value="UNKNOWN",
        ):
            _sync_explicit_source_site_patch_to_canonical(
                source,
                canonical,
                venue_map,
                {"curated_venue_name", "city", "state"},
                site_agreement_guaranteed=True,
            )

        self.assertEqual(canonical["venue_key"], "example-fieldhouse")
        self.assertEqual(canonical["venue_id"], "VEN-1")
        self.assertEqual(canonical["site_city"], "Example City")
        self.assertEqual(canonical["site_state"], "EX")

    def test_unproven_site_patch_still_requires_agreement(self):
        source = {
            "source_program_key": "test",
            "source_game_id": "TEST-1",
            "normalized_opponent_key": "other",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "Example Fieldhouse",
            "city": "Example City",
            "state": "EX",
            "game_date": "1946-02-01",
        }
        canonical = {
            "team_a_key": "other",
            "team_b_key": "test",
            "site_type": "TEAM_B_HOME",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        venue_map = {
            "example fieldhouse": {
                "venue_key": "example-fieldhouse",
                "venue_id": "VEN-1",
                "city": "Example City",
                "state": "EX",
            }
        }

        with mock.patch(
            "onboarding_plan._assertion_site_to_canonical",
            return_value="UNKNOWN",
        ):
            _sync_explicit_source_site_patch_to_canonical(
                source,
                canonical,
                venue_map,
                {"curated_venue_name", "city", "state"},
            )

        self.assertEqual(canonical["venue_key"], "")
        self.assertEqual(canonical["venue_id"], "")
        self.assertEqual(canonical["site_city"], "")
        self.assertEqual(canonical["site_state"], "")

    def test_reconciled_researched_unknown_home_adds_marker(self):
        canonical = {
            "canonical_game_id": "CBBG-1",
            "team_a_key": "other",
            "team_b_key": "test",
            "site_type": "TEAM_B_HOME",
            "venue_key": "",
            "venue_id": "",
            "site_city": "Example City",
            "site_state": "EX",
            "game_type": "REGULAR_SEASON",
            "notes": "",
        }
        source = {
            "source_program_key": "test",
            "source_game_id": "TEST-1",
            "normalized_opponent_key": "other",
            "curated_site_type": "UNKNOWN",
            "site_research_status": "RESEARCHED_UNRESOLVED",
            "site_research_basis": "Bounded H/A/N research remains unresolved.",
        }
        reciprocal = {
            "canonical_game_id": "CBBG-1",
            "source_program_key": "other",
            "source_game_id": "OTHER-1",
            "normalized_opponent_key": "test",
            "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": "",
            "city": "",
            "state": "",
        }
        discrepancy = {
            "canonical_game_id": "CBBG-1",
            "field_name": "site_type",
            "source_a_program_key": "test",
            "status": "RESOLVED",
            "resolution_basis": "Reciprocal source establishes canonical HOME.",
        }
        item = {
            "decision_id": "DISCREPANCY-TEST-1-SITE_TYPE",
            "canonical_game_id": "CBBG-1",
            "source_game_id": "TEST-1",
            "field_name": "site_type",
            "decision": "KEEP_CANONICAL",
            "canonical_patch": {
                "site_city": "Example City",
                "site_state": "EX",
            },
        }
        counts = _record_reconciled_unresolved_home_venue_markers(
            "test", [item], {"CBBG-1": canonical}, {"TEST-1": source},
            [reciprocal], [discrepancy],
        )
        self.assertEqual(
            counts["reconciled_unknown_site_home_venue_markers_added"], 1
        )
        self.assertIn(
            "[RECONCILED_UNKNOWN_SITE_HOME_VENUE "
            "source=test/TEST-1 reciprocal=other/OTHER-1]",
            canonical["notes"],
        )
        self.assertEqual(source["curated_site_type"], "UNKNOWN")


if __name__ == "__main__":
    unittest.main()
