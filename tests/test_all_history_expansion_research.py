import csv
import copy
import sys
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import all_history_expansion_research as expansion  # noqa: E402
from all_history_expansion_research import (  # noqa: E402
    BASELINE_PUBLISHED,
    EXPANSION_REQUIRED,
    PRE_INCEPTION,
    ExpansionResearchAuthorityError,
    expansion_season_disposition,
    project_complete_institutional_program_row,
    validate_expansion_baseline_program,
)


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def season(start):
    return f"{start:04d}-{start + 1:04d}"


def legacy_program(**overrides):
    row = {
        "program_key": "legacy",
        "program_name": "Legacy",
        "display_name": "Legacy",
        "public_page_enabled": "Yes",
        "program_inception_season": "",
        "history_coverage_status": "LEGACY_TOP_LEVEL_ONLY",
        "history_start_season": "1970-1971",
        "history_scope_status": "OWNER_CONFIRMED",
        "history_scope_basis": "FIRST_TOP_LEVEL_SEASON",
        "history_scope_notes": "Accepted legacy top-level scope.",
        "history_scope_intervals": "",
        "custom_field": "preserve exactly",
    }
    row.update(overrides)
    return row


class AllHistoryExpansionResearchTests(unittest.TestCase):
    def test_published_legacy_target_is_eligible(self):
        self.assertIsNone(validate_expansion_baseline_program(legacy_program()))

    def test_complete_institutional_target_is_rejected(self):
        row = legacy_program(
            history_coverage_status="COMPLETE_INSTITUTIONAL",
            program_inception_season="1930-1931",
        )
        with self.assertRaises(ExpansionResearchAuthorityError):
            validate_expansion_baseline_program(row)

    def test_unmigrated_target_is_rejected(self):
        with self.assertRaises(ExpansionResearchAuthorityError):
            validate_expansion_baseline_program(
                legacy_program(history_coverage_status="UNMIGRATED")
            )

    def test_unpublished_legacy_target_is_rejected(self):
        with self.assertRaises(ExpansionResearchAuthorityError):
            validate_expansion_baseline_program(
                legacy_program(public_page_enabled="No")
            )

    def test_simple_scope_classifies_pre_d1_delta_and_baseline(self):
        row = legacy_program()
        for year in range(1930, 1970):
            self.assertEqual(
                expansion_season_disposition(
                    season(year),
                    row,
                    "1930-1931",
                ),
                EXPANSION_REQUIRED,
                year,
            )
        for year in (1970, 1971, 2000, 2026):
            self.assertEqual(
                expansion_season_disposition(
                    season(year),
                    row,
                    "1930-1931",
                ),
                BASELINE_PUBLISHED,
                year,
            )

    def test_season_before_researched_inception_is_pre_inception(self):
        self.assertEqual(
            expansion_season_disposition(
                "1929-1930",
                legacy_program(),
                "1930-1931",
            ),
            PRE_INCEPTION,
        )

    def test_interrupted_baseline_includes_early_and_internal_gap_delta(self):
        row = legacy_program(
            history_start_season="1928-1929",
            history_scope_basis="TOP_LEVEL_INTERVALS",
            history_scope_intervals=(
                "1928-1929..1950-1951|1968-1969+"
            ),
        )
        self.assertEqual(
            expansion_season_disposition("1920-1921", row, "1915-1916"),
            EXPANSION_REQUIRED,
        )
        self.assertEqual(
            expansion_season_disposition("1940-1941", row, "1915-1916"),
            BASELINE_PUBLISHED,
        )
        self.assertEqual(
            expansion_season_disposition("1951-1952", row, "1915-1916"),
            EXPANSION_REQUIRED,
        )
        self.assertEqual(
            expansion_season_disposition("1967-1968", row, "1915-1916"),
            EXPANSION_REQUIRED,
        )
        self.assertEqual(
            expansion_season_disposition("1968-1969", row, "1915-1916"),
            BASELINE_PUBLISHED,
        )

    def test_interrupted_history_is_not_collapsed_to_first_start_cutoff(self):
        row = legacy_program(
            history_start_season="1928-1929",
            history_scope_basis="TOP_LEVEL_INTERVALS",
            history_scope_intervals=(
                "1928-1929..1950-1951|1968-1969+"
            ),
        )
        self.assertGreater("1955-1956", row["history_start_season"])
        self.assertEqual(
            expansion_season_disposition("1955-1956", row, "1915-1916"),
            EXPANSION_REQUIRED,
        )

    def test_invalid_season_label_fails_closed(self):
        with self.assertRaises(ExpansionResearchAuthorityError):
            expansion_season_disposition(
                "1970-71",
                legacy_program(),
                "1930-1931",
            )

    def test_invalid_researched_inception_fails_closed(self):
        with self.assertRaises(ExpansionResearchAuthorityError):
            expansion_season_disposition(
                "1960-1961",
                legacy_program(),
                "1930-31",
            )

    def test_unknown_or_malformed_coverage_status_fails_closed(self):
        for status in ("", "UNKNOWN", "legacy_top_level_only"):
            with self.subTest(status=status):
                with self.assertRaises(ExpansionResearchAuthorityError):
                    validate_expansion_baseline_program(
                        legacy_program(history_coverage_status=status)
                    )

    def test_researched_inception_cannot_postdate_published_baseline(self):
        with self.assertRaises(ExpansionResearchAuthorityError):
            expansion_season_disposition(
                "1980-1981",
                legacy_program(),
                "1975-1976",
            )

    def test_existing_baseline_inception_must_not_conflict(self):
        with self.assertRaises(ExpansionResearchAuthorityError):
            project_complete_institutional_program_row(
                legacy_program(program_inception_season="1931-1932"),
                "1930-1931",
            )

    def test_projected_row_changes_exactly_two_fields(self):
        baseline = legacy_program()
        before = copy.deepcopy(baseline)
        projected = project_complete_institutional_program_row(
            baseline,
            "1930-1931",
        )
        changed = {
            key
            for key in set(baseline) | set(projected)
            if baseline.get(key) != projected.get(key)
        }
        self.assertEqual(
            changed,
            {"program_inception_season", "history_coverage_status"},
        )
        self.assertEqual(projected["program_inception_season"], "1930-1931")
        self.assertEqual(
            projected["history_coverage_status"],
            "COMPLETE_INSTITUTIONAL",
        )
        self.assertEqual(baseline, before)

    def test_projected_row_preserves_top_level_and_publication_authority(self):
        baseline = legacy_program(
            history_start_season="1928-1929",
            history_scope_basis="TOP_LEVEL_INTERVALS",
            history_scope_intervals=(
                "1928-1929..1950-1951|1968-1969+"
            ),
            history_scope_notes="Exact accepted interrupted scope.",
        )
        projected = project_complete_institutional_program_row(
            baseline,
            "1915-1916",
        )
        for field in (
            "history_start_season",
            "history_scope_intervals",
            "history_scope_status",
            "history_scope_basis",
            "history_scope_notes",
            "public_page_enabled",
        ):
            self.assertEqual(projected[field], baseline[field], field)

    def test_season_disposition_delegates_to_program_history_publication_helper(self):
        row = legacy_program()
        with mock.patch.object(
            expansion,
            "season_is_published_history",
            return_value=False,
        ) as published:
            self.assertEqual(
                expansion_season_disposition(
                    "1970-1971",
                    row,
                    "1930-1931",
                ),
                EXPANSION_REQUIRED,
            )
        published.assert_called_once_with("1970-1971", row)

    def test_module_does_not_reimplement_interval_or_top_level_logic(self):
        source = (
            ROOT / "tools/all_history_expansion_research.py"
        ).read_text(encoding="utf-8")
        self.assertIn("season_is_published_history", source)
        self.assertIn("history_coverage_errors", source)
        self.assertIn("history_scope_errors", source)
        self.assertNotIn("parse_history_scope_intervals", source)
        self.assertNotIn("season_is_top_level", source)

    def test_current_portfolio_expansion_eligibility_is_mechanical_and_read_only(self):
        programs = read_csv(ROOT / "data/reference/programs.csv")
        before = copy.deepcopy(programs)

        published = [
            row for row in programs
            if row["public_page_enabled"].strip() == "Yes"
        ]
        complete = [
            row for row in published
            if row["history_coverage_status"].strip()
            == "COMPLETE_INSTITUTIONAL"
        ]
        eligible = []
        for row in programs:
            try:
                validate_expansion_baseline_program(row)
            except ExpansionResearchAuthorityError:
                continue
            eligible.append(row)

        self.assertEqual(len(published), 113)
        self.assertEqual(len(eligible), 24)
        self.assertEqual(len(complete), 89)
        self.assertTrue(
            all(
                row["history_coverage_status"] == "LEGACY_TOP_LEVEL_ONLY"
                and row["public_page_enabled"] == "Yes"
                for row in eligible
            )
        )

        for row in complete:
            with self.assertRaises(ExpansionResearchAuthorityError):
                validate_expansion_baseline_program(row)

        for row in programs:
            if row["history_coverage_status"] == "UNMIGRATED":
                with self.assertRaises(ExpansionResearchAuthorityError):
                    validate_expansion_baseline_program(row)

        self.assertEqual(programs, before)


if __name__ == "__main__":
    unittest.main()
