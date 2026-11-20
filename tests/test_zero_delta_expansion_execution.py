import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import onboard_school  # noqa: E402
import release_school  # noqa: E402
from onboarding_plan import WorkflowError  # noqa: E402


class ZeroDeltaExpansionExecutionTests(unittest.TestCase):
    def approved(self, **summary_overrides):
        population = [
            {"source_game_id": f"EX-{i:03}", "canonical_game_id": f"CBBG-{i:07}",
             "field_name": "team_score", "source_value": "61", "canonical_value": "60"}
            for i in range(13)
        ]
        summary = {
            "zero_delta_excluded_discrepancy_population": population,
            "inherited_stale_accomplishment_blockers_excluded": 1,
            "inherited_accomplishment_decisions_excluded": 0,
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
        mirrors=0, population=None,
    ):
        if population is None:
            population = self.approved()["summary"]["zero_delta_excluded_discrepancy_population"]
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
            onboard_school.ZERO_DELTA_DISCREPANCY_AUDIT_MARKER
            + json.dumps(population, sort_keys=True, separators=(",", ":")),
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
        self.assertIn("--zero-delta-discrepancy-audit", command)
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


    @mock.patch.object(onboard_school, "run")
    def test_same_count_swapped_discrepancy_identity_fails(self, runner):
        altered = self.approved()["summary"]["zero_delta_excluded_discrepancy_population"]
        altered[0]["canonical_game_id"] = "CBBG-9999999"
        runner.return_value = self.dry_run_output(population=altered)
        with self.assertRaisesRegex(WorkflowError, "discrepancy identities changed"):
            onboard_school._run_approved_ingestion(
                Path("."), "example", Path("plan.json"), self.approved(),
                {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 12},
            )

    @mock.patch.object(onboard_school, "run")
    def test_missing_audit_marker_fails(self, runner):
        runner.return_value = self.dry_run_output().replace(
            onboard_school.ZERO_DELTA_DISCREPANCY_AUDIT_MARKER, "OTHER="
        )
        with self.assertRaisesRegex(WorkflowError, "lacks exact discrepancy population"):
            onboard_school._run_approved_ingestion(
                Path("."), "example", Path("plan.json"), self.approved(),
                {"kind": "ZERO_DELTA_METADATA_ONLY", "inherited_source_game_count": 12},
            )

    def test_zero_delta_tracked_outputs_fail_closed(self):
        h = "a" * 64
        archive = "data/reconciliation/onboarding-decisions/example-" + h[:12] + ".json"
        onboard_school._assert_zero_delta_apply_paths(
            [archive, "site/data/teams/example.json"], "example", h
        )
        for forbidden in (
            "data/reference/historical-season-accounting.csv",
            "data/reference/programs.csv",
            "site/data/teams/other-school.json",
        ):
            with self.subTest(path=forbidden), self.assertRaisesRegex(
                WorkflowError, "unauthorized tracked paths"
            ):
                onboard_school._assert_zero_delta_apply_paths(
                    [archive, forbidden], "example", h
                )

    def test_snapshot_protects_registry_and_coverage_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            names = sorted(set(
                list(onboard_school.ZERO_DELTA_HISTORICAL_GLOBAL_PATHS)
                + [f"schools/example/{x}" for x in onboard_school.REQUIRED_PACKAGE_FILES]
                + ["data/reference/programs.csv",
                   "data/reference/conference-membership.csv",
                   "data/reference/historical-season-coverage.csv",
                   "data/reference/historical-season-accounting.csv"]
            ))
            for name in names:
                p = root / name
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("baseline\n")
            with mock.patch.object(
                onboard_school, "git", return_value="\0".join(names) + "\0"
            ):
                before = onboard_school._zero_delta_historical_state_snapshot(root, "example")
                (root / "data/reference/historical-season-accounting.csv").write_text(
                    "changed\n"
                )
                after = onboard_school._zero_delta_historical_state_snapshot(root, "example")
            with self.assertRaisesRegex(
                WorkflowError, "changed inherited historical state"
            ):
                onboard_school._assert_zero_delta_historical_state_unchanged(before, after)

    def test_stale_accomplishment_exception_requires_exact_verdict_and_match(self):
        output = (
            "example: STALE_ADMIN_DIFFERENCE | since 2000-2001\n"
            "FAIL: 1 program cross-check(s) need review."
        )
        def rows(path):
            if path.name == "programs.csv":
                return [], [{"program_key": "example",
                             "history_start_season": "2000-2001",
                             "history_scope_intervals": ""}]
            if path.name == "program-accomplishments.csv":
                return [], [{
                    "program_key": "example",
                    "verification_status": "OWNER_BASELINE_UNVERIFIED",
                    "canonical_crosscheck_status": "EXPLAINED_ADMIN_DIFFERENCE",
                    "ncaa_tournament_appearances": "1",
                    "final_four_appearances": "0",
                    "national_championships": "0",
                    "best_finish_key": "", "best_finish_year": "",
                }]
            return [], [{"canonical_game_id": "CBBG-1"}]
        derived = {
            "ncaa_tournament_appearances": 1, "final_four_appearances": 0,
            "national_championships": 0, "best_finish_key": None,
            "best_finish_year": None,
        }
        with mock.patch.object(onboard_school, "read_csv_table", side_effect=rows):
            with mock.patch("program_history.history_scope_errors", return_value=[]):
                with mock.patch(
                    "program_history.derive_top_level_ncaa_accomplishments",
                    return_value=derived,
                ):
                    self.assertIn(
                        "UNVERIFIED",
                        onboard_school._assert_inherited_stale_accomplishment(
                            Path("."), "example", output
                        ),
                    )
                    derived["ncaa_tournament_appearances"] = 2
                    with self.assertRaisesRegex(WorkflowError, "canonical conflict"):
                        onboard_school._assert_inherited_stale_accomplishment(
                            Path("."), "example", output
                        )
                    with self.assertRaisesRegex(WorkflowError, "different failure"):
                        onboard_school._assert_inherited_stale_accomplishment(
                            Path("."), "example",
                            output.replace("STALE_ADMIN_DIFFERENCE", "CONFLICT"),
                        )

    def test_exact_manifest_proof_carries_to_standalone_verification(self):
        summary = {**self.approved()["summary"], "already_public": True}
        proof = {"status": "PASS", "tracked_path_count": 25,
                 "snapshot_sha256": "a" * 64}
        manifest = {
            "school_key": "example", "approved_plan_hash": "b" * 64,
            "summary": summary,
            "execution": {
                "expansion_site_nonregression": {
                    "mode": onboard_school.EXPANSION_MODE,
                    "school_key": "example",
                },
                "zero_delta_historical_state_proof": proof,
            },
        }
        kwargs = onboard_school.correction_gate_kwargs_from_manifest(
            manifest, "example"
        )
        self.assertEqual(kwargs["zero_delta_historical_state_proof"], proof)
        self.assertEqual(kwargs["zero_delta_approved_plan_hash"], "b" * 64)
        manifest["execution"]["zero_delta_historical_state_proof"] = None
        with self.assertRaisesRegex(WorkflowError, "lacks sealed proofs"):
            onboard_school.correction_gate_kwargs_from_manifest(
                manifest, "example"
            )

    def test_legacy_release_requires_valid_expansion_freeze(self):
        summary = self.approved()["summary"]
        approved = {"school_key": "example", "summary": summary}
        manifest = {"summary": summary}
        with mock.patch.object(
            release_school, "correction_integration_freeze_bytes",
            return_value=None,
        ), mock.patch.object(
            onboard_school, "_validated_expansion_freeze_bytes",
            return_value=b"immutable freeze",
        ), mock.patch.object(
            onboard_school, "_authenticated_zero_delta_execution_context",
            return_value={"kind": "ZERO_DELTA_METADATA_ONLY"},
        ):
            self.assertEqual(
                release_school.runtime_integration_freeze_bytes(
                    Path("."), "example", manifest, approved
                ),
                (None, b"immutable freeze"),
            )
        with mock.patch.object(
            release_school, "correction_integration_freeze_bytes", return_value=None
        ), mock.patch.object(
            onboard_school, "_validated_expansion_freeze_bytes", return_value=None
        ):
            with self.assertRaisesRegex(WorkflowError, "lacks authenticated"):
                release_school.runtime_integration_freeze_bytes(
                    Path("."), "example", manifest, approved
                )


    def test_gate_proof_fails_closed_when_canonical_snapshot_differs(self):
        summary = self.approved()["summary"]
        snapshot = {"data/canonical/games.csv": "a" * 64}
        proof = onboard_school._assert_zero_delta_historical_state_unchanged(
            snapshot, dict(snapshot)
        )
        with mock.patch.object(
            onboard_school, "_authenticated_zero_delta_execution_context",
            return_value={"kind": "ZERO_DELTA_METADATA_ONLY"},
        ), mock.patch.object(
            onboard_school, "_zero_delta_historical_state_snapshot",
            return_value=snapshot,
        ):
            self.assertIsNotNone(
                onboard_school._zero_delta_gate_context(
                    Path("."), "example", self.approved(), summary, proof
                )
            )
            bad = dict(proof, snapshot_sha256="b" * 64)
            with self.assertRaisesRegex(WorkflowError, "drifted at gate"):
                onboard_school._zero_delta_gate_context(
                    Path("."), "example", self.approved(), summary, bad
                )
            with self.assertRaisesRegex(WorkflowError, "differs from sealed"):
                onboard_school._zero_delta_gate_context(
                    Path("."), "example", self.approved(),
                    dict(summary, inherited_unrelated_reviews_excluded=12), proof
                )

    def test_zero_delta_is_not_mistaken_for_correction_freeze(self):
        manifest = {"summary": self.approved()["summary"]}
        self.assertIsNone(
            release_school.correction_integration_freeze_bytes(
                Path("."), "example", manifest
            )
        )

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
