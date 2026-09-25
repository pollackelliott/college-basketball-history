import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import WorkflowError  # noqa: E402
from stage_research_portfolio import rebase_venues  # noqa: E402


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


class StageResearchPortfolioVenueReuseTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
