"""Website-only synthetic Non-D1 display and exact sealed Hawai‘i rehearsal.

This test never changes historical memberships, canonical games or public JSON.
It constructs the G + one-site-file candidate inside a disposable Git index.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = (ROOT / "site/index.html").read_text(encoding="utf-8")
SEALED_G = "0730d706a3084cbcd4647584052ad61ace040eb2"
SEALED_TEAM_SHA256 = "c005a41b133be141c7a9116580304a37d6bfcb7a111c515acefd1ea27a268b67"

START = "function conferenceTimelineDisplayHistory(history) {"
DISPLAY_START = "function conferenceTimelineDisplayName(key, membership) {"
MARKUP_END = "\nfunction teamView(key) {"
PROJECT_START = "function projectCurrentConferenceHistory(history, team, referenceSeason) {"
PROJECT_END = "\nfunction normalizeProgram(program) {"
assert SITE.count(START) == SITE.count(DISPLAY_START) == SITE.count(MARKUP_END) == 1
assert SITE.count(PROJECT_START) == SITE.count(PROJECT_END) == 1
TIMELINE = SITE[SITE.index(START):SITE.index(MARKUP_END)]
PROJECTOR = SITE[SITE.index(PROJECT_START):SITE.index(PROJECT_END)]
NEW_LOOKUP = "  const displayHistory = conferenceTimelineDisplayHistory(history);"
OLD_LOOKUP = "  const history = DB.conferenceHistory[key] || [];"
assert SITE.count(NEW_LOOKUP) == 1

JS = (
    'const cases = JSON.parse(require("fs").readFileSync(0, "utf8"));\n'
    'const DB = {teams: {test: {primary: "#116644"}}, '
    'conferenceHistory: {}, conferenceNames: {}};\n'
    'function displayConferenceName(key, name) {return name || key || "Conference";}\n'
    'function esc(x) {return String(x ?? "");}\n'
    + PROJECTOR + "\n" + TIMELINE + "\n"
    + 'const output = cases.map(item => {\n'
    + '  const source = item.history;\n'
    + '  const original = JSON.stringify(source);\n'
    + '  const history = item.project ? projectCurrentConferenceHistory(source, '
      '{currentConferenceKey: "mountain-west", '
      'currentConferenceName: "Mountain West"}, "2026-2027") : source;\n'
    + '  DB.conferenceHistory.test = history;\n'
    + '  const displayed = conferenceTimelineDisplayHistory(history);\n'
    + '  const markup = conferenceHistoryMarkup("test");\n'
    + '  return {displayed, markup, unchanged: JSON.stringify(source) === original};\n'
    + '});\n'
    + 'process.stdout.write(JSON.stringify(output));\n'
)


def synthetic(start, end):
    return {
        "start_season": start, "end_season": end,
        "conference_key": "", "conference_name": "Non-D1",
        "membership_type": "classification",
        "classification": "NON_D1_CLASSIFICATION",
    }


def affiliated(key, name, start, end):
    return {
        "start_season": start, "end_season": end,
        "conference_key": key, "conference_name": name,
        "membership_type": "conference",
    }


def render(cases):
    result = subprocess.run(
        ["node", "-e", JS], input=json.dumps(cases), text=True,
        capture_output=True, check=True,
    )
    return json.loads(result.stdout)


def git(*args, input=None, env=None):
    return subprocess.run(
        ["git", "-C", str(ROOT), *args], input=input,
        capture_output=True, check=True, env=env,
    ).stdout


@unittest.skipUnless(shutil.which("node"), "Node.js is required to execute the real site JS")
class SyntheticNonD1TimelineTests(unittest.TestCase):
    def test_world_war_ii_hiatus_is_one_display_era_on_desktop_and_mobile(self):
        source = [
            synthetic("1921-1922", "1941-1942"),
            synthetic("1946-1947", "1969-1970"),
            affiliated("independent", "Independent", "1970-1971", "1978-1979"),
        ]
        result = render([{"history": source}])[0]
        self.assertTrue(result["unchanged"])
        self.assertEqual(source[0]["end_season"], "1941-1942")
        self.assertEqual(len(result["displayed"]), 2)
        self.assertEqual(result["displayed"][0]["start_season"], "1921-1922")
        self.assertEqual(result["displayed"][0]["end_season"], "1969-1970")
        self.assertEqual(
            result["markup"].count('<div class="conference-era-name">Non-D1</div>'), 1
        )
        self.assertEqual(
            result["markup"].count('<div class="conference-era-mobile-name">Non-D1</div>'), 1
        )
        for markup_class in ("conference-era-seasons", "conference-era-mobile-seasons"):
            self.assertIn(f'<div class="{markup_class}">1921-1970</div>', result["markup"])
        self.assertNotIn("1921-1942", result["markup"])
        self.assertNotIn("1946-1970", result["markup"])
        self.assertIn("Independent", result["markup"])

    def test_real_affiliations_and_renaming_boundaries_are_not_collapsed(self):
        prior = synthetic("1921-1922", "1941-1942")
        later = synthetic("1946-1947", "1969-1970")
        cases = [
            [prior, affiliated("independent", "Independent", "1942-1943", "1945-1946"), later],
            [prior, affiliated("wac", "WAC", "1942-1943", "1945-1946"), later],
            [prior, {**later, "classification": "OTHER_CLASSIFICATION"}],
            [prior, {**later, "membership_type": "conference"}],
            [prior, {**later, "conference_key": "some-real-conference"}],
            [prior, {**later, "conference_name": "Different historical category"}],
            [prior, {**later, "start_season": "1940-1941"}],
            [prior, {**later, "start_season": ""}],
            [
                affiliated("midwestern-city", "Midwestern City Conference",
                           "1980-1981", "1981-1982"),
                affiliated("midwestern-collegiate", "Midwestern Collegiate Conference",
                           "1982-1983", "1983-1984"),
            ],
        ]
        for case, result in zip(cases, render([{"history": x} for x in cases])):
            with self.subTest(history=case):
                self.assertTrue(result["unchanged"])
                self.assertEqual(result["displayed"], case)
        self.assertEqual(
            render([{"history": [prior, later]}])[0]["displayed"][0]["end_season"],
            "1969-1970",
        )

    def test_exact_sealed_hawaii_public_json_and_one_file_successor_tree(self):
        # The exact sealed G is fetched by full-depth GitHub PR CI. Fail closed
        # if this immutable public JSON is missing rather than testing invented data.
        if subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-e", f"{SEALED_G}^{{commit}}"],
            capture_output=True,
        ).returncode:
            self.skipTest("sealed Hawai‘i G object is not present in this isolated replay")
        raw = git("show", f"{SEALED_G}:site/data/teams/hawai-i.json")
        self.assertEqual(hashlib.sha256(raw).hexdigest(), SEALED_TEAM_SHA256)
        document = json.loads(raw)
        source = document["conference_history"]
        pre_d1 = [x for x in source if x.get("classification") == "NON_D1_CLASSIFICATION"]
        self.assertEqual(
            [(x["start_season"], x["end_season"]) for x in pre_d1],
            [("1921-1922", "1941-1942"), ("1946-1947", "1969-1970")],
        )
        rendered = render([{"history": source, "project": True}])[0]
        self.assertTrue(rendered["unchanged"])
        self.assertEqual(len(rendered["displayed"]), len(source))
        self.assertEqual(
            [(x["start_season"], x["end_season"]) for x in
             rendered["displayed"] if x.get("classification") == "NON_D1_CLASSIFICATION"],
            [("1921-1922", "1969-1970")],
        )
        for name_class in ("conference-era-name", "conference-era-mobile-name"):
            self.assertEqual(
                rendered["markup"].count(f'<div class="{name_class}">Non-D1</div>'), 1,
            )
        self.assertIn("1921-1970", rendered["markup"])
        for name in ("Independent", "Big West", "Mountain West"):
            self.assertIn(name, rendered["markup"])
        self.assertEqual(
            [row["conference_key"] for row in rendered["displayed"]
             if row.get("conference_key") == "wac"], ["wac"],
        )

        # Reconstruct G+C from actual G index/tree, no school-ref write,
        # and prove the changed path population is only site/index.html.
        original_site = git("show", f"{SEALED_G}:site/index.html").decode("utf-8")
        merge_begin = SITE.index("// Consecutive synthetic Non-D1 blocks describe one classification era, even")
        merge_end = SITE.index(DISPLAY_START)
        insertion = SITE[merge_begin:merge_end]
        restored = SITE.replace(insertion, "", 1).replace(
            "  const displayHistory = conferenceTimelineDisplayHistory(history);\n", "", 1
        ).replace(
            "conferenceTimelineDisplayNames(key, displayHistory)",
            "conferenceTimelineDisplayNames(key, history)", 1
        ).replace(
            "const desktop = displayHistory.map(",
            "const desktop = history.map(", 1
        ).replace(
            "const mobile = displayHistory.map(",
            "const mobile = history.map(", 1
        )
        self.assertEqual(restored, original_site)

        with tempfile.TemporaryDirectory(prefix="hawaii-site-gc-") as tmp:
            env = dict(os.environ, GIT_INDEX_FILE=str(Path(tmp) / "candidate-index"))
            git("read-tree", SEALED_G, env=env)
            blob = git("hash-object", "-w", "--stdin",
                       input=SITE.encode("utf-8")).decode().strip()
            git("update-index", "--add", "--cacheinfo",
                f"100644,{blob},site/index.html", env=env)
            candidate_tree = git("write-tree", env=env).decode().strip()
            paths = git("diff-tree", "-r", "--name-only",
                        SEALED_G, candidate_tree).decode().splitlines()
            self.assertEqual(paths, ["site/index.html"])
            self.assertEqual(
                git("show", f"{candidate_tree}:site/data/teams/hawai-i.json"), raw,
            )


if __name__ == "__main__":
    unittest.main()
