import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools/conference_tournament_reference.py"
spec = importlib.util.spec_from_file_location("conference_tournament_reference", MODULE_PATH)
ctr = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(ctr)


class ConferenceTournamentReferenceTests(unittest.TestCase):
    def test_snapshot_contract(self):
        self.assertEqual(ctr.check_snapshot(), 0)

    def test_acc_reference_is_complete_for_virginia_era(self):
        rows = ctr.load_snapshot()
        acc = [row for row in rows if row["conference_key"] == "acc"]
        self.assertTrue(acc)
        years = {int(row["tournament_year"]) for row in acc}
        self.assertEqual(min(years), 1954)
        self.assertGreaterEqual(max(years), 2026)
        self.assertTrue(all(row["reference_status"] == "COMPLETE" for row in acc))


if __name__ == "__main__":
    unittest.main()
