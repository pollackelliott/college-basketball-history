#!/usr/bin/env python3
import base64
import gzip
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from remote_implementation_io import Stop, decode_research_transport  # noqa: E402


class RemoteImplementationResearchTransportTests(unittest.TestCase):
    def test_plain_base64_transport_preserves_exact_bytes(self):
        original = b"exact immutable research zip bytes"
        encoded = base64.b64encode(original)
        self.assertEqual(
            decode_research_transport(encoded, "git_base64_parts"),
            original,
        )

    def test_gzip_base64_transport_preserves_exact_bytes(self):
        original = (b"source-game-row,venue,opponent\n" * 1000) + b"EOF"
        encoded = base64.b64encode(gzip.compress(original, mtime=0))
        self.assertEqual(
            decode_research_transport(encoded, "git_gzip_base64_parts"),
            original,
        )

    def test_gzip_transport_rejects_non_gzip_payload(self):
        encoded = base64.b64encode(b"not-gzip")
        with self.assertRaisesRegex(Stop, "RESEARCH_CHECKPOINT_GZIP_INVALID"):
            decode_research_transport(encoded, "git_gzip_base64_parts")


if __name__ == "__main__":
    unittest.main()
