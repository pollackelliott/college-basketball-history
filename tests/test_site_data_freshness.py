import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from check_site_data_freshness import freshness_report  # noqa: E402


class SiteDataFreshnessTests(unittest.TestCase):
    def test_committed_public_json_matches_deterministic_rebuild(self):
        report = freshness_report(ROOT)
        self.assertEqual(
            report["stale_paths"],
            [],
            "Committed site/data is stale relative to canonical/reference inputs. "
            "Run `python tools/build_site_data.py --apply` and commit every changed "
            "generated JSON file before Preview/release. Stale paths: "
            + ", ".join(report["stale_paths"][:20]),
        )


if __name__ == "__main__":
    unittest.main()
