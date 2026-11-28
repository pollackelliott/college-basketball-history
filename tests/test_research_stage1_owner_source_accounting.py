"""Issue #732 owner-scoped Fresno Stage 1 closeout adversarial regressions.

These tests deliberately use the exact Git-committed Research checkpoint 0035.
CI fetches that commit; an environment without it skips the source-dependent
tests rather than substituting a synthetic historical game universe.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "fresno_owner_source_accounting",
    ROOT / "tools" / "research_stage1_owner_source_accounting.py",
)
mod = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)
CASE_SHA = "b2996ffc3e0e9e5f780cd6e7ccbb56789b55754b"


def git_show(commit, path):
    return subprocess.check_output(
        ["git", "-C", str(ROOT), "show", commit + ":" + path],
        stderr=subprocess.DEVNULL,
    )


def available():
    return subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "-e", CASE_SHA + "^{commit}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        check=False,
    ).returncode == 0


@unittest.skipUnless(available(), "exact Fresno Research checkpoint must be fetched")
class OwnerAccountingCloseoutTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "parent"
        self.root.mkdir()
        self.case = copy.deepcopy(mod.load_authority())
        prefix = self.case["checkpoint_path"]
        for file in [mod.MANIFEST, *self.case["member_git_blobs"]]:
            (self.root / file).write_bytes(git_show(CASE_SHA, prefix + file))
        self.assertEqual(mod.audit_checkpoint(self.root, self.case)["status"],
                         "ELIGIBLE_OWNER_SOURCE_ACCOUNTING_UNCERTAINTY")

    def assert_blocked(self):
        result = mod.audit_checkpoint(self.root, self.case)
        self.assertEqual(result["status"], "BLOCKED", result)
        self.assertFalse(result["stage1_complete"])

    def rebind(self, name):
        """Re-hash a tampered member AND its manifest to challenge semantic gates.

        The public CLI never allows caller-supplied authority; this internal
        test override proves that even forged internally consistent hashes
        cannot evade the separate permanent historical invariant checks.
        """
        raw = (self.root / name).read_bytes()
        self.case["member_git_blobs"][name] = mod.git_blob(raw)
        manifest = json.loads((self.root / mod.MANIFEST).read_bytes())
        manifest["members"][name] = mod.git_blob(raw)
        (self.root / mod.MANIFEST).write_bytes(mod.canonical(manifest))
        self.case["checkpoint_manifest_blob_sha"] = mod.git_blob(
            (self.root / mod.MANIFEST).read_bytes()
        )

    def edit_csv(self, name, fn, *, rebind=True):
        path = self.root / name
        value = path.read_text(encoding="utf-8")
        rdr = csv.DictReader(io.StringIO(value, newline=""))
        fields = list(rdr.fieldnames)
        rows = list(rdr)
        fn(rows)
        target = io.StringIO(newline="")
        writer = csv.DictWriter(target, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
        path.write_bytes(target.getvalue().encode("utf-8"))
        if rebind:
            self.rebind(name)

    def edit_json(self, name, fn, *, rebind=True):
        path = self.root / name
        raw = json.loads(path.read_bytes())
        fn(raw)
        path.write_bytes(mod.canonical(raw))
        if rebind:
            self.rebind(name)

    def test_exact_source_accepts_and_ordinary_other_seasons_checked(self):
        report = mod.audit_checkpoint(self.root, self.case)
        self.assertTrue(report["ucd_representation_checked"])
        self.assertTrue(report["ordinary_other_seasons_checked"])
        self.assertFalse(report["stage1_complete"])
        self.assertEqual(report["findings"]["accepted_games"], 1011)

    def test_complete_audit_closeout_independent_verify(self):
        audit = mod.audit_checkpoint(self.root, self.case)
        audit_file = Path(self.tmp.name) / "audit.json"
        audit_file.write_bytes(mod.canonical(audit))
        target = Path(self.tmp.name) / "closeout.zip"
        result = mod.closeout(self.root, audit_file, target,
                              audit_sha=mod.sha256(audit_file.read_bytes()),
                              case=self.case)
        self.assertFalse(result["stage1_complete"])
        self.assertEqual(result["status"], "AWAITING_INDEPENDENT_VERIFICATION")
        check = mod.verify_closeout(
            self.root, target, audit_file, closeout_sha=mod.sha256(target.read_bytes()),
            audit_sha=mod.sha256(audit_file.read_bytes()), case=self.case,
        )
        self.assertTrue(check["stage1_complete"])
        self.assertTrue(check["historical_uncertainty_retained"])
        with __import__("zipfile").ZipFile(target) as z:
            terminal = json.loads(z.read("stage1-terminal-source-accounting.json"))
            coverage = json.loads(z.read("stage4-authoring/season-coverage.json"))
            self.assertEqual(terminal["identified_competitive"], {
                "games": 28, "wins": 21, "losses": 7,
            })
            self.assertEqual(terminal["reported_institutional"], {
                "games": 29, "wins": 21, "losses": 8,
            })
            self.assertTrue(terminal["independent_additional_loss_possible"])
            self.assertFalse(terminal["unidentified_game_count_asserted"])
            self.assertFalse(terminal["reported_games_are_game_derived"])
            self.assertEqual(coverage["terminal_source_accounting_uncertainties"],
                             [terminal])
            self.assertEqual(
                z.read(mod.LEDGER), (self.root / mod.LEDGER).read_bytes()
            )
            self.assertEqual(
                z.read(mod.SOURCE), (self.root / mod.SOURCE).read_bytes()
            )
            self.assertEqual(
                z.read(mod.CENSUS), (self.root / mod.CENSUS).read_bytes()
            )

    def test_audit_cannot_claim_stage1_complete(self):
        self.assertFalse(mod.audit_checkpoint(self.root, self.case)["stage1_complete"])

    def test_wrong_school(self):
        self.case["school_key"] = "nevada"
        self.assert_blocked()

    def test_wrong_season(self):
        self.case["season"] = "1964-65"
        self.assert_blocked()

    def test_wrong_research_base(self):
        self.case["research_base_sha"] = "a" * 40
        self.assert_blocked()

    def test_wrong_parent_commit_manifest(self):
        self.case["checkpoint_previous_research_sha"] = "a" * 40
        self.assert_blocked()

    def test_wrong_checkpoint_path(self):
        self.case["checkpoint_path"] = "research/another-school/checkpoint/"
        self.assert_blocked()

    def test_missing_required_member(self):
        (self.root / mod.SOURCE).unlink()
        self.assert_blocked()

    def test_extra_member(self):
        (self.root / "unknown-provenance.csv").write_text("a,b\n")
        self.assert_blocked()

    def test_bad_parent_manifest_hash(self):
        (self.root / mod.MANIFEST).write_bytes(b"{}\n")
        self.assert_blocked()

    def test_altered_literal_source_without_rebind(self):
        path = self.root / mod.SOURCE
        path.write_bytes(path.read_bytes().replace(b"San Diego State W 67-63",
                                                 b"San Diego State W 60-60", 1))
        self.assert_blocked()

    def test_rebound_game_identity_must_still_fail(self):
        def change(rows):
            next(r for r in rows if r["season"] == "1965-66")[
                "research_game_id"] = "FABRICATED-IDENTITY"
        self.edit_csv(mod.LEDGER, change)
        self.assert_blocked()

    def test_rebound_extra_anonymous_game_must_fail(self):
        def change(rows):
            new = dict(rows[-1])
            new["research_game_id"] = "ANONYMOUS-29TH"
            new["source_entry_id"] = "UNSUPPORTED-29TH"
            new["opponent_literal"] = "Anonymous opponent"
            new["season"] = "1965-66"
            rows.append(new)
        self.edit_csv(mod.LEDGER, change)
        self.assert_blocked()

    def test_rebound_wl_count_tamper(self):
        def change(rows):
            next(r for r in rows if r["season"] == "1965-66")[
                "played_result"] = "L"
        self.edit_csv(mod.LEDGER, change)
        self.assert_blocked()

    def test_rebound_source_literal_mismatch(self):
        def change(rows):
            next(r for r in rows if r["season_label"] == "1965-66")[
                "source_raw_text"] = "opponent erased"
        self.edit_csv(mod.SOURCE, change)
        self.assert_blocked()

    def test_rebound_other_season_blocker(self):
        def change(rows):
            next(r for r in rows if r["season"] == "1961-62")[
                "final_status"] = "ADDITIONAL_UNRESOLVED_GAME"
        self.edit_csv(mod.CENSUS, change)
        self.assert_blocked()

    def test_rebound_extra_candidate_census_change(self):
        def change(rows):
            next(r for r in rows if r["season"] == "1952-53")[
                "working_L"] = "999"
        self.edit_csv(mod.CANDIDATE, change)
        self.assert_blocked()

    def test_rebound_official_reported_result(self):
        self.edit_json(mod.RULING, lambda x: x["preserve_official_printed_summary"].update(
            losses=7))
        self.assert_blocked()

    def test_rebound_unsupported_no_missing_game_assertion(self):
        self.edit_json(mod.RULING, lambda x: x.update(
            assume_no_missing_game_proven=True))
        self.assert_blocked()

    def test_rebound_owner_ruling_substitution(self):
        self.edit_json(mod.RULING, lambda x: x.update(
            owner_statement_verbatim="I approve inventing the game"))
        self.assert_blocked()

    def test_rebound_ucd_accepted_game_cannot_gain_score(self):
        def change(rows):
            next(r for r in rows if r["research_game_id"]
                 == "FRESNO-EXP-RECIP-UCD-1926-27-04")["team_points"] = "31"
        self.edit_csv(mod.LEDGER, change)
        self.assert_blocked()

    def test_rebound_ucd_claim_cannot_be_mapped_to_a_game(self):
        def change(rows):
            next(r for r in rows if r["source_entry_id"]
                 == "FRESNO-EXP-CAND-1926-27-006")[
                     "stage1_curated_game_id"] = "FRESNO-EXP-RECIP-UCD-1926-27-04"
        self.edit_csv(mod.SOURCE, change)
        self.assert_blocked()

    def test_rebound_clowns_exhibition_cannot_be_included(self):
        def change(rows):
            next(r for r in rows if r["source_entry_id"]
                 == "FRESNO-EXP-CAND-1935-36-019")[
                     "stage1_bulk_disposition"] = "ACCEPTED_NEW_COMPETITIVE_SOURCE_GAME"
        self.edit_csv(mod.SOURCE, change)
        self.assert_blocked()

    def test_rebound_source_duplicate_becomes_a_new_game(self):
        def change(rows):
            next(r for r in rows if r["source_entry_id"]
                 == "FRESNO-EXP-CAND-1965-66-022")[
                     "stage1_bulk_disposition"] = "ACCEPTED_NEW_COMPETITIVE_SOURCE_GAME"
        self.edit_csv(mod.SOURCE, change)
        self.assert_blocked()

    def test_rebound_extra_pending_blocker(self):
        def change(rows):
            rows.append({
                "source_entry_id": "ANOTHER", "season": "1964-65",
                "guide_source": "test", "blocker": "new", "needed_evidence": "test",
            })
        self.edit_csv(mod.PENDING, change)
        self.assert_blocked()

    def test_invalid_audit_hash_rejected(self):
        audit_file = Path(self.tmp.name) / "audit.json"
        audit_file.write_bytes(mod.canonical(mod.audit_checkpoint(self.root, self.case)))
        with self.assertRaises(ValueError):
            mod.closeout(self.root, audit_file, Path(self.tmp.name) / "successor.zip",
                         audit_sha="0" * 64, case=self.case)

    def test_stale_rebound_parent_invalidates_audit(self):
        audit_file = Path(self.tmp.name) / "audit.json"
        audit_file.write_bytes(mod.canonical(mod.audit_checkpoint(self.root, self.case)))
        self.edit_csv(mod.CANDIDATE, lambda rows: next(
            r for r in rows if r["season"] == "1965-66").update(
                final_status="INVALID"))
        with self.assertRaises(ValueError):
            mod.closeout(self.root, audit_file, Path(self.tmp.name) / "successor.zip",
                         audit_sha=mod.sha256(audit_file.read_bytes()), case=self.case)

    def test_tampered_closeout_rejected_by_independent_verify(self):
        audit_file = Path(self.tmp.name) / "audit.json"
        audit_file.write_bytes(mod.canonical(mod.audit_checkpoint(self.root, self.case)))
        target = Path(self.tmp.name) / "successor.zip"
        mod.closeout(self.root, audit_file, target,
                     audit_sha=mod.sha256(audit_file.read_bytes()), case=self.case)
        original = target.read_bytes()
        target.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
        result = mod.verify_closeout(
            self.root, target, audit_file, closeout_sha=mod.sha256(target.read_bytes()),
            audit_sha=mod.sha256(audit_file.read_bytes()), case=self.case,
        )
        self.assertEqual(result["status"], "FAIL")


    def verified_chain(self):
        """Actual exact-parent audit, ZIP closeout and independent verifier."""
        audit = mod.audit_checkpoint(self.root, self.case)
        audit_path = Path(self.tmp.name) / "audit-for-handoff.json"
        audit_path.write_bytes(mod.canonical(audit))
        audit_sha = mod.sha256(audit_path.read_bytes())
        zip_path = Path(self.tmp.name) / "closeout-for-handoff.zip"
        closeout = mod.closeout(
            self.root, audit_path, zip_path, audit_sha=audit_sha, case=self.case)
        self.assertFalse(closeout["stage1_complete"])
        zip_sha = mod.sha256(zip_path.read_bytes())
        verification = mod.verify_closeout(
            self.root, zip_path, audit_path,
            closeout_sha=zip_sha, audit_sha=audit_sha, case=self.case)
        self.assertTrue(verification["stage1_complete"], verification)
        verified_path = Path(self.tmp.name) / "independent-verified.json"
        verified_path.write_bytes(mod.canonical(verification))
        verified_sha = mod.sha256(verified_path.read_bytes())
        return audit_path, audit_sha, zip_path, zip_sha, verified_path, verified_sha

    def test_all_eleven_original_checkpoint_files_survive_byte_for_byte(self):
        audit_path, audit_sha, zip_path, zip_sha, _, _ = self.verified_chain()
        with zipfile.ZipFile(zip_path) as z:
            names = set(z.namelist())
            expected = set(self.case["member_git_blobs"]) | {mod.MANIFEST}
            self.assertEqual(len(expected), 11)
            self.assertTrue(expected.issubset(names))
            self.assertIn("49-season-stage1-terminal-census.csv", names)
            self.assertIn("stage4-authoring/season-coverage.json", names)
            manifest = json.loads(z.read("manifest.json"))
            self.assertEqual(set(manifest["inherited_parent_git_blobs"]), expected)
            self.assertEqual(manifest["parent_checkpoint_commit_sha"], CASE_SHA)
            self.assertEqual(manifest["parent_manifest_git_blob_sha"],
                             self.case["checkpoint_manifest_blob_sha"])
            for name in expected:
                original = (self.root / name).read_bytes()
                self.assertEqual(z.read(name), original, name)
                self.assertEqual(manifest["inherited_parent_git_blobs"][name],
                                 mod.git_blob(original))
            self.assertFalse(json.loads(z.read(
                "stage1-closeout-status.json"))["stage1_complete"])

    def test_omit_predecessor_admission_diagnostic_in_successor_fails(self):
        audit_path, audit_sha, zip_path, _, _, _ = self.verified_chain()
        with zipfile.ZipFile(zip_path) as z:
            members = {name: z.read(name) for name in z.namelist()}
        self.assertIn("stage1-admission-diagnostic-0035.json", members)
        del members["stage1-admission-diagnostic-0035.json"]
        tampered = Path(self.tmp.name) / "dropped-original-diagnostic.zip"
        tampered.write_bytes(mod.zip_bytes(members))
        result = mod.verify_closeout(
            self.root, tampered, audit_path,
            closeout_sha=mod.sha256(tampered.read_bytes()),
            audit_sha=audit_sha, case=self.case)
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["stage1_complete"])

    def test_mutate_original_readme_in_successor_with_rehashed_zip_fails(self):
        audit_path, audit_sha, zip_path, _, _, _ = self.verified_chain()
        with zipfile.ZipFile(zip_path) as z:
            members = {name: z.read(name) for name in z.namelist()}
        self.assertIn("README.md", members)
        members["README.md"] += b"\nNew invented diagnostic conclusion.\n"
        root_manifest = json.loads(members["manifest.json"])
        root_manifest["member_sha256"]["README.md"] = mod.sha256(members["README.md"])
        root_manifest["member_bytes"]["README.md"] = len(members["README.md"])
        members["manifest.json"] = mod.canonical(root_manifest)
        tampered = Path(self.tmp.name) / "rewritten-parent-evidence.zip"
        tampered.write_bytes(mod.zip_bytes(members))
        result = mod.verify_closeout(
            self.root, tampered, audit_path,
            closeout_sha=mod.sha256(tampered.read_bytes()),
            audit_sha=audit_sha, case=self.case)
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["stage1_complete"])

    def test_verified_handoff_binds_pass_audit_zip_and_full_coverage(self):
        audit_path, audit_sha, zip_path, zip_sha, verified_path, verified_sha = (
            self.verified_chain())
        handoff = Path(self.tmp.name) / "verified-stage1-handoff.json"
        sealed = mod.seal_handoff(
            self.root, zip_path, audit_path, verified_path, handoff,
            closeout_sha=zip_sha, audit_sha=audit_sha,
            verification_sha=verified_sha, case=self.case)
        self.assertFalse(sealed["stage1_complete"])
        self.assertTrue(handoff.is_file())
        payload = json.loads(handoff.read_bytes())
        self.assertEqual(payload["state"], "STAGE_1_COMPLETE_VERIFIED")
        self.assertEqual(payload["closeout_zip_sha256"], zip_sha)
        self.assertEqual(payload["audit_sha256"], audit_sha)
        self.assertEqual(payload["independent_verifier_report_sha256"],
                         verified_sha)
        self.assertTrue(payload["independent_additional_loss_possible"])
        self.assertEqual(payload["require_downstream_stage2_verification"],
                         "verify-handoff")
        accepted = mod.verify_handoff(
            self.root, zip_path, audit_path, verified_path, handoff,
            closeout_sha=zip_sha, audit_sha=audit_sha,
            verification_sha=verified_sha,
            handoff_sha=sealed["handoff_sha256"], case=self.case)
        self.assertEqual(accepted["status"], "VERIFIED_STAGE1_COMPLETE_HANDOFF")
        self.assertTrue(accepted["stage1_complete"])
        self.assertFalse(accepted["stage2_authorized"])

    def test_unverified_closeout_or_eligibility_cannot_seal_handoff(self):
        audit_path, audit_sha, zip_path, zip_sha, verified_path, _ = (
            self.verified_chain())
        verified_path.write_bytes((audit_path).read_bytes())
        forged_sha = mod.sha256(verified_path.read_bytes())
        with self.assertRaises(ValueError):
            mod.seal_handoff(
                self.root, zip_path, audit_path, verified_path,
                Path(self.tmp.name) / "invalid-handoff.json",
                closeout_sha=zip_sha, audit_sha=audit_sha,
                verification_sha=forged_sha, case=self.case)
        self.assertFalse((Path(self.tmp.name) / "invalid-handoff.json").exists())

    def test_handoff_wrong_parent_or_zip_hash_fails_closed(self):
        audit_path, audit_sha, zip_path, zip_sha, verified_path, verified_sha = (
            self.verified_chain())
        handoff = Path(self.tmp.name) / "valid-handoff.json"
        sealed = mod.seal_handoff(
            self.root, zip_path, audit_path, verified_path, handoff,
            closeout_sha=zip_sha, audit_sha=audit_sha,
            verification_sha=verified_sha, case=self.case)
        wrong = mod.verify_handoff(
            self.root, zip_path, audit_path, verified_path, handoff,
            closeout_sha="0"*64, audit_sha=audit_sha,
            verification_sha=verified_sha,
            handoff_sha=sealed["handoff_sha256"], case=self.case)
        self.assertEqual(wrong["status"], "FAIL")
        changed = copy.deepcopy(self.case)
        changed["checkpoint_commit_sha"] = "a"*40
        wrong_parent = mod.verify_handoff(
            self.root, zip_path, audit_path, verified_path, handoff,
            closeout_sha=zip_sha, audit_sha=audit_sha,
            verification_sha=verified_sha,
            handoff_sha=sealed["handoff_sha256"], case=changed)
        self.assertEqual(wrong_parent["status"], "FAIL")

    def test_handoff_tampered_caveat_rejected_even_if_rehashed(self):
        audit_path, audit_sha, zip_path, zip_sha, verified_path, verified_sha = (
            self.verified_chain())
        handoff = Path(self.tmp.name) / "tamper-handoff.json"
        mod.seal_handoff(
            self.root, zip_path, audit_path, verified_path, handoff,
            closeout_sha=zip_sha, audit_sha=audit_sha,
            verification_sha=verified_sha, case=self.case)
        payload = json.loads(handoff.read_bytes())
        payload["independent_additional_loss_possible"] = False
        handoff.write_bytes(mod.canonical(payload))
        result = mod.verify_handoff(
            self.root, zip_path, audit_path, verified_path, handoff,
            closeout_sha=zip_sha, audit_sha=audit_sha,
            verification_sha=verified_sha,
            handoff_sha=mod.sha256(handoff.read_bytes()), case=self.case)
        self.assertEqual(result["status"], "FAIL")

    def test_missing_verified_report_disallows_stage1_handoff(self):
        audit_path, audit_sha, zip_path, zip_sha, verified_path, verified_sha = (
            self.verified_chain())
        verified_path.unlink()
        with self.assertRaises(OSError):
            mod.seal_handoff(
                self.root, zip_path, audit_path, verified_path,
                Path(self.tmp.name) / "no-verifier-handoff.json",
                closeout_sha=zip_sha, audit_sha=audit_sha,
                verification_sha=verified_sha, case=self.case)

    def test_cli_pipeline_keeps_closeout_zip_intact_and_verifies_handoff(self):
        """Protect against CLI report overwriting ZIP and skipped last gate."""
        root = Path(self.tmp.name)
        audit, closeout, verified = (root / n for n in (
            "cli-audit.json", "cli-closeout.zip", "cli-verified.json"))
        handoff, proof = root / "cli-handoff.json", root / "cli-handoff-proof.json"
        exe = [sys.executable, str(ROOT / "tools" /
                                  "research_stage1_owner_source_accounting.py")]
        def run(*argv):
            result = subprocess.run([*exe, *map(str, argv)], capture_output=True,
                                    text=True, check=False)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        parent = ["--expected-parent-sha", CASE_SHA]
        run("audit", self.root, *parent, "--output", audit)
        audit_sha = mod.sha256(audit.read_bytes())
        run("closeout", self.root, audit, *parent,
            "--expected-audit-sha256", audit_sha, "--output", closeout)
        self.assertTrue(zipfile.is_zipfile(closeout), "CLI must not clobber ZIP")
        closeout_sha = mod.sha256(closeout.read_bytes())
        run("verify-closeout", self.root, closeout, audit, *parent,
            "--expected-audit-sha256", audit_sha,
            "--expected-closeout-sha256", closeout_sha, "--output", verified)
        verifier_sha = mod.sha256(verified.read_bytes())
        run("seal-handoff", self.root, closeout, audit, verified, *parent,
            "--expected-audit-sha256", audit_sha,
            "--expected-closeout-sha256", closeout_sha,
            "--expected-verification-sha256", verifier_sha,
            "--output", handoff)
        self.assertTrue(handoff.is_file())
        run("verify-handoff", self.root, closeout, audit, verified, handoff, *parent,
            "--expected-audit-sha256", audit_sha,
            "--expected-closeout-sha256", closeout_sha,
            "--expected-verification-sha256", verifier_sha,
            "--expected-handoff-sha256", mod.sha256(handoff.read_bytes()),
            "--output", proof)
        result = json.loads(proof.read_bytes())
        self.assertEqual(result["status"], "VERIFIED_STAGE1_COMPLETE_HANDOFF")
        self.assertTrue(result["stage1_complete"])
        self.assertFalse(result["stage2_authorized"])
        self.assertEqual(mod.sha256(closeout.read_bytes()), closeout_sha)



if __name__ == "__main__":
    unittest.main()
