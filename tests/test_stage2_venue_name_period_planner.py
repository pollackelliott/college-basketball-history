"""Stage 2 planner regressions for reused venue-name period authority."""

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
import onboarding_plan  # noqa: E402
from location_safety import registry_fallback_marker  # noqa: E402


SCHOOL_VENUE_FIELDS = [
    "source_program_key", "venue_key", "venue_id", "canonical_name", "aliases",
    "city", "state", "venue_type", "known_opened", "known_closed",
    "venue_date_precision", "games_currently_assigned", "first_assigned_game",
    "last_assigned_game", "relationship_type", "relationship_start",
    "relationship_end", "relationship_date_precision", "site_rule",
    "source_basis", "notes",
]
GLOBAL_VENUE_FIELDS = [
    "venue_id", "venue_key", "display_name", "city", "state", "opened",
    "closed", "date_precision", "identity_status", "source_basis", "notes",
]
VENUE_NAME_FIELDS = [
    "venue_id", "venue_name", "normalized_name", "name_type", "valid_from",
    "valid_to", "date_precision", "source_basis", "notes",
]


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def school_venue(key, venue_id, *, name="Shared Arena", aliases=""):
    return {
        "source_program_key": "example-school",
        "venue_key": key,
        "venue_id": venue_id,
        "canonical_name": name,
        "aliases": aliases,
        "city": "Example City",
        "state": "EX",
        "venue_type": "arena",
        "known_opened": "",
        "known_closed": "",
        "venue_date_precision": "",
        "games_currently_assigned": "0",
        "first_assigned_game": "",
        "last_assigned_game": "",
        "relationship_type": "GAME_SITE",
        "relationship_start": "",
        "relationship_end": "",
        "relationship_date_precision": "",
        "site_rule": "fixture",
        "source_basis": "fixture",
        "notes": "",
    }


def global_venue(venue_id, key, opened, closed):
    return {
        "venue_id": venue_id,
        "venue_key": key,
        "display_name": "Shared Arena",
        "city": "Example City",
        "state": "EX",
        "opened": opened,
        "closed": closed,
        "date_precision": "YEAR",
        "identity_status": "VERIFIED",
        "source_basis": "fixture",
        "notes": "",
    }


def name_row(venue_id, name, valid_from, valid_to, name_type="PROJECT_DISPLAY"):
    return {
        "venue_id": venue_id,
        "venue_name": name,
        "normalized_name": ingest_school.re.sub(r"[^a-z0-9]+", "", name.casefold()),
        "name_type": name_type,
        "valid_from": valid_from,
        "valid_to": valid_to,
        "date_precision": "YEAR" if valid_from or valid_to else "",
        "source_basis": "fixture",
        "notes": "",
    }


class Stage2VenueNamePeriodPlannerTests(unittest.TestCase):
    def make_repo(self, *, include_old_period=True, include_new_period=True):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        repo = Path(temporary.name)
        school = repo / "schools/example-school"
        reference = repo / "data/reference"

        venue_rows = [
            school_venue("shared-arena-old", "VEN-OLD", aliases="Shared Alias"),
            school_venue("shared-arena-new", "VEN-NEW", aliases="Shared Alias"),
        ]
        write_csv(school / "venues.csv", SCHOOL_VENUE_FIELDS, venue_rows)

        global_rows = [
            global_venue("VEN-OLD", "shared-arena-old", "1955", ""),
            global_venue("VEN-NEW", "shared-arena-new", "1988", "2005"),
        ]
        write_csv(reference / "venues.csv", GLOBAL_VENUE_FIELDS, global_rows)

        name_rows = []
        name_rows.append(name_row(
            "VEN-OLD", "Shared Arena",
            "1955" if include_old_period else "",
            "1988" if include_old_period else "",
        ))
        name_rows.append(name_row(
            "VEN-NEW", "Shared Arena",
            "1988" if include_new_period else "",
            "2005" if include_new_period else "",
        ))
        name_rows.extend([
            name_row("VEN-OLD", "Shared Alias", "", "", "ALIAS"),
            name_row("VEN-NEW", "Shared Alias", "", "", "ALIAS"),
        ])
        write_csv(reference / "venue-names.csv", VENUE_NAME_FIELDS, name_rows)
        return repo, venue_rows

    def source(self, season="2000-2001", venue_name="Shared Arena"):
        return {
            "source_game_id": "EXAMPLE-2000-01-001",
            "source_program_key": "example-school",
            "season_label": season,
            "game_date": "",
            "source_opponent_label": "Example Opponent",
            "normalized_opponent_key": "example-opponent",
            "normalized_opponent_name": "Example Opponent",
            "team_score": "60",
            "opponent_score": "50",
            "played_result": "W",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "source_venue_name": venue_name,
            "curated_venue_name": venue_name,
            "city": "Example City",
            "state": "EX",
            "curated_game_type": "REGULAR_SEASON",
            "curated_postseason_round": "",
            "normalization_status": "RESEARCH_ACCEPTED",
            "raw_text": "Fixture source row",
            "notes": "",
        }

    def plan_fixture(self, repo: Path, source):
        school = repo / "schools/example-school"
        write_csv(school / "source-games.csv", list(source), [source])
        write_csv(
            repo / "data/canonical/games.csv",
            [
                "canonical_game_id", "season_label", "game_date", "team_a_key",
                "team_b_key", "team_a_score", "team_b_score",
                "result_winner_team_key", "overtime_periods", "site_type",
                "designated_home_team_key", "venue_key", "venue_id", "site_city",
                "site_state", "game_type", "postseason_round",
                "administrative_status", "administrative_note",
                "canonical_status", "notes",
            ],
            [],
        )
        write_csv(
            repo / "data/evidence/game-assertions.csv",
            ["canonical_game_id", "source_program_key", "source_game_id"],
            [],
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
                "national_championships", "best_finish_key",
                "best_finish_year", "verification_status",
                "verification_basis", "canonical_crosscheck_status", "notes",
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

        captured = []
        original_build = ingest_school.build_new_canonical

        def capture_build(*args, **kwargs):
            result = original_build(*args, **kwargs)
            captured.append(dict(result))
            return result

        package = {
            "errors": [],
            "warnings": [],
            "counts": {"source_games": 1},
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
            patch.object(onboarding_plan, "_source_assertion_sync_issues", return_value=([], [])),
            patch.object(onboarding_plan, "frozen_venue_split_authority", return_value={}),
            patch.object(onboarding_plan, "frozen_owner_final_date_directives", return_value={}),
            patch.object(onboarding_plan, "_post_publication_identity_review_decisions", return_value=([], {})),
            patch.object(onboarding_plan, "_post_publication_site_review_decisions", return_value=[]),
            patch.object(onboarding_plan, "_canonical_site_patch_review_decisions", return_value=[]),
            patch.object(onboarding_plan, "_accomplishment_conflicts", return_value=(derived, [])),
            patch.object(onboarding_plan, "_discover_reciprocal_only_site_gap_provenance", return_value={}),
            patch.object(onboarding_plan, "input_fingerprint", return_value={"sha256": "fixture"}),
            patch.object(ingest_school, "build_new_canonical", side_effect=capture_build),
        ):
            plan = onboarding_plan.build_plan(repo, "example-school")
        return plan, captured

    def test_permanent_stage2_planner_and_runtime_agree_on_later_building(self):
        repo, _ = self.make_repo()
        source = self.source()
        plan, captured = self.plan_fixture(repo, source)
        self.assertEqual(plan["blockers"], [])
        self.assertEqual(plan["summary"]["new_canonical_games"], 1)
        self.assertTrue(captured)
        self.assertTrue(all(row.get("venue_id") == "VEN-NEW" for row in captured), captured)

        globals_by_id, _, _ = onboarding_plan.load_global_venue_reference(repo)
        runtime_map = ingest_school.load_runtime_venue_metadata_map(
            repo,
            "example-school",
            repo / "schools/example-school/venues.csv",
            globals_by_id,
        )
        runtime = ingest_school.resolve_venue_metadata(source, runtime_map)
        self.assertEqual(runtime["venue_id"], "VEN-NEW")
        self.assertEqual(runtime["venue_key"], "shared-arena-new")

    def test_permanent_stage2_planner_transition_season_remains_fail_closed(self):
        repo, _ = self.make_repo()
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            self.plan_fixture(repo, self.source(season="1988-1989"))

    def test_permanent_stage2_planner_incomplete_period_authority_remains_fail_closed(self):
        repo, _ = self.make_repo(include_old_period=False)
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            self.plan_fixture(repo, self.source())

    def test_undated_aliases_do_not_become_disambiguating_authority(self):
        repo, _ = self.make_repo()
        globals_by_id, _, _ = onboarding_plan.load_global_venue_reference(repo)
        metadata = ingest_school.load_venue_metadata_map_with_name_periods(
            repo,
            repo / "schools/example-school/venues.csv",
            globals_by_id,
        )
        with self.assertRaisesRegex(ValueError, "available date/season evidence"):
            ingest_school.resolve_venue_metadata(self.source(venue_name="Shared Alias"), metadata)

    def test_registry_fallback_support_uses_same_name_period_semantics(self):
        repo, _ = self.make_repo()
        assertion = self.source()
        assertion["canonical_game_id"] = "CBBG-EXAMPLE"
        marker = registry_fallback_marker(
            "example-school",
            assertion["source_game_id"],
            "shared-arena-new",
            "NEUTRAL",
            ["venue_key", "venue_id", "site_city", "site_state"],
        )
        canonical = {
            "canonical_game_id": "CBBG-EXAMPLE",
            "site_type": "NEUTRAL",
            "venue_key": "shared-arena-new",
            "venue_id": "VEN-NEW",
            "site_city": "Example City",
            "site_state": "EX",
            "notes": marker,
        }
        retired = onboarding_plan._retire_invalid_registry_fallbacks_after_site_reconciliation(
            repo,
            canonical,
            {("example-school", assertion["source_game_id"]): [assertion]},
            {},
        )
        self.assertEqual(retired, 0)
        self.assertIn("VENUE_REGISTRY_FALLBACK", canonical["notes"])

    def test_single_candidate_venue_behavior_is_unchanged(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        repo = Path(temporary.name)
        venue_path = repo / "schools/example-school/venues.csv"
        write_csv(
            venue_path,
            SCHOOL_VENUE_FIELDS,
            [school_venue("solo-arena", "VEN-SOLO", name="Solo Arena")],
        )
        metadata = ingest_school.load_venue_metadata_map_with_name_periods(
            repo,
            venue_path,
            {
                "VEN-SOLO": {
                    "venue_id": "VEN-SOLO",
                    "city": "Example City",
                    "state": "EX",
                    "opened": "",
                    "closed": "",
                }
            },
        )
        resolved = ingest_school.resolve_venue_metadata(
            {
                "source_game_id": "SOLO",
                "season_label": "2000-2001",
                "game_date": "",
                "curated_venue_name": "Solo Arena",
                "city": "Elsewhere",
                "state": "ZZ",
            },
            metadata,
        )
        self.assertEqual(resolved["venue_id"], "VEN-SOLO")


if __name__ == "__main__":
    unittest.main()
