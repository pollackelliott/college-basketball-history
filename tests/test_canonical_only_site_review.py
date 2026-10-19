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
    _canonical_site_patch_review_decisions,
    apply_reconciliation_decisions,
    approve_plan,
    REVIEW_COLUMNS,
)


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def canonical_game(game_id="CBBG-1"):
    row = {field: "" for field in ingest_school.CANONICAL_FIELDS}
    row.update(
        {
            "canonical_game_id": game_id,
            "season_label": "2002-2003",
            "game_date": "2003-02-09",
            "date_precision": "EXACT",
            "team_a_key": "alpha",
            "team_b_key": "beta",
            "team_a_score": "70",
            "team_b_score": "60",
            "result_winner_team_key": "alpha",
            "site_type": "TEAM_A_HOME",
            "designated_home_team_key": "alpha",
            "game_type": "REGULAR_SEASON",
            "canonical_status": "PROVISIONAL",
        }
    )
    return row


def reciprocal_assertion(game_id="CBBG-1"):
    row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
    row.update(
        {
            "assertion_id": "ASRT-BETA-1",
            "canonical_game_id": game_id,
            "source_program_key": "beta",
            "source_game_id": "BETA-1",
            "season_label": "2002-2003",
            "game_date": "2003-02-09",
            "normalized_opponent_key": "alpha",
            "curated_site_type": "OPPONENT_HOME",
            "match_status": "MATCHED",
            "match_method": "FIXTURE",
        }
    )
    return row


def relationship(venue_id, venue_key, canonical_name):
    return {
        "venue_id": venue_id,
        "venue_key": venue_key,
        "canonical_name": canonical_name,
        "city": "Alpha City",
        "state": "AA",
        "relationship_type": "source_program_home",
        "relationship_start": "2002-2003",
        "relationship_end": "2002-2003",
        "source_basis": "documented home chronology",
    }


def registry(venue_id, venue_key, display_name):
    return {
        "venue_id": venue_id,
        "venue_key": venue_key,
        "display_name": display_name,
        "city": "Alpha City",
        "state": "AA",
    }


class CanonicalOnlySiteReviewTests(unittest.TestCase):
    def test_ambiguous_reciprocal_only_home_gap_becomes_owner_review(self):
        game = canonical_game()
        assertions = {"CBBG-1": [reciprocal_assertion()]}
        rel_a = relationship("VEN-1", "arena-a", "Arena A")
        rel_b = relationship("VEN-2", "arena-b", "Arena B")
        reg_a = registry("VEN-1", "arena-a", "Arena A")
        reg_b = registry("VEN-2", "arena-b", "Arena B")

        decisions = _canonical_site_patch_review_decisions(
            school_key="alpha",
            history_start_season="1900-1901",
            canonical_rows=[game],
            assertions_by_game=assertions,
            planned_target_canonical_ids=set(),
            school_venue_rows=[rel_a, rel_b],
            venues_by_id={"VEN-1": reg_a, "VEN-2": reg_b},
            venues_by_key={"arena-a": reg_a, "arena-b": reg_b},
        )

        self.assertEqual(len(decisions), 1)
        decision = decisions[0]
        self.assertEqual(
            decision["decision_id"],
            "CANONICAL-SITE-PATCH-CBBG-1",
        )
        self.assertEqual(decision["category"], "canonical_site_patch")
        self.assertEqual(
            decision["allowed_actions"],
            ["APPLY_CANONICAL_PATCH", "LEAVE_UNRESOLVED"],
        )
        self.assertIn("Arena A", decision["relevant_evidence"])
        self.assertIn("Arena B", decision["relevant_evidence"])

    def test_unique_open_ended_chronology_remains_automatic_not_owner_review(self):
        game = canonical_game()
        assertions = {"CBBG-1": [reciprocal_assertion()]}
        rel = relationship("VEN-1", "arena-a", "Arena A")
        rel["relationship_end"] = "present"
        reg = registry("VEN-1", "arena-a", "Arena A")

        decisions = _canonical_site_patch_review_decisions(
            school_key="alpha",
            history_start_season="1900-1901",
            canonical_rows=[game],
            assertions_by_game=assertions,
            planned_target_canonical_ids=set(),
            school_venue_rows=[rel],
            venues_by_id={"VEN-1": reg},
            venues_by_key={"arena-a": reg},
        )

        self.assertEqual(decisions, [])


    def test_identity_candidate_without_confirmed_match_gets_conditional_site_review(self):
        game = canonical_game()
        assertions = {"CBBG-1": [reciprocal_assertion()]}
        args = {
            "school_key": "alpha",
            "history_start_season": "1900-1901",
            "canonical_rows": [game],
            "assertions_by_game": assertions,
            "school_venue_rows": [],
            "venues_by_id": {},
            "venues_by_key": {},
            "candidate_identity_source_ids_by_canonical": {"CBBG-1": {"ALPHA-1"}},
        }
        decisions = _canonical_site_patch_review_decisions(
            planned_target_canonical_ids=set(), **args
        )
        self.assertEqual(len(decisions), 1)
        self.assertEqual(
            decisions[0]["conditional_identity_source_game_ids"], ["ALPHA-1"]
        )
        self.assertEqual(
            decisions[0]["decision_id"], "CANONICAL-SITE-PATCH-CBBG-1"
        )
        self.assertEqual(
            _canonical_site_patch_review_decisions(
                planned_target_canonical_ids={"CBBG-1"}, **args
            ),
            [],
        )

    def test_conditional_site_patch_seals_only_when_identity_is_rejected(self):
        game = canonical_game()
        site_decision = _canonical_site_patch_review_decisions(
            school_key="alpha",
            history_start_season="1900-1901",
            canonical_rows=[game],
            assertions_by_game={"CBBG-1": [reciprocal_assertion()]},
            planned_target_canonical_ids=set(),
            candidate_identity_source_ids_by_canonical={"CBBG-1": {"ALPHA-1"}},
            school_venue_rows=[],
            venues_by_id={},
            venues_by_key={},
        )[0]
        identity = {
            "decision_id": "IDENTITY-ALPHA-1",
            "category": "identity",
            "source_game_id": "ALPHA-1",
            "canonical_value": "CBBG-1",
            "allowed_actions": ["FORCE_NEW", "MATCH_CANONICAL:CBBG-1"],
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
        }
        expected_patch = {
            "venue_id": "VEN-1",
            "venue_key": "arena-a",
            "site_city": "Alpha City",
            "site_state": "AA",
        }
        for selected, expected_site_action in (
            ("FORCE_NEW", "APPLY_CANONICAL_PATCH"),
            ("MATCH_CANONICAL:CBBG-1", "NOT_APPLICABLE"),
        ):
            with self.subTest(selected=selected), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                plan = {
                    "school_key": "alpha",
                    "input_fingerprint": {"sha256": "fixed-fixture"},
                    "decisions": [identity, site_decision],
                }
                plan_path = root / "plan.json"
                plan_path.write_text(json.dumps(plan), encoding="utf-8")
                review_path = root / "review.csv"
                review_rows = []
                for decision in plan["decisions"]:
                    row = {field: decision.get(field, "") for field in REVIEW_COLUMNS}
                    row["allowed_actions"] = " | ".join(decision["allowed_actions"])
                    row["decision"] = (
                        selected if decision["category"] == "identity"
                        else "APPLY_CANONICAL_PATCH"
                    )
                    row["resolution_basis"] = "Test evidence and owner choice"
                    row["canonical_patch_json"] = (
                        "{}" if decision["category"] == "identity"
                        else json.dumps(expected_patch)
                    )
                    review_rows.append(row)
                write_csv(review_path, REVIEW_COLUMNS, review_rows)
                with patch(
                    "onboarding_plan.input_fingerprint",
                    return_value={"sha256": "fixed-fixture"},
                ):
                    approved, _ = approve_plan(
                        root, plan_path, review_path, "test-owner"
                    )
                site = next(
                    item for item in approved["decisions"]
                    if item["category"] == "canonical_site_patch"
                )
                self.assertEqual(site["decision"], expected_site_action)
                self.assertEqual(
                    site["canonical_patch"],
                    expected_patch if selected == "FORCE_NEW" else {},
                )

    def test_conditional_site_not_applicable_does_not_mutate_reciprocal_game(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            game = canonical_game()
            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [game],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS,
                [reciprocal_assertion()],
            )
            write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS, [],
            )
            write_csv(
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS, [],
            )
            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "a" * 64,
                "decisions": [{
                    "decision_id": "CANONICAL-SITE-PATCH-CBBG-1",
                    "category": "canonical_site_patch",
                    "source_game_id": "",
                    "canonical_game_id": "CBBG-1",
                    "conditional_identity_source_game_ids": ["ALPHA-1"],
                    "decision": "NOT_APPLICABLE",
                    "canonical_patch": {},
                    "source_patch": {},
                }],
            }
            counts = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(
                counts["conditional_canonical_site_not_applicable"], 1
            )
            with (repo / "data/canonical/games.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                after = list(csv.DictReader(handle))[0]
            self.assertEqual(after["site_type"], game["site_type"])
            self.assertEqual(after["venue_key"], "")
            with (repo / "data/evidence/game-assertions.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 1)

    def test_owner_patch_updates_only_canonical_site_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            game = canonical_game()
            assertion = reciprocal_assertion()

            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [game],
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
                repo / "schools/alpha/source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [],
            )
            write_csv(
                repo / "data/reference/venues.csv",
                [
                    "venue_id",
                    "venue_key",
                    "display_name",
                    "city",
                    "state",
                ],
                [
                    {
                        "venue_id": "VEN-1",
                        "venue_key": "arena-a",
                        "display_name": "Arena A",
                        "city": "Alpha City",
                        "state": "AA",
                    }
                ],
            )

            approved = {
                "school_key": "alpha",
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": "CANONICAL-SITE-PATCH-CBBG-1",
                        "category": "canonical_site_patch",
                        "source_game_id": "",
                        "canonical_game_id": "CBBG-1",
                        "field_name": "site_metadata",
                        "decision": "APPLY_CANONICAL_PATCH",
                        "resolution_basis": "Owner identified the alternate HOME venue.",
                        "canonical_patch": {
                            "venue_id": "VEN-1",
                            "venue_key": "arena-a",
                            "site_city": "Alpha City",
                            "site_state": "AA",
                        },
                        "source_patch": {},
                    }
                ],
            }

            counts = apply_reconciliation_decisions(repo, approved)

            self.assertEqual(counts["canonical_site_patches"], 1)
            with (repo / "data/canonical/games.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                updated = list(csv.DictReader(handle))[0]
            self.assertEqual(updated["site_type"], "TEAM_A_HOME")
            self.assertEqual(updated["venue_id"], "VEN-1")
            self.assertEqual(updated["venue_key"], "arena-a")
            self.assertEqual(updated["site_city"], "Alpha City")
            self.assertEqual(updated["site_state"], "AA")
            self.assertIn("OWNER_APPROVED_CANONICAL_SITE_PATCH", updated["notes"])

            with (repo / "data/evidence/game-assertions.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                assertions = list(csv.DictReader(handle))
            self.assertEqual(len(assertions), 1)
            self.assertEqual(assertions[0]["source_program_key"], "beta")
            self.assertFalse(
                any(row["source_program_key"] == "alpha" for row in assertions)
            )


if __name__ == "__main__":
    unittest.main()
