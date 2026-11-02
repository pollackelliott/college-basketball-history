import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
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
        writer.writerows(
            [{field: row.get(field, "") for field in fields} for row in rows]
        )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def canonical_game() -> dict[str, str]:
    row = {field: "" for field in ingest_school.CANONICAL_FIELDS}
    row.update(
        {
            "canonical_game_id": "CBBG-1",
            "season_label": "1919-1920",
            "game_date": "1920-03-05",
            "date_precision": "EXACT",
            "team_a_key": "test",
            "team_b_key": "other",
            "team_a_score": "21",
            "team_b_score": "14",
            "result_winner_team_key": "test",
            "site_type": "TEAM_A_HOME",
            "designated_home_team_key": "test",
            "game_type": "REGULAR_SEASON",
            "canonical_status": "PROVISIONAL",
        }
    )
    return row


def reciprocal_assertion(
    *,
    source_game_id: str = "OTHER-1",
    venue: str = "",
    city: str = "",
    state: str = "",
) -> dict[str, str]:
    row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
    row.update(
        {
            "assertion_id": f"ASRT-{source_game_id}",
            "canonical_game_id": "CBBG-1",
            "source_program_key": "other",
            "source_game_id": source_game_id,
            "season_label": "1919-1920",
            "game_date": "1920-03-05",
            "normalized_opponent_key": "test",
            "normalized_opponent_name": "Test",
            "team_score": "14",
            "opponent_score": "21",
            "played_result": "L",
            "curated_site_type": "OPPONENT_HOME",
            "curated_venue_name": venue,
            "city": city,
            "state": state,
            "curated_game_type": "REGULAR_SEASON",
            "match_status": "MATCHED",
            "match_method": "FIXTURE",
            "raw_text": "Mar. 5 A L 14-21 Test",
        }
    )
    return row


class ReciprocalOnlyHomeSitePatchTransactionTests(unittest.TestCase):
    def make_repo(
        self,
        root: Path,
        *,
        reciprocal_rows: list[dict[str, str]] | None = None,
        target_assertion: bool = False,
    ) -> dict:
        canonical = canonical_game()
        assertions = list(reciprocal_rows or [reciprocal_assertion()])
        if target_assertion:
            target = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            target.update(
                {
                    "assertion_id": "ASRT-TEST-1",
                    "canonical_game_id": "CBBG-1",
                    "source_program_key": "test",
                    "source_game_id": "TEST-1",
                    "season_label": "1919-1920",
                    "game_date": "1920-03-05",
                    "normalized_opponent_key": "other",
                    "curated_site_type": "SOURCE_PROGRAM_HOME",
                    "curated_game_type": "REGULAR_SEASON",
                    "match_status": "MATCHED",
                    "match_method": "FIXTURE",
                }
            )
            assertions.append(target)

        write_csv(
            root / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS,
            [canonical],
        )
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS,
            assertions,
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            [],
        )
        write_csv(
            root / "schools/test/source-games.csv",
            SOURCE_FIELDS,
            [],
        )
        write_csv(
            root / "data/reference/programs.csv",
            ["program_key", "history_start_season", "history_scope_intervals"],
            [
                {
                    "program_key": "test",
                    "history_start_season": "1900-1901",
                    "history_scope_intervals": "",
                }
            ],
        )

        return {
            "school_key": "test",
            "approved_plan_hash": "a" * 64,
            "decisions": [
                {
                    "decision_id": "CANONICAL-SITE-PATCH-CBBG-1",
                    "category": "canonical_site_patch",
                    "source_game_id": "",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "site_metadata",
                    "decision": "APPLY_CANONICAL_PATCH",
                    "resolution_basis": (
                        "Owner-reviewed institutional research establishes the HOME "
                        "locality while the physical venue remains unrecoverable."
                    ),
                    "canonical_patch": {
                        "site_city": "Example City",
                        "site_state": "EX",
                    },
                    "source_patch": {},
                }
            ],
        }

    def test_locality_only_patch_emits_valid_reciprocal_home_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.make_repo(repo)
            assertions_before = read_csv(
                repo / "data/evidence/game-assertions.csv"
            )

            first_counts = apply_reconciliation_decisions(repo, approved)
            first = read_csv(repo / "data/canonical/games.csv")[0]
            assertions_after = read_csv(
                repo / "data/evidence/game-assertions.csv"
            )

            marker = (
                "[RECIPROCAL_ONLY_UNRESOLVED_HOME_VENUE "
                "target=test reciprocal=other/OTHER-1]"
            )
            self.assertEqual(first_counts["canonical_site_patches"], 1)
            self.assertEqual(
                first_counts[
                    "reciprocal_only_site_patch_home_venue_markers_added"
                ],
                1,
            )
            self.assertEqual(first["site_type"], "TEAM_A_HOME")
            self.assertEqual(first["designated_home_team_key"], "test")
            self.assertEqual(first["site_city"], "Example City")
            self.assertEqual(first["site_state"], "EX")
            self.assertEqual(first["venue_key"], "")
            self.assertEqual(first["venue_id"], "")
            self.assertIn(marker, first["notes"])
            self.assertEqual(first["notes"].count(marker), 1)
            self.assertIn(
                "[OWNER_APPROVED_CANONICAL_SITE_PATCH",
                first["notes"],
            )
            self.assertEqual(assertions_after, assertions_before)
            self.assertFalse(
                any(
                    row["source_program_key"] == "test"
                    for row in assertions_after
                )
            )

            second_counts = apply_reconciliation_decisions(repo, approved)
            second = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(
                second_counts[
                    "reciprocal_only_site_patch_home_venue_markers_existing"
                ],
                1,
            )
            self.assertEqual(second["notes"].count(marker), 1)

            report = implementation_site_report(repo, "test")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 0)
            self.assertEqual(
                report["counts"]["reciprocal_only_unresolved_home_venue"],
                1,
            )

    def test_known_reciprocal_venue_refuses_exception_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.make_repo(
                repo,
                reciprocal_rows=[
                    reciprocal_assertion(venue="Known Arena")
                ],
            )
            assertions_before = read_csv(
                repo / "data/evidence/game-assertions.csv"
            )

            counts = apply_reconciliation_decisions(repo, approved)
            game = read_csv(repo / "data/canonical/games.csv")[0]

            self.assertEqual(counts["canonical_site_patches"], 1)
            self.assertNotIn(
                "reciprocal_only_site_patch_home_venue_markers_added",
                counts,
            )
            self.assertNotIn(
                "[RECIPROCAL_ONLY_UNRESOLVED_HOME_VENUE",
                game["notes"],
            )
            self.assertEqual(game["venue_key"], "")
            self.assertEqual(game["venue_id"], "")
            self.assertEqual(
                read_csv(repo / "data/evidence/game-assertions.csv"),
                assertions_before,
            )
            report = implementation_site_report(repo, "test")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 1)
            self.assertEqual(report["counts"]["reciprocal_venue_unpropagated"], 1)

    def test_conflicting_reciprocal_locality_refuses_exception_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.make_repo(
                repo,
                reciprocal_rows=[
                    reciprocal_assertion(
                        city="Different City",
                        state="ZZ",
                    )
                ],
            )

            counts = apply_reconciliation_decisions(repo, approved)
            game = read_csv(repo / "data/canonical/games.csv")[0]

            self.assertEqual(counts["canonical_site_patches"], 1)
            self.assertNotIn(
                "reciprocal_only_site_patch_home_venue_markers_added",
                counts,
            )
            self.assertNotIn(
                "[RECIPROCAL_ONLY_UNRESOLVED_HOME_VENUE",
                game["notes"],
            )
            report = implementation_site_report(repo, "test")
            self.assertEqual(report["status"], "FAIL")
            self.assertEqual(report["counts"]["strict_home_gap_rows"], 1)

    def test_target_assertion_refuses_reciprocal_only_marker(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            approved = self.make_repo(repo, target_assertion=True)

            counts = apply_reconciliation_decisions(repo, approved)
            game = read_csv(repo / "data/canonical/games.csv")[0]

            self.assertEqual(counts["canonical_site_patches"], 1)
            self.assertNotIn(
                "reciprocal_only_site_patch_home_venue_markers_added",
                counts,
            )
            self.assertNotIn(
                "[RECIPROCAL_ONLY_UNRESOLVED_HOME_VENUE",
                game["notes"],
            )


if __name__ == "__main__":
    unittest.main()
