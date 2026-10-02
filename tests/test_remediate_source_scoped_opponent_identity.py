import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remediate_source_scoped_opponent_identity import (  # noqa: E402
    ScopedIdentityError,
    apply_plan,
    build_plan,
    read_csv,
)


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class SourceScopedOpponentIdentityTests(unittest.TestCase):
    def make_repo(self, root: Path):
        write_csv(
            root / "data/reference/programs.csv",
            ["program_key", "current_d1"],
            [
                {"program_key": "virginia-tech", "current_d1": "Yes"},
                {"program_key": "baylor", "current_d1": "Yes"},
            ],
        )
        opponent_fields = [
            "index",
            "source_program_key",
            "source_opponent_label",
            "canonical_opponent_key",
            "canonical_opponent_name",
            "current_d1",
            "games_with_source_label",
            "first_season",
            "last_season",
            "resolution_status",
            "resolution_method",
            "user_choice",
            "audit_note",
        ]
        write_csv(
            root / "schools/alabama/opponents.csv",
            opponent_fields,
            [
                {
                    "index": "641",
                    "source_program_key": "alabama",
                    "source_opponent_label": "Virginia Tech ^",
                    "canonical_opponent_key": "virginia-tech",
                    "canonical_opponent_name": "Virginia Tech",
                    "current_d1": "Yes",
                    "games_with_source_label": "3",
                    "first_season": "1960-1961",
                    "last_season": "1964-1965",
                    "resolution_status": "RESOLVED",
                    "resolution_method": "legacy",
                    "user_choice": "",
                    "audit_note": "",
                }
            ],
        )
        source_fields = [
            "source_game_id",
            "source_program_key",
            "season_label",
            "game_date",
            "source_opponent_label",
            "normalized_opponent_key",
            "normalized_opponent_name",
            "opponent_current_d1",
            "notes",
            "raw_text",
        ]
        write_csv(
            root / "schools/alabama/source-games.csv",
            source_fields,
            [
                {
                    "source_game_id": "ALARAW-00923",
                    "source_program_key": "alabama",
                    "season_label": "1960-1961",
                    "game_date": "1960-12-16",
                    "source_opponent_label": "Virginia Tech ^",
                    "normalized_opponent_key": "virginia-tech",
                    "normalized_opponent_name": "Virginia Tech",
                    "opponent_current_d1": "Yes",
                    "notes": "",
                    "raw_text": "Dec. 16 vs. Virginia Tech ^ -/- W 72 55",
                },
                {
                    "source_game_id": "ALARAW-00948",
                    "source_program_key": "alabama",
                    "season_label": "1961-1962",
                    "game_date": "1961-12-15",
                    "source_opponent_label": "Virginia Tech ^",
                    "normalized_opponent_key": "virginia-tech",
                    "normalized_opponent_name": "Virginia Tech",
                    "opponent_current_d1": "Yes",
                    "notes": "",
                    "raw_text": "Dec. 15 vs. Virginia Tech ^ -/- L 65 70",
                },
                {
                    "source_game_id": "ALARAW-01025",
                    "source_program_key": "alabama",
                    "season_label": "1964-1965",
                    "game_date": "1964-12-18",
                    "source_opponent_label": "Virginia Tech ^",
                    "normalized_opponent_key": "virginia-tech",
                    "normalized_opponent_name": "Virginia Tech",
                    "opponent_current_d1": "Yes",
                    "notes": "",
                    "raw_text": "Dec. 18 vs. Virginia Tech ^ -/- W 72 53",
                },
            ],
        )
        canonical_fields = [
            "canonical_game_id",
            "season_label",
            "game_date",
            "date_precision",
            "team_a_key",
            "team_b_key",
            "team_a_score",
            "team_b_score",
            "result_winner_team_key",
            "overtime_periods",
            "site_type",
            "designated_home_team_key",
            "venue_key",
            "venue_id",
            "site_city",
            "site_state",
            "game_type",
            "postseason_round",
            "administrative_status",
            "administrative_note",
            "canonical_status",
            "notes",
        ]
        def game(gid, date, opponent):
            a, b = sorted(("alabama", opponent))
            return {
                "canonical_game_id": gid,
                "season_label": "1960-1961",
                "game_date": date,
                "date_precision": "EXACT",
                "team_a_key": a,
                "team_b_key": b,
                "team_a_score": "72",
                "team_b_score": "55",
                "result_winner_team_key": "alabama",
                "overtime_periods": "0",
                "site_type": "NEUTRAL",
                "designated_home_team_key": "",
                "venue_key": "",
                "venue_id": "",
                "site_city": "Birmingham" if opponent == "baylor" else "",
                "site_state": "AL" if opponent == "baylor" else "",
                "game_type": "REGULAR_SEASON",
                "postseason_round": "",
                "administrative_status": "",
                "administrative_note": "",
                "canonical_status": "PROVISIONAL",
                "notes": "",
            }
        write_csv(
            root / "data/canonical/games.csv",
            canonical_fields,
            [
                game("CBBG-0028395", "1960-12-16", "virginia-tech"),
                game("CBBG-0099629", "1960-12-14", "baylor"),
            ],
        )
        assertion_fields = [
            "assertion_id",
            "canonical_game_id",
            "source_program_key",
            "source_game_id",
            "game_date",
            "source_opponent_label",
            "normalized_opponent_key",
            "normalized_opponent_name",
            "match_status",
            "match_method",
            "raw_text",
        ]
        write_csv(
            root / "data/evidence/game-assertions.csv",
            assertion_fields,
            [
                {
                    "assertion_id": "ASRT-A",
                    "canonical_game_id": "CBBG-0028395",
                    "source_program_key": "alabama",
                    "source_game_id": "ALARAW-00923",
                    "game_date": "1960-12-16",
                    "source_opponent_label": "Virginia Tech ^",
                    "normalized_opponent_key": "virginia-tech",
                    "normalized_opponent_name": "Virginia Tech",
                    "match_status": "MATCHED",
                    "match_method": "NO_SAME_SEASON_TEAM_PAIR",
                    "raw_text": "Dec. 16 vs. Virginia Tech ^ -/- W 72 55",
                },
                {
                    "assertion_id": "ASRT-B",
                    "canonical_game_id": "CBBG-0099629",
                    "source_program_key": "baylor",
                    "source_game_id": "BAYRAW-01043",
                    "game_date": "1960-12-14",
                    "source_opponent_label": "vs. Alabama1",
                    "normalized_opponent_key": "alabama",
                    "normalized_opponent_name": "Alabama",
                    "match_status": "MATCHED",
                    "match_method": "NO_SAME_SEASON_TEAM_PAIR",
                    "raw_text": "D14 — — vs. Alabama1 L 55-72",
                },
            ],
        )
        discrepancy_fields = [
            "discrepancy_id",
            "canonical_game_id",
            "field_name",
            "source_a_program_key",
            "source_a_value",
            "source_b_program_key",
            "source_b_value",
            "canonical_value",
            "status",
            "resolution_basis",
            "notes",
        ]
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            discrepancy_fields,
            [],
        )
        tools_dir = root / "tools"
        tools_dir.mkdir(parents=True, exist_ok=True)
        (tools_dir / "validate_data.py").write_text(
            "raise SystemExit(0)\n", encoding="utf-8"
        )

    def test_mixed_literal_population_splits_one_game_and_reconciles_date(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            basis = (
                "Owner-approved Alabama/Baylor correction: reciprocal institutional "
                "and contemporary evidence identify Alabama 72-Baylor 55 on 1960-12-16."
            )
            plan = build_plan(
                repo,
                source_program="alabama",
                source_label="Virginia Tech ^",
                source_game_id="ALARAW-00923",
                old_key="virginia-tech",
                new_key="baylor",
                new_name="Baylor",
                stale_canonical_id="CBBG-0028395",
                survivor_canonical_id="CBBG-0099629",
                basis=basis,
                canonical_game_date="1960-12-16",
            )
            self.assertEqual(plan["payload"]["original_literal_label_games"], 3)
            self.assertEqual(plan["payload"]["remaining_old_identity_games"], 2)
            self.assertEqual(len(plan["payload"]["new_discrepancies"]), 1)

            result = apply_plan(repo, plan, plan["sha256"])
            self.assertEqual(result["opponent_mapping_split"], 1)
            self.assertEqual(result["discrepancies_added"], 1)

            _, opponents = read_csv(repo / "schools/alabama/opponents.csv")
            mapping = {
                row["canonical_opponent_key"]: row
                for row in opponents
                if row["source_opponent_label"] == "Virginia Tech ^"
            }
            self.assertEqual(mapping["virginia-tech"]["games_with_source_label"], "2")
            self.assertEqual(mapping["virginia-tech"]["first_season"], "1961-1962")
            self.assertEqual(mapping["virginia-tech"]["last_season"], "1964-1965")
            self.assertEqual(mapping["baylor"]["games_with_source_label"], "1")
            self.assertEqual(mapping["baylor"]["first_season"], "1960-1961")
            self.assertEqual(mapping["baylor"]["last_season"], "1960-1961")

            _, sources = read_csv(repo / "schools/alabama/source-games.csv")
            keys = {row["source_game_id"]: row["normalized_opponent_key"] for row in sources}
            self.assertEqual(keys["ALARAW-00923"], "baylor")
            self.assertEqual(keys["ALARAW-00948"], "virginia-tech")
            self.assertEqual(keys["ALARAW-01025"], "virginia-tech")
            raw = {row["source_game_id"]: row["raw_text"] for row in sources}
            self.assertEqual(
                raw["ALARAW-00923"],
                "Dec. 16 vs. Virginia Tech ^ -/- W 72 55",
            )

            _, games = read_csv(repo / "data/canonical/games.csv")
            by_id = {row["canonical_game_id"]: row for row in games}
            self.assertNotIn("CBBG-0028395", by_id)
            self.assertEqual(by_id["CBBG-0099629"]["game_date"], "1960-12-16")
            self.assertEqual(by_id["CBBG-0099629"]["site_city"], "Birmingham")
            self.assertEqual(by_id["CBBG-0099629"]["site_state"], "AL")

            _, assertions = read_csv(repo / "data/evidence/game-assertions.csv")
            alabama = next(row for row in assertions if row["source_program_key"] == "alabama")
            baylor = next(row for row in assertions if row["source_program_key"] == "baylor")
            self.assertEqual(alabama["canonical_game_id"], "CBBG-0099629")
            self.assertEqual(alabama["normalized_opponent_key"], "baylor")
            self.assertEqual(alabama["game_date"], "1960-12-16")
            self.assertEqual(baylor["game_date"], "1960-12-14")

            _, discrepancies = read_csv(repo / "data/reconciliation/discrepancies.csv")
            self.assertEqual(len(discrepancies), 1)
            discrepancy = discrepancies[0]
            self.assertEqual(discrepancy["field_name"], "game_date")
            self.assertEqual(discrepancy["source_a_program_key"], "baylor")
            self.assertEqual(discrepancy["source_a_value"], "1960-12-14")
            self.assertEqual(discrepancy["source_b_program_key"], "alabama")
            self.assertEqual(discrepancy["source_b_value"], "1960-12-16")
            self.assertEqual(discrepancy["canonical_value"], "1960-12-16")
            self.assertEqual(discrepancy["status"], "RESOLVED")

    def test_date_conflict_requires_explicit_canonical_date(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            with self.assertRaisesRegex(ScopedIdentityError, "game_date"):
                build_plan(
                    repo,
                    source_program="alabama",
                    source_label="Virginia Tech ^",
                    source_game_id="ALARAW-00923",
                    old_key="virginia-tech",
                    new_key="baylor",
                    new_name="Baylor",
                    stale_canonical_id="CBBG-0028395",
                    survivor_canonical_id="CBBG-0099629",
                    basis="Evidence basis.",
                )

    def test_explicit_date_must_be_one_counterpart_date(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            with self.assertRaisesRegex(
                ScopedIdentityError, "must match one of the two counterpart dates"
            ):
                build_plan(
                    repo,
                    source_program="alabama",
                    source_label="Virginia Tech ^",
                    source_game_id="ALARAW-00923",
                    old_key="virginia-tech",
                    new_key="baylor",
                    new_name="Baylor",
                    stale_canonical_id="CBBG-0028395",
                    survivor_canonical_id="CBBG-0099629",
                    basis="Evidence basis.",
                    canonical_game_date="1960-12-15",
                )


if __name__ == "__main__":
    unittest.main()
