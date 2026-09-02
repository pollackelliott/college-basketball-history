import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import opponent_identity_collision_audit as audit


def plan(affected):
    return {
        "plan_sha256": "plan-sha",
        "global_key_map": {"texas-a-and-m": "texas-a-m"},
        "affected_canonical_game_ids": {"texas-a-and-m->texas-a-m": affected},
    }


def game(
    game_id,
    *,
    date="1993-12-18",
    opponent="texas-a-and-m",
    northwestern_score="67",
    opponent_score="48",
    overtime="0",
    site_type="TEAM_B_HOME",
):
    return {
        "canonical_game_id": game_id,
        "season_label": "1993-1994",
        "game_date": date,
        "team_a_key": "northwestern",
        "team_b_key": opponent,
        "team_a_score": northwestern_score,
        "team_b_score": opponent_score,
        "result_winner_team_key": "northwestern",
        "overtime_periods": overtime,
        "site_type": site_type,
        "designated_home_team_key": opponent if site_type == "TEAM_B_HOME" else "",
        "venue_key": "",
        "venue_id": "",
        "site_city": "",
        "site_state": "",
        "game_type": "REGULAR_SEASON",
        "postseason_round": "",
        "administrative_status": "",
        "administrative_note": "",
    }


class OpponentIdentityCollisionAuditTests(unittest.TestCase):
    def test_exact_same_date_pair_is_exact_core_match(self):
        rows = [
            game("CBBG-10"),
            game("CBBG-20", opponent="texas-a-m"),
        ]
        report = audit.audit_rows(plan(["CBBG-10"]), rows)
        self.assertEqual(report["exact_core_match_group_count"], 1)
        self.assertEqual(report["same_date_identity_conflict_group_count"], 0)
        self.assertEqual(report["unpaired_affected_game_count"], 0)
        self.assertEqual(
            report["collision_groups"][0]["oldest_id_candidate"], "CBBG-10"
        )
        self.assertEqual(
            report["collision_groups"][0]["survivor_status"],
            "REVIEW_CANDIDATE_ONLY",
        )

    def test_overtime_disagreement_is_same_date_identity_conflict(self):
        rows = [
            game("CBBG-10", overtime="0"),
            game("CBBG-20", opponent="texas-a-m", overtime="1"),
        ]
        report = audit.audit_rows(plan(["CBBG-10"]), rows)
        self.assertEqual(report["exact_core_match_group_count"], 0)
        self.assertEqual(report["same_date_identity_conflict_group_count"], 1)
        group = report["collision_groups"][0]
        self.assertIn("overtime_periods", group["field_differences"])
        self.assertEqual(report["unpaired_affected_game_count"], 0)

    def test_score_disagreement_is_same_date_identity_conflict(self):
        rows = [
            game("CBBG-10", opponent_score="48"),
            game("CBBG-20", opponent="texas-a-m", opponent_score="49"),
        ]
        report = audit.audit_rows(plan(["CBBG-10"]), rows)
        self.assertEqual(report["same_date_identity_conflict_group_count"], 1)
        group = report["collision_groups"][0]
        self.assertIn("team_b_score", group["field_differences"])

    def test_affected_game_without_same_date_counterpart_is_unpaired(self):
        report = audit.audit_rows(plan(["CBBG-10"]), [game("CBBG-10")])
        self.assertEqual(report["same_date_collision_group_count"], 0)
        self.assertEqual(report["unpaired_affected_game_ids"], ["CBBG-10"])

    def test_unrelated_same_date_group_is_ignored(self):
        rows = [
            game("CBBG-10"),
            {
                **game("CBBG-30", opponent="texas-a-m"),
                "team_a_key": "oklahoma",
                "team_a_score": "80",
                "team_b_score": "75",
            },
            {
                **game("CBBG-40", opponent="texas-a-m"),
                "team_a_key": "oklahoma",
                "team_a_score": "80",
                "team_b_score": "75",
            },
        ]
        report = audit.audit_rows(plan(["CBBG-10"]), rows)
        self.assertEqual(report["same_date_collision_group_count"], 0)
        self.assertEqual(report["unpaired_affected_game_ids"], ["CBBG-10"])

    def test_audit_hash_is_deterministic(self):
        rows = [game("CBBG-10"), game("CBBG-20", opponent="texas-a-m")]
        one = audit.audit_rows(plan(["CBBG-10"]), rows)
        two = audit.audit_rows(plan(["CBBG-10"]), rows)
        self.assertEqual(one["audit_sha256"], two["audit_sha256"])


if __name__ == "__main__":
    unittest.main()
