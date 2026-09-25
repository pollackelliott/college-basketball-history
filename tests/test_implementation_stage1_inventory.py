import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from stage_research_portfolio import (  # noqa: E402
    build_stage1_reconciliation_inventory,
    program_alias_inventory,
    venue_reconciliation_inventory,
)


def global_venue(
    venue_id: str,
    venue_key: str,
    name: str,
    city: str,
    state: str,
    *,
    notes: str = "",
    identity_status: str = "TEST",
):
    return {
        "venue_id": venue_id,
        "venue_key": venue_key,
        "display_name": name,
        "city": city,
        "state": state,
        "opened": "",
        "closed": "",
        "date_precision": "",
        "identity_status": identity_status,
        "source_basis": "test",
        "notes": notes,
    }


def venue_name(
    venue_id: str,
    name: str,
    name_type: str = "HISTORICAL_OR_ALIAS",
):
    normalized = "".join(ch.lower() for ch in name if ch.isalnum())
    return {
        "venue_id": venue_id,
        "venue_name": name,
        "normalized_name": normalized,
        "name_type": name_type,
        "valid_from": "",
        "valid_to": "",
        "date_precision": "",
        "source_basis": "test",
        "notes": "",
    }


def local_venue(
    key: str,
    name: str,
    *,
    aliases: str = "",
    city: str = "",
    state: str = "",
    notes: str = "",
):
    return {
        "source_program_key": "test-school",
        "venue_key": key,
        "venue_id": "",
        "canonical_name": name,
        "aliases": aliases,
        "city": city,
        "state": state,
        "venue_type": "",
        "known_opened": "",
        "known_closed": "",
        "venue_date_precision": "unknown",
        "games_currently_assigned": "1",
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


class Stage1VenueInventoryTests(unittest.TestCase):
    def test_safe_reuse_reports_geography_normalization_without_mutation(self):
        local = local_venue(
            "hp-field-house",
            "HP Field House",
            city="Lake Buena Vista",
            state="FL",
            notes=(
                "Research physical identity: DEFINITE_RESEARCH_BASE_REUSE; "
                "historical/local label maps to research-base key=hp-field-house; "
                "research-base venue_id=VEN-000084."
            ),
        )
        global_row = global_venue(
            "VEN-000084",
            "hp-field-house",
            "HP Field House",
            "Orlando",
            "FL",
        )
        report = venue_reconciliation_inventory(
            [local],
            [global_row],
            [venue_name("VEN-000084", "HP Field House", "PROJECT_DISPLAY")],
        )

        self.assertEqual(report["blocker_count"], 0)
        row = report["rows"][0]
        self.assertEqual(row["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(row["resolution"], "REUSE_RESEARCH_BASE_IDENTITY")
        self.assertEqual(row["target_venue_id"], "VEN-000084")
        self.assertIn("CANONICAL_GEOGRAPHY_NORMALIZATION", row["issues"])
        self.assertEqual(local["city"], "Lake Buena Vista")

    def test_research_deferred_exact_key_is_one_shared_maintenance_blocker(self):
        local = local_venue(
            "the-pit",
            "The Pit",
            aliases="Bob King Court",
            city="Albuquerque",
            state="NM",
            notes=(
                "Research-base registry contains multiple University Arena/The Pit "
                "physical IDs for the same Albuquerque building; Research resolves "
                "one physical building and defers authoritative ID reconciliation "
                "to Implementation."
            ),
        )
        report = venue_reconciliation_inventory(
            [local],
            [
                global_venue(
                    "VEN-000208",
                    "the-pit",
                    "The Pit",
                    "Albuquerque",
                    "NM",
                )
            ],
            [venue_name("VEN-000208", "The Pit", "PROJECT_DISPLAY")],
        )

        self.assertEqual(report["blocker_count"], 1)
        row = report["blockers"][0]
        self.assertEqual(row["classification"], "SHARED_GLOBAL_MAINTENANCE")
        self.assertIn(
            "RESEARCH_SETTLED_GLOBAL_RECONCILIATION_PENDING",
            row["issues"],
        )

    def test_reconciled_survivor_note_closes_research_deferred_exact_key(self):
        local = local_venue(
            "the-pit",
            "The Pit",
            aliases="Bob King Court",
            city="Albuquerque",
            state="NM",
            notes=(
                "Research resolves one physical building and defers authoritative "
                "ID reconciliation to Implementation."
            ),
        )
        survivor = global_venue(
            "VEN-000208",
            "the-pit",
            "The Pit",
            "Albuquerque",
            "NM",
            notes=(
                "VEN-000427 retired during shared-reference reconciliation after "
                "determining University Arena (The Pit) and The Pit are the same venue."
            ),
        )
        report = venue_reconciliation_inventory(
            [local],
            [survivor],
            [venue_name("VEN-000208", "The Pit", "PROJECT_DISPLAY")],
        )

        self.assertEqual(report["blocker_count"], 0)
        self.assertEqual(
            report["rows"][0]["classification"],
            "SAFE_REPRESENTATION_REUSE",
        )

    def test_conflicting_registered_name_identity_is_collected_not_raised(self):
        local = local_venue(
            "rocket-arena",
            "Rocket Arena",
            aliases="Rocket Mortgage FieldHouse",
            city="Cleveland",
            state="OH",
            notes=(
                "Research resolves the building as one physical identity and defers "
                "authoritative ID reconciliation to Implementation."
            ),
        )
        globals_ = [
            global_venue(
                "VEN-000179",
                "rocket-arena",
                "Rocket Arena",
                "Cleveland",
                "OH",
            ),
            global_venue(
                "VEN-000420",
                "rocket-mortgage-fieldhouse",
                "Rocket Mortgage FieldHouse",
                "Cleveland",
                "OH",
            ),
        ]
        names = [
            venue_name("VEN-000179", "Rocket Arena", "PROJECT_DISPLAY"),
            venue_name(
                "VEN-000420",
                "Rocket Mortgage FieldHouse",
                "PROJECT_DISPLAY",
            ),
        ]

        report = venue_reconciliation_inventory([local], globals_, names)

        self.assertEqual(report["blocker_count"], 1)
        self.assertEqual(
            report["blockers"][0]["classification"],
            "SHARED_GLOBAL_MAINTENANCE",
        )
        self.assertEqual(
            report["blockers"][0]["candidate_venue_ids"],
            ["VEN-000179", "VEN-000420"],
        )

    def test_resolved_history_without_registered_current_name_is_maintenance(self):
        local = local_venue(
            "birmingham-city-auditorium-birmingham",
            "Municipal Auditorium (Birmingham)",
            aliases="Municipal Auditorium",
            city="Birmingham",
            state="AL",
            notes=(
                "Historical physical identity: RESOLVED. Research-base exact/unique "
                "alias reconciliation did not establish one authoritative shared venue "
                "identity. Global registration/current-main reuse decision remains for "
                "serialized Implementation."
            ),
        )
        global_row = global_venue(
            "VEN-000515",
            "birmingham-city-auditorium",
            "Birmingham City Auditorium",
            "Birmingham",
            "AL",
        )

        report = venue_reconciliation_inventory(
            [local],
            [global_row],
            [venue_name("VEN-000515", "Birmingham City Auditorium", "PROJECT_DISPLAY")],
        )

        self.assertEqual(report["blocker_count"], 1)
        row = report["blockers"][0]
        self.assertEqual(row["classification"], "SHARED_GLOBAL_MAINTENANCE")
        self.assertEqual(row["candidate_venue_ids"], [])
        self.assertIn(
            "RESEARCH_SETTLED_GLOBAL_RECONCILIATION_PENDING",
            row["issues"],
        )

    def test_registered_alias_closes_resolved_history_name_gap(self):
        local = local_venue(
            "birmingham-city-auditorium-birmingham",
            "Municipal Auditorium (Birmingham)",
            aliases="Municipal Auditorium",
            city="Birmingham",
            state="AL",
            notes=(
                "Historical physical identity: RESOLVED. Global registration/current-main "
                "reuse decision remains for serialized Implementation."
            ),
        )
        global_row = global_venue(
            "VEN-000515",
            "birmingham-city-auditorium",
            "Birmingham City Auditorium",
            "Birmingham",
            "AL",
        )
        names = [
            venue_name("VEN-000515", "Birmingham City Auditorium", "PROJECT_DISPLAY"),
            venue_name(
                "VEN-000515",
                "Municipal Auditorium (Birmingham)",
                "HISTORICAL_OR_ALIAS",
            ),
            venue_name(
                "VEN-000515",
                "Municipal Auditorium",
                "HISTORICAL_OR_ALIAS",
            ),
        ]

        report = venue_reconciliation_inventory([local], [global_row], names)

        self.assertEqual(report["blocker_count"], 0)
        row = report["rows"][0]
        self.assertEqual(row["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(row["resolution"], "REUSE_REGISTERED_ALIAS")
        self.assertEqual(row["target_venue_id"], "VEN-000515")

    def test_inventory_collects_multiple_blockers_in_one_pass(self):
        deferred = local_venue(
            "the-pit",
            "The Pit",
            city="Albuquerque",
            state="NM",
            notes=(
                "Research resolves one physical building and defers authoritative "
                "ID reconciliation to Implementation."
            ),
        )
        ambiguous = local_venue(
            "local-arena",
            "Shared Arena",
            city="Test City",
            state="TX",
        )
        globals_ = [
            global_venue(
                "VEN-000208",
                "the-pit",
                "The Pit",
                "Albuquerque",
                "NM",
            ),
            global_venue(
                "VEN-000300",
                "shared-arena-a",
                "Shared Arena",
                "Test City",
                "TX",
            ),
            global_venue(
                "VEN-000301",
                "shared-arena-b",
                "Shared Arena",
                "Test City",
                "TX",
            ),
        ]
        names = [
            venue_name("VEN-000208", "The Pit", "PROJECT_DISPLAY"),
            venue_name("VEN-000300", "Shared Arena", "PROJECT_DISPLAY"),
            venue_name("VEN-000301", "Shared Arena", "PROJECT_DISPLAY"),
        ]

        report = venue_reconciliation_inventory(
            [deferred, ambiguous],
            globals_,
            names,
        )

        self.assertEqual(report["blocker_count"], 2)
        self.assertEqual(
            report["classification_counts"]["SHARED_GLOBAL_MAINTENANCE"],
            1,
        )
        self.assertEqual(
            report["classification_counts"]["STOP_AMBIGUOUS"],
            1,
        )


    def test_exact_key_researched_split_ignores_generic_name_overlap(self):
        local = local_venue(
            "arena-1968",
            "Shared Arena IV",
            aliases="Shared Arena",
            city="New York",
            state="NY",
        )
        globals_ = [
            global_venue(
                "VEN-000100",
                "arena-1925",
                "Shared Arena",
                "New York",
                "NY",
                identity_status="RESEARCHED_SPLIT",
            ),
            global_venue(
                "VEN-000101",
                "arena-1968",
                "Shared Arena",
                "New York",
                "NY",
                identity_status="RESEARCHED_SPLIT",
            ),
        ]
        names = [
            venue_name("VEN-000100", "Shared Arena", "PROJECT_DISPLAY"),
            venue_name("VEN-000101", "Shared Arena", "PROJECT_DISPLAY"),
            venue_name("VEN-000101", "Shared Arena IV", "HISTORICAL_OR_ALIAS"),
        ]

        report = venue_reconciliation_inventory([local], globals_, names)

        self.assertEqual(report["blocker_count"], 0)
        row = report["rows"][0]
        self.assertEqual(row["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(row["target_venue_id"], "VEN-000101")
        self.assertIn("INTENTIONAL_RESEARCHED_SPLIT_NAME_OVERLAP", row["issues"])

    def test_exact_key_non_split_duplicate_name_remains_blocked(self):
        local = local_venue(
            "memorial-coliseum-kentucky",
            "Memorial Coliseum",
            city="Lexington",
            state="KY",
        )
        globals_ = [
            global_venue(
                "VEN-000129",
                "memorial-coliseum-kentucky",
                "Memorial Coliseum",
                "Lexington",
                "KY",
            ),
            global_venue(
                "VEN-000407",
                "memorial-coliseum-lexington",
                "Memorial Coliseum (Lexington)",
                "Lexington",
                "KY",
            ),
        ]
        names = [
            venue_name("VEN-000129", "Memorial Coliseum", "PROJECT_DISPLAY"),
            venue_name("VEN-000407", "Memorial Coliseum (Lexington)", "PROJECT_DISPLAY"),
            venue_name("VEN-000407", "Memorial Coliseum", "HISTORICAL_OR_ALIAS"),
        ]

        report = venue_reconciliation_inventory([local], globals_, names)

        self.assertEqual(report["blocker_count"], 1)
        self.assertEqual(
            report["blockers"][0]["issues"],
            ["CONFLICTING_REGISTERED_NAME_IDENTITIES"],
        )

    def test_us_virgin_islands_jurisdiction_normalizes_to_vi(self):
        local = local_venue(
            "sports-and-fitness-center",
            "Sports and Fitness Center",
            city="St. Thomas",
            state="U.S. Virgin Islands",
        )
        global_row = global_venue(
            "VEN-000191",
            "sports-and-fitness-center",
            "Sports and Fitness Center",
            "St. Thomas",
            "VI",
        )
        report = venue_reconciliation_inventory(
            [local],
            [global_row],
            [venue_name("VEN-000191", "Sports and Fitness Center", "PROJECT_DISPLAY")],
        )

        self.assertEqual(report["blocker_count"], 0)
        row = report["rows"][0]
        self.assertEqual(row["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(row["target_venue_id"], "VEN-000191")
        self.assertIn("CANONICAL_GEOGRAPHY_NORMALIZATION", row["issues"])


class Stage1ProgramInventoryTests(unittest.TestCase):
    def test_program_alias_inventory_collects_ambiguous_verified_alias(self):
        programs = [
            {"program_key": "a"},
            {"program_key": "b"},
        ]
        aliases = [
            {
                "program_key": "a",
                "alias_name": "Old College",
                "verification_status": "VERIFIED",
                "effective_start_season": "",
                "effective_end_season": "",
            },
            {
                "program_key": "b",
                "alias_name": "Old College",
                "verification_status": "VERIFIED",
                "effective_start_season": "",
                "effective_end_season": "",
            },
        ]
        opponents = [
            {
                "source_opponent_label": "Old College",
                "canonical_opponent_key": "old-college",
                "canonical_opponent_name": "Old College",
                "first_season": "1950-1951",
                "last_season": "1950-1951",
            }
        ]

        report = program_alias_inventory(programs, aliases, opponents)

        self.assertEqual(report["blocker_count"], 1)
        self.assertEqual(
            report["rows"][0]["classification"],
            "STOP_AMBIGUOUS",
        )
        self.assertEqual(
            report["rows"][0]["candidate_program_keys"],
            ["a", "b"],
        )

    def test_full_inventory_status_prefers_maintenance_over_ambiguity(self):
        local = local_venue(
            "the-pit",
            "The Pit",
            city="Albuquerque",
            state="NM",
            notes=(
                "Research resolves one physical building and defers authoritative "
                "ID reconciliation to Implementation."
            ),
        )
        report = build_stage1_reconciliation_inventory(
            "test-school",
            [local],
            [
                global_venue(
                    "VEN-000208",
                    "the-pit",
                    "The Pit",
                    "Albuquerque",
                    "NM",
                )
            ],
            [venue_name("VEN-000208", "The Pit", "PROJECT_DISPLAY")],
            [{"program_key": "a"}],
            [],
            [],
        )

        self.assertEqual(report["status"], "MAINTENANCE_REQUIRED")
        self.assertEqual(report["maintenance_required_count"], 1)


if __name__ == "__main__":
    unittest.main()
