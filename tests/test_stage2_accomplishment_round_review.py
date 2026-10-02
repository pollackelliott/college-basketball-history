import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
from onboarding_plan import apply_reconciliation_decisions  # noqa: E402


def write_csv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


class Stage2AccomplishmentRoundReviewTests(unittest.TestCase):
    def test_new_game_round_patch_resolves_canonical_id_after_ingestion(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            school_key = "example"
            source_id = "EXAMPLE-NEW-TITLE"
            canonical_id = "CBBG-NEW-0001"

            canonical = {field: "" for field in ingest_school.CANONICAL_FIELDS}
            canonical.update(
                {
                    "canonical_game_id": canonical_id,
                    "season_label": "2003-2004",
                    "game_date": "2004-04-05",
                    "date_precision": "EXACT",
                    "team_a_key": school_key,
                    "team_b_key": "opponent",
                    "team_a_score": "73",
                    "team_b_score": "82",
                    "result_winner_team_key": "opponent",
                    "overtime_periods": "0",
                    "site_type": "NEUTRAL",
                    "game_type": "NCAA_TOURNAMENT",
                    "postseason_round": "",
                    "canonical_status": "PROVISIONAL",
                }
            )

            source = {field: "" for field in ingest_school.ASSERTION_FIELDS}
            source.update(
                {
                    "source_program_key": school_key,
                    "source_game_id": source_id,
                    "season_label": "2003-2004",
                    "game_date": "2004-04-05",
                    "normalized_opponent_key": "opponent",
                    "team_score": "73",
                    "opponent_score": "82",
                    "played_result": "L",
                    "overtime_periods": "0",
                    "curated_site_type": "NEUTRAL",
                    "curated_game_type": "NCAA_TOURNAMENT",
                    "curated_postseason_round": "",
                    "raw_text": "National championship game; raw source preserved.",
                }
            )
            assertion = dict(source)
            assertion.update(
                {
                    "assertion_id": "ASRT-EXAMPLE-1",
                    "canonical_game_id": canonical_id,
                    "match_status": "NEW_CANONICAL",
                    "match_method": "NEW_GAME",
                }
            )

            write_csv(
                repo / "data/canonical/games.csv",
                ingest_school.CANONICAL_FIELDS,
                [canonical],
            )
            write_csv(
                repo / "data/evidence/game-assertions.csv",
                ingest_school.ASSERTION_FIELDS,
                [assertion],
            )
            write_csv(
                repo / "data/reconciliation/discrepancies.csv",
                ingest_school.DISCREPANCY_FIELDS,
                [],
            )
            write_csv(
                repo / "schools" / school_key / "source-games.csv",
                ingest_school.ASSERTION_FIELDS,
                [source],
            )

            approved = {
                "school_key": school_key,
                "approved_plan_hash": "a" * 64,
                "decisions": [
                    {
                        "decision_id": "NCAA-ROUND-PATCH-EXAMPLE-NEW-TITLE",
                        "category": "ncaa_round_patch",
                        "source_game_id": source_id,
                        # Preflight cannot know the ID assigned to a NEW_GAME.
                        "canonical_game_id": "",
                        "field_name": "postseason_round",
                        "decision": "APPLY_NCAA_ROUND_PATCH",
                        "resolution_basis": "Authoritative tournament evidence.",
                        "canonical_patch": {"postseason_round": "Championship"},
                        "source_patch": {
                            "curated_postseason_round": "Championship"
                        },
                    }
                ],
            }

            counts = apply_reconciliation_decisions(repo, approved)
            self.assertEqual(counts["ncaa_round_patches"], 1)

            with (repo / "data/canonical/games.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                canonical_after = next(csv.DictReader(handle))
            with (repo / "data/evidence/game-assertions.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                assertion_after = next(csv.DictReader(handle))
            with (repo / "schools" / school_key / "source-games.csv").open(
                encoding="utf-8-sig", newline=""
            ) as handle:
                source_after = next(csv.DictReader(handle))

            self.assertEqual(canonical_after["postseason_round"], "Championship")
            self.assertEqual(
                assertion_after["curated_postseason_round"],
                "Championship",
            )
            self.assertEqual(
                source_after["curated_postseason_round"],
                "Championship",
            )
            self.assertEqual(
                source_after["raw_text"],
                "National championship game; raw source preserved.",
            )


if __name__ == "__main__":
    unittest.main()
