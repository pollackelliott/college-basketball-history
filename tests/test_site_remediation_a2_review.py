import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from site_remediation_a2_review import (  # noqa: E402
    build_a2_review,
    classify_review_bucket,
    evidence_profile,
)


ASSERTION_FIELDS = [
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "normalized_opponent_key",
    "curated_site_type",
    "source_site_candidate",
    "source_venue_name",
    "curated_venue_name",
    "city",
    "state",
    "event_or_tournament",
    "source_page",
    "raw_text",
    "match_method",
]
DISCREPANCY_FIELDS = [
    "canonical_game_id",
    "field_name",
    "status",
    "resolution_basis",
]


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def candidate(**overrides):
    row = {
        "canonical_game_id": "CBBG-0000001",
        "season_label": "1950-1951",
        "game_date": "1951-01-02",
        "team_a_key": "alpha",
        "team_b_key": "beta",
        "game_type": "REGULAR_SEASON",
        "tier": "A2_UNCONTESTED_SITE_TYPE",
        "current_site_type": "UNKNOWN",
        "proposed_site_type": "TEAM_B_HOME",
        "proposed_venue_id": "VEN-000001",
        "proposed_venue_key": "example-arena",
        "proposed_city": "Beta City",
        "proposed_state": "BB",
        "supporting_programs": "beta",
        "supporting_source_game_ids": "BRAW-1",
    }
    row.update(overrides)
    return row


def assertion(program, source_id, site_type, **overrides):
    opponent = "beta" if program == "alpha" else "alpha"
    row = {
        "canonical_game_id": "CBBG-0000001",
        "source_program_key": program,
        "source_game_id": source_id,
        "normalized_opponent_key": opponent,
        "curated_site_type": site_type,
        "source_site_candidate": site_type,
        "source_venue_name": "Example Arena" if site_type != "UNKNOWN" else "",
        "curated_venue_name": "Example Arena" if site_type != "UNKNOWN" else "",
        "city": "Beta City" if site_type != "UNKNOWN" else "",
        "state": "BB" if site_type != "UNKNOWN" else "",
        "event_or_tournament": "",
        "source_page": "42",
        "raw_text": "Official year-by-year result.",
        "match_method": "EXISTING_SOURCE_ASSERTION",
    }
    row.update(overrides)
    return row


class A2ReviewHelperTests(unittest.TestCase):
    def test_evidence_profiles(self):
        self.assertEqual(
            evidence_profile({"proposed_venue_id": "V", "proposed_city": "X", "proposed_state": "Y"}),
            "VENUE_AND_LOCATION",
        )
        self.assertEqual(
            evidence_profile({"proposed_venue_id": "V", "proposed_city": "", "proposed_state": ""}),
            "VENUE_ONLY",
        )
        self.assertEqual(
            evidence_profile({"proposed_venue_id": "", "proposed_city": "X", "proposed_state": "Y"}),
            "LOCATION_ONLY",
        )
        self.assertEqual(evidence_profile({}), "SITE_ASSERTION_ONLY")

    def test_review_bucket_separates_consensus_physical_and_site_only(self):
        self.assertEqual(classify_review_bucket("SITE_ASSERTION_ONLY", 2), "RECIPROCAL_CONSENSUS")
        self.assertEqual(
            classify_review_bucket("VENUE_AND_LOCATION", 1),
            "ONE_SIDED_WITH_PHYSICAL_SUPPORT",
        )
        self.assertEqual(
            classify_review_bucket("SITE_ASSERTION_ONLY", 1),
            "ONE_SIDED_SITE_ASSERTION_ONLY",
        )


class A2ReviewIntegrationTests(unittest.TestCase):
    def make_repo(self, root, *, assertions=None, discrepancies=None):
        assertions = assertions if assertions is not None else [
            assertion("alpha", "ARAW-1", "UNKNOWN"),
            assertion("beta", "BRAW-1", "SOURCE_PROGRAM_HOME"),
        ]
        discrepancies = discrepancies if discrepancies is not None else []
        write_csv(root / "data/evidence/game-assertions.csv", ASSERTION_FIELDS, assertions)
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            DISCREPANCY_FIELDS,
            discrepancies,
        )

    def tier_payload(self):
        return {"rows": [candidate()], "review_rows": [], "summary": {}}

    def test_one_sided_reciprocal_support_is_described_not_applied(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            with patch(
                "site_remediation_a2_review.build_tier_report",
                return_value=self.tier_payload(),
            ):
                report = build_a2_review(root)
            self.assertEqual(report["summary"]["status"], "PASS")
            self.assertEqual(report["summary"]["candidate_games"], 1)
            row = report["rows"][0]
            self.assertEqual(row["proposed_site_type"], "TEAM_B_HOME")
            self.assertEqual(row["proposed_home_team_key"], "beta")
            self.assertEqual(row["supporting_programs"], "beta")
            self.assertEqual(row["evidence_profile"], "VENUE_AND_LOCATION")
            self.assertEqual(row["review_bucket"], "ONE_SIDED_WITH_PHYSICAL_SUPPORT")
            self.assertEqual(
                row["other_participant_evidence_state"],
                "OTHER_PARTICIPANT_UNKNOWN_ASSERTION",
            )

    def test_site_discrepancy_excludes_candidate_from_clean_owner_batch(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                discrepancies=[
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "field_name": "site_type",
                        "status": "UNDER_REVIEW",
                        "resolution_basis": "",
                    }
                ],
            )
            with patch(
                "site_remediation_a2_review.build_tier_report",
                return_value=self.tier_payload(),
            ):
                report = build_a2_review(root)
            self.assertEqual(report["summary"]["status"], "FAIL")
            self.assertTrue(any("field-specific site reconciliation" in e for e in report["summary"]["errors"]))

    def test_conflicting_known_participant_site_is_not_clean_a2(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(
                root,
                assertions=[
                    assertion("alpha", "ARAW-1", "SOURCE_PROGRAM_HOME"),
                    assertion("beta", "BRAW-1", "SOURCE_PROGRAM_HOME"),
                ],
            )
            with patch(
                "site_remediation_a2_review.build_tier_report",
                return_value=self.tier_payload(),
            ):
                report = build_a2_review(root)
            self.assertEqual(report["summary"]["status"], "FAIL")
            self.assertTrue(any("participant assertion site universe" in e for e in report["summary"]["errors"]))


if __name__ == "__main__":
    unittest.main()
