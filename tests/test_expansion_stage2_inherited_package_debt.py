"""Regression: All-History expansion Stage 2 scopes only exact inherited legacy debt."""

import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from onboarding_plan import validate_package  # noqa: E402


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_row(source_game_id="LEGACY-001", venue="Allen Fieldhouse"):
    return {
        "source_game_id": source_game_id,
        "source_program_key": "example-school",
        "season_label": "1966-1967",
        "game_date": "1966-12-10",
        "source_opponent_label": "Kansas State",
        "normalized_opponent_key": "kansas-state",
        "normalized_opponent_name": "Kansas State",
        "team_score": "58",
        "opponent_score": "81",
        "played_result": "L",
        "overtime_periods": "0",
        "curated_site_type": "NEUTRAL",
        "curated_venue_name": venue,
        "city": "Lawrence",
        "state": "KS",
        "curated_game_type": "REGULAR_SEASON",
        "curated_postseason_round": "",
        "raw_text": "D10 at Kansas State L 58-81",
    }


class ExpansionInheritedPackageDebtTests(unittest.TestCase):
    def git(self, root, *args):
        return subprocess.check_output(
            ["git", *args], cwd=root, text=True, stderr=subprocess.PIPE
        ).strip()

    def fixture(self, root):
        self.git(root, "init")
        self.git(root, "config", "user.name", "Test")
        self.git(root, "config", "user.email", "test@example.com")

        school = root / "schools" / "example-school"
        school.mkdir(parents=True)
        legacy = source_row()
        fields = list(legacy)
        write_csv(school / "source-games.csv", fields, [legacy])
        write_csv(
            school / "opponents.csv",
            [
                "source_program_key",
                "source_opponent_name",
                "canonical_opponent_key",
                "canonical_opponent_name",
                "current_d1",
            ],
            [{
                "source_program_key": "example-school",
                "source_opponent_name": "Kansas State",
                "canonical_opponent_key": "kansas-state",
                "canonical_opponent_name": "Kansas State",
                "current_d1": "Yes",
            }],
        )
        write_csv(
            school / "venues.csv",
            ["source_program_key", "venue_key", "canonical_name", "aliases", "city", "state"],
            [],
        )
        write_csv(
            school / "conferences.csv",
            ["source_program_key", "conference_key"],
            [],
        )
        (school / "notes.md").write_text("# Fixture\n", encoding="utf-8")
        (school / "source-notes.md").write_text("# Fixture\n", encoding="utf-8")

        write_csv(
            root / "data" / "reference" / "programs.csv",
            ["program_key", "program_name", "current_d1"],
            [
                {
                    "program_key": "example-school",
                    "program_name": "Example School",
                    "current_d1": "Yes",
                },
                {
                    "program_key": "kansas-state",
                    "program_name": "Kansas State",
                    "current_d1": "Yes",
                },
            ],
        )
        write_csv(
            root / "data" / "reference" / "conferences.csv",
            ["conference_key"],
            [],
        )

        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "published baseline")
        research_base_sha = self.git(root, "rev-parse", "HEAD")
        baseline_source_hash = hashlib.sha256(
            (school / "source-games.csv").read_bytes()
        ).hexdigest()
        return school, fields, legacy, research_base_sha, baseline_source_hash

    def write_manifest(
        self,
        root,
        *,
        research_base_sha,
        baseline_source_hash,
        inherited_count,
        supplemental_count,
    ):
        path = (
            root
            / ".onboarding"
            / "example-school"
            / "integration-freeze.json"
        )
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "kind": "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
                    "status": "INTEGRATION_FROZEN",
                    "school_key": "example-school",
                    "research_base_sha": research_base_sha,
                    "baseline_package_member_sha256": {
                        "source-games.csv": baseline_source_hash,
                    },
                    "source_preservation": {
                        "inherited_count": inherited_count,
                        "supplemental_count": supplemental_count,
                        "combined_count": inherited_count + supplemental_count,
                    },
                }
            ),
            encoding="utf-8",
        )

    def validate(self, root):
        with patch("onboarding_plan.history_scope_errors", return_value=[]):
            return validate_package(root, "example-school")

    def test_unchanged_inherited_missing_venue_is_legacy_warning(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, _, _, base, source_hash = self.fixture(root)
            self.write_manifest(
                root,
                research_base_sha=base,
                baseline_source_hash=source_hash,
                inherited_count=1,
                supplemental_count=0,
            )
            result = self.validate(root)
            self.assertFalse(
                any("curated venue 'Allen Fieldhouse'" in value for value in result["errors"]),
                result,
            )
            self.assertTrue(
                any(
                    "curated venue 'Allen Fieldhouse'" in value
                    and "outside this expansion" in value
                    for value in result["warnings"]
                ),
                result,
            )

    def test_new_supplemental_missing_venue_remains_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            school, fields, legacy, base, source_hash = self.fixture(root)
            supplemental = source_row("EXP-001", "New Missing Arena")
            write_csv(school / "source-games.csv", fields, [legacy, supplemental])
            self.write_manifest(
                root,
                research_base_sha=base,
                baseline_source_hash=source_hash,
                inherited_count=1,
                supplemental_count=1,
            )
            result = self.validate(root)
            self.assertTrue(
                any(
                    "EXP-001: curated venue 'New Missing Arena' absent from venues.csv"
                    in value
                    for value in result["errors"]
                ),
                result,
            )

    def test_changed_inherited_row_remains_blocking(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            school, fields, _, base, source_hash = self.fixture(root)
            changed = source_row("LEGACY-001", "Changed Missing Arena")
            write_csv(school / "source-games.csv", fields, [changed])
            self.write_manifest(
                root,
                research_base_sha=base,
                baseline_source_hash=source_hash,
                inherited_count=1,
                supplemental_count=0,
            )
            result = self.validate(root)
            self.assertTrue(
                any(
                    "LEGACY-001: curated venue 'Changed Missing Arena' absent from venues.csv"
                    in value
                    for value in result["errors"]
                ),
                result,
            )


if __name__ == "__main__":
    unittest.main()
