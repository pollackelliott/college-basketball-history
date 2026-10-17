"""Regression: Stage-2 integration accepts sourced foreign localities, not domestic gaps."""

import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
from location_safety import source_location_preflight  # noqa: E402
from onboarding_plan import validate_package  # noqa: E402


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def example_source(**overrides):
    row = {
        "source_game_id": "GTG-S1-02569",
        "source_program_key": "georgetown",
        "season_label": "2014-2015",
        "game_date": "2014-11-26",
        "source_opponent_label": "Florida",
        "normalized_opponent_key": "florida",
        "normalized_opponent_name": "Florida",
        "team_score": "66",
        "opponent_score": "65",
        "played_result": "W",
        "overtime_periods": "1",
        "curated_site_type": "NEUTRAL",
        "source_venue_name": "Imperial Arena",
        "curated_venue_name": "Imperial Arena",
        "city": "Paradise Island",
        "state": "",
        "country": "Bahamas",
        "curated_game_type": "REGULAR_SEASON",
        "curated_postseason_round": "",
        "raw_text": "Georgetown beat Florida 66-65 in overtime",
    }
    row.update(overrides)
    return row


class ForeignLocationStage2Tests(unittest.TestCase):
    def package_fixture(self, root, source):
        school = root / "schools" / "georgetown"
        school.mkdir(parents=True)
        write_csv(school / "source-games.csv", list(source), [source])
        write_csv(
            school / "opponents.csv",
            ["source_program_key", "canonical_opponent_key",
             "canonical_opponent_name", "current_d1"],
            [{"source_program_key": "georgetown", "canonical_opponent_key": "florida",
              "canonical_opponent_name": "Florida", "current_d1": "Yes"}],
        )
        write_csv(
            school / "venues.csv",
            ["source_program_key", "venue_key", "canonical_name", "aliases", "city", "state"],
            [{"source_program_key": "georgetown", "venue_key": "imperial-arena",
              "canonical_name": "Imperial Arena", "aliases": "", "city": "Nassau",
              "state": "BS"}],
        )
        write_csv(school / "conferences.csv", ["source_program_key", "conference_key"], [])
        for name in ("notes.md", "source-notes.md"):
            (school / name).write_text("# Fixture\n", encoding="utf-8")
        write_csv(
            root / "data" / "reference" / "programs.csv",
            ["program_key", "program_name", "current_d1"],
            [
                {"program_key": "georgetown", "program_name": "Georgetown",
                 "current_d1": "Yes"},
                {"program_key": "florida", "program_name": "Florida",
                 "current_d1": "Yes"},
            ],
        )
        write_csv(root / "data" / "reference" / "conferences.csv", ["conference_key"], [])

    def package_errors(self, source):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.package_fixture(root, source)
            with patch("onboarding_plan.history_scope_errors", return_value=[]):
                return validate_package(root, "georgetown")["errors"]

    def test_supported_foreign_city_and_country_pass_stage2_package_qa(self):
        self.assertEqual(self.package_errors(example_source()), [])

    def test_missing_or_domestic_country_cannot_exempt_partial_location(self):
        for country in ("", "United States", "USA"):
            with self.subTest(country=country):
                errors = self.package_errors(example_source(country=country))
                self.assertTrue(any("normalized city/state" in s for s in errors), errors)

    def test_foreign_country_cannot_exempt_missing_city(self):
        errors = self.package_errors(example_source(city="", state="BS"))
        self.assertTrue(any("normalized city/state" in s for s in errors), errors)

    def test_source_preflight_respects_same_foreign_rule(self):
        row = example_source()
        self.assertEqual(source_location_preflight([row], set(), {"imperial arena"}), ([], []))
        for changed in ({"country": ""}, {"country": "USA"}, {"city": "", "state": "BS"}):
            with self.subTest(changed=changed):
                errors, warnings = source_location_preflight(
                    [{**row, **changed}], set(), {"imperial arena"}
                )
                self.assertEqual(len(errors), 1)
                self.assertEqual(warnings, [])

    def test_new_canonical_uses_global_venue_geography_but_keeps_source_locality(self):
        row = example_source()
        metadata = {
            "imperial arena": {
                "venue_key": "imperial-arena",
                "venue_id": "VEN-000088",
                "city": "Nassau",
                "state": "BS",
            }
        }
        canonical = ingest_school.build_new_canonical(
            row, "CBBG-TEST", {}, metadata
        )
        assertion = ingest_school.build_assertion(
            row, "CBBG-TEST", "TEST_MATCH"
        )
        self.assertEqual(
            (canonical["site_city"], canonical["site_state"]), ("Nassau", "BS")
        )
        self.assertEqual(canonical["venue_id"], "VEN-000088")
        self.assertEqual((assertion["city"], assertion["state"]), ("Paradise Island", ""))
        self.assertEqual(row["country"], "Bahamas")
        self.assertIn("VENUE_REGISTRY_FALLBACK", canonical["notes"])

    def test_matched_game_enrichment_uses_global_venue_for_foreign_locality(self):
        row = example_source()
        canonical = {
            "site_type": "NEUTRAL", "venue_key": "", "venue_id": "",
            "site_city": "", "site_state": "", "notes": "",
        }
        metadata = {
            "imperial arena": {
                "venue_key": "imperial-arena", "venue_id": "VEN-000088",
                "city": "Nassau", "state": "BS",
            }
        }
        updates = dict(
            ingest_school.canonical_enrichment_candidates(row, canonical, metadata)
        )
        self.assertEqual((updates["site_city"], updates["site_state"]), ("Nassau", "BS"))
        self.assertEqual(updates["venue_id"], "VEN-000088")


if __name__ == "__main__":
    unittest.main()
