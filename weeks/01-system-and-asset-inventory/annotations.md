# Four reusable order-boundary review fixtures

**Contribution 002 · Scheduled 19 November 2026 · Synthetic review fixtures**

The [fixture set](review-fixtures.json) narrows the [day-one scope](scope-and-evidence.md) to a customer portal, order API, mocked agent, gateway, order store and decision buffer. These retain the original asset identifiers. All people, orders, roles and classifications are invented.

“Acceptable” means the particular local read/deny behavior is acceptable for the stated boundary. It is not an assessment of the whole application.

| Fixture | Type | What the reviewer should observe | What remains missing |
|---|---|---|---|
| P01 | Problematic | A tenant value from the client reaches a direct-store path; the synthetic wrong-tenant record can be returned. Inspect the extra diagnostic copy and the bypass of gateway/API authorization. | Ownership/classification for the extra buffer; approved flow contracts; real deployed controls |
| P02 | Problematic | Configuration names an order tool and export helper outside its inventory. The agent claims administrator authority, but no backend execution or delegated subject is available. | Backend decision/access trace, trusted subject, grants, asset classifications and flow contracts |
| A01 | Acceptable | The originating customer reads their own order. Forged client tenant/role and agent role claims do not alter the trusted customer context. | Real authentication and delegation, network/storage controls and accepted owners |
| A02 | Acceptable | The other customer's order exists in the same tenant but is denied. An administrator claim in agent text does not grant access. | The same real deployment evidence; revocation and concurrent mutation behavior |

## Reuse and data dictionary

- `declared_assets`: proposed inventory, class labels and fictional accountable roles.
- `declared_flows`: intended request/decision flows, including data fields, purpose, owner and contract reference.
- `request` and `agent_proposal`: **untrusted** content, including order identifiers and role/tenant claims.
- `trusted_context`: separately supplied **server-fixture** data. It stands in for verified context; no token validation is implemented.
- `baseline_mode`: which bounded in-process specimen to exercise. It is not a description of a real service.
- `configuration_candidates`: possible paths named by the specimen's configuration. They do not establish reachability or executed traffic.
- `authoritative_synthetic_orders`: fixture-owned resource metadata used to assess subject and tenant boundaries.
- `missing_evidence`: questions that remain open regardless of a passing local example.

Return/response transport, supplier model calls, refund approval/execution, the identity service and live audit storage remain outside this narrowed experiment. The response is an in-process return value; no response network path has been observed. A10 is a temporary decision buffer, not durable audit storage.

## ASVS source and original interpretation

Reference: [OWASP ASVS 5.0.0 authorization chapter](https://github.com/OWASP/ASVS/blob/5cf9b032440be53ce345ab3c130fda46ba1ce7a2/5.0/en/0x17-V8-Authorization.md), pinned to release `v5.0.0_release`, commit `5cf9b032440be53ce345ab3c130fda46ba1ce7a2`. The API's moving `latest` release is a bleeding-edge build; it was not used as the normative version.

| Selected requirement | Paraphrased relevance |
|---|---|
| v5.0.0-8.1.1 | Define function and data-access rules with relevant consumer/resource attributes. |
| v5.0.0-8.2.1 and 8.2.2 | Require explicit function and object permissions. |
| v5.0.0-8.3.1 | Enforce the decision in a service tier the consumer cannot rewrite. |
| v5.0.0-8.3.3 | Preserve the originating subject's permissions through intermediary services. |
| v5.0.0-8.4.1 | Enforce tenant separation. |

The fixture schema, classifications, measurements and four scenarios are original design choices. They are not OWASP-prescribed test cases. This is independent research, with no upstream ASVS submission, acceptance, compliance certification or client deployment claimed.
