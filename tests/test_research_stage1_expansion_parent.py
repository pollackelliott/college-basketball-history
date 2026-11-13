"""Fail-closed Arizona State v2 expansion Stage 1 accounting regressions."""
import io
import json
import sys
import tempfile
import unittest
import zipfile
from collections import Counter
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import research_stage1_expansion_parent as mod

# Inherited Research-base season identity totals; original full rows are never invented.
COUNTS = {
    1911:(0,1),1912:(2,2),1913:(0,2),1914:(0,1),1918:(1,4),1920:(1,0),
    1921:(10,1),1922:(5,3),1923:(0,1),1924:(4,3),1925:(9,3),1926:(6,6),
    1927:(10,5),1928:(3,13),1929:(3,10),1930:(12,6),1931:(6,12),
    1932:(8,10),1933:(4,10),1934:(1,11),1935:(5,10),1936:(8,8),
    1937:(10,11),1938:(13,13),1939:(6,14),1940:(11,8),1941:(10,6),
    1942:(10,7),1944:(2,4),1945:(12,15),1946:(7,12),1947:(13,11),
    1948:(11,16),1949:(12,15)}
CANDIDATES = [
    ("Phoenix Indian", "W",44,14), ("Mesa High","W",40,21),
    ("Phoenix College","W",29,27),("Phoenix Indian","W",47,14),
    ("Mesa High","L",31,33),("Prescott High","W",31,20),
    ("Prescott High","W",36,12),("Phoenix High","L",12,20),
    ("Gilbert High","W",55,17),("Phoenix College","W",55,15)]
ISSUES = ["ASU-S1-1916-17-AGG", "ASU-S1-1917-18-AGG", "ASU-S1-1919-20-AGG",
          "ASU-S1-1943-44-AGG", "ASU-S1-1920-21-RECORD", "ASU-S1-1920-21-IDENTITY",
          "ASU-S1-1920-21-PROVISIONAL-INCLUSION"]


def zbytes(members):
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for name, raw in sorted(members.items()):
            z.writestr(name, raw)
    return out.getvalue()


class ExpansionParentAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.parent = self.root / "parent.zip"
        self.registry = self.root / "registry.json"
        self.report = self.root / "audit.json"
        self.successor = self.root / "successor.zip"
        self.source = self.root / "source-games.csv"
        self.input = self.root / "checkpoint.zip"
        self.rows = []
        for year, (wins, losses) in COUNTS.items():
            season = f"{year}-{year + 1}"
            for result, count in (("W", wins), ("L", losses)):
                for i in range(count):
                    nau = year == 1920
                    self.rows.append({"source_game_id": "ASU-STG2-PRE1950-1920-21-001" if nau else
                                      f"TEST-{season}-{result}-{i:03}", "season_label": season,
                                      "source_opponent_label": "Northern Arizona / Flagstaff" if nau else f"Opponent {season}-{result}-{i}",
                                      "played_result": result, "team_score": "45" if nau else "50",
                                      "opponent_score": "13" if nau else "30",
                                      "curated_game_type": "REGULAR_SEASON", "raw_text": "literal score", "source_page": "test"})
        self.assertEqual(len(self.rows), 469)
        for i in range(2211):
            self.rows.append({"source_game_id": f"PUBLISHED-{i}", "season_label": "1950-1951",
                              "source_opponent_label": "Existing", "played_result": "W",
                              "team_score": "50", "opponent_score": "30", "curated_game_type": "REGULAR_SEASON",
                              "raw_text": "literal", "source_page": "test"})
        self.rewrite_source()
        self.make_checkpoint()
        for attr, val in (("ORIGINAL_BLOB",mod.blob(self.source.read_bytes())),
                          ("CHECKPOINT_0018",mod.sha(self.input.read_bytes())),
                          ("TRANSPORT_SHA",self.transport_sha)):
            stub = patch.object(mod, attr, val)
            stub.start(); self.addCleanup(stub.stop)
        self.input_sha = mod.CHECKPOINT_0018

    def rewrite_source(self):
        self.source.write_bytes(mod.write_csv(self.rows))

    def make_checkpoint(self):
        original = [{"season": "1920-1921", "result": r, "asu_score": str(a),
                     "opponent_score": str(b), "literal_opponent": op}
                    for op,r,a,b in CANDIDATES + [("ASC","W",42,13)]]
        literal_bytes = mod.write_csv(original)
        z2 = zbytes({"official-1920-21-literal-results.csv": literal_bytes,
                     "manifest.json": mod.jb({"members_sha256": {
                         "official-1920-21-literal-results.csv": mod.sha(literal_bytes)}})})
        transport = zbytes({"originals/arizona-state-early-universe-partial-0002.zip": z2,
                            "transport-manifest.json": mod.jb({"original_checkpoints": [{"sha256": mod.sha(z2)}]})})
        self.transport_sha = mod.sha(transport)
        candidates = [{"research_candidate_id":f"ASU-EXP-1920-21-CAND-{i:03}",
                       "season_label":"1920-1921", "source_literal_opponent":op,
                       "source_result":result, "asu_score":str(a), "opponent_score":str(b),
                       "source_page":"25", "source_title":"ASU official record book",
                       "site_type":"UNKNOWN", "game_date":"", "status":"PROVISIONAL_SUPPLEMENTAL_IDENTITY"}
                      for i,(op,result,a,b) in enumerate(CANDIDATES,1)]
        census = []
        for year in range(1911,1950):
            season = f"{year}-{year+1}"
            w,l = COUNTS.get(year,(0,0))
            off = mod.AGGREGATES.get(season)
            if year == 1920: off = (11,3)
            census.append({"season_label":season, "activity":"NO_TEAM" if year==1915 else "ACTIVE",
                           "inherited_accepted_rows":str(w+l), "inherited_accepted_wins":str(w),
                           "inherited_accepted_losses":str(l), "new_supplemental_provisional_rows":"10" if year==1920 else "0",
                           "source_institutional_aggregate_wins":str(off[0]) if off else "",
                           "source_institutional_aggregate_losses":str(off[1]) if off else "",
                           "source_institutional_aggregate_games":str(sum(off)) if off else "",
                           "census_class":"AGGREGATE_ONLY_UNIDENTIFIED" if season in mod.AGGREGATES else "INHERITED_ACCEPTED_REFERENCE_ONLY"})
        issues = [{"issue_id":id, "season":id[7:14],"issue_class":"UNKNOWN",
                   "authority_state":"STAGE1_BLOCKING"} for id in ISSUES]
        members = {"inputs/original-checkpoints-0001-0006-transport.zip":transport,
                   "stage1/complete-mechanical-season-census.csv":mod.write_csv(census),
                   "stage1/retained-1920-21-provisional-candidates.csv":mod.write_csv(candidates),
                   "stage1/exact-remaining-source-blockers-and-acceptance-prerequisites.csv":mod.write_csv(issues),
                   "stage1/unaligned-and-separate-research-issues-preserved.csv":b"issue,status\n1943,ACCOMPLISHMENT_SEPARATE\n"}
        manifest = {"checkpoint_number":18,"research_base_sha":mod.BASE,
                    "member_sha256": {k:mod.sha(v) for k,v in members.items()},
                    "member_bytes": {k:len(v) for k,v in members.items()}}
        self.input.write_bytes(zbytes({**members,"manifest.json":mod.jb(manifest)}))

    def make_parent(self, accept=True):
        return mod.materialize(self.input,self.source,self.input_sha,
                               mod.ORIGINAL_BLOB,self.parent,accept=accept)

    def make_authority(self):
        with zipfile.ZipFile(self.parent) as z:
            ledger_hash = mod.sha(z.read("stage1-identified-game-ledger.csv"))
            census_hash = mod.sha(z.read("stage1-season-census.csv"))
        payload = {"schema_version":1,"authority_type":"OWNER_APPROVED_EXPANSION_STAGE1_ACCOUNTING","cases":[{
            "school_key":"arizona-state","parent_sha256":mod.sha(self.parent.read_bytes()),
            "research_base_sha":mod.BASE,"owner_disposition":"https://github.com/example/issues/1",
            "identified_ledger_sha256":ledger_hash,"census_sha256":census_hash,
            "aggregate_only_seasons":[{"season":s,"institutional_record":{"wins":w,"losses":l,"games":w+l},
                **({"exception_kind":"EXACT_WARTIME_NONFOUNDING_1943_44"} if s=="1943-1944" else {})}
                for s,(w,l) in mod.AGGREGATES.items()],
            "accounting_contradiction":{"season":"1920-1921","official":{"wins":11,"losses":3,"games":14},
                "identified":{"wins":9,"losses":2,"games":11},
                "arithmetic_only_difference":{"wins":2,"losses":1,"games":3}},
            "contested_representation":{"season":"1920-1921","literal_assertion":"ASC W42-13",
                "inherited_game_id":"ASU-STG2-PRE1950-1920-21-001","inherited_result":"Northern Arizona W45-13",
                "disposition":"TERMINAL_CONTESTED_SOURCE_REPRESENTATION__NOT_IDENTITY_RESOLVED__NO_ROW_ADDED"},
        }]}
        self.registry.write_bytes(mod.jb(payload))

    def test_generic_parent_has_all_accepted_evidence_and_two_research_families(self):
        out = self.make_parent()
        self.assertEqual(out["status"], "BLOCKED_PARENT_MATERIALIZED")
        self.assertEqual((out["inherited_identified"], out["accepted_supplemental"], out["aggregate_unidentified"]),
                         (469, 10, 41))
        with zipfile.ZipFile(self.parent) as z:
            files = set(z.namelist())
            self.assertEqual(set(json.loads(z.read("manifest.json"))["files"][0]), {"path", "size", "sha256"})
            self.assertNotIn("member_sha256", json.loads(z.read("manifest.json")))
            required = {"stage1-status.json", "stage1-residuals.csv", "stage1-identified-game-ledger.csv",
                        "stage1-season-census.csv", "source-explicit-aggregate-only-seasons.csv",
                        "early-period-season-accounting.csv", "early-reconciliation-summary.json",
                        "terminal-contested-source-representation.json", "original-recovery-checkpoint-0018.zip",
                        "original-research-base-source-games.csv", "separate-source-questions.csv"}
            self.assertTrue(required.issubset(files), required-files)
            led = mod.read_csv(z.read("stage1-identified-game-ledger.csv"))
            self.assertEqual(Counter(r["authority"] for r in led), {"REUSE_INHERITED":469, "NEW_SUPPLEMENTAL_SOURCE_VERIFIED":10})
            self.assertEqual(len({r["research_game_id"] for r in led}),479)
            self.assertTrue(all(r["literal_raw_text"] for r in led))
            self.assertNotIn("ASC", {r["source_opponent_label"] for r in led if r["season_label"]=="1920-1921"})
            census = mod.read_csv(z.read("stage1-season-census.csv"))
            self.assertEqual(len(census),39)
            self.assertEqual(next(r for r in census if r["season"]=="1920-1921")["identified_games"],"11")
            blockers = mod.read_csv(z.read("stage1-residuals.csv"))
            self.assertEqual(len(blockers),2)
            self.assertEqual({r["residual_class"] for r in blockers},
                {"EARLY_SOURCE_EXPLICIT_AGGREGATE_ONLY_GAME_IDENTITIES_UNKNOWN",
                 "EARLY_DETAILED_VS_OVERALL_CLUB_ACCOUNTING_CONTRADICTION"})
            self.assertEqual(len(mod.read_csv(z.read("original-six-source-blockers-and-provisional-precondition.csv"))),7)
            self.assertEqual(json.loads(z.read("stage1-status.json"))["stage1_complete"],False)
            self.assertFalse(json.loads(z.read("terminal-contested-source-representation.json"))["same_game_identity_proven"])

    def test_deterministic_parent_exact_bytes(self):
        self.make_parent()
        original=self.parent.read_bytes()
        self.make_parent()
        self.assertEqual(original,self.parent.read_bytes())

    def test_wrong_research_base_source_blob_rejected(self):
        with self.assertRaisesRegex(ValueError,"UNAPPROVED_INPUT_IDENTITY"):
            mod.materialize(self.input,self.source,self.input_sha,"0"*40,self.parent,accept=True)

    def test_no_unverified_provisional_acceptance(self):
        with self.assertRaisesRegex(ValueError,"ONLY_VERIFIED_AND_OWNER_PERMITTED"):
            self.make_parent(False)

    def test_check_and_retain_exact_wartime_population(self):
        self.make_parent()
        with zipfile.ZipFile(self.parent) as z:
            cov=mod.read_csv(z.read("source-explicit-aggregate-only-seasons.csv"))
        self.assertEqual({r["season"] for r in cov},{"1916-1917","1917-1918","1919-1920","1943-1944"})
        self.assertEqual(sum(int(r["official_games"]) for r in cov),41)
        self.assertIn("wartime exception",next(r for r in cov if r["season"]=="1943-1944")["source_note"])

    def test_contested_representation_preserved_not_reclassified(self):
        self.make_parent()
        with zipfile.ZipFile(self.parent) as z:
            evidence=json.loads(z.read("early-reconciliation-summary.json"))
            self.assertIsNone(evidence["simple_union_implied_overlap_games"])
            self.assertEqual(len(evidence["direct_candidate_result_conflicts"]),1)
            self.assertEqual(evidence["direct_candidate_result_conflicts"][0]["identity_relationship"],
                "NOT_ESTABLISHED; neither duplicate nor additional game inferred")
            row=mod.read_csv(z.read("early-period-season-accounting.csv"))[0]
        self.assertEqual((row["official_w"],row["official_l"],row["identified_w"],row["identified_l"]),("11","3","9","2"))

    def _generic_authority_fixture(self):
        import research_stage1_early_accounting_closeout as current
        self.make_parent()
        with zipfile.ZipFile(self.parent) as z:
            read=lambda f: mod.read_csv(z.read(f))
            agg=read("source-explicit-aggregate-only-seasons.csv")
            summary=json.loads(z.read("early-reconciliation-summary.json"))
            case={
                "school_key":"arizona-state", "parent_checkpoint_sha256":mod.sha(self.parent.read_bytes()),
                "research_base_sha":mod.BASE, "owner_disposition":"https://github.com/example/project/issues/1",
                "identified_ledger_sha256":mod.sha(z.read("stage1-identified-game-ledger.csv")),
                "season_census_sha256":mod.sha(z.read("stage1-season-census.csv")),
                "identified_rows":479, "accepted_nonexcluded_rows":479,
                "aggregate_only_seasons":[{
                    "season":x["season"],
                    "institutional_record":{"wins":int(x["official_w"]),"losses":int(x["official_l"]),"games":int(x["official_games"])},
                    "identified_record":{"wins":0,"losses":0,"games":0},
                    "source_note":x["source_note"],
                    **({"exception_kind":"EXACT_WARTIME_NONFOUNDING_1943_44"} if x["season"]=="1943-1944" else {})
                } for x in agg],
                "accounting_contradiction_seasons":[{
                    "season":"1920-1921",
                    "institutional_record":{"wins":11,"losses":3,"games":14},
                    "identified_record":{"wins":9,"losses":2,"games":11},
                    "mechanical_delta":{"wins":2,"losses":1,"games":3},
                }],
                "accounting_summary":{k:summary[k] for k in (
                    "official_season_aggregate","chronological_detail",
                    "club_high_school_aggregate","simple_union_implied_overlap_games")},
                "minimum_direct_result_conflicts":1,
            }
            registry={"schema_version":1,"authority_type":"OWNER_APPROVED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT","cases":[case]}
        self.registry.write_bytes(current.json_bytes(registry))
        return current

    def test_current_generic_closeout_and_independent_verify(self):
        current=self._generic_authority_fixture()
        psha=current.digest(self.parent.read_bytes())
        report=current.audit_checkpoint(self.parent,expected_parent_sha256=psha,registry=self.registry)
        self.assertEqual(report["status"],current.ELIGIBLE,report["defects"])
        self.report.write_bytes(current.json_bytes(report))
        asha=current.digest(self.report.read_bytes())
        current.closeout(self.parent,self.report,self.successor,parent_sha=psha,audit_sha=asha,registry=self.registry)
        ssha=current.digest(self.successor.read_bytes())
        result=current.verify_closeout(self.parent,self.successor,self.report,parent_sha=psha,successor_sha=ssha,
                                      audit_sha=asha,registry=self.registry)
        self.assertEqual(result["status"],current.VERIFIED,result["defects"])
        self.assertTrue(result["stage1_complete"])
        self.assertEqual(sum(x["unidentified_record"]["games"] for x in result["aggregate_coverage"]),41)
        with zipfile.ZipFile(self.successor) as z:
            terminal=json.loads(z.read("terminal-contested-source-representation.json"))
            self.assertFalse(terminal["same_game_identity_proven"])
            self.assertEqual(terminal["new_rows_created_from_ASC_assertion"],0)
            self.assertEqual(json.loads(z.read("stage1-status.json"))["blocking_residual_count"],0)

    def test_generic_audit_rejects_missing_owner_authority(self):
        current=self._generic_authority_fixture()
        self.registry.write_bytes(current.json_bytes({"schema_version":1,
            "authority_type":"OWNER_APPROVED_EARLY_HISTORY_ACCOUNTING_CLOSEOUT","cases":[]}))
        r=current.audit_checkpoint(self.parent,expected_parent_sha256=current.digest(self.parent.read_bytes()),registry=self.registry)
        self.assertIn("NO_EXACT_OWNER_AUTHORITY",r["defects"])
        self.assertFalse(r["stage1_complete"])

    def test_generic_verify_rejects_changed_closeout_bytes(self):
        current=self._generic_authority_fixture();psha=current.digest(self.parent.read_bytes())
        report=current.audit_checkpoint(self.parent,expected_parent_sha256=psha,registry=self.registry)
        self.report.write_bytes(current.json_bytes(report));asha=current.digest(self.report.read_bytes())
        current.closeout(self.parent,self.report,self.successor,parent_sha=psha,audit_sha=asha,registry=self.registry)
        with zipfile.ZipFile(self.successor) as z:
            members={n:z.read(n) for n in z.namelist()}
        members["terminal-contested-source-representation.json"]=b"{}\n"
        self.successor.write_bytes(zbytes(members))
        v=current.verify_closeout(self.parent,self.successor,self.report,parent_sha=psha,
           successor_sha=current.digest(self.successor.read_bytes()),audit_sha=asha,registry=self.registry)
        self.assertEqual(v["status"],"FAIL")
        self.assertFalse(v["stage1_complete"])

    def test_modified_real_source_content_rejected(self):
        self.source.write_bytes(self.source.read_bytes()+b"\n")
        with self.assertRaisesRegex(ValueError,"IMMUTABLE_SOURCE_BLOB_MISMATCH"):
            self.make_parent()

    def test_changed_checkpoint_hash_rejected(self):
        with self.assertRaisesRegex(ValueError,"UNAPPROVED_INPUT_IDENTITY"):
            mod.materialize(self.input,self.source,"0"*64,mod.ORIGINAL_BLOB,self.parent,accept=True)

if __name__=="__main__":unittest.main()
