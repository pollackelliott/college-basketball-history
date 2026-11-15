import hashlib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from research_stage4 import _institutional_scope_payload, _notes


def make_checkpoint(path: Path, payload: dict):
    raw = json.dumps(payload, sort_keys=True).encode() + b"\n"
    manifest = {
        "files": {
            "stage4-authoring/institutional-scope.json": {
                "sha256": hashlib.sha256(raw).hexdigest(),
                "bytes": len(raw),
            }
        }
    }
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("stage4-authoring/institutional-scope.json", raw)
        archive.writestr("manifest.json", json.dumps(manifest))


def valid_payload():
    return {
        "schema_version": 1,
        "kind": "COMPLETE_INSTITUTIONAL_RESEARCH_SCOPE_V1",
        "school_key": "unlv",
        "research_base_sha": "a" * 40,
        "program_inception_season": "1958-1959",
        "top_level_scope": "1969-70+",
        "publication_universe": "INCEPTION_THROUGH_PRESENT",
        "transition_mode": "IN_PROGRESS_RETROFIT",
        "parent_artifact_sha256": "b" * 64,
        "preservation_rule": "PRESERVE_ACCEPTED_PARENT_WORK_EXCEPT_GENUINE_CONTRADICTION",
    }


def test_complete_institutional_scope_payload_validates(tmp_path):
    path = tmp_path / "scope.zip"
    payload = valid_payload()
    make_checkpoint(path, payload)
    with zipfile.ZipFile(path) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        actual, defects, summary = _institutional_scope_payload(
            archive, "", manifest, school_key="unlv", research_base_sha="a" * 40
        )
    assert actual == payload
    assert defects == []
    assert summary["program_inception_season"] == "1958-1959"
    assert summary["transition_mode"] == "IN_PROGRESS_RETROFIT"


def test_retrofit_scope_requires_parent_hash(tmp_path):
    path = tmp_path / "scope-invalid.zip"
    payload = valid_payload()
    payload.pop("parent_artifact_sha256")
    make_checkpoint(path, payload)
    with zipfile.ZipFile(path) as archive:
        manifest = json.loads(archive.read("manifest.json"))
        _, defects, _ = _institutional_scope_payload(
            archive, "", manifest, school_key="unlv", research_base_sha="a" * 40
        )
    assert {"reason": "INSTITUTIONAL_SCOPE_PARENT_HASH_REQUIRED"} in defects


def test_stage4_notes_render_inception_and_top_level_scope_separately():
    text = _notes(
        "unlv",
        "c" * 64,
        {"research_base_sha": "a" * 40, "status": "COMPLETE"},
        [],
        {
            "primary_source_historical_cutoff": "2024-2025",
            "required_completed_season_cutoff": "2025-2026",
        },
        valid_payload(),
    )
    assert "Program inception season: 1958-1959" in text
    assert "Accepted top-level/D-I scope: 1969-70+" in text
    assert "does not clip this ordinary institutional game universe" in text
