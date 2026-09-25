import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from onboarding_plan import (  # noqa: E402
    CANONICAL_PATCH_FIELDS,
    WorkflowError,
    _apply_canonical_patch,
)


class CanonicalVenuePairPatchTests(unittest.TestCase):
    def test_patch_schema_allows_explicit_venue_id_and_key_pair(self):
        self.assertIn("venue_key", CANONICAL_PATCH_FIELDS)
        self.assertIn("venue_id", CANONICAL_PATCH_FIELDS)

        canonical = {
            "venue_key": "",
            "venue_id": "",
            "site_type": "NEUTRAL",
            "notes": "",
        }

        retired = _apply_canonical_patch(
            canonical,
            {
                "venue_key": "chicago-stadium",
                "venue_id": "VEN-000044",
            },
            valid_venue_pairs={("VEN-000044", "chicago-stadium")},
        )

        self.assertEqual(retired, 0)
        self.assertEqual(canonical["venue_key"], "chicago-stadium")
        self.assertEqual(canonical["venue_id"], "VEN-000044")

    def test_venue_identity_patch_requires_both_halves(self):
        canonical = {
            "venue_key": "",
            "venue_id": "",
            "site_type": "NEUTRAL",
            "notes": "",
        }

        with self.assertRaisesRegex(
            WorkflowError,
            "provide venue_key and venue_id together",
        ):
            _apply_canonical_patch(
                canonical,
                {"venue_key": "chicago-stadium"},
                valid_venue_pairs={("VEN-000044", "chicago-stadium")},
            )

    def test_venue_identity_patch_must_match_global_registry_pair(self):
        canonical = {
            "venue_key": "",
            "venue_id": "",
            "site_type": "NEUTRAL",
            "notes": "",
        }

        with self.assertRaisesRegex(
            WorkflowError,
            "does not match the global venue registry",
        ):
            _apply_canonical_patch(
                canonical,
                {
                    "venue_key": "chicago-stadium",
                    "venue_id": "VEN-999999",
                },
                valid_venue_pairs={("VEN-000044", "chicago-stadium")},
            )


if __name__ == "__main__":
    unittest.main()
