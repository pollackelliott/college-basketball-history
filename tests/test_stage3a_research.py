import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from stage3a_research import (  # noqa: E402
    apply_sparse_updates,
    canonical_neutral_lookup,
    stage3a_state_report,
)


FIELDS = [
    "research_game_id",
    "source_program_key",
    "season_label",
    "game_date",
    "normalized_opponent_key",
    "stage3a_disposition",
    "stage3a_han",
    "stage3a_han_basis",
    "stage3a_venue_name",
    "stage3a_city",
    "stage3a_state",
    "stage3a_site_research_status",
    "stage3a_site_research_basis",
    "stage3a_boundary_correction",
    "stage3a_next_action",
]


def row(gid, **overrides):
    value = {
        "research_game_id": gid,
        "source_program_key": "cincinnati",
        "season_label": "1994-1995",
        "game_date": "1994-12-01",
        "normalized_opponent_key": "iowa",
        "stage3a_disposition": "REGULAR_SEASON",
        "stage3a_han": "HOME",
        "stage3a_han_basis": "fixture H/A/N evidence",
        "stage3a_venue_name": "Shoemaker Center",
        "stage3a_city": "Cincinnati",
        "stage3a_state": "OH",
        "stage3a_site_research_status": "",
        "stage3a_site_research_basis": "fixture site evidence",
        "stage3a_boundary_correction": "",
        "stage3a_next_action": "NONE",
    }
    value.update(overrides)
    return value


class Stage3AStateTests(unittest.TestCase):
    def test_clean_mixed_state_is_complete(self):
        rows = [
            row("A"),
            row(
                "B",
                stage3a_han="OPPONENT_HOME",
                stage3a_venue_name="",
                stage3a_city="",
                stage3a_state="",
                stage3a_site_research_basis="",
                stage3a_next_action="NO_SOURCE_SCHOOL_VENUE_RESEARCH",
            ),
            row(
                "C",
                stage3a_han="NEUTRAL",
                stage3a_venue_name="Chicago Stadium",
                stage3a_city="Chicago",
                stage3a_state="IL",
            ),
            row(
                "D",
                season_label="1950-1951",
                stage3a_han="NEUTRAL",
                stage3a_venue_name="",
                stage3a_city="Toledo",
                stage3a_state="OH",
                stage3a_site_research_status="RESEARCHED_PARTIAL",
                stage3a_site_research_basis="City proven; building unsupported after event research.",
            ),
            row(
                "E",
                stage3a_disposition="POSTSEASON_HANDOFF",
                stage3a_han="",
                stage3a_venue_name="",
                stage3a_city="",
                stage3a_state="",
                stage3a_site_research_basis="",
                stage3a_next_action="POSTSEASON_HANDOFF",
            ),
        ]
        universe = [{"research_game_id": r["research_game_id"]} for r in rows]
        report = stage3a_state_report(["research_game_id"], universe, FIELDS, rows)
        self.assertTrue(report["complete"])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["regular_season_rows"], 4)
        self.assertEqual(report["counts"]["postseason_handoff_rows"], 1)
        self.assertEqual(report["counts"]["historical_neutral_unresolved_rows"], 1)

    def test_active_action_is_healthy_but_incomplete(self):
        rows = [
            row(
                "A",
                stage3a_venue_name="",
                stage3a_city="",
                stage3a_state="",
                stage3a_next_action="RESEARCH_HOME_VENUE",
            )
        ]
        universe = [{"research_game_id": "A"}]
        report = stage3a_state_report(["research_game_id"], universe, FIELDS, rows)
        self.assertFalse(report["complete"])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["active_action_rows"], 1)

    def test_universe_mismatch_is_error(self):
        report = stage3a_state_report(
            ["research_game_id"],
            [{"research_game_id": "A"}, {"research_game_id": "B"}],
            FIELDS,
            [row("A")],
        )
        self.assertFalse(report["complete"])
        self.assertTrue(any("missing 1 Stage 1 IDs" in error for error in report["errors"]))

    def test_home_blank_requires_dedicated_exception_when_terminal(self):
        rows = [
            row(
                "A",
                season_label="1920-21",
                stage3a_venue_name="",
                stage3a_city="Cincinnati",
                stage3a_state="OH",
                stage3a_site_research_status="RESEARCHED_UNRESOLVED_HOME_VENUE",
                stage3a_site_research_basis="Institutional and archival facility evidence exhausted.",
            )
        ]
        report = stage3a_state_report(
            ["research_game_id"], [{"research_game_id": "A"}], FIELDS, rows
        )
        self.assertTrue(report["complete"])
        self.assertEqual(report["counts"]["home_researched_unresolved_venue_rows"], 1)

    def test_exact_home_requires_site_provenance(self):
        rows = [row("A", stage3a_site_research_basis="")]
        report = stage3a_state_report(
            ["research_game_id"], [{"research_game_id": "A"}], FIELDS, rows
        )
        self.assertFalse(report["complete"])
        self.assertTrue(any("missing stage3a_site_research_basis" in error for error in report["errors"]))

    def test_regular_row_requires_han_basis(self):
        rows = [row("A", stage3a_han_basis="")]
        report = stage3a_state_report(
            ["research_game_id"], [{"research_game_id": "A"}], FIELDS, rows
        )
        self.assertFalse(report["complete"])
        self.assertTrue(any("missing stage3a_han_basis" in error for error in report["errors"]))

    def test_postseason_handoff_must_match_disposition_exactly(self):
        rows = [
            row("A"),
            row(
                "B",
                stage3a_disposition="POSTSEASON_HANDOFF",
                stage3a_han="",
                stage3a_venue_name="",
                stage3a_city="",
                stage3a_state="",
                stage3a_next_action="POSTSEASON_HANDOFF",
            ),
        ]
        universe = [{"research_game_id": "A"}, {"research_game_id": "B"}]
        report = stage3a_state_report(
            ["research_game_id"],
            universe,
            FIELDS,
            rows,
            handoff_fields=["research_game_id"],
            handoff=[{"research_game_id": "A"}],
        )
        self.assertFalse(report["complete"])
        self.assertTrue(any("handoff ID set differs" in error for error in report["errors"]))


class NeutralLookupTests(unittest.TestCase):
    def test_exact_canonical_neutral_candidate_is_read_only(self):
        ledger = [
            row(
                "A",
                stage3a_han="NEUTRAL",
                stage3a_venue_name="",
                stage3a_city="",
                stage3a_state="",
                stage3a_next_action="RESEARCH_NEUTRAL_VENUE",
            )
        ]
        canonical = [
            {
                "canonical_game_id": "CBBG-1",
                "game_date": "1994-12-01",
                "team_a_key": "cincinnati",
                "team_b_key": "iowa",
                "site_type": "NEUTRAL",
                "venue_key": "chicago-stadium",
                "venue_id": "VEN-1",
                "site_city": "Chicago",
                "site_state": "IL",
                "canonical_status": "PUBLISHED",
                "notes": "fixture",
            }
        ]
        venues = [
            {
                "venue_id": "VEN-1",
                "venue_key": "chicago-stadium",
                "display_name": "Chicago Stadium",
                "city": "Chicago",
                "state": "IL",
            }
        ]
        result = canonical_neutral_lookup(ledger, canonical, venues)
        self.assertEqual(result[0]["lookup_status"], "EXACT_VENUE_CANDIDATE")
        self.assertEqual(result[0]["canonical_venue_name"], "Chicago Stadium")
        self.assertEqual(ledger[0]["stage3a_venue_name"], "")

    def test_canonical_home_claim_surfaces_as_contradiction_not_override(self):
        ledger = [
            row(
                "A",
                stage3a_han="NEUTRAL",
                stage3a_venue_name="",
                stage3a_city="",
                stage3a_state="",
            )
        ]
        canonical = [
            {
                "canonical_game_id": "CBBG-1",
                "game_date": "1994-12-01",
                "team_a_key": "cincinnati",
                "team_b_key": "iowa",
                "site_type": "TEAM_A_HOME",
                "venue_key": "",
                "venue_id": "",
                "site_city": "Cincinnati",
                "site_state": "OH",
                "canonical_status": "PUBLISHED",
                "notes": "fixture",
            }
        ]
        result = canonical_neutral_lookup(ledger, canonical, [])
        self.assertEqual(result[0]["lookup_status"], "H_A_N_CONTRADICTION")
        self.assertEqual(result[0]["canonical_han_for_source"], "HOME")


class ApplyUpdatesTests(unittest.TestCase):
    def test_sparse_updates_write_through_and_support_clear(self):
        ledger = [row("A", stage3a_boundary_correction="old")]
        updates = [
            {
                "research_game_id": "A",
                "stage3a_venue_name": "Chicago Stadium",
                "stage3a_city": "Chicago",
                "stage3a_state": "IL",
                "stage3a_boundary_correction": "__CLEAR__",
            }
        ]
        out, report = apply_sparse_updates(FIELDS, ledger, list(updates[0]), updates)
        self.assertEqual(out[0]["stage3a_venue_name"], "Chicago Stadium")
        self.assertEqual(out[0]["stage3a_boundary_correction"], "")
        self.assertEqual(report["changed_rows"], 1)


if __name__ == "__main__":
    unittest.main()
