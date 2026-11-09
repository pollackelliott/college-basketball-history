import hashlib
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
import sys

TOOLS = Path(__file__).parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from research_authoring_capsule import checkpoint_continuity_defects  # noqa: E402


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def manifest_bytes(members: dict[str, bytes]) -> bytes:
    payload = {
        "files": [
            {
                "name": name,
                "sha256": sha(data),
                "size_bytes": len(data),
            }
            for name, data in sorted(members.items())
        ]
    }
    return (json.dumps(payload, sort_keys=True) + "\n").encode()


def make_checkpoint(
    path: Path,
    *,
    old_bytes: bytes = b"old-opponents\n",
    new_bytes: bytes = b"new-opponents\n",
    include_authorization: bool = True,
    legacy_authorization: bool = True,
    historical_authority_changed=False,
    wrong_old=False,
    wrong_new=False,
    include_old_claim=True,
    include_new_claim=True,
    extra_claim_hash: str = "",
    generic_replacements=None,
):
    old_hash = sha(old_bytes)
    new_hash = sha(new_bytes)
    old_claim = {
        "stage4_authoring_carried": {
            "opponents.csv": {"sha256": old_hash}
        }
    }
    new_claim = {
        "stage4_authoring_carried": {
            "opponents.csv": {"sha256": new_hash}
        }
    }

    members: dict[str, bytes] = {
        "stage4-authoring/opponents.csv": new_bytes,
    }
    if include_old_claim:
        members["stage3a4-qa.json"] = json.dumps(old_claim, sort_keys=True).encode()
    if include_new_claim:
        members["stage3b-status.json"] = json.dumps(new_claim, sort_keys=True).encode()
    if extra_claim_hash:
        members["extra-claim.json"] = json.dumps(
            {
                "stage4_authoring_carried": {
                    "opponents.csv": {"sha256": extra_claim_hash}
                }
            },
            sort_keys=True,
        ).encode()

    if include_authorization:
        if generic_replacements is not None:
            auth = {"stage4_authoring_replacements": generic_replacements}
        elif legacy_authorization:
            auth = {
                "authoring_provenance_population": {
                    "classification": (
                        "AUTHORIZED_STAGE3B_CAPSULE_REPLACEMENT_VS_"
                        "INHERITED_STAGE3A4_BYTE_PRESERVATION_CLAIM"
                    ),
                    "member": "stage4-authoring/opponents.csv",
                    "old_inherited_sha256": (
                        "0" * 64 if wrong_old else old_hash
                    ),
                    "new_authorized_sha256": (
                        "f" * 64 if wrong_new else new_hash
                    ),
                    "old_claim_member": "stage3a4-qa.json",
                    "new_claim_member": "stage3b-status.json",
                    "historical_authority_changed": historical_authority_changed,
                }
            }
        else:
            auth = {}
        members["stage3b-preflight-defect-summary.json"] = json.dumps(
            auth, sort_keys=True
        ).encode()

    members["manifest.json"] = manifest_bytes(members)
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    return old_hash, new_hash


class AuthoringCapsuleSupersessionTests(unittest.TestCase):
    def test_valid_legacy_old_to_new_replacement_explains_historical_hashes(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            make_checkpoint(path)
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(checkpoint_continuity_defects(archive), [])

    def test_valid_generic_replacement_shape_is_supported(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            old = b"old-opponents\n"
            new = b"new-opponents\n"
            make_checkpoint(
                path,
                old_bytes=old,
                new_bytes=new,
                legacy_authorization=False,
                generic_replacements=[
                    {
                        "member": "stage4-authoring/opponents.csv",
                        "old_sha256": sha(old),
                        "new_sha256": sha(new),
                        "old_claim_member": "stage3a4-qa.json",
                        "new_claim_member": "stage3b-status.json",
                        "historical_authority_changed": False,
                    }
                ],
            )
            with zipfile.ZipFile(path) as archive:
                self.assertEqual(checkpoint_continuity_defects(archive), [])

    def test_multiple_hashes_without_authorization_remain_ambiguous(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            make_checkpoint(path, include_authorization=False)
            with zipfile.ZipFile(path) as archive:
                defects = checkpoint_continuity_defects(archive)
            self.assertIn(
                "AMBIGUOUS_INHERITED_AUTHORING_AUTHORITY",
                {item["reason"] for item in defects},
            )

    def test_wrong_old_or_new_claim_hash_fails_closed(self):
        for field in ("old", "new"):
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as td:
                    path = Path(td) / "checkpoint.zip"
                    make_checkpoint(
                        path,
                        wrong_old=field == "old",
                        wrong_new=field == "new",
                    )
                    with zipfile.ZipFile(path) as archive:
                        defects = checkpoint_continuity_defects(archive)
                    reasons = {item["reason"] for item in defects}
                    self.assertIn(
                        (
                            "AUTHORIZED_REPLACEMENT_OLD_CLAIM_MISMATCH"
                            if field == "old"
                            else "AUTHORIZED_REPLACEMENT_NEW_CLAIM_MISMATCH"
                        ),
                        reasons,
                    )
                    self.assertIn(
                        "AMBIGUOUS_INHERITED_AUTHORING_AUTHORITY",
                        reasons,
                    )

    def test_missing_claim_member_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            make_checkpoint(path, include_old_claim=False)
            with zipfile.ZipFile(path) as archive:
                defects = checkpoint_continuity_defects(archive)
            reasons = {item["reason"] for item in defects}
            self.assertIn(
                "AUTHORIZED_REPLACEMENT_CLAIM_MEMBER_MISSING",
                reasons,
            )

    def test_historical_authority_change_cannot_be_compatibility_supersession(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            make_checkpoint(path, historical_authority_changed=True)
            with zipfile.ZipFile(path) as archive:
                defects = checkpoint_continuity_defects(archive)
            reasons = {item["reason"] for item in defects}
            self.assertIn(
                "AUTHORIZED_REPLACEMENT_CHANGED_HISTORICAL_AUTHORITY",
                reasons,
            )
            self.assertIn(
                "AMBIGUOUS_INHERITED_AUTHORING_AUTHORITY",
                reasons,
            )

    def test_current_bytes_must_equal_terminal_hash(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            old = b"old-opponents\n"
            new = b"new-opponents\n"
            actual = b"third-opponents\n"
            old_hash = sha(old)
            new_hash = sha(new)
            old_claim = {
                "stage4_authoring_carried": {
                    "opponents.csv": {"sha256": old_hash}
                }
            }
            new_claim = {
                "stage4_authoring_carried": {
                    "opponents.csv": {"sha256": new_hash}
                }
            }
            auth = {
                "stage4_authoring_replacements": [
                    {
                        "member": "stage4-authoring/opponents.csv",
                        "old_sha256": old_hash,
                        "new_sha256": new_hash,
                        "old_claim_member": "stage3a4-qa.json",
                        "new_claim_member": "stage3b-status.json",
                        "historical_authority_changed": False,
                    }
                ]
            }
            members = {
                "stage4-authoring/opponents.csv": actual,
                "stage3a4-qa.json": json.dumps(old_claim).encode(),
                "stage3b-status.json": json.dumps(new_claim).encode(),
                "repair.json": json.dumps(auth).encode(),
            }
            members["manifest.json"] = manifest_bytes(members)
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in members.items():
                    archive.writestr(name, data)
            with zipfile.ZipFile(path) as archive:
                defects = checkpoint_continuity_defects(archive)
            self.assertIn(
                "AMBIGUOUS_INHERITED_AUTHORING_AUTHORITY",
                {item["reason"] for item in defects},
            )

    def test_third_unexplained_hash_remains_ambiguous(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            third_hash = sha(b"third historical version")
            make_checkpoint(path, extra_claim_hash=third_hash)
            with zipfile.ZipFile(path) as archive:
                defects = checkpoint_continuity_defects(archive)
            self.assertIn(
                "AMBIGUOUS_INHERITED_AUTHORING_AUTHORITY",
                {item["reason"] for item in defects},
            )

    def test_branching_replacement_chain_fails_closed(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "checkpoint.zip"
            old = b"old-opponents\n"
            new = b"new-opponents\n"
            third = b"third-opponents\n"
            old_hash = sha(old)
            new_hash = sha(new)
            third_hash = sha(third)
            old_claim = {
                "stage4_authoring_carried": {
                    "opponents.csv": {"sha256": old_hash}
                }
            }
            new_claim = {
                "stage4_authoring_carried": {
                    "opponents.csv": {"sha256": new_hash}
                }
            }
            third_claim = {
                "stage4_authoring_carried": {
                    "opponents.csv": {"sha256": third_hash}
                }
            }
            auth = {
                "stage4_authoring_replacements": [
                    {
                        "member": "stage4-authoring/opponents.csv",
                        "old_sha256": old_hash,
                        "new_sha256": new_hash,
                        "old_claim_member": "old.json",
                        "new_claim_member": "new.json",
                        "historical_authority_changed": False,
                    },
                    {
                        "member": "stage4-authoring/opponents.csv",
                        "old_sha256": old_hash,
                        "new_sha256": third_hash,
                        "old_claim_member": "old.json",
                        "new_claim_member": "third.json",
                        "historical_authority_changed": False,
                    },
                ]
            }
            members = {
                "stage4-authoring/opponents.csv": new,
                "old.json": json.dumps(old_claim).encode(),
                "new.json": json.dumps(new_claim).encode(),
                "third.json": json.dumps(third_claim).encode(),
                "repair.json": json.dumps(auth).encode(),
            }
            members["manifest.json"] = manifest_bytes(members)
            with zipfile.ZipFile(path, "w") as archive:
                for name, data in members.items():
                    archive.writestr(name, data)
            with zipfile.ZipFile(path) as archive:
                defects = checkpoint_continuity_defects(archive)
            self.assertIn(
                "AMBIGUOUS_INHERITED_AUTHORING_AUTHORITY",
                {item["reason"] for item in defects},
            )


if __name__ == "__main__":
    unittest.main()
