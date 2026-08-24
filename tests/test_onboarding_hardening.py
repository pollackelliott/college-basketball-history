import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_hardening import (  # noqa: E402
    carry_forward_review,
    fill_review_from_map,
    research_portfolio_report,
)
from stage_research_portfolio import rebase_venues  # noqa: E402


REVIEW_FIELDS = [
    "decision_id",
    "category",
    "source_game_id",
    "season_label",
    "source_game_date",
    "canonical_game_date",
    "matchup",
    "field_name",
    "source_value",
    "canonical_value",
    "relevant_evidence",
    "recommended_action",
    "allowed_actions",
    "decision",
    "resolution_basis",
    "canonical_patch_json",
    "source_patch_json",
    "notes",
]


def write_csv(path, fieldnames, rows):
    with Path(path).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class ResearchFreezeAcceptanceTests(unittest.TestCase):
    def make_package(self, root: Path, ncaa_complete=True):
        game_fields = [
            "source_game_id",
            "source_program_key",
            "season_label",
            "game_date",
            "source_opponent_label",
            "normalized_opponent_key",
            "team_score",
            "opponent_score",
            "played_result",
            "curated_site_type",
            "curated_venue_name",
            "city",
            "state",
            "event_or_tournament",
            "curated_game_type",
            "curated_postseason_round",
            "raw_text",
        ]
        write_csv(
            root / "source-games.csv",
            game_fields,
            [
                {
                    "source_game_id": "TESTRAW-00001",
                    "source_program_key": "test",
                    "season_label": "2025-2026",
                    "game_date": "2026-03-19",
                    "source_opponent_label": "Example",
                    "normalized_opponent_key": "example",
                    "team_score": "70",
                    "opponent_score": "60",
                    "played_result": "W",
                    "curated_site_type": "NEUTRAL",
                    "curated_venue_name": "Example Arena" if ncaa_complete else "",
                    "city": "Example City" if ncaa_complete else "",
                    "state": "EX" if ncaa_complete else "",
                    "event_or_tournament": "NCAA Tournament",
                    "curated_game_type": "NCAA_TOURNAMENT",
                    "curated_postseason_round": "R64" if ncaa_complete else "",
                    "raw_text": "NCAA Tournament game",
                }
            ],
        )
        write_csv(
            root / "opponents.csv",
            ["source_program_key", "canonical_opponent_key"],
            [{"source_program_key": "test", "canonical_opponent_key": "example"}],
        )
        write_csv(
            root / "venues.csv",
            [
                "source_program_key",
                "venue_key",
                "venue_id",
                "canonical_name",
                "aliases",
                "city",
                "state",
            ],
            [
                {
                    "source_program_key": "test",
                    "venue_key": "example-arena",
                    "venue_id": "VEN-999999",
                    "canonical_name": "Example Arena",
                    "aliases": "",
                    "city": "Example City",
                    "state": "EX",
                }
            ],
        )
        write_csv(
            root / "conferences.csv",
            ["source_program_key"],
            [{"source_program_key": "test"}],
        )
        (root / "notes.md").write_text("# notes\n", encoding="utf-8")
        (root / "source-notes.md").write_text("# source notes\n", encoding="utf-8")

    def test_complete_ncaa_site_passes_research_freeze(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_package(root, ncaa_complete=True)
            report = research_portfolio_report(root, school_key="test")
            self.assertEqual(report["status"], "PASS")
            self.assertEqual(report["errors"], [])

    def test_incomplete_ncaa_site_blocks_research_freeze(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.make_package(root, ncaa_complete=False)
            report = research_portfolio_report(root, school_key="test")
            self.assertEqual(report["status"], "FAIL")
            self.assertTrue(
                any(
                    "NCAA Tournament research freeze requires curated_venue_name"
                    in error
                    for error in report["errors"]
                )
            )
            self.assertTrue(
                any(
                    "NCAA Tournament research freeze requires city" in error
                    for error in report["errors"]
                )
            )
            self.assertTrue(
                any(
                    "NCAA Tournament research freeze requires state" in error
                    for error in report["errors"]
                )
            )


class ReviewAutomationTests(unittest.TestCase):
    def sample_rows(self):
        base = {
            "season_label": "1905-1906",
            "source_game_date": "1906-01-01",
            "canonical_game_date": "1906-01-02",
            "matchup": "test vs other",
            "source_value": "",
            "canonical_value": "",
            "relevant_evidence": "reciprocal evidence",
            "recommended_action": "",
            "decision": "PENDING",
            "resolution_basis": "",
            "canonical_patch_json": "{}",
            "source_patch_json": "{}",
            "notes": "",
        }
        identity = dict(
            base,
            decision_id="IDENTITY-TESTRAW-00001",
            category="identity",
            source_game_id="TESTRAW-00001",
            field_name="game_identity",
            canonical_value="CBBG-0000001;CBBG-0000002",
            allowed_actions=(
                "MATCH_CANONICAL:CBBG-0000001 | "
                "MATCH_CANONICAL:CBBG-0000002 | FORCE_NEW"
            ),
        )
        selected = dict(
            base,
            decision_id=(
                "CONDITIONAL-DISCREPANCY-TESTRAW-00001-"
                "CBBG-0000001-GAME_DATE"
            ),
            category="conditional_discrepancy",
            source_game_id="TESTRAW-00001",
            field_name="game_date",
            allowed_actions=(
                "KEEP_CANONICAL | LEAVE_UNRESOLVED | "
                "NORMALIZE_SOURCE_TO_CANONICAL | NOT_APPLICABLE | USE_SOURCE"
            ),
        )
        rejected = dict(
            base,
            decision_id=(
                "CONDITIONAL-DISCREPANCY-TESTRAW-00001-"
                "CBBG-0000002-GAME_DATE"
            ),
            category="conditional_discrepancy",
            source_game_id="TESTRAW-00001",
            field_name="game_date",
            allowed_actions=(
                "KEEP_CANONICAL | LEAVE_UNRESOLVED | "
                "NORMALIZE_SOURCE_TO_CANONICAL | NOT_APPLICABLE | USE_SOURCE"
            ),
        )
        discrepancy = dict(
            base,
            decision_id="DISCREPANCY-TESTRAW-00003-SCORE",
            category="discrepancy",
            source_game_id="TESTRAW-00003",
            field_name="score",
            allowed_actions=(
                "KEEP_CANONICAL | LEAVE_UNRESOLVED | "
                "NORMALIZE_SOURCE_TO_CANONICAL | USE_SOURCE"
            ),
        )
        publication = dict(
            base,
            decision_id="PUBLICATION-TEST",
            category="publication",
            source_game_id="",
            field_name="public_page_enabled",
            allowed_actions="ENABLE_PUBLIC_PAGE | KEEP_DISABLED",
        )
        return [identity, selected, rejected, discrepancy, publication]

    def test_fill_review_expands_selected_and_rejected_conditionals(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            review = root / "review.csv"
            mapping = root / "map.json"
            write_csv(review, REVIEW_FIELDS, self.sample_rows())
            mapping.write_text(
                json.dumps(
                    {
                        "identity": {
                            "TESTRAW-00001": "MATCH_CANONICAL:CBBG-0000001"
                        },
                        "defaults": {
                            "discrepancy": "KEEP_CANONICAL",
                            "selected_conditional": "KEEP_CANONICAL",
                            "basis": (
                                "Owner Gate 1 approved ordinary reciprocal handling."
                            ),
                            "identity_basis": "Owner Gate 1 approved identity match.",
                        },
                        "decisions": {
                            "PUBLICATION-TEST": "ENABLE_PUBLIC_PAGE"
                        },
                        "basis_by_decision": {
                            "PUBLICATION-TEST": "Owner Gate 1 approved publication."
                        },
                    }
                ),
                encoding="utf-8",
            )
            counts = fill_review_from_map(review, mapping)
            self.assertEqual(counts["MATCH_CANONICAL:CBBG-0000001"], 1)
            self.assertEqual(counts["KEEP_CANONICAL"], 2)
            self.assertEqual(counts["NOT_APPLICABLE"], 1)
            self.assertEqual(counts["ENABLE_PUBLIC_PAGE"], 1)

            with review.open(encoding="utf-8-sig", newline="") as handle:
                rows = {r["decision_id"]: r for r in csv.DictReader(handle)}
            self.assertEqual(
                rows[
                    "CONDITIONAL-DISCREPANCY-TESTRAW-00001-"
                    "CBBG-0000001-GAME_DATE"
                ]["decision"],
                "KEEP_CANONICAL",
            )
            self.assertEqual(
                rows[
                    "CONDITIONAL-DISCREPANCY-TESTRAW-00001-"
                    "CBBG-0000002-GAME_DATE"
                ]["decision"],
                "NOT_APPLICABLE",
            )

    def test_carry_forward_requires_substantively_identical_review(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            old = root / "old.csv"
            new = root / "new.csv"
            rows = self.sample_rows()
            for row in rows:
                row["decision"] = (
                    "ENABLE_PUBLIC_PAGE"
                    if row["category"] == "publication"
                    else "KEEP_CANONICAL"
                )
                if row["category"] == "identity":
                    row["decision"] = "MATCH_CANONICAL:CBBG-0000001"
                if row["category"] == "conditional_discrepancy":
                    row["decision"] = (
                        "KEEP_CANONICAL"
                        if "CBBG-0000001" in row["decision_id"]
                        else "NOT_APPLICABLE"
                    )
                row["resolution_basis"] = "Approved basis."
            write_csv(old, REVIEW_FIELDS, rows)

            fresh = []
            for row in rows:
                copy = dict(row)
                copy["decision"] = "PENDING"
                copy["resolution_basis"] = ""
                fresh.append(copy)
            write_csv(new, REVIEW_FIELDS, fresh)

            counts = carry_forward_review(old, new)
            self.assertEqual(sum(counts.values()), len(rows))

            with new.open(encoding="utf-8-sig", newline="") as handle:
                carried = list(csv.DictReader(handle))
            self.assertTrue(
                all(r["resolution_basis"] == "Approved basis." for r in carried)
            )

            carried[0]["source_value"] = "changed"
            write_csv(new, REVIEW_FIELDS, carried)
            with self.assertRaises(Exception):
                carry_forward_review(old, new)


class VenueRebaseTests(unittest.TestCase):
    def test_collision_renumbers_new_identity_and_exact_key_reuses_existing(self):
        global_rows = [
            {
                "venue_id": "VEN-000010",
                "venue_key": "existing-arena",
                "display_name": "Existing Arena",
                "city": "Existing City",
                "state": "EX",
                "opened": "",
                "closed": "",
                "date_precision": "",
                "identity_status": "CURATED_SEED",
                "source_basis": "seed",
                "notes": "",
            }
        ]
        names = [
            {
                "venue_id": "VEN-000010",
                "venue_name": "Existing Arena",
                "normalized_name": "existingarena",
                "name_type": "PROJECT_DISPLAY",
                "valid_from": "",
                "valid_to": "",
                "date_precision": "",
                "source_basis": "seed",
                "notes": "",
            }
        ]
        local = [
            {
                "venue_key": "existing-arena",
                "venue_id": "VEN-999999",
                "canonical_name": "Old Sponsor Name",
                "aliases": "",
                "city": "Existing City",
                "state": "EX",
                "known_opened": "",
                "known_closed": "",
                "venue_date_precision": "unknown",
                "source_basis": "school source",
                "notes": "",
            },
            {
                "venue_key": "new-building",
                "venue_id": "VEN-000010",
                "canonical_name": "New Building",
                "aliases": "",
                "city": "New City",
                "state": "NW",
                "known_opened": "",
                "known_closed": "",
                "venue_date_precision": "unknown",
                "source_basis": "school source",
                "notes": "",
            },
        ]
        local_after, global_after, names_after, mappings = rebase_venues(
            "test",
            local,
            global_rows,
            names,
        )
        self.assertEqual(local_after[0]["venue_id"], "VEN-000010")
        self.assertEqual(local_after[1]["venue_id"], "VEN-000011")
        self.assertEqual(mappings[0]["resolution"], "REUSE_EXACT_KEY")
        self.assertEqual(mappings[1]["resolution"], "NEW_GLOBAL_IDENTITY")
        self.assertTrue(
            any(
                row["venue_id"] == "VEN-000010"
                and row["venue_name"] == "Old Sponsor Name"
                and row["name_type"] == "HISTORICAL_OR_ALIAS"
                for row in names_after
            )
        )
        self.assertTrue(
            any(row["venue_id"] == "VEN-000011" for row in global_after)
        )


if __name__ == "__main__":
    unittest.main()
