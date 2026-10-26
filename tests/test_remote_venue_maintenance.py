import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remote_implementation_io import Stop  # noqa: E402
from remote_implementation_venue_maintenance import (  # noqa: E402
    _parse_apply_result,
    validate_repository_spec_path,
)


class RemoteVenueMaintenanceTests(unittest.TestCase):
    def test_repository_spec_path_is_school_scoped(self):
        self.assertEqual(
            validate_repository_spec_path(
                "gonzaga",
                "data/reconciliation/venue-identity-maintenance/gonzaga-stage1.json",
            ),
            "data/reconciliation/venue-identity-maintenance/gonzaga-stage1.json",
        )

    def test_repository_spec_path_rejects_other_school(self):
        with self.assertRaisesRegex(
            Stop,
            "VENUE_MAINTENANCE_REPOSITORY_SPEC_PATH_INVALID",
        ):
            validate_repository_spec_path(
                "gonzaga",
                "data/reconciliation/venue-identity-maintenance/ucla-stage1.json",
            )

    def test_apply_result_requires_permanent_tool_pass_record(self):
        result = _parse_apply_result(
            'noise\nPASS: {"venues_retired":1,"canonical_rows_updated":3}\n'
        )
        self.assertEqual(result["venues_retired"], 1)
        self.assertEqual(result["canonical_rows_updated"], 3)

    def test_apply_result_rejects_missing_pass(self):
        with self.assertRaisesRegex(
            Stop,
            "VENUE_MAINTENANCE_APPLY_RESULT_MISSING",
        ):
            _parse_apply_result("FAIL: fixture\n")


if __name__ == "__main__":
    unittest.main()
