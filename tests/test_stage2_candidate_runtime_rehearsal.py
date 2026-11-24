import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_io import Stop  # noqa: E402
from stage2_candidate_runtime_rehearsal import (  # noqa: E402
    candidate_changed_paths,
    candidate_census_decision_universe,
    classify_candidate_result,
    validate_candidate_scope,
)


class CandidateRuntimeLiveMainScopeTests(unittest.TestCase):
    """Old frozen main ancestry must not count intervening main changes as PR edits."""

    @staticmethod
    def git(repo, *args):
        return subprocess.run(
            ["git", *args], cwd=repo, text=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        ).stdout.strip()

    def prepare(self, root):
        repo, remote = root / "candidate", root / "remote.git"
        self.git(root, "init", "-q", "--bare", str(remote))
        self.git(root, "init", "-q", "-b", "main", str(repo))
        self.git(repo, "config", "user.email", "fixture@example.invalid")
        self.git(repo, "config", "user.name", "Fixture")
        (repo / "data/reference").mkdir(parents=True)
        (repo / "data/reference/example.csv").write_text("old\n")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "historical request main")
        old = self.git(repo, "rev-parse", "HEAD")
        (repo / "data/reference/research-home-location-exceptions.csv").write_text("intervening main\n")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "main-only reference edit")
        main = self.git(repo, "rev-parse", "HEAD")
        self.git(repo, "remote", "add", "origin", str(remote))
        self.git(repo, "push", "-q", "origin", "main")
        self.git(repo, "fetch", "-q", "origin", "main")
        (repo / "tools").mkdir()
        (repo / "tools/example.py").write_text("print('tooling')\n")
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-qm", "candidate tooling")
        return repo, old, main, self.git(repo, "rev-parse", "HEAD")

    def test_main_only_data_change_excluded_from_pr_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, old, main, head = self.prepare(Path(tmp))
            paths, scoped_main = candidate_changed_paths(repo, old, head)
            self.assertEqual((paths, scoped_main), (["tools/example.py"], main))
            validate_candidate_scope(paths)

    def test_actual_candidate_data_edit_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, old, main, _ = self.prepare(Path(tmp))
            (repo / "data/reference/example.csv").write_text("candidate edit\n")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-qm", "forbidden candidate data change")
            paths, scoped_main = candidate_changed_paths(
                repo, old, self.git(repo, "rev-parse", "HEAD")
            )
            self.assertEqual(scoped_main, main)
            with self.assertRaisesRegex(Stop, "NON_TOOLING_PATHS"):
                validate_candidate_scope(paths)

    def test_candidate_without_current_main_ancestry_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo, old, _, _ = self.prepare(Path(tmp))
            self.git(repo, "checkout", "-q", "-b", "old-base", old)
            (repo / "tools").mkdir(exist_ok=True)
            (repo / "tools/example.py").write_text("print('stale')\n")
            self.git(repo, "add", ".")
            self.git(repo, "commit", "-qm", "stale candidate")
            with self.assertRaisesRegex(Stop, "NOT_BASED_ON_CURRENT_MAIN"):
                candidate_changed_paths(repo, old, self.git(repo, "rev-parse", "HEAD"))


class CandidateRuntimeScopeTests(unittest.TestCase):
    def test_generic_tooling_paths_are_allowed(self):
        validate_candidate_scope([
            "tools/onboarding_plan.py",
            "tests/test_example.py",
            "docs/implementation-efficiency-recovery.md",
            ".github/workflows/example.yml",
            "AGENTS.md",
        ])

    def test_basketball_data_path_is_rejected(self):
        with self.assertRaisesRegex(Stop, "NON_TOOLING_PATHS"):
            validate_candidate_scope([
                "tools/onboarding_plan.py",
                "schools/example/source-games.csv",
            ])

    def test_reference_data_path_is_rejected(self):
        with self.assertRaisesRegex(Stop, "NON_TOOLING_PATHS"):
            validate_candidate_scope([
                "data/reference/venues.csv",
            ])


class CandidateRuntimeDecisionUniverseTests(unittest.TestCase):
    def test_candidate_census_exposes_recomputed_decision_universe(self):
        value = "a" * 64
        self.assertEqual(
            candidate_census_decision_universe(
                {
                    "status": {
                        "preflight": {
                            "decision_universe_sha256": value,
                        }
                    }
                }
            ),
            value,
        )

    def test_candidate_census_requires_decision_universe_fingerprint(self):
        with self.assertRaisesRegex(
            Stop,
            "CANDIDATE_REHEARSAL_DECISION_UNIVERSE_MISSING",
        ):
            candidate_census_decision_universe(
                {"status": {"preflight": {}}}
            )


    def test_repaired_nonempty_universe_need_not_equal_blocked_empty_universe(self):
        blocked_empty_universe = (
            "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"
        )
        repaired_universe = "a" * 64
        repaired = {
            "status": {
                "preflight": {
                    "decision_count": 12,
                    "decision_universe_sha256": repaired_universe,
                }
            }
        }
        self.assertEqual(
            candidate_census_decision_universe(repaired),
            repaired_universe,
        )
        self.assertNotEqual(repaired_universe, blocked_empty_universe)


class CandidateRuntimeClassificationTests(unittest.TestCase):
    def test_gate1_ready_is_terminal_success(self):
        self.assertEqual(
            classify_candidate_result(
                {"last_error": "old blocker"},
                {"stage2_status": "OWNER_GATE_1_READY", "status": {}},
            ),
            "RESOLVED_TO_GATE1",
        )

    def test_different_blocker_is_material_progress(self):
        self.assertEqual(
            classify_candidate_result(
                {"last_error": "old blocker"},
                {
                    "stage2_status": "BLOCKED",
                    "status": {"last_error": "different blocker"},
                },
            ),
            "ADVANCED_TO_DIFFERENT_BLOCKER",
        )

    def test_same_coarse_site_error_with_reduced_blocker_population_advances(self):
        baseline_site = {
            "counts": {
                "strict_home_gap_rows": 13,
                "unaccounted_public_gap_rows": 5,
            },
            "examples": {
                "strict_home_gap_rows": ["HOME-1"],
                "unaccounted_public_gap_rows": [
                    "NEUTRAL-1",
                    "NEUTRAL-2",
                    "HOME-1",
                    "HOME-2",
                    "HOME-3",
                ],
            },
        }
        candidate_site = {
            "counts": {
                "strict_home_gap_rows": 13,
                "unaccounted_public_gap_rows": 3,
            },
            "examples": {
                "strict_home_gap_rows": ["HOME-1"],
                "unaccounted_public_gap_rows": [
                    "HOME-1",
                    "HOME-2",
                    "HOME-3",
                ],
            },
        }
        self.assertEqual(
            classify_candidate_result(
                {
                    "last_error": "site_completeness failed with exit code 1",
                    "site_diagnostic": baseline_site,
                },
                {
                    "stage2_status": "BLOCKED",
                    "status": {
                        "last_error": "site_completeness failed with exit code 1",
                    },
                    "site_diagnostic": candidate_site,
                },
            ),
            "ADVANCED_TO_DIFFERENT_BLOCKER",
        )

    def test_same_coarse_site_error_with_same_structured_blocker_is_no_progress(self):
        site = {
            "counts": {
                "strict_home_gap_rows": 13,
                "unaccounted_public_gap_rows": 5,
            },
            "examples": {
                "strict_home_gap_rows": ["HOME-1"],
                "unaccounted_public_gap_rows": ["NEUTRAL-1", "HOME-1"],
            },
        }
        self.assertEqual(
            classify_candidate_result(
                {
                    "last_error": "site_completeness failed with exit code 1",
                    "site_diagnostic": site,
                },
                {
                    "stage2_status": "BLOCKED",
                    "status": {
                        "last_error": "site_completeness failed with exit code 1",
                    },
                    "site_diagnostic": site,
                },
            ),
            "NO_PROGRESS_SAME_BLOCKER",
        )

    def test_same_blocker_is_no_progress(self):
        self.assertEqual(
            classify_candidate_result(
                {"last_error": "same blocker"},
                {
                    "stage2_status": "BLOCKED",
                    "status": {"last_error": "same blocker"},
                },
            ),
            "NO_PROGRESS_SAME_BLOCKER",
        )

    def test_missing_baseline_error_still_classifies_new_blocker(self):
        self.assertEqual(
            classify_candidate_result(
                {},
                {
                    "stage2_status": "BLOCKED",
                    "status": {"last_error": "candidate blocker"},
                },
            ),
            "ADVANCED_TO_DIFFERENT_BLOCKER",
        )


class CandidateRuntimeWorkflowRecoveryTests(unittest.TestCase):
    def test_targetless_not_attempted_read_only_recovery_is_supported(self):
        workflow = (
            ROOT / ".github/workflows/stage2-candidate-runtime-rehearsal.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("read_only_not_attempted = (", workflow)
        self.assertIn("classification == 'NOT_ATTEMPTED'", workflow)
        self.assertIn("recovery.get('target_branch') is None", workflow)
        self.assertIn("recovery.get('actual_target_sha') is None", workflow)
        self.assertIn(
            "not (read_only_not_attempted or mutation_target)",
            workflow,
        )
        self.assertIn("if mutation_target:", workflow)

    def test_fresh_opponent_display_successor_supports_live_census_rehearsal(self):
        workflow = (
            ROOT / ".github/workflows/stage2-candidate-runtime-rehearsal.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "last.get('operation') == 'STAGE2_OPPONENT_DISPLAY_NORMALIZE'",
            workflow,
        )
        self.assertIn(
            "mode = 'LIVE_CENSUS_AFTER_OPPONENT_DISPLAY'",
            workflow,
        )
        self.assertIn(
            "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
            workflow,
        )
        self.assertIn(
            "stage2_opponent_display_successor",
            workflow,
        )
        self.assertIn(
            "EXACT_LIVE_CENSUS_AFTER_OPPONENT_DISPLAY_REPLAY=PASS",
            workflow,
        )
        self.assertIn(
            'elif [[ "$AUTHORITY_MODE" == "LIVE_CENSUS_AFTER_OPPONENT_DISPLAY" ]]',
            workflow,
        )


    def test_fresh_blocked_census_replays_candidate_before_specialized_repairs(self):
        workflow = (
            ROOT / ".github/workflows/stage2-candidate-runtime-rehearsal.yml"
        ).read_text(encoding="utf-8")
        self.assertIn(
            "last.get('operation') == 'STAGE2_CENSUS'",
            workflow,
        )
        self.assertIn(
            "mode = 'BLOCKED_CENSUS_OPPONENT_REPRESENTATION'",
            workflow,
        )
        self.assertIn(
            "EXACT_BLOCKED_CENSUS_CANDIDATE_REPLAY=PASS",
            workflow,
        )
        self.assertIn(
            "verify_phase0_authority(",
            workflow,
        )
        self.assertIn(
            "run_stage2_census_tool(",
            workflow,
        )
        self.assertIn(
            "scratch_branch = (",
            workflow,
        )
        self.assertIn(
            "['git', '-C', str(candidate), 'branch', '-D', scratch_branch]",
            workflow,
        )
        self.assertIn(
            "baseline_blockers <= candidate_blockers",
            workflow,
        )
        self.assertIn(
            "int(preflight.get('warning_count', -1)) < 0",
            workflow,
        )
        self.assertNotIn(
            "int(preflight.get('warning_count', -1)) != 0",
            workflow,
        )
        self.assertIn(
            "verify_census_and_freeze_authority(",
            workflow,
        )
        self.assertIn(
            "run_normalizer_dry_run(",
            workflow,
        )
        self.assertIn(
            "classification = 'RESOLVED_BY_OPPONENT_REPRESENTATION'",
            workflow,
        )
        self.assertIn(
            "'accepted_legacy_warnings': repair_authority[",
            workflow,
        )
        self.assertIn(
            "baseline_decision_count == 0",
            workflow,
        )
        self.assertIn(
            "repaired_decision_count > 0",
            workflow,
        )
        self.assertIn(
            "repaired_universe != baseline_universe",
            workflow,
        )
        self.assertIn(
            "repeated_universe == repaired_universe",
            workflow,
        )
        self.assertIn(
            "repeated_stage2['artifact_normalized_sha256']",
            workflow,
        )
        self.assertIn(
            "== 'CAPABILITY_CENSUS_READY'",
            workflow,
        )
        self.assertIn(
            "list(repaired_plan.get('warnings') or [])",
            workflow,
        )
        self.assertNotIn(
            "int(repaired_preflight.get('decision_count', 0) or 0)\n"
            "                      == baseline_decision_count",
            workflow,
        )
        self.assertNotIn(
            "repaired_preflight.get('decision_universe_sha256')\n"
            "                      == baseline_universe",
            workflow,
        )
        self.assertIn(
            "classification = 'ADVANCED_TO_DIFFERENT_BLOCKER'",
            workflow,
        )
        self.assertIn(
            'elif [[ "$AUTHORITY_MODE" == "BLOCKED_CENSUS_OPPONENT_REPRESENTATION" ]]',
            workflow,
        )
        self.assertIn(
            "'candidate_scope_main_sha': scoped_main",
            workflow,
        )
        self.assertIn(
            "blocked-census-candidate-summary.json",
            workflow,
        )
        self.assertNotIn(
            "assert scoped_main == expected_main, (scoped_main, expected_main)",
            workflow,
        )

    def test_prepared_recovery_still_requires_authenticated_data_target(self):
        workflow = (
            ROOT / ".github/workflows/stage2-candidate-runtime-rehearsal.yml"
        ).read_text(encoding="utf-8")
        self.assertIn("valid_sha(target_sha)", workflow)
        self.assertIn("school.startswith('data/')", workflow)
        self.assertIn(
            "recovered-idle target no longer equals classified unpublished target",
            workflow,
        )


if __name__ == "__main__":
    unittest.main()
