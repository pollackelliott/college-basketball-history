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
    _unique_adjacent_season_score_identity_candidate,
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
        season_label="1962-1963",
        game_date="1962-12-13",
        normalized_opponent_key="beta",
        normalized_opponent_name="Beta",
        team_score="77",
        opponent_score="86",
        played_result="L",
        overtime_periods="0",
        curated_site_type="UNKNOWN",
        curated_game_type="REGULAR_SEASON",
        raw_text="Dec. 13 Beta L 77-86",
    )
    row.update(updates)
    return row


def canonical_row(game_id, season, date, score_a, score_b, **updates):
    row = blank_row(
        ingest_school.CANONICAL_FIELDS,
        canonical_game_id=game_id,
        season_label=season,
        game_date=date,
        date_precision="EXACT",
        team_a_key="alpha",
        team_b_key="beta",
        team_a_score=score_a,
        team_b_score=score_b,
        result_winner_team_key=(
            "alpha" if int(score_a) > int(score_b) else "beta"
        ),
        site_type="UNKNOWN",
        game_type="REGULAR_SEASON",
    )
    row.update(updates)
    return row


def cross_identity_item():
    action = "MATCH_CANONICAL:CBBG-OLD"
    return {
        "decision_id": "IDENTITY-ALPHA-1",
        "category": "identity",
        "source_game_id": "ALPHA-1",
        "season_label": "1962-1963",
        "source_game_date": "1962-12-13",
        "canonical_game_date": "1962-12-22;1963-01-14;1962-02-12",
        "matchup": "alpha vs beta",
        "field_name": "game_identity",
        "source_value": "date=1962-12-13; score=77-86",
        "canonical_value": "CBBG-CUR1;CBBG-CUR2;CBBG-OLD",
        "relevant_evidence": "unique adjacent-season exact-score candidate",
        "recommended_action": "REVIEW_REQUIRED",
        "allowed_actions": [
            "MATCH_CANONICAL:CBBG-CUR1",
            "MATCH_CANONICAL:CBBG-CUR2",
            action,
            "FORCE_NEW",
        ],
        "decision": "PENDING",
        "resolution_basis": "",
        "canonical_patch_json": "{}",
        "source_patch_json": "{}",
        "source_identity_expected": {
            "season_label": "1962-1963",
            "game_date": "1962-12-13",
        },
        "cross_season_source_patch_by_action": {
            action: {
                "season_label": "1961-1962",
                "game_date": "1962-02-12",
            }
        },
        "notes": "UNIQUE_ADJACENT_SEASON_EXACT_SCORE_CANDIDATE",
    }


class AdjacentSeasonCandidateTests(unittest.TestCase):
    def index(self, rows):
        result = {}
        for row in rows:
            key = (
                row["team_a_key"],
                row["team_b_key"],
                row["season_label"],
            )
            result.setdefault(key, []).append(row)
        return result

    def test_unique_adjacent_exact_score_candidate_is_surfaced(self):
        source = source_row()
        rows = [
            canonical_row("CBBG-CUR1", "1962-1963", "1962-12-22", "70", "60"),
            canonical_row("CBBG-CUR2", "1962-1963", "1963-01-14", "65", "55"),
            canonical_row("CBBG-OLD", "1961-1962", "1962-02-12", "77", "86"),
        ]
        candidate = _unique_adjacent_season_score_identity_candidate(
            source,
            self.index(rows),
        )
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate["canonical_game_id"], "CBBG-OLD")

    def test_current_season_exact_score_suppresses_adjacent_candidate(self):
        source = source_row()
        rows = [
            canonical_row("CBBG-CUR", "1962-1963", "1962-12-22", "77", "86"),
            canonical_row("CBBG-OLD", "1961-1962", "1962-02-12", "77", "86"),
        ]
        self.assertIsNone(
            _unique_adjacent_season_score_identity_candidate(
                source,
                self.index(rows),
            )
        )

    def test_ambiguous_adjacent_exact_score_population_is_rejected(self):
        source = source_row()
        rows = [
            canonical_row("CBBG-OLD", "1961-1962", "1962-02-12", "77", "86"),
            canonical_row("CBBG-NEXT", "1963-1964", "1963-12-15", "77", "86"),
        ]
        self.assertIsNone(
            _unique_adjacent_season_score_identity_candidate(
                source,
                self.index(rows),
            )
        )


class AdjacentSeasonApprovalTests(unittest.TestCase):
    def write_plan_review(self, directory, *, action, source_patch):
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
            row["decision"] = action
            row["resolution_basis"] = "Owner-approved identity correction."
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

    def test_cross_season_identity_requires_exact_preflight_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            plan, review = self.write_plan_review(
                directory,
                action="MATCH_CANONICAL:CBBG-OLD",
                source_patch={
                    "season_label": "1961-1962",
                    "game_date": "1962-02-12",
                },
            )
            approved, _ = self.approve(plan, review)
            self.assertEqual(
                approved["decisions"][0]["source_patch"],
                {
                    "season_label": "1961-1962",
                    "game_date": "1962-02-12",
                },
            )

    def test_cross_season_identity_rejects_missing_or_wrong_patch(self):
        for bad_patch in (
            {},
            {"season_label": "1961-1962"},
            {
                "season_label": "1961-1962",
                "game_date": "1962-02-13",
            },
        ):
            with self.subTest(bad_patch=bad_patch):
                with tempfile.TemporaryDirectory() as directory:
                    plan, review = self.write_plan_review(
                        directory,
                        action="MATCH_CANONICAL:CBBG-OLD",
                        source_patch=bad_patch,
                    )
                    with self.assertRaisesRegex(
                        WorkflowError,
                        "exact preflight-proven season_label and game_date",
                    ):
                        self.approve(plan, review)

    def test_current_season_identity_rejects_arbitrary_source_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            plan, review = self.write_plan_review(
                directory,
                action="MATCH_CANONICAL:CBBG-CUR1",
                source_patch={"game_date": "1962-12-22"},
            )
            with self.assertRaisesRegex(
                WorkflowError,
                "source patches are permitted only",
            ):
                self.approve(plan, review)


class AdjacentSeasonMapTests(unittest.TestCase):
    def test_compact_map_can_encode_cross_season_identity_patch(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            review_path = root / "review.csv"
            item = cross_identity_item()
            with review_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(
                    handle,
                    fieldnames=list(REVIEW_COLUMNS),
                    lineterminator="\n",
                )
                writer.writeheader()
                row = {field: item.get(field, "") for field in REVIEW_COLUMNS}
                row["allowed_actions"] = " | ".join(item["allowed_actions"])
                writer.writerow(row)

            mapping = root / "map.json"
            mapping.write_text(
                json.dumps(
                    {
                        "identity": {
                            "ALPHA-1": "MATCH_CANONICAL:CBBG-OLD"
                        },
                        "defaults": {
                            "identity_basis": "Owner-approved identity correction."
                        },
                        "source_patch_by_decision": {
                            "IDENTITY-ALPHA-1": {
                                "season_label": "1961-1962",
                                "game_date": "1962-02-12",
                            }
                        },
                    }
                ),
                encoding="utf-8",
            )

            counts = fill_review_from_map(review_path, mapping)
            self.assertEqual(
                counts["MATCH_CANONICAL:CBBG-OLD"],
                1,
            )
            with review_path.open(
                encoding="utf-8-sig",
                newline="",
            ) as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(
                json.loads(row["source_patch_json"]),
                {
                    "season_label": "1961-1962",
                    "game_date": "1962-02-12",
                },
            )


class AdjacentSeasonPreIngestTests(unittest.TestCase):
    def test_sealed_patch_runs_before_exact_identity_resolution(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            source = source_row()
            canonical = canonical_row(
                "CBBG-OLD",
                "1961-1962",
                "1962-02-12",
                "77",
                "86",
            )
            write_csv(
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [source],
            )
            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )

            item = cross_identity_item()
            item["decision"] = "MATCH_CANONICAL:CBBG-OLD"
            item["resolution_basis"] = "Owner-approved identity correction."
            item["canonical_patch"] = {}
            item["source_patch"] = {
                "season_label": "1961-1962",
                "game_date": "1962-02-12",
            }
            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "a" * 64,
                "decisions": [item],
            }

            counts = apply_pre_ingest_source_patches(repo, approved)
            self.assertEqual(counts["adjacent_season_identity_patches"], 1)

            with (
                repo / "schools/alpha/source-games.csv"
            ).open(encoding="utf-8-sig", newline="") as handle:
                patched = next(csv.DictReader(handle))

            self.assertEqual(patched["season_label"], "1961-1962")
            self.assertEqual(patched["game_date"], "1962-02-12")
            self.assertEqual(
                patched["raw_text"],
                "Dec. 13 Beta L 77-86",
            )

            status, game_id, method = ingest_school.resolve_sealed_identity_decision(
                patched,
                "MATCH_CANONICAL:CBBG-OLD",
                [canonical],
                {"CBBG-OLD": canonical},
            )
            self.assertEqual(status, ingest_school.CONFIDENT)
            self.assertEqual(game_id, "CBBG-OLD")
            self.assertEqual(method, "SEALED_OWNER_MATCH_CANONICAL")

    def test_pre_ingest_refuses_canonical_season_date_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            source = source_row()
            canonical = canonical_row(
                "CBBG-OLD",
                "1961-1962",
                "1962-02-13",
                "77",
                "86",
            )
            write_csv(
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [source],
            )
            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )
            item = cross_identity_item()
            item["decision"] = "MATCH_CANONICAL:CBBG-OLD"
            item["source_patch"] = {
                "season_label": "1961-1962",
                "game_date": "1962-02-12",
            }
            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "b" * 64,
                "decisions": [item],
            }
            with self.assertRaisesRegex(
                WorkflowError,
                "canonical season/date drifted",
            ):
                apply_pre_ingest_source_patches(repo, approved)


if __name__ == "__main__":
    unittest.main()
