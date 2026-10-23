import csv
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from integration_freeze_guard import (  # noqa: E402
    build_source_game_semantic_snapshot,
    semantic_snapshot_sha256,
)
from remote_implementation_control import RemoteImplementationError  # noqa: E402
from remote_implementation_stage2_opponent_display import (  # noqa: E402
    apply_and_prepare_repair,
    field_level_mutation_proof,
    run_normalizer_dry_run,
    verify_census_and_freeze_authority,
)


SCHOOL = "example-school"
TARGET_BRANCH = "data/example-school-onboarding"
KEYS = ["alpha-academy", "beta-club"]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class RemoteStage2OpponentDisplayTests(unittest.TestCase):
    def git(self, repo: Path, *args: str, check: bool = True) -> str:
        cp = subprocess.run(
            ["git", *args],
            cwd=repo,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if check and cp.returncode:
            self.fail(cp.stdout)
        return cp.stdout.strip()

    def make_repo(self, *, mode: str = "normal") -> tuple[Path, str, bytes]:
        repo = Path(tempfile.mkdtemp(prefix="stage2-display-test-"))
        self.addCleanup(lambda: shutil.rmtree(repo, ignore_errors=True))
        self.git(repo, "init")
        self.git(repo, "config", "user.name", "Test")
        self.git(repo, "config", "user.email", "test@example.com")
        (repo / ".gitignore").write_text(".onboarding/\n", encoding="utf-8")
        (repo / "mode.txt").write_text(mode + "\n", encoding="utf-8")
        (repo / "keys.json").write_text(
            json.dumps(KEYS) + "\n",
            encoding="utf-8",
        )

        write_csv(
            repo / "schools" / SCHOOL / "opponents.csv",
            [
                "source_program_key",
                "source_opponent_label",
                "canonical_opponent_key",
                "canonical_opponent_name",
                "notes",
            ],
            [
                {
                    "source_program_key": SCHOOL,
                    "source_opponent_label": "Alpha old",
                    "canonical_opponent_key": "alpha-academy",
                    "canonical_opponent_name": "Alpha old",
                    "notes": "literal one",
                },
                {
                    "source_program_key": SCHOOL,
                    "source_opponent_label": "Beta old",
                    "canonical_opponent_key": "beta-club",
                    "canonical_opponent_name": "Beta old",
                    "notes": "literal two",
                },
            ],
        )
        write_csv(
            repo / "schools" / SCHOOL / "source-games.csv",
            [
                "source_game_id",
                "normalized_opponent_key",
                "normalized_opponent_name",
                "source_opponent_label",
                "raw_text",
                "season_label",
                "game_date",
                "team_score",
                "opponent_score",
                "played_result",
                "site_type",
                "curated_venue_name",
                "curated_game_type",
                "curated_postseason_round",
            ],
            [
                {
                    "source_game_id": "E-1",
                    "normalized_opponent_key": "alpha-academy",
                    "normalized_opponent_name": "Alpha old",
                    "source_opponent_label": "Alpha literal",
                    "raw_text": "at Alpha literal",
                    "season_label": "1940-41",
                    "game_date": "1941-01-01",
                    "team_score": "50",
                    "opponent_score": "40",
                    "played_result": "W",
                    "site_type": "OPPONENT_HOME",
                    "curated_venue_name": "",
                    "curated_game_type": "REGULAR_SEASON",
                    "curated_postseason_round": "",
                },
                {
                    "source_game_id": "E-2",
                    "normalized_opponent_key": "beta-club",
                    "normalized_opponent_name": "Beta old",
                    "source_opponent_label": "Beta literal",
                    "raw_text": "vs Beta literal",
                    "season_label": "1940-41",
                    "game_date": "1941-01-02",
                    "team_score": "45",
                    "opponent_score": "44",
                    "played_result": "W",
                    "site_type": "NEUTRAL",
                    "curated_venue_name": "Test Arena",
                    "curated_game_type": "REGULAR_SEASON",
                    "curated_postseason_round": "",
                },
            ],
        )

        tools = repo / "tools"
        tools.mkdir()
        normalizer = r'''#!/usr/bin/env python3
import argparse,csv,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("school")
p.add_argument("--repo",type=Path,required=True)
p.add_argument("--sync-source-games",action="store_true")
p.add_argument("--apply",action="store_true")
p.add_argument("--json-output",type=Path)
a=p.parse_args()
repo=a.repo.resolve()
keys=json.loads((repo/"keys.json").read_text())
mode=(repo/"mode.txt").read_text().strip()
changes=[
 {"canonical_opponent_key":key,"from_names":[key+" old"],"to_name":key+" authority"}
 for key in keys
]
report={
 "schema_version":1,"school_key":a.school,
 "status":"BLOCKED" if mode=="ambiguous" else "PASS",
 "change_key_count":len(keys),"change_row_count":len(keys),
 "changes":changes,
 "ambiguous_key_count":1 if mode=="ambiguous" else 0,
 "ambiguous":[{"canonical_opponent_key":keys[0]}] if mode=="ambiguous" else [],
 "source_game_display_change_rows":len(keys),
 "source_game_display_change_keys":len(keys),
 "source_game_display_changes":[
  {"source_game_id":"E-%d"%(i+1),"normalized_opponent_key":key,
   "from_name":key+" old","to_name":key+" authority"}
  for i,key in enumerate(keys)
 ],
}
if a.json_output:
 a.json_output.parent.mkdir(parents=True,exist_ok=True)
 a.json_output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
if mode=="ambiguous":
 raise SystemExit(1)
if not a.apply:
 raise SystemExit(0)
def read(path):
 with path.open(newline="",encoding="utf-8") as h:
  r=csv.DictReader(h); return list(r.fieldnames or []),list(r)
def write(path,fields,rows):
 with path.open("w",newline="",encoding="utf-8") as h:
  w=csv.DictWriter(h,fieldnames=fields,lineterminator="\n"); w.writeheader(); w.writerows(rows)
op=repo/"schools"/a.school/"opponents.csv"
fields,rows=read(op)
for row in rows:
 if row["canonical_opponent_key"] in keys:
  row["canonical_opponent_name"]=row["canonical_opponent_key"]+" authority"
write(op,fields,rows)
src=repo/"schools"/a.school/"source-games.csv"
fields,rows=read(src)
for row in rows:
 if row["normalized_opponent_key"] in keys:
  row["normalized_opponent_name"]=row["normalized_opponent_key"]+" authority"
  if mode=="bad-source":
   row["raw_text"]="MUTATED RAW EVIDENCE"
write(src,fields,rows)
'''
        (tools / "normalize_historical_opponent_displays.py").write_text(
            normalizer,
            encoding="utf-8",
        )

        snapshot = build_source_game_semantic_snapshot(
            repo / "schools" / SCHOOL / "source-games.csv"
        )
        semantic = semantic_snapshot_sha256(snapshot)
        freeze = {
            "status": "INTEGRATION_FROZEN",
            "school_key": SCHOOL,
            "integration_base_sha": "1" * 40,
            "origin_main_sha": "1" * 40,
            "source_game_semantic_guard": {
                "snapshot": snapshot,
                "snapshot_sha256": semantic,
            },
        }
        freeze_bytes = (
            json.dumps(freeze, indent=2, sort_keys=True) + "\n"
        ).encode()

        self.git(repo, "add", ".")
        self.git(repo, "commit", "-m", "fixture")
        predecessor = self.git(repo, "rev-parse", "HEAD")
        self.git(repo, "branch", "-m", "remote-fixture")
        return repo, predecessor, freeze_bytes

    def test_dry_run_is_exact_and_has_no_tracked_mutation(self):
        repo, predecessor, freeze = self.make_repo()
        before = self.git(repo, "status", "--porcelain", "--untracked-files=all")
        result = run_normalizer_dry_run(
            repo,
            SCHOOL,
            freeze,
            KEYS,
            repo.parent / "diag-dry",
        )
        after = self.git(repo, "status", "--porcelain", "--untracked-files=all")
        self.assertEqual(before, after)
        self.assertEqual(result["report"]["status"], "PASS")
        self.assertEqual(
            sorted(x["canonical_opponent_key"] for x in result["report"]["changes"]),
            KEYS,
        )
        self.assertEqual(self.git(repo, "rev-parse", "HEAD"), predecessor)

    def test_dry_run_refuses_broader_key_population(self):
        repo, _, freeze = self.make_repo()
        (repo / "keys.json").write_text(
            json.dumps(KEYS + ["gamma-institute"]) + "\n",
            encoding="utf-8",
        )
        self.git(repo, "add", "keys.json")
        self.git(repo, "commit", "-m", "broader plan")
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "KEY_POPULATION_MISMATCH",
        ):
            run_normalizer_dry_run(
                repo,
                SCHOOL,
                freeze,
                KEYS,
                repo.parent / "diag-broader",
            )

    def test_ambiguous_authority_is_refused_without_mutation(self):
        repo, predecessor, freeze = self.make_repo(mode="ambiguous")
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "DRY_RUN_FAILED",
        ):
            run_normalizer_dry_run(
                repo,
                SCHOOL,
                freeze,
                KEYS,
                repo.parent / "diag-ambiguous",
            )
        self.assertEqual(self.git(repo, "rev-parse", "HEAD"), predecessor)
        self.assertEqual(
            self.git(repo, "status", "--porcelain", "--untracked-files=all"),
            "",
        )

    def test_apply_changes_only_allowed_display_fields(self):
        repo, predecessor, freeze = self.make_repo()
        dry = run_normalizer_dry_run(
            repo, SCHOOL, freeze, KEYS, repo.parent / "diag-apply"
        )
        result = apply_and_prepare_repair(
            repo,
            SCHOOL,
            predecessor,
            freeze,
            dry,
            KEYS,
            repo.parent / "diag-apply",
        )
        self.assertEqual(result["prepared_parent_sha"], predecessor)
        self.assertEqual(
            set(result["changed_paths"]),
            {
                "schools/example-school/opponents.csv",
                "schools/example-school/source-games.csv",
            },
        )
        proof = result["field_level_proof"]
        self.assertEqual(proof["opponent_changed_keys"], KEYS)
        self.assertEqual(proof["opponent_key_changes"], 0)
        self.assertEqual(proof["source_game_non_name_field_changes"], 0)
        self.assertEqual(proof["literal_evidence_changes"], 0)
        self.assertEqual(proof["source_game_normalized_name_row_count"], 2)
        self.assertEqual(result["semantic_drift_after"]["status"], "PASS")

    def test_apply_rejects_literal_evidence_mutation(self):
        repo, predecessor, freeze = self.make_repo(mode="bad-source")
        dry = run_normalizer_dry_run(
            repo, SCHOOL, freeze, KEYS, repo.parent / "diag-bad"
        )
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "SOURCE_FIELD_CHANGED",
        ):
            apply_and_prepare_repair(
                repo,
                SCHOOL,
                predecessor,
                freeze,
                dry,
                KEYS,
                repo.parent / "diag-bad",
            )

    def test_field_proof_rejects_opponent_key_change(self):
        before_opp = (
            "canonical_opponent_key,canonical_opponent_name\n"
            "alpha-academy,Old\n"
        ).encode()
        after_opp = (
            "canonical_opponent_key,canonical_opponent_name\n"
            "different-key,New\n"
        ).encode()
        source = (
            "source_game_id,normalized_opponent_key,normalized_opponent_name\n"
            "E-1,alpha-academy,Old\n"
        ).encode()
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "OPPONENT_KEY_CHANGED|KEY_POPULATION_MISMATCH",
        ):
            field_level_mutation_proof(
                school_key=SCHOOL,
                before_opponents=before_opp,
                after_opponents=after_opp,
                before_source_games=source,
                after_source_games=source,
                expected_blocker_keys=["alpha-academy"],
            )

    def make_authority_repo(self):
        repo, target_sha, freeze_bytes = self.make_repo()
        freeze_sha = hashlib.sha256(freeze_bytes).hexdigest()
        semantic = json.loads(freeze_bytes)["source_game_semantic_guard"][
            "snapshot_sha256"
        ]

        writeahead_path = (
            ".remote-implementation/writeahead/example-school/phase0/"
            "writeahead-manifest.json"
        )
        freeze_path = (
            Path(writeahead_path).parent / "integration-freeze.json"
        ).as_posix()
        (repo / freeze_path).parent.mkdir(parents=True, exist_ok=True)
        (repo / freeze_path).write_bytes(freeze_bytes)
        phase0_writeahead = {
            "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": semantic,
            "sidecars": {"integration-freeze.json": freeze_sha},
        }
        phase0_wa_bytes = (
            json.dumps(phase0_writeahead, indent=2, sort_keys=True) + "\n"
        ).encode()
        (repo / writeahead_path).write_bytes(phase0_wa_bytes)

        phase0_path = (
            ".remote-implementation/successors/example-school/phase0/"
            "successor-manifest.json"
        )
        phase0 = {
            "kind": "REMOTE_IMPLEMENTATION_SUCCESSOR",
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "actual_published_target_sha": target_sha,
            "prepared_commit_sha": target_sha,
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": semantic,
            "repository_validation": "PASS",
            "final_transaction_state": "COMPLETE",
            "writeahead_manifest_path": writeahead_path,
            "writeahead_manifest_sha256": hashlib.sha256(
                phase0_wa_bytes
            ).hexdigest(),
        }
        phase0_bytes = (
            json.dumps(phase0, indent=2, sort_keys=True) + "\n"
        ).encode()
        (repo / phase0_path).parent.mkdir(parents=True, exist_ok=True)
        (repo / phase0_path).write_bytes(phase0_bytes)

        checkpoint_dir = (
            repo
            / ".remote-implementation/checkpoints"
            / SCHOOL
            / "stage2-census"
        )
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        blockers = [
            "historical opponent display conflict: %s: ['old', 'authority']. "
            "Normalize the school opponent display to existing project authority before Gate 1."
            % key
            for key in KEYS
        ]
        status = {
            "status": "BLOCKED",
            "blockers": blockers,
            "preflight": {
                "blocker_count": len(KEYS),
                "warning_count": 0,
                "decision_count": 0,
            },
        }
        status_bytes = (
            json.dumps(status, indent=2, sort_keys=True) + "\n"
        ).encode()
        (checkpoint_dir / "implementation-stage2-status.json").write_bytes(
            status_bytes
        )
        manifest = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT",
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "target_sha": target_sha,
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": semantic,
            "stage2_status": "BLOCKED",
            "capability_census_status": "PREFLIGHT_BLOCKED",
            "preflight": {
                "blocker_count": len(KEYS),
                "warning_count": 0,
                "decision_count": 0,
            },
            "artifact_sha256": {
                "implementation-stage2-status.json": hashlib.sha256(
                    status_bytes
                ).hexdigest()
            },
            "phase0_successor_path": phase0_path,
            "phase0_successor_sha256": hashlib.sha256(
                phase0_bytes
            ).hexdigest(),
        }
        manifest_bytes = (
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        ).encode()
        manifest_path = (
            checkpoint_dir / "checkpoint-manifest.json"
        )
        manifest_path.write_bytes(manifest_bytes)
        self.git(repo, "add", ".remote-implementation")
        self.git(repo, "commit", "-m", "control authority")
        control_sha = self.git(repo, "rev-parse", "HEAD")
        request = {
            "school_key": SCHOOL,
            "target_branch": TARGET_BRANCH,
            "target_sha": target_sha,
            "stage2_census_checkpoint": {
                "path": manifest_path.relative_to(repo).as_posix(),
                "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
            },
            "integration_freeze_sha256": freeze_sha,
            "semantic_snapshot_sha256": semantic,
        }
        return repo, control_sha, request

    def test_census_and_freeze_authority_is_authenticated(self):
        repo, control_sha, request = self.make_authority_repo()
        authority = verify_census_and_freeze_authority(
            request,
            control_sha,
            source_repo=repo,
        )
        self.assertEqual(authority["blocker_keys"], KEYS)
        self.assertEqual(
            hashlib.sha256(authority["freeze_bytes"]).hexdigest(),
            request["integration_freeze_sha256"],
        )

    def test_census_with_unrelated_blocker_is_refused(self):
        repo, control_sha, request = self.make_authority_repo()
        status_path = (
            repo
            / ".remote-implementation/checkpoints"
            / SCHOOL
            / "stage2-census"
            / "implementation-stage2-status.json"
        )
        status = json.loads(status_path.read_text())
        status["blockers"].append("unrelated blocker")
        status["preflight"]["blocker_count"] += 1
        status_path.write_text(
            json.dumps(status, indent=2, sort_keys=True) + "\n"
        )
        manifest_path = status_path.parent / "checkpoint-manifest.json"
        manifest = json.loads(manifest_path.read_text())
        status_bytes = status_path.read_bytes()
        manifest["preflight"]["blocker_count"] += 1
        manifest["artifact_sha256"][
            "implementation-stage2-status.json"
        ] = hashlib.sha256(status_bytes).hexdigest()
        manifest_path.write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n"
        )
        self.git(repo, "add", ".remote-implementation")
        self.git(repo, "commit", "-m", "unrelated blocker")
        bad_control = self.git(repo, "rev-parse", "HEAD")
        request["stage2_census_checkpoint"]["sha256"] = hashlib.sha256(
            manifest_path.read_bytes()
        ).hexdigest()
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "OTHER_BLOCKER",
        ):
            verify_census_and_freeze_authority(
                request,
                bad_control,
                source_repo=repo,
            )


if __name__ == "__main__":
    unittest.main()
