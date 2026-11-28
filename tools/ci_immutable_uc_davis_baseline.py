#!/usr/bin/env python3
"""Create and verify an isolated exact historical data checkout for UC Davis CI.

The resulting clone pins both HEAD and its *private* origin/main tracking ref
to the immutable Stage 1 baseline. It never mutates the source PR checkout,
the real remote, or any accepted historical data. Tools run from PR HEAD.
"""
from __future__ import annotations
import argparse
import re
import subprocess
from pathlib import Path

class BaselineStop(ValueError):
    pass

def git(repo: Path, *args: str, check: bool = True) -> str:
    cp = subprocess.run(['git', '-C', str(repo), *args], text=True,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and cp.returncode:
        raise BaselineStop('GIT_BASELINE_COMMAND_FAILED:' + ' '.join(args) + ':' + cp.stderr[-350:])
    return cp.stdout.strip()

def verify_baseline(repo: Path, expected_sha: str) -> None:
    if not re.fullmatch('[0-9a-f]{40}', expected_sha):
        raise BaselineStop('BASELINE_SHA_MALFORMED')
    if git(repo, 'rev-parse', 'HEAD') != expected_sha:
        raise BaselineStop('BASELINE_HEAD_MISMATCH')
    if git(repo, 'rev-parse', 'refs/remotes/origin/main') != expected_sha:
        raise BaselineStop('BASELINE_PRIVATE_MAIN_MISMATCH')
    if git(repo, 'status', '--porcelain', '--untracked-files=all'):
        raise BaselineStop('BASELINE_DATA_DIRTY')
    if git(repo, 'rev-parse', expected_sha + '^{commit}') != expected_sha:
        raise BaselineStop('BASELINE_OBJECT_MISMATCH')

def create_baseline(runtime: Path, dest: Path, expected_sha: str) -> None:
    runtime = runtime.resolve()
    dest = dest.resolve()
    if dest.exists():
        raise BaselineStop('BASELINE_OUTPUT_ALREADY_EXISTS')
    if not re.fullmatch('[0-9a-f]{40}', expected_sha):
        raise BaselineStop('BASELINE_SHA_MALFORMED')
    if git(runtime, 'status', '--porcelain', '--untracked-files=all'):
        raise BaselineStop('CANDIDATE_RUNTIME_DIRTY')
    if git(runtime, 'rev-parse', expected_sha + '^{commit}') != expected_sha:
        raise BaselineStop('BASELINE_COMMIT_OBJECT_MISSING')
    result = subprocess.run(['git', 'clone', '--local', '--no-hardlinks',
                             str(runtime), str(dest)], capture_output=True, text=True)
    if result.returncode:
        raise BaselineStop('ISOLATED_BASELINE_CLONE_FAILED:' + result.stderr[-350:])
    git(dest, 'checkout', '--detach', expected_sha)
    # Private clone remote-tracking ref, never the real repository's origin/main.
    git(dest, 'update-ref', 'refs/remotes/origin/main', expected_sha)
    verify_baseline(dest, expected_sha)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--runtime', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--baseline-sha', required=True)
    opts = parser.parse_args()
    create_baseline(opts.runtime, opts.output, opts.baseline_sha)
    print('UC_DAVIS_IMMUTABLE_DATA_BASELINE=PASS')
    print('HISTORICAL_BASE_SHA=' + opts.baseline_sha)
    print('TOOLS_RUNTIME_SHA=' + git(opts.runtime, 'rev-parse', 'HEAD'))
    return 0

if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except BaselineStop as exc:
        raise SystemExit('UC_DAVIS_IMMUTABLE_BASELINE_STOP:' + str(exc))
