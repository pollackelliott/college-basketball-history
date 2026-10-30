import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    _accomplishment_conflicts,
    _accomplishment_crosscheck_game,
    _accomplishment_round_conflict_is_reviewable,
    _project_accomplishment_games_with_existing_seasons,
    _ncaa_round_patch_decisions,
)
from program_history import (  # noqa: E402
    NCAA_NON_APPEARANCE_QUALIFIER_MARKER,
    derive_ncaa_accomplishments,
    ncaa_game_counts_as_appearance,
)



def ncaa_game(
    game_id,
    season,
    game_date,
    round_name,
    *,
    opponent="opponent",
    winner="opponent",
):
    return {
        "canonical_game_id": game_id,
        "season_label": season,
        "game_date": game_date,
        "date_precision": "EXACT",
        "team_a_key": "usc",
        "team_b_key": opponent,
        "team_a_score": "60",
        "team_b_score": "70",
        "result_winner_team_key": winner,
        "overtime_periods": "0",
        "site_type": "NEUTRAL",
        "designated_home_team_key": "",
        "venue_key": "",
        "venue_id": "",
        "site_city": "",
        "site_state": "",
        "game_type": "NCAA_TOURNAMENT",
        "postseason_round": round_name,
        "administrative_status": "",
        "administrative_note": "",
        "canonical_status": "PROVISIONAL",
        "notes": "",
    }


class HistoricalRoundAccomplishmentCrosscheckTests(unittest.TestCase):
    def setUp(self):
        self.program = {
            "program_key": "usc",
            "history_start_season": "1906-1907",
        }
        self.reference = {
            "ncaa_tournament_appearances": "2",
            "final_four_appearances": "1",
            "national_championships": "0",
            "best_finish_key": "FINAL_FOUR",
            "best_finish_year": "1954",
        }
        self.games = [
            ncaa_game(
                "CBBG-FF",
                "1953-1954",
                "1954-03-19",
                "Final Four",
            ),
            # Deliberately blank: an old tournament format with no honest
            # controlled-vocabulary equivalent.
            ncaa_game(
                "CBBG-OLD-FORMAT",
                "1959-1960",
                "1960-03-07",
                "",
            ),
        ]

    def test_research_accepted_nonbracket_qualifier_does_not_count_as_appearance(self):
        source = {
            "source_program_key": "usc",
            "source_game_id": "USC-1947-QUALIFIER",
            "season_label": "1946-1947",
            "game_date": "1947-03-18",
            "normalized_opponent_key": "oklahoma",
            "team_score": "41",
            "opponent_score": "47",
            "played_result": "L",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "Kansas City",
            "state": "MO",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "",
            "normalization_status": "RESEARCH_ACCEPTED",
            "notes": (
                "Stage 6 NCAA-round audit: this was a district playoff/qualifier "
                "rather than a national-bracket round; standardized NCAA round "
                "intentionally remains blank."
            ),
        }

        predicted = _accomplishment_crosscheck_game(
            source,
            ingest_school.NEW_GAME,
            "",
            {},
            {},
            {},
            "PREFLIGHT-USC-1947-QUALIFIER",
        )

        self.assertIn(
            NCAA_NON_APPEARANCE_QUALIFIER_MARKER,
            predicted["notes"],
        )
        self.assertFalse(ncaa_game_counts_as_appearance(predicted))

        derived = derive_ncaa_accomplishments(
            [predicted],
            "usc",
            "1906-1907",
        )
        self.assertEqual(derived["ncaa_tournament_appearances"], 0)
        self.assertEqual(derived["ncaa_nonappearance_qualifier_game_count"], 1)
        self.assertEqual(derived["incomplete_reasons"], [])

    def test_nonbracket_qualifier_does_not_inherit_reciprocal_round(self):
        source = {
            "source_program_key": "usc",
            "source_game_id": "USC-1947-QUALIFIER",
            "season_label": "1946-1947",
            "game_date": "1947-03-18",
            "normalized_opponent_key": "oklahoma",
            "team_score": "41",
            "opponent_score": "47",
            "played_result": "L",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "Kansas City",
            "state": "MO",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "",
            "normalization_status": "RESEARCH_ACCEPTED",
            "notes": (
                "district playoff/qualifier rather than a national-bracket round"
            ),
        }
        canonical = ncaa_game(
            "CBBG-QUALIFIER-CONFLICT",
            "1946-1947",
            "1947-03-18",
            "R64",
            opponent="oklahoma",
            winner="oklahoma",
        )

        predicted = _accomplishment_crosscheck_game(
            source,
            ingest_school.CONFIDENT,
            "CBBG-QUALIFIER-CONFLICT",
            {"CBBG-QUALIFIER-CONFLICT": canonical},
            {},
            {},
            "PREFLIGHT-USC-1947-QUALIFIER",
        )

        self.assertEqual(predicted["postseason_round"], "")
        self.assertFalse(ncaa_game_counts_as_appearance(predicted))

    def test_confident_blank_source_round_inherits_known_canonical_round(self):
        source = {
            "source_program_key": "usc",
            "source_game_id": "USC-2010-FF",
            "season_label": "2009-2010",
            "game_date": "2010-04-03",
            "normalized_opponent_key": "duke",
            "team_score": "57",
            "opponent_score": "78",
            "played_result": "L",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "Indianapolis",
            "state": "IN",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "",
        }
        canonical = ncaa_game(
            "CBBG-2010-FF",
            "2009-2010",
            "2010-04-03",
            "Final Four",
            opponent="duke",
            winner="duke",
        )

        predicted = _accomplishment_crosscheck_game(
            source,
            ingest_school.CONFIDENT,
            "CBBG-2010-FF",
            {"CBBG-2010-FF": canonical},
            {},
            {},
            "PREFLIGHT-USC-2010-FF",
        )

        self.assertEqual(predicted["postseason_round"], "Final Four")
        self.assertEqual(source["curated_postseason_round"], "")

    def test_nonblank_source_round_is_not_overwritten_by_canonical_fallback(self):
        source = {
            "source_program_key": "usc",
            "source_game_id": "USC-ROUND-CONFLICT",
            "season_label": "2009-2010",
            "game_date": "2010-03-21",
            "normalized_opponent_key": "duke",
            "team_score": "70",
            "opponent_score": "68",
            "played_result": "W",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "Indianapolis",
            "state": "IN",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "R32",
        }
        canonical = ncaa_game(
            "CBBG-ROUND-CONFLICT",
            "2009-2010",
            "2010-03-21",
            "Final Four",
            opponent="duke",
            winner="usc",
        )

        predicted = _accomplishment_crosscheck_game(
            source,
            ingest_school.CONFIDENT,
            "CBBG-ROUND-CONFLICT",
            {"CBBG-ROUND-CONFLICT": canonical},
            {},
            {},
            "PREFLIGHT-USC-ROUND-CONFLICT",
        )

        self.assertEqual(predicted["postseason_round"], "R32")

    def test_honest_blank_round_does_not_block_matching_aggregates(self):
        derived, conflicts = _accomplishment_conflicts(
            self.program,
            self.reference,
            self.games,
        )

        self.assertEqual(
            derived["ncaa_tournament_appearances"],
            2,
        )
        self.assertIn(
            "1959-1960 has no resolved NCAA round",
            derived["incomplete_reasons"],
        )
        self.assertEqual(conflicts, [])

    def test_deeper_reference_with_blank_round_candidate_is_gate_reviewable(self):
        reference = dict(self.reference)
        reference["final_four_appearances"] = "2"
        reference["best_finish_key"] = "NATIONAL_RUNNER_UP"
        reference["best_finish_year"] = "1960"
        derived, _ = _accomplishment_conflicts(
            self.program,
            reference,
            self.games,
        )
        candidates = [
            {
                "source": {
                    "source_game_id": "USC-1960-TITLE",
                    "season_label": "1959-1960",
                    "game_date": "1960-03-07",
                    "normalized_opponent_key": "opponent",
                    "played_result": "L",
                },
                "canonical_game_id": "",
                "canonical_game_date": "",
                "calendar_year": 1960,
            }
        ]

        self.assertTrue(
            _accomplishment_round_conflict_is_reviewable(
                reference,
                derived,
                candidates,
            )
        )
        decisions = _ncaa_round_patch_decisions("usc", candidates)
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["category"], "ncaa_round_patch")
        self.assertIn("APPLY_NCAA_ROUND_PATCH", decisions[0]["allowed_actions"])


    def test_established_runner_up_allows_later_final_four_review(self):
        reference = {
            "ncaa_tournament_appearances": "2",
            "final_four_appearances": "2",
            "national_championships": "0",
            "best_finish_key": "NATIONAL_RUNNER_UP",
            "best_finish_year": "1952",
        }
        derived = {
            "ncaa_tournament_appearances": 2,
            "final_four_appearances": 1,
            "national_championships": 0,
            "best_finish_key": "NATIONAL_RUNNER_UP",
            "best_finish_year": 1952,
        }
        candidates = [{
            "source": {
                "source_game_id": "1985-SEMIFINAL",
                "season_label": "1984-1985",
                "played_result": "L",
            },
            "calendar_year": 1985,
        }]
        self.assertTrue(
            _accomplishment_round_conflict_is_reviewable(
                reference, derived, candidates
            )
        )

        # A newly claimed runner-up finish still requires evidence
        # from the year to which that claim refers.
        derived["best_finish_key"] = "FINAL_FOUR"
        self.assertFalse(
            _accomplishment_round_conflict_is_reviewable(
                reference, derived, candidates
            )
        )

    def test_round_gap_requires_enough_distinct_candidate_seasons(self):
        reference = dict(self.reference)
        reference["final_four_appearances"] = "3"
        reference["best_finish_key"] = "FINAL_FOUR"
        reference["best_finish_year"] = "1954"
        derived, _ = _accomplishment_conflicts(
            self.program,
            self.reference,
            self.games,
        )
        candidates = [
            {
                "source": {
                    "source_game_id": "USC-1960-ROUND",
                    "season_label": "1959-1960",
                    "game_date": "1960-03-07",
                    "normalized_opponent_key": "opponent",
                    "played_result": "L",
                },
                "calendar_year": 1960,
            }
        ]

        self.assertFalse(
            _accomplishment_round_conflict_is_reviewable(
                reference,
                derived,
                candidates,
            )
        )

    def test_round_gap_cannot_hide_shallower_reference(self):
        reference = dict(self.reference)
        reference["final_four_appearances"] = "0"
        derived, _ = _accomplishment_conflicts(
            self.program,
            self.reference,
            self.games,
        )
        candidates = [
            {
                "source": {
                    "source_game_id": "USC-1960-ROUND",
                    "season_label": "1959-1960",
                    "game_date": "1960-03-07",
                    "normalized_opponent_key": "opponent",
                },
                "calendar_year": 1960,
            }
        ]

        self.assertFalse(
            _accomplishment_round_conflict_is_reviewable(
                reference,
                derived,
                candidates,
            )
        )

    def test_blank_round_diagnostic_remains_when_aggregates_conflict(self):
        reference = dict(self.reference)
        reference["final_four_appearances"] = "2"

        _, conflicts = _accomplishment_conflicts(
            self.program,
            reference,
            self.games,
        )

        self.assertTrue(
            any(
                item.startswith("final_four_appearances:")
                for item in conflicts
            )
        )
        self.assertIn(
            "1959-1960 has no resolved NCAA round",
            conflicts,
        )


    def test_canonical_only_ncaa_season_reconciles_projected_appearance_count(self):
        # Target Research is a complete accepted ledger, but a previously
        # canonical NCAA appearance season may still have no target rows.
        source = [
            ncaa_game("SOURCE-1939", "1938-1939", "1939-03-18", ""),
            ncaa_game(
                "SOURCE-1985", "1984-1985", "1985-04-01", "",
                opponent="georgetown", winner="usc",
            ),
        ]
        previously_canonical = [
            ncaa_game("CAN-1939", "1938-1939", "1939-03-18", ""),
            ncaa_game("CAN-1985", "1984-1985", "1985-03-17", "R32"),
            ncaa_game(
                "CAN-1971", "1970-1971", "1971-03-27", "Championship",
                opponent="ucla", winner="ucla",
            ),
            ncaa_game(
                "CAN-2026", "2025-2026", "2026-03-20", "R64",
                opponent="opponent", winner="opponent",
            ),
        ]
        projected = _project_accomplishment_games_with_existing_seasons(
            self.program, source, previously_canonical,
        )
        self.assertEqual(
            [g["canonical_game_id"] for g in projected],
            ["SOURCE-1939", "SOURCE-1985", "CAN-1971", "CAN-2026"],
        )
        reference = {
            "ncaa_tournament_appearances": "4",
            "final_four_appearances": "3",
            "national_championships": "1",
            "best_finish_key": "NATIONAL_CHAMPION",
            "best_finish_year": "1985",
        }
        projected_derived, conflicts = _accomplishment_conflicts(
            self.program, reference, projected,
        )
        self.assertEqual(projected_derived["ncaa_tournament_appearances"], 4)
        self.assertEqual(projected_derived["final_four_appearances"], 1)
        self.assertEqual(projected_derived["national_championships"], 0)
        self.assertTrue(conflicts)

        candidates = [
            {
                "source": {
                    "source_game_id": "SOURCE-1939",
                    "season_label": "1938-1939",
                    "game_date": "1939-03-18",
                    "normalized_opponent_key": "ohio-state",
                    "played_result": "L",
                },
                "canonical_game_id": "CAN-1939",
                "canonical_game_date": "1939-03-18",
                "calendar_year": 1939,
            },
            {
                "source": {
                    "source_game_id": "SOURCE-1985",
                    "season_label": "1984-1985",
                    "game_date": "1985-04-01",
                    "normalized_opponent_key": "georgetown",
                    "played_result": "W",
                },
                # The new title game's ID is unknown before ingestion.
                "canonical_game_id": "",
                "canonical_game_date": "",
                "calendar_year": 1985,
            },
        ]
        self.assertTrue(
            _accomplishment_round_conflict_is_reviewable(
                reference, projected_derived, candidates,
            )
        )
        decisions = _ncaa_round_patch_decisions("usc", candidates)
        self.assertEqual(len(decisions), 2)
        self.assertEqual(decisions[0]["canonical_game_id"], "CAN-1939")
        self.assertEqual(decisions[1]["canonical_game_id"], "")
        self.assertEqual(
            {item["category"] for item in decisions},
            {"ncaa_round_patch"},
        )
        self.assertEqual(
            {item["decision"] for item in decisions}, {"PENDING"},
        )

        # Without the accepted supplemental appearances the original
        # source-only projection must still fail the guard.
        incomplete, _ = _accomplishment_conflicts(
            self.program, reference, source,
        )
        self.assertFalse(
            _accomplishment_round_conflict_is_reviewable(
                reference, incomplete, candidates,
            )
        )

    def test_projection_excludes_generic_postseason_and_other_programs(self):
        source = [
            ncaa_game("SOURCE-1954", "1953-1954", "1954-03-19", "Final Four"),
        ]
        duplicate_ncaa = ncaa_game(
            "CAN-1954-CHAMP", "1953-1954", "1954-04-01", "Championship",
            winner="usc",
        )
        generic_postseason = ncaa_game(
            "CAN-CROWN", "2025-2026", "2026-04-01", "Championship",
            winner="usc",
        )
        generic_postseason["game_type"] = "POSTSEASON"
        other_program = ncaa_game(
            "CAN-OTHER", "2024-2025", "2025-04-01", "Championship",
            winner="other",
        )
        other_program["team_a_key"] = "other"
        other_program["team_b_key"] = "second-other"
        projected = _project_accomplishment_games_with_existing_seasons(
            self.program, source,
            [duplicate_ncaa, generic_postseason, other_program],
        )
        self.assertEqual(
            [g["canonical_game_id"] for g in projected], ["SOURCE-1954"],
        )
        derived = _accomplishment_conflicts(
            self.program,
            {
                "ncaa_tournament_appearances": "1",
                "final_four_appearances": "1",
                "national_championships": "0",
                "best_finish_key": "FINAL_FOUR",
                "best_finish_year": "1954",
            },
            projected,
        )[0]
        self.assertEqual(derived["ncaa_tournament_appearances"], 1)
        self.assertEqual(derived["national_championships"], 0)

    def test_projection_does_not_infer_missing_round(self):
        source = [ncaa_game(
            "SOURCE-1960", "1959-1960", "1960-03-07", "",
        )]
        preexisting = [
            ncaa_game("CAN-1960", "1959-1960", "1960-03-07", "Championship"),
            ncaa_game("CAN-1961", "1960-1961", "1961-03-07", ""),
        ]
        projection = _project_accomplishment_games_with_existing_seasons(
            self.program, source, preexisting,
        )
        self.assertEqual(len(projection), 2)
        self.assertEqual(projection[0]["postseason_round"], "")
        self.assertEqual(projection[1]["postseason_round"], "")
        self.assertEqual(
            _accomplishment_conflicts(
                self.program, self.reference, projection,
            )[0]["national_championships"],
            0,
        )


if __name__ == "__main__":
    unittest.main()
