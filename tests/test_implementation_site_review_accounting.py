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
from test_implementation_site_gate import (  # noqa: E402
    ImplementationSiteGateTests,
    canonical_row,
    source_row,
    target_assertion,
)


class ImplementationSiteReviewAccountingTests(unittest.TestCase):
    def test_field_specific_reconciliation_cannot_waive_target_home_blank(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()
            fixture.make_repo(
                root,
                canonical=[
                    canonical_row(
                        venue_key="",
                        venue_id="",
                        site_city="",
                        site_state="",
                    )
                ],
                discrepancies=[
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "field_name": "venue",
                        "status": "UNDER_REVIEW",
                        "resolution_basis": "",
                    },
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "field_name": "location",
                        "status": "UNDER_REVIEW",
                        "resolution_basis": "",
                    },
                ],
            )

            report = implementation_site_report(root, "test")

            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["public_gap_rows"], 1)
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 1)
            self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 0)
            self.assertEqual(report["counts"]["target_source_information_loss"], 0)
            self.assertTrue(
                any("home-site completeness is non-waivable" in error for error in report["errors"])
            )

    def test_field_specific_reconciliation_can_account_for_neutral_blank(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()
            source = source_row(
                curated_site_type="NEUTRAL",
                curated_venue_name="",
                city="",
                state="",
                site_research_status="RESEARCHED_UNRESOLVED",
                site_research_basis="Neutral site remains under field-specific review.",
            )
            canonical = canonical_row(
                site_type="NEUTRAL",
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            )
            assertion = target_assertion(
                curated_site_type="NEUTRAL",
                curated_venue_name="",
                city="",
                state="",
            )
            fixture.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=[assertion],
                discrepancies=[
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "field_name": "venue",
                        "status": "UNDER_REVIEW",
                        "resolution_basis": "",
                    },
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "field_name": "location",
                        "status": "UNDER_REVIEW",
                        "resolution_basis": "",
                    },
                ],
            )

            report = implementation_site_report(root, "test")

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["public_gap_rows"], 1)
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 0)
            self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 0)


if __name__ == "__main__":
    unittest.main()
