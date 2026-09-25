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
        self.assertEqual(local_rows[0]["city"], "Lake Buena Vista")
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
        self.assertEqual(local_rows[0]["city"], "Paradise Island")
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
        self.assertEqual(local_rows[0]["state"], "Ohio")
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
