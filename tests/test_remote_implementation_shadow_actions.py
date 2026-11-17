"""Fail-closed contract of the GitHub-hosted, read-only shadow pilot.

Static tests deliberately avoid depending on PyYAML or any external service.
They verify that the event-driven pilot uses trusted main, read-only scope,
and the existing non-mutating Stage A observer.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (
    ROOT / ".github" / "workflows" / "remote-implementation-shadow.yml"
)


class ShadowActionsContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_one_repository_owned_workflow_run_trigger_and_main_bootstrap(self):
        text = self.workflow
        self.assertIn("name: Remote Implementation shadow observation", text)
        self.assertIn("  workflow_run:", text)
        self.assertIn("      - Remote Implementation control plane", text)
        self.assertIn("      - completed", text)
        self.assertIn("  push:", text)
        self.assertIn("      - main", text)
        self.assertIn(
            "      - .github/workflows/remote-implementation-shadow.yml",
            text,
        )
        self.assertNotIn("workflow_dispatch:", text)
        self.assertNotIn("schedule:", text)
        self.assertNotIn("pull_request:", text)

    def test_effective_token_scope_is_read_only(self):
        text = self.workflow
        self.assertRegex(text, r"(?m)^permissions:\n  contents: read\n")
        self.assertEqual(len(re.findall(r"(?m)^permissions:", text)), 1)
        self.assertNotRegex(text, r"(?m)^\s+contents: write\s*$")
        self.assertNotRegex(text, r"(?m)^\s+pull-requests: write\s*$")
        self.assertNotIn("secrets.", text)
        self.assertNotIn("GITHUB_TOKEN", text)

    def test_trusted_main_code_only_and_no_persisted_checkout_credentials(self):
        text = self.workflow
        self.assertIn("uses: actions/checkout@v4", text)
        self.assertIn("          ref: main", text)
        self.assertIn("          persist-credentials: false", text)
        self.assertIn(
            "+refs/heads/control/remote-implementation:"
            "refs/remotes/origin/remote-control",
            text,
        )
        self.assertEqual(text.count("git fetch"), 1)
        self.assertNotIn("ref: control/remote-implementation", text)
        self.assertIn("python -B tools/remote_implementation_connector_shadow.py", text)

    def test_event_guard_and_no_write_or_exec_from_control_history(self):
        text = self.workflow
        self.assertIn("github.event.workflow_run.conclusion == 'success'", text)
        self.assertIn(
            "github.event.workflow_run.head_repository.full_name"
            " == github.repository",
            text,
        )
        self.assertNotRegex(
            text,
            r"(?m)^\s*(?:run:|\s+)\s*(?:gh pr create|gh pr merge|"
            r"git push|git commit|gh workflow run|curl -X POST)",
        )
        self.assertNotIn("actions/upload-artifact", text)
        self.assertNotIn("docker/build-push-action", text)
        self.assertNotIn("uses: actions/create-github-app-token", text)

    def test_single_observer_job_short_runtime(self):
        text = self.workflow
        self.assertEqual(len(re.findall(r"(?m)^  observe-shadow:", text)), 1)
        self.assertIn("    timeout-minutes: 5", text)
        self.assertIn("PYTHONDONTWRITEBYTECODE: '1'", text)


if __name__ == "__main__":
    unittest.main()
