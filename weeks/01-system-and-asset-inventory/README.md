# Week 01 — design the order-service trust boundaries

Sentinel Logistics is a fictional service. The original [source-led note](evidence-note.md) and [ten-asset intended scope](scope-and-evidence.md) establish the connected story. These contributions narrow it to a customer order passing through a portal, mock agent and order system.

## Calendar contributions

| Day | Scheduled date | Primary artifact | Supporting evidence |
|---|---|---|---|
| 001 | 2026-11-18 | [Evidence note](evidence-note.md) | [Proposed scope](scope-and-evidence.md) |
| 002 | 2026-11-19 | [Four synthetic review fixtures](annotations.md) | [Four fixtures](review-fixtures.json) · [Pinned ASVS source](asvs-source.json) |
| 003 | 2026-11-20 | [Review procedure and baseline observations](review-procedure.md) | [Baseline CSV](baseline-observations.csv) · [Raw observations](evidence/baseline/observations.json) |
| 004 | 2026-11-21 | [Boundary contract and worked example](control-or-playbook.md) | [Worked example](worked-example.md) · [Boundary implementation](../../tools/week01_boundary.py) |
| 005 | 2026-11-22 | [Evidence evaluation and limitations](evaluation-summary.md) | [Results CSV](review-results.csv) · [Limitations](limitations.md) |

The scheduled dates describe the calendar, not execution or publication dates. See Git commit metadata and raw execution timestamps for actual activity. Source references do not imply submission to, or acceptance by, OWASP.

## Reproduce the original specimen

```bash
python3 tools/week01_review.py --out /tmp/ashish-week01-baseline
```

Run from the repository root with Python 3.12 or newer. The mocks use only the standard library and require no network, model, credentials or package installation.

## Inspect the complete result

```bash
python3 tools/verify_week01.py --out /tmp/ashish-week01-verification
```

The recorded local suite has 22 unique regression cases. The expanded review identifies three unclassified fixture-level asset records and four undocumented flow records: two observed local calls and two configuration-only candidates. It preserves the original unavailable-backend case as indeterminate.

[Evaluation interpretation](evaluation-summary.md) · [Independent verification workflow](../../.github/workflows/verify-week01.yml).

All results are bounded synthetic observations, not customer deployments, learned-model assurance, regulatory certification or evidence of real traffic.
