"""Fail-closed isolated UC Davis historical-data replay authority tests."""
from __future__ import annotations
import subprocess, sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from ci_immutable_uc_davis_baseline import BaselineStop, create_baseline, git, verify_baseline, require_runtime_sha

class ImmutableHistoricalDataTests(unittest.TestCase):
    def test_separate_candidate_tools_and_exact_historical_data(self):
        with tempfile.TemporaryDirectory(prefix='ucd-baseline-test-') as folder:
            base=Path(folder);runtime=base/'runtime';runtime.mkdir()
            subprocess.run(['git','init','-q',str(runtime)],check=True)
            git(runtime,'config','user.name','test')
            git(runtime,'config','user.email','test@example.invalid')
            (runtime/'data').mkdir()
            (runtime/'data'/'registry.csv').write_text('frozen-data\n')
            git(runtime,'add','data/registry.csv');git(runtime,'commit','-qm','frozen')
            old=git(runtime,'rev-parse','HEAD')
            (runtime/'data'/'registry.csv').write_text('current-data\n')
            (runtime/'tools').mkdir()
            (runtime/'tools'/'new.py').write_text('CANDIDATE_TOOLS=True\n')
            git(runtime,'add','data/registry.csv','tools/new.py')
            git(runtime,'commit','-qm','candidate tooling')
            new=git(runtime,'rev-parse','HEAD')
            require_runtime_sha(runtime,new)
            with self.assertRaises(BaselineStop):
                require_runtime_sha(runtime,old)
            with self.assertRaises(BaselineStop):
                require_runtime_sha(runtime,'invalid-sha')
            target=base/'baseline'
            create_baseline(runtime,target,old)
            self.assertEqual(git(target,'rev-parse','HEAD'),old)
            self.assertEqual(git(target,'rev-parse','refs/remotes/origin/main'),old)
            self.assertEqual((target/'data'/'registry.csv').read_text(),'frozen-data\n')
            self.assertEqual((runtime/'data'/'registry.csv').read_text(),'current-data\n')
            self.assertTrue((runtime/'tools'/'new.py').exists())
            self.assertEqual(git(runtime,'rev-parse','HEAD'),new)
            with self.assertRaises(BaselineStop):
                create_baseline(runtime,target,old)
            with self.assertRaises(BaselineStop):
                create_baseline(runtime,base/'invalid','0'*40)
            git(target,'update-ref','refs/remotes/origin/main',new)
            with self.assertRaises(BaselineStop):
                verify_baseline(target,old)
            git(target,'update-ref','refs/remotes/origin/main',old)
            (target/'data'/'registry.csv').write_text('tampered\n')
            with self.assertRaises(BaselineStop):
                verify_baseline(target,old)
            self.assertEqual((runtime/'data'/'registry.csv').read_text(),'current-data\n')
