#!/usr/bin/env python3
"""Immutable George Mason expansion presentation regression.

Pinned immutable inputs are the sealed historical apply G, the reviewed website
fix commit, and the accepted guarded presentation successor C. The regression
never reads mutable pull-request refs. It executes the actual corrected browser
series selector against the real sealed George Mason team JSON and proves that
C is exactly the one-file successor reproduced by the permanent refresh logic.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "tools"))

from remote_implementation_presentation_refresh import (  # noqa: E402
    ASSET_PATH,
    presentation_refresh_tree_plan,
    verify_presentation_successor,
)

SEALED_G = "0fe86b37405bc5322bec5639a28c1819bb97d5f7"
SEALED_G_TREE = "da3081fb1867f9fc8ff82429ebdfd57c9a594918"
REVIEWED_FIX = "fc42631af872e2ae6573efcbb15b93f668360fb2"
GUARDED_C = "9db724322351dc2facdaf2934248b8c34912c3a3"
REVIEWED_SITE_BLOB = "73328a90c7d8b8dc835663ca6226382cd708698e"
SEALED_TEAM_JSON_SHA256 = "8486ca5c4eaddcd22319aa98f11a8b88e8f7998729e279cf6954aa0b2dc2ca0a"
TEAM_JSON = "site/data/teams/george-mason.json"
TEAM = "george-mason"
OPPONENT = "james-madison"


def run(*args: str, input: bytes | None = None) -> bytes:
    return subprocess.run(
        list(args), cwd=REPO, input=input, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, check=True,
    ).stdout


def require(ok: bool, description: str) -> None:
    if not ok:
        raise AssertionError("EXACT_GMU_PRESENTATION_REHEARSAL:" + description)


def git(*args: str) -> str:
    return run("git", *args).decode("utf-8").strip()


def blob(commit: str, path: str) -> bytes:
    return run("git", "show", f"{commit}:{path}")


def selector_from_html(html: str) -> str:
    marker = "function seriesGamesFor(teamKey, opponentKey) {"
    require(html.count(marker) == 1, "SERIES_SELECTOR_NOT_UNIQUE")
    selector = marker + html.split(marker, 1)[1].split("\nfunction ", 1)[0]
    require("DB.games[teamKey]" in selector, "SERIES_SELECTOR_WRONG_DATA_SOURCE")
    require("game.opponentKey === opponentKey" in selector, "SERIES_SELECTOR_WRONG_OPPONENT")
    require("gameInProgramScope" not in selector, "TOP_LEVEL_FILTER_STILL_APPLIED")
    return selector


def browser_series(series_source: str, all_games: list[dict]) -> dict:
    # Execute the EXACT website selector with the live G-generated team JSON,
    # not a rewritten Python approximation or a made-up 102-game fixture.
    browser_rows = [
        {
            "canonicalGameId": row.get("canonical_game_id"),
            "opponentKey": row.get("opponent_key"),
            "season": row.get("season_label"),
            "date": row.get("game_date"),
            "datePrecision": row.get("date_precision"),
            "teamScore": row.get("team_score"),
            "oppScore": row.get("opponent_score"),
            "result": row.get("result"),
            "scoreKnown": row.get("score_known"),
            "site": row.get("site"),
            "venue": row.get("venue_name"),
            "venueId": row.get("venue_id"),
            "venueKey": row.get("venue_key"),
            "location": ",".join(
                filter(None, (row.get("site_city"), row.get("site_state")))
            ),
            "siteCity": row.get("site_city"),
            "siteState": row.get("site_state"),
            "gameType": row.get("game_type"),
            "postseasonRound": row.get("postseason_round"),
            "administrativeStatus": row.get("administrative_status"),
            "administrativeNote": row.get("administrative_note"),
        }
        for row in all_games
    ]
    browser_js = (
        "const fs = require('fs');\n"
        "const rows = JSON.parse(fs.readFileSync(0, 'utf8'));\n"
        "const DB = {teams: {'george-mason': {name: 'George Mason'}}, "
        "games: {'george-mason': rows}};\n"
        "function opponentProfile(_school, _opp) {return {name:'James Madison'};}\n"
        "function oppositeResult(value) {return value==='W'?'L':value==='L'?'W':value;}\n"
        + series_source
        + "\nconst games = seriesGamesFor('george-mason','james-madison');\n"
        "const result = { meetings:games.length, "
        "wins:games.filter(x=>x.results['george-mason']==='W').length, "
        "losses:games.filter(x=>x.results['george-mason']==='L').length, "
        "ties:games.filter(x=>x.results['george-mason']==='T').length, "
        "distinctGames:new Set(games.map(x=>x.canonicalGameId)).size, "
        "early:games.filter(x=>x.season<'1978-1979').length};\n"
        "process.stdout.write(JSON.stringify(result));\n"
    )
    return json.loads(run("node", "-e", browser_js,
                          input=json.dumps(browser_rows).encode()))


def main() -> int:
    require(shutil.which("node") is not None, "NODE_REQUIRED")
    # This is an immutable regression fixture, not a live release locator.
    # A future school PR must never fail because a historical George Mason PR
    # ref moved, closed, or disappeared. The pinned commits themselves are the
    # durable regression authority and must remain in current repository history.
    for commit, label in (
        (SEALED_G, "SEALED_G"),
        (REVIEWED_FIX, "REVIEWED_FIX"),
        (GUARDED_C, "GUARDED_C"),
    ):
        require(git("rev-parse", f"{commit}^{{commit}}") == commit,
                label + "_COMMIT_MISSING")
        require(git("merge-base", commit, "HEAD") == commit,
                label + "_NOT_ANCESTOR_OF_CURRENT_HISTORY")
    require(git("rev-parse", f"{SEALED_G}^{{tree}}") == SEALED_G_TREE,
            "SEALED_HISTORICAL_TREE_CHANGED")
    require(git("rev-parse", f"{GUARDED_C}^") == SEALED_G,
            "GUARDED_C_PARENT_MISMATCH")
    require(git("rev-parse", f"{REVIEWED_FIX}:{ASSET_PATH}")
            == REVIEWED_SITE_BLOB, "ACCEPTED_SITE_BLOB_CHANGED")

    raw_team = blob(SEALED_G, TEAM_JSON)
    require(hashlib.sha256(raw_team).hexdigest() == SEALED_TEAM_JSON_SHA256,
            "SEALED_TEAM_JSON_HASH_MISMATCH")
    doc = json.loads(raw_team)
    games = doc["games"]
    require(isinstance(games, list) and len(games) == 1769,
            "SEALED_PUBLISHED_TEAM_GAME_COUNT")
    jmu_games = [g for g in games if g.get("opponent_key") == OPPONENT]
    require(len(jmu_games) == 102, "SEALED_JMU_EXPECTED_102_GAMES")
    require(len({g["canonical_game_id"] for g in jmu_games}) == 102,
            "SEALED_JMU_CANONICAL_ID_DUPLICATES")
    require(sum(g.get("result") == "W" for g in jmu_games) == 51,
            "SEALED_JMU_WIN_COUNT")
    require(sum(g.get("result") == "L" for g in jmu_games) == 51,
            "SEALED_JMU_LOSS_COUNT")
    require(sum(g.get("season_label", "") < "1978-1979" for g in jmu_games) == 16,
            "PRE_TOP_LEVEL_16_GAMES")
    require(sum(g.get("season_label", "") >= "1978-1979" for g in jmu_games) == 86,
            "TOP_LEVEL_86_GAMES")
    fixed_source = blob(REVIEWED_FIX, ASSET_PATH).decode()
    actual = browser_series(selector_from_html(fixed_source), games)
    require(actual == {
        "meetings": 102, "wins": 51, "losses": 51,
        "ties": 0, "distinctGames": 102, "early": 16,
    }, "FIXED_BROWSER_102_MEETINGS_51_51_MISMATCH:" + str(actual))

    # Reproduce the accepted C tree from immutable G + reviewed website blob,
    # then independently verify the already-merged C commit. No commit is
    # synthesized and no Git identity or mutable PR transport is required.
    plan = presentation_refresh_tree_plan(
        REPO, sealed_commit_sha=SEALED_G, repair_main_sha=REVIEWED_FIX,
        expected_sealed_tree_sha=SEALED_G_TREE,
        expected_asset_blob_sha=REVIEWED_SITE_BLOB,
    )
    require(plan["allowed_changed_paths"] == [ASSET_PATH],
            "CANDIDATE_CHANGE_SCOPE_NOT_SITE_ONLY")
    require(plan["candidate_tree_sha"] == git("rev-parse", f"{GUARDED_C}^{{tree}}"),
            "GUARDED_C_TREE_NOT_REPRODUCED")
    proof = verify_presentation_successor(
        REPO, sealed_commit_sha=SEALED_G, successor_sha=GUARDED_C,
        repair_main_sha=REVIEWED_FIX,
        expected_sealed_tree_sha=SEALED_G_TREE,
        expected_asset_blob_sha=REVIEWED_SITE_BLOB,
    )
    require(proof["fresh_tree_equivalence"] == "PASS"
            and proof["sealed_parent"] == SEALED_G
            and proof["allowed_changed_paths"] == [ASSET_PATH],
            "EXACT_CANDIDATE_NOT_EQUIVALENT")
    require(git("diff", "--name-only", SEALED_G, GUARDED_C)
            == ASSET_PATH, "EXTRA_CANONICAL_OR_SITE_DATA_MUTATION")
    require(git("rev-parse", f"{GUARDED_C}:{TEAM_JSON}")
            == git("rev-parse", f"{SEALED_G}:{TEAM_JSON}"),
            "SEALED_TEAM_JSON_CHANGED_IN_C")
    require(git("rev-parse", f"{GUARDED_C}:{ASSET_PATH}")
            == REVIEWED_SITE_BLOB, "C_WEBSITE_NOT_EXACT_REVIEWED_FIX")
    print(json.dumps({
        "status": "EXACT_GMU_G_TO_C_PRESENTATION_REHEARSAL_PASS",
        "sealed_g": SEALED_G,
        "guarded_c": GUARDED_C,
        "c_tree": plan["candidate_tree_sha"],
        "changed_paths": [ASSET_PATH],
        "sealed_published_games": len(games),
        "jmu_meetings": actual["meetings"],
        "jmu_record": f'{actual["wins"]}-{actual["losses"]}',
        "pre_top_level_games": actual["early"],
        "historical_games_mutated": 0,
        "owner_gate_2_approved": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
