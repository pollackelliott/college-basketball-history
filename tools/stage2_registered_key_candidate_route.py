"""Strict routing for an exact, approved registered-key candidate replay.

This recognizes one independently frozen preflight-blocked Stage 2 census,
and never converts it into a display-normalizer or synthetic decision universe.
"""
from __future__ import annotations
import json
from pathlib import Path

from remote_implementation_control import OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE
from remote_implementation_registered_key_rebase import (
    BLOCKER, CENSUS_SHA256, KeyRebaseStop, digest, require_census,
)

CONTROL = '81a6191b927459fff30d2826b69cc43d9de27b15'
MAIN = '242370fc551fd749c157c74d92917ddfafbe40e0'
TARGET = 'f67371c2380b7b28255e525922e780a65737a475'
FREEZE = '2d4063679b27c109d94f88ea09c58d9046063d5f22f03ef0de23b61d5e7b608d'
SEMANTIC = 'e9424df1a55f68fcab755f11a920259ee3759ff0cb92e9a0f74bce28e4905319'
CHECKPOINT = '.remote-implementation/checkpoints/grand-canyon/grand-canyon-stage2-census-0001/checkpoint-manifest.json'


def candidate_route(control_dir: Path, control_head: str, last: dict,
                    manifest: dict, checkpoint: str, manifest_bytes: bytes) -> bool:
    """False for unrelated census families; exact GCU case or hard failure."""
    if last.get('operation') != 'STAGE2_CENSUS' or last.get('school_key') != 'grand-canyon':
        return False
    if OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE != 'STAGE2_CURRENT_PROGRAM_KEY_REBASE':
        raise KeyRebaseStop('REGISTERED_KEY_OPERATION_NOT_REGISTERED')
    if (control_head != CONTROL
            or checkpoint != CHECKPOINT
            or digest(manifest_bytes) != CENSUS_SHA256
            or last.get('checkpoint_manifest_sha256') != CENSUS_SHA256
            or last.get('stage2_status') != 'BLOCKED'
            or last.get('fresh_runner_verification') != 'PASS'
            or last.get('remote_stage2_census_equivalence') != 'PASS'
            or last.get('target_branch') != 'data/grand-canyon-onboarding'
            or last.get('target_sha') != TARGET
            or last.get('protected_main_sha') != MAIN):
        raise KeyRebaseStop('REGISTERED_KEY_ROUTE_CONTROL_OR_CHECKPOINT_DRIFT')
    if (manifest.get('kind') != 'REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT'
            or manifest.get('request_id') != 'grand-canyon-stage2-census-0001'
            or manifest.get('school_key') != 'grand-canyon'
            or manifest.get('target_branch') != 'data/grand-canyon-onboarding'
            or manifest.get('target_sha') != TARGET
            or manifest.get('protected_main_sha') != MAIN
            or manifest.get('integration_freeze_sha256') != FREEZE
            or manifest.get('semantic_snapshot_sha256') != SEMANTIC
            or manifest.get('stage2_status') != 'BLOCKED'
            or manifest.get('capability_census_status') != 'PREFLIGHT_BLOCKED'):
        raise KeyRebaseStop('REGISTERED_KEY_ROUTE_FREEZE_OR_MANIFEST_DRIFT')
    parent = control_dir / Path(checkpoint).parent
    artifacts = {}
    for filename in ('implementation-stage2-status.json', 'implementation-stage2-capability-census.json'):
        raw = (parent / filename).read_bytes()
        if digest(raw) != manifest.get('artifact_sha256', {}).get(filename):
            raise KeyRebaseStop('REGISTERED_KEY_ROUTE_ARTIFACT_HASH_MISMATCH:' + filename)
        artifacts[filename] = json.loads(raw)
    display = require_census(artifacts['implementation-stage2-status.json'],
                             artifacts['implementation-stage2-capability-census.json'])
    if len(display) != 39 or BLOCKER not in artifacts['implementation-stage2-status.json']['blockers']:
        raise KeyRebaseStop('REGISTERED_KEY_ROUTE_BLOCKER_POPULATION_MISMATCH')
    return True
