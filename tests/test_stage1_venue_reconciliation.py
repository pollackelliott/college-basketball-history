"""Regression tests for explicit, hash-bound Stage 1 venue identity reuse."""
import hashlib
import csv
import json
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from onboarding_plan import WorkflowError  # noqa: E402
from onboarding_hardening import venue_summary_consistency_report  # noqa: E402
from stage1_venue_reconciliation import (  # noqa: E402
    explicit_reuse_locality_compatible,
    load_venue_reconciliation,
)
from stage_research_portfolio import (  # noqa: E402
    build_stage1_reconciliation_inventory,
    rebase_venues,
    rebase_program_aliases,
    program_alias_inventory,
    refresh_local_venue_assignment_summaries,
    venue_reconciliation_inventory,
)


def sha(b):
    return hashlib.sha256(b).hexdigest()


class ExplicitVenueReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.package = self.root / "package.zip"
        venues_bytes = b"venue_key,canonical_name,city,state\nreitz-arena,Reitz Arena,Baltimore,MD\n"
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        self.local = {
            "source_program_key": "test-school",
            "venue_key": "reitz-arena", "venue_id": "",
            "canonical_name": "Reitz Arena", "aliases": "",
            "city": "Baltimore", "state": "MD",
            "known_opened": "", "known_closed": "", "venue_date_precision": "unknown",
            "first_assigned_game": "1985-03-02", "last_assigned_game": "1985-03-04",
            "notes": "Historical identity: RESOLVED. Global registration: PENDING_CURRENT_MAIN_REBASE.",
        }
        self.global_row = {
            "venue_id": "VEN-000925", "venue_key": "reitz-arena-loyola-maryland",
            "display_name": "Reitz Arena", "city": "Baltimore", "state": "MD",
            "opened": "", "closed": "", "identity_status": "TEST", "notes": "",
        }
        self.doc = {
            "schema_version": 1,
            "school_key": "test-school",
            "owner_approval_basis": "Control Center disposition: same physical venue",
            "expected_research_zip_sha256": sha(self.package.read_bytes()),
            "expected_venues_sha256": sha(venues_bytes),
            "mappings": [{
                "local_venue_key": "reitz-arena",
                "expected_local_name": "Reitz Arena",
                "expected_local_city": "Baltimore", "expected_local_state": "MD",
                "global_venue_id": "VEN-000925",
                "global_venue_key": "reitz-arena-loyola-maryland",
                "expected_global_city": "Baltimore", "expected_global_state": "MD",
                "resolution_basis": "Loyola reference + explicit owner authority",
            }],
        }
        self.spec = self.root / "reconciliation.json"
        self.save()

    def save(self):
        self.spec.write_text(json.dumps(self.doc), encoding="utf-8")

    def load(self):
        return load_venue_reconciliation(
            self.spec, school_key="test-school", package_path=self.package,
            local_venues=[dict(self.local)], global_venues=[dict(self.global_row)],
        )

    def test_explicit_reuse_accepts_jm_jamaica_representation_equivalence(self):
        local = {
            "city": "Montego Bay",
            "state": "JM",
        }
        global_row = {
            "city": "Montego Bay",
            "state": "Jamaica",
        }
        mapping = {
            "allow_locality_variant": False,
            "locality_variant_basis": "",
        }
        self.assertTrue(
            explicit_reuse_locality_compatible(local, global_row, mapping)
        )
        self.assertFalse(
            explicit_reuse_locality_compatible(
                local,
                {"city": "Montego Bay", "state": "BS"},
                mapping,
            )
        )

    def test_explicit_locality_variant_predicate_fails_closed(self):
        mapping = {
            "allow_locality_variant": True,
            "locality_variant_basis": "Documented representation difference.",
        }
        self.assertTrue(
            explicit_reuse_locality_compatible(
                {"city": "Old City", "state": "NY"},
                {"city": "New City", "state": "NY"},
                mapping,
            )
        )
        self.assertTrue(
            explicit_reuse_locality_compatible(
                {"city": "George Town", "state": "Grand Cayman"},
                {"city": "George Town", "state": "Cayman Islands"},
                mapping,
            )
        )
        self.assertFalse(
            explicit_reuse_locality_compatible(
                {"city": "Old City", "state": "NY"},
                {"city": "New City", "state": "PA"},
                mapping,
            )
        )

    def test_inventory_and_rebase_share_explicit_identity(self):
        mapping, meta = self.load()
        result = venue_reconciliation_inventory(
            [dict(self.local)], [dict(self.global_row)], [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(result["blocker_count"], 0)
        item = result["rows"][0]
        self.assertEqual(item["classification"], "SAFE_REPRESENTATION_REUSE")
        self.assertEqual(item["target_venue_id"], "VEN-000925")
        self.assertEqual(item["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        whole = build_stage1_reconciliation_inventory(
            "test-school", [dict(self.local)], [dict(self.global_row)], [], [], [], [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(whole["status"], "PASS")
        locals_, globals_, _, outcomes = rebase_venues(
            "test-school", [dict(self.local)], [dict(self.global_row)], [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(locals_[0]["venue_key"], "reitz-arena-loyola-maryland")
        self.assertEqual(locals_[0]["venue_id"], "VEN-000925")
        self.assertEqual(len(globals_), 1)
        self.assertEqual(outcomes[0]["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        self.assertEqual(meta["frozen_venues_sha256"], self.doc["expected_venues_sha256"])

    def test_no_spec_keeps_ambiguous_stop(self):
        result = venue_reconciliation_inventory(
            [dict(self.local)], [dict(self.global_row)], []
        )
        self.assertEqual(result["blocker_count"], 1)

    def test_ordinary_repeated_venue_reuse_needs_no_explicit_mapping(self):
        local_rows = [
            {
                **dict(self.local),
                "venue_key": "shared-arena",
                "venue_id": "",
                "canonical_name": "Shared Arena",
                "city": "Example City",
                "state": "NY",
                "notes": "",
                "first_assigned_game": "2000-01-01",
                "last_assigned_game": "2000-01-01",
            },
            {
                **dict(self.local),
                "venue_key": "shared-arena",
                "venue_id": "",
                "canonical_name": "Shared Arena",
                "city": "Example City",
                "state": "NY",
                "notes": "",
                "first_assigned_game": "2001-01-01",
                "last_assigned_game": "2001-01-01",
            },
        ]
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000100",
            "venue_key": "shared-arena",
            "display_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }

        result = venue_reconciliation_inventory(
            local_rows,
            [global_row],
            [],
        )

        self.assertEqual(result["blocker_count"], 0)
        self.assertEqual(
            [row["target_venue_id"] for row in result["rows"]],
            ["VEN-000100", "VEN-000100"],
        )

    def test_package_hash_mismatch_fails(self):
        self.doc["expected_research_zip_sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(WorkflowError, "package SHA-256 mismatch"):
            self.load()

    def test_member_hash_mismatch_fails(self):
        self.doc["expected_venues_sha256"] = "0" * 64
        self.save()
        with self.assertRaisesRegex(WorkflowError, "venues.csv SHA-256 mismatch"):
            self.load()

    def test_unknown_local_key_fails(self):
        self.doc["mappings"][0]["local_venue_key"] = "wrong-key"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "unknown local key"):
            self.load()

    def test_stale_global_id_fails(self):
        self.doc["mappings"][0]["global_venue_id"] = "VEN-111111"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "stale global venue ID/key"):
            self.load()

    def test_stale_global_key_fails(self):
        self.doc["mappings"][0]["global_venue_key"] = "wrong-key"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "stale global venue ID/key"):
            self.load()

    def test_global_geography_mismatch_fails(self):
        self.doc["mappings"][0]["expected_global_state"] = "NJ"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "global geography mismatch"):
            self.load()

    def test_local_identity_drift_fails(self):
        self.doc["mappings"][0]["expected_local_name"] = "Reitz Gym"
        self.save()
        with self.assertRaisesRegex(WorkflowError, "frozen local identity drift"):
            self.load()

    def test_duplicate_key_fails(self):
        self.doc["mappings"].append(dict(self.doc["mappings"][0]))
        self.save()
        with self.assertRaisesRegex(WorkflowError, "repeats local key"):
            self.load()

    def test_blank_key_row_index_reuse_is_hash_bound_and_safe(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Reitz Arena,Baltimore,MD\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        local = {**dict(self.local), "venue_key": "", "venue_id": ""}
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "Reitz Arena",
            "expected_local_city": "Baltimore",
            "expected_local_state": "MD",
            "global_venue_id": "VEN-000925",
            "global_venue_key": "reitz-arena-loyola-maryland",
            "expected_global_city": "Baltimore",
            "expected_global_state": "MD",
            "resolution_basis": "Exact immutable frozen row and current-main identity.",
        }]
        self.save()

        mapping, meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[local],
            global_venues=[dict(self.global_row)],
        )
        inventory = venue_reconciliation_inventory(
            [dict(local)],
            [dict(self.global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            inventory["rows"][0]["resolution"],
            "REUSE_EXPLICIT_RECONCILIATION",
        )
        staged, globals_, _names, outcomes = rebase_venues(
            "test-school",
            [dict(local)],
            [dict(self.global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(staged[0]["venue_key"], "reitz-arena-loyola-maryland")
        self.assertEqual(staged[0]["venue_id"], "VEN-000925")
        self.assertEqual(len(globals_), 1)
        self.assertEqual(outcomes[0]["resolution"], "REUSE_EXPLICIT_RECONCILIATION")
        self.assertEqual(meta["schema_version"], 2)

    def test_row_index_selector_rejects_nonblank_local_key(self):
        self.doc["schema_version"] = 2
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "Reitz Arena",
            "expected_local_city": "Baltimore",
            "expected_local_state": "MD",
            "global_venue_id": "VEN-000925",
            "global_venue_key": "reitz-arena-loyola-maryland",
            "expected_global_city": "Baltimore",
            "expected_global_state": "MD",
            "resolution_basis": "Row-index selectors are blank-key only.",
        }]
        self.save()
        with self.assertRaisesRegex(
            WorkflowError, "limited to blank-key frozen rows"
        ):
            self.load()

    def test_blank_key_row_index_can_select_intentional_researched_split(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        local = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "first_assigned_game": "1961-03-01",
            "last_assigned_game": "1962-03-01",
        }
        original = {
            **dict(self.global_row),
            "venue_id": "VEN-000100",
            "venue_key": "shared-arena-1955",
            "display_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "identity_status": "RESEARCHED_SPLIT",
        }
        replacement = {
            **dict(self.global_row),
            "venue_id": "VEN-000101",
            "venue_key": "shared-arena-1988",
            "display_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "identity_status": "RESEARCHED_SPLIT",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "global_venue_id": "VEN-000100",
            "global_venue_key": "shared-arena-1955",
            "expected_global_city": "Example City",
            "expected_global_state": "NY",
            "resolution_basis": "Exact immutable row plus settled split identity.",
        }]
        self.save()

        mapping, _meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[local],
            global_venues=[original, replacement],
        )
        inventory = venue_reconciliation_inventory(
            [dict(local)],
            [dict(original), dict(replacement)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        row = inventory["rows"][0]
        self.assertEqual(row["target_venue_id"], "VEN-000100")
        self.assertIn("INTENTIONAL_RESEARCHED_SPLIT_NAME_OVERLAP", row["issues"])

    def test_blank_key_redundant_row_can_be_dropped_without_changing_frozen_input(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena-1955,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        blank = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        keyed = {
            **dict(blank),
            "venue_key": "shared-arena-1955",
            "venue_id": "VEN-000100",
        }
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000100",
            "venue_key": "shared-arena-1955",
            "display_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "DROP_REDUNDANT_LOCAL_ROW",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "resolution_basis": "Broad blank-key row is redundant with retained keyed row.",
        }]
        self.save()

        mapping, _meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[blank, keyed],
            global_venues=[global_row],
        )
        inventory = venue_reconciliation_inventory(
            [dict(blank), dict(keyed)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            inventory["rows"][0]["classification"],
            "SAFE_REPRESENTATION_DROP",
        )
        staged, globals_, _names, outcomes = rebase_venues(
            "test-school",
            [dict(blank), dict(keyed)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(len(staged), 1)
        self.assertEqual(staged[0]["venue_key"], "shared-arena-1955")
        self.assertEqual(len(globals_), 1)
        self.assertEqual(outcomes[0]["resolution"], "DROP_REDUNDANT_LOCAL_ROW")

    def test_redundant_split_drop_preserves_identical_site_rule_and_counts(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena-old,Shared Arena,Example City,NY\n"
            b"shared-arena-new,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        common = {
            **dict(self.local),
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "site_rule": "Per-game assignment; venue identity does not establish H/A/N.",
            "source_basis": "Accepted row-level site research.",
            "notes": "Representation metadata only.",
        }
        blank = {
            **common,
            "venue_key": "",
            "venue_id": "",
            "games_currently_assigned": "25",
            "first_assigned_game": "1975-12-26",
            "last_assigned_game": "2022-03-29",
        }
        old = {
            **common,
            "venue_key": "shared-arena-old",
            "venue_id": "VEN-000100",
            "games_currently_assigned": "18",
            "first_assigned_game": "1951-01-01",
            "last_assigned_game": "1967-12-31",
        }
        new = {
            **common,
            "venue_key": "shared-arena-new",
            "venue_id": "VEN-000101",
            "games_currently_assigned": "7",
            "first_assigned_game": "1975-12-26",
            "last_assigned_game": "2022-03-29",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "DROP_REDUNDANT_LOCAL_ROW",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "resolution_basis": "Aggregate representation is exactly preserved by retained split rows.",
        }]
        self.save()

        mapping, meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[blank, old, new],
            global_venues=[dict(self.global_row)],
        )
        item = meta["mappings"][0]
        self.assertEqual(item["dropped_games_currently_assigned"], "25")
        self.assertEqual(item["retained_games_currently_assigned"], "25")
        inventory = venue_reconciliation_inventory(
            [dict(blank), dict(old), dict(new)],
            [],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            inventory["rows"][0]["classification"],
            "SAFE_REPRESENTATION_DROP",
        )

    def test_redundant_split_drop_rejects_different_site_rule(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena-old,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        blank = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "site_rule": "Protected rule A.",
        }
        keyed = {
            **dict(blank),
            "venue_key": "shared-arena-old",
            "venue_id": "VEN-000100",
            "site_rule": "Different rule B.",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "DROP_REDUNDANT_LOCAL_ROW",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "resolution_basis": "Attempted unsafe site-rule drop.",
        }]
        self.save()

        with self.assertRaisesRegex(
            WorkflowError, "cannot discard unique frozen site_rule authority"
        ):
            load_venue_reconciliation(
                self.spec,
                school_key="test-school",
                package_path=self.package,
                local_venues=[blank, keyed],
                global_venues=[dict(self.global_row)],
            )

    def test_redundant_split_drop_rejects_assignment_count_mismatch(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena-old,Shared Arena,Example City,NY\n"
            b"shared-arena-new,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        blank = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "games_currently_assigned": "25",
        }
        old = {
            **dict(blank),
            "venue_key": "shared-arena-old",
            "venue_id": "VEN-000100",
            "games_currently_assigned": "18",
        }
        new = {
            **dict(blank),
            "venue_key": "shared-arena-new",
            "venue_id": "VEN-000101",
            "games_currently_assigned": "6",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "DROP_REDUNDANT_LOCAL_ROW",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "resolution_basis": "Attempted incomplete partition.",
        }]
        self.save()

        with self.assertRaisesRegex(
            WorkflowError, "do not exactly partition the dropped row"
        ):
            load_venue_reconciliation(
                self.spec,
                school_key="test-school",
                package_path=self.package,
                local_venues=[blank, old, new],
                global_venues=[dict(self.global_row)],
            )

    def test_redundant_drop_rejects_relationship_authority(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena-1955,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        blank = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "relationship_type": "HOME",
        }
        keyed = {**dict(blank), "venue_key": "shared-arena-1955", "relationship_type": ""}
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "DROP_REDUNDANT_LOCAL_ROW",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "resolution_basis": "Attempted unsafe relationship drop.",
        }]
        self.save()

        with self.assertRaisesRegex(
            WorkflowError, "cannot discard venue relationship authority"
        ):
            load_venue_reconciliation(
                self.spec,
                school_key="test-school",
                package_path=self.package,
                local_venues=[blank, keyed],
                global_venues=[dict(self.global_row)],
            )

    def test_explicit_reuse_can_preserve_relationship_bearing_local_row(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Reilly Center,St. Bonaventure,NY\n"
            b"reilly-center-st-bonaventure,Reilly Center,Olean,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)

        relationship = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Reilly Center",
            "city": "St. Bonaventure",
            "state": "NY",
            "relationship_type": "HOME",
            "relationship_start": "1966-12-02",
            "relationship_end": "",
            "relationship_date_precision": "EXACT",
            "site_rule": "HOME relationship chronology with documented exceptions.",
            "source_basis": "Accepted facility chronology.",
            "notes": "Preserve school-local HOME relationship authority.",
            "venue_type": "ARENA",
            "games_currently_assigned": "0",
            "first_assigned_game": "",
            "last_assigned_game": "",
        }
        per_game = {
            **dict(relationship),
            "venue_key": "reilly-center-st-bonaventure",
            "venue_id": "VEN-000926",
            "city": "Olean",
            "relationship_type": "",
            "relationship_start": "",
            "relationship_end": "",
            "relationship_date_precision": "",
            "site_rule": "Per-game venue representation.",
            "source_basis": "Accepted row-level site research.",
            "notes": "Separate per-game representation.",
            "venue_type": "",
        }
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000926",
            "venue_key": "reilly-center-st-bonaventure",
            "display_name": "Reilly Center",
            "city": "Olean",
            "state": "NY",
        }

        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "Reilly Center",
            "expected_local_city": "St. Bonaventure",
            "expected_local_state": "NY",
            "global_venue_id": "VEN-000926",
            "global_venue_key": "reilly-center-st-bonaventure",
            "expected_global_city": "Olean",
            "expected_global_state": "NY",
            "allow_locality_variant": True,
            "locality_variant_basis": (
                "School-local locality label and global physical-venue locality "
                "refer to the same authenticated building."
            ),
            "preserve_local_representation": True,
            "resolution_basis": (
                "Reuse the exact physical identity while preserving the distinct "
                "school-local HOME relationship chronology."
            ),
        }]
        self.save()

        mapping, meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[relationship, per_game],
            global_venues=[global_row],
        )
        preserved = meta["mappings"][0]
        self.assertTrue(preserved["preserve_local_representation"])
        self.assertIn(
            "RELATIONSHIP_AUTHORITY_PRESENT",
            preserved["preservation_conflicts"],
        )

        inventory = venue_reconciliation_inventory(
            [dict(relationship), dict(per_game)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        row = inventory["rows"][0]
        self.assertEqual(row["classification"], "SAFE_REPRESENTATION_PRESERVE")
        self.assertEqual(
            row["resolution"],
            "REUSE_EXPLICIT_RECONCILIATION_PRESERVE_LOCAL_ROW",
        )
        self.assertIn(
            "EXPLICIT_REUSE_PRESERVES_RELATIONSHIP_LOCAL_ROW",
            row["issues"],
        )

        source_games = [
            {
                "source_game_id": "HOME-0001",
                "season_label": "1966-1967",
                "game_date": "1967-02-25",
                "curated_venue_name": "Reilly Center",
                "city": "St. Bonaventure",
                "state": "NY",
            }
        ]
        source_games.extend(
            {
                "source_game_id": f"HOME-{index:04d}",
                "season_label": "1999-2000",
                "game_date": "2000-01-01",
                "curated_venue_name": "Reilly Center",
                "city": "St. Bonaventure",
                "state": "NY",
            }
            for index in range(2, 784)
        )
        source_games.append(
            {
                "source_game_id": "HOME-0784",
                "season_label": "2025-2026",
                "game_date": "2026-03-01",
                "curated_venue_name": "Reilly Center",
                "city": "St. Bonaventure",
                "state": "NY",
            }
        )
        source_games.extend(
            {
                "source_game_id": f"OLEAN-{index:04d}",
                "season_label": "2025-2026",
                "game_date": f"2026-03-{index + 2:02d}",
                "curated_venue_name": "Reilly Center",
                "city": "Olean",
                "state": "NY",
            }
            for index in range(1, 6)
        )
        source_games_before = [dict(game) for game in source_games]
        summary_match_rows = []

        staged, globals_, _names, outcomes = rebase_venues(
            "test-school",
            [dict(relationship), dict(per_game)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
            source_games=source_games,
            summary_match_rows_out=summary_match_rows,
        )
        self.assertEqual(len(staged), 2)
        self.assertEqual(len(globals_), 1)
        self.assertEqual(staged[0]["venue_id"], "VEN-000926")
        self.assertEqual(
            staged[0]["venue_key"], "reilly-center-st-bonaventure"
        )
        self.assertEqual(staged[0]["city"], "Olean")
        self.assertEqual(staged[1]["city"], "Olean")
        self.assertEqual(staged[0]["games_currently_assigned"], "784")
        self.assertEqual(staged[1]["games_currently_assigned"], "5")
        self.assertEqual(staged[0]["first_assigned_game"], "1967-02-25")
        self.assertEqual(staged[0]["last_assigned_game"], "2026-03-01")
        self.assertEqual(staged[1]["first_assigned_game"], "2026-03-03")
        self.assertEqual(staged[1]["last_assigned_game"], "2026-03-07")
        self.assertEqual(
            sum(int(row["games_currently_assigned"]) for row in staged),
            789,
        )
        self.assertEqual(
            min(row["first_assigned_game"] for row in staged),
            "1967-02-25",
        )
        self.assertEqual(
            max(row["last_assigned_game"] for row in staged),
            "2026-03-07",
        )
        self.assertEqual(source_games, source_games_before)
        self.assertEqual(len(summary_match_rows), 2)
        self.assertEqual(summary_match_rows[0]["city"], "St. Bonaventure")
        self.assertEqual(summary_match_rows[1]["city"], "Olean")

        strict_staged = venue_summary_consistency_report(source_games, staged)
        self.assertEqual(strict_staged["status"], "FAIL")
        self.assertTrue(
            any(
                "games_currently_assigned total 789 != 5 source-game assignments"
                in error
                for error in strict_staged["errors"]
            )
        )
        preserved_match = venue_summary_consistency_report(
            source_games,
            staged,
            source_match_venues=summary_match_rows,
        )
        self.assertEqual(preserved_match["status"], "PASS")
        self.assertEqual(preserved_match["errors"], [])
        self.assertEqual(staged[0]["relationship_type"], "HOME")
        self.assertEqual(staged[0]["relationship_start"], "1966-12-02")
        self.assertEqual(
            staged[0]["site_rule"],
            "HOME relationship chronology with documented exceptions.",
        )
        self.assertEqual(staged[0]["source_basis"], "Accepted facility chronology.")
        self.assertEqual(staged[0]["venue_type"], "ARENA")
        self.assertEqual(
            outcomes[0]["resolution"],
            "REUSE_EXPLICIT_RECONCILIATION_PRESERVE_LOCAL_ROW",
        )

    def test_preserve_local_representation_requires_relationship_authority(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        blank = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        keyed = {
            **dict(blank),
            "venue_key": "shared-arena",
            "venue_id": "VEN-000100",
        }
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000100",
            "venue_key": "shared-arena",
            "display_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "global_venue_id": "VEN-000100",
            "global_venue_key": "shared-arena",
            "expected_global_city": "Example City",
            "expected_global_state": "NY",
            "preserve_local_representation": True,
            "resolution_basis": "Attempted preservation without relationship authority.",
        }]
        self.save()

        with self.assertRaisesRegex(
            WorkflowError,
            "limited to frozen rows carrying venue relationship authority",
        ):
            load_venue_reconciliation(
                self.spec,
                school_key="test-school",
                package_path=self.package,
                local_venues=[blank, keyed],
                global_venues=[global_row],
            )

    def test_preserved_relationship_pair_keeps_summary_refresh_fail_closed(self):
        rows = [
            {
                "venue_key": "shared-arena",
                "canonical_name": "Shared Arena",
                "aliases": "",
                "city": "Example City",
                "state": "NY",
                "relationship_type": "HOME",
                "relationship_start": "1966-12-02",
                "relationship_end": "",
                "relationship_date_precision": "EXACT",
                "games_currently_assigned": "0",
                "first_assigned_game": "",
                "last_assigned_game": "",
            },
            {
                "venue_key": "shared-arena",
                "canonical_name": "Shared Arena",
                "aliases": "",
                "city": "Example City",
                "state": "NY",
                "relationship_type": "",
                "relationship_start": "",
                "relationship_end": "",
                "relationship_date_precision": "",
                "games_currently_assigned": "0",
                "first_assigned_game": "",
                "last_assigned_game": "",
            },
        ]
        games = [{
            "source_game_id": "G1",
            "season_label": "1970-1971",
            "game_date": "1971-01-02",
            "curated_venue_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }]

        with self.assertRaisesRegex(
            WorkflowError, "stale venue summary cannot be refreshed safely"
        ):
            refresh_local_venue_assignment_summaries(rows, games)

    def test_redundant_drop_fails_closed_without_retained_keyed_identity(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        blank = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "DROP_REDUNDANT_LOCAL_ROW",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "resolution_basis": "Attempted unsafe drop.",
        }]
        self.save()

        with self.assertRaisesRegex(
            WorkflowError, "requires a retained keyed row"
        ):
            load_venue_reconciliation(
                self.spec,
                school_key="test-school",
                package_path=self.package,
                local_venues=[blank],
                global_venues=[dict(self.global_row)],
            )

    def test_cutover_split_reconciles_all_matching_source_games(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena-old,Shared Arena,Example City,NY\n"
            b"shared-arena-new,Shared Arena,Example City,NY\n"
        )
        source_bytes = (
            b"source_game_id,season_label,game_date,curated_venue_name,city,state\n"
            b"G1,1960-1961,1961-03-17,Shared Arena,Example City,NY\n"
            b"G2,1966-1967,,Shared Arena,Example City,NY\n"
            b"G3,1968-1969,,Shared Arena,Example City,NY\n"
            b"G4,1976-1977,1977-03-15,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
            z.writestr("source-games.csv", source_bytes)

        common = {
            **dict(self.local),
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "site_rule": "Per-game accepted venue assignment.",
            "source_basis": "Accepted row-level site research.",
            "notes": "Representation metadata only.",
            "games_currently_assigned": "1",
            "first_assigned_game": "",
            "last_assigned_game": "",
        }
        broad = {**common, "venue_key": "", "venue_id": ""}
        old = {
            **common,
            "venue_key": "shared-arena-old",
            "venue_id": "VEN-000100",
        }
        new = {
            **common,
            "venue_key": "shared-arena-new",
            "venue_id": "VEN-000101",
        }
        globals_ = [
            {
                **dict(self.global_row),
                "venue_id": "VEN-000100",
                "venue_key": "shared-arena-old",
                "display_name": "Shared Arena",
                "city": "Example City",
                "state": "NY",
                "identity_status": "RESEARCHED_SPLIT",
            },
            {
                **dict(self.global_row),
                "venue_id": "VEN-000101",
                "venue_key": "shared-arena-new",
                "display_name": "Shared Arena",
                "city": "Example City",
                "state": "NY",
                "identity_status": "RESEARCHED_SPLIT",
            },
        ]
        source_games = list(csv.DictReader(source_bytes.decode().splitlines()))
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "SPLIT_LOCAL_ROW_BY_CUTOVER",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "cutover_date": "1968-02-11",
            "cutover_basis": "Settled physical-building transition authority.",
            "before_global_venue_id": "VEN-000100",
            "before_global_venue_key": "shared-arena-old",
            "after_global_venue_id": "VEN-000101",
            "after_global_venue_key": "shared-arena-new",
            "resolution_basis": "Hash-bound frozen source-game split.",
        }]
        self.save()

        mapping, meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[broad, old, new],
            global_venues=globals_,
        )
        targets = meta["mappings"][0]["split_targets"]
        self.assertEqual(
            [(target["side"], target["games_currently_assigned"]) for target in targets],
            [("BEFORE", "2"), ("AFTER", "2")],
        )
        inventory = venue_reconciliation_inventory(
            [dict(broad), dict(old), dict(new)],
            [dict(row) for row in globals_],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            inventory["rows"][0]["classification"],
            "SAFE_REPRESENTATION_SPLIT",
        )

        staged, _global_rows, _names, outcomes = rebase_venues(
            "test-school",
            [dict(broad), dict(old), dict(new)],
            [dict(row) for row in globals_],
            [],
            venue_reconciliation=mapping,
            source_games=source_games,
        )
        self.assertEqual(len(staged), 2)
        by_key = {row["venue_key"]: row for row in staged}
        self.assertEqual(
            by_key["shared-arena-old"]["games_currently_assigned"], "2"
        )
        self.assertEqual(
            by_key["shared-arena-new"]["games_currently_assigned"], "2"
        )
        self.assertEqual(
            outcomes[0]["resolution"], "SPLIT_LOCAL_ROW_BY_CUTOVER"
        )

    def test_cutover_split_rejects_undated_transition_season(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena-old,Shared Arena,Example City,NY\n"
            b"shared-arena-new,Shared Arena,Example City,NY\n"
        )
        source_bytes = (
            b"source_game_id,season_label,game_date,curated_venue_name,city,state\n"
            b"G1,1967-1968,,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
            z.writestr("source-games.csv", source_bytes)
        common = {
            **dict(self.local),
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        local_rows = [
            {**common, "venue_key": "", "venue_id": ""},
            {**common, "venue_key": "shared-arena-old", "venue_id": "VEN-000100"},
            {**common, "venue_key": "shared-arena-new", "venue_id": "VEN-000101"},
        ]
        globals_ = [
            {**dict(self.global_row), "venue_id": "VEN-000100", "venue_key": "shared-arena-old", "display_name": "Shared Arena", "city": "Example City", "state": "NY"},
            {**dict(self.global_row), "venue_id": "VEN-000101", "venue_key": "shared-arena-new", "display_name": "Shared Arena", "city": "Example City", "state": "NY"},
        ]
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "action": "SPLIT_LOCAL_ROW_BY_CUTOVER",
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "cutover_date": "1968-02-11",
            "cutover_basis": "Settled transition.",
            "before_global_venue_id": "VEN-000100",
            "before_global_venue_key": "shared-arena-old",
            "after_global_venue_id": "VEN-000101",
            "after_global_venue_key": "shared-arena-new",
            "resolution_basis": "Must fail closed without exact transition-season date.",
        }]
        self.save()
        with self.assertRaisesRegex(
            WorkflowError, "transition-season game lacks an exact date"
        ):
            load_venue_reconciliation(
                self.spec,
                school_key="test-school",
                package_path=self.package,
                local_venues=local_rows,
                global_venues=globals_,
            )

    def test_explicit_reuse_consolidates_existing_local_identity_and_refreshes_count(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b"shared-arena,Shared Arena,Example City,NY\n"
        )
        source_bytes = (
            b"source_game_id,season_label,game_date,curated_venue_name,city,state\n"
            b"G1,2020-2021,2021-01-01,Shared Arena,Example City,NY\n"
            b"G2,2020-2021,,Shared Arena,Example City,NY\n"
            b"G3,2021-2022,2022-01-01,Shared Arena,Example City,NY\n"
            b"G4,2021-2022,2022-02-01,Shared Arena,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
            z.writestr("source-games.csv", source_bytes)
        common = {
            **dict(self.local),
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
            "site_rule": "Per-game assignment.",
            "source_basis": "Accepted site research.",
            "notes": "Representation metadata.",
        }
        blank = {
            **common, "venue_key": "", "venue_id": "",
            "games_currently_assigned": "2",
        }
        keyed = {
            **common, "venue_key": "shared-arena", "venue_id": "VEN-000100",
            "games_currently_assigned": "3",
        }
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000100",
            "venue_key": "shared-arena",
            "display_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Example City",
            "expected_local_state": "NY",
            "global_venue_id": "VEN-000100",
            "global_venue_key": "shared-arena",
            "expected_global_city": "Example City",
            "expected_global_state": "NY",
            "resolution_basis": "Same physical identity.",
        }]
        self.save()
        mapping, _meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[blank, keyed],
            global_venues=[global_row],
        )
        inventory = venue_reconciliation_inventory(
            [dict(blank), dict(keyed)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(
            inventory["rows"][0]["classification"],
            "SAFE_REPRESENTATION_CONSOLIDATION",
        )
        staged, _globals, _names, outcomes = rebase_venues(
            "test-school",
            [dict(blank), dict(keyed)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
            source_games=list(csv.DictReader(source_bytes.decode().splitlines())),
        )
        self.assertEqual(len(staged), 1)
        self.assertEqual(staged[0]["games_currently_assigned"], "4")
        self.assertEqual(staged[0]["first_assigned_game"], "")
        self.assertEqual(staged[0]["last_assigned_game"], "")
        self.assertEqual(outcomes[0]["resolution"], "CONSOLIDATE_EXPLICIT_REUSE")

    def test_blank_key_new_identity_requires_explicit_registration(self):
        local = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "New Armory",
            "city": "Olean",
            "state": "NY",
        }
        inventory = venue_reconciliation_inventory(
            [local], [], [], venue_reconciliation={}
        )
        self.assertEqual(inventory["blocker_count"], 1)
        self.assertIn(
            "BLANK_KEY_NEW_IDENTITY_REQUIRES_EXPLICIT_REGISTRATION",
            inventory["rows"][0]["issues"],
        )

    def test_explicit_new_identity_preserves_two_relationship_rows_and_refreshes_counts(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",New Armory,Olean,NY\n"
            b",New Armory,Olean,NY\n"
        )
        source_bytes = (
            b"source_game_id,season_label,game_date,curated_venue_name,city,state\n"
            b"G1,1915-1916,,New Armory,Olean,NY\n"
            b"G2,1948-1949,1948-12-18,New Armory,Olean,NY\n"
            b"G3,1950-1951,,New Armory,Olean,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
            z.writestr("source-games.csv", source_bytes)
        common = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "New Armory",
            "city": "Olean",
            "state": "NY",
            "venue_type": "armory",
            "site_rule": "HOME only after independent classification.",
            "source_basis": "Accepted HOME chronology.",
            "notes": "One physical building with separate relationship eras.",
        }
        early = {
            **common,
            "games_currently_assigned": "1",
            "relationship_type": "source_program_home_exception",
            "relationship_start": "1915-1916",
            "relationship_end": "1915-1916",
            "relationship_date_precision": "season",
        }
        later = {
            **common,
            "games_currently_assigned": "1",
            "relationship_type": "source_program_home",
            "relationship_start": "1946",
            "relationship_end": "1966-01-19",
            "relationship_date_precision": "date",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [
            {
                "action": "REGISTER_NEW_IDENTITY",
                "local_venue_row_index": 1,
                "expected_local_name": "New Armory",
                "expected_local_city": "Olean",
                "expected_local_state": "NY",
                "new_global_venue_key": "new-armory",
                "resolution_basis": "One settled physical building.",
            },
            {
                "action": "REGISTER_NEW_IDENTITY",
                "local_venue_row_index": 2,
                "expected_local_name": "New Armory",
                "expected_local_city": "Olean",
                "expected_local_state": "NY",
                "new_global_venue_key": "new-armory",
                "resolution_basis": "Same settled physical building.",
            },
        ]
        self.save()
        mapping, _meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[early, later],
            global_venues=[],
        )
        inventory = venue_reconciliation_inventory(
            [dict(early), dict(later)],
            [],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        staged, global_rows, _names, _outcomes = rebase_venues(
            "test-school",
            [dict(early), dict(later)],
            [],
            [],
            venue_reconciliation=mapping,
            source_games=list(csv.DictReader(source_bytes.decode().splitlines())),
        )
        self.assertEqual(len(global_rows), 1)
        self.assertEqual({row["venue_key"] for row in staged}, {"new-armory"})
        self.assertEqual(len({row["venue_id"] for row in staged}), 1)
        self.assertEqual(
            [row["games_currently_assigned"] for row in staged],
            ["1", "2"],
        )

    def test_two_row_index_mappings_may_reuse_one_authenticated_target(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Shared Arena,Example City,NY\n"
            b",Shared Arena Former Name,Example City,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        first = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        second = {
            **dict(first),
            "canonical_name": "Shared Arena Former Name",
        }
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000100",
            "venue_key": "shared-arena",
            "display_name": "Shared Arena",
            "city": "Example City",
            "state": "NY",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [
            {
                "local_venue_row_index": 1,
                "expected_local_name": "Shared Arena",
                "expected_local_city": "Example City",
                "expected_local_state": "NY",
                "global_venue_id": "VEN-000100",
                "global_venue_key": "shared-arena",
                "expected_global_city": "Example City",
                "expected_global_state": "NY",
                "resolution_basis": "First immutable representation.",
            },
            {
                "local_venue_row_index": 2,
                "expected_local_name": "Shared Arena Former Name",
                "expected_local_city": "Example City",
                "expected_local_state": "NY",
                "global_venue_id": "VEN-000100",
                "global_venue_key": "shared-arena",
                "expected_global_city": "Example City",
                "expected_global_state": "NY",
                "resolution_basis": "Second immutable representation of the same venue.",
            },
        ]
        self.save()

        mapping, _meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[first, second],
            global_venues=[global_row],
        )
        inventory = venue_reconciliation_inventory(
            [dict(first), dict(second)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            [row["target_venue_id"] for row in inventory["rows"]],
            ["VEN-000100", "VEN-000100"],
        )
        staged, globals_, _names, _outcomes = rebase_venues(
            "test-school",
            [dict(first), dict(second)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(len(globals_), 1)
        self.assertEqual(len(staged), 2)
        self.assertEqual({row["venue_id"] for row in staged}, {"VEN-000100"})
        self.assertEqual({row["venue_key"] for row in staged}, {"shared-arena"})

    def test_explicit_same_state_locality_variant_can_consolidate(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",Reilly Center,Saint Bonaventure,NY\n"
            b"reilly-center,Reilly Center,Olean,NY\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        common = {
            **dict(self.local),
            "canonical_name": "Reilly Center",
            "aliases": "",
            "venue_type": "",
            "site_rule": "",
            "source_basis": "",
            "notes": "",
            "known_opened": "",
            "known_closed": "",
            "venue_date_precision": "",
        }
        blank = {
            **common,
            "venue_key": "",
            "venue_id": "",
            "city": "Saint Bonaventure",
            "state": "NY",
        }
        keyed = {
            **common,
            "venue_key": "reilly-center",
            "venue_id": "VEN-000926",
            "city": "Olean",
            "state": "NY",
        }
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000926",
            "venue_key": "reilly-center",
            "display_name": "Reilly Center",
            "city": "Olean",
            "state": "NY",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "Reilly Center",
            "expected_local_city": "Saint Bonaventure",
            "expected_local_state": "NY",
            "global_venue_id": "VEN-000926",
            "global_venue_key": "reilly-center",
            "expected_global_city": "Olean",
            "expected_global_state": "NY",
            "allow_locality_variant": True,
            "locality_variant_basis": "Exact physical identity; school-local locality label differs from registry locality.",
            "resolution_basis": "Hash-bound representation-only canonicalization.",
        }]
        self.save()

        mapping, meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[blank, keyed],
            global_venues=[global_row],
        )
        self.assertTrue(meta["mappings"][0]["allow_locality_variant"])
        inventory = venue_reconciliation_inventory(
            [dict(blank), dict(keyed)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertEqual(
            inventory["rows"][0]["classification"],
            "SAFE_REPRESENTATION_CONSOLIDATION",
        )
        staged, _globals, _names, outcomes = rebase_venues(
            "test-school",
            [dict(blank), dict(keyed)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(len(staged), 1)
        self.assertEqual(staged[0]["city"], "Olean")
        self.assertEqual(staged[0]["state"], "NY")
        self.assertEqual(outcomes[0]["resolution"], "CONSOLIDATE_EXPLICIT_REUSE")

    def test_explicit_same_city_jurisdiction_variant_canonicalizes(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b",John Gray Gymnasium,George Town,Grand Cayman\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        local = {
            **dict(self.local),
            "venue_key": "",
            "venue_id": "",
            "canonical_name": "John Gray Gymnasium",
            "city": "George Town",
            "state": "Grand Cayman",
        }
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000470",
            "venue_key": "provisional-john-gray-gym",
            "display_name": "John Gray Gym",
            "city": "George Town",
            "state": "Cayman Islands",
        }
        self.doc["schema_version"] = 2
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"] = [{
            "local_venue_row_index": 1,
            "expected_local_name": "John Gray Gymnasium",
            "expected_local_city": "George Town",
            "expected_local_state": "Grand Cayman",
            "global_venue_id": "VEN-000470",
            "global_venue_key": "provisional-john-gray-gym",
            "expected_global_city": "George Town",
            "expected_global_state": "Cayman Islands",
            "allow_locality_variant": True,
            "locality_variant_basis": "Same exact venue and city; local region label differs from registry jurisdiction.",
            "resolution_basis": "Registered alias identifies the exact physical venue.",
        }]
        self.save()

        mapping, _meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=[local],
            global_venues=[global_row],
        )
        inventory = venue_reconciliation_inventory(
            [dict(local)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(inventory["blocker_count"], 0)
        self.assertIn(
            "CANONICAL_GEOGRAPHY_NORMALIZATION",
            inventory["rows"][0]["issues"],
        )
        staged, _globals, _names, _outcomes = rebase_venues(
            "test-school",
            [dict(local)],
            [dict(global_row)],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(staged[0]["city"], "George Town")
        self.assertEqual(staged[0]["state"], "Cayman Islands")

    def test_repeated_frozen_physical_key_with_historical_names_is_supported(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b"spectrum-center-charlotte,Spectrum Center,Charlotte,NC\n"
            b"spectrum-center-charlotte,Time Warner Cable Arena (now Spectrum Center),Charlotte,NC\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        local_rows = [
            {
                **dict(self.local),
                "venue_key": "spectrum-center-charlotte",
                "canonical_name": "Spectrum Center",
                "city": "Charlotte",
                "state": "NC",
            },
            {
                **dict(self.local),
                "venue_key": "spectrum-center-charlotte",
                "canonical_name": "Time Warner Cable Arena (now Spectrum Center)",
                "city": "Charlotte",
                "state": "NC",
            },
        ]
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000190",
            "venue_key": "spectrum-center",
            "display_name": "Spectrum Center",
            "city": "Charlotte",
            "state": "NC",
        }
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"][0].update({
            "local_venue_key": "spectrum-center-charlotte",
            "expected_local_name": "Spectrum Center",
            "expected_local_city": "Charlotte",
            "expected_local_state": "NC",
            "global_venue_id": "VEN-000190",
            "global_venue_key": "spectrum-center",
            "expected_global_city": "Charlotte",
            "expected_global_state": "NC",
            "resolution_basis": "Same physical arena across historical naming rows.",
        })
        self.save()

        mapping, _meta = load_venue_reconciliation(
            self.spec,
            school_key="test-school",
            package_path=self.package,
            local_venues=local_rows,
            global_venues=[global_row],
        )
        result = venue_reconciliation_inventory(
            local_rows,
            [global_row],
            [],
            venue_reconciliation=mapping,
        )
        self.assertEqual(result["blocker_count"], 0)
        self.assertEqual(
            [row["target_venue_id"] for row in result["rows"]],
            ["VEN-000190", "VEN-000190"],
        )

    def test_repeated_frozen_key_still_rejects_conflicting_geography(self):
        venues_bytes = (
            b"venue_key,canonical_name,city,state\n"
            b"shared-arena,Shared Arena,Charlotte,NC\n"
            b"shared-arena,Shared Arena,Raleigh,NC\n"
        )
        with zipfile.ZipFile(self.package, "w") as z:
            z.writestr("venues.csv", venues_bytes)
        local_rows = [
            {**dict(self.local), "venue_key": "shared-arena",
             "canonical_name": "Shared Arena", "city": "Charlotte", "state": "NC"},
            {**dict(self.local), "venue_key": "shared-arena",
             "canonical_name": "Shared Arena", "city": "Raleigh", "state": "NC"},
        ]
        global_row = {
            **dict(self.global_row),
            "venue_id": "VEN-000190",
            "venue_key": "shared-arena-current",
            "display_name": "Shared Arena",
            "city": "Charlotte",
            "state": "NC",
        }
        self.doc["expected_research_zip_sha256"] = sha(self.package.read_bytes())
        self.doc["expected_venues_sha256"] = sha(venues_bytes)
        self.doc["mappings"][0].update({
            "local_venue_key": "shared-arena",
            "expected_local_name": "Shared Arena",
            "expected_local_city": "Charlotte",
            "expected_local_state": "NC",
            "global_venue_id": "VEN-000190",
            "global_venue_key": "shared-arena-current",
            "expected_global_city": "Charlotte",
            "expected_global_state": "NC",
        })
        self.save()

        with self.assertRaisesRegex(WorkflowError, "frozen local identity drift"):
            load_venue_reconciliation(
                self.spec,
                school_key="test-school",
                package_path=self.package,
                local_venues=local_rows,
                global_venues=[global_row],
            )


class DaytonHistoricalNameBoundTests(unittest.TestCase):
    """Current verified predecessor name must not attach a 1986 opponent to Dayton."""

    def setUp(self):
        path = ROOT / "data/reference/program-names.csv"
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        matches = [r for r in rows
                   if r["program_key"] == "dayton"
                   and r["alias_name"] == "St. Mary's College"]
        self.assertEqual(len(matches), 1)
        self.alias = matches[0]
        self.programs = [{"program_key": "dayton", "program_name": "Dayton",
                          "display_name": "Dayton", "current_d1": "Yes"}]

    def opponent(self, season):
        return {
            "source_program_key": "test-school",
            "source_opponent_label": "St. Mary’s College",
            "canonical_opponent_key": "st-marys-college",
            "canonical_opponent_name": "St. Mary’s College",
            "current_d1": "FALSE",
            "games_with_source_label": "1",
            "first_season": season, "last_season": season,
        }

    def game(self, season):
        return {
            "source_game_id": "FDU-S1-000488" if season == "1986-1987" else "fixture-early",
            "source_program_key": "test-school", "season_label": season,
            "source_opponent_label": "St. Mary’s College",
            "normalized_opponent_key": "st-marys-college",
            "normalized_opponent_name": "St. Mary’s College",
            "raw_text": "W 86-54 St. Mary’s College",
            "opponent_current_d1": "FALSE",
        }

    def test_dayton_alias_is_bounded_at_1919_1920(self):
        self.assertEqual(self.alias["effective_end_season"], "1919-1920")
        self.assertEqual(self.alias["verification_status"], "VERIFIED")

    def test_early_dayton_usage_remains_eligible(self):
        opponents, games, mappings = rebase_program_aliases(
            self.programs, [self.alias], [self.opponent("1915-1916")],
            [self.game("1915-1916")],
        )
        self.assertEqual(opponents[0]["canonical_opponent_key"], "dayton")
        self.assertEqual(games[0]["normalized_opponent_key"], "dayton")
        self.assertEqual(len(mappings), 1)

    def test_1986_fdu_opponent_remains_non_d1_literal_identity(self):
        opponent = self.opponent("1986-1987")
        game = self.game("1986-1987")
        inventory = program_alias_inventory(self.programs, [self.alias], [opponent])
        self.assertEqual(inventory["classification_counts"], {"NO_CURRENT_VERIFIED_ALIAS": 1})
        opponents, games, mappings = rebase_program_aliases(
            self.programs, [self.alias], [opponent], [game],
        )
        self.assertEqual(opponents[0]["canonical_opponent_key"], "st-marys-college")
        self.assertEqual(opponents[0]["current_d1"], "FALSE")
        self.assertEqual(games[0]["normalized_opponent_key"], "st-marys-college")
        self.assertEqual(games[0]["opponent_current_d1"], "FALSE")
        self.assertEqual(games[0]["raw_text"], "W 86-54 St. Mary’s College")
        self.assertEqual(mappings, [])


if __name__ == "__main__":
    unittest.main()
