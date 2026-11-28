"""Fail-closed adversarial tests for the issue #736 registered-key case."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import remote_implementation_registered_key_rebase as rebase


def serial(fields: list[str], rows: list[dict[str, str]]) -> bytes:
    f = io.StringIO(newline='')
    w = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    w.writeheader()
    w.writerows(rows)
    return f.getvalue().encode('utf-8')


class PureExactCaseTests(unittest.TestCase):
    def setUp(self):
        self.registry = (b'program_key,current_d1,display_name,city\n'
                         b'south-carolina-upstate,Yes,USC Upstate,Spartanburg\n')
        opp_header = ['source_opponent_label', 'canonical_opponent_key',
                      'canonical_opponent_name', 'current_d1', 'audit_note']
        src_header = ['source_game_id', 'normalized_opponent_key',
                      'normalized_opponent_name', 'source_opponent_label',
                      'game_date', 'team_score', 'opponent_score', 'played_result',
                      'curated_site_type', 'curated_game_type', 'city', 'raw_text']
        opponents = [{h: '' for h in opp_header} for _ in range(491)]
        games = [{h: '' for h in src_header} for _ in range(2147)]
        for i, row in enumerate(opponents):
            row.update(source_opponent_label=f'Example-{i}',
                       canonical_opponent_key=f'unique-{i}',
                       canonical_opponent_name=f'Example-{i}',current_d1='No')
        for i, row in enumerate(games):
            row.update(source_game_id=f'example-{i}',normalized_opponent_key=f'unique-{i}')
        opponents[437].update(source_opponent_label='USC-Spartanburg',
                              canonical_opponent_key='usc-upstate',
                              canonical_opponent_name='USC Upstate', current_d1='Yes')
        games[1497].update(source_game_id=rebase.GAME_ID,
            normalized_opponent_key='usc-upstate',normalized_opponent_name='USC Upstate',
            source_opponent_label='USC-Spartanburg',game_date='1990-03-15',
            team_score='69',opponent_score='75',played_result='L',
            curated_site_type='NEUTRAL',curated_game_type='POSTSEASON',city='Kansas City')
        self.opp = serial(opp_header, opponents)
        self.src = serial(src_header, games)
        n=b',usc-upstate,'
        self.newopp=self.opp.replace(n,b',south-carolina-upstate,',1)
        self.newsrc=self.src.replace(n,b',south-carolina-upstate,',1)
        self.hashes={k:rebase.digest(v) for k,v in [('opponents.csv',self.opp),('source-games.csv',self.src)]}
        self.after_hashes={k:rebase.digest(v) for k,v in [('opponents.csv',self.newopp),('source-games.csv',self.newsrc)]}
        self.hash_patch=patch.multiple(rebase,SOURCE_HASHES=self.hashes,TARGET_HASHES=self.after_hashes)
        self.hash_patch.start();self.addCleanup(self.hash_patch.stop)

    def apply(self, opp=None, src=None, registry=None):
        return rebase.make_candidate(opp if opp is not None else self.opp,
            src if src is not None else self.src,
            registry if registry is not None else self.registry)

    def test_positive_exact_two_cells(self):
        after,proof=self.apply()
        self.assertEqual(after,{'opponents.csv':self.newopp,'source-games.csv':self.newsrc})
        self.assertEqual(len(proof['field_changes']),2)
        self.assertEqual([x['row'] for x in proof['field_changes']],[439,1499])
        self.assertEqual(rebase.require_exact_target_files(
            {'opponents.csv':self.opp,'source-games.csv':self.src},after,self.registry),proof)

    def test_registry_wrong_key_flag_city_and_duplicate(self):
        for payload in (
            self.registry.replace(b',Yes,',b',No,'),
            self.registry.replace(b'Spartanburg',b'Greenville'),
            self.registry.replace(b'south-carolina-upstate',b'usc-upstate'),
            self.registry + b'south-carolina-upstate,Yes,USC Upstate,Spartanburg\n',
            self.registry + b'usc-upstate,Yes,USC Upstate,Spartanburg\n',
        ):
            with self.subTest(payload=payload[-50:]):
                with self.assertRaises(rebase.KeyRebaseStop):self.apply(registry=payload)

    def test_multiple_missing_or_colliding_target_rows(self):
        variants=(
            self.opp.replace(b',usc-upstate,',b',bad-key,'),
            self.opp.replace(b',unique-1,',b',south-carolina-upstate,'),
            self.opp.replace(b',unique-1,',b',usc-upstate,'),
        )
        for v in variants:
            with self.subTest(hash=hashlib.sha256(v).hexdigest()):
                with self.assertRaises(rebase.KeyRebaseStop): self.apply(opp=v)

    def test_multiple_missing_or_wrong_game(self):
        variants=(
            self.src.replace(b',usc-upstate,',b',not-usc-upstate,'),
            self.src.replace(b',unique-1,',b',usc-upstate,'),
            self.src.replace(b',1990-03-15,',b',1990-03-16,'),
            self.src.replace(b',69,75,',b',69,76,'),
        )
        for v in variants:
            with self.subTest(hash=hashlib.sha256(v).hexdigest()):
                with self.assertRaises(rebase.KeyRebaseStop):self.apply(src=v)

    def test_forged_file_hash_and_extra_field_changes(self):
        after,proof=self.apply()
        self.assertEqual(len(proof['field_changes']),2)
        modified=dict(after)
        modified['source-games.csv']=modified['source-games.csv'].replace(b',69,75,',b',69,76,')
        with self.assertRaises(rebase.KeyRebaseStop):
            rebase.verify_diff({'opponents.csv':self.opp,'source-games.csv':self.src},modified)
        modified=dict(after)
        modified['extra.csv']=b''
        with self.assertRaises(rebase.KeyRebaseStop):
            rebase.verify_diff({'opponents.csv':self.opp,'source-games.csv':self.src},modified)

    def test_complete_census_validates_other_blockers(self):
        keys=[f'test{i}' for i in range(39)]
        blockers=[rebase.BLOCKER]+[f'historical opponent display conflict: {k}: ["a", "b"]' for k in keys]
        status={'status':'BLOCKED','blockers':blockers,
                'semantic_drift':{'status':'PASS'},
                'preflight':{'blocker_count':40,'warning_count':0,'decision_count':0}}
        census={'status':'PREFLIGHT_BLOCKED','preflight':{'blocker_count':40}}
        self.assertEqual(rebase.require_census(status,census), sorted(keys))
        for change in ('unexpected','duplicate','warning','decision','drift'):
            altered={'status':status['status'], 'blockers':list(blockers),
                     'semantic_drift':dict(status['semantic_drift']),
                     'preflight':dict(status['preflight'])}
            if change=='unexpected':altered['blockers'][-1]='other blocker: wrong'
            if change=='duplicate':altered['blockers'][-1]=altered['blockers'][-2]
            if change=='warning':altered['preflight']['warning_count']=1
            if change=='decision':altered['preflight']['decision_count']=1
            if change=='drift':altered['semantic_drift']['status']='FAIL'
            with self.subTest(change=change):
                with self.assertRaises(rebase.KeyRebaseStop):rebase.require_census(altered,census)

class GuardedTransactionBoundaryTests(unittest.TestCase):
    """Exercise transaction stop paths, not only the pure CSV transformer."""

    def setUp(self):
        import remote_implementation_control as control
        import remote_implementation_stage2_key_rebase as transaction
        self.control = control
        self.tx = transaction
        self.request = {
            'schema_version': 1,
            'request_id': 'grand-canyon-stage2-key-rebase-0001',
            'school_key': 'grand-canyon',
            'operation': control.OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE,
            'target_branch': 'data/grand-canyon-onboarding',
            'target_sha': '1' * 40,
            'expected_protected_main_sha': '2' * 40,
            'integration_freeze_sha256': '3' * 64,
            'semantic_snapshot_sha256': '4' * 64,
            'stage2_census_checkpoint': {
                'path': '.remote-implementation/checkpoints/grand-canyon/grand-canyon-stage2-census-0001/checkpoint-manifest.json',
                'sha256': rebase.CENSUS_SHA256,
            },
        }

    def test_moved_target_refuses_lock_and_publication(self):
        tx = self.tx
        with patch.object(tx, '_scope', return_value={'freeze_bytes': b'baseline'}), \
             patch.object(tx, 'remote_head', return_value='unexpected-head'), \
             patch.object(tx, 'begin_request') as begin, \
             patch.object(tx, 'publish_ref_cas') as publish:
            with self.assertRaisesRegex(tx.Stop, 'KEY_REBASE_TARGET_HEAD_MOVED'):
                tx.run_key_rebase(self.control.initial_control_state(), self.request,
                                  b'request', 'a'*40, 'b'*40, '2'*40)
            begin.assert_not_called()
            publish.assert_not_called()

    def test_occupied_global_lock_refuses_second_mutation(self):
        tx = self.tx
        active = self.control.begin_request(
            self.control.initial_control_state(), self.request, '5'*64,
            run_id='1', run_attempt='1', request_commit='a'*40)
        with patch.object(tx, '_scope', return_value={'freeze_bytes': b'baseline'}), \
             patch.object(tx, 'remote_head', return_value=self.request['target_sha']), \
             patch.object(tx, 'commit_control') as commit, \
             patch.object(tx, 'publish_ref_cas') as publish:
            with self.assertRaisesRegex(self.control.RemoteImplementationError,
                                        'GLOBAL_IMPLEMENTATION_LOCK_OCCUPIED'):
                tx.run_key_rebase(active, self.request, b'request',
                                  'a'*40, 'b'*40, '2'*40)
            commit.assert_not_called()
            publish.assert_not_called()

    def _prepare_to_publication(self, *, main_moved=False):
        """Mock only Git/ref and prepared-worktree effects; use real write-ahead bytes."""
        import os
        import tempfile
        from contextlib import ExitStack
        from types import SimpleNamespace

        tx = self.tx
        with tempfile.TemporaryDirectory(prefix='gcu-guarded-cas-test-') as folder:
            with ExitStack() as stack:
                old_cwd = Path.cwd()
                os.chdir(folder)
                stack.callback(os.chdir, old_cwd)
                stack.enter_context(patch.object(tx, 'STATE_PATH', Path('control-state.json')))
                stack.enter_context(patch.object(tx, 'DIAG', Path('diagnostics')))
                stack.enter_context(patch.object(tx, '_scope', return_value={
                    'freeze_bytes': b'baseline', 'census_manifest_bytes': b'census'}))
                stack.enter_context(patch.object(tx, 'add_existing_onboarding_worktree',
                                                  return_value=Path(folder)))
                stack.enter_context(patch.object(tx, '_candidate', return_value={
                    'prepared_commit_sha': '6'*40,
                    'prepared_tree_sha': '7'*40,
                    'prepared_parent_sha': self.request['target_sha'],
                    'changed_paths': list(rebase.ALLOWED_PATHS),
                    'changed_file_sha256': {'schools/grand-canyon/'+name: sha
                                             for name, sha in rebase.TARGET_HASHES.items()},
                    'field_level_proof': {'allowed_paths': list(rebase.ALLOWED_PATHS),
                                          'field_changes': [1, 2]},
                    'semantic_drift_before': {'status': 'PASS', 'changes': []},
                    'semantic_drift_after': {'status': 'PASS', 'changes': []},
                }))
                stack.enter_context(patch.object(tx, 'run', return_value=SimpleNamespace(
                    returncode=0, stdout='VALIDATION=PASS')))
                commit = stack.enter_context(patch.object(tx, 'commit_control',
                    side_effect=['a'*40, 'b'*40, 'c'*40, 'd'*40]))
                original_target = self.request['target_sha']
                def head(_root, branch):
                    if branch == 'main':
                        return 'm'*40 if main_moved else '2'*40
                    return original_target
                stack.enter_context(patch.object(tx, 'remote_head', side_effect=head))
                publish = stack.enter_context(patch.object(tx, 'publish_ref_cas',
                    side_effect=tx.Stop('SIMULATED_PUBLICATION_CAS_FAILED')))
                finalize = stack.enter_context(patch.object(tx, '_finalize'))
                with self.assertRaises(tx.Stop) as failure:
                    tx.run_key_rebase(self.control.initial_control_state(),
                        self.request, b'request', 'a'*40, 'b'*40, '2'*40)
                expected_error = ('KEY_REBASE_PROTECTED_MAIN_MOVED'
                                  if main_moved else 'SIMULATED_PUBLICATION_CAS_FAILED')
                self.assertIn(expected_error, str(failure.exception))
                self.assertEqual(commit.call_count, 4 if not main_moved else 2)
                if not main_moved:
                    manifest = Path('.remote-implementation/writeahead/grand-canyon/'
                                    'grand-canyon-stage2-key-rebase-0001/'
                                    'writeahead-manifest.json')
                    self.assertTrue(manifest.is_file(), 'CAS reached without durable writeahead')
                    self.assertEqual(json.loads(manifest.read_text())['mutation_state'],
                                     'PREPARED_NOT_PUBLISHED')
                publish.assert_called_once() if not main_moved else publish.assert_not_called()
                finalize.assert_not_called()

    def test_failed_publication_cas_preserves_writeahead(self):
        self._prepare_to_publication()

    def test_moved_main_aborts_before_lock_or_cas(self):
        self._prepare_to_publication(main_moved=True)

    def test_bad_fresh_successor_cannot_persist_pass(self):
        tx = self.tx
        state = self.control.initial_control_state()
        state['last_operation'] = {
            'operation': self.control.OP_STAGE2_CURRENT_PROGRAM_KEY_REBASE,
            'request_id': self.request['request_id'],
            'successor_manifest_path': '.remote-implementation/forged.json',
            'successor_manifest_sha256': 'f'*64,
            'integration_freeze_sha256': '3'*64,
            'semantic_snapshot_sha256': '4'*64,
            'fresh_runner_verification': 'PENDING',
        }
        with patch.object(tx, 'git', return_value=None), \
             patch.object(tx, '_read_bound_successor', side_effect=tx.Stop(
                 'KEY_REBASE_SUCCESSOR_HASH_MISMATCH')), \
             patch.object(tx, 'commit_control') as commit:
            with self.assertRaisesRegex(tx.Stop, 'KEY_REBASE_SUCCESSOR_HASH_MISMATCH'):
                tx.verify_key_rebase('2'*40, 'a'*40, state)
            commit.assert_not_called()


if __name__=='__main__':unittest.main()
