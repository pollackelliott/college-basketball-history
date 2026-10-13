"""Regression tests for the sealed non-merge venue structural transaction."""
import csv
import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "venue_structural_transaction.py"
if not TOOL.exists():
    TOOL = Path("/tmp/venue_structural_transaction.py")
spec = importlib.util.spec_from_file_location("venue_structural_transaction", TOOL)
transaction = importlib.util.module_from_spec(spec)
spec.loader.exec_module(transaction)


def write_csv(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class VenueStructuralTransactionTests(unittest.TestCase):
    def make_repo(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)

        venue_fields = [
            "venue_id", "venue_key", "display_name", "city", "state", "opened",
            "closed", "date_precision", "identity_status", "source_basis", "notes",
        ]
        name_fields = [
            "venue_id", "venue_name", "normalized_name", "name_type", "valid_from",
            "valid_to", "date_precision", "source_basis", "notes",
        ]
        blank_venue = dict.fromkeys(venue_fields, "")
        blank_name = dict.fromkeys(name_fields, "")
        write_csv(root / "data/reference/venues.csv", venue_fields, [
            blank_venue | {"venue_id": "VEN-000001", "venue_key": "wrong-key", "display_name": "Wrong Name", "city": "Town", "state": "IL"},
            blank_venue | {"venue_id": "VEN-000002", "venue_key": "other", "display_name": "Other", "city": "Else", "state": "IL"},
        ])
        write_csv(root / "data/reference/venue-names.csv", name_fields, [
            blank_name | {"venue_id": "VEN-000001", "venue_name": "Wrong Name", "normalized_name": "wrongname", "name_type": "PROJECT_DISPLAY"},
            blank_name | {"venue_id": "VEN-000001", "venue_name": "Bad Alias", "normalized_name": "badalias", "name_type": "HISTORICAL_OR_ALIAS"},
            blank_name | {"venue_id": "VEN-000002", "venue_name": "Other", "normalized_name": "other", "name_type": "PROJECT_DISPLAY"},
        ])
        write_csv(root / "data/canonical/games.csv", ["canonical_game_id", "venue_id", "venue_key"], [
            {"canonical_game_id": "G1", "venue_id": "VEN-000001", "venue_key": "wrong-key"}
        ])
        write_csv(root / "data/evidence/game-assertions.csv", ["id", "venue_id", "venue_key"], [])
        write_csv(root / "data/evidence/ncaa-tournament-sites.csv", ["canonical_game_id", "venue_id", "venue_key"], [])
        school_fields = [
            "source_program_key", "venue_key", "venue_id", "canonical_name", "aliases",
            "city", "state", "games_currently_assigned", "first_assigned_game", "last_assigned_game",
        ]
        write_csv(root / "schools/test/venues.csv", school_fields, [
            {"source_program_key": "test", "venue_key": "wrong-key", "venue_id": "VEN-000001", "canonical_name": "Wrong Name", "aliases": "Bad Alias;Keep", "city": "Town", "state": "IL", "games_currently_assigned": "2", "first_assigned_game": "2000-01-01", "last_assigned_game": "2000-01-02"}
        ])
        source_fields = ["source_game_id", "curated_site_type", "curated_venue_name", "city", "state", "game_date", "raw_text"]
        write_csv(root / "schools/test/source-games.csv", source_fields, [
            {"source_game_id": "S1", "curated_site_type": "SOURCE_PROGRAM_HOME", "curated_venue_name": "Wrong Name", "city": "Town", "state": "IL", "game_date": "2000-01-01", "raw_text": "normal"},
            {"source_game_id": "S2", "curated_site_type": "SOURCE_PROGRAM_HOME", "curated_venue_name": "Wrong Name", "city": "Town", "state": "IL", "game_date": "2000-01-02", "raw_text": "(C)"},
        ])
        (root / "site/data").mkdir(parents=True)
        (root / "site/data/x.json").write_text("{}\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()

        spec_doc = {
            "schema_version": 1,
            "expected_base_sha": base,
            "venue_updates": [{
                "venue_id": "VEN-000001",
                "expected": {"venue_key": "wrong-key", "display_name": "Wrong Name"},
                "set": {"venue_key": "right-key", "display_name": "Right Name"},
                "expected_canonical_rows": 1,
                "expected_assertion_rows": 0,
                "expected_ncaa_rows": 0,
            }],
            "venue_additions": [{
                "require_next_numeric_id": True,
                "row": blank_venue | {"venue_id": "VEN-000003", "venue_key": "new", "display_name": "New", "city": "Town", "state": "IL"},
            }],
            "venue_name_updates": [{
                "match": {"eq": {"venue_id": "VEN-000001", "name_type": "PROJECT_DISPLAY"}},
                "expected_count": 1,
                "set": {"venue_name": "Right Name", "normalized_name": "rightname"},
            }],
            "venue_name_deletes": [{
                "match": {"eq": {"venue_id": "VEN-000001", "venue_name": "Bad Alias"}},
                "expected_count": 1,
            }],
            "venue_name_additions": [{
                "row": blank_name | {"venue_id": "VEN-000003", "venue_name": "New", "normalized_name": "new", "name_type": "PROJECT_DISPLAY"},
            }],
            "school_venue_updates": [{
                "path": "schools/test/venues.csv",
                "match": {"eq": {"venue_id": "VEN-000001"}},
                "expected_count": 1,
                "set": {"venue_key": "right-key", "canonical_name": "Right Name"},
                "remove_aliases": ["Bad Alias"],
            }],
            "source_game_rules": [
                {"path": "schools/test/source-games.csv", "description": "C rows", "match": {"eq": {"curated_site_type": "SOURCE_PROGRAM_HOME"}, "regex": {"raw_text": "\\(C\\)"}}, "expected_count": 1, "set": {"curated_venue_name": "Other", "city": "Else", "state": "IL"}},
                {"path": "schools/test/source-games.csv", "description": "non-C rows", "match": {"eq": {"curated_site_type": "SOURCE_PROGRAM_HOME"}, "not_regex": {"raw_text": "\\(C\\)"}}, "expected_count": 1, "set": {"curated_venue_name": "Right Name", "city": "Town", "state": "IL"}},
            ],
            "postconditions": [{"path": "schools/test/source-games.csv", "match": {"eq": {"curated_venue_name": "Other"}}, "expected_count": 1}],
            "allowed_changed_paths": ["data/reference/*.csv", "data/canonical/games.csv", "schools/test/*.csv", "site/data/*.json"],
        }
        spec_path = root / "spec.json"
        spec_path.write_text(json.dumps(spec_doc), encoding="utf-8")
        return temp, root, spec_path, spec_doc

    def test_plan_and_apply_exact_transaction(self):
        temp, root, spec_path, _ = self.make_repo()
        self.addCleanup(temp.cleanup)
        plan = transaction.build_plan(root, spec_path)
        self.assertEqual(plan["blockers"], [])
        result = transaction.apply_transaction(root, spec_path, plan["plan_sha256"], run_checks=False)
        self.assertEqual(result["source_game_updates"], 2)
        venues = {r["venue_id"]: r for r in read_rows(root / "data/reference/venues.csv")}
        self.assertEqual(venues["VEN-000001"]["venue_key"], "right-key")
        self.assertIn("VEN-000003", venues)
        self.assertEqual(read_rows(root / "data/canonical/games.csv")[0]["venue_key"], "right-key")
        self.assertEqual(read_rows(root / "schools/test/venues.csv")[0]["aliases"], "Keep")
        games = read_rows(root / "schools/test/source-games.csv")
        self.assertEqual([g["curated_venue_name"] for g in games], ["Right Name", "Other"])

    def test_overlapping_source_rules_are_blockers(self):
        temp, root, spec_path, spec_doc = self.make_repo()
        self.addCleanup(temp.cleanup)
        spec_doc["source_game_rules"][1]["match"] = {"eq": {"curated_site_type": "SOURCE_PROGRAM_HOME"}}
        spec_doc["source_game_rules"][1]["expected_count"] = 2
        spec_path.write_text(json.dumps(spec_doc), encoding="utf-8")
        plan = transaction.build_plan(root, spec_path)
        self.assertTrue(any("overlaps" in item for item in plan["blockers"]))

    def test_failed_postcondition_rolls_back_source_state(self):
        temp, root, spec_path, spec_doc = self.make_repo()
        self.addCleanup(temp.cleanup)
        before = (root / "data/reference/venues.csv").read_bytes()
        spec_doc["postconditions"] = [{"path": "data/reference/venues.csv", "match": {"eq": {"venue_id": "DOES-NOT-EXIST"}}, "expected_count": 1}]
        spec_path.write_text(json.dumps(spec_doc), encoding="utf-8")
        plan = transaction.build_plan(root, spec_path)
        self.assertEqual(plan["blockers"], [])
        with self.assertRaises(transaction.TransactionError):
            transaction.apply_transaction(root, spec_path, plan["plan_sha256"], run_checks=False)
        self.assertEqual((root / "data/reference/venues.csv").read_bytes(), before)


if __name__ == "__main__":
    unittest.main()