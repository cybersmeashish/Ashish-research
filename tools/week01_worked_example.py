"""Execute the P01 before/after decision using unchanged inputs."""
import json
from week01_review import load, run_fixture
from week01_boundary import controlled_read

def example():
    data = load()
    fixture = next(f for f in data["fixtures"] if f["fixture_id"] == "P01")
    orders = {o["order_id"]: o for o in data["authoritative_synthetic_orders"]}
    before = run_fixture(fixture, orders)
    after = controlled_read(fixture, orders)
    return {
        "fixture_id": fixture["fixture_id"],
        "trusted_subject": fixture["trusted_context"]["subject_id"],
        "trusted_tenant": fixture["trusted_context"]["tenant_id"],
        "client_tenant_claim": fixture["request"]["tenant_id"],
        "requested_order": fixture["agent_proposal"]["order_id"],
        "before": {k: before[k] for k in ("decision", "reason", "response", "evidence_state")},
        "proposed_control": after,
        "scope": "same synthetic input; actual local calls; no deployed enforcement claim",
    }

if __name__ == "__main__":
    print(json.dumps(example(), indent=2))
