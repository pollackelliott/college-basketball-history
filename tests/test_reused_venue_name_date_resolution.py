import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import ingest_school
from integration_freeze_guard import (
    build_source_game_semantic_snapshot,
    semantic_snapshot_sha256,
)
from frozen_venue_authority import (
    FrozenVenueSplitAuthorityError,
    sealed_post_reconciliation_semantic_delta,
    sealed_pre_ingest_semantic_delta,
)
from onboard_school import copy_repository
from onboarding_plan import (
    WorkflowError,
    _apply_sealed_game_site_venue_relationship_patches,
    _venue_maps,
    apply_pre_ingest_source_patches,
    frozen_venue_split_authority,
)

FIELDS = [
    "source_program_key","venue_key","venue_id","canonical_name","aliases",
    "city","state","venue_type","known_opened","known_closed","venue_date_precision",
    "games_currently_assigned","first_assigned_game","last_assigned_game",
    "relationship_type","relationship_start","relationship_end","relationship_date_precision",
    "site_rule","source_basis","notes",
]


def venue_row(key, vid, first, last):
    return {
        "source_program_key":"depaul","venue_key":key,"venue_id":vid,
        "canonical_name":"Charlotte Coliseum","aliases":"","city":"Charlotte","state":"NC",
        "venue_type":"arena","known_opened":"","known_closed":"","venue_date_precision":"",
        "games_currently_assigned":"1","first_assigned_game":first,"last_assigned_game":last,
        "relationship_type":"","relationship_start":"","relationship_end":"",
        "relationship_date_precision":"","site_rule":"","source_basis":"fixture","notes":"",
    }


class ReusedVenueNameDateResolutionTests(unittest.TestCase):
    def test_sealed_pre_ingest_semantic_delta_covers_complete_supported_matrix(self):
        approved = {
            "approved_plan_hash": "a" * 64,
            "decisions": [
                {
                    "decision_id": "POST",
                    "category": "postseason_classification",
                    "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
                    "source_game_id": "POST",
                    "source_patch": {
                        "curated_game_type": "NCAA_TOURNAMENT",
                        "curated_postseason_round": "Round of 32",
                        "curated_site_type": "NEUTRAL",
                    },
                },
                {
                    "decision_id": "SITE",
                    "category": "new_game_site_patch",
                    "decision": "APPLY_SOURCE_SITE_PATCH",
                    "source_game_id": "SITE",
                    "source_patch": {"curated_site_type": "OPPONENT_HOME"},
                },
                {
                    "decision_id": "DATE",
                    "category": "new_game_date_patch",
                    "decision": "APPLY_SOURCE_DATE_PATCH",
                    "source_game_id": "DATE",
                    "source_patch": {"game_date": "1983-03-09"},
                },
                {
                    "decision_id": "NCAA-DATE",
                    "category": "ncaa_round_patch",
                    "decision": "APPLY_NCAA_ROUND_PATCH",
                    "source_game_id": "NCAA-DATE",
                    "source_patch": {
                        "curated_postseason_round": "Sweet 16",
                        "game_date": "1977-03-17",
                    },
                },
                {
                    "decision_id": "ADJACENT",
                    "category": "identity",
                    "decision": "MATCH_CANONICAL:CBBG-X",
                    "source_game_id": "ADJACENT",
                    "source_patch": {
                        "season_label": "1978-1979",
                        "game_date": "1979-01-02",
                    },
                    "cross_season_source_patch_by_action": {
                        "MATCH_CANONICAL:CBBG-X": {
                            "season_label": "1978-1979",
                            "game_date": "1979-01-02",
                        },
                    },
                },
                {
                    "decision_id": "CROSS-OPPONENT",
                    "category": "identity",
                    "decision": "MATCH_CANONICAL:CBBG-Y",
                    "source_game_id": "CROSS-OPPONENT",
                    "source_patch": {
                        "normalized_opponent_key": "example",
                        "canonical_opponent_name": "Example",
                    },
                    "cross_opponent_source_patch_by_action": {
                        "MATCH_CANONICAL:CBBG-Y": {
                            "normalized_opponent_key": "example",
                            "canonical_opponent_name": "Example",
                        },
                    },
                },
                {
                    "decision_id": "SCORE",
                    "category": "source_consistency",
                    "decision": "APPLY_SOURCE_CONSISTENCY_PATCH",
                    "source_game_id": "SCORE",
                    "source_patch": {"played_result": "W"},
                },
            ],
        }
        self.assertEqual(
            sealed_pre_ingest_semantic_delta(approved),
            {
                "POST": {
                    "curated_game_type": "NCAA_TOURNAMENT",
                    "curated_postseason_round": "Round of 32",
                    "curated_site_type": "NEUTRAL",
                },
                "SITE": {"curated_site_type": "OPPONENT_HOME"},
                "DATE": {"game_date": "1983-03-09"},
                "NCAA-DATE": {"game_date": "1977-03-17"},
                "ADJACENT": {
                    "season_label": "1978-1979",
                    "game_date": "1979-01-02",
                },
            },
        )

    def test_sealed_post_reconciliation_semantic_delta_is_exact_and_fail_closed(self):
        approved = {
            "school_key": "example",
            "approved_plan_hash": "b" * 64,
            "decisions": [
                {
                    "decision_id": "PRE",
                    "category": "new_game_date_patch",
                    "decision": "APPLY_SOURCE_DATE_PATCH",
                    "source_game_id": "PRE",
                    "source_patch": {"game_date": "1983-03-09"},
                },
                {
                    "decision_id": "DATE",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "DATE",
                    "canonical_game_id": "CBBG-DATE",
                    "field_name": "game_date",
                    "canonical_value": "1983-03-11",
                },
                {
                    "decision_id": "TYPE",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "TYPE",
                    "canonical_game_id": "CBBG-TYPE",
                    "field_name": "game_type",
                    "canonical_value": "NIT",
                },
                {
                    "decision_id": "ROUND",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "ROUND",
                    "canonical_game_id": "CBBG-ROUND",
                    "field_name": "postseason_round",
                    "canonical_value": "Championship",
                },
                {
                    "decision_id": "SITE",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "SITE",
                    "canonical_game_id": "CBBG-SITE",
                    "field_name": "site_type",
                    "canonical_value": "TEAM_B_HOME",
                    "source_patch": {
                        "curated_venue_name": "Patched Arena",
                        "city": "Patched City",
                        "state": "PA",
                    },
                },
                {
                    "decision_id": "OT",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "OT",
                    "canonical_game_id": "CBBG-OT",
                    "field_name": "overtime_periods",
                    "canonical_value": "1",
                },
                {
                    "decision_id": "SCORE-NORM",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "SCORE-NORM",
                    "canonical_game_id": "CBBG-SCORE",
                    "field_name": "score",
                    "canonical_value": "70-60",
                },
                {
                    "decision_id": "RESULT-NORM",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "RESULT-NORM",
                    "canonical_game_id": "CBBG-RESULT",
                    "field_name": "result_winner_team_key",
                    "canonical_value": "example",
                },
                {
                    "decision_id": "SOURCE-CONSISTENCY",
                    "category": "source_consistency",
                    "decision": "APPLY_SOURCE_CONSISTENCY_PATCH",
                    "source_game_id": "SOURCE-CONSISTENCY",
                    "source_consistency_expected": {
                        "team_score": "60",
                        "opponent_score": "61",
                        "played_result": "W",
                    },
                    "source_patch": {"played_result": "L"},
                },
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            path = repo / "data" / "canonical" / "games.csv"
            path.parent.mkdir(parents=True)
            fields = [
                "canonical_game_id", "team_a_key", "team_b_key", "game_date",
                "team_a_score", "team_b_score", "result_winner_team_key",
                "overtime_periods", "game_type", "postseason_round", "site_type",
                "venue_key", "site_city", "site_state",
            ]
            rows = [
                {
                    "canonical_game_id": "CBBG-DATE", "team_a_key": "example",
                    "team_b_key": "opponent", "game_date": "1983-03-11",
                    "game_type": "REGULAR_SEASON", "postseason_round": "",
                    "site_type": "TEAM_A_HOME",
                },
                {
                    "canonical_game_id": "CBBG-TYPE", "team_a_key": "example",
                    "team_b_key": "opponent", "game_date": "2022-03-15",
                    "game_type": "NIT", "postseason_round": "",
                    "site_type": "NEUTRAL",
                },
                {
                    "canonical_game_id": "CBBG-ROUND", "team_a_key": "example",
                    "team_b_key": "opponent", "game_date": "2022-03-29",
                    "game_type": "NIT", "postseason_round": "Championship",
                    "site_type": "NEUTRAL",
                },
                {
                    "canonical_game_id": "CBBG-SITE", "team_a_key": "opponent",
                    "team_b_key": "example", "game_date": "2010-03-09",
                    "game_type": "REGULAR_SEASON", "postseason_round": "",
                    "site_type": "TEAM_B_HOME", "venue_key": "arena",
                    "site_city": "Canonical City", "site_state": "NY",
                },
                {
                    "canonical_game_id": "CBBG-OT", "team_a_key": "example",
                    "team_b_key": "opponent", "game_date": "1943-01-01",
                    "game_type": "REGULAR_SEASON", "postseason_round": "",
                    "site_type": "UNKNOWN", "overtime_periods": "1",
                },
                {
                    "canonical_game_id": "CBBG-SCORE", "team_a_key": "opponent",
                    "team_b_key": "example", "game_date": "2000-01-01",
                    "team_a_score": "70", "team_b_score": "60",
                    "result_winner_team_key": "opponent",
                    "game_type": "REGULAR_SEASON", "postseason_round": "",
                    "site_type": "UNKNOWN",
                },
                {
                    "canonical_game_id": "CBBG-RESULT", "team_a_key": "opponent",
                    "team_b_key": "example", "game_date": "2000-01-02",
                    "team_a_score": "60", "team_b_score": "61",
                    "result_winner_team_key": "example",
                    "game_type": "REGULAR_SEASON", "postseason_round": "",
                    "site_type": "UNKNOWN",
                },
            ]
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)

            venue_path = repo / "schools" / "example" / "venues.csv"
            venue_path.parent.mkdir(parents=True)
            with venue_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["venue_key", "canonical_name"])
                writer.writeheader()
                writer.writerow({"venue_key": "arena", "canonical_name": "Canonical Arena"})

            self.assertEqual(
                sealed_post_reconciliation_semantic_delta(repo, "example", approved),
                {
                    "PRE": {"game_date": "1983-03-09"},
                    "DATE": {"game_date": "1983-03-11"},
                    "TYPE": {"curated_game_type": "NIT"},
                    "ROUND": {"curated_postseason_round": "Championship"},
                    "SITE": {
                        "curated_site_type": "SOURCE_PROGRAM_HOME",
                        "curated_venue_name": "Patched Arena",
                        "city": "Patched City",
                        "state": "PA",
                    },
                    "OT": {"overtime_periods": "1"},
                    "SCORE-NORM": {
                        "team_score": "60",
                        "opponent_score": "70",
                        "played_result": "L",
                    },
                    "RESULT-NORM": {"played_result": "W"},
                    "SOURCE-CONSISTENCY": {"played_result": "L"},
                },
            )

            rows[0]["game_date"] = "1983-03-12"
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(
                FrozenVenueSplitAuthorityError,
                "sealed canonical game_date no longer matches",
            ):
                sealed_post_reconciliation_semantic_delta(repo, "example", approved)

    def test_sealed_post_reconciliation_authenticates_complete_four_four_five_one_topology(self):
        decisions = []
        rows = []
        fields = [
            "canonical_game_id", "team_a_key", "team_b_key", "game_date",
            "team_a_score", "team_b_score", "result_winner_team_key",
            "overtime_periods", "game_type", "postseason_round", "site_type",
            "venue_key", "site_city", "site_state",
        ]
        for index in range(4):
            source_id = f"DATE-{index}"
            game_id = f"CBBG-DATE-{index}"
            value = f"1983-03-{11 + index:02d}"
            decisions.append({
                "decision_id": source_id,
                "category": "discrepancy",
                "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                "source_game_id": source_id,
                "canonical_game_id": game_id,
                "field_name": "game_date",
                "canonical_value": value,
            })
            rows.append({
                "canonical_game_id": game_id, "team_a_key": "example",
                "team_b_key": "opponent", "game_date": value,
                "game_type": "REGULAR_SEASON", "site_type": "UNKNOWN",
            })
        for index, value in enumerate(("1", "2", "1", "1")):
            source_id = f"OT-{index}"
            game_id = f"CBBG-OT-{index}"
            decisions.append({
                "decision_id": source_id,
                "category": "discrepancy",
                "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                "source_game_id": source_id,
                "canonical_game_id": game_id,
                "field_name": "overtime_periods",
                "canonical_value": value,
            })
            rows.append({
                "canonical_game_id": game_id, "team_a_key": "example",
                "team_b_key": "opponent", "game_date": f"1949-01-{index + 1:02d}",
                "overtime_periods": value, "game_type": "REGULAR_SEASON",
                "site_type": "UNKNOWN",
            })
        for index, value in enumerate(("POSTSEASON", "NIT", "NIT", "NIT", "NIT")):
            source_id = f"TYPE-{index}"
            game_id = f"CBBG-TYPE-{index}"
            decisions.append({
                "decision_id": source_id,
                "category": "discrepancy",
                "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                "source_game_id": source_id,
                "canonical_game_id": game_id,
                "field_name": "game_type",
                "canonical_value": value,
            })
            rows.append({
                "canonical_game_id": game_id, "team_a_key": "example",
                "team_b_key": "opponent", "game_date": f"2022-03-{index + 1:02d}",
                "game_type": value, "site_type": "UNKNOWN",
            })
        decisions.append({
            "decision_id": "SITE",
            "category": "discrepancy",
            "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
            "source_game_id": "SITE",
            "canonical_game_id": "CBBG-SITE",
            "field_name": "site_type",
            "canonical_value": "TEAM_B_HOME",
        })
        rows.append({
            "canonical_game_id": "CBBG-SITE", "team_a_key": "opponent",
            "team_b_key": "example", "game_date": "2010-03-09",
            "game_type": "REGULAR_SEASON", "site_type": "TEAM_B_HOME",
        })
        approved = {
            "school_key": "example",
            "approved_plan_hash": "d" * 64,
            "decisions": decisions,
        }
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            path = repo / "data" / "canonical" / "games.csv"
            path.parent.mkdir(parents=True)
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=fields)
                writer.writeheader()
                writer.writerows(rows)
            delta = sealed_post_reconciliation_semantic_delta(repo, "example", approved)
        self.assertEqual(len(delta), 14)
        self.assertEqual(
            sum("game_date" in values for values in delta.values()), 4
        )
        self.assertEqual(
            sum("overtime_periods" in values for values in delta.values()), 4
        )
        self.assertEqual(
            sum("curated_game_type" in values for values in delta.values()), 5
        )
        self.assertEqual(
            delta["SITE"]["curated_site_type"], "SOURCE_PROGRAM_HOME"
        )

    def test_sealed_post_reconciliation_rejects_unsealed_raw_text_patch(self):
        approved = {
            "school_key": "example",
            "approved_plan_hash": "e" * 64,
            "decisions": [{
                "decision_id": "RAW",
                "category": "discrepancy",
                "decision": "KEEP_CANONICAL",
                "source_game_id": "RAW",
                "source_patch": {"raw_text": "changed"},
            }],
        }
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            path = repo / "data" / "canonical" / "games.csv"
            path.parent.mkdir(parents=True)
            with path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=["canonical_game_id"])
                writer.writeheader()
                writer.writerow({"canonical_game_id": "CBBG-X"})
            with self.assertRaisesRegex(
                FrozenVenueSplitAuthorityError,
                "may not mutate raw_text",
            ):
                sealed_post_reconciliation_semantic_delta(repo, "example", approved)


    def test_runtime_venue_map_uses_final_delta_only_for_post_apply_verification(self):
        approved = {
            "school_key": "example",
            "approved_plan_hash": "c" * 64,
            "decisions": [
                {
                    "decision_id": "DATE",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": "DATE",
                    "canonical_game_id": "CBBG-DATE",
                    "field_name": "game_date",
                    "canonical_value": "1983-03-11",
                }
            ],
        }
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            canonical = repo / "data" / "canonical" / "games.csv"
            canonical.parent.mkdir(parents=True)
            with canonical.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=[
                        "canonical_game_id", "team_a_key", "team_b_key",
                        "game_date", "game_type", "postseason_round", "site_type",
                    ],
                )
                writer.writeheader()
                writer.writerow({
                    "canonical_game_id": "CBBG-DATE",
                    "team_a_key": "example",
                    "team_b_key": "opponent",
                    "game_date": "1983-03-11",
                    "game_type": "REGULAR_SEASON",
                    "postseason_round": "",
                    "site_type": "TEAM_A_HOME",
                })
            venue_path = repo / "schools" / "example" / "venues.csv"
            with patch.object(
                ingest_school,
                "load_frozen_venue_split_authority",
                return_value={},
            ) as loader:
                ingest_school.load_runtime_venue_metadata_map(
                    repo,
                    "example",
                    venue_path,
                    {},
                    sealed_plan_context=approved,
                    post_reconciliation_semantics=True,
                )
            self.assertEqual(
                loader.call_args.kwargs["allowed_semantic_delta"],
                {"DATE": {"game_date": "1983-03-11"}},
            )

            with patch.object(
                ingest_school,
                "load_frozen_venue_split_authority",
                return_value={},
            ) as loader:
                ingest_school.load_runtime_venue_metadata_map(
                    repo,
                    "example",
                    venue_path,
                    {},
                    sealed_plan_context=approved,
                )
            self.assertEqual(
                loader.call_args.kwargs["allowed_semantic_delta"],
                {},
            )

    def make_map(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "venues.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow(venue_row("charlotte-coliseum-1955","VEN-000040","1976-03-13","1976-03-13"))
            writer.writerow(venue_row("charlotte-coliseum-1988","VEN-000041","1991-12-07","1991-12-07"))
        globals_by_id = {
            "VEN-000040":{"venue_id":"VEN-000040","city":"Charlotte","state":"NC","opened":"1955","closed":""},
            "VEN-000041":{"venue_id":"VEN-000041","city":"Charlotte","state":"NC","opened":"1988","closed":"2005"},
        }
        return ingest_school.load_venue_metadata_map(path, globals_by_id)

    def make_runtime_name_period_map(self, *, include_old=True, include_new=True):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        repo = Path(directory.name)
        school = repo / "schools" / "example"
        reference = repo / "data" / "reference"
        school.mkdir(parents=True)
        reference.mkdir(parents=True)

        venue_path = school / "venues.csv"
        with venue_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow(venue_row("charlotte-coliseum-1955", "VEN-000040", "", ""))
            writer.writerow(venue_row("charlotte-coliseum-1988", "VEN-000041", "", ""))

        name_fields = [
            "venue_id", "venue_name", "normalized_name", "name_type",
            "valid_from", "valid_to", "date_precision", "source_basis", "notes",
        ]
        name_rows = []
        if include_old:
            name_rows.append({
                "venue_id": "VEN-000040", "venue_name": "Charlotte Coliseum",
                "normalized_name": "charlottecoliseum", "name_type": "PROJECT_DISPLAY",
                "valid_from": "1955", "valid_to": "1988", "date_precision": "YEAR",
                "source_basis": "fixture", "notes": "",
            })
        if include_new:
            name_rows.append({
                "venue_id": "VEN-000041", "venue_name": "Charlotte Coliseum",
                "normalized_name": "charlottecoliseum", "name_type": "PROJECT_DISPLAY",
                "valid_from": "1988", "valid_to": "2005", "date_precision": "YEAR",
                "source_basis": "fixture", "notes": "",
            })
        with (reference / "venue-names.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=name_fields)
            writer.writeheader()
            writer.writerows(name_rows)

        globals_by_id = {
            "VEN-000040": {
                "venue_id": "VEN-000040", "city": "Charlotte", "state": "NC",
                "opened": "1955", "closed": "",
            },
            "VEN-000041": {
                "venue_id": "VEN-000041", "city": "Charlotte", "state": "NC",
                "opened": "1988", "closed": "2005",
            },
        }
        return ingest_school.load_runtime_venue_metadata_map(
            repo,
            "example",
            venue_path,
            globals_by_id,
        )

    def test_1976_resolves_original(self):
        result = ingest_school.resolve_venue_metadata(
            {"source_game_id":"DEPRAW-01178","game_date":"1976-03-13","curated_venue_name":"Charlotte Coliseum"},
            self.make_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000040")
        self.assertEqual(result["venue_key"], "charlotte-coliseum-1955")

    def test_1991_resolves_new_building(self):
        result = ingest_school.resolve_venue_metadata(
            {"source_game_id":"DEPRAW-01659","game_date":"1991-12-07","curated_venue_name":"Charlotte Coliseum"},
            self.make_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000041")
        self.assertEqual(result["venue_key"], "charlotte-coliseum-1988")

    def test_undated_reused_name_without_season_stops(self):
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id":"UNDATED",
                    "game_date":"",
                    "season_label":"",
                    "curated_venue_name":"Charlotte Coliseum",
                },
                self.make_map(),
            )

    def test_undated_2000_01_resolves_from_registered_name_period(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id": "RICHMOND-2000-01",
                "game_date": "",
                "season_label": "2000-2001",
                "curated_venue_name": "Charlotte Coliseum",
                "city": "Charlotte",
                "state": "NC",
            },
            self.make_runtime_name_period_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000041")
        self.assertEqual(result["venue_key"], "charlotte-coliseum-1988")

    def test_registered_name_period_transition_season_still_stops(self):
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "TRANSITION-1988-89",
                    "game_date": "",
                    "season_label": "1988-1989",
                    "curated_venue_name": "Charlotte Coliseum",
                    "city": "Charlotte",
                    "state": "NC",
                },
                self.make_runtime_name_period_map(),
            )

    def test_incomplete_registered_name_period_authority_still_stops(self):
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "INCOMPLETE-PERIOD-AUTHORITY",
                    "game_date": "",
                    "season_label": "2000-2001",
                    "curated_venue_name": "Charlotte Coliseum",
                    "city": "Charlotte",
                    "state": "NC",
                },
                self.make_runtime_name_period_map(include_old=False),
            )

    def test_ambiguous_exact_date_stops(self):
        with self.assertRaisesRegex(ValueError, "does not resolve exactly one candidate"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id":"OTHER",
                    "game_date":"1989-01-01",
                    "season_label":"1988-1989",
                    "curated_venue_name":"Charlotte Coliseum",
                },
                self.make_map(),
            )

    def memorial_map(self):
        return {
            "memorial coliseum": [
                {
                    "venue_key": "memorial-coliseum-winston-salem",
                    "venue_id": "VEN-WINSTON",
                    "city": "Winston-Salem",
                    "state": "NC",
                    "local_valid_from": "",
                    "local_valid_to": "",
                    "physical_opened": "",
                    "physical_closed": "",
                },
                {
                    "venue_key": "memorial-coliseum-kentucky",
                    "venue_id": "VEN-LEXINGTON",
                    "city": "Lexington",
                    "state": "KY",
                    "local_valid_from": "",
                    "local_valid_to": "",
                    "physical_opened": "",
                    "physical_closed": "",
                },
            ]
        }

    def test_complete_geography_resolves_reused_name_across_cities(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id": "WF-EXAMPLE",
                "game_date": "1955-12-06",
                "season_label": "1955-1956",
                "curated_venue_name": "Memorial Coliseum",
                "city": "Winston-Salem",
                "state": "NC",
            },
            self.memorial_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-WINSTON")

    def test_complete_geography_resolves_other_physical_candidate(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id": "LEX-EXAMPLE",
                "game_date": "1955-12-06",
                "season_label": "1955-1956",
                "curated_venue_name": "Memorial Coliseum",
                "city": "Lexington",
                "state": "KY",
            },
            self.memorial_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-LEXINGTON")

    def test_same_city_reused_name_still_requires_date_resolution(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id": "CHARLOTTE-EXAMPLE",
                "game_date": "1976-03-13",
                "season_label": "1975-1976",
                "curated_venue_name": "Charlotte Coliseum",
                "city": "Charlotte",
                "state": "NC",
            },
            self.make_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000040")

    def test_partial_geography_preserves_existing_date_resolution(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id": "PARTIAL-EXAMPLE",
                "game_date": "1976-03-13",
                "season_label": "1975-1976",
                "curated_venue_name": "Charlotte Coliseum",
                "city": "Charlotte",
                "state": "",
            },
            self.make_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000040")

    def test_conflicting_complete_geography_stops_before_date_fallback(self):
        with self.assertRaisesRegex(
            ValueError,
            "does not match any registered physical candidate",
        ):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "CONFLICTING-GEOGRAPHY",
                    "game_date": "1976-03-13",
                    "season_label": "1975-1976",
                    "curated_venue_name": "Charlotte Coliseum",
                    "city": "Raleigh",
                    "state": "NC",
                },
                self.make_map(),
            )

    def make_msg_map(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "venues.csv"
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            old = venue_row(
                "madison-square-garden-1925",
                "VEN-000123",
                "1937-02-24",
                "1966-03-10",
            )
            old["canonical_name"] = "Madison Square Garden"
            new = venue_row(
                "madison-square-garden-1968",
                "VEN-000124",
                "1983-02-20",
                "2026-03-11",
            )
            new["canonical_name"] = "Madison Square Garden"
            writer.writerow(old)
            writer.writerow(new)
        globals_by_id = {
            "VEN-000123":{
                "venue_id":"VEN-000123",
                "city":"New York",
                "state":"NY",
                "opened":"1925",
                "closed":"1968",
            },
            "VEN-000124":{
                "venue_id":"VEN-000124",
                "city":"New York",
                "state":"NY",
                "opened":"1968-02-11",
                "closed":"",
            },
        }
        return ingest_school.load_venue_metadata_map(path, globals_by_id)

    def test_undated_1935_36_msg_resolves_msg_iii_by_season(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id":"DEPRAW-00201",
                "game_date":"",
                "season_label":"1935-1936",
                "curated_venue_name":"Madison Square Garden",
            },
            self.make_msg_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000123")

    def test_undated_1937_38_msg_resolves_msg_iii_by_season(self):
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id":"DEPRAW-00235",
                "game_date":"",
                "season_label":"1937-1938",
                "curated_venue_name":"Madison Square Garden",
            },
            self.make_msg_map(),
        )
        self.assertEqual(result["venue_id"], "VEN-000123")

    def test_msg_transition_season_stops(self):
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id":"TRANSITION",
                    "game_date":"",
                    "season_label":"1967-1968",
                    "curated_venue_name":"Madison Square Garden",
                },
                self.make_msg_map(),
            )


    def test_frozen_split_authority_resolves_exact_53_row_msg_population(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        repo = Path(directory.name)
        school = repo / "schools" / "st-bonaventure"
        onboarding = repo / ".onboarding" / "st-bonaventure"
        school.mkdir(parents=True)
        onboarding.mkdir(parents=True)

        before_ids = [f"STB-MSG-BEFORE-{index:02d}" for index in range(1, 35)]
        after_ids = ["STB-1968-69-018"] + [
            f"STB-MSG-AFTER-{index:02d}" for index in range(1, 19)
        ]
        self.assertEqual(len(before_ids), 34)
        self.assertEqual(len(after_ids), 19)

        source_fields = [
            "source_game_id",
            "source_program_key",
            "season_label",
            "game_date",
            "normalized_opponent_key",
            "overtime_periods",
            "curated_site_type",
            "curated_venue_name",
            "city",
            "state",
            "curated_game_type",
            "curated_postseason_round",
            "notes",
        ]
        with (school / "source-games.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=source_fields)
            writer.writeheader()
            for source_id in before_ids:
                writer.writerow({
                    "source_game_id": source_id,
                    "source_program_key": "st-bonaventure",
                    "season_label": "1966-1967",
                    "game_date": "",
                    "curated_venue_name": "Madison Square Garden",
                    "city": "New York",
                    "state": "NY",
                })
            for source_id in after_ids:
                writer.writerow({
                    "source_game_id": source_id,
                    "source_program_key": "st-bonaventure",
                    "season_label": (
                        "1968-1969"
                        if source_id == "STB-1968-69-018"
                        else "1969-1970"
                    ),
                    "game_date": "",
                    "curated_venue_name": "Madison Square Garden",
                    "city": "New York",
                    "state": "NY",
                })
            writer.writerow({
                "source_game_id": "STB-1982-83-028",
                "source_program_key": "st-bonaventure",
                "season_label": "1982-1983",
                "game_date": "1983-03-07",
                "normalized_opponent_key": "example-opponent",
                "curated_game_type": "CONFERENCE_TOURNAMENT",
            })

        canonical = repo / "data" / "canonical"
        canonical.mkdir(parents=True)
        (canonical / "games.csv").write_text(
            "canonical_game_id,season_label,game_date,team_a_key,team_b_key\n",
            encoding="utf-8",
        )

        with (school / "venues.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            old = venue_row(
                "madison-square-garden-1925",
                "VEN-000123",
                "1937-02-24",
                "1966-03-10",
            )
            old["source_program_key"] = "st-bonaventure"
            old["canonical_name"] = "Madison Square Garden"
            old["city"] = "New York"
            old["state"] = "NY"
            new = venue_row(
                "madison-square-garden-1968",
                "VEN-000124",
                "1983-02-20",
                "2026-03-11",
            )
            new["source_program_key"] = "st-bonaventure"
            new["canonical_name"] = "Madison Square Garden"
            new["city"] = "New York"
            new["state"] = "NY"
            writer.writerow(old)
            writer.writerow(new)

        snapshot = build_source_game_semantic_snapshot(
            school / "source-games.csv"
        )
        manifest = {
            "schema_version": 2,
            "school_key": "st-bonaventure",
            "status": "INTEGRATION_FROZEN",
            "package_member_sha256": {
                "venues.csv": hashlib.sha256(
                    (school / "venues.csv").read_bytes()
                ).hexdigest(),
            },
            "source_game_semantic_guard": {
                "schema_version": 1,
                "snapshot_sha256": semantic_snapshot_sha256(snapshot),
                "snapshot": snapshot,
            },
            "venue_reconciliation": {
                "schema_version": 2,
                "mappings": [{
                    "action": "SPLIT_LOCAL_ROW_BY_CUTOVER",
                    "expected_local_name": "Madison Square Garden",
                    "expected_local_city": "New York",
                    "expected_local_state": "NY",
                    "cutover_date": "1968-02-11",
                    "split_source_game_count": "53",
                    "split_targets": [
                        {
                            "side": "BEFORE",
                            "global_venue_id": "VEN-000123",
                            "global_venue_key": "madison-square-garden-1925",
                            "games_currently_assigned": "34",
                            "source_game_ids": before_ids,
                        },
                        {
                            "side": "AFTER",
                            "global_venue_id": "VEN-000124",
                            "global_venue_key": "madison-square-garden-1968",
                            "games_currently_assigned": "19",
                            "source_game_ids": after_ids,
                        },
                    ],
                }],
            },
        }
        (onboarding / "integration-freeze.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

        authority = frozen_venue_split_authority(repo, "st-bonaventure")
        self.assertEqual(len(authority), 53)
        self.assertEqual(
            sum(
                item["venue_id"] == "VEN-000123"
                for item in authority.values()
            ),
            34,
        )
        self.assertEqual(
            sum(
                item["venue_id"] == "VEN-000124"
                for item in authority.values()
            ),
            19,
        )
        self.assertEqual(
            authority["STB-1968-69-018"]["venue_id"],
            "VEN-000124",
        )

        global_venues = {
            "VEN-000123": {
                "venue_id": "VEN-000123",
                "city": "New York",
                "state": "NY",
                "opened": "1925",
                "closed": "1968",
            },
            "VEN-000124": {
                "venue_id": "VEN-000124",
                "city": "New York",
                "state": "NY",
                "opened": "1968-02-11",
                "closed": "",
            },
        }
        # Model the minimal global physical-venue registry required by the real reconciliation loader.
        reference = repo / "data" / "reference"
        reference.mkdir(parents=True, exist_ok=True)
        venue_fields = [
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
        ]
        with (reference / "venues.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=venue_fields)
            writer.writeheader()
            writer.writerow({
                "venue_id": "VEN-000123",
                "venue_key": "madison-square-garden-1925",
                "display_name": "Madison Square Garden (1925)",
                "city": "New York",
                "state": "NY",
                "opened": "1925",
                "closed": "1968",
                "date_precision": "YEAR",
                "identity_status": "VERIFIED",
                "source_basis": "fixture",
                "notes": "",
            })
            writer.writerow({
                "venue_id": "VEN-000124",
                "venue_key": "madison-square-garden-1968",
                "display_name": "Madison Square Garden",
                "city": "New York",
                "state": "NY",
                "opened": "1968-02-11",
                "closed": "",
                "date_precision": "DAY",
                "identity_status": "VERIFIED",
                "source_basis": "fixture",
                "notes": "",
            })
        name_fields = [
            "venue_id",
            "venue_name",
            "normalized_name",
            "name_type",
            "valid_from",
            "valid_to",
            "date_precision",
            "source_basis",
            "notes",
        ]
        with (reference / "venue-names.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=name_fields)
            writer.writeheader()
            writer.writerow({
                "venue_id": "VEN-000123",
                "venue_name": "Madison Square Garden (1925)",
                "normalized_name": "madisonsquaregarden1925",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "1925",
                "valid_to": "1968",
                "date_precision": "YEAR",
                "source_basis": "fixture",
                "notes": "",
            })
            writer.writerow({
                "venue_id": "VEN-000123",
                "venue_name": "Madison Square Garden",
                "normalized_name": "madisonsquaregarden",
                "name_type": "HISTORICAL",
                "valid_from": "1925",
                "valid_to": "1968",
                "date_precision": "YEAR",
                "source_basis": "fixture",
                "notes": "",
            })
            writer.writerow({
                "venue_id": "VEN-000124",
                "venue_name": "Madison Square Garden",
                "normalized_name": "madisonsquaregarden",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "1968-02-11",
                "valid_to": "",
                "date_precision": "DAY",
                "source_basis": "fixture",
                "notes": "",
            })
        metadata = ingest_school.load_venue_metadata_map(
            school / "venues.csv",
            global_venues,
        )

        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "STB-1968-69-018",
                    "game_date": "",
                    "season_label": "1968-1969",
                    "curated_venue_name": "Madison Square Garden",
                    "city": "New York",
                    "state": "NY",
                },
                metadata,
            )

        ingest_school.bind_frozen_venue_split_authority(metadata, authority)
        result = ingest_school.resolve_venue_metadata(
            {
                "source_game_id": "STB-1968-69-018",
                "game_date": "",
                "season_label": "1968-1969",
                "curated_venue_name": "Madison Square Garden",
                "city": "New York",
                "state": "NY",
            },
            metadata,
        )
        self.assertEqual(result["venue_id"], "VEN-000124")
        self.assertEqual(result["venue_key"], "madison-square-garden-1968")

        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "UNAUTHORIZED-AMBIGUOUS",
                    "game_date": "",
                    "season_label": "1968-1969",
                    "curated_venue_name": "Madison Square Garden",
                    "city": "New York",
                    "state": "NY",
                },
                metadata,
            )

        # The permanent rehearsal/apply boundary strips ignored .onboarding state
        # before constructing a disposable repository. copy_repository() must
        # transport this exact manifest only after authenticating the split.
        with tempfile.TemporaryDirectory() as copied:
            rehearsal = Path(copied) / "repository"
            copy_repository(repo, rehearsal, school_key="st-bonaventure")
            copied_freeze = (
                rehearsal
                / ".onboarding"
                / "st-bonaventure"
                / "integration-freeze.json"
            )
            self.assertTrue(copied_freeze.is_file())
            self.assertEqual(
                copied_freeze.read_bytes(),
                (onboarding / "integration-freeze.json").read_bytes(),
            )

            runtime_metadata = ingest_school.load_runtime_venue_metadata_map(
                rehearsal,
                "st-bonaventure",
                rehearsal / "schools" / "st-bonaventure" / "venues.csv",
                global_venues,
            )
            runtime_result = ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "STB-1968-69-018",
                    "game_date": "",
                    "season_label": "1968-1969",
                    "curated_venue_name": "Madison Square Garden",
                    "city": "New York",
                    "state": "NY",
                },
                runtime_metadata,
            )
            self.assertEqual(runtime_result["venue_id"], "VEN-000124")
            self.assertEqual(
                runtime_result["venue_key"],
                "madison-square-garden-1968",
            )

        # Exercise the topology that blocked St. Bonaventure proposal -0003:
        # exact frozen split authority + sealed pre-ingest date mutation + runtime
        # rehydration. The date row is unrelated to the 53-row MSG population.
        approved = {
            "school_key": "st-bonaventure",
            "approved_plan_hash": "b" * 64,
            "decisions": [{
                "decision_id": "NEW-GAME-DATE-PATCH-STB-1982-83-028",
                "category": "new_game_date_patch",
                "decision": "APPLY_SOURCE_DATE_PATCH",
                "source_game_id": "STB-1982-83-028",
                "source_game_date": "1983-03-07",
                "source_game_type": "CONFERENCE_TOURNAMENT",
                "season_label": "1982-1983",
                "canonical_game_id": "",
                "source_patch": {"game_date": "1983-03-09"},
            }],
        }
        with tempfile.TemporaryDirectory() as copied:
            rehearsal = Path(copied) / "repository"
            copy_repository(repo, rehearsal, school_key="st-bonaventure")
            counts = apply_pre_ingest_source_patches(rehearsal, approved)
            self.assertEqual(counts["new_game_date_patches"], 1)

            runtime_metadata = ingest_school.load_runtime_venue_metadata_map(
                rehearsal,
                "st-bonaventure",
                rehearsal / "schools" / "st-bonaventure" / "venues.csv",
                global_venues,
                sealed_plan_context=approved,
            )
            runtime_result = ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "STB-1968-69-018",
                    "game_date": "",
                    "season_label": "1968-1969",
                    "curated_venue_name": "Madison Square Garden",
                    "city": "New York",
                    "state": "NY",
                },
                runtime_metadata,
            )
            self.assertEqual(runtime_result["venue_id"], "VEN-000124")

            with self.assertRaisesRegex(
                FrozenVenueSplitAuthorityError,
                "does not match current source semantics",
            ):
                _venue_maps(rehearsal, "st-bonaventure")

            reconciliation_metadata, _ = _venue_maps(
                rehearsal,
                "st-bonaventure",
                approved_plan=approved,
            )
            reconciliation_result = ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "STB-1968-69-018",
                    "game_date": "",
                    "season_label": "1968-1969",
                    "curated_venue_name": "Madison Square Garden",
                    "city": "New York",
                    "state": "NY",
                },
                reconciliation_metadata,
            )
            self.assertEqual(reconciliation_result["venue_id"], "VEN-000124")
            self.assertEqual(
                reconciliation_result["venue_key"],
                "madison-square-garden-1968",
            )

            source_path = rehearsal / "schools" / "st-bonaventure" / "source-games.csv"
            rows = list(csv.DictReader(source_path.open(encoding="utf-8-sig", newline="")))
            rows[0]["game_date"] = "1967-01-01"
            with source_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=source_fields)
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(
                FrozenVenueSplitAuthorityError,
                "outside the exact sealed pre-ingest semantic delta",
            ):
                ingest_school.load_runtime_venue_metadata_map(
                    rehearsal,
                    "st-bonaventure",
                    rehearsal / "schools" / "st-bonaventure" / "venues.csv",
                    global_venues,
                    sealed_plan_context=approved,
                )

        # Exercise the complete post-reconciliation authority contract through
        # the real Integration Freeze matcher. This is the production topology that
        # proposal -0008 exposed: 4 dates + 4 OT + 5 game types + 1 site type.
        with tempfile.TemporaryDirectory() as copied:
            rehearsal = Path(copied) / "repository"
            copy_repository(repo, rehearsal, school_key="st-bonaventure")
            source_path = rehearsal / "schools" / "st-bonaventure" / "source-games.csv"
            source_rows = list(
                csv.DictReader(
                    source_path.open(encoding="utf-8-sig", newline="")
                )
            )
            source_by_id = {row["source_game_id"]: row for row in source_rows}
            date_ids = before_ids[0:4]
            overtime_ids = before_ids[4:8]
            game_type_ids = before_ids[8:13]
            site_id = "STB-1968-69-018"

            final_decisions = []
            canonical_rows = []
            canonical_fields = [
                "canonical_game_id",
                "season_label",
                "game_date",
                "team_a_key",
                "team_b_key",
                "team_a_score",
                "team_b_score",
                "result_winner_team_key",
                "overtime_periods",
                "site_type",
                "venue_key",
                "site_city",
                "site_state",
                "game_type",
                "postseason_round",
            ]

            for index, source_id in enumerate(date_ids, start=1):
                value = f"1966-01-{index:02d}"
                source_by_id[source_id]["game_date"] = value
                game_id = f"CBBG-FINAL-DATE-{index}"
                final_decisions.append({
                    "decision_id": f"FINAL-DATE-{index}",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": source_id,
                    "canonical_game_id": game_id,
                    "field_name": "game_date",
                    "canonical_value": value,
                })
                canonical_rows.append({
                    "canonical_game_id": game_id,
                    "season_label": "1966-1967",
                    "game_date": value,
                    "team_a_key": "st-bonaventure",
                    "team_b_key": "example-opponent",
                    "site_type": "UNKNOWN",
                    "game_type": "REGULAR_SEASON",
                })

            overtime_values = ("1", "2", "1", "1")
            for index, (source_id, value) in enumerate(
                zip(overtime_ids, overtime_values),
                start=1,
            ):
                source_by_id[source_id]["overtime_periods"] = value
                game_id = f"CBBG-FINAL-OT-{index}"
                final_decisions.append({
                    "decision_id": f"FINAL-OT-{index}",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": source_id,
                    "canonical_game_id": game_id,
                    "field_name": "overtime_periods",
                    "canonical_value": value,
                })
                canonical_rows.append({
                    "canonical_game_id": game_id,
                    "season_label": "1966-1967",
                    "team_a_key": "st-bonaventure",
                    "team_b_key": "example-opponent",
                    "overtime_periods": value,
                    "site_type": "UNKNOWN",
                    "game_type": "REGULAR_SEASON",
                })

            game_type_values = ("POSTSEASON", "NIT", "NIT", "NIT", "NIT")
            for index, (source_id, value) in enumerate(
                zip(game_type_ids, game_type_values),
                start=1,
            ):
                source_by_id[source_id]["curated_game_type"] = value
                game_id = f"CBBG-FINAL-TYPE-{index}"
                final_decisions.append({
                    "decision_id": f"FINAL-TYPE-{index}",
                    "category": "discrepancy",
                    "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                    "source_game_id": source_id,
                    "canonical_game_id": game_id,
                    "field_name": "game_type",
                    "canonical_value": value,
                })
                canonical_rows.append({
                    "canonical_game_id": game_id,
                    "season_label": "1966-1967",
                    "team_a_key": "st-bonaventure",
                    "team_b_key": "example-opponent",
                    "site_type": "UNKNOWN",
                    "game_type": value,
                })

            source_by_id[site_id]["curated_site_type"] = "SOURCE_PROGRAM_HOME"
            final_decisions.append({
                "decision_id": "FINAL-SITE",
                "category": "discrepancy",
                "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                "source_game_id": site_id,
                "canonical_game_id": "CBBG-FINAL-SITE",
                "field_name": "site_type",
                "canonical_value": "TEAM_A_HOME",
            })
            canonical_rows.append({
                "canonical_game_id": "CBBG-FINAL-SITE",
                "season_label": "1968-1969",
                "team_a_key": "st-bonaventure",
                "team_b_key": "example-opponent",
                "site_type": "TEAM_A_HOME",
                "venue_key": "madison-square-garden-1968",
                "site_city": "New York",
                "site_state": "NY",
                "game_type": "REGULAR_SEASON",
            })

            with source_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=source_fields)
                writer.writeheader()
                writer.writerows(source_rows)

            canonical_path = rehearsal / "data" / "canonical" / "games.csv"
            with canonical_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=canonical_fields)
                writer.writeheader()
                writer.writerows(canonical_rows)

            final_approved = {
                "school_key": "st-bonaventure",
                "approved_plan_hash": "f" * 64,
                "decisions": final_decisions,
            }

            # Final verification explicitly admits the sealed final semantic
            # universe and still returns the exact frozen split authority.
            final_metadata = ingest_school.load_runtime_venue_metadata_map(
                rehearsal,
                "st-bonaventure",
                rehearsal / "schools" / "st-bonaventure" / "venues.csv",
                global_venues,
                sealed_plan_context=final_approved,
                post_reconciliation_semantics=True,
            )
            final_result = ingest_school.resolve_venue_metadata(
                source_by_id[site_id],
                final_metadata,
            )
            self.assertEqual(final_result["venue_id"], "VEN-000124")

            # The identical final-state delta remains forbidden in ordinary
            # pre-ingest authentication.
            with self.assertRaisesRegex(
                FrozenVenueSplitAuthorityError,
                "does not match current source semantics",
            ):
                ingest_school.load_runtime_venue_metadata_map(
                    rehearsal,
                    "st-bonaventure",
                    rehearsal / "schools" / "st-bonaventure" / "venues.csv",
                    global_venues,
                    sealed_plan_context=final_approved,
                )

            # Changed canonical authority is rejected before the matcher can
            # authenticate the final source state.
            wrong_approved = json.loads(json.dumps(final_approved))
            wrong_approved["decisions"][4]["canonical_value"] = "9"
            with self.assertRaisesRegex(
                FrozenVenueSplitAuthorityError,
                "sealed canonical overtime_periods no longer matches",
            ):
                ingest_school.load_runtime_venue_metadata_map(
                    rehearsal,
                    "st-bonaventure",
                    rehearsal / "schools" / "st-bonaventure" / "venues.csv",
                    global_venues,
                    sealed_plan_context=wrong_approved,
                    post_reconciliation_semantics=True,
                )

            # Unsealed final semantic drift is still fail-closed.
            unrelated_id = before_ids[20]
            source_by_id[unrelated_id]["overtime_periods"] = "3"
            with source_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=source_fields)
                writer.writeheader()
                writer.writerows(source_rows)
            with self.assertRaisesRegex(
                FrozenVenueSplitAuthorityError,
                "outside the exact sealed post-reconciliation semantic delta",
            ):
                ingest_school.load_runtime_venue_metadata_map(
                    rehearsal,
                    "st-bonaventure",
                    rehearsal / "schools" / "st-bonaventure" / "venues.csv",
                    global_venues,
                    sealed_plan_context=final_approved,
                    post_reconciliation_semantics=True,
                )

        # An ignored manifest cannot be smuggled across the disposable-copy
        # boundary after its frozen package representation has drifted.
        with (school / "venues.csv").open("a", encoding="utf-8") as handle:
            handle.write("\n")
        with tempfile.TemporaryDirectory() as copied:
            with self.assertRaisesRegex(
                WorkflowError,
                "does not match current venues.csv",
            ):
                copy_repository(
                    repo,
                    Path(copied) / "repository",
                    school_key="st-bonaventure",
                )

    def test_post_reconciliation_frozen_venues_allow_only_exact_sealed_game_site_delta(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        repo = Path(directory.name)
        school_key = "example-school"
        school = repo / "schools" / school_key
        onboarding = repo / ".onboarding" / school_key
        reference = repo / "data" / "reference"
        canonical_dir = repo / "data" / "canonical"
        school.mkdir(parents=True)
        onboarding.mkdir(parents=True)
        reference.mkdir(parents=True)
        canonical_dir.mkdir(parents=True)

        source_fields = [
            "source_game_id",
            "season_label",
            "game_date",
            "curated_venue_name",
            "city",
            "state",
            "curated_site_type",
            "curated_game_type",
            "curated_postseason_round",
        ]
        source_rows = [
            {
                "source_game_id": "SPLIT-1",
                "season_label": "1960-1961",
                "game_date": "1961-01-15",
                "curated_venue_name": "Frozen Arena",
                "city": "Frozen City",
                "state": "FC",
                "curated_site_type": "NEUTRAL",
                "curated_game_type": "REGULAR_SEASON",
                "curated_postseason_round": "",
            },
            {
                "source_game_id": "EX-2",
                "season_label": "2011-2012",
                "game_date": "2012-03-15",
                "curated_venue_name": "",
                "city": "",
                "state": "",
                "curated_site_type": "OPPONENT_HOME",
                "curated_game_type": "REGULAR_SEASON",
                "curated_postseason_round": "",
            },
        ]
        source_path = school / "source-games.csv"
        with source_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=source_fields)
            writer.writeheader()
            writer.writerows(source_rows)

        frozen_row = {field: "" for field in FIELDS}
        frozen_row.update({
            "source_program_key": school_key,
            "venue_key": "frozen-arena",
            "venue_id": "VEN-000901",
            "canonical_name": "Frozen Arena",
            "city": "Frozen City",
            "state": "FC",
            "games_currently_assigned": "1",
            "first_assigned_game": "1961-01-15",
            "last_assigned_game": "1961-01-15",
            "relationship_type": "GAME_SITE",
            "site_rule": "fixture",
            "source_basis": "fixture",
            "notes": "fixture",
        })
        venue_path = school / "venues.csv"
        with venue_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerow(frozen_row)
        frozen_bytes = venue_path.read_bytes()
        frozen_hash = hashlib.sha256(frozen_bytes).hexdigest()

        global_fields = [
            "venue_id", "venue_key", "display_name", "city", "state",
            "opened", "closed", "date_precision", "identity_status",
            "source_basis", "notes",
        ]
        with (reference / "venues.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=global_fields)
            writer.writeheader()
            writer.writerow({
                "venue_id": "VEN-000901",
                "venue_key": "frozen-arena",
                "display_name": "Frozen Arena",
                "city": "Frozen City",
                "state": "FC",
                "opened": "",
                "closed": "",
                "date_precision": "",
                "identity_status": "VERIFIED",
                "source_basis": "fixture",
                "notes": "",
            })
            writer.writerow({
                "venue_id": "VEN-000902",
                "venue_key": "sealed-arena",
                "display_name": "Sealed Arena",
                "city": "Sealed City",
                "state": "SC",
                "opened": "2000",
                "closed": "",
                "date_precision": "YEAR",
                "identity_status": "VERIFIED",
                "source_basis": "fixture",
                "notes": "",
            })

        name_fields = [
            "venue_id", "venue_name", "normalized_name", "name_type",
            "valid_from", "valid_to", "date_precision", "source_basis", "notes",
        ]
        with (reference / "venue-names.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=name_fields)
            writer.writeheader()
            writer.writerow({
                "venue_id": "VEN-000901",
                "venue_name": "Frozen Arena",
                "normalized_name": "frozenarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "fixture",
                "notes": "",
            })
            writer.writerow({
                "venue_id": "VEN-000902",
                "venue_name": "Sealed Arena",
                "normalized_name": "sealedarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "fixture",
                "notes": "",
            })

        canonical_fields = [
            "canonical_game_id", "season_label", "game_date",
            "team_a_key", "team_b_key", "team_a_score", "team_b_score",
            "result_winner_team_key", "overtime_periods", "site_type",
            "venue_key", "site_city", "site_state", "game_type",
            "postseason_round",
        ]
        with (canonical_dir / "games.csv").open(
            "w", encoding="utf-8", newline=""
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=canonical_fields)
            writer.writeheader()
            writer.writerow({
                "canonical_game_id": "CBBG-EX-2",
                "season_label": "2011-2012",
                "game_date": "2012-03-15",
                "team_a_key": school_key,
                "team_b_key": "example-opponent",
                "site_type": "TEAM_B_HOME",
                "venue_key": "sealed-arena",
                "site_city": "Sealed City",
                "site_state": "SC",
                "game_type": "NIT",
                "postseason_round": "",
            })

        snapshot_fields = [
            "season_label",
            "game_date",
            "curated_venue_name",
            "city",
            "state",
            "curated_site_type",
            "curated_game_type",
            "curated_postseason_round",
        ]
        snapshot = {
            "schema_version": 1,
            "fields": snapshot_fields,
            "rows": {
                row["source_game_id"]: {
                    field: row[field]
                    for field in snapshot_fields
                }
                for row in source_rows
            },
        }
        manifest = {
            "schema_version": 2,
            "school_key": school_key,
            "status": "INTEGRATION_FROZEN",
            "package_member_sha256": {"venues.csv": frozen_hash},
            "source_game_semantic_guard": {
                "schema_version": 1,
                "snapshot_sha256": hashlib.sha256(
                    json.dumps(
                        snapshot,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ).encode("utf-8")
                ).hexdigest(),
                "snapshot": snapshot,
            },
            "venue_reconciliation": {
                "schema_version": 2,
                "mappings": [{
                    "action": "SPLIT_LOCAL_ROW_BY_CUTOVER",
                    "expected_local_name": "Frozen Arena",
                    "expected_local_city": "Frozen City",
                    "expected_local_state": "FC",
                    "cutover_date": "1960-01-01",
                    "split_source_game_count": "1",
                    "split_targets": [{
                        "side": "AFTER",
                        "global_venue_id": "VEN-000901",
                        "global_venue_key": "frozen-arena",
                        "games_currently_assigned": "1",
                        "source_game_ids": ["SPLIT-1"],
                    }],
                }],
            },
        }
        (onboarding / "integration-freeze.json").write_text(
            json.dumps(manifest), encoding="utf-8"
        )

        approved = {
            "school_key": school_key,
            "approved_plan_hash": "a" * 64,
            "decisions": [{
                "decision_id": "DISCREPANCY-EX-2-GAME_TYPE",
                "category": "discrepancy",
                "decision": "NORMALIZE_SOURCE_TO_CANONICAL",
                "source_game_id": "EX-2",
                "source_game_date": "2012-03-15",
                "canonical_game_id": "CBBG-EX-2",
                "field_name": "game_type",
                "canonical_value": "NIT",
                "resolution_basis": "Official host source identifies exact site.",
                "source_patch": {
                    "curated_venue_name": "Sealed Arena",
                    "city": "Sealed City",
                    "state": "SC",
                },
                "venue_relationship_patch": {
                    "venue_id": "VEN-000902",
                    "venue_key": "sealed-arena",
                },
            }],
        }

        global_venues = {
            row["venue_id"]: row
            for row in csv.DictReader(
                (reference / "venues.csv").open(
                    encoding="utf-8-sig", newline=""
                )
            )
        }
        self.assertEqual(
            _apply_sealed_game_site_venue_relationship_patches(repo, approved),
            1,
        )

        # The same venue mutation remains forbidden during ordinary pre-ingest
        # authentication while source semantics are still exactly frozen.
        with self.assertRaisesRegex(
            FrozenVenueSplitAuthorityError,
            "does not match current venues.csv",
        ):
            ingest_school.load_runtime_venue_metadata_map(
                repo,
                school_key,
                venue_path,
                global_venues,
                sealed_plan_context=approved,
            )

        # Generic reconciliation writes the sealed GAME_SITE suffix immediately,
        # but source reconciliations remain in memory until the final CSV write.
        # Exercise that real mixed transaction state: venue bytes are post-
        # reconciliation while source semantics are still exactly pre-ingest.
        metadata, names_by_key = _venue_maps(
            repo,
            school_key,
            approved_plan=approved,
        )
        self.assertIn(
            ingest_school.FROZEN_VENUE_SPLIT_AUTHORITY_KEY,
            metadata,
        )
        self.assertEqual(names_by_key["sealed-arena"], "Sealed Arena")
        exact_post_bytes = venue_path.read_bytes()

        # The final/no-op authentication mode remains exact and must not accept
        # the still-pre-ingest source state merely because the venue suffix is valid.
        with self.assertRaisesRegex(
            FrozenVenueSplitAuthorityError,
            "outside the exact sealed post-reconciliation semantic delta",
        ):
            ingest_school.load_runtime_venue_metadata_map(
                repo,
                school_key,
                venue_path,
                global_venues,
                sealed_plan_context=approved,
                post_reconciliation_semantics=True,
            )

        # Model the paired final source state produced when reconciliation
        # eventually persists its in-memory source changes.
        source_rows[1]["curated_game_type"] = "NIT"
        source_rows[1]["curated_venue_name"] = "Sealed Arena"
        source_rows[1]["city"] = "Sealed City"
        source_rows[1]["state"] = "SC"
        with source_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=source_fields)
            writer.writeheader()
            writer.writerows(source_rows)

        final_metadata = ingest_school.load_runtime_venue_metadata_map(
            repo,
            school_key,
            venue_path,
            global_venues,
            sealed_plan_context=approved,
            post_reconciliation_semantics=True,
        )
        self.assertIn(
            ingest_school.FROZEN_VENUE_SPLIT_AUTHORITY_KEY,
            final_metadata,
        )

        # A changed frozen row remains forbidden.
        frozen_mutation = bytearray(exact_post_bytes)
        marker = b"fixture"
        marker_pos = frozen_mutation.find(marker)
        self.assertGreaterEqual(marker_pos, 0)
        frozen_mutation[marker_pos:marker_pos + len(marker)] = b"changed"
        venue_path.write_bytes(bytes(frozen_mutation))
        with self.assertRaisesRegex(
            FrozenVenueSplitAuthorityError,
            "outside the exact sealed post-reconciliation GAME_SITE delta",
        ):
            ingest_school.load_runtime_venue_metadata_map(
                repo,
                school_key,
                venue_path,
                global_venues,
                sealed_plan_context=approved,
                post_reconciliation_semantics=True,
            )

        # An unrelated extra row remains forbidden.
        venue_path.write_bytes(exact_post_bytes)
        with venue_path.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=FIELDS)
            extra = {field: "" for field in FIELDS}
            extra.update({
                "source_program_key": school_key,
                "venue_key": "frozen-arena",
                "venue_id": "VEN-000901",
                "canonical_name": "Frozen Arena",
            })
            writer.writerow(extra)
        with self.assertRaisesRegex(
            FrozenVenueSplitAuthorityError,
            "outside the exact sealed post-reconciliation GAME_SITE delta",
        ):
            ingest_school.load_runtime_venue_metadata_map(
                repo,
                school_key,
                venue_path,
                global_venues,
                sealed_plan_context=approved,
                post_reconciliation_semantics=True,
            )

        # A malformed sealed suffix remains forbidden.
        venue_path.write_bytes(exact_post_bytes.replace(
            b"2012-03-15,2012-03-15",
            b"2012-03-16,2012-03-15",
            1,
        ))
        with self.assertRaisesRegex(
            FrozenVenueSplitAuthorityError,
            "outside the exact sealed post-reconciliation GAME_SITE delta",
        ):
            ingest_school.load_runtime_venue_metadata_map(
                repo,
                school_key,
                venue_path,
                global_venues,
                sealed_plan_context=approved,
                post_reconciliation_semantics=True,
            )

        # Missing the sealed addition is also forbidden in final-phase auth.
        venue_path.write_bytes(frozen_bytes)
        with self.assertRaisesRegex(
            FrozenVenueSplitAuthorityError,
            "outside the exact sealed post-reconciliation GAME_SITE delta",
        ):
            ingest_school.load_runtime_venue_metadata_map(
                repo,
                school_key,
                venue_path,
                global_venues,
                sealed_plan_context=approved,
                post_reconciliation_semantics=True,
            )

    def test_frozen_split_authority_mismatch_fails_closed(self):
        metadata = self.make_msg_map()
        ingest_school.bind_frozen_venue_split_authority(
            metadata,
            {
                "TRANSITION": {
                    "venue_id": "VEN-DOES-NOT-EXIST",
                    "venue_key": "wrong-building",
                    "curated_venue_name": "Madison Square Garden",
                }
            },
        )
        with self.assertRaisesRegex(
            ValueError,
            "does not match exactly one current venue candidate",
        ):
            ingest_school.resolve_venue_metadata(
                {
                    "source_game_id": "TRANSITION",
                    "game_date": "",
                    "season_label": "1967-1968",
                    "curated_venue_name": "Madison Square Garden",
                },
                metadata,
            )

if __name__ == "__main__":
    unittest.main()
