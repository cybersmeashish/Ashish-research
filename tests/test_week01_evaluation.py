from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from week01_review import load
from week01_evaluate import evaluate

class EvidenceExpansion(unittest.TestCase):
    def setUp(self):
        data = load()
        self.fixtures = {f["fixture_id"]: f for f in data["fixtures"]}
        self.orders = {o["order_id"]: o for o in data["authoritative_synthetic_orders"]}
    def test_trace_exposes_uninventoried_diagnostic_and_undocumented_bypass(self):
        row, detail = evaluate(self.fixtures["P01"], self.orders)
        self.assertEqual(row["unclassified_asset_ids"], "A11")
        self.assertEqual(row["undocumented_observed_local_flows"], 2)
        self.assertEqual(row["undocumented_configuration_only_flows"], 0)
        self.assertEqual(row["proposed_control_decision"], "deny")
        self.assertEqual(detail["original"]["decision"], "allow")
    def test_configured_targets_remain_candidates_not_executed_traffic(self):
        row, detail = evaluate(self.fixtures["P02"], self.orders)
        self.assertEqual(row["unclassified_asset_ids"], "A06;A12")
        self.assertEqual(row["undocumented_configuration_only_flows"], 2)
        self.assertEqual(row["undocumented_observed_local_flows"], 0)
        self.assertEqual(row["original_backend_decidable"], "no")
        self.assertEqual(row["original_evidence_state"], "missing_evidence")
        self.assertEqual(row["proposed_control_decision"], "deny")
        for flow in detail["expanded_flows"]:
            if flow["destination"] in ("A06", "A12"):
                self.assertNotIn("observed_local", flow["origins"])
    def test_acceptable_cases_keep_declared_scope_and_expected_behavior(self):
        for key, decision in (("A01", "allow"), ("A02", "deny")):
            with self.subTest(key=key):
                row, _ = evaluate(self.fixtures[key], self.orders)
                self.assertEqual(row["identified_assets"], row["baseline_assets"])
                self.assertEqual(row["unclassified_assets"], 0)
                self.assertEqual(row["undocumented_flows"], 0)
                self.assertEqual(row["proposed_control_decision"], decision)
    def test_missing_flow_owner_is_missing_documentation_not_automatic_safe_zero(self):
        from copy import deepcopy
        fixture = deepcopy(self.fixtures["A01"])
        fixture["declared_flows"][0]["proposed_owner_role"] = None
        row, _ = evaluate(fixture, self.orders)
        self.assertEqual(row["undocumented_flows"], 1)
        self.assertEqual(row["proposed_control_decision"], "allow")

if __name__ == "__main__":
    unittest.main()
