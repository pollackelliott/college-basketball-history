import sys
import unittest
from pathlib import Path


TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

import build_site_data  # noqa: E402
from conference_reference import (  # noqa: E402
    history_errors,
    matching_history_rows,
    resolved_history_key,
)


REGISTRY = {
    "independent": {
        "conference_key": "independent",
        "conference_name": "Independent",
        "tournament_label": "",
    },
    "sec": {
        "conference_key": "sec",
        "conference_name": "SEC",
        "tournament_label": "SEC",
    },
    "siaa": {
        "conference_key": "siaa",
        "conference_name": "Southern Intercollegiate Athletic Association",
        "tournament_label": "SIAA",
    },
    "southern": {
        "conference_key": "southern",
        "conference_name": "Southern",
        "tournament_label": "Southern",
    },
}


def history_row(start, end, key):
    return {
        "source_program_key": "example",
        "start_season": start,
        "end_season": end,
        "conference_key": key,
        "conference_name": REGISTRY.get(key, {}).get("conference_name", key),
        "membership_type": "independent" if key == "independent" else "conference",
        "ongoing": "false" if end else "true",
        "basis": "test",
        "notes": "",
    }


class ConferenceHistoryTests(unittest.TestCase):
    def test_exactly_one_season_interval_resolves(self):
        rows = [
            history_row("1920-1921", "1931-1932", "southern"),
            history_row("1932-1933", "", "sec"),
        ]
        self.assertEqual(resolved_history_key(rows, "1921-1922"), "southern")
        self.assertEqual(resolved_history_key(rows, "2025-2026"), "sec")

    def test_zero_multiple_and_independent_do_not_resolve(self):
        self.assertIsNone(
            resolved_history_key(
                [history_row("1900-1901", "1910-1911", "sec")],
                "1920-1921",
            )
        )
        overlap = [
            history_row("1900-1901", "1920-1921", "sec"),
            history_row("1910-1911", "1930-1931", "southern"),
        ]
        self.assertEqual(len(matching_history_rows(overlap, "1915-1916")), 2)
        self.assertIsNone(resolved_history_key(overlap, "1915-1916"))
        self.assertIsNone(
            resolved_history_key(
                [history_row("1900-1901", "1920-1921", "independent")],
                "1915-1916",
            )
        )

    def test_explicit_one_season_dual_membership_preserves_both(self):
        notes = (
            "Concurrent dual conference membership in the institution's "
            "inaugural season; supported by its official affiliation history."
        )
        rows = [
            dict(
                history_row("1916-1917", "1916-1917", "sec"),
                notes=notes,
                basis="Official institutional conference-affiliation chronology.",
            ),
            dict(
                history_row("1916-1917", "1916-1917", "southern"),
                notes=notes,
                basis="Official institutional conference-affiliation chronology.",
            ),
            history_row("1917-1918", "1921-1922", "independent"),
        ]
        self.assertEqual(
            history_errors(rows, set(REGISTRY), expected_program_key="example"),
            [],
        )
        self.assertEqual(len(matching_history_rows(rows, "1916-1917")), 2)
        # Never assign an arbitrary single conference to games when two exist.
        self.assertIsNone(resolved_history_key(rows, "1916-1917"))
        self.assertIsNone(resolved_history_key(rows, "1917-1918"))

    def test_undocumented_same_season_overlap_still_fails(self):
        annotated = dict(
            history_row("1916-1917", "1916-1917", "sec"),
            notes="Concurrent dual conference membership, independently documented.",
        )
        unannotated = history_row("1916-1917", "1916-1917", "southern")
        problems = history_errors([annotated, unannotated], set(REGISTRY))
        self.assertEqual(len(problems), 1)
        self.assertIn("conference-history intervals overlap", problems[0])

    def test_dual_membership_requires_two_distinct_conferences_and_sources(self):
        note = "Concurrent dual conference membership documented by official source."
        first = dict(history_row("1916-1917", "1916-1917", "sec"), notes=note)
        same_conference = dict(first)
        self.assertTrue(
            any(
                "conference-history intervals overlap" in problem
                for problem in history_errors([first, same_conference], set(REGISTRY))
            )
        )
        second = dict(
            history_row("1916-1917", "1916-1917", "southern"), notes=note,
            basis="",
        )
        self.assertTrue(
            any(
                "conference-history intervals overlap" in problem
                for problem in history_errors([first, second], set(REGISTRY))
            )
        )

    def test_dual_note_cannot_waive_longer_overlaps_or_three_memberships(self):
        note = "Concurrent dual conference membership documented by official source."
        two_season = [
            dict(history_row("1916-1917", "1917-1918", "sec"), notes=note),
            dict(history_row("1916-1917", "1917-1918", "southern"), notes=note),
        ]
        self.assertTrue(history_errors(two_season, set(REGISTRY)))
        three = [
            dict(history_row("1916-1917", "1916-1917", key), notes=note)
            for key in ("sec", "southern", "siaa")
        ]
        self.assertTrue(history_errors(three, set(REGISTRY)))
        independent = [
            dict(history_row("1916-1917", "1916-1917", key), notes=note)
            for key in ("sec", "independent")
        ]
        self.assertTrue(history_errors(independent, set(REGISTRY)))
        open_ended = [
            dict(history_row("1916-1917", "", "sec"), notes=note),
            dict(history_row("1917-1918", "", "southern"), notes=note),
        ]
        self.assertTrue(history_errors(open_ended, set(REGISTRY)))

    def test_unknown_registry_identity_is_rejected(self):
        errors = history_errors(
            [history_row("2000-2001", "", "unknown-league")],
            set(REGISTRY),
            expected_program_key="example",
        )
        self.assertEqual(len(errors), 1)
        self.assertIn("stop for owner review", errors[0])


class ConferencePublicationTests(unittest.TestCase):
    def test_conflicting_event_is_review_only_and_membership_stays_controlling(self):
        history = [history_row("1921-1922", "1931-1932", "southern")]
        games = [
            {
                "canonical_game_id": "CBBG-TEST",
                "season_label": "1921-1922",
                "game_type": "CONFERENCE_TOURNAMENT",
            }
        ]
        assertions = [
            {
                "canonical_game_id": "CBBG-TEST",
                "source_program_key": "example",
                "curated_game_type": "CONFERENCE_TOURNAMENT",
                "event_or_tournament": "SIAA Tournament",
            }
        ]
        metadata = build_site_data.conference_publication_metadata(
            "example", history, REGISTRY, games, assertions
        )
        self.assertEqual(
            set(metadata),
            {
                "conference_history",
                "conference_names",
                "conference_tournament_labels",
                "conference_tournament_review_flags",
            },
        )
        self.assertEqual(metadata["conference_names"], {"southern": "Southern"})
        self.assertEqual(metadata["conference_tournament_labels"], {"southern": "Southern"})
        self.assertEqual(
            metadata["conference_tournament_review_flags"],
            [
                {
                    "canonical_game_id": "CBBG-TEST",
                    "membership_conference_key": "southern",
                    "conflicting_event_conference_keys": ["siaa"],
                    "source_events": ["SIAA Tournament"],
                }
            ],
        )
        self.assertEqual(len(metadata["conference_history"]), 1)

    def test_matching_event_creates_no_review_flag(self):
        metadata = build_site_data.conference_publication_metadata(
            "example",
            [history_row("2000-2001", "", "sec")],
            REGISTRY,
            [
                {
                    "canonical_game_id": "CBBG-TEST",
                    "season_label": "2025-2026",
                    "game_type": "CONFERENCE_TOURNAMENT",
                }
            ],
            [
                {
                    "canonical_game_id": "CBBG-TEST",
                    "source_program_key": "example",
                    "curated_game_type": "CONFERENCE_TOURNAMENT",
                    "event_or_tournament": "SEC Tournament",
                }
            ],
        )
        self.assertEqual(metadata["conference_tournament_review_flags"], [])

    def test_other_schools_assertions_are_ignored(self):
        metadata = build_site_data.conference_publication_metadata(
            "example",
            [history_row("2000-2001", "", "sec")],
            REGISTRY,
            [
                {
                    "canonical_game_id": "CBBG-TEST",
                    "season_label": "2025-2026",
                    "game_type": "CONFERENCE_TOURNAMENT",
                }
            ],
            [
                {
                    "canonical_game_id": "CBBG-TEST",
                    "source_program_key": "other-school",
                    "curated_game_type": "CONFERENCE_TOURNAMENT",
                    "event_or_tournament": "SIAA Tournament",
                }
            ],
        )
        self.assertEqual(metadata["conference_tournament_review_flags"], [])


if __name__ == "__main__":
    unittest.main()
