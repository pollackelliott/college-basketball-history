"""Stage 2 owner-gated generic postseason classification regressions."""

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    WorkflowError, apply_pre_ingest_source_patches,
    apply_reconciliation_decisions,
)
from postseason_classification_review import (  # noqa: E402
    build_review_rows, mismatch_is_reviewable, row_fingerprint,
)


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sample_source():
    row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
    row.update({
        "source_game_id": "SCHOOL-POST-01",
        "source_program_key": "school",
        "season_label": "2023-2024",
        "game_date": "2024-04-08",
        "normalized_opponent_key": "purdue",
        "source_opponent_label": "Purdue",
        "team_score": "75",
        "opponent_score": "60",
        "played_result": "W",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_game_type": "POSTSEASON",
        "curated_postseason_round": "",
        "curated_venue_name": "Example Arena",
        "raw_text": "Institutional 2024 title score; immutable literal.",
    })
    return row


def review_item(row=None, **changes):
    row = row or sample_source()
    candidate = {
        "source": row,
        "canonical_game_id": "",
        "canonical_game_date": "",
        "canonical_game_type": "",
    }
    item = build_review_rows("school", [candidate])[0]
    item.update({
        "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
        "resolution_basis": "Owner-approved, exact institutional result.",
        "source_patch": {
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "Championship",
        },
        "canonical_patch": {},
    })
    item.update(changes)
    return item


def make_source_repo(root, source=None):
    source = source or sample_source()
    path = root / "schools/school/source-games.csv"
    write_csv(path, list(source), [source])
    return path


class EligibilityAndReviewTests(unittest.TestCase):
    def setUp(self):
        self.reference = {
            "ncaa_tournament_appearances": "3",
            "final_four_appearances": "1",
            "national_championships": "1",
        }
        self.derived = {
            "ncaa_tournament_appearances": 1,
            "final_four_appearances": 0,
            "national_championships": 0,
        }

    def candidates(self, seasons):
        return [{
            "source": {**sample_source(),
                       "source_game_id": f"POST-{j}",
                       "season_label": season},
        } for j, season in enumerate(seasons)]

    def test_missing_appearances_with_sufficient_generic_seasons_reviewable(self):
        self.assertTrue(mismatch_is_reviewable(
            self.reference, self.derived,
            self.candidates(["2022-2023", "2023-2024"]),
        ))

    def test_absent_generic_postseason_remains_blocked(self):
        self.assertFalse(mismatch_is_reviewable(
            self.reference, self.derived, [],
        ))

    def test_insufficient_distinct_seasons_remains_blocked(self):
        self.assertFalse(mismatch_is_reviewable(
            self.reference, self.derived,
            self.candidates(["2023-2024", "2023-2024"]),
        ))

    def test_existing_earned_titles_cannot_be_erased(self):
        self.derived["national_championships"] = 2
        self.assertFalse(mismatch_is_reviewable(
            self.reference, self.derived,
            self.candidates(["2022-2023", "2023-2024"]),
        ))

    def test_no_automatic_ncaa_reclassification(self):
        row = sample_source()
        original = dict(row)
        decisions = build_review_rows("school", [{
            "source": row, "canonical_game_id": "",
        }])
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["decision"], "PENDING")
        self.assertEqual(decisions[0]["source_value"], "POSTSEASON")
        self.assertEqual(decisions[0]["source_game_date"], "2024-04-08")
        self.assertEqual(row, original)

    def test_duplicate_or_non_generic_rows_refused(self):
        candidate = {"source": sample_source()}
        with self.assertRaisesRegex(ValueError, "unique"):
            build_review_rows("school", [candidate, candidate])
        row = sample_source()
        row["curated_game_type"] = "NCAA_TOURNAMENT"
        with self.assertRaisesRegex(ValueError, "generic"):
            build_review_rows("school", [{"source": row}])

    def test_fingerprint_binds_every_frozen_source_field(self):
        source = sample_source()
        original = row_fingerprint(source)
        source["raw_text"] += " changed"
        self.assertNotEqual(row_fingerprint(source), original)


class SealedPreIngestTests(unittest.TestCase):
    def run_apply(self, **changes):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = make_source_repo(repo)
            item = review_item(**changes)
            result = apply_pre_ingest_source_patches(
                repo, {"school_key": "school", "decisions": [item]}
            )
            return result, read_csv(path)[0]

    def test_source_type_and_round_only_under_sealed_decision(self):
        counts, row = self.run_apply()
        self.assertEqual(counts["postseason_classifications_applied"], 1)
        self.assertEqual(row["curated_game_type"], "NCAA_TOURNAMENT")
        self.assertEqual(row["curated_postseason_round"], "Championship")
        self.assertEqual(row["curated_site_type"], "SOURCE_PROGRAM_HOME")
        self.assertEqual(
            row["raw_text"], "Institutional 2024 title score; immutable literal."
        )

    def test_explicit_site_change_is_separate_and_counted(self):
        counts, row = self.run_apply(source_patch={
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "Championship",
            "curated_site_type": "NEUTRAL",
        })
        self.assertEqual(counts["postseason_owner_site_patches"], 1)
        self.assertEqual(row["curated_site_type"], "NEUTRAL")

    def test_unknown_round_cannot_pass(self):
        with self.assertRaisesRegex(WorkflowError, "invalid NCAA round"):
            self.run_apply(source_patch={
                "curated_game_type": "NCAA_TOURNAMENT",
                "curated_postseason_round": "Regional Quarterfinal",
            })

    def test_invalid_type_cannot_pass(self):
        with self.assertRaisesRegex(WorkflowError, "invalid sealed postseason"):
            self.run_apply(source_patch={"curated_game_type": "REGULAR_SEASON"})

    def test_raw_text_patch_cannot_pass(self):
        with self.assertRaisesRegex(WorkflowError, "forbidden source fields"):
            self.run_apply(source_patch={
                "curated_game_type": "NIT",
                "raw_text": "fabricated",
            })

    def test_fingerprint_change_stops_transaction(self):
        with self.assertRaisesRegex(WorkflowError, "frozen postseason"):
            self.run_apply(source_row_sha256="0" * 64)

    def test_unresolved_status_requires_no_patch(self):
        counts, row = self.run_apply(
            decision="KEEP_POSTSEASON_UNRESOLVED", source_patch={}
        )
        self.assertEqual(counts["postseason_classifications_left_unresolved"], 1)
        self.assertEqual(row["curated_game_type"], "POSTSEASON")
        with self.assertRaisesRegex(WorkflowError, "unchanged"):
            self.run_apply(decision="KEEP_POSTSEASON_UNRESOLVED")


class PostIngestCanonicalTests(unittest.TestCase):
    def make_repo(self, root, canonical_type="POSTSEASON", source_type="NCAA_TOURNAMENT"):
        src = sample_source()
        src["curated_game_type"] = source_type
        src["curated_postseason_round"] = "Championship"
        source_path = make_source_repo(root, src)
        assertion = dict(src)
        assertion.update({
            "assertion_id": "ASRT-TEST-0001",
            "canonical_game_id": "CBBG-0000001",
            "match_status": "CONFIDENT",
            "match_method": "EXACT",
        })
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS, [assertion],
        )
        canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
        canonical.update({
            "canonical_game_id": "CBBG-0000001",
            "season_label": "2023-2024",
            "game_date": "2024-04-08",
            "date_precision": "EXACT",
            "team_a_key": "purdue",
            "team_b_key": "school",
            "site_type": "NEUTRAL",
            "game_type": canonical_type,
            "postseason_round": "",
        })
        write_csv(
            root / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS, [canonical],
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS, [],
        )
        return source_path

    def make_approved(self):
        return {
            "school_key": "school",
            "approved_plan_hash": "a" * 64,
            "decisions": [{
                "decision_id": "POSTSEASON-CLASSIFICATION-SCHOOL-POST-01",
                "category": "postseason_classification",
                "source_game_id": "SCHOOL-POST-01",
                "canonical_game_id": "CBBG-0000001",
                "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
                "resolution_basis": "Institutional championship result.",
                "source_patch": {
                    "curated_game_type": "NCAA_TOURNAMENT",
                    "curated_postseason_round": "Championship",
                },
                "canonical_patch": {},
            }],
        }

    def test_generic_canonical_is_enriched_after_owner_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.make_repo(repo)
            counts = apply_reconciliation_decisions(repo, self.make_approved())
            self.assertEqual(counts["postseason_canonical_types_enriched"], 1)
            final = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(final["game_type"], "NCAA_TOURNAMENT")
            self.assertEqual(final["postseason_round"], "Championship")

    def test_established_conflicting_canonical_requires_separate_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.make_repo(repo, canonical_type="REGULAR_SEASON")
            with self.assertRaisesRegex(WorkflowError, "own explicit Gate 1"):
                apply_reconciliation_decisions(repo, self.make_approved())

    def test_original_review_population_not_auto_approved(self):
        source = sample_source()
        decision = build_review_rows("school", [{"source": source}])[0]
        self.assertEqual(decision["decision"], "PENDING")
        self.assertEqual(decision["allowed_actions"], [
            "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
            "KEEP_POSTSEASON_UNRESOLVED",
        ])


if __name__ == "__main__":
    unittest.main()
