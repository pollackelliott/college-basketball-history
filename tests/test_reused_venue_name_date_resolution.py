import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import ingest_school
from integration_freeze_guard import (
    build_source_game_semantic_snapshot,
    semantic_snapshot_sha256,
)
from frozen_venue_authority import (
    FrozenVenueSplitAuthorityError,
    sealed_pre_ingest_semantic_delta,
)
from onboard_school import copy_repository
from onboarding_plan import (
    WorkflowError,
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
