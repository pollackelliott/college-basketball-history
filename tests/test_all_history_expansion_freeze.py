import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import all_history_expansion_freeze as freeze  # noqa: E402
from all_history_expansion_freeze import (  # noqa: E402
    CORRECTION_QUESTION_FIELDS,
    EXCLUSION_FIELDS,
    MANIFEST_MEMBER,
    NON_D1_SCAN_FIELDS,
    OPPONENT_SUPPORT_FIELDS,
    PAYLOAD_MEMBERS,
    RESIDUAL_FIELDS,
    SEASON_ACCOUNTING_FIELDS,
    VENUE_SUPPORT_FIELDS,
    ExpansionFreezeError,
    authenticate_baseline,
    canonical_json_bytes,
    canonical_row_sha256,
    freeze_expansion,
    verify_expansion,
    write_deterministic_zip,
)


SOURCE_FIELDS = [
    "source_game_id",
    "source_program_key",
    "season_label",
    "game_date",
    "source_opponent_label",
    "normalized_opponent_key",
    "normalized_opponent_name",
    "team_score",
    "opponent_score",
    "played_result",
    "overtime_periods",
    "curated_site_type",
    "curated_venue_name",
    "city",
    "state",
    "curated_game_type",
    "curated_postseason_round",
    "event_or_tournament",
    "administrative_status",
    "site_research_status",
    "site_research_basis",
    "raw_text",
    "source_page",
    "source_series_event_note",
]
OPPONENT_FIELDS = [
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
]
VENUE_FIELDS = [
    "source_program_key",
    "venue_key",
    "venue_id",
    "canonical_name",
    "aliases",
    "city",
    "state",
    "venue_type",
    "known_opened",
    "known_closed",
    "venue_date_precision",
    "games_currently_assigned",
    "first_assigned_game",
    "last_assigned_game",
    "relationship_type",
    "relationship_start",
    "relationship_end",
    "relationship_date_precision",
    "site_rule",
    "source_basis",
    "notes",
]
CANONICAL_FIELDS = [
    "canonical_game_id",
    "season_label",
    "game_date",
    "date_precision",
    "team_a_key",
    "team_b_key",
    "team_a_score",
    "team_b_score",
    "result_winner_team_key",
    "overtime_periods",
    "site_type",
    "designated_home_team_key",
    "venue_key",
    "venue_id",
    "site_city",
    "site_state",
    "game_type",
    "postseason_round",
    "administrative_status",
    "administrative_note",
    "canonical_status",
    "notes",
]


def csv_bytes(fields, rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({field: row.get(field, "") for field in fields})
    return stream.getvalue().encode("utf-8")


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(csv_bytes(fields, rows))


def git(repo, *args):
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if result.returncode:
        raise AssertionError(result.stderr)
    return result.stdout.strip()


def source_row(source_id, season, opponent_key="lower-college", label="Lower College"):
    return {
        "source_game_id": source_id,
        "source_program_key": "legacy",
        "season_label": season,
        "game_date": season[:4] + "-12-01",
        "source_opponent_label": label,
        "normalized_opponent_key": opponent_key,
        "normalized_opponent_name": label,
        "team_score": "70",
        "opponent_score": "60",
        "played_result": "W",
        "overtime_periods": "0",
        "curated_site_type": "OPPONENT_HOME",
        "curated_venue_name": "",
        "city": "",
        "state": "",
        "curated_game_type": "REGULAR_SEASON",
        "curated_postseason_round": "",
        "event_or_tournament": "",
        "administrative_status": "",
        "site_research_status": "",
        "site_research_basis": "",
        "raw_text": f"accepted W 70-60 vs {label}",
        "source_page": f"source-{source_id}",
        "source_series_event_note": "",
    }


def opponent_row(label, key, current_d1="FALSE"):
    return {
        "source_program_key": "legacy",
        "source_opponent_label": label,
        "canonical_opponent_key": key,
        "canonical_opponent_name": label,
        "current_d1": current_d1,
        "games_with_source_label": "1",
        "first_season": "1968-1969",
        "last_season": "1969-1970",
        "resolution_status": "RESOLVED",
        "resolution_method": "EXPANSION_RESEARCH",
        "user_choice": "",
        "audit_note": "accepted supplemental identity",
    }


def venue_row(key="legacy-gym"):
    return {
        "source_program_key": "legacy",
        "venue_key": key,
        "venue_id": "VEN-000001",
        "canonical_name": "Legacy Gym",
        "aliases": "",
        "city": "Legacy",
        "state": "IL",
        "venue_type": "ARENA",
        "known_opened": "1950",
        "known_closed": "",
        "venue_date_precision": "YEAR",
        "games_currently_assigned": "2",
        "first_assigned_game": "1970-12-01",
        "last_assigned_game": "1971-12-01",
        "relationship_type": "HOME",
        "relationship_start": "1970",
        "relationship_end": "",
        "relationship_date_precision": "YEAR",
        "site_rule": "",
        "source_basis": "accepted baseline chronology",
        "notes": "",
    }


class ExpansionFreezeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        git(self.repo, "init")
        git(self.repo, "config", "user.email", "tests@example.invalid")
        git(self.repo, "config", "user.name", "Expansion Tests")
        self._write_baseline()
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "baseline")
        self.base = git(self.repo, "rev-parse", "HEAD")
        self.delta = self.root / "delta"
        self.output = self.root / "freeze.zip"
        self._write_valid_delta()

    def tearDown(self):
        self.temporary.cleanup()

    def _program(self, **overrides):
        row = {
            "program_key": "legacy",
            "program_name": "Legacy University",
            "display_name": "Legacy University",
            "nickname": "Legacy",
            "city": "Legacy",
            "state": "IL",
            "primary_hex": "#000000",
            "secondary_hex": "#FFFFFF",
            "current_d1": "Yes",
            "public_page_enabled": "Yes",
            "program_inception_season": "",
            "history_coverage_status": "LEGACY_TOP_LEVEL_ONLY",
            "history_start_season": "1970-1971",
            "history_scope_status": "OWNER_CONFIRMED",
            "history_scope_basis": "FIRST_TOP_LEVEL_SEASON",
            "history_scope_notes": "Accepted baseline top-level history.",
            "history_scope_intervals": "",
        }
        row.update(overrides)
        return row

    def _write_baseline(self, program=None, baseline_raw_text="accepted baseline"):
        program = program or self._program()
        write_csv(
            self.repo / "data/reference/programs.csv",
            list(program),
            [program],
        )
        write_csv(
            self.repo / "data/reference/program-top-level-scope.csv",
            ["school", "top_level_scope"],
            [{"school": "Legacy University", "top_level_scope": "1970-71+"}],
        )
        write_csv(
            self.repo / "data/reference/program-accomplishments.csv",
            [
                "program_key",
                "conference_regular_season_championships",
                "conference_tournament_championships",
                "ncaa_tournament_appearances",
                "final_four_appearances",
                "national_championships",
                "best_finish_key",
                "best_finish_year",
                "verification_status",
                "verification_basis",
                "canonical_crosscheck_status",
                "notes",
            ],
            [{
                "program_key": "legacy",
                "conference_regular_season_championships": "0",
                "conference_tournament_championships": "0",
                "ncaa_tournament_appearances": "0",
                "final_four_appearances": "0",
                "national_championships": "0",
                "best_finish_key": "",
                "best_finish_year": "",
                "verification_status": "VERIFIED",
                "verification_basis": "accepted baseline",
                "canonical_crosscheck_status": "PASS",
                "notes": "",
            }],
        )
        baseline_sources = [
            source_row("BASE-1", "1970-1971", "baseline-opp", "Baseline Opp"),
            source_row("BASE-2", "1971-1972", "baseline-opp", "Baseline Opp"),
        ]
        for row in baseline_sources:
            row["raw_text"] = baseline_raw_text
        write_csv(
            self.repo / "schools/legacy/source-games.csv",
            SOURCE_FIELDS,
            baseline_sources,
        )
        write_csv(
            self.repo / "schools/legacy/opponents.csv",
            OPPONENT_FIELDS,
            [opponent_row("Baseline Opp", "baseline-opp", "FALSE")],
        )
        write_csv(
            self.repo / "schools/legacy/venues.csv",
            VENUE_FIELDS,
            [venue_row()],
        )
        write_csv(
            self.repo / "schools/legacy/conferences.csv",
            [
                "source_program_key",
                "conference_key",
                "conference_name",
                "membership_start",
                "membership_end",
                "membership_type",
                "source_basis",
                "notes",
            ],
            [],
        )
        (self.repo / "schools/legacy/notes.md").write_text(
            "accepted baseline notes\n", encoding="utf-8"
        )
        (self.repo / "schools/legacy/source-notes.md").write_text(
            "accepted baseline source notes\n", encoding="utf-8"
        )
        canonical = [
            {
                "canonical_game_id": "CBBG-1",
                "season_label": "1970-1971",
                "team_a_key": "baseline-opp",
                "team_b_key": "legacy",
                "game_type": "REGULAR_SEASON",
            },
            {
                "canonical_game_id": "CBBG-2",
                "season_label": "1971-1972",
                "team_a_key": "baseline-opp",
                "team_b_key": "legacy",
                "game_type": "REGULAR_SEASON",
            },
            {
                "canonical_game_id": "CBBG-X",
                "season_label": "1969-1970",
                "team_a_key": "legacy",
                "team_b_key": "other",
                "game_type": "REGULAR_SEASON",
            },
        ]
        write_csv(
            self.repo / "data/canonical/games.csv",
            CANONICAL_FIELDS,
            canonical,
        )

    def _support_opponent(self, label="Lower College", key="lower-college"):
        candidate = opponent_row(label, key, "FALSE")
        return {
            "support_id": "OPP-1",
            "support_action": "NEW_SUPPLEMENTAL",
            "source_opponent_label": label,
            "canonical_opponent_key": key,
            "baseline_row_sha256": "",
            "changed_fields": "",
            "candidate_row_json": json.dumps(
                candidate, ensure_ascii=False, sort_keys=True, separators=(",", ":")
            ),
            "evidence_basis": "supplemental opponent research",
        }

    def _write_valid_delta(self, inception="1968-1969"):
        self.delta.mkdir(exist_ok=True)
        rows = [
            source_row("EXP-1", "1968-1969"),
            source_row("EXP-2", "1969-1970"),
        ]
        write_csv(self.delta / "expansion-source-games.csv", SOURCE_FIELDS, rows)
        write_csv(
            self.delta / "expansion-opponents.csv",
            OPPONENT_SUPPORT_FIELDS,
            [self._support_opponent()],
        )
        write_csv(
            self.delta / "expansion-venues.csv",
            VENUE_SUPPORT_FIELDS,
            [],
        )
        write_csv(
            self.delta / "expansion-season-accounting.csv",
            SEASON_ACCOUNTING_FIELDS,
            [
                {
                    "season_label": "1968-1969",
                    "activity_disposition": "ACTIVE",
                    "identified_competitive_game_count": "1",
                    "accounting_basis": "institutional results ledger",
                },
                {
                    "season_label": "1969-1970",
                    "activity_disposition": "ACTIVE",
                    "identified_competitive_game_count": "1",
                    "accounting_basis": "institutional results ledger",
                },
            ],
        )
        write_csv(
            self.delta / "expansion-exclusions.csv",
            EXCLUSION_FIELDS,
            [],
        )
        write_csv(
            self.delta / "expansion-residuals.csv",
            RESIDUAL_FIELDS,
            [],
        )
        write_csv(
            self.delta / "expansion-non-d1-scan.csv",
            NON_D1_SCAN_FIELDS,
            [{
                "opponent_key": "lower-college",
                "supplemental_game_count": "2",
                "representative_raw_labels": "Lower College",
                "support_scope": "SUPPLEMENTAL_NEW",
                "scan_disposition": "CLEARED",
                "scan_basis": "",
            }],
        )
        write_csv(
            self.delta / "expansion-baseline-correction-questions.csv",
            CORRECTION_QUESTION_FIELDS,
            [],
        )
        (self.delta / "expansion-notes.md").write_text(
            f"research_base_sha={self.base}\n"
            f"researched institutional inception={inception}\n"
            "The accepted baseline is inherited and was not reopened.\n"
            "Expansion-required seasons were researched from institutional sources.\n",
            encoding="utf-8",
        )
        (self.delta / "expansion-source-notes.md").write_text(
            "Supplemental institutional results and schedule source family.\n",
            encoding="utf-8",
        )

    def _freeze(self, inception="1968-1969", output=None):
        return freeze_expansion(
            self.repo,
            "legacy",
            self.delta,
            self.base,
            inception,
            output or self.output,
        )

    def _rows(self, name):
        with (self.delta / name).open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def _rewrite(self, name, fields, rows):
        write_csv(self.delta / name, fields, rows)

    def _recommit_baseline(self):
        git(self.repo, "add", ".")
        git(self.repo, "commit", "-m", "alternate baseline")
        self.base = git(self.repo, "rev-parse", "HEAD")
        self._write_valid_delta()

    def _manifest(self):
        with zipfile.ZipFile(self.output) as archive:
            return json.loads(archive.read(MANIFEST_MEMBER))

    def _rewrite_artifact_manifest(self, mutate):
        with zipfile.ZipFile(self.output) as archive:
            members = {name: archive.read(name) for name in archive.namelist()}
        manifest = json.loads(members[MANIFEST_MEMBER])
        mutate(manifest)
        manifest["manifest_self_fingerprint_sha256"] = ""
        manifest["manifest_self_fingerprint_sha256"] = freeze.manifest_self_fingerprint(
            manifest
        )
        members[MANIFEST_MEMBER] = canonical_json_bytes(manifest)
        write_deterministic_zip(self.output, members)

    def test_01_valid_simple_expansion_freezes_and_verifies(self):
        report = self._freeze()
        self.assertEqual(report["status"], "EXPANSION_RESEARCH_FROZEN")
        verified = verify_expansion(self.repo, self.output)
        self.assertEqual(verified["status"], "VERIFIED_EXPANSION_RESEARCH_FROZEN")
        self.assertEqual(verified["supplemental_source_game_count"], 2)

    def test_02_identical_inputs_produce_identical_zip(self):
        second = self.root / "freeze-2.zip"
        one = self._freeze()
        two = self._freeze(output=second)
        self.assertEqual(self.output.read_bytes(), second.read_bytes())
        self.assertEqual(one["zip_sha256"], two["zip_sha256"])

    def test_03_complete_baseline_rejected(self):
        self._write_baseline(self._program(
            history_coverage_status="COMPLETE_INSTITUTIONAL",
            program_inception_season="1968-1969",
        ))
        self._recommit_baseline()
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_04_unmigrated_and_unpublished_baselines_rejected(self):
        for overrides in (
            {"history_coverage_status": "UNMIGRATED"},
            {"public_page_enabled": "No"},
        ):
            with self.subTest(overrides=overrides):
                other = self.root / ("case-" + str(len(list(self.root.iterdir()))))
                other.mkdir()
                repo = other / "repo"
                repo.mkdir()
                git(repo, "init")
                git(repo, "config", "user.email", "tests@example.invalid")
                git(repo, "config", "user.name", "Expansion Tests")
                old_repo = self.repo
                self.repo = repo
                self._write_baseline(self._program(**overrides))
                git(repo, "add", ".")
                git(repo, "commit", "-m", "baseline")
                base = git(repo, "rev-parse", "HEAD")
                self.repo = old_repo
                with self.assertRaises(ExpansionFreezeError):
                    authenticate_baseline(repo, "legacy", base)

    def test_05_wrong_or_missing_research_base_rejected(self):
        with self.assertRaises(ExpansionFreezeError):
            freeze_expansion(
                self.repo, "legacy", self.delta, "", "1968-1969", self.output
            )
        with self.assertRaises(ExpansionFreezeError):
            freeze_expansion(
                self.repo,
                "legacy",
                self.delta,
                "0" * 40,
                "1968-1969",
                self.output,
            )

    def test_06_baseline_package_member_drift_detected(self):
        self._freeze()
        self._rewrite_artifact_manifest(
            lambda manifest: manifest["baseline"]["package_member_sha256"].__setitem__(
                "notes.md", "0" * 64
            )
        )
        with self.assertRaises(ExpansionFreezeError):
            verify_expansion(self.repo, self.output)

    def test_07_baseline_program_row_drift_detected(self):
        self._freeze()
        self._rewrite_artifact_manifest(
            lambda manifest: manifest["baseline"].__setitem__(
                "program_row_sha256", "0" * 64
            )
        )
        with self.assertRaises(ExpansionFreezeError):
            verify_expansion(self.repo, self.output)

    def test_08_baseline_scope_row_drift_detected(self):
        self._freeze()
        self._rewrite_artifact_manifest(
            lambda manifest: manifest["baseline"].__setitem__(
                "top_level_scope_row_sha256", "0" * 64
            )
        )
        with self.assertRaises(ExpansionFreezeError):
            verify_expansion(self.repo, self.output)

    def test_09_baseline_source_population_hash_is_bound(self):
        self._freeze()
        self._rewrite_artifact_manifest(
            lambda manifest: manifest["baseline"].__setitem__(
                "source_game_id_population_sha256", "0" * 64
            )
        )
        with self.assertRaises(ExpansionFreezeError):
            verify_expansion(self.repo, self.output)

    def test_10_baseline_published_canonical_population_is_bound(self):
        self._freeze()
        self._rewrite_artifact_manifest(
            lambda manifest: manifest["baseline"].__setitem__(
                "publication_authorized_canonical_id_population_sha256", "0" * 64
            )
        )
        with self.assertRaises(ExpansionFreezeError):
            verify_expansion(self.repo, self.output)

    def test_11_supplemental_source_id_collision_rejected(self):
        rows = self._rows("expansion-source-games.csv")
        rows[0]["source_game_id"] = "BASE-1"
        self._rewrite("expansion-source-games.csv", SOURCE_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_12_duplicate_supplemental_source_ids_rejected(self):
        rows = self._rows("expansion-source-games.csv")
        rows[1]["source_game_id"] = rows[0]["source_game_id"]
        self._rewrite("expansion-source-games.csv", SOURCE_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_13_baseline_published_source_season_rejected(self):
        rows = self._rows("expansion-source-games.csv")
        rows[0]["season_label"] = "1970-1971"
        self._rewrite("expansion-source-games.csv", SOURCE_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_14_pre_inception_source_season_rejected(self):
        rows = self._rows("expansion-source-games.csv")
        rows[0]["season_label"] = "1967-1968"
        self._rewrite("expansion-source-games.csv", SOURCE_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_15_interrupted_history_internal_gap_is_accepted(self):
        program = self._program(
            history_start_season="1960-1961",
            history_scope_basis="TOP_LEVEL_INTERVALS",
            history_scope_intervals="1960-1961..1965-1966|1970-1971+",
        )
        self._write_baseline(program)
        write_csv(
            self.repo / "data/reference/program-top-level-scope.csv",
            ["school", "top_level_scope"],
            [{"school": "Legacy University", "top_level_scope": "1960-61..1965-66|1970-71+"}],
        )
        self._recommit_baseline()
        rows = [source_row("EXP-GAP", "1966-1967")]
        self._rewrite("expansion-source-games.csv", SOURCE_FIELDS, rows)
        self._rewrite(
            "expansion-opponents.csv",
            OPPONENT_SUPPORT_FIELDS,
            [self._support_opponent()],
        )
        accounting = []
        for year in range(1959, 1970):
            label = f"{year:04d}-{year + 1:04d}"
            if year in range(1960, 1966):
                continue
            accounting.append({
                "season_label": label,
                "activity_disposition": "ACTIVE" if year == 1966 else "DORMANT_OR_NO_TEAM",
                "identified_competitive_game_count": "1" if year == 1966 else "0",
                "accounting_basis": "expansion season accounting",
            })
        self._rewrite(
            "expansion-season-accounting.csv",
            SEASON_ACCOUNTING_FIELDS,
            accounting,
        )
        scan = self._rows("expansion-non-d1-scan.csv")
        scan[0]["supplemental_game_count"] = "1"
        self._rewrite("expansion-non-d1-scan.csv", NON_D1_SCAN_FIELDS, scan)
        (self.delta / "expansion-notes.md").write_text(
            f"research_base_sha={self.base}\n"
            "researched institutional inception=1959-1960\n"
            "The accepted baseline is inherited and was not reopened.\n",
            encoding="utf-8",
        )
        self.assertEqual(
            self._freeze(inception="1959-1960")["status"],
            "EXPANSION_RESEARCH_FROZEN",
        )

    def test_16_missing_required_season_accounting_rejected(self):
        rows = self._rows("expansion-season-accounting.csv")
        self._rewrite("expansion-season-accounting.csv", SEASON_ACCOUNTING_FIELDS, rows[:1])
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_17_extra_baseline_published_accounting_rejected(self):
        rows = self._rows("expansion-season-accounting.csv")
        rows.append({
            "season_label": "1970-1971",
            "activity_disposition": "DORMANT_OR_NO_TEAM",
            "identified_competitive_game_count": "0",
            "accounting_basis": "wrong extra row",
        })
        self._rewrite("expansion-season-accounting.csv", SEASON_ACCOUNTING_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_18_active_count_mismatch_rejected(self):
        rows = self._rows("expansion-season-accounting.csv")
        rows[0]["identified_competitive_game_count"] = "0"
        self._rewrite("expansion-season-accounting.csv", SEASON_ACCOUNTING_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_19_dormant_season_with_game_rejected(self):
        rows = self._rows("expansion-season-accounting.csv")
        rows[0]["activity_disposition"] = "DORMANT_OR_NO_TEAM"
        rows[0]["identified_competitive_game_count"] = "0"
        self._rewrite("expansion-season-accounting.csv", SEASON_ACCOUNTING_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_20_empty_accounting_basis_rejected(self):
        rows = self._rows("expansion-season-accounting.csv")
        rows[0]["accounting_basis"] = ""
        self._rewrite("expansion-season-accounting.csv", SEASON_ACCOUNTING_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_21_blocking_residual_rejects_freeze(self):
        self._rewrite(
            "expansion-residuals.csv",
            RESIDUAL_FIELDS,
            [{
                "residual_id": "RES-1",
                "season_label": "1968-1969",
                "source_game_id": "EXP-1",
                "residual_category": "SITE",
                "status": "BLOCKING",
                "research_basis": "unresolved blocker",
            }],
        )
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_22_researched_nonblocking_residual_survives_and_verifies(self):
        self._rewrite(
            "expansion-residuals.csv",
            RESIDUAL_FIELDS,
            [{
                "residual_id": "RES-1",
                "season_label": "1968-1969",
                "source_game_id": "EXP-1",
                "residual_category": "RESEARCHED_SITE_DETAIL",
                "status": "NONBLOCKING_RESEARCHED",
                "research_basis": "accepted under substantive Research policy",
            }],
        )
        self._freeze()
        self.assertEqual(
            verify_expansion(self.repo, self.output)["status"],
            "VERIFIED_EXPANSION_RESEARCH_FROZEN",
        )

    def test_23_missing_required_non_d1_scan_identity_rejected(self):
        self._rewrite("expansion-non-d1-scan.csv", NON_D1_SCAN_FIELDS, [])
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_24_unresolved_owner_flag_rejected(self):
        rows = self._rows("expansion-non-d1-scan.csv")
        rows[0]["scan_disposition"] = "UNRESOLVED"
        self._rewrite("expansion-non-d1-scan.csv", NON_D1_SCAN_FIELDS, rows)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_25_blocks_expansion_correction_question_rejected(self):
        self._rewrite(
            "expansion-baseline-correction-questions.csv",
            CORRECTION_QUESTION_FIELDS,
            [{
                "question_id": "Q-1",
                "inherited_source_game_id": "BASE-1",
                "canonical_game_id": "CBBG-1",
                "issue": "baseline contradiction",
                "evidence_basis": "new authoritative source",
                "expansion_impact": "BLOCKS_EXPANSION",
                "disposition": "routed to correction",
            }],
        )
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_26_no_impact_correction_question_is_preserved_without_authority(self):
        self._rewrite(
            "expansion-baseline-correction-questions.csv",
            CORRECTION_QUESTION_FIELDS,
            [{
                "question_id": "Q-1",
                "inherited_source_game_id": "BASE-1",
                "canonical_game_id": "CBBG-1",
                "issue": "separate baseline question",
                "evidence_basis": "supplemental discovery",
                "expansion_impact": "NO_EXPANSION_IMPACT",
                "disposition": "separately routed; no expansion mutation authority",
            }],
        )
        self._freeze()
        manifest = self._manifest()
        self.assertEqual(
            manifest["expansion"]["baseline_correction_question_count"], 1
        )
        self.assertIn("Supplemental expansion Research authority only", manifest["authority_statement"])
        verify_expansion(self.repo, self.output)

    def test_27_support_delta_cannot_silently_overwrite_inherited_identity(self):
        baseline = authenticate_baseline(self.repo, "legacy", self.base)
        inherited = baseline["opponent_rows"][0]
        candidate = dict(inherited)
        candidate["canonical_opponent_name"] = "Rewritten Baseline Opponent"
        row = {
            "support_id": "OPP-BASE",
            "support_action": "EXTEND_INHERITED",
            "source_opponent_label": "Baseline Opp",
            "canonical_opponent_key": "baseline-opp",
            "baseline_row_sha256": canonical_row_sha256(inherited),
            "changed_fields": "canonical_opponent_name",
            "candidate_row_json": json.dumps(candidate, sort_keys=True, separators=(",", ":")),
            "evidence_basis": "attempted rewrite",
        }
        sources = self._rows("expansion-source-games.csv")
        for source in sources:
            source["source_opponent_label"] = "Baseline Opp"
            source["normalized_opponent_key"] = "baseline-opp"
            source["normalized_opponent_name"] = "Baseline Opp"
        self._rewrite("expansion-source-games.csv", SOURCE_FIELDS, sources)
        self._rewrite("expansion-opponents.csv", OPPONENT_SUPPORT_FIELDS, [row])
        scan = self._rows("expansion-non-d1-scan.csv")
        scan[0]["opponent_key"] = "baseline-opp"
        scan[0]["support_scope"] = "INHERITED_EXTENSION"
        self._rewrite("expansion-non-d1-scan.csv", NON_D1_SCAN_FIELDS, scan)
        with self.assertRaises(ExpansionFreezeError):
            self._freeze()

    def test_28_hash_bound_venue_chronology_extension_is_representable(self):
        baseline = authenticate_baseline(self.repo, "legacy", self.base)
        inherited = baseline["venue_rows"][0]
        candidate = dict(inherited)
        candidate["relationship_start"] = "1968"
        candidate["source_basis"] = "accepted baseline plus supplemental chronology evidence"
        venue_support = {
            "support_id": "VEN-EXT",
            "support_action": "EXTEND_INHERITED",
            "venue_key": "legacy-gym",
            "baseline_row_sha256": canonical_row_sha256(inherited),
            "changed_fields": "relationship_start;source_basis",
            "candidate_row_json": json.dumps(candidate, sort_keys=True, separators=(",", ":")),
            "evidence_basis": "supplemental HOME chronology extension",
        }
        self._rewrite("expansion-venues.csv", VENUE_SUPPORT_FIELDS, [venue_support])
        self._freeze()
        manifest = self._manifest()
        self.assertEqual(manifest["expansion"]["venue_support_count"], 1)
        verify_expansion(self.repo, self.output)

    def test_29_freeze_contains_no_complete_inherited_package(self):
        self._freeze()
        with zipfile.ZipFile(self.output) as archive:
            names = set(archive.namelist())
        self.assertEqual(names, set(PAYLOAD_MEMBERS) | {MANIFEST_MEMBER})
        self.assertFalse(names.intersection({
            "source-games.csv", "opponents.csv", "venues.csv", "conferences.csv",
            "notes.md", "source-notes.md",
        }))

    def test_30_verify_does_not_apply_new_research_rules_to_inherited_rows(self):
        self._write_baseline(baseline_raw_text="")
        self._recommit_baseline()
        self._freeze()
        self.assertEqual(
            verify_expansion(self.repo, self.output)["status"],
            "VERIFIED_EXPANSION_RESEARCH_FROZEN",
        )

    def test_31_freeze_and_verify_do_not_mutate_tracked_repository_data(self):
        before = git(self.repo, "status", "--porcelain")
        tracked_before = git(self.repo, "ls-files", "-s")
        self._freeze()
        verify_expansion(self.repo, self.output)
        self.assertEqual(git(self.repo, "status", "--porcelain"), before)
        self.assertEqual(git(self.repo, "ls-files", "-s"), tracked_before)

    def test_32_manifest_records_exact_required_baseline_fingerprints(self):
        baseline = authenticate_baseline(self.repo, "legacy", self.base)
        self._freeze()
        manifest = self._manifest()
        recorded = manifest["baseline"]
        self.assertEqual(recorded["program_row_sha256"], baseline["program_row_sha256"])
        self.assertEqual(recorded["top_level_scope_row_sha256"], baseline["scope_row_sha256"])
        self.assertEqual(recorded["accomplishment_row_status"], "PRESENT")
        self.assertEqual(recorded["accomplishment_row_sha256"], baseline["accomplishment_row_sha256"])
        self.assertEqual(recorded["package_member_sha256"], baseline["package_member_sha256"])

    def test_33_manifest_payload_hashes_cover_all_non_manifest_members(self):
        self._freeze()
        manifest = self._manifest()
        self.assertEqual(
            set(manifest["frozen_payload_member_sha256"]),
            set(PAYLOAD_MEMBERS),
        )

    def test_34_fresh_verify_rejects_member_byte_drift(self):
        self._freeze()
        with zipfile.ZipFile(self.output) as archive:
            members = {name: archive.read(name) for name in archive.namelist()}
        members["expansion-notes.md"] += b"tampered\n"
        write_deterministic_zip(self.output, members)
        with self.assertRaises(ExpansionFreezeError):
            verify_expansion(self.repo, self.output)


if __name__ == "__main__":
    unittest.main()
