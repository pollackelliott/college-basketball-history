import csv
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import research_stage4_closeout as mod


def write_csv(path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fields,
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def package_rows(ids=("G1",)):
    games = []
    for i, game_id in enumerate(ids, start=1):
        games.append(
            {
                "source_game_id": game_id,
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": f"2000-12-{i:02d}",
                "source_opponent_label": (
                    "Old College"
                    if i == 1
                    else "Old College Alias"
                ),
                "normalized_opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "administrative_status": "",
                "administrative_note": "",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "Test Gym",
                "city": "Testville",
                "state": "TS",
                "curated_game_type": "REGULAR_SEASON",
                "curated_postseason_round": "",
                "raw_text": f"raw {game_id}",
                "site_research_status": "",
                "site_research_basis": "",
            }
        )
    return games


def make_package(root: Path, ids=("G1",)):
    root.mkdir(parents=True, exist_ok=True)
    games = package_rows(ids)
    write_csv(
        root / "source-games.csv",
        list(games[0]),
        games,
    )
    write_csv(
        root / "opponents.csv",
        [
            "source_program_key",
            "source_opponent_label",
            "canonical_opponent_key",
            "canonical_opponent_name",
            "current_d1",
            "games_with_source_label",
            "first_season",
            "last_season",
            "resolution_status",
            "resolution_method",
            "user_choice",
            "audit_note",
        ],
        [
            {
                "source_program_key": "test",
                "source_opponent_label": "Old College",
                "canonical_opponent_key": "old-college",
                "canonical_opponent_name": "Old College",
                "current_d1": "No",
                "games_with_source_label": str(len(ids)),
                "first_season": "2000-2001",
                "last_season": "2000-2001",
                "resolution_status": "RESOLVED",
                "resolution_method": "test",
                "user_choice": "",
                "audit_note": "",
            }
        ],
    )
    write_csv(
        root / "venues.csv",
        [
            "source_program_key",
            "venue_key",
            "venue_id",
            "canonical_name",
            "aliases",
            "city",
            "state",
        ],
        [
            {
                "source_program_key": "test",
                "venue_key": "test-gym",
                "venue_id": "",
                "canonical_name": "Test Gym",
                "aliases": "",
                "city": "Testville",
                "state": "TS",
            }
        ],
    )
    write_csv(
        root / "conferences.csv",
        [
            "source_program_key",
            "start_season",
            "end_season",
            "conference_key",
            "conference_name",
            "membership_type",
            "ongoing",
            "basis",
            "notes",
        ],
        [
            {
                "source_program_key": "test",
                "start_season": "2000-2001",
                "end_season": "",
                "conference_key": "independent",
                "conference_name": "Independent",
                "membership_type": "independent",
                "ongoing": "True",
                "basis": "test",
                "notes": "",
            }
        ],
    )
    (root / "notes.md").write_text(
        "# notes\n",
        encoding="utf-8",
    )
    (root / "source-notes.md").write_text(
        "# sources\n",
        encoding="utf-8",
    )


def make_parent(path: Path, ids=("G1",)):
    fields = [
        "research_game_id",
        "source_program_key",
        "season_label",
        "game_date",
        "opponent_program_key",
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
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer,
        fieldnames=fields,
        lineterminator="\n",
    )
    writer.writeheader()
    for i, game_id in enumerate(ids, start=1):
        writer.writerow(
            {
                "research_game_id": game_id,
                "source_program_key": "test",
                "season_label": "2000-01",
                "game_date": f"2000-12-{i:02d}",
                "opponent_program_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "game_type": "REGULAR_SEASON",
                "raw_text": f"raw {game_id}",
                "stage3b_status": (
                    "NOT_APPLICABLE_REGULAR_SEASON"
                ),
                "stage3a_final_site_type": "HOME",
                "stage3a_final_physical_venue_name": (
                    "Test Gym"
                ),
                "stage3a_final_venue_city": "Testville",
                "stage3a_final_venue_state": "TS",
            }
        )

    ledger = buffer.getvalue().encode()
    status = json.dumps(
        {
            "status": "COMPLETE",
            "school_key": "test",
            "research_base_sha": "a" * 40,
        },
        sort_keys=True,
    ).encode()
    members = {
        "stage3b-working-ledger.csv": ledger,
        "stage3b-status.json": status,
    }
    manifest = {
        "files": [
            {
                "name": name,
                "bytes": len(data),
                "sha256": mod.sha256_bytes(data),
            }
            for name, data in sorted(members.items())
        ],
        "research_base_sha": "a" * 40,
    }
    members["checkpoint-manifest.json"] = (
        json.dumps(manifest, sort_keys=True) + "\n"
    ).encode()
    mod.write_deterministic_zip(path, members)


def make_legacy_parent(
    path: Path,
    ids=("G1",),
    *,
    prefix="test-stage3b-complete-checkpoint",
):
    current = path.with_name(path.stem + "-current.zip")
    make_parent(current, ids)
    with zipfile.ZipFile(current) as archive:
        ledger = archive.read("stage3b-working-ledger.csv")
        status = archive.read("stage3b-status.json")
    current.unlink()

    logical_members = {
        "stage3b-ledger.csv": ledger,
        "stage3b-status.json": status,
    }
    manifest = {
        "files": {
            name: {
                "bytes": len(data),
                "sha256": mod.sha256_bytes(data),
            }
            for name, data in sorted(logical_members.items())
        },
        "research_base_sha": "a" * 40,
    }
    members = {
        f"{prefix}/{name}": data
        for name, data in logical_members.items()
    }
    members[f"{prefix}/manifest.json"] = (
        json.dumps(manifest, sort_keys=True) + "\n"
    ).encode()
    mod.write_deterministic_zip(path, members)


def fake_report(
    package,
    *,
    school_key,
    expected_sha256="",
):
    with zipfile.ZipFile(package) as archive:
        games = list(
            csv.DictReader(
                io.StringIO(
                    archive.read(
                        "source-games.csv"
                    ).decode()
                )
            )
        )
        opponents = list(
            csv.DictReader(
                io.StringIO(
                    archive.read(
                        "opponents.csv"
                    ).decode()
                )
            )
        )
        venues = list(
            csv.DictReader(
                io.StringIO(
                    archive.read(
                        "venues.csv"
                    ).decode()
                )
            )
        )
        conferences = list(
            csv.DictReader(
                io.StringIO(
                    archive.read(
                        "conferences.csv"
                    ).decode()
                )
            )
        )
    return {
        "status": "PASS",
        "errors": [],
        "warnings": [],
        "counts": {
            "competitive_games": len(games),
            "opponent_rows": len(opponents),
            "venue_rows": len(venues),
            "conference_rows": len(conferences),
            "unresolved_opponents": 0,
            "unknown_exact_dates": 0,
            "unknown_played_scores": 0,
            "ncaa_rows": 0,
            "site_types": {
                "SOURCE_PROGRAM_HOME": len(games)
            },
            "game_types": {
                "REGULAR_SEASON": len(games)
            },
            "site_completeness": {
                "home_publication_blocker_rows": 0,
                "material_gap_rows": 0,
                "researched_gap_rows": 0,
                "unaccounted_gap_rows": 0,
            },
        },
    }


class Stage4CloseoutTests(unittest.TestCase):
    def test_missing_markdown_stops_before_parent_or_qa(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "pkg"
            make_package(package)
            (package / "notes.md").unlink()
            output = root / "out"

            with patch.object(
                mod,
                "research_portfolio_report",
                side_effect=AssertionError(
                    "research-check should not run"
                ),
            ):
                status = mod.closeout(
                    "test",
                    package,
                    root / "missing-parent.zip",
                    "b" * 40,
                    output,
                )

            self.assertEqual(
                status["status"],
                "PACKAGE_AUTHORING_INCOMPLETE",
            )
            self.assertEqual(
                status["missing_required_files"],
                ["notes.md"],
            )

    def test_complete_closeout_is_deterministic_and_groups_non_d1(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "pkg"
            make_package(package, ("G1", "G2"))
            parent = root / "parent.zip"
            make_parent(parent, ("G1", "G2"))

            with patch.object(
                mod,
                "research_portfolio_report",
                side_effect=fake_report,
            ):
                first = mod.closeout(
                    "test",
                    package,
                    parent,
                    "b" * 40,
                    root / "out1",
                )
                second = mod.closeout(
                    "test",
                    package,
                    parent,
                    "b" * 40,
                    root / "out2",
                )

            self.assertEqual(
                first["status"],
                "COMPLETE_OWNER_NON_D1_SANITY_SCAN_READY",
            )
            self.assertEqual(
                first["checkpoint_sha256"],
                second["checkpoint_sha256"],
            )
            self.assertEqual(
                first["six_file_package_sha256"],
                second["six_file_package_sha256"],
            )
            self.assertEqual(
                first[
                    "non_d1_owner_scan_distinct_identities"
                ],
                1,
            )
            self.assertEqual(
                first["non_d1_owner_scan_games"],
                2,
            )

            with (
                root
                / "out1"
                / "non-d1-owner-scan.csv"
            ).open() as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(rows[0]["game_count"], "2")
            self.assertIn(
                "Old College Alias",
                rows[0]["representative_source_labels"],
            )

    def test_legacy_single_directory_parent_is_accepted_unchanged(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "pkg"
            make_package(package, ("G1", "G2"))
            parent = root / "legacy-parent.zip"
            make_legacy_parent(parent, ("G1", "G2"))
            parent_bytes = parent.read_bytes()
            parent_sha = mod.sha256_bytes(parent_bytes)

            with patch.object(
                mod,
                "research_portfolio_report",
                side_effect=fake_report,
            ):
                status = mod.closeout(
                    "test",
                    package,
                    parent,
                    "b" * 40,
                    root / "out",
                )

            self.assertEqual(
                status["source_stage3b_complete_checkpoint_sha256"],
                parent_sha,
            )
            sanity = json.loads(
                (
                    root
                    / "out"
                    / "stage4-parent-sanity-check.json"
                ).read_text()
            )
            self.assertEqual(
                sanity["stage3b_parent_topology"],
                "LEGACY_SINGLE_DIRECTORY",
            )
            self.assertEqual(
                sanity["stage3b_parent_rows"],
                2,
            )
            self.assertTrue(
                sanity["source_game_id_population_exact_match"]
            )
            self.assertEqual(
                sanity[
                    "semantic_comparison_unexpected_mismatches"
                ],
                0,
            )

            checkpoint = (
                root
                / "out"
                / "test-stage4-complete-checkpoint.zip"
            )
            with zipfile.ZipFile(checkpoint) as archive:
                embedded = archive.read(
                    "stage3b-complete-checkpoint.zip"
                )
            self.assertEqual(embedded, parent_bytes)
            self.assertEqual(
                mod.sha256_bytes(embedded),
                parent_sha,
            )

    def test_mixed_current_and_legacy_parent_layout_stops(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "pkg"
            make_package(package)
            parent = root / "mixed-parent.zip"
            make_legacy_parent(parent)

            with zipfile.ZipFile(parent, "a") as archive:
                prefix = "test-stage3b-complete-checkpoint"
                ledger = archive.read(
                    f"{prefix}/stage3b-ledger.csv"
                )
                status = archive.read(
                    f"{prefix}/stage3b-status.json"
                )
                manifest = {
                    "files": [
                        {
                            "name": "stage3b-working-ledger.csv",
                            "bytes": len(ledger),
                            "sha256": mod.sha256_bytes(ledger),
                        },
                        {
                            "name": "stage3b-status.json",
                            "bytes": len(status),
                            "sha256": mod.sha256_bytes(status),
                        },
                    ]
                }
                archive.writestr(
                    "stage3b-working-ledger.csv",
                    ledger,
                )
                archive.writestr(
                    "stage3b-status.json",
                    status,
                )
                archive.writestr(
                    "checkpoint-manifest.json",
                    json.dumps(manifest),
                )

            with patch.object(
                mod,
                "research_portfolio_report",
                side_effect=fake_report,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "ambiguous mixed current/legacy",
                ):
                    mod.closeout(
                        "test",
                        package,
                        parent,
                        "b" * 40,
                        root / "out",
                    )

    def test_corrupt_legacy_parent_manifest_stops(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "pkg"
            make_package(package)
            parent = root / "legacy-parent.zip"
            make_legacy_parent(parent)
            prefix = "test-stage3b-complete-checkpoint"

            with zipfile.ZipFile(parent, "a") as archive:
                manifest = json.loads(
                    archive.read(
                        f"{prefix}/manifest.json"
                    )
                )
                manifest["files"]["stage3b-ledger.csv"][
                    "sha256"
                ] = "0" * 64
                archive.writestr(
                    f"{prefix}/manifest.json",
                    json.dumps(manifest),
                )

            with patch.object(
                mod,
                "research_portfolio_report",
                side_effect=fake_report,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "manifest validation failed",
                ):
                    mod.closeout(
                        "test",
                        package,
                        parent,
                        "b" * 40,
                        root / "out",
                    )

    def test_legacy_stage3_semantic_vocabulary_compares_cleanly(self):
        parent = [
            {
                "research_game_id": "G1",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2001-03-15",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "game_type": "NCAA",
                "raw_text": "raw G1",
                "stage3a_final_han": "NEUTRAL",
                "stage3b_curated_venue_key": "test-gym",
                "stage3b_curated_venue_name": "Test Gym",
                "stage3b_site_city": "Testville",
                "stage3b_site_state": "TS",
            }
        ]
        package = [
            {
                "source_game_id": "G1",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2001-03-15",
                "normalized_opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Test Gym",
                "city": "Testville",
                "state": "TS",
                "curated_game_type": "NCAA_TOURNAMENT",
                "raw_text": "raw G1",
            }
        ]
        venues = [
            {
                "venue_key": "test-gym",
                "canonical_name": "Test Gym",
                "aliases": "",
            }
        ]
        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )

    def test_legacy_stage3a4_venue_fields_match_author_projection(self):
        parent = [
            {
                "research_game_id": "LEGACY-STG3A4",
                "source_program_key": "test",
                "season_label": "2024-2025",
                "game_date": "2025-01-15",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "game_type": "REGULAR_SEASON",
                "raw_text": "raw LEGACY-STG3A4",
                "stage3a_final_site_type": "SOURCE_PROGRAM_HOME",
                "venue_name": "Test Gym",
                "venue_city": "Testville",
                "venue_state": "TS",
            }
        ]
        package = [
            {
                "source_game_id": "LEGACY-STG3A4",
                "source_program_key": "test",
                "season_label": "2024-2025",
                "game_date": "2025-01-15",
                "normalized_opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "Test Gym",
                "city": "Testville",
                "state": "TS",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "raw LEGACY-STG3A4",
            }
        ]
        venues = [
            {
                "venue_key": "test-gym",
                "canonical_name": "Test Gym",
                "aliases": "",
                "city": "Testville",
                "state": "TS",
            }
        ]

        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )

        changed = [dict(package[0])]
        changed[0]["city"] = "Elsewhere"
        mismatches = mod.compare_parent_semantics(parent, changed, venues)
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["field"], "city")

    def test_base_venue_locality_fields_match_author_projection(self):
        parent = [
            {
                "research_game_id": "BASE-FIELDS",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "game_type": "REGULAR_SEASON",
                "raw_text": "raw BASE-FIELDS",
                "stage3b_status": "COMPLETE",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "Test Gym",
                "city": "Testville",
                "state": "TS",
            }
        ]
        package = [
            {
                "source_game_id": "BASE-FIELDS",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "normalized_opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "0",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "Test Gym",
                "city": "Testville",
                "state": "TS",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "raw BASE-FIELDS",
            }
        ]
        venues = [
            {
                "venue_key": "test-gym",
                "canonical_name": "Test Gym",
                "aliases": "",
                "city": "Testville",
                "state": "TS",
            }
        ]

        for stage3b_status in (
            "COMPLETE",
            "NOT_APPLICABLE_REGULAR_SEASON",
        ):
            with self.subTest(stage3b_status=stage3b_status):
                parent[0]["stage3b_status"] = stage3b_status
                self.assertEqual(
                    mod.compare_parent_semantics(parent, package, venues),
                    [],
                )

        parent[0]["stage3b_status"] = "COMPLETE"
        for field, value, expected_field in (
            ("city", "Elsewhere", "city"),
            ("state", "ZZ", "state"),
            ("curated_venue_name", "", "venue_present"),
        ):
            with self.subTest(field=field):
                changed = [dict(package[0])]
                changed[0][field] = value
                mismatches = mod.compare_parent_semantics(
                    parent,
                    changed,
                    venues,
                )
                self.assertEqual(len(mismatches), 1)
                self.assertEqual(
                    mismatches[0]["field"],
                    expected_field,
                )

    def test_semantic_drift_stops(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "pkg"
            make_package(package)
            parent = root / "parent.zip"
            make_parent(parent)

            with (
                package / "source-games.csv"
            ).open() as handle:
                rows = list(csv.DictReader(handle))
            rows[0]["team_score"] = "71"
            write_csv(
                package / "source-games.csv",
                list(rows[0]),
                rows,
            )

            with patch.object(
                mod,
                "research_portfolio_report",
                side_effect=fake_report,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "changed 1 accepted Stage 3B semantic",
                ):
                    mod.closeout(
                        "test",
                        package,
                        parent,
                        "b" * 40,
                        root / "out",
                    )

            check = json.loads(
                (
                    root
                    / "out"
                    / "stage4-parent-sanity-check.json"
                ).read_text()
            )
            self.assertEqual(
                check[
                    "semantic_comparison_unexpected_mismatches"
                ],
                1,
            )

    def test_corrupt_parent_manifest_stops(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "pkg"
            make_package(package)
            parent = root / "parent.zip"
            make_parent(parent)

            with zipfile.ZipFile(parent, "a") as archive:
                archive.writestr(
                    "stage3b-status.json",
                    json.dumps(
                        {
                            "status": "COMPLETE",
                            "school_key": "test",
                            "research_base_sha": "a" * 40,
                            "changed": True,
                        }
                    ),
                )

            with patch.object(
                mod,
                "research_portfolio_report",
                side_effect=fake_report,
            ):
                with self.assertRaisesRegex(
                    ValueError,
                    "manifest validation failed",
                ):
                    mod.closeout(
                        "test",
                        package,
                        parent,
                        "b" * 40,
                        root / "out",
                    )


    def test_reused_charlotte_coliseum_names_resolve_by_parent_key(self):
        parent = [
            {
                "research_game_id": "C1955",
                "source_program_key": "test",
                "season_label": "1970-1971",
                "game_date": "1971-01-01",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "stage3a_final_han": "NEUTRAL",
                "stage3a_curated_venue_key": "charlotte-coliseum-1955",
                "stage3a_curated_venue_name": "Charlotte Coliseum",
                "stage3a_site_city": "Charlotte",
                "stage3a_site_state": "NC",
            },
            {
                "research_game_id": "C1988",
                "source_program_key": "test",
                "season_label": "1990-1991",
                "game_date": "1991-01-01",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "stage3a_final_han": "NEUTRAL",
                "stage3a_curated_venue_key": "charlotte-coliseum-1988",
                "stage3a_curated_venue_name": "Charlotte Coliseum",
                "stage3a_site_city": "Charlotte",
                "stage3a_site_state": "NC",
            },
        ]
        package = [
            {
                "source_game_id": row["research_game_id"],
                "source_program_key": "test",
                "season_label": row["season_label"],
                "game_date": row["game_date"],
                "normalized_opponent_key": "old-college",
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Charlotte Coliseum",
                "city": "Charlotte",
                "state": "NC",
                "curated_game_type": "REGULAR_SEASON",
            }
            for row in parent
        ]
        venues = [
            {
                "venue_key": "charlotte-coliseum-1955",
                "canonical_name": "Charlotte Coliseum",
                "aliases": "",
                "city": "Charlotte",
                "state": "NC",
            },
            {
                "venue_key": "charlotte-coliseum-1988",
                "canonical_name": "Charlotte Coliseum",
                "aliases": "",
                "city": "Charlotte",
                "state": "NC",
            },
        ]

        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )

    def test_reused_madison_square_garden_names_resolve_by_parent_key(self):
        parent = [
            {
                "research_game_id": "M1925",
                "source_program_key": "test",
                "season_label": "1948-1949",
                "game_date": "1948-12-20",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "stage3a_final_han": "NEUTRAL",
                "stage3a_curated_venue_key": "madison-square-garden-1925",
                "stage3a_curated_venue_name": "Madison Square Garden",
                "stage3a_site_city": "New York",
                "stage3a_site_state": "NY",
            },
            {
                "research_game_id": "M1968",
                "source_program_key": "test",
                "season_label": "1970-1971",
                "game_date": "1970-03-13",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "stage3a_final_han": "NEUTRAL",
                "stage3a_curated_venue_key": "madison-square-garden-1968",
                "stage3a_curated_venue_name": "Madison Square Garden",
                "stage3a_site_city": "New York",
                "stage3a_site_state": "NY",
            },
        ]
        package = [
            {
                "source_game_id": row["research_game_id"],
                "source_program_key": "test",
                "season_label": row["season_label"],
                "game_date": row["game_date"],
                "normalized_opponent_key": "old-college",
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Madison Square Garden",
                "city": "New York",
                "state": "NY",
                "curated_game_type": "REGULAR_SEASON",
            }
            for row in parent
        ]
        venues = [
            {
                "venue_key": "madison-square-garden-1925",
                "canonical_name": "Madison Square Garden",
                "aliases": "Madison Square Garden (1925)",
                "city": "New York",
                "state": "NY",
            },
            {
                "venue_key": "madison-square-garden-1968",
                "canonical_name": "Madison Square Garden",
                "aliases": "Madison Square Garden (1968)",
                "city": "New York",
                "state": "NY",
            },
        ]

        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )

    def test_parent_venue_key_rejects_incompatible_exact_venue_row(self):
        parent = [
            {
                "research_game_id": "DRIFT",
                "source_program_key": "test",
                "season_label": "1970-1971",
                "game_date": "1971-01-01",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "stage3a_final_han": "NEUTRAL",
                "stage3a_curated_venue_key": "charlotte-coliseum-1955",
                "stage3a_curated_venue_name": "Charlotte Coliseum",
                "stage3a_site_city": "Charlotte",
                "stage3a_site_state": "NC",
            }
        ]
        package = [
            {
                "source_game_id": "DRIFT",
                "source_program_key": "test",
                "season_label": "1970-1971",
                "game_date": "1971-01-01",
                "normalized_opponent_key": "old-college",
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Charlotte Coliseum",
                "city": "Charlotte",
                "state": "NC",
                "curated_game_type": "REGULAR_SEASON",
            }
        ]
        venues = [
            {
                "venue_key": "charlotte-coliseum-1955",
                "canonical_name": "Charlotte Coliseum",
                "aliases": "",
                "city": "Greensboro",
                "state": "NC",
            },
            {
                "venue_key": "charlotte-coliseum-1988",
                "canonical_name": "Charlotte Coliseum",
                "aliases": "",
                "city": "Charlotte",
                "state": "NC",
            },
        ]

        mismatches = mod.compare_parent_semantics(parent, package, venues)
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["field"], "venue_key")
        self.assertEqual(
            mismatches[0]["parent_value"],
            "charlotte-coliseum-1955",
        )
        self.assertEqual(mismatches[0]["package_value"], "")

    def test_venue_key_allows_game_locality_alias_without_competing_venue(self):
        parent = [
            {
                "research_game_id": "IMPERIAL",
                "source_program_key": "test",
                "season_label": "2024-2025",
                "game_date": "2024-11-28",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "stage3a_final_han": "NEUTRAL",
                "accepted_venue_key": "imperial-arena",
                "accepted_venue_name": "Imperial Arena",
                "accepted_city": "Paradise Island",
                "accepted_state": "BS",
            }
        ]
        package = [
            {
                "source_game_id": "IMPERIAL",
                "source_program_key": "test",
                "season_label": "2024-2025",
                "game_date": "2024-11-28",
                "normalized_opponent_key": "old-college",
                "curated_site_type": "NEUTRAL",
                "curated_venue_name": "Imperial Arena",
                "city": "Paradise Island",
                "state": "BS",
                "curated_game_type": "REGULAR_SEASON",
            }
        ]
        venues = [
            {
                "venue_key": "imperial-arena",
                "canonical_name": "Imperial Arena",
                "aliases": "Imperial Arena at Atlantis Resort",
                "city": "Nassau",
                "state": "BS",
            }
        ]

        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )

    def test_unique_venue_name_comparison_remains_unchanged(self):
        parent = [
            {
                "research_game_id": "UNIQUE",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "opponent_key": "old-college",
                "game_type": "REGULAR_SEASON",
                "stage3a_final_han": "HOME",
                "stage3a_curated_venue_key": "test-gym",
                "stage3a_curated_venue_name": "Test Gym",
                "stage3a_site_city": "Testville",
                "stage3a_site_state": "TS",
            }
        ]
        package = [
            {
                "source_game_id": "UNIQUE",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "normalized_opponent_key": "old-college",
                "curated_site_type": "HOME",
                "curated_venue_name": "Old Test Gym",
                "city": "Testville",
                "state": "TS",
                "curated_game_type": "REGULAR_SEASON",
            }
        ]
        venues = [
            {
                "venue_key": "test-gym",
                "canonical_name": "Test Gym",
                "aliases": "Old Test Gym",
                "city": "Testville",
                "state": "TS",
            }
        ]

        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )


    def test_accepted_legacy_venue_aliases_compare_cleanly(self):
        parent = [
            {
                "research_game_id": "ACCEPTED",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "",
                "game_type": "REGULAR_SEASON",
                "raw_text": "raw ACCEPTED",
                "stage3a_final_han": "HOME",
                "accepted_venue_key": "test-gym",
                "accepted_venue_name": "Old Test Gym",
                "accepted_city": "Testville",
                "accepted_state": "TS",
            }
        ]
        package = [
            {
                "source_game_id": "ACCEPTED",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "normalized_opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "",
                "curated_site_type": "HOME",
                "curated_venue_name": "Old Test Gym",
                "city": "Testville",
                "state": "TS",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "raw ACCEPTED",
            }
        ]
        venues = [
            {
                "venue_key": "test-gym",
                "canonical_name": "Test Gym",
                "aliases": "Old Test Gym",
                "city": "Testville",
                "state": "TS",
            }
        ]
        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )

    def test_blank_overtime_remains_semantically_strict(self):
        parent = [
            {
                "research_game_id": "BLANK-OT",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "",
                "game_type": "REGULAR_SEASON",
                "raw_text": "raw BLANK-OT",
                "stage3a_final_han": "HOME",
                "stage3a_final_venue_name": "Test Gym",
                "stage3a_final_city": "Testville",
                "stage3a_final_state": "TS",
                "accepted_venue_key": "test-gym",
            }
        ]
        package = [
            {
                "source_game_id": "BLANK-OT",
                "source_program_key": "test",
                "season_label": "2000-2001",
                "game_date": "2000-12-01",
                "normalized_opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "",
                "curated_site_type": "HOME",
                "curated_venue_name": "Test Gym",
                "city": "Testville",
                "state": "TS",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "raw BLANK-OT",
            }
        ]
        venues = [
            {
                "venue_key": "test-gym",
                "canonical_name": "Test Gym",
                "aliases": "",
                "city": "Testville",
                "state": "TS",
            }
        ]

        self.assertEqual(
            mod.compare_parent_semantics(parent, package, venues),
            [],
        )
        package[0]["overtime_periods"] = "0"
        mismatches = mod.compare_parent_semantics(parent, package, venues)
        self.assertEqual(len(mismatches), 1)
        self.assertEqual(mismatches[0]["field"], "overtime_periods")


    def test_dual_id_parent_namespace_and_projection_semantics_compare_cleanly(self):
        parent = [
            {
                "source_game_id": "SRC-1",
                "research_game_id": "RG-1",
                "source_program_key": "test",
                "season_label": "1999-00",
                "game_date": "2000-03-15",
                "opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "",
                "game_type": "REGULAR_SEASON",
                "raw_text": "",
                "source_raw_text": "  accepted literal  ",
                "stage3a_final_han": "HOME",
            }
        ]
        package = [
            {
                "source_game_id": "SRC-1",
                "source_program_key": "test",
                "season_label": "1999-2000",
                "game_date": "2000-03-15",
                "normalized_opponent_key": "old-college",
                "team_score": "70",
                "opponent_score": "60",
                "played_result": "W",
                "overtime_periods": "",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "",
                "city": "",
                "state": "",
                "curated_game_type": "REGULAR_SEASON",
                "raw_text": "  accepted literal  ",
            }
        ]
        self.assertEqual(mod.project_game_id(parent[0]), "SRC-1")
        self.assertEqual(
            mod.compare_parent_semantics(parent, package, []),
            [],
        )


if __name__ == "__main__":
    unittest.main()
