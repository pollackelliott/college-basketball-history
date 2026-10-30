import contextlib
import csv
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import ingest_school  # noqa: E402
import verify_program_accomplishments  # noqa: E402


SCHOOL = "fresno-state"
SOURCE_FIELDS = [
    field
    for field in ingest_school.ASSERTION_FIELDS
    if field
    not in {
        "assertion_id",
        "canonical_game_id",
        "match_status",
        "match_method",
    }
]


def write_csv(path: Path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_game(round_name="Sweet Sixteen", game_type="NCAA_TOURNAMENT"):
    row = {field: "" for field in SOURCE_FIELDS}
    row.update(
        {
            "source_game_id": "FRESNO-S1-1981-82-030",
            "source_program_key": SCHOOL,
            "season_label": "1981-1982",
            "game_date": "1982-03-18",
            "source_opponent_label": "vs. Georgetown (4)",
            "normalized_opponent_key": "georgetown",
            "normalized_opponent_name": "Georgetown",
            "team_score": "40",
            "opponent_score": "58",
            "played_result": "L",
            "source_site_candidate": "vs.",
            "curated_site_type": "NEUTRAL",
            "city": "Provo",
            "state": "UT",
            "curated_game_type": game_type,
            "curated_postseason_round": round_name,
            "source_page": "47",
            "raw_text": "M 20 vs. Georgetown (4) L 58-40 15,237",
            "normalization_status": "PENDING_STAGE_2",
        }
    )
    return row


def canonical_game(
    game_id,
    season,
    date,
    opponent,
    fresno_score,
    opponent_score,
    round_name,
):
    row = {field: "" for field in ingest_school.CANONICAL_FIELDS}
    row.update(
        {
            "canonical_game_id": game_id,
            "season_label": season,
            "game_date": date,
            "date_precision": "EXACT",
            "team_a_key": SCHOOL,
            "team_b_key": opponent,
            "team_a_score": str(fresno_score),
            "team_b_score": str(opponent_score),
            "result_winner_team_key": (
                SCHOOL if fresno_score > opponent_score else opponent
            ),
            "site_type": "NEUTRAL",
            "venue_key": "fixture-arena",
            "venue_id": "VEN-999999",
            "site_city": "Provo",
            "site_state": "UT",
            "game_type": "NCAA_TOURNAMENT",
            "postseason_round": round_name,
            "canonical_status": "PROVISIONAL",
        }
    )
    return row


class PostseasonRoundEnrichmentTopologyTests(unittest.TestCase):
    def test_populated_ncaa_source_round_fills_blank_canonical_round(self):
        source = source_game()
        canonical = canonical_game(
            "CBBG-0000003",
            "1981-1982",
            "1982-03-18",
            "georgetown",
            40,
            58,
            "",
        )

        applied = ingest_school.apply_canonical_enrichment_candidates(
            source, canonical, {}
        )

        self.assertIn(("postseason_round", "Sweet Sixteen"), applied)
        self.assertEqual(canonical["postseason_round"], "Sweet Sixteen")

    def test_blank_source_round_leaves_blank_canonical_round_unresolved(self):
        source = source_game(round_name="")
        canonical = canonical_game(
            "CBBG-0000003",
            "1981-1982",
            "1982-03-18",
            "georgetown",
            40,
            58,
            "",
        )

        applied = ingest_school.apply_canonical_enrichment_candidates(
            source, canonical, {}
        )

        self.assertFalse(any(field == "postseason_round" for field, _ in applied))
        self.assertEqual(canonical["postseason_round"], "")

    def test_nonblank_canonical_round_is_never_overwritten(self):
        source = source_game(round_name="Sweet Sixteen")
        canonical = canonical_game(
            "CBBG-0000003",
            "1981-1982",
            "1982-03-18",
            "georgetown",
            40,
            58,
            "R32",
        )

        disagreements = ingest_school.discrepancy_candidates(source, canonical)
        applied = ingest_school.apply_canonical_enrichment_candidates(
            source, canonical, {}
        )

        self.assertIn(
            ("postseason_round", "Sweet Sixteen", "R32"),
            disagreements,
        )
        self.assertFalse(any(field == "postseason_round" for field, _ in applied))
        self.assertEqual(canonical["postseason_round"], "R32")

    def test_research_accepted_nonbracket_qualifier_marks_blank_canonical(self):
        source = source_game(round_name="")
        source["normalization_status"] = "RESEARCH_ACCEPTED"
        source["notes"] = (
            "district playoff/qualifier rather than a national-bracket round"
        )
        canonical = canonical_game(
            "CBBG-QUALIFIER",
            "1946-1947",
            "1947-03-18",
            "georgetown",
            41,
            47,
            "",
        )

        applied = ingest_school.apply_canonical_enrichment_candidates(
            source,
            canonical,
            {},
        )

        self.assertTrue(
            any(
                field == "notes"
                and "[NCAA_NON_APPEARANCE_QUALIFIER]" in value
                for field, value in applied
            )
        )
        self.assertIn(
            "[NCAA_NON_APPEARANCE_QUALIFIER]",
            canonical["notes"],
        )

    def test_nonbracket_qualifier_conflicts_with_existing_canonical_round(self):
        source = source_game(round_name="")
        source["normalization_status"] = "RESEARCH_ACCEPTED"
        source["notes"] = (
            "district playoff/qualifier rather than a national-bracket round"
        )
        canonical = canonical_game(
            "CBBG-QUALIFIER-CONFLICT",
            "1946-1947",
            "1947-03-18",
            "georgetown",
            41,
            47,
            "R64",
        )

        disagreements = ingest_school.discrepancy_candidates(
            source,
            canonical,
        )
        applied = ingest_school.apply_canonical_enrichment_candidates(
            source,
            canonical,
            {},
        )

        self.assertIn(
            (
                "postseason_round",
                "[NCAA_NON_APPEARANCE_QUALIFIER]",
                "R64",
            ),
            disagreements,
        )
        self.assertFalse(
            any(
                field == "notes"
                and "[NCAA_NON_APPEARANCE_QUALIFIER]" in value
                for field, value in applied
            )
        )

    def test_round_fill_is_narrowly_limited_to_ncaa_tournament_games(self):
        source = source_game(
            round_name="Championship",
            game_type="CONFERENCE_TOURNAMENT",
        )
        canonical = canonical_game(
            "CBBG-0000003",
            "1981-1982",
            "1982-03-18",
            "georgetown",
            40,
            58,
            "",
        )
        canonical["game_type"] = "CONFERENCE_TOURNAMENT"

        applied = ingest_school.apply_canonical_enrichment_candidates(
            source, canonical, {}
        )

        self.assertFalse(any(field == "postseason_round" for field, _ in applied))
        self.assertEqual(canonical["postseason_round"], "")


class FresnoDisposableIngestionRegressionTests(unittest.TestCase):
    def program_row(self):
        return {
            "program_key": SCHOOL,
            "public_page_enabled": "No",
            "history_start_season": "1970-1971",
            "history_scope_status": "OWNER_CONFIRMED",
            "history_scope_basis": "FIRST_TOP_LEVEL_SEASON",
            "history_scope_intervals": "",
        }

    def accomplishment_row(self):
        return {
            "program_key": SCHOOL,
            "conference_regular_season_championships": "5",
            "conference_tournament_championships": "2",
            "ncaa_tournament_appearances": "4",
            "final_four_appearances": "0",
            "national_championships": "0",
            "best_finish_key": "SWEET_SIXTEEN",
            "best_finish_year": "1982",
            "verification_status": "VERIFIED",
            "verification_basis": "Fresno regression fixture.",
            "canonical_crosscheck_status": "MATCH",
            "notes": "",
        }

    def canonical_games(self):
        return [
            canonical_game(
                "CBBG-0000001",
                "1980-1981",
                "1981-03-13",
                "northeastern",
                53,
                55,
                "",
            ),
            canonical_game(
                "CBBG-0000002",
                "1981-1982",
                "1982-03-13",
                "west-virginia",
                50,
                46,
                "R32",
            ),
            canonical_game(
                "CBBG-0000003",
                "1981-1982",
                "1982-03-18",
                "georgetown",
                40,
                58,
                "",
            ),
            canonical_game(
                "CBBG-0000004",
                "1983-1984",
                "1984-03-15",
                "louisiana-tech",
                56,
                66,
                "",
            ),
            canonical_game(
                "CBBG-0000005",
                "2000-2001",
                "2001-03-18",
                "michigan-state",
                65,
                81,
                "R32",
            ),
        ]

    def make_repo(self, repo: Path):
        write_csv(
            repo / "schools/fresno-state/source-games.csv",
            SOURCE_FIELDS,
            [source_game()],
        )
        write_csv(
            repo / "schools/fresno-state/venues.csv",
            (
                "venue_key",
                "venue_id",
                "canonical_name",
                "aliases",
                "city",
                "state",
                "first_assigned_game",
                "last_assigned_game",
                "relationship_start",
                "relationship_end",
                "known_opened",
                "known_closed",
            ),
            [],
        )
        write_csv(
            repo / "schools/fresno-state/conferences.csv",
            (
                "source_program_key",
                "start_season",
                "end_season",
                "conference_key",
                "conference_name",
                "membership_type",
                "ongoing",
                "basis",
                "notes",
            ),
            [],
        )
        write_csv(
            repo / "data/reference/conferences.csv",
            (
                "conference_key",
                "conference_name",
                "tournament_label",
                "status",
                "notes",
            ),
            [],
        )
        write_csv(
            repo / "data/reference/programs.csv",
            tuple(self.program_row()),
            [self.program_row()],
        )
        write_csv(
            repo / "data/reference/program-accomplishments.csv",
            tuple(self.accomplishment_row()),
            [self.accomplishment_row()],
        )
        write_csv(
            repo / "data/reference/venues.csv",
            (
                "venue_id",
                "venue_key",
                "display_name",
                "city",
                "state",
                "opened",
                "closed",
                "date_precision",
                "identity_status",
                "source_basis",
                "notes",
            ),
            [
                {
                    "venue_id": "VEN-999999",
                    "venue_key": "fixture-arena",
                    "display_name": "Fixture Arena",
                    "city": "Provo",
                    "state": "UT",
                    "opened": "",
                    "closed": "",
                    "date_precision": "",
                    "identity_status": "VERIFIED",
                    "source_basis": "Regression fixture.",
                    "notes": "",
                }
            ],
        )
        write_csv(
            repo / "data/reference/venue-names.csv",
            (
                "venue_id",
                "venue_name",
                "normalized_name",
                "name_type",
                "valid_from",
                "valid_to",
                "date_precision",
                "source_basis",
                "notes",
            ),
            [
                {
                    "venue_id": "VEN-999999",
                    "venue_name": "Fixture Arena",
                    "normalized_name": "fixturearena",
                    "name_type": "PROJECT_DISPLAY",
                    "valid_from": "",
                    "valid_to": "",
                    "date_precision": "",
                    "source_basis": "Regression fixture.",
                    "notes": "",
                }
            ],
        )
        write_csv(
            repo / "data/canonical/games.csv",
            ingest_school.CANONICAL_FIELDS,
            self.canonical_games(),
        )
        write_csv(
            repo / "data/evidence/game-assertions.csv",
            ingest_school.ASSERTION_FIELDS,
            [],
        )
        write_csv(
            repo / "data/reconciliation/discrepancies.csv",
            ingest_school.DISCREPANCY_FIELDS,
            [],
        )

    def run_ingest(self, repo: Path):
        output = io.StringIO()
        with patch.object(
            sys,
            "argv",
            [
                "ingest_school.py",
                SCHOOL,
                "--apply",
                "--repo",
                str(repo),
            ],
        ):
            with contextlib.redirect_stdout(output):
                result = ingest_school.main()
        return result, output.getvalue()

    def run_verifier(self, repo: Path):
        output = io.StringIO()
        with patch.object(
            sys,
            "argv",
            [
                "verify_program_accomplishments.py",
                SCHOOL,
                "--repo",
                str(repo),
            ],
        ):
            with contextlib.redirect_stdout(output):
                result = verify_program_accomplishments.main()
        return result, output.getvalue()

    def test_fresno_1982_sweet_sixteen_survives_ingestion_and_verifies(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            self.make_repo(repo)

            pre_result, pre_output = self.run_verifier(repo)
            self.assertEqual(pre_result, 1)
            self.assertIn("fresno-state: CONFLICT", pre_output)
            self.assertIn(
                "best_finish_key: reference='SWEET_SIXTEEN', canonical='ROUND_OF_32'",
                pre_output,
            )
            self.assertIn(
                "best_finish_year: reference='1982', canonical='2001'",
                pre_output,
            )

            ingest_result, ingest_output = self.run_ingest(repo)
            self.assertEqual(ingest_result, 0, ingest_output)

            canonical = {
                row["canonical_game_id"]: row
                for row in read_csv(repo / "data/canonical/games.csv")
            }
            self.assertEqual(
                canonical["CBBG-0000003"]["postseason_round"],
                "Sweet Sixteen",
            )

            post_result, post_output = self.run_verifier(repo)
            self.assertEqual(post_result, 0, post_output)
            self.assertIn("fresno-state: MATCH", post_output)
            self.assertIn(
                "1980-1981 has no resolved NCAA round",
                post_output,
            )
            self.assertIn(
                "1983-1984 has no resolved NCAA round",
                post_output,
            )


if __name__ == "__main__":
    unittest.main()
