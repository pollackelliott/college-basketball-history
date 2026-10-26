import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ImplementationIntakePolicyContractTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_owner_designated_attachment_fallback_is_controlling(self):
        agents = self.read("AGENTS.md")
        bounded = self.read("docs/implementation-lane-bounded-execution.md")
        bootstrap = self.read("docs/implementation-lane-bootstrap-template.md")
        hardening = self.read("docs/onboarding-process-hardening.md")

        self.assertIn("owner-designated-artifact fallback", agents)
        self.assertIn("Owner-designated Research Freeze attachment fallback", bounded)
        self.assertIn("owner-designated final attachment", bootstrap)
        self.assertIn("owner-designated bytes", hardening)

    def test_missing_copied_hash_alone_is_not_recovery_stop(self):
        bounded = self.read("docs/implementation-lane-bounded-execution.md")
        self.assertIn(
            "must not classify that omission alone as `STOP — RECOVERY REQUIRED`",
            bounded,
        )

    def test_scope_conflict_does_not_skip_read_only_stage1_inventory(self):
        bounded = self.read("docs/implementation-lane-bounded-execution.md")
        self.assertIn(
            "does not by itself justify skipping\nor blocking the read-only inventory",
            bounded,
        )


if __name__ == "__main__":
    unittest.main()
