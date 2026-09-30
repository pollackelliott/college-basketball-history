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


def csv_bytes(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def opponent_bytes():
    fields = sorted(mod.OPPONENT_FIELDS)
    return csv_bytes(
        fields,
        [
            {
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "canonical_opponent_key": "old-college",
                "canonical_opponent_name": "Old College",
                "current_d1": "No",
                "games_with_source_label": "1",
                "first_season": "2000-2001",
                "last_season": "2000-2001",
                "resolution_status": "RESOLVED",
                "resolution_method": "ACCEPTED_STAGE2_DURABLE_IDENTITY",
                "user_choice": "",
                "audit_note": "accepted",
            }
        ],
    )


def venue_bytes():
    fields = sorted(mod.VENUE_FIELDS)
    return csv_bytes(
        fields,
        [
            {
                "source_program_key": "test",
                "venue_key": "test-gym",
                "venue_id": "",
                "canonical_name": "Test Gym",
                "aliases": "Old Test Gym",
                "city": "Testville",
                "state": "TS",
                "venue_type": "",
                "known_opened": "",
                "known_closed": "",
                "venue_date_precision": "unknown",
                "games_currently_assigned": "1",
                "first_assigned_game": "2000-12-01",
                "last_assigned_game": "2000-12-01",
                "relationship_type": "GAME_SITE",
                "relationship_start": "",
                "relationship_end": "",
                "relationship_date_precision": "",
                "site_rule": "accepted game-level assignment",
                "source_basis": "accepted Stage 3 research",
                "notes": "",
            }
        ],
    )


def conference_bytes():
    fields = sorted(mod.CONFERENCE_FIELDS)
    return csv_bytes(
        fields,
        [
            {
                "source_program_key": "test",
                "start_season": "2000-2001",
                "end_season": "",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "True",
                "basis": "accepted source chronology",
                "notes": "",
            }
        ],
    )


def current_ledger_bytes():
    fields = [
        "research_game_id",
        "source_program_key",
        "season_label",
        "game_date",
        "source_opponent_label",
        "opponent_key",
        "team_score",
        "opponent_score",
        "played_result",
        "overtime_periods",
        "game_type",
        "raw_text",
        "stage3b_status",
        "stage3a_final_site_type",
        "stage3a_final_physical_venue_name",
        "stage3a_final_venue_city",
        "stage3a_final_venue_state",
    ]
    return csv_bytes(
        fields,
        [
            {
                "research_game_id": "G1",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "game_type": "REGULAR_SEASON",
                "raw_text": "Old College",
                "stage3b_status": "NOT_APPLICABLE_REGULAR_SEASON",
                "stage3a_final_site_type": "HOME",
                "stage3a_final_physical_venue_name": "Test Gym",
                "stage3a_final_venue_city": "Testville",
                "stage3a_final_venue_state": "TS",
            }
        ],
    )


def legacy_ledger_bytes():
    fields = [
        "research_game_id",
        "source_program_key",
        "season_label",
        "game_date",
        "source_opponent_text",
        "opponent_key",
        "team_score",
        "opponent_score",
        "played_result",
        "overtime_periods",
        "game_type",
        "raw_text",
        "stage3a_final_han",
        "stage3a_curated_venue_key",
        "stage3a_curated_venue_name",
        "stage3a_site_city",
        "stage3a_site_state",
        "stage3b_curated_venue_key",
        "stage3b_curated_venue_name",
        "stage3b_site_city",
        "stage3b_site_state",
    ]
    return csv_bytes(
        fields,
        [
            {
                "research_game_id": "G1",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2001-03-15",
                "source_opponent_text": "Old College",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "game_type": "NCAA",
                "raw_text": "Old College NCAA",
                "stage3a_final_han": "NEUTRAL",
                "stage3a_curated_venue_key": "",
                "stage3a_curated_venue_name": "",
                "stage3a_site_city": "",
                "stage3a_site_state": "",
                "stage3b_curated_venue_key": "test-gym",
                "stage3b_curated_venue_name": "Test Gym",
                "stage3b_site_city": "Testville",
                "stage3b_site_state": "TS",
            }
        ],
    )


def make_checkpoint(path, *, legacy=False, include_capsule=True, manifest_capsule=True):
    ledger = legacy_ledger_bytes() if legacy else current_ledger_bytes()
    status = json.dumps(
        {
            "stage": "STAGE_3B",
            "status": "COMPLETE",
            "school_key": "test",
            "research_base_sha": "a" * 40,
        },
        sort_keys=True,
    ).encode()

    capsule = {
        "opponents.csv": opponent_bytes(),
        "venues.csv": venue_bytes(),
        "conferences.csv": conference_bytes(),
    }

    if legacy:
        prefix = "test-stage3b-complete-checkpoint/"
        logical = {
            "stage3b-ledger.csv": ledger,
            "stage3b-status.json": status,
        }
        if include_capsule:
            logical.update(
                {
                    "stage4-authoring/" + name: data
                    for name, data in capsule.items()
                }
            )
        manifested = dict(logical)
        if include_capsule and not manifest_capsule:
            manifested = {
                name: data
                for name, data in logical.items()
                if not name.startswith("stage4-authoring/")
            }
        manifest = {
            "research_base_sha": "a" * 40,
            "files": {
                name: {
                    "bytes": len(data),
                    "sha256": mod.sha256_bytes(data),
                }
                for name, data in sorted(manifested.items())
            },
        }
        members = {prefix + name: data for name, data in logical.items()}
        members[prefix + "manifest.json"] = (
            json.dumps(manifest, sort_keys=True) + "\n"
        ).encode()
    else:
        logical = {
            "stage3b-working-ledger.csv": ledger,
            "stage3b-status.json": status,
        }
        if include_capsule:
            logical.update(
                {
                    "stage4-authoring/" + name: data
                    for name, data in capsule.items()
                }
            )
        manifested = dict(logical)
        if include_capsule and not manifest_capsule:
            manifested = {
                name: data
                for name, data in logical.items()
                if not name.startswith("stage4-authoring/")
            }
        manifest = {
            "research_base_sha": "a" * 40,
            "files": [
                {
                    "name": name,
                    "bytes": len(data),
                    "sha256": mod.sha256_bytes(data),
                }
                for name, data in sorted(manifested.items())
            ],
        }
        members = dict(logical)
        members["checkpoint-manifest.json"] = (
            json.dumps(manifest, sort_keys=True) + "\n"
        ).encode()

    write_deterministic_zip(path, members)


class Stage4AuthoringTests(unittest.TestCase):
    def test_current_checkpoint_preflight_passes(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "current.zip"
            make_checkpoint(checkpoint)
            result = mod.inspect_checkpoint("test", checkpoint)
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["projected_source_games"], 1)
            self.assertEqual(result["opponent_rows"], 1)
            self.assertEqual(result["venue_rows"], 1)
            self.assertEqual(result["conference_rows"], 1)

    def test_missing_authoring_capsule_stops_cleanly(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "current.zip"
            make_checkpoint(checkpoint, include_capsule=False)
            result = mod.inspect_checkpoint("test", checkpoint)
            self.assertEqual(
                result["status"],
                "STAGE4_AUTHORING_INPUT_INCOMPLETE",
            )
            self.assertEqual(
                result["missing_authoring_files"],
                ["opponents.csv", "venues.csv", "conferences.csv"],
            )

    def test_unmanifested_capsule_is_invalid(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "current.zip"
            make_checkpoint(
                checkpoint,
                include_capsule=True,
                manifest_capsule=False,
            )
            result = mod.inspect_checkpoint("test", checkpoint)
            self.assertEqual(
                result["status"],
                "STAGE4_AUTHORING_INPUT_INVALID",
            )
            self.assertEqual(
                {
                    item["name"]
                    for item in result["defects"]
                    if item["reason"] == "AUTHORING_MEMBER_NOT_MANIFESTED"
                },
                {
                    "stage4-authoring/opponents.csv",
                    "stage4-authoring/venues.csv",
                    "stage4-authoring/conferences.csv",
                },
            )

    def test_legacy_columns_author_package_without_reinterpretation(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkpoint = root / "legacy.zip"
            make_checkpoint(checkpoint, legacy=True)
            original_parent = checkpoint.read_bytes()

            fake_closeout = {
                "status": "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
                "checkpoint_sha256": "c" * 64,
            }
            with patch.object(mod, "closeout", return_value=fake_closeout):
                result = mod.author(
                    "test",
                    checkpoint,
                    "b" * 40,
                    root / "out",
                )

            self.assertEqual(
                result["status"],
                "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
            )
            with (root / "out" / "package" / "source-games.csv").open(
                encoding="utf-8",
                newline="",
            ) as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["source_game_id"], "G1")
            self.assertEqual(row["normalized_opponent_key"], "old-college")
            self.assertEqual(row["normalized_opponent_name"], "Old College")
            self.assertEqual(row["curated_site_type"], "NEUTRAL")
            self.assertEqual(row["curated_venue_name"], "Test Gym")
            self.assertEqual(row["city"], "Testville")
            self.assertEqual(row["state"], "TS")
            self.assertEqual(row["curated_game_type"], "NCAA_TOURNAMENT")
            self.assertEqual(checkpoint.read_bytes(), original_parent)
            self.assertTrue((root / "out" / "package" / "notes.md").is_file())
            self.assertTrue(
                (root / "out" / "package" / "source-notes.md").is_file()
            )


if __name__ == "__main__":
    unittest.main()
