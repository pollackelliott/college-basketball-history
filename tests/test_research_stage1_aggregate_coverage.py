"""The approved early-aggregate exception never manufactures games or bypasses other blockers."""
import csv
import hashlib
import io
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import research_stage1_aggregate_coverage as mod


def jb(x):
    return mod.json_bytes(x)


def rows_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode()


class AggregateCoverageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.parent = self.root / "parent.zip"
        self.audit_file = self.root / "audit.json"
        self.closeout_file = self.root / "closeout.zip"
        self.registry = self.root / "authorities.json"
        rows = [
            {"research_game_id": "A", "season_label": "1919-20", "opponent_literal": "Alumni",
             "game_type": "REGULAR_SEASON", "game_universe_state": "ACCEPTED",
             "game_inclusion": "INCLUDED", "played_result": "W"},
            {"research_game_id": "B", "season_label": "1919-20", "opponent_literal": "Seton Hall",
             "game_type": "REGULAR_SEASON", "game_universe_state": "ACCEPTED",
             "game_inclusion": "INCLUDED", "played_result": "L"},
            {"research_game_id": "C", "season_label": "1920-21", "opponent_literal": "Canisius",
             "game_type": "REGULAR_SEASON", "game_universe_state": "ACCEPTED",
             "game_inclusion": "INCLUDED", "played_result": "W"},
        ]
        evidence = {
            "school_key": "example", "season": "1919-20", "research_base_sha": "a" * 40,
            "policy_result": "RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED",
            "rows_added": 0, "accepted_game_rows_before": 3, "accepted_game_rows_after": 3,
            "anonymous_placeholder_rows": 0, "rows_added_from_aggregate_inference": 0,
            "institutional_record": {"wins": 2, "losses": 2, "games": 4},
            "identified_game_rows": 2, "unidentified_game_rows": 2,
            "systematic_evidence_checked": [
                {"source": "Example institutional record book", "authority": "target institutional",
                 "finding": "Season was 2-2, but individual results incomplete"},
                {"source": "Official archive", "authority": "target institutional archive",
                 "finding": "No accessible 1919 pages"},
                {"source": "Opponent results", "authority": "reciprocal institutional",
                 "finding": "No new games"},
            ],
        }
        residual = [{
            "blocker_id": "BLOCK-1", "season": "1919-20",
            "class": "FOUNDING_SEASON_PARTIAL_ROW_IDENTIFICATION",
            "research_state": "RESEARCH_EXHAUSTED_SOURCE_COVERAGE",
            "detail": {"identified_game_rows": 2, "unidentified_game_rows": 2},
            "research_evidence_summary": "Archives and reciprocal records exhausted.",
        }]
        status = {
            "school_key": "example", "status": "RESEARCH_BLOCKED_SOURCE_COVERAGE",
            "stage1_complete": False, "research_base_sha": "a" * 40,
            "total_candidate_game_rows": 3, "blocking_residual_count": 1
        }
        census = [
            {"season_label": "1919-20", "source_aggregate_wins": "2",
             "source_aggregate_losses": "2", "source_aggregate_games": "4",
             "accepted_or_identified_rows": "2", "known_played_wins": "1",
             "known_played_losses": "1"},
            {"season_label": "1920-21", "source_aggregate_wins": "1",
             "source_aggregate_losses": "0", "source_aggregate_games": "1",
             "accepted_or_identified_rows": "1", "known_played_wins": "1",
             "known_played_losses": "0"},
        ]
        self.members = {
            "structured-stage1-ledger.csv": rows_bytes(rows),
            "season-census.csv": rows_bytes(census),
            "blocking-residuals.json": jb(residual),
            "stage1-status.json": jb(status),
            mod.SOURCE_MEMBER: jb(evidence),
            "research-log.md": b"Preserved literal notes",
        }
        self.write_parent()
        self.write_authority()

    def write_parent(self):
        members = self.members.copy()
        members["stage1-manifest.json"] = jb({
            "game_rows": 3, "research_base_sha": "a" * 40, "blocking_residuals": 1,
            "members": {name: {"size": len(data), "sha256": mod.digest(data)}
                        for name, data in members.items()}
        })
        mod.serialize_zip(members, self.parent)
        self.parent_sha = mod.digest(self.parent.read_bytes())

    def write_authority(self):
        self.registry.write_bytes(jb({
            "schema_version": 1, "authority_type": "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE",
            "cases": [{
                "school_key": "example", "season": "1919-20",
                "parent_checkpoint_sha256": self.parent_sha, "research_base_sha": "a" * 40,
                "owner_disposition": "https://github.com/example/history/issues/1",
                "institutional_record": {"wins": 2, "losses": 2, "games": 4},
                "identified_record": {"wins": 1, "losses": 1, "games": 2},
                "unidentified_record": {"wins": 1, "losses": 1, "games": 2},
                "maximum_eligible_season_start_year": 1930,
            }]
        }))

    def audit(self):
        return mod.audit_checkpoint(self.parent,
                                    expected_parent_sha256=self.parent_sha,
                                    registry=self.registry)

    def mutate(self, name, fn):
        content = json.loads(self.members[name]) if name.endswith(".json") else None
        fn(content)
        self.members[name] = jb(content)
        self.write_parent()
        self.write_authority()

    def test_valid_aggregate_gap_requires_exact_owner_authority(self):
        report = self.audit()
        self.assertEqual(report["status"], mod.ELIGIBLE, report["defects"])
        self.assertEqual(report["season_coverage"]["unidentified_record"],
                         {"wins": 1, "losses": 1, "games": 2})
        self.assertFalse(report["stage1_complete"])

    def test_parent_hash_mismatch_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "CHECKPOINT_HASH_MISMATCH"):
            mod.audit_checkpoint(self.parent, expected_parent_sha256="0" * 64,
                                 registry=self.registry)

    def test_no_owner_authority_fails(self):
        registry = json.loads(self.registry.read_bytes())
        registry["cases"] = []
        self.registry.write_bytes(jb(registry))
        self.assertIn("NO_EXACT_OWNER_AUTHORITY", self.audit()["defects"])

    def test_second_blocker_fails(self):
        self.mutate("blocking-residuals.json",
                    lambda x: x.append({**x[0], "blocker_id": "BLOCK-2"}))
        self.assertIn("OTHER_STAGE1_BLOCKERS", self.audit()["defects"])

    def test_source_aggregate_drift_fails(self):
        self.mutate(mod.SOURCE_MEMBER,
                    lambda x: x["institutional_record"].update({"wins": 3}))
        self.assertIn("INSTITUTIONAL_RECORD_AUTHORITY_MISMATCH", self.audit()["defects"])

    def test_research_not_exhausted_fails(self):
        self.mutate(mod.SOURCE_MEMBER,
                    lambda x: x.update({"policy_result": "STILL_SEARCHING"}))
        self.assertIn("EVIDENCE_EXHAUSTION_INCONSISTENT", self.audit()["defects"])

    def test_founding_era_limit_fails(self):
        registry = json.loads(self.registry.read_bytes())
        registry["cases"][0]["maximum_eligible_season_start_year"] = 1900
        self.registry.write_bytes(jb(registry))
        self.assertIn("OUTSIDE_FOUNDING_ERA", self.audit()["defects"])

    def test_no_fictional_game_rows_or_result_allocations(self):
        report = self.audit()
        self.audit_file.write_bytes(jb(report))
        audit_sha = mod.digest(self.audit_file.read_bytes())
        created = mod.closeout(self.parent, self.audit_file, self.closeout_file,
                               parent_sha=self.parent_sha, audit_sha=audit_sha,
                               registry=self.registry)
        self.assertEqual(created["status"], "STAGE1_CLOSEOUT_CANDIDATE_CREATED")
        closeout_sha = mod.digest(self.closeout_file.read_bytes())
        verify = mod.verify_closeout(self.parent, self.closeout_file, self.audit_file,
                                     parent_sha=self.parent_sha, successor_sha=closeout_sha,
                                     audit_sha=audit_sha, registry=self.registry)
        self.assertEqual(verify["status"], mod.VERIFIED, verify["defects"])
        p, _ = mod.read_zip(self.parent, self.parent_sha)
        s, _ = mod.read_zip(self.closeout_file, closeout_sha)
        self.assertEqual(p["structured-stage1-ledger.csv"], s["structured-stage1-ledger.csv"])
        self.assertEqual(p["season-census.csv"], s["season-census.csv"])
        self.assertEqual(json.loads(s["blocking-residuals.json"]), [])
        self.assertEqual(json.loads(s[mod.AUTHORING_MEMBER])["coverage"][0]
                         ["terminal_classification"], mod.TERMINAL)

    def test_tampered_successor_cannot_verify(self):
        report = self.audit()
        self.audit_file.write_bytes(jb(report))
        audit_sha = mod.digest(self.audit_file.read_bytes())
        mod.closeout(self.parent, self.audit_file, self.closeout_file,
                     parent_sha=self.parent_sha, audit_sha=audit_sha,
                     registry=self.registry)
        members, _ = mod.read_zip(self.closeout_file,
                                  mod.digest(self.closeout_file.read_bytes()))
        members["research-log.md"] = b"changed source evidence"
        manifest = json.loads(members["stage1-manifest.json"])
        manifest["members"]["research-log.md"] = {
            "size": len(members["research-log.md"]),
            "sha256": mod.digest(members["research-log.md"]),
        }
        members["stage1-manifest.json"] = jb(manifest)
        sha = mod.serialize_zip(members, self.closeout_file)
        verify = mod.verify_closeout(self.parent, self.closeout_file, self.audit_file,
                                     parent_sha=self.parent_sha, successor_sha=sha,
                                     audit_sha=audit_sha, registry=self.registry)
        self.assertIn("CLOSEOUT_CONTENT_OR_HISTORICAL_LEDGER_DRIFT", verify["defects"])


if __name__ == "__main__":
    unittest.main()
