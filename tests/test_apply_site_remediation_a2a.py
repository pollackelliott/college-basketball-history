import csv
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import apply_site_remediation_a2a as a2a  # noqa: E402


CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "team_a_key",
    "team_b_key",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "notes",
]


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def review_row(
    game_id,
    *,
    raw,
    proposed="TEAM_A_HOME",
    source_form="OPPONENT_HOME",
    source_program="beta",
    source_id="BRAW-1",
    profile="SITE_ASSERTION_ONLY",
):
    home = "alpha" if proposed == "TEAM_A_HOME" else "beta" if proposed == "TEAM_B_HOME" else ""
    return {
        "canonical_game_id": game_id,
        "season_label": "2000-2001",
        "team_a_key": "alpha",
        "team_b_key": "beta",
        "current_site_type": "UNKNOWN",
        "proposed_site_type": proposed,
        "proposed_home_team_key": home,
        "supporting_programs": source_program,
        "supporting_source_game_ids": source_id,
        "supporting_assertion_count": "1",
        "other_participant_evidence_state": "OTHER_PARTICIPANT_UNKNOWN_ASSERTION",
        "site_discrepancy_statuses": "",
        "source_site_forms": source_form,
        "source_site_candidates": raw,
        "evidence_profile": profile,
    }


class ApplySiteRemediationA2ATests(unittest.TestCase):
    def make_repo(self, root: Path):
        games = [
            {
                "canonical_game_id": "CBBG-0000001",
                "season_label": "2000-2001",
                "team_a_key": "alpha",
                "team_b_key": "beta",
                "site_type": "UNKNOWN",
                "designated_home_team_key": "",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "notes": "",
            },
            {
                "canonical_game_id": "CBBG-0000002",
                "season_label": "2000-2001",
                "team_a_key": "alpha",
                "team_b_key": "beta",
                "site_type": "UNKNOWN",
                "designated_home_team_key": "",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "notes": "",
            },
            {
                "canonical_game_id": "CBBG-0000003",
                "season_label": "2000-2001",
                "team_a_key": "alpha",
                "team_b_key": "beta",
                "site_type": "UNKNOWN",
                "designated_home_team_key": "",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "notes": "",
            },
        ]
        write_csv(root / "data/canonical/games.csv", CANONICAL_FIELDS, games)
        for relative in (
            "data/evidence/game-assertions.csv",
            "data/reconciliation/discrepancies.csv",
        ):
            write_csv(root / relative, ["placeholder"], [])
        for relative in (
            "tools/site_remediation_audit.py",
            "tools/site_remediation_tier_report.py",
            "tools/site_remediation_a2_review.py",
            "tools/site_remediation_a2_census.py",
            "tools/apply_site_remediation_a2a.py",
        ):
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(relative + "\n", encoding="utf-8")

    def initial_review(self):
        return {
            "summary": {"status": "PASS"},
            "rows": [
                review_row("CBBG-0000001", raw="H", source_form="SOURCE_PROGRAM_HOME", source_program="alpha", source_id="ARAW-1"),
                review_row("CBBG-0000002", raw="at", source_form="OPPONENT_HOME", source_program="beta", source_id="BRAW-2", profile="VENUE_AND_LOCATION"),
                review_row("CBBG-0000003", raw="3", proposed="NEUTRAL", source_form="NEUTRAL", source_program="beta", source_id="BRAW-3"),
            ],
        }

    def dynamic_review(self, repo: Path):
        current = {
            row["canonical_game_id"]: row
            for row in read_rows(repo / "data/canonical/games.csv")
        }
        rows = []
        for row in self.initial_review()["rows"]:
            if current[row["canonical_game_id"]]["site_type"] == "UNKNOWN":
                rows.append(row)
        return {"summary": {"status": "PASS"}, "rows": rows}

    def owner_count_patch(self):
        return patch.multiple(
            a2a,
            EXPECTED_APPROVED_COUNT=2,
            EXPECTED_HELD_COUNT=1,
            EXPECTED_HELD_RAW_COUNTS={"3": 1},
        )

    def test_plan_selects_explicit_and_at_but_holds_opaque_code(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            with self.owner_count_patch(), patch.object(a2a, "build_a2_review", return_value=self.initial_review()):
                plan = a2a.build_a2a_plan(repo)
            self.assertEqual(plan["payload"]["approved_count"], 2)
            self.assertEqual(plan["payload"]["held_count"], 1)
            self.assertEqual(
                [row["canonical_game_id"] for row in plan["payload"]["approved"]],
                ["CBBG-0000001", "CBBG-0000002"],
            )
            self.assertEqual(plan["payload"]["held"][0]["raw_site_candidate"], "3")

    def test_apply_changes_only_site_semantics_and_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)

            def review_builder(_repo):
                return self.dynamic_review(repo)

            with self.owner_count_patch(), patch.object(a2a, "build_a2_review", side_effect=review_builder):
                plan = a2a.build_a2a_plan(repo)
                result = a2a.apply_a2a_plan(repo, plan["sha256"], run_validation=False)

            self.assertEqual(result["applied_games"], 2)
            self.assertEqual(result["held_games"], 1)
            rows = {row["canonical_game_id"]: row for row in read_rows(repo / "data/canonical/games.csv")}

            explicit = rows["CBBG-0000001"]
            self.assertEqual(explicit["site_type"], "TEAM_A_HOME")
            self.assertEqual(explicit["designated_home_team_key"], "alpha")
            self.assertIn("SITE_ASSERTION_PROPAGATION", explicit["notes"])

            at_row = rows["CBBG-0000002"]
            self.assertEqual(at_row["site_type"], "TEAM_A_HOME")
            self.assertEqual(at_row["designated_home_team_key"], "alpha")
            # A2a deliberately does not apply physical support.
            self.assertEqual(at_row["venue_id"], "")
            self.assertEqual(at_row["venue_key"], "")
            self.assertEqual(at_row["site_city"], "")
            self.assertEqual(at_row["site_state"], "")

            held = rows["CBBG-0000003"]
            self.assertEqual(held["site_type"], "UNKNOWN")
            self.assertEqual(held["notes"], "")

    def test_apply_requires_exact_plan_hash(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            with self.owner_count_patch(), patch.object(a2a, "build_a2_review", return_value=self.initial_review()):
                with self.assertRaises(a2a.A2AApplyError):
                    a2a.apply_a2a_plan(repo, "wrong-hash", run_validation=False)
            self.assertTrue(all(row["site_type"] == "UNKNOWN" for row in read_rows(repo / "data/canonical/games.csv")))

    def test_owner_boundary_rejects_changed_held_signature(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            changed = self.initial_review()
            changed["rows"][2] = review_row(
                "CBBG-0000003",
                raw="mystery",
                proposed="NEUTRAL",
                source_form="NEUTRAL",
                source_program="beta",
                source_id="BRAW-3",
            )
            with self.owner_count_patch(), patch.object(a2a, "build_a2_review", return_value=changed):
                with self.assertRaises(a2a.A2AApplyError):
                    a2a.build_a2a_plan(repo)

    def test_reciprocal_state_must_remain_unknown(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)
            bad = self.initial_review()
            bad["rows"][0] = dict(bad["rows"][0])
            bad["rows"][0]["other_participant_evidence_state"] = "OTHER_PARTICIPANT_HAS_KNOWN_SITE"
            with self.owner_count_patch(), patch.object(a2a, "build_a2_review", return_value=bad):
                with self.assertRaises(a2a.A2AApplyError):
                    a2a.build_a2a_plan(repo)


if __name__ == "__main__":
    unittest.main()
