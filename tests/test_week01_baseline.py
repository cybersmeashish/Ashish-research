from copy import deepcopy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from week01_review import load, run_fixture

class BaselineObservations(unittest.TestCase):
    def setUp(self):
        data = load()
        self.fixtures = {f["fixture_id"]: f for f in data["fixtures"]}
        self.orders = {o["order_id"]: o for o in data["authoritative_synthetic_orders"]}
    def observe(self, key):
        return run_fixture(deepcopy(self.fixtures[key]), deepcopy(self.orders))
    def test_own_order_remains_available_despite_forged_client_claims(self):
        result = self.observe("A01")
        self.assertEqual(result["response"], {"order_id": "order-a", "status": "packed"})
        self.assertEqual(result["evidence_state"], "observed_expected_behavior")
    def test_same_tenant_other_owner_is_denied(self):
        self.assertIn("order-a2", self.orders)
        result = self.observe("A02")
        self.assertEqual((result["decision"], result["reason"]), ("deny", "owner_mismatch"))
        self.assertIsNone(result["response"])
    def test_legacy_read_actually_returns_other_tenant_record(self):
        result = self.observe("P01")
        self.assertEqual(result["response"]["tenant_id"], "tenant-beta")
        self.assertEqual(result["evidence_state"], "confirmed_local_failure")
    def test_extra_copy_and_bypass_are_actual_local_calls(self):
        result = self.observe("P01")
        pairs = {(h["source"], h["destination"]) for h in result["trace"]}
        self.assertIn(("A04", "A06"), pairs)
        self.assertIn(("A06", "A11"), pairs)
        self.assertNotIn(("A04", "A05"), pairs)
        self.assertEqual(result["diagnostic_copy"][0]["order_id"], "order-b")
    def test_unavailable_backend_is_unknown_not_a_failure_or_pass(self):
        result = self.observe("P02")
        self.assertEqual((result["decision"], result["evidence_state"]), ("unknown", "missing_evidence"))
        self.assertIsNone(result["response"])
        self.assertNotIn("A06", {h["destination"] for h in result["trace"]})
    def test_reference_denies_cross_tenant_without_changing_object_existence(self):
        fixture = deepcopy(self.fixtures["A01"])
        fixture["agent_proposal"]["order_id"] = "order-b"
        result = run_fixture(fixture, self.orders)
        self.assertEqual(result["reason"], "tenant_mismatch")

if __name__ == "__main__":
    unittest.main()
