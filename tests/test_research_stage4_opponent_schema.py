"""Regression for accepted Stage 2 opponent capsule aliases at Stage 4."""
import csv
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import research_stage4 as mod
from research_stage4_closeout import write_deterministic_zip
from test_research_stage4 import make_descriptive_checkpoint, opponent_bytes, csv_bytes


ALIASES = {
    "canonical_opponent_name": "canonical_opponent_display_name",
    "current_d1": "current_d1_at_research_base",
    "games_with_source_label": "game_count",
    "user_choice": "owner_choice",
    "audit_note": "audit_provenance_note",
}


def legacy_checkpoint(path, *, conflict=False, bad_d1=False, missing_key=False):
    make_descriptive_checkpoint(path, status_value="COMPLETE")
    with zipfile.ZipFile(path) as archive:
        members = {name: archive.read(name) for name in archive.namelist()}
    fields, original = mod._csv_bytes(opponent_bytes())
    renamed_fields = [ALIASES.get(field, field) for field in fields]
    rows = [
        {ALIASES.get(field, field): value for field, value in row.items()}
        for row in original
    ]
    if conflict:
        renamed_fields.append("canonical_opponent_name")
        rows[0]["canonical_opponent_name"] = "Conflicting College"
    if bad_d1:
        rows[0]["current_d1_at_research_base"] = ""
    if missing_key:
        renamed_fields.remove("canonical_opponent_key")
        rows[0].pop("canonical_opponent_key")
    path_in_zip = "stage4-authoring/opponents.csv"
    members[path_in_zip] = csv_bytes(renamed_fields, rows)
    manifest = json.loads(members["manifest.json"])
    manifest["files"][path_in_zip] = {
        "size_bytes": len(members[path_in_zip]),
        "sha256": mod.sha256_bytes(members[path_in_zip]),
    }
    members["manifest.json"] = (json.dumps(manifest, sort_keys=True) + "\n").encode()
    write_deterministic_zip(path, members)


class LegacyOpponentSchemaCompatibility(unittest.TestCase):
    def test_01_all_five_aliases_project_without_mutating_inputs(self):
        fields, old_rows = mod._csv_bytes(opponent_bytes())
        old_fields = [ALIASES.get(field, field) for field in fields]
        old_rows = [
            {ALIASES.get(field, field): value for field, value in row.items()}
            for row in old_rows
        ]
        normalized_fields, normalized, defects, summary = (
            mod._opponent_authoring_schema_compatibility(old_fields, old_rows)
        )
        self.assertEqual(defects, [])
        self.assertEqual(set(summary["projected_canonical_columns"]), set(ALIASES))
        self.assertEqual(summary["source_opponent_rows"], 1)
        self.assertNotIn("canonical_opponent_name", old_rows[0])
        for canonical, alias in ALIASES.items():
            self.assertIn(canonical, normalized_fields)
            self.assertEqual(normalized[0][canonical], old_rows[0][alias])
            self.assertIn(alias, normalized_fields)

    def test_02_current_schema_is_unchanged(self):
        fields, rows = mod._csv_bytes(opponent_bytes())
        mapped_fields, mapped_rows, defects, summary = (
            mod._opponent_authoring_schema_compatibility(fields, rows)
        )
        self.assertEqual((mapped_fields, mapped_rows, defects), (fields, rows, []))
        self.assertFalse(summary["legacy_schema_detected"])

    def test_03_legacy_complete_checkpoint_preflight_and_package_authoring(self):
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp) / "legacy.zip"
            legacy_checkpoint(parent)
            sha = mod.sha256_bytes(parent.read_bytes())
            result = mod.inspect_checkpoint("test", parent)
            self.assertEqual(result["status"], "PASS", result["defects"])
            self.assertEqual(result["projected_source_games"], 1)
            self.assertEqual(result["authoring_opponent_rows"], 1)
            with patch.object(mod, "closeout", return_value={
                "status": "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
            }):
                authored = mod.author("test", parent, "b" * 40, Path(tmp) / "out")
            self.assertEqual(authored["status"], "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY")
            self.assertEqual(mod.sha256_bytes(parent.read_bytes()), sha)
            with (Path(tmp) / "out/package/opponents.csv").open(newline="") as handle:
                package = list(csv.DictReader(handle))
            self.assertEqual(package[0]["canonical_opponent_name"], "Old College")
            self.assertEqual(package[0]["canonical_opponent_display_name"], "Old College")
            self.assertEqual(package[0]["current_d1"], "No")
            self.assertEqual(package[0]["current_d1_at_research_base"], "No")

    def test_04_conflicting_dual_columns_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "conflict.zip"
            legacy_checkpoint(path, conflict=True)
            result = mod.inspect_checkpoint("test", path)
            self.assertEqual(result["status"], "STAGE4_AUTHORING_INPUT_INVALID")
            self.assertIn("LEGACY_OPPONENT_SCHEMA_ALIAS_CONFLICT",
                          [d["reason"] for d in result["defects"]])

    def test_05_blank_legacy_d1_remains_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "blank.zip"
            legacy_checkpoint(path, bad_d1=True)
            result = mod.inspect_checkpoint("test", path)
            self.assertIn("INVALID_CURRENT_D1",
                          [d["reason"] for d in result["defects"]])

    def test_06_missing_opponent_identity_remains_blocking(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "missing.zip"
            legacy_checkpoint(path, missing_key=True)
            result = mod.inspect_checkpoint("test", path)
            self.assertEqual(result["status"], "STAGE4_AUTHORING_INPUT_INVALID")
            self.assertIn("MISSING_COLUMNS",
                          [d["reason"] for d in result["defects"]])


if __name__ == "__main__":
    unittest.main()
