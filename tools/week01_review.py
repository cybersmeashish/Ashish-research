"""Run the original four bounded, in-process review specimens. Standard library only."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import platform
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
WEEK = ROOT / "weeks/01-system-and-asset-inventory"
CLASSES = {"PUBLIC", "INTERNAL", "CONFIDENTIAL", "RESTRICTED"}

def load():
    data = json.loads((WEEK / "review-fixtures.json").read_text())
    ids = [f["fixture_id"] for f in data["fixtures"]]
    if len(ids) != 4 or set(ids) != {"P01", "P02", "A01", "A02"}:
        raise ValueError("The experiment requires the four distinct published fixtures")
    return data

def missing_class(asset):
    return asset.get("classification") not in CLASSES

def flow_documented(flow):
    return bool(flow and flow.get("purpose") and flow.get("data_fields")
                and flow.get("data_classification") in CLASSES
                and flow.get("proposed_owner_role") and flow.get("contract_ref"))

def run_fixture(fixture, orders):
    """Execute local functions; the trace records actual local dispatch, never network traffic."""
    trace = []
    diagnostic = []
    decision_events = []
    def hop(source, destination, fields):
        trace.append({"source": source, "destination": destination, "data_fields": fields,
                      "basis": "observed in-process function dispatch"})
    def portal():
        hop("A01", "A02", sorted(fixture["request"]))
        return order_api()
    def order_api():
        hop("A02", "A04", ["order_id", "user_message"])
        result = mock_agent()
        if fixture["baseline_mode"] != "unavailable-backend":
            hop("A02", "A10", ["fixture_id", "order_id", "decision", "reason"])
            decision_events.append({k: result[k] for k in ("decision", "reason")})
        return result
    def mock_agent():
        proposal = dict(fixture["agent_proposal"])
        mode = fixture["baseline_mode"]
        if mode == "unavailable-backend":
            return {"decision": "unknown", "reason": "backend_evidence_unavailable",
                    "response": None}
        if mode == "legacy-direct-store":
            hop("A04", "A06", ["order_id", "client_tenant_claim"])
            order = orders.get(proposal["order_id"])
            if not order or order["tenant_id"] != fixture["request"].get("tenant_id"):
                return {"decision": "deny", "reason": "legacy_tenant_claim_mismatch", "response": None}
            hop("A06", "A11", sorted(order))
            diagnostic.append(dict(order))
            return {"decision": "allow", "reason": "legacy_trusted_client_tenant",
                    "response": dict(order)}
        if mode != "scoped-reference":
            raise ValueError("Unknown specimen mode")
        hop("A04", "A05", sorted(proposal))
        return gateway(proposal)
    def gateway(proposal):
        context = fixture["trusted_context"]
        order = orders.get(proposal["order_id"])
        if not context or not order:
            return {"decision": "deny", "reason": "missing_context_or_object", "response": None}
        if order["tenant_id"] != context["tenant_id"]:
            return {"decision": "deny", "reason": "tenant_mismatch", "response": None}
        if order["owner_id"] != context["subject_id"]:
            return {"decision": "deny", "reason": "owner_mismatch", "response": None}
        hop("A05", "A02", ["action", "order_id"])
        return dispatch_order_api(order)
    def dispatch_order_api(order):
        context = fixture["trusted_context"]
        if (order["tenant_id"], order["owner_id"]) != (context["tenant_id"], context["subject_id"]):
            return {"decision": "deny", "reason": "dispatch_scope_mismatch", "response": None}
        hop("A02", "A06", ["order_id"])
        return {"decision": "allow", "reason": "subject_tenant_owner_match",
                "response": {k: order[k] for k in ("order_id", "status")}}
    result = portal()
    order = orders.get(fixture["agent_proposal"]["order_id"])
    context = fixture["trusted_context"]
    if result["decision"] == "unknown" or context is None:
        evidence_state = "missing_evidence"
    elif result["decision"] == "allow" and (
        not order or (order["tenant_id"], order["owner_id"]) !=
        (context["tenant_id"], context["subject_id"])
    ):
        evidence_state = "confirmed_local_failure"
    else:
        evidence_state = "observed_expected_behavior"
    return {**result, "evidence_state": evidence_state, "trace": trace,
            "diagnostic_copy": diagnostic, "decision_events": decision_events}

def baseline_row(fixture, observation):
    return {
        "fixture_id": fixture["fixture_id"], "fixture_type": fixture["review_label"],
        "procedure_version": "v1-declared-scope",
        "decision": observation["decision"], "reason": observation["reason"],
        "evidence_state": observation["evidence_state"],
        "declared_assets": len(fixture["declared_assets"]),
        "unclassified_assets": sum(missing_class(a) for a in fixture["declared_assets"]),
        "declared_flows": len(fixture["declared_flows"]),
        "undocumented_flows": sum(not flow_documented(f) for f in fixture["declared_flows"]),
        "missing_evidence": "; ".join(fixture["missing_evidence"]),
    }

def write_csv(path, rows):
    with path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

def manifest(paths):
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}

def execute(output):
    data = load()
    orders = {o["order_id"]: o for o in data["authoritative_synthetic_orders"]}
    observations = {f["fixture_id"]: run_fixture(f, orders) for f in data["fixtures"]}
    rows = [baseline_row(f, observations[f["fixture_id"]]) for f in data["fixtures"]]
    output.mkdir(parents=True, exist_ok=True)
    write_csv(output / "baseline-observations.csv", rows)
    report = {
        "procedure": "v1-declared-scope", "executed_at": datetime.now(timezone.utc).isoformat(),
        "runtime": {"python": platform.python_version(), "system": platform.system(),
                    "machine": platform.machine()},
        "execution_scope": "actual in-process Python calls; no HTTP, network or learned model",
        "observations": observations,
    }
    (output / "observations.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "source-manifest.json").write_text(json.dumps(manifest([
        WEEK / "review-fixtures.json", Path(__file__)]), indent=2) + "\n")
    return rows, report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows, _ = execute(args.out)
    print(json.dumps({"fixture_decisions": {r["fixture_id"]: r["decision"] for r in rows},
                      "evidence_states": {r["fixture_id"]: r["evidence_state"] for r in rows}}, indent=2))
