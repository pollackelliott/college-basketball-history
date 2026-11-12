"""Regression coverage for bounded multi-game post-publication identity correction."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import ingest_school
import onboard_school
import onboarding_plan as plan
from correction_site_nonregression import prove, verify_current
from tests.test_correction_identity_patch import (
    SOURCE_FIELDS, assertion, canonical, snapshot, source, write_table,
)


class MultiGameCorrectionIdentityTests(unittest.TestCase):
    def _fixture(self, root: Path):
        before1 = source()
        before2 = source(
            'test-old', '', source_game_id='TENRAW-00137',
            game_date='1919-03-01', source_opponent_label='Test Old',
            raw_text='M1 at Test Old L, 33-34 Test City', city='Test City',
        )
        after1 = source('georgetown-ky', '')
        after2 = source(
            'test-new', '', source_game_id='TENRAW-00137',
            game_date='1919-03-01', source_opponent_label='Test Old',
            raw_text='M1 at Test Old L, 33-34 Test City', city='Test City',
        )
        source_path = root / 'schools/tennessee/source-games.csv'
        write_table(source_path, SOURCE_FIELDS, [before1, before2])
        subprocess.run(['git', 'init', '-q', str(root)], check=True)
        subprocess.run(['git', 'add', 'schools/tennessee/source-games.csv'], cwd=root, check=True)
        subprocess.run([
            'git', '-c', 'user.name=Regression', '-c',
            'user.email=regression@example.test', 'commit', '-qm', 'baseline'
        ], cwd=root, check=True)
        base_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        write_table(source_path, SOURCE_FIELDS, [after1, after2])

        game1 = canonical()
        game2 = canonical(
            canonical_game_id='CBBG-0020299', game_date='1919-03-01',
            team_a_key='tennessee', team_b_key='test-old',
            team_a_score='33', team_b_score='34',
            result_winner_team_key='test-old', site_type='TEAM_B_HOME',
            designated_home_team_key='test-old', site_city='Test City',
        )
        write_table(root / 'data/canonical/games.csv', ingest_school.CANONICAL_FIELDS, [game1, game2])
        assertion1 = assertion(before1)
        assertion2 = assertion(
            before2, assertion_id='ASSERT-TENRAW-00137',
            canonical_game_id='CBBG-0020299', source_game_id='TENRAW-00137',
        )
        write_table(root / 'data/evidence/game-assertions.csv', ingest_school.ASSERTION_FIELDS, [assertion1, assertion2])
        write_table(root / 'data/reconciliation/discrepancies.csv', ingest_school.DISCREPANCY_FIELDS, [])
        write_table(root / 'data/reference/venues.csv', ['venue_id', 'venue_key', 'city', 'state'], [])
        manifest = {
            'schema_version': 2, 'workflow_kind': 'POST_PUBLICATION_CORRECTION',
            'status': 'INTEGRATION_FROZEN', 'school_key': 'tennessee',
            'research_base_sha': base_sha,
            'correction_source_game_ids': ['TENRAW-00136', 'TENRAW-00137'],
            'pre_correction_source_semantic_guard': snapshot([before1, before2]),
            'source_game_semantic_guard': snapshot([after1, after2]),
            'package_member_sha256': {'source-games.csv': plan.sha256_file(source_path)},
        }
        manifest_path = root / '.onboarding/tennessee/integration-freeze.json'
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(manifest), encoding='utf-8')

        sources = plan.read_csv(source_path)
        games = plan.read_csv(root / 'data/canonical/games.csv')
        assertions = plan.read_csv(root / 'data/evidence/game-assertions.csv')
        game_by_id = {row['canonical_game_id']: row for row in games}
        by_source, by_game = {}, {}
        for row in assertions:
            by_source.setdefault((row['source_program_key'], row['source_game_id']), []).append(row)
            by_game.setdefault(row['canonical_game_id'], []).append(row)
        identities, projected = plan._post_publication_identity_review_decisions(
            root, 'tennessee', sources, game_by_id, by_source, by_game
        )
        sites = plan._post_publication_site_review_decisions(
            root, 'tennessee', sources, projected, by_source, by_game
        )
        return source_path, identities, sites

    def test_classifier_accepts_exact_identity_population_and_rejects_site(self):
        identities = [
            {'source_game_id': 'A', 'canonical_game_id': 'G1'},
            {'source_game_id': 'B', 'canonical_game_id': 'G2'},
        ]
        self.assertEqual(
            plan._correction_transaction_kind({'A', 'B'}, identities, []),
            'MULTI_GAME_IDENTITY_ONLY',
        )
        with self.assertRaisesRegex(plan.WorkflowError, 'canonical site review requires explicit tooling'):
            plan._correction_transaction_kind({'A', 'B'}, identities, [{'source_game_id': 'A'}])

    def test_exact_multi_game_sealed_execution_changes_only_bound_rows(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source_path, identities, sites = self._fixture(root)
            self.assertEqual(len(identities), 2)
            self.assertEqual(sites, [])
            items = [{
                **item, 'decision': plan.CORRECTION_IDENTITY_ACTION,
                'resolution_basis': 'Owner-authorized historical identity correction',
                'source_patch': {}, 'canonical_patch': {},
            } for item in identities]
            bindings = sorted((item['source_game_id'], item['canonical_game_id']) for item in identities)
            approved = {
                'school_key': 'tennessee', 'approved_plan_hash': 'd' * 64,
                'decisions': items,
                'summary': {
                    'correction_transaction_kind': 'MULTI_GAME_IDENTITY_ONLY',
                    'correction_source_game_ids': [sid for sid, _ in bindings],
                    'correction_canonical_game_ids': sorted(gid for _, gid in bindings),
                    'correction_game_bindings': [
                        {'source_game_id': sid, 'canonical_game_id': gid} for sid, gid in bindings
                    ],
                },
            }
            report = {
                'school_key': 'tennessee', 'history_start_season': '1908-1909',
                'source_validation_scope': {
                    'mode': 'CORRECTION_DELTA', 'scoped_source_games': 2,
                    'correction_source_games': 2,
                },
                'source_site_counts': {'rows': 2},
                'counts': {'target_canonical_games': 2}, 'examples': {},
                'status': 'PASS', 'errors': [], 'warnings': [],
            }
            before_bytes = source_path.read_bytes()
            with (
                patch.object(onboard_school, 'run', return_value='site build mocked'),
                patch.object(onboard_school, 'capture_correction_site_report', side_effect=[report, report]),
            ):
                result = onboard_school.execute_approved_in_place(root, approved)
            self.assertEqual(result['transaction_kind'], 'MULTI_GAME_IDENTITY_ONLY')
            self.assertEqual(result['correction_site_nonregression']['mode'], 'MULTI_GAME_CORRECTION_NONREGRESSION')
            self.assertEqual(source_path.read_bytes(), before_bytes)
            games = {r['canonical_game_id']: r for r in plan.read_csv(root / 'data/canonical/games.csv')}
            self.assertEqual(games['CBBG-0020298']['team_a_key'], 'georgetown-ky')
            self.assertEqual(games['CBBG-0020299']['team_b_key'], 'test-new')
            assertions = {r['source_game_id']: r for r in plan.read_csv(root / 'data/evidence/game-assertions.csv')}
            self.assertEqual(assertions['TENRAW-00136']['normalized_opponent_key'], 'georgetown-ky')
            self.assertEqual(assertions['TENRAW-00137']['normalized_opponent_key'], 'test-new')

    def test_multi_game_site_proof_release_binding_and_noop_scope(self):
        report = {
            'school_key': 'tennessee', 'history_start_season': '1908-1909',
            'source_validation_scope': {'mode': 'CORRECTION_DELTA', 'scoped_source_games': 2, 'correction_source_games': 2},
            'source_site_counts': {'rows': 2},
            'counts': {'target_canonical_games': 2}, 'examples': {},
            'status': 'PASS', 'errors': [], 'warnings': [],
        }
        proof = prove(report, report, ['G1', 'G2'])
        verify_current(report, proof, 'tennessee')
        manifest = {
            'school_key': 'tennessee',
            'summary': {
                'correction_transaction_kind': 'MULTI_GAME_IDENTITY_ONLY',
                'correction_source_game_ids': ['A', 'B'],
                'correction_canonical_game_ids': ['G1', 'G2'],
                'correction_game_bindings': [
                    {'source_game_id': 'A', 'canonical_game_id': 'G1'},
                    {'source_game_id': 'B', 'canonical_game_id': 'G2'},
                ],
            },
            'execution': {'correction_site_nonregression': proof},
        }
        kwargs = onboard_school.correction_gate_kwargs_from_manifest(manifest, 'tennessee')
        self.assertEqual(kwargs['correction_source_ids'], ['A', 'B'])
        observed = []
        def fake_run(command, *, cwd, label, echo=True):
            observed.append((label, command)); return 'PASS'
        with patch.object(onboard_school, 'run', side_effect=fake_run):
            onboard_school.run_gates(Path('/tmp'), 'tennessee', include_tests=False, correction_source_ids=['A', 'B'])
        target = next(command for label, command in observed if label == 'target_no_op')
        self.assertEqual([target[i+1] for i,v in enumerate(target[:-1]) if v == '--source-game-id'], ['A','B'])


if __name__ == '__main__':
    unittest.main()
