import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import build_site_data  # noqa: E402
import ingest_school  # noqa: E402
from location_safety import (  # noqa: E402
    assertion_drift,
    parse_registry_fallback_markers,
    source_location_preflight,
    venue_location_conflicts,
)


def source_row(city="", state=""):
    return {
        "source_program_key": "new-school",
        "source_game_id": "NEW-0001",
        "normalized_opponent_key": "opponent",
        "curated_site_type": "NEUTRAL",
        "curated_venue_name": "Example Arena",
        "source_venue_name": "Example Arena",
        "city": city,
        "state": state,
    }


class SourcePackagePreflightTests(unittest.TestCase):
    def preflight(self, city, state):
        return source_location_preflight(
            [source_row(city, state)], set(), {"example arena"}
        )

    def test_city_only_new_domestic_location_is_rejected(self):
        errors, warnings = self.preflight("Exampleville", "")
        self.assertEqual(len(errors), 1)
        self.assertIn("partial normalized location", errors[0])
        self.assertEqual(warnings, [])

    def test_state_only_new_domestic_location_is_rejected(self):
        errors, warnings = self.preflight("", "EX")
        self.assertEqual(len(errors), 1)
        self.assertIn("partial normalized location", errors[0])
        self.assertEqual(warnings, [])

    def test_complete_location_passes(self):
        self.assertEqual(self.preflight("Exampleville", "EX"), ([], []))

    def test_blank_location_passes(self):
        self.assertEqual(self.preflight("", ""), ([], []))

    def test_venue_name_in_city_is_rejected(self):
        errors, _ = self.preflight("Example Arena", "EX")
        self.assertIn("venue name", errors[0])

    def test_combined_city_is_rejected(self):
        errors, _ = self.preflight("Alpha and Beta", "EX")
        self.assertIn("multi-city", errors[0])

    def test_existing_legacy_partial_is_warning_only(self):
        row = source_row("Exampleville", "")
        pair = {(row["source_program_key"], row["source_game_id"])}
        errors, warnings = source_location_preflight(
            [row], pair, {"example arena"}
        )
        self.assertEqual(errors, [])
        self.assertEqual(len(warnings), 1)


class CanonicalEnrichmentTests(unittest.TestCase):
    def test_complete_registry_fallback_is_atomic_and_auditable(self):
        source = source_row()
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "city": "Exampleville",
                "state": "EX",
            }
        }
        changes = dict(
            ingest_school.canonical_enrichment_candidates(
                source, canonical, metadata
            )
        )
        self.assertEqual(changes["venue_key"], "example-arena")
        self.assertEqual(changes["site_city"], "Exampleville")
        self.assertEqual(changes["site_state"], "EX")
        self.assertNotIn("site_type", changes)
        markers = parse_registry_fallback_markers(changes["notes"])
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0]["source_game_id"], "NEW-0001")
        self.assertEqual(markers[0]["venue_key"], "example-arena")
        self.assertEqual(markers[0]["site_type"], "NEUTRAL")

    def test_registry_cannot_establish_site_type(self):
        source = source_row()
        source["curated_site_type"] = "UNKNOWN"
        canonical = {
            "site_type": "UNKNOWN",
            "venue_key": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "city": "Exampleville",
                "state": "EX",
            }
        }
        self.assertEqual(
            ingest_school.canonical_enrichment_candidates(
                source, canonical, metadata
            ),
            [],
        )

    def test_partial_source_location_is_not_completed_from_registry(self):
        source = source_row("Exampleville", "")
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "city": "Exampleville",
                "state": "EX",
            }
        }
        changes = dict(
            ingest_school.canonical_enrichment_candidates(
                source, canonical, metadata
            )
        )
        self.assertNotIn("site_city", changes)
        self.assertNotIn("site_state", changes)


class SynchronizationAndPublicationTests(unittest.TestCase):
    def test_target_source_assertion_drift_is_detected(self):
        source = source_row("Exampleville", "EX")
        source.update(
            {
                "game_date": "2026-01-01",
                "event_or_tournament": "Original Event",
                "raw_text": "original",
            }
        )
        assertion = dict(source)
        assertion["city"] = "Elsewhere"
        assertion["event_or_tournament"] = "Changed Event"
        assertion["raw_text"] = "rewritten"
        drift = assertion_drift(source, assertion)
        self.assertEqual(
            set(drift), {"city", "event_or_tournament", "raw_text"}
        )

    def test_public_game_suppresses_partial_location_pair(self):
        row = {
            "canonical_game_id": "CBBG-TEST",
            "season_label": "2025-2026",
            "game_date": "2026-01-01",
            "date_precision": "EXACT",
            "team_a_key": "new-school",
            "team_b_key": "opponent",
            "team_a_score": "70",
            "team_b_score": "60",
            "result_winner_team_key": "new-school",
            "overtime_periods": "0",
            "site_type": "NEUTRAL",
            "designated_home_team_key": "",
            "venue_key": "example-arena",
            "site_city": "Exampleville",
            "site_state": "",
            "game_type": "REGULAR_SEASON",
            "postseason_round": "",
            "administrative_status": "",
            "administrative_note": "",
        }
        game = build_site_data.perspective_game(
            row,
            "new-school",
            {"opponent": "Opponent"},
            {"example-arena": "Example Arena"},
            {},
        )
        self.assertIsNone(game["site_city"])
        self.assertIsNone(game["site_state"])
        self.assertEqual(game["venue_name"], "Example Arena")

    def test_incompatible_shared_venue_locations_are_detected(self):
        conflicts = venue_location_conflicts(
            [
                ("schools/a/venues.csv", {"venue_key": "same", "city": "A", "state": "AA", "notes": ""}),
                ("schools/b/venues.csv", {"venue_key": "same", "city": "B", "state": "BB", "notes": ""}),
            ]
        )
        self.assertEqual(len(conflicts), 1)


if __name__ == "__main__":
    unittest.main()
