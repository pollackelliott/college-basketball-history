import copy
import csv
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import onboarding_plan  # noqa: E402
from onboarding_hardening import carry_forward_review, fill_review_from_map  # noqa: E402
from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS,
    WorkflowError,
    apply_publication_decisions,
    approve_plan,
)
from verify_program_accomplishments import compare_program  # noqa: E402


SCHOOL = "long-island-university"
ACCOMPLISHMENT_ID = "ACCOMPLISHMENTS-LONG-ISLAND-UNIVERSITY"
PUBLICATION_ID = "PUBLICATION-LONG-ISLAND-UNIVERSITY"


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class Stage2AccomplishmentPatchTests(unittest.TestCase):
    def accomplishment_row(self):
        return {
            "program_key": SCHOOL,
            "conference_regular_season_championships": "13",
            "conference_tournament_championships": "8",
            "ncaa_tournament_appearances": "8",
            "final_four_appearances": "0",
            "national_championships": "0",
            "best_finish_key": "ROUND_OF_64",
            "best_finish_year": "2026",
            "verification_status": "OWNER_BASELINE_UNVERIFIED",
            "verification_basis": "Owner baseline pending authoritative verification.",
            "canonical_crosscheck_status": "NOT_CHECKED",
            "notes": "",
        }

    def program_row(self):
        return {
            "program_key": SCHOOL,
            "public_page_enabled": "No",
            "history_start_season": "1928-1929",
            "history_scope_intervals": "",
        }

    def make_repo(self, root: Path):
        write_csv(
            root / "data/reference/programs.csv",
            (
                "program_key",
                "public_page_enabled",
                "history_start_season",
                "history_scope_intervals",
            ),
            [self.program_row()],
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
            [self.accomplishment_row()],
        )

    def accomplishment_item(self):
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
                    "conference_regular_season_championships": "13",
                    "conference_tournament_championships": "8",
                    "ncaa_tournament_appearances": "8",
                    "final_four_appearances": "0",
                    "national_championships": "0",
                    "best_finish_key": "ROUND_OF_64",
                    "best_finish_year": "2026",
                },
                sort_keys=True,
            ),
            "canonical_value": json.dumps(
                {
                    "ncaa_tournament_appearances": 8,
                    "final_four_appearances": 0,
                    "national_championships": 0,
                    "best_finish_key": "ROUND_OF_64",
                    "best_finish_year": 2026,
                },
                sort_keys=True,
            ),
            "relevant_evidence": (
                "Canonical NCAA fields match; conference titles require authoritative "
                "source verification."
            ),
            "recommended_action": "VERIFY_REFERENCE_VALUES",
            "allowed_actions": [
                "APPLY_ACCOMPLISHMENT_PATCH",
                "KEEP_UNDER_REVIEW",
                "VERIFY_REFERENCE_VALUES",
            ],
            "decision": "PENDING",
            "resolution_basis": "",
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
            "notes": "Approval basis must cite the authoritative accomplishment source.",
        }

    def publication_item(self):
        return {
            "decision_id": PUBLICATION_ID,
            "category": "publication",
            "source_game_id": "",
            "season_label": "",
            "source_game_date": "[unknown]",
            "canonical_game_date": "[unknown]",
            "matchup": SCHOOL,
            "field_name": "public_page_enabled",
            "source_value": "No",
            "canonical_value": "Yes",
            "relevant_evidence": "Fixture publication decision.",
            "recommended_action": "ENABLE_PUBLIC_PAGE",
            "allowed_actions": ["ENABLE_PUBLIC_PAGE", "KEEP_DISABLED"],
            "decision": "PENDING",
            "resolution_basis": "",
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
            "notes": "Publication only after permanent gates pass.",
        }

    def plan(self):
        return {
            "schema_version": 1,
            "workflow_version": 1,
            "school_key": SCHOOL,
            "input_fingerprint": {"sha256": "fixture-fingerprint"},
            "blockers": [],
            "warnings": [],
            "summary": {},
            "decisions": [self.accomplishment_item(), self.publication_item()],
        }

    def review_row(self, item):
        row = {field: "" for field in REVIEW_COLUMNS}
        for field in REVIEW_COLUMNS:
            value = item.get(field, "")
            if field == "allowed_actions" and isinstance(value, list):
                value = " | ".join(value)
            row[field] = value
        return row

    def write_plan_review(self, root: Path):
        plan_path = root / "plan.json"
        review_path = root / "review.csv"
        plan_path.write_text(json.dumps(self.plan()), encoding="utf-8")
        write_csv(
            review_path,
            REVIEW_COLUMNS,
            [
                self.review_row(self.accomplishment_item()),
                self.review_row(self.publication_item()),
            ],
        )
        return plan_path, review_path

    def write_map(self, path: Path, *, patch_value="7", patch_field=None):
        field = patch_field or "conference_regular_season_championships"
        payload = {
            "decisions": {
                ACCOMPLISHMENT_ID: "APPLY_ACCOMPLISHMENT_PATCH",
                PUBLICATION_ID: "ENABLE_PUBLIC_PAGE",
            },
            "basis_by_decision": {
                ACCOMPLISHMENT_ID: (
                    "Authoritative institutional evidence corrects the stale baseline "
                    "while preserving Owner Gate 1 authority."
                ),
                PUBLICATION_ID: "Publication is approved only after the corrected values pass gates.",
            },
            "canonical_patch_by_decision": {
                ACCOMPLISHMENT_ID: {field: patch_value},
            },
        }
        path.write_text(json.dumps(payload), encoding="utf-8")

    def seal_from_map(self, repo: Path, root: Path, *, patch_value="7"):
        plan_path, review_path = self.write_plan_review(root)
        map_path = root / "map.json"
        self.write_map(map_path, patch_value=patch_value)
        fill_review_from_map(review_path, map_path)
        with patch(
            "onboarding_plan.input_fingerprint",
            return_value={"sha256": "fixture-fingerprint"},
        ):
            approved, approved_hash = approve_plan(
                repo,
                plan_path,
                review_path,
                "owner",
            )
        return approved, approved_hash, review_path

    def canonical_games(self):
        seasons = [
            ("1980-1981", "1981-03-01"),
            ("1983-1984", "1984-03-01"),
            ("1996-1997", "1997-03-01"),
            ("1997-1998", "1998-03-01"),
            ("2010-2011", "2011-03-01"),
            ("2011-2012", "2012-03-01"),
            ("2017-2018", "2018-03-01"),
            ("2025-2026", "2026-03-01"),
        ]
        return [
            {
                "canonical_game_id": f"CBBG-TEST-{index}",
                "season_label": season,
                "game_date": date,
                "team_a_key": SCHOOL,
                "team_b_key": "opponent",
                "game_type": "NCAA_TOURNAMENT",
                "postseason_round": "R64",
                "result_winner_team_key": "opponent",
            }
            for index, (season, date) in enumerate(seasons, start=1)
        ]

    def test_liu_exact_topology_patch_is_sealed_hash_bound_and_publishable(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            fixture = root / "fixture"
            self.make_repo(repo)
            fixture.mkdir()

            approved, approved_hash, _ = self.seal_from_map(repo, fixture)
            accomplishment = next(
                item
                for item in approved["decisions"]
                if item["decision_id"] == ACCOMPLISHMENT_ID
            )
            publication = next(
                item
                for item in approved["decisions"]
                if item["decision_id"] == PUBLICATION_ID
            )
            self.assertEqual(accomplishment["decision"], "APPLY_ACCOMPLISHMENT_PATCH")
            self.assertEqual(
                accomplishment["canonical_patch"],
                {"conference_regular_season_championships": "7"},
            )
            self.assertEqual(publication["decision"], "ENABLE_PUBLIC_PAGE")

            changed = copy.deepcopy(approved)
            changed_accomplishment = next(
                item
                for item in changed["decisions"]
                if item["decision_id"] == ACCOMPLISHMENT_ID
            )
            changed_accomplishment["canonical_patch"][
                "conference_regular_season_championships"
            ] = "8"
            self.assertNotEqual(
                approved_hash,
                onboarding_plan.sha256_text(onboarding_plan.canonical_json(changed)),
            )

    def test_invalid_accomplishment_patch_field_is_refused_by_compact_map(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            _, review_path = self.write_plan_review(root)
            map_path = root / "map.json"
            self.write_map(
                map_path,
                patch_field="verification_status",
                patch_value="VERIFIED",
            )
            with self.assertRaisesRegex(
                WorkflowError,
                "forbidden accomplishment patch fields",
            ):
                fill_review_from_map(review_path, map_path)

    def test_missing_accomplishment_patch_payload_is_refused(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            fixture = root / "fixture"
            self.make_repo(repo)
            fixture.mkdir()
            plan_path, review_path = self.write_plan_review(fixture)
            map_path = fixture / "map.json"
            map_path.write_text(
                json.dumps(
                    {
                        "decisions": {
                            ACCOMPLISHMENT_ID: "APPLY_ACCOMPLISHMENT_PATCH",
                            PUBLICATION_ID: "KEEP_DISABLED",
                        },
                        "basis_by_decision": {
                            ACCOMPLISHMENT_ID: "Authoritative correction fixture.",
                            PUBLICATION_ID: "Keep disabled in negative fixture.",
                        },
                    }
                ),
                encoding="utf-8",
            )
            fill_review_from_map(review_path, map_path)
            with patch(
                "onboarding_plan.input_fingerprint",
                return_value={"sha256": "fixture-fingerprint"},
            ):
                with self.assertRaisesRegex(
                    WorkflowError,
                    "requires a nonempty accomplishment patch",
                ):
                    approve_plan(repo, plan_path, review_path, "owner")

    def test_disposable_apply_uses_corrected_values_without_real_repo_mutation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real_repo = root / "real"
            rehearsal = root / "rehearsal"
            fixture = root / "fixture"
            self.make_repo(real_repo)
            shutil.copytree(real_repo, rehearsal)
            fixture.mkdir()

            approved, approved_hash, _ = self.seal_from_map(real_repo, fixture)
            approved["approved_plan_hash"] = approved_hash
            counts = apply_publication_decisions(rehearsal, approved)

            real_accomplishment = read_rows(
                real_repo / "data/reference/program-accomplishments.csv"
            )[0]
            rehearsed_accomplishment = read_rows(
                rehearsal / "data/reference/program-accomplishments.csv"
            )[0]
            real_program = read_rows(real_repo / "data/reference/programs.csv")[0]
            rehearsed_program = read_rows(rehearsal / "data/reference/programs.csv")[0]

            self.assertEqual(
                real_accomplishment["conference_regular_season_championships"],
                "13",
            )
            self.assertEqual(real_accomplishment["verification_status"], "OWNER_BASELINE_UNVERIFIED")
            self.assertEqual(real_program["public_page_enabled"], "No")

            self.assertEqual(
                rehearsed_accomplishment["conference_regular_season_championships"],
                "7",
            )
            self.assertEqual(rehearsed_accomplishment["verification_status"], "VERIFIED")
            self.assertEqual(rehearsed_accomplishment["canonical_crosscheck_status"], "MATCH")
            self.assertEqual(rehearsed_program["public_page_enabled"], "Yes")
            self.assertEqual(counts["accomplishments_patched"], 1)
            self.assertEqual(counts["accomplishment_fields_patched"], 1)
            self.assertEqual(counts["pages_enabled"], 1)
            self.assertTrue(
                compare_program(
                    rehearsed_program,
                    rehearsed_accomplishment,
                    self.canonical_games(),
                )
            )

    def test_publication_remains_blocked_when_accomplishment_is_under_review(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            fixture = root / "fixture"
            self.make_repo(repo)
            fixture.mkdir()
            plan_path, review_path = self.write_plan_review(fixture)
            rows = read_rows(review_path)
            for row in rows:
                if row["decision_id"] == ACCOMPLISHMENT_ID:
                    row["decision"] = "KEEP_UNDER_REVIEW"
                    row["resolution_basis"] = "Historical value remains under review."
                else:
                    row["decision"] = "ENABLE_PUBLIC_PAGE"
                    row["resolution_basis"] = "Publication fixture."
            write_csv(review_path, REVIEW_COLUMNS, rows)

            with patch(
                "onboarding_plan.input_fingerprint",
                return_value={"sha256": "fixture-fingerprint"},
            ):
                with self.assertRaisesRegex(
                    WorkflowError,
                    "Publication cannot be enabled while accomplishments remain under review",
                ):
                    approve_plan(repo, plan_path, review_path, "owner")

    def test_verify_reference_values_path_remains_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            self.make_repo(repo)
            approved = {
                "school_key": SCHOOL,
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": ACCOMPLISHMENT_ID,
                        "category": "accomplishments",
                        "decision": "VERIFY_REFERENCE_VALUES",
                        "resolution_basis": "Existing values are authoritatively verified.",
                        "canonical_patch": {},
                    },
                    {
                        "decision_id": PUBLICATION_ID,
                        "category": "publication",
                        "decision": "ENABLE_PUBLIC_PAGE",
                        "resolution_basis": "Publication approved.",
                        "canonical_patch": {},
                    },
                ],
            }
            apply_publication_decisions(repo, approved)
            accomplishment = read_rows(
                repo / "data/reference/program-accomplishments.csv"
            )[0]
            program = read_rows(repo / "data/reference/programs.csv")[0]
            self.assertEqual(
                accomplishment["conference_regular_season_championships"],
                "13",
            )
            self.assertEqual(accomplishment["verification_status"], "VERIFIED")
            self.assertEqual(accomplishment["canonical_crosscheck_status"], "MATCH")
            self.assertEqual(program["public_page_enabled"], "Yes")

    def test_carry_forward_preserves_approved_accomplishment_patch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            fixture = root / "fixture"
            self.make_repo(repo)
            fixture.mkdir()
            _, _, old_review = self.seal_from_map(repo, fixture)
            new_review = root / "new-review.csv"
            fresh = []
            for row in read_rows(old_review):
                copy_row = dict(row)
                copy_row["decision"] = "PENDING"
                copy_row["resolution_basis"] = ""
                copy_row["canonical_patch_json"] = "{}"
                fresh.append(copy_row)
            write_csv(new_review, REVIEW_COLUMNS, fresh)

            counts = carry_forward_review(old_review, new_review)
            rows = {row["decision_id"]: row for row in read_rows(new_review)}
            self.assertEqual(counts["APPLY_ACCOMPLISHMENT_PATCH"], 1)
            self.assertEqual(
                json.loads(rows[ACCOMPLISHMENT_ID]["canonical_patch_json"]),
                {"conference_regular_season_championships": "7"},
            )
            self.assertEqual(
                rows[ACCOMPLISHMENT_ID]["decision"],
                "APPLY_ACCOMPLISHMENT_PATCH",
            )


if __name__ == "__main__":
    unittest.main()
