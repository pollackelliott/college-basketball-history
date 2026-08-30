import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTES = ROOT / "schools/mississippi-state/source-notes.md"
MARKER = "## Retroactive HOME-site remediation (2026-08-30)"


class MississippiStateSourceNotesRemediationTests(unittest.TestCase):
    def test_remediation_note_is_unique_and_has_clean_eof(self):
        text = NOTES.read_text(encoding="utf-8")
        self.assertEqual(text.count(MARKER), 1)
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith("\n\n"))


if __name__ == "__main__":
    unittest.main()
