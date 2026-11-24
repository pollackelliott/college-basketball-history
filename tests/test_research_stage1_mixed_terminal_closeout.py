import csv
import hashlib
import importlib.util
import io
import json
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "mixed_terminal",
    ROOT / "tools" / "research_stage1_mixed_terminal_closeout.py",
)
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


def j(value):
    return (json.dumps(value, sort_keys=True) + "\n").encode()


def csv_bytes(rows):
    out = io.StringIO(newline="")
    writer = csv.DictWriter(out, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return out.getvalue().encode()


def write_candidate(path: Path, documents: dict[str, bytes]) -> str:
    manifest = {
        "schema_version": 1,
        "school_key": "test-school",
        "stage": "STAGE_1",
        "status": "BLOCKED_SHARED_AUTHORITY_AND_MIXED_TERMINAL_CLOSEOUT",
        "research_base_sha": "a" * 40,
        "parent_checkpoint_sha256": "b" * 64,
        "game_rows": 3,
        "blocking_residuals": 2,
        "members": {
            name: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            for name, data in documents.items()
        },
    }
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, data in sorted(documents.items()):
            archive.writestr("checkpoint/" + name, data)
        archive.writestr("checkpoint/stage1-manifest.json", j(manifest))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def base_docs():
    ledger = [
        {
            "research_game_id": "G-U",
            "school_key": "test-school",
            "season_label": "1922-23",
            "opponent_literal": "National Guard",
            "game_type": "REGULAR_SEASON",
            "played_result": "",
            "team_score": "",
            "opponent_score": "",
            "game_universe_state": "IDENTIFIED_COMPETITIVE",
        },
        {
            "research_game_id": "G-A1",
            "school_key": "test-school",
            "season_label": "1924-25",
            "opponent_literal": "Opponent One",
            "game_type": "REGULAR_SEASON",
            "played_result": "W",
            "team_score": "20",
            "opponent_score": "10",
            "game_universe_state": "IDENTIFIED_COMPETITIVE",
        },
        {
            "research_game_id": "G-A2",
            "school_key": "test-school",
            "season_label": "1924-25",
            "opponent_literal": "Opponent Two",
            "game_type": "REGULAR_SEASON",
            "played_result": "L",
            "team_score": "10",
            "opponent_score": "20",
            "game_universe_state": "IDENTIFIED_COMPETITIVE",
        },
    ]
    census = [
        {
            "season": "1922-23",
            "source_all_time_record_wins": "0",
            "source_all_time_record_losses": "1",
            "source_all_time_record_games": "1",
            "identified_competitive_games": "1",
            "identified_wins": "0",
            "identified_losses": "0",
        },
        {
            "season": "1924-25",
            "source_all_time_record_wins": "1",
            "source_all_time_record_losses": "2",
            "source_all_time_record_games": "3",
            "identified_competitive_games": "2",
            "identified_wins": "1",
            "identified_losses": "1",
        },
    ]
    blockers = [
        {
            "blocker_id": "UNKNOWN-1",
            "class": mod.UNKNOWN_RESULT_BLOCKER,
            "season": "1922-23",
            "research_game_id": "G-U",
            "research_state": "RESEARCHED_UNRESOLVED",
            "research_evidence_summary": "Two institutional sources preserve the blank result.",
            "terminal_classification": mod.UNKNOWN_RESULT_TERMINAL,
        },
        {
            "blocker_id": "AGG-1",
            "class": mod.AGG_BLOCKER,
            "season": "1924-25",
            "research_state": "RESEARCH_EXHAUSTED_SOURCE_COVERAGE",
            "research_evidence_summary": "Institutional aggregate exceeds identified ledger by one loss.",
            "terminal_classification": mod.AGG_TERMINAL,
            "detail": {"identified_game_rows": 2, "unidentified_game_rows": 1},
        },
    ]
    status = {
        "schema_version": 1,
        "school": "test-school",
        "school_key": "test-school",
        "stage": "STAGE_1",
        "stage1_complete": False,
        "status": "BLOCKED_SHARED_AUTHORITY_AND_MIXED_TERMINAL_CLOSEOUT",
        "research_base_sha": "a" * 40,
        "parent_checkpoint_sha256": "b" * 64,
        "blocking_residual_count": 2,
        "total_candidate_game_rows": 3,
        "identified_competitive_games": 3,
    }
    authority = {
        "identified_ledger_sha256": hashlib.sha256(csv_bytes(ledger)).hexdigest(),
        "identified_record": {"games": 2, "losses": 1, "wins": 1},
        "identified_rows": 3,
        "institutional_record": {"games": 3, "losses": 2, "wins": 1},
        "maximum_eligible_season_start_year": 1930,
        "notes": "Owner-approved aggregate debt; no anonymous game.",
        "owner_disposition": "https://github.com/example/repo/issues/1",
        "parent_checkpoint_sha256": "b" * 64,
        "research_base_sha": "a" * 40,
        "school_key": "test-school",
        "season": "1924-25",
        "unidentified_record": {"games": 1, "losses": 1, "wins": 0},
    }
    uncertainty = {
        "schema_version": 1,
        "school_key": "test-school",
        "research_base_sha": "a" * 40,
        "parent_checkpoint_sha256": "b" * 64,
        "identified_game_count": 3,
        "known_result_game_count": 2,
        "known_result_wins": 1,
        "known_result_losses": 1,
        "known_result_ties": 0,
        "class_a": [],
        "class_b": [
            {
                "research_game_id": "G-U",
                "season": "1922-23",
                "opponent_literal": "National Guard",
                "game_type": "REGULAR_SEASON",
                "competitive_inclusion": True,
                "direct_score_or_result_evidence_present": False,
                "aggregate_result_allocation_used": False,
                "research_exhausted": True,
                "systematic_evidence_checked": [
                    {"source": "Institutional source A", "authority": "target institutional primary", "finding": "Result blank."},
                    {"source": "Institutional source B", "authority": "target institutional repeated source family", "finding": "Result still blank."},
                ],
            }
        ],
    }
    evidence = {
        "schema_version": 1,
        "school_key": "test-school",
        "season": "1924-25",
        "policy_result": "RESEARCH_EXHAUSTED_IDENTITIES_UNRESOLVED",
        "identified_game_rows": 2,
        "unidentified_game_rows": 1,
        "accepted_game_rows_before": 3,
        "accepted_game_rows_after": 3,
        "rows_added": 0,
        "anonymous_placeholder_rows": 0,
        "rows_added_from_aggregate_inference": 0,
        "institutional_record": {"games": 3, "losses": 2, "wins": 1},
        "systematic_evidence_checked": [
            {"source": "Institutional source A", "authority": "target institutional primary", "finding": "3-game aggregate, 2 listed."},
            {"source": "Institutional source B", "authority": "target institutional repeated source family", "finding": "Same mismatch."},
            {"source": "Institutional archive", "authority": "target institutional archival", "finding": "No third identity recovered."},
        ],
    }
    docs = {
        "structured-stage1-ledger.csv": csv_bytes(ledger),
        "season-census.csv": csv_bytes(census),
        "blocking-residuals.json": j(blockers),
        "stage1-status.json": j(status),
        mod.AGG_PROPOSAL: j(authority),
        mod.UNCERTAINTY_PROPOSAL: j(uncertainty),
        mod.AGG_EVIDENCE: j(evidence),
        "literal-evidence.txt": b"preserve me byte-for-byte\n",
    }
    return docs, authority


def make_fixture(root: Path, mutate_docs=None, mutate_authority=None):
    docs, authority = base_docs()
    if mutate_docs:
        mutate_docs(docs)
    if mutate_authority:
        mutate_authority(authority)
        docs[mod.AGG_PROPOSAL] = j(authority)
    candidate = root / "candidate.zip"
    candidate_sha = write_candidate(candidate, docs)
    registry = root / "registry.json"
    registry.write_bytes(j({
        "schema_version": 1,
        "authority_type": "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE",
        "cases": [authority],
    }))
    return candidate, candidate_sha, registry, docs


def test_mixed_aggregate_plus_unknown_result_closes_and_verifies_without_core_drift():
    with tempfile.TemporaryDirectory() as name:
        root = Path(name)
        candidate, candidate_sha, registry, docs = make_fixture(root)
        audit = mod.audit_candidate(candidate, expected_candidate_sha256=candidate_sha, registry_path=registry)
        assert audit["status"] == mod.ELIGIBLE
        assert audit["defects"] == []
        assert audit["terminal_classifications"] == [mod.AGG_TERMINAL, mod.UNKNOWN_RESULT_TERMINAL]

        audit_path = root / "audit.json"
        audit_path.write_bytes(mod.json_bytes(audit))
        audit_sha = hashlib.sha256(audit_path.read_bytes()).hexdigest()
        closeout = root / "closeout.zip"
        created = mod.closeout(candidate, audit_path, closeout, candidate_sha=candidate_sha, audit_sha=audit_sha, registry_path=registry)
        assert created["stage1_complete"] is False
        closeout_sha = hashlib.sha256(closeout.read_bytes()).hexdigest()
        verified = mod.verify_closeout(candidate, closeout, audit_path, candidate_sha=candidate_sha, successor_sha=closeout_sha, audit_sha=audit_sha, registry_path=registry)
        assert verified["status"] == mod.VERIFIED
        assert verified["defects"] == []
        assert verified["stage1_complete"] is True

        members, _ = mod.read_zip(closeout, closeout_sha)
        assert members["structured-stage1-ledger.csv"] == docs["structured-stage1-ledger.csv"]
        assert members["season-census.csv"] == docs["season-census.csv"]
        assert members["literal-evidence.txt"] == docs["literal-evidence.txt"]
        assert json.loads(members["blocking-residuals.json"]) == []
        assert json.loads(members["stage1-status.json"])["stage1_complete"] is True


def test_unknown_result_cannot_be_allocated_from_aggregate():
    def mutate(docs):
        value = json.loads(docs[mod.UNCERTAINTY_PROPOSAL])
        value["class_b"][0]["aggregate_result_allocation_used"] = True
        docs[mod.UNCERTAINTY_PROPOSAL] = j(value)

    with tempfile.TemporaryDirectory() as name:
        candidate, candidate_sha, registry, _ = make_fixture(Path(name), mutate_docs=mutate)
        result = mod.audit_candidate(candidate, expected_candidate_sha256=candidate_sha, registry_path=registry)
        assert "CLASS_B_AGGREGATE_ALLOCATION_NOT_EXCLUDED:G-U" in result["defects"]


def test_unrelated_third_blocker_is_rejected():
    def mutate(docs):
        blockers = json.loads(docs["blocking-residuals.json"])
        blockers.append({"class": "DUPLICATE_GAME_ID_UNRESOLVED", "season": "1930-31"})
        docs["blocking-residuals.json"] = j(blockers)
        status = json.loads(docs["stage1-status.json"])
        status["blocking_residual_count"] = 3
        docs["stage1-status.json"] = j(status)

    with tempfile.TemporaryDirectory() as name:
        root = Path(name)
        docs, authority = base_docs()
        mutate(docs)
        candidate = root / "candidate.zip"
        # The manifest must truthfully advertise all three blockers.
        with zipfile.ZipFile(candidate, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for member, data in sorted(docs.items()):
                archive.writestr("checkpoint/" + member, data)
            manifest = {
                "schema_version": 1,
                "school_key": "test-school",
                "stage": "STAGE_1",
                "status": "BLOCKED_SHARED_AUTHORITY_AND_MIXED_TERMINAL_CLOSEOUT",
                "research_base_sha": "a" * 40,
                "parent_checkpoint_sha256": "b" * 64,
                "game_rows": 3,
                "blocking_residuals": 3,
                "members": {member: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()} for member, data in docs.items()},
            }
            archive.writestr("checkpoint/stage1-manifest.json", j(manifest))
        candidate_sha = hashlib.sha256(candidate.read_bytes()).hexdigest()
        registry = root / "registry.json"
        registry.write_bytes(j({"schema_version": 1, "authority_type": "OWNER_APPROVED_EARLY_AGGREGATE_COVERAGE", "cases": [authority]}))
        result = mod.audit_candidate(candidate, expected_candidate_sha256=candidate_sha, registry_path=registry)
        assert "UNRELATED_STAGE1_BLOCKERS" in result["defects"]


def test_registry_binding_must_match_candidate_authority_parent():
    def mutate(authority):
        authority["parent_checkpoint_sha256"] = "c" * 64

    with tempfile.TemporaryDirectory() as name:
        candidate, candidate_sha, registry, _ = make_fixture(Path(name), mutate_authority=mutate)
        result = mod.audit_candidate(candidate, expected_candidate_sha256=candidate_sha, registry_path=registry)
        assert "OWNER_AUTHORITY_BINDING_MISMATCH:1924-25" in result["defects"]


def test_verify_closeout_rejects_ledger_drift():
    with tempfile.TemporaryDirectory() as name:
        root = Path(name)
        candidate, candidate_sha, registry, _ = make_fixture(root)
        audit = mod.audit_candidate(candidate, expected_candidate_sha256=candidate_sha, registry_path=registry)
        audit_path = root / "audit.json"
        audit_path.write_bytes(mod.json_bytes(audit))
        audit_sha = hashlib.sha256(audit_path.read_bytes()).hexdigest()
        closeout = root / "closeout.zip"
        mod.closeout(candidate, audit_path, closeout, candidate_sha=candidate_sha, audit_sha=audit_sha, registry_path=registry)
        closeout_sha = hashlib.sha256(closeout.read_bytes()).hexdigest()
        members, _ = mod.read_zip(closeout, closeout_sha)
        rows = list(csv.DictReader(io.StringIO(members["structured-stage1-ledger.csv"].decode())))
        rows[0]["opponent_literal"] = "Changed"
        members["structured-stage1-ledger.csv"] = csv_bytes(rows)
        manifest = json.loads(members["stage1-manifest.json"])
        manifest["members"] = {
            member: {"size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
            for member, data in sorted(members.items())
            if member != "stage1-manifest.json"
        }
        members["stage1-manifest.json"] = mod.json_bytes(manifest)
        drifted = root / "drifted.zip"
        drifted_sha = mod.serialize_zip(members, drifted)
        result = mod.verify_closeout(candidate, drifted, audit_path, candidate_sha=candidate_sha, successor_sha=drifted_sha, audit_sha=audit_sha, registry_path=registry)
        assert "HISTORICAL_CORE_DRIFT:structured-stage1-ledger.csv" in result["defects"]
