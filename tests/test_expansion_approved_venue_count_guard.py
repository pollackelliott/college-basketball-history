"""Frozen venue compatibility when an owner-approved pre-Integration site move
causes Phase 0 to recompute one derived assignment summary.

The fixture reproduces 27 inherited + 22 registered supplemental venue rows,
three frozen Hickey-like HOME assertions corrected to opponent HOME, 318 -> 315,
and a later opponent-display successor's exact frozen-file reconstruction.
"""
import copy
import csv
import hashlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import all_history_expansion_display_successor_guard as guard  # noqa: E402

SCHOOL = "fixture-school"
PARENT = "1" * 40
PHASE0 = "2" * 40
FIELDS = [
    "venue_key", "venue_id", "canonical_name", "aliases", "city", "state",
    "games_currently_assigned", "first_assigned_game", "last_assigned_game",
    "notes",
]
SOURCE_FIELDS = [
    "source_program_key", "source_game_id", "curated_site_type",
    "curated_venue_name", "city", "state", "game_date",
]


def csv_bytes(fields, rows):
    value = io.StringIO(newline="")
    writer = csv.DictWriter(value, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return value.getvalue().encode("utf-8")


def canonical(value):
    return (json.dumps(
        value, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def venue(key, name, assigned):
    return {
        "venue_key": key,
        "venue_id": "",
        "canonical_name": name,
        "aliases": "",
        "city": "Davis",
        "state": "CA",
        "games_currently_assigned": assigned,
        "first_assigned_game": "",
        "last_assigned_game": "",
        "notes": "Accepted venue evidence.",
    }


class OwnerApprovedDerivedVenueCountTests(unittest.TestCase):
    def setUp(self):
        self.inherited = [
            venue(f"inherited-{i:02d}", f"Inherited {i}", "")
            for i in range(27)
        ]
        self.supplemental = [
            venue(
                "hickey-gymnasium" if i == 0 else f"other-{i:02d}",
                "Hickey Gymnasium" if i == 0 else f"Other Venue {i}",
                "318" if i == 0 else "",
            ) for i in range(22)
        ]
        self.frozen_rows = self.inherited + self.supplemental
        self.frozen_hash = digest(csv_bytes(FIELDS, self.frozen_rows))
        self.global_ids = {}
        census_rows = []
        self.phase0_rows = copy.deepcopy(self.frozen_rows)
        for i, row in enumerate(self.phase0_rows[27:], 1):
            final_id = f"VEN-{i:06d}"
            self.global_ids[row["venue_key"]] = final_id
            census_rows.append({
                "venue_key": row["venue_key"],
                "target_venue_key": row["venue_key"],
                "research_venue_id": "",
                "target_venue_id": "",
                "classification": "NEW_GLOBAL_IDENTITY",
            })
            row["venue_id"] = final_id
            row["notes"] += (
                f" Integration rebase resolved final global venue ID {final_id}."
            )
        self.phase0_rows[27]["games_currently_assigned"] = "315"

        self.source_rows = [
            {
                "source_program_key": SCHOOL,
                "source_game_id": f"FIXTURE-{i:04d}",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "Hickey Gymnasium",
                "city": "Davis", "state": "CA", "game_date": "",
            } for i in range(315)
        ]
        moved = [
            ("Dayton Fieldhouse", "Dayton", "OH"),
            ("Toledo Court", "Toledo", "OH"),
            ("Maples Pavilion", "Stanford", "CA"),
        ]
        for i, (name, city, state) in enumerate(moved, 315):
            self.source_rows.append({
                "source_program_key": SCHOOL,
                "source_game_id": f"FIXTURE-{i:04d}",
                "curated_site_type": "OPPONENT_HOME",
                "curated_venue_name": name,
                "city": city, "state": state, "game_date": "",
            })
        ids = [row["source_game_id"] for row in self.source_rows[-3:]]
        self.receipt = {
            "kind": "PREINTEGRATION_OWNER_CORRECTION_RECEIPT",
            "owner_approved": True,
            "owner_gate_1_approval": False,
            "school_key": SCHOOL,
            "artifact_sha256": "a" * 64,
            "approval_issue_url": "https://github.com/example/example/issues/1",
            "approved_source_game_ids": ids,
            "source_row_receipts": [{
                "source_game_id": row["source_game_id"],
                "field_names": [
                    "city", "curated_site_type", "curated_venue_name", "state",
                ],
                "effective_row_sha256": digest(canonical(row)),
            } for row in self.source_rows[-3:]],
            "effective_source_rows_sha256": digest(canonical(self.source_rows)),
        }
        self.freeze = {
            "kind": "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
            "status": "INTEGRATION_FROZEN",
            "school_key": SCHOOL,
            "integration_base_sha": PARENT,
            "candidate_member_sha256": {"venues.csv": self.frozen_hash},
            "venue_reconciliation_census": {
                "schema_version": 1, "blocker_count": 0,
                "venue_count": 22, "rows": census_rows,
            },
            "owner_preintegration_correction": self.receipt,
            "owner_preintegration_correction_sha256": "a" * 64,
        }

    def check(self):
        def git(_, *args):
            if args == ("rev-list", "--parents", "-n", "1", PHASE0):
                return f"{PHASE0} {PARENT}\n".encode()
            if args == ("show", "-s", "--format=%s", PHASE0):
                return f"Stage {SCHOOL} all-history expansion Phase 0\n".encode()
            return None

        def blob(_, commit, school, name):
            if school != SCHOOL:
                return None
            if (commit, name) == (PARENT, "venues.csv"):
                return csv_bytes(FIELDS, self.inherited)
            if (commit, name) == (PARENT, "source-games.csv"):
                return csv_bytes(SOURCE_FIELDS, [])
            if (commit, name) == (PHASE0, "source-games.csv"):
                return csv_bytes(SOURCE_FIELDS, self.source_rows)
            return None

        diagnostics = []
        with (
            patch.object(guard, "_git", side_effect=git),
            patch.object(guard, "_blob", side_effect=blob),
            patch.object(guard, "_registry_ids_by_key",
                         return_value=self.global_ids),
        ):
            accepted = guard._reconstruct_frozen_venues(
                ROOT, SCHOOL, PHASE0,
                csv_bytes(FIELDS, self.phase0_rows),
                self.frozen_hash, self.freeze,
                diagnostics=diagnostics,
            )
        return accepted, diagnostics

    def test_exact_22_registration_three_approved_moves_replays(self):
        accepted, diagnostics = self.check()
        self.assertTrue(accepted, diagnostics)
        self.assertEqual(len(self.freeze["venue_reconciliation_census"]["rows"]), 22)
        self.assertEqual(self.supplemental[0]["games_currently_assigned"], "318")
        self.assertEqual(self.phase0_rows[27]["games_currently_assigned"], "315")

    def test_no_owner_approval_is_not_a_count_exception(self):
        self.receipt["owner_approved"] = False
        self.assertFalse(self.check()[0])

    def test_wrong_receipt_artifact_binding_is_rejected(self):
        self.freeze["owner_preintegration_correction_sha256"] = "b" * 64
        self.assertFalse(self.check()[0])

    def test_effective_source_population_must_match_receipt(self):
        self.source_rows[20]["city"] = "Elsewhere"
        self.assertFalse(self.check()[0])

    def test_changed_approved_source_row_must_match_receipt(self):
        self.source_rows[-1]["curated_venue_name"] = "An Unapproved Building"
        self.receipt["effective_source_rows_sha256"] = digest(
            canonical(self.source_rows)
        )
        self.assertFalse(self.check()[0])

    def test_unapproved_count_difference_is_rejected(self):
        self.phase0_rows[27]["games_currently_assigned"] = "314"
        self.assertFalse(self.check()[0])

    def test_wrong_direction_count_change_is_rejected(self):
        self.phase0_rows[27]["games_currently_assigned"] = "319"
        self.assertFalse(self.check()[0])

    def test_second_summary_difference_is_rejected(self):
        self.phase0_rows[28]["games_currently_assigned"] = "1"
        self.assertFalse(self.check()[0])

    def test_unrelated_frozen_venue_bytes_are_immutable(self):
        self.phase0_rows[27]["city"] = "Somewhere Else"
        self.assertFalse(self.check()[0])

    def test_invalid_global_venue_identity_is_rejected(self):
        self.phase0_rows[27]["venue_id"] = "VEN-999999"
        self.assertFalse(self.check()[0])

    def test_nonsite_corrections_cannot_authorize_venue_counts(self):
        for item in self.receipt["source_row_receipts"]:
            item["field_names"] = ["team_score"]
        self.assertFalse(self.check()[0])

    def test_stale_approved_source_does_not_replay_derived_count(self):
        # This modified source is additionally hash-consistent with the receipt;
        # the deterministic venue refresh still sees 316, not the published 315.
        self.source_rows[-1]["curated_venue_name"] = "Hickey Gymnasium"
        self.source_rows[-1]["city"] = "Davis"
        self.receipt["effective_source_rows_sha256"] = digest(
            canonical(self.source_rows)
        )
        self.receipt["source_row_receipts"][-1]["effective_row_sha256"] = (
            digest(canonical(self.source_rows[-1]))
        )
        self.assertFalse(self.check()[0])


if __name__ == "__main__":
    unittest.main()
