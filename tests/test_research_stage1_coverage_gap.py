"""The exception is source-count scoped; known-game history must remain untouched."""
import csv
import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path

import research_stage1_coverage_gap as mod


def csv_bytes(rows):
    data = io.StringIO(newline="")
    writer = csv.DictWriter(data, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return data.getvalue().encode()


def make_checkpoint(directory, mutate=None):
    ledger = [
        dict(research_game_id="G1", season_label="1916-1917", opponent_literal="Dartmouth",
             game_type="REGULAR_SEASON", game_universe_state="CANDIDATE_SOURCE_LISTED"),
        dict(research_game_id="G2", season_label="1916-1917", opponent_literal="Georgetown",
             game_type="REGULAR_SEASON", game_universe_state="CANDIDATE_SOURCE_LISTED"),
        dict(research_game_id="G3", season_label="1930-1931", opponent_literal="Fordham",
             game_type="REGULAR_SEASON", game_universe_state="CANDIDATE_SOURCE_LISTED"),
    ]
    census = [
        {"season": "1916-1917", "observed_games": "2", "expected_games": "2", "state": "MATCH"},
        {"season": "1930-1931", "observed_games": "1", "expected_games": "3", "state": "MISMATCH"},
    ]
    evidence = {
        "policy_result": "RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED",
        "rows_added": 0, "accepted_game_rows_before": 3, "accepted_game_rows_after": 3,
        "unknown_real_games_represented_by_blockers": 3,
        "seasons": [
            {
                "season": "1916-1917",
                "primary_source_state": {
                    "heading": "1916-17 (2-0)", "listed_game_rows": 2,
                    "listed_result_tally": "2-0", "explicit_note": "(one game missing)",
                },
                "systematic_evidence_checked": [
                    {"source": "official archives", "authority": "institutional",
                     "finding": "no document survives"},
                    {"source": "reciprocal institutional records", "authority": "institutional",
                     "finding": "no additional game identified"},
                ],
                "disposition": "BLOCKING_RESEARCHED_UNRESOLVED",
                "reason": "identity not established",
            },
            {
                "season": "1930-1931",
                "primary_source_state": {
                    "heading": "1930-31 (3-0)", "listed_game_rows": 1,
                    "listed_result_tally": "1-0", "explicit_note": "(two games missing)",
                },
                "systematic_evidence_checked": [
                    {"source": "official yearbook", "authority": "institutional",
                     "finding": "no identity found"},
                    {"source": "official newspapers", "authority": "institutional",
                     "finding": "no identity found"},
                ],
                "disposition": "BLOCKING_RESEARCHED_UNRESOLVED",
                "reason": "identities not established",
            },
        ],
    }
    blockers = [
        {"class": "SOURCE_EXPLICIT_GAME_MISSING", "season": "1916-1917",
         "source_note": {"text": "(one game missing)", "page": 104},
         "research_state": "RESEARCHED_UNRESOLVED",
         "research_evidence_summary": "systematic archival search exhausted"},
        {"class": "SEASON_OUTCOME_CENSUS_MISMATCH", "season": "1930-1931",
         "detail": {"expected_games": 3, "observed_games": 1},
         "research_state": "RESEARCHED_UNRESOLVED",
         "research_evidence_summary": "systematic archival search exhausted"},
    ]
    status = {
        "school": "sample", "research_base_sha": "a"*40,
        "total_candidate_game_rows": 3, "blocking_residual_count": 2,
        "remaining_unknown_real_games": 3,
    }
    documents = {
        "structured-stage1-ledger.csv": csv_bytes(ledger),
        "season-census.csv": csv_bytes(census),
        "blocking-residuals.json": json.dumps(blockers).encode(),
        "stage1-status.json": json.dumps(status).encode(),
        "missing-game-evidence.json": json.dumps(evidence).encode(),
    }
    if mutate:
        mutate(documents)
    status_obj = json.loads(documents["stage1-status.json"])
    evidence_obj = json.loads(documents["missing-game-evidence.json"])
    manifest = {
        "research_base_sha": "a"*40,
        "game_rows": status_obj["total_candidate_game_rows"],
        "blocking_residuals": status_obj["blocking_residual_count"],
        "unknown_real_games": evidence_obj["unknown_real_games_represented_by_blockers"],
        "members": {n: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                    for n, data in documents.items()},
    }
    path = directory / "checkpoint.zip"
    with zipfile.ZipFile(path, "w") as z:
        for name, data in documents.items():
            z.writestr("checkpoint/" + name, data)
        z.writestr("checkpoint/stage1-manifest.json", json.dumps(manifest))
    return path, hashlib.sha256(path.read_bytes()).hexdigest()


class Stage1SourceAcknowledgedGapTests(unittest.TestCase):
    def audit(self, mutate=None):
        with tempfile.TemporaryDirectory() as name:
            path, digest = make_checkpoint(Path(name), mutate)
            return mod.audit_checkpoint(path, evidence_member="missing-game-evidence.json",
                                        expected_sha256=digest)

    def test_eligible_but_never_stage1_complete(self):
        result = self.audit()
        self.assertEqual(result["status"], "ELIGIBLE_FOR_SOURCE_ACKNOWLEDGED_COVERAGE_GAP")
        self.assertEqual(result["defects"], [])
        self.assertEqual(result["identified_competitive_games"], 3)
        self.assertEqual(result["unidentified_games_not_added"], 3)
        self.assertFalse(result["stage1_complete"])

    def test_outcome_specific_missing_counts_pass_full_audit(self):
        def mutation(doc):
            evidence = json.loads(doc["missing-game-evidence.json"])
            evidence["seasons"][0]["primary_source_state"]["explicit_note"] = (
                "one win missing from archives"
            )
            evidence["seasons"][1]["primary_source_state"]["explicit_note"] = (
                "one win and one loss missing from archives"
            )
            doc["missing-game-evidence.json"] = json.dumps(evidence).encode()

            blockers = json.loads(doc["blocking-residuals.json"])
            blockers[0]["source_note"]["text"] = "one win missing from archives"
            doc["blocking-residuals.json"] = json.dumps(blockers).encode()

        result = self.audit(mutation)
        self.assertEqual(result["status"], "ELIGIBLE_FOR_SOURCE_ACKNOWLEDGED_COVERAGE_GAP")
        self.assertEqual(result["defects"], [])
        self.assertEqual(result["unidentified_games_not_added"], 3)
        self.assertEqual(
            [gap["institutional_missing_count"] for gap in result["source_coverage_gaps"]],
            [1, 2],
        )

    def test_missing_count_parser_handles_separate_outcome_clauses(self):
        self.assertEqual(
            mod._count_missing("one win missing from archives; one loss missing from archives"),
            2,
        )
        self.assertIsNone(mod._count_missing("record has ten wins and seven losses; archive incomplete"))

    def test_partial_source_gap_recovery_counts_only_remaining_unknown_games(self):
        def mutation(doc):
            rows = list(csv.DictReader(io.StringIO(
                doc["structured-stage1-ledger.csv"].decode())))
            rows.append(dict(
                research_game_id="G4", season_label="1930-1931",
                opponent_literal="Recovered Opponent", game_type="REGULAR_SEASON",
                game_universe_state="RESEARCH_RECOVERED",
            ))
            doc["structured-stage1-ledger.csv"] = csv_bytes(rows)

            census = list(csv.DictReader(io.StringIO(doc["season-census.csv"].decode())))
            census[1]["observed_games"] = "2"
            census[1]["expected_games"] = "3"
            doc["season-census.csv"] = csv_bytes(census)

            evidence = json.loads(doc["missing-game-evidence.json"])
            evidence["accepted_game_rows_before"] = 4
            evidence["accepted_game_rows_after"] = 4
            evidence["unknown_real_games_represented_by_blockers"] = 2
            evidence["seasons"][1]["primary_source_state"]["explicit_note"] = (
                "one win and one loss missing from archives"
            )
            doc["missing-game-evidence.json"] = json.dumps(evidence).encode()

            blockers = json.loads(doc["blocking-residuals.json"])
            blockers[1]["detail"] = {
                "expected_games": 3, "observed_games": 2,
                "unidentified_games": 1, "unidentified_wins": 1,
                "unidentified_losses": 0,
            }
            doc["blocking-residuals.json"] = json.dumps(blockers).encode()

            status = json.loads(doc["stage1-status.json"])
            status["total_candidate_game_rows"] = 4
            status["remaining_unknown_real_games"] = 2
            doc["stage1-status.json"] = json.dumps(status).encode()

        result = self.audit(mutation)
        self.assertEqual(result["status"], "ELIGIBLE_FOR_SOURCE_ACKNOWLEDGED_COVERAGE_GAP")
        self.assertEqual(result["defects"], [])
        self.assertEqual(result["identified_competitive_games"], 4)
        self.assertEqual(result["unidentified_games_not_added"], 2)
        recovered = next(
            gap for gap in result["source_coverage_gaps"]
            if gap["season"] == "1930-1931"
        )
        self.assertEqual(recovered["institutional_missing_count"], 2)
        self.assertEqual(recovered["identified_recovered_from_gap"], 1)
        self.assertEqual(recovered["remaining_unidentified_count"], 1)

    def test_partial_gap_count_without_identified_row_stays_blocking(self):
        def mutation(doc):
            evidence = json.loads(doc["missing-game-evidence.json"])
            evidence["unknown_real_games_represented_by_blockers"] = 2
            evidence["seasons"][1]["primary_source_state"]["explicit_note"] = (
                "one win and one loss missing from archives"
            )
            doc["missing-game-evidence.json"] = json.dumps(evidence).encode()

            blockers = json.loads(doc["blocking-residuals.json"])
            blockers[1]["detail"]["expected_games"] = 2
            blockers[1]["detail"]["unidentified_games"] = 1
            doc["blocking-residuals.json"] = json.dumps(blockers).encode()

            status = json.loads(doc["stage1-status.json"])
            status["remaining_unknown_real_games"] = 2
            doc["stage1-status.json"] = json.dumps(status).encode()

        result = self.audit(mutation)
        self.assertIn("SOURCE_LISTED_ROWS_MISMATCH:1930-1931", result["defects"])

    def test_missing_note_cannot_be_inferred_from_aggregate(self):
        def mutation(doc):
            obj = json.loads(doc["missing-game-evidence.json"])
            obj["seasons"][1]["primary_source_state"]["explicit_note"] = "record uncertain"
            doc["missing-game-evidence.json"] = json.dumps(obj).encode()
        self.assertIn("NO_EXPLICIT_INSTITUTIONAL_MISSING_COUNT:1930-1931",
                      self.audit(mutation)["defects"])

    def test_wrong_census_delta_stays_blocking(self):
        def mutation(doc):
            obj = json.loads(doc["blocking-residuals.json"])
            obj[1]["detail"]["expected_games"] = 2
            doc["blocking-residuals.json"] = json.dumps(obj).encode()
        self.assertIn("SEASON_GAME_DELTA_CONFLICT:1930-1931",
                      self.audit(mutation)["defects"])

    def test_other_game_identity_blocker_is_not_waived(self):
        def mutation(doc):
            obj = json.loads(doc["blocking-residuals.json"])
            obj[1]["class"] = "DUPLICATE_GAME_ID_UNRESOLVED"
            doc["blocking-residuals.json"] = json.dumps(obj).encode()
        self.assertIn("UNRELATED_BLOCKER:1930-1931",
                      self.audit(mutation)["defects"])

    def test_fabricated_placeholder_and_unknown_opponent_fail(self):
        def mutation(doc):
            rows = list(csv.DictReader(io.StringIO(
                doc["structured-stage1-ledger.csv"].decode())))
            rows[0]["game_universe_state"] = "UNIDENTIFIED_PLACEHOLDER"
            rows[0]["opponent_literal"] = ""
            doc["structured-stage1-ledger.csv"] = csv_bytes(rows)
        defects = self.audit(mutation)["defects"]
        self.assertIn("FABRICATED_UNIDENTIFIED_GAME_ROW", defects)
        self.assertIn("UNIDENTIFIED_OR_UNTYPED_LEDGER_GAME", defects)

    def test_exhausted_institutional_research_is_required(self):
        def mutation(doc):
            obj = json.loads(doc["missing-game-evidence.json"])
            obj["policy_result"] = "STILL_RESEARCHING"
            doc["missing-game-evidence.json"] = json.dumps(obj).encode()
        self.assertIn("RESEARCH_NOT_EXHAUSTED", self.audit(mutation)["defects"])

    def test_missing_game_count_separate_from_known_game_count(self):
        def mutation(doc):
            obj = json.loads(doc["stage1-status.json"])
            obj["remaining_unknown_real_games"] = 2
            doc["stage1-status.json"] = json.dumps(obj).encode()
        self.assertIn("UNIDENTIFIED_COUNT_MISMATCH:status",
                      self.audit(mutation)["defects"])

    def test_sha_pin_required(self):
        with tempfile.TemporaryDirectory() as name:
            path, digest = make_checkpoint(Path(name))
            result = mod.audit_checkpoint(path, evidence_member="missing-game-evidence.json",
                                          expected_sha256="0"*64)
            self.assertEqual(result["status"], "FAIL")
            self.assertIn("CHECKPOINT_HASH_MISMATCH_OR_UNPINNED", result["defects"])


if __name__ == "__main__":
    unittest.main()
