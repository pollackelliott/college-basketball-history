import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from onboarding_plan import WorkflowError  # noqa: E402
from stage_research_portfolio import rebase_program_aliases  # noqa: E402


def program(key, name, current="Yes"):
    return {
        "program_key": key,
        "program_name": name,
        "display_name": name,
        "current_d1": current,
    }


def alias(key, name, start="", end=""):
    return {
        "program_key": key,
        "alias_name": name,
        "alias_type": "OFFICIAL_HISTORICAL_NAME",
        "effective_start_season": start,
        "effective_end_season": end,
        "verification_status": "VERIFIED",
        "evidence_basis": "fixture",
        "evidence_url": "https://example.test/",
        "notes": "",
    }


def opponent(label, key, name, games="1", first="1945-1946", last="1945-1946"):
    return {
        "source_program_key": "depaul",
        "source_opponent_label": label,
        "canonical_opponent_key": key,
        "canonical_opponent_name": name,
        "current_d1": "TRUE",
        "games_with_source_label": games,
        "first_season": first,
        "last_season": last,
    }


def game(label, key, name):
    return {
        "source_game_id": "D-1",
        "source_program_key": "depaul",
        "season_label": "1945-1946",
        "source_opponent_label": label,
        "normalized_opponent_key": key,
        "normalized_opponent_name": name,
        "raw_text": "W 44-40 Oklahoma A&M",
    }


class ProgramAliasRebaseTests(unittest.TestCase):
    def test_verified_historical_alias_rebases_identity_but_preserves_evidence(self):
        opponents = [opponent("at Oklahoma A&M", "oklahoma-a-m", "Oklahoma A&M")]
        games = [game("at Oklahoma A&M", "oklahoma-a-m", "Oklahoma A&M")]
        raw_before = games[0]["raw_text"]
        label_before = games[0]["source_opponent_label"]

        opponents, games, mappings = rebase_program_aliases(
            [program("oklahoma-state", "Oklahoma State")],
            [alias("oklahoma-state", "Oklahoma A&M")],
            opponents,
            games,
        )

        self.assertEqual(opponents[0]["canonical_opponent_key"], "oklahoma-state")
        self.assertEqual(opponents[0]["canonical_opponent_name"], "Oklahoma State")
        self.assertEqual(games[0]["normalized_opponent_key"], "oklahoma-state")
        self.assertEqual(games[0]["normalized_opponent_name"], "Oklahoma State")
        self.assertEqual(games[0]["source_opponent_label"], label_before)
        self.assertEqual(games[0]["raw_text"], raw_before)
        self.assertEqual(len(mappings), 1)
        self.assertEqual(mappings[0]["source_games_rebased"], 1)

    def test_ambiguous_verified_alias_is_a_stop(self):
        opponents = [opponent("Example", "stale-key", "Shared Historic Name")]
        games = [game("Example", "stale-key", "Shared Historic Name")]
        with self.assertRaisesRegex(WorkflowError, "ambiguous verified program alias"):
            rebase_program_aliases(
                [program("alpha", "Alpha"), program("beta", "Beta")],
                [
                    alias("alpha", "Shared Historic Name"),
                    alias("beta", "Shared Historic Name"),
                ],
                opponents,
                games,
            )

    def test_sibling_school_name_is_not_inferred_without_verified_alias(self):
        opponents = [opponent("Iowa", "iowa", "Iowa")]
        games = [game("Iowa", "iowa", "Iowa")]
        opponents, games, mappings = rebase_program_aliases(
            [program("iowa-state", "Iowa State")],
            [],
            opponents,
            games,
        )
        self.assertEqual(opponents[0]["canonical_opponent_key"], "iowa")
        self.assertEqual(games[0]["normalized_opponent_key"], "iowa")
        self.assertEqual(mappings, [])

    def test_bounded_alias_does_not_apply_outside_its_verified_era(self):
        opponents = [
            opponent(
                "Historic",
                "stale-key",
                "Historic Name",
                first="1960-1961",
                last="1960-1961",
            )
        ]
        games = [game("Historic", "stale-key", "Historic Name")]
        opponents, games, mappings = rebase_program_aliases(
            [program("alpha", "Alpha")],
            [alias("alpha", "Historic Name", start="1940-1941", end="1950-1951")],
            opponents,
            games,
        )
        self.assertEqual(opponents[0]["canonical_opponent_key"], "stale-key")
        self.assertEqual(games[0]["normalized_opponent_key"], "stale-key")
        self.assertEqual(mappings, [])


if __name__ == "__main__":
    unittest.main()
