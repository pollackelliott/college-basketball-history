import csv
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
TESTS = ROOT / "tests"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TESTS))

from implementation_site_gate import implementation_site_report  # noqa: E402
from onboarding_hardening import fill_review_from_map  # noqa: E402
from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS,
    WorkflowError,
    _record_reciprocal_only_site_gap_provenance,
    _validate_reciprocal_only_site_gap_provenance_rows,
)
from test_implementation_site_gate import (  # noqa: E402
    ImplementationSiteGateTests,
    canonical_row,
    target_assertion,
)


def neutral_game(game_id="CBBG-0000001", *, game_type="REGULAR_SEASON"):
    return canonical_row(
        canonical_game_id=game_id,
        team_a_key="other",
        team_b_key="test",
        site_type="NEUTRAL",
        venue_key="",
        venue_id="",
        site_city="",
        site_state="",
        game_type=game_type,
        notes="",
        game_date="1919-02-01",
        team_a_score="11",
        team_b_score="25",
    )


def reciprocal(
    game_id="CBBG-0000001",
    *,
    program="other",
    source_id="OTHER-1",
    site="NEUTRAL",
    venue="",
    city="",
    state="",
    game_type="REGULAR_SEASON",
):
    row = target_assertion(
        canonical_game_id=game_id,
        source_program_key=program,
        source_game_id=source_id,
        normalized_opponent_key="test",
        curated_site_type=site,
        curated_venue_name=venue,
        city=city,
        state=state,
    )
    row["curated_game_type"] = game_type
    row["source_venue_name"] = ""
    return row


def plan(*, decisions=None):
    return {
        "school_key": "test",
        "decisions": decisions
        if decisions is not None
        else [
            {
                "decision_id": "PUBLICATION-test",
                "category": "publication",
                "canonical_game_id": "",
                "canonical_value": "",
                "allowed_actions": ["ENABLE_PUBLIC_PAGE", "KEEP_DISABLED"],
            }
        ],
    }


def provenance(game_id="CBBG-0000001", *, program="other", source_id="OTHER-1"):
    return {
        "canonical_game_id": game_id,
        "fields": ["venue", "location"],
        "reciprocal_source_program_key": program,
        "reciprocal_source_game_id": source_id,
        "resolution_basis": (
            "Reviewed reciprocal-only regular-season NEUTRAL evidence; the surviving "
            "record supports H/A/N but does not support venue or locality, so those "
            "fields remain explicitly unresolved."
        ),
    }


def validate(
    *,
    entries=None,
    canonical=None,
    assertions=None,
    sources=None,
    discrepancies=None,
    plan_value=None,
):
    return _validate_reciprocal_only_site_gap_provenance_rows(
        "test",
        plan_value if plan_value is not None else plan(),
        entries if entries is not None else [provenance()],
        canonical if canonical is not None else [neutral_game()],
        assertions if assertions is not None else [reciprocal()],
        sources if sources is not None else [],
        discrepancies if discrepancies is not None else [],
    )


class ReciprocalOnlySiteGapProvenanceTests(unittest.TestCase):
    def test_01_target_source_assertion_uses_ordinary_accounting(self):
        assertions = [
            reciprocal(),
            target_assertion(
                canonical_game_id="CBBG-0000001",
                source_program_key="test",
                source_game_id="TESTRAW-1",
                normalized_opponent_key="other",
                curated_site_type="NEUTRAL",
                curated_venue_name="",
                city="",
                state="",
            ),
        ]
        with self.assertRaisesRegex(WorkflowError, "target source assertion exists"):
            validate(assertions=assertions)

    def test_02_reciprocal_only_gap_validates_and_materializes(self):
        entries = validate()
        canonical = [neutral_game()]
        assertions = [reciprocal()]
        discrepancies = []
        approved = {
            **plan(),
            "site_gap_provenance": entries,
            "approved_plan_hash": "a" * 64,
        }

        result = _record_reciprocal_only_site_gap_provenance(
            "test",
            approved,
            canonical,
            assertions,
            [],
            discrepancies,
        )

        self.assertEqual(result["reciprocal_only_site_gap_games_accounted"], 1)
        self.assertEqual(result["reciprocal_only_site_gap_provenance_rows_added"], 2)
        self.assertEqual({row["field_name"] for row in discrepancies}, {"venue", "location"})
        self.assertTrue(all(row["status"] == "RESOLVED" for row in discrepancies))

    def test_03_materialization_does_not_invent_venue_or_locality(self):
        entries = validate()
        canonical = [neutral_game()]
        before = copy.deepcopy(canonical)
        discrepancies = []
        _record_reciprocal_only_site_gap_provenance(
            "test",
            {**plan(), "site_gap_provenance": entries, "approved_plan_hash": "b" * 64},
            canonical,
            [reciprocal()],
            [],
            discrepancies,
        )
        self.assertEqual(canonical, before)
        self.assertEqual(canonical[0]["venue_key"], "")
        self.assertEqual(canonical[0]["venue_id"], "")
        self.assertEqual(canonical[0]["site_city"], "")
        self.assertEqual(canonical[0]["site_state"], "")

    def test_04_materialization_does_not_change_han(self):
        entries = validate()
        canonical = [neutral_game()]
        _record_reciprocal_only_site_gap_provenance(
            "test",
            {**plan(), "site_gap_provenance": entries, "approved_plan_hash": "c" * 64},
            canonical,
            [reciprocal()],
            [],
            [],
        )
        self.assertEqual(canonical[0]["site_type"], "NEUTRAL")

    def test_05_materialization_does_not_create_target_assertion(self):
        entries = validate()
        assertions = [reciprocal()]
        before = copy.deepcopy(assertions)
        _record_reciprocal_only_site_gap_provenance(
            "test",
            {**plan(), "site_gap_provenance": entries, "approved_plan_hash": "d" * 64},
            [neutral_game()],
            assertions,
            [],
            [],
        )
        self.assertEqual(assertions, before)
        self.assertFalse(
            any(row.get("source_program_key") == "test" for row in assertions)
        )

    def test_06_field_specific_provenance_satisfies_public_site_gate(self):
        entries = validate()
        discrepancies = []
        _record_reciprocal_only_site_gap_provenance(
            "test",
            {**plan(), "site_gap_provenance": entries, "approved_plan_hash": "e" * 64},
            [neutral_game()],
            [reciprocal()],
            [],
            discrepancies,
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()
            fixture.make_repo(
                root,
                sources=[],
                canonical=[neutral_game()],
                assertions=[reciprocal()],
                discrepancies=[
                    {
                        "canonical_game_id": row["canonical_game_id"],
                        "source_a_program_key": row["source_a_program_key"],
                        "field_name": row["field_name"],
                        "status": row["status"],
                        "resolution_basis": row["resolution_basis"],
                    }
                    for row in discrepancies
                ],
            )
            report = implementation_site_report(root, "test")

        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 0)
        self.assertEqual(report["counts"]["public_gap_rows"], 1)

    def test_07_unreviewed_reciprocal_only_gap_remains_blocked(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()
            fixture.make_repo(
                root,
                sources=[],
                canonical=[neutral_game()],
                assertions=[reciprocal()],
                discrepancies=[],
            )
            report = implementation_site_report(root, "test")

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["counts"]["unaccounted_public_gap_rows"], 1)

    def test_08_materially_conflicting_reciprocal_han_fails_closed(self):
        assertions = [
            reciprocal(),
            reciprocal(
                program="third",
                source_id="THIRD-1",
                site="SOURCE_PROGRAM_HOME",
            ),
        ]
        with self.assertRaisesRegex(WorkflowError, "conflicting reciprocal H/A/N"):
            validate(assertions=assertions)

    def test_09_home_requirements_remain_strict_and_unwaived(self):
        home = neutral_game()
        home["site_type"] = "TEAM_B_HOME"
        with self.assertRaisesRegex(WorkflowError, "requires an already-established NEUTRAL"):
            validate(canonical=[home])

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()
            fixture.make_repo(
                root,
                sources=[],
                canonical=[home],
                assertions=[
                    reciprocal(site="OPPONENT_HOME")
                ],
                discrepancies=[
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "source_a_program_key": "other",
                        "field_name": "venue",
                        "status": "RESOLVED",
                        "resolution_basis": "Reviewed.",
                    },
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "source_a_program_key": "other",
                        "field_name": "location",
                        "status": "RESOLVED",
                        "resolution_basis": "Reviewed.",
                    },
                ],
            )
            report = implementation_site_report(root, "test")

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["counts"]["strict_home_gap_rows"], 1)

    def test_10_ncaa_and_postseason_strictness_remain_nonwaivable(self):
        ncaa = neutral_game(game_type="NCAA_TOURNAMENT")
        with self.assertRaisesRegex(WorkflowError, "cannot waive NCAA or other postseason"):
            validate(canonical=[ncaa])

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            fixture = ImplementationSiteGateTests()
            fixture.make_repo(
                root,
                sources=[],
                canonical=[ncaa],
                assertions=[reciprocal(game_type="NCAA_TOURNAMENT")],
                discrepancies=[
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "source_a_program_key": "other",
                        "field_name": "venue",
                        "status": "RESOLVED",
                        "resolution_basis": "Reviewed.",
                    },
                    {
                        "canonical_game_id": "CBBG-0000001",
                        "source_a_program_key": "other",
                        "field_name": "location",
                        "status": "RESOLVED",
                        "resolution_basis": "Reviewed.",
                    },
                ],
            )
            report = implementation_site_report(root, "test")

        self.assertEqual(report["status"], "FAIL")
        self.assertEqual(report["counts"]["strict_ncaa_gap_rows"], 1)

    def test_11_map_payload_does_not_expand_substantive_decision_count(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            review_path = root / "review.csv"
            map_path = root / "map.json"
            with review_path.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(REVIEW_COLUMNS))
                writer.writeheader()
                writer.writerow(
                    {
                        "decision_id": "PUBLICATION-test",
                        "category": "publication",
                        "allowed_actions": "ENABLE_PUBLIC_PAGE | KEEP_DISABLED",
                        "decision": "PENDING",
                    }
                )
            map_path.write_text(
                json.dumps(
                    {
                        "decisions": {"PUBLICATION-test": "ENABLE_PUBLIC_PAGE"},
                        "basis_by_decision": {
                            "PUBLICATION-test": "Publication only after every gate passes."
                        },
                        "site_gap_provenance": [provenance()],
                    }
                ),
                encoding="utf-8",
            )

            counts = fill_review_from_map(review_path, map_path)
            with review_path.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(sum(counts.values()), 1)
        self.assertEqual(len(rows), 1)
        payload = json.loads(rows[0]["site_gap_provenance_json"])
        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["canonical_game_id"], "CBBG-0000001")

    def test_12_exact_two_gw_diagnostic_topologies_are_generic_fixtures(self):
        games = [
            {
                **neutral_game("CBBG-0056182"),
                "team_a_key": "george-washington",
                "team_b_key": "maryland",
                "game_date": "1919-02-01",
                "team_a_score": "25",
                "team_b_score": "11",
            },
            {
                **neutral_game("CBBG-0056185"),
                "team_a_key": "george-washington",
                "team_b_key": "maryland",
                "game_date": "1919-03-08",
                "team_a_score": "53",
                "team_b_score": "20",
            },
        ]
        assertions = [
            {
                **reciprocal("CBBG-0056182", program="maryland", source_id="MDRAW-00040"),
                "normalized_opponent_key": "george-washington",
            },
            {
                **reciprocal("CBBG-0056185", program="maryland", source_id="MDRAW-00043"),
                "normalized_opponent_key": "george-washington",
            },
        ]
        entries = [
            {
                **provenance("CBBG-0056182", program="maryland", source_id="MDRAW-00040"),
            },
            {
                **provenance("CBBG-0056185", program="maryland", source_id="MDRAW-00043"),
            },
        ]
        gw_plan = {
            "school_key": "george-washington",
            "decisions": [
                {
                    "decision_id": "PUBLICATION-george-washington",
                    "category": "publication",
                    "canonical_game_id": "",
                    "canonical_value": "",
                    "allowed_actions": ["ENABLE_PUBLIC_PAGE", "KEEP_DISABLED"],
                }
            ],
        }
        normalized = _validate_reciprocal_only_site_gap_provenance_rows(
            "george-washington",
            gw_plan,
            entries,
            games,
            assertions,
            [],
            [],
        )
        before_games = copy.deepcopy(games)
        before_assertions = copy.deepcopy(assertions)
        discrepancies = []
        result = _record_reciprocal_only_site_gap_provenance(
            "george-washington",
            {
                **gw_plan,
                "site_gap_provenance": normalized,
                "approved_plan_hash": "f" * 64,
            },
            games,
            assertions,
            [],
            discrepancies,
        )

        self.assertEqual(result["reciprocal_only_site_gap_games_accounted"], 2)
        self.assertEqual(result["reciprocal_only_site_gap_provenance_rows_added"], 4)
        self.assertEqual(games, before_games)
        self.assertEqual(assertions, before_assertions)
        self.assertEqual(
            {row["canonical_game_id"] for row in discrepancies},
            {"CBBG-0056182", "CBBG-0056185"},
        )

    def test_13_available_reciprocal_site_evidence_must_be_reconciled(self):
        with self.assertRaisesRegex(WorkflowError, "reciprocal venue evidence exists"):
            validate(assertions=[reciprocal(venue="Known Arena")])
        with self.assertRaisesRegex(WorkflowError, "reciprocal locality evidence exists"):
            validate(assertions=[reciprocal(city="Washington", state="DC")])


if __name__ == "__main__":
    unittest.main()
