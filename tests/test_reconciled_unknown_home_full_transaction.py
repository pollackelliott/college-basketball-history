import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
import onboard_school  # noqa: E402
from implementation_site_gate import implementation_site_report  # noqa: E402
from onboarding_plan import apply_reconciliation_decisions  # noqa: E402


SOURCE_FIELDS = list(ingest_school.ASSERTION_FIELDS) + [
    "site_research_status",
    "site_research_basis",
]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows([{field: row.get(field, "") for field in fields} for row in rows])


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class ReconciledUnknownHomeFullTransactionTests(unittest.TestCase):
    def make_repo(
        self,
        root: Path,
        *,
        target_team_a: bool,
        conditional_identity: bool,
    ) -> tuple[dict, str]:
        school = "test"
        opponent = "zeta" if target_team_a else "other"
        game_id = "CBBG-1"
        source_id = "TEST-1"
        reciprocal_id = "OTHER-1"

        canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
        canonical.update(
            {
                "canonical_game_id": game_id,
                "season_label": "1908-1909",
                "game_date": "1909-02-19",
                "date_precision": "EXACT",
                "team_a_key": school if target_team_a else opponent,
                "team_b_key": opponent if target_team_a else school,
                "team_a_score": "37" if target_team_a else "18",
                "team_b_score": "18" if target_team_a else "37",
                "result_winner_team_key": school if target_team_a else opponent,
                "site_type": "TEAM_A_HOME" if target_team_a else "TEAM_B_HOME",
                "designated_home_team_key": school,
                "game_type": "REGULAR_SEASON",
                "canonical_status": "PROVISIONAL",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "notes": "",
            }
        )

        # A second reciprocal-only HOME game forces the chronology phase to
        # rewrite the canonical CSV after reconciliation, reproducing the real
        # full-transaction ordering that exposed the Utah State defect.
        chronology_game = {field: "" for field in ingest_school.CANONICAL_FIELDS}
        chronology_game.update(
            {
                "canonical_game_id": "CBBG-2",
                "season_label": "1949-1950",
                "game_date": "1950-01-10",
                "date_precision": "EXACT",
                "team_a_key": opponent,
                "team_b_key": school,
                "team_a_score": "20",
                "team_b_score": "30",
                "result_winner_team_key": school,
                "site_type": "TEAM_B_HOME",
                "designated_home_team_key": school,
                "game_type": "REGULAR_SEASON",
                "canonical_status": "PROVISIONAL",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "notes": "",
            }
        )

        source = {field: "" for field in SOURCE_FIELDS}
        source.update(
            {
                "source_program_key": school,
                "source_game_id": source_id,
                "season_label": "1908-1909",
                "game_date": "" if conditional_identity else "1909-02-19",
                "normalized_opponent_key": opponent,
                "normalized_opponent_name": "Opponent",
                "team_score": "18",
                "opponent_score": "37",
                "played_result": "L",
                "overtime_periods": "0",
                "curated_site_type": "UNKNOWN",
                "curated_venue_name": "",
                "city": "",
                "state": "",
                "curated_game_type": "REGULAR_SEASON",
                "normalization_status": "RESEARCH_ACCEPTED",
                "site_research_status": "RESEARCHED_UNRESOLVED",
                "site_research_basis": "Bounded H/A/N research remains unresolved.",
                "raw_text": "Preserved historical source text.",
            }
        )

        target_assertion = {
            field: source.get(field, "") for field in ingest_school.ASSERTION_FIELDS
        }
        target_assertion.update(
            {
                "assertion_id": "ASRT-TEST-1",
                "canonical_game_id": game_id,
                "match_status": "MATCHED",
                "match_method": "FIXTURE",
            }
        )

        reciprocal = {field: "" for field in ingest_school.ASSERTION_FIELDS}
        reciprocal.update(
            {
                "assertion_id": "ASRT-OTHER-1",
                "canonical_game_id": game_id,
                "source_program_key": opponent,
                "source_game_id": reciprocal_id,
                "season_label": "1908-1909",
                "game_date": "1909-02-19",
                "normalized_opponent_key": school,
                "normalized_opponent_name": "Test",
                "curated_site_type": "OPPONENT_HOME",
                "curated_venue_name": "",
                "city": "",
                "state": "",
                "curated_game_type": "REGULAR_SEASON",
                "match_status": "MATCHED",
                "match_method": "FIXTURE",
            }
        )
        chronology_reciprocal = dict(reciprocal)
        chronology_reciprocal.update(
            {
                "assertion_id": "ASRT-OTHER-2",
                "canonical_game_id": "CBBG-2",
                "source_game_id": "OTHER-2",
                "season_label": "1949-1950",
                "game_date": "1950-01-10",
            }
        )

        discrepancy = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
        discrepancy.update(
            {
                "discrepancy_id": "DISC-SITE-1",
                "canonical_game_id": game_id,
                "field_name": "site_type",
                "source_a_program_key": school,
                "source_a_value": "UNKNOWN",
                "canonical_value": canonical["site_type"],
                "status": "UNDER_REVIEW",
            }
        )

        write_csv(
            root / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS,
            [canonical, chronology_game],
        )
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS,
            [target_assertion, reciprocal, chronology_reciprocal],
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            [discrepancy],
        )
        write_csv(root / "schools/test/source-games.csv", SOURCE_FIELDS, [source])
        write_csv(
            root / f"schools/{opponent}/source-games.csv",
            SOURCE_FIELDS,
            [
                {
                    **{field: "" for field in SOURCE_FIELDS},
                    "source_program_key": opponent,
                    "source_game_id": reciprocal_id,
                    "season_label": "1908-1909",
                    "game_date": "1909-02-19",
                    "normalized_opponent_key": school,
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_game_type": "REGULAR_SEASON",
                },
                {
                    **{field: "" for field in SOURCE_FIELDS},
                    "source_program_key": opponent,
                    "source_game_id": "OTHER-2",
                    "season_label": "1949-1950",
                    "game_date": "1950-01-10",
                    "normalized_opponent_key": school,
                    "curated_site_type": "OPPONENT_HOME",
                    "curated_game_type": "REGULAR_SEASON",
                },
            ],
        )
        write_csv(
            root / "data/reference/programs.csv",
            ["program_key", "history_start_season", "history_scope_intervals"],
            [
                {
                    "program_key": school,
                    "history_start_season": "1900-1901",
                    "history_scope_intervals": "",
                }
            ],
        )
        write_csv(
            root / "data/reference/venues.csv",
            [
                "venue_id",
                "venue_key",
                "display_name",
                "city",
                "state",
                "opened",
                "closed",
                "date_precision",
                "identity_status",
                "source_basis",
                "notes",
            ],
            [
                {
                    "venue_id": "VEN-999999",
                    "venue_key": "example-fieldhouse",
                    "display_name": "Example Fieldhouse",
                    "city": "Example City",
                    "state": "EX",
                    "opened": "1940",
                    "closed": "1970",
                    "date_precision": "year",
                    "identity_status": "CURATED_SEED",
                    "source_basis": "Regression fixture.",
                    "notes": "",
                }
            ],
        )
        write_csv(
            root / "schools/test/venues.csv",
            [
                "source_program_key",
                "venue_key",
                "venue_id",
                "canonical_name",
                "aliases",
                "city",
                "state",
                "venue_type",
                "known_opened",
                "known_closed",
                "venue_date_precision",
                "games_currently_assigned",
                "first_assigned_game",
                "last_assigned_game",
                "relationship_type",
                "relationship_start",
                "relationship_end",
                "relationship_date_precision",
                "site_rule",
                "source_basis",
                "notes",
            ],
            [
                {
                    "source_program_key": school,
                    "venue_key": "example-fieldhouse",
                    "venue_id": "VEN-999999",
                    "canonical_name": "Example Fieldhouse",
                    "city": "Example City",
                    "state": "EX",
                    "venue_type": "arena",
                    "known_opened": "1940",
                    "known_closed": "1970",
                    "venue_date_precision": "year",
                    "games_currently_assigned": "1",
                    "first_assigned_game": "1940-01-01",
                    "last_assigned_game": "1970-12-31",
                    "relationship_type": "HOME",
                    "relationship_start": "1940-01-01",
                    "relationship_end": "1970-12-31",
                    "relationship_date_precision": "day",
                    "site_rule": "HOME only after independent H/A/N classification.",
                    "source_basis": "Regression fixture.",
                    "notes": "",
                }
            ],
        )

        decision_id = (
            "CONDITIONAL-DISCREPANCY-TEST-1-CBBG-1-SITE_TYPE"
            if conditional_identity
            else "DISCREPANCY-TEST-1-SITE_TYPE"
        )
        decisions = []
        if conditional_identity:
            decisions.append(
                {
                    "decision_id": "IDENTITY-TEST-1",
                    "category": "identity",
                    "source_game_id": source_id,
                    "decision": "MATCH_CANONICAL:CBBG-1",
                }
            )
        decisions.append(
            {
                "decision_id": decision_id,
                # approve_plan converts a selected conditional_discrepancy to
                # discrepancy before the real apply transaction.
                "category": "discrepancy",
                "conditional_identity_satisfied": conditional_identity,
                "source_game_id": source_id,
                "canonical_game_id": game_id,
                "field_name": "site_type",
                "source_value": "UNKNOWN",
                "canonical_value": canonical["site_type"],
                "decision": "KEEP_CANONICAL",
                "resolution_basis": "Reciprocal assertion establishes target HOME.",
                "canonical_patch": {
                    "site_city": "Example City",
                    "site_state": "EX",
                },
                "source_patch": {},
            }
        )
        approved = {
            "school_key": school,
            "approved_plan_hash": "a" * 64,
            "decisions": decisions,
        }
        return approved, game_id

    def assert_full_path(self, *, target_team_a: bool, conditional_identity: bool) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved, game_id = self.make_repo(
                repo,
                target_team_a=target_team_a,
                conditional_identity=conditional_identity,
            )
            marker = (
                "[RECONCILED_UNKNOWN_SITE_HOME_VENUE "
                "source=test/TEST-1 reciprocal="
            )

            first_counts = apply_reconciliation_decisions(repo, approved)
            first = {
                row["canonical_game_id"]: row
                for row in read_csv(repo / "data/canonical/games.csv")
            }[game_id]
            source = read_csv(repo / "schools/test/source-games.csv")[0]
            assertion = next(
                row
                for row in read_csv(repo / "data/evidence/game-assertions.csv")
                if row["source_program_key"] == "test"
            )

            self.assertEqual(
                first_counts["reconciled_unknown_site_home_venue_markers_added"],
                1,
            )
            self.assertEqual(source["curated_site_type"], "UNKNOWN")
            self.assertEqual(assertion["curated_site_type"], "UNKNOWN")
            self.assertEqual(
                first["site_type"],
                "TEAM_A_HOME" if target_team_a else "TEAM_B_HOME",
            )
            self.assertEqual(first["site_city"], "Example City")
            self.assertEqual(first["site_state"], "EX")
            self.assertEqual(first["venue_key"], "")
            self.assertEqual(first["venue_id"], "")
            self.assertIn(marker, first["notes"])
            self.assertEqual(first["notes"].count(marker), 1)

            # Idempotence: replaying the exact approved reconciliation must not
            # duplicate the provenance marker.
            second_counts = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(
                second_counts["reconciled_unknown_site_home_venue_markers_existing"],
                1,
            )
            second = {
                row["canonical_game_id"]: row
                for row in read_csv(repo / "data/canonical/games.csv")
            }[game_id]
            self.assertEqual(second["notes"].count(marker), 1)

            chronology = onboard_school.backfill_reciprocal_only_home_chronology(
                repo,
                "test",
            )
            self.assertEqual(chronology["applied_games"], 1)
            post_chronology = {
                row["canonical_game_id"]: row
                for row in read_csv(repo / "data/canonical/games.csv")
            }[game_id]
            self.assertEqual(post_chronology["notes"].count(marker), 1)
            self.assertEqual(post_chronology["venue_key"], "")
            self.assertEqual(post_chronology["venue_id"], "")
            self.assertEqual(post_chronology["site_city"], "Example City")
            self.assertEqual(post_chronology["site_state"], "EX")

            report = implementation_site_report(repo, "test")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 0)
            self.assertEqual(
                report["counts"]["reconciled_unknown_site_unresolved_home_venue"],
                1,
            )

    def test_ordinary_researched_unknown_home_provenance_survives_full_path(self):
        self.assert_full_path(target_team_a=False, conditional_identity=False)

    def test_selected_conditional_researched_unknown_home_provenance_survives_full_path(self):
        self.assert_full_path(target_team_a=True, conditional_identity=True)


if __name__ == "__main__":
    unittest.main()
