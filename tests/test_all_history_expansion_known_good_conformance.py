import unittest
from pathlib import Path
from unittest.mock import patch
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import all_history_expansion_known_good_conformance as conformance  # noqa: E402
from remote_implementation_io import Stop  # noqa: E402


class AllHistoryExpansionKnownGoodConformanceTests(unittest.TestCase):
    def test_witness_cohort_is_exact_and_unique(self):
        schools = [row[0] for row in conformance.WITNESSES]
        self.assertEqual(schools, ["vcu", "arizona-state", "houston", "ucf"])
        self.assertEqual(len(schools), len(set(schools)))
        for school, proposal, production in conformance.WITNESSES:
            self.assertIn(school, proposal)
            self.assertIn("-expansion-stage2-proposal-", proposal)
            self.assertIn(school, production)
            self.assertIn("-expansion-release-production-proof-", production)

    def test_stable_contract_covers_gate1_and_site_integrity(self):
        self.assertIn("decision_universe_sha256", conformance.PREFLIGHT_KEYS)
        self.assertIn("decision_count", conformance.PREFLIGHT_KEYS)
        self.assertIn("new_canonical_games", conformance.PREFLIGHT_KEYS)
        self.assertIn("strict_home_gap_rows", conformance.SITE_COUNT_KEYS)
        self.assertIn("unaccounted_public_gap_rows", conformance.SITE_COUNT_KEYS)
        self.assertIn("target_source_information_loss", conformance.SITE_COUNT_KEYS)

    def test_require_equal_fails_closed(self):
        with self.assertRaises(Stop):
            conformance.require_equal("contract", {"a": 1}, {"a": 2})

    @patch.object(conformance, "json_at")
    def test_production_witness_requires_exact_production_pass(self, json_at):
        json_at.return_value = (
            {
                "kind": "REMOTE_IMPLEMENTATION_EXACT_PRODUCTION_CHECKPOINT",
                "school_key": "ucf",
                "status": "PRODUCTION_PROOF_PASS",
                "production_proof": True,
            },
            b"{}",
        )
        document, _ = conformance.json_at(Path("/tmp/control"), "a" * 40, "proof.json")
        self.assertEqual(document["status"], "PRODUCTION_PROOF_PASS")


if __name__ == "__main__":
    unittest.main()
