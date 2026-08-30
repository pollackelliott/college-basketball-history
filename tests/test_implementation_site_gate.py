import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from implementation_site_gate import implementation_site_report  # noqa: E402


SOURCE_FIELDS = [
    "source_game_id",
    "source_program_key",
    "season_label",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "site_research_status",
    "site_research_basis",
]
CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "team_a_key",
    "team_b_key",
    "site_type",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "game_type",
]
ASSERTION_FIELDS = [
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
]
DISCREPANCY_FIELDS = [
    "canonical_game_id",
    "field_name",
    "status",
    "resolution_basis",
]


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_row(**overrides):
    row = {
        "source_game_id": "TESTRAW-00001",
        "source_program_key": "test",
        "season_label": "2025-2026",
        "normalized_opponent_key": "other",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_venue_name": "Example Arena",
        "city": "Example City",
        "state": "EX",
        "curated_game_type": "REGULAR_SEASON",
        "site_research_status": "",
        "site_research_basis": "",
    }
    row.update(overrides)
    return row


def canonical_row(**overrides):
    row = {
        "canonical_game_id": "CBBG-0000001",
        "season_label": "2025-2026",
        "team_a_key": "other",
        "team_b_key": "test",
        "site_type": "TEAM_B_HOME",
        "venue_key": "example-arena",
        "venue_id": "VEN-999999",
        "site_city": "Example City",
        "site_state": "EX",
        "game_type": "REGULAR_SEASON",
    }
    row.update(overrides)
    return row


def target_assertion(**overrides):
    row = {
        "canonical_game_id": "CBBG-0000001",
        "source_program_key": "test",
        "source_game_id": "TESTRAW-00001",
        "normalized_opponent_key": "other",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_venue_name": "Example Arena",
        "city": "Example City",
        "state": "EX",
    }
    row.update(overrides)
    return row


class ImplementationSiteGateTests(unittest.TestCase):
    def make_repo(
        self,
        root: Path,
        *,
        sources=None,
        canonical=None,
        assertions=None,
        discrepancies=None,
        history_start="1900-1901",
    ):
        sources = sources if sources is not None else [source_row()]
        canonical = canonical if canonical is not None else [canonical_row()]
        assertions = assertions if assertions is not None else [target_assertion()]
        discrepancies = discrepancies if discrepancies is not None else []

        write_csv(root / "schools/test/source-games.csv", SOURCE_FIELDS, sources)
        write_csv(
            root / "data/reference/programs.csv",
            ["program_key", "history_start_season"],
            [{"program_key": "test", "history_start_season": history_start}],
        )
        write_csv(root / "data/canonical/games.csv", CANONICAL_FIELDS, canonical)
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ASSERTION_FIELDS,
            assertions,
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            DISCREPANCY_FIELDS,
            discrepancies,
        )

    def test_complete_canonical_result_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            report = implementation_site_report(root, "test")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["public_gap_rows"], 0)
            self.assertEqual(report["counts"]["target_source_information_loss"], 0)

    def test_researched_unresolved_home_gap_can_survive_canonically(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = source_row(
                curated_venue_name="",
                city="",
                state="",
                site_research_status="RESEARCHED_UNRESOLVED",
                site_research_basis="Facility chronology checked; exact historical site unsupported.",
            )
            canonical = canonical_row(
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            )
            assertion = target_assertion(curated_venue_name="", city="", state="")
            self.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=[assertion],
            )
            report = implementation_site_report(root, "test")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["public_gap_rows"], 1)
            self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 0)

    def test_target_source_venue_and_location_loss_blocks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            canonical = canonical_row(
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            )
            self.make_repo(root, canonical=[canonical])
            report = implementation_site_report(root, "test")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["target_source_venue_lost"], 1)
            self.assertEqual(report["counts"]["target_source_location_lost"], 1)

    def test_safe_reciprocal_evidence_must_not_remain_unpropagated(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = source_row(
                curated_venue_name="",
                city="",
                state="",
                site_research_status="RESEARCHED_UNRESOLVED",
                site_research_basis="Target source does not establish the exact site.",
            )
            canonical = canonical_row(
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            )
            assertions = [
                target_assertion(curated_venue_name="", city="", state=""),
                {
                    "canonical_game_id": "CBBG-0000001",
                    "source_program_key": "other",
                    "source_game_id": "OTHRAW-1",
                    "normalized_opponent_key": "test",
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_venue_name": "Example Arena",
                    "city": "Example City",
                    "state": "EX",
                },
            ]
            self.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=assertions,
            )
            report = implementation_site_report(root, "test")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["reciprocal_venue_unpropagated"], 1)
            self.assertEqual(report["counts"]["reciprocal_location_unpropagated"], 1)

    def test_reconciliation_record_can_acknowledge_reciprocal_conflict(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = source_row(
                curated_venue_name="",
                city="",
                state="",
                site_research_status="RESEARCHED_UNRESOLVED",
                site_research_basis="Target source does not establish the exact site.",
            )
            canonical = canonical_row(
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            )
            assertions = [
                target_assertion(curated_venue_name="", city="", state=""),
                {
                    "canonical_game_id": "CBBG-0000001",
                    "source_program_key": "other",
                    "source_game_id": "OTHRAW-1",
                    "normalized_opponent_key": "test",
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_venue_name": "Example Arena",
                    "city": "Example City",
                    "state": "EX",
                },
            ]
            discrepancies = [
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
            ]
            self.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=assertions,
                discrepancies=discrepancies,
            )
            report = implementation_site_report(root, "test")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["reciprocal_unpropagated"], 0)

    def test_ncaa_canonical_site_gap_is_non_waivable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = source_row(
                curated_site_type="NEUTRAL",
                curated_venue_name="",
                city="",
                state="",
                curated_game_type="NCAA_TOURNAMENT",
                site_research_status="RESEARCHED_UNRESOLVED",
                site_research_basis="Marker cannot waive NCAA completeness.",
            )
            canonical = canonical_row(
                site_type="NEUTRAL",
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
                game_type="NCAA_TOURNAMENT",
            )
            assertion = target_assertion(
                curated_site_type="NEUTRAL",
                curated_venue_name="",
                city="",
                state="",
            )
            self.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=[assertion],
            )
            report = implementation_site_report(root, "test")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["strict_ncaa_gap_rows"], 1)

    def test_history_cutoff_excludes_old_canonical_gap(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = source_row(
                season_label="1899-1900",
                curated_venue_name="",
                city="",
                state="",
            )
            canonical = canonical_row(
                season_label="1899-1900",
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            )
            assertion = target_assertion()
            self.make_repo(
                root,
                sources=[source],
                canonical=[canonical],
                assertions=[assertion],
                history_start="1900-1901",
            )
            report = implementation_site_report(root, "test")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["target_canonical_games"], 0)


if __name__ == "__main__":
    unittest.main()
