#!/usr/bin/env python3
"""Guarded Grand Canyon registered-key correction transaction and fresh proof.

One explicitly approved historical-identity representation case only.
No other program, school or opponent key can use this operation.
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from integration_freeze_guard import semantic_drift_report
from remote_implementation_control import (
    OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE, begin_request, bind_lock_commit,
    finalize_success, publish_ref_cas, sha256_bytes, sha256_file,
    validate_control_state,
)
from remote_implementation_io import (
    ROOT, STATE_PATH, Stop, commit_control, configure_git, git, git_show_bytes,
    read_json, remote_head, run, write_json,
)
from remote_implementation_stage2_census import (
    add_existing_onboarding_worktree, restore_integration_freeze,
    tracked_worktree_state,
)
from remote_implementation_stage2_opponent_display import verify_census_and_freeze_authority
from remote_implementation_registered_key_rebase import (
    ALLOWED_PATHS, BLOCKER, CENSUS_SHA256, GAME_ID, NEW_KEY, OLD_KEY,
    RULING_URL, SCHOOL, SOURCE_HASHES, TARGET_HASHES, digest,
    make_candidate, require, require_census, require_exact_target_files,
)

DIAG = Path(os.environ.get('REMOTE_IMPLEMENTATION_DIAG', '/tmp/remote-implementation-diagnostics'))


def _scope(request: dict, state: dict, control_commit: str) -> dict[str, Any]:
    """Authenticate the published Phase 0, full blocked census, and ruling."""
    if request.get('school_key') != SCHOOL or request.get('target_branch') != 'data/grand-canyon-onboarding':
        raise Stop('KEY_REBASE_SCHOOL_OR_TARGET_FORBIDDEN')
    if request.get('stage2_census_checkpoint', {}).get('sha256') != CENSUS_SHA256:
        raise Stop('KEY_REBASE_CENSUS_NOT_OWNER_BOUND')
    if request.get('ruling_url') != RULING_URL or request.get('case') != GAME_ID:
        raise Stop('KEY_REBASE_RULING_OR_CASE_MISMATCH')
    last = state.get('last_operation') or {}
    if not (last.get('operation') == 'STAGE2_CENSUS'
            and last.get('request_id') == 'grand-canyon-stage2-census-0001'
            and last.get('fresh_runner_verification') == 'PASS'
            and last.get('remote_stage2_census_equivalence') == 'PASS'
            and last.get('checkpoint_manifest_sha256') == CENSUS_SHA256
            and last.get('target_sha') == request.get('target_sha')):
        raise Stop('KEY_REBASE_CURRENT_CONTROL_CENSUS_AUTHORITY_MISSING')
    authority = verify_census_and_freeze_authority(request, control_commit)
    manifest = authority['census_manifest']
    if (manifest.get('stage2_status') != 'BLOCKED'
            or manifest.get('capability_census_status') != 'PREFLIGHT_BLOCKED'
            or manifest.get('preflight', {}).get('blocker_count') != 40
            or manifest.get('preflight', {}).get('decision_count') != 0
            or manifest.get('preflight', {}).get('warning_count') != 0):
        raise Stop('KEY_REBASE_PREFLIGHT_AUTHORITY_MISMATCH')
    cp = Path(request['stage2_census_checkpoint']['path']).parent
    census = json.loads(git_show_bytes(control_commit,
        (cp / 'implementation-stage2-capability-census.json').as_posix()))
    require_census(authority['status'], census)
    if authority['display_blocker_keys'] != sorted(set(authority['display_blocker_keys'])) \
            or len(authority['display_blocker_keys']) != 39 \
            or authority['current_d1_blocker_keys'] != [OLD_KEY] \
            or len(authority['blocker_keys']) != 40:
        raise Stop('KEY_REBASE_COMPLETE_BLOCKER_POPULATION_MISMATCH')
    if authority['phase0_successor']['prepared_commit_sha'] != request['target_sha']:
        raise Stop('KEY_REBASE_NOT_ORIGINAL_PHASE0_TARGET')
    return authority


def _files_at(commit: str) -> dict[str, bytes]:
    return {name: git_show_bytes(commit, f'schools/{SCHOOL}/{name}')
            for name in SOURCE_HASHES}


def _semantic_pass(worktree: Path, freeze: bytes, phase: str) -> dict:
    restore_integration_freeze(worktree, SCHOOL, freeze)
    proof = semantic_drift_report(worktree, SCHOOL)
    if proof.get('status') != 'PASS' or proof.get('changes'):
        raise Stop('KEY_REBASE_SEMANTIC_DRIFT_' + phase)
    return proof


def _candidate(worktree: Path, predecessor: str, freeze: bytes) -> dict:
    before_state = tracked_worktree_state(worktree)
    if before_state['head_sha'] != predecessor or before_state['status']:
        raise Stop('KEY_REBASE_DIRTY_OR_STALE_PREDECESSOR')
    before = _files_at(predecessor)
    registry = (worktree / 'data/reference/programs.csv').read_bytes()
    pre = _semantic_pass(worktree, freeze, 'BEFORE')
    after, proof = make_candidate(before['opponents.csv'], before['source-games.csv'], registry)
    for name, value in after.items():
        (worktree / 'schools' / SCHOOL / name).write_bytes(value)
    if require_exact_target_files(before, after, registry) != proof:
        raise Stop('KEY_REBASE_CANDIDATE_PROOF_MISMATCH')
    post = _semantic_pass(worktree, freeze, 'AFTER')
    paths = sorted(x.strip() for x in git('diff', '--name-only', cwd=worktree).stdout.splitlines() if x.strip())
    if paths != sorted(ALLOWED_PATHS):
        raise Stop('KEY_REBASE_ADDITIONAL_CHANGED_PATHS')
    git('add', '--', *ALLOWED_PATHS, cwd=worktree)
    git('commit', '-m', f'Guarded Grand Canyon registered key rebase {GAME_ID}', cwd=worktree)
    prepared = git('rev-parse', 'HEAD', cwd=worktree).stdout.strip()
    tree = git('rev-parse', 'HEAD^{tree}', cwd=worktree).stdout.strip()
    parent = git('rev-parse', 'HEAD^', cwd=worktree).stdout.strip()
    if parent != predecessor:
        raise Stop('KEY_REBASE_PREPARED_PARENT_MISMATCH')
    candidate_sha = {f'schools/{SCHOOL}/{name}': digest(value) for name, value in after.items()}
    return {'prepared_commit_sha': prepared, 'prepared_tree_sha': tree,
            'prepared_parent_sha': parent, 'changed_paths': paths,
            'changed_file_sha256': candidate_sha, 'field_level_proof': proof,
            'semantic_drift_before': pre, 'semantic_drift_after': post}


def _finalize(active: dict, request: dict, request_bytes: bytes, live_main: str,
              writeahead: dict, writeahead_path: str, writeahead_sha: str,
              writeahead_commit: str, expected_remote: str,
              *, recovery_id: str | None = None, recovery_classification: str | None = None,
              extra_paths: list[str | Path] | None = None) -> str:
    rid = request['request_id']
    if remote_head(ROOT, request['target_branch']) != writeahead['prepared_commit_sha']:
        raise Stop('KEY_REBASE_NOT_PUBLISHED_EXACT')
    folder = Path('.remote-implementation/successors') / SCHOOL / rid
    folder.mkdir(parents=True, exist_ok=True)
    successor = {k: v for k, v in writeahead.items()
                 if k not in {'sidecars', 'mutation_state'}}
    successor.update({'kind': 'REMOTE_IMPLEMENTATION_STAGE2_REGISTERED_KEY_REBASE_SUCCESSOR',
                      'actual_published_target_sha': writeahead['prepared_commit_sha'],
                      'writeahead_manifest_path': writeahead_path,
                      'writeahead_manifest_sha256': writeahead_sha,
                      'writeahead_commit': writeahead_commit,
                      'publication_cas': 'EXISTING_REF_CAS_PASS' if not recovery_id else 'RECOVERY_ADOPTION_EXACT_MATCH',
                      'final_transaction_state': 'COMPLETE',
                      'recovery_request_id': recovery_id,
                      'recovery_classification': recovery_classification})
    sp = folder / 'successor-manifest.json'
    write_json(sp, successor)
    new_state = finalize_success(active, request_id=rid, last_operation={
        'operation': OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE,
        'request_id': rid, 'school_key': SCHOOL, 'protected_main_sha': live_main,
        'target_branch': request['target_branch'],
        'target_predecessor_sha': request['target_sha'],
        'target_sha': writeahead['prepared_commit_sha'],
        'successor_manifest_path': sp.as_posix(),
        'successor_manifest_sha256': sha256_file(sp),
        'integration_freeze_sha256': request['integration_freeze_sha256'],
        'semantic_snapshot_sha256': request['semantic_snapshot_sha256'],
        'fresh_runner_verification': 'PENDING',
        'remote_stage2_registered_key_rebase_equivalence': 'PENDING'})
    if recovery_id and recovery_id not in new_state['consumed_request_ids']:
        new_state['consumed_request_ids'].append(recovery_id)
    write_json(STATE_PATH, new_state)
    return commit_control(expected_remote, 'finalize guarded registered key rebase ' + rid,
                          [STATE_PATH, folder, *(extra_paths or [])])


def run_key_rebase(state: dict, request: dict, request_bytes: bytes,
                   request_commit: str, predecessor_commit: str, live_main: str) -> None:
    authority = _scope(request, state, predecessor_commit)
    branch = request['target_branch']
    predecessor = request['target_sha']
    if remote_head(ROOT, branch) != predecessor:
        raise Stop('KEY_REBASE_TARGET_HEAD_MOVED')
    active = begin_request(state, request, sha256_bytes(request_bytes),
                           run_id=os.getenv('GITHUB_RUN_ID', 'local'),
                           run_attempt=os.getenv('GITHUB_RUN_ATTEMPT', '1'),
                           request_commit=request_commit)
    write_json(STATE_PATH, active)
    archived = Path('.remote-implementation/requests') / request['request_id'] / 'request.json'
    archived.parent.mkdir(parents=True, exist_ok=True)
    archived.write_bytes(request_bytes)
    lock_commit = commit_control(request_commit,
        'acquire registered key-rebase global lock ' + request['request_id'],
        [STATE_PATH, archived])
    active = bind_lock_commit(active, lock_commit)
    write_json(STATE_PATH, active)
    lock_bound = commit_control(lock_commit,
        'bind registered key-rebase global lock ' + request['request_id'], [STATE_PATH])
    worktree = add_existing_onboarding_worktree(branch, predecessor, SCHOOL)
    prepared = _candidate(worktree, predecessor, authority['freeze_bytes'])
    if remote_head(ROOT, branch) != predecessor:
        raise Stop('KEY_REBASE_TARGET_MOVED_BEFORE_WRITEAHEAD')
    valid = run([sys.executable, 'tools/validate_data.py'], cwd=worktree, check=False)
    if valid.returncode:
        raise Stop('KEY_REBASE_REPOSITORY_VALIDATION_FAILED:' + valid.stdout[-800:])
    DIAG.mkdir(parents=True, exist_ok=True)
    (DIAG / 'key-rebase-validate.log').write_text(valid.stdout)
    assert live_main == remote_head(ROOT, 'main'), 'KEY_REBASE_PROTECTED_MAIN_MOVED'

    folder = Path('.remote-implementation/writeahead') / SCHOOL / request['request_id']
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'integration-freeze.json').write_bytes(authority['freeze_bytes'])
    (folder / 'census-checkpoint-manifest.json').write_bytes(authority['census_manifest_bytes'])
    write_json(folder / 'field-level-proof.json', prepared['field_level_proof'])
    write_json(folder / 'semantic-drift-proof.json', {
        'before': prepared['semantic_drift_before'], 'after': prepared['semantic_drift_after']})
    sidecars = {p: sha256_file(folder / p) for p in (
        'integration-freeze.json', 'census-checkpoint-manifest.json',
        'field-level-proof.json', 'semantic-drift-proof.json')}
    ahead = {'schema_version': 1, 'kind': 'REMOTE_IMPLEMENTATION_WRITEAHEAD',
             'operation': OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE,
             'request_id': request['request_id'],
             'request_sha256': sha256_bytes(request_bytes),
             'school_key': SCHOOL, 'global_lock_commit': lock_commit,
             'protected_main_sha': live_main, 'target_branch': branch,
             'expected_target_predecessor_sha': predecessor,
             'stage2_census_checkpoint_path': request['stage2_census_checkpoint']['path'],
             'stage2_census_checkpoint_sha256': CENSUS_SHA256,
             'integration_freeze_sha256': request['integration_freeze_sha256'],
             'semantic_snapshot_sha256': request['semantic_snapshot_sha256'],
             'ruling_url': RULING_URL, 'case': GAME_ID,
             'allowed_paths': list(ALLOWED_PATHS),
             'changed_paths': prepared['changed_paths'],
             'changed_file_sha256': prepared['changed_file_sha256'],
             'prepared_commit_sha': prepared['prepared_commit_sha'],
             'prepared_tree_sha': prepared['prepared_tree_sha'],
             'prepared_parent_sha': prepared['prepared_parent_sha'],
             'field_level_proof_sha256': sidecars['field-level-proof.json'],
             'semantic_drift_before': prepared['semantic_drift_before'],
             'semantic_drift_after': prepared['semantic_drift_after'],
             'sidecars': sidecars, 'repository_validation': 'PASS',
             'mutation_state': 'PREPARED_NOT_PUBLISHED'}
    apath = folder / 'writeahead-manifest.json'
    write_json(apath, ahead)
    ahead_sha = sha256_file(apath)
    active['transaction_state'] = 'PREPARED_NOT_PUBLISHED'
    active['active_writeahead_path'] = apath.as_posix()
    active['active_writeahead_sha256'] = ahead_sha
    active['active_prepared_commit_sha'] = prepared['prepared_commit_sha']
    active['active_prepared_tree_sha'] = prepared['prepared_tree_sha']
    write_json(STATE_PATH, active)
    writeahead_commit = commit_control(lock_bound,
        'publish registered key-rebase write-ahead ' + request['request_id'],
        [STATE_PATH, folder])
    active['active_writeahead_commit'] = writeahead_commit
    write_json(STATE_PATH, active)
    writeahead_bound = commit_control(writeahead_commit,
        'bind registered key-rebase write-ahead ' + request['request_id'], [STATE_PATH])
    if live_main != remote_head(ROOT, 'main'):
        raise Stop('KEY_REBASE_PROTECTED_MAIN_MOVED_BEFORE_CAS')
    publish_ref_cas(ROOT, branch=branch,
        prepared_commit=prepared['prepared_commit_sha'], expected_predecessor=predecessor)
    if remote_head(ROOT, branch) != prepared['prepared_commit_sha']:
        raise Stop('KEY_REBASE_PUBLICATION_CAS_UNCERTAIN')
    commit = _finalize(active, request, request_bytes, live_main, ahead,
                       apath.as_posix(), ahead_sha, writeahead_commit,
                       writeahead_bound)
    print('REGISTERED KEY REBASE COMPLETE; fresh proof pending; commit=' + commit)


def _read_bound_successor(request: dict, control_head: str, *,
                          base_sha: str | None = None, require_verified: bool = False) -> dict:
    ref = request.get('stage2_current_program_key_rebase_successor') or {}
    path = str(ref.get('path') or '')
    if not path or not str(ref.get('sha256') or ''):
        raise Stop('KEY_REBASE_SUCCESSOR_NOT_BOUND')
    raw = git_show_bytes(control_head, path)
    if digest(raw) != ref['sha256']:
        raise Stop('KEY_REBASE_SUCCESSOR_HASH_MISMATCH')
    obj = json.loads(raw)
    if (obj.get('kind') != 'REMOTE_IMPLEMENTATION_STAGE2_REGISTERED_KEY_REBASE_SUCCESSOR'
            or obj.get('operation') != OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE
            or obj.get('school_key') != SCHOOL
            or obj.get('target_branch') != 'data/grand-canyon-onboarding'
            or obj.get('repository_validation') != 'PASS'
            or obj.get('final_transaction_state') != 'COMPLETE'
            or obj.get('publication_cas') != 'EXISTING_REF_CAS_PASS'):
        raise Stop('KEY_REBASE_SUCCESSOR_AUTHORITY_INVALID')
    if base_sha is not None and (obj.get('prepared_parent_sha') != base_sha
                                  or obj.get('expected_target_predecessor_sha') != base_sha):
        raise Stop('KEY_REBASE_SUCCESSOR_BASE_MISMATCH')
    if obj.get('integration_freeze_sha256') != request['integration_freeze_sha256'] \
            or obj.get('semantic_snapshot_sha256') != request['semantic_snapshot_sha256']:
        raise Stop('KEY_REBASE_SUCCESSOR_FREEZE_MISMATCH')
    before = _files_at(obj['prepared_parent_sha'])
    after = _files_at(obj['prepared_commit_sha'])
    registry = git_show_bytes(obj['prepared_parent_sha'], 'data/reference/programs.csv')
    require_exact_target_files(before, after, registry)
    parents = git('show', '-s', '--format=%P', obj['prepared_commit_sha']).stdout.strip().split()
    tree = git('rev-parse', obj['prepared_commit_sha'] + '^{tree}').stdout.strip()
    changed = sorted(git('diff', '--name-only', obj['prepared_parent_sha'],
                         obj['prepared_commit_sha']).stdout.splitlines())
    if (parents != [obj['prepared_parent_sha']]
            or tree != obj['prepared_tree_sha']
            or changed != sorted(ALLOWED_PATHS)
            or obj.get('changed_file_sha256') != {
                f'schools/{SCHOOL}/{name}': TARGET_HASHES[name] for name in SOURCE_HASHES}):
        raise Stop('KEY_REBASE_SUCCESSOR_TREE_OR_DIFF_MISMATCH')
    apath = obj['writeahead_manifest_path']
    raw_ahead = git_show_bytes(control_head, apath)
    if digest(raw_ahead) != obj.get('writeahead_manifest_sha256'):
        raise Stop('KEY_REBASE_WRITEAHEAD_HASH_MISMATCH')
    ahead = json.loads(raw_ahead)
    for field in ('request_id', 'request_sha256', 'school_key', 'operation',
                  'target_branch', 'prepared_commit_sha', 'prepared_tree_sha',
                  'prepared_parent_sha', 'expected_target_predecessor_sha',
                  'integration_freeze_sha256', 'semantic_snapshot_sha256',
                  'changed_paths', 'changed_file_sha256', 'field_level_proof_sha256'):
        if obj.get(field) != ahead.get(field):
            raise Stop('KEY_REBASE_WRITEAHEAD_SUCCESSOR_MISMATCH:' + field)
    for name, h in (ahead.get('sidecars') or {}).items():
        actual = git_show_bytes(control_head, (Path(apath).parent / name).as_posix())
        if digest(actual) != h:
            raise Stop('KEY_REBASE_WRITEAHEAD_SIDECAR_MISMATCH:' + name)
    if require_verified:
        p = Path('.remote-implementation/verifications') / SCHOOL / obj['request_id'] / 'registered-key-rebase-verification.json'
        v = json.loads(git_show_bytes(control_head, p.as_posix()))
        if (v.get('kind') != 'REMOTE_IMPLEMENTATION_STAGE2_REGISTERED_KEY_REBASE_VERIFICATION'
                or v.get('equivalence') != 'PASS'
                or v.get('target_sha') != obj['prepared_commit_sha']
                or v.get('target_tree_sha') != obj['prepared_tree_sha']
                or v.get('field_level_proof_sha256') != ahead['field_level_proof_sha256']):
            raise Stop('KEY_REBASE_INDEPENDENT_VERIFICATION_MISSING')
    return obj


def verify_key_rebase(live_main: str, control_head: str, state: dict) -> int:
    last = state.get('last_operation') or {}
    if last.get('fresh_runner_verification') == 'PASS':
        print('REGISTERED KEY REBASE FRESH EQUIVALENCE PASS (already verified)')
        return 0
    ref = {'stage2_current_program_key_rebase_successor': {
        'path': last['successor_manifest_path'], 'sha256': last['successor_manifest_sha256']},
        'integration_freeze_sha256': last['integration_freeze_sha256'],
        'semantic_snapshot_sha256': last['semantic_snapshot_sha256']}
    git('fetch', '--no-tags', 'origin', '+refs/heads/data/grand-canyon-onboarding:refs/remotes/origin/rebase-fresh-target')
    obj = _read_bound_successor(ref, control_head, require_verified=False)
    if (obj.get('protected_main_sha') != live_main
            or remote_head(ROOT, obj['target_branch']) != obj['prepared_commit_sha']):
        raise Stop('KEY_REBASE_FRESH_MAIN_OR_TARGET_MOVED')
    archive = git_show_bytes(control_head,
        f'.remote-implementation/requests/{obj["request_id"]}/request.json')
    if digest(archive) != obj['request_sha256']:
        raise Stop('KEY_REBASE_FRESH_REQUEST_HASH_MISMATCH')
    original_request = json.loads(archive)
    ahead = json.loads(git_show_bytes(control_head, obj['writeahead_manifest_path']))
    control_folder = Path(obj['writeahead_manifest_path']).parent
    freeze = git_show_bytes(control_head, (control_folder / 'integration-freeze.json').as_posix())
    if digest(freeze) != obj['integration_freeze_sha256']:
        raise Stop('KEY_REBASE_FRESH_FREEZE_HASH_MISMATCH')
    source_worktree = add_existing_onboarding_worktree(obj['target_branch'],
                                                       obj['prepared_commit_sha'], SCHOOL)
    drift = _semantic_pass(source_worktree, freeze, 'FRESH')
    validation = run([sys.executable, 'tools/validate_data.py'], cwd=source_worktree, check=False)
    if validation.returncode:
        raise Stop('KEY_REBASE_FRESH_REPOSITORY_VALIDATION_FAILED')
    proof = require_exact_target_files(_files_at(obj['prepared_parent_sha']),
                                       _files_at(obj['prepared_commit_sha']),
                                       git_show_bytes(obj['prepared_parent_sha'], 'data/reference/programs.csv'))
    stored = json.loads(git_show_bytes(control_head,
        (control_folder / 'field-level-proof.json').as_posix()))
    if stored != proof or ahead['field_level_proof_sha256'] != digest(git_show_bytes(
            control_head, (control_folder / 'field-level-proof.json').as_posix())):
        raise Stop('KEY_REBASE_FRESH_FIELD_PROOF_MISMATCH')
    folder = Path('.remote-implementation/verifications') / SCHOOL / obj['request_id']
    write_json(folder / 'registered-key-rebase-verification.json', {
        'schema_version': 1, 'kind': 'REMOTE_IMPLEMENTATION_STAGE2_REGISTERED_KEY_REBASE_VERIFICATION',
        'request_id': obj['request_id'], 'school_key': SCHOOL,
        'protected_main_sha': live_main, 'target_sha': obj['prepared_commit_sha'],
        'target_tree_sha': obj['prepared_tree_sha'],
        'field_level_proof_sha256': ahead['field_level_proof_sha256'],
        'integration_freeze_sha256': obj['integration_freeze_sha256'],
        'semantic_snapshot_sha256': obj['semantic_snapshot_sha256'],
        'semantic_drift': drift['status'], 'repository_validation': 'PASS',
        'equivalence': 'PASS'})
    state2 = read_json(STATE_PATH)
    validate_control_state(state2)
    current = state2.get('last_operation') or {}
    if current.get('operation') != OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE \
            or current.get('request_id') != obj['request_id']:
        raise Stop('KEY_REBASE_FRESH_CONTROL_MOVED')
    current['fresh_runner_verification'] = 'PASS'
    current['remote_stage2_registered_key_rebase_equivalence'] = 'PASS'
    state2['last_operation'] = current
    write_json(STATE_PATH, state2)
    commit = commit_control(control_head,
        'persist fresh registered key-rebase verification ' + obj['request_id'],
        [STATE_PATH, folder])
    print('REGISTERED KEY REBASE FRESH EQUIVALENCE PASS commit=' + commit)
    return 0


def verify_registered_key_successor(request: dict, control_head: str,
                                    *, phase0_sha: str) -> dict:
    obj = _read_bound_successor(request, control_head,
                                base_sha=phase0_sha, require_verified=True)
    return {'target_sha': obj['prepared_commit_sha'], 'successor': obj}


def finalize_recovered_key_rebase(active: dict, request: dict, request_bytes: bytes,
                                   live_main: str, ahead: dict, ahead_path: str,
                                   ahead_sha: str, ahead_commit: str,
                                   expected_control: str, recovery_id: str,
                                   recovery_classification: str, recovery_dir: Path) -> str:
    _read_bound = require_exact_target_files(
        _files_at(ahead['expected_target_predecessor_sha']),
        _files_at(ahead['prepared_commit_sha']),
        git_show_bytes(ahead['expected_target_predecessor_sha'], 'data/reference/programs.csv'))
    if digest(git_show_bytes(expected_control, (Path(ahead_path).parent / 'field-level-proof.json').as_posix())) != ahead['field_level_proof_sha256']:
        raise Stop('KEY_REBASE_RECOVERY_FIELD_PROOF_MISMATCH')
    return _finalize(active, request, request_bytes, live_main, ahead,
                     ahead_path, ahead_sha, ahead_commit, expected_control,
                     recovery_id=recovery_id, recovery_classification=recovery_classification,
                     extra_paths=[recovery_dir])
