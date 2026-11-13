"""Real local Git CAS and interrupted-transaction regression.

All remotes are created under TemporaryDirectory; never contacts origin.
The tested CAS/recovery primitives are the existing remote Implementation
controller functions, not an alternate GitHub publication path.
"""
from __future__ import annotations
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))

from remote_implementation_control import (
    RemoteImplementationError, publish_ref_cas, remote_head,
)
from all_history_expansion_remote_contract import (
    inspect_recovery, check_cas,
    IntegrationAuthorityError,
)


def git(path:Path,*args:str) -> str:
    cp=subprocess.run(["git",*args],cwd=path,text=True,
                      stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if cp.returncode:
        raise AssertionError(f"git {args}: {cp.stdout}")
    return cp.stdout.strip()


class DisposableExpansionGitTransactionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="expansion-disposable-git-")
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.remote=self.root/"remote.git"
        self.work=self.root/"work"
        git(self.root,"init","--bare",str(self.remote))
        git(self.root,"init","-b","main",str(self.work))
        git(self.work,"config","user.name","Disposable Test")
        git(self.work,"config","user.email","test@example.invalid")
        git(self.work,"remote","add","origin",str(self.remote))
        (self.work/"schools/example").mkdir(parents=True)
        (self.work/"schools/example/source-games.csv").write_text(
            "source_game_id\nOLD-1\n")
        git(self.work,"add","schools/example/source-games.csv")
        git(self.work,"commit","-m","immutable prior published school")
        self.predecessor=git(self.work,"rev-parse","HEAD")
        git(self.work,"push","origin","main")
        git(self.work,"push","origin","HEAD:refs/heads/data/example-onboarding")
        (self.work/"doc.txt").write_text("ordinary unrelated main advance\n")
        git(self.work,"add","doc.txt")
        git(self.work,"commit","-m","main-only unrelated update")
        self.main=git(self.work,"rev-parse","HEAD")
        git(self.work,"push","origin","main")
        (self.work/"schools/example/source-games.csv").write_text(
            "source_game_id\nOLD-1\nNEW-1\n")
        git(self.work,"add","schools/example/source-games.csv")
        git(self.work,"commit","-m","disposable expanded candidate")
        self.prepared=git(self.work,"rev-parse","HEAD")
        self.tree=git(self.work,"rev-parse","HEAD^{tree}")
        self.target="data/example-onboarding"
        self.writeahead={
            "expected_target_predecessor_sha":self.predecessor,
            "prepared_commit_sha":self.prepared,
            "prepared_parent_sha":self.main,
            "prepared_tree_sha":self.tree,
            "protected_main_sha":self.main,
        }

    def test_disposable_real_cas_then_recovery_classifies_single_publication(self):
        self.assertEqual(remote_head(self.work,self.target),self.predecessor)
        self.assertEqual(git(self.work,"rev-parse",self.prepared+"^"),self.main)
        self.assertEqual(inspect_recovery(
            expected_target_predecessor=self.predecessor,
            actual_target=self.predecessor,writeahead=self.writeahead)[
                "safe_next_action"],"ABANDON_PREPARED_UNPUBLISHED")
        # The genuine controller CAS is used, but only on a local temporary
        # bare remote. Write-ahead is durable before its first publication.
        manifest=self.root/"control-writeahead.json"
        manifest.write_text(json.dumps(self.writeahead,sort_keys=True))
        self.assertTrue(manifest.exists())
        publish_ref_cas(self.work,branch=self.target,
                        prepared_commit=self.prepared,
                        expected_predecessor=self.predecessor)
        self.assertEqual(remote_head(self.work,self.target),self.prepared)
        self.assertEqual(inspect_recovery(
            expected_target_predecessor=self.predecessor,
            actual_target=self.prepared,writeahead=self.writeahead)[
                "safe_next_action"],
            "ADOPT_ONLY_AFTER_EXACT_PREPARED_TREE_REPLAY")
        # No double-application, even with an exact target head.
        with self.assertRaises(RemoteImplementationError):
            publish_ref_cas(self.work,branch=self.target,
                            prepared_commit=self.prepared,
                            expected_predecessor=self.predecessor)
        success={
            "prepared_commit_sha":self.prepared,
            "actual_published_target_sha":self.prepared,
            "final_transaction_state":"COMPLETE",
        }
        self.assertEqual(inspect_recovery(
            expected_target_predecessor=self.predecessor,
            actual_target=self.prepared,
            writeahead=self.writeahead,successor=success)[
                "safe_next_action"],"NO_REAPPLICATION_PERMITTED")
        self.assertEqual(git(self.work,"rev-parse","HEAD^{tree}"),self.tree)

    def test_intervening_target_movement_refuses_cas(self):
        git(self.work,"checkout","-b","foreign",self.predecessor)
        (self.work/"foreign.txt").write_text("concurrent independent change\n")
        git(self.work,"add","foreign.txt")
        git(self.work,"commit","-m","foreign change")
        conflict=git(self.work,"rev-parse","HEAD")
        git(self.work,"push","origin",f"HEAD:refs/heads/{self.target}")
        self.assertEqual(remote_head(self.work,self.target),conflict)
        with self.assertRaises(RemoteImplementationError):
            publish_ref_cas(self.work,branch=self.target,
                            prepared_commit=self.prepared,
                            expected_predecessor=self.predecessor)
        self.assertEqual(remote_head(self.work,self.target),conflict)
        with self.assertRaisesRegex(IntegrationAuthorityError,"DIVERGED"):
            inspect_recovery(expected_target_predecessor=self.predecessor,
                             actual_target=conflict,writeahead=self.writeahead)

    def test_no_published_target_after_prepared_abort(self):
        self.assertEqual(remote_head(self.work,self.target),self.predecessor)
        disposition=inspect_recovery(expected_target_predecessor=self.predecessor,
                                      actual_target=self.predecessor,writeahead=None)
        self.assertEqual(disposition["safe_next_action"],"ABANDON_WITHOUT_PUBLICATION")
        self.assertEqual(remote_head(self.work,self.target),self.predecessor)


if __name__=="__main__":
    unittest.main()
