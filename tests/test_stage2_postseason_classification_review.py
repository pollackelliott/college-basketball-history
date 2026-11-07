"""Stage 2 owner-gated generic postseason classification regressions."""

import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
from onboarding_plan import (  # noqa: E402
    REVIEW_COLUMNS, WorkflowError, approve_plan,
    apply_pre_ingest_source_patches, apply_reconciliation_decisions,
)
from postseason_classification_review import (  # noqa: E402
    HISTORICAL_CHALLENGE_CANONICAL_IDENTITY_FIELDS,
    HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE,
    build_historical_game_type_challenge_review,
    build_review_rows,
    mismatch_is_reviewable,
    nonappearance_qualifier_mismatch_is_reviewable,
    row_fingerprint,
    validate_historical_game_type_challenges,
)
from program_history import NCAA_NON_APPEARANCE_QUALIFIER_MARKER  # noqa: E402


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def sample_source():
    row = {field: "" for field in ingest_school.ASSERTION_FIELDS}
    row.update({
        "source_game_id": "SCHOOL-POST-01",
        "source_program_key": "school",
        "season_label": "2023-2024",
        "game_date": "2024-04-08",
        "normalized_opponent_key": "purdue",
        "source_opponent_label": "Purdue",
        "team_score": "75",
        "opponent_score": "60",
        "played_result": "W",
        "curated_site_type": "SOURCE_PROGRAM_HOME",
        "curated_game_type": "POSTSEASON",
        "curated_postseason_round": "",
        "curated_venue_name": "Example Arena",
        "raw_text": "Institutional 2024 title score; immutable literal.",
    })
    return row


def review_item(row=None, **changes):
    row = row or sample_source()
    candidate = {
        "source": row,
        "canonical_game_id": "",
        "canonical_game_date": "",
        "canonical_game_type": "",
    }
    item = build_review_rows("school", [candidate])[0]
    item.update({
        "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
        "resolution_basis": "Owner-approved, exact institutional result.",
        "source_patch": {
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "Championship",
        },
        "canonical_patch": {},
    })
    item.update(changes)
    return item


def make_source_repo(root, source=None):
    source = source or sample_source()
    path = root / "schools/school/source-games.csv"
    write_csv(path, list(source), [source])
    return path


class EligibilityAndReviewTests(unittest.TestCase):
    def setUp(self):
        self.reference = {
            "ncaa_tournament_appearances": "3",
            "final_four_appearances": "1",
            "national_championships": "1",
        }
        self.derived = {
            "ncaa_tournament_appearances": 1,
            "final_four_appearances": 0,
            "national_championships": 0,
        }

    def candidates(self, seasons):
        return [{
            "source": {**sample_source(),
                       "source_game_id": f"POST-{j}",
                       "season_label": season},
        } for j, season in enumerate(seasons)]

    def test_missing_appearances_with_sufficient_generic_seasons_reviewable(self):
        self.assertTrue(mismatch_is_reviewable(
            self.reference, self.derived,
            self.candidates(["2022-2023", "2023-2024"]),
        ))

    def test_absent_generic_postseason_remains_blocked(self):
        self.assertFalse(mismatch_is_reviewable(
            self.reference, self.derived, [],
        ))

    def test_insufficient_distinct_seasons_remains_blocked(self):
        self.assertFalse(mismatch_is_reviewable(
            self.reference, self.derived,
            self.candidates(["2023-2024", "2023-2024"]),
        ))

    def test_existing_earned_titles_cannot_be_erased(self):
        self.derived["national_championships"] = 2
        self.assertFalse(mismatch_is_reviewable(
            self.reference, self.derived,
            self.candidates(["2022-2023", "2023-2024"]),
        ))

    def test_no_automatic_ncaa_reclassification(self):
        row = sample_source()
        original = dict(row)
        decisions = build_review_rows("school", [{
            "source": row, "canonical_game_id": "",
        }])
        self.assertEqual(len(decisions), 1)
        self.assertEqual(decisions[0]["decision"], "PENDING")
        self.assertEqual(decisions[0]["source_value"], "POSTSEASON")
        self.assertEqual(decisions[0]["source_game_date"], "2024-04-08")
        self.assertEqual(row, original)

    def test_duplicate_or_non_generic_rows_refused(self):
        candidate = {"source": sample_source()}
        with self.assertRaisesRegex(ValueError, "unique"):
            build_review_rows("school", [candidate, candidate])
        row = sample_source()
        row["curated_game_type"] = "NCAA_TOURNAMENT"
        with self.assertRaisesRegex(ValueError, "generic"):
            build_review_rows("school", [{"source": row}])

    def test_fingerprint_binds_every_frozen_source_field(self):
        source = sample_source()
        original = row_fingerprint(source)
        source["raw_text"] += " changed"
        self.assertNotEqual(row_fingerprint(source), original)


class HistoricalGameTypeChallengeTests(unittest.TestCase):
    def challenge(self, source):
        return {
            "source_game_id": source["source_game_id"],
            "source_row_sha256": row_fingerprint(source),
            "expected_source_game_type": "REGULAR_SEASON",
            "proposed_source_game_type": "NCAA_TOURNAMENT",
            "evidence_basis": "Institutional evidence identifies this exact NCAA game.",
        }

    def regular_source(self):
        row = sample_source()
        row["curated_game_type"] = "REGULAR_SEASON"
        row["curated_postseason_round"] = ""
        row["curated_site_type"] = "NEUTRAL"
        return row

    def expected_identity(self):
        return {
            field: "" for field in HISTORICAL_CHALLENGE_CANONICAL_IDENTITY_FIELDS
        }

    def test_challenge_document_is_strict_and_unapproved(self):
        source = self.regular_source()
        doc = {
            "schema_version": 1,
            "kind": "STAGE2_HISTORICAL_GAME_TYPE_CHALLENGES",
            "school_key": "school",
            "authority_basis": "Control Center post-freeze contradiction disposition.",
            "challenges": [self.challenge(source)],
        }
        parsed = validate_historical_game_type_challenges(doc, "school")
        self.assertEqual(parsed[source["source_game_id"]]["proposed_source_game_type"],
                         "NCAA_TOURNAMENT")
        decision = build_historical_game_type_challenge_review(
            "school",
            {"source": source, "planned_identity_status": "NEW_GAME"},
            parsed[source["source_game_id"]],
            self.expected_identity(),
        )
        self.assertEqual(decision["decision"], "PENDING")
        self.assertEqual(decision["source_value"], "REGULAR_SEASON")
        self.assertEqual(decision["allowed_actions"],
                         ["APPLY_POSTSEASON_CLASSIFICATION_PATCH"])
        self.assertEqual(decision["frozen_source_row"], source)

    def test_challenge_rejects_widened_or_stale_payload(self):
        source = self.regular_source()
        doc = {
            "schema_version": 1,
            "kind": "STAGE2_HISTORICAL_GAME_TYPE_CHALLENGES",
            "school_key": "school",
            "authority_basis": "Control Center disposition.",
            "challenges": [self.challenge(source)],
        }
        doc["challenges"][0]["curated_postseason_round"] = "R64"
        with self.assertRaisesRegex(ValueError, "require exactly"):
            validate_historical_game_type_challenges(doc, "school")

        doc["challenges"][0].pop("curated_postseason_round")
        doc["challenges"][0]["source_row_sha256"] = "0" * 64
        parsed = validate_historical_game_type_challenges(doc, "school")
        with self.assertRaisesRegex(ValueError, "fingerprint"):
            build_historical_game_type_challenge_review(
                "school",
                {"source": source, "planned_identity_status": "NEW_GAME"},
                parsed[source["source_game_id"]],
                self.expected_identity(),
            )

    def test_challenge_pre_ingest_changes_only_game_type(self):
        source = self.regular_source()
        frozen = dict(source)
        challenge = self.challenge(source)
        decision = build_historical_game_type_challenge_review(
            "school",
            {"source": source, "planned_identity_status": "NEW_GAME"},
            challenge,
            self.expected_identity(),
        )
        decision.update({
            "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
            "resolution_basis": "Owner Gate 1 approved institutional evidence.",
            "source_patch": {"curated_game_type": "NCAA_TOURNAMENT"},
            "canonical_patch": {},
        })
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source_path = make_source_repo(repo, source)
            counts = apply_pre_ingest_source_patches(
                repo, {"school_key": "school", "decisions": [decision]}
            )
            final = read_csv(source_path)[0]
        self.assertEqual(counts["historical_game_type_challenges_applied"], 1)
        self.assertEqual(final["curated_game_type"], "NCAA_TOURNAMENT")
        for field, value in frozen.items():
            if field != "curated_game_type":
                self.assertEqual(final[field], value, field)


class HistoricalNonappearanceQualifierChallengeTests(unittest.TestCase):
    def qualifier_source(self):
        row = sample_source()
        row.update({
            "source_game_id": "FORDHAM-1990-91-031",
            "season_label": "1990-1991",
            "game_date": "1991-03-06",
            "normalized_opponent_key": "saint-francis-pa",
            "source_opponent_label": "St. Francis (NCP)",
            "team_score": "64",
            "opponent_score": "70",
            "played_result": "L",
            "curated_site_type": "OPPONENT_HOME",
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "Play-in",
            "normalization_status": "RESEARCH_ACCEPTED",
            "notes": (
                "Stage 6 NCAA-round review: Fordham institutional history explicitly "
                "identifies the Saint Francis game as an NCAA Play-In game."
            ),
            "raw_text": "Mar. 6 at St. Francis (NCP) 64 70 L",
        })
        return row

    def challenge(self, source, expected_round="Play-in", proposed_round=""):
        return {
            "challenge_type": HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE,
            "source_game_id": source["source_game_id"],
            "source_row_sha256": row_fingerprint(source),
            "expected_source_game_type": "NCAA_TOURNAMENT",
            "proposed_source_game_type": "NCAA_TOURNAMENT",
            "expected_source_postseason_round": expected_round,
            "proposed_source_postseason_round": proposed_round,
            "evidence_basis": (
                "Fordham institutional history says the Patriot League lacked an "
                "automatic bid, Fordham lost this NCAA-administered play-in, then "
                "awaited an at-large bid before entering the NIT."
            ),
        }

    def expected_identity(self):
        return {
            field: "" for field in HISTORICAL_CHALLENGE_CANONICAL_IDENTITY_FIELDS
        }

    def document(self, source, **changes):
        challenge = self.challenge(source)
        challenge.update(changes)
        return {
            "schema_version": 1,
            "kind": "STAGE2_HISTORICAL_GAME_TYPE_CHALLENGES",
            "school_key": "school",
            "authority_basis": "Control Center Issue #502.",
            "challenges": [challenge],
        }

    def test_exact_fordham_1991_qualifier_topology_is_owner_reviewable(self):
        source = self.qualifier_source()
        parsed = validate_historical_game_type_challenges(
            self.document(source), "school"
        )
        challenge = parsed[source["source_game_id"]]
        self.assertEqual(
            challenge["challenge_type"],
            HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE,
        )
        decision = build_historical_game_type_challenge_review(
            "school",
            {"source": source, "planned_identity_status": "NEW_GAME"},
            challenge,
            self.expected_identity(),
        )
        self.assertTrue(
            decision["historical_ncaa_nonappearance_qualifier_challenge"]
        )
        self.assertEqual(decision["source_value"], "Play-in")
        self.assertEqual(decision["decision"], "PENDING")
        self.assertEqual(
            decision["allowed_actions"],
            ["APPLY_POSTSEASON_CLASSIFICATION_PATCH"],
        )

        reference = {
            "ncaa_tournament_appearances": "4",
            "final_four_appearances": "0",
            "national_championships": "0",
        }
        derived = {
            "ncaa_tournament_appearances": 5,
            "final_four_appearances": 0,
            "national_championships": 0,
        }
        candidate = {
            "source": source,
            "historical_challenge_type":
                HISTORICAL_CHALLENGE_NONAPPEARANCE_TYPE,
        }
        self.assertTrue(
            nonappearance_qualifier_mismatch_is_reviewable(
                reference,
                derived,
                [candidate],
                {"1990-1991": 1},
            )
        )
        self.assertFalse(
            nonappearance_qualifier_mismatch_is_reviewable(
                reference,
                derived,
                [candidate],
                {"1990-1991": 2},
            )
        )

    def test_qualifier_challenge_fails_closed_on_wrong_or_nonblank_round(self):
        source = self.qualifier_source()
        with self.assertRaisesRegex(ValueError, "must clear"):
            validate_historical_game_type_challenges(
                self.document(
                    source,
                    proposed_source_postseason_round="R64",
                ),
                "school",
            )

        parsed = validate_historical_game_type_challenges(
            self.document(
                source,
                expected_source_postseason_round="R64",
            ),
            "school",
        )
        with self.assertRaisesRegex(ValueError, "source round changed"):
            build_historical_game_type_challenge_review(
                "school",
                {"source": source, "planned_identity_status": "NEW_GAME"},
                parsed[source["source_game_id"]],
                self.expected_identity(),
            )

    def test_qualifier_pre_ingest_changes_only_round_and_durable_marker(self):
        source = self.qualifier_source()
        frozen = dict(source)
        parsed = validate_historical_game_type_challenges(
            self.document(source), "school"
        )
        decision = build_historical_game_type_challenge_review(
            "school",
            {"source": source, "planned_identity_status": "NEW_GAME"},
            parsed[source["source_game_id"]],
            self.expected_identity(),
        )
        decision.update({
            "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
            "resolution_basis": "Owner Gate 1 approved exact institutional evidence.",
            "source_patch": {
                "curated_game_type": "NCAA_TOURNAMENT",
                "curated_postseason_round": "",
            },
            "canonical_patch": {},
        })
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source_path = make_source_repo(repo, source)
            counts = apply_pre_ingest_source_patches(
                repo, {"school_key": "school", "decisions": [decision]}
            )
            final = read_csv(source_path)[0]

        self.assertEqual(
            counts["historical_ncaa_nonappearance_qualifier_challenges_applied"],
            1,
        )
        self.assertEqual(final["curated_game_type"], "NCAA_TOURNAMENT")
        self.assertEqual(final["curated_postseason_round"], "")
        self.assertIn(NCAA_NON_APPEARANCE_QUALIFIER_MARKER, final["notes"])
        for field, value in frozen.items():
            if field not in {"curated_postseason_round", "notes"}:
                self.assertEqual(final[field], value, field)


class SealedPreIngestTests(unittest.TestCase):
    def run_apply(self, **changes):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            path = make_source_repo(repo)
            item = review_item(**changes)
            result = apply_pre_ingest_source_patches(
                repo, {"school_key": "school", "decisions": [item]}
            )
            return result, read_csv(path)[0]

    def test_source_type_and_round_only_under_sealed_decision(self):
        counts, row = self.run_apply()
        self.assertEqual(counts["postseason_classifications_applied"], 1)
        self.assertEqual(row["curated_game_type"], "NCAA_TOURNAMENT")
        self.assertEqual(row["curated_postseason_round"], "Championship")
        self.assertEqual(row["curated_site_type"], "SOURCE_PROGRAM_HOME")
        self.assertEqual(
            row["raw_text"], "Institutional 2024 title score; immutable literal."
        )

    def test_explicit_site_change_is_separate_and_counted(self):
        counts, row = self.run_apply(source_patch={
            "curated_game_type": "NCAA_TOURNAMENT",
            "curated_postseason_round": "Championship",
            "curated_site_type": "NEUTRAL",
        })
        self.assertEqual(counts["postseason_owner_site_patches"], 1)
        self.assertEqual(row["curated_site_type"], "NEUTRAL")

    def test_unknown_round_cannot_pass(self):
        with self.assertRaisesRegex(WorkflowError, "invalid NCAA round"):
            self.run_apply(source_patch={
                "curated_game_type": "NCAA_TOURNAMENT",
                "curated_postseason_round": "Regional Quarterfinal",
            })

    def test_invalid_type_cannot_pass(self):
        with self.assertRaisesRegex(WorkflowError, "invalid sealed postseason"):
            self.run_apply(source_patch={"curated_game_type": "REGULAR_SEASON"})

    def test_raw_text_patch_cannot_pass(self):
        with self.assertRaisesRegex(WorkflowError, "forbidden source fields"):
            self.run_apply(source_patch={
                "curated_game_type": "NIT",
                "raw_text": "fabricated",
            })

    def test_fingerprint_change_stops_transaction(self):
        with self.assertRaisesRegex(WorkflowError, "frozen postseason"):
            self.run_apply(source_row_sha256="0" * 64)

    def test_unresolved_status_requires_no_patch(self):
        counts, row = self.run_apply(
            decision="KEEP_POSTSEASON_UNRESOLVED", source_patch={}
        )
        self.assertEqual(counts["postseason_classifications_left_unresolved"], 1)
        self.assertEqual(row["curated_game_type"], "POSTSEASON")
        with self.assertRaisesRegex(WorkflowError, "unchanged"):
            self.run_apply(decision="KEEP_POSTSEASON_UNRESOLVED")


class PostIngestCanonicalTests(unittest.TestCase):
    def make_repo(
        self, root, canonical_type="POSTSEASON",
        source_type="NCAA_TOURNAMENT", canonical_round="",
    ):
        src = sample_source()
        src["curated_game_type"] = source_type
        src["curated_postseason_round"] = "Championship"
        source_path = make_source_repo(root, src)
        assertion = dict(src)
        assertion.update({
            "assertion_id": "ASRT-TEST-0001",
            "canonical_game_id": "CBBG-0000001",
            "match_status": "CONFIDENT",
            "match_method": "EXACT",
        })
        write_csv(
            root / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS, [assertion],
        )
        canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
        canonical.update({
            "canonical_game_id": "CBBG-0000001",
            "season_label": "2023-2024",
            "game_date": "2024-04-08",
            "date_precision": "EXACT",
            "team_a_key": "purdue",
            "team_b_key": "school",
            "site_type": "NEUTRAL",
            "game_type": canonical_type,
            "postseason_round": canonical_round,
        })
        write_csv(
            root / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS, [canonical],
        )
        write_csv(
            root / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS, [],
        )
        return source_path

    def make_approved(self):
        return {
            "school_key": "school",
            "approved_plan_hash": "a" * 64,
            "decisions": [{
                "decision_id": "POSTSEASON-CLASSIFICATION-SCHOOL-POST-01",
                "category": "postseason_classification",
                "source_game_id": "SCHOOL-POST-01",
                "canonical_game_id": "CBBG-0000001",
                "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
                "resolution_basis": "Institutional championship result.",
                "source_patch": {
                    "curated_game_type": "NCAA_TOURNAMENT",
                    "curated_postseason_round": "Championship",
                },
                "canonical_patch": {},
            }],
        }

    def test_generic_canonical_is_enriched_after_owner_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.make_repo(repo)
            counts = apply_reconciliation_decisions(repo, self.make_approved())
            self.assertEqual(counts["postseason_canonical_types_enriched"], 1)
            final = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(final["game_type"], "NCAA_TOURNAMENT")
            self.assertEqual(final["postseason_round"], "Championship")

    def test_established_conflicting_canonical_requires_separate_review(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.make_repo(repo, canonical_type="REGULAR_SEASON")
            with self.assertRaisesRegex(WorkflowError, "own explicit Gate 1"):
                apply_reconciliation_decisions(repo, self.make_approved())

    def test_established_round_is_not_silently_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            self.make_repo(
                repo, canonical_type="NCAA_TOURNAMENT",
                canonical_round="Sweet Sixteen",
            )
            with self.assertRaisesRegex(WorkflowError, "cannot overwrite established"):
                apply_reconciliation_decisions(repo, self.make_approved())

    def test_explicit_sealed_canonical_round_correction(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            source_path = self.make_repo(
                repo, canonical_type="NCAA_TOURNAMENT",
                canonical_round="Sweet Sixteen",
            )
            approved = self.make_approved()
            approved["decisions"][0]["canonical_patch"] = {
                "postseason_round": "Championship",
            }
            result = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(result["postseason_canonical_rounds_corrected"], 1)
            canonical = read_csv(repo / "data/canonical/games.csv")[0]
            self.assertEqual(canonical["postseason_round"], "Championship")
            self.assertIn("Sweet Sixteen", canonical["notes"])
            self.assertIn("POSTSEASON-CLASSIFICATION-SCHOOL-POST-01", canonical["notes"])
            self.assertEqual(read_csv(source_path)[0]["raw_text"],
                             "Institutional 2024 title score; immutable literal.")

    def test_wrong_or_redundant_canonical_round_patch_rejected(self):
        for old_round, correction in (
            ("Sweet Sixteen", "R32"),
            ("Championship", "Championship"),
        ):
            with self.subTest(old_round=old_round, correction=correction):
                with tempfile.TemporaryDirectory() as tmp:
                    repo = Path(tmp)
                    self.make_repo(
                        repo, canonical_type="NCAA_TOURNAMENT",
                        canonical_round=old_round,
                    )
                    approved = self.make_approved()
                    approved["decisions"][0]["canonical_patch"] = {
                        "postseason_round": correction,
                    }
                    with self.assertRaisesRegex(
                        WorkflowError, "exact owner-reviewed patch|redundant",
                    ):
                        apply_reconciliation_decisions(repo, approved)

    def test_owner_review_validates_round_correction_before_sealing(self):
        for prior, correction, expected_error in (
            ("Sweet Sixteen", "Championship", None),
            ("Sweet Sixteen", "R32", "must equal"),
            ("", "Championship", "established, conflicting"),
            ("Championship", "Championship", "established, conflicting"),
        ):
            with self.subTest(prior=prior, correction=correction):
                with tempfile.TemporaryDirectory() as tmp:
                    repo = Path(tmp)
                    self.make_repo(
                        repo, canonical_type="NCAA_TOURNAMENT",
                        canonical_round=prior,
                    )
                    item = review_item(canonical_game_id="CBBG-0000001")
                    plan = {
                        "school_key": "school",
                        "blockers": [],
                        "input_fingerprint": {"sha256": "frozen"},
                        "decisions": [item],
                    }
                    plan_path = repo / "plan.json"
                    plan_path.write_text(json.dumps(plan), encoding="utf-8")
                    review = {
                        **item,
                        "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
                        "canonical_patch_json": json.dumps(
                            {"postseason_round": correction}
                        ),
                        "source_patch_json": json.dumps(item["source_patch"]),
                    }
                    review_path = repo / "review.csv"
                    write_csv(review_path, list(REVIEW_COLUMNS), [
                        {field: review.get(field, "") for field in REVIEW_COLUMNS}
                    ])
                    with patch(
                        "onboarding_plan.input_fingerprint",
                        return_value={"sha256": "frozen"},
                    ):
                        if expected_error:
                            with self.assertRaisesRegex(WorkflowError, expected_error):
                                approve_plan(repo, plan_path, review_path, "owner")
                        else:
                            sealed, _ = approve_plan(
                                repo, plan_path, review_path, "owner",
                            )
                            self.assertEqual(
                                sealed["decisions"][0]["canonical_patch"],
                                {"postseason_round": "Championship"},
                            )

    def challenge_approved(self, canonical_identity, frozen_source):
        return {
            "school_key": "school",
            "approved_plan_hash": "a" * 64,
            "decisions": [{
                "decision_id": "HISTORICAL-GAME-TYPE-SCHOOL-POST-01",
                "category": "postseason_classification",
                "source_game_id": "SCHOOL-POST-01",
                "canonical_game_id": "",
                "season_label": frozen_source["season_label"],
                "source_game_date": frozen_source["game_date"],
                "source_value": "REGULAR_SEASON",
                "decision": "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
                "resolution_basis": "Owner-approved exact institutional NCAA evidence.",
                "source_patch": {"curated_game_type": "NCAA_TOURNAMENT"},
                "canonical_patch": {},
                "source_row_sha256": row_fingerprint(frozen_source),
                "frozen_source_row": dict(frozen_source),
                "expected_canonical_identity": dict(canonical_identity),
                "planned_identity_status": "NEW_GAME",
                "historical_game_type_challenge": True,
                "proposed_game_type": "NCAA_TOURNAMENT",
            }],
        }

    def test_historical_challenge_verifies_exact_post_ingest_canonical_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            frozen = sample_source()
            frozen["curated_game_type"] = "REGULAR_SEASON"
            frozen["curated_postseason_round"] = ""
            frozen["curated_site_type"] = "NEUTRAL"
            applied = dict(frozen)
            applied["curated_game_type"] = "NCAA_TOURNAMENT"
            make_source_repo(repo, applied)
            assertion = dict(applied)
            assertion.update({
                "assertion_id": "ASRT-TEST-0001",
                "canonical_game_id": "CBBG-0000001",
                "match_status": "CONFIDENT",
                "match_method": "NEW_GAME",
            })
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS, [assertion],
            )
            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            canonical.update({
                "canonical_game_id": "CBBG-0000001",
                "season_label": frozen["season_label"],
                "game_date": frozen["game_date"],
                "date_precision": "EXACT",
                "team_a_key": "purdue",
                "team_b_key": "school",
                "team_a_score": "60",
                "team_b_score": "75",
                "result_winner_team_key": "school",
                "overtime_periods": "",
                "site_type": "NEUTRAL",
                "designated_home_team_key": "",
                "venue_key": "",
                "venue_id": "",
                "site_city": "",
                "site_state": "",
                "game_type": "NCAA_TOURNAMENT",
                "postseason_round": "",
                "canonical_status": "PROVISIONAL",
            })
            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS, [canonical],
            )
            write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS, [],
            )
            identity = {
                field: canonical.get(field, "")
                for field in HISTORICAL_CHALLENGE_CANONICAL_IDENTITY_FIELDS
            }
            result = apply_reconciliation_decisions(
                repo, self.challenge_approved(identity, frozen)
            )
            self.assertEqual(result.get("postseason_canonical_types_enriched", 0), 0)
            self.assertEqual(
                read_csv(repo / "data/canonical/games.csv")[0]["game_type"],
                "NCAA_TOURNAMENT",
            )

    def test_historical_challenge_rejects_identity_drift_and_inferred_round(self):
        for mutation, pattern in (
            ({"team_a_score": "61"}, "canonical identity changed"),
            ({"postseason_round": "R64"}, "unauthorized postseason round"),
        ):
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory() as tmp:
                    repo = Path(tmp)
                    frozen = sample_source()
                    frozen["curated_game_type"] = "REGULAR_SEASON"
                    frozen["curated_postseason_round"] = ""
                    frozen["curated_site_type"] = "NEUTRAL"
                    applied = dict(frozen)
                    applied["curated_game_type"] = "NCAA_TOURNAMENT"
                    make_source_repo(repo, applied)
                    assertion = dict(applied)
                    assertion.update({
                        "assertion_id": "ASRT-TEST-0001",
                        "canonical_game_id": "CBBG-0000001",
                        "match_status": "CONFIDENT",
                        "match_method": "NEW_GAME",
                    })
                    write_csv(
                        repo / "data/evidence/game-assertions.csv",
                        ingest_school.ASSERTION_FIELDS, [assertion],
                    )
                    canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
                    canonical.update({
                        "canonical_game_id": "CBBG-0000001",
                        "season_label": frozen["season_label"],
                        "game_date": frozen["game_date"],
                        "date_precision": "EXACT",
                        "team_a_key": "purdue",
                        "team_b_key": "school",
                        "team_a_score": "60",
                        "team_b_score": "75",
                        "result_winner_team_key": "school",
                        "site_type": "NEUTRAL",
                        "game_type": "NCAA_TOURNAMENT",
                        "canonical_status": "PROVISIONAL",
                    })
                    identity = {
                        field: canonical.get(field, "")
                        for field in HISTORICAL_CHALLENGE_CANONICAL_IDENTITY_FIELDS
                    }
                    canonical.update(mutation)
                    write_csv(
                        repo / "data/canonical/games.csv",
                        ingest_school.CANONICAL_FIELDS, [canonical],
                    )
                    write_csv(
                        repo / "data/reconciliation/discrepancies.csv",
                        ingest_school.DISCREPANCY_FIELDS, [],
                    )
                    with self.assertRaisesRegex(WorkflowError, pattern):
                        apply_reconciliation_decisions(
                            repo, self.challenge_approved(identity, frozen)
                        )

    def test_original_review_population_not_auto_approved(self):
        source = sample_source()
        decision = build_review_rows("school", [{"source": source}])[0]
        self.assertEqual(decision["decision"], "PENDING")
        self.assertEqual(decision["allowed_actions"], [
            "APPLY_POSTSEASON_CLASSIFICATION_PATCH",
            "KEEP_POSTSEASON_UNRESOLVED",
        ])


if __name__ == "__main__":
    unittest.main()
