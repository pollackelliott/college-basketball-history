import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remediate_oklahoma_home_history import (  # noqa: E402
    CANONICAL_ONLY_OKLAHOMA_HOME,
    RECONCILED_NON_OKLAHOMA_HOME,
    TRANSITION_1927_28_OVERRIDES,
    facility_key_for,
    oklahoma_home,
    resolved_site_discrepancy,
    site_patch,
)


class OklahomaHomeChronologyTests(unittest.TestCase):
    def test_primary_era_boundaries(self):
        self.assertEqual(
            facility_key_for({"season_label": "1907-1908", "game_date": ""}),
            ("ou-gymnasium", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1919-1920", "game_date": ""}),
            ("ou-rotc-armory", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1928-1929", "game_date": ""}),
            ("mccasland-field-house", None),
        )
        self.assertEqual(
            facility_key_for({"season_label": "1974-1975", "game_date": ""}),
            ("mccasland-field-house", None),
        )

    def test_1928_transition_is_date_aware_when_date_exists(self):
        self.assertEqual(
            facility_key_for(
                {"season_label": "1927-1928", "game_date": "1928-01-12"}
            ),
            ("ou-rotc-armory", None),
        )
        self.assertEqual(
            facility_key_for(
                {"season_label": "1927-1928", "game_date": "1928-01-13"}
            ),
            ("mccasland-field-house", None),
        )

    def test_1928_verified_sequence_overrides_exact_eight_source_rows(self):
        self.assertEqual(len(TRANSITION_1927_28_OVERRIDES), 8)
        self.assertEqual(
            TRANSITION_1927_28_OVERRIDES["OKLRAW-00274"],
            "ou-rotc-armory",
        )
        self.assertEqual(
            TRANSITION_1927_28_OVERRIDES["OKLRAW-00275"],
            "ou-rotc-armory",
        )
        self.assertEqual(
            TRANSITION_1927_28_OVERRIDES["OKLRAW-00279"],
            "mccasland-field-house",
        )
        for source_id in (
            "OKLRAW-00281",
            "OKLRAW-00284",
            "OKLRAW-00285",
            "OKLRAW-00286",
            "OKLRAW-00291",
        ):
            self.assertEqual(
                facility_key_for(
                    {
                        "source_game_id": source_id,
                        "season_label": "1927-1928",
                        "game_date": "",
                    }
                ),
                ("mccasland-field-house", None),
            )

    def test_unverified_1928_undated_row_still_holds(self):
        key, reason = facility_key_for(
            {
                "source_game_id": "OKLRAW-UNLISTED",
                "season_label": "1927-1928",
                "game_date": "",
            }
        )
        self.assertIsNone(key)
        self.assertEqual(
            reason,
            "1927-28_transition_missing_date_not_in_verified_sequence",
        )

    def test_1975_transition_is_date_aware(self):
        self.assertEqual(
            facility_key_for(
                {"season_label": "1975-1976", "game_date": "1975-11-30"}
            ),
            ("mccasland-field-house", None),
        )
        self.assertEqual(
            facility_key_for(
                {"season_label": "1975-1976", "game_date": "1975-12-01"}
            ),
            ("lloyd-noble-center", None),
        )
        key, reason = facility_key_for(
            {"season_label": "1975-1976", "game_date": ""}
        )
        self.assertIsNone(key)
        self.assertEqual(reason, "1975-76_transition_missing_date")

    def test_modern_blank_is_not_blanket_lloyd_noble(self):
        key, reason = facility_key_for(
            {"season_label": "2012-2013", "game_date": "2012-12-31"}
        )
        self.assertIsNone(key)
        self.assertEqual(reason, "post_1975_primary_history_not_sufficient")

    def test_oklahoma_home_requires_independent_site_classification(self):
        self.assertTrue(
            oklahoma_home(
                {
                    "site_type": "TEAM_A_HOME",
                    "team_a_key": "oklahoma",
                    "team_b_key": "texas",
                }
            )
        )
        self.assertFalse(
            oklahoma_home(
                {
                    "site_type": "UNKNOWN",
                    "team_a_key": "oklahoma",
                    "team_b_key": "texas",
                }
            )
        )

    def test_site_patch_fills_blanks_but_refuses_conflicts(self):
        facility = {
            "venue_key": "ou-gymnasium",
            "venue_id": "VEN-000341",
            "display_name": "OU Gymnasium",
            "city": "Norman",
            "state": "OK",
        }
        patch, conflict = site_patch(
            {
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
            },
            facility,
            canonical=True,
        )
        self.assertIsNone(conflict)
        self.assertEqual(patch["venue_key"], "ou-gymnasium")
        self.assertEqual(patch["venue_id"], "VEN-000341")
        self.assertEqual(
            (patch["site_city"], patch["site_state"]),
            ("Norman", "OK"),
        )

        patch, conflict = site_patch(
            {
                "venue_key": "other-arena",
                "venue_id": "VEN-999999",
                "site_city": "Norman",
                "site_state": "OK",
            },
            facility,
            canonical=True,
        )
        self.assertEqual(patch, {})
        self.assertTrue(conflict.startswith("existing_canonical_venue_key:"))

    def test_source_site_patch_does_not_require_canonical_agreement(self):
        facility = {
            "venue_key": "ou-rotc-armory",
            "venue_id": "VEN-000342",
            "display_name": "R.O.T.C. Armory",
            "city": "Norman",
            "state": "OK",
        }
        patch, conflict = site_patch(
            {
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "",
                "city": "",
                "state": "",
            },
            facility,
            canonical=False,
        )
        self.assertIsNone(conflict)
        self.assertEqual(patch["curated_venue_name"], "R.O.T.C. Armory")
        self.assertEqual((patch["city"], patch["state"]), ("Norman", "OK"))

    def test_exact_reconciled_source_conflict_universe_is_two(self):
        self.assertEqual(
            set(RECONCILED_NON_OKLAHOMA_HOME),
            {"OKLRAW-00218", "OKLRAW-01226"},
        )
        self.assertEqual(
            RECONCILED_NON_OKLAHOMA_HOME["OKLRAW-00218"]["discrepancy_id"],
            "DISC-001890",
        )
        self.assertEqual(
            RECONCILED_NON_OKLAHOMA_HOME["OKLRAW-01226"]["discrepancy_id"],
            "DISC-001918",
        )

    def test_exact_canonical_only_universe_is_1942_kansas_game(self):
        self.assertEqual(set(CANONICAL_ONLY_OKLAHOMA_HOME), {"CBBG-0012117"})
        item = CANONICAL_ONLY_OKLAHOMA_HOME["CBBG-0012117"]
        self.assertEqual(item["discrepancy_id"], "DISC-001901")
        self.assertEqual(item["facility_key"], "mccasland-field-house")

    def test_resolved_site_discrepancy_requires_exact_resolution(self):
        rows = {
            "DISC-X": {
                "discrepancy_id": "DISC-X",
                "canonical_game_id": "CBBG-X",
                "field_name": "site_type",
                "source_a_program_key": "oklahoma",
                "canonical_value": "TEAM_B_HOME",
                "status": "RESOLVED",
                "resolution_basis": "Reciprocal official source establishes Norman.",
            }
        }
        resolved = resolved_site_discrepancy(
            rows,
            discrepancy_id="DISC-X",
            canonical_game_id="CBBG-X",
            canonical_site_type="TEAM_B_HOME",
        )
        self.assertEqual(resolved["status"], "RESOLVED")

        bad = dict(rows["DISC-X"])
        bad["status"] = "UNDER_REVIEW"
        with self.assertRaises(RuntimeError):
            resolved_site_discrepancy(
                {"DISC-X": bad},
                discrepancy_id="DISC-X",
                canonical_game_id="CBBG-X",
                canonical_site_type="TEAM_B_HOME",
            )


if __name__ == "__main__":
    unittest.main()
