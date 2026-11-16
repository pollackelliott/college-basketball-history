import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from home_location_exception_authority import (  # noqa: E402
    HOME_LOCATION_EXCEPTION_MARKER,
    RESEARCHED_UNRESOLVED_HOME_LOCATION_STATUS,
    owner_authorized_home_location_exception,
)
from implementation_site_gate import implementation_site_report  # noqa: E402
from ingest_school import build_new_canonical  # noqa: E402
from published_site_standard import published_site_standard_report  # noqa: E402
from site_completeness import source_site_completeness_report  # noqa: E402


SOURCE_FIELDS = [
    "source_game_id", "source_program_key", "season_label", "game_date",
    "source_opponent_label", "normalized_opponent_key", "normalized_opponent_name",
    "team_score", "opponent_score", "played_result", "overtime_periods",
    "source_site_candidate", "curated_site_type", "source_venue_name",
    "curated_venue_name", "city", "state", "country", "event_or_tournament",
    "source_round", "curated_game_type", "curated_postseason_round", "source_page",
    "raw_text", "normalization_status", "administrative_status",
    "administrative_note", "notes", "site_research_status", "site_research_basis",
]


def authority_source(**overrides):
    row = {field: "" for field in SOURCE_FIELDS}
    row.update({
        "source_game_id": "UCF-EXP-197374-002",
        "source_program_key": "ucf",
        "season_label": "1973-1974",
        "game_date": "1973-12-05",
        "source_opponent_label": "St. Leo",
        "normalized_opponent_key": "saint-leo",
        "normalized_opponent_name": "Saint Leo",
        "team_score": "65",
        "opponent_score": "49",
        "played_result": "W",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_game_type": "REGULAR_SEASON",
        "normalization_status": "RESEARCH_ACCEPTED",
        "site_research_status": RESEARCHED_UNRESOLVED_HOME_LOCATION_STATUS,
        "site_research_basis": (
            "Bounded target/facility/reciprocal/archive paths exhausted; "
            "locality and building unsupported."
        ),
    })
    row.update(overrides)
    return row


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class HomeLocationAuthorityTests(unittest.TestCase):
    def test_exact_registered_ucf_row_is_authorized(self):
        self.assertTrue(owner_authorized_home_location_exception(authority_source()))
        self.assertFalse(
            owner_authorized_home_location_exception(
                authority_source(team_score="66")
            )
        )

    def test_registered_source_gap_passes_but_unregistered_gap_fails(self):
        good = source_site_completeness_report(SOURCE_FIELDS, [authority_source()])
        self.assertEqual(good["errors"], [])
        self.assertEqual(good["counts"]["home_publication_blocker_rows"], 0)
        self.assertEqual(good["counts"]["researched_unresolved_home_location_rows"], 1)

        bad = source_site_completeness_report(
            SOURCE_FIELDS,
            [authority_source(source_game_id="UCF-NOT-REGISTERED")],
        )
        self.assertEqual(bad["counts"]["home_publication_blocker_rows"], 1)
        self.assertTrue(
            any("RESEARCHED_UNRESOLVED_HOME_LOCATION" in error for error in bad["errors"])
        )

    def test_ncaa_cannot_use_registered_location_exception(self):
        report = source_site_completeness_report(
            SOURCE_FIELDS,
            [authority_source(curated_game_type="NCAA_TOURNAMENT")],
        )
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)

    def test_ingest_preserves_explicit_canonical_marker(self):
        canonical = build_new_canonical(
            authority_source(),
            "CBBG-TEST",
            {},
            {},
        )
        self.assertEqual(canonical["site_city"], "")
        self.assertEqual(canonical["site_state"], "")
        self.assertEqual(canonical["venue_key"], "")
        self.assertIn(
            f"{HOME_LOCATION_EXCEPTION_MARKER} source=ucf/UCF-EXP-197374-002]",
            canonical["notes"],
        )

    def test_implementation_and_published_gates_accept_exact_registered_unknown(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = authority_source()
            write_csv(root / "schools/ucf/source-games.csv", SOURCE_FIELDS, [source])
            program_fields = [
                "program_key", "history_start_season", "history_scope_intervals",
                "public_page_enabled", "history_coverage_status",
                "program_inception_season",
            ]
            write_csv(
                root / "data/reference/programs.csv",
                program_fields,
                [
                    {
                        "program_key": "ucf",
                        "history_start_season": "1971-1972",
                        "history_scope_intervals": "",
                        "public_page_enabled": "Yes",
                        "history_coverage_status": "COMPLETE_INSTITUTIONAL",
                        "program_inception_season": "1969-1970",
                    },
                    {
                        "program_key": "saint-leo",
                        "history_start_season": "",
                        "history_scope_intervals": "",
                        "public_page_enabled": "No",
                        "history_coverage_status": "",
                        "program_inception_season": "",
                    },
                ],
            )
            canonical_fields = [
                "canonical_game_id", "season_label", "team_a_key", "team_b_key",
                "site_type", "venue_key", "venue_id", "site_city", "site_state",
                "game_type", "notes",
            ]
            canonical = {
                "canonical_game_id": "CBBG-TEST",
                "season_label": "1973-1974",
                "team_a_key": "saint-leo",
                "team_b_key": "ucf",
                "site_type": "TEAM_B_HOME",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "game_type": "REGULAR_SEASON",
                "notes": (
                    f"{HOME_LOCATION_EXCEPTION_MARKER} "
                    "source=ucf/UCF-EXP-197374-002]"
                ),
            }
            write_csv(root / "data/canonical/games.csv", canonical_fields, [canonical])
            assertion_fields = [
                "canonical_game_id", "source_program_key", "source_game_id",
                "normalized_opponent_key", "curated_site_type",
                "curated_venue_name", "city", "state",
            ]
            write_csv(
                root / "data/evidence/game-assertions.csv",
                assertion_fields,
                [{
                    "canonical_game_id": "CBBG-TEST",
                    "source_program_key": "ucf",
                    "source_game_id": "UCF-EXP-197374-002",
                    "normalized_opponent_key": "saint-leo",
                    "curated_site_type": "SOURCE_PROGRAM_HOME",
                    "curated_venue_name": "",
                    "city": "",
                    "state": "",
                }],
            )
            write_csv(
                root / "data/reconciliation/discrepancies.csv",
                ["canonical_game_id", "source_a_program_key", "field_name", "status", "resolution_basis"],
                [],
            )

            implementation = implementation_site_report(root, "ucf")
            self.assertEqual(implementation["status"], "PASS")
            self.assertEqual(
                implementation["counts"]["researched_unresolved_home_location_rows"],
                1,
            )
            published = published_site_standard_report(root)
            self.assertEqual(published["status"], "PASS")
            self.assertEqual(
                published["counts"]["researched_unresolved_home_location_games"],
                1,
            )

    def test_unmarked_published_home_location_blank_still_fails(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            write_csv(
                root / "data/reference/programs.csv",
                ["program_key", "public_page_enabled"],
                [
                    {"program_key": "ucf", "public_page_enabled": "Yes"},
                    {"program_key": "saint-leo", "public_page_enabled": "No"},
                ],
            )
            write_csv(
                root / "data/canonical/games.csv",
                [
                    "canonical_game_id", "team_a_key", "team_b_key", "site_type",
                    "venue_key", "venue_id", "site_city", "site_state", "notes",
                ],
                [{
                    "canonical_game_id": "CBBG-BAD",
                    "team_a_key": "saint-leo",
                    "team_b_key": "ucf",
                    "site_type": "TEAM_B_HOME",
                    "venue_key": "",
                    "venue_id": "",
                    "site_city": "",
                    "site_state": "",
                    "notes": "",
                }],
            )
            report = published_site_standard_report(root)
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["hard_published_home_blocker_games"], 1)


if __name__ == "__main__":
    unittest.main()
