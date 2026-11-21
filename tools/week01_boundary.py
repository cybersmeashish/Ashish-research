"""Proposed read-only boundary; separately supplied trusted fixtures, not real authentication."""
from __future__ import annotations

def authorize(proposal, context, orders):
    if not isinstance(context, dict) or context.get("origin") != "server-fixture":
        return {"decision": "deny", "reason": "missing_trusted_context", "response": None}
    if not all(isinstance(context.get(k), str) and context[k] for k in ("subject_id", "tenant_id")):
        return {"decision": "deny", "reason": "invalid_subject_context", "response": None}
    if not isinstance(proposal, dict) or proposal.get("action") != "read_order":
        return {"decision": "deny", "reason": "unsupported_action", "response": None}
    if not isinstance(proposal.get("order_id"), str) or not proposal["order_id"]:
        return {"decision": "deny", "reason": "invalid_object_reference", "response": None}
    if (not isinstance(context.get("subject_permissions"), list)
            or "read_order:own" not in context["subject_permissions"]):
        return {"decision": "deny", "reason": "subject_permission_missing", "response": None}
    if (not isinstance(context.get("service_permissions"), list)
            or "read_order" not in context["service_permissions"]):
        return {"decision": "deny", "reason": "service_permission_missing", "response": None}
    order = orders.get(proposal["order_id"])
    if not isinstance(order, dict):
        return {"decision": "deny", "reason": "object_unavailable", "response": None}
    if order.get("tenant_id") != context["tenant_id"]:
        return {"decision": "deny", "reason": "tenant_mismatch", "response": None}
    if order.get("owner_id") != context["subject_id"]:
        return {"decision": "deny", "reason": "owner_mismatch", "response": None}
    if not isinstance(order.get("status"), str):
        return {"decision": "deny", "reason": "invalid_resource_record", "response": None}
    return {"decision": "allow", "reason": "subject_tenant_owner_match",
            "response": {"order_id": proposal["order_id"], "status": order["status"]}}

def controlled_read(fixture, orders):
    # The agent proposal stays separate from server-supplied identity/permissions.
    gateway = authorize(fixture["agent_proposal"], fixture["trusted_context"], orders)
    if gateway["decision"] != "allow":
        return gateway
    # Recheck at the order-API dispatch boundary in this single-threaded mock.
    return authorize(fixture["agent_proposal"], fixture["trusted_context"], orders)
