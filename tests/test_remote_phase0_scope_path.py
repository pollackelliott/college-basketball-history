import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remote_implementation_io import phase0_allowed_paths  # noqa: E402


class RemotePhase0ScopePathTests(unittest.TestCase):
    def test_target_scope_reference_is_allowed_phase0_global_path(self):
        allowed = phase0_allowed_paths("gonzaga")
        self.assertIn("data/reference/program-top-level-scope.csv", allowed)
        self.assertIn("data/reference/programs.csv", allowed)
        self.assertIn("schools/gonzaga/source-games.csv", allowed)


if __name__ == "__main__":
    unittest.main()
