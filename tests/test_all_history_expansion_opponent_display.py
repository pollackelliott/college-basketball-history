from __future__ import annotations

import csv
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from all_history_expansion_opponent_display import (  # noqa: E402
    OpponentDisplayReconciliationError,
    canonical_json_bytes,
    derive_reconciliation,
    validate_reconciliation,
)


def csv_bytes(fields, rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


class ExpansionOpponentDisplayReconciliationTests(unittest.TestCase):
    def git(self, repo: Path, *args: str) -> str:
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if cp.returncode:
            self.fail(cp.stdout)
        return cp.stdout.strip()

    def fixture(self):
        root = Path(tempfile.mkdtemp(prefix="expansion-display-test-"))
        self.addCleanup(lambda: shutil.rmtree(root, ignore_errors=True))
        repo = root / "repo"
        candidate = root / "candidate"
        repo.mkdir()
        candidate.mkdir()

        self.git(repo, "init")
        self.git(repo, "config", "user.name", "Test")
        self.git(repo, "config", "user.email", "test@example.com")

        ref = repo / "data" / "reference"
        ref.mkdir(parents=True)
        (ref / "programs.csv").write_text(
            "program_key,current_d1\nregistered-program,Yes\n",
            encoding="utf-8",
        )

        authority = repo / "schools" / "authority-school"
        authority.mkdir(parents=True)
        (authority / "opponents.csv").write_bytes(
            csv_bytes(
                [
                    "source_opponent_label",
                    "canonical_opponent_key",
                    "canonical_opponent_name",
                    "current_d1",
                ],
                [
                    {
                        "source_opponent_label": "Rio Grande",
                        "canonical_opponent_key": "rio-grande",
                        "canonical_opponent_name": "Rio Grande",
                        "current_d1": "No",
                    }
                ],
            )
        )

        target = repo / "schools" / "miami"
        target.mkdir(parents=True)
        (target / "opponents.csv").write_text(
            "source_opponent_label,canonical_opponent_key,canonical_opponent_name,current_d1\n",
            encoding="utf-8",
        )
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "authority")
        main_sha = self.git(repo, "rev-parse", "HEAD")

        (candidate / "opponents.csv").write_bytes(
            csv_bytes(
                [
                    "source_opponent_label",
                    "canonical_opponent_key",
                    "canonical_opponent_name",
                    "current_d1",
                    "notes",
                ],
                [
                    {
                        "source_opponent_label": "Rio Grande",
                        "canonical_opponent_key": "rio-grande",
                        "canonical_opponent_name": "Rio Grande College (Ohio)",
                        "current_d1": "No",
                        "notes": "Historical institution remains Rio Grande College in Ohio.",
                    }
                ],
            )
        )
        (candidate / "source-games.csv").write_bytes(
            csv_bytes(
                [
                    "source_game_id",
                    "normalized_opponent_key",
                    "normalized_opponent_name",
                    "source_opponent_label",
                    "raw_text",
                ],
                [
                    {
                        "source_game_id": "MIA-EXP-S1-1953-002",
                        "normalized_opponent_key": "rio-grande",
                        "normalized_opponent_name": "Rio Grande College (Ohio)",
                        "source_opponent_label": "Rio Grande",
                        "raw_text": "12/19 Rio Grande L 88-98",
                    }
                ],
            )
        )
        return root, repo, candidate, main_sha

    def test_rio_grande_projection_is_exactly_representation_only(self):
        _, repo, candidate, main_sha = self.fixture()
        result = derive_reconciliation(
            repo,
            "miami",
            candidate,
            protected_main_sha=main_sha,
            research_freeze_sha256="a" * 64,
        )
        self.assertTrue(result["required"])
        doc = result["document"]
        self.assertEqual(doc["changed_keys"], ["rio-grande"])
        self.assertEqual(doc["field_level_proof"]["opponent_key_changes"], 0)
        self.assertEqual(doc["field_level_proof"]["current_d1_changes"], 0)
        self.assertEqual(doc["field_level_proof"]["literal_evidence_changes"], 0)
        self.assertEqual(
            doc["field_level_proof"]["source_game_non_name_field_changes"], 0
        )
        self.assertEqual(len(doc["opponent_changes"]), 1)
        self.assertEqual(
            doc["opponent_changes"][0]["from_name"],
            "Rio Grande College (Ohio)",
        )
        self.assertEqual(doc["opponent_changes"][0]["to_name"], "Rio Grande")
        self.assertEqual(
            doc["source_game_changes"][0]["source_game_id"],
            "MIA-EXP-S1-1953-002",
        )

        projected_opponents = result["projected_bytes"]["opponents.csv"].decode()
        projected_sources = result["projected_bytes"]["source-games.csv"].decode()
        self.assertIn("Rio Grande,No", projected_opponents)
        self.assertIn(
            "rio-grande,Rio Grande,Rio Grande,12/19 Rio Grande L 88-98",
            projected_sources,
        )
        self.assertIn(
            "Historical institution remains Rio Grande College in Ohio.",
            projected_opponents,
        )

    def test_canonical_sidecar_revalidates_exactly(self):
        root, repo, candidate, main_sha = self.fixture()
        derived = derive_reconciliation(
            repo,
            "miami",
            candidate,
            protected_main_sha=main_sha,
            research_freeze_sha256="b" * 64,
        )
        sidecar = root / "sidecar.json"
        sidecar.write_bytes(canonical_json_bytes(derived["document"]))
        verified = validate_reconciliation(
            repo,
            "miami",
            candidate,
            sidecar,
            protected_main_sha=main_sha,
            research_freeze_sha256="b" * 64,
        )
        self.assertEqual(verified["document"], derived["document"])
        self.assertEqual(
            verified["projected_bytes"], derived["projected_bytes"]
        )

    def test_tampered_sidecar_is_rejected(self):
        root, repo, candidate, main_sha = self.fixture()
        derived = derive_reconciliation(
            repo,
            "miami",
            candidate,
            protected_main_sha=main_sha,
            research_freeze_sha256="c" * 64,
        )
        doc = json.loads(canonical_json_bytes(derived["document"]))
        doc["opponent_changes"][0]["to_name"] = "Invented Name"
        sidecar = root / "sidecar.json"
        sidecar.write_bytes(canonical_json_bytes(doc))
        with self.assertRaisesRegex(
            OpponentDisplayReconciliationError,
            "SIDECAR_AUTHORITY_DRIFT",
        ):
            validate_reconciliation(
                repo,
                "miami",
                candidate,
                sidecar,
                protected_main_sha=main_sha,
                research_freeze_sha256="c" * 64,
            )

    def test_ambiguous_project_authority_is_rejected(self):
        _, repo, candidate, main_sha = self.fixture()
        other = repo / "schools" / "second-authority"
        other.mkdir(parents=True)
        (other / "opponents.csv").write_bytes(
            csv_bytes(
                [
                    "source_opponent_label",
                    "canonical_opponent_key",
                    "canonical_opponent_name",
                    "current_d1",
                ],
                [
                    {
                        "source_opponent_label": "Rio Grande",
                        "canonical_opponent_key": "rio-grande",
                        "canonical_opponent_name": "Rio Grande University RedStorm",
                        "current_d1": "No",
                    }
                ],
            )
        )
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "ambiguous authority")
        main_sha = self.git(repo, "rev-parse", "HEAD")
        with self.assertRaisesRegex(
            OpponentDisplayReconciliationError,
            "AUTHORITY_AMBIGUOUS",
        ):
            derive_reconciliation(
                repo,
                "miami",
                candidate,
                protected_main_sha=main_sha,
                research_freeze_sha256="d" * 64,
            )

    def test_registered_program_key_is_not_rewritten(self):
        _, repo, candidate, _ = self.fixture()
        programs = repo / "data" / "reference" / "programs.csv"
        programs.write_text(
            "program_key,current_d1\nrio-grande,Yes\n",
            encoding="utf-8",
        )
        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "registered identity")
        main_sha = self.git(repo, "rev-parse", "HEAD")
        result = derive_reconciliation(
            repo,
            "miami",
            candidate,
            protected_main_sha=main_sha,
            research_freeze_sha256="e" * 64,
        )
        self.assertFalse(result["required"])


if __name__ == "__main__":
    unittest.main()
