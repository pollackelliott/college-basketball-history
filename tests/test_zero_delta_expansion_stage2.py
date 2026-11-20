import csv
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from zero_delta_expansion_stage2 import (  # noqa: E402
    ZERO_DELTA_STALE_ACCOMPLISHMENT_BLOCKER,
    ZeroDeltaExpansionError,
    apply_zero_delta_projection,
    authenticate_zero_delta_expansion,
)


def canonical_row_sha256(row):
    payload = (
        json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


class ZeroDeltaExpansionStage2Tests(unittest.TestCase):
    def fixture(self, root: Path):
        school = "example-school"
        school_dir = root / "schools" / school
        school_dir.mkdir(parents=True)
        source_bytes = (
            "source_game_id,source_program_key,season_label\n"
            "EX-001,example-school,2000-2001\n"
        ).encode("utf-8")
        (school_dir / "source-games.csv").write_bytes(source_bytes)
        source_sha = hashlib.sha256(source_bytes).hexdigest()

        ref_dir = root / "data" / "reference"
        ref_dir.mkdir(parents=True)
        accomplishment = {
            "program_key": school,
            "verification_status": "OWNER_BASELINE_UNVERIFIED",
            "canonical_crosscheck_status": "EXPLAINED_ADMIN_DIFFERENCE",
            "verification_basis": "accepted inherited baseline",
        }
        fields = list(accomplishment)
        with (ref_dir / "program-accomplishments.csv").open(
            "w", newline="", encoding="utf-8"
        ) as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerow(accomplishment)

        manifest_dir = root / ".onboarding" / school
        manifest_dir.mkdir(parents=True)
        manifest = {
            "kind": "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
            "status": "INTEGRATION_FROZEN",
            "school_key": school,
            "source_preservation": {
                "inherited_count": 1,
                "supplemental_count": 0,
                "combined_count": 1,
            },
            "package_member_sha256": {"source-games.csv": source_sha},
            "baseline_package_member_sha256": {"source-games.csv": source_sha},
            "opponent_support_actions": {
                "NEW_SUPPLEMENTAL": 0,
                "REUSE_INHERITED": 0,
                "EXTEND_INHERITED": 0,
            },
            "venue_support_actions": {
                "NEW_SUPPLEMENTAL": 0,
                "REUSE_INHERITED": 0,
                "EXTEND_INHERITED": 0,
            },
            "canonical_identity_counts": {
                "IDENTITY_REVIEW_BLOCKER": 0,
                "PROVISIONAL_NEW_CANONICAL": 0,
                "REUSE_CANONICAL": 0,
            },
            "canonical_reuses": [],
            "unresolved_history_decisions": 0,
            "current_main_reconciliation": {
                "changed_source_game_ids": [],
            },
            "accomplishment_status": "PRESENT",
            "accomplishment_row_sha256": canonical_row_sha256(accomplishment),
        }
        path = manifest_dir / "integration-freeze.json"
        path.write_text(json.dumps(manifest), encoding="utf-8")
        return school, path, manifest

    def plan(self):
        decisions = [
            {
                "decision_id": f"DISCREPANCY-EX-{i:03d}",
                "category": "discrepancy",
                "source_game_id": f"EX-{i:03d}",
                "canonical_game_id": f"CBBG-{i:07}",
                "field_name": "team_score",
                "source_value": "61",
                "canonical_value": "60",
            }
            for i in range(13)
        ]
        decisions.append(
            {
                "decision_id": "ACCOMPLISHMENTS-example-school",
                "category": "accomplishments",
                "source_game_id": "",
            }
        )
        return {
            "summary": {
                "new_canonical_games": 0,
                "identity_review_required": 0,
                "assertions_to_add": 0,
                "canonical_enrichment_games": 0,
                "canonical_enrichment_fields": 0,
                "conditional_discrepancies": 0,
                "canonical_site_patch_reviews": 0,
                "discrepancies_to_add": 13,
                "affected_public_programs": ["other-school"],
            },
            "blockers": [ZERO_DELTA_STALE_ACCOMPLISHMENT_BLOCKER],
            "decisions": decisions,
            "identity_collision_groups": [],
            "identity_cardinality_constraints": [],
        }

    def test_authenticates_exact_zero_delta_freeze(self):
        with tempfile.TemporaryDirectory() as temp:
            school, _, _ = self.fixture(Path(temp))
            context = authenticate_zero_delta_expansion(Path(temp), school)
            self.assertEqual(context["kind"], "ZERO_DELTA_METADATA_ONLY")
            self.assertEqual(context["inherited_source_game_count"], 1)

    def test_nonzero_supplemental_population_is_not_zero_delta(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            school, path, manifest = self.fixture(root)
            manifest["source_preservation"]["supplemental_count"] = 1
            manifest["source_preservation"]["combined_count"] = 2
            path.write_text(json.dumps(manifest), encoding="utf-8")
            self.assertIsNone(authenticate_zero_delta_expansion(root, school))

    def test_source_game_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            school, _, _ = self.fixture(root)
            (root / "schools" / school / "source-games.csv").write_text(
                "source_game_id,source_program_key,season_label\n"
                "EX-001,example-school,2001-2002\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ZeroDeltaExpansionError, "source-game bytes differ"
            ):
                authenticate_zero_delta_expansion(root, school)

    def test_accomplishment_authority_drift_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            school, _, _ = self.fixture(root)
            path = root / "data" / "reference" / "program-accomplishments.csv"
            path.write_text(
                "program_key,verification_status,canonical_crosscheck_status,verification_basis\n"
                "example-school,VERIFIED,MATCH,changed\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(
                ZeroDeltaExpansionError, "accomplishment authority drifted"
            ):
                authenticate_zero_delta_expansion(root, school)

    def test_kentucky_shape_excludes_thirteen_inherited_decisions(self):
        plan = self.plan()
        apply_zero_delta_projection(
            plan,
            {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 3232},
        )
        self.assertEqual(plan["blockers"], [])
        self.assertEqual(plan["decisions"], [])
        self.assertEqual(plan["summary"]["inherited_unrelated_reviews_excluded"], 13)
        self.assertEqual(
            len(plan["summary"]["zero_delta_excluded_discrepancy_population"]), 13
        )
        self.assertEqual(
            plan["summary"]["inherited_accomplishment_decisions_excluded"], 1
        )
        self.assertEqual(
            plan["summary"]["inherited_stale_accomplishment_blockers_excluded"], 1
        )
        self.assertEqual(plan["summary"]["discrepancies_to_add"], 0)
        self.assertEqual(plan["summary"]["affected_public_programs"], [])

    def test_unrelated_blocker_is_retained(self):
        plan = self.plan()
        plan["blockers"].append("GENUINE_OTHER_BLOCKER")
        apply_zero_delta_projection(
            plan,
            {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 1},
        )
        self.assertEqual(plan["blockers"], ["GENUINE_OTHER_BLOCKER"])

    def test_unexpected_decision_category_fails_closed(self):
        plan = self.plan()
        plan["decisions"].append(
            {
                "decision_id": "IDENTITY-EX-999",
                "category": "identity",
                "source_game_id": "EX-999",
            }
        )
        with self.assertRaisesRegex(
            ZeroDeltaExpansionError, "unsupported Stage 2 decision categories"
        ):
            apply_zero_delta_projection(
                plan,
                {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 1},
            )

    def test_new_canonical_work_fails_closed(self):
        plan = self.plan()
        plan["summary"]["new_canonical_games"] = 1
        with self.assertRaisesRegex(
            ZeroDeltaExpansionError, "non-baseline Stage 2 work"
        ):
            apply_zero_delta_projection(
                plan,
                {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 1},
            )


if __name__ == "__main__":
    unittest.main()
