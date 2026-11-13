"""Composed semantic contract for one representative ALL_HISTORY_EXPANSION program."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from all_history_expansion_research import (  # noqa: E402
    project_complete_institutional_program_row,
    validate_expansion_baseline_program,
)
from program_history import (  # noqa: E402
    partition_stage2_source_rows,
    publication_conference_timeline,
    publication_history_start,
    season_is_top_level,
)
from remote_implementation_control import (  # noqa: E402
    FINAL_RELEASE_CONTINUATION_KIND,
    OP_RELEASE_GATE2_APPROVAL,
    OP_RELEASE_READINESS,
    OP_STAGE2_GATE1_FILL,
    OP_STAGE2_GATE1_SEAL,
    OP_STAGE2_PRESEAL_REHEARSAL,
    RELEASE_PHASE_CONTINUATION_KIND,
    STAGE2_POST_GATE1_CONTINUATION_KIND,
    validate_final_release_continuation,
    validate_release_phase_continuation,
    validate_stage2_phase_continuation,
)


class AllHistoryExpansionImplementationCompositionTests(unittest.TestCase):
    def setUp(self):
        self.legacy = {
            "program_key": "sample",
            "program_name": "Sample",
            "display_name": "Sample",
            "public_page_enabled": "Yes",
            "program_inception_season": "",
            "history_coverage_status": "LEGACY_TOP_LEVEL_ONLY",
            "history_start_season": "1978-1979",
            "history_scope_status": "OWNER_CONFIRMED",
            "history_scope_basis": "FIRST_TOP_LEVEL_SEASON",
            "history_scope_notes": "Accepted top-level history begins 1978-79.",
            "history_scope_intervals": "",
        }

    def test_representative_expansion_semantics_and_continuations_compose(self):
        validate_expansion_baseline_program(self.legacy)
        complete = project_complete_institutional_program_row(
            self.legacy, "1966-1967"
        )

        changed = {
            key for key in complete
            if complete[key] != self.legacy[key]
        }
        self.assertEqual(
            changed,
            {"program_inception_season", "history_coverage_status"},
        )
        self.assertEqual(publication_history_start(complete), "1966-1967")
        self.assertEqual(complete["history_start_season"], "1978-1979")

        rows = [
            {"source_game_id": "PRE", "season_label": "1965-1966"},
            {"source_game_id": "EARLY-1", "season_label": "1966-1967"},
            {"source_game_id": "EARLY-2", "season_label": "1977-1978"},
            {"source_game_id": "TOP", "season_label": "1978-1979"},
        ]
        published, unpublished, top_level = partition_stage2_source_rows(
            rows, complete
        )
        self.assertEqual(
            [row["source_game_id"] for row in published],
            ["EARLY-1", "EARLY-2", "TOP"],
        )
        self.assertEqual(
            [row["source_game_id"] for row in unpublished],
            ["PRE"],
        )
        self.assertEqual(
            [row["source_game_id"] for row in top_level],
            ["TOP"],
        )
        self.assertFalse(
            season_is_top_level(
                "1977-1978",
                complete["history_start_season"],
                complete["history_scope_intervals"],
            )
        )

        timeline = publication_conference_timeline(
            [
                {
                    "start_season": "1978-1979",
                    "end_season": "",
                    "conference_key": "sample-conference",
                    "conference_name": "Sample Conference",
                    "membership_type": "conference",
                    "classification": "D1",
                }
            ],
            complete,
            ["1966-1967", "1967-1968", "1977-1978", "1978-1979"],
        )
        synthetic = [
            row for row in timeline
            if row.get("classification") == "NON_D1_CLASSIFICATION"
        ]
        self.assertEqual(
            synthetic,
            [
                {
                    "start_season": "1966-1967",
                    "end_season": "1967-1968",
                    "conference_key": "",
                    "conference_name": "Non-D1",
                    "membership_type": "classification",
                    "classification": "NON_D1_CLASSIFICATION",
                },
                {
                    "start_season": "1977-1978",
                    "end_season": "1977-1978",
                    "conference_key": "",
                    "conference_name": "Non-D1",
                    "membership_type": "classification",
                    "classification": "NON_D1_CLASSIFICATION",
                },
            ],
        )

        post_gate1 = {
            "kind": STAGE2_POST_GATE1_CONTINUATION_KIND,
            "preseal_request_id": "sample-preseal-0001",
            "seal_request_id": "sample-seal-0001",
            "apply_request_id": "sample-apply-0001",
        }
        validate_stage2_phase_continuation(
            OP_STAGE2_GATE1_FILL, "sample-fill-0001", post_gate1
        )
        validate_stage2_phase_continuation(
            OP_STAGE2_PRESEAL_REHEARSAL,
            post_gate1["preseal_request_id"],
            post_gate1,
        )
        validate_stage2_phase_continuation(
            OP_STAGE2_GATE1_SEAL,
            post_gate1["seal_request_id"],
            post_gate1,
        )

        release = {
            "kind": RELEASE_PHASE_CONTINUATION_KIND,
            "preview_request_id": "sample-preview-0001",
        }
        validate_release_phase_continuation(
            OP_RELEASE_READINESS, "sample-readiness-0001", release
        )

        final = {
            "kind": FINAL_RELEASE_CONTINUATION_KIND,
            "production_request_id": "sample-production-0001",
        }
        validate_final_release_continuation(
            OP_RELEASE_GATE2_APPROVAL, "sample-gate2-0001", final
        )


if __name__ == "__main__":
    unittest.main()
