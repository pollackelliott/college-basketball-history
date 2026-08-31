import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from published_site_completeness_census import build_census  # noqa: E402


SOURCE_FIELDS = [
    "source_game_id",
    "source_program_key",
    "season_label",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "site_research_status",
    "site_research_basis",
]
CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "team_a_key",
    "team_b_key",
    "site_type",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "game_type",
    "notes",
]
ASSERTION_FIELDS = [
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "event_or_tournament",
]
DISCREPANCY_FIELDS = [
    "canonical_game_id",
    "field_name",
    "status",
    "resolution_basis",
]


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_row(program, game_id, opponent, **overrides):
    row = {
        "source_game_id": game_id,
        "source_program_key": program,
        "season_label": "2025-2026",
        "normalized_opponent_key": opponent,
        "curated_site_type": "NEUTRAL",
        "curated_venue_name": "Example Arena",
        "city": "Example City",
        "state": "EX",
        "curated_game_type": "REGULAR_SEASON",
        "site_research_status": "",
        "site_research_basis": "",
    }
    row.update(overrides)
    return row


def canonical_row(game_id, team_a="alpha", team_b="beta", **overrides):
    row = {
        "canonical_game_id": game_id,
        "season_label": "2025-2026",
        "team_a_key": team_a,
        "team_b_key": team_b,
        "site_type": "NEUTRAL",
        "venue_key": "example-arena",
        "venue_id": "VEN-999999",
        "site_city": "Example City",
        "site_state": "EX",
        "game_type": "REGULAR_SEASON",
        "notes": "",
    }
    row.update(overrides)
    return row


def assertion(program, source_id, canonical_id, opponent, **overrides):
    row = {
        "canonical_game_id": canonical_id,
        "source_program_key": program,
        "source_game_id": source_id,
        "normalized_opponent_key": opponent,
        "curated_site_type": "NEUTRAL",
        "curated_venue_name": "Example Arena",
        "city": "Example City",
        "state": "EX",
        "curated_game_type": "REGULAR_SEASON",
        "event_or_tournament": "",
    }
    row.update(overrides)
    return row


class PublishedSiteCompletenessCensusTests(unittest.TestCase):
    def make_repo(self, root: Path):
        programs = [
            {
                "program_key": "alpha",
                "display_name": "Alpha",
                "history_start_season": "1900-1901",
                "public_page_enabled": "yes",
            },
            {
                "program_key": "beta",
                "display_name": "Beta",
                "history_start_season": "1900-1901",
                "public_page_enabled": "yes",
            },
            {
                "program_key": "gamma",
                "display_name": "Gamma",
                "history_start_season": "2000-2001",
                "public_page_enabled": "no",
            },
        ]
        write_csv(
            root / "data/reference/programs.csv",
            [
                "program_key",
                "display_name",
                "history_start_season",
                "public_page_enabled",
            ],
            programs,
        )

        alpha_sources = [
            source_row(
                "alpha",
                "ARAW-1",
                "beta",
                curated_site_type="SOURCE_PROGRAM_HOME",
                curated_venue_name="",
                city="Alpha City",
                state="AA",
                site_research_status="RESEARCHED_UNRESOLVED_HOME_VENUE",
                site_research_basis="Exhaustive archival research; exact building unresolved.",
            )
        ]
        beta_sources = [
            source_row(
                "beta",
                "BRAW-1",
                "alpha",
                curated_site_type="SOURCE_PROGRAM_HOME",
                curated_venue_name="",
                city="",
                state="",
            )
        ]
        write_csv(root / "schools/alpha/source-games.csv", SOURCE_FIELDS, alpha_sources)
        write_csv(root / "schools/beta/source-games.csv", SOURCE_FIELDS, beta_sources)

        canonical = [
            canonical_row(
                "CBBG-1",
                site_type="TEAM_A_HOME",
                venue_key="",
                venue_id="",
                site_city="Alpha City",
                site_state="AA",
                notes="[RESEARCHED_UNRESOLVED_HOME_VENUE source=alpha/ARAW-1]",
            ),
            canonical_row(
                "CBBG-2",
                site_type="TEAM_B_HOME",
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            ),
            canonical_row(
                "CBBG-3",
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            ),
            canonical_row(
                "CBBG-4",
                venue_key="",
                venue_id="",
                site_city="Tournament City",
                site_state="TC",
                game_type="CONFERENCE_TOURNAMENT",
            ),
            canonical_row(
                "CBBG-5",
                team_a="gamma",
                team_b="delta",
                venue_key="",
                venue_id="",
                site_city="",
                site_state="",
            ),
        ]
        write_csv(root / "data/canonical/games.csv", CANONICAL_FIELDS, canonical)

        assertions = [
            assertion(
                "alpha",
                "ARAW-1",
                "CBBG-1",
                "beta",
                curated_site_type="SOURCE_PROGRAM_HOME",
                curated_venue_name="",
                city="Alpha City",
                state="AA",
            ),
            assertion(
                "beta",
                "BRAW-1",
                "CBBG-2",
                "alpha",
                curated_site_type="SOURCE_PROGRAM_HOME",
                curated_venue_name="",
                city="",
                state="",
            ),
            assertion(
                "alpha",
                "ARAW-CT",
                "CBBG-4",
                "beta",
                curated_game_type="CONFERENCE_TOURNAMENT",
                curated_venue_name="",
                city="Tournament City",
                state="TC",
                event_or_tournament="Example Conference Tournament",
            ),
        ]
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ASSERTION_FIELDS,
            assertions,
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            DISCREPANCY_FIELDS,
            [],
        )

    def test_exact_public_site_debt_buckets(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            report = build_census(root)

            self.assertEqual(report["published_program_count"], 2)
            self.assertEqual(report["published_unique_canonical_games"], 4)

            self.assertEqual(report["home"]["missing_any"], 2)
            self.assertEqual(report["home"]["hard_blockers"], 1)
            self.assertEqual(
                report["home"]["researched_unresolved_venue_exceptions"], 1
            )

            self.assertEqual(report["neutral"]["regular_season"]["missing_any"], 1)
            self.assertEqual(
                report["neutral"]["published_vs_published"]["missing_any"], 2
            )
            self.assertEqual(report["postseason"]["conference_tournament"]["total"], 1)
            self.assertEqual(
                report["postseason"]["conference_tournament"]["missing_venue"], 1
            )

            events = report["conference_tournament_gap_events"]
            self.assertEqual(len(events), 1)
            self.assertEqual(events[0]["event_labels"], ["Example Conference Tournament"])
            self.assertEqual(events[0]["games"], 1)

    def test_unpublished_only_games_do_not_enter_public_denominator(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            report = build_census(root)
            self.assertNotIn("gamma", report["published_program_keys"])
            self.assertEqual(report["published_unique_canonical_games"], 4)


if __name__ == "__main__":
    unittest.main()
