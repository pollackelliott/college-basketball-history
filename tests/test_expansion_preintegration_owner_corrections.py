"""Fail-closed tests for owner-approved pre-Integration correction overlays."""
import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from expansion_preintegration_owner_corrections import (
    OwnerCorrectionStop,
    AUTHORITY_KIND,
    canonical,
    digest,
    project_effective_source_rows,
    validate_reference,
)


class OwnerCorrectionTests(unittest.TestCase):
    def setUp(self):
        self.school = "sample"
        self.research_base = "a" * 40
        self.freeze_sha = "b" * 64
        self.ids = ["EXP-1", "EXP-2", "EXP-3"]
        self.original = [
            {
                "source_game_id": sid,
                "source_program_key": "sample",
                "season_label": "1963-1964",
                "source_opponent_label": opp,
                "normalized_opponent_key": opp.lower(),
                "team_score": score,
                "opponent_score": other,
                "game_date": "",
                "curated_site_type": "SOURCE_PROGRAM_HOME",
                "curated_venue_name": "Old Hall",
                "city": "Home",
                "state": "CA",
                "raw_text": "literal historic source evidence",
                "source_site_candidate": "vs.",
                "source_page": "record book 123",
                "played_result": "L",
                "curated_game_type": "REGULAR_SEASON",
            }
            for sid, opp, score, other in (
                ("EXP-1", "Alpha", "47", "76"),
                ("EXP-2", "Beta", "48", "74"),
                ("EXP-3", "Gamma", "65", "95"),
            )
        ]
        patch_values = [
            {"game_date": "1963-12-04", "team_score": "48",
             "opponent_score": "74", "curated_site_type": "OPPONENT_HOME",
             "curated_venue_name": "Alpha Arena", "city": "Alpha City", "state": "OH"},
            {"game_date": "1963-12-02", "team_score": "47",
             "opponent_score": "76", "curated_site_type": "OPPONENT_HOME",
             "curated_venue_name": "", "city": "Beta City", "state": "OH"},
            {"game_date": "1963-12-20", "team_score": "66",
             "curated_site_type": "OPPONENT_HOME", "curated_venue_name": "Gamma Hall",
             "city": "Gamma City", "state": "NY"},
        ]
        approved_rows = []
        for row, patches in zip(self.original, patch_values):
            after = dict(row, **patches)
            approved_rows.append({
                "source_game_id": row["source_game_id"],
                "immutable_original_row_sha256": digest(canonical(row)),
                "hypothetical_approved_overlay_row_sha256": digest(canonical(after)),
                "exact_owner_approved_field_changes": {
                    key: {"before": row[key], "approved_after": value}
                    for key, value in patches.items()
                },
            })
        self.artifact = {
            "kind": "GENERIC_OWNER_APPROVED_PREINTEGRATION_CORRECTION",
            "authority": {
                "school": self.school,
                "research_base_sha": self.research_base,
                "frozen_original_zip_sha256": self.freeze_sha,
                "protected_main_sha": "c" * 40,
            },
            "approval": {
                "owner_response": "APPROVED. Proceed",
                "exact_scope": "Exactly three authenticated source-game rows",
                "owner_gate_1_approval": "NOT_IMPLIED",
                "owner_gate_2_approval": "NOT_IMPLIED",
            },
            "approved_source_rows": approved_rows,
        }
        self.update_ref()

    def update_ref(self):
        self.raw = canonical(self.artifact)
        self.ref = {
            "authority_kind": AUTHORITY_KIND,
            "approval_issue_url": "https://github.com/example/repository/issues/23",
            "school_key": self.school,
            "freeze_sha256": self.freeze_sha,
            "sha256": digest(self.raw),
            "owner_checkpoint_sha256": digest(self.raw),
            "approved_source_game_ids": self.ids[:],
            "path": "approved/owner-correction.json",
        }

    def project(self, *, original=None, artifact=None, reference=None):
        return project_effective_source_rows(
            self.raw if artifact is None else artifact,
            self.ref if reference is None else reference,
            self.original if original is None else original,
            school=self.school,
            freeze_sha=self.freeze_sha,
            research_base=self.research_base,
        )

    def test_effective_rows_only_preserve_literal_and_opponents_and_hashes(self):
        untouched = copy.deepcopy(self.original)
        a, receipt = self.project()
        b, proof = self.project()
        self.assertEqual((a, receipt), (b, proof))
        self.assertEqual(self.original, untouched)
        self.assertEqual(receipt["artifact_sha256"], digest(self.raw))
        self.assertEqual(receipt["approved_source_game_ids"], self.ids)
        self.assertEqual(receipt["effective_source_rows_sha256"], digest(canonical(a)))
        self.assertFalse(receipt["owner_gate_1_approval"])
        self.assertEqual([x["normalized_opponent_key"] for x in a],
                         [x["normalized_opponent_key"] for x in untouched])
        for orig, now in zip(untouched, a):
            for col in ("source_game_id", "raw_text", "source_site_candidate",
                        "source_page", "played_result", "curated_game_type",
                        "source_opponent_label", "normalized_opponent_key"):
                self.assertEqual(orig[col], now[col])
        self.assertEqual(a[1]["curated_venue_name"], "")
        self.assertEqual(a[2]["team_score"], "66")

    def test_reject_hash_stale_or_fake_approval(self):
        with self.assertRaisesRegex(OwnerCorrectionStop, "ARTIFACT_SHA_MISMATCH"):
            self.project(artifact=self.raw + b"\n")
        tampered = copy.deepcopy(self.original)
        tampered[0]["raw_text"] = "different literal evidence"
        with self.assertRaisesRegex(OwnerCorrectionStop, "ORIGINAL_SOURCE_HASH_STALE"):
            self.project(original=tampered)
        changed = dict(self.ref, freeze_sha256="c"*64)
        with self.assertRaisesRegex(OwnerCorrectionStop, "REFERENCE_FREEZE_BINDING"):
            self.project(reference=changed)
        for k in ("research_base_sha", "frozen_original_zip_sha256", "school"):
            bad = copy.deepcopy(self.artifact)
            bad["authority"][k] = "d" * 40 if k == "research_base_sha" else "fake"
            ref = self.make_ref(bad)
            with self.assertRaisesRegex(OwnerCorrectionStop, "APPROVAL_AUTHORITY_BINDING"):
                self.project(artifact=canonical(bad), reference=ref)
        bad = copy.deepcopy(self.artifact)
        bad["approval"]["owner_response"] = "Not approved"
        with self.assertRaisesRegex(OwnerCorrectionStop, "EXPLICIT_OWNER_APPROVAL_MISSING"):
            self.project(artifact=canonical(bad), reference=self.make_ref(bad))

    def make_ref(self, obj):
        digest_value = digest(canonical(obj))
        return dict(self.ref, sha256=digest_value,
                    owner_checkpoint_sha256=digest_value)

    def test_reject_fourth_row_or_missing_row_or_set_mismatch(self):
        bad = copy.deepcopy(self.artifact)
        fourth = copy.deepcopy(bad["approved_source_rows"][0])
        fourth["source_game_id"] = "EXP-4"
        bad["approved_source_rows"].append(fourth)
        with self.assertRaisesRegex(OwnerCorrectionStop, "APPROVED_SOURCE_SET_MISMATCH"):
            self.project(artifact=canonical(bad), reference=self.make_ref(bad))
        bad = copy.deepcopy(self.artifact)
        bad["approved_source_rows"].pop()
        with self.assertRaisesRegex(OwnerCorrectionStop, "APPROVED_SOURCE_SET_MISMATCH"):
            self.project(artifact=canonical(bad), reference=self.make_ref(bad))
        with self.assertRaisesRegex(OwnerCorrectionStop, "SOURCE_ID_SET_INVALID"):
            validate_reference(dict(self.ref, approved_source_game_ids=self.ids[:2]+self.ids[:1]),
                               school=self.school,freeze_sha=self.freeze_sha)

    def test_reject_extra_fields_and_opponent_game_type_raw_mutations(self):
        for field in ("normalized_opponent_key","source_opponent_label",
                      "curated_game_type","raw_text","source_site_candidate",
                      "source_page","played_result","source_game_id",
                      "date_precision"):
            bad = copy.deepcopy(self.artifact)
            bad["approved_source_rows"][0]["exact_owner_approved_field_changes"][field] = {
                "before": self.original[0].get(field, ""),
                "approved_after": "malicious",
            }
            with self.subTest(field=field), self.assertRaisesRegex(
                OwnerCorrectionStop, "UNAUTHORIZED_FIELD"
            ):
                self.project(artifact=canonical(bad), reference=self.make_ref(bad))

    def test_reject_stale_before_after_and_row_hashes(self):
        for tag in ("before","approved_after"):
            bad = copy.deepcopy(self.artifact)
            bad["approved_source_rows"][0]["exact_owner_approved_field_changes"]["team_score"][tag] = "999"
            with self.subTest(tag=tag), self.assertRaises(OwnerCorrectionStop):
                self.project(artifact=canonical(bad), reference=self.make_ref(bad))
        for field in ("immutable_original_row_sha256",
                      "hypothetical_approved_overlay_row_sha256"):
            bad = copy.deepcopy(self.artifact)
            bad["approved_source_rows"][0][field] = "0" * 64
            with self.subTest(field=field), self.assertRaises(OwnerCorrectionStop):
                self.project(artifact=canonical(bad), reference=self.make_ref(bad))

    def test_reject_wrong_identity_and_disallowed_date_score_site(self):
        bad = copy.deepcopy(self.original)
        bad[0]["source_program_key"] = "other"
        with self.assertRaisesRegex(OwnerCorrectionStop, "SOURCE_PROGRAM_CHANGED"):
            # Updating original hash alone cannot change the bound school.
            obj = copy.deepcopy(self.artifact)
            obj["approved_source_rows"][0]["immutable_original_row_sha256"] = digest(canonical(bad[0]))
            self.project(original=bad, artifact=canonical(obj),reference=self.make_ref(obj))

    def test_reject_unbound_scope(self):
        for field in ("authority_kind","approval_issue_url","owner_checkpoint_sha256",
                      "path","approved_source_game_ids"):
            bad = dict(self.ref)
            bad[field] = None
            with self.subTest(field=field), self.assertRaises(OwnerCorrectionStop):
                self.project(reference=bad)


if __name__ == "__main__":
    unittest.main()
