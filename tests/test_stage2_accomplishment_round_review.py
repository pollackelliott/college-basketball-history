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
from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS,
    WorkflowError,
    apply_pre_ingest_source_patches,
    apply_reconciliation_decisions,
    approve_plan,
)


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class Stage2AccomplishmentRoundReviewTests(unittest.TestCase):
    def test_new_game_round_patch_resolves_canonical_id_after_ingestion(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            school_key = "example"
            source_id = "EXAMPLE-NEW-TITLE"
            canonical_id = "CBBG-NEW-0001"

            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            canonical.update(
                {
                    "canonical_game_id": canonical_id,
                    "season_label": "2003-2004",
                    "game_date": "2004-04-05",
                    "date_precision": "EXACT",
                    "team_a_key": school_key,
                    "team_b_key": "opponent",
                    "team_a_score": "73",
                    "team_b_score": "82",
                    "result_winner_team_key": "opponent",
                    "overtime_periods": "0",
                    "site_type": "NEUTRAL",
                    "game_type": "NCAA_TOURNAMENT",
                    "postseason_round": "",
                    "canonical_status": "PROVISIONAL",
                }
            )

            source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            source.update(
                {
                    "source_program_key": school_key,
                    "source_game_id": source_id,
                    "season_label": "2003-2004",
                    "game_date": "2004-04-05",
                    "normalized_opponent_key": "opponent",
                    "team_score": "73",
                    "opponent_score": "82",
                    "played_result": "L",
                    "overtime_periods": "0",
                    "curated_site_type": "NEUTRAL",
                    "curated_game_type": "NCAA_TOURNAMENT",
                    "curated_postseason_round": "",
                    "raw_text": "National championship game; raw source preserved.",
                }
            )
            assertion = dict(source)
            assertion.update(
                {
                    "assertion_id": "ASRT-EXAMPLE-1",
                    "canonical_game_id": canonical_id,
                    "match_status": "NEW_CANONICAL",
                    "match_method": "NEW_GAME",
                }
            )

            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS,
                [assertion],
            )
            write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS,
                [],
            )
            write_csv(
                repo / "schools" / school_key / "source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [source],
            )

            approved = {
                "school_key": school_key,
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": "NCAA-ROUND-PATCH-EXAMPLE-NEW-TITLE",
                        "category": "ncaa_round_patch",
                        "source_game_id": source_id,
                        # Preflight cannot know the ID assigned to a NEW_GAME.
                        "canonical_game_id": "",
                        "field_name": "postseason_round",
                        "decision": "APPLY_NCAA_ROUND_PATCH",
                        "resolution_basis": "Authoritative tournament evidence.",
                        "canonical_patch": {"postseason_round": "Championship"},
                        "source_patch": {
                            "curated_postseason_round": "Championship"
                        },
                    }
                ],
            }

            counts = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(counts["ncaa_round_patches"], 1)

            with (repo / "data/canonical/games.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                canonical_after = next(csv.DictReader(handle))
            with (repo / "data/evidence/game-assertions.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                assertion_after = next(csv.DictReader(handle))
            with (repo / "schools" / school_key / "source-games.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                source_after = next(csv.DictReader(handle))

            self.assertEqual(canonical_after["postseason_round"], "Championship")
            self.assertEqual(
                assertion_after["curated_postseason_round"],
                "Championship",
            )
            self.assertEqual(
                source_after["curated_postseason_round"],
                "Championship",
            )
            self.assertEqual(
                source_after["raw_text"],
                "National championship game; raw source preserved.",
            )



class OwnerReviewedNewGameDateTests(unittest.TestCase):
    """New canonical-game dates require a sealed, evidenced, bounded patch."""

    def make_case(
        self, repo, *, new_date="2015-03-19",
        action="LEAVE_UNRESOLVED", canonical_id="", notes=None,
        source_patch=None, canonical_patch=None,
    ):
        school = "example"
        source_id = "EXAMPLE-LAFAYETTE"
        original = "2015-03-11"
        decision_id = "NCAA-ROUND-PATCH-" + source_id
        source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
        source.update({
            "source_program_key": school,
            "source_game_id": source_id,
            "season_label": "2014-2015",
            "game_date": original,
            "normalized_opponent_key": "lafayette",
            "team_score": "93",
            "opponent_score": "52",
            "played_result": "W",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_site_type": "NEUTRAL",
            "curated_postseason_round": "",
            "raw_text": "Frozen record-book transcription: March 11, Lafayette.",
        })
        source_path = repo / "schools/example/source-games.csv"
        write_csv(source_path, ingest_school.ASSERTION_FIELDS, [source])
        write_csv(
            repo / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS, [],
        )
        item = {
            "decision_id": decision_id,
            "category": "ncaa_round_patch",
            "source_game_id": source_id,
            "source_game_date": original,
            "canonical_game_id": canonical_id,
            "season_label": "2014-2015",
            "allowed_actions": [
                "APPLY_NCAA_ROUND_PATCH", "LEAVE_UNRESOLVED",
            ],
        }
        plan_path = repo / "plan.json"
        plan_path.write_text(json.dumps({
            "school_key": school,
            "input_fingerprint": {"sha256": "frozen"},
            "blockers": [],
            "decisions": [item],
        }), encoding="utf-8")
        if source_patch is None:
            source_patch = {"game_date": new_date}
        if canonical_patch is None:
            canonical_patch = {}
        row = {field: "" for field in REVIEW_COLUMNS}
        row.update({
            "decision_id": decision_id,
            "decision": action,
            "resolution_basis": (
                "Institutional official NCAA schedule proves the game date."
            ),
            "notes": notes if notes is not None else (
                f"Official schedule correction from {original} to {new_date}."
            ),
            "source_patch_json": json.dumps(source_patch),
            "canonical_patch_json": json.dumps(canonical_patch),
        })
        review_path = repo / "review.csv"
        write_csv(review_path, REVIEW_COLUMNS, [row])
        return source_path, plan_path, review_path

    def seal(self, repo, plan, review):
        with patch("onboarding_plan.input_fingerprint",
                   return_value={"sha256": "frozen"}):
            return approve_plan(repo, plan, review, "owner")[0]

    def test_sealed_date_patch_changes_only_date_and_preserves_literal(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source_path, plan, review = self.make_case(repo)
            approved = self.seal(repo, plan, review)
            item = approved["decisions"][0]
            self.assertEqual(item["source_patch"], {"game_date": "2015-03-19"})
            counts = apply_pre_ingest_source_patches(repo, approved)
            self.assertEqual(counts, {"new_game_date_patches": 1})
            with source_path.open(encoding="utf-8-sig", newline="") as handle:
                source = next(csv.DictReader(handle))
            self.assertEqual(source["game_date"], "2015-03-19")
            self.assertEqual(source["season_label"], "2014-2015")
            self.assertEqual(source["curated_postseason_round"], "")
            self.assertIn("March 11", source["raw_text"])
            self.assertIn("old=2015-03-11 new=2015-03-19", source["notes"])

            # Simulate the standard ingest result: one newly minted canonical
            # row and one target assertion, both on the corrected date.
            canonical_id = "CBBG-NEW-0001"
            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            canonical.update({
                "canonical_game_id": canonical_id,
                "season_label": "2014-2015",
                "game_date": "2015-03-19",
                "team_a_key": "example",
                "team_b_key": "lafayette",
                "game_type": "NCAA_TOURNAMENT",
            })
            write_csv(repo / "data/canonical/games.csv",
                      ingest_school.CANONICAL_FIELDS, [canonical])
            assertion = dict(source)
            assertion.update({
                "assertion_id": "ASRT-EXAMPLE-1",
                "canonical_game_id": canonical_id,
                "match_status": "MATCHED",
                "match_method": "NO_SAME_SEASON_TEAM_PAIR",
            })
            write_csv(repo / "data/evidence/game-assertions.csv",
                      ingest_school.ASSERTION_FIELDS, [assertion])
            write_csv(repo / "data/reconciliation/discrepancies.csv",
                      ingest_school.DISCREPANCY_FIELDS, [])
            counts = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(counts["new_game_dates_verified"], 1)
            self.assertEqual(counts["ncaa_rounds_left_unresolved"], 1)
            with (repo / "data/canonical/games.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                canonical = next(csv.DictReader(handle))
            self.assertIn("OWNER_APPROVED_NEW_GAME_DATE_PATCH", canonical["notes"])
            self.assertEqual(canonical["game_date"], "2015-03-19")

    def test_round_enrichment_and_date_patch_can_coexist(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _, plan, review = self.make_case(
                repo, action="APPLY_NCAA_ROUND_PATCH",
                source_patch={
                    "game_date": "2015-03-19",
                    "curated_postseason_round": "R64",
                },
                canonical_patch={"postseason_round": "R64"},
            )
            item = self.seal(repo, plan, review)["decisions"][0]
            self.assertEqual(
                item["source_patch"]["curated_postseason_round"], "R64"
            )
            self.assertEqual(item["source_patch"]["game_date"], "2015-03-19")

    def test_rejects_arbitrary_new_game_date_changes(self):
        cases = [
            ({"game_date": "2015-03-11"}, "", "must change"),
            ({"game_date": "2015-03-XX"}, "", "exact ISO"),
            ({"game_date": "2016-03-19"}, "", "cannot change the season"),
            ({"game_date": "2015-03-19", "team_score": "1"}, "",
             "may not carry NCAA round patches"),
            ({"game_date": "2015-03-19"}, "CBBG-0123456",
             "requires a NEW_GAME"),
        ]
        for source_patch, canonical_id, error in cases:
            with self.subTest(source_patch=source_patch, canonical_id=canonical_id):
                with tempfile.TemporaryDirectory() as tmp:
                    repo = Path(tmp)
                    _, plan, review = self.make_case(
                        repo, source_patch=source_patch,
                        canonical_id=canonical_id,
                    )
                    with self.assertRaisesRegex(WorkflowError, error):
                        self.seal(repo, plan, review)

    def test_rejects_missing_date_evidence_and_source_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _, plan, review = self.make_case(
                repo, notes="Only a round note, no dates."
            )
            with self.assertRaisesRegex(WorkflowError, "date patch notes"):
                self.seal(repo, plan, review)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source_path, plan, review = self.make_case(repo)
            approved = self.seal(repo, plan, review)
            with source_path.open(encoding="utf-8", newline="") as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["game_date"] = "2015-03-12"
            write_csv(source_path, ingest_school.ASSERTION_FIELDS, rows)
            with self.assertRaisesRegex(WorkflowError, "frozen new-game"):
                apply_pre_ingest_source_patches(repo, approved)

    def test_rejects_collision_with_already_canonical_game(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _, plan, review = self.make_case(repo)
            approved = self.seal(repo, plan, review)
            existing = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            existing.update({
                "canonical_game_id": "CBBG-0000900",
                "team_a_key": "example",
                "team_b_key": "lafayette",
                "season_label": "2014-2015",
                "game_date": "2015-03-19",
            })
            write_csv(repo / "data/canonical/games.csv",
                      ingest_school.CANONICAL_FIELDS, [existing])
            with self.assertRaisesRegex(
                WorkflowError, "explicit identity review required"
            ):
                apply_pre_ingest_source_patches(repo, approved)

    def test_original_round_only_unresolved_review_needs_no_date_patch(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            _, plan, review = self.make_case(
                repo, source_patch={}, notes="Round genuinely unresolved."
            )
            approved = self.seal(repo, plan, review)
            self.assertEqual(apply_pre_ingest_source_patches(repo, approved), {})



if __name__ == "__main__":
    unittest.main()
