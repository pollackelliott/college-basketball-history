"""Static safety contract for the connector-only request-validation workflow.

The live validator semantics and CAS are covered by
test_remote_implementation_request_submit.py. This test prevents accidental
workflow privilege expansion or bypass of the permanent validator.
"""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/connector-request-validation.yml"


class ConnectorValidationWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text()

    def test_only_template_push_can_trigger(self):
        w = self.workflow
        self.assertIn("push:", w)
        self.assertIn("'request-validation/**'", w)
        self.assertIn("'.remote-implementation/validation-template.json'", w)
        self.assertNotIn("workflow_dispatch:", w)
        self.assertNotIn("pull_request:", w)

    def test_no_write_permission_or_repository_mutation(self):
        w = self.workflow
        self.assertIn("contents: read", w)
        self.assertNotIn("contents: write", w)
        self.assertNotIn("git push", w)
        self.assertNotIn("--submit", w)
        self.assertNotIn("update-ref", w)
        self.assertNotIn("GH_TOKEN:", w)

    def test_protected_main_executes_permanent_validator(self):
        w = self.workflow
        self.assertIn("ref: main", w)
        self.assertIn("persist-credentials: false", w)
        self.assertIn("from remote_implementation_request_submit import", w)
        self.assertIn("prepare_exact_request(", w)
        self.assertIn("fetch_exact_heads(", w)
        self.assertIn("read_control_snapshot(", w)
        self.assertIn("PROTECTED_MAIN_MOVED_DURING_RUNTIME_CHECKOUT", w)
        self.assertIn("AUTHORITATIVE_REFS_MOVED_AFTER_VALIDATION", w)

    def test_exact_request_and_receipt_are_artifacts_not_publications(self):
        w = self.workflow
        self.assertIn('"VALIDATED_NOT_PUBLISHED"', w)
        self.assertIn('"control_state_sha256"', w)
        self.assertIn('"request_sha256"', w)
        self.assertIn('"control_parent_sha"', w)
        self.assertIn('(output / "request.json").write_bytes(raw)', w)
        self.assertIn('uses: actions/upload-artifact@v4', w)
        self.assertIn("retention-days: 7", w)


if __name__ == "__main__":
    unittest.main()
