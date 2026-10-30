"""Regression coverage for terminal early-history Stage 1 uncertainty."""
import csv
import hashlib
import io
import json
import tempfile
import zipfile
from pathlib import Path

import research_stage1_early_history_uncertainty as mod


def csv_bytes(rows):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=list(rows[0]),
        lineterminator="\n",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode()


def base_docs():
    ledger = [
        {
            "research_game_id": "G1",
            "season_label": "1907-1908",
            "opponent_literal": "Charlotte YMCA",
            "game_type": "REGULAR_SEASON",
            "game_universe_state": "SOURCE_LISTED",
            "team_score": "",
            "opponent_score": "",
            "played_result": "",
        },
        {
            "research_game_id": "G2",
            "season_label": "1908-1909",
            "opponent_literal": "Wake Forest",
            "game_type": "REGULAR_SEASON",
            "game_universe_state": "SOURCE_LISTED",
            "team_score": "30",
            "opponent_score": "20",
            "played_result": "W",
        },
        {
            "research_game_id": "G3",
            "season_label": "1908-1909",
            "opponent_literal": "North Carolina",
            "game_type": "REGULAR_SEASON",
            "game_universe_state": "SOURCE_LISTED",
            "team_score": "10",
            "opponent_score": "12",
            "played_result": "L",
        },
    ]
    census = [
        {
            "season": "1907-1908",
            "observed_games": "1",
            "expected_games": "",
            "state": "UNQUANTIFIED",
        },
        {
            "season": "1908-1909",
            "observed_games": "2",
            "expected_games": "2",
            "state": "MATCH",
        },
    ]
    blockers = [
        {
            "class": "FOUNDING_SEASON_COVERAGE_UNQUANTIFIED",
            "season": "1907-1908",
        },
        {
            "class": "IDENTIFIED_GAME_RESULT_UNRESOLVED",
            "season": "1907-1908",
            "research_game_id": "G1",
        },
    ]
    status = {
        "school": "sample",
        "research_base_sha": "a" * 40,
        "blocking_residual_count": 2,
        "stage1_complete": False,
        "status": "INCOMPLETE",
    }
    return {
        "structured-stage1-ledger.csv": csv_bytes(ledger),
        "season-census.csv": csv_bytes(census),
        "blocking-residuals.json": json.dumps(
            blockers, sort_keys=True
        ).encode(),
        "stage1-status.json": json.dumps(
            status, sort_keys=True
        ).encode(),
    }


def metadata(parent_sha):
    evidence = [
        {
            "source": "official archive",
            "authority": "institutional",
            "finding": "No record survives",
        },
        {
            "source": "reciprocal institutional records",
            "authority": "institutional",
            "finding": "No additional result recovered",
        },
    ]
    return {
        "schema_version": 1,
        "school_key": "sample",
        "research_base_sha": "a" * 40,
        "parent_checkpoint_sha256": parent_sha,
        "identified_game_count": 3,
        "known_result_game_count": 2,
        "known_result_wins": 1,
        "known_result_losses": 1,
        "known_result_ties": 0,
        "class_a": [
            {
                "season": "1907-1908",
                "program_inception_season": "1907-1908",
                "founding_era_end_season": "1909-1910",
                "source_state": "NO_RECORD",
                "source_note": "No Record",
                "explicit_missing_game_count": None,
                "zero_competitive_games_established": False,
                "competitive_game_count_established": False,
                "research_exhausted": True,
                "systematic_evidence_checked": evidence,
                "observed_identified_game_ids": ["G1"],
            }
        ],
        "class_b": [
            {
                "research_game_id": "G1",
                "opponent_literal": "Charlotte YMCA",
                "competitive_inclusion": True,
                "game_type": "REGULAR_SEASON",
                "direct_score_or_result_evidence_present": False,
                "aggregate_result_allocation_used": False,
                "research_exhausted": True,
                "systematic_evidence_checked": evidence,
            }
        ],
    }


def write_zip(path, documents):
    blockers = json.loads(documents["blocking-residuals.json"])
    manifest = {
        "research_base_sha": "a" * 40,
        "game_rows": 3,
        "blocking_residuals": len(blockers),
        "members": {
            name: {
                "size": len(data),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
            for name, data in documents.items()
        },
    }
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in documents.items():
            archive.writestr("checkpoint/" + name, data)
        archive.writestr(
            "checkpoint/stage1-manifest.json",
            json.dumps(manifest, sort_keys=True).encode(),
        )
    return hashlib.sha256(path.read_bytes()).hexdigest()


def make_parent_candidate(
    root,
    *,
    mutate_metadata=None,
    mutate_candidate_documents=None,
):
    parent = root / "parent.zip"
    parent_docs = base_docs()
    parent_sha = write_zip(parent, parent_docs)

    candidate_docs = base_docs()
    candidate_metadata = metadata(parent_sha)
    if mutate_metadata:
        mutate_metadata(candidate_metadata)
    candidate_docs[mod.METADATA] = json.dumps(
        candidate_metadata, sort_keys=True
    ).encode()
    if mutate_candidate_documents:
        mutate_candidate_documents(candidate_docs)
    candidate = root / "candidate.zip"
    candidate_sha = write_zip(candidate, candidate_docs)
    return (
        parent,
        parent_sha,
        candidate,
        candidate_sha,
        candidate_docs,
    )


def make_closeout(root, candidate, candidate_sha, candidate_docs):
    audit = mod.audit_candidate(
        root / "parent.zip",
        candidate,
        expected_parent_sha256=hashlib.sha256(
            (root / "parent.zip").read_bytes()
        ).hexdigest(),
        expected_candidate_sha256=candidate_sha,
    )
    audit_path = root / "audit.json"
    audit_path.write_text(
        json.dumps(audit, sort_keys=True),
        encoding="utf-8",
    )
    audit_sha = hashlib.sha256(audit_path.read_bytes()).hexdigest()

    documents = dict(candidate_docs)
    closeout_metadata = json.loads(documents[mod.METADATA])
    closeout_metadata["audit_sha256"] = audit_sha
    closeout_metadata["terminal_classifications"] = {
        "class_a": mod.TERMINAL_A,
        "class_b": mod.TERMINAL_B,
    }
    metadata_bytes = json.dumps(
        closeout_metadata, sort_keys=True
    ).encode()
    documents[mod.METADATA] = metadata_bytes
    documents[mod.AUTHORING_METADATA] = metadata_bytes
    documents["blocking-residuals.json"] = b"[]"

    status = json.loads(documents["stage1-status.json"])
    status.update(
        {
            "blocking_residual_count": 0,
            "stage1_complete": True,
            "status": "COMPLETE",
        }
    )
    documents["stage1-status.json"] = json.dumps(
        status, sort_keys=True
    ).encode()

    closeout = root / "closeout.zip"
    closeout_sha = write_zip(closeout, documents)
    return audit, audit_path, audit_sha, closeout, closeout_sha


def audit_once(
    *,
    mutate_metadata=None,
    mutate_candidate_documents=None,
):
    temporary = tempfile.TemporaryDirectory()
    root = Path(temporary.name)
    (
        parent,
        parent_sha,
        candidate,
        candidate_sha,
        candidate_docs,
    ) = make_parent_candidate(
        root,
        mutate_metadata=mutate_metadata,
        mutate_candidate_documents=mutate_candidate_documents,
    )
    result = mod.audit_candidate(
        parent,
        candidate,
        expected_parent_sha256=parent_sha,
        expected_candidate_sha256=candidate_sha,
    )
    return temporary, root, result, (
        parent,
        parent_sha,
        candidate,
        candidate_sha,
        candidate_docs,
    )


def test_mixed_classes_are_eligible_but_never_complete():
    temporary, _, result, _ = audit_once()
    try:
        assert result["status"] == mod.ELIGIBLE
        assert result["defects"] == []
        assert result["identified_game_count"] == 3
        assert result["known_result_game_count"] == 2
        assert result["known_result_wins"] == 1
        assert result["known_result_losses"] == 1
        assert result["unknown_result_game_ids"] == ["G1"]
        assert result["unquantified_coverage_seasons"] == [
            "1907-1908"
        ]
        assert result["stage1_complete"] is False
    finally:
        temporary.cleanup()


def test_class_a_explicit_count_routes_to_counted_gap_path():
    def mutate(value):
        value["class_a"][0]["source_note"] = (
            "one game missing from the record"
        )

    temporary, _, result, _ = audit_once(
        mutate_metadata=mutate
    )
    try:
        assert (
            "CLASS_A_EXPLICIT_COUNT_BELONGS_TO_COUNTED_GAP_PATH:"
            "1907-1908"
        ) in result["defects"]
    finally:
        temporary.cleanup()


def test_class_a_explicit_zero_games_is_not_eligible():
    def mutate(value):
        value["class_a"][0][
            "zero_competitive_games_established"
        ] = True

    temporary, _, result, _ = audit_once(
        mutate_metadata=mutate
    )
    try:
        assert (
            "CLASS_A_ZERO_GAMES_NOT_EXCLUDED:1907-1908"
            in result["defects"]
        )
    finally:
        temporary.cleanup()


def test_class_a_mid_history_gap_is_rejected():
    def mutate(value):
        value["class_a"][0]["program_inception_season"] = (
            "1890-1891"
        )
        value["class_a"][0]["founding_era_end_season"] = (
            "1892-1893"
        )

    temporary, _, result, _ = audit_once(
        mutate_metadata=mutate
    )
    try:
        assert (
            "CLASS_A_NOT_FOUNDING_ERA:1907-1908"
            in result["defects"]
        )
    finally:
        temporary.cleanup()


def test_class_b_known_result_is_rejected():
    def mutate(value):
        value["class_b"][0].update(
            {
                "research_game_id": "G2",
                "opponent_literal": "Wake Forest",
            }
        )

    temporary, _, result, _ = audit_once(
        mutate_metadata=mutate
    )
    try:
        assert (
            "CLASS_B_RESULT_NOT_GENUINELY_UNKNOWN:G2"
            in result["defects"]
        )
        assert (
            "CLASS_B_UNKNOWN_RESULT_POPULATION_MISMATCH"
            in result["defects"]
        )
    finally:
        temporary.cleanup()


def test_class_b_aggregate_result_allocation_is_rejected():
    def mutate(value):
        value["class_b"][0][
            "aggregate_result_allocation_used"
        ] = True

    temporary, _, result, _ = audit_once(
        mutate_metadata=mutate
    )
    try:
        assert (
            "CLASS_B_AGGREGATE_ALLOCATION_NOT_EXCLUDED:G1"
            in result["defects"]
        )
    finally:
        temporary.cleanup()


def test_unrelated_stage1_blocker_is_rejected():
    def mutate(documents):
        blockers = json.loads(
            documents["blocking-residuals.json"]
        )
        blockers.append(
            {
                "class": "DUPLICATE_GAME_ID_UNRESOLVED",
                "season": "1950-1951",
            }
        )
        documents["blocking-residuals.json"] = json.dumps(
            blockers, sort_keys=True
        ).encode()
        status = json.loads(documents["stage1-status.json"])
        status["blocking_residual_count"] = 3
        documents["stage1-status.json"] = json.dumps(
            status, sort_keys=True
        ).encode()

    temporary, _, result, _ = audit_once(
        mutate_candidate_documents=mutate
    )
    try:
        assert "UNRELATED_STAGE1_BLOCKER:2" in result["defects"]
    finally:
        temporary.cleanup()


def test_candidate_historical_core_drift_is_rejected():
    def mutate(documents):
        rows = list(
            csv.DictReader(
                io.StringIO(
                    documents[
                        "structured-stage1-ledger.csv"
                    ].decode()
                )
            )
        )
        rows[0]["opponent_literal"] = "Changed Opponent"
        documents["structured-stage1-ledger.csv"] = csv_bytes(
            rows
        )

    temporary, _, result, _ = audit_once(
        mutate_candidate_documents=mutate
    )
    try:
        assert (
            "CANDIDATE_HISTORICAL_CORE_DRIFT:"
            "structured-stage1-ledger.csv"
        ) in result["defects"]
    finally:
        temporary.cleanup()


def test_candidate_cannot_claim_stage1_complete():
    def mutate(documents):
        status = json.loads(documents["stage1-status.json"])
        status["stage1_complete"] = True
        status["status"] = "COMPLETE"
        documents["stage1-status.json"] = json.dumps(
            status, sort_keys=True
        ).encode()

    temporary, _, result, _ = audit_once(
        mutate_candidate_documents=mutate
    )
    try:
        assert "PREMATURE_STAGE1_COMPLETE" in result["defects"]
    finally:
        temporary.cleanup()


def test_verified_closeout_preserves_ledger_and_terminal_debt():
    with tempfile.TemporaryDirectory() as name:
        root = Path(name)
        (
            parent,
            parent_sha,
            candidate,
            candidate_sha,
            candidate_docs,
        ) = make_parent_candidate(root)
        (
            audit,
            audit_path,
            audit_sha,
            closeout,
            closeout_sha,
        ) = make_closeout(
            root, candidate, candidate_sha, candidate_docs
        )
        assert audit["status"] == mod.ELIGIBLE
        result = mod.verify_closeout(
            candidate,
            closeout,
            audit_path,
            expected_candidate_sha256=candidate_sha,
            expected_closeout_sha256=closeout_sha,
            expected_audit_sha256=audit_sha,
        )
        assert result["status"] == mod.VERIFIED
        assert result["defects"] == []
        assert result["stage1_complete"] is True


def test_closeout_ledger_drift_is_rejected():
    with tempfile.TemporaryDirectory() as name:
        root = Path(name)
        (
            _,
            _,
            candidate,
            candidate_sha,
            candidate_docs,
        ) = make_parent_candidate(root)
        (
            _,
            audit_path,
            audit_sha,
            closeout,
            _,
        ) = make_closeout(
            root, candidate, candidate_sha, candidate_docs
        )

        with zipfile.ZipFile(closeout) as archive:
            members = {
                item: archive.read(item)
                for item in archive.namelist()
                if not item.endswith("/")
            }
        prefix = "checkpoint/"
        rows = list(
            csv.DictReader(
                io.StringIO(
                    members[
                        prefix
                        + "structured-stage1-ledger.csv"
                    ].decode()
                )
            )
        )
        rows[0]["opponent_literal"] = "Changed Opponent"
        documents = {
            name[len(prefix):]: data
            for name, data in members.items()
            if name != prefix + "stage1-manifest.json"
        }
        documents["structured-stage1-ledger.csv"] = csv_bytes(
            rows
        )
        drifted = root / "drifted-closeout.zip"
        drifted_sha = write_zip(drifted, documents)

        result = mod.verify_closeout(
            candidate,
            drifted,
            audit_path,
            expected_candidate_sha256=candidate_sha,
            expected_closeout_sha256=drifted_sha,
            expected_audit_sha256=audit_sha,
        )
        assert (
            "CLOSEOUT_HISTORICAL_CORE_DRIFT:"
            "structured-stage1-ledger.csv"
        ) in result["defects"]
