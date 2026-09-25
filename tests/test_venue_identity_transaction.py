import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import venue_identity_transaction as transaction  # noqa: E402


def write_csv(path: Path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class VenueIdentityTransactionTests(unittest.TestCase):
    def make_repo(self):
        temporary = tempfile.TemporaryDirectory()
        repo = Path(temporary.name)

        venue_fields = [
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
        ]
        write_csv(
            repo / "data/reference/venues.csv",
            venue_fields,
            [
                {
                    "venue_id": "VEN-000001",
                    "venue_key": "survivor",
                    "display_name": "Test Arena",
                    "city": "Test City",
                    "state": "TX",
                    "opened": "",
                    "closed": "",
                    "date_precision": "",
                    "identity_status": "CURATED_SEED",
                    "source_basis": "survivor evidence",
                    "notes": "",
                },
                {
                    "venue_id": "VEN-000002",
                    "venue_key": "duplicate",
                    "display_name": "Test Arena (City)",
                    "city": "Test City",
                    "state": "TX",
                    "opened": "",
                    "closed": "",
                    "date_precision": "",
                    "identity_status": "RESEARCHED",
                    "source_basis": "duplicate evidence",
                    "notes": "",
                },
            ],
        )
        name_fields = [
            "venue_id",
            "venue_name",
            "normalized_name",
            "name_type",
            "valid_from",
            "valid_to",
            "date_precision",
            "source_basis",
            "notes",
        ]
        write_csv(
            repo / "data/reference/venue-names.csv",
            name_fields,
            [
                {
                    "venue_id": "VEN-000001",
                    "venue_name": "Test Arena",
                    "normalized_name": "testarena",
                    "name_type": "PROJECT_DISPLAY",
                    "valid_from": "",
                    "valid_to": "",
                    "date_precision": "",
                    "source_basis": "survivor evidence",
                    "notes": "",
                },
                {
                    "venue_id": "VEN-000002",
                    "venue_name": "Test Arena (City)",
                    "normalized_name": "testarenacity",
                    "name_type": "PROJECT_DISPLAY",
                    "valid_from": "",
                    "valid_to": "",
                    "date_precision": "",
                    "source_basis": "duplicate evidence",
                    "notes": "",
                },
            ],
        )
        write_csv(
            repo / "data/canonical/games.csv",
            [
                "canonical_game_id",
                "venue_key",
                "venue_id",
                "site_city",
                "site_state",
                "notes",
            ],
            [
                {
                    "canonical_game_id": "G1",
                    "venue_key": "duplicate",
                    "venue_id": "VEN-000002",
                    "site_city": "Test City",
                    "site_state": "TX",
                    "notes": (
                        "[VENUE_REGISTRY_FALLBACK "
                        "source=test/S1;venue_key=duplicate;"
                        "site_type=NEUTRAL;fields=venue_id,venue_key]"
                    ),
                }
            ],
        )
        write_csv(
            repo / "data/evidence/game-assertions.csv",
            [
                "assertion_id",
                "canonical_game_id",
                "source_program_key",
                "source_game_id",
                "game_date",
                "curated_venue_name",
            ],
            [
                {
                    "assertion_id": "A1",
                    "canonical_game_id": "G1",
                    "source_program_key": "test",
                    "source_game_id": "S1",
                    "game_date": "2000-01-01",
                    "curated_venue_name": "Test Arena (City)",
                }
            ],
        )
        write_csv(
            repo / "schools/test/venues.csv",
            [
                "source_program_key",
                "venue_key",
                "venue_id",
                "canonical_name",
                "aliases",
                "city",
                "state",
                "notes",
            ],
            [
                {
                    "source_program_key": "test",
                    "venue_key": "duplicate",
                    "venue_id": "VEN-000002",
                    "canonical_name": "Test Arena (City)",
                    "aliases": "",
                    "city": "Test City",
                    "state": "TX",
                    "notes": "",
                }
            ],
        )
        spec = repo / "data/reconciliation/venue-identity-maintenance/test.json"
        spec.parent.mkdir(parents=True, exist_ok=True)
        spec.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "merges": [
                        {
                            "survivor_venue_id": "VEN-000001",
                            "absorbed_venue_id": "VEN-000002",
                            "expected_canonical_rows": 1,
                            "expected_school_rows": 1,
                            "resolution_basis": "fixture duplicate physical identity",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return temporary, repo, spec

    def test_plan_and_apply_merge_duplicate_identity_transactionally(self):
        temporary, repo, spec = self.make_repo()
        self.addCleanup(temporary.cleanup)

        plan = transaction.build_plan(repo, spec)
        self.assertEqual(plan["blockers"], [])
        self.assertEqual(plan["merges"][0]["canonical_rows"], 1)
        self.assertEqual(plan["merges"][0]["school_rows"], 1)
        self.assertEqual(plan["merges"][0]["provenance_markers"], 1)

        result = transaction.apply_transaction(
            repo,
            spec,
            plan["plan_sha256"],
            run_validation=False,
        )
        self.assertEqual(result["venues_retired"], 1)
        self.assertEqual(result["canonical_rows_updated"], 1)
        self.assertEqual(result["provenance_markers_updated"], 1)
        self.assertEqual(result["school_rows_updated"], 1)
        self.assertEqual(result["site_files_refreshed"], 0)

        venues = read_rows(repo / "data/reference/venues.csv")
        self.assertEqual([row["venue_id"] for row in venues], ["VEN-000001"])
        self.assertIn("VEN-000002 retired", venues[0]["notes"])

        canonical = read_rows(repo / "data/canonical/games.csv")
        self.assertEqual(canonical[0]["venue_id"], "VEN-000001")
        self.assertEqual(canonical[0]["venue_key"], "survivor")
        self.assertIn(";venue_key=survivor;", canonical[0]["notes"])
        self.assertNotIn(";venue_key=duplicate;", canonical[0]["notes"])

        school = read_rows(repo / "schools/test/venues.csv")
        self.assertEqual(school[0]["venue_id"], "VEN-000001")
        self.assertEqual(school[0]["venue_key"], "survivor")

        names = read_rows(repo / "data/reference/venue-names.csv")
        self.assertFalse(any(row["venue_id"] == "VEN-000002" for row in names))
        displays = [
            row
            for row in names
            if row["venue_id"] == "VEN-000001"
            and row["name_type"] == "PROJECT_DISPLAY"
        ]
        self.assertEqual(len(displays), 1)
        self.assertTrue(
            any(
                row["venue_name"] == "Test Arena (City)"
                and row["name_type"] == "HISTORICAL_OR_ALIAS"
                for row in names
            )
        )

    def test_site_refresh_applies_generated_data_before_freshness_check(self):
        calls = []

        class Result:
            returncode = 0

        def fake_run(command, cwd):
            calls.append((command, cwd))
            return Result()

        repo = Path("/tmp/venue-transaction-regression")

        with patch.object(transaction.subprocess, "run", side_effect=fake_run):
            transaction._run_site_refresh(repo)

        self.assertEqual(
            calls[0][0],
            [sys.executable, "tools/build_site_data.py", "--apply"],
        )
        self.assertEqual(
            calls[1][0],
            [sys.executable, "tools/check_site_data_freshness.py"],
        )
        self.assertEqual(calls[0][1], repo)
        self.assertEqual(calls[1][1], repo)

    def test_site_refresh_failure_rolls_back_reference_and_generated_state(self):
        temporary, repo, spec = self.make_repo()
        self.addCleanup(temporary.cleanup)

        generated = repo / "site/data/teams/test.json"
        generated.parent.mkdir(parents=True, exist_ok=True)
        generated.write_text('{"state":"before"}\n', encoding="utf-8")

        plan = transaction.build_plan(repo, spec)

        def fail_refresh(repo_arg):
            target = repo_arg / "site/data/teams/test.json"
            target.write_text('{"state":"after"}\n', encoding="utf-8")
            extra = repo_arg / "site/data/teams/new.json"
            extra.write_text('{"state":"new"}\n', encoding="utf-8")
            raise transaction.TransactionError("synthetic refresh failure")

        with (
            patch.object(transaction, "_run_validation"),
            patch.object(transaction, "_run_site_refresh", side_effect=fail_refresh),
        ):
            with self.assertRaises(transaction.TransactionError):
                transaction.apply_transaction(
                    repo,
                    spec,
                    plan["plan_sha256"],
                    run_validation=True,
                )

        venues = read_rows(repo / "data/reference/venues.csv")
        self.assertEqual(
            [row["venue_id"] for row in venues],
            ["VEN-000001", "VEN-000002"],
        )
        self.assertEqual(
            generated.read_text(encoding="utf-8"),
            '{"state":"before"}\n',
        )
        self.assertFalse((repo / "site/data/teams/new.json").exists())

    def test_site_refresh_is_counted_inside_transaction(self):
        temporary, repo, spec = self.make_repo()
        self.addCleanup(temporary.cleanup)

        generated = repo / "site/data/teams/test.json"
        generated.parent.mkdir(parents=True, exist_ok=True)
        generated.write_text('{"state":"before"}\n', encoding="utf-8")

        plan = transaction.build_plan(repo, spec)

        def refresh(repo_arg):
            (repo_arg / "site/data/teams/test.json").write_text(
                '{"state":"after"}\n',
                encoding="utf-8",
            )

        with (
            patch.object(transaction, "_run_validation"),
            patch.object(transaction, "_run_site_refresh", side_effect=refresh),
        ):
            result = transaction.apply_transaction(
                repo,
                spec,
                plan["plan_sha256"],
                run_validation=True,
            )

        self.assertEqual(result["site_files_refreshed"], 1)
        self.assertEqual(
            generated.read_text(encoding="utf-8"),
            '{"state":"after"}\n',
        )

    def test_expected_count_mismatch_blocks_plan(self):
        temporary, repo, spec = self.make_repo()
        self.addCleanup(temporary.cleanup)
        doc = json.loads(spec.read_text(encoding="utf-8"))
        doc["merges"][0]["expected_canonical_rows"] = 2
        spec.write_text(json.dumps(doc), encoding="utf-8")

        plan = transaction.build_plan(repo, spec)

        self.assertEqual(len(plan["blockers"]), 1)
        self.assertIn("expected 2, found 1", plan["blockers"][0])


if __name__ == "__main__":
    unittest.main()
