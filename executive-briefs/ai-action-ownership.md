# Before an AI agent acts, decide who owns the action

An AI support assistant changes the order-service risk conversation. It may retrieve customer information, send context to a model supplier, and suggest an operational action. The useful first question is which systems, data, and actions it can reach, and who accepts each boundary.

The Sentinel Logistics [reference inventory](../weeks/01-system-and-asset-inventory/scope-and-evidence.md) records ten proposed assets, eight intended flows, and five action decisions. Its [primary-source note](../weeks/01-system-and-asset-inventory/evidence-note.md) relates the inventory to NIST CSF 2.0. The scenario is fictional and the routes have not been validated in a live environment.

## A decision for leadership

Assign an accountable owner for each permitted action and external data exit before expanding autonomy. Separate proposing a refund, approving it, and executing it. A model suggestion should pass through the service that owns the authorization decision.

## Evidence to request

- A current inventory of service identities, data, tools, destinations, and owners.
- Valid and denied cases showing the intended authority.
- An attributable decision record and a review trigger for new tools or destinations.
- A documented recovery or suspension path when an action or identity is revoked.

The [Sovereign AI reference control plane](https://github.com/cybersmeashish/sovereign-AI) and [application authorization lab](https://github.com/cybersmeashish/secure-coding-examples) provide local examples to inspect. Their tests support bounded reference behavior, not a claim that an enterprise deployment has been secured.
