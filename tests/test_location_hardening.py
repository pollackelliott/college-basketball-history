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
    registry_fallback_marker,
    retire_site_mismatched_registry_fallbacks,
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
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "venue_id": "VEN-EXAMPLE",
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
        self.assertEqual(changes["venue_id"], "VEN-EXAMPLE")
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
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "venue_id": "VEN-EXAMPLE",
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

    def test_conflicting_registry_venue_is_not_added_to_known_canonical_geography(self):
        source = source_row("Atlanta", "GA")
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "",
            "venue_id": "",
            "site_city": "Nashville",
            "site_state": "TN",
            "notes": "",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "venue_id": "VEN-EXAMPLE",
                "city": "Atlanta",
                "state": "GA",
            }
        }

        changes = dict(
            ingest_school.canonical_enrichment_candidates(
                source, canonical, metadata
            )
        )

        self.assertNotIn("venue_key", changes)
        self.assertNotIn("venue_id", changes)
        self.assertNotIn("site_city", changes)
        self.assertNotIn("site_state", changes)

    def test_partial_source_location_is_not_completed_from_registry(self):
        source = source_row("Exampleville", "")
        canonical = {
            "site_type": "NEUTRAL",
            "venue_key": "",
            "venue_id": "",
            "site_city": "",
            "site_state": "",
            "notes": "",
        }
        metadata = {
            "example arena": {
                "venue_key": "example-arena",
                "venue_id": "VEN-EXAMPLE",
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
            "venue_id": "VEN-EXAMPLE",
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
            {"VEN-EXAMPLE": "Example Arena"},
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


class RegistryFallbackLifecycleTests(unittest.TestCase):
    def test_site_change_retires_only_mismatched_fallback_marker(self):
        stale = registry_fallback_marker(
            "old-school",
            "OLD-0001",
            "old-arena",
            "TEAM_B_HOME",
            ["venue_key"],
        )
        current = registry_fallback_marker(
            "new-school",
            "NEW-0001",
            "new-arena",
            "TEAM_A_HOME",
            ["venue_key"],
        )
        notes = f"Historical note. {stale} {current}"

        cleaned, retired = retire_site_mismatched_registry_fallbacks(
            notes,
            "TEAM_A_HOME",
        )

        self.assertEqual(retired, 1)
        self.assertTrue(cleaned.startswith("Historical note."))
        markers = parse_registry_fallback_markers(cleaned)
        self.assertEqual(len(markers), 1)
        self.assertEqual(markers[0]["source_program_key"], "new-school")
        self.assertEqual(markers[0]["source_game_id"], "NEW-0001")
        self.assertEqual(markers[0]["site_type"], "TEAM_A_HOME")

    def test_matching_fallback_marker_is_preserved(self):
        marker = registry_fallback_marker(
            "source-school",
            "SRC-0001",
            "example-arena",
            "NEUTRAL",
            ["venue_key", "site_city", "site_state"],
        )
        notes = f"Existing narrative. {marker}"

        cleaned, retired = retire_site_mismatched_registry_fallbacks(
            notes,
            "NEUTRAL",
        )

        self.assertEqual(retired, 0)
        self.assertEqual(cleaned, notes)


if __name__ == "__main__":
    unittest.main()
