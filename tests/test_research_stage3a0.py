import csv
import io
import json
import subprocess
import sys
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).parents[1] / "tools" / "research_stage3a0.py"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def csv_text(rows):
    stream = io.StringIO()
    writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()


def run_path(tmp_path, input_path, extra_args=None):
    out = tmp_path / "out"
    args = [
        sys.executable,
        str(SCRIPT),
        "creighton",
        str(input_path),
        "--output-dir",
        str(out),
        "--main-sha",
        "PINNED",
    ]
    if extra_args:
        args.extend(extra_args)
    process = subprocess.run(args, text=True, capture_output=True, cwd=tmp_path)
    status = json.loads((out / "stage3a0-status.json").read_text())
    return process, status, out


def run_rows(tmp_path, ledger_rows, extra_args=None):
    ledger = tmp_path / "ledger.csv"
    write_csv(ledger, ledger_rows)
    return run_path(tmp_path, ledger, extra_args=extra_args)


def base_rows():
    return [
        {
            "research_game_id": "C-1",
            "season_label": "2024-2025",
            "game_date": "2024-11-01",
            "opponent_key": "duke",
            "site_type": "HOME",
            "game_type": "REGULAR_SEASON",
        },
        {
            "research_game_id": "C-2",
            "season_label": "1990-1991",
            "game_date": "1991-03-15",
            "opponent_key": "unc",
            "site_type": "NEUTRAL",
            "game_type": "NCAA",
        },
        {
            "research_game_id": "C-3",
            "season_label": "1995-1996",
            "game_date": "1995-12-01",
            "opponent_key": "wake-forest",
            "site_type": "NEUTRAL",
            "game_type": "REGULAR_SEASON",
        },
    ]


def creighton_legacy_stage1_rows():
    return [
        {
            "research_game_id": "CREI-S1-00001",
            "season": "1911-1912",
            "game_date": "1912-01-10",
            "source_opponent_field": "Omaha YMCA",
            "source_event_code": "",
            "source_site_token": "@",
            "source_opponent_label": "Omaha YMCA",
            "on_court_result": "W",
            "creighton_score": "35",
            "opponent_score": "20",
            "overtime_periods": "0",
            "conference_marker": "",
            "game_type": "REGULAR_SEASON",
            "event_or_tournament": "",
            "source_kind": "MEDIA_GUIDE",
            "source_locator": "guide",
            "source_raw_text": "Omaha YMCA",
            "source_pdf_page": "1",
            "source_column": "1",
        },
        {
            "research_game_id": "CREI-S1-00002",
            "season": "1911-1912",
            "game_date": "1912-02-10",
            "source_opponent_field": "Drake",
            "source_event_code": "N",
            "source_site_token": "N",
            "source_opponent_label": "Drake",
            "on_court_result": "L",
            "creighton_score": "18",
            "opponent_score": "22",
            "overtime_periods": "0",
            "conference_marker": "",
            "game_type": "REGULAR_SEASON",
            "event_or_tournament": "",
            "source_kind": "MEDIA_GUIDE",
            "source_locator": "guide",
            "source_raw_text": "Drake",
            "source_pdf_page": "1",
            "source_column": "1",
        },
        {
            "research_game_id": "CREI-S1-00003",
            "season": "1911-1912",
            "game_date": "1912-03-01",
            "source_opponent_field": "Nebraska",
            "source_event_code": "",
            "source_site_token": "",
            "source_opponent_label": "Nebraska",
            "on_court_result": "L",
            "creighton_score": "20",
            "opponent_score": "24",
            "overtime_periods": "0",
            "conference_marker": "",
            "game_type": "NCAA",
            "event_or_tournament": "",
            "source_kind": "MEDIA_GUIDE",
            "source_locator": "guide",
            "source_raw_text": "Nebraska",
            "source_pdf_page": "1",
            "source_column": "1",
        },
    ]


def creighton_opponent_census():
    return [
        {
            "source_opponent_label": "Omaha YMCA",
            "game_count": "1",
            "first_season": "1911-1912",
            "last_season": "1911-1912",
            "classification": "NON_D1",
            "proposed_program_key": "omaha-ymca",
            "current_d1": "No",
            "status": "RESOLVED",
            "basis": "accepted",
        },
        {
            "source_opponent_label": "Drake",
            "game_count": "1",
            "first_season": "1911-1912",
            "last_season": "1911-1912",
            "classification": "CURRENT_D1",
            "proposed_program_key": "drake",
            "current_d1": "Yes",
            "status": "RESOLVED",
            "basis": "accepted",
        },
        {
            "source_opponent_label": "Nebraska",
            "game_count": "1",
            "first_season": "1911-1912",
            "last_season": "1911-1912",
            "classification": "CURRENT_D1",
            "proposed_program_key": "nebraska",
            "current_d1": "Yes",
            "status": "RESOLVED",
            "basis": "accepted",
        },
    ]


def test_complete_checkpoint_only_partition_without_repository(tmp_path):
    process, status, out = run_rows(tmp_path, base_rows())
    assert process.returncode == 0
    assert status["status"] == "COMPLETE"
    assert status["protected_main_sha"] == "PINNED"
    assert status["entry_mode"] == "ledger_csv"
    assert status["repository_state_required"] is False
    assert status["project_evidence_reuse"]["performed_in_stage3a0"] is False
    assert status["partition"] == {
        "postseason": 1,
        "regular_season": 2,
        "unclassified": 0,
    }
    assert status["regular_season_site_census"] == {
        "HOME": 1,
        "OPPONENT_HOME": 0,
        "NEUTRAL": 1,
        "UNKNOWN": 0,
    }
    assert len(json.loads((out / "stage3a2-home-queue.json").read_text())) == 1
    assert len(json.loads((out / "stage3b-postseason-handoff.json").read_text())) == 1
    assert len(
        json.loads((out / "stage3a3-historical-neutral-queue.json").read_text())
    ) == 1
    assert not (out / "target-canonical-matches.json").exists()
    assert not (tmp_path / "data").exists()


def test_missing_standardized_site_defaults_to_unknown_without_parsing_raw_token(tmp_path):
    process, status, out = run_rows(
        tmp_path,
        [
            {
                "research_game_id": "C-U",
                "season_label": "2024-2025",
                "game_date": "2024-11-01",
                "opponent_key": "duke",
                "source_site_token": "@",
                "game_type": "REGULAR_SEASON",
            }
        ],
    )
    assert process.returncode == 0
    assert status["site_type_defaulted_to_unknown_count"] == 1
    assert status["regular_season_site_census"]["UNKNOWN"] == 1
    queue = json.loads((out / "stage3a1-unknown-han-queue.json").read_text())
    assert queue[0]["site_type"] == "UNKNOWN"
    assert queue[0]["source_site_token"] == "@"


def test_explicit_source_defined_site_type_survives_with_raw_token(tmp_path):
    process, status, out = run_rows(
        tmp_path,
        [
            {
                "research_game_id": "C-SOURCE-HAN",
                "season_label": "2024-2025",
                "game_date": "2024-11-01",
                "opponent_key": "duke",
                "source_site_token": "@",
                "site_type": "OPPONENT_HOME",
                "game_type": "REGULAR_SEASON",
            }
        ],
    )
    assert process.returncode == 0
    assert status["site_type_defaulted_to_unknown_count"] == 0
    assert status["regular_season_site_census"]["OPPONENT_HOME"] == 1
    with (out / "stage3a0-input-ledger.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        row = next(csv.DictReader(handle))
    assert row["site_type"] == "OPPONENT_HOME"
    assert row["source_site_token"] == "@"


def test_stage2_checkpoint_zip_is_direct_entrypoint(tmp_path):
    checkpoint = tmp_path / "stage2-complete.zip"
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr("nested/structured-stage2-ledger.csv", csv_text(base_rows()))
        archive.writestr("manifest.json", "{}")
    process, status, out = run_path(tmp_path, checkpoint)
    assert process.returncode == 0
    assert status["status"] == "COMPLETE"
    assert status["entry_mode"] == "checkpoint_zip"
    assert status["input_checkpoint_member"] == "nested/structured-stage2-ledger.csv"
    assert (out / "stage3a0-input-ledger.csv").exists()


def test_stage2_checkpoint_carries_stage4_authoring_capsule(tmp_path):
    checkpoint = tmp_path / "stage2-complete.zip"
    opponent_bytes = b"source_program_key,source_opponent_label\ncreighton,Drake\n"
    venue_bytes = b"source_program_key,venue_key\ncreighton,test-gym\n"
    conference_bytes = (
        b"source_program_key,start_season\ncreighton,1911-1912\n"
    )
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr(
            "nested/structured-stage2-ledger.csv",
            csv_text(base_rows()),
        )
        archive.writestr(
            "nested/stage4-authoring/opponents.csv",
            opponent_bytes,
        )
        archive.writestr(
            "nested/stage4-authoring/venues.csv",
            venue_bytes,
        )
        archive.writestr(
            "nested/stage4-authoring/conferences.csv",
            conference_bytes,
        )

    process, status, out = run_path(tmp_path, checkpoint)
    assert process.returncode == 0
    assert status["status"] == "COMPLETE"
    assert set(status["stage4_authoring_carried"]) == {
        "opponents.csv",
        "venues.csv",
        "conferences.csv",
    }
    assert (
        out / "stage4-authoring" / "opponents.csv"
    ).read_bytes() == opponent_bytes
    assert (
        out / "stage4-authoring" / "venues.csv"
    ).read_bytes() == venue_bytes
    assert (
        out / "stage4-authoring" / "conferences.csv"
    ).read_bytes() == conference_bytes

    manifest = json.loads((out / "manifest.json").read_text())
    assert "stage4_authoring_opponents" in manifest
    assert "stage4_authoring_venues" in manifest
    assert "stage4_authoring_conferences" in manifest


def test_creighton_shaped_legacy_checkpoint_materializes_complete_stage2_ledger(tmp_path):
    checkpoint = tmp_path / "creighton-stage2-complete-checkpoint.zip"
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr(
            "creighton_stage1_working_ledger.csv",
            csv_text(creighton_legacy_stage1_rows()),
        )
        archive.writestr(
            "creighton_stage2_opponent_census.csv",
            csv_text(creighton_opponent_census()),
        )
        archive.writestr(
            "creighton_stage2_current_d1_aliases.csv",
            csv_text(creighton_opponent_census()[:1]),
        )
        archive.writestr(
            "checkpoint.json",
            json.dumps(
                {
                    "stage": "STAGE_2",
                    "status": "COMPLETE",
                    "complete": True,
                }
            ),
        )

    process, status, out = run_path(tmp_path, checkpoint)
    assert process.returncode == 0
    assert status["status"] == "COMPLETE"
    assert status["entry_mode"] == "legacy_stage2_materialized"
    assert (
        status["legacy_game_ledger_member"]
        == "creighton_stage1_working_ledger.csv"
    )
    assert (
        status["legacy_opponent_mapping_member"]
        == "creighton_stage2_opponent_census.csv"
    )
    assert status["legacy_opponent_labels_required"] == 3
    assert status["legacy_opponent_mapping_coverage"] == "COMPLETE"
    assert status["site_type_defaulted_to_unknown_count"] == 3
    assert status["partition"] == {
        "postseason": 1,
        "regular_season": 2,
        "unclassified": 0,
    }
    assert status["regular_season_site_census"] == {
        "HOME": 0,
        "OPPONENT_HOME": 0,
        "NEUTRAL": 0,
        "UNKNOWN": 2,
    }

    with (out / "stage3a0-input-ledger.csv").open(
        newline="", encoding="utf-8"
    ) as handle:
        materialized = list(csv.DictReader(handle))
    assert [row["opponent_key"] for row in materialized] == [
        "omaha-ymca",
        "drake",
        "nebraska",
    ]
    assert [row["site_type"] for row in materialized] == [
        "UNKNOWN",
        "UNKNOWN",
        "UNKNOWN",
    ]
    assert [row["source_site_token"] for row in materialized] == ["@", "N", ""]


def test_legacy_checkpoint_requires_complete_label_mapping(tmp_path):
    checkpoint = tmp_path / "legacy-incomplete.zip"
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr(
            "creighton_stage1_working_ledger.csv",
            csv_text(creighton_legacy_stage1_rows()),
        )
        archive.writestr(
            "creighton_stage2_opponent_census.csv",
            csv_text(creighton_opponent_census()[:2]),
        )

    process, status, out = run_path(tmp_path, checkpoint)
    assert process.returncode == 2
    assert status["status"] == "STAGE_3A0_ENTRY_NOT_READY"
    assert status["entry_error"].startswith(
        "NO_COMPLETE_LEGACY_STAGE2_OPPONENT_MAPPING"
    )
    assert not (out / "stage3a0-summary.json").exists()


def test_legacy_checkpoint_rejects_incorrect_mapping_game_counts(tmp_path):
    checkpoint = tmp_path / "legacy-bad-count.zip"
    census = [dict(row) for row in creighton_opponent_census()]
    census[0]["game_count"] = "2"
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr(
            "school_stage1_working_ledger.csv",
            csv_text(creighton_legacy_stage1_rows()),
        )
        archive.writestr(
            "school_stage2_opponent_census.csv",
            csv_text(census),
        )

    process, status, _ = run_path(tmp_path, checkpoint)
    assert process.returncode == 2
    assert status["entry_error"].startswith(
        "NO_COMPLETE_LEGACY_STAGE2_OPPONENT_MAPPING"
    )


def test_equivalent_complete_mapping_candidates_are_deterministic(tmp_path):
    checkpoint = tmp_path / "legacy-equivalent.zip"
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr(
            "school_stage1_working_ledger.csv",
            csv_text(creighton_legacy_stage1_rows()),
        )
        archive.writestr(
            "school_stage2_opponent_census.csv",
            csv_text(creighton_opponent_census()),
        )
        duplicate = [
            {
                "source_opponent_label": row["source_opponent_label"],
                "canonical_opponent_key": row["proposed_program_key"],
            }
            for row in creighton_opponent_census()
        ]
        archive.writestr(
            "school_stage2_opponent_reconciliation.csv",
            csv_text(duplicate),
        )

    process, status, _ = run_path(tmp_path, checkpoint)
    assert process.returncode == 0
    assert status["legacy_opponent_mapping_coverage"] == "COMPLETE"


def test_conflicting_best_complete_mappings_fail_closed(tmp_path):
    checkpoint = tmp_path / "legacy-conflict.zip"
    census = creighton_opponent_census()
    conflicting = [dict(row) for row in census]
    conflicting[1]["proposed_program_key"] = "not-drake"
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr(
            "school_stage1_working_ledger.csv",
            csv_text(creighton_legacy_stage1_rows()),
        )
        archive.writestr("a_stage2_opponent_census.csv", csv_text(census))
        archive.writestr("b_stage2_opponent_census.csv", csv_text(conflicting))

    process, status, _ = run_path(tmp_path, checkpoint)
    assert process.returncode == 2
    assert status["entry_error"].startswith(
        "AMBIGUOUS_COMPLETE_LEGACY_STAGE2_OPPONENT_MAPPING"
    )


def test_checkpoint_zip_without_game_ledger_still_fails_entry(tmp_path):
    checkpoint = tmp_path / "bad.zip"
    with zipfile.ZipFile(checkpoint, "w") as archive:
        archive.writestr("counts.csv", "season,count\n2024-2025,1\n")
        archive.writestr(
            "stage2-opponent-census.csv",
            csv_text(creighton_opponent_census()),
        )
    process, status, out = run_path(tmp_path, checkpoint)
    assert process.returncode == 2
    assert status["status"] == "STAGE_3A0_ENTRY_NOT_READY"
    assert status["entry_error"] == "NO_STAGE2_LEDGER_FOUND"
    assert not (out / "stage3a0-summary.json").exists()


def test_missing_game_type_fails_readiness_before_partition(tmp_path):
    process, status, out = run_rows(
        tmp_path,
        [
            {
                "research_game_id": "C-1",
                "season_label": "1912-1913",
                "game_date": "1913-01-01",
                "opponent_key": "davidson",
                "site_type": "HOME",
                "game_type": "",
            }
        ],
    )
    assert process.returncode == 2
    assert status["status"] == "STAGE_3A0_INPUT_NOT_READY"
    assert status["readiness"]["blocking_defects"]["missing_game_type"] == ["C-1"]
    assert status["remediation_code"] == "MISSING_GAME_TYPE_ONLY"
    assert not (out / "stage3a0-summary.json").exists()


def test_explicit_unknown_site_is_a_valid_queue_value(tmp_path):
    process, status, out = run_rows(
        tmp_path,
        [
            {
                "research_game_id": "C-U",
                "season_label": "1912-1913",
                "game_date": "1913-01-01",
                "opponent_key": "davidson",
                "site_type": "UNKNOWN",
                "game_type": "REGULAR_SEASON",
            }
        ],
    )
    assert process.returncode == 0
    assert status["regular_season_site_census"]["UNKNOWN"] == 1
    queue = json.loads((out / "stage3a1-unknown-han-queue.json").read_text())
    assert [row["research_game_id"] for row in queue] == ["C-U"]


def test_unrecognized_site_type_is_rejected(tmp_path):
    process, status, _ = run_rows(
        tmp_path,
        [
            {
                "research_game_id": "C-BAD",
                "season_label": "1912-1913",
                "game_date": "1913-01-01",
                "opponent_key": "davidson",
                "site_type": "MYSTERY",
                "game_type": "REGULAR_SEASON",
            }
        ],
    )
    assert process.returncode == 2
    assert status["readiness"]["blocking_defects"]["unrecognized_site_type"] == [
        "C-BAD"
    ]


def test_legacy_migration_rejects_non_game_type_change(tmp_path):
    base = tmp_path / "base.csv"
    fixed = tmp_path / "fixed.csv"
    migration = Path(__file__).parents[1] / "tools" / "research_stage3a0_migrate.py"
    write_csv(
        base,
        [
            {
                "research_game_id": "C-1",
                "game_date": "1982-02-13",
                "opponent_key": "virginia",
                "site_type": "HOME",
                "game_type": "",
            }
        ],
    )
    write_csv(
        fixed,
        [
            {
                "research_game_id": "C-1",
                "game_date": "1982-03-05",
                "opponent_key": "virginia",
                "site_type": "HOME",
                "game_type": "CONFERENCE_TOURNAMENT",
            }
        ],
    )
    process = subprocess.run(
        [sys.executable, str(migration), str(base), str(fixed)],
        text=True,
        capture_output=True,
    )
    assert process.returncode == 2
    assert "non-game-type fields changed" in process.stdout


def test_policy_makes_stage3a0_materialize_legacy_stage2_and_future_stage2_write_through():
    root = Path(__file__).parents[1]

    contract = (root / "docs" / "stage3a0-local-only-contract.md").read_text(
        encoding="utf-8"
    )
    bounded = (root / "docs" / "research-lane-bounded-execution.md").read_text(
        encoding="utf-8"
    )
    portable = (root / "docs" / "research-portable-execution.md").read_text(
        encoding="utf-8"
    )
    agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    self_challenge = (root / "docs" / "research-freeze-self-challenge.md").read_text(
        encoding="utf-8"
    )

    assert "legacy Stage 2" in contract
    assert "complete label-level opponent mapping" in contract
    assert "never infer H/A/N from source_site_token" in contract
    assert "structured-stage2-ledger.csv" in contract
    assert "structured-stage2-ledger.csv" in agents
    assert "site_type=UNKNOWN" in agents
    assert "explicitly documents an H/A/N notation convention" in agents
    assert "raw `source_site_token` alone is never an H/A/N inference rule" in agents
    assert "mechanically normalize the preserved source token" in bounded
    assert "COMPLETE_PRE_FREEZE_SELF_CHALLENGE_PASS" in bounded
    assert "return immediately" in self_challenge
    assert "checkpoint-only" in bounded.lower()
    assert "repository archive is not required for Stage 3A-0" in portable
    assert "fetch the exact `tools/research_stage3a0.py` file" in portable
    assert "Do not use codeload" in contract
