import csv
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import research_stage4 as stage4
import research_stage4_closeout as closeout
from research_stage3a4_accounting import (
    OPPONENT_HOME_RESPONSIBILITY_FILE,
    STAGE3A4_STATUS_FILE,
    reconcile_opponent_home_outside_responsibility,
)


BASIS = (
    "Regular-season OPPONENT_HOME exact-building reconstruction is outside "
    "test source-school Stage 3A responsibility; literal source token remains preserved."
)


def csv_bytes(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def opponent_bytes():
    fields = sorted(stage4.OPPONENT_FIELDS)
    return csv_bytes(
        fields,
        [
            {
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "canonical_opponent_key": "old-college",
                "canonical_opponent_name": "Old College",
                "current_d1": "No",
                "games_with_source_label": "3",
                "first_season": "1974-1975",
                "last_season": "1974-1975",
                "resolution_status": "RESOLVED",
                "resolution_method": "ACCEPTED_STAGE2_DURABLE_IDENTITY",
                "user_choice": "",
                "audit_note": "accepted",
            }
        ],
    )


def venue_bytes():
    return csv_bytes(sorted(stage4.VENUE_FIELDS), [])


def conference_bytes():
    fields = sorted(stage4.CONFERENCE_FIELDS)
    return csv_bytes(
        fields,
        [
            {
                "source_program_key": "test",
                "start_season": "1974-1975",
                "end_season": "",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "True",
                "basis": "accepted",
                "notes": "",
            }
        ],
    )


def ledger_rows():
    rows = []
    for index, game_id in enumerate(("G1", "G2", "G3"), start=1):
        rows.append(
            {
                "research_game_id": game_id,
                "source_program_key": "test",
                "season_label": "1974-75",
                "game_date": f"1975-02-{20 + index:02d}",
                "source_opponent_label": "Old College",
                "opponent_key": "old-college",
                "team_score": "60",
                "opponent_score": "70",
                "played_result": "L",
                "game_type": "REGULAR_SEASON",
                "source_venue_token": "RC" if game_id == "G1" else "",
                "source_entry_literal": (
                    "Feb. 21 Old College RC L 60-70"
                    if game_id == "G1"
                    else f"Feb. {20 + index} Old College L 60-70"
                ),
                "stage3a_final_site_type": "OPPONENT_HOME",
                "stage3a_site_research_status": "",
                "stage3a_site_research_basis": "",
            }
        )
    return rows


def sidecar_rows():
    rows = []
    for row in ledger_rows():
        rows.append(
            {
                "research_game_id": row["research_game_id"],
                "season": row["season_label"],
                "game_date": row["game_date"],
                "opponent_key": row["opponent_key"],
                "source_venue_token": row["source_venue_token"],
                "basis": BASIS,
            }
        )
    return rows


def make_checkpoint(
    path,
    *,
    ledger=None,
    sidecar=None,
    declared_count=3,
    manifest_sidecar=True,
    manifest_status=True,
):
    ledger = [dict(row) for row in (ledger or ledger_rows())]
    sidecar = [dict(row) for row in (sidecar or sidecar_rows())]
    ledger_fields = list(ledger[0])
    ledger_data = csv_bytes(ledger_fields, ledger)
    status = json.dumps(
        {
            "stage": "STAGE_3B",
            "status": "COMPLETE",
            "school_key": "test",
            "research_base_sha": "a" * 40,
            "primary_source_historical_cutoff": "1974-75",
            "required_completed_season_cutoff": "1974-75",
        },
        sort_keys=True,
    ).encode()
    stage3a4_status = json.dumps(
        {
            "stage3a4_complete": True,
            "opponent_home_rows_outside_source_school_building_responsibility": declared_count,
        },
        sort_keys=True,
    ).encode()
    logical = {
        "stage3b-working-ledger.csv": ledger_data,
        "stage3b-status.json": status,
        "stage4-authoring/opponents.csv": opponent_bytes(),
        "stage4-authoring/venues.csv": venue_bytes(),
        "stage4-authoring/conferences.csv": conference_bytes(),
        OPPONENT_HOME_RESPONSIBILITY_FILE: json.dumps(
            sidecar, sort_keys=True
        ).encode(),
        STAGE3A4_STATUS_FILE: stage3a4_status,
    }
    manifested = dict(logical)
    if not manifest_sidecar:
        manifested.pop(OPPONENT_HOME_RESPONSIBILITY_FILE)
    if not manifest_status:
        manifested.pop(STAGE3A4_STATUS_FILE)
    manifest = {
        "research_base_sha": "a" * 40,
        "files": [
            {
                "name": name,
                "bytes": len(data),
                "sha256": stage4.sha256_bytes(data),
            }
            for name, data in sorted(manifested.items())
        ],
    }
    members = dict(logical)
    members["checkpoint-manifest.json"] = (
        json.dumps(manifest, sort_keys=True) + "\n"
    ).encode()
    closeout.write_deterministic_zip(path, members)


class Stage3A4OpponentHomeAccountingReconciliationTests(unittest.TestCase):
    def test_population_reconciles_and_only_material_literal_row_is_accounted(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            checkpoint = root / "parent.zip"
            make_checkpoint(checkpoint)

            preflight = stage4.inspect_checkpoint("test", checkpoint)
            self.assertEqual(preflight["status"], "PASS")
            summary = preflight["stage3a4_opponent_home_responsibility"]
            self.assertEqual(summary["sidecar_rows"], 3)
            self.assertEqual(summary["ledger_regular_season_opponent_home_rows"], 3)
            self.assertEqual(summary["material_literal_source_gap_rows"], 1)
            self.assertTrue(summary["reconciled"])

            fake_closeout = {
                "status": "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
                "checkpoint_sha256": "c" * 64,
            }
            output = root / "out"
            with patch.object(stage4, "closeout", return_value=fake_closeout):
                result = stage4.author(
                    "test",
                    checkpoint,
                    "b" * 40,
                    output,
                )
            self.assertEqual(
                result["status"],
                "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
            )

            with (output / "package" / "source-games.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                games = {
                    row["source_game_id"]: row
                    for row in csv.DictReader(handle)
                }
            self.assertEqual(games["G1"]["source_venue_name"], "RC")
            self.assertEqual(games["G1"]["curated_venue_name"], "")
            self.assertEqual(games["G1"]["city"], "")
            self.assertEqual(games["G1"]["state"], "")
            self.assertEqual(
                games["G1"]["site_research_status"],
                "RESEARCHED_PARTIAL",
            )
            self.assertEqual(games["G1"]["site_research_basis"], BASIS)
            for game_id in ("G2", "G3"):
                self.assertEqual(games[game_id]["source_venue_name"], "")
                self.assertEqual(games[game_id]["site_research_status"], "")
                self.assertEqual(games[game_id]["site_research_basis"], "")

    def test_manifest_presence_is_required(self):
        with tempfile.TemporaryDirectory() as td:
            checkpoint = Path(td) / "parent.zip"
            make_checkpoint(checkpoint, manifest_sidecar=False)
            result = stage4.inspect_checkpoint("test", checkpoint)
            self.assertEqual(result["status"], "STAGE4_AUTHORING_INPUT_INVALID")
            self.assertIn(
                "STAGE3A4_OPPONENT_HOME_SIDECAR_NOT_MANIFESTED",
                {item["reason"] for item in result["defects"]},
            )

    def test_population_and_row_invariants_fail_closed(self):
        cases = {}

        missing = sidecar_rows()[:-1]
        cases["missing"] = (ledger_rows(), missing, 3)

        extra = sidecar_rows() + [
            {
                "research_game_id": "G4",
                "season": "1974-75",
                "game_date": "1975-02-24",
                "opponent_key": "old-college",
                "source_venue_token": "",
                "basis": BASIS,
            }
        ]
        cases["extra"] = (ledger_rows(), extra, 3)

        duplicate = sidecar_rows() + [dict(sidecar_rows()[0])]
        cases["duplicate"] = (ledger_rows(), duplicate, 3)

        classification = ledger_rows()
        classification[0]["stage3a_final_site_type"] = "HOME"
        cases["classification"] = (classification, sidecar_rows(), 3)

        token = sidecar_rows()
        token[0]["source_venue_token"] = "XX"
        cases["token"] = (ledger_rows(), token, 3)

        blank_basis = sidecar_rows()
        blank_basis[0]["basis"] = ""
        cases["blank_basis"] = (ledger_rows(), blank_basis, 3)

        date = sidecar_rows()
        date[0]["game_date"] = "1975-02-28"
        cases["date"] = (ledger_rows(), date, 3)

        season = sidecar_rows()
        season[0]["season"] = "1975-76"
        cases["season"] = (ledger_rows(), season, 3)

        opponent = sidecar_rows()
        opponent[0]["opponent_key"] = "different-college"
        cases["opponent"] = (ledger_rows(), opponent, 3)

        conflict = ledger_rows()
        conflict[0]["stage3a_site_research_status"] = "RESEARCHED_UNRESOLVED"
        conflict[0]["stage3a_site_research_basis"] = "different"
        cases["row_accounting_conflict"] = (conflict, sidecar_rows(), 3)

        cases["declared_count"] = (ledger_rows(), sidecar_rows(), 2)

        for name, (ledger, sidecar, declared) in cases.items():
            with self.subTest(name=name):
                with tempfile.TemporaryDirectory() as td:
                    checkpoint = Path(td) / "parent.zip"
                    make_checkpoint(
                        checkpoint,
                        ledger=ledger,
                        sidecar=sidecar,
                        declared_count=declared,
                    )
                    result = stage4.inspect_checkpoint("test", checkpoint)
                    self.assertEqual(
                        result["status"],
                        "STAGE4_AUTHORING_INPUT_INVALID",
                    )
                    self.assertTrue(result["defects"], result)

    def test_shared_reconciler_reports_exact_population(self):
        with tempfile.TemporaryDirectory() as td:
            checkpoint = Path(td) / "parent.zip"
            make_checkpoint(checkpoint)
            with zipfile.ZipFile(checkpoint) as archive:
                manifest = json.loads(
                    archive.read("checkpoint-manifest.json")
                )
                _, ledger = stage4._csv_bytes(
                    archive.read("stage3b-working-ledger.csv")
                )
                reconciled, defects, summary = (
                    reconcile_opponent_home_outside_responsibility(
                        archive,
                        "",
                        manifest,
                        ledger,
                        normalize_game_type=closeout.normalize_game_type,
                        normalize_site=closeout.normalize_site,
                        project_game_id=closeout.project_game_id,
                    )
                )
            self.assertEqual(defects, [])
            self.assertEqual(set(reconciled), {"G1", "G2", "G3"})
            self.assertEqual(summary["material_literal_source_gap_rows"], 1)


class Stage4CloseoutOpponentHomeAccountingGuardTests(unittest.TestCase):
    def test_closeout_guard_requires_exact_material_accounting(self):
        reconciled = {
            "G1": {"basis": BASIS},
            "G2": {"basis": BASIS},
            "G3": {"basis": BASIS},
        }
        rows = [
            {
                "source_game_id": "G1",
                "curated_game_type": "REGULAR_SEASON",
                "curated_site_type": "OPPONENT_HOME",
                "source_venue_name": "RC",
                "curated_venue_name": "",
                "site_research_status": "RESEARCHED_PARTIAL",
                "site_research_basis": BASIS,
            },
            {
                "source_game_id": "G2",
                "curated_game_type": "REGULAR_SEASON",
                "curated_site_type": "OPPONENT_HOME",
                "source_venue_name": "",
                "curated_venue_name": "",
                "site_research_status": "",
                "site_research_basis": "",
            },
            {
                "source_game_id": "G3",
                "curated_game_type": "REGULAR_SEASON",
                "curated_site_type": "OPPONENT_HOME",
                "source_venue_name": "",
                "curated_venue_name": "",
                "site_research_status": "",
                "site_research_basis": "",
            },
        ]
        self.assertEqual(
            closeout.compare_opponent_home_responsibility_accounting(
                rows,
                reconciled,
            ),
            [],
        )

        missing = [dict(row) for row in rows]
        missing[0]["site_research_status"] = ""
        mismatches = closeout.compare_opponent_home_responsibility_accounting(
            missing,
            reconciled,
        )
        self.assertEqual(
            {item["field"] for item in mismatches},
            {"site_research_status"},
        )

        changed = [dict(row) for row in rows]
        changed[0]["site_research_basis"] = "wrong"
        mismatches = closeout.compare_opponent_home_responsibility_accounting(
            changed,
            reconciled,
        )
        self.assertEqual(
            {item["field"] for item in mismatches},
            {"site_research_basis"},
        )
