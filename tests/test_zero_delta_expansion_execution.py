import sys
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import onboard_school  # noqa: E402
from onboarding_plan import WorkflowError  # noqa: E402


class ZeroDeltaExpansionExecutionTests(unittest.TestCase):
    def approved(self, **summary_overrides):
        summary = {
            "expansion_transaction_kind": "ZERO_DELTA_METADATA_ONLY",
            "zero_delta_inherited_source_game_count": 12,
            "new_canonical_games": 0,
            "identity_review_required": 0,
            "assertions_to_add": 0,
            "canonical_enrichment_games": 0,
            "canonical_enrichment_fields": 0,
            "conditional_discrepancies": 0,
            "canonical_site_patch_reviews": 0,
            "source_rows": 12,
            "in_scope_source_rows": 12,
            "existing_game_matches": 12,
            "discrepancies_to_add": 0,
            "inherited_unrelated_reviews_excluded": 13,
        }
        summary.update(summary_overrides)
        return {"school_key": "example", "summary": summary, "decisions": []}

    @mock.patch.object(onboard_school, "authenticate_zero_delta_expansion")
    def test_exact_zero_delta_plan_authenticates_execution_exception(self, auth):
        auth.return_value = {
            "kind": "ZERO_DELTA_METADATA_ONLY",
            "inherited_source_game_count": 12,
        }
        context = onboard_school._authenticated_zero_delta_execution_context(
            Path("."), self.approved()
        )
        self.assertEqual(context["kind"], "ZERO_DELTA_METADATA_ONLY")

    @mock.patch.object(onboard_school, "authenticate_zero_delta_expansion")
    def test_nonzero_historical_work_cannot_claim_zero_delta_exception(self, auth):
        auth.return_value = {
            "kind": "ZERO_DELTA_METADATA_ONLY",
            "inherited_source_game_count": 12,
        }
        with self.assertRaisesRegex(WorkflowError, "surfaced historical work"):
            onboard_school._authenticated_zero_delta_execution_context(
                Path("."), self.approved(new_canonical_games=1)
            )

    @mock.patch.object(onboard_school, "authenticate_zero_delta_expansion")
    def test_untrusted_zero_delta_marker_fails_closed(self, auth):
        auth.return_value = None
        with self.assertRaisesRegex(WorkflowError, "lacks authenticated zero-delta"):
            onboard_school._authenticated_zero_delta_execution_context(
                Path("."), self.approved()
            )

    @mock.patch.object(onboard_school, "annotate_reciprocal_only_unknown_site_provenance")
    @mock.patch.object(onboard_school, "backfill_resolved_target_home_chronology")
    @mock.patch.object(onboard_school, "backfill_reciprocal_only_home_chronology")
    def test_true_zero_delta_skips_inherited_baseline_site_remediation(
        self, reciprocal, resolved, unknown
    ):
        results = onboard_school._run_inherited_baseline_site_compatibility(
            Path("."),
            "example",
            zero_delta_context={"kind": "ZERO_DELTA_METADATA_ONLY"},
        )
        reciprocal.assert_not_called()
        resolved.assert_not_called()
        unknown.assert_not_called()
        self.assertTrue(
            all(item["skipped_zero_delta_inherited_baseline"] for item in results)
        )

    @mock.patch.object(onboard_school, "annotate_reciprocal_only_unknown_site_provenance")
    @mock.patch.object(onboard_school, "backfill_resolved_target_home_chronology")
    @mock.patch.object(onboard_school, "backfill_reciprocal_only_home_chronology")
    def test_nonzero_or_ordinary_expansion_still_runs_site_remediation(
        self, reciprocal, resolved, unknown
    ):
        reciprocal.return_value = {"applied_games": 0}
        resolved.return_value = {"applied_games": 0}
        unknown.return_value = {"annotated_games": 0}
        onboard_school._run_inherited_baseline_site_compatibility(
            Path("."), "example", zero_delta_context=None
        )
        reciprocal.assert_called_once()
        resolved.assert_called_once()
        unknown.assert_called_once()


    def dry_run_output(
        self, *, discrepancies=13, assertions=0, matches=12, enrichments=0,
        mirrors=0,
    ):
        return "\n".join([
            "College Basketball History — school ingestion",
            "Mode:       DRY RUN",
            "Source rows:                         12",
            "Publication-eligible source rows:   12",
            f"Existing-game matches:      {matches}",
            "New canonical games:        0",
            "Identity review required:   0",
            f"Canonical enrichments:       0 games / {enrichments} fields",
            f"Assertions to add:           {assertions}",
            f"Local assertion mirrors:     {mirrors}",
            f"Discrepancies to add:        {discrepancies}",
            "DRY RUN COMPLETE: no files changed.",
        ])

    @mock.patch.object(onboard_school, "run")
    def test_authenticated_zero_delta_uses_strict_read_only_ingestion(self, runner):
        runner.return_value = self.dry_run_output()
        output, proof = onboard_school._run_approved_ingestion(
            Path("."), "example", Path("sealed-plan.json"), self.approved(),
            {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 12},
        )
        command = runner.call_args.args[0]
        self.assertIn("--check-package", command)
        self.assertNotIn("--apply", command)
        self.assertIn("--identity-decisions", command)
        self.assertEqual(output, runner.return_value)
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["inherited_discrepancies_preserved"], 13)
        self.assertEqual(proof["tracked_historical_write"], "NONE")

    @mock.patch.object(onboard_school, "run")
    def test_zero_delta_rejects_unplanned_discrepancy_population(self, runner):
        runner.return_value = self.dry_run_output(discrepancies=14)
        with self.assertRaisesRegex(WorkflowError, "unapproved work"):
            onboard_school._run_approved_ingestion(
                Path("."), "example", Path("sealed-plan.json"), self.approved(),
                {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 12},
            )
        self.assertNotIn("--apply", runner.call_args.args[0])

    @mock.patch.object(onboard_school, "run")
    def test_zero_delta_rejects_new_assertions_or_enrichments(self, runner):
        context = {
            "kind": "ZERO_DELTA_METADATA_ONLY",
            "inherited_source_game_count": 12,
        }
        for output in [
            self.dry_run_output(assertions=1),
            self.dry_run_output(enrichments=1),
            self.dry_run_output(mirrors=1),
        ]:
            with self.subTest(output=output):
                runner.return_value = output
                with self.assertRaisesRegex(
                    WorkflowError, "unapproved work|enrichment work|mirror work"
                ):
                    onboard_school._run_approved_ingestion(
                        Path("."), "example", Path("sealed-plan.json"),
                        self.approved(), context,
                    )

    @mock.patch.object(onboard_school, "run")
    def test_zero_delta_requires_dry_run_completion(self, runner):
        runner.return_value = self.dry_run_output().replace(
            "DRY RUN COMPLETE: no files changed.", "STOP: source identity review"
        )
        with self.assertRaisesRegex(WorkflowError, "did not complete"):
            onboard_school._run_approved_ingestion(
                Path("."), "example", Path("sealed-plan.json"), self.approved(),
                {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 12},
            )

    @mock.patch.object(onboard_school, "run")
    def test_normal_ingestion_still_applies(self, runner):
        runner.return_value = "PASS: ingestion applied"
        output, proof = onboard_school._run_approved_ingestion(
            Path("."), "example", Path("sealed-plan.json"),
            {"school_key": "example", "summary": {}}, None,
        )
        self.assertIn("--apply", runner.call_args.args[0])
        self.assertNotIn("--check-package", runner.call_args.args[0])
        self.assertEqual(output, runner.return_value)
        self.assertIsNone(proof)

    def test_altered_inherited_historical_row_fails_nonmutation_proof(self):
        before = {
            "data/canonical/games.csv": "a" * 64,
            "schools/example/source-games.csv": "b" * 64,
        }
        after = dict(before, **{"data/canonical/games.csv": "c" * 64})
        with self.assertRaisesRegex(WorkflowError, "changed inherited historical state"):
            onboard_school._assert_zero_delta_historical_state_unchanged(
                before, after
            )

    def test_unchanged_inherited_historical_state_produces_proof(self):
        snapshot = {
            "data/canonical/games.csv": "a" * 64,
            "schools/example/source-games.csv": "b" * 64,
        }
        proof = onboard_school._assert_zero_delta_historical_state_unchanged(
            snapshot, dict(snapshot)
        )
        self.assertEqual(proof["status"], "PASS")
        self.assertEqual(proof["tracked_path_count"], 2)
        self.assertEqual(len(proof["snapshot_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
