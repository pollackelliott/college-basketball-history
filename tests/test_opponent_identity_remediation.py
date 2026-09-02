import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import opponent_identity_remediation as tool


PROGRAM_HEADERS = [
    "program_key",
    "program_name",
    "display_name",
    "current_d1",
    "public_page_enabled",
    "history_start_season",
]
OPPONENT_HEADERS = [
    "source_program_key",
    "source_opponent_label",
    "canonical_opponent_key",
    "canonical_opponent_name",
    "current_d1",
    "games_with_source_label",
    "first_season",
    "last_season",
]
SOURCE_HEADERS = [
    "source_game_id",
    "source_program_key",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_name",
    "normalized_opponent_key",
    "opponent_current_d1",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
]
CANONICAL_HEADERS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "team_a_score",
    "team_b_score",
    "overtime_periods",
]
ASSERTION_HEADERS = [
    "assertion_id",
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "normalized_opponent_key",
]
DECISION_HEADERS = tool.REQUIRED_DECISION_FIELDS
ALIAS_HEADERS = tool.REQUIRED_ALIAS_FIELDS


class OpponentIdentityRemediationTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)
        (self.repo / "data/reference").mkdir(parents=True)
        (self.repo / "data/canonical").mkdir(parents=True)
        (self.repo / "data/evidence").mkdir(parents=True)
        for school in ("northwestern", "texas-a-m"):
            (self.repo / "schools" / school).mkdir(parents=True)

        self._write(
            self.repo / "data/reference/programs.csv",
            PROGRAM_HEADERS,
            [
                ["northwestern", "Northwestern", "Northwestern", "Yes", "Yes", "1904-1905"],
                ["texas-a-m", "Texas A&M", "Texas A&M", "Yes", "Yes", "1912-1913"],
                ["northwestern-state", "Northwestern State", "Northwestern State", "Yes", "No", ""],
                ["florida-southern", "Florida Southern", "Florida Southern", "No", "No", ""],
                ["southern", "Southern", "Southern", "Yes", "No", ""],
            ],
        )
        self._write(self.repo / "data/reference/program-names.csv", ALIAS_HEADERS, [])
        self._write(self.repo / "schools/texas-a-m/opponents.csv", OPPONENT_HEADERS, [])
        self._write(self.repo / "schools/texas-a-m/source-games.csv", SOURCE_HEADERS, [])
        self._write(self.repo / "data/canonical/games.csv", CANONICAL_HEADERS, [])
        self._write(self.repo / "data/evidence/game-assertions.csv", ASSERTION_HEADERS, [])

    def tearDown(self):
        self.tempdir.cleanup()

    def _write(self, path, headers, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            writer.writerows(rows)

    def _northwestern_split(self):
        self._write(
            self.repo / "schools/northwestern/opponents.csv",
            OPPONENT_HEADERS,
            [
                [
                    "northwestern",
                    "Texas A&M",
                    "texas-a-and-m",
                    "Texas A&M",
                    "No",
                    "1",
                    "1993-1994",
                    "1993-1994",
                ]
            ],
        )
        self._write(
            self.repo / "schools/northwestern/source-games.csv",
            SOURCE_HEADERS,
            [
                [
                    "NW-1",
                    "northwestern",
                    "1993-1994",
                    "1993-12-01",
                    "Texas A&M",
                    "Texas A&M",
                    "texas-a-and-m",
                    "No",
                    "70",
                    "68",
                    "W",
                    "0",
                ]
            ],
        )

    def _decision_file(self, rows):
        path = self.repo / "decisions.csv"
        self._write(path, DECISION_HEADERS, rows)
        return path

    def test_empty_alias_registry_is_valid(self):
        report = tool.validate_alias_registry(self.repo)
        self.assertEqual(report["row_count"], 0)
        self.assertEqual(report["errors"], [])

    def test_alias_requires_registry_program_and_evidence(self):
        self._write(
            self.repo / "data/reference/program-names.csv",
            ALIAS_HEADERS,
            [
                [
                    "missing-program",
                    "Old Name",
                    "OFFICIAL_HISTORICAL_NAME",
                    "1920-1921",
                    "1930-1931",
                    "VERIFIED",
                    "",
                    "https://example.test",
                    "",
                ]
            ],
        )
        report = tool.validate_alias_registry(self.repo)
        self.assertTrue(any("unknown program_key" in item for item in report["errors"]))
        self.assertTrue(any("evidence_basis is required" in item for item in report["errors"]))

    def test_ambiguous_alias_needs_disjoint_eras(self):
        self._write(
            self.repo / "data/reference/program-names.csv",
            ALIAS_HEADERS,
            [
                [
                    "northwestern",
                    "Aggies",
                    "SOURCE_ABBREVIATION",
                    "",
                    "",
                    "VERIFIED",
                    "source A",
                    "https://a.test",
                    "",
                ],
                [
                    "texas-a-m",
                    "Aggies",
                    "SOURCE_ABBREVIATION",
                    "",
                    "",
                    "VERIFIED",
                    "source B",
                    "https://b.test",
                    "",
                ],
            ],
        )
        report = tool.validate_alias_registry(self.repo)
        self.assertTrue(any("ambiguous alias" in item for item in report["errors"]))

    def test_sanity_report_surfaces_stale_non_d1_rows(self):
        self._northwestern_split()
        report = tool.sanity_report(self.repo, "northwestern")
        self.assertEqual(report["non_current_or_non_d1_rows"], 1)
        row = report["rows"][0]
        self.assertEqual(row["canonical_opponent_key"], "texas-a-and-m")
        self.assertEqual(row["tool_flags"][0]["priority"], "P0")
        self.assertEqual(row["tool_flags"][0]["suggested_program_key"], "texas-a-m")

    def test_stable_decision_id_ignores_evidence_wording(self):
        base = {
            "source_program_key": "northwestern",
            "source_opponent_label": "Texas A&M",
            "from_program_key": "texas-a-and-m",
            "to_program_key": "texas-a-m",
            "decision": "MERGE_TO_PROGRAM",
            "evidence_basis": "one",
            "evidence_url": "https://one.test",
        }
        changed = dict(base, evidence_basis="different wording")
        self.assertEqual(tool.decision_id(base), tool.decision_id(changed))

    def test_plan_rejects_source_game_count_mismatch(self):
        self._northwestern_split()
        # opponents.csv claims two games while source-games has one.
        opponents = tool.read_csv(self.repo / "schools/northwestern/opponents.csv")
        opponents[0]["games_with_source_label"] = "2"
        self._write(
            self.repo / "schools/northwestern/opponents.csv",
            OPPONENT_HEADERS,
            [[row.get(h, "") for h in OPPONENT_HEADERS] for row in opponents],
        )
        decisions = self._decision_file(
            [[
                "northwestern",
                "Texas A&M",
                "texas-a-and-m",
                "texas-a-m",
                "MERGE_TO_PROGRAM",
                "reciprocal evidence",
                "https://example.test",
            ]]
        )
        plan = tool.build_plan(self.repo, decisions)
        self.assertTrue(any("source-games match count" in item for item in plan["blockers"]))

    def test_plan_detects_exact_canonical_collision_after_merge(self):
        self._northwestern_split()
        self._write(
            self.repo / "data/canonical/games.csv",
            CANONICAL_HEADERS,
            [
                ["CBBG-1", "1993-1994", "1993-12-01", "northwestern", "texas-a-and-m", "70", "68", "0"],
                ["CBBG-2", "1993-1994", "1993-12-01", "northwestern", "texas-a-m", "70", "68", "0"],
            ],
        )
        self._write(
            self.repo / "data/evidence/game-assertions.csv",
            ASSERTION_HEADERS,
            [["A-1", "CBBG-1", "northwestern", "NW-1", "texas-a-and-m"]],
        )
        decisions = self._decision_file(
            [[
                "northwestern",
                "Texas A&M",
                "texas-a-and-m",
                "texas-a-m",
                "MERGE_TO_PROGRAM",
                "reciprocal evidence",
                "https://example.test",
            ]]
        )
        plan = tool.build_plan(self.repo, decisions)
        self.assertEqual(len(plan["exact_collision_candidates"]), 1)
        self.assertTrue(any("exact-date canonical collision" in item for item in plan["blockers"]))

    def test_plan_is_deterministic_and_fingerprinted(self):
        self._northwestern_split()
        self._write(
            self.repo / "data/canonical/games.csv",
            CANONICAL_HEADERS,
            [["CBBG-1", "1993-1994", "1993-12-01", "northwestern", "texas-a-and-m", "70", "68", "0"]],
        )
        self._write(
            self.repo / "data/evidence/game-assertions.csv",
            ASSERTION_HEADERS,
            [["A-1", "CBBG-1", "northwestern", "NW-1", "texas-a-and-m"]],
        )
        decisions = self._decision_file(
            [[
                "northwestern",
                "Texas A&M",
                "texas-a-and-m",
                "texas-a-m",
                "MERGE_TO_PROGRAM",
                "reciprocal evidence",
                "https://example.test",
            ]]
        )
        one = tool.build_plan(self.repo, decisions)
        two = tool.build_plan(self.repo, decisions)
        self.assertEqual(one["plan_sha256"], two["plan_sha256"])
        self.assertEqual(one["blockers"], [])
        self.assertEqual(one["affected_assertion_counts"]["texas-a-and-m->texas-a-m"], 1)
        self.assertEqual(one["affected_canonical_game_ids"]["texas-a-and-m->texas-a-m"], ["CBBG-1"])
        self.assertIn("canonical-games.csv", one["fingerprints"])

    def test_mark_current_d1_requires_same_registry_key(self):
        self._write(
            self.repo / "schools/northwestern/opponents.csv",
            OPPONENT_HEADERS,
            [[
                "northwestern",
                "Northwestern State",
                "northwestern-state",
                "Northwestern State",
                "No",
                "1",
                "2020-2021",
                "2020-2021",
            ]],
        )
        self._write(
            self.repo / "schools/northwestern/source-games.csv",
            SOURCE_HEADERS,
            [[
                "NW-2",
                "northwestern",
                "2020-2021",
                "2020-12-01",
                "Northwestern State",
                "Northwestern State",
                "northwestern-state",
                "No",
                "80",
                "70",
                "W",
                "0",
            ]],
        )
        decisions = self._decision_file(
            [[
                "northwestern",
                "Northwestern State",
                "northwestern-state",
                "texas-a-m",
                "MARK_CURRENT_D1",
                "registry evidence",
                "https://example.test",
            ]]
        )
        plan = tool.build_plan(self.repo, decisions)
        self.assertTrue(any("MARK_CURRENT_D1 requires" in item for item in plan["blockers"]))


if __name__ == "__main__":
    unittest.main()
