import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from site_remediation_tier_report import build_tier_report  # noqa: E402


CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "team_a_key",
    "team_b_key",
    "site_type",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "game_type",
]
VENUE_FIELDS = [
    "venue_id",
    "venue_key",
    "display_name",
    "city",
    "state",
]


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def game(**overrides):
    row = {
        "canonical_game_id": "CBBG-0000001",
        "season_label": "2025-2026",
        "game_date": "2026-01-01",
        "team_a_key": "alpha",
        "team_b_key": "beta",
        "site_type": "TEAM_A_HOME",
        "venue_key": "",
        "venue_id": "",
        "site_city": "",
        "site_state": "",
        "game_type": "REGULAR_SEASON",
    }
    row.update(overrides)
    return row


def audit_row(field, **overrides):
    row = {
        "canonical_game_id": "CBBG-0000001",
        "field_name": field,
        "classification": "SINGLE_SOURCE_PROPAGATION",
        "proposed_value": "",
        "proposed_venue_id": "",
        "proposed_venue_key": "",
        "proposed_city": "",
        "proposed_state": "",
        "supporting_programs": "alpha",
        "supporting_source_game_ids": "ARAW-1",
        "evidence_values": "",
        "reason": "test evidence",
    }
    row.update(overrides)
    return row


class SiteRemediationTierReportTests(unittest.TestCase):
    def make_repo(self, root, canonical_rows):
        write_csv(root / "data/canonical/games.csv", CANONICAL_FIELDS, canonical_rows)
        write_csv(
            root / "data/reference/venues.csv",
            VENUE_FIELDS,
            [
                {
                    "venue_id": "VEN-000001",
                    "venue_key": "example-arena",
                    "display_name": "Example Arena",
                    "city": "Alpha City",
                    "state": "AA",
                }
            ],
        )

    def test_registry_geography_is_a0(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                [game(venue_key="example-arena", venue_id="VEN-000001")],
            )
            audit = {
                "mechanical": [],
                "review": [],
                "summary": {
                    "mechanical_game_candidates": 0,
                    "mechanical_field_candidates": 0,
                },
            }
            with patch("site_remediation_tier_report.build_audit", return_value=audit):
                report = build_tier_report(root)
            self.assertEqual(len(report["rows"]), 1)
            row = report["rows"][0]
            self.assertEqual(row["tier"], "A0_REGISTRY_GEOGRAPHY")
            self.assertEqual(row["proposed_city"], "Alpha City")
            self.assertEqual(row["proposed_state"], "AA")
            self.assertEqual(row["change_fields"], "site_city|site_state")

    def test_existing_site_source_propagation_is_a1(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, [game()])
            audit = {
                "mechanical": [
                    audit_row(
                        "venue",
                        proposed_value="Example Arena",
                        proposed_venue_id="VEN-000001",
                        proposed_venue_key="example-arena",
                    ),
                    audit_row(
                        "location",
                        proposed_value="Alpha City, AA",
                        proposed_city="Alpha City",
                        proposed_state="AA",
                    ),
                ],
                "review": [],
                "summary": {
                    "mechanical_game_candidates": 1,
                    "mechanical_field_candidates": 2,
                },
            }
            with patch("site_remediation_tier_report.build_audit", return_value=audit):
                report = build_tier_report(root)
            self.assertEqual(len(report["rows"]), 1)
            row = report["rows"][0]
            self.assertEqual(row["tier"], "A1_EXISTING_SITE_PROPAGATION")
            self.assertEqual(row["proposed_venue_id"], "VEN-000001")
            self.assertEqual(row["proposed_city"], "Alpha City")

    def test_unknown_site_change_is_always_a2(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, [game(site_type="UNKNOWN")])
            audit = {
                "mechanical": [
                    audit_row(
                        "site_type",
                        classification="RECIPROCAL_ONLY",
                        proposed_value="TEAM_A_HOME",
                    )
                ],
                "review": [],
                "summary": {
                    "mechanical_game_candidates": 1,
                    "mechanical_field_candidates": 1,
                },
            }
            with patch("site_remediation_tier_report.build_audit", return_value=audit):
                report = build_tier_report(root)
            self.assertEqual(len(report["rows"]), 1)
            row = report["rows"][0]
            self.assertEqual(row["tier"], "A2_UNCONTESTED_SITE_TYPE")
            self.assertEqual(row["proposed_site_type"], "TEAM_A_HOME")
            self.assertEqual(row["change_fields"], "site_type")


if __name__ == "__main__":
    unittest.main()
