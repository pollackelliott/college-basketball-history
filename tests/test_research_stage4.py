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


def make_checkpoint(
    path,
    *,
    legacy=False,
    include_capsule=True,
    manifest_capsule=True,
    include_coverage=True,
):
    ledger = legacy_ledger_bytes() if legacy else current_ledger_bytes()
    status_payload = {
        "stage": "STAGE_3B",
        "status": "COMPLETE",
        "school_key": "test",
        "research_base_sha": "a" * 40,
    }
    if include_coverage:
        status_payload.update(
            {
                "primary_source_historical_cutoff": "1999-2000",
                "required_completed_season_cutoff": "2000-2001",
            }
        )
    status = json.dumps(status_payload, sort_keys=True).encode()

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


def make_descriptive_checkpoint(
    path,
    *,
    status_value="RESEARCH_SUBSTANTIVELY_COMPLETE_PREFLIGHT_READY",
    duplicate_terminal=False,
    manifest_ledger=True,
    ledger_sha_override="",
):
    ledger_name = "stage3b-postseason-research-complete-ledger.csv"
    status_name = "stage3b-preflight-ready-status.json"
    ledger = current_ledger_bytes()
    status_payload = {
        "stage": "STAGE_3B",
        "status": status_value,
        "school_key": "test",
        "research_base_sha": "a" * 40,
        "primary_source_historical_cutoff": "1999-2000",
        "required_completed_season_cutoff": "2000-2001",
        "durable_stage3b_complete": status_value == "COMPLETE",
        "authoritative_working_ledger": {
            "path": ledger_name,
            "rows": 1,
            "sha256": ledger_sha_override or mod.sha256_bytes(ledger),
        },
    }
    status = json.dumps(status_payload, sort_keys=True).encode()

    logical = {
        ledger_name: ledger,
        status_name: status,
        "stage4-authoring/opponents.csv": opponent_bytes(),
        "stage4-authoring/venues.csv": venue_bytes(),
        "stage4-authoring/conferences.csv": conference_bytes(),
    }
    if duplicate_terminal:
        duplicate = dict(status_payload)
        duplicate["status"] = "COMPLETE"
        logical["stage3b-other-terminal-status.json"] = json.dumps(
            duplicate,
            sort_keys=True,
        ).encode()

    manifested = dict(logical)
    if not manifest_ledger:
        manifested.pop(ledger_name)
    manifest = {
        "checkpoint_status": "STAGE_3B_" + status_value,
        "research_base_sha": "a" * 40,
        "files": {
            name: {
                "size_bytes": len(data),
                "sha256": mod.sha256_bytes(data),
            }
            for name, data in sorted(manifested.items())
        },
    }
    members = dict(logical)
    members["manifest.json"] = (
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


    def test_descriptive_root_preflight_ready_passes_only_for_preflight(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "descriptive.zip"
            make_descriptive_checkpoint(checkpoint)

            ordinary = mod.inspect_checkpoint("test", checkpoint)
            self.assertEqual(
                ordinary["status"],
                "STAGE4_AUTHORING_INPUT_INVALID",
            )
            self.assertIn(
                "STAGE3B_NOT_COMPLETE",
                {item["reason"] for item in ordinary["defects"]},
            )

            preflight = mod.inspect_checkpoint(
                "test",
                checkpoint,
                allow_preflight_ready=True,
            )
            self.assertEqual(preflight["status"], "PASS")
            self.assertEqual(
                preflight["stage3b_parent_topology"],
                "MANIFESTED_DESCRIPTIVE_ROOT",
            )
            self.assertEqual(preflight["projected_source_games"], 1)

    def test_author_accepts_descriptive_complete_parent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkpoint = root / "descriptive-complete.zip"
            make_descriptive_checkpoint(
                checkpoint,
                status_value="COMPLETE",
            )
            fake_closeout = {
                "status": "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
                "checkpoint_sha256": "c" * 64,
            }
            with patch.object(
                mod,
                "closeout",
                return_value=fake_closeout,
            ):
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

    def test_author_rejects_descriptive_preflight_ready_parent(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            checkpoint = root / "descriptive.zip"
            make_descriptive_checkpoint(checkpoint)
            with patch.object(
                mod,
                "closeout",
                side_effect=AssertionError("closeout must not run"),
            ):
                result = mod.author(
                    "test",
                    checkpoint,
                    "b" * 40,
                    root / "out",
                )
            self.assertEqual(
                result["status"],
                "STAGE4_AUTHORING_INPUT_INVALID",
            )
            self.assertIn(
                "STAGE3B_NOT_COMPLETE",
                {item["reason"] for item in result["defects"]},
            )

    def test_descriptive_root_multiple_terminal_statuses_stop(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "ambiguous.zip"
            make_descriptive_checkpoint(
                checkpoint,
                duplicate_terminal=True,
            )
            with self.assertRaisesRegex(
                ValueError,
                "multiple terminal descriptive-root",
            ):
                mod.inspect_checkpoint(
                    "test",
                    checkpoint,
                    allow_preflight_ready=True,
                )

    def test_descriptive_root_unmanifested_ledger_stops(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "unmanifested.zip"
            make_descriptive_checkpoint(
                checkpoint,
                manifest_ledger=False,
            )
            with self.assertRaisesRegex(
                ValueError,
                "ledger is not manifested",
            ):
                mod.inspect_checkpoint(
                    "test",
                    checkpoint,
                    allow_preflight_ready=True,
                )

    def test_descriptive_root_ledger_pointer_hash_mismatch_stops(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "bad-pointer.zip"
            make_descriptive_checkpoint(
                checkpoint,
                ledger_sha_override="0" * 64,
            )
            with self.assertRaisesRegex(
                ValueError,
                "ledger hash mismatch",
            ):
                mod.inspect_checkpoint(
                    "test",
                    checkpoint,
                    allow_preflight_ready=True,
                )

    def test_missing_coverage_declaration_stops_preflight(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "current.zip"
            make_checkpoint(checkpoint, include_coverage=False)
            result = mod.inspect_checkpoint("test", checkpoint)
            self.assertEqual(result["status"], "STAGE4_AUTHORING_INPUT_INVALID")
            self.assertEqual(
                {
                    item["field"]
                    for item in result["defects"]
                    if item["reason"] == "RESEARCH_COVERAGE_DECLARATION_MISSING"
                },
                {
                    "primary_source_historical_cutoff",
                    "required_completed_season_cutoff",
                },
            )

    def test_explicit_coverage_overrides_recover_inflight_checkpoint(self):
        with tempfile.TemporaryDirectory() as temporary:
            checkpoint = Path(temporary) / "current.zip"
            make_checkpoint(checkpoint, include_coverage=False)
            result = mod.inspect_checkpoint(
                "test",
                checkpoint,
                primary_source_historical_cutoff="1999-2000",
                required_completed_season_cutoff="2000-2001",
            )
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(
                result["coverage"]["primary_source_historical_cutoff"],
                "1999-2000",
            )
            self.assertEqual(
                result["coverage"]["required_completed_season_cutoff"],
                "2000-2001",
            )

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
            source_notes = (
                root / "out" / "package" / "source-notes.md"
            ).read_text(encoding="utf-8")
            self.assertIn(
                "- Primary-source historical results cutoff: 1999-2000",
                source_notes,
            )
            self.assertIn(
                "- Required completed-season cutoff: 2000-2001",
                source_notes,
            )
            self.assertIn(
                "media-guide title or filename never establishes the results cutoff",
                source_notes,
            )


    def test_projection_preserves_blank_overtime(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        games, defects = mod._projection(
            [
                {
                    "research_game_id": "BLANK-OT",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "overtime_periods": "",
                }
            ],
            opponents,
            venues,
        )
        self.assertEqual(defects, [])
        self.assertEqual(games[0]["overtime_periods"], "")

    def test_projection_accepts_legacy_venue_location_aliases_and_key(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        ledger = [
            {
                "research_game_id": "FINAL-ALIASES",
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "stage3a_final_venue_name": "Test Gym",
                "stage3a_final_city": "Testville",
                "stage3a_final_state": "TS",
            },
            {
                "research_game_id": "ACCEPTED-ALIASES",
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "accepted_venue_name": "Old Test Gym",
                "accepted_city": "Testville",
                "accepted_state": "TS",
                "accepted_venue_key": "test-gym",
            },
            {
                "research_game_id": "ACCEPTED-KEY",
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "accepted_venue_key": "test-gym",
            },
        ]
        games, defects = mod._projection(ledger, opponents, venues)
        self.assertEqual(defects, [])
        by_id = {row["source_game_id"]: row for row in games}

        final_aliases = by_id["FINAL-ALIASES"]
        self.assertEqual(final_aliases["curated_venue_name"], "Test Gym")
        self.assertEqual(final_aliases["city"], "Testville")
        self.assertEqual(final_aliases["state"], "TS")

        accepted_aliases = by_id["ACCEPTED-ALIASES"]
        self.assertEqual(accepted_aliases["curated_venue_name"], "Old Test Gym")
        self.assertEqual(accepted_aliases["city"], "Testville")
        self.assertEqual(accepted_aliases["state"], "TS")

        accepted_key = by_id["ACCEPTED-KEY"]
        self.assertEqual(accepted_key["curated_venue_name"], "Test Gym")
        self.assertEqual(accepted_key["city"], "Testville")
        self.assertEqual(accepted_key["state"], "TS")

    def test_projection_preserves_legacy_stage3a4_site_fields(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        ledger = [
            {
                "research_game_id": "HOME-DEBT",
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "season_label": "1920-1921",
                "stage3a_final_site_type": "SOURCE_PROGRAM_HOME",
                "venue_city": "Testville",
                "venue_state": "TS",
                "han_research_status": "PREESTABLISHED",
                "han_research_note": "H/A/N already established.",
                "venue_research_status": "RESEARCHED_UNRESOLVED_HOME_VENUE",
                "venue_research_note": (
                    "HOME and locality established; exact building unresolved."
                ),
            },
            {
                "research_game_id": "EXACT-HOME",
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "season_label": "2024-2025",
                "stage3a_final_site_type": "SOURCE_PROGRAM_HOME",
                "venue_key": "test-gym",
                "venue_name": "Test Gym",
                "venue_city": "Testville",
                "venue_state": "TS",
                "han_research_status": "PREESTABLISHED",
                "venue_research_status": "RESOLVED_EXACT_HOME_VENUE",
            },
            {
                "research_game_id": "UNKNOWN-HAN",
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "season_label": "1965-1966",
                "stage3a_final_site_type": "UNKNOWN",
                "han_research_status": "RESEARCHED_UNRESOLVED",
                "han_research_note": (
                    "Accepted institutional evidence remains contradictory."
                ),
                "venue_research_status": "STAGE3A1_RESEARCHED_UNRESOLVED_HAN",
            },
        ]

        games, defects = mod._projection(ledger, opponents, venues)
        self.assertEqual(defects, [])
        by_id = {row["source_game_id"]: row for row in games}

        debt = by_id["HOME-DEBT"]
        self.assertEqual(debt["curated_venue_name"], "")
        self.assertEqual(debt["city"], "Testville")
        self.assertEqual(debt["state"], "TS")
        self.assertEqual(
            debt["site_research_status"],
            "RESEARCHED_UNRESOLVED_HOME_VENUE",
        )
        self.assertEqual(
            debt["site_research_basis"],
            "HOME and locality established; exact building unresolved.",
        )

        exact = by_id["EXACT-HOME"]
        self.assertEqual(exact["curated_venue_name"], "Test Gym")
        self.assertEqual(exact["city"], "Testville")
        self.assertEqual(exact["state"], "TS")
        self.assertEqual(exact["site_research_status"], "")
        self.assertEqual(exact["site_research_basis"], "")

        unknown = by_id["UNKNOWN-HAN"]
        self.assertEqual(unknown["curated_site_type"], "UNKNOWN")
        self.assertEqual(
            unknown["site_research_status"],
            "RESEARCHED_UNRESOLVED",
        )
        self.assertEqual(
            unknown["site_research_basis"],
            "Accepted institutional evidence remains contradictory.",
        )

    def test_projection_carries_postseason_han_research_accounting(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        games, defects = mod._projection(
            [
                {
                    "research_game_id": "HAN-DEBT",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "stage3b_postseason_han_status": "RESEARCHED_UNRESOLVED",
                    "stage3b_postseason_han_basis": (
                        "Accepted postseason H/A/N evidence paths exhausted."
                    ),
                }
            ],
            opponents,
            venues,
        )
        self.assertEqual(defects, [])
        self.assertEqual(
            games[0]["site_research_status"],
            "RESEARCHED_UNRESOLVED",
        )
        self.assertEqual(
            games[0]["site_research_basis"],
            "Accepted postseason H/A/N evidence paths exhausted.",
        )


    def test_projection_prefers_source_game_id_namespace(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        games, defects = mod._projection(
            [
                {
                    "source_game_id": "SRC-1",
                    "research_game_id": "RG-1",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season_label": "2000-01",
                }
            ],
            opponents,
            venues,
        )
        self.assertEqual(defects, [])
        self.assertEqual(games[0]["source_game_id"], "SRC-1")

    def test_projection_preserves_literal_raw_text_and_fallback(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        games, defects = mod._projection(
            [
                {
                    "research_game_id": "RAW-PRIMARY",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season_label": "2000-01",
                    "raw_text": "  literal source text  \t",
                    "source_raw_text": "fallback should not win",
                },
                {
                    "research_game_id": "RAW-FALLBACK",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season_label": "2000-01",
                    "raw_text": "",
                    "source_raw_text": "  fallback source text  ",
                },
            ],
            opponents,
            venues,
        )
        self.assertEqual(defects, [])
        self.assertEqual(
            games[0]["raw_text"],
            "  literal source text  \t",
        )
        self.assertEqual(
            games[1]["raw_text"],
            "  fallback source text  ",
        )

    def test_projection_expands_valid_compact_season_label(self):
        self.assertEqual(
            mod.project_season_label("1999-00"),
            "1999-2000",
        )
        self.assertEqual(
            mod.project_season_label("2000-2001"),
            "2000-2001",
        )

    def test_projection_rejects_malformed_or_inconsistent_season_label(self):
        for value in ("1999-01", "1999-0x", "1999-2002"):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    mod.project_season_label(value)

    def test_projection_normalizes_legacy_administrative_statuses(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        games, defects = mod._projection(
            [
                {
                    "research_game_id": "FORFEIT-LOSS",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season_label": "1986-87",
                    "played_result": "W",
                    "administrative_status": "FORFEIT_LOSS",
                    "administrative_note": "Accepted forfeit loss.",
                    "raw_text": "accepted literal forfeit loss",
                },
                {
                    "research_game_id": "FORFEIT-WIN",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season_label": "1979-80",
                    "played_result": "L",
                    "administrative_status": "FORFEIT_WIN",
                    "administrative_note": "Opponent forfeited after the game.",
                    "raw_text": "accepted literal forfeit win",
                },
                {
                    "research_game_id": "VACATED-WIN",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season_label": "1995-96",
                    "played_result": "W",
                    "administrative_status": "VACATED",
                    "administrative_note": "This game was later vacated.",
                    "raw_text": "accepted literal vacated win",
                },
                {
                    "research_game_id": "VACATED-LOSS",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season_label": "2017-18",
                    "played_result": "L",
                    "administrative_status": "VACATED",
                    "administrative_note": "This game was later vacated.",
                    "raw_text": "accepted literal vacated loss",
                },
            ],
            opponents,
            venues,
        )
        self.assertEqual(defects, [])
        by_id = {row["source_game_id"]: row for row in games}

        for game_id, expected_status, expected_played, literal in (
            (
                "FORFEIT-LOSS",
                "FORFEIT",
                "W",
                "accepted literal forfeit loss",
            ),
            (
                "FORFEIT-WIN",
                "FORFEIT",
                "L",
                "accepted literal forfeit win",
            ),
            (
                "VACATED-WIN",
                "VACATED_GAME",
                "W",
                "accepted literal vacated win",
            ),
            (
                "VACATED-LOSS",
                "VACATED_GAME",
                "L",
                "accepted literal vacated loss",
            ),
        ):
            with self.subTest(game_id=game_id):
                row = by_id[game_id]
                self.assertEqual(row["administrative_status"], expected_status)
                self.assertEqual(row["played_result"], expected_played)
                self.assertEqual(row["raw_text"], literal)
                self.assertIn(
                    f"projected to {expected_status}",
                    row["administrative_note"],
                )
                self.assertIn(
                    f"played_result={expected_played} unchanged",
                    row["administrative_note"],
                )

        self.assertTrue(
            by_id["FORFEIT-WIN"]["administrative_note"].startswith(
                "Opponent forfeited after the game."
            )
        )
        self.assertTrue(
            by_id["VACATED-WIN"]["administrative_note"].startswith(
                "This game was later vacated."
            )
        )
        self.assertIn(
            "administrative_status FORFEIT_WIN projected to FORFEIT",
            by_id["FORFEIT-WIN"]["administrative_note"],
        )
        self.assertIn(
            "administrative_status VACATED projected to VACATED_GAME",
            by_id["VACATED-WIN"]["administrative_note"],
        )

    def test_projection_leaves_current_administrative_vocabulary_unchanged(self):
        for status in ("", "FORFEIT", "VACATED_GAME", "VACATED_WIN"):
            with self.subTest(status=status):
                projected, note = mod.project_administrative_status(
                    {
                        "administrative_status": status,
                        "administrative_note": "accepted current note",
                        "played_result": "W",
                    }
                )
                self.assertEqual(projected, status)
                self.assertEqual(note, "accepted current note")

    def test_projection_does_not_consume_vacated_season_context_sentinel(self):
        status, note = mod.project_administrative_status(
            {
                "administrative_status": "VACATED_SEASON_CONTEXT",
                "administrative_note": "Victories were vacated.",
                "played_result": "W",
            }
        )
        self.assertEqual(status, "VACATED_SEASON_CONTEXT")
        self.assertEqual(note, "Victories were vacated.")


    def test_legacy_on_court_result_provenance_preserves_play(self):
        for status, expected_status in (
            ("FORFEIT_LOSS", "FORFEIT"),
            ("FORFEIT_WIN", "FORFEIT"),
            ("VACATED", "VACATED_GAME"),
        ):
            with self.subTest(status=status):
                row = {
                    "administrative_status": status,
                    "administrative_note": "accepted note",
                    "on_court_result": "L",
                }
                projected, note = mod.project_administrative_status(row)
                self.assertEqual(projected, expected_status)
                self.assertTrue(note.startswith("accepted note"))
                self.assertIn("on-court played_result=L unchanged.", note)
                self.assertNotIn("[blank]", note)

                # Current vocabulary takes precedence if both fields exist.
                row["played_result"] = "W"
                projected, note = mod.project_administrative_status(row)
                self.assertEqual(projected, expected_status)
                self.assertIn("on-court played_result=W unchanged.", note)


    def test_legacy_stage3a_accounting_preserves_exact_accepted_debt(self):
        cases = (
            (
                "UNKNOWN", "REGULAR_SEASON",
                {"season_label": "1947-1948",
                 "stage3a1_status": "RESEARCHED_UNRESOLVED",
                 "stage3a1_evidence_basis": "Official guide ambiguous H/A/N."},
                "RESEARCHED_UNRESOLVED",
            ),
            (
                "NEUTRAL", "REGULAR_SEASON",
                {"season_label": "1950-1951", "city": "New Orleans", "state": "LA",
                 "stage3a3_historical_location_status": "LOCATION_ACCEPTED",
                 "stage3a3_historical_venue_status": "HISTORICAL_VENUE_NOT_REQUIRED",
                 "stage3a3_historical_evidence_basis": "Official event code."},
                "RESEARCHED_PARTIAL",
            ),
            (
                "NEUTRAL", "REGULAR_SEASON",
                {"season_label": "1973-1974", "city": "New Orleans", "state": "LA"},
                "RESEARCHED_PARTIAL",
            ),
            (
                "NEUTRAL", "REGULAR_SEASON",
                {"season_label": "1996-1997", "city": "Bayamon", "state": "PR",
                 "stage3a3_modern_recurring_status":
                     "RESEARCHED_UNRESOLVED_EXACT_VENUE_UNIT2",
                 "stage3a3_modern_recurring_provenance":
                     "Exact-edition official conflicting site reports."},
                "RESEARCHED_UNRESOLVED",
            ),
            (
                "OPPONENT_HOME", "REGULAR_SEASON",
                {"season_label": "1965-1966", "source_venue_name": "(MSG)",
                 "stage3a1_status": "RESOLVED",
                 "stage3a1_evidence_basis": "Official all-time series marks AWAY."},
                "RESEARCHED_PARTIAL",
            ),
        )
        for site, game_type, details, expected in cases:
            with self.subTest(site=site, details=details):
                status, basis = mod._research_accounting({
                    "site_type": site, "game_type": game_type, **details
                })
                self.assertEqual(status, expected)
                self.assertTrue(basis)
        for row in (
            {"site_type": "NEUTRAL", "game_type": "NCAA",
             "season_label": "1950-1951", "city": "New Orleans", "state": "LA"},
            {"site_type": "NEUTRAL", "game_type": "REGULAR_SEASON",
             "season_label": "2017-2018", "city": "Orlando", "state": "FL"},
            {"site_type": "OPPONENT_HOME", "game_type": "REGULAR_SEASON",
             "source_venue_name": "(MSG)", "stage3a1_status": "RESOLVED"},
            {"site_type": "OPPONENT_HOME", "game_type": "REGULAR_SEASON",
             "source_venue_name": "John E. Glaser Arena | Philadelphia, Pa.",
             "stage3a1_evidence_basis": "Official schedule."},
        ):
            with self.subTest(must_fail_closed=row):
                self.assertEqual(mod._research_accounting(row), ("", ""))

    def test_legacy_stage4_projector_maps_ncaa_locality_postseason_and_away_site(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        inputs = (
            {
                "research_game_id": "NCAA-LEGACY",
                "source_program_key": "test",
                "season_label": "1984-1985",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "game_type": "NCAA",
                "site_type": "NEUTRAL",
                "curated_venue_name": "Test Gym",
                "curated_city": "Lexington",
                "curated_state": "KY",
            },
            {
                "research_game_id": "OTHER-LEGACY",
                "source_program_key": "test",
                "season_label": "2024-2025",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "game_type": "OTHER_POSTSEASON",
                "site_type": "NEUTRAL",
            },
            {
                "research_game_id": "AWAY-LEGACY",
                "source_program_key": "test",
                "season_label": "2025-2026",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "site_type": "AWAY",
                "source_venue_name": "Crisler Center | Ann Arbor, Mich.",
            },
        )
        games, defects = mod._projection(list(inputs), opponents, venues)
        self.assertEqual(defects, [])
        by_id = {game["source_game_id"]: game for game in games}
        self.assertEqual(
            (by_id["NCAA-LEGACY"]["city"], by_id["NCAA-LEGACY"]["state"]),
            ("Lexington", "KY"),
        )
        self.assertEqual(
            by_id["NCAA-LEGACY"]["curated_game_type"], "NCAA_TOURNAMENT"
        )
        self.assertEqual(
            by_id["OTHER-LEGACY"]["curated_game_type"], "POSTSEASON"
        )
        self.assertEqual(
            (by_id["AWAY-LEGACY"]["curated_venue_name"],
             by_id["AWAY-LEGACY"]["city"], by_id["AWAY-LEGACY"]["state"]),
            ("Crisler Center", "Ann Arbor", "MI"),
        )
        self.assertEqual(
            by_id["AWAY-LEGACY"]["source_venue_name"],
            "Crisler Center | Ann Arbor, Mich.",
        )
        self.assertEqual(by_id["AWAY-LEGACY"]["site_research_status"], "")

    def test_wagner_legacy_fields_preserve_semantics_and_scope_exceptions(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        base = {
            "source_program_key": "test",
            "source_opponent_label": "Old College",
            "opponent_key": "old-college",
            "season": "1989-90",
            "wagner_points": "73",
            "opponent_points": "69",
            "source_result": "W",
            "source_locator": "Official guide p. 70",
        }
        neutral = {
            **base, "research_game_id": "NEUTRAL", "game_type": "REGULAR_SEASON",
            "site_type": "NEUTRAL", "curated_venue_city": "Springfield",
            "curated_venue_state": "MA",
            "neutral_venue_research_status":
                "HISTORICAL_LOCATION_ACCEPTED_EXACT_BUILDING_ENRICHMENT_UNRESOLVED",
            "neutral_venue_research_basis": "Official host archive checked",
        }
        road = {
            **base, "research_game_id": "ROAD", "game_type": "CONFERENCE_TOURNAMENT",
            "site_type": "OPPONENT_HOME", "postseason_round": "Quarterfinal",
            "postseason_site_research_status":
                "OPPONENT_HOME_VENUE_OUTSIDE_TARGET_RESEARCH_RESPONSIBILITY",
            "postseason_site_research_basis":
                "OWNER_EXPLICIT_NEC_ROAD_SITE_SCOPE_AND_OFFICIAL_CAMPUS_FORMAT",
            "postseason_shared_ref_source_row": "1274",
        }
        ncaa = {
            **base, "research_game_id": "NCAA", "game_type": "NCAA",
            "site_type": "NEUTRAL", "postseason_round": "First Four",
            "source_round": "NCAA First Four",
            "curated_venue_name": "Test Gym",
        }
        nit = {
            **base, "research_game_id": "NIT", "game_type": "NIT",
            "site_type": "OPPONENT_HOME", "postseason_round": "Second Round",
            "source_round": "NIT second-round official source",
        }
        games, defects = mod._projection([neutral, road, ncaa, nit], opponents, venues)
        self.assertEqual(defects, [])
        by_id = {g["source_game_id"]: g for g in games}
        for g in games:
            self.assertEqual(g["season_label"], "1989-1990")
            self.assertEqual(g["team_score"], "73")
            self.assertEqual(g["opponent_score"], "69")
            self.assertEqual(g["played_result"], "W")
            self.assertEqual(g["source_page"], "Official guide p. 70")
        self.assertEqual(by_id["NEUTRAL"]["site_research_status"], "RESEARCHED_PARTIAL")
        self.assertIn("Official host archive", by_id["NEUTRAL"]["site_research_basis"])
        self.assertEqual(by_id["ROAD"]["site_research_status"], "RESEARCHED_PARTIAL")
        self.assertIn("not claimed research-exhausted",
                      by_id["ROAD"]["site_research_basis"])
        self.assertEqual(by_id["ROAD"]["source_round"], "Quarterfinal")
        self.assertEqual(by_id["ROAD"]["curated_postseason_round"], "")
        self.assertEqual(by_id["NCAA"]["curated_postseason_round"], "Play-in")
        self.assertEqual(by_id["NIT"]["curated_postseason_round"], "")
        self.assertIn("Accepted Stage 3B postseason round: Second Round.",
                      by_id["NIT"]["notes"])

    def test_dayton_legacy_fields_project_scores_result_and_overtime(self):
        _, opponents = mod._csv_bytes(opponent_bytes())
        _, venues = mod._csv_bytes(venue_bytes())
        tokens = (("OT", "1"), ("2OT", "2"), ("3OT", "3"), ("5OT", "5"))
        rows = []
        for index, (token, _) in enumerate(tokens, start=1):
            rows.append(
                {
                    "research_game_id": f"DAYTON-LEGACY-{index}",
                    "source_program_key": "test",
                    "source_opponent_label": "Old College",
                    "opponent_key": "old-college",
                    "season": "1989-90",
                    "dayton_score": "73",
                    "opponent_score": "69",
                    "result": "W",
                    "overtime": token,
                    "game_type": "REGULAR_SEASON",
                    "site_type": "UNKNOWN",
                    "source_locator": "Official Dayton ledger",
                }
            )

        games, defects = mod._projection(rows, opponents, venues)
        self.assertEqual(defects, [])
        self.assertEqual(len(games), 4)
        for parent, projected, (_, expected_ot) in zip(rows, games, tokens):
            self.assertEqual(projected["team_score"], "73")
            self.assertEqual(projected["opponent_score"], "69")
            self.assertEqual(projected["played_result"], "W")
            self.assertEqual(projected["overtime_periods"], expected_ot)
            self.assertEqual(
                mod._semantic_projection_defects(parent, projected),
                [],
            )

    def test_scope_exception_fails_closed_without_owner_and_shared_reference(self):
        row = {
            "game_type": "NCAA", "site_type": "NEUTRAL",
            "postseason_site_research_status":
                "OPPONENT_HOME_VENUE_OUTSIDE_TARGET_RESEARCH_RESPONSIBILITY",
            "postseason_site_research_basis":
                "OWNER_EXPLICIT_NEC_ROAD_SITE_SCOPE_AND_OFFICIAL_CAMPUS_FORMAT",
        }
        self.assertEqual(mod._research_accounting(row), ("", ""))
        row.update({"game_type": "CONFERENCE_TOURNAMENT",
                    "site_type": "OPPONENT_HOME"})
        self.assertEqual(mod._research_accounting(row), ("", ""))
        row["postseason_shared_ref_source_row"] = "1274"
        self.assertEqual(mod._research_accounting(row)[0], "RESEARCHED_PARTIAL")

    def test_semantic_parity_detects_silent_field_and_accounting_loss(self):
        parent = {
            "season": "1982-83", "wagner_points": "80",
            "opponent_points": "79", "source_result": "W",
            "postseason_round": "Semifinal",
            "source_locator": "Guide p. 72",
            "neutral_venue_research_status":
                "HISTORICAL_LOCATION_ACCEPTED_EXACT_BUILDING_ENRICHMENT_UNRESOLVED",
        }
        projected = {
            "source_game_id": "G1", "season_label": "", "team_score": "",
            "opponent_score": "", "played_result": "", "source_page": "",
            "source_round": "", "curated_postseason_round": "", "notes": "",
            "site_research_status": "", "site_research_basis": "",
        }
        defects = mod._semantic_projection_defects(parent, projected)
        self.assertEqual(
            {d["reason"] for d in defects},
            {"ACCEPTED_SOURCE_FIELD_LOST", "ACCEPTED_POSTSEASON_ROUND_LOST",
             "ACCEPTED_SITE_RESEARCH_ACCOUNTING_LOST"},
        )


if __name__ == "__main__":
    unittest.main()
