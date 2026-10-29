import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from remote_implementation_control import (  # noqa: E402
    LIFECYCLE_ACTIVE,
    OP_PHASE0_SCOPE_SUPERSESSION,
    RemoteImplementationError,
    begin_request,
    initial_control_state,
    validate_request,
)
from remote_implementation_scope_supersession import (  # noqa: E402
    build_scope_superseded_package,
    deterministic_package_zip_bytes,
)


HASH = "f" * 64
MAIN = "a" * 40
TARGET = "b" * 40
PRED = "c" * 40


def csv_text(header, rows):
    return (header + "\n" + "\n".join(rows) + "\n").encode()


def source_row(
    source_game_id,
    season,
    label,
    key,
    name,
    *,
    venue="",
    site="OPPONENT_HOME",
):
    values = [
        source_game_id,
        "example-school",
        "",
        season,
        "",
        label,
        key,
        name,
        "70",
        "60",
        "W",
        "",
        "",
        site,
        "",
        venue,
        "",
        "",
        "",
        "",
        "",
        "REGULAR_SEASON",
        "",
        "1",
        f"{label} W 70-60",
        "PENDING_STAGE_2",
        "",
        "",
        "",
        "",
        "",
    ]
    return ",".join(values)


SOURCE_HEADER = (
    "source_game_id,source_program_key,source_era,season_label,game_date,"
    "source_opponent_label,normalized_opponent_key,normalized_opponent_name,"
    "team_score,opponent_score,played_result,overtime_periods,"
    "source_site_candidate,curated_site_type,source_venue_name,"
    "curated_venue_name,city,state,country,event_or_tournament,source_round,"
    "curated_game_type,curated_postseason_round,source_page,raw_text,"
    "normalization_status,administrative_status,administrative_note,notes,"
    "site_research_status,site_research_basis"
)


def package_members():
    source = csv_text(
        SOURCE_HEADER,
        [
            source_row(
                "G-OLD",
                "1955-1956",
                "Old Only",
                "old-only",
                "Old Only",
                venue="Old Gym",
                site="SOURCE_PROGRAM_HOME",
            ),
            source_row(
                "G-SHARED-OLD",
                "1955-1956",
                "Shared",
                "shared",
                "Shared",
                venue="Old Gym",
                site="SOURCE_PROGRAM_HOME",
            ),
            source_row(
                "G-SHARED-NEW",
                "1970-1971",
                "Shared",
                "shared",
                "Shared",
                venue="Registered Arena",
                site="SOURCE_PROGRAM_HOME",
            ),
            source_row(
                "G-NEW",
                "1971-1972",
                "New Only",
                "new-only",
                "New Only",
                venue="New Arena",
                site="SOURCE_PROGRAM_HOME",
            ),
        ],
    )
    opponents = csv_text(
        "index,source_program_key,source_opponent_label,canonical_opponent_key,"
        "canonical_opponent_name,current_d1,games_with_source_label,first_season,"
        "last_season,resolution_status,resolution_method,user_choice,audit_note",
        [
            "1,example-school,Old Only,old-only,Old Only,No,1,1955-56,1955-56,RESOLVED,SOURCE,,old",
            "2,example-school,Shared,shared,Shared,Yes,2,1955-56,1970-71,RESOLVED,CURRENT,,shared",
            "3,example-school,New Only,new-only,New Only,No,1,1971-72,1971-72,RESOLVED,SOURCE,,new",
        ],
    )
    conferences = csv_text(
        "source_program_key,start_season,end_season,conference_key,conference_name,"
        "membership_type,ongoing,basis,notes",
        [
            "example-school,1955-1956,1955-1956,ccaa,CCAA,conference,False,old,old",
            "example-school,1970-1971,1971-1972,big-west,PCAA,conference,False,new,new",
        ],
    )
    venues = csv_text(
        "index,source_program_key,venue_key,venue_id,canonical_name,aliases,city,"
        "state,venue_type,known_opened,known_closed,venue_date_precision,"
        "games_currently_assigned,first_assigned_game,last_assigned_game,"
        "relationship_type,relationship_start,relationship_end,"
        "relationship_date_precision,site_rule,source_basis,notes",
        [
            "1,example-school,old-gym,VEN-999991,Old Gym,,Oldtown,CA,gymnasium,,,,2,,,primary_home,,,,,basis,Integration rebase resolved final global venue ID VEN-999991.",
            "2,example-school,registered-arena,VEN-999992,Registered Arena,,City,CA,arena,,,,1,,,primary_home,,,,,basis,old id",
            "3,example-school,new-arena,VEN-999993,New Arena,,City,CA,arena,,,,1,,,primary_home,,,,,basis,Integration rebase resolved final global venue ID VEN-999993.",
        ],
    )
    notes = (
        "# example-school research package notes\n\n"
        "- Competitive games: 4\n"
        "- Primary-source historical results cutoff: 1955-1956\n"
        "## Final game census\n"
        "- REGULAR_SEASON: 4\n"
        "## Final H/A/N census\n"
        "- SOURCE_PROGRAM_HOME: 4\n"
        "- OPPONENT_HOME: 0\n"
        "- NEUTRAL: 0\n"
    ).encode()
    source_notes = (
        "# example-school source notes\n\n"
        "- Primary-source historical results cutoff: 1955-1956\n"
    ).encode()
    return {
        "conferences.csv": conferences,
        "notes.md": notes,
        "opponents.csv": opponents,
        "source-games.csv": source,
        "source-notes.md": source_notes,
        "venues.csv": venues,
    }


def scope_spec(excluded=None, drops=None):
    return {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_SCOPE_SUPERSESSION",
        "school_key": "example-school",
        "old_scope": "1955-56..1955-56|1970-71+",
        "new_scope": "1970-71+",
        "history_start_season": "1970-1971",
        "authority_statement": "Owner and Control Center superseded public scope.",
        "excluded_source_game_ids": excluded or ["G-OLD", "G-SHARED-OLD"],
        "expected_source_game_count_before": 4,
        "expected_source_game_count_after": 2,
        "drop_school_venue_keys": drops or ["old-gym"],
    }


def request():
    return {
        "schema_version": 1,
        "kind": "REMOTE_IMPLEMENTATION_REQUEST",
        "request_id": "example-scope-supersession-0001",
        "school_key": "example-school",
        "operation": OP_PHASE0_SCOPE_SUPERSESSION,
        "previous_control_state_commit": PRED,
        "previous_control_state_sha256": HASH,
        "expected_protected_main_sha": MAIN,
        "target_branch": "data/example-school-onboarding",
        "target_sha": TARGET,
        "research_checkpoint": {
            "sha256": "1" * 64,
            "research_base_sha": "2" * 40,
            "transport": {
                "kind": "git_base64_parts",
                "commit_sha": "3" * 40,
                "path_prefix": "checkpoints/example.zip.part",
                "part_count": 2,
            },
        },
        "venue_reconciliation": None,
        "conference_reconciliation": None,
        "scope_supersession_spec": {
            "path": ".remote-implementation/inputs/example/scope.json",
            "sha256": "4" * 64,
        },
        "superseded_phase0_successor": {
            "path": ".remote-implementation/successors/example/phase0/successor-manifest.json",
            "sha256": "5" * 64,
        },
        "superseded_successor": {
            "path": ".remote-implementation/successors/example/current/successor-manifest.json",
            "sha256": "6" * 64,
        },
        "superseded_successor_verification": {
            "path": ".remote-implementation/verifications/example/current/verification.json",
            "sha256": "9" * 64,
        },
        "superseded_integration_freeze_sha256": "7" * 64,
        "superseded_semantic_snapshot_sha256": "8" * 64,
        "history_scope": {
            "start_season": "1970-1971",
            "basis": "TOP_LEVEL_INTERVALS",
            "intervals": "1970-71+",
            "notes": "Owner-confirmed superseded scope.",
        },
        "scope_supersession_authorization": {
            "approved": True,
            "authority_kind": "CONTROL_CENTER_EXPLICIT",
            "authorization_basis": "Bounded pre-publication scope reset.",
            "spec_sha256": "4" * 64,
        },
        "creation_provenance": {
            "origin": "test",
            "authorization": "owner and Control Center",
        },
        "authority": {
            "owner_gate_1": False,
            "owner_gate_2": False,
            "release": False,
            "phase0": False,
            "phase0_scope_supersession": True,
            "recovery": False,
            "stage2_census": False,
            "stage2_opponent_display_normalize": False,
            "stage2_proposal_rehearsal": False,
            "stage2_gate1_fill": False,
            "stage2_preseal_rehearsal": False,
            "stage2_gate1_seal": False,
            "stage2_sealed_apply": False,
            "stage2_reconciliation_diagnostic": False,
            "release_readiness": False,
            "release_preview_verify": False,
            "release_gate2_approval": False,
            "release_production_proof": False,
            "venue_identity_maintenance": False,
        },
    }


class ScopeSupersessionTransformTests(unittest.TestCase):
    def current_main_venues(self):
        return csv_text(
            "venue_id,venue_key,display_name,city,state,opened,closed,"
            "date_precision,identity_status,source_basis,notes",
            [
                "VEN-000100,registered-arena,Registered Arena,City,CA,,,,VERIFIED,basis,",
            ],
        )

    def test_build_clips_scope_and_regenerates_supporting_rows(self):
        members, proof = build_scope_superseded_package(
            package_members(),
            self.current_main_venues(),
            scope_spec(),
            school_key="example-school",
        )
        text = members["source-games.csv"].decode()
        self.assertNotIn("G-OLD", text)
        self.assertNotIn("G-SHARED-OLD", text)
        self.assertIn("G-SHARED-NEW", text)
        self.assertIn("G-NEW", text)
        self.assertEqual(proof["source_game_count_before"], 4)
        self.assertEqual(proof["source_game_count_after"], 2)
        self.assertEqual(proof["excluded_source_game_count"], 2)
        self.assertEqual(proof["retained_semantic_equivalence"], "PASS")

        opponents = members["opponents.csv"].decode()
        self.assertNotIn("Old Only", opponents)
        self.assertIn("Shared,shared,Shared,Yes,1,1970-71,1970-71", opponents)
        self.assertEqual(proof["opponents"]["removed_rows"], 1)
        self.assertEqual(proof["opponents"]["recounted_rows"], 1)

        conferences = members["conferences.csv"].decode()
        self.assertNotIn("ccaa", conferences)
        self.assertIn("big-west", conferences)
        self.assertEqual(proof["conferences"]["removed_rows"], 1)

        venues = members["venues.csv"].decode()
        self.assertNotIn("old-gym", venues)
        self.assertIn("registered-arena,VEN-000100", venues)
        self.assertIn("new-arena,,New Arena", venues)
        self.assertEqual(proof["venues"]["dropped_keys"], ["old-gym"])
        self.assertEqual(
            proof["venues"]["cleared_unregistered_ids"], ["new-arena"]
        )

    def test_rejects_incomplete_excluded_id_authority(self):
        spec = scope_spec(excluded=["G-OLD", "G-NEW"])
        with self.assertRaisesRegex(Exception, "EXCLUDED_ID_SET_MISMATCH"):
            build_scope_superseded_package(
                package_members(),
                self.current_main_venues(),
                spec,
                school_key="example-school",
            )

    def test_refuses_to_drop_venue_still_used_in_retained_scope(self):
        spec = scope_spec(drops=["registered-arena"])
        with self.assertRaisesRegex(Exception, "DROP_VENUE_STILL_USED"):
            build_scope_superseded_package(
                package_members(),
                self.current_main_venues(),
                spec,
                school_key="example-school",
            )

    def test_deterministic_candidate_zip(self):
        members, _ = build_scope_superseded_package(
            package_members(),
            self.current_main_venues(),
            scope_spec(),
            school_key="example-school",
        )
        self.assertEqual(
            deterministic_package_zip_bytes(members),
            deterministic_package_zip_bytes(members),
        )


class ScopeSupersessionControlTests(unittest.TestCase):
    def test_valid_request_requires_global_mutation_lock(self):
        req = request()
        validate_request(req)
        active = begin_request(
            initial_control_state(),
            req,
            HASH,
            run_id="123",
            run_attempt="1",
            request_commit=PRED,
        )
        self.assertEqual(active["lifecycle_state"], LIFECYCLE_ACTIVE)
        self.assertEqual(active["transaction_state"], "LOCKED")
        self.assertEqual(
            active["active_target_branch"], "data/example-school-onboarding"
        )

    def test_control_center_authorization_is_required(self):
        req = request()
        req["scope_supersession_authorization"]["approved"] = False
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "SCOPE_SUPERSESSION_CONTROL_CENTER_APPROVAL_REQUIRED",
        ):
            validate_request(req)

    def test_other_operation_cannot_claim_scope_supersession_authority(self):
        req = request()
        req["operation"] = "STAGE1_INVENTORY"
        with self.assertRaisesRegex(
            RemoteImplementationError,
            "REQUEST_SCOPE_SUPERSESSION_AUTHORITY_FORBIDDEN",
        ):
            validate_request(req)


if __name__ == "__main__":
    unittest.main()
