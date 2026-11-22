"""Regression coverage for pre-Phase0 opponent display reconciliation."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from all_history_expansion_opponent_display_reconciliation import (  # noqa: E402
    KIND,
    OpponentDisplayReconciliationError,
    reconcile_opponent_display,
)
from expansion_implementation_stage1 import render_csv  # noqa: E402


class ExpansionOpponentDisplayReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path(tempfile.mkdtemp(prefix="expansion-display-reconcile-"))
        self.addCleanup(lambda: shutil.rmtree(self.repo, ignore_errors=True))
        subprocess.run(
            ["git", "init"], cwd=self.repo, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test"],
            cwd=self.repo, check=True,
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=self.repo, check=True,
        )
        (self.repo / "data/reference").mkdir(parents=True)
        (self.repo / "data/reference/programs.csv").write_text(
            "program_key,current_d1\nexample,Yes\n",
            encoding="utf-8",
        )
        other = self.repo / "schools/other"
        other.mkdir(parents=True)
        (other / "opponents.csv").write_text(
            "canonical_opponent_key,canonical_opponent_name\n"
            "rio-grande,Rio Grande\n",
            encoding="utf-8",
        )
        self.opponent_fields = [
            "opponent_id", "source_opponent_label",
            "canonical_opponent_name", "canonical_opponent_key", "current_d1",
        ]
        self.opponent_rows = [{
            "opponent_id": "OPP-1",
            "source_opponent_label": "Rio Grande",
            "canonical_opponent_name": "Rio Grande College (Ohio)",
            "canonical_opponent_key": "rio-grande",
            "current_d1": "No",
        }]
        self.source_fields = [
            "source_game_id", "normalized_opponent_name",
            "normalized_opponent_key", "source_opponent_label", "raw_text",
        ]
        self.source_rows = [{
            "source_game_id": "SRC-1",
            "normalized_opponent_name": "Rio Grande College (Ohio)",
            "normalized_opponent_key": "rio-grande",
            "source_opponent_label": "Rio Grande",
            "raw_text": "12/19 Rio Grande L 88-98",
        }]
        self.main = "1" * 40
        self.freeze = "2" * 64

    def spec(self):
        return {
            "schema_version": 1,
            "kind": KIND,
            "school_key": "example",
            "protected_main_sha": self.main,
            "research_freeze_sha256": self.freeze,
            "opponent_changes": [{
                "source_opponent_label": "Rio Grande",
                "canonical_opponent_key": "rio-grande",
                "from_name": "Rio Grande College (Ohio)",
                "to_name": "Rio Grande",
            }],
            "source_game_changes": [{
                "source_game_id": "SRC-1",
                "normalized_opponent_key": "rio-grande",
                "from_name": "Rio Grande College (Ohio)",
                "to_name": "Rio Grande",
            }],
        }

    def reconcile(self, spec=None):
        spec_bytes = (
            json.dumps(spec or self.spec(), indent=2, sort_keys=True) + "\n"
        ).encode()
        return reconcile_opponent_display(
            repo=self.repo,
            school_key="example",
            protected_main_sha=self.main,
            research_freeze_sha256=self.freeze,
            opponents_bytes=render_csv(self.opponent_fields, self.opponent_rows),
            source_games_bytes=render_csv(self.source_fields, self.source_rows),
            spec_bytes=spec_bytes,
        )

    def test_exact_representation_only_projection_passes(self):
        result = self.reconcile()
        self.assertNotIn(
            b"Rio Grande College (Ohio)", result["opponents_bytes"]
        )
        self.assertIn(
            b"12/19 Rio Grande L 88-98", result["source_games_bytes"]
        )
        proof = result["metadata"]["field_level_proof"]
        self.assertEqual(proof["opponent_changed_keys"], ["rio-grande"])
        self.assertEqual(proof["source_game_changed_ids"], ["SRC-1"])
        self.assertEqual(proof["opponent_key_changes"], 0)
        self.assertEqual(proof["literal_evidence_changes"], 0)
        self.assertEqual(proof["source_game_non_name_field_changes"], 0)
        self.assertEqual(proof["opponent_current_d1_changed_key_count"], 0)

    def test_stale_before_value_is_rejected(self):
        spec = self.spec()
        spec["opponent_changes"][0]["from_name"] = "Stale Name"
        with self.assertRaisesRegex(
            OpponentDisplayReconciliationError,
            "OPPONENT_POPULATION_MISMATCH",
        ):
            self.reconcile(spec)

    def test_unexpected_source_population_is_rejected(self):
        spec = self.spec()
        spec["source_game_changes"] = []
        with self.assertRaisesRegex(
            OpponentDisplayReconciliationError,
            "SOURCE_POPULATION_MISMATCH",
        ):
            self.reconcile(spec)

    def test_ambiguous_project_authority_fails_closed(self):
        other = self.repo / "schools/other-two"
        other.mkdir(parents=True)
        (other / "opponents.csv").write_text(
            "canonical_opponent_key,canonical_opponent_name\n"
            "rio-grande,Completely Different Institution\n",
            encoding="utf-8",
        )
        with self.assertRaisesRegex(
            OpponentDisplayReconciliationError,
            "AUTHORITY_AMBIGUOUS:rio-grande",
        ):
            self.reconcile()


if __name__ == "__main__":
    unittest.main()
