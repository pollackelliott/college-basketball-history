import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remote_implementation_io import Stop  # noqa: E402
from remote_implementation_venue_maintenance import (  # noqa: E402
    _parse_apply_result,
    _validate_changed_paths,
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

    def test_geography_only_diff_does_not_require_name_registry(self):
        spec_path = (
            "data/reconciliation/venue-identity-maintenance/"
            "fresno-state-stage1.json"
        )
        plan = {
            "merges": [],
            "geography_corrections": [
                {
                    "school_files": [
                        {
                            "path": "schools/west-virginia/venues.csv",
                            "row_count": 1,
                        }
                    ]
                }
            ],
        }
        changed = [
            "data/reference/venues.csv",
            "data/canonical/games.csv",
            "schools/west-virginia/venues.csv",
            spec_path,
        ]

        allowed = _validate_changed_paths(changed, plan, spec_path)

        self.assertIn("data/reference/venues.csv", allowed)
        self.assertIn("data/canonical/games.csv", allowed)
        self.assertNotIn("data/reference/venue-names.csv", allowed)
        self.assertNotIn("data/evidence/game-assertions.csv", allowed)
        self.assertNotIn("data/evidence/ncaa-tournament-sites.csv", allowed)

    def test_geography_only_diff_rejects_source_evidence_mutation(self):
        spec_path = (
            "data/reconciliation/venue-identity-maintenance/"
            "fresno-state-stage1.json"
        )
        plan = {
            "merges": [],
            "geography_corrections": [{"school_files": []}],
        }
        changed = [
            "data/reference/venues.csv",
            "data/evidence/game-assertions.csv",
            spec_path,
        ]

        with self.assertRaisesRegex(
            Stop,
            "VENUE_MAINTENANCE_DIFF_OUTSIDE_CONTRACT",
        ):
            _validate_changed_paths(changed, plan, spec_path)

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
