#!/usr/bin/env python3
"""Read-only candidate-runtime replay of the exact Grand Canyon blocked census.

This PR test never writes onboarding files or publishes any Git ref.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from remote_implementation_registered_key_rebase import (
    CENSUS_SHA256, SOURCE_HASHES, TARGET_HASHES, digest,
    make_candidate, require_census, verify_diff,
)

EXPECTED_MAIN = '242370fc551fd749c157c74d92917ddfafbe40e0'
EXPECTED_TARGET = 'f67371c2380b7b28255e525922e780a65737a475'
EXPECTED_CONTROL = '81a6191b927459fff30d2826b69cc43d9de27b15'
CENSUS_PATH = '.remote-implementation/checkpoints/grand-canyon/grand-canyon-stage2-census-0001'


def git(repo: Path, *args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=repo, text=True).strip()


def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--runtime', type=Path, required=True)
    p.add_argument('--control', type=Path, required=True)
    p.add_argument('--target', type=Path, required=True)
    args=p.parse_args()
    runtime=args.runtime.resolve();control=args.control.resolve();target=args.target.resolve()
    assert git(control, 'rev-parse', 'HEAD') == EXPECTED_CONTROL, 'CONTROL_CHANGED'
    assert git(target, 'rev-parse', 'HEAD') == EXPECTED_TARGET, 'TARGET_CHANGED'
    assert git(runtime, 'merge-base', 'HEAD', EXPECTED_MAIN) == EXPECTED_MAIN, 'BASE_MAIN_NOT_ANCESTOR'
    cp=control / CENSUS_PATH
    assert digest((cp/'checkpoint-manifest.json').read_bytes()) == CENSUS_SHA256, 'CENSUS_HASH_CHANGED'
    status=json.loads((cp/'implementation-stage2-status.json').read_bytes())
    census=json.loads((cp/'implementation-stage2-capability-census.json').read_bytes())
    assert len(require_census(status, census)) == 39, 'CENSUS_39_CONFLICTS_MISSING'
    school=target/'schools/grand-canyon'
    before={name:(school/name).read_bytes() for name in SOURCE_HASHES}
    after,proof=make_candidate(before['opponents.csv'],before['source-games.csv'],
        (target/'data/reference/programs.csv').read_bytes())
    assert verify_diff(before,after) == proof and len(proof['field_changes']) == 2
    for name,value in before.items():
        assert digest(value) == SOURCE_HASHES[name], name + ' ORIGINAL_HASH'
        assert digest(after[name]) == TARGET_HASHES[name], name + ' AFTER_HASH'
    assert not git(target, 'status', '--porcelain', '--untracked-files=all'), 'TARGET_DIRTY'
    assert not git(control, 'status', '--porcelain', '--untracked-files=all'), 'CONTROL_DIRTY'
    print(json.dumps({'status':'PASS','original_game_count':2147,'opponent_count':491,
        'display_conflict_count':39,'registered_key_rebase_cells':2,
        'original_sha256':SOURCE_HASHES,'candidate_sha256':TARGET_HASHES},indent=2))
    return 0

if __name__ == '__main__':
    try:sys.exit(main())
    except (AssertionError,ValueError,subprocess.CalledProcessError) as exc:
        print('STAGE2_KEY_REBASE_CANDIDATE_REPLAY_STOP:',exc,file=sys.stderr)
        sys.exit(1)
