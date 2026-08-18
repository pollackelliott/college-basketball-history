import csv
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
from ncaa_safety import canonical_ncaa_errors, ncaa_evidence_errors  # noqa: E402
from onboarding_plan import _planned_ncaa_safety_errors, build_plan  # noqa: E402
from venue_reference import load_global_venue_reference  # noqa: E402


def rows(path: Path):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


class NcaaSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.canonical = rows(ROOT / "data/canonical/games.csv")
        cls.canonical_by_id = {
            row["canonical_game_id"]: row for row in cls.canonical
        }
        cls.venues_by_id, cls.venues_by_key, _ = load_global_venue_reference(ROOT)

    def test_current_canonical_ncaa_layer_is_publishable(self):
        self.assertEqual(
            canonical_ncaa_errors(self.canonical, self.venues_by_id),
            [],
        )

    def test_committed_ncaa_site_evidence_is_exact_and_complete(self):
        evidence = rows(ROOT / "data/evidence/ncaa-tournament-sites.csv")
        self.assertEqual(len(evidence), 773)
        self.assertEqual(
            len({row["canonical_game_id"] for row in evidence}),
            773,
        )
        self.assertEqual(
            ncaa_evidence_errors(ROOT, self.canonical, self.venues_by_id),
            [],
        )

    def test_no_ncaa_r64_before_1978_1979(self):
        bad = [
            row["canonical_game_id"]
            for row in self.canonical
            if row.get("game_type") == "NCAA_TOURNAMENT"
            and row.get("postseason_round") == "R64"
            and row.get("season_label", "") < "1978-1979"
        ]
        self.assertEqual(bad, [])

    def test_locked_round_corrections_are_r32(self):
        self.assertEqual(
            self.canonical_by_id["CBBG-0021340"]["postseason_round"],
            "R32",
        )
        self.assertEqual(
            self.canonical_by_id["CBBG-0021364"]["postseason_round"],
            "R32",
        )

    def test_locked_ncaa_venue_normalizations(self):
        expected = {
            "CBBG-0021439": (
                "greensboro-coliseum",
                "VEN-000076",
                "Greensboro",
                "NC",
            ),
            "CBBG-0005748": (
                "t-mobile-arena",
                "VEN-000201",
                "Paradise",
                "NV",
            ),
            "CBBG-0031836": (
                "state-farm-arena",
                "VEN-000195",
                "Atlanta",
                "GA",
            ),
            "CBBG-0031837": (
                "state-farm-arena",
                "VEN-000195",
                "Atlanta",
                "GA",
            ),
        }
        for game_id, values in expected.items():
            row = self.canonical_by_id[game_id]
            self.assertEqual(
                (
                    row["venue_key"],
                    row["venue_id"],
                    row["site_city"],
                    row["site_state"],
                ),
                values,
            )

    def test_reunion_arena_locked_row(self):
        row = self.canonical_by_id["CBBG-0004439"]
        self.assertEqual(row["venue_key"], "reunion-arena")
        self.assertEqual((row["site_city"], row["site_state"]), ("Dallas", "TX"))

    def test_miami_correction_is_game_specific(self):
        row = self.canonical_by_id["CBBG-0008400"]
        self.assertEqual(row["team_b_key"], "miami")
        self.assertEqual(row["result_winner_team_key"], "miami")

        illinois_source = rows(ROOT / "schools/illinois/source-games.csv")
        source = next(
            row for row in illinois_source
            if row["source_game_id"] == "ILLRAW-02600"
        )
        self.assertEqual(source["normalized_opponent_key"], "miami")
        self.assertEqual(source["normalized_opponent_name"], "Miami (FL)")

        opponents = rows(ROOT / "schools/illinois/opponents.csv")
        generic = next(
            row for row in opponents
            if row["source_opponent_label"] == "Miami"
        )
        self.assertEqual(generic["canonical_opponent_key"], "miami-oh")

    def test_incomplete_ncaa_row_is_fatal(self):
        fixture = {
            "canonical_game_id": "FIXTURE-1",
            "season_label": "2025-2026",
            "game_type": "NCAA_TOURNAMENT",
            "postseason_round": "R64",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
        }
        errors = canonical_ncaa_errors([fixture], self.venues_by_id)
        self.assertTrue(errors)
        self.assertIn("site is incomplete", errors[0])

    def test_pre_1979_r64_is_fatal(self):
        global_venue = self.venues_by_id["VEN-000076"]
        fixture = {
            "canonical_game_id": "FIXTURE-2",
            "season_label": "1977-1978",
            "game_type": "NCAA_TOURNAMENT",
            "postseason_round": "R64",
            "venue_key": "greensboro-coliseum",
            "venue_id": "VEN-000076",
            "site_city": global_venue["city"],
            "site_state": global_venue["state"],
        }
        errors = canonical_ncaa_errors([fixture], self.venues_by_id)
        self.assertTrue(any("R64 is invalid" in error for error in errors))

    def test_matched_legacy_source_uses_complete_canonical_outcome(self):
        source = {
            "source_program_key": "fixture",
            "source_game_id": "LEGACY-NCAA",
            "normalized_opponent_key": "opponent",
            "game_date": "",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "",
            "state": "",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "R32",
        }
        canonical = {
            "canonical_game_id": "MATCHED-1",
            "season_label": "2024-2025",
            "game_date": "",
            "date_precision": "SEASON",
            "site_type": "NEUTRAL",
            "designated_home_team_key": "",
            "venue_key": "greensboro-coliseum",
            "venue_id": "VEN-000076",
            "site_city": self.venues_by_id["VEN-000076"]["city"],
            "site_state": self.venues_by_id["VEN-000076"]["state"],
            "game_type": "NCAA_TOURNAMENT",
            "postseason_round": "R32",
            "notes": "",
        }
        errors = _planned_ncaa_safety_errors(
            source,
            ingest_school.CONFIDENT,
            "MATCHED-1",
            {"MATCHED-1": canonical},
            {},
            {},
            self.venues_by_id,
        )
        self.assertEqual(errors, [])

    def test_new_incomplete_ncaa_game_is_blocked_before_owner_review(self):
        source = {
            "source_program_key": "alpha",
            "source_game_id": "NEW-NCAA",
            "season_label": "2025-2026",
            "game_date": "2026-03-20",
            "normalized_opponent_key": "beta",
            "team_score": "70",
            "opponent_score": "65",
            "played_result": "W",
            "overtime_periods": "0",
            "curated_site_type": "NEUTRAL",
            "curated_venue_name": "",
            "city": "",
            "state": "",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "R64",
        }
        errors = _planned_ncaa_safety_errors(
            source,
            ingest_school.NEW_GAME,
            "",
            {},
            {},
            {},
            self.venues_by_id,
        )
        self.assertTrue(errors)
        self.assertTrue(any("site is incomplete" in error for error in errors))

    def test_existing_vanderbilt_plan_is_not_retroactively_blocked(self):
        plan = build_plan(ROOT, "vanderbilt")
        ncaa_blockers = [
            blocker
            for blocker in plan.get("blockers", [])
            if "NCAA safety before owner review" in blocker
        ]
        self.assertEqual(ncaa_blockers, [])


if __name__ == "__main__":
    unittest.main()
