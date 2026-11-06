import hashlib
import json
import zipfile
from pathlib import Path
import sys

TOOLS = Path(__file__).parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from research_authoring_capsule import (  # noqa: E402
    carry_authoring_capsule,
    checkpoint_continuity_defects,
    compare_parent_child,
)


def make_zip(path, members):
    with zipfile.ZipFile(path, "w") as z:
        for name, data in members.items():
            if isinstance(data, str):
                data = data.encode()
            z.writestr(name, data)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def test_fordham_shaped_dropped_capsule_is_explicit_not_reconstructed(tmp_path):
    opponents = b"source_program_key,source_opponent_label,current_d1\nfordham,Army,Yes\n"
    coverage = b'{"schema_version":1,"coverage":[]}\n'
    checkpoint = tmp_path / "child.zip"
    status = {
        "stage4_authoring_carried": {
            "opponents.csv": {
                "sha256": sha(opponents),
                "input_member": "stage4-authoring/opponents.csv",
            },
            "season-coverage.json": {
                "sha256": sha(coverage),
                "input_member": "stage4-authoring/season-coverage.json",
            },
        }
    }
    make_zip(checkpoint, {"stage3a0-status.json": json.dumps(status)})
    with zipfile.ZipFile(checkpoint) as z:
        defects = checkpoint_continuity_defects(z)
    assert {d["name"] for d in defects} == {
        "stage4-authoring/opponents.csv",
        "stage4-authoring/season-coverage.json",
    }
    assert all(d["reason"] == "DROPPED_INHERITED_AUTHORING_MEMBER" for d in defects)
    assert {d["expected_sha256"] for d in defects} == {sha(opponents), sha(coverage)}


def test_exact_parent_bytes_are_carried_and_changed_inheritance_fails(tmp_path):
    opponents = b"source_program_key,source_opponent_label\nfordham,Army\n"
    venues = b"source_program_key,venue_key\nfordham,rose-hill\n"
    parent_path = tmp_path / "parent.zip"
    make_zip(parent_path, {
        "stage4-authoring/opponents.csv": opponents,
        "stage4-authoring/venues.csv": venues,
    })
    out = tmp_path / "out"
    with zipfile.ZipFile(parent_path) as parent:
        carried = carry_authoring_capsule(parent, out)
    assert (out / "stage4-authoring/opponents.csv").read_bytes() == opponents
    assert (out / "stage4-authoring/venues.csv").read_bytes() == venues
    assert carried["opponents.csv"]["sha256"] == sha(opponents)

    child_path = tmp_path / "child.zip"
    make_zip(child_path, {
        "stage4-authoring/opponents.csv": opponents + b"#changed\n",
        "stage4-authoring/venues.csv": venues,
    })
    with zipfile.ZipFile(parent_path) as parent, zipfile.ZipFile(child_path) as child:
        defects = compare_parent_child(parent, child)
    assert defects == [{
        "reason": "CHANGED_INHERITED_AUTHORING_MEMBER",
        "name": "stage4-authoring/opponents.csv",
        "expected_sha256": sha(opponents),
        "actual_sha256": sha(opponents + b"#changed\n"),
    }]


def test_owned_member_may_be_updated_but_unowned_member_may_not(tmp_path):
    opponents = b"opponents-old"
    venues = b"venues-old"
    parent_path = tmp_path / "parent.zip"
    child_path = tmp_path / "child.zip"
    make_zip(parent_path, {
        "stage4-authoring/opponents.csv": opponents,
        "stage4-authoring/venues.csv": venues,
    })
    make_zip(child_path, {
        "stage4-authoring/opponents.csv": opponents,
        "stage4-authoring/venues.csv": b"venues-new",
    })
    with zipfile.ZipFile(parent_path) as parent, zipfile.ZipFile(child_path) as child:
        assert compare_parent_child(parent, child, owned_updates={"venues.csv"}) == []
