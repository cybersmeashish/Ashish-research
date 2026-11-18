# Know what your AI service can reach before adding controls

**Day 001 · 18 November 2026 · Primary-source evidence note**

**Audience:** CISOs, security architects, and AI security researchers.

**Business question:** Which assets and actions need an explicit access owner before we automate?

## Primary source and supported finding

This note examines the [NIST Cybersecurity Framework 2.0, NIST CSWP 29](https://doi.org/10.6028/NIST.CSWP.29), published on 26 February 2024. The relevant source locations are the **IDENTIFY → Asset Management (ID.AM)** outcomes in the CSF Core.

ID.AM-02 states:

> “Inventories of software, services, and systems managed by the organization are maintained.”

The adjacent outcomes extend the inventory view to authorized communications and data flows (**ID.AM-03**), supplier-provided services (**ID.AM-04**), and asset prioritization according to importance and impact (**ID.AM-05**).

**Supported finding:** The source supports maintaining a view of systems, services, dependencies, and their authorized connections. A component list alone does not represent all of those outcomes.

The framework describes outcomes. The fields and AI-specific design choices below are my proposed implementation, rather than a NIST-prescribed agent-security architecture.

## My interpretation for an AI-enabled service

In the fictional Sentinel Logistics design, an assistant can retrieve order information, call an external model provider, and propose tool actions. Listing an “AI assistant” as one asset hides several separate decisions:

1. Which tenant's information may the current request retrieve?
2. What data may leave the organization for a supplier's model service?
3. Can a model-generated action change an order, or only propose a change?
4. Which service must enforce the decision, and who owns that boundary?

My proposed inventory therefore adds **actor or service identity, data accessed, permitted actions, destination, enforcement point, accountable role, and validation status**. These additions connect the component inventory to a concrete authorization review.

This is a design inference from the source's inventory and flow outcomes. It does not establish that every AI deployment must use these exact fields.

## Applying the finding to today's scope

The [supporting scope and evidence artifact](scope-and-evidence.md) records **10 proposed assets, 8 intended flows, and 5 action decisions**.

| Source outcome | Proposed application to Sentinel Logistics |
| --- | --- |
| ID.AM-02 | Record the order API, agent orchestrator, retrieval service, and tool gateway as separate assets. |
| ID.AM-03 | Describe the proposed allowed routes between those services, including the model-provider data exit. |
| ID.AM-04 | Record the external model provider as a supplier dependency with a proposed integration owner. |
| ID.AM-05 | Review the order store and refund-execution boundary according to the consequences of misuse. |

One important design decision is to separate **proposing a refund**, **approving it**, and **executing it**. The model's suggested action would not itself grant authority. The proposed gateway and order API would check the relevant identity, tenant, resource, and approval before a mutation.

That separation is my design choice. Its effectiveness has not yet been tested.

## What this contribution establishes

Today's output is a reviewable reference inventory and action map. The named owners are **proposed roles in a fictional organization**, not confirmed employees or accepted assignments.

No application was deployed or tested for this contribution. The recorded flows are intended permissions, not observations of live traffic. There is no measured reduction in attack success, business loss, or operational risk.

The useful next step is to compare the proposed map with implementation evidence: configured identities, tool registrations, storage permissions, and observed request paths. Each unknown should remain visible until checked.

## Open question

**What mechanism should detect and review changes to the agent's reachable tools and external destinations before a new route becomes usable?**

A static inventory may become stale when tool registration or supplier routing changes. A future experiment should test change detection and ownership review, rather than assume that writing the inventory keeps it accurate.

## Source

National Institute of Standards and Technology. *The NIST Cybersecurity Framework (CSF) 2.0.* NIST CSWP 29, 26 February 2024. [DOI and official publication](https://doi.org/10.6028/NIST.CSWP.29) · [Official PDF](https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf). See CSF Core outcomes ID.AM-02 through ID.AM-05.
