import copy
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS,
    WorkflowError,
    apply_publication_decisions,
    approve_plan,
)
from program_history import accomplishment_row_issues  # noqa: E402
from verify_program_accomplishments import compare_program  # noqa: E402


SCHOOL = "admin-difference-fixture"
ACCOMPLISHMENT_ID = "ACCOMPLISHMENTS-ADMIN-DIFFERENCE-FIXTURE"


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def read_one(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return next(csv.DictReader(handle))


class Stage2AccomplishmentAdministrativeDifferenceTests(unittest.TestCase):
    def program(self):
        return {
            "program_key": SCHOOL,
            "public_page_enabled": "No",
            "history_start_season": "1909-1910",
            "history_scope_status": "OWNER_CONFIRMED",
            "history_scope_basis": "ALWAYS_TOP_LEVEL_FROM_INCEPTION",
            "history_scope_intervals": "",
        }

    def reference(self, **updates):
        row = {
            "program_key": SCHOOL,
            "conference_regular_season_championships": "20",
            "conference_tournament_championships": "6",
            "ncaa_tournament_appearances": "1",
            "final_four_appearances": "1",
            "national_championships": "0",
            "best_finish_key": "ELITE_EIGHT",
            "best_finish_year": "2004",
            "verification_status": "OWNER_BASELINE_UNVERIFIED",
            "verification_basis": "Owner baseline pending authoritative verification.",
            "canonical_crosscheck_status": "NOT_CHECKED",
            "notes": "",
        }
        row.update(updates)
        return row

    def canonical_games(self):
        return [
            {
                "canonical_game_id": "CBBG-ADMIN-1961",
                "season_label": "1960-1961",
                "game_date": "1961-03-24",
                "date_precision": "EXACT",
                "team_a_key": SCHOOL,
                "team_b_key": "opponent",
                "team_a_score": "60",
                "team_b_score": "70",
                "result_winner_team_key": "opponent",
                "site_type": "NEUTRAL",
                "designated_home_team_key": "",
                "game_type": "NCAA_TOURNAMENT",
                "postseason_round": "Final Four",
                "notes": "",
            }
        ]

    def make_repo(self, root: Path, accomplishment=None):
        write_csv(
            root / "data/reference/programs.csv",
            (
                "program_key",
                "public_page_enabled",
                "history_start_season",
                "history_scope_status",
                "history_scope_basis",
                "history_scope_intervals",
            ),
            [self.program()],
        )
        write_csv(
            root / "data/reference/program-accomplishments.csv",
            (
                "program_key",
                "conference_regular_season_championships",
                "conference_tournament_championships",
                "ncaa_tournament_appearances",
                "final_four_appearances",
                "national_championships",
                "best_finish_key",
                "best_finish_year",
                "verification_status",
                "verification_basis",
                "canonical_crosscheck_status",
                "notes",
            ),
            [accomplishment or self.reference()],
        )

    def accomplishment_item(self, *, conflicts=True):
        return {
            "decision_id": ACCOMPLISHMENT_ID,
            "category": "accomplishments",
            "source_game_id": "",
            "season_label": "",
            "source_game_date": "[unknown]",
            "canonical_game_date": "[unknown]",
            "matchup": SCHOOL,
            "field_name": "program_accomplishments",
            "source_value": json.dumps(
                {
                    "conference_regular_season_championships": "20",
                    "conference_tournament_championships": "6",
                    "ncaa_tournament_appearances": "1",
                    "final_four_appearances": "1",
                    "national_championships": "0",
                    "best_finish_key": "ELITE_EIGHT",
                    "best_finish_year": "2004",
                },
                sort_keys=True,
            ),
            "canonical_value": json.dumps(
                {
                    "ncaa_tournament_appearances": 1,
                    "final_four_appearances": 1,
                    "national_championships": 0,
                    "best_finish_key": "FINAL_FOUR",
                    "best_finish_year": 1961,
                },
                sort_keys=True,
            ),
            "relevant_evidence": "Fixture administrative difference.",
            "recommended_action": "KEEP_UNDER_REVIEW",
            "allowed_actions": [
                "APPLY_ACCOMPLISHMENT_PATCH",
                "APPLY_ACCOMPLISHMENT_PATCH_WITH_ADMIN_DIFFERENCE",
                "KEEP_UNDER_REVIEW",
                "VERIFY_EXPLAINED_ADMIN_DIFFERENCE",
                "VERIFY_REFERENCE_VALUES",
            ],
            "accomplishment_conflicts": (
                [
                    "best_finish_key: reference='ELITE_EIGHT', canonical='FINAL_FOUR'",
                    "best_finish_year: reference='2004', canonical='1961'",
                ]
                if conflicts
                else []
            ),
            "decision": "PENDING",
            "resolution_basis": "",
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
            "notes": "",
        }

    def review_row(self, item, decision, basis, canonical_patch="{}"):
        row = {field: "" for field in REVIEW_COLUMNS}
        for field in REVIEW_COLUMNS:
            value = item.get(field, "")
            if field == "allowed_actions" and isinstance(value, list):
                value = " | ".join(value)
            row[field] = value
        row["decision"] = decision
        row["resolution_basis"] = basis
        row["canonical_patch_json"] = canonical_patch
        return row

    def test_ordinary_exact_match_still_passes(self):
        reference = self.reference(
            best_finish_key="FINAL_FOUR",
            best_finish_year="1961",
            verification_status="VERIFIED",
            verification_basis="Authoritative exact-match fixture.",
            canonical_crosscheck_status="MATCH",
        )
        self.assertTrue(compare_program(self.program(), reference, self.canonical_games()))

    def test_ordinary_unexplained_conflict_still_fails(self):
        self.assertFalse(
            compare_program(self.program(), self.reference(), self.canonical_games())
        )

    def test_owner_approved_explained_admin_difference_passes_without_game_mutation(self):
        games = self.canonical_games()
        before = copy.deepcopy(games)
        reference = self.reference(
            verification_status="VERIFIED",
            verification_basis=(
                "Authoritative institutional evidence documents an administrative "
                "vacatur while preserving the played NCAA games."
            ),
            canonical_crosscheck_status="EXPLAINED_ADMIN_DIFFERENCE",
        )
        self.assertTrue(compare_program(self.program(), reference, games))
        self.assertEqual(games, before)

    def test_stale_explained_admin_difference_does_not_pass(self):
        reference = self.reference(
            best_finish_key="FINAL_FOUR",
            best_finish_year="1961",
            verification_status="VERIFIED",
            verification_basis="Administrative-difference fixture.",
            canonical_crosscheck_status="EXPLAINED_ADMIN_DIFFERENCE",
        )
        self.assertFalse(compare_program(self.program(), reference, self.canonical_games()))

    def test_explained_admin_difference_requires_verified_authority_and_basis(self):
        row = self.reference(
            verification_status="OWNER_BASELINE_UNVERIFIED",
            verification_basis="",
            canonical_crosscheck_status="EXPLAINED_ADMIN_DIFFERENCE",
        )
        errors, _warnings = accomplishment_row_issues(row, self.program(), False)
        self.assertTrue(
            any("requires VERIFIED accomplishment authority" in item for item in errors)
        )
        self.assertTrue(
            any("requires a nonblank verification_basis" in item for item in errors)
        )

    def test_no_gate1_authority_is_inferred_without_live_conflict(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            self.make_repo(repo)
            item = self.accomplishment_item(conflicts=False)
            item["notes"] = (
                "Institutional source note says the historical participation was vacated."
            )
            plan = {
                "schema_version": 1,
                "workflow_version": 1,
                "school_key": SCHOOL,
                "input_fingerprint": {"sha256": "fixture-fingerprint"},
                "blockers": [],
                "warnings": [],
                "summary": {},
                "decisions": [item],
            }
            plan_path = root / "plan.json"
            review_path = root / "review.csv"
            plan_path.write_text(json.dumps(plan), encoding="utf-8")
            write_csv(
                review_path,
                REVIEW_COLUMNS,
                [
                    self.review_row(
                        item,
                        "VERIFY_EXPLAINED_ADMIN_DIFFERENCE",
                        "A source note alone cannot create Gate 1 authority.",
                    )
                ],
            )
            with patch(
                "onboarding_plan.input_fingerprint",
                return_value={"sha256": "fixture-fingerprint"},
            ):
                with self.assertRaisesRegex(
                    WorkflowError,
                    "requires a live accomplishment/canonical conflict",
                ):
                    approve_plan(repo, plan_path, review_path, "owner")

    def test_explained_admin_difference_apply_preserves_reference_values(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            approved = {
                "school_key": SCHOOL,
                "approved_plan_hash": "b" * 64,
                "decisions": [
                    {
                        "decision_id": ACCOMPLISHMENT_ID,
                        "category": "accomplishments",
                        "decision": "VERIFY_EXPLAINED_ADMIN_DIFFERENCE",
                        "resolution_basis": (
                            "Owner-approved institutional evidence documents the "
                            "administrative difference."
                        ),
                        "canonical_patch": {},
                    }
                ],
            }
            before = read_one(repo / "data/reference/program-accomplishments.csv")
            counts = apply_publication_decisions(repo, approved)
            row = read_one(repo / "data/reference/program-accomplishments.csv")
            self.assertEqual(row["best_finish_key"], before["best_finish_key"])
            self.assertEqual(row["best_finish_year"], before["best_finish_year"])
            self.assertEqual(row["verification_status"], "VERIFIED")
            self.assertEqual(
                row["canonical_crosscheck_status"], "EXPLAINED_ADMIN_DIFFERENCE"
            )
            self.assertEqual(counts["accomplishments_verified"], 1)
            self.assertEqual(counts["accomplishment_admin_differences_explained"], 1)
            self.assertTrue(compare_program(self.program(), row, self.canonical_games()))

    def test_value_patch_plus_explained_admin_difference_is_supported(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            approved = {
                "school_key": SCHOOL,
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": ACCOMPLISHMENT_ID,
                        "category": "accomplishments",
                        "decision": "APPLY_ACCOMPLISHMENT_PATCH_WITH_ADMIN_DIFFERENCE",
                        "resolution_basis": (
                            "Owner-approved authoritative correction plus documented "
                            "administrative difference."
                        ),
                        "canonical_patch": {
                            "conference_regular_season_championships": "19"
                        },
                    }
                ],
            }
            counts = apply_publication_decisions(repo, approved)
            row = read_one(repo / "data/reference/program-accomplishments.csv")
            self.assertEqual(row["conference_regular_season_championships"], "19")
            self.assertEqual(row["verification_status"], "VERIFIED")
            self.assertEqual(
                row["canonical_crosscheck_status"], "EXPLAINED_ADMIN_DIFFERENCE"
            )
            self.assertEqual(counts["accomplishments_patched"], 1)
            self.assertEqual(counts["accomplishment_fields_patched"], 1)
            self.assertEqual(counts["accomplishment_admin_differences_explained"], 1)
            self.assertTrue(compare_program(self.program(), row, self.canonical_games()))


if __name__ == "__main__":
    unittest.main()
