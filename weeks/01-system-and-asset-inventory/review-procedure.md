# Repeatable boundary review: baseline and evidence expansion

**Contribution 003 · Scheduled 20 November 2026 · Procedure v1 and baseline observations**

Start with [the annotations](annotations.md) and the unchanged [four fixtures](review-fixtures.json). The procedure separates a directly observed local failure from absent evidence.

## Scope and preparation

Use Python 3.12 or newer, the standard library and this repository. No packages, credentials, browser, network service or model download is required. Run from the repository root:

```bash
python3 tools/week01_review.py --out /tmp/ashish-week01-baseline
python3 -m unittest discover -s tests -p 'test_week01_baseline.py' -v
```

The tool executes actual in-process mock functions. Hop records describe those local function calls. They do not measure service identity, network reachability or deployed enforcement.

## Procedure v1

1. Record the fixture's asset scope, declared classifications, owner roles and intended flow contracts.
2. Keep request/agent fields separate from the separately supplied trusted-context fixture.
3. Trace the actual local specimen through the portal, API, mock agent and available order-access function.
4. For an allowed result, compare returned order metadata with the originating subject and tenant. A mismatch supports a **confirmed local failure**.
5. For a denial, record the existing order and the reason. Use A01 to check that legitimate work remains possible.
6. If the backend, context or necessary observation is absent, mark **missing evidence / cannot determine**. Do not turn an unknown into a pass or a confirmed failure.
7. Record missing evidence and the source/input hashes alongside the result.

Baseline inventory metrics consider the **declared** scope only. That is a deliberately bounded documentation check, not a complete discovery method. A zero missing-classification count cannot establish that no asset was omitted.

Documentation completeness means a record has the stated fields and a declared reference to the earlier intended-flow design. The tool does not authenticate approvals, accepted ownership or the referenced control's deployment.

## Evidence states

| State | Required evidence |
|---|---|
| `confirmed_local_failure` | Actual mock access returns a record outside the separately supplied subject/tenant boundary |
| `observed_expected_behavior` | Existing in-scope allowed read or existing out-of-scope denial matches the stated rule |
| `missing_evidence` | Relevant backend decision, authenticated context or access observation is unavailable |

“Observed expected behavior” is narrower than “the application is secure.”

## Baseline artifacts

[Baseline observations](baseline-observations.csv) · [Raw in-process observations](evidence/baseline/observations.json) · [Source manifest](evidence/baseline/source-manifest.json).

## Updated procedure v2 — contribution 005

After the boundary contract is available, expand the **same original fixture** inventory:

1. Union declared assets with identifiers present in original local call traces and configured tool targets.
2. Union declared flows with original traced calls and configured candidate flows. Deduplicate by directed endpoint pair within each fixture.
3. Record whether each added path is **observed local execution** or **configuration-only**.
4. An asset is unclassified when no declared record supplies one of the four allowed class labels. A recognized asset name does not supply a missing classification.
5. A flow is undocumented when its declared record lacks purpose, data fields, classification, proposed owner or contract reference. A candidate route can be undocumented while its execution remains unproven.
6. Apply the proposed control to a fresh local copy. Record that comparison separately; it does not supply evidence about the unavailable original backend.
7. Preserve P02's original indeterminate enforcement conclusion until the missing evidence is provided.

Use `python3 tools/week01_evaluate.py --out /tmp/ashish-week01-evaluation` once contributions 004–005 are present. See [results](review-results.csv) and [limitations](limitations.md).

Counts are fixture-level observations, not unique enterprise assets or estimates of real-world effectiveness. The union exposes review blind spots; it does not repair classifications, approve paths or establish network isolation.
