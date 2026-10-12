"""Regression checks for accepted Stage 3B source, venue, locality and HOME authority."""
import csv
import tempfile
import unittest
from pathlib import Path

import research_stage4 as author
from research_stage4_closeout import compare_parent_semantics
from onboarding_hardening import research_portfolio_report
from site_completeness import (
    has_supported_foreign_locality,
    source_home_chronology_report,
    source_site_completeness_report,
)


def write_csv(path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class Stage4SourceProjectionCompatibilityTests(unittest.TestCase):
    def test_missing_row_owner_uses_explicit_verified_school_only(self):
        row = {
            "source_game_id": "GTG-1", "season_label": "1993-94",
            "source_opponent_label": "Miami", "normalized_opponent_key": "miami",
            "game_date": "1993-12-10", "site_type": "HOME",
            "game_type": "REGULAR_SEASON",
            "curated_venue_name": "Test Arena",
            "curated_venue_city": "Washington",
            "curated_venue_state": "DC",
        }
        opponents = [{"canonical_opponent_key": "miami",
                      "canonical_opponent_name": "Miami"}]
        games, defects = author._projection(
            [row], opponents, [], school_key="georgetown",
        )
        self.assertEqual(defects, [])
        self.assertEqual(games[0]["source_program_key"], "georgetown")
        self.assertEqual(games[0]["city"], "Washington")
        self.assertEqual(games[0]["state"], "DC")
        self.assertEqual(compare_parent_semantics(
            [row], games, [], school_key="georgetown",
        ), [])
        original = dict(row, source_program_key="another-school")
        explicit, _ = author._projection(
            [original], opponents, [], school_key="georgetown",
        )
        self.assertEqual(explicit[0]["source_program_key"], "another-school")

    def test_parent_semantic_guard_rejects_location_and_country_changes(self):
        row = {
            "source_game_id": "G2", "season_label": "2014-15",
            "source_opponent_label": "Florida", "normalized_opponent_key": "florida",
            "game_date": "2014-11-26", "site_type": "NEUTRAL",
            "game_type": "REGULAR_SEASON",
            "curated_venue_name": "Imperial Arena",
            "curated_venue_city": "Paradise Island",
            "curated_venue_country": "Bahamas",
        }
        games, errors = author._projection(
            [row], [{"canonical_opponent_key": "florida",
                      "canonical_opponent_name": "Florida"}], [],
            school_key="georgetown",
        )
        self.assertEqual(errors, [])
        self.assertEqual(games[0]["country"], "Bahamas")
        self.assertEqual(compare_parent_semantics(
            [row], games, [], school_key="georgetown",
        ), [])
        modified = [dict(games[0], country="United States", city="Nassau")]
        mismatches = compare_parent_semantics(
            [row], modified, [], school_key="georgetown",
        )
        self.assertEqual({x["field"] for x in mismatches}, {"city", "country"})

    def test_historical_neutral_evidence_is_research_accounted(self):
        row = {
            "source_game_id": "G3", "season_label": "1970-71",
            "site_type": "NEUTRAL", "game_type": "REGULAR_SEASON",
            "curated_venue_city": "West Palm Beach",
            "curated_venue_state": "FL",
            "venue_research_basis": "Accepted reciprocal exact-game record",
            "site_research_status": "RESEARCHED_COMPLETE",
        }
        status, basis = author._research_accounting(row)
        self.assertEqual(status, "RESEARCHED_PARTIAL")
        self.assertIn("Accepted reciprocal exact-game record", basis)
        self.assertIn("West Palm Beach", basis)
        self.assertEqual(
            author._research_accounting(dict(row, game_type="NIT"))[0], ""
        )

    def test_foreign_locality_requires_explicit_country(self):
        row = {
            "source_game_id": "G4", "curated_site_type": "NEUTRAL",
            "curated_game_type": "REGULAR_SEASON",
            "curated_venue_name": "Imperial Arena",
            "city": "Paradise Island", "state": "", "country": "Bahamas",
        }
        self.assertTrue(has_supported_foreign_locality(row))
        self.assertEqual(source_site_completeness_report(
            row.keys(), [row],
        )["counts"]["material_gap_rows"], 0)
        for country in ("", "USA", "United States"):
            changed = dict(row, country=country)
            self.assertFalse(has_supported_foreign_locality(changed))
            self.assertEqual(source_site_completeness_report(
                changed.keys(), [changed],
            )["counts"]["material_gap_rows"], 1)

    def test_foreign_venue_requires_matching_country_qualified_game(self):
        with tempfile.TemporaryDirectory() as path:
            root = Path(path)
            game = {field: "" for field in author.SOURCE_GAME_FIELDS}
            game.update({
                "source_game_id": "G5", "source_program_key": "georgetown",
                "season_label": "2025-2026", "game_date": "2025-11-15",
                "source_opponent_label": "Florida",
                "normalized_opponent_key": "florida", "team_score": "70",
                "opponent_score": "65", "played_result": "W",
                "overtime_periods": "0", "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Imperial Arena",
                "city": "Paradise Island", "state": "", "country": "Bahamas",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "Florida 70-65",
                "normalization_status": "RESEARCH_ACCEPTED",
            })
            write_csv(root / "source-games.csv", [game], author.SOURCE_GAME_FIELDS)
            write_csv(root / "opponents.csv",
                      [{"canonical_opponent_key": "florida"}],
                      ["canonical_opponent_key"])
            venue = {
                "source_program_key": "georgetown",
                "venue_key": "imperial-arena-atlantis",
                "canonical_name": "Imperial Arena", "city": "Paradise Island",
                "state": "", "relationship_type": "GAME_SITE",
            }
            write_csv(root / "venues.csv", [venue], list(venue))
            write_csv(root / "conferences.csv", [], ["source_program_key"])
            (root / "source-notes.md").write_text(
                "- Primary-source historical results cutoff: 2024-2025\n"
                "- Required completed-season cutoff: 2025-2026\n",
                encoding="utf-8",
            )
            (root / "notes.md").write_text("Synthetic Research fixture\n", encoding="utf-8")
            result = research_portfolio_report(root, school_key="georgetown")
            self.assertEqual(result["status"], "PASS", result["errors"])
            game["country"] = ""
            write_csv(root / "source-games.csv", [game], author.SOURCE_GAME_FIELDS)
            result = research_portfolio_report(root, school_key="georgetown")
            self.assertEqual(result["status"], "FAIL")
            self.assertTrue(any("city/state" in e for e in result["errors"]))

    def test_missing_home_chronology_relationship_remains_blocker(self):
        row = {
            "source_game_id": "GTG-S1-01882", "game_date": "1993-03-25",
            "season_label": "1992-1993",
            "curated_site_type": "SOURCE_PROGRAM_HOME",
            "curated_venue_name": "Patriot Center",
        }
        other_home = {
            "source_program_key": "georgetown", "canonical_name": "Home Gym",
            "relationship_type": "HOME", "relationship_start": "1990-01-01",
        }
        patriot = {
            "source_program_key": "georgetown", "canonical_name": "EagleBank Arena",
            "aliases": "Patriot Center", "relationship_type": "",
        }
        report = source_home_chronology_report(
            [row], [other_home, patriot], school_key="georgetown",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 1)
        patriot.update(
            relationship_type="HOME",
            relationship_start="1993-03-25",
            relationship_end="1993-03-25",
        )
        report = source_home_chronology_report(
            [row], [other_home, patriot], school_key="georgetown",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 0)


if __name__ == "__main__":
    unittest.main()
