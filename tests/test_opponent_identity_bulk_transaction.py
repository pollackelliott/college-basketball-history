import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import opponent_identity_bulk_transaction as bulk
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


def game(gid, opponent, *, date='2000-01-01', a='alpha', a_score='70', b_score='60', site='TEAM_A_HOME', home='alpha', venue='', city='', notes=''):
    return [
        gid,'1999-2000',date,'EXACT' if date else 'SEASON',a,opponent,a_score,b_score,a,0,
        site,home,venue,'VEN-1' if venue else '',city,'ST' if city else '',
        'REGULAR_SEASON','','','', 'PROVISIONAL',notes,
    ]


class BulkOpponentIdentityTransactionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.repo = Path(self.temp.name)
        for path in ['data/reference','data/canonical','data/evidence','data/reconciliation','schools/alpha']:
            (self.repo/path).mkdir(parents=True,exist_ok=True)
        self._write(self.repo/'data/reference/programs.csv',PROGRAM_HEADERS,[
            ['alpha','Alpha','Alpha','Yes','Yes'],
            ['target','Target','Target','Yes','No'],
        ])
        self._write(self.repo/'data/reference/program-names.csv',tx.remediation.REQUIRED_ALIAS_FIELDS,[])
        self._write(self.repo/'data/reconciliation/discrepancies.csv',tx.DISC_FIELDS,[])
        self.manifest=self.repo/'manifest.csv'
        self.resolutions=self.repo/'resolutions.json'

    def tearDown(self):
        self.temp.cleanup()

    def _write(self,path,headers,rows):
        with path.open('w',encoding='utf-8',newline='') as handle:
            w=csv.writer(handle); w.writerow(headers); w.writerows(rows)

    def _read(self,path):
        with path.open(encoding='utf-8',newline='') as handle:
            return list(csv.DictReader(handle))

    def _manifest(self,*,label='Old Target',old='old-target',new='target',name='Target',current='Yes',decision='MERGE_TO_PROGRAM',games=1):
        self._write(self.manifest,bulk.MANIFEST_FIELDS,[[
            'alpha',label,old,new,name,current,decision,'owner reviewed identity','https://example.test'
        ]])
        self._write(self.repo/'schools/alpha/opponents.csv',OPPONENT_HEADERS,[[
            'alpha',label,old,label,'No',str(games),'1999-2000','1999-2000'
        ]])
        rows=[]
        for i in range(games):
            rows.append([
                f'SRC-{i+1}','alpha','1999-2000','',label,label,old,'No','','','W','0',f'raw {label} {i+1}'
            ])
        self._write(self.repo/'schools/alpha/source-games.csv',SOURCE_HEADERS,rows)

    def _resolution(self,pairs=None,distinct=None):
        self.resolutions.write_text(json.dumps({
            'schema_version':2,'resolutions':pairs or [],'retain_distinct':distinct or []
        }),encoding='utf-8')

    def test_in_place_remap_without_duplicate(self):
        self._manifest()
        self._resolution()
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[game('CBBG-1','old-target')])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[['A1','CBBG-1','alpha','SRC-1','old-target']])
        plan=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        self.assertEqual(plan['remap_only_canonical_game_ids'],['CBBG-1'])
        self.assertEqual(plan['absorbed_canonical_game_ids'],[])
        result=bulk.apply(self.repo,self.manifest,self.resolutions,plan['plan_sha256'],run_validation=False)
        self.assertEqual(result['canonical_games_remapped_in_place'],1)
        row=self._read(self.repo/'data/canonical/games.csv')[0]
        self.assertEqual(row['team_b_key'],'target')
        self.assertIn('in_place_remap=old-target->target',row['notes'])
        self.assertEqual(self._read(self.repo/'data/evidence/game-assertions.csv')[0]['normalized_opponent_key'],'target')
        self.assertEqual(self._read(self.repo/'schools/alpha/source-games.csv')[0]['raw_text'],'raw Old Target 1')

    def test_exact_collision_auto_absorbs_and_enriches(self):
        self._manifest()
        self._resolution()
        stale=game('CBBG-9','old-target',site='UNKNOWN',home='',venue='',city='')
        counterpart=game('CBBG-2','target',site='TEAM_B_HOME',home='target',venue='target-gym',city='Target City')
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[stale,counterpart])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[
            ['A1','CBBG-9','alpha','SRC-1','old-target'],['A2','CBBG-2','target','T-1','alpha']
        ])
        plan=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        self.assertEqual(len(plan['canonical_pairs']),1)
        self.assertEqual(plan['canonical_pairs'][0]['survivor_canonical_game_id'],'CBBG-9')
        self.assertEqual(plan['canonical_pairs'][0]['absorbed_canonical_game_id'],'CBBG-2')
        self.assertEqual(plan['canonical_pairs'][0]['final_canonical_values']['venue_key'],'target-gym')
        bulk.apply(self.repo,self.manifest,self.resolutions,plan['plan_sha256'],run_validation=False)
        rows=self._read(self.repo/'data/canonical/games.csv')
        self.assertEqual([r['canonical_game_id'] for r in rows],['CBBG-9'])
        self.assertEqual(rows[0]['team_b_key'],'target')
        self.assertEqual(rows[0]['venue_key'],'target-gym')
        self.assertEqual({r['canonical_game_id'] for r in self._read(self.repo/'data/evidence/game-assertions.csv')},{'CBBG-9'})

    def test_same_date_core_conflict_requires_explicit_resolution(self):
        self._manifest()
        self._resolution()
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[
            game('CBBG-9','old-target',b_score='61'),game('CBBG-2','target',b_score='60')
        ])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[['A1','CBBG-9','alpha','SRC-1','old-target']])
        plan=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertTrue(any('material same-date conflict requires explicit resolution' in x for x in plan['blockers']))

    def test_unknown_date_distinct_games_require_and_honor_explicit_retention(self):
        self._manifest(games=2)
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[
            game('CBBG-1','old-target',date='',a_score='',b_score='',site='TEAM_A_HOME',home='alpha'),
            game('CBBG-2','old-target',date='',a_score='',b_score='',site='TEAM_B_HOME',home='old-target'),
        ])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[
            ['A1','CBBG-1','alpha','SRC-1','old-target'],['A2','CBBG-2','alpha','SRC-2','old-target']
        ])
        self._resolution()
        blocked=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertTrue(any('unknown-date collision requires explicit' in x for x in blocked['blockers']))
        self._resolution(distinct=[{
            'resolution_id':'DIST-1','canonical_game_ids':['CBBG-1','CBBG-2'],
            'resolution_basis':'source ledger has two separate season entries with opposite home designations',
            'evidence_urls':[]
        }])
        plan=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        self.assertEqual(plan['retained_distinct_canonical_game_ids'],['CBBG-1','CBBG-2'])
        bulk.apply(self.repo,self.manifest,self.resolutions,plan['plan_sha256'],run_validation=False)
        rows=self._read(self.repo/'data/canonical/games.csv')
        self.assertEqual(len(rows),2)
        self.assertTrue(all(r['team_b_key']=='target' for r in rows))

    def test_owner_reviewed_non_d1_rekey_does_not_set_current_d1(self):
        self._manifest(label='Arkansas A&M',old='arkansas-a-m',new='arkansas-monticello',name='Arkansas-Monticello',current='No',decision='REKEY_DISTINCT_NON_D1')
        self._resolution()
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[game('CBBG-1','arkansas-a-m')])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[['A1','CBBG-1','alpha','SRC-1','arkansas-a-m']])
        plan=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        bulk.apply(self.repo,self.manifest,self.resolutions,plan['plan_sha256'],run_validation=False)
        opponent=self._read(self.repo/'schools/alpha/opponents.csv')[0]
        source=self._read(self.repo/'schools/alpha/source-games.csv')[0]
        self.assertEqual(opponent['canonical_opponent_key'],'arkansas-monticello')
        self.assertEqual(opponent['current_d1'],'No')
        self.assertEqual(source['normalized_opponent_key'],'arkansas-monticello')
        self.assertEqual(source['opponent_current_d1'],'No')

    def test_unpaired_exact_date_can_use_explicit_counterpart(self):
        self._manifest()
        stale=game('CBBG-9','old-target',date='2000-01-02',b_score='60')
        counterpart=game('CBBG-2','target',date='2000-01-01',b_score='60')
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[stale,counterpart])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[
            ['A1','CBBG-9','alpha','SRC-1','old-target'],['A2','CBBG-2','target','T-1','alpha']
        ])
        self._resolution(pairs=[{
            'resolution_id':'PAIR-DATE-1',
            'kind':'EXPLICIT_COUNTERPART',
            'survivor_canonical_game_id':'CBBG-9',
            'absorbed_canonical_game_id':'CBBG-2',
            'canonical_values':{'game_date':'2000-01-01'},
            'resolution_basis':'reviewed reciprocal evidence establishes one game and the authoritative date',
            'evidence_urls':['https://example.test/date'],
            'discrepancies':[]
        }])
        plan=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        self.assertEqual(plan['canonical_pairs'][0]['survivor_canonical_game_id'],'CBBG-9')
        self.assertEqual(plan['canonical_pairs'][0]['absorbed_canonical_game_id'],'CBBG-2')
        self.assertEqual(plan['canonical_pairs'][0]['final_canonical_values']['game_date'],'2000-01-01')

    def test_omitted_global_package_usage_fails_and_rolls_back(self):
        self._manifest()
        self._resolution()
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[game('CBBG-1','old-target')])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[['A1','CBBG-1','alpha','SRC-1','old-target']])
        (self.repo/'schools/beta').mkdir(parents=True,exist_ok=True)
        self._write(self.repo/'schools/beta/opponents.csv',OPPONENT_HEADERS,[[
            'beta','Old Target','old-target','Old Target','No','1','1999-2000','1999-2000'
        ]])
        self._write(self.repo/'schools/beta/source-games.csv',SOURCE_HEADERS,[[
            'BETA-1','beta','1999-2000','','Old Target','Old Target','old-target','No','','','W','0','beta raw'
        ]])
        plan=bulk.build_plan(self.repo,self.manifest,self.resolutions)
        self.assertEqual(plan['blockers'],[])
        before=(self.repo/'schools/alpha/source-games.csv').read_bytes()
        with self.assertRaisesRegex(bulk.BulkTransactionError,'stale school-package key remains'):
            bulk.apply(self.repo,self.manifest,self.resolutions,plan['plan_sha256'],run_validation=False)
        self.assertEqual((self.repo/'schools/alpha/source-games.csv').read_bytes(),before)
        self.assertEqual(self._read(self.repo/'data/canonical/games.csv')[0]['team_b_key'],'old-target')

    def test_hash_mismatch_refuses_before_write(self):
        self._manifest(); self._resolution()
        self._write(self.repo/'data/canonical/games.csv',CANONICAL_HEADERS,[game('CBBG-1','old-target')])
        self._write(self.repo/'data/evidence/game-assertions.csv',ASSERTION_HEADERS,[['A1','CBBG-1','alpha','SRC-1','old-target']])
        before=(self.repo/'data/canonical/games.csv').read_bytes()
        with self.assertRaises(bulk.BulkTransactionError):
            bulk.apply(self.repo,self.manifest,self.resolutions,'wrong',run_validation=False)
        self.assertEqual((self.repo/'data/canonical/games.csv').read_bytes(),before)


if __name__=='__main__':
    unittest.main()
