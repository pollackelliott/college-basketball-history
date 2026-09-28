import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
from implementation_site_gate import implementation_site_report  # noqa: E402
from onboarding_hardening import fill_review_from_map  # noqa: E402
from onboarding_plan import (  # noqa: E402
    SOURCE_ASSERTION_COPY_FIELDS,
    WorkflowError,
    _sync_site_metadata_to_source,
    apply_reconciliation_decisions,
)


REVIEW_FIELDS = [
    "decision_id",
    "category",
    "source_game_id",
    "season_label",
    "source_game_date",
    "canonical_game_date",
    "matchup",
    "field_name",
    "source_value",
    "canonical_value",
    "relevant_evidence",
    "recommended_action",
    "allowed_actions",
    "decision",
    "resolution_basis",
    "canonical_patch_json",
    "source_patch_json",
    "notes",
]


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


class Stage2SiteResearchSourcePatchMapTests(unittest.TestCase):
    decision_id = "DISCREPANCY-TESTRAW-1-GAME_DATE"

    def make_review(self, root):
        review = root / "review.csv"
        write_csv(
            review,
            REVIEW_FIELDS,
            [
                {
                    "decision_id": self.decision_id,
                    "category": "discrepancy",
                    "source_game_id": "TESTRAW-1",
                    "season_label": "1939-1940",
                    "source_game_date": "1940-01-02",
                    "canonical_game_date": "1940-01-01",
                    "matchup": "test vs other",
                    "field_name": "game_date",
                    "source_value": "1940-01-02",
                    "canonical_value": "1940-01-01",
                    "relevant_evidence": "fixture",
                    "recommended_action": "KEEP_CANONICAL",
                    "allowed_actions": (
                        "KEEP_CANONICAL | LEAVE_UNRESOLVED | "
                        "NORMALIZE_SOURCE_TO_CANONICAL | USE_SOURCE"
                    ),
                    "decision": "PENDING",
                    "resolution_basis": "",
                    "canonical_patch_json": "{}",
                    "source_patch_json": "{}",
                    "notes": "",
                }
            ],
        )
        return review

    def write_map(self, root, **extra):
        mapping = {
            "defaults": {
                "discrepancy": "KEEP_CANONICAL",
                "basis": "Owner-approved historical review fixture.",
            },
            **extra,
        }
        path = root / "map.json"
        path.write_text(json.dumps(mapping), encoding="utf-8")
        return path

    def test_compact_map_accepts_paired_source_research_patch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            review = self.make_review(root)
            mapping = self.write_map(
                root,
                source_patch_by_decision={
                    self.decision_id: {
                        "site_research_status": "RESEARCHED_UNRESOLVED",
                        "site_research_basis": (
                            "Institutional and reciprocal site evidence reviewed; "
                            "exact historical neutral site remains unresolved."
                        ),
                    }
                },
            )

            fill_review_from_map(review, mapping)

            row = read_csv(review)[0]
            self.assertEqual(
                json.loads(row["source_patch_json"]),
                {
                    "site_research_status": "RESEARCHED_UNRESOLVED",
                    "site_research_basis": (
                        "Institutional and reciprocal site evidence reviewed; "
                        "exact historical neutral site remains unresolved."
                    ),
                },
            )

    def test_research_accounting_fields_are_rejected_from_canonical_patch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            review = self.make_review(root)
            mapping = self.write_map(
                root,
                canonical_patch_by_decision={
                    self.decision_id: {
                        "site_research_status": "RESEARCHED_UNRESOLVED",
                    }
                },
            )

            with self.assertRaisesRegex(
                WorkflowError,
                "forbidden canonical patch fields",
            ):
                fill_review_from_map(review, mapping)

    def test_protected_raw_text_remains_rejected_from_source_patch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            review = self.make_review(root)
            mapping = self.write_map(
                root,
                source_patch_by_decision={
                    self.decision_id: {"raw_text": "rewritten evidence"}
                },
            )

            with self.assertRaisesRegex(
                WorkflowError,
                "forbidden source patch fields",
            ):
                fill_review_from_map(review, mapping)


class Stage2SiteResearchSourcePatchApplyTests(unittest.TestCase):
    def make_repo(self, root, research_columns=()):
        source_fields = list(SOURCE_ASSERTION_COPY_FIELDS) + list(research_columns)
        source = {
            "source_program_key": "test",
            "source_game_id": "TESTRAW-1",
            "source_era": "historical",
            "season_label": "1939-1940",
            "game_date": "1940-01-02",
            "source_opponent_label": "Other",
            "normalized_opponent_key": "other",
            "normalized_opponent_name": "Other",
            "team_score": "50",
            "opponent_score": "40",
            "played_result": "W",
            "overtime_periods": "0",
            "source_site_candidate": "Neutral",
            "curated_site_type": "NEUTRAL",
            "source_venue_name": "",
            "curated_venue_name": "",
            "city": "",
            "state": "",
            "event_or_tournament": "",
            "source_round": "",
            "curated_game_type": "REGULAR_SEASON",
            "curated_postseason_round": "",
            "source_page": "fixture",
            "raw_text": "literal source evidence",
            "normalization_status": "CURATED",
            "administrative_status": "",
            "administrative_note": "",
            "notes": "",
            "site_research_status": "",
            "site_research_basis": "",
        }
        write_csv(
            root / "schools/test/source-games.csv",
            source_fields,
            [source],
        )

        canonical = {
            "canonical_game_id": "CBBG-1",
            "season_label": "1939-1940",
            "game_date": "1940-01-01",
            "date_precision": "EXACT",
            "team_a_key": "test",
            "team_b_key": "other",
            "team_a_score": "50",
            "team_b_score": "40",
            "result_winner_team_key": "test",
            "overtime_periods": "0",
            "site_type": "NEUTRAL",
            "designated_home_team_key": "",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "game_type": "REGULAR_SEASON",
            "postseason_round": "",
            "administrative_status": "",
            "administrative_note": "",
            "canonical_status": "CURATED",
            "notes": "",
        }
        write_csv(
            root / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS,
            [canonical],
        )

        assertion = {
            **source,
            "assertion_id": "AST-1",
            "canonical_game_id": "CBBG-1",
            "match_status": "MATCHED",
            "match_method": "fixture",
        }
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS,
            [assertion],
        )

        discrepancy = {
            "discrepancy_id": "DISC-000001",
            "canonical_game_id": "CBBG-1",
            "field_name": "game_date",
            "source_a_program_key": "test",
            "source_a_value": "1940-01-02",
            "source_b_program_key": "",
            "source_b_value": "",
            "canonical_value": "1940-01-01",
            "status": "UNDER_REVIEW",
            "resolution_basis": "",
            "notes": "",
        }
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            [discrepancy],
        )

        write_csv(
            root / "data/reference/programs.csv",
            ["program_key", "history_start_season"],
            [{"program_key": "test", "history_start_season": "1900-1901"}],
        )

    def approved(self, source_patch):
        return {
            "school_key": "test",
            "approved_plan_hash": "a" * 64,
            "decisions": [
                {
                    "decision_id": "DISCREPANCY-TESTRAW-1-GAME_DATE",
                    "category": "discrepancy",
                    "source_game_id": "TESTRAW-1",
                    "canonical_game_id": "CBBG-1",
                    "field_name": "game_date",
                    "source_value": "1940-01-02",
                    "canonical_value": "1940-01-01",
                    "decision": "KEEP_CANONICAL",
                    "resolution_basis": "Owner-approved fixture.",
                    "canonical_patch": {},
                    "source_patch": source_patch,
                }
            ],
        }

    def apply_and_report(self, patch):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        self.make_repo(root)
        apply_reconciliation_decisions(root, self.approved(patch))
        return root, implementation_site_report(root, "test")

    def test_apply_path_persists_metadata_without_assertion_pollution(self):
        basis = (
            "Institutional and reciprocal evidence reviewed; exact historical "
            "neutral venue and locality remain unresolved."
        )
        root, report = self.apply_and_report(
            {
                "site_research_status": "RESEARCHED_UNRESOLVED",
                "site_research_basis": basis,
            }
        )

        source_path = root / "schools/test/source-games.csv"
        with source_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertIn("site_research_status", reader.fieldnames)
            self.assertIn("site_research_basis", reader.fieldnames)
            source = next(reader)
        self.assertEqual(source["site_research_status"], "RESEARCHED_UNRESOLVED")
        self.assertEqual(source["site_research_basis"], basis)

        assertion_path = root / "data/evidence/game-assertions.csv"
        with assertion_path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            self.assertNotIn("site_research_status", reader.fieldnames)
            self.assertNotIn("site_research_basis", reader.fieldnames)
            next(reader)

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["counts"]["public_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 0)

    def test_missing_basis_is_rejected_by_site_completeness(self):
        _, report = self.apply_and_report(
            {"site_research_status": "RESEARCHED_UNRESOLVED"}
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(
            any(
                "site_research_basis is required" in error
                for error in report["errors"]
            )
        )

    def test_missing_status_is_rejected_by_site_completeness(self):
        _, report = self.apply_and_report(
            {
                "site_research_basis": (
                    "Evidence reviewed but status intentionally omitted in fixture."
                )
            }
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(
            any(
                "site_research_status is required" in error
                for error in report["errors"]
            )
        )

    def test_invalid_status_is_rejected_by_site_completeness(self):
        _, report = self.apply_and_report(
            {
                "site_research_status": "UNSUPPORTED_STATUS",
                "site_research_basis": "Evidence reviewed.",
            }
        )
        self.assertEqual(report["status"], "FAIL")
        self.assertTrue(
            any(
                "invalid site_research_status" in error
                for error in report["errors"]
            )
        )

    def test_malformed_one_column_source_schema_is_rejected_before_write(self):
        for lone_column in ("site_research_status", "site_research_basis"):
            with self.subTest(lone_column=lone_column):
                with tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    self.make_repo(root, research_columns=(lone_column,))
                    with self.assertRaisesRegex(
                        WorkflowError,
                        "must contain both site_research_status and site_research_basis",
                    ):
                        apply_reconciliation_decisions(
                            root,
                            self.approved(
                                {
                                    "site_research_status": "RESEARCHED_UNRESOLVED",
                                    "site_research_basis": "Evidence reviewed.",
                                }
                            ),
                        )

    def test_fully_resolved_site_still_clears_stale_research_metadata(self):
        source = {
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "",
            "state": "",
            "curated_game_type": "REGULAR_SEASON",
            "site_research_status": "RESEARCHED_UNRESOLVED",
            "site_research_basis": "Previously unresolved.",
        }
        canonical = {
            "venue_key": "example-arena",
            "site_city": "Example City",
            "site_state": "EX",
        }

        _sync_site_metadata_to_source(
            source,
            canonical,
            {"example-arena": "Example Arena"},
        )

        self.assertEqual(source["curated_venue_name"], "Example Arena")
        self.assertEqual(source["city"], "Example City")
        self.assertEqual(source["state"], "EX")
        self.assertEqual(source["site_research_status"], "")
        self.assertEqual(source["site_research_basis"], "")


if __name__ == "__main__":
    unittest.main()
