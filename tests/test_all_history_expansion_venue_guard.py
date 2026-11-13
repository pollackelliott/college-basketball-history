"""Adverse and acceptance regression for expansion venue identity guard."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"tools"))

from all_history_expansion_venue_guard import census, require_clean, ExpansionVenueConflict


class ExpansionVenueGuardTest(unittest.TestCase):
    def setUp(self):
        self.registered=[
            {"venue_id":"VEN-000934","venue_key":"retriever-activities-center",
             "display_name":"Retriever Activities Center (RAC) Arena",
             "city":"Catonsville","state":"MD"},
            {"venue_id":"VEN-000933","venue_key":"towson-center",
             "display_name":"Towson Center","city":"Towson","state":"MD"}]
        self.aliases=[
            {"venue_id":"VEN-000934","venue_name":"UMBC Fieldhouse",
             "normalized_name":"umbcfieldhouse","name_type":"HISTORICAL_OR_ALIAS"},
            {"venue_id":"VEN-000933","venue_name":"Towson Center",
             "normalized_name":"towsoncenter","name_type":"PROJECT_DISPLAY"}]
        self.umbc={"venue_key":"umbc-fieldhouse","canonical_name":"UMBC Fieldhouse",
                   "aliases":"","city":"Baltimore","state":"MD"}
        self.towson={"venue_key":"towson-center","canonical_name":"Towson Center",
                     "aliases":"","city":"Towson","state":"MD"}

    def test_umbc_case_blocks_without_choosing_same_or_different_physical_identity(self):
        outcome=census([self.umbc],self.registered,self.aliases)
        self.assertEqual(outcome["status"],"BLOCKED_VENUE_IDENTITY_RECONCILIATION")
        self.assertEqual(outcome["blocker_count"],1)
        row=outcome["blockers"][0]
        self.assertEqual(row["class"],"VENUE_POTENTIAL_EXISTING_PHYSICAL_IDENTITY")
        self.assertEqual(row["global_venue_id"],"VEN-000934")
        self.assertEqual((row["local_city"],row["registered_city"]),
                         ("Baltimore","Catonsville"))
        self.assertIn("HISTORICAL_OR_ALIAS",row["registered_alias_types"])
        self.assertFalse(row["locality_agrees"])
        with self.assertRaisesRegex(ExpansionVenueConflict,"umbc-fieldhouse"):
            require_clean(outcome)

    def test_registered_exact_key_and_locality_is_usable(self):
        outcome=census([self.towson],self.registered,self.aliases)
        self.assertEqual(outcome["status"],"PASS")
        self.assertEqual(require_clean(outcome)["rows"][0]["existing_key_reuse_id"],
                         "VEN-000933")

    def test_known_new_distinct_local_venue_can_register(self):
        outcome=census([dict(self.umbc,venue_key="new-unique-gym",
                              canonical_name="Unique Town Gym")],
                       self.registered,self.aliases)
        self.assertEqual(outcome["status"],"PASS")
        self.assertEqual(outcome["blocker_count"],0)

    def test_same_locality_alias_under_other_key_does_not_silently_reuse(self):
        venue=dict(self.umbc,city="Catonsville")
        outcome=census([venue],self.registered,self.aliases)
        self.assertEqual(outcome["blocker_count"],1)
        self.assertTrue(outcome["blockers"][0]["locality_agrees"])

    def test_alias_in_secondary_local_names_triggers_conflict(self):
        venue=dict(self.umbc,canonical_name="Alternative Gym",aliases="UMBC Fieldhouse;Short Name")
        self.assertEqual(census([venue],self.registered,self.aliases)["blocker_count"],1)

    def test_duplicate_new_key_blocks(self):
        venue=dict(self.umbc,venue_key="new-town-gym",canonical_name="Unique Town Gym")
        outcome=census([venue,dict(venue,city="Other")],self.registered,self.aliases)
        self.assertIn("VENUE_NEW_SUPPORT_DUPLICATE_KEY",
                      {x["class"] for x in outcome["blockers"]})

    def test_exact_key_locality_conflict_blocks(self):
        venue=dict(self.towson,city="Baltimore")
        outcome=census([venue],self.registered,self.aliases)
        self.assertIn("VENUE_EXACT_KEY_LOCALITY_CONFLICT",
                      {x["class"] for x in outcome["blockers"]})

    def test_duplicate_global_ids_block(self):
        venue=dict(self.umbc,venue_key="unknown",canonical_name="Unique Town Gym")
        outcome=census([venue],self.registered,self.aliases)
        self.assertEqual(outcome["status"],"PASS")
        r=census([self.umbc,self.towson],self.registered,self.aliases)
        self.assertEqual(r["blocker_count"],1)
        self.assertEqual(r["new_support_count"],2)
