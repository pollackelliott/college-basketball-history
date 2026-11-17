"""Fail-closed All-History expansion Freeze transport into nested rehearsals.

These synthetic cases exercise the same copy_repository boundary used by
onboarding_hardening.rehearse_review. No school or shared data are changed.
"""
from __future__ import annotations

import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import onboard_school
from integration_freeze_guard import (
    build_source_game_semantic_snapshot, semantic_snapshot_sha256,
)
from onboarding_plan import WorkflowError

PACKAGE_NAMES = (
    "conferences.csv", "notes.md", "opponents.csv",
    "source-games.csv", "source-notes.md", "venues.csv",
)


def fingerprint(manifest: dict) -> str:
    canonical = dict(manifest, manifest_self_fingerprint_sha256="")
    raw = (json.dumps(canonical, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")) + "\n").encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def fixture(root: Path) -> Path:
    school = root / "schools" / "example"
    school.mkdir(parents=True)
    for name in PACKAGE_NAMES:
        (school / name).write_text(
            ("source_game_id,season_label,source_program_key\n"
             "E-1,1968-1969,example\n")
            if name == "source-games.csv" else "fixture\n",
            encoding="utf-8",
        )
    hashes = {name: onboard_school.file_sha(school / name)
              for name in PACKAGE_NAMES}
    snapshot = build_source_game_semantic_snapshot(school / "source-games.csv")
    manifest = {
        "schema_version": 1,
        "kind": "ALL_HISTORY_EXPANSION_INTEGRATION_FREEZE",
        "status": "INTEGRATION_FROZEN",
        "school_key": "example",
        "tracked_mutation": "NONE",
        "release_authority": False,
        "research_base_sha": "a" * 40,
        "protected_main_sha": "b" * 40,
        "integration_base_sha": "b" * 40,
        "candidate_member_sha256": hashes,
        "package_member_sha256": hashes,
        "source_game_semantic_guard": {
            "snapshot": snapshot,
            "snapshot_sha256": semantic_snapshot_sha256(snapshot),
        },
        "venue_reconciliation": None,
        "venue_reconciliation_sha256": "",
        "manifest_self_fingerprint_sha256": "",
    }
    manifest["manifest_self_fingerprint_sha256"] = fingerprint(manifest)
    authority = root / ".onboarding" / "example" / "integration-freeze.json"
    authority.parent.mkdir(parents=True)
    authority.write_text(json.dumps(manifest, sort_keys=True) + "\n",
                         encoding="utf-8")
    (authority.parent / "untrusted.json").write_text("untrusted\n",
                                                    encoding="utf-8")
    return authority


class ExpansionNestedRehearsalFreezeTests(unittest.TestCase):
    def test_valid_expansion_freeze_survives_copy_without_ignored_neighbors(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src, dst = root / "source", root / "rehearsal"
            authority = fixture(src)
            self.assertIsNone(
                onboard_school.frozen_venue_split_freeze_bytes(src, "example")
            )
            onboard_school.copy_repository(src, dst, school_key="example")
            transferred = dst / ".onboarding" / "example" / "integration-freeze.json"
            self.assertEqual(transferred.read_bytes(), authority.read_bytes())
            self.assertIsNotNone(
                onboard_school._all_history_expansion_integration_freeze(
                    dst, "example"
                )
            )
            self.assertFalse(
                (dst / ".onboarding" / "example" / "untrusted.json").exists()
            )

    def test_absent_manifest_grants_no_expansion_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src, dst = root / "source", root / "rehearsal"
            authority = fixture(src)
            authority.unlink()
            onboard_school.copy_repository(src, dst, school_key="example")
            self.assertFalse((dst / ".onboarding").exists())
            self.assertIsNone(
                onboard_school._all_history_expansion_integration_freeze(
                    dst, "example"
                )
            )

    def test_malformed_or_unbound_expansion_freezes_fail_before_copy(self):
        for variant in (
            "invalid_json", "wrong_school", "status", "fingerprint",
            "package_hash", "package_bytes", "source_snapshot",
            "semantic_sha", "release_authority", "venue_hash",
        ):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                src, dst = root / "source", root / "rehearsal"
                path = fixture(src)
                manifest = json.loads(path.read_text(encoding="utf-8"))
                if variant == "invalid_json":
                    path.write_text("{invalid", encoding="utf-8")
                elif variant == "package_bytes":
                    (src / "schools/example/venues.csv").write_text(
                        "tampered\n", encoding="utf-8"
                    )
                else:
                    if variant == "wrong_school":
                        manifest["school_key"] = "other"
                    elif variant == "status":
                        manifest["status"] = "NOT_FROZEN"
                    elif variant == "fingerprint":
                        manifest["manifest_self_fingerprint_sha256"] = "0" * 64
                    elif variant == "package_hash":
                        manifest["candidate_member_sha256"]["venues.csv"] = "0" * 64
                        manifest["package_member_sha256"]["venues.csv"] = "0" * 64
                    elif variant == "source_snapshot":
                        manifest["source_game_semantic_guard"]["snapshot"]["rows"][
                            "E-1"
                        ]["season_label"] = "1967-1968"
                        manifest["source_game_semantic_guard"][
                            "snapshot_sha256"
                        ] = semantic_snapshot_sha256(
                            manifest["source_game_semantic_guard"]["snapshot"]
                        )
                    elif variant == "semantic_sha":
                        manifest["source_game_semantic_guard"]["snapshot_sha256"] = "0" * 64
                    elif variant == "release_authority":
                        manifest["release_authority"] = True
                    elif variant == "venue_hash":
                        manifest["venue_reconciliation_sha256"] = "0" * 64
                    if variant != "fingerprint":
                        manifest["manifest_self_fingerprint_sha256"] = fingerprint(manifest)
                    path.write_text(json.dumps(manifest) + "\n", encoding="utf-8")
                with self.assertRaises(WorkflowError):
                    onboard_school.copy_repository(src, dst, school_key="example")
                self.assertFalse(dst.exists())

    def test_wrong_kind_does_not_create_expansion_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            src, dst = root / "source", root / "rehearsal"
            path = fixture(src)
            manifest = json.loads(path.read_text(encoding="utf-8"))
            manifest["kind"] = "UNTRUSTED"
            manifest["manifest_self_fingerprint_sha256"] = fingerprint(manifest)
            path.write_text(json.dumps(manifest), encoding="utf-8")
            onboard_school.copy_repository(src, dst, school_key="example")
            self.assertFalse((dst / ".onboarding").exists())



class AuthenticatedDisplaySuccessorFreezeTests(unittest.TestCase):
    """Regression for the exact UCF Phase0 -> refresh -> normalization -> rehearsal defect."""

    @staticmethod
    def git(root: Path, *args: str) -> str:
        import subprocess
        proc = subprocess.run(
            ["git", "-C", str(root), *args], text=True,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        if proc.returncode:
            raise AssertionError(f"git {args!r}: {proc.stdout}")
        return proc.stdout.strip()

    def make_git_fixture(self, src: Path) -> None:
        authority = fixture(src)
        school = src / "schools/example"
        (school / "opponents.csv").write_text(
            "source_program_key,source_opponent_label,canonical_opponent_key,canonical_opponent_name\n"
            "example,Historic Label,other-college,Old College\n",
            encoding="utf-8",
        )
        (school / "source-games.csv").write_text(
            "source_game_id,source_program_key,season_label,source_opponent_label,"
            "normalized_opponent_key,normalized_opponent_name,raw_text\n"
            "E-1,example,1968-1969,Historic Label,other-college,Old College,"
            "Original institutional evidence\n",
            encoding="utf-8",
        )
        other = src / "schools/published-example"
        other.mkdir(parents=True)
        (other / "opponents.csv").write_text(
            "source_program_key,source_opponent_label,canonical_opponent_key,canonical_opponent_name\n"
            "published-example,Published Label,other-college,Preferred College\n",
            encoding="utf-8",
        )
        programs = src / "data/reference/programs.csv"
        programs.parent.mkdir(parents=True)
        programs.write_text(
            "program_key\nexample\npublished-example\n", encoding="utf-8",
        )
        manifest = json.loads(authority.read_text(encoding="utf-8"))
        hashes = {name: onboard_school.file_sha(school / name)
                  for name in PACKAGE_NAMES}
        snapshot = build_source_game_semantic_snapshot(school / "source-games.csv")
        manifest["candidate_member_sha256"] = hashes
        manifest["package_member_sha256"] = hashes
        manifest["source_game_semantic_guard"] = {
            "snapshot": snapshot,
            "snapshot_sha256": semantic_snapshot_sha256(snapshot),
        }
        manifest["manifest_self_fingerprint_sha256"] = fingerprint(manifest)
        authority.write_text(json.dumps(manifest, sort_keys=True) + "\n",
                             encoding="utf-8")
        self.git(src, "init", "-b", "main")
        self.git(src, "config", "user.name", "Synthetic Guard Test")
        self.git(src, "config", "user.email", "test@example.invalid")
        self.git(src, "add", "schools", "data")
        self.git(src, "commit", "-m", "Accepted immutable Phase 0 predecessor")

    def commit_display(self, src: Path, *, variant: str = "valid") -> None:
        school = src / "schools/example"
        opp = school / "opponents.csv"
        games = school / "source-games.csv"
        opp.write_text(
            opp.read_text(encoding="utf-8").replace(
                "Old College", "Invented College" if variant == "invented" else
                "Preferred College"
            ), encoding="utf-8",
        )
        games.write_text(
            games.read_text(encoding="utf-8")
            .replace("Old College", "Preferred College")
            .replace("Original institutional evidence",
                     "Changed institutional evidence"
                     if variant == "raw_tamper" else
                     "Original institutional evidence"),
            encoding="utf-8",
        )
        if variant == "extra_tracked_path":
            (src / "data/reference/programs.csv").write_text(
                "program_key\nexample\npublished-example\nspoofed\n",
                encoding="utf-8",
            )
        self.git(src, "add", "schools/example/opponents.csv",
                 "schools/example/source-games.csv")
        if variant == "extra_tracked_path":
            self.git(src, "add", "data/reference/programs.csv")
        self.git(
            src, "commit", "-m",
            "Normalize example historical opponent display representation",
        )

    def test_authorized_committed_display_only_successor_survives_rehearsal(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / "source", Path(temp) / "copy"
            self.make_git_fixture(src)
            self.commit_display(src)
            onboard_school.copy_repository(src, dst, school_key="example")
            self.assertEqual(
                (dst / ".onboarding/example/integration-freeze.json").read_bytes(),
                (src / ".onboarding/example/integration-freeze.json").read_bytes(),
            )
            self.assertIn(
                "Preferred College",
                (dst / "schools/example/opponents.csv").read_text(),
            )

    def test_unapproved_or_non_display_successors_fail_closed(self):
        for variant in ("invented", "raw_tamper", "extra_tracked_path"):
            with self.subTest(variant=variant), tempfile.TemporaryDirectory() as temp:
                src, dst = Path(temp) / "source", Path(temp) / "copy"
                self.make_git_fixture(src)
                self.commit_display(src, variant=variant)
                with self.assertRaisesRegex(
                    WorkflowError, "Integration Freeze package mismatch"
                ):
                    onboard_school.copy_repository(src, dst, school_key="example")
                self.assertFalse(dst.exists())

    def test_uncommitted_display_edit_does_not_claim_successor_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / "source", Path(temp) / "copy"
            self.make_git_fixture(src)
            p = src / "schools/example/opponents.csv"
            p.write_text(p.read_text().replace("Old College", "Preferred College"))
            with self.assertRaises(WorkflowError):
                onboard_school.copy_repository(src, dst, school_key="example")
            self.assertFalse(dst.exists())

    def test_disjoint_main_merge_after_normalization_preserves_authority(self):
        with tempfile.TemporaryDirectory() as temp:
            src, dst = Path(temp) / "source", Path(temp) / "copy"
            self.make_git_fixture(src)
            baseline = self.git(src, "rev-parse", "HEAD")
            self.commit_display(src)
            self.git(src, "branch", "normalized", "HEAD")
            self.git(src, "checkout", "-b", "main-update", baseline)
            doc = src / "README.md"
            doc.write_text("Unrelated generic tooling change\n", encoding="utf-8")
            self.git(src, "add", "README.md")
            self.git(src, "commit", "-m", "Intervening main-only docs")
            self.git(src, "checkout", "normalized")
            self.git(src, "merge", "--no-ff", "main-update", "-m",
                     "Merge unrelated current main after normalization")
            onboard_school.copy_repository(src, dst, school_key="example")
            self.assertTrue(
                (dst / ".onboarding/example/integration-freeze.json").is_file()
            )


if __name__ == "__main__":
    unittest.main()
