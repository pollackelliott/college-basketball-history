import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import WorkflowError  # noqa: E402
from stage_research_portfolio import (  # noqa: E402
    accepted_top_level_scope_expression,
    rebase_venues,
    reconcile_top_level_scope_reference,
    update_program_scope,
    venue_reconciliation_inventory,
    venue_date_bounds,
    write_top_level_scope_reference,
)


def global_venue(venue_id: str, venue_key: str, name: str, city: str, state: str):
    return {
        "venue_id": venue_id,
        "venue_key": venue_key,
        "display_name": name,
        "city": city,
        "state": state,
        "opened": "",
        "closed": "",
        "date_precision": "",
        "identity_status": "TEST",
        "source_basis": "test",
        "notes": "",
    }


def local_venue(notes: str, *, city: str = "", state: str = ""):
    return {
        "source_program_key": "test-school",
        "venue_key": "addition-financial-arena",
        "venue_id": "",
        "canonical_name": "Addition Financial Arena",
        "aliases": "",
        "city": city,
        "state": state,
        "venue_type": "",
        "known_opened": "",
        "known_closed": "",
        "venue_date_precision": "unknown",
        "games_currently_assigned": "2",
        "first_assigned_game": "",
        "last_assigned_game": "",
        "relationship_type": "",
        "relationship_start": "",
        "relationship_end": "",
        "relationship_date_precision": "",
        "site_rule": "",
        "source_basis": "test",
        "notes": notes,
    }


class StageResearchPortfolioVenueChronologyTests(unittest.TestCase):
    """Two identically named physical buildings must not be conflated by rebase."""

    def test_1940_replacement_rejects_1938_game_even_with_exact_key(self):
        replacement = global_venue(
            "VEN-000156", "patten-gymnasium-1940",
            "Patten Gymnasium (1940 building)", "Evanston", "IL",
        )
        replacement["opened"] = "1940"
        replacement["date_precision"] = "YEAR"
        local = {
            **local_venue("", city="Evanston", state="IL"),
            "venue_key": "patten-gymnasium-1940",
            "canonical_name": "Patten Gymnasium",
            "first_assigned_game": "1938-12-30",
        }
        inventory = venue_reconciliation_inventory([local], [replacement], [])
        result = inventory["rows"][0]
        self.assertEqual(result["classification"], "STOP_AMBIGUOUS")
        self.assertIn("PHYSICAL_VENUE_CHRONOLOGY_CONFLICT", result["issues"])
        self.assertIn("1938-12-30", result["chronology_conflicts"][0])
        with self.assertRaisesRegex(WorkflowError, "before physical opening"):
            rebase_venues("test-school", [local], [replacement], [])

    def test_original_1909_building_rejects_1942_game(self):
        original = global_venue(
            "VEN-000160", "patten-gymnasium-1909",
            "Patten Gymnasium", "Evanston", "IL",
        )
        original.update(opened="1909", closed="1940", date_precision="YEAR")
        local = {
            **local_venue("", city="Evanston", state="IL"),
            "venue_key": "patten-gymnasium-1909",
            "canonical_name": "Patten Gymnasium",
            "last_assigned_game": "1942-02-09",
        }
        inventory = venue_reconciliation_inventory([local], [original], [])
        self.assertEqual(inventory["blocker_count"], 1)
        with self.assertRaisesRegex(WorkflowError, "after physical closing"):
            rebase_venues("test-school", [local], [original], [])

    def test_earlier_local_closure_rejects_new_building_reuse(self):
        replacement = global_venue(
            "VEN-000156", "patten-gymnasium-1940",
            "Patten Gymnasium (1940 building)", "Evanston", "IL",
        )
        replacement.update(opened="1940", date_precision="YEAR")
        local = {
            **local_venue("", city="Evanston", state="IL"),
            "venue_key": "patten-gymnasium-1940",
            "canonical_name": "Patten Gymnasium",
            "known_opened": "1909",
            "known_closed": "1939",
        }
        inventory = venue_reconciliation_inventory([local], [replacement], [])
        self.assertEqual(inventory["blocker_count"], 1)
        with self.assertRaisesRegex(WorkflowError, "known_closed=1939"):
            rebase_venues("test-school", [local], [replacement], [])

    def test_research_base_hint_cannot_bypass_chronology(self):
        replacement = global_venue(
            "VEN-000156", "patten-gymnasium-1940",
            "Patten Gymnasium (1940 building)", "Evanston", "IL",
        )
        replacement.update(opened="1940", date_precision="YEAR")
        local = {
            **local_venue(
                "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE; "
                "research-base key=patten-gymnasium-1940; "
                "research-base venue_id=VEN-000156.",
                city="Evanston", state="IL",
            ),
            "first_assigned_game": "1938-12-30",
        }
        inventory = venue_reconciliation_inventory([local], [replacement], [])
        self.assertEqual(inventory["blocker_count"], 1)
        with self.assertRaisesRegex(WorkflowError, "before physical opening"):
            rebase_venues("test-school", [local], [replacement], [])

    def test_boundary_year_and_documented_split_are_safe(self):
        original = global_venue(
            "VEN-000160", "patten-gymnasium-1909",
            "Patten Gymnasium", "Evanston", "IL",
        )
        original.update(opened="1909", closed="1940", date_precision="YEAR",
                        identity_status="RESEARCHED_SPLIT")
        replacement = global_venue(
            "VEN-000156", "patten-gymnasium-1940",
            "Patten Gymnasium (1940 building)", "Evanston", "IL",
        )
        replacement.update(opened="1940", date_precision="YEAR",
                           identity_status="RESEARCHED_SPLIT")
        alias = {
            "venue_id": "VEN-000156",
            "venue_name": "Patten Gymnasium",
            "normalized_name": "pattengymnasium",
            "name_type": "HISTORICAL_OR_ALIAS",
            "valid_from": "", "valid_to": "", "date_precision": "",
        }
        local = {
            **local_venue("", city="Evanston", state="IL"),
            "venue_key": "patten-gymnasium-1940",
            "canonical_name": "Patten Gymnasium",
            "first_assigned_game": "1940-12-01",
        }
        inventory = venue_reconciliation_inventory(
            [local], [original, replacement], [alias],
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            inventory["rows"][0]["classification"],
            "SAFE_REPRESENTATION_REUSE",
        )
        staged, globals_, _, _ = rebase_venues(
            "test-school", [local], [original, replacement], [alias],
        )
        self.assertEqual(staged[0]["venue_id"], "VEN-000156")
        self.assertEqual(len(globals_), 2)

    def test_unknown_and_partial_dates_do_not_infer_a_venue(self):
        replacement = global_venue(
            "VEN-000156", "patten-gymnasium-1940",
            "Patten Gymnasium (1940 building)", "Evanston", "IL",
        )
        replacement.update(opened="1940", date_precision="YEAR")
        local = {
            **local_venue("", city="Evanston", state="IL"),
            "venue_key": "patten-gymnasium-1940",
            "canonical_name": "Patten Gymnasium",
            "first_assigned_game": "circa 1938",
        }
        inventory = venue_reconciliation_inventory([local], [replacement], [])
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertIsNone(venue_date_bounds("circa 1938"))
        self.assertEqual(
            venue_date_bounds("1940")[0].isoformat(), "1940-01-01"
        )
        staged, _, _, _ = rebase_venues(
            "test-school", [local], [replacement], [],
        )
        self.assertEqual(staged[0]["venue_id"], "VEN-000156")


class StageResearchPortfolioVenueReuseTests(unittest.TestCase):
    def test_explicit_reconciliation_allows_intentional_researched_split_name_overlap(self):
        original = global_venue(
            "VEN-000100",
            "shared-arena-1955",
            "Shared Arena",
            "Example City",
            "NY",
        )
        original["identity_status"] = "RESEARCHED_SPLIT"
        replacement = global_venue(
            "VEN-000101",
            "shared-arena-1988",
            "Shared Arena",
            "Example City",
            "NY",
        )
        replacement["identity_status"] = "RESEARCHED_SPLIT"
        local = {
            **local_venue(
                "Explicit current-main reconciliation resolves the original building.",
                city="Example City",
                state="NY",
            ),
            "venue_key": "local-shared-arena-original",
            "canonical_name": "Shared Arena (Original building)",
            "aliases": "Shared Arena",
        }
        names = [
            {
                "venue_id": "VEN-000100",
                "venue_name": "Shared Arena",
                "normalized_name": "sharedarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
            {
                "venue_id": "VEN-000101",
                "venue_name": "Shared Arena",
                "normalized_name": "sharedarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
        ]
        reconciliation = {
            "local-shared-arena-original": {
                "global_venue_id": "VEN-000100",
                "global_venue_key": "shared-arena-1955",
            }
        }

        inventory = venue_reconciliation_inventory(
            [dict(local)],
            [dict(original), dict(replacement)],
            [dict(row) for row in names],
            venue_reconciliation=reconciliation,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        row = inventory["rows"][0]
        self.assertEqual(row["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(row["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        self.assertEqual(row["target_venue_id"], "VEN-000100")
        self.assertEqual(row["target_venue_key"], "shared-arena-1955")
        self.assertIn(
            "INTENTIONAL_RESEARCHED_SPLIT_NAME_OVERLAP",
            row["issues"],
        )
        self.assertIn(
            "GLOBAL_NAME_REGISTRATION_DURING_PHASE0",
            row["issues"],
        )
        self.assertEqual(
            row["missing_registered_names"],
            ["Shared Arena (Original building)"],
        )

        staged, globals_, staged_names, mappings = rebase_venues(
            "test-school",
            [dict(local)],
            [dict(original), dict(replacement)],
            [dict(row) for row in names],
            venue_reconciliation=reconciliation,
        )
        self.assertEqual(len(globals_), 2)
        self.assertEqual(staged[0]["venue_id"], "VEN-000100")
        self.assertEqual(staged[0]["venue_key"], "shared-arena-1955")
        self.assertEqual(mappings[0]["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        registered = [
            row for row in staged_names
            if row["venue_id"] == "VEN-000100"
            and row["venue_name"] == "Shared Arena (Original building)"
        ]
        self.assertEqual(len(registered), 1)
        self.assertEqual(registered[0]["name_type"], "HISTORICAL_OR_ALIAS")

    def test_explicit_reconciliation_does_not_waive_non_split_name_conflict(self):
        selected = global_venue(
            "VEN-000100",
            "shared-arena-1955",
            "Shared Arena",
            "Example City",
            "NY",
        )
        selected["identity_status"] = "RESEARCHED_SPLIT"
        conflicting = global_venue(
            "VEN-000101",
            "other-shared-arena",
            "Shared Arena",
            "Example City",
            "NY",
        )
        local = {
            **local_venue(
                "Explicit reconciliation must not erase a genuine name conflict.",
                city="Example City",
                state="NY",
            ),
            "venue_key": "local-shared-arena-original",
            "canonical_name": "Shared Arena (Original building)",
            "aliases": "Shared Arena",
        }
        names = [
            {
                "venue_id": "VEN-000100",
                "venue_name": "Shared Arena",
                "normalized_name": "sharedarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
            {
                "venue_id": "VEN-000101",
                "venue_name": "Shared Arena",
                "normalized_name": "sharedarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
        ]
        reconciliation = {
            "local-shared-arena-original": {
                "global_venue_id": "VEN-000100",
                "global_venue_key": "shared-arena-1955",
            }
        }

        inventory = venue_reconciliation_inventory(
            [local],
            [selected, conflicting],
            names,
            venue_reconciliation=reconciliation,
        )
        self.assertEqual(inventory["blocker_count"], 1)
        row = inventory["rows"][0]
        self.assertEqual(row["classification"], "STOP_AMBIGUOUS")
        self.assertEqual(row["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        self.assertEqual(row["target_venue_id"], "VEN-000100")
        self.assertIn("CONFLICTING_REGISTERED_NAME_IDENTITIES", row["issues"])
        self.assertNotIn(
            "INTENTIONAL_RESEARCHED_SPLIT_NAME_OVERLAP",
            row["issues"],
        )

    def test_explicit_research_base_reuse_hint_survives_local_key_drift(self):
        globals_ = [
            global_venue(
                "VEN-000038",
                "cfe-arena",
                "Addition Financial Arena",
                "Orlando",
                "FL",
            )
        ]
        locals_ = [
            local_venue(
                "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE; "
                "historical/local label maps to research-base key=cfe-arena; "
                "research-base venue_id=VEN-000038."
            )
        ]

        local_rows, global_rows, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            [],
        )

        self.assertEqual(local_rows[0]["venue_id"], "VEN-000038")
        self.assertEqual(len(global_rows), 1)
        self.assertEqual(mappings[0]["final_venue_id"], "VEN-000038")
        self.assertEqual(
            mappings[0]["resolution"],
            "REUSE_RESEARCH_BASE_IDENTITY",
        )

    def test_explicit_research_base_reuse_hint_canonicalizes_local_key(self):
        globals_ = [
            global_venue(
                "VEN-000038",
                "cfe-arena",
                "Addition Financial Arena",
                "Orlando",
                "FL",
            )
        ]
        locals_ = [
            local_venue(
                "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE; "
                "historical/local label maps to research-base key=cfe-arena; "
                "research-base venue_id=VEN-000038."
            )
        ]

        local_rows, _globals, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            [],
        )

        self.assertEqual(local_rows[0]["venue_id"], "VEN-000038")
        self.assertEqual(local_rows[0]["venue_key"], "cfe-arena")
        self.assertEqual(
            mappings[0]["resolution"],
            "REUSE_RESEARCH_BASE_IDENTITY",
        )

    def test_unique_registered_alias_reuses_authoritative_identity(self):
        globals_ = [
            global_venue(
                "VEN-000505",
                "rochester-war-memorial",
                "Rochester War Memorial",
                "Rochester",
                "NY",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Research resolved Blue Cross Arena as the Rochester "
                    "War Memorial physical facility.",
                    city="Rochester",
                    state="NY",
                ),
                "venue_key": "blue-cross-blue-shield-arena",
                "canonical_name": "Blue Cross/Blue Shield Arena",
            }
        ]
        names = [
            {
                "venue_id": "VEN-000505",
                "venue_name": "Blue Cross/Blue Shield Arena",
                "normalized_name": "bluecrossblueshieldarena",
                "name_type": "HISTORICAL_OR_ALIAS",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            }
        ]

        local_rows, global_rows, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            names,
        )

        self.assertEqual(len(global_rows), 1)
        self.assertEqual(local_rows[0]["venue_id"], "VEN-000505")
        self.assertEqual(local_rows[0]["venue_key"], "rochester-war-memorial")
        self.assertEqual(
            mappings[0]["resolution"],
            "REUSE_REGISTERED_ALIAS",
        )

    def test_current_display_plus_registered_alias_cluster_reuses_identity(self):
        globals_ = [
            global_venue(
                "VEN-000179",
                "rocket-arena",
                "Rocket Arena",
                "Cleveland",
                "OH",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Research resolves the naming eras as one physical building.",
                    city="Cleveland",
                    state="OH",
                ),
                "venue_key": "rocket-arena-cleveland-physical",
                "canonical_name": "Rocket Arena",
                "aliases": "Quicken Loans Arena; Rocket Mortgage FieldHouse",
            }
        ]
        names = [
            {
                "venue_id": "VEN-000179",
                "venue_name": "Rocket Arena",
                "normalized_name": "rocketarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
            {
                "venue_id": "VEN-000179",
                "venue_name": "Quicken Loans Arena",
                "normalized_name": "quickenloansarena",
                "name_type": "HISTORICAL_OR_ALIAS",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
            {
                "venue_id": "VEN-000179",
                "venue_name": "Rocket Mortgage FieldHouse",
                "normalized_name": "rocketmortgagefieldhouse",
                "name_type": "HISTORICAL_OR_ALIAS",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
        ]

        local_rows, global_rows, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            names,
        )

        self.assertEqual(len(global_rows), 1)
        self.assertEqual(local_rows[0]["venue_id"], "VEN-000179")
        self.assertEqual(local_rows[0]["venue_key"], "rocket-arena")
        self.assertEqual(
            mappings[0]["resolution"],
            "REUSE_REGISTERED_NAME_CLUSTER",
        )

    def test_name_cluster_stops_when_aliases_resolve_to_different_ids(self):
        globals_ = [
            global_venue(
                "VEN-000179",
                "rocket-arena",
                "Rocket Arena",
                "Cleveland",
                "OH",
            ),
            global_venue(
                "VEN-000999",
                "other-arena",
                "Other Arena",
                "Cleveland",
                "OH",
            ),
        ]
        locals_ = [
            {
                **local_venue(
                    "Conflicting cluster test.",
                    city="Cleveland",
                    state="OH",
                ),
                "venue_key": "rocket-arena-cleveland-physical",
                "canonical_name": "Rocket Arena",
                "aliases": "Quicken Loans Arena",
            }
        ]
        names = [
            {
                "venue_id": "VEN-000179",
                "venue_name": "Rocket Arena",
                "normalized_name": "rocketarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
            {
                "venue_id": "VEN-000999",
                "venue_name": "Quicken Loans Arena",
                "normalized_name": "quickenloansarena",
                "name_type": "HISTORICAL_OR_ALIAS",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
        ]

        with self.assertRaisesRegex(
            WorkflowError,
            "possible physical venue match",
        ):
            rebase_venues("test-school", locals_, globals_, names)

    def test_project_display_name_without_alias_still_stops(self):
        globals_ = [
            global_venue(
                "VEN-000505",
                "rochester-war-memorial",
                "Rochester War Memorial",
                "Rochester",
                "NY",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Display-name-only match is not enough.",
                    city="Rochester",
                    state="NY",
                ),
                "venue_key": "different-local-key",
                "canonical_name": "Rochester War Memorial",
            }
        ]
        names = [
            {
                "venue_id": "VEN-000505",
                "venue_name": "Rochester War Memorial",
                "normalized_name": "rochesterwarmemorial",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            }
        ]

        with self.assertRaisesRegex(
            WorkflowError,
            "possible physical venue match",
        ):
            rebase_venues("test-school", locals_, globals_, names)

    def test_registered_alias_still_stops_when_multiple_physical_ids_match(self):
        globals_ = [
            global_venue(
                "VEN-000505",
                "rochester-war-memorial",
                "Rochester War Memorial",
                "Rochester",
                "NY",
            ),
            global_venue(
                "VEN-000999",
                "other-rochester-arena",
                "Other Rochester Arena",
                "Rochester",
                "NY",
            ),
        ]
        locals_ = [
            {
                **local_venue(
                    "Ambiguous alias test.",
                    city="Rochester",
                    state="NY",
                ),
                "venue_key": "blue-cross-blue-shield-arena",
                "canonical_name": "Blue Cross/Blue Shield Arena",
            }
        ]
        names = [
            {
                "venue_id": "VEN-000505",
                "venue_name": "Blue Cross/Blue Shield Arena",
                "normalized_name": "bluecrossblueshieldarena",
                "name_type": "HISTORICAL_OR_ALIAS",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
            {
                "venue_id": "VEN-000999",
                "venue_name": "Blue Cross/Blue Shield Arena",
                "normalized_name": "bluecrossblueshieldarena",
                "name_type": "HISTORICAL_OR_ALIAS",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            },
        ]

        with self.assertRaisesRegex(
            WorkflowError,
            "possible physical venue match",
        ):
            rebase_venues("test-school", locals_, globals_, names)

    def test_research_base_reuse_hint_must_still_match_current_main(self):
        globals_ = [
            global_venue(
                "VEN-000999",
                "cfe-arena",
                "Addition Financial Arena",
                "Orlando",
                "FL",
            )
        ]
        locals_ = [
            local_venue(
                "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE; "
                "historical/local label maps to research-base key=cfe-arena; "
                "research-base venue_id=VEN-000038."
            )
        ]

        with self.assertRaisesRegex(
            WorkflowError,
            "reuse hint no longer matches current main",
        ):
            rebase_venues("test-school", locals_, globals_, [])

    def test_research_base_reuse_hint_allows_same_state_locality_variant(self):
        globals_ = [
            global_venue(
                "VEN-000084",
                "hp-field-house",
                "HP Field House",
                "Orlando",
                "FL",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE; "
                    "historical/local label maps to research-base key=hp-field-house; "
                    "research-base venue_id=VEN-000084.",
                    city="Lake Buena Vista",
                    state="FL",
                ),
                "venue_key": "hp-field-house",
                "canonical_name": "HP Field House",
            }
        ]

        local_rows, global_rows, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            [],
        )

        self.assertEqual(local_rows[0]["venue_id"], "VEN-000084")
        self.assertEqual(local_rows[0]["city"], "Orlando")
        self.assertEqual(local_rows[0]["state"], "FL")
        self.assertEqual(global_rows[0]["city"], "Orlando")
        self.assertEqual(
            mappings[0]["resolution"],
            "REUSE_RESEARCH_BASE_IDENTITY",
        )

    def test_exact_key_reuse_allows_same_jurisdiction_locality_variant(self):
        globals_ = [
            global_venue(
                "VEN-000088",
                "imperial-arena",
                "Imperial Arena",
                "Nassau",
                "BS",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE.",
                    city="Paradise Island",
                    state="BS",
                ),
                "venue_key": "imperial-arena",
                "canonical_name": "Imperial Arena",
            }
        ]

        local_rows, global_rows, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            [],
        )

        self.assertEqual(local_rows[0]["venue_id"], "VEN-000088")
        self.assertEqual(local_rows[0]["city"], "Nassau")
        self.assertEqual(local_rows[0]["state"], "BS")
        self.assertEqual(global_rows[0]["city"], "Nassau")
        self.assertEqual(mappings[0]["resolution"], "REUSE_EXACT_KEY")

    def test_exact_key_reuse_normalizes_us_state_name(self):
        globals_ = [
            global_venue(
                "VEN-000148",
                "nationwide-arena",
                "Nationwide Arena",
                "Columbus",
                "OH",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE.",
                    city="Columbus",
                    state="Ohio",
                ),
                "venue_key": "nationwide-arena",
                "canonical_name": "Nationwide Arena",
            }
        ]

        local_rows, _globals, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            [],
        )

        self.assertEqual(local_rows[0]["venue_id"], "VEN-000148")
        self.assertEqual(local_rows[0]["city"], "Columbus")
        self.assertEqual(local_rows[0]["state"], "OH")
        self.assertEqual(mappings[0]["resolution"], "REUSE_EXACT_KEY")

    def test_registered_alias_reuse_canonicalizes_global_geography(self):
        globals_ = [
            global_venue(
                "VEN-000505",
                "rochester-war-memorial",
                "Rochester War Memorial",
                "Rochester",
                "NY",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Historical alias maps to the current global identity.",
                    city="Rochester City",
                    state="NY",
                ),
                "venue_key": "blue-cross-blue-shield-arena",
                "canonical_name": "Blue Cross/Blue Shield Arena",
            }
        ]
        names = [
            {
                "venue_id": "VEN-000505",
                "venue_name": "Blue Cross/Blue Shield Arena",
                "normalized_name": "bluecrossblueshieldarena",
                "name_type": "HISTORICAL_OR_ALIAS",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "test",
                "notes": "",
            }
        ]

        # Alias detection itself still requires compatible geography, so use
        # an exact compatible city for resolution and then verify the reused
        # row receives registry-owned geography.
        locals_[0]["city"] = "Rochester"

        local_rows, _globals, _names, mappings = rebase_venues(
            "test-school",
            locals_,
            globals_,
            names,
        )

        self.assertEqual(local_rows[0]["venue_id"], "VEN-000505")
        self.assertEqual(local_rows[0]["venue_key"], "rochester-war-memorial")
        self.assertEqual(local_rows[0]["city"], "Rochester")
        self.assertEqual(local_rows[0]["state"], "NY")
        self.assertEqual(
            mappings[0]["resolution"],
            "REUSE_REGISTERED_ALIAS",
        )


    def test_foreign_exact_key_country_subdivision_rebase_uses_global_geography(self):
        venue = global_venue(
            "VEN-000358",
            "puerto-vallarta-international-convention-center",
            "Puerto Vallarta International Convention Center",
            "Puerto Vallarta",
            "MX",
        )
        local = {
            **local_venue("", city="Puerto Vallarta", state="Jalisco"),
            "venue_key": venue["venue_key"],
            "canonical_name": venue["display_name"],
        }
        report = venue_reconciliation_inventory([local], [venue], [])
        self.assertEqual(report["blocker_count"], 0)
        rebased, global_rows, _names, mappings = rebase_venues(
            "test-school", [local], [venue], []
        )
        self.assertEqual(rebased[0]["venue_id"], "VEN-000358")
        self.assertEqual(rebased[0]["state"], "MX")
        self.assertEqual(global_rows[0]["state"], "MX")
        self.assertEqual(mappings[0]["resolution"], "REUSE_EXACT_KEY")

    def test_exact_key_reuse_still_blocks_jurisdiction_conflict(self):
        globals_ = [
            global_venue(
                "VEN-000088",
                "imperial-arena",
                "Imperial Arena",
                "Nassau",
                "BS",
            )
        ]
        locals_ = [
            {
                **local_venue(
                    "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE.",
                    city="Miami",
                    state="FL",
                ),
                "venue_key": "imperial-arena",
                "canonical_name": "Imperial Arena",
            }
        ]

        with self.assertRaisesRegex(WorkflowError, "jurisdiction conflicts"):
            rebase_venues("test-school", locals_, globals_, [])

    def test_new_venue_disambiguates_existing_school_key_geography_collision(self):
        globals_ = []
        locals_ = [
            {
                **local_venue(
                    "New Cincinnati physical identity.",
                    city="Cincinnati",
                    state="OH",
                ),
                "source_program_key": "cincinnati",
                "venue_key": "armory-fieldhouse",
                "canonical_name": "Armory Fieldhouse",
            }
        ]
        existing_school_venues = [
            {
                "source_program_key": "tennessee",
                "venue_key": "armory-fieldhouse",
                "venue_id": "VEN-000199",
                "canonical_name": "Armory-Fieldhouse",
                "city": "Knoxville",
                "state": "TN",
                "_school_key": "tennessee",
            }
        ]

        local_rows, global_rows, _names, mappings = rebase_venues(
            "cincinnati",
            locals_,
            globals_,
            [],
            existing_school_venues=existing_school_venues,
        )

        self.assertEqual(len(global_rows), 1)
        self.assertEqual(local_rows[0]["venue_key"], "armory-fieldhouse-cincinnati")
        self.assertEqual(global_rows[0]["venue_key"], "armory-fieldhouse-cincinnati")
        self.assertEqual(
            mappings[0]["resolution"],
            "NEW_GLOBAL_IDENTITY_DISAMBIGUATED_KEY",
        )
        self.assertEqual(
            mappings[0]["final_venue_key"],
            "armory-fieldhouse-cincinnati",
        )

    def test_new_foreign_venue_uses_unanimous_source_country_as_registry_jurisdiction(self):
        locals_ = [
            {
                **local_venue(
                    "Historical identity resolved research-locally.",
                    city="Cork",
                    state="",
                ),
                "source_program_key": "saint-louis",
                "venue_key": "neptune-stadium-cork",
                "canonical_name": "Neptune Stadium",
            }
        ]
        source_games = [
            {
                "curated_venue_name": "Neptune Stadium",
                "source_venue_name": "",
                "city": "Cork",
                "state": "",
                "country": "IE",
            },
            {
                "curated_venue_name": "Neptune Stadium",
                "source_venue_name": "",
                "city": "Cork",
                "state": "",
                "country": "IE",
            },
        ]

        local_rows, global_rows, _names, mappings = rebase_venues(
            "saint-louis",
            locals_,
            [],
            [],
            source_games=source_games,
        )

        self.assertEqual(len(global_rows), 1)
        self.assertEqual(global_rows[0]["city"], "Cork")
        self.assertEqual(global_rows[0]["state"], "IE")
        self.assertEqual(local_rows[0]["state"], "IE")
        self.assertEqual(mappings[0]["resolution"], "NEW_GLOBAL_IDENTITY")
        self.assertEqual([row["state"] for row in source_games], ["", ""])
        self.assertEqual([row["country"] for row in source_games], ["IE", "IE"])

    def test_new_venue_does_not_use_domestic_country_as_missing_state(self):
        locals_ = [
            {
                **local_venue("", city="Orlando", state=""),
                "venue_key": "test-orlando-venue",
                "canonical_name": "Test Orlando Venue",
            }
        ]
        source_games = [
            {
                "curated_venue_name": "Test Orlando Venue",
                "source_venue_name": "",
                "city": "Orlando",
                "state": "",
                "country": "US",
            }
        ]

        local_rows, global_rows, _names, _mappings = rebase_venues(
            "test-school",
            locals_,
            [],
            [],
            source_games=source_games,
        )

        self.assertEqual(global_rows[0]["state"], "")
        self.assertEqual(local_rows[0]["state"], "")

    def test_new_foreign_venue_requires_unanimous_complete_country_evidence(self):
        locals_ = [
            {
                **local_venue("", city="Cork", state=""),
                "venue_key": "test-cork-venue",
                "canonical_name": "Test Cork Venue",
            }
        ]
        source_games = [
            {
                "curated_venue_name": "Test Cork Venue",
                "source_venue_name": "",
                "city": "Cork",
                "state": "",
                "country": "IE",
            },
            {
                "curated_venue_name": "Test Cork Venue",
                "source_venue_name": "",
                "city": "Cork",
                "state": "",
                "country": "",
            },
        ]

        local_rows, global_rows, _names, _mappings = rebase_venues(
            "test-school",
            locals_,
            [],
            [],
            source_games=source_games,
        )

        self.assertEqual(global_rows[0]["state"], "")
        self.assertEqual(local_rows[0]["state"], "")

    def test_research_base_reuse_hint_still_blocks_state_conflict(self):
        globals_ = [
            global_venue(
                "VEN-000038",
                "cfe-arena",
                "Addition Financial Arena",
                "Orlando",
                "FL",
            )
        ]
        locals_ = [
            local_venue(
                "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE; "
                "historical/local label maps to research-base key=cfe-arena; "
                "research-base venue_id=VEN-000038.",
                city="Atlanta",
                state="GA",
            )
        ]

        with self.assertRaisesRegex(WorkflowError, "jurisdiction conflicts"):
            rebase_venues("test-school", locals_, globals_, [])


class StageResearchPortfolioHistoryScopeTests(unittest.TestCase):
    def test_scope_expression_uses_explicit_intervals(self):
        self.assertEqual(
            accepted_top_level_scope_expression(
                start_season="1958-1959",
                basis="TOP_LEVEL_INTERVALS",
                intervals="1958-59+",
            ),
            "1958-59+",
        )

    def test_scope_expression_projects_inception_basis(self):
        self.assertEqual(
            accepted_top_level_scope_expression(
                start_season="1911-1912",
                basis="ALWAYS_TOP_LEVEL_FROM_INCEPTION",
                intervals="",
            ),
            "INCEPTION+",
        )

    def test_scope_expression_projects_first_top_level_season(self):
        self.assertEqual(
            accepted_top_level_scope_expression(
                start_season="1958-1959",
                basis="FIRST_TOP_LEVEL_SEASON",
                intervals="",
            ),
            "1958-59+",
        )

    def test_reconcile_scope_updates_only_target_row(self):
        rows = [
            {"school": "Boise State", "top_level_scope": "1970-71+"},
            {"school": "Gonzaga", "top_level_scope": "1952-53+"},
            {"school": "Saint Louis", "top_level_scope": "INCEPTION+"},
        ]
        result = reconcile_top_level_scope_reference(
            rows,
            {"program_name": "Gonzaga", "display_name": "Gonzaga"},
            accepted_scope="1958-59+",
        )
        self.assertEqual(result["action"], "UPDATED")
        self.assertEqual(result["prior_top_level_scope"], "1952-53+")
        self.assertEqual(rows[1]["top_level_scope"], "1958-59+")
        self.assertEqual(rows[0]["top_level_scope"], "1970-71+")
        self.assertEqual(rows[2]["top_level_scope"], "INCEPTION+")

    def test_reconcile_scope_confirmation_is_noop(self):
        rows = [{"school": "Gonzaga", "top_level_scope": "1958-59+"}]
        result = reconcile_top_level_scope_reference(
            rows,
            {"program_name": "Gonzaga", "display_name": "Gonzaga"},
            accepted_scope="1958-59+",
        )
        self.assertEqual(result["action"], "CONFIRMED")
        self.assertFalse(result["changed"])

    def test_scope_writer_preserves_reference_shape(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "program-top-level-scope.csv"
            path.write_text(
                'school,top_level_scope\n"Boise State","1970-71+"\n'
                '"Gonzaga","1952-53+"\n',
                encoding="utf-8",
            )
            rows = [
                {"school": "Boise State", "top_level_scope": "1970-71+"},
                {"school": "Gonzaga", "top_level_scope": "1958-59+"},
            ]
            write_top_level_scope_reference(
                path,
                ["school", "top_level_scope"],
                rows,
            )
            self.assertEqual(
                path.read_text(encoding="utf-8"),
                'school,top_level_scope\n"Boise State","1970-71+"\n'
                '"Gonzaga","1958-59+"\n',
            )

    def test_update_program_scope_persists_interrupted_intervals(self):
        programs = [
            {
                "program_key": "miami",
                "history_start_season": "",
                "history_scope_status": "",
                "history_scope_basis": "",
                "history_scope_notes": "",
                "history_scope_intervals": "",
            }
        ]
        intervals = "1948-49..1952-53|1954-55..1970-71|1985-86+"
        update_program_scope(
            programs,
            "miami",
            start_season="1948-1949",
            basis="TOP_LEVEL_INTERVALS",
            intervals=intervals,
            notes="Owner-confirmed interrupted scope.",
        )
        self.assertEqual(programs[0]["history_start_season"], "1948-1949")
        self.assertEqual(programs[0]["history_scope_basis"], "TOP_LEVEL_INTERVALS")
        self.assertEqual(programs[0]["history_scope_intervals"], intervals)


if __name__ == "__main__":
    unittest.main()
