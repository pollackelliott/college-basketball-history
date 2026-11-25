"""Regression guard: Stage 2 candidate-runtime is not a Stage 1 startup gate.

This static contract checks the actual GitHub Actions job expression. Stage 2
workflow_dispatch and other tooling PRs must keep their existing guard.
"""
from pathlib import Path
import unittest


WORKFLOW = (
    Path(__file__).resolve().parents[1]
    / ".github/workflows/stage2-candidate-runtime-rehearsal.yml"
)


class Stage2CandidateRuntimeScopeTests(unittest.TestCase):
    def test_stage1_tooling_excluded_without_disabling_other_candidate_checks(self):
        raw = WORKFLOW.read_text(encoding="utf-8")
        section = raw.split("  rehearse-candidate-runtime:\n", 1)[1].split(
            "    runs-on:", 1
        )[0]
        self.assertIn("github.event_name == 'workflow_dispatch'", section)
        self.assertIn(
            "github.event.pull_request.head.repo.full_name == github.repository",
            section,
        )
        self.assertIn(
            "startsWith(github.event.pull_request.head.ref, 'tooling/')",
            section,
        )
        self.assertIn(
            "!contains(github.event.pull_request.head.ref, 'expansion-stage1-')",
            section,
        )
        # The exclusion is scoped to the candidate-runtime job, not the
        # Stage 2 workflow-dispatch authority logic or the Stage 1 CI jobs.
        self.assertEqual(
            raw.count("!contains(github.event.pull_request.head.ref, 'expansion-stage1-')"),
            1,
        )


if __name__ == "__main__":
    unittest.main()
