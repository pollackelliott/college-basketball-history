"""Regressions for Stage 2 confident many-to-one canonical identity collisions."""

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import implementation_stage2  # noqa: E402
import ingest_school  # noqa: E402
import onboarding_hardening  # noqa: E402
import onboarding_plan  # noqa: E402


SOURCE_FIELDS = [
    "source_game_id", "source_program_key", "season_label", "game_date",
    "source_opponent_label", "normalized_opponent_key", "normalized_opponent_name",
    "team_score", "opponent_score", "played_result", "overtime_periods",
    "source_site_candidate", "curated_site_type", "source_venue_name",
    "curated_venue_name", "city", "state", "event_or_tournament", "source_round",
    "curated_game_type", "curated_postseason_round", "source_page", "raw_text",
    "normalization_status", "administrative_status", "administrative_note", "notes",
]
CANONICAL_FIELDS = [
    "canonical_game_id", "season_label", "game_date", "date_precision",
    "team_a_key", "team_b_key", "team_a_score", "team_b_score",
    "result_winner_team_key", "overtime_periods", "site_type",
    "designated_home_team_key", "venue_key", "venue_id", "site_city",
    "site_state", "game_type", "postseason_round", "administrative_status",
    "administrative_note", "canonical_status", "notes",
]
ASSERTION_FIELDS = [
    "canonical_game_id", "source_program_key", "source_game_id", "season_label",
    "game_date", "normalized_opponent_key", "normalized_opponent_name",
    "team_score", "opponent_score", "played_result", "overtime_periods",
    "curated_site_type", "curated_game_type", "curated_postseason_round",
]
VENUE_FIELDS = [
    "source_program_key", "venue_key", "venue_id", "canonical_name", "aliases",
    "city", "state", "venue_type", "known_opened", "known_closed",
    "venue_date_precision", "games_currently_assigned", "first_assigned_game",
    "last_assigned_game", "relationship_type", "relationship_start",
    "relationship_end", "relationship_date_precision", "site_rule",
    "source_basis", "notes",
]


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_a():
    return {
        "source_game_id": "EXAMPLE-2013-14-030",
        "source_program_key": "example-school",
        "season_label": "2013-2014",
        "game_date": "",
        "source_opponent_label": "Example Opponent",
        "normalized_opponent_key": "example-opponent",
        "normalized_opponent_name": "Example Opponent",
        "team_score": "50",
        "opponent_score": "56",
        "played_result": "L",
        "overtime_periods": "0",
        "source_site_candidate": "HOME",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "source_venue_name": "",
        "curated_venue_name": "",
        "city": "",
        "state": "",
        "event_or_tournament": "",
        "source_round": "",
        "curated_game_type": "REGULAR_SEASON",
        "curated_postseason_round": "",
        "source_page": "fixture",
        "raw_text": "Mar. 6 Example Opponent ... L 50-56",
        "normalization_status": "RESEARCH_ACCEPTED",
        "administrative_status": "",
        "administrative_note": "",
        "notes": "",
    }


def source_b(*, review_only=False):
    return {
        "source_game_id": "EXAMPLE-2013-14-033",
        "source_program_key": "example-school",
        "season_label": "2013-2014",
        "game_date": "" if review_only else "2014-03-14",
        "source_opponent_label": "Example Opponent",
        "normalized_opponent_key": "example-opponent",
        "normalized_opponent_name": "Example Opponent",
        "team_score": "53",
        "opponent_score": "71",
        "played_result": "L",
        "overtime_periods": "0",
        "source_site_candidate": "NEUTRAL",
        "curated_site_type": "NEUTRAL",
        "source_venue_name": "",
        "curated_venue_name": "",
        "city": "",
        "state": "",
        "event_or_tournament": "Conference Tournament",
        "source_round": "",
        "curated_game_type": "CONFERENCE_TOURNAMENT",
        "curated_postseason_round": "",
        "source_page": "fixture",
        "raw_text": "Mar. 14 vs. Example Opponent ... L 53-71",
        "normalization_status": "RESEARCH_ACCEPTED",
        "administrative_status": "",
        "administrative_note": "",
        "notes": "",
    }


def hybrid_canonical():
    # Canonical orientation is example-opponent (team A) vs example-school (team B).
    return {
        "canonical_game_id": "CBBG-TEST0001",
        "season_label": "2013-2014",
        "game_date": "2014-03-14",
        "date_precision": "EXACT",
        "team_a_key": "example-opponent",
        "team_b_key": "example-school",
        "team_a_score": "56",
        "team_b_score": "50",
        "result_winner_team_key": "example-opponent",
        "overtime_periods": "0",
        "site_type": "NEUTRAL",
        "designated_home_team_key": "",
        "venue_key": "",
        "venue_id": "",
        "site_city": "",
        "site_state": "",
        "game_type": "CONFERENCE_TOURNAMENT",
        "postseason_round": "",
        "administrative_status": "",
        "administrative_note": "",
        "canonical_status": "ACTIVE",
        "notes": "",
    }


class ConfidentCanonicalCollisionTests(unittest.TestCase):
    def make_repo(self, *, review_second=False, assertions=None):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        repo = Path(temporary.name)
        school = repo / "schools/example-school"

        rows = [source_a(), source_b(review_only=review_second)]
        write_csv(school / "source-games.csv", SOURCE_FIELDS, rows)
        write_csv(school / "venues.csv", VENUE_FIELDS, [])
        write_csv(repo / "data/canonical/games.csv", CANONICAL_FIELDS, [hybrid_canonical()])
        write_csv(
            repo / "data/evidence/game-assertions.csv",
            ASSERTION_FIELDS,
            assertions or [],
        )
        write_csv(
            repo / "data/reconciliation/discrepancies.csv",
            ["canonical_game_id", "field_name", "source_a_program_key"],
            [],
        )
        write_csv(
            repo / "data/reference/programs.csv",
            [
                "program_key", "program_name", "display_name",
                "public_page_enabled", "history_start_season",
                "history_scope_intervals",
            ],
            [
                {
                    "program_key": "example-school",
                    "program_name": "Example School",
                    "display_name": "Example School",
                    "public_page_enabled": "Yes",
                    "history_start_season": "1900-1901",
                    "history_scope_intervals": "",
                },
                {
                    "program_key": "example-opponent",
                    "program_name": "Example Opponent",
                    "display_name": "Example Opponent",
                    "public_page_enabled": "No",
                    "history_start_season": "1900-1901",
                    "history_scope_intervals": "",
                },
            ],
        )
        write_csv(
            repo / "data/reference/program-accomplishments.csv",
            [
                "program_key", "conference_regular_season_championships",
                "conference_tournament_championships",
                "ncaa_tournament_appearances", "final_four_appearances",
                "national_championships", "best_finish_key", "best_finish_year",
                "verification_status", "verification_basis",
                "canonical_crosscheck_status", "notes",
            ],
            [{
                "program_key": "example-school",
                "conference_regular_season_championships": "0",
                "conference_tournament_championships": "0",
                "ncaa_tournament_appearances": "0",
                "final_four_appearances": "0",
                "national_championships": "0",
                "best_finish_key": "",
                "best_finish_year": "",
                "verification_status": "VERIFIED",
                "verification_basis": "fixture",
                "canonical_crosscheck_status": "MATCH",
                "notes": "",
            }],
        )
        return repo, rows

    def build(self, repo):
        package = {
            "errors": [],
            "warnings": [],
            "counts": {"source_games": 2},
            "source_consistency_issues": [],
        }
        derived = {
            "ncaa_tournament_appearances": 0,
            "final_four_appearances": 0,
            "national_championships": 0,
            "best_finish_key": "",
            "best_finish_year": None,
        }
        with (
            patch.object(onboarding_plan, "validate_package", return_value=package),
            patch.object(onboarding_plan, "source_location_preflight", return_value=([], [])),
            patch.object(onboarding_plan, "_source_assertion_sync_issues", return_value=([], [])),
            patch.object(onboarding_plan, "load_global_venue_reference", return_value=({}, {}, {})),
            patch.object(ingest_school, "load_venue_metadata_map_with_name_periods", return_value={}),
            patch.object(onboarding_plan, "frozen_venue_split_authority", return_value={}),
            patch.object(onboarding_plan, "frozen_owner_final_date_directives", return_value={}),
            patch.object(onboarding_plan, "_planned_venue_geography_errors", return_value=[]),
            patch.object(onboarding_plan, "_planned_ncaa_safety_errors", return_value=[]),
            patch.object(ingest_school, "canonical_enrichment_candidates", return_value=[]),
            patch.object(onboarding_plan, "_post_publication_identity_review_decisions", return_value=([], {})),
            patch.object(onboarding_plan, "_post_publication_site_review_decisions", return_value=[]),
            patch.object(onboarding_plan, "_canonical_site_patch_review_decisions", return_value=[]),
            patch.object(onboarding_plan, "_accomplishment_conflicts", return_value=(derived, [])),
            patch.object(onboarding_plan, "_discover_reciprocal_only_site_gap_provenance", return_value={}),
            patch.object(onboarding_plan, "input_fingerprint", return_value={"sha256": "fixture"}),
        ):
            return onboarding_plan.build_plan(repo, "example-school")

    def identity_rows(self, plan):
        return {
            row["source_game_id"]: row
            for row in plan["decisions"]
            if row.get("category") == "identity"
        }

    def conditional_rows(self, plan, source_id):
        return [
            row for row in plan["decisions"]
            if row.get("category") == "conditional_discrepancy"
            and row.get("source_game_id") == source_id
        ]

    def seal_map(self, repo, plan, identities, *, canonical_patch=None):
        out = repo / "review"
        paths = onboarding_plan.write_preflight_artifacts(plan, out)
        map_path = out / "map.json"
        decision_map = {
            "identity": identities,
            "defaults": {
                "selected_conditional": "USE_SOURCE",
                "discrepancy": "KEEP_CANONICAL",
                "basis": "Fixture owner-reviewed reconciliation.",
                "identity_basis": "Fixture owner-reviewed identity split.",
            },
        }
        if canonical_patch:
            decision_map["canonical_patch_by_decision"] = canonical_patch
        map_path.write_text(json.dumps(decision_map), encoding="utf-8")
        onboarding_hardening.fill_review_from_map(paths["review"], map_path)
        return onboarding_plan.approve_plan(
            repo,
            paths["plan"],
            paths["review"],
            "fixture-owner",
            approved_at="2026-01-01T00:00:00+00:00",
        )[0]

    def test_actual_planner_converts_confident_collision_to_coupled_identity_review(self):
        repo, _ = self.make_repo()
        source_bytes = (repo / "schools/example-school/source-games.csv").read_bytes()
        plan = self.build(repo)

        self.assertEqual(plan["blockers"], [])
        self.assertEqual(plan["summary"]["confident_collision_groups"], 1)
        self.assertEqual(plan["summary"]["confident_collision_source_rows"], 2)
        self.assertEqual(plan["summary"]["existing_game_matches"], 0)
        self.assertEqual(plan["summary"]["identity_review_required"], 2)
        self.assertEqual(len(plan["identity_collision_groups"]), 1)

        identities = self.identity_rows(plan)
        self.assertEqual(set(identities), {
            "EXAMPLE-2013-14-030",
            "EXAMPLE-2013-14-033",
        })
        for row in identities.values():
            self.assertEqual(
                row["allowed_actions"],
                ["MATCH_CANONICAL:CBBG-TEST0001", "FORCE_NEW"],
            )
            self.assertEqual(
                row["confident_collision_canonical_game_id"],
                "CBBG-TEST0001",
            )
            self.assertIn("hybridized", row["relevant_evidence"])

        a_fields = {row["field_name"] for row in self.conditional_rows(
            plan, "EXAMPLE-2013-14-030"
        )}
        b_fields = {row["field_name"] for row in self.conditional_rows(
            plan, "EXAMPLE-2013-14-033"
        )}
        self.assertEqual(a_fields, {"site_type", "game_type"})
        self.assertEqual(b_fields, {"score"})
        self.assertEqual(
            (repo / "schools/example-school/source-games.csv").read_bytes(),
            source_bytes,
        )

        census = implementation_stage2._capability_census(plan)
        represented = [
            row for row in census["topology_groups"]
            if row["topology"] == "confident_many_to_one_canonical_identity_collision"
        ]
        self.assertEqual(len(represented), 1)
        self.assertEqual(represented[0]["classification"], "REPRESENTED_BY_COUPLED_IDENTITY_REVIEW")

    def test_map_contract_rejects_double_match_and_zero_match(self):
        repo, _ = self.make_repo()
        plan = self.build(repo)
        out = repo / "invalid-review"
        paths = onboarding_plan.write_preflight_artifacts(plan, out)

        double_map = out / "double.json"
        double_map.write_text(json.dumps({
            "identity": {
                "EXAMPLE-2013-14-030": "MATCH_CANONICAL:CBBG-TEST0001",
                "EXAMPLE-2013-14-033": "MATCH_CANONICAL:CBBG-TEST0001",
            },
            "defaults": {
                "selected_conditional": "KEEP_CANONICAL",
                "basis": "fixture",
                "identity_basis": "fixture",
            },
        }), encoding="utf-8")
        with self.assertRaisesRegex(onboarding_plan.WorkflowError, "same canonical identity"):
            onboarding_hardening.fill_review_from_map(paths["review"], double_map)

        zero_map = out / "zero.json"
        zero_map.write_text(json.dumps({
            "identity": {
                "EXAMPLE-2013-14-030": "FORCE_NEW",
                "EXAMPLE-2013-14-033": "FORCE_NEW",
            },
            "defaults": {
                "selected_conditional": "KEEP_CANONICAL",
                "basis": "fixture",
                "identity_basis": "fixture",
            },
        }), encoding="utf-8")
        onboarding_hardening.fill_review_from_map(paths["review"], zero_map)
        with self.assertRaisesRegex(onboarding_plan.WorkflowError, "requires exactly 1 target match"):
            onboarding_plan.approve_plan(
                repo, paths["plan"], paths["review"], "fixture-owner"
            )

    def test_both_split_orientations_are_sealable_and_force_new_is_collision_bound(self):
        for retain_source in ("EXAMPLE-2013-14-030", "EXAMPLE-2013-14-033"):
            with self.subTest(retain_source=retain_source):
                repo, _ = self.make_repo()
                plan = self.build(repo)
                force_source = (
                    "EXAMPLE-2013-14-033"
                    if retain_source == "EXAMPLE-2013-14-030"
                    else "EXAMPLE-2013-14-030"
                )
                identities = {
                    retain_source: "MATCH_CANONICAL:CBBG-TEST0001",
                    force_source: "FORCE_NEW",
                }
                canonical_patch = {}
                if retain_source == "EXAMPLE-2013-14-030":
                    game_type_row = next(
                        row for row in self.conditional_rows(plan, retain_source)
                        if row["field_name"] == "game_type"
                    )
                    # Source A has no exact structured date. If A retains the hybrid
                    # canonical, clearing the sibling-derived exact date is supported;
                    # inventing March 6 as an exact date is not.
                    canonical_patch[game_type_row["decision_id"]] = {
                        "game_date": "",
                        "date_precision": "",
                    }

                approved = self.seal_map(
                    repo, plan, identities, canonical_patch=canonical_patch
                )
                authority = (
                    ingest_school.confident_collision_force_new_authority_from_sealed_plan(
                        approved
                    )
                )
                self.assertEqual(authority[force_source], "CBBG-TEST0001")

                sources = {
                    row["source_game_id"]: row
                    for row in (source_a(), source_b())
                }
                canonical = hybrid_canonical()
                candidates = [canonical]
                status, _, method = ingest_school.resolve_sealed_identity_decision(
                    sources[force_source],
                    "FORCE_NEW",
                    candidates,
                    {"CBBG-TEST0001": canonical},
                    authority[force_source],
                )
                self.assertEqual(status, ingest_school.NEW_GAME)
                self.assertEqual(
                    method,
                    "SEALED_OWNER_FORCE_NEW_CONFIDENT_CANONICAL_COLLISION",
                )

                # Without the sealed collision binding, ordinary FORCE_NEW remains
                # fail-closed against a confident normal matcher.
                status, _, method = ingest_school.resolve_sealed_identity_decision(
                    sources[force_source],
                    "FORCE_NEW",
                    candidates,
                    {"CBBG-TEST0001": canonical},
                )
                self.assertEqual(status, ingest_school.REVIEW)
                self.assertIn("CONFLICTS_WITH", method)

                retained = dict(canonical)
                for item in approved["decisions"]:
                    if (
                        item.get("category") == "discrepancy"
                        and item.get("source_game_id") == retain_source
                        and item.get("decision") == "USE_SOURCE"
                    ):
                        onboarding_plan.set_canonical_field(
                            retained,
                            item["field_name"],
                            item["source_value"],
                        )
                        onboarding_plan._apply_canonical_patch(
                            retained,
                            item.get("canonical_patch", {}),
                        )

                new_game = ingest_school.build_new_canonical(
                    sources[force_source],
                    "CBBG-NEW0001",
                    {},
                    {},
                )
                if retain_source == "EXAMPLE-2013-14-030":
                    self.assertEqual(retained["game_date"], "")
                    self.assertEqual(retained["date_precision"], "")
                    self.assertEqual(retained["game_type"], "REGULAR_SEASON")
                    self.assertEqual(retained["site_type"], "TEAM_B_HOME")
                    self.assertEqual(new_game["game_date"], "2014-03-14")
                    self.assertEqual(new_game["game_type"], "CONFERENCE_TOURNAMENT")
                    self.assertEqual(new_game["team_a_score"], "71")
                    self.assertEqual(new_game["team_b_score"], "53")
                else:
                    self.assertEqual(retained["game_date"], "2014-03-14")
                    self.assertEqual(retained["game_type"], "CONFERENCE_TOURNAMENT")
                    self.assertEqual(retained["team_a_score"], "71")
                    self.assertEqual(retained["team_b_score"], "53")
                    self.assertEqual(new_game["game_date"], "")
                    self.assertEqual(new_game["game_type"], "REGULAR_SEASON")
                    self.assertEqual(new_game["site_type"], "TEAM_B_HOME")

                # Raw evidence is never rewritten by identity splitting.
                self.assertIn("Mar.", sources[force_source]["raw_text"])

    def test_existing_review_population_gets_cardinality_without_duplicate_identity(self):
        repo, _ = self.make_repo(review_second=True)
        plan = self.build(repo)
        identities = self.identity_rows(plan)

        self.assertEqual(plan["identity_collision_groups"], [])
        self.assertEqual(set(identities), {"EXAMPLE-2013-14-033"})
        self.assertEqual(
            identities["EXAMPLE-2013-14-033"]["allowed_actions"],
            ["MATCH_CANONICAL:CBBG-TEST0001", "FORCE_NEW"],
        )
        constraints = plan["identity_cardinality_constraints"]
        self.assertEqual(len(constraints), 1)
        self.assertEqual(
            constraints[0]["fixed_confident_source_game_ids"],
            ["EXAMPLE-2013-14-030"],
        )
        self.assertEqual(
            constraints[0]["review_source_game_ids"],
            ["EXAMPLE-2013-14-033"],
        )

        # The already-confident source reserves the canonical identity, so the
        # existing REVIEW row remains available but cannot legally duplicate it.
        out = repo / "review-existing"
        paths = onboarding_plan.write_preflight_artifacts(plan, out)
        map_path = out / "map.json"
        map_path.write_text(json.dumps({
            "identity": {
                "EXAMPLE-2013-14-033": "MATCH_CANONICAL:CBBG-TEST0001",
            },
            "defaults": {
                "selected_conditional": "KEEP_CANONICAL",
                "basis": "fixture",
                "identity_basis": "fixture",
            },
        }), encoding="utf-8")
        onboarding_hardening.fill_review_from_map(paths["review"], map_path)
        with self.assertRaisesRegex(onboarding_plan.WorkflowError, "observed 2"):
            onboarding_plan.approve_plan(
                repo, paths["plan"], paths["review"], "fixture-owner"
            )

    def test_existing_source_assertions_are_durable_duplicate_authority(self):
        assertions = []
        for source in (source_a(), source_b()):
            assertions.append({
                "canonical_game_id": "CBBG-TEST0001",
                "source_program_key": "example-school",
                "source_game_id": source["source_game_id"],
                "season_label": source["season_label"],
                "game_date": source["game_date"],
                "normalized_opponent_key": source["normalized_opponent_key"],
                "normalized_opponent_name": source["normalized_opponent_name"],
                "team_score": source["team_score"],
                "opponent_score": source["opponent_score"],
                "played_result": source["played_result"],
                "overtime_periods": source["overtime_periods"],
                "curated_site_type": source["curated_site_type"],
                "curated_game_type": source["curated_game_type"],
                "curated_postseason_round": source["curated_postseason_round"],
            })
        repo, _ = self.make_repo(assertions=assertions)
        plan = self.build(repo)

        self.assertEqual(plan["blockers"], [])
        self.assertEqual(plan["identity_collision_groups"], [])
        self.assertEqual(self.identity_rows(plan), {})
        self.assertEqual(plan["summary"]["existing_game_matches"], 2)


if __name__ == "__main__":
    unittest.main()
