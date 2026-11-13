"""Presentation-only regression checks for All-History team header semantics."""
import csv
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
PROGRAMS = json.loads(
    (ROOT / "site" / "data" / "programs.json").read_text(encoding="utf-8")
)["programs"]
with (ROOT / "data/reference/programs.csv").open(
    encoding="utf-8-sig", newline=""
) as handle:
    REFERENCE_PUBLIC = {
        row["program_key"]: row
        for row in csv.DictReader(handle)
        if row["public_page_enabled"] == "Yes"
    }


def helper_source():
    return SITE.split("function teamHistoryLabel(team) {", 1)[1].split(
        "\nfunction ", 1
    )[0]


class AllHistoryHeaderSemanticsTests(unittest.TestCase):
    def test_normalization_consumes_all_history_metadata_fields(self):
        normalize = SITE.split("function normalizeProgram(program) {", 1)[1].split(
            "\nfunction ", 1
        )[0]
        self.assertIn(
            "publishedHistoryStartSeason:\n"
            "      program.published_history_start_season\n"
            "      || program.history_start_season\n"
            '      || "",',
            normalize,
        )
        self.assertIn(
            'd1SinceSeason: program.d1_since_season || "",',
            normalize,
        )
        self.assertIn(
            'historyCoverageStatus: program.history_coverage_status || "",',
            normalize,
        )
        self.assertIn(
            'historyStartSeason: program.history_start_season || "",',
            normalize,
        )

    def test_complete_institutional_uses_institutional_since_semantics(self):
        helper = helper_source()
        self.assertIn("const published = team.publishedHistoryStartSeason;", helper)
        self.assertIn(
            'team.historyCoverageStatus === "LEGACY_TOP_LEVEL_ONLY"',
            helper,
        )
        self.assertIn('? "PUBLISHED SINCE"', helper)
        self.assertIn(': "SINCE";', helper)
        self.assertIn(
            "const labels = [`${prefix} ${formatSinceSeason(published)}`];",
            helper,
        )
        complete = [
            program for program in PROGRAMS
            if program.get("public_page_enabled")
            and program.get("history_coverage_status") == "COMPLETE_INSTITUTIONAL"
        ]
        self.assertEqual(
            len(complete),
            sum(row["history_coverage_status"] == "COMPLETE_INSTITUTIONAL"
                for row in REFERENCE_PUBLIC.values()),
        )
        self.assertTrue(
            all(program.get("published_history_start_season") for program in complete)
        )

    def test_legacy_uses_published_since_not_false_institutional_since(self):
        helper = helper_source()
        self.assertIn('? "PUBLISHED SINCE"', helper)
        self.assertNotIn("team.historyStartSeason", helper)
        legacy = [
            program for program in PROGRAMS
            if program.get("public_page_enabled")
            and program.get("history_coverage_status") == "LEGACY_TOP_LEVEL_ONLY"
        ]
        self.assertEqual(
            len(legacy),
            sum(row["history_coverage_status"] == "LEGACY_TOP_LEVEL_ONLY"
                for row in REFERENCE_PUBLIC.values()),
        )
        self.assertTrue(
            all(
                program.get("published_history_start_season")
                == program.get("history_start_season")
                for program in legacy
            )
        )

    def test_d1_since_is_appended_only_when_start_differs(self):
        helper = helper_source()
        self.assertIn(
            "if (team.d1SinceSeason && team.d1SinceSeason !== published) {",
            helper,
        )
        self.assertIn(
            "labels.push(`D1 SINCE ${formatSinceSeason(team.d1SinceSeason)}`);",
            helper,
        )
        self.assertIn('return labels.join(" • ");', helper)

    def test_redundant_d1_since_is_suppressed_when_starts_match(self):
        helper = helper_source()
        self.assertIn("team.d1SinceSeason !== published", helper)
        self.assertNotIn("team.d1SinceSeason === published", helper)

    def test_team_hero_uses_history_label_helper(self):
        team = SITE.split("function teamView(key) {", 1)[1].split(
            "\nfunction toggleTeamFilters(", 1
        )[0]
        self.assertIn("${esc(teamHistoryLabel(team))}", team)
        self.assertNotIn(
            "SINCE ${esc(formatSinceSeason(team.historyStartSeason))}",
            team,
        )

    def test_current_generated_coverage_populations(self):
        published = [
            program for program in PROGRAMS if program.get("public_page_enabled")
        ]
        complete = [
            program for program in published
            if program.get("history_coverage_status") == "COMPLETE_INSTITUTIONAL"
        ]
        legacy = [
            program for program in published
            if program.get("history_coverage_status") == "LEGACY_TOP_LEVEL_ONLY"
        ]
        self.assertEqual(len(published), 113)
        self.assertEqual(len(complete) + len(legacy), len(published))
        self.assertEqual(
            {program["program_key"] for program in published},
            set(REFERENCE_PUBLIC),
        )
        for program in published:
            reference = REFERENCE_PUBLIC[program["program_key"]]
            self.assertEqual(
                program["history_coverage_status"],
                reference["history_coverage_status"],
                program["program_key"],
            )
            expected_start = (
                reference["program_inception_season"]
                if reference["history_coverage_status"] == "COMPLETE_INSTITUTIONAL"
                else reference["history_start_season"]
            )
            self.assertEqual(
                program["published_history_start_season"],
                expected_start,
                program["program_key"],
            )


if __name__ == "__main__":
    unittest.main()
