import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/remote-implementation.yml"


class RemoteImplementationWorkflowRuntimeAuthorityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_request_processing_authenticates_and_executes_exact_main_runner(self):
        text = self.workflow
        self.assertIn(
            "protected_main_sha: ${{ steps.detect.outputs.protected_main_sha }}",
            text,
        )
        self.assertIn(
            'print("protected_main_sha="+str(request.get("expected_protected_main_sha","")))',
            text,
        )
        self.assertIn(
            'git fetch --no-tags origin "+refs/heads/main:refs/remotes/origin/main"',
            text,
        )
        self.assertIn(
            'actual_main="$(git rev-parse refs/remotes/origin/main)"',
            text,
        )
        self.assertIn(
            'if [[ "$actual_main" != "$expected_main" ]]; then',
            text,
        )
        self.assertIn(
            "ref: ${{ steps.detect.outputs.protected_main_sha }}\n"
            "          path: runtime",
            text,
        )
        self.assertIn(
            'working-directory: control\n'
            "        env:\n"
            "          GH_TOKEN: ${{ github.token }}\n"
            '        run: python "$GITHUB_WORKSPACE/runtime/tools/remote_implementation_runner.py"',
            text,
        )

    def test_stale_control_runner_and_verifier_copies_are_not_executable_paths(self):
        text = self.workflow
        self.assertNotIn("run: python tools/remote_implementation_runner.py", text)
        self.assertNotIn("run: python tools/remote_implementation_verify.py", text)
        self.assertEqual(
            text.count(
                'run: python "$GITHUB_WORKSPACE/runtime/tools/remote_implementation_runner.py"'
            ),
            1,
        )
        verifier_count = text.count(
            'run: python "$GITHUB_WORKSPACE/runtime/tools/remote_implementation_verify.py"'
        )
        self.assertGreater(verifier_count, 0)
        self.assertEqual(
            text.count(
                "ref: ${{ needs.process-request.outputs.protected_main_sha }}\n"
                "          path: runtime"
            ),
            verifier_count,
        )

    def test_control_checkout_remains_state_authority(self):
        text = self.workflow
        self.assertIn(
            "ref: ${{ github.sha }}\n"
            "          path: control",
            text,
        )
        self.assertIn(
            "ref: control/remote-implementation\n"
            "          path: control",
            text,
        )
        process = text.split(
            "  fresh-owner-gate2-approval-verification:", 1
        )[0]
        self.assertIn("working-directory: control", process)
        self.assertNotIn("working-directory: runtime", process)


if __name__ == "__main__":
    unittest.main()
