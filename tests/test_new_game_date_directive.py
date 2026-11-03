import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS,
    WorkflowError,
    _new_game_date_patch_decision,
    apply_pre_ingest_source_patches,
    apply_reconciliation_decisions,
    approve_plan,
    frozen_owner_final_date_directives,
    read_csv,
)


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


class OwnerFinalNewGameDatePatchTests(unittest.TestCase):
    directive_line = (
        "- Owner-final Implementation reconciliation directive — "
        "STB-1982-83-028 — GAME_DATE: game_date=1983-03-09. "
        "Reconcile inherited date to 1983-03-09 during Implementation; "
        "exact site remains Civic Arena physical identity VEN-000241."
    )

    def make_repo(self, root: Path):
        school = root / "schools" / "st-bonaventure"
        onboarding = root / ".onboarding" / "st-bonaventure"
        school.mkdir(parents=True)
        onboarding.mkdir(parents=True)

        source_fields = [
            "source_game_id",
            "source_program_key",
            "season_label",
            "game_date",
            "normalized_opponent_key",
            "curated_game_type",
            "notes",
            "raw_text",
        ]
        write_csv(
            school / "source-games.csv",
            source_fields,
            [{
                "source_game_id": "STB-1982-83-028",
                "source_program_key": "st-bonaventure",
                "season_label": "1982-1983",
                "game_date": "1983-03-07",
                "normalized_opponent_key": "george-washington",
                "curated_game_type": "CONFERENCE_TOURNAMENT",
                "notes": "",
                "raw_text": "3/7 Geo. Wash. (A-10) 77-67 W",
            }],
        )
        source_notes = (
            "# source notes\n\n"
            "## Durable source register: stage3b-owner-authority-source-register.json\n\n"
            + self.directive_line
            + "\n"
        )
        source_notes_path = school / "source-notes.md"
        source_notes_path.write_text(source_notes, encoding="utf-8")
        manifest = {
            "status": "INTEGRATION_FROZEN",
            "school_key": "st-bonaventure",
            "package_member_sha256": {
                "source-notes.md": hashlib.sha256(
                    source_notes_path.read_bytes()
                ).hexdigest(),
            },
        }
        (onboarding / "integration-freeze.json").write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

        write_csv(
            root / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS,
            [],
        )
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS,
            [],
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            [],
        )
        return school

    def decision(self, repo: Path):
        directives = frozen_owner_final_date_directives(repo, "st-bonaventure")
        self.assertEqual(set(directives), {"STB-1982-83-028"})
        self.assertEqual(
            directives["STB-1982-83-028"]["game_date"],
            "1983-03-09",
        )
        source = read_csv(
            repo / "schools/st-bonaventure/source-games.csv"
        )[0]
        decision = _new_game_date_patch_decision(
            "st-bonaventure",
            source,
            ingest_school.NEW_GAME,
            directives["STB-1982-83-028"],
        )
        self.assertIsNotNone(decision)
        return decision

    def seal(self, repo: Path, decision, corrected="1983-03-09"):
        plan = {
            "school_key": "st-bonaventure",
            "blockers": [],
            "input_fingerprint": {"sha256": "frozen"},
            "decisions": [decision],
        }
        plan_path = repo / "plan.json"
        plan_path.write_text(json.dumps(plan), encoding="utf-8")
        review = {
            **decision,
            "decision": "APPLY_SOURCE_DATE_PATCH",
            "resolution_basis": (
                "Frozen owner-final Research directive for the 1983 A-10 tournament."
            ),
            "canonical_patch_json": "{}",
            "source_patch_json": json.dumps({"game_date": corrected}),
            "notes": "Original 1983-03-07; corrected 1983-03-09.",
        }
        review_path = repo / "review.csv"
        write_csv(
            review_path,
            REVIEW_COLUMNS,
            [{field: review.get(field, "") for field in REVIEW_COLUMNS}],
        )
        with patch(
            "onboarding_plan.input_fingerprint",
            return_value={"sha256": "frozen"},
        ):
            return approve_plan(
                repo,
                plan_path,
                review_path,
                "owner",
                approved_at="2026-11-03T00:00:00+00:00",
            )[0]

    def test_exact_st_bonaventure_directive_round_trips_through_seal_and_apply(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.make_repo(repo)
            decision = self.decision(repo)

            self.assertEqual(decision["category"], "new_game_date_patch")
            self.assertEqual(decision["source_game_date"], "1983-03-07")
            self.assertEqual(
                decision["allowed_source_date_value"],
                "1983-03-09",
            )
            self.assertEqual(
                decision["allowed_actions"],
                ["APPLY_SOURCE_DATE_PATCH"],
            )
            self.assertEqual(decision["planned_identity_status"], ingest_school.NEW_GAME)

            approved = self.seal(repo, decision)
            counts = apply_pre_ingest_source_patches(repo, approved)
            self.assertEqual(counts["new_game_date_patches"], 1)
            source = read_csv(
                repo / "schools/st-bonaventure/source-games.csv"
            )[0]
            self.assertEqual(source["game_date"], "1983-03-09")
            self.assertIn("OWNER_APPROVED_NEW_GAME_DATE_PATCH", source["notes"])

            assertion = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            assertion.update(source)
            assertion.update({
                "assertion_id": "ASRT-STB-DATE-0001",
                "canonical_game_id": "CBBG-TEST-DATE",
                "match_status": "CONFIDENT_MATCH",
                "match_method": "NEW_GAME",
            })
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS,
                [assertion],
            )

            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            team_a, team_b = ingest_school.ordered_pair(
                "st-bonaventure",
                "george-washington",
            )
            canonical.update({
                "canonical_game_id": "CBBG-TEST-DATE",
                "season_label": "1982-1983",
                "game_date": "1983-03-09",
                "date_precision": "EXACT",
                "team_a_key": team_a,
                "team_b_key": team_b,
                "game_type": "CONFERENCE_TOURNAMENT",
                "notes": "",
            })
            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )

            post = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(post["new_game_dates_verified"], 1)
            final = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(final["game_date"], "1983-03-09")
            self.assertIn("OWNER_APPROVED_NEW_GAME_DATE_PATCH", final["notes"])
            self.assertIn(
                decision["owner_final_directive_sha256"][:12],
                final["notes"],
            )

    def test_wrong_date_cannot_be_sealed(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.make_repo(repo)
            decision = self.decision(repo)
            with self.assertRaisesRegex(
                WorkflowError,
                "does not equal the frozen owner-final directive",
            ):
                self.seal(repo, decision, corrected="1983-03-10")

    def test_source_notes_hash_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            school = self.make_repo(repo)
            with (school / "source-notes.md").open("a", encoding="utf-8") as handle:
                handle.write("\nchanged after freeze\n")
            with self.assertRaisesRegex(
                WorkflowError,
                "does not match frozen source-notes.md",
            ):
                frozen_owner_final_date_directives(repo, "st-bonaventure")

    def test_non_directive_new_game_gets_no_date_decision(self):
        source = {
            "source_game_id": "OTHER-NEW-GAME",
            "source_program_key": "st-bonaventure",
            "season_label": "1982-1983",
            "game_date": "1983-03-07",
            "normalized_opponent_key": "george-washington",
            "curated_game_type": "CONFERENCE_TOURNAMENT",
        }
        self.assertIsNone(
            _new_game_date_patch_decision(
                "st-bonaventure",
                source,
                ingest_school.NEW_GAME,
                None,
            )
        )


if __name__ == "__main__":
    unittest.main()
