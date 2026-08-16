import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school


def source(game_date, team_score, opponent_score):
    return {
        "source_program_key": "alabama",
        "normalized_opponent_key": "florida",
        "season_label": "2023-2024",
        "game_date": game_date,
        "team_score": str(team_score),
        "opponent_score": str(opponent_score),
        "curated_site_type": "UNKNOWN",
        "curated_venue_name": "",
        "city": "",
        "state": "",
        "source_game_id": "TEST",
    }


def candidate(game_id, game_date, alabama_score, florida_score, date_precision="EXACT"):
    return {
        "canonical_game_id": game_id,
        "season_label": "2023-2024",
        "game_date": game_date,
        "date_precision": date_precision,
        "team_a_key": "alabama",
        "team_b_key": "florida",
        "team_a_score": str(alabama_score),
        "team_b_score": str(florida_score),
        "site_type": "UNKNOWN",
        "venue_key": "",
        "site_city": "",
        "site_state": "",
        "designated_home_team_key": "",
        "notes": "",
    }


class IdentityMatchingSafetyTests(unittest.TestCase):
    def test_far_score_collision_without_exact_date_requires_review(self):
        src = source("2024-03-15", 87, 105)
        candidates = [
            candidate("CBBG-MAR05", "2024-03-05", 87, 105),
            candidate("CBBG-FEB21", "2024-02-21", 98, 93),
        ]
        status, game_id, method = ingest_school.identify_game(src, candidates)
        self.assertEqual(status, ingest_school.REVIEW)
        self.assertEqual(game_id, "")
        self.assertEqual(
            method,
            "UNIQUE_PAIR_SEASON_SCORE_DATE_CONFLICT_REQUIRES_REVIEW",
        )

    def test_far_score_collision_does_not_override_exact_date(self):
        src = source("2024-03-15", 87, 105)
        candidates = [
            candidate("CBBG-MAR15", "2024-03-15", 88, 102),
            candidate("CBBG-MAR05", "2024-03-05", 87, 105),
        ]
        status, game_id, method = ingest_school.identify_game(src, candidates)
        self.assertEqual(status, ingest_school.CONFIDENT)
        self.assertEqual(game_id, "CBBG-MAR15")
        self.assertEqual(method, "UNIQUE_PAIR_SEASON_DATE")

    def test_one_day_score_date_shift_remains_confident(self):
        src = source("1992-03-12", 62, 60)
        candidates = [
            candidate("CBBG-MAR13", "1992-03-13", 62, 60),
            candidate("CBBG-OTHER", "1992-01-01", 80, 70),
        ]
        status, game_id, method = ingest_school.identify_game(src, candidates)
        self.assertEqual(status, ingest_school.CONFIDENT)
        self.assertEqual(game_id, "CBBG-MAR13")
        self.assertEqual(method, "UNIQUE_PAIR_SEASON_SCORE_DATE_CONFLICT")

    def test_exact_date_enrichment_is_independent_of_site(self):
        src = source("1935-01-26", 33, 44)
        can = candidate("CBBG-OLD", "", 33, 34, date_precision="SEASON")
        enrichments = ingest_school.canonical_enrichment_candidates(src, can, {})
        self.assertIn(("game_date", "1935-01-26"), enrichments)
        self.assertIn(("date_precision", "EXACT"), enrichments)

    def test_nonblank_canonical_date_is_never_proposed_for_overwrite(self):
        src = source("1935-01-26", 33, 44)
        can = candidate("CBBG-OLD", "1935-01-27", 33, 34, date_precision="EXACT")
        enrichments = ingest_school.canonical_enrichment_candidates(src, can, {})
        self.assertNotIn(("game_date", "1935-01-26"), enrichments)


if __name__ == "__main__":
    unittest.main()
