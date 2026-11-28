"""Fail-closed adversarial tests for the issue #736 registered-key case."""
from __future__ import annotations

import csv
import hashlib
import io
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


if __name__=='__main__':unittest.main()
