import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import published_opponent_identity_census as census


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


class PublishedOpponentIdentityCensusTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.repo = Path(self.tempdir.name)
        (self.repo / "data/reference").mkdir(parents=True)
        (self.repo / "schools/northwestern").mkdir(parents=True)
        (self.repo / "schools/texas-a-m").mkdir(parents=True)

        programs = [
            [
                "northwestern",
                "Northwestern",
                "Northwestern",
                "Yes",
                "Yes",
                "1904-1905",
            ],
            [
                "texas-a-m",
                "Texas A&M",
                "Texas A&M",
                "Yes",
                "Yes",
                "1912-1913",
            ],
            [
                "east-texas-a-m",
                "East Texas A&M",
                "East Texas A&M",
                "Yes",
                "No",
                "",
            ],
            [
                "northwestern-state",
                "Northwestern State",
                "Northwestern State",
                "Yes",
                "No",
                "",
            ],
            [
                "missouri-state",
                "Missouri State",
                "Missouri State",
                "Yes",
                "No",
                "",
            ],
        ]
        programs.extend(
            [
                [
                    "florida-southern",
                    "Florida Southern",
                    "Florida Southern",
                    "No",
                    "No",
                    "",
                ],
                [
                    "southern",
                    "Southern",
                    "Southern",
                    "Yes",
                    "No",
                    "",
                ],
            ]
        )

        self._write_csv(
            self.repo / "data/reference/programs.csv",
            PROGRAM_HEADERS,
            programs,
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def _write_csv(self, path, headers, rows):
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            writer.writerows(rows)

    def _write_opponents(self, northwestern_rows, texas_am_rows):
        self._write_csv(
            self.repo / "schools/northwestern/opponents.csv",
            OPPONENT_HEADERS,
            northwestern_rows,
        )
        self._write_csv(
            self.repo / "schools/texas-a-m/opponents.csv",
            OPPONENT_HEADERS,
            texas_am_rows,
        )

    def test_published_program_name_split_is_p0(self):
        self._write_opponents(
            [
                [
                    "northwestern",
                    "Texas A&M",
                    "texas-a-and-m",
                    "Texas A&M",
                    "",
                    "5",
                    "1969-1970",
                    "1993-1994",
                ]
            ],
            [],
        )

        report = census.build_census(self.repo)
        finding = report["findings"][0]
        self.assertEqual(finding["priority"], "P0")
        self.assertEqual(finding["finding_type"], "CURRENT_PROGRAM_NAME_SPLIT")
        self.assertEqual(finding["suggested_program_key"], "texas-a-m")
        self.assertEqual(finding["games_with_source_label"], 5)

    def test_current_registry_key_with_stale_flag_is_p1(self):
        self._write_opponents(
            [],
            [
                [
                    "texas-a-m",
                    "NORTHWESTERN STATE",
                    "northwestern-state",
                    "Northwestern State",
                    "No",
                    "13",
                    "1969-1970",
                    "2025-2026",
                ]
            ],
        )

        report = census.build_census(self.repo)
        finding = report["findings"][0]
        self.assertEqual(finding["priority"], "P1")
        self.assertEqual(finding["finding_type"], "STALE_CURRENT_D1_FLAG")
        self.assertEqual(finding["suggested_program_key"], "northwestern-state")

    def test_cross_package_alias_is_review_trigger_not_auto_merge(self):
        self._write_opponents(
            [
                [
                    "northwestern",
                    "SW Missouri State",
                    "sw-missouri-state",
                    "SW Missouri State",
                    "No",
                    "1",
                    "2001-2002",
                    "2001-2002",
                ]
            ],
            [
                [
                    "texas-a-m",
                    "SW Missouri State",
                    "missouri-state",
                    "Missouri State",
                    "Yes",
                    "1",
                    "1999-2000",
                    "1999-2000",
                ]
            ],
        )

        report = census.build_census(self.repo)
        finding = next(
            row
            for row in report["findings"]
            if row["source_program_key"] == "northwestern"
        )
        self.assertEqual(finding["priority"], "P2")
        self.assertEqual(finding["finding_type"], "CROSS_PACKAGE_ALIAS_SPLIT")
        self.assertEqual(finding["suggested_program_key"], "missouri-state")

    def test_modern_non_d1_identity_is_surfaced_for_review(self):
        self._write_opponents(
            [],
            [
                [
                    "texas-a-m",
                    "TAMU-COMMERCE",
                    "tamu-commerce",
                    "Tamu-commerce",
                    "No",
                    "1",
                    "2023-2024",
                    "2023-2024",
                ]
            ],
        )

        report = census.build_census(self.repo)
        finding = report["findings"][0]
        self.assertEqual(finding["priority"], "P3")
        self.assertEqual(finding["finding_type"], "MODERN_NON_D1_REVIEW")
        self.assertEqual(finding["suggested_program_key"], "")

    def test_old_genuine_non_d1_is_inventory_not_forced_finding(self):
        self._write_opponents(
            [
                [
                    "northwestern",
                    "Chicago YMCA",
                    "chicago-ymca",
                    "Chicago YMCA",
                    "",
                    "1",
                    "1915-1916",
                    "1915-1916",
                ]
            ],
            [],
        )

        report = census.build_census(self.repo)
        self.assertEqual(report["finding_count"], 0)
        self.assertEqual(report["non_d1_identity_count"], 1)
        self.assertEqual(
            report["non_d1_identity_inventory"][0]["canonical_opponent_key"],
            "chicago-ymca",
        )

    def test_registered_noncurrent_program_is_not_remapped_by_name_collision(self):
        self._write_opponents(
            [
                [
                    "northwestern",
                    "Southern",
                    "florida-southern",
                    "Southern",
                    "No",
                    "24",
                    "2000-2001",
                    "2024-2025",
                ]
            ],
            [],
        )

        report = census.build_census(self.repo)
        self.assertFalse(
            any(
                row["suggested_program_key"] == "southern"
                for row in report["findings"]
            )
        )

    def test_cross_package_alias_cannot_be_p0_even_for_published_target(self):
        self._write_opponents(
            [
                [
                    "northwestern",
                    "Aggies",
                    "texas-a-m",
                    "Texas A&M",
                    "Yes",
                    "1",
                    "1980-1981",
                    "1980-1981",
                ],
                [
                    "northwestern",
                    "Aggies",
                    "texas-aggies",
                    "Texas Aggies",
                    "No",
                    "1",
                    "1970-1971",
                    "1970-1971",
                ],
            ],
            [],
        )

        report = census.build_census(self.repo)
        finding = next(
            row
            for row in report["findings"]
            if row["canonical_opponent_key"] == "texas-aggies"
        )
        self.assertEqual(finding["priority"], "P2")
        self.assertEqual(finding["finding_type"], "CROSS_PACKAGE_ALIAS_SPLIT")
        self.assertEqual(finding["suggested_program_key"], "texas-a-m")

    def test_raw_source_name_alone_does_not_create_exact_program_split(self):
        self._write_opponents(
            [
                [
                    "northwestern",
                    "Texas A&M",
                    "texas-agricultural",
                    "Texas Agricultural",
                    "No",
                    "1",
                    "1940-1941",
                    "1940-1941",
                ]
            ],
            [],
        )

        report = census.build_census(self.repo)
        self.assertFalse(
            any(row["priority"] == "P0" for row in report["findings"])
        )

    def test_name_normalization_handles_ampersand_and_whitespace(self):
        self.assertEqual(
            census.normalize_name(" Texas A&M  "),
            census.normalize_name("Texas A&M"),
        )
        self.assertEqual(census.normalize_name("Texas A&M"), "texas a and m")


if __name__ == "__main__":
    unittest.main()
