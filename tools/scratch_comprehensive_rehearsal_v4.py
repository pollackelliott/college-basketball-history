#!/usr/bin/env python3
import csv
import hashlib
import json
import subprocess
import sys
from pathlib import Path

BASE = "25d4e02ea492ad2af96f4ae40822431db7ecc50a"
SEAL = "25b8eacc467760c27cabb061e533ced45ba0f3a3a467a22f13852cd56a2e4151"


def rows(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def projection_hash(paths, mutable):
    digest = hashlib.sha256()
    for path in sorted(paths, key=str):
        for row in rows(path):
            payload = [(key, row.get(key, "")) for key in row if key not in mutable]
            digest.update((str(path) + "|" + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n").encode())
    return digest.hexdigest()


def run(cmd, cwd, *, capture=False):
    print("+", " ".join(cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd, check=True, text=True, capture_output=capture)


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: scratch_comprehensive_rehearsal_v4.py REPO ARTIFACT_DIR")
    repo = Path(sys.argv[1]).resolve()
    artifact = Path(sys.argv[2]).resolve()
    plan = json.loads((artifact / "plan-a.json").read_text())
    assert plan["plan_sha256"] == SEAL
    assert plan["git_head"] == BASE
    assert plan["blockers"] == []
    assert (
        plan["affected_canonical_game_count"],
        len(plan["remap_only_canonical_game_ids"]),
        len(plan["canonical_pairs"]),
        len(plan["absorbed_canonical_game_ids"]),
        len(plan["retained_distinct_canonical_game_ids"]),
        len(plan["new_discrepancies"]),
        len(plan["venue_registry_additions"]),
        len(plan["venue_name_additions"]),
    ) == (434, 376, 58, 58, 2, 5, 1, 1)

    pre = {
        "canonical": len(rows(repo / "data/canonical/games.csv")),
        "assertions": len(rows(repo / "data/evidence/game-assertions.csv")),
        "discrepancies": len(rows(repo / "data/reconciliation/discrepancies.csv")),
        "venues": len(rows(repo / "data/reference/venues.csv")),
        "venue_names": len(rows(repo / "data/reference/venue-names.csv")),
        "source_immutable": projection_hash(repo.glob("schools/*/source-games.csv"), {"normalized_opponent_key", "opponent_current_d1"}),
        "assertion_immutable": projection_hash([repo / "data/evidence/game-assertions.csv"], {"canonical_game_id", "normalized_opponent_key"}),
        "opponent_immutable": projection_hash(repo.glob("schools/*/opponents.csv"), {"canonical_opponent_key", "canonical_opponent_name", "current_d1"}),
    }
    assert (pre["canonical"], pre["assertions"], pre["discrepancies"], pre["venues"]) == (67583, 89815, 2152, 368)
    print("PRE_COUNTS", json.dumps(pre, sort_keys=True))

    run([
        "python", "tools/opponent_identity_bulk_transaction.py", "apply",
        str(artifact / "manifest.csv"), str(artifact / "resolutions.json"),
        "--expected-plan-sha256", SEAL, "--apply"
    ], repo)

    canonical = rows(repo / "data/canonical/games.csv")
    assertions = rows(repo / "data/evidence/game-assertions.csv")
    discrepancies = rows(repo / "data/reconciliation/discrepancies.csv")
    venues = rows(repo / "data/reference/venues.csv")
    venue_names = rows(repo / "data/reference/venue-names.csv")
    assert (len(canonical), len(assertions), len(discrepancies), len(venues), len(venue_names)) == (
        67525, 89815, 2157, 369, pre["venue_names"] + 1
    )
    assert projection_hash(repo.glob("schools/*/source-games.csv"), {"normalized_opponent_key", "opponent_current_d1"}) == pre["source_immutable"]
    assert projection_hash([repo / "data/evidence/game-assertions.csv"], {"canonical_game_id", "normalized_opponent_key"}) == pre["assertion_immutable"]
    assert projection_hash(repo.glob("schools/*/opponents.csv"), {"canonical_opponent_key", "canonical_opponent_name", "current_d1"}) == pre["opponent_immutable"]

    old_keys = set(plan["global_key_map"])
    by_id = {row["canonical_game_id"]: row for row in canonical}
    assert not any(row["team_a_key"] in old_keys or row["team_b_key"] in old_keys for row in canonical)
    assert not any(row.get("normalized_opponent_key", "") in old_keys for row in assertions)
    for path in repo.glob("schools/*/source-games.csv"):
        assert not any(row.get("normalized_opponent_key", "") in old_keys for row in rows(path)), path
    for path in repo.glob("schools/*/opponents.csv"):
        assert not any(row.get("canonical_opponent_key", "") in old_keys for row in rows(path)), path

    absorbed = set(plan["absorbed_canonical_game_ids"])
    assert len(absorbed) == 58 and absorbed.isdisjoint(by_id)
    assert not any(row["canonical_game_id"] in absorbed for row in assertions)
    for pair in plan["canonical_pairs"]:
        row = by_id[pair["survivor_canonical_game_id"]]
        for field, value in pair["final_canonical_values"].items():
            assert row.get(field, "") == str(value), (pair["survivor_canonical_game_id"], field, row.get(field, ""), value)

    for game_id in ("CBBG-0065455", "CBBG-0065459"):
        assert game_id in by_id and "sam-houston" in {by_id[game_id]["team_a_key"], by_id[game_id]["team_b_key"]}
    tam_rows = rows(repo / "schools/texas-a-m/source-games.csv")
    sam = [row for row in tam_rows if row.get("source_opponent_label") == "Sam Houston NC"]
    assert len(sam) == 13 and all(row.get("normalized_opponent_key") == "sam-houston" for row in sam)

    ohio = by_id["CBBG-0046360"]
    assert (
        ohio["site_type"], ohio["designated_home_team_key"], ohio["venue_key"], ohio["venue_id"], ohio["site_city"], ohio["site_state"]
    ) == ("NEUTRAL", "", "eugenio-guerra-sports-complex", "VEN-000371", "Bayamón", "PR")
    venue = [row for row in venues if row["venue_id"] == "VEN-000371"]
    assert len(venue) == 1 and venue[0]["venue_key"] == "eugenio-guerra-sports-complex"
    name = [row for row in venue_names if row["venue_id"] == "VEN-000371"]
    assert len(name) == 1 and (name[0]["venue_name"], name[0]["normalized_name"], name[0]["name_type"]) == (
        "Eugenio Guerra Sports Complex", "eugenioguerrasportscomplex", "PROJECT_DISPLAY"
    )

    new_ids = {row["discrepancy_id"] for row in plan["new_discrepancies"]}
    found = [row for row in discrepancies if row["discrepancy_id"] in new_ids]
    assert len(found) == 5 and {row["discrepancy_id"] for row in found} == new_ids and all(row["status"] == "RESOLVED" for row in found)
    print("ACCOUNTING_PASS affected=434 in_place=376 absorbed=58 retained_distinct=2 discrepancies=5 venue_additions=1 venue_name_additions=1")

    run(["python", "tools/validate_data.py"], repo)
    run(["python", "tools/build_site_data.py"], repo)
    run(["python", "tools/check_site_data_freshness.py"], repo)
    run(["python", "-m", "unittest", "discover", "-s", "tests", "-v"], repo)
    census = run(["python", "tools/published_opponent_identity_census.py", "--json"], repo, capture=True)
    census_json = json.loads(census.stdout)
    assert census_json["priority_counts"]["P0"] == 0, census_json["priority_counts"]
    print("P0_OPPONENT_IDENTITY_FINDINGS=0")
    run(["python", "tools/published_site_completeness_census.py", "--json"], repo, capture=True)

    changed = run(["git", "diff", "--name-only"], repo, capture=True).stdout.splitlines()
    print("CHANGED_PATH_COUNT=" + str(len(changed)))
    for path in changed:
        print(path)
    print("REHEARSAL_V4_PASS")


if __name__ == "__main__":
    main()
