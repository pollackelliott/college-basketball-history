import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from remote_implementation_two_lane_contract import (  # noqa: E402
    BARRIER_MAIN_ADVANCED,
    CLASS_LANE_MUTATION,
    CLASS_LANE_READ_ONLY,
    CLASS_PUBLICATION,
    CLASS_SHARED_MUTATION,
    LANE_A,
    LANE_B,
    OP_EXPANSION_PHASE0,
    OP_PHASE0,
    OP_RECOVER,
    OP_RELEASE_PREVIEW_VERIFY,
    OP_RELEASE_PRODUCTION_PROOF,
    OP_STAGE2_CENSUS,
    OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
    OP_STAGE2_SEALED_APPLY,
    PUBLICATION_MERGED,
    SLOT_FREE,
    TwoLaneContractError,
    acquire_publication_slot,
    acquire_shared_mutation_slot,
    activate_lane_b,
    build_migration_manifest,
    claim_lane,
    initial_arbiter_state,
    initial_lane_state,
    mark_publication_merged,
    may_begin_operation,
    operation_class,
    rebind_lane_main,
    release_publication_slot_after_production,
    release_shared_mutation_slot,
    validate_arbiter_state,
    validate_lane_state,
    validate_migration_manifest,
)

MAIN = "a" * 40
LEGACY = "b" * 40
HASH = "c" * 64
PR_HEAD = "d" * 40
MERGE = "e" * 40


class TwoLaneContractTests(unittest.TestCase):
    def setup_shadow(self):
        migration = build_migration_manifest(
            legacy_control_commit=LEGACY,
            legacy_control_state_sha256=HASH,
            protected_main_sha=MAIN,
        )
        arbiter = initial_arbiter_state(
            protected_main_sha=MAIN,
            migration_manifest=migration,
        )
        lane_a = initial_lane_state(
            LANE_A,
            protected_main_sha=MAIN,
            enabled=True,
        )
        lane_b = initial_lane_state(
            LANE_B,
            protected_main_sha=MAIN,
            enabled=False,
        )
        return migration, arbiter, lane_a, lane_b

    def setup_two_active(self):
        migration, arbiter, lane_a, lane_b = self.setup_shadow()
        arbiter, lane_a = claim_lane(
            arbiter,
            lane_a,
            school_key="nevada",
            implementation_kind="ORDINARY",
        )
        arbiter = activate_lane_b(
            arbiter,
            compatibility_pilot_passed=True,
            adversarial_suite_passed=True,
            owner_authorized=True,
        )
        lane_b = initial_lane_state(
            LANE_B,
            protected_main_sha=MAIN,
            enabled=True,
        )
        arbiter, lane_b = claim_lane(
            arbiter,
            lane_b,
            school_key="grand-canyon",
            implementation_kind="ORDINARY",
        )
        return migration, arbiter, lane_a, lane_b

    def test_migration_is_shadow_only_and_binds_legacy_bytes(self):
        migration, _, _, _ = self.setup_shadow()
        validate_migration_manifest(migration)
        self.assertEqual(
            migration["status"],
            "SHADOW_ONLY_NOT_ACTIVATED",
        )
        self.assertFalse(migration["lane_b_activation_authority"])
        self.assertFalse(migration["live_runner_integration"])
        self.assertEqual(migration["legacy_control_commit"], LEGACY)
        self.assertEqual(
            migration["legacy_control_state_sha256"],
            HASH,
        )

    def test_initial_shadow_capacity_disables_lane_b(self):
        _, arbiter, lane_a, lane_b = self.setup_shadow()
        validate_arbiter_state(arbiter)
        validate_lane_state(lane_a)
        validate_lane_state(lane_b)
        self.assertEqual(arbiter["max_active_lanes"], 1)
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "LANE_B_DISABLED",
        ):
            claim_lane(
                arbiter,
                initial_lane_state(
                    LANE_B,
                    protected_main_sha=MAIN,
                    enabled=True,
                ),
                school_key="grand-canyon",
                implementation_kind="ORDINARY",
            )

    def test_lane_b_activation_requires_all_three_proofs(self):
        _, arbiter, _, _ = self.setup_shadow()
        cases = [
            (
                False,
                True,
                True,
                "COMPATIBILITY_PILOT_REQUIRED",
            ),
            (
                True,
                False,
                True,
                "ADVERSARIAL_SUITE_REQUIRED",
            ),
            (
                True,
                True,
                False,
                "OWNER_AUTHORIZATION_REQUIRED",
            ),
        ]
        for pilot, suite, owner, code in cases:
            with self.subTest(code=code):
                with self.assertRaisesRegex(
                    TwoLaneContractError,
                    code,
                ):
                    activate_lane_b(
                        arbiter,
                        compatibility_pilot_passed=pilot,
                        adversarial_suite_passed=suite,
                        owner_authorized=owner,
                    )

    def test_same_school_cannot_occupy_two_lanes(self):
        _, arbiter, lane_a, _ = self.setup_shadow()
        arbiter, lane_a = claim_lane(
            arbiter,
            lane_a,
            school_key="nevada",
            implementation_kind="ORDINARY",
        )
        arbiter = activate_lane_b(
            arbiter,
            compatibility_pilot_passed=True,
            adversarial_suite_passed=True,
            owner_authorized=True,
        )
        lane_b = initial_lane_state(
            LANE_B,
            protected_main_sha=MAIN,
            enabled=True,
        )
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "DUPLICATE_SCHOOL",
        ):
            claim_lane(
                arbiter,
                lane_b,
                school_key="nevada",
                implementation_kind="ORDINARY",
            )

    def test_operation_classes_are_explicit_and_recovery_inherits(self):
        self.assertEqual(
            operation_class(OP_STAGE2_CENSUS),
            CLASS_LANE_READ_ONLY,
        )
        self.assertEqual(
            operation_class(OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE),
            CLASS_LANE_MUTATION,
        )
        self.assertEqual(
            operation_class(OP_PHASE0),
            CLASS_SHARED_MUTATION,
        )
        self.assertEqual(
            operation_class(OP_RELEASE_PRODUCTION_PROOF),
            CLASS_PUBLICATION,
        )
        self.assertEqual(
            operation_class(
                OP_RECOVER,
                recovered_operation=OP_EXPANSION_PHASE0,
            ),
            CLASS_SHARED_MUTATION,
        )
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "RECOVERY_OPERATION_REQUIRED",
        ):
            operation_class(OP_RECOVER)

    def test_two_lanes_can_begin_read_only_work_concurrently(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        self.assertTrue(
            may_begin_operation(
                arbiter,
                lane_a,
                OP_STAGE2_CENSUS,
            )
        )
        self.assertTrue(
            may_begin_operation(
                arbiter,
                lane_b,
                OP_RELEASE_PREVIEW_VERIFY,
            )
        )

    def test_lane_local_mutation_does_not_take_shared_slot(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        arbiter = acquire_shared_mutation_slot(
            arbiter,
            lane_a,
            request_id="nevada-phase0-0001",
            operation=OP_PHASE0,
        )
        self.assertTrue(
            may_begin_operation(
                arbiter,
                lane_b,
                OP_STAGE2_OPPONENT_DISPLAY_NORMALIZE,
            )
        )

    def test_shared_mutation_slot_has_exact_single_owner(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        arbiter = acquire_shared_mutation_slot(
            arbiter,
            lane_a,
            request_id="nevada-phase0-0001",
            operation=OP_PHASE0,
        )
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "SHARED_SLOT_BEGIN_FORBIDDEN",
        ):
            acquire_shared_mutation_slot(
                arbiter,
                lane_b,
                request_id="grand-canyon-apply-0001",
                operation=OP_STAGE2_SEALED_APPLY,
            )
        arbiter = release_shared_mutation_slot(
            arbiter,
            lane_id=LANE_A,
            request_id="nevada-phase0-0001",
            disposition="COMPLETE",
        )
        self.assertEqual(
            arbiter["shared_mutation_slot"]["state"],
            SLOT_FREE,
        )

    def test_publication_cannot_start_while_shared_mutation_is_held(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        arbiter = acquire_shared_mutation_slot(
            arbiter,
            lane_a,
            request_id="nevada-phase0-0001",
            operation=OP_PHASE0,
        )
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "SHARED_MUTATION_BUSY",
        ):
            acquire_publication_slot(
                arbiter,
                lane_b,
                pr_number=700,
                pr_head_sha=PR_HEAD,
            )

    def test_publication_barrier_blocks_new_other_lane_work(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        arbiter = acquire_publication_slot(
            arbiter,
            lane_a,
            pr_number=700,
            pr_head_sha=PR_HEAD,
        )
        self.assertFalse(
            may_begin_operation(
                arbiter,
                lane_b,
                OP_STAGE2_CENSUS,
            )
        )
        self.assertTrue(
            may_begin_operation(
                arbiter,
                lane_a,
                OP_STAGE2_CENSUS,
            )
        )

    def test_merge_advances_main_and_other_lane_stays_stale(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        arbiter = acquire_publication_slot(
            arbiter,
            lane_a,
            pr_number=700,
            pr_head_sha=PR_HEAD,
        )
        arbiter = mark_publication_merged(
            arbiter,
            lane_id=LANE_A,
            merge_sha=MERGE,
        )
        self.assertEqual(
            arbiter["publication_slot"]["state"],
            PUBLICATION_MERGED,
        )
        self.assertEqual(
            arbiter["main_advance_barrier"]["state"],
            BARRIER_MAIN_ADVANCED,
        )
        self.assertEqual(
            arbiter["protected_main_sha"],
            MERGE,
        )
        self.assertFalse(
            may_begin_operation(
                arbiter,
                lane_b,
                OP_STAGE2_CENSUS,
            )
        )
        self.assertTrue(
            may_begin_operation(
                arbiter,
                lane_a,
                OP_RELEASE_PRODUCTION_PROOF,
            )
        )

    def test_production_proof_must_match_exact_merge_before_release(self):
        _, arbiter, lane_a, _ = self.setup_two_active()
        arbiter = acquire_publication_slot(
            arbiter,
            lane_a,
            pr_number=700,
            pr_head_sha=PR_HEAD,
        )
        arbiter = mark_publication_merged(
            arbiter,
            lane_id=LANE_A,
            merge_sha=MERGE,
        )
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "PRODUCTION_PROOF_REQUIRED",
        ):
            release_publication_slot_after_production(
                arbiter,
                lane_id=LANE_A,
                production_proof_passed=False,
                proved_main_sha=MERGE,
            )
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "PRODUCTION_MAIN_MISMATCH",
        ):
            release_publication_slot_after_production(
                arbiter,
                lane_id=LANE_A,
                production_proof_passed=True,
                proved_main_sha="f" * 40,
            )
        arbiter = release_publication_slot_after_production(
            arbiter,
            lane_id=LANE_A,
            production_proof_passed=True,
            proved_main_sha=MERGE,
        )
        self.assertEqual(
            arbiter["publication_slot"]["state"],
            SLOT_FREE,
        )

    def test_stale_other_lane_requires_explicit_main_rebind(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        arbiter = acquire_publication_slot(
            arbiter,
            lane_a,
            pr_number=700,
            pr_head_sha=PR_HEAD,
        )
        arbiter = mark_publication_merged(
            arbiter,
            lane_id=LANE_A,
            merge_sha=MERGE,
        )
        arbiter = release_publication_slot_after_production(
            arbiter,
            lane_id=LANE_A,
            production_proof_passed=True,
            proved_main_sha=MERGE,
        )
        self.assertFalse(
            may_begin_operation(
                arbiter,
                lane_b,
                OP_STAGE2_CENSUS,
            )
        )
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "REBIND_PROOF_REQUIRED",
        ):
            rebind_lane_main(
                lane_b,
                new_main_sha=MERGE,
                proof_kind="STAGE2_CURRENT_MAIN_REFRESH",
                proof_passed=False,
            )
        lane_b = rebind_lane_main(
            lane_b,
            new_main_sha=MERGE,
            proof_kind="STAGE2_CURRENT_MAIN_REFRESH",
            proof_passed=True,
        )
        self.assertTrue(
            may_begin_operation(
                arbiter,
                lane_b,
                OP_STAGE2_CENSUS,
            )
        )

    def test_recovery_is_lane_scoped_not_global(self):
        _, arbiter, lane_a, lane_b = self.setup_two_active()
        lane_a["active_request_id"] = "nevada-stage2-census-0001"
        lane_a["active_operation"] = OP_STAGE2_CENSUS
        lane_a["recovery_required"] = True
        validate_lane_state(lane_a)
        self.assertTrue(
            may_begin_operation(
                arbiter,
                lane_b,
                OP_STAGE2_CENSUS,
            )
        )

    def test_invalid_free_slot_owner_fails_closed(self):
        _, arbiter, _, _ = self.setup_shadow()
        arbiter["shared_mutation_slot"]["school_key"] = "nevada"
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "FREE_SHARED_SLOT_HAS_OWNER",
        ):
            validate_arbiter_state(arbiter)

    def test_unknown_operation_fails_closed(self):
        with self.assertRaisesRegex(
            TwoLaneContractError,
            "OPERATION_UNKNOWN",
        ):
            operation_class("DO_WHATEVER")


if __name__ == "__main__":
    unittest.main()
