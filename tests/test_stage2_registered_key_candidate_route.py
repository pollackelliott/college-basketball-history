"""No cross-family routing or unchecked historical-key exception."""
from __future__ import annotations
import json, sys, tempfile, unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import stage2_registered_key_candidate_route as route
from remote_implementation_registered_key_rebase import BLOCKER, KeyRebaseStop, digest

class ExactRegisteredKeyRouteTests(unittest.TestCase):
    def test_other_school_or_operation_retains_existing_route(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertFalse(route.candidate_route(Path(d),'wrong',{'operation':'STAGE2_CENSUS','school_key':'other'}, {}, 'bad', b''))
            self.assertFalse(route.candidate_route(Path(d),'wrong',{'operation':'STAGE2_PROPOSAL_REHEARSAL','school_key':'grand-canyon'}, {}, 'bad', b''))

    def test_exact_census_and_adversarial_boundaries(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            folder = root / Path(route.CHECKPOINT).parent
            folder.mkdir(parents=True)
            blockers = [BLOCKER] + [
                "historical opponent display conflict: sample-%02d: ['A', 'B']" % i
                for i in range(39)
            ]
            status = {'status':'BLOCKED','blockers':blockers, 'semantic_drift':{'status':'PASS'},
                      'preflight':{'blocker_count':40,'warning_count':0,'decision_count':0}}
            census = {'status':'PREFLIGHT_BLOCKED','preflight':{'blocker_count':40}}
            hashes={}
            for n,obj in [('implementation-stage2-status.json',status),('implementation-stage2-capability-census.json',census)]:
                raw=(json.dumps(obj,sort_keys=True)+'\n').encode()
                (folder/n).write_bytes(raw)
                hashes[n]=digest(raw)
            manifest={'kind':'REMOTE_IMPLEMENTATION_STAGE2_CENSUS_CHECKPOINT',
                      'request_id':'grand-canyon-stage2-census-0001','school_key':'grand-canyon',
                      'target_branch':'data/grand-canyon-onboarding',
                      'target_sha':route.TARGET,'protected_main_sha':route.MAIN,
                      'integration_freeze_sha256':route.FREEZE,
                      'semantic_snapshot_sha256':route.SEMANTIC,
                      'stage2_status':'BLOCKED','capability_census_status':'PREFLIGHT_BLOCKED',
                      'artifact_sha256':hashes}
            raw=(json.dumps(manifest,sort_keys=True)+'\n').encode()
            sh=digest(raw)
            last={'operation':'STAGE2_CENSUS','school_key':'grand-canyon',
                  'checkpoint_manifest_sha256':sh,
                  'stage2_status':'BLOCKED','fresh_runner_verification':'PASS',
                  'remote_stage2_census_equivalence':'PASS',
                  'target_branch':'data/grand-canyon-onboarding','target_sha':route.TARGET,
                  'protected_main_sha':route.MAIN}
            with patch.object(route,'CENSUS_SHA256',sh):
                self.assertTrue(route.candidate_route(root,route.CONTROL,last,manifest,route.CHECKPOINT,raw))
                for field,invalid in [('target_sha','0'*40),('protected_main_sha','1'*40),
                                      ('fresh_runner_verification','PENDING'),
                                      ('checkpoint_manifest_sha256','2'*64)]:
                    bad=dict(last);bad[field]=invalid
                    with self.subTest(field=field),self.assertRaises(KeyRebaseStop):
                        route.candidate_route(root,route.CONTROL,bad,manifest,route.CHECKPOINT,raw)
                with self.assertRaises(KeyRebaseStop):
                    route.candidate_route(root,'0'*40,last,manifest,route.CHECKPOINT,raw)
                with self.assertRaises(KeyRebaseStop):
                    route.candidate_route(root,route.CONTROL,last,manifest,route.CHECKPOINT,raw+b' ')
                status['blockers'][-1]='unexpected blocker'
                (folder/'implementation-stage2-status.json').write_text(json.dumps(status,sort_keys=True)+'\n')
                with self.assertRaises(KeyRebaseStop):
                    route.candidate_route(root,route.CONTROL,last,manifest,route.CHECKPOINT,raw)
