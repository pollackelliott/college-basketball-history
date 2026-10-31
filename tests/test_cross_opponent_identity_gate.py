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
from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS,
    WorkflowError,
    _canonical_exact_fingerprint_index,
    _cross_opponent_exact_identity_candidates,
    apply_pre_ingest_source_patches,
    approve_plan,
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


def source_row(**updates):
    row = blank_row(
        ingest_school.ASSERTION_FIELDS,
        source_program_key="alpha",
        source_game_id="ALPHA-1",
        season_label="1951-1952",
        game_date="1951-12-19",
        normalized_opponent_key="beta",
        normalized_opponent_name="Beta",
        team_score="53",
        opponent_score="58",
        played_result="L",
        overtime_periods="0",
        curated_site_type="UNKNOWN",
        curated_game_type="REGULAR_SEASON",
        raw_text="Dec. 19 Beta L 53-58",
    )
    row.update(updates)
    return row


def canonical_row(
    game_id,
    opponent,
    game_date="1951-12-19",
    alpha_score="53",
    opponent_score="58",
    *,
    alpha_is_team_a=True,
):
    if alpha_is_team_a:
        team_a, team_b = "alpha", opponent
        score_a, score_b = alpha_score, opponent_score
    else:
        team_a, team_b = opponent, "alpha"
        score_a, score_b = opponent_score, alpha_score
    return blank_row(
        ingest_school.CANONICAL_FIELDS,
        canonical_game_id=game_id,
        season_label="1951-1952",
        game_date=game_date,
        date_precision="EXACT",
        team_a_key=team_a,
        team_b_key=team_b,
        team_a_score=score_a,
        team_b_score=score_b,
        result_winner_team_key=team_b if int(score_b) > int(score_a) else team_a,
        site_type="UNKNOWN",
        game_type="REGULAR_SEASON",
    )


def cross_identity_item():
    action = "MATCH_CANONICAL:CBBG-GAMMA"
    return {
        "decision_id": "IDENTITY-ALPHA-1",
        "category": "identity",
        "source_game_id": "ALPHA-1",
        "season_label": "1951-1952",
        "source_game_date": "1951-12-19",
        "canonical_game_date": "1951-12-19",
        "matchup": "alpha vs beta",
        "field_name": "game_identity",
        "source_value": "date=1951-12-19; score=53-58",
        "canonical_value": "CBBG-GAMMA",
        "relevant_evidence": "exact date/score cross-opponent candidate",
        "recommended_action": "REVIEW_REQUIRED",
        "allowed_actions": [action, "FORCE_NEW"],
        "decision": "PENDING",
        "resolution_basis": "",
        "canonical_patch_json": "{}",
        "source_patch_json": "{}",
        "source_identity_expected": {
            "season_label": "1951-1952",
            "game_date": "1951-12-19",
            "normalized_opponent_key": "beta",
            "normalized_opponent_name": "Beta",
        },
        "cross_season_source_patch_by_action": {},
        "cross_opponent_source_patch_by_action": {
            action: {
                "normalized_opponent_key": "gamma",
                "normalized_opponent_name": "Gamma",
            }
        },
        "notes": "EXACT_DATE_SCORE_CROSS_OPPONENT_CANDIDATE",
    }


class CrossOpponentCandidateTests(unittest.TestCase):
    def test_exact_date_score_candidate_is_surfaced(self):
        src = source_row()
        rows = [canonical_row("CBBG-GAMMA", "gamma")]
        candidates = _cross_opponent_exact_identity_candidates(
            src,
            _canonical_exact_fingerprint_index(rows),
        )
        self.assertEqual(
            [row["canonical_game_id"] for row in candidates],
            ["CBBG-GAMMA"],
        )

    def test_reverse_canonical_orientation_is_surfaced(self):
        src = source_row()
        rows = [
            canonical_row(
                "CBBG-GAMMA",
                "gamma",
                alpha_is_team_a=False,
            )
        ]
        candidates = _cross_opponent_exact_identity_candidates(
            src,
            _canonical_exact_fingerprint_index(rows),
        )
        self.assertEqual(
            [row["canonical_game_id"] for row in candidates],
            ["CBBG-GAMMA"],
        )

    def test_ambiguous_exact_population_remains_owner_reviewable(self):
        src = source_row()
        rows = [
            canonical_row("CBBG-DELTA", "delta"),
            canonical_row("CBBG-GAMMA", "gamma"),
        ]
        candidates = _cross_opponent_exact_identity_candidates(
            src,
            _canonical_exact_fingerprint_index(rows),
        )
        self.assertEqual(
            [row["canonical_game_id"] for row in candidates],
            ["CBBG-DELTA", "CBBG-GAMMA"],
        )

    def test_near_misses_are_rejected(self):
        src = source_row()
        rows = [
            canonical_row(
                "CBBG-WRONG-DATE",
                "gamma",
                game_date="1951-12-20",
            ),
            canonical_row(
                "CBBG-WRONG-SCORE",
                "delta",
                alpha_score="54",
                opponent_score="58",
            ),
        ]
        candidates = _cross_opponent_exact_identity_candidates(
            src,
            _canonical_exact_fingerprint_index(rows),
        )
        self.assertEqual(candidates, [])


class CrossOpponentApprovalTests(unittest.TestCase):
    def write_plan_review(self, directory, source_patch):
        root = Path(directory)
        item = cross_identity_item()
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
            writer = csv.DictWriter(
                handle,
                fieldnames=list(REVIEW_COLUMNS),
                lineterminator="\n",
            )
            writer.writeheader()
            row = {field: item.get(field, "") for field in REVIEW_COLUMNS}
            row["allowed_actions"] = " | ".join(item["allowed_actions"])
            row["decision"] = "MATCH_CANONICAL:CBBG-GAMMA"
            row["resolution_basis"] = "Owner-approved opponent identity correction."
            row["canonical_patch_json"] = "{}"
            row["source_patch_json"] = json.dumps(source_patch)
            writer.writerow(row)
        return plan_path, review_path

    def approve(self, plan_path, review_path):
        with patch.object(
            onboarding_plan,
            "input_fingerprint",
            return_value={"sha256": "fixture"},
        ):
            return approve_plan(
                ROOT,
                plan_path,
                review_path,
                "owner",
            )

    def test_cross_opponent_identity_requires_exact_preflight_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            plan, review = self.write_plan_review(
                directory,
                {
                    "normalized_opponent_key": "gamma",
                    "normalized_opponent_name": "Gamma",
                },
            )
            approved, _ = self.approve(plan, review)
            self.assertEqual(
                approved["decisions"][0]["source_patch"],
                {
                    "normalized_opponent_key": "gamma",
                    "normalized_opponent_name": "Gamma",
                },
            )

    def test_arbitrary_cross_opponent_patch_is_rejected(self):
        for bad_patch in (
            {},
            {
                "normalized_opponent_key": "gamma",
                "normalized_opponent_name": "Wrong Name",
            },
            {
                "normalized_opponent_key": "gamma",
                "normalized_opponent_name": "Gamma",
                "game_date": "1951-12-20",
            },
        ):
            with self.subTest(bad_patch=bad_patch):
                with tempfile.TemporaryDirectory() as directory:
                    plan, review = self.write_plan_review(directory, bad_patch)
                    with self.assertRaisesRegex(
                        WorkflowError,
                        "exact preflight-proven normalized_opponent_key",
                    ):
                        self.approve(plan, review)


class CrossOpponentPreIngestTests(unittest.TestCase):
    def test_patch_preserves_literal_evidence_and_reuses_one_canonical_game(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            src = source_row()
            canonical = canonical_row("CBBG-GAMMA", "gamma")
            write_csv(
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [src],
            )
            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )

            item = cross_identity_item()
            item["decision"] = "MATCH_CANONICAL:CBBG-GAMMA"
            item["resolution_basis"] = "Owner-approved opponent identity correction."
            item["canonical_patch"] = {}
            item["source_patch"] = {
                "normalized_opponent_key": "gamma",
                "normalized_opponent_name": "Gamma",
            }
            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "a" * 64,
                "decisions": [item],
            }

            counts = apply_pre_ingest_source_patches(repo, approved)
            self.assertEqual(counts["cross_opponent_identity_patches"], 1)

            with (
                repo / "schools/alpha/source-games.csv"
            ).open(encoding="utf-8-sig", newline="") as handle:
                patched = next(csv.DictReader(handle))

            self.assertEqual(patched["normalized_opponent_key"], "gamma")
            self.assertEqual(patched["normalized_opponent_name"], "Gamma")
            self.assertEqual(patched["raw_text"], "Dec. 19 Beta L 53-58")

            status, game_id, method = ingest_school.resolve_sealed_identity_decision(
                patched,
                "MATCH_CANONICAL:CBBG-GAMMA",
                [canonical],
                {"CBBG-GAMMA": canonical},
            )
            self.assertEqual(status, ingest_school.CONFIDENT)
            self.assertEqual(game_id, "CBBG-GAMMA")
            self.assertEqual(method, "SEALED_OWNER_MATCH_CANONICAL")

    def test_pre_ingest_refuses_exact_fingerprint_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            src = source_row()
            canonical = canonical_row(
                "CBBG-GAMMA",
                "gamma",
                opponent_score="59",
            )
            write_csv(
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [src],
            )
            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )
            item = cross_identity_item()
            item["decision"] = "MATCH_CANONICAL:CBBG-GAMMA"
            item["source_patch"] = {
                "normalized_opponent_key": "gamma",
                "normalized_opponent_name": "Gamma",
            }
            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "b" * 64,
                "decisions": [item],
            }
            with self.assertRaisesRegex(
                WorkflowError,
                "exact fingerprint drifted",
            ):
                apply_pre_ingest_source_patches(repo, approved)


if __name__ == "__main__":
    unittest.main()
