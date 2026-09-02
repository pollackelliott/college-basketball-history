import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import opponent_identity_transaction as tx

CANONICAL_HEADERS = [
    'canonical_game_id','season_label','game_date','date_precision','team_a_key','team_b_key',
    'team_a_score','team_b_score','result_winner_team_key','overtime_periods','site_type',
    'designated_home_team_key','venue_key','venue_id','site_city','site_state','game_type',
    'postseason_round','administrative_status','administrative_note','canonical_status','notes',
]
ASSERTION_HEADERS = ['assertion_id','canonical_game_id','source_program_key','source_game_id','normalized_opponent_key']
OPPONENT_HEADERS = ['source_program_key','source_opponent_label','canonical_opponent_key','canonical_opponent_name','current_d1','games_with_source_label','first_season','last_season']
SOURCE_HEADERS = ['source_game_id','source_program_key','season_label','game_date','source_opponent_label','normalized_opponent_name','normalized_opponent_key','opponent_current_d1','team_score','opponent_score','played_result','overtime_periods','raw_text']
PROGRAM_HEADERS = ['program_key','program_name','display_name','current_d1','public_page_enabled']
ALIAS_HEADERS = tx.remediation.REQUIRED_ALIAS_FIELDS


def canonical(game_id, opponent_key, *, date='2005-01-18', a_score='70', b_score='54', overtime='0', venue='', city='', status='PROVISIONAL'):
    return [
        game_id,'2004-2005',date,'EXACT','oklahoma',opponent_key,a_score,b_score,'oklahoma',
        overtime,'TEAM_B_HOME',opponent_key,venue,'VEN-1' if venue else '',city,'TX' if city else '',
        'REGULAR_SEASON','','','',status,''
    ]


class OpponentIdentityTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        for path in [
            'data/reference','data/canonical','data/evidence','data/reconciliation',
            'schools/oklahoma',
        ]:
            (self.repo / path).mkdir(parents=True, exist_ok=True)

        self._write(self.repo/'data/reference/programs.csv', PROGRAM_HEADERS, [
            ['oklahoma','Oklahoma','Oklahoma','Yes','Yes'],
            ['texas-a-m','Texas A&M','Texas A&M','Yes','Yes'],
        ])
        self._write(self.repo/'data/reference/program-names.csv', ALIAS_HEADERS, [])
        self._write(self.repo/'data/canonical/games.csv', CANONICAL_HEADERS, [
            # Survivor intentionally has the numerically larger ID. The transaction must
            # preserve the affected stale-key row, not choose the lowest number.
            canonical('CBBG-99','texas-a-and-m',b_score='56'),
            canonical('CBBG-10','texas-a-m',b_score='54',venue='reed-arena',city='College Station'),
        ])
        self._write(self.repo/'data/evidence/game-assertions.csv', ASSERTION_HEADERS, [
            ['A1','CBBG-99','oklahoma','OKL-1','texas-a-and-m'],
            ['A2','CBBG-10','texas-a-m','TAM-1','oklahoma'],
        ])
        self._write(self.repo/'data/reconciliation/discrepancies.csv', tx.DISCREPANCY_FIELDS, [
            ['DISC-000001','CBBG-10','site_type','texas-a-m','TEAM_B_HOME','','','TEAM_B_HOME','RESOLVED','existing','existing'],
        ])
        self._write(self.repo/'schools/oklahoma/opponents.csv', OPPONENT_HEADERS, [
            ['oklahoma','Texas A&M','texas-a-and-m','Texas A&M','No','1','2004-2005','2004-2005'],
        ])
        self._write(self.repo/'schools/oklahoma/source-games.csv', SOURCE_HEADERS, [
            ['OKL-1','oklahoma','2004-2005','2005-01-18','Texas A&M','Texas A&M','texas-a-and-m','No','70','56','W','0','at Texas A&M W 70-56'],
        ])
        self.decisions = self.repo/'decisions.csv'
        self._write(self.decisions, tx.remediation.REQUIRED_DECISION_FIELDS, [[
            'oklahoma','Texas A&M','texas-a-and-m','texas-a-m','MERGE_TO_PROGRAM','verified lineage','https://example.test'
        ]])
        self.resolutions = self.repo/'resolutions.json'
        self._resolution_file([
            {
                'resolution_id':'OIR-1',
                'kind':'SAME_DATE_IDENTITY_CONFLICT',
                'survivor_canonical_game_id':'CBBG-99',
                'absorbed_canonical_game_id':'CBBG-10',
                'canonical_values':{'team_b_score':'54'},
                'resolution_basis':'two official contemporary sources agree',
                'evidence_urls':['https://example.test/a'],
                'discrepancies':[{
                    'field_name':'score','source_a_program_key':'oklahoma','source_a_value':'70-56',
                    'source_b_program_key':'texas-a-m','source_b_value':'70-54','canonical_value':'70-54',
                    'status':'RESOLVED','resolution_basis':'contemporary sources agree','notes':'later assertion retained'
                }]
            }
        ])

        self.base_plan = {
            'plan_sha256':'base-plan',
            'global_key_map':{'texas-a-and-m':'texas-a-m'},
            'affected_canonical_game_ids':{'texas-a-and-m->texas-a-m':['CBBG-99']},
            'blockers':['program-key replacement exposes 1 exact-date canonical collision candidate(s); these require one-real-game reconciliation'],
            'warnings':[],
            'decisions':[{
                'decision_id':'OID-1','decision':'MERGE_TO_PROGRAM','source_program_key':'oklahoma',
                'source_opponent_label':'Texas A&M','from_program_key':'texas-a-and-m','to_program_key':'texas-a-m',
                'source_game_ids':['OKL-1'],
            }],
        }
        self.audit = {
            'audit_sha256':'audit',
            'collision_groups':[{
                'kind':'SAME_DATE_IDENTITY_CONFLICT',
                'canonical_game_ids':['CBBG-10','CBBG-99'],
            }],
            'unpaired_affected_game_ids':[],
        }
        self.patches = [
            mock.patch.object(tx.remediation,'build_plan',return_value=self.base_plan),
            mock.patch.object(tx.remediation,'load_programs',return_value=({
                'oklahoma':{'display_name':'Oklahoma'},
                'texas-a-m':{'display_name':'Texas A&M'},
            }, {'oklahoma','texas-a-m'}, {'oklahoma','texas-a-m'})),
            mock.patch.object(tx.collision_audit,'audit_rows',return_value=self.audit),
        ]
        for patcher in self.patches:
            patcher.start()

    def tearDown(self):
        for patcher in reversed(self.patches):
            patcher.stop()
        self.temp.cleanup()

    def _write(self,path,headers,rows):
        with path.open('w',encoding='utf-8',newline='') as handle:
            writer=csv.writer(handle)
            writer.writerow(headers)
            writer.writerows(rows)

    def _read(self,path):
        with path.open(encoding='utf-8',newline='') as handle:
            return list(csv.DictReader(handle))

    def _resolution_file(self,rows):
        self.resolutions.write_text(json.dumps({'schema_version':1,'resolutions':rows}),encoding='utf-8')

    def test_plan_preserves_affected_survivor_not_lowest_id(self):
        plan=tx.build_transaction_plan(self.repo,self.decisions,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        pair=plan['canonical_pairs'][0]
        self.assertEqual(pair['survivor_canonical_game_id'],'CBBG-99')
        self.assertEqual(pair['absorbed_canonical_game_id'],'CBBG-10')
        self.assertEqual(pair['final_canonical_values']['team_b_key'],'texas-a-m')
        self.assertEqual(pair['final_canonical_values']['team_b_score'],'54')
        self.assertEqual(pair['final_canonical_values']['venue_key'],'reed-arena')
        self.assertEqual(pair['final_canonical_values']['site_city'],'College Station')
        self.assertEqual(len(plan['new_discrepancies']),1)

    def test_material_conflict_requires_explicit_resolution(self):
        self._resolution_file([])
        plan=tx.build_transaction_plan(self.repo,self.decisions,self.resolutions)
        self.assertTrue(any('requires explicit resolution' in item for item in plan['blockers']))

    def test_blank_explicit_canonical_value_is_rejected(self):
        payload=json.loads(self.resolutions.read_text())
        payload['resolutions'][0]['canonical_values']={'team_b_score':''}
        self.resolutions.write_text(json.dumps(payload))
        with self.assertRaises(tx.OpponentIdentityTransactionError):
            tx.build_transaction_plan(self.repo,self.decisions,self.resolutions)

    def test_apply_redirects_assertions_retargets_discrepancies_and_preserves_raw(self):
        plan=tx.build_transaction_plan(self.repo,self.decisions,self.resolutions)
        result=tx.apply_transaction(self.repo,self.decisions,self.resolutions,plan['plan_sha256'],run_validation=False)
        self.assertEqual(result['canonical_games_absorbed'],1)
        games=self._read(self.repo/'data/canonical/games.csv')
        self.assertEqual([row['canonical_game_id'] for row in games],['CBBG-99'])
        self.assertEqual(games[0]['team_b_key'],'texas-a-m')
        self.assertEqual(games[0]['team_b_score'],'54')
        self.assertEqual(games[0]['venue_key'],'reed-arena')

        assertions=self._read(self.repo/'data/evidence/game-assertions.csv')
        self.assertEqual(len(assertions),2)
        self.assertEqual({row['canonical_game_id'] for row in assertions},{'CBBG-99'})
        self.assertFalse(any(row['normalized_opponent_key']=='texas-a-and-m' for row in assertions))

        discrepancies=self._read(self.repo/'data/reconciliation/discrepancies.csv')
        self.assertEqual(len(discrepancies),2)
        self.assertTrue(all(row['canonical_game_id']=='CBBG-99' for row in discrepancies))
        self.assertEqual(discrepancies[-1]['status'],'RESOLVED')

        source=self._read(self.repo/'schools/oklahoma/source-games.csv')[0]
        self.assertEqual(source['source_opponent_label'],'Texas A&M')
        self.assertEqual(source['raw_text'],'at Texas A&M W 70-56')
        self.assertEqual(source['opponent_score'],'56')
        self.assertEqual(source['normalized_opponent_key'],'texas-a-m')
        opponent=self._read(self.repo/'schools/oklahoma/opponents.csv')[0]
        self.assertEqual(opponent['canonical_opponent_key'],'texas-a-m')
        self.assertEqual(opponent['current_d1'],'Yes')

    def test_unpaired_date_error_can_use_explicit_counterpart(self):
        self.audit={'audit_sha256':'audit2','collision_groups':[],'unpaired_affected_game_ids':['CBBG-99']}
        tx.collision_audit.audit_rows.return_value=self.audit
        payload=json.loads(self.resolutions.read_text())
        row=payload['resolutions'][0]
        row['kind']='EXPLICIT_COUNTERPART'
        row['canonical_values']={'game_date':'2005-01-18','team_b_score':'54'}
        self.resolutions.write_text(json.dumps(payload))
        plan=tx.build_transaction_plan(self.repo,self.decisions,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        self.assertEqual(plan['canonical_pairs'][0]['kind'],'EXPLICIT_COUNTERPART')

    def test_hash_mismatch_refuses_before_write(self):
        before=(self.repo/'data/canonical/games.csv').read_bytes()
        with self.assertRaises(tx.OpponentIdentityTransactionError):
            tx.apply_transaction(self.repo,self.decisions,self.resolutions,'wrong',run_validation=False)
        self.assertEqual((self.repo/'data/canonical/games.csv').read_bytes(),before)

    def test_validation_failure_rolls_back_every_touched_file(self):
        plan=tx.build_transaction_plan(self.repo,self.decisions,self.resolutions)
        paths=[
            self.repo/'data/canonical/games.csv',self.repo/'data/evidence/game-assertions.csv',
            self.repo/'data/reconciliation/discrepancies.csv',self.repo/'schools/oklahoma/opponents.csv',
            self.repo/'schools/oklahoma/source-games.csv',
        ]
        before={path:path.read_bytes() for path in paths}
        with mock.patch.object(tx,'_run_validation',side_effect=tx.OpponentIdentityTransactionError('boom')):
            with self.assertRaises(tx.OpponentIdentityTransactionError):
                tx.apply_transaction(self.repo,self.decisions,self.resolutions,plan['plan_sha256'],run_validation=True)
        self.assertEqual({path:path.read_bytes() for path in paths},before)


if __name__=='__main__':
    unittest.main()
