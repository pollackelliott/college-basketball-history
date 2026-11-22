import csv
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import build_site_data  # noqa: E402


class PendingOpponentDisplayProjectionTests(unittest.TestCase):
    @staticmethod
    def _write_opponents(
        repo: Path,
        school: str,
        rows: list[tuple[str, str]],
    ) -> None:
        path = repo / "schools" / school / "opponents.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=["canonical_opponent_key", "canonical_opponent_name"],
                lineterminator="\n",
            )
            writer.writeheader()
            for key, name in rows:
                writer.writerow({
                    "canonical_opponent_key": key,
                    "canonical_opponent_name": name,
                })

    def test_normal_publication_mode_still_fails_target_display_conflict(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._write_opponents(repo, "alpha", [("rio-grande", "Rio Grande")])
            self._write_opponents(
                repo,
                "miami",
                [("rio-grande", "Rio Grande College (Ohio)")],
            )
            with self.assertRaisesRegex(
                ValueError,
                "Conflicting historical opponent display names",
            ):
                build_site_data.load_opponent_names(repo, {})

    def test_pending_target_uses_unique_external_project_display(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._write_opponents(repo, "alpha", [("rio-grande", "Rio Grande")])
            self._write_opponents(
                repo,
                "miami",
                [("rio-grande", "Rio Grande College (Ohio)")],
            )
            resolved = build_site_data.load_opponent_names(
                repo,
                {},
                pending_opponent_display_school="miami",
            )
            self.assertEqual(resolved["rio-grande"], "Rio Grande")
            self.assertEqual(
                (repo / "schools/miami/opponents.csv").read_text(encoding="utf-8"),
                "canonical_opponent_key,canonical_opponent_name\n"
                "rio-grande,Rio Grande College (Ohio)\n",
            )

    def test_pending_target_rejects_unrelated_external_conflict(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._write_opponents(repo, "alpha", [("rio-grande", "Rio Grande")])
            self._write_opponents(
                repo,
                "beta",
                [("rio-grande", "Rio Grande College (Ohio)")],
            )
            self._write_opponents(repo, "miami", [("other", "Other")])
            with self.assertRaisesRegex(
                ValueError,
                "Conflicting historical opponent display names",
            ):
                build_site_data.load_opponent_names(
                    repo,
                    {},
                    pending_opponent_display_school="miami",
                )

    def test_pending_target_rejects_ambiguous_external_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._write_opponents(repo, "alpha", [("rio-grande", "Rio Grande")])
            self._write_opponents(
                repo,
                "beta",
                [("rio-grande", "Rio Grande College")],
            )
            self._write_opponents(
                repo,
                "miami",
                [("rio-grande", "Rio Grande College (Ohio)")],
            )
            with self.assertRaisesRegex(
                ValueError,
                "Conflicting historical opponent display names",
            ):
                build_site_data.load_opponent_names(
                    repo,
                    {},
                    pending_opponent_display_school="miami",
                )

    def test_pending_target_rejects_missing_external_authority(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._write_opponents(
                repo,
                "miami",
                [
                    ("rio-grande", "Rio Grande"),
                    ("rio-grande", "Rio Grande College (Ohio)"),
                ],
            )
            with self.assertRaisesRegex(
                ValueError,
                "Conflicting historical opponent display names",
            ):
                build_site_data.load_opponent_names(
                    repo,
                    {},
                    pending_opponent_display_school="miami",
                )

    def test_pending_target_requires_existing_target_package(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self._write_opponents(repo, "alpha", [("rio-grande", "Rio Grande")])
            with self.assertRaisesRegex(
                ValueError,
                "Pending opponent-display school has no opponents.csv",
            ):
                build_site_data.load_opponent_names(
                    repo,
                    {},
                    pending_opponent_display_school="miami",
                )


if __name__ == "__main__":
    unittest.main()
