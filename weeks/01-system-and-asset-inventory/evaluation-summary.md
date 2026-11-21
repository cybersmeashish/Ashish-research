# Evidence evaluation: broader scope exposes review blind spots

**Contribution 005 · Scheduled 22 November 2026 · Actual procedure-v2 results**

The same four fixtures were reviewed with [procedure v2](review-procedure.md#updated-procedure-v2--contribution-005). Inputs and decisions are retained in the [raw evaluation](evidence/evaluation/observations.json), [CSV](review-results.csv) and [source manifest](evidence/evaluation/source-manifest.json).

| Fixture | Original decision | Original evidence state | Proposed boundary | Unclassified / identified assets | Undocumented / identified flows |
|---|---|---|---|---|---|
| P01 | allow | confirmed_local_failure | deny | 1/7 | 2/8 |
| P02 | unknown | missing_evidence | deny | 2/5 | 2/4 |
| A01 | allow | observed_expected_behavior | allow | 0/6 | 0/6 |
| A02 | deny | observed_expected_behavior | deny | 0/6 | 0/6 |

## What the expanded review found

| Metric | Declared-scope baseline | Expanded original evidence |
|---|---:|---:|
| Fixture-level asset records | 21 | 24 |
| Unclassified asset records | 0 | 3 |
| Fixture-level directed flow records | 20 | 24 |
| Undocumented flow records | 0 | 4 |
| Undocumented observed local calls | Not included in the v1 discovery union | 2 |
| Undocumented configuration-only candidates | Not included in the v1 discovery union | 2 |

P01 contributes A11, an unclassified diagnostic buffer, and two undocumented actual local calls: direct agent-to-store access and the store-to-diagnostic copy. P02 contributes A06 and A12 as unclassified configured targets and two undocumented candidate paths. Those P02 paths were **not observed executing**.

The metric increase is the result of a more complete evidence scope. It is not a deterioration caused by the procedure, a count of unique enterprise assets, or a measured reduction in risk. Shared IDs are counted again within different fixtures; there are 24 fixture-level asset observations, not 24 unique systems.

The proposed gate denies P01's wrong-tenant read while preserving A01's legitimate read and A02's object-level denial. Its separate P02 denial does not resolve the unavailable original backend's behavior.

## Reproduce

```bash
python3 tools/week01_review.py --out /tmp/ashish-week01-baseline
python3 tools/week01_evaluate.py --out /tmp/ashish-week01-evaluation
python3 tools/verify_week01.py --out /tmp/ashish-week01-verification
```

The verification command compares saved CSV bytes with fresh execution, checks input hashes, reruns the worked example and executes the regression suite. Environment/timestamp metadata is recorded separately and is not required to be byte-identical across runs.

## CSV data dictionary

- `baseline_assets`, `baseline_flows`: the fixture's original declared scope.
- `identified_assets`: union of declared identifiers, original traced endpoints and configured tool targets.
- `unclassified_assets`: identified assets without a declared classification in the four-label vocabulary.
- `identified_flows`: union of directed endpoint pairs, deduplicated within the fixture; return network paths are excluded.
- `undocumented_flows`: pairs without a complete declared purpose/data/classification/owner/contract record.
- `undocumented_observed_local_flows`: incomplete flow records with an actual local function-call observation.
- `undocumented_configuration_only_flows`: incomplete candidate records with no observed execution.
- `original_evidence_state`, `original_backend_decidable`: the unchanged original-backend assessment.
- `proposed_control_decision`, `proposed_control_reason`: a separate local comparison using the original subject and request.
- `missing_evidence`: outstanding evidence questions; a passing local decision does not close them.

The timestamps in raw evidence describe the actual run. Contribution headings preserve scheduled calendar dates; they do not assert execution or publication occurred on those dates.

[Limitations and indeterminate case](limitations.md) · [Selected ASVS source](asvs-source.json).
