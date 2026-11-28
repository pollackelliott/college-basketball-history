"""Exact Phase 0 venue-sidecar recovery for ordinary and expansion Stage 2."""
import hashlib
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import remote_implementation_stage2_proposal as proposal  # noqa: E402
from remote_implementation_io import Stop  # noqa: E402


def packed(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


class VenueSidecarProposalTests(unittest.TestCase):
    def make_fixture(self, *, expansion=False):
        sidecar = packed({"mappings": [{"action": "REUSE_CURRENT_IDENTITY"}]})
        sidecar_sha = digest(sidecar)
        freeze = {
            "schema_version": 2,
            "status": "INTEGRATION_FROZEN",
            "school_key": "example-school",
            "venue_reconciliation": {"spec_sha256": sidecar_sha},
        }
        if expansion:
            freeze["kind"] = proposal.EXPANSION_FREEZE_KIND
            freeze["venue_reconciliation_sha256"] = sidecar_sha
        freeze_bytes = packed(freeze)
        freeze_sha = digest(freeze_bytes)
        writeahead_path = ".remote-implementation/writeahead/example/phase0/writeahead-manifest.json"
        successor_path = ".remote-implementation/successors/example/phase0/successor-manifest.json"
        census_path = ".remote-implementation/checkpoints/example/census/checkpoint-manifest.json"
        operation = "EXPANSION_PHASE0" if expansion else None
        writeahead = {
            "kind": "REMOTE_IMPLEMENTATION_WRITEAHEAD",
            "request_id": "example-phase0-0001",
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "integration_freeze_sha256": freeze_sha,
            "sidecars": {"venue-reconciliation.json": sidecar_sha},
        }
        successor = {
            "kind": "REMOTE_IMPLEMENTATION_SUCCESSOR",
            "request_id": "example-phase0-0001",
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "integration_freeze_sha256": freeze_sha,
            "writeahead_manifest_path": writeahead_path,
        }
        if operation:
            writeahead["operation"] = operation
            successor["operation"] = operation
        writeahead_bytes = packed(writeahead)
        successor["writeahead_manifest_sha256"] = digest(writeahead_bytes)
        successor_bytes = packed(successor)
        census = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT",
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "integration_freeze_sha256": freeze_sha,
            "phase0_successor_path": successor_path,
            "phase0_successor_sha256": digest(successor_bytes),
        }
        census_bytes = packed(census)
        authority = {
            "kind": "REMOTE_IMPLEMENTATION_STAGE2_OPPONENT_DISPLAY_SUCCESSOR",
            "stage2_census_checkpoint_path": census_path,
            "stage2_census_checkpoint_sha256": digest(census_bytes),
        }
        request = {
            "school_key": "example-school",
            "target_branch": "data/example-school-onboarding",
            "integration_freeze_sha256": freeze_sha,
        }
        mapping = {
            census_path: census_bytes,
            successor_path: successor_bytes,
            writeahead_path: writeahead_bytes,
            ".remote-implementation/writeahead/example/phase0/venue-reconciliation.json": sidecar,
        }
        return request, authority, freeze_bytes, mapping, sidecar

    def check(self, request, authority, freeze_bytes, mapping):
        with patch.object(
            proposal, "git_show_bytes",
            side_effect=lambda commit, path, **kwargs: mapping[path],
        ):
            return proposal._phase0_venue_reconciliation_bytes(
                control_commit="c" * 40,
                stage2_authority=authority,
                request=request,
                freeze_bytes=freeze_bytes,
                source_repo=ROOT,
            )

    def test_ordinary_phase0_sidecar_from_nested_freeze_digest(self):
        request, authority, freeze, mapping, sidecar = self.make_fixture()
        self.assertEqual(self.check(request, authority, freeze, mapping), sidecar)

    def test_expansion_phase0_legacy_top_level_digest_remains_supported(self):
        request, authority, freeze, mapping, sidecar = self.make_fixture(expansion=True)
        self.assertEqual(self.check(request, authority, freeze, mapping), sidecar)

    def test_missing_and_conflicting_digests_fail_closed(self):
        request, authority, freeze, mapping, _ = self.make_fixture()
        obj = json.loads(freeze)
        obj["venue_reconciliation"].pop("spec_sha256")
        with self.assertRaisesRegex(Stop, "HASH_INVALID"):
            self.check(request, authority, packed(obj), mapping)
        obj["venue_reconciliation"]["spec_sha256"] = "a" * 64
        obj["venue_reconciliation_sha256"] = "b" * 64
        with self.assertRaisesRegex(Stop, "HASH_CONFLICT"):
            self.check(request, authority, packed(obj), mapping)

    def test_tampered_sidecar_bytes_are_rejected(self):
        request, authority, freeze, mapping, _ = self.make_fixture()
        path = ".remote-implementation/writeahead/example/phase0/venue-reconciliation.json"
        mapping[path] += b" "
        with self.assertRaisesRegex(Stop, "SIDECAR_HASH_MISMATCH"):
            self.check(request, authority, freeze, mapping)

    def test_expansion_operation_cannot_be_missing_or_ordinary(self):
        request, authority, freeze, mapping, _ = self.make_fixture(expansion=True)
        census_path = authority["stage2_census_checkpoint_path"]
        census = json.loads(mapping[census_path])
        successor_path = census["phase0_successor_path"]
        successor = json.loads(mapping[successor_path])
        successor["operation"] = "PHASE0"
        mapping[successor_path] = packed(successor)
        census["phase0_successor_sha256"] = digest(mapping[successor_path])
        mapping[census_path] = packed(census)
        authority["stage2_census_checkpoint_sha256"] = digest(mapping[census_path])
        with self.assertRaisesRegex(Stop, "SUCCESSOR_MISMATCH"):
            self.check(request, authority, freeze, mapping)

    def test_ordinary_rejects_unrelated_expansion_operation(self):
        request, authority, freeze, mapping, _ = self.make_fixture()
        census_path = authority["stage2_census_checkpoint_path"]
        census = json.loads(mapping[census_path])
        successor_path = census["phase0_successor_path"]
        successor = json.loads(mapping[successor_path])
        successor["operation"] = "EXPANSION_PHASE0"
        mapping[successor_path] = packed(successor)
        census["phase0_successor_sha256"] = digest(mapping[successor_path])
        mapping[census_path] = packed(census)
        authority["stage2_census_checkpoint_sha256"] = digest(mapping[census_path])
        with self.assertRaisesRegex(Stop, "SUCCESSOR_MISMATCH"):
            self.check(request, authority, freeze, mapping)


if __name__ == "__main__":
    unittest.main()
