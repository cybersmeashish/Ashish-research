# Worked example: preserve identity across an agent proposal

**Contribution 004 · Scheduled 21 November 2026 · Actual local before/after observation**

Run `python3 tools/week01_worked_example.py` from the repository root. The [raw output](evidence/worked-example.json) uses the unchanged P01 fixture, request and order dictionary.

| Input or observation | Recorded value |
|---|---|
| Separately supplied subject | `customer-a` |
| Separately supplied tenant | `tenant-alpha` |
| Untrusted client tenant claim | `tenant-beta` |
| Requested object | `order-b` |
| Original local specimen | `allow` — `legacy_trusted_client_tenant` |
| Original returned object's tenant | `tenant-beta` |
| Original evidence state | `confirmed_local_failure` |
| Proposed control | `deny` — `tenant_mismatch` |
| Proposed returned object | No response data |

The legacy mock used the tenant supplied in the request and bypassed the proposed gateway/API path. The separately supplied subject belonged to a different tenant from the returned order, supporting a confirmed **local** authorization failure.

The new decision derives tenant and subject from the separately supplied context, checks resource metadata and denies the same requested object. Changing the agent's role claim cannot change those permissions. A01 supplies the legitimate-read control case; A02 supplies the same-tenant different-owner case.

This result changes a bounded decision. It does not show that direct database access, an external data exit or a network route is blocked in production. The old specimen also produces an unclassified local diagnostic copy; that inventory/flow gap remains in the original evidence set.

[Boundary contract](control-or-playbook.md) · [Boundary implementation](../../tools/week01_boundary.py) · [Reproducible example](../../tools/week01_worked_example.py).
