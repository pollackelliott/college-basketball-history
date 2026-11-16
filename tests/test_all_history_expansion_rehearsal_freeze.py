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


if __name__ == "__main__":
    unittest.main()
