import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
TESTS = ROOT / "tests"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TESTS))

from implementation_site_gate import implementation_site_report  # noqa: E402
from onboarding_plan import (  # noqa: E402
    _record_dependent_site_gap_discrepancies,
    _record_reconciled_unresolved_home_venue_markers,
)
from test_implementation_site_gate import (  # noqa: E402
    ImplementationSiteGateTests,
    canonical_row,
    source_row,
    target_assertion,
)


class OnboardingSiteReconciliationProvenanceTests(unittest.TestCase):
    def test_reconciled_home_venue_exception_passes_without_rewriting_target_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()

            source = source_row(
                curated_site_type="OPPONENT_HOME",
                curated_venue_name="",
                city="",
                state="",
            )
            canonical = canonical_row(
                site_type="TEAM_B_HOME",
                venue_key="",
                venue_id="",
                site_city="Example City",
                site_state="EX",
                notes=(
                    "[RECONCILED_UNRESOLVED_HOME_VENUE "
                    "source=test/TESTRAW-00001 reciprocal=other/OTHRAW-1]"
                ),
            )
            assertions = [
                target_assertion(
                    curated_site_type="OPPONENT_HOME",
                    curated_venue_name="",
                    city="",
                    state="",
                ),
                {
                    "canonical_game_id": "CBBG-0000001",
                    "source_program_key": "other",
                    "source_game_id": "OTHRAW-1",
                    "normalized_opponent_key": "test",
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_venue_name": "",
                    "city": "Example City",
                    "state": "EX",
                },
            ]
            discrepancies = [
                {
                    "canonical_game_id": "CBBG-0000001",
                    "source_a_program_key": "test",
                    "field_name": "site_type",
                    "status": "RESOLVED",
                    "resolution_basis": (
                        "Owner-approved reciprocal evidence establishes test HOME."
                    ),
                }
            ]

            fixture.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=assertions,
                discrepancies=discrepancies,
            )

            report = implementation_site_report(root, "test")

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 0)
            self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 0)
            self.assertEqual(
                report["counts"]["reconciled_unresolved_home_venue"],
                1,
            )

    def test_known_agreeing_reciprocal_venue_defeats_reconciled_exception(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()

            source = source_row(
                curated_site_type="OPPONENT_HOME",
                curated_venue_name="",
                city="",
                state="",
            )
            canonical = canonical_row(
                site_type="TEAM_B_HOME",
                venue_key="",
                venue_id="",
                site_city="Example City",
                site_state="EX",
                notes=(
                    "[RECONCILED_UNRESOLVED_HOME_VENUE "
                    "source=test/TESTRAW-00001 reciprocal=other/OTHRAW-1]"
                ),
            )
            assertions = [
                target_assertion(
                    curated_site_type="OPPONENT_HOME",
                    curated_venue_name="",
                    city="",
                    state="",
                ),
                {
                    "canonical_game_id": "CBBG-0000001",
                    "source_program_key": "other",
                    "source_game_id": "OTHRAW-1",
                    "normalized_opponent_key": "test",
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_venue_name": "Known Arena",
                    "city": "Example City",
                    "state": "EX",
                },
            ]
            discrepancies = [
                {
                    "canonical_game_id": "CBBG-0000001",
                    "source_a_program_key": "test",
                    "field_name": "site_type",
                    "status": "RESOLVED",
                    "resolution_basis": "Owner-approved site resolution.",
                }
            ]

            fixture.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=assertions,
                discrepancies=discrepancies,
            )

            report = implementation_site_report(root, "test")

            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 1)
            self.assertEqual(
                report["counts"]["invalid_home_venue_exception_marker_rows"],
                1,
            )

    def test_dependent_site_gap_provenance_is_field_specific_and_idempotent(self):
        canonical = {
            "canonical_game_id": "CBBG-1",
            "team_a_key": "other",
            "team_b_key": "test",
            "site_type": "NEUTRAL",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
        }
        source = {
            "source_game_id": "TESTRAW-1",
            "source_program_key": "test",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "Source Arena",
            "city": "Example City",
            "state": "EX",
        }
        items = [
            {
                "decision_id": "D-1",
                "canonical_game_id": "CBBG-1",
                "source_game_id": "TESTRAW-1",
                "field_name": "site_type",
                "decision": "LEAVE_UNRESOLVED",
                "resolution_basis": "Owner approved preservation of the H/A/N conflict.",
            }
        ]
        discrepancies = []

        first = _record_dependent_site_gap_discrepancies(
            "test",
            items,
            {"CBBG-1": canonical},
            {"TESTRAW-1": source},
            discrepancies,
        )
        second = _record_dependent_site_gap_discrepancies(
            "test",
            items,
            {"CBBG-1": canonical},
            {"TESTRAW-1": source},
            discrepancies,
        )

        self.assertEqual(first["dependent_site_gap_discrepancies_added"], 2)
        self.assertEqual(
            second["dependent_site_gap_discrepancies_existing"],
            2,
        )
        self.assertEqual(len(discrepancies), 2)
        self.assertEqual(
            {row["field_name"] for row in discrepancies},
            {"venue", "location"},
        )
        self.assertTrue(
            all(row["status"] == "UNDER_REVIEW" for row in discrepancies)
        )

    def test_reconciled_home_marker_is_generated_from_resolved_site_conflict(self):
        canonical = {
            "canonical_game_id": "CBBG-1",
            "team_a_key": "other",
            "team_b_key": "test",
            "site_type": "TEAM_B_HOME",
            "venue_key": "",
            "venue_id": "",
            "site_city": "Example City",
            "site_state": "EX",
            "game_type": "REGULAR_SEASON",
            "notes": "",
        }
        source = {
            "source_game_id": "TESTRAW-1",
            "source_program_key": "test",
            "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": "",
            "city": "",
            "state": "",
        }
        reciprocal = {
            "canonical_game_id": "CBBG-1",
            "source_program_key": "other",
            "source_game_id": "OTHRAW-1",
            "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": "",
            "city": "Example City",
            "state": "EX",
        }
        items = [
            {
                "decision_id": "D-1",
                "canonical_game_id": "CBBG-1",
                "source_game_id": "TESTRAW-1",
                "field_name": "site_type",
                "decision": "KEEP_CANONICAL",
                "resolution_basis": "Owner approved reciprocal HOME evidence.",
            }
        ]
        discrepancies = [
            {
                "canonical_game_id": "CBBG-1",
                "field_name": "site_type",
                "source_a_program_key": "test",
                "status": "RESOLVED",
                "resolution_basis": "Owner approved reciprocal HOME evidence.",
            }
        ]

        result = _record_reconciled_unresolved_home_venue_markers(
            "test",
            items,
            {"CBBG-1": canonical},
            {"TESTRAW-1": source},
            [reciprocal],
            discrepancies,
        )

        self.assertEqual(result["reconciled_home_venue_markers_added"], 1)
        self.assertIn(
            "[RECONCILED_UNRESOLVED_HOME_VENUE "
            "source=test/TESTRAW-1 reciprocal=other/OTHRAW-1]",
            canonical["notes"],
        )


if __name__ == "__main__":
    unittest.main()
