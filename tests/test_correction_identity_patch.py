"""Fail-closed regressions for sealed post-publication canonical identity repair."""

from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import ingest_school  # noqa: E402
import onboard_school  # noqa: E402
import onboarding_plan as plan  # noqa: E402
from integration_freeze_guard import (  # noqa: E402
    SEMANTIC_SOURCE_GAME_FIELDS,
    semantic_snapshot_sha256,
)


SOURCE_FIELDS = list(dict.fromkeys([
    "source_game_id", "source_program_key",
    "normalized_opponent_key", "normalized_opponent_name", "notes",
    *SEMANTIC_SOURCE_GAME_FIELDS,
]))


def write_table(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def source(opponent="georgetown", state="", **changes):
    row = dict.fromkeys(SOURCE_FIELDS, "")
    row.update({
        "source_game_id": "TENRAW-00136",
        "source_program_key": "tennessee",
        "normalized_opponent_key": opponent,
        "normalized_opponent_name": (
            "Georgetown" if opponent == "georgetown"
            else "Georgetown (Ky.)" if opponent == "georgetown-ky"
            else "Test College"
        ),
        "season_label": "1918-1919",
        "game_date": "1919-02-27",
        "source_opponent_label": "Georgetown",
        "team_score": "33", "opponent_score": "34", "played_result": "L",
        "curated_site_type": "OPPONENT_HOME",
        "city": "Lexington", "state": state,
        "curated_game_type": "REGULAR_SEASON",
        "raw_text": "F27 at Georgetown L, 33-34 Lexington",
    })
    row.update(changes)
    return row


def canonical(**changes):
    row = dict.fromkeys(ingest_school.CANONICAL_FIELDS, "")
    row.update({
        "canonical_game_id": "CBBG-0020298",
        "season_label": "1918-1919",
        "game_date": "1919-02-27",
        "date_precision": "EXACT",
        "team_a_key": "georgetown", "team_b_key": "tennessee",
        "team_a_score": "34", "team_b_score": "33",
        "result_winner_team_key": "georgetown",
        "site_type": "TEAM_A_HOME",
        "designated_home_team_key": "georgetown",
        "site_city": "Lexington", "site_state": "",
        "game_type": "REGULAR_SEASON",
    })
    row.update(changes)
    return row


def assertion(previous, **changes):
    row = dict.fromkeys(ingest_school.ASSERTION_FIELDS, "")
    row.update(previous)
    row.update({
        "assertion_id": "ASSERT-TENRAW-00136",
        "canonical_game_id": "CBBG-0020298",
        "source_program_key": "tennessee",
        "source_game_id": "TENRAW-00136",
        "normalized_opponent_key": previous["normalized_opponent_key"],
        "normalized_opponent_name": previous["normalized_opponent_name"],
    })
    row.update(changes)
    return row


def snapshot(rows):
    value = {
        "schema_version": 1,
        "fields": list(SEMANTIC_SOURCE_GAME_FIELDS),
        "rows": {
            row["source_game_id"]: {
                field: row.get(field, "") for field in SEMANTIC_SOURCE_GAME_FIELDS
            }
            for row in rows
        },
    }
    return {
        "schema_version": 1,
        "snapshot": value,
        "snapshot_sha256": semantic_snapshot_sha256(value),
    }


class CorrectionIdentityTests(unittest.TestCase):
    def fixture(
        self, root, *, new_opponent="georgetown-ky", new_state="KY",
        correction_ids=None,
    ):
        root.mkdir(parents=True, exist_ok=True)
        before = source()
        after = source(new_opponent, new_state)
        source_path = root / "schools/tennessee/source-games.csv"
        write_table(source_path, SOURCE_FIELDS, [before])
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        subprocess.run(["git", "add", "schools/tennessee/source-games.csv"],
                       cwd=root, check=True)
        subprocess.run([
            "git", "-c", "user.name=Regression", "-c",
            "user.email=regression@example.test", "commit", "-qm", "baseline"
        ], cwd=root, check=True)
        base_sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True
        ).strip()
        write_table(source_path, SOURCE_FIELDS, [after])
        write_table(root / "data/canonical/games.csv",
                    ingest_school.CANONICAL_FIELDS, [canonical()])
        write_table(root / "data/evidence/game-assertions.csv",
                    ingest_school.ASSERTION_FIELDS, [assertion(before)])
        manifest = {
            "schema_version": 2,
            "workflow_kind": "POST_PUBLICATION_CORRECTION",
            "status": "INTEGRATION_FROZEN",
            "school_key": "tennessee",
            "research_base_sha": base_sha,
            "correction_source_game_ids": correction_ids if correction_ids is not None
                                          else ["TENRAW-00136"],
            "pre_correction_source_semantic_guard": snapshot([before]),
            "source_game_semantic_guard": snapshot([after]),
            "package_member_sha256": {
                "source-games.csv": plan.sha256_file(source_path)
            },
        }
        manifest_path = root / ".onboarding/tennessee/integration-freeze.json"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return before, after, manifest_path

    def reviews(self, root):
        src = plan.read_csv(root / "schools/tennessee/source-games.csv")
        canonicals = plan.read_csv(root / "data/canonical/games.csv")
        assertions = plan.read_csv(root / "data/evidence/game-assertions.csv")
        game_by_id = {r["canonical_game_id"]: r for r in canonicals}
        by_source = {}
        by_game = {}
        for a in assertions:
            by_source.setdefault(
                (a["source_program_key"], a["source_game_id"]), []
            ).append(a)
            by_game.setdefault(a["canonical_game_id"], []).append(a)
        return plan._post_publication_identity_review_decisions(
            root, "tennessee", src, game_by_id, by_source, by_game
        )

    def approved(self, decision):
        decision = {**decision,
                    "decision": plan.CORRECTION_IDENTITY_ACTION,
                    "resolution_basis": "Owner-authorized historical identity correction",
                    "source_patch": {}, "canonical_patch": {}}
        return {
            "school_key": "tennessee",
            "approved_plan_hash": "e" * 64,
            "decisions": [decision],
        }

    def test_exact_tennessee_correction_preserves_ids_literal_evidence_and_home(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            before, after, _ = self.fixture(root)
            decisions, projected = self.reviews(root)
            self.assertEqual(len(decisions), 1)
            decision = decisions[0]
            self.assertEqual(decision["old_opponent_key"], "georgetown")
            self.assertEqual(decision["new_opponent_key"], "georgetown-ky")
            self.assertEqual(decision["canonical_game_id"], "CBBG-0020298")
            self.assertEqual(projected["CBBG-0020298"]["team_a_key"], "georgetown-ky")
            self.assertEqual(plan.apply_pre_ingest_correction_identity_patches(
                root, self.approved(decision)
            ), {"correction_identity_patches": 1})
            game = plan.read_csv(root / "data/canonical/games.csv")[0]
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")[0]
            s = plan.read_csv(root / "schools/tennessee/source-games.csv")[0]
            self.assertEqual(game["canonical_game_id"], "CBBG-0020298")
            self.assertEqual((game["team_a_key"], game["team_b_key"]),
                             ("georgetown-ky", "tennessee"))
            self.assertEqual((game["team_a_score"], game["team_b_score"]), ("34", "33"))
            self.assertEqual(game["result_winner_team_key"], "georgetown-ky")
            self.assertEqual(game["site_type"], "TEAM_A_HOME")
            self.assertEqual(game["designated_home_team_key"], "georgetown-ky")
            # Locality remains an explicit Gate 1 site operation, never silently patched.
            self.assertEqual((game["site_city"], game["site_state"]), ("Lexington", ""))
            self.assertEqual((s["city"], s["state"]), ("Lexington", "KY"))
            self.assertEqual((a["assertion_id"], a["canonical_game_id"]),
                             ("ASSERT-TENRAW-00136", "CBBG-0020298"))
            self.assertEqual(a["normalized_opponent_key"], "georgetown-ky")
            self.assertEqual(a["normalized_opponent_name"], "Georgetown (Ky.)")
            self.assertEqual(a["source_opponent_label"], "Georgetown")
            self.assertEqual(a["raw_text"], before["raw_text"])
            self.assertEqual(s["raw_text"], after["raw_text"])

    def test_site_gate_review_is_projected_after_identity_retarget(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            decisions, projected = self.reviews(root)
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")
            review = plan._post_publication_site_review_decisions(
                root, "tennessee",
                plan.read_csv(root / "schools/tennessee/source-games.csv"),
                projected,
                {("tennessee", "TENRAW-00136"): a},
                {"CBBG-0020298": a},
            )
            self.assertEqual(len(decisions), 1)
            self.assertEqual(len(review), 1)
            self.assertEqual(review[0]["category"], "correction_site_patch")
            self.assertEqual(review[0]["canonical_site_expected"]["site_type"],
                             "TEAM_A_HOME")

    def test_normal_ingestion_locality_fill_is_accepted_only_when_exact(self):
        before = {
            "site_type": "TEAM_A_HOME",
            "venue_key": "", "venue_id": "",
            "site_city": "Lexington", "site_state": "",
        }
        after = {**before, "site_state": "KY"}
        src = source("georgetown-ky", "KY")
        self.assertTrue(plan._verified_correction_ingest_locality_enrichment(
            src, before, after
        ))
        self.assertFalse(plan._verified_correction_ingest_locality_enrichment(
            src, before, {**after, "site_city": "Louisville"}
        ))
        self.assertFalse(plan._verified_correction_ingest_locality_enrichment(
            src, before, {**after, "site_type": "NEUTRAL"}
        ))
        self.assertFalse(plan._verified_correction_ingest_locality_enrichment(
            src, before, {**after, "venue_key": "unsupported"}
        ))
        self.assertFalse(plan._verified_correction_ingest_locality_enrichment(
            src, before, before
        ))

    def test_sealed_site_reconciliation_accepts_exact_prior_ingestion_fill(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            identity_decisions, projected = self.reviews(root)
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")
            site_reviews = plan._post_publication_site_review_decisions(
                root, "tennessee",
                plan.read_csv(root / "schools/tennessee/source-games.csv"),
                projected,
                {("tennessee", "TENRAW-00136"): a},
                {"CBBG-0020298": a},
            )
            self.assertEqual(len(site_reviews), 1)
            site_item = {
                **site_reviews[0],
                "decision": "APPLY_CANONICAL_PATCH",
                "resolution_basis": "Owner-authorized correction of Kentucky locality",
                "canonical_patch": {
                    **site_reviews[0]["canonical_site_expected"],
                    "site_state": "KY",
                },
                "source_patch": {},
            }
            approved = self.approved(identity_decisions[0])
            approved["decisions"].append(site_item)
            plan.apply_pre_ingest_correction_identity_patches(root, approved)
            # This exact state is what ordinary ingestion may safely enrich.
            canonical_path = root / "data/canonical/games.csv"
            games = plan.read_csv(canonical_path)
            games[0]["site_state"] = "KY"
            write_table(canonical_path, ingest_school.CANONICAL_FIELDS, games)
            write_table(
                root / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS, []
            )
            write_table(
                root / "data/reference/venues.csv",
                ["venue_id", "venue_key", "city", "state"], []
            )
            result = plan.apply_reconciliation_decisions(root, approved)
            self.assertEqual(result["correction_site_patches"], 1)
            actual = plan.read_csv(canonical_path)[0]
            self.assertEqual((actual["site_city"], actual["site_state"]),
                             ("Lexington", "KY"))
            self.assertEqual(actual["team_a_key"], "georgetown-ky")
            self.assertIn("OWNER_APPROVED_CORRECTION_SITE_PATCH", actual["notes"])
            assertion_row = plan.read_csv(
                root / "data/evidence/game-assertions.csv"
            )[0]
            self.assertEqual((assertion_row["city"], assertion_row["state"]),
                             ("Lexington", "KY"))

    def test_single_game_transaction_kind_accepts_identity_only(self):
        self.assertEqual(
            plan._single_game_correction_transaction_kind(
                {"TENRAW-00136"}, [{"decision_id": "identity"}], []
            ),
            "SINGLE_GAME_IDENTITY",
        )
        self.assertEqual(
            plan._single_game_correction_transaction_kind(
                {"TENRAW-00136"},
                [{"decision_id": "identity"}],
                [{"decision_id": "site"}],
            ),
            "SINGLE_GAME_IDENTITY_SITE",
        )

    def test_single_game_transaction_kind_rejects_broader_scope(self):
        with self.assertRaisesRegex(
            plan.WorkflowError, "zero or one canonical site review"
        ):
            plan._single_game_correction_transaction_kind(
                {"TENRAW-00136"},
                [{"decision_id": "identity"}],
                [{"decision_id": "site-1"}, {"decision_id": "site-2"}],
            )

    def test_one_game_identity_only_execution_preserves_staged_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root, new_state="")
            identity_decisions, projected = self.reviews(root)
            assertions = plan.read_csv(root / "data/evidence/game-assertions.csv")
            sites = plan._post_publication_site_review_decisions(
                root, "tennessee",
                plan.read_csv(root / "schools/tennessee/source-games.csv"),
                projected,
                {("tennessee", "TENRAW-00136"): assertions},
                {"CBBG-0020298": assertions},
            )
            self.assertEqual((len(identity_decisions), len(sites)), (1, 0))
            approved = self.approved(identity_decisions[0])
            approved["summary"] = {
                "correction_transaction_kind": "SINGLE_GAME_IDENTITY",
                "correction_source_game_id": "TENRAW-00136",
                "correction_canonical_game_id": "CBBG-0020298",
            }
            write_table(root / "data/reconciliation/discrepancies.csv",
                        ingest_school.DISCREPANCY_FIELDS, [])
            write_table(root / "data/reference/venues.csv",
                        ["venue_id", "venue_key", "city", "state"], [])
            archive = root / "data/reconciliation/onboarding-decisions/test.json"
            site_report = {
                "school_key": "tennessee",
                "history_start_season": "1908-1909",
                "source_validation_scope": {
                    "mode": "CORRECTION_DELTA", "scoped_source_games": 1,
                    "correction_source_games": 1,
                },
                "source_site_counts": {"rows": 1},
                "counts": {"target_canonical_games": 1},
                "examples": {},
                "status": "PASS", "errors": [], "warnings": [],
            }
            source_path = root / "schools/tennessee/source-games.csv"
            source_before = source_path.read_bytes()
            with (
                patch.object(onboard_school, "run", return_value="site build mocked"),
                patch.object(
                    onboard_school, "capture_correction_site_report",
                    side_effect=[site_report, site_report],
                ),
            ):
                result = onboard_school.execute_approved_in_place(root, approved)
            self.assertEqual(result["transaction_kind"], "SINGLE_GAME_IDENTITY")
            self.assertEqual(source_path.read_bytes(), source_before)
            game = plan.read_csv(root / "data/canonical/games.csv")[0]
            assertion_row = plan.read_csv(
                root / "data/evidence/game-assertions.csv"
            )[0]
            self.assertEqual(game["team_a_key"], "georgetown-ky")
            self.assertEqual(game["result_winner_team_key"], "georgetown-ky")
            self.assertEqual(assertion_row["normalized_opponent_key"], "georgetown-ky")
            self.assertEqual(
                assertion_row["normalized_opponent_name"], "Georgetown (Ky.)"
            )
            rerun_identity, rerun_projected = self.reviews(root)
            rerun_assertions = plan.read_csv(
                root / "data/evidence/game-assertions.csv"
            )
            rerun_sites = plan._post_publication_site_review_decisions(
                root, "tennessee",
                plan.read_csv(root / "schools/tennessee/source-games.csv"),
                rerun_projected,
                {("tennessee", "TENRAW-00136"): rerun_assertions},
                {"CBBG-0020298": rerun_assertions},
            )
            self.assertEqual((rerun_identity, rerun_sites), ([], []))

    def test_one_game_sealed_execution_changes_only_authorized_records(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            identity_decisions, projected = self.reviews(root)
            assertions = plan.read_csv(root / "data/evidence/game-assertions.csv")
            sites = plan._post_publication_site_review_decisions(
                root, "tennessee",
                plan.read_csv(root / "schools/tennessee/source-games.csv"),
                projected,
                {("tennessee", "TENRAW-00136"): assertions},
                {"CBBG-0020298": assertions},
            )
            self.assertEqual((len(identity_decisions), len(sites)), (1, 1))
            site = {
                **sites[0],
                "decision": "APPLY_CANONICAL_PATCH",
                "resolution_basis": "Frozen Lexington, KY opponent-home site",
                "canonical_patch": {
                    "site_type": "TEAM_A_HOME", "site_city": "Lexington",
                    "site_state": "KY", "venue_id": "", "venue_key": "",
                },
                "source_patch": {},
            }
            approved = self.approved(identity_decisions[0])
            approved["decisions"].append(site)
            approved["summary"] = {
                "correction_transaction_kind": "SINGLE_GAME_IDENTITY_SITE",
                "correction_source_game_id": "TENRAW-00136",
                "correction_canonical_game_id": "CBBG-0020298",
            }
            write_table(root / "data/reconciliation/discrepancies.csv",
                        ingest_school.DISCREPANCY_FIELDS, [])
            write_table(root / "data/reference/venues.csv",
                        ["venue_id", "venue_key", "city", "state"], [])
            archive = root / "data/reconciliation/onboarding-decisions/test.json"
            baseline_site = {
                "school_key": "tennessee",
                "history_start_season": "1908-1909",
                "source_validation_scope": {
                    "mode": "CORRECTION_DELTA", "scoped_source_games": 1,
                    "correction_source_games": 1,
                },
                "source_site_counts": {"rows": 1},
                "counts": {
                    "target_canonical_games": 1,
                    "target_source_location_lost": 1,
                },
                "examples": {
                    "target_source_location_lost": ["CBBG-0020298"],
                },
                "status": "FAIL", "errors": ["legacy gap"], "warnings": [],
            }
            corrected_site = {
                **baseline_site,
                "counts": {
                    "target_canonical_games": 1,
                    "target_source_location_lost": 0,
                },
                "examples": {},
                "status": "PASS", "errors": [], "warnings": [],
            }
            with (
                patch.object(onboard_school, "run", return_value="site build mocked"),
                patch.object(
                    onboard_school, "capture_correction_site_report",
                    side_effect=[baseline_site, corrected_site],
                ),
            ):
                result = onboard_school.execute_approved_in_place(root, approved)
            self.assertEqual(result["transaction_kind"], "SINGLE_GAME_IDENTITY_SITE")
            game = plan.read_csv(root / "data/canonical/games.csv")[0]
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")[0]
            src = plan.read_csv(root / "schools/tennessee/source-games.csv")[0]
            self.assertEqual((game["team_a_key"], game["result_winner_team_key"]),
                             ("georgetown-ky", "georgetown-ky"))
            self.assertEqual((game["site_city"], game["site_state"]),
                             ("Lexington", "KY"))
            self.assertEqual((a["normalized_opponent_key"], a["state"]),
                             ("georgetown-ky", "KY"))
            self.assertEqual(src["raw_text"], source()["raw_text"])
            self.assertEqual(plan.read_csv(root / "data/reconciliation/discrepancies.csv"), [])
            rerun_identity, rerun_projected = self.reviews(root)
            rerun_assertions = plan.read_csv(
                root / "data/evidence/game-assertions.csv"
            )
            rerun_sites = plan._post_publication_site_review_decisions(
                root, "tennessee",
                plan.read_csv(root / "schools/tennessee/source-games.csv"),
                rerun_projected,
                {("tennessee", "TENRAW-00136"): rerun_assertions},
                {"CBBG-0020298": rerun_assertions},
            )
            self.assertEqual((rerun_identity, rerun_sites), ([], []))

    def test_applied_identity_without_archived_plan_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root, new_state="")
            decisions, _ = self.reviews(root)
            plan.apply_pre_ingest_correction_identity_patches(
                root, self.approved(decisions[0])
            )
            with self.assertRaisesRegex(
                plan.WorkflowError, "lacks archived sealed plan"
            ):
                self.reviews(root)

    def test_identity_only_boundary_rejects_source_note_mutation(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root, new_state="")
            write_table(root / "data/reconciliation/discrepancies.csv",
                        ingest_school.DISCREPANCY_FIELDS, [])
            before = onboard_school._single_game_correction_snapshot(
                root, "tennessee"
            )
            source_path = root / "schools/tennessee/source-games.csv"
            rows = plan.read_csv(source_path)
            rows[0]["notes"] = "unexpected mutation"
            write_table(source_path, SOURCE_FIELDS, rows)
            after = onboard_school._single_game_correction_snapshot(
                root, "tennessee"
            )
            with self.assertRaisesRegex(
                plan.WorkflowError, "identity-only correction changed staged source row"
            ):
                onboard_school._prove_single_game_correction_boundary(
                    before, after, source_id="TENRAW-00136",
                    game_id="CBBG-0020298", school="tennessee",
                    expect_source_change=False,
                )

    def test_single_game_delta_guard_rejects_any_other_game_or_discrepancy(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            write_table(root / "data/reconciliation/discrepancies.csv",
                        ingest_school.DISCREPANCY_FIELDS, [])
            old = onboard_school._single_game_correction_snapshot(root, "tennessee")
            other = canonical(canonical_game_id="CBBG-9999999", game_date="1919-03-03")
            cp = root / "data/canonical/games.csv"
            write_table(cp, ingest_school.CANONICAL_FIELDS, [canonical(), other])
            after = onboard_school._single_game_correction_snapshot(root, "tennessee")
            with self.assertRaisesRegex(plan.WorkflowError, "canonical row IDs"):
                onboard_school._prove_single_game_correction_boundary(
                    old, after, source_id="TENRAW-00136",
                    game_id="CBBG-0020298", school="tennessee",
                )
            write_table(cp, ingest_school.CANONICAL_FIELDS, [canonical()])
            disc = {field: "" for field in ingest_school.DISCREPANCY_FIELDS}
            disc["discrepancy_id"] = "DISC-999999"
            write_table(root / "data/reconciliation/discrepancies.csv",
                        ingest_school.DISCREPANCY_FIELDS, [disc])
            after = onboard_school._single_game_correction_snapshot(root, "tennessee")
            with self.assertRaisesRegex(plan.WorkflowError, "discrepancy row IDs"):
                onboard_school._prove_single_game_correction_boundary(
                    old, after, source_id="TENRAW-00136",
                    game_id="CBBG-0020298", school="tennessee",
                )

    def test_single_game_delta_guard_prohibits_changes_to_raw_source(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.fixture(root)
            write_table(root / "data/reconciliation/discrepancies.csv",
                        ingest_school.DISCREPANCY_FIELDS, [])
            old = onboard_school._single_game_correction_snapshot(root, "tennessee")
            source_path = root / "schools/tennessee/source-games.csv"
            changed = source("georgetown-ky", "KY", raw_text="invented evidence")
            write_table(source_path, SOURCE_FIELDS, [changed])
            after = onboard_school._single_game_correction_snapshot(root, "tennessee")
            with self.assertRaisesRegex(plan.WorkflowError, "unauthorized source evidence"):
                onboard_school._prove_single_game_correction_boundary(
                    old, after, source_id="TENRAW-00136",
                    game_id="CBBG-0020298", school="tennessee",
                )

    def test_lexicographic_flip_preserves_score_winner_and_site(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root, new_opponent="zz-college")
            decisions, _ = self.reviews(root)
            plan.apply_pre_ingest_correction_identity_patches(
                root, self.approved(decisions[0])
            )
            game = plan.read_csv(root / "data/canonical/games.csv")[0]
            self.assertEqual((game["team_a_key"], game["team_b_key"]),
                             ("tennessee", "zz-college"))
            self.assertEqual((game["team_a_score"], game["team_b_score"]), ("33", "34"))
            self.assertEqual(game["result_winner_team_key"], "zz-college")
            self.assertEqual(game["site_type"], "TEAM_B_HOME")
            self.assertEqual(game["designated_home_team_key"], "zz-college")

    def test_single_source_multiple_assertions_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")
            a.append({**a[0], "assertion_id": "ANOTHER"})
            write_table(root / "data/evidence/game-assertions.csv",
                        ingest_school.ASSERTION_FIELDS, a)
            with self.assertRaisesRegex(plan.WorkflowError, "exactly one"):
                self.reviews(root)

    def test_other_assertion_on_same_canonical_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")
            a.append({**a[0], "assertion_id": "OTHER", "source_program_key": "other"})
            write_table(root / "data/evidence/game-assertions.csv",
                        ingest_school.ASSERTION_FIELDS, a)
            with self.assertRaisesRegex(plan.WorkflowError, "exclusively"):
                self.reviews(root)

    def test_collision_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            rows = plan.read_csv(root / "data/canonical/games.csv")
            rows.append(canonical(canonical_game_id="CBBG-COLLISION",
                                  team_a_key="georgetown-ky"))
            write_table(root / "data/canonical/games.csv",
                        ingest_school.CANONICAL_FIELDS, rows)
            with self.assertRaisesRegex(plan.WorkflowError, "collision"):
                self.reviews(root)

    def test_original_published_opponent_must_match_existing_assertion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")
            a[0]["normalized_opponent_key"] = "unrelated"
            write_table(root / "data/evidence/game-assertions.csv",
                        ingest_school.ASSERTION_FIELDS, a)
            with self.assertRaisesRegex(plan.WorkflowError, "original assertion"):
                self.reviews(root)

    def test_out_of_scope_source_id_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            decisions, _ = self.reviews(root)
            manifest_path = root / ".onboarding/tennessee/integration-freeze.json"
            manifest = json.loads(manifest_path.read_text())
            manifest["correction_source_game_ids"] = ["OTHER"]
            manifest_path.write_text(json.dumps(manifest))
            with self.assertRaises(plan.WorkflowError):
                plan.apply_pre_ingest_correction_identity_patches(
                    root, self.approved(decisions[0])
                )

    def test_stale_frozen_package_hash_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            decisions, _ = self.reviews(root)
            source_path = root / "schools/tennessee/source-games.csv"
            rows = plan.read_csv(source_path)
            rows[0]["normalized_opponent_name"] = "stale unsealed value"
            write_table(source_path, SOURCE_FIELDS, rows)
            with self.assertRaisesRegex(plan.WorkflowError, "frozen package/source hash"):
                plan.apply_pre_ingest_correction_identity_patches(
                    root, self.approved(decisions[0])
                )

    def test_corrupted_snapshot_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            decisions, _ = self.reviews(root)
            path = root / ".onboarding/tennessee/integration-freeze.json"
            manifest = json.loads(path.read_text())
            manifest["source_game_semantic_guard"]["snapshot_sha256"] = "f" * 64
            path.write_text(json.dumps(manifest))
            with self.assertRaisesRegex(plan.WorkflowError, "hash mismatch"):
                plan.apply_pre_ingest_correction_identity_patches(
                    root, self.approved(decisions[0])
                )

    def test_source_semantic_drift_outside_authorized_delta_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            a = plan.read_csv(root / "data/evidence/game-assertions.csv")
            a[0]["raw_text"] = "changed literal evidence"
            write_table(root / "data/evidence/game-assertions.csv",
                        ingest_school.ASSERTION_FIELDS, a)
            with self.assertRaisesRegex(plan.WorkflowError, "unapproved assertion drift"):
                self.reviews(root)

    def test_no_correction_manifest_cannot_retarget_standard_ingestion(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            decisions, _ = self.reviews(root)
            (root / ".onboarding/tennessee/integration-freeze.json").unlink()
            self.assertEqual(self.reviews(root)[0], [])
            with self.assertRaisesRegex(plan.WorkflowError, "verified correction freeze"):
                plan.apply_pre_ingest_correction_identity_patches(
                    root, self.approved(decisions[0])
                )

    def test_disposable_copy_preserves_exact_scope_and_rejects_tampering(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "original"
            copy = Path(temp) / "disposable"
            self.fixture(root)
            decisions, _ = self.reviews(root)
            onboard_school.copy_repository(root, copy, school_key="tennessee")
            self.assertEqual(
                (root / ".onboarding/tennessee/integration-freeze.json").read_bytes(),
                (copy / ".onboarding/tennessee/integration-freeze.json").read_bytes(),
            )
            plan.apply_pre_ingest_correction_identity_patches(
                copy, self.approved(decisions[0])
            )
            self.assertEqual(
                plan.read_csv(copy / "data/canonical/games.csv")[0]["team_a_key"],
                "georgetown-ky",
            )
            self.assertEqual(
                plan.read_csv(root / "data/canonical/games.csv")[0]["team_a_key"],
                "georgetown",
            )
            target = Path(temp) / "rejected"
            manifest_path = root / ".onboarding/tennessee/integration-freeze.json"
            payload = json.loads(manifest_path.read_text())
            payload["package_member_sha256"]["source-games.csv"] = "f" * 64
            manifest_path.write_text(json.dumps(payload))
            with self.assertRaises(onboard_school.WorkflowError):
                onboard_school.copy_repository(root, target, school_key="tennessee")

    def test_seal_rejects_unreviewed_canonical_identity_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            decisions, _ = self.reviews(root)
            item = decisions[0]
            planned = {
                "school_key": "tennessee",
                "decisions": [item],
                "blockers": [],
                "input_fingerprint": {"sha256": "same"},
            }
            plan_path, review_path = root / "plan.json", root / "review.csv"
            plan_path.write_text(json.dumps(planned))
            with review_path.open("w", newline="") as stream:
                writer = csv.DictWriter(stream, fieldnames=plan.REVIEW_COLUMNS)
                writer.writeheader()
                writer.writerow({
                    **{k: item.get(k, "") for k in plan.REVIEW_COLUMNS},
                    "decision": plan.CORRECTION_IDENTITY_ACTION,
                    "resolution_basis": "Owner-authorized historical correction",
                    "canonical_patch_json": '{"team_a_key":"unreviewed"}',
                    "source_patch_json": "{}",
                })
            with patch.object(plan, "input_fingerprint", return_value={"sha256": "same"}):
                with self.assertRaisesRegex(plan.WorkflowError, "without field patches"):
                    plan.approve_plan(root, plan_path, review_path, "Owner")


if __name__ == "__main__":
    unittest.main()
