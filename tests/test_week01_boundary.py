from copy import deepcopy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from week01_review import load
from week01_boundary import controlled_read

class BoundaryDecisions(unittest.TestCase):
    def setUp(self):
        data = load()
        self.fixtures = {f["fixture_id"]: deepcopy(f) for f in data["fixtures"]}
        self.orders = {o["order_id"]: deepcopy(o) for o in data["authoritative_synthetic_orders"]}
    def test_preserves_owner_read_and_minimizes_fields(self):
        result = controlled_read(self.fixtures["A01"], self.orders)
        self.assertEqual(result["response"], {"order_id": "order-a", "status": "packed"})
    def test_forged_tenant_and_admin_claim_cannot_allow_cross_tenant(self):
        result = controlled_read(self.fixtures["P01"], self.orders)
        self.assertEqual((result["decision"], result["reason"]), ("deny", "tenant_mismatch"))
    def test_same_tenant_other_owner_denied(self):
        self.assertEqual(controlled_read(self.fixtures["A02"], self.orders)["reason"], "owner_mismatch")
    def test_agent_approval_cannot_replace_missing_context(self):
        self.assertEqual(controlled_read(self.fixtures["P02"], self.orders)["reason"], "missing_trusted_context")
    def test_user_supplied_context_is_not_read_as_authority(self):
        fixture = self.fixtures["P02"]
        fixture["request"]["trusted_context"] = self.fixtures["A01"]["trusted_context"]
        self.assertEqual(controlled_read(fixture, self.orders)["reason"], "missing_trusted_context")
    def test_missing_subject_permission_stays_denied_with_admin_text(self):
        fixture = self.fixtures["A01"]
        fixture["trusted_context"]["subject_permissions"] = []
        self.assertEqual(controlled_read(fixture, self.orders)["reason"], "subject_permission_missing")
    def test_service_scope_limits_delegation(self):
        fixture = self.fixtures["A01"]
        fixture["trusted_context"]["service_permissions"] = []
        self.assertEqual(controlled_read(fixture, self.orders)["reason"], "service_permission_missing")
    def test_unsupported_mutation_is_denied(self):
        fixture = self.fixtures["A01"]
        fixture["agent_proposal"]["action"] = "execute_refund"
        self.assertEqual(controlled_read(fixture, self.orders)["reason"], "unsupported_action")
    def test_unknown_object_is_not_returned(self):
        fixture = self.fixtures["A01"]
        fixture["agent_proposal"]["order_id"] = "not-an-order"
        self.assertEqual(controlled_read(fixture, self.orders)["reason"], "object_unavailable")
    def test_invalid_object_reference_denied(self):
        fixture = self.fixtures["A01"]
        fixture["agent_proposal"]["order_id"] = ["order-a"]
        self.assertEqual(controlled_read(fixture, self.orders)["reason"], "invalid_object_reference")
    def test_missing_tenant_denied(self):
        fixture = self.fixtures["A01"]
        del fixture["trusted_context"]["tenant_id"]
        self.assertEqual(controlled_read(fixture, self.orders)["reason"], "invalid_subject_context")
    def test_malformed_resource_does_not_leak_data(self):
        self.orders["order-a"]["status"] = None
        self.assertEqual(controlled_read(self.fixtures["A01"], self.orders)["reason"], "invalid_resource_record")

if __name__ == "__main__":
    unittest.main()
