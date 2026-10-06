import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from site_completeness import (  # noqa: E402
    source_home_chronology_report,
    source_site_completeness_report,
)


FIELDS = [
    "source_game_id",
    "season_label",
    "curated_site_type",
    "source_venue_name",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "site_research_status",
    "site_research_basis",
]


def row(**overrides):
    value = {
        "source_game_id": "TESTRAW-00001",
        "season_label": "2025-2026",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "source_venue_name": "",
        "curated_venue_name": "Example Arena",
        "city": "Example City",
        "state": "EX",
        "curated_game_type": "REGULAR_SEASON",
        "site_research_status": "",
        "site_research_basis": "",
    }
    value.update(overrides)
    return value


class SourceSiteCompletenessTests(unittest.TestCase):
    def test_complete_home_row_has_no_material_gap(self):
        report = source_site_completeness_report(FIELDS, [row()])
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["material_gap_rows"], 0)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 0)

    def test_unaccounted_home_blank_blocks(self):
        report = source_site_completeness_report(
            FIELDS,
            [row(curated_venue_name="", city="", state="")],
        )
        self.assertEqual(report["counts"]["material_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 1)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)
        self.assertEqual(report["counts"]["home_missing_venue"], 1)
        self.assertEqual(report["counts"]["home_missing_location"], 1)
        self.assertEqual(report["counts"]["home_missing_both"], 1)
        self.assertTrue(any("material site-gap" in error for error in report["errors"]))

    def test_ordinary_researched_unresolved_home_blank_still_blocks_freeze(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    city="",
                    state="",
                    site_research_status="RESEARCHED_UNRESOLVED",
                    site_research_basis=(
                        "Primary ledger and facility chronology checked; exact site unsupported."
                    ),
                )
            ],
        )
        self.assertEqual(report["counts"]["researched_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)
        self.assertTrue(any("ordinary" in error.lower() for error in report["errors"]))

    def test_dedicated_researched_unresolved_home_venue_exception_passes_source_gate(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    city="Starkville",
                    state="MS",
                    site_research_status="RESEARCHED_UNRESOLVED_HOME_VENUE",
                    site_research_basis=(
                        "Official record book, institutional facility history, reciprocal "
                        "published evidence, and archival sources reviewed; exact physical "
                        "home venue identity is not supported by the surviving record."
                    ),
                )
            ],
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["material_gap_rows"], 1)
        self.assertEqual(report["counts"]["researched_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 0)
        self.assertEqual(report["counts"]["researched_unresolved_home_venue_rows"], 1)
        self.assertEqual(report["counts"]["home_missing_venue"], 1)
        self.assertNotIn("home_missing_location", report["counts"])

    def test_dedicated_home_venue_exception_cannot_waive_location(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    city="Starkville",
                    state="",
                    site_research_status="RESEARCHED_UNRESOLVED_HOME_VENUE",
                    site_research_basis="Exact physical venue remains unsupported after research.",
                )
            ],
        )
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)
        self.assertEqual(report["counts"]["researched_unresolved_home_venue_rows"], 0)
        self.assertTrue(
            any("RESEARCHED_UNRESOLVED_HOME_VENUE is valid only" in error for error in report["errors"])
        )

    def test_partial_home_gap_still_blocks_freeze(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    site_research_status="RESEARCHED_PARTIAL",
                    site_research_basis=(
                        "Official schedule establishes Norman, Oklahoma; exact building unresolved."
                    ),
                )
            ],
        )
        self.assertEqual(report["counts"]["home_missing_venue"], 1)
        self.assertNotIn("home_missing_location", report["counts"])
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 1)

    def test_unknown_site_type_requires_accounting(self):
        report = source_site_completeness_report(
            FIELDS,
            [row(curated_site_type="UNKNOWN")],
        )
        self.assertEqual(report["counts"]["unknown_site_type"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 1)

    def test_away_regular_season_blank_is_not_a_research_freeze_gap(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="OPPONENT_HOME",
                    source_venue_name="",
                    curated_venue_name="",
                    city="",
                    state="",
                )
            ],
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["material_gap_rows"], 0)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 0)

    def test_explicit_opponent_home_source_venue_cannot_disappear_silently(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="OPPONENT_HOME",
                    source_venue_name="Opponent Arena",
                    curated_venue_name="",
                    city="",
                    state="",
                )
            ],
        )
        self.assertEqual(report["counts"]["material_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 1)
        self.assertEqual(
            report["counts"]["opponent_home_source_venue_unpreserved"],
            1,
        )
        self.assertEqual(
            report["counts"]["opponent_home_source_site_location_missing"],
            1,
        )

    def test_ambiguous_explicit_opponent_home_evidence_can_be_accounted(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="OPPONENT_HOME",
                    source_venue_name="Armory",
                    curated_venue_name="",
                    city="",
                    state="",
                    site_research_status="RESEARCHED_PARTIAL",
                    site_research_basis=(
                        "Target source preserves the literal venue label, but the "
                        "physical identity/locality is ambiguous; no opponent-home "
                        "archaeology was opened."
                    ),
                )
            ],
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["material_gap_rows"], 1)
        self.assertEqual(report["counts"]["researched_gap_rows"], 1)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)

    def test_non_ncaa_neutral_and_postseason_gaps_are_counted(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="NEUTRAL",
                    curated_venue_name="",
                    city="",
                    state="",
                    curated_game_type="NIT",
                    site_research_status="RESEARCHED_UNRESOLVED",
                    site_research_basis="NIT site sources checked; exact historical site unsupported.",
                )
            ],
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["neutral_missing_venue"], 1)
        self.assertEqual(report["counts"]["neutral_missing_location"], 1)
        self.assertEqual(report["counts"]["postseason_missing_venue"], 1)
        self.assertEqual(report["counts"]["postseason_missing_location"], 1)
        self.assertEqual(report["counts"]["material_gap_rows"], 1)

    def test_ncaa_neutral_blank_is_not_waivable_here(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_site_type="NEUTRAL",
                    curated_venue_name="",
                    city="",
                    state="",
                    curated_game_type="NCAA_TOURNAMENT",
                    site_research_status="RESEARCHED_UNRESOLVED",
                    site_research_basis="This marker must not substitute for the strict NCAA gate.",
                )
            ],
        )
        self.assertEqual(report["counts"]["material_gap_rows"], 0)
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 0)
        self.assertEqual(len(report["warnings"]), 1)

    def test_status_and_basis_must_be_paired(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    curated_venue_name="",
                    site_research_status="RESEARCHED_PARTIAL",
                    site_research_basis="",
                )
            ],
        )
        self.assertTrue(any("site_research_basis is required" in error for error in report["errors"]))
        self.assertEqual(report["counts"]["unaccounted_gap_rows"], 1)

    def test_decade_breakdown_exposes_chronology_holes(self):
        report = source_site_completeness_report(
            FIELDS,
            [
                row(
                    source_game_id="A",
                    season_label="1907-1908",
                    curated_venue_name="",
                    city="",
                    state="",
                ),
                row(
                    source_game_id="B",
                    season_label="1975-1976",
                    curated_venue_name="",
                    city="",
                    state="",
                ),
            ],
        )
        self.assertEqual(report["by_decade"]["home_missing_both"]["1900s"], 1)
        self.assertEqual(report["by_decade"]["home_missing_both"]["1970s"], 1)
        self.assertEqual(report["counts"]["home_publication_blocker_rows"], 2)



class HomeChronologyChallengeTests(unittest.TestCase):
    def venue(
        self,
        name,
        relationship_type="",
        start="",
        end="",
        aliases="",
        site_rule="",
        notes="",
    ):
        return {
            "source_program_key": "test",
            "canonical_name": name,
            "aliases": aliases,
            "relationship_type": relationship_type,
            "relationship_start": start,
            "relationship_end": end,
            "site_rule": site_rule,
            "notes": notes,
        }

    def home_game(self, venue_name, game_date="2026-01-15"):
        return row(
            source_game_id="HOME-1",
            season_label="2025-2026",
            game_date=game_date,
            curated_site_type="SOURCE_PROGRAM_HOME",
            curated_venue_name=venue_name,
            city="Example City",
            state="EX",
        )

    def test_primary_home_relationship_passes(self):
        report = source_home_chronology_report(
            [self.home_game("Example Arena")],
            [
                self.venue(
                    "Example Arena",
                    "primary_home",
                    "2020-11-01",
                    "2030-03-31",
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 0)

    def test_documented_alternate_home_exception_passes(self):
        report = source_home_chronology_report(
            [self.home_game("Downtown Arena")],
            [
                self.venue("Example Arena", "primary_home", "2020-11-01", "2030-03-31"),
                self.venue(
                    "Downtown Arena",
                    "alternate_home",
                    "2026-01-15",
                    "2026-01-15",
                ),
            ],
            school_key="test",
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 0)

    def test_documented_later_home_exception_on_same_venue_row_passes(self):
        report = source_home_chronology_report(
            [self.home_game("Legacy Arena", "2000-12-07")],
            [
                self.venue(
                    "Legacy Arena",
                    "PRIMARY_HOME_WITH_LATER_EXCEPTIONS",
                    "1950-11-01",
                    "1988-03-12",
                    site_rule=(
                        "Primary HOME through 1988; later HOME exceptions: "
                        "1998-12-01; 1999-12-07; 1999-12-29; "
                        "2000-12-07; 2002-01-02."
                    ),
                    notes=(
                        "Accepted institutional facility chronology; exact "
                        "listed exception dates override the primary interval."
                    ),
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 0)

    def test_unlisted_date_still_fails_exception_relationship(self):
        report = source_home_chronology_report(
            [self.home_game("Legacy Arena", "2000-12-08")],
            [
                self.venue(
                    "Legacy Arena",
                    "PRIMARY_HOME_WITH_LATER_EXCEPTIONS",
                    "1950-11-01",
                    "1988-03-12",
                    site_rule="Later HOME exception: 2000-12-07.",
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 1)

    def test_date_in_ordinary_home_notes_does_not_waive_chronology(self):
        report = source_home_chronology_report(
            [self.home_game("Legacy Arena", "2000-12-07")],
            [
                self.venue(
                    "Legacy Arena",
                    "primary_home",
                    "1950-11-01",
                    "1988-03-12",
                    notes=(
                        "Research note mentions 2000-12-07, but this "
                        "relationship does not declare an exception topology."
                    ),
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 1)

    def test_per_game_home_support_passes_without_interval(self):
        report = source_home_chronology_report(
            [self.home_game("Mixed Use Arena", "1981-03-07")],
            [
                self.venue(
                    "Mixed Use Arena",
                    site_rule=(
                        "Per-game accepted venue assignment; venue identity "
                        "does not establish H/A/N."
                    ),
                    notes=(
                        "Venue can host SOURCE_PROGRAM_HOME and explicitly "
                        "NEUTRAL games; accepted assignments are game-level."
                    ),
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["chronology_rows"], 1)
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 0)

    def test_hybrid_home_interval_and_per_game_support_passes_outside_interval(self):
        report = source_home_chronology_report(
            [
                self.home_game("Hybrid Arena", "1979-02-28"),
                self.home_game("Hybrid Arena", "1990-01-15"),
            ],
            [
                self.venue(
                    "Hybrid Arena",
                    "source_program_home",
                    "1983-1984",
                    "1999-2000",
                    site_rule=(
                        "Per-game accepted regular-season HOME assignment; "
                        "venue identity does not establish H/A/N."
                    ),
                    notes=(
                        "Earlier SOURCE_PROGRAM_HOME assignments remain accepted "
                        "at game level; the continuous interval documents the later "
                        "primary HOME era."
                    ),
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"]["chronology_rows"], 1)
        self.assertEqual(report["counts"]["home_rows_checked"], 2)
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 0)

    def test_per_game_home_wording_without_accepted_semantics_still_fails(self):
        report = source_home_chronology_report(
            [self.home_game("Hybrid Arena", "1979-02-28")],
            [
                self.venue(
                    "Hybrid Arena",
                    "source_program_home",
                    "1983-1984",
                    "1999-2000",
                    site_rule=(
                        "Per-game proposed regular-season HOME assignment; "
                        "venue identity does not establish H/A/N."
                    ),
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 1)

    def test_home_interval_without_per_game_rule_still_blocks_outside_interval(self):
        report = source_home_chronology_report(
            [self.home_game("Hybrid Arena", "1979-02-28")],
            [
                self.venue(
                    "Hybrid Arena",
                    "source_program_home",
                    "1983-1984",
                    "1999-2000",
                    notes=(
                        "Primary HOME relationship is limited to the documented "
                        "continuous interval."
                    ),
                )
            ],
            school_key="test",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 1)

    def test_per_game_rule_without_explicit_home_authority_still_fails(self):
        report = source_home_chronology_report(
            [self.home_game("Neutral Event Arena", "1981-03-07")],
            [
                self.venue(
                    "Neutral Event Arena",
                    site_rule="Per-game accepted venue assignment.",
                    notes="Accepted neutral-event assignments only.",
                ),
                self.venue(
                    "Example Arena",
                    "primary_home",
                    "2020-11-01",
                    "2030-03-31",
                ),
            ],
            school_key="test",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 1)

    def test_exact_home_venue_outside_documented_chronology_is_flagged_only(self):
        game = self.home_game("Opponent Gym")
        report = source_home_chronology_report(
            [game],
            [
                self.venue("Example Arena", "primary_home", "2020-11-01", "2030-03-31"),
                self.venue("Opponent Gym"),
            ],
            school_key="test",
        )
        self.assertEqual(report["counts"]["home_chronology_conflicts"], 1)
        self.assertTrue(any("adversarial review signal only" in e for e in report["errors"]))
        self.assertEqual(game["curated_site_type"], "SOURCE_PROGRAM_HOME")


if __name__ == "__main__":
    unittest.main()
