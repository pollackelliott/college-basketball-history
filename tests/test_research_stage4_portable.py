import json
import tempfile
import unittest
from pathlib import Path

import research_stage4_portable as mod


class ResearchStage4PortableTests(unittest.TestCase):
    def test_build_and_verify_exact_tool_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            tools = repo / "tools"
            tools.mkdir(parents=True)

            for name, body in {
                "research_stage4.py": "print('author')\n",
                "research_stage4_closeout.py": "print('closeout')\n",
                "research_stage4_portable.py": "print('portable')\n",
                "onboarding_hardening.py": "print('hardening')\n",
                "other_helper.py": "print('helper')\n",
            }.items():
                (tools / name).write_text(
                    body,
                    encoding="utf-8",
                )

            output = root / "bundle"
            sha = "a" * 40
            built = mod.build(repo, output, sha)

            self.assertEqual(
                built["protected_main_sha"],
                sha,
            )
            self.assertEqual(len(built["files"]), 5)

            result = mod.verify(output, sha)
            self.assertEqual(result["status"], "COMPLETE")
            self.assertEqual(result["defects"], [])

            manifest = json.loads(
                (output / mod.MANIFEST).read_text(
                    encoding="utf-8"
                )
            )
            self.assertEqual(
                {
                    item["path"]
                    for item in manifest["files"]
                },
                {
                    "tools/research_stage4.py",
                    "tools/research_stage4_closeout.py",
                    "tools/research_stage4_portable.py",
                    "tools/onboarding_hardening.py",
                    "tools/other_helper.py",
                },
            )

    def test_verify_rejects_tampered_bundle(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            repo = root / "repo"
            tools = repo / "tools"
            tools.mkdir(parents=True)

            for name in mod.REQUIRED_FIXED:
                path = repo / name
                path.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )
                path.write_text(
                    name + "\n",
                    encoding="utf-8",
                )

            output = root / "bundle"
            sha = "b" * 40
            mod.build(repo, output, sha)
            (
                output
                / "tools"
                / "research_stage4_closeout.py"
            ).write_text(
                "tampered\n",
                encoding="utf-8",
            )

            result = mod.verify(output, sha)
            self.assertEqual(result["status"], "INVALID")
            self.assertTrue(
                any(
                    defect["reason"]
                    == "SNAPSHOT_FILE_HASH_MISMATCH"
                    for defect in result["defects"]
                )
            )


if __name__ == "__main__":
    unittest.main()
