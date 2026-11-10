import csv
import io
import shutil
import sys
import tempfile
import unittest
from collections import Counter
from contextlib import redirect_stdout
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ingest_school  # noqa: E402
import validate_data  # noqa: E402
from location_safety import append_note, registry_fallback_marker  # noqa: E402


VENUE_NAME = "Fixture Shared Arena"
OLD_KEY = "fixture-shared-arena-old"
NEW_KEY = "fixture-shared-arena-new"
OLD_ID = "VEN-999997"
NEW_ID = "VEN-999998"
CITY = "Fixture City"
STATE = "IL"


def read_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(path: Path, fields, rows):
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class ValidateDataVenueNamePeriodIntegrationTests(unittest.TestCase):
    def test_real_validation_loader_uses_registered_name_periods_and_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            repo = Path(temporary)
            shutil.copytree(ROOT / "data", repo / "data")
            shutil.copytree(ROOT / "schools", repo / "schools")

            canonical_path = repo / "data/canonical/games.csv"
            assertions_path = repo / "data/evidence/game-assertions.csv"
            source_path = repo / "schools/depaul/source-games.csv"
            school_venues_path = repo / "schools/depaul/venues.csv"
            global_venues_path = repo / "data/reference/venues.csv"
            venue_names_path = repo / "data/reference/venue-names.csv"

            canonical_fields, canonical_rows = read_csv(canonical_path)
            assertion_fields, assertion_rows = read_csv(assertions_path)
            source_fields, source_rows = read_csv(source_path)
            school_venue_fields, school_venue_rows = read_csv(school_venues_path)
            global_venue_fields, global_venue_rows = read_csv(global_venues_path)
            venue_name_fields, venue_name_rows = read_csv(venue_names_path)

            self.assertNotIn(OLD_ID, {row.get("venue_id", "") for row in global_venue_rows})
            self.assertNotIn(NEW_ID, {row.get("venue_id", "") for row in global_venue_rows})

            canonical_by_id = {
                row.get("canonical_game_id", ""): row for row in canonical_rows
            }
            assertion_counts = Counter(
                row.get("canonical_game_id", "") for row in assertion_rows
            )
            source_by_id = {
                row.get("source_game_id", ""): row for row in source_rows
            }

            selected_assertion = None
            selected_canonical = None
            for assertion in assertion_rows:
                if assertion.get("source_program_key", "") != "depaul":
                    continue
                canonical_id = assertion.get("canonical_game_id", "")
                canonical = canonical_by_id.get(canonical_id)
                if (
                    not canonical
                    or assertion_counts[canonical_id] != 1
                    or not assertion.get("source_game_id", "")
                    or assertion.get("source_game_id", "") not in source_by_id
                    or not assertion.get("game_date", "")
                    or canonical.get("site_type", "") in {"", "UNKNOWN"}
                ):
                    continue
                try:
                    source_site, _ = ingest_school.source_site_to_canonical(assertion)
                except (KeyError, ValueError):
                    continue
                if source_site != canonical.get("site_type", ""):
                    continue
                selected_assertion = assertion
                selected_canonical = canonical
                break

            self.assertIsNotNone(selected_assertion)
            self.assertIsNotNone(selected_canonical)
            assertion = selected_assertion
            canonical = selected_canonical
            source = source_by_id[assertion["source_game_id"]]

            game_day = date.fromisoformat(assertion["game_date"])
            old_end = (game_day - timedelta(days=1)).isoformat()
            game_date = game_day.isoformat()

            for row in (assertion, source):
                row["curated_venue_name"] = VENUE_NAME
                row["city"] = CITY
                row["state"] = STATE

            canonical["venue_key"] = NEW_KEY
            canonical["venue_id"] = NEW_ID
            canonical["site_city"] = CITY
            canonical["site_state"] = STATE
            original_notes = canonical.get("notes", "")
            marker = registry_fallback_marker(
                "depaul",
                assertion["source_game_id"],
                NEW_KEY,
                canonical["site_type"],
                ["venue_key", "venue_id", "site_city", "site_state"],
            )
            canonical["notes"] = append_note(original_notes, marker)

            def blank_row(fields):
                return {field: "" for field in fields}

            for venue_id, venue_key in ((OLD_ID, OLD_KEY), (NEW_ID, NEW_KEY)):
                row = blank_row(global_venue_fields)
                row.update(
                    {
                        "venue_id": venue_id,
                        "venue_key": venue_key,
                        "display_name": VENUE_NAME,
                        "city": CITY,
                        "state": STATE,
                        "opened": "1900",
                        "closed": "",
                        "date_precision": "YEAR",
                        "identity_status": "RESEARCHED_SPLIT",
                        "source_basis": "Integrated validate_data fixture",
                        "notes": "Two physical identities intentionally share one exact textual name.",
                    }
                )
                global_venue_rows.append(row)

                school_row = blank_row(school_venue_fields)
                school_row.update(
                    {
                        "source_program_key": "depaul",
                        "venue_key": venue_key,
                        "venue_id": venue_id,
                        "canonical_name": VENUE_NAME,
                        "city": CITY,
                        "state": STATE,
                        "known_opened": "1900",
                        "venue_date_precision": "YEAR",
                        "games_currently_assigned": "1",
                        "relationship_type": "GAME_SITE",
                        "site_rule": "Fixture venue identity does not establish H/A/N.",
                        "source_basis": "Integrated validate_data fixture",
                        "notes": "No local assignment window; naming-period authority must disambiguate.",
                    }
                )
                school_venue_rows.append(school_row)

            def name_row(venue_id, valid_from, valid_to):
                row = blank_row(venue_name_fields)
                row.update(
                    {
                        "venue_id": venue_id,
                        "venue_name": VENUE_NAME,
                        "normalized_name": "fixturesharedarena",
                        "name_type": "PROJECT_DISPLAY",
                        "valid_from": valid_from,
                        "valid_to": valid_to,
                        "date_precision": "EXACT" if valid_from or valid_to else "",
                        "source_basis": "Integrated validate_data fixture",
                        "notes": (
                            "Synthetic dated exact-name authority."
                            if valid_from or valid_to
                            else "Synthetic undated display identity only."
                        ),
                    }
                )
                return row

            unique_periods = [
                name_row(OLD_ID, "1900-01-01", old_end),
                name_row(NEW_ID, game_date, "2099-12-31"),
            ]

            def install_name_rows(rows):
                retained = [
                    row
                    for row in venue_name_rows
                    if row.get("venue_id", "") not in {OLD_ID, NEW_ID}
                ]
                write_csv(venue_names_path, venue_name_fields, retained + rows)

            write_csv(canonical_path, canonical_fields, canonical_rows)
            write_csv(assertions_path, assertion_fields, assertion_rows)
            write_csv(source_path, source_fields, source_rows)
            write_csv(school_venues_path, school_venue_fields, school_venue_rows)
            write_csv(global_venues_path, global_venue_fields, global_venue_rows)
            install_name_rows(unique_periods)

            global_by_id = {
                row["venue_id"]: row for row in global_venue_rows if row.get("venue_id")
            }
            metadata = ingest_school.load_venue_metadata_map_with_name_periods(
                repo,
                school_venues_path,
                global_by_id,
            )
            resolved = ingest_school.resolve_venue_metadata(assertion, metadata)
            self.assertEqual(resolved["venue_key"], NEW_KEY)
            self.assertEqual(resolved["venue_id"], NEW_ID)

            code, output = self.run_validate(repo)
            self.assertEqual(code, 0, output)

            # Transition/overlap: both exact-name periods cover the game date.
            install_name_rows(
                [
                    name_row(OLD_ID, "1900-01-01", game_date),
                    name_row(NEW_ID, game_date, "2099-12-31"),
                ]
            )
            code, output = self.run_validate(repo)
            self.assertNotEqual(code, 0)
            self.assertIn("registry fallback marker venue identity cannot be resolved date-safely", output)

            # Incomplete authority: one competing physical identity has no dated
            # exact-name period, so the resolver must not infer from geography.
            install_name_rows(
                [
                    name_row(OLD_ID, "", ""),
                    name_row(NEW_ID, game_date, "2099-12-31"),
                ]
            )
            code, output = self.run_validate(repo)
            self.assertNotEqual(code, 0)
            self.assertIn("registry fallback marker venue identity cannot be resolved date-safely", output)

            # Restore unique periods, then prove malformed fallback provenance
            # remains an integrated repository-validation failure.
            install_name_rows(unique_periods)
            canonical["notes"] = append_note(
                original_notes,
                (
                    "[VENUE_REGISTRY_FALLBACK "
                    f"source=depaul/{assertion['source_game_id']};"
                    f"venue_key={NEW_KEY};site_type={canonical['site_type']}]"
                ),
            )
            write_csv(canonical_path, canonical_fields, canonical_rows)
            code, output = self.run_validate(repo)
            self.assertNotEqual(code, 0)
            self.assertIn("malformed VENUE_REGISTRY_FALLBACK marker", output)

    @staticmethod
    def run_validate(repo: Path):
        output = io.StringIO()
        with patch.object(sys, "argv", ["validate_data.py", str(repo)]):
            with redirect_stdout(output):
                code = validate_data.main()
        return code, output.getvalue()


if __name__ == "__main__":
    unittest.main()
