"""Exact approved Lahaina site transaction regression and drift rejection."""
import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from maintenance_lahaina_2019 import (
    CURRENT, EXPECTED, NEW, VENUE, patch_rows, validate_venue,
)


def row(gid):
    return {"canonical_game_id": gid, **EXPECTED[gid], **CURRENT,
            "team_a_score": "93", "team_b_score": "63", "notes": "literal preservation"}


class LahainaSiteMaintenanceTests(unittest.TestCase):
    def test_only_four_fields_change_in_exactly_two_games(self):
        original = [row(gid) for gid in EXPECTED] + [
            {"canonical_game_id": "OTHER", "site_city": "Maui", "site_state": ""}
        ]
        before = copy.deepcopy(original)
        report = patch_rows(original)
        self.assertEqual(report["changed_game_ids"], sorted(EXPECTED))
        for old, new in zip(before, original):
            difference = {k for k in old if old[k] != new[k]}
            if old["canonical_game_id"] in EXPECTED:
                self.assertEqual(difference, set(NEW))
                self.assertEqual(new["site_type"], "NEUTRAL")
                self.assertEqual(new["game_type"], "REGULAR_SEASON")
                self.assertEqual(new["notes"], "literal preservation")
            else:
                self.assertEqual(difference, set())

    def test_rejects_missing_duplicate_or_modified_approved_rows(self):
        valid = [row(gid) for gid in EXPECTED]
        with self.assertRaisesRegex(ValueError, "both authorized"):
            patch_rows(copy.deepcopy(valid[:1]))
        with self.assertRaisesRegex(ValueError, "Duplicate affected canonical ID"):
            patch_rows(copy.deepcopy(valid + [valid[0]]))
        wrong = copy.deepcopy(valid)
        wrong[0]["site_state"] = "HI"
        with self.assertRaisesRegex(ValueError, "expected site_state"):
            patch_rows(wrong)
        wrong = copy.deepcopy(valid)
        wrong[1]["game_date"] = "2019-11-26"
        with self.assertRaisesRegex(ValueError, "expected game_date"):
            patch_rows(wrong)

    def test_global_venue_identity_must_be_exact(self):
        validate_venue([dict(VENUE)])
        wrong = dict(VENUE)
        wrong["city"] = "Maui"
        with self.assertRaisesRegex(ValueError, "Registered venue drift"):
            validate_venue([wrong])
        with self.assertRaisesRegex(ValueError, "exactly one"):
            validate_venue([])


if __name__ == "__main__":
    unittest.main()
