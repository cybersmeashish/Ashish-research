# Week 01 — design the order-service trust boundaries

Sentinel Logistics is a fictional service. The original [source-led note](evidence-note.md) and [ten-asset intended scope](scope-and-evidence.md) establish the connected story. These contributions narrow it to a customer order passing through a portal, mock agent and order system.

## Calendar contributions

| Day | Scheduled date | Primary artifact | Supporting evidence |
|---|---|---|---|
| 001 | 2026-11-18 | [Evidence note](evidence-note.md) | [Proposed scope](scope-and-evidence.md) |
| 002 | 2026-11-19 | [Four synthetic review fixtures](annotations.md) | [Four fixtures](review-fixtures.json) · [Pinned ASVS source](asvs-source.json) |
| 003 | 2026-11-20 | [Review procedure and baseline observations](review-procedure.md) | [Baseline CSV](baseline-observations.csv) · [Raw observations](evidence/baseline/observations.json) |

The scheduled dates describe the calendar, not execution or publication dates. See Git commit metadata and raw execution timestamps for actual activity. Source references do not imply submission to, or acceptance by, OWASP.

## Reproduce the original specimen

```bash
python3 tools/week01_review.py --out /tmp/ashish-week01-baseline
```

Run from the repository root with Python 3.12 or newer. The mocks use only the standard library and require no network, model, credentials or package installation.
