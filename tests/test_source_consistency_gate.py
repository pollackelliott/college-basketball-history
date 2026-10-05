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

import ingest_school  # noqa: E402
import onboarding_plan  # noqa: E402
from onboarding_hardening import fill_review_from_map  # noqa: E402
from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS,
    WorkflowError,
    apply_reconciliation_decisions,
    approve_plan,
    score_result_consistency_issue,
)


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def blank_row(fields, **updates):
    row = {field: "" for field in fields}
    row.update(updates)
    return row


def source_consistency_item(
    *,
    source_game_id="ALPHA-1",
    planned_identity_status=ingest_school.NEW_GAME,
):
    return {
        "decision_id": f"SOURCE-CONSISTENCY-{source_game_id}",
        "category": "source_consistency",
        "source_game_id": source_game_id,
        "canonical_game_id": "",
        "season_label": "2020-2021",
        "source_game_date": "2020-12-30",
        "canonical_game_date": "[unknown]",
        "matchup": "alpha vs beta",
        "field_name": "score_result_consistency",
        "source_value": "score=81-61; played_result=L",
        "canonical_value": "[new canonical game]",
        "relevant_evidence": "Frozen structured score implies W while played_result is L.",
        "recommended_action": "REVIEW_REQUIRED",
        "allowed_actions": ["APPLY_SOURCE_CONSISTENCY_PATCH"],
        "decision": "APPLY_SOURCE_CONSISTENCY_PATCH",
        "resolution_basis": "Owner-approved correction from authoritative game evidence.",
        "canonical_patch": {},
        "source_patch": {"team_score": "61", "opponent_score": "81"},
        "source_consistency_expected": {
            "team_score": "81",
            "opponent_score": "61",
            "played_result": "L",
        },
        "planned_identity_status": planned_identity_status,
        "identity_method": "fixture",
        "notes": "raw_text preserved",
    }


class SourceConsistencyIssueTests(unittest.TestCase):
    def test_structured_issue_detects_score_result_contradiction(self):
        issue = score_result_consistency_issue(
            {
                "source_game_id": "A-1",
                "team_score": "81",
                "opponent_score": "61",
                "played_result": "L",
            }
        )
        self.assertEqual(issue["score_implied_result"], "W")
        self.assertEqual(issue["played_result"], "L")

    def test_consistent_row_has_no_issue(self):
        self.assertIsNone(
            score_result_consistency_issue(
                {
                    "source_game_id": "A-1",
                    "team_score": "61",
                    "opponent_score": "81",
                    "played_result": "L",
                }
            )
        )


class SourceConsistencyApprovalTests(unittest.TestCase):
    def write_plan_and_review(self, directory, patch_payload):
        root = Path(directory)
        item = source_consistency_item()
        item["decision"] = "PENDING"
        item["resolution_basis"] = ""
        item["canonical_patch_json"] = "{}"
        item["source_patch_json"] = "{}"
        item.pop("canonical_patch", None)
        item.pop("source_patch", None)
        plan = {
            "schema_version": 1,
            "workflow_version": 1,
            "school_key": "alpha",
            "input_fingerprint": {"sha256": "fixture"},
            "blockers": [],
            "warnings": [],
            "summary": {},
            "decisions": [item],
        }
        plan_path = root / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        review_path = root / "review.csv"
        with review_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(REVIEW_COLUMNS), lineterminator="\n")
            writer.writeheader()
            row = {field: item.get(field, "") for field in REVIEW_COLUMNS}
            row["allowed_actions"] = " | ".join(item["allowed_actions"])
            row["decision"] = "APPLY_SOURCE_CONSISTENCY_PATCH"
            row["resolution_basis"] = "Owner-approved authoritative correction."
            row["canonical_patch_json"] = "{}"
            row["source_patch_json"] = json.dumps(patch_payload)
            writer.writerow(row)
        return plan_path, review_path

    def test_approval_accepts_consistency_restoring_source_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path, review_path = self.write_plan_and_review(
                directory,
                {"team_score": "61", "opponent_score": "81"},
            )
            with patch.object(
                onboarding_plan,
                "input_fingerprint",
                return_value={"sha256": "fixture"},
            ):
                approved, _ = approve_plan(
                    ROOT,
                    plan_path,
                    review_path,
                    "owner",
                )
            item = approved["decisions"][0]
            self.assertEqual(
                item["source_patch"],
                {"team_score": "61", "opponent_score": "81"},
            )

    def test_approval_rejects_patch_that_remains_contradictory(self):
        with tempfile.TemporaryDirectory() as directory:
            plan_path, review_path = self.write_plan_and_review(
                directory,
                {"team_score": "70"},
            )
            with patch.object(
                onboarding_plan,
                "input_fingerprint",
                return_value={"sha256": "fixture"},
            ):
                with self.assertRaisesRegex(WorkflowError, "remains contradictory"):
                    approve_plan(
                        ROOT,
                        plan_path,
                        review_path,
                        "owner",
                    )


class SourceConsistencyMapTests(unittest.TestCase):
    def test_compact_map_accepts_source_consistency_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review = root / "review.csv"
            item = source_consistency_item()
            with review.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(REVIEW_COLUMNS), lineterminator="\n")
                writer.writeheader()
                row = {field: item.get(field, "") for field in REVIEW_COLUMNS}
                row["allowed_actions"] = " | ".join(item["allowed_actions"])
                row["decision"] = "PENDING"
                row["resolution_basis"] = ""
                row["canonical_patch_json"] = "{}"
                row["source_patch_json"] = "{}"
                writer.writerow(row)

            mapping = root / "map.json"
            mapping.write_text(
                json.dumps(
                    {
                        "decisions": {
                            item["decision_id"]: "APPLY_SOURCE_CONSISTENCY_PATCH"
                        },
                        "basis_by_decision": {
                            item["decision_id"]: "Owner-approved authoritative correction."
                        },
                        "source_patch_by_decision": {
                            item["decision_id"]: {
                                "team_score": "61",
                                "opponent_score": "81",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )
            counts = fill_review_from_map(review, mapping)
            self.assertEqual(counts["APPLY_SOURCE_CONSISTENCY_PATCH"], 1)
            with review.open(encoding="utf-8-sig", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(
                json.loads(row["source_patch_json"]),
                {"team_score": "61", "opponent_score": "81"},
            )


class SourceConsistencyApplyTests(unittest.TestCase):
    def base_source(self, **updates):
        row = blank_row(
            ingest_school.ASSERTION_FIELDS,
            source_program_key="alpha",
            source_game_id="ALPHA-1",
            season_label="2020-2021",
            game_date="2020-12-30",
            normalized_opponent_key="beta",
            team_score="81",
            opponent_score="61",
            played_result="L",
            curated_site_type="UNKNOWN",
            curated_game_type="REGULAR_SEASON",
            raw_text="Official source literal remains untouched.",
        )
        row.update(updates)
        return row

    def base_canonical(self, **updates):
        row = blank_row(
            ingest_school.CANONICAL_FIELDS,
            canonical_game_id="CBBG-1",
            season_label="2020-2021",
            game_date="2020-12-30",
            team_a_key="alpha",
            team_b_key="beta",
            team_a_score="81",
            team_b_score="61",
            result_winner_team_key="alpha",
            site_type="UNKNOWN",
            game_type="REGULAR_SEASON",
        )
        row.update(updates)
        return row

    def prepare_repo(self, root, canonical, source, discrepancies=None):
        assertion = dict(source)
        assertion.update(
            {
                "assertion_id": "ASRT-ALPHA-1",
                "canonical_game_id": canonical["canonical_game_id"],
                "match_status": "MATCHED",
                "match_method": "FIXTURE",
            }
        )
        write_csv(
            root / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS,
            [canonical],
        )
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS,
            [assertion],
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            discrepancies or [],
        )
        write_csv(
            root / "schools/alpha/source-games.csv",
            ingest_school.ASSERTION_FIELDS,
            [source],
        )

    def read_one(self, path):
        with path.open(encoding="utf-8-sig", newline="") as handle:
            return next(csv.DictReader(handle))

    def test_warning_only_new_game_patch_synchronizes_new_canonical(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            source = self.base_source()
            canonical = self.base_canonical()
            self.prepare_repo(repo, canonical, source)

            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "a" * 64,
                "decisions": [source_consistency_item()],
            }
            counts = apply_reconciliation_decisions(repo, approved)

            corrected = self.read_one(repo / "schools/alpha/source-games.csv")
            assertion = self.read_one(repo / "data/evidence/game-assertions.csv")
            canonical_after = self.read_one(repo / "data/canonical/games.csv")
            self.assertEqual((corrected["team_score"], corrected["opponent_score"]), ("61", "81"))
            self.assertEqual((assertion["team_score"], assertion["opponent_score"]), ("61", "81"))
            self.assertEqual((canonical_after["team_a_score"], canonical_after["team_b_score"]), ("61", "81"))
            self.assertEqual(canonical_after["result_winner_team_key"], "beta")
            self.assertEqual(counts["source_consistency_patches"], 1)
            self.assertEqual(counts["source_consistency_canonical_syncs"], 1)
            self.assertEqual(corrected["raw_text"], "Official source literal remains untouched.")

    def test_overlap_with_reciprocal_score_discrepancy_does_not_double_apply(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            source = self.base_source(
                team_score="64",
                opponent_score="56",
                played_result="L",
            )
            canonical = self.base_canonical(
                team_a_key="alpha",
                team_b_key="beta",
                team_a_score="71",
                team_b_score="73",
                result_winner_team_key="beta",
            )
            discrepancy = blank_row(
                ingest_school.DISCREPANCY_FIELDS,
                discrepancy_id="DISC-1",
                canonical_game_id="CBBG-1",
                field_name="score",
                source_a_program_key="alpha",
                source_a_value="64-56",
                canonical_value="71-73",
                status="UNDER_REVIEW",
            )
            self.prepare_repo(repo, canonical, source, [discrepancy])

            consistency = source_consistency_item(
                planned_identity_status=ingest_school.CONFIDENT
            )
            consistency["source_value"] = "score=64-56; played_result=L"
            consistency["source_consistency_expected"] = {
                "team_score": "64",
                "opponent_score": "56",
                "played_result": "L",
            }
            consistency["source_patch"] = {
                "team_score": "71",
                "opponent_score": "73",
            }
            score_decision = {
                "decision_id": "DISCREPANCY-ALPHA-1-SCORE",
                "category": "discrepancy",
                "source_game_id": "ALPHA-1",
                "canonical_game_id": "CBBG-1",
                "field_name": "score",
                "source_value": "64-56",
                "canonical_value": "71-73",
                "decision": "KEEP_CANONICAL",
                "resolution_basis": "Reciprocal authoritative score controls.",
                "canonical_patch": {},
                "source_patch": {},
            }
            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "b" * 64,
                "decisions": [score_decision, consistency],
            }
            counts = apply_reconciliation_decisions(repo, approved)

            corrected = self.read_one(repo / "schools/alpha/source-games.csv")
            assertion = self.read_one(repo / "data/evidence/game-assertions.csv")
            canonical_after = self.read_one(repo / "data/canonical/games.csv")
            discrepancy_after = self.read_one(
                repo / "data/reconciliation/discrepancies.csv"
            )
            self.assertEqual((corrected["team_score"], corrected["opponent_score"]), ("71", "73"))
            self.assertEqual((assertion["team_score"], assertion["opponent_score"]), ("71", "73"))
            self.assertEqual((canonical_after["team_a_score"], canonical_after["team_b_score"]), ("71", "73"))
            self.assertEqual(discrepancy_after["source_a_value"], "64-56")
            self.assertEqual(discrepancy_after["status"], "RESOLVED")
            self.assertEqual(counts["canonical_retentions"], 1)
            self.assertEqual(counts["source_consistency_patches"], 1)


if __name__ == "__main__":
    unittest.main()
