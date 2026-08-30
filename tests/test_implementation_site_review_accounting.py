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
)


class ImplementationSiteReviewAccountingTests(unittest.TestCase):
    def test_field_specific_reconciliation_can_account_for_canonical_blank(self):
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

            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["public_gap_rows"], 1)
            self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 0)
            self.assertEqual(report["counts"]["target_source_information_loss"], 0)


if __name__ == "__main__":
    unittest.main()
