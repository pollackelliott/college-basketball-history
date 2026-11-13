import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

WORKFLOWS = (
    ROOT / ".github/workflows/opponent-identity-tooling-validation.yml",
    ROOT / ".github/workflows/opponent-identity-transaction-validation.yml",
)


class FrozenReleasePrRevalidationWorkflowTests(unittest.TestCase):
    def test_required_workflows_support_reopen_live_main_revalidation(self):
        for path in WORKFLOWS:
            source = path.read_text(encoding="utf-8")
            with self.subTest(workflow=path.name):
                self.assertIn(
                    "types: [opened, synchronize, reopened]",
                    source,
                )
                self.assertIn(
                    'ref: ${{ github.event.pull_request.head.sha }}',
                    source,
                )
                self.assertIn(
                    'git fetch --no-tags origin "+refs/heads/main:refs/remotes/origin/main"',
                    source,
                )
                self.assertIn(
                    'git merge --no-ff --no-edit "$EXPECTED_HEAD_SHA"',
                    source,
                )
                self.assertIn(
                    'test "$(git rev-parse HEAD^1)" = "$live_main"',
                    source,
                )
                self.assertIn(
                    'test "$(git rev-parse HEAD^2)" = "$EXPECTED_HEAD_SHA"',
                    source,
                )
                self.assertIn("git ls-remote origin refs/heads/main", source)
                self.assertIn("LIVE_MAIN_STABILITY=PASS", source)
                self.assertNotIn(
                    'refs/pull/${{ github.event.pull_request.number }}/merge',
                    source,
                )
                self.assertNotIn(
                    'EXPECTED_BASE_SHA: ${{ github.event.pull_request.base.sha }}',
                    source,
                )
                self.assertNotIn("assigned", source)


if __name__ == "__main__":
    unittest.main()
