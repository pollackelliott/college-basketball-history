#!/usr/bin/env python3
"""Fail-closed disposable full-runtime rehearsal of issue #736's exact case.

Runs the real guarded candidate preparation and permanent Stage 2 census in a
throwaway local clone. Publishes no branch, acquires no production mutation lock,
and cannot constitute approval to dispatch the live registered-key operation.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

from remote_implementation_registered_key_rebase import (
    BLOCKER, CENSUS_SHA256, SOURCE_HASHES, TARGET_HASHES, digest,
    make_candidate, require_census, verify_diff,
)
from remote_implementation_stage2_key_rebase import _candidate
from remote_implementation_stage2_census import run_stage2_census_tool

EXPECTED_MAIN = '242370fc551fd749c157c74d92917ddfafbe40e0'
EXPECTED_TARGET = 'f67371c2380b7b28255e525922e780a65737a475'
EXPECTED_CONTROL = '81a6191b927459fff30d2826b69cc43d9de27b15'
EXPECTED_FREEZE = '2d4063679b27c109d94f88ea09c58d9046063d5f22f03ef0de23b61d5e7b608d'
CENSUS_PATH = '.remote-implementation/checkpoints/grand-canyon/grand-canyon-stage2-census-0001'
FREEZE_PATH = '.remote-implementation/writeahead/grand-canyon/grand-canyon-phase0-0001/integration-freeze.json'


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=repo, text=True).strip()


def checked(*args: str, cwd: Path | None = None) -> None:
    subprocess.run(list(args), cwd=cwd, check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--runtime', type=Path, required=True)
    p.add_argument('--control', type=Path, required=True)
    p.add_argument('--target', type=Path, required=True)
    args = p.parse_args()
    runtime, control, target = (value.resolve() for value in
                                (args.runtime, args.control, args.target))
    assert git(control, 'rev-parse', 'HEAD') == EXPECTED_CONTROL, 'CONTROL_CHANGED'
    assert git(target, 'rev-parse', 'HEAD') == EXPECTED_TARGET, 'TARGET_CHANGED'
    assert git(runtime, 'merge-base', 'HEAD', EXPECTED_MAIN) == EXPECTED_MAIN, 'BASE_MAIN_NOT_ANCESTOR'
    assert not git(target, 'status', '--porcelain', '--untracked-files=all'), 'TARGET_DIRTY'
    assert not git(control, 'status', '--porcelain', '--untracked-files=all'), 'CONTROL_DIRTY'
    cp = control / CENSUS_PATH
    assert digest((cp/'checkpoint-manifest.json').read_bytes()) == CENSUS_SHA256, 'CENSUS_HASH_CHANGED'
    original_status = json.loads((cp/'implementation-stage2-status.json').read_bytes())
    original_census = json.loads((cp/'implementation-stage2-capability-census.json').read_bytes())
    assert len(require_census(original_status, original_census)) == 39, 'CENSUS_39_CONFLICTS_MISSING'
    expected_remaining = sorted(x for x in original_status['blockers'] if x != BLOCKER)
    assert len(expected_remaining) == 39, 'BASELINE_BLOCKER_COUNT_CHANGED'

    freeze = (control / FREEZE_PATH).read_bytes()
    assert digest(freeze) == EXPECTED_FREEZE, 'PHASE0_FREEZE_HASH_CHANGED'
    before = {name: (target/'schools/grand-canyon'/name).read_bytes()
              for name in SOURCE_HASHES}
    after, pure_proof = make_candidate(before['opponents.csv'], before['source-games.csv'],
        (target/'data/reference/programs.csv').read_bytes())
    assert verify_diff(before, after) == pure_proof and len(pure_proof['field_changes']) == 2
    for name in before:
        assert digest(before[name]) == SOURCE_HASHES[name], name + ' ORIGINAL_HASH'
        assert digest(after[name]) == TARGET_HASHES[name], name + ' AFTER_HASH'

    with tempfile.TemporaryDirectory(prefix='gcu-exact-key-rebase-rehearsal-') as folder:
        scratch = Path(folder) / 'scratch'
        checked('git', 'clone', '--local', '--no-hardlinks', str(target), str(scratch))
        checked('git', 'checkout', '--detach', EXPECTED_TARGET, cwd=scratch)
        checked('git', 'config', 'user.name', 'candidate-rehearsal', cwd=scratch)
        checked('git', 'config', 'user.email', 'candidate-rehearsal@example.invalid', cwd=scratch)
        prepared = _candidate(scratch, EXPECTED_TARGET, freeze)
        assert prepared['prepared_parent_sha'] == EXPECTED_TARGET, 'PREPARED_PARENT_CHANGED'
        assert prepared['field_level_proof'] == pure_proof, 'PREPARED_FIELD_PROOF_CHANGED'
        assert sorted(prepared['changed_paths']) == sorted(pure_proof['allowed_paths']), 'PREPARED_PATHS_CHANGED'
        assert prepared['semantic_drift_before']['status'] == 'PASS', 'BEFORE_SEMANTIC_DRIFT'
        assert prepared['semantic_drift_after']['status'] == 'PASS', 'AFTER_SEMANTIC_DRIFT'
        assert not prepared['semantic_drift_after']['changes'], 'HISTORICAL_SOURCE_CHANGED'
        for name in TARGET_HASHES:
            assert digest((scratch/'schools/grand-canyon'/name).read_bytes()) == TARGET_HASHES[name], 'PREPARED_BYTES_MISMATCH'
        validation = subprocess.run([sys.executable, str(runtime/'tools/validate_data.py'), str(scratch)],
            cwd=runtime, capture_output=True, text=True)
        assert validation.returncode == 0, 'PROJECT_VALIDATION_FAILED: ' + validation.stdout[-2500:]

        output = run_stage2_census_tool(scratch, 'grand-canyon', freeze,
                                        Path(folder)/'stage2-diagnostics', tool_repo=runtime)
        result = output['status']
        blockers = sorted(result.get('blockers') or [])
        assert output['stage2_status'] == 'BLOCKED', 'STAGE2_UNEXPECTED_STATUS'
        assert blockers == expected_remaining, 'STAGE2_NOT_EXACT_39_DISPLAY_BLOCKERS: ' + repr(blockers)
        assert not any('current-D1 opponent key' in x for x in blockers), 'CURRENT_D1_REBASE_UNRESOLVED'
        assert output['tracked_mutation_proof']['tracked_stage2_mutation'] == 'NONE', 'STAGE2_MUTATED_TRACKED_STATE'
        assert result['preflight']['warning_count'] == 0, 'STAGE2_WARNINGS'
        assert result['preflight']['decision_count'] == 0, 'STAGE2_OWNER_DECISIONS'
        print(json.dumps({
            'status': 'EXACT_CANDIDATE_RUNTIME_REPLAY_PASS',
            'candidate_runtime_sha': git(runtime, 'rev-parse', 'HEAD'),
            'original_target_sha': EXPECTED_TARGET,
            'prepared_commit_sha': prepared['prepared_commit_sha'],
            'after_census_blockers': len(blockers),
            'only_display_blockers': True,
            'original_game_count': 2147,
            'original_opponent_count': 491,
            'registered_key_rebase_cells': 2,
            'semantic_drift': 'PASS',
            'repository_validation': 'PASS',
            'tracked_publication': 'NONE',
        }, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (AssertionError, ValueError, subprocess.CalledProcessError) as exc:
        print('STAGE2_KEY_REBASE_CANDIDATE_REPLAY_STOP:', exc, file=sys.stderr)
        sys.exit(1)
