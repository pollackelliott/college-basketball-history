import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from site_remediation_audit import build_audit  # noqa: E402


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
ASSERTION_FIELDS = [
    "canonical_game_id",
    "source_program_key",
    "source_game_id",
    "normalized_opponent_key",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
]
DISCREPANCY_FIELDS = [
    "canonical_game_id",
    "field_name",
    "status",
    "resolution_basis",
]
GLOBAL_VENUE_FIELDS = [
    "venue_id",
    "venue_key",
    "display_name",
    "city",
    "state",
    "opened",
    "closed",
    "date_precision",
    "identity_status",
    "source_basis",
    "notes",
]
VENUE_NAME_FIELDS = [
    "venue_id",
    "venue_name",
    "normalized_name",
    "name_type",
    "valid_from",
    "valid_to",
    "date_precision",
    "source_basis",
    "notes",
]
SCHOOL_VENUE_FIELDS = [
    "source_program_key",
    "venue_key",
    "venue_id",
    "canonical_name",
    "aliases",
    "city",
    "state",
]


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def canonical(**overrides):
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


def assertion(program, source_id, **overrides):
    opponent = "beta" if program == "alpha" else "alpha"
    row = {
        "canonical_game_id": "CBBG-0000001",
        "source_program_key": program,
        "source_game_id": source_id,
        "normalized_opponent_key": opponent,
        "curated_site_type": "SOURCE_PROGRAM_HOME" if program == "alpha" else "OPPONENT_HOME",
        "curated_venue_name": "Example Arena",
        "city": "Alpha City",
        "state": "AA",
    }
    row.update(overrides)
    return row


class SiteRemediationAuditTests(unittest.TestCase):
    def make_repo(self, root, *, games=None, assertions=None, discrepancies=None):
        games = games if games is not None else [canonical()]
        assertions = assertions if assertions is not None else [
            assertion("alpha", "ARAW-1"),
            assertion("beta", "BRAW-1"),
        ]
        discrepancies = discrepancies if discrepancies is not None else []

        write_csv(root / "data/canonical/games.csv", CANONICAL_FIELDS, games)
        write_csv(root / "data/evidence/game-assertions.csv", ASSERTION_FIELDS, assertions)
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            DISCREPANCY_FIELDS,
            discrepancies,
        )
        write_csv(
            root / "data/reference/venues.csv",
            GLOBAL_VENUE_FIELDS,
            [
                {
                    "venue_id": "VEN-000001",
                    "venue_key": "example-arena",
                    "display_name": "Example Arena",
                    "city": "Alpha City",
                    "state": "AA",
                },
                {
                    "venue_id": "VEN-000002",
                    "venue_key": "other-arena",
                    "display_name": "Other Arena",
                    "city": "Other City",
                    "state": "BB",
                },
            ],
        )
        write_csv(
            root / "data/reference/venue-names.csv",
            VENUE_NAME_FIELDS,
            [
                {
                    "venue_id": "VEN-000001",
                    "venue_name": "Example Arena",
                    "normalized_name": "examplearena",
                    "name_type": "PROJECT_DISPLAY",
                },
                {
                    "venue_id": "VEN-000002",
                    "venue_name": "Other Arena",
                    "normalized_name": "otherarena",
                    "name_type": "PROJECT_DISPLAY",
                },
            ],
        )
        for program in ("alpha", "beta"):
            write_csv(
                root / f"schools/{program}/venues.csv",
                SCHOOL_VENUE_FIELDS,
                [
                    {
                        "source_program_key": program,
                        "venue_key": "example-arena",
                        "venue_id": "VEN-000001",
                        "canonical_name": "Example Arena",
                        "aliases": "",
                        "city": "Alpha City",
                        "state": "AA",
                    }
                ],
            )

    def mechanical_by_field(self, report):
        return {row["field_name"]: row for row in report["mechanical"]}

    def test_blank_canonical_fields_with_reciprocal_consensus_are_mechanical(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root)
            report = build_audit(root)
            fields = self.mechanical_by_field(report)
            self.assertEqual(set(fields), {"venue", "location"})
            self.assertEqual(fields["venue"]["proposed_venue_id"], "VEN-000001")
            self.assertEqual(fields["location"]["proposed_value"], "Alpha City, AA")
            self.assertEqual(fields["venue"]["classification"], "RECIPROCAL_CONSENSUS")

    def test_unknown_site_type_can_be_repaired_without_using_geography_to_infer_it(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_repo(root, games=[canonical(site_type="UNKNOWN")])
            report = build_audit(root)
            fields = self.mechanical_by_field(report)
            self.assertEqual(fields["site_type"]["proposed_value"], "TEAM_A_HOME")
            self.assertEqual(fields["venue"]["proposed_venue_id"], "VEN-000001")
            self.assertEqual(fields["location"]["proposed_city"], "Alpha City")

    def test_reciprocal_only_evidence_is_labeled_separately(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [
                assertion("alpha", "ARAW-1", curated_venue_name="", city="", state=""),
                assertion("beta", "BRAW-1"),
            ]
            self.make_repo(root, assertions=rows)
            report = build_audit(root)
            fields = self.mechanical_by_field(report)
            self.assertEqual(fields["venue"]["classification"], "RECIPROCAL_ONLY")
            self.assertEqual(fields["location"]["classification"], "RECIPROCAL_ONLY")

    def test_conflicting_location_is_review_not_mechanical(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [
                assertion("alpha", "ARAW-1"),
                assertion("beta", "BRAW-1", city="Other City", state="BB"),
            ]
            self.make_repo(root, assertions=rows)
            report = build_audit(root)
            self.assertFalse(any(row["field_name"] == "location" for row in report["mechanical"]))
            conflict = [
                row for row in report["review"]
                if row["field_name"] == "location" and row["classification"] == "CONFLICT_REVIEW"
            ]
            self.assertEqual(len(conflict), 1)

    def test_conflicting_site_type_suppresses_downstream_mechanical_site_enrichment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [
                assertion("alpha", "ARAW-1"),
                assertion("beta", "BRAW-1", curated_site_type="SOURCE_PROGRAM_HOME"),
            ]
            self.make_repo(root, games=[canonical(site_type="UNKNOWN")], assertions=rows)
            report = build_audit(root)
            self.assertFalse(report["mechanical"])
            conflicts = [
                row for row in report["review"]
                if row["field_name"] == "site_type" and row["classification"] == "CONFLICT_REVIEW"
            ]
            self.assertEqual(len(conflicts), 1)

    def test_known_canonical_site_conflict_blocks_dependent_enrichment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [
                assertion("alpha", "ARAW-1"),
                assertion(
                    "beta",
                    "BRAW-1",
                    curated_site_type="SOURCE_PROGRAM_HOME",
                    curated_venue_name="Other Arena",
                    city="Other City",
                    state="BB",
                ),
            ]
            self.make_repo(root, assertions=rows)
            report = build_audit(root)
            self.assertFalse(report["mechanical"])
            conflicts = [
                row for row in report["review"]
                if row["field_name"] == "site_type"
                and row["classification"] == "CANONICAL_ASSERTION_CONFLICT"
            ]
            self.assertEqual(len(conflicts), 1)

    def test_resolved_known_site_conflict_allows_only_canonical_agreeing_enrichment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [
                assertion("alpha", "ARAW-1"),
                assertion(
                    "beta",
                    "BRAW-1",
                    curated_site_type="SOURCE_PROGRAM_HOME",
                    curated_venue_name="Other Arena",
                    city="Other City",
                    state="BB",
                ),
            ]
            discrepancies = [
                {
                    "canonical_game_id": "CBBG-0000001",
                    "field_name": "site_type",
                    "status": "RESOLVED",
                    "resolution_basis": "Owner-reviewed source conflict; TEAM_A_HOME retained.",
                }
            ]
            self.make_repo(root, assertions=rows, discrepancies=discrepancies)
            report = build_audit(root)
            fields = self.mechanical_by_field(report)
            self.assertEqual(set(fields), {"venue", "location"})
            self.assertEqual(fields["venue"]["proposed_venue_id"], "VEN-000001")
            self.assertEqual(fields["location"]["proposed_value"], "Alpha City, AA")
            resolved = [
                row for row in report["review"]
                if row["field_name"] == "site_type"
                and row["classification"] == "RECONCILIATION_RESOLVED"
            ]
            self.assertEqual(len(resolved), 1)

    def test_under_review_known_site_conflict_blocks_dependent_enrichment(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [
                assertion("alpha", "ARAW-1"),
                assertion("beta", "BRAW-1", curated_site_type="SOURCE_PROGRAM_HOME"),
            ]
            discrepancies = [
                {
                    "canonical_game_id": "CBBG-0000001",
                    "field_name": "site_type",
                    "status": "UNDER_REVIEW",
                    "resolution_basis": "",
                }
            ]
            self.make_repo(root, assertions=rows, discrepancies=discrepancies)
            report = build_audit(root)
            self.assertFalse(report["mechanical"])
            holds = [
                row for row in report["review"]
                if row["field_name"] == "site_type"
                and row["classification"] == "RECONCILIATION_HOLD"
            ]
            self.assertEqual(len(holds), 1)

    def test_field_specific_reconciliation_provenance_holds_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            discrepancies = [
                {
                    "canonical_game_id": "CBBG-0000001",
                    "field_name": "location",
                    "status": "RESOLVED",
                    "resolution_basis": "Owner-reviewed historical conflict; canonical location remains blank.",
                }
            ]
            self.make_repo(root, discrepancies=discrepancies)
            report = build_audit(root)
            self.assertFalse(any(row["field_name"] == "location" for row in report["mechanical"]))
            holds = [
                row for row in report["review"]
                if row["field_name"] == "location" and row["classification"] == "RECONCILIATION_HOLD"
            ]
            self.assertEqual(len(holds), 1)

    def test_existing_nonblank_canonical_fields_are_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            game = canonical(
                venue_key="existing-arena",
                venue_id="VEN-999999",
                site_city="Canonical City",
                site_state="CC",
            )
            self.make_repo(root, games=[game])
            report = build_audit(root)
            self.assertFalse(any(row["field_name"] in {"venue", "location"} for row in report["mechanical"]))

    def test_unresolvable_venue_identity_is_never_mechanical(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            rows = [
                assertion("alpha", "ARAW-1", curated_venue_name="Mystery Hall"),
                assertion("beta", "BRAW-1", curated_venue_name="Mystery Hall"),
            ]
            self.make_repo(root, assertions=rows)
            report = build_audit(root)
            self.assertFalse(any(row["field_name"] == "venue" for row in report["mechanical"]))
            venue_review = [
                row for row in report["review"]
                if row["field_name"] == "venue" and row["classification"] == "VENUE_IDENTITY_REVIEW"
            ]
            self.assertEqual(len(venue_review), 1)


if __name__ == "__main__":
    unittest.main()
