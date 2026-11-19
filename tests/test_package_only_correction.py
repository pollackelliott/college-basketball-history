import argparse
import csv
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import onboard_school  # noqa: E402
import onboarding_plan  # noqa: E402
from correction_lifecycle import (  # noqa: E402
    PACKAGE_ONLY_MODE,
    freeze,
)
from implementation_site_gate import (  # noqa: E402
    _correction_source_validation_scope,
)
from integration_freeze_guard import (  # noqa: E402
    SEMANTIC_SOURCE_GAME_FIELDS,
    build_source_game_semantic_snapshot,
    semantic_snapshot_sha256,
)
from onboarding_plan import REQUIRED_PACKAGE_FILES, WorkflowError  # noqa: E402


HISTORY_FIELDS = [
    "source_program_key",
    "start_season",
    "end_season",
    "conference_key",
    "conference_name",
    "membership_type",
    "ongoing",
    "basis",
    "notes",
]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class PackageOnlyCorrectionTests(unittest.TestCase):
    def git(self, root: Path, *args: str) -> str:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode:
            raise AssertionError(result.stdout)
        return result.stdout.strip()

    def source_fields(self) -> list[str]:
        return list(dict.fromkeys(["source_game_id", "source_program_key", *SEMANTIC_SOURCE_GAME_FIELDS]))

    def source_row(self) -> dict[str, str]:
        row = {field: "" for field in self.source_fields()}
        row.update(
            source_game_id="MIA-BASE-1",
            source_program_key="miami",
            season_label="1965-1966",
            game_date="1966-01-01",
            normalized_opponent_key="opponent",
            normalized_opponent_name="Opponent",
            played_result="W",
            team_score="70",
            opponent_score="60",
            curated_site_type="SOURCE_PROGRAM_HOME",
            curated_game_type="REGULAR_SEASON",
            raw_text="Opponent W 70-60",
        )
        return row

    def baseline_conferences(self) -> list[dict[str, str]]:
        return [
            {
                "source_program_key": "miami",
                "start_season": "1948-1949",
                "end_season": "1970-1971",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "False",
                "basis": "published inherited baseline",
                "notes": "legacy continuous Independent chronology",
            }
        ]

    def corrected_conferences(self) -> list[dict[str, str]]:
        return [
            {
                "source_program_key": "miami",
                "start_season": "1948-1949",
                "end_season": "1953-1954",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "False",
                "basis": "accepted Miami Stage 6 authority",
                "notes": "pre-FIC",
            },
            {
                "source_program_key": "miami",
                "start_season": "1954-1955",
                "end_season": "1964-1965",
                "conference_key": "florida-intercollegiate-conference",
                "conference_name": "Florida Intercollegiate Conference",
                "membership_type": "conference",
                "ongoing": "False",
                "basis": "accepted Miami Stage 6 authority",
                "notes": "FIC chronology",
            },
            {
                "source_program_key": "miami",
                "start_season": "1965-1966",
                "end_season": "1970-1971",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "False",
                "basis": "accepted Miami Stage 6 authority",
                "notes": "post-FIC",
            },
        ]

    def make_repo(self, root: Path) -> str:
        self.git(root, "init")
        self.git(root, "config", "user.email", "fixture@example.com")
        self.git(root, "config", "user.name", "Fixture")
        write_csv(
            root / "data/reference/programs.csv",
            ["program_key", "public_page_enabled"],
            [{"program_key": "miami", "public_page_enabled": "Yes"}],
        )
        write_csv(
            root / "data/reference/conferences.csv",
            ["conference_key", "conference_name", "tournament_label", "status", "notes"],
            [
                {
                    "conference_key": "independent",
                    "conference_name": "Independent",
                    "tournament_label": "",
                    "status": "active",
                    "notes": "",
                },
                {
                    "conference_key": "florida-intercollegiate-conference",
                    "conference_name": "Florida Intercollegiate Conference",
                    "tournament_label": "Florida Intercollegiate Conference",
                    "status": "historical",
                    "notes": "",
                },
            ],
        )
        school = root / "schools/miami"
        write_csv(school / "source-games.csv", self.source_fields(), [self.source_row()])
        write_csv(
            school / "opponents.csv",
            ["source_program_key", "source_opponent_label", "canonical_opponent_key"],
            [{"source_program_key": "miami", "source_opponent_label": "Opponent", "canonical_opponent_key": "opponent"}],
        )
        write_csv(
            school / "venues.csv",
            ["source_program_key", "venue_key"],
            [],
        )
        write_csv(school / "conferences.csv", HISTORY_FIELDS, self.baseline_conferences())
        (school / "notes.md").write_text("baseline notes\n", encoding="utf-8")
        (school / "source-notes.md").write_text("baseline source notes\n", encoding="utf-8")
        self.git(root, "add", ".")
        self.git(root, "commit", "-m", "published baseline")
        return self.git(root, "rev-parse", "HEAD")

    def candidate_zip(
        self,
        root: Path,
        *,
        source_change: bool = False,
        opponent_change: bool = False,
    ) -> Path:
        school = root / "schools/miami"
        candidate = root / "candidate"
        candidate.mkdir()
        for name in REQUIRED_PACKAGE_FILES:
            (candidate / name).write_bytes((school / name).read_bytes())
        write_csv(candidate / "conferences.csv", HISTORY_FIELDS, self.corrected_conferences())
        if source_change:
            rows = [self.source_row()]
            rows[0]["game_date"] = "1966-01-02"
            write_csv(candidate / "source-games.csv", self.source_fields(), rows)
        if opponent_change:
            (candidate / "opponents.csv").write_text("unexpected change\n", encoding="utf-8")
        output = root / "candidate.zip"
        with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
            for name in REQUIRED_PACKAGE_FILES:
                archive.write(candidate / name, name)
        return output

    def freeze_args(
        self,
        base: str,
        candidate: Path,
        report: Path,
        *,
        expected: str = "",
        output: Path | None = None,
    ) -> argparse.Namespace:
        return argparse.Namespace(
            school_key="miami",
            candidate_zip=candidate,
            research_base=base,
            scope="package-field-correction",
            research_authority_ref="miami-expansion-stage6-complete-0034",
            research_authority_digest="56bf810b7879ce077e7d77091f876674d28df5ed8df088b5df5d2c1555e11978",
            package_member=["conferences.csv"],
            required_completed_season_cutoff="",
            expected_diff_sha256=expected,
            report_json=report,
            output=output,
        )

    def test_exact_miami_conference_topology_freezes_with_zero_source_ids(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            base = self.make_repo(root)
            candidate = self.candidate_zip(root)
            report = root / "report.json"

            self.assertEqual(freeze(self.freeze_args(base, candidate, report), root), 0)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["correction_mode"], PACKAGE_ONLY_MODE)
            self.assertEqual(payload["correction_package_members"], ["conferences.csv"])
            self.assertEqual(payload["correction_diff"]["source_games"]["changed_source_game_ids"], [])
            self.assertEqual(
                [
                    row["conference_key"]
                    for row in self.corrected_conferences()
                ],
                [
                    "independent",
                    "florida-intercollegiate-conference",
                    "independent",
                ],
            )

            frozen = root / "miami-package-only-correction.zip"
            self.assertEqual(
                freeze(
                    self.freeze_args(
                        base,
                        candidate,
                        report,
                        expected=payload["correction_diff_sha256"],
                        output=frozen,
                    ),
                    root,
                ),
                0,
            )
            with zipfile.ZipFile(frozen) as archive:
                manifest = json.loads(archive.read("correction-freeze.json"))
            self.assertEqual(manifest["correction_mode"], PACKAGE_ONLY_MODE)
            self.assertEqual(manifest["correction_package_members"], ["conferences.csv"])
            self.assertEqual(manifest["correction_source_game_ids"], [])

    def test_package_only_rejects_source_or_undeclared_member_changes(self):
        for mode in ("source", "opponent"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                base = self.make_repo(root)
                candidate = self.candidate_zip(
                    root,
                    source_change=mode == "source",
                    opponent_change=mode == "opponent",
                )
                with self.assertRaises(WorkflowError):
                    freeze(
                        self.freeze_args(base, candidate, root / "report.json"),
                        root,
                    )

    def package_manifest(self, root: Path) -> dict:
        school = root / "schools/miami"
        snapshot = build_source_game_semantic_snapshot(school / "source-games.csv")
        hashes = {
            name: hashlib.sha256((school / name).read_bytes()).hexdigest()
            for name in REQUIRED_PACKAGE_FILES
        }
        return {
            "schema_version": 2,
            "workflow_kind": "POST_PUBLICATION_CORRECTION",
            "status": "INTEGRATION_FROZEN",
            "school_key": "miami",
            "research_base_sha": "a" * 40,
            "correction_mode": PACKAGE_ONLY_MODE,
            "correction_package_members": ["conferences.csv"],
            "correction_source_game_ids": [],
            "correction_diff_sha256": "b" * 64,
            "package_member_sha256": hashes,
            "pre_correction_source_semantic_guard": {
                "schema_version": 1,
                "snapshot_sha256": semantic_snapshot_sha256(snapshot),
                "snapshot": snapshot,
            },
            "source_game_semantic_guard": {
                "schema_version": 1,
                "snapshot_sha256": semantic_snapshot_sha256(snapshot),
                "snapshot": snapshot,
            },
        }

    def test_package_only_freeze_transport_and_zero_source_site_scope(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_repo(root)
            manifest = self.package_manifest(root)
            onboard = root / ".onboarding/miami"
            onboard.mkdir(parents=True)
            freeze_path = onboard / "integration-freeze.json"
            freeze_path.write_text(json.dumps(manifest), encoding="utf-8")

            self.assertIsNotNone(
                onboard_school._validated_correction_freeze_bytes(root, "miami")
            )
            fields = self.source_fields()
            row = self.source_row()
            scoped, info = _correction_source_validation_scope(root, "miami", [row])
            self.assertEqual(scoped, [])
            self.assertEqual(info["mode"], "PACKAGE_ONLY_CORRECTION")
            self.assertEqual(info["scoped_source_games"], 0)

            drifted = dict(row)
            drifted["game_date"] = "1966-01-02"
            scoped, info = _correction_source_validation_scope(
                root, "miami", [drifted]
            )
            self.assertEqual([r["source_game_id"] for r in scoped], ["MIA-BASE-1"])
            self.assertEqual(info["scoped_source_games"], 1)

    def test_stage2_package_only_context_has_zero_decision_universe(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_repo(root)
            school = root / "schools/miami"
            write_csv(
                school / "conferences.csv",
                HISTORY_FIELDS,
                self.corrected_conferences(),
            )
            manifest = self.package_manifest(root)
            onboard = root / ".onboarding/miami"
            onboard.mkdir(parents=True)
            (onboard / "integration-freeze.json").write_text(
                json.dumps(manifest),
                encoding="utf-8",
            )
            with (
                patch.object(
                    onboarding_plan,
                    "validate_package",
                    return_value={"errors": [], "warnings": []},
                ),
                patch.object(
                    onboarding_plan,
                    "input_fingerprint",
                    return_value={"sha256": "c" * 64},
                ),
            ):
                plan = onboarding_plan.build_plan(root, "miami")
            self.assertEqual(plan["decisions"], [])
            self.assertEqual(
                plan["summary"]["correction_transaction_kind"],
                "PACKAGE_ONLY_FIELD_CORRECTION",
            )
            self.assertEqual(
                plan["summary"]["correction_package_members"],
                ["conferences.csv"],
            )
            self.assertEqual(
                plan["summary"]["correction_diff_sha256"],
                "b" * 64,
            )
            self.assertEqual(plan["summary"]["assertions_to_add"], 0)
            self.assertEqual(plan["summary"]["new_canonical_games"], 0)

    def test_package_only_transport_rejects_post_freeze_conference_drift(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self.make_repo(root)
            school = root / "schools/miami"
            write_csv(school / "conferences.csv", HISTORY_FIELDS, self.corrected_conferences())
            manifest = self.package_manifest(root)
            onboard = root / ".onboarding/miami"
            onboard.mkdir(parents=True)
            (onboard / "integration-freeze.json").write_text(
                json.dumps(manifest), encoding="utf-8"
            )
            with (school / "conferences.csv").open("a", encoding="utf-8") as handle:
                handle.write("\n")
            with self.assertRaisesRegex(
                WorkflowError,
                "package-only correction package member changed: conferences.csv",
            ):
                onboard_school._validated_correction_freeze_bytes(root, "miami")


if __name__ == "__main__":
    unittest.main()
