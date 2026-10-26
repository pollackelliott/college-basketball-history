"""Regression: future-effective conference membership appears without future games."""

import csv
import json
import shutil
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site" / "index.html").read_text(encoding="utf-8")
START = "function projectCurrentConferenceHistory(history, team, referenceSeason) {"
END = "\nfunction normalizeProgram(program) {"
assert SITE.count(START) == 1 and SITE.count(END) == 1
PROJECTOR = START + SITE.split(START, 1)[1].split(END, 1)[0]

RUNNER = (
    PROJECTOR
    + '\nconst input = JSON.parse(require("fs").readFileSync(0, "utf8"));\n'
    + "process.stdout.write(JSON.stringify(input.map((x) => "
    + "projectCurrentConferenceHistory(x.history, x.team, x.season))));\n"
)


def read_rows(path):
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def project(cases):
    completed = subprocess.run(
        ["node", "-e", RUNNER],
        input=json.dumps(cases),
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(completed.stdout)


def current_team(row):
    return {
        "currentConferenceKey": row["conference_key"],
        "currentConferenceName": row["conference_name"],
    }


@unittest.skipUnless(shutil.which("node"), "Node.js required for actual site JavaScript tests")
class CurrentConferenceHistoryProjectionTests(unittest.TestCase):
    def test_all_published_school_timelines_reconcile_with_current_reference(self):
        manifest = json.loads((ROOT / "site/data/manifest.json").read_text())
        season = manifest["reference_season"]
        memberships = {
            row["program_key"]: row
            for row in read_rows(ROOT / "data/reference/conference-membership.csv")
            if row["season_label"] == season
        }
        published = [
            row["program_key"]
            for row in read_rows(ROOT / "data/reference/programs.csv")
            if row["public_page_enabled"] == "Yes"
        ]
        self.assertGreater(len(published), 0)
        cases = []
        for key in published:
            self.assertIn(key, memberships)
            path = ROOT / "schools" / key / "conferences.csv"
            self.assertTrue(path.exists(), key)
            cases.append(
                {"history": read_rows(path), "team": current_team(memberships[key]), "season": season}
            )

        results = project(cases)
        self.assertEqual(len(results), len(published))
        for key, case, result in zip(published, cases, results):
            with self.subTest(school=key):
                self.assertGreater(len(result), 0)
                matching = [
                    era for era in result
                    if era["start_season"] <= season
                    and (not era["end_season"] or era["end_season"] >= season)
                ]
                self.assertEqual(len(matching), 1)
                self.assertEqual(
                    matching[0]["conference_key"], case["team"]["currentConferenceKey"]
                )
                self.assertIsNone(matching[0].get("end_season") or None)
                # Projection never alters the authoritative source chronology.
                if len(result) > len(case["history"]):
                    self.assertEqual(result[:-2], case["history"][:-1])
                    self.assertEqual(result[-2]["end_season"], "2025-2026")

    def test_boise_and_washington_state_show_2026_pac12_without_games(self):
        membership = {
            row["program_key"]: row
            for row in read_rows(ROOT / "data/reference/conference-membership.csv")
        }
        schools = ("boise-state", "washington-state")
        cases = [
            {
                "history": read_rows(ROOT / "schools" / key / "conferences.csv"),
                "team": current_team(membership[key]),
                "season": "2026-2027",
            }
            for key in schools
        ]
        result = project(cases)
        for key, timeline in zip(schools, result):
            with self.subTest(school=key):
                self.assertEqual(timeline[-1]["start_season"], "2026-2027")
                self.assertEqual(timeline[-1]["conference_key"], "pac-12")
                self.assertFalse(timeline[-1]["end_season"])
                self.assertEqual(timeline[-2]["end_season"], "2025-2026")

    def test_existing_oregon_state_future_era_not_duplicated(self):
        history = read_rows(ROOT / "schools/oregon-state/conferences.csv")
        team = {"currentConferenceKey": "pac-12", "currentConferenceName": "Pac-12"}
        self.assertEqual(
            project([{"history": history, "team": team, "season": "2026-2027"}])[0],
            history,
        )

    def test_maac_metro_and_wac_uac_rebrands_are_distinct_eras(self):
        cases = [
            {
                "history": [{"start_season": "1990-1991", "end_season": "",
                             "conference_key": "maac", "conference_name": "MAAC"}],
                "team": {"currentConferenceKey": "metro",
                         "currentConferenceName": "Metro"},
                "season": "2026-2027",
            },
            {
                "history": [{"start_season": "2005-2006", "end_season": "",
                             "conference_key": "wac", "conference_name": "WAC"}],
                "team": {"currentConferenceKey": "united-athletic",
                         "currentConferenceName": "United Athletic"},
                "season": "2026-2027",
            },
        ]
        for before, after in zip(cases, project(cases)):
            self.assertEqual(len(after), 2)
            self.assertEqual(after[0]["conference_key"], before["history"][0]["conference_key"])
            self.assertEqual(after[0]["end_season"], "2025-2026")
            self.assertEqual(after[1]["conference_key"], before["team"]["currentConferenceKey"])
            self.assertEqual(after[1]["start_season"], "2026-2027")
            self.assertIsNone(after[1]["end_season"])
            self.assertEqual(before["history"][0]["end_season"], "")

    def test_unchanged_membership_does_not_split_arizona_era(self):
        history = read_rows(ROOT / "schools/arizona/conferences.csv")
        team = {"currentConferenceKey": "big-12", "currentConferenceName": "Big 12"}
        self.assertEqual(
            project([{"history": history, "team": team, "season": "2026-2027"}])[0],
            history,
        )

    def test_unexplained_gap_is_not_silently_filled(self):
        history = [{"start_season": "2000-2001", "end_season": "2023-2024",
                    "conference_key": "old", "conference_name": "Old"}]
        team = {"currentConferenceKey": "new", "currentConferenceName": "New"}
        self.assertEqual(
            project([{"history": history, "team": team, "season": "2026-2027"}])[0],
            history,
        )

    def test_full_2026_transition_cohort_and_rebrands_are_registered(self):
        current = {
            row["program_key"]: row["conference_key"]
            for row in read_rows(ROOT / "data/reference/conference-membership.csv")
            if row["season_label"] == "2026-2027"
        }
        movers = {
            "austin-peay": "united-athletic", "boise-state": "pac-12",
            "california-baptist": "big-west", "central-arkansas": "united-athletic",
            "colorado-state": "pac-12", "denver": "wcc",
            "eastern-kentucky": "united-athletic", "fresno-state": "pac-12",
            "gonzaga": "pac-12", "hawai-i": "mountain-west",
            "little-rock": "united-athletic", "louisiana-tech": "sun-belt",
            "north-alabama": "united-athletic", "northern-illinois": "horizon",
            "oregon-state": "pac-12", "sacramento-state": "big-west",
            "san-diego-state": "pac-12", "southern-utah": "big-sky",
            "tennessee-tech": "southern", "texas-state": "pac-12",
            "uc-davis": "mountain-west", "utep": "mountain-west",
            "utah-state": "pac-12", "utah-tech": "big-sky",
            "utah-valley": "big-west", "washington-state": "pac-12",
            "west-florida": "atlantic-sun", "west-georgia": "united-athletic",
        }
        self.assertEqual(len(movers), 28)
        for key, conference in movers.items():
            with self.subTest(school=key):
                self.assertEqual(current.get(key), conference)

        metro = [key for key, conference in current.items() if conference == "metro"]
        self.assertEqual(len(metro), 13)
        registry = {r["conference_key"]: r for r in read_rows(ROOT / "data/reference/conferences.csv")}
        for historical, new in (("maac", "metro"), ("wac", "united-athletic")):
            self.assertEqual(registry[historical]["status"], "historical")
            self.assertEqual(registry[new]["status"], "current")

    def test_live_data_uses_projected_history_for_both_display_and_lookups(self):
        self.assertIn("DB.referenceSeason = manifest.reference_season", SITE)
        self.assertIn("currentConferenceKey: program.current_conference?.conference_key", SITE)
        self.assertIn("DB.conferenceHistory[key] = projectCurrentConferenceHistory(", SITE)
        self.assertIn("const history = DB.conferenceHistory[key] || [];", SITE)


if __name__ == "__main__":
    unittest.main()
