# Audit Finding Contract

Use this for repository-baseline findings, evidence gaps, and suggested next owners. Diff findings remain owned by `review/FINDING-CONTRACT.md`.

## Burden Of Proof

Admit a defect only when all five gates close:

- **Expectation:** an authoritative Charter contract, methodology, invariant, budget, comparison basis, or required evidence rule.
- **Reach:** a supported scenario inside the named repository baseline.
- **Evidence:** direct evidence from the immutable snapshot.
- **Impact:** a concrete correctness, domain, robustness, methodology, model-risk, data, validation, metric, analytics, or performance failure under that expectation.
- **Proportion:** proof proportionate to the claim.

```text
Defect ID:
Domain or lens:
Severity: P0 | P1 | P2 | P3
Location:
Expected contract, invariant, or methodology:
Supported scenario:
Verified evidence:
Impact:
Confidence:
Required proof:
```

Admit first, then assign severity by impact. Severity orders defects; evidence state and work shape choose the suggestion. Severity issues no release decision and grants no mutation authority. Omit unsupported possibilities. A verified beneficial opportunity without a violated expectation is an advisory only when enabled.

## Evidence Gap

Preserve required evidence that cannot be obtained read-only as a gap, not a defect or speculative advisory.

```text
Gap ID:
Domain or lens:
Blocked claim or decision:
Missing evidence:
Why the audit cannot obtain it:
Coverage and confidence impact:
```

## Suggest One Owner

Each defect, gap, advisory, or cohesive finding cluster receives exactly zero or one non-authoritative suggested next owner. Append:

```text
Suggested next owner: <skill> | none
Suggestion reason:
Pickup prerequisite:
```

Choose by the unresolved work:

| Evidence state or work shape | Suggested owner |
| --- | --- |
| One external authoritative fact is missing | `$research` |
| One disposable runnable probe or performance experiment is needed | `$prototype` |
| A domain rule, term, preference, or material tradeoff belongs to the user | `$grill-with-docs` |
| Expected behavior, symptom, cause, or trusted reproduction remains uncertain | `$diagnosing-bugs` |
| Remediation intent, acceptance, or migration remains unsettled | `$to-spec` |
| The solution is settled and only slicing remains across multiple implementation items | `$to-tickets` |
| Exactly one bounded remediation item is ready | `$implement` |
| Broad structural deepening, consolidation, or simplification needs its own survey | `$improve-codebase` |
| A cluster has multiple unresolved decisions or prerequisites and needs a tracker-backed, multi-session route | `$wayfinder` |
| No next owner is justified | `none` |

Name the immediate owner and stop; encode no workflow chain.

## Bound

Verification may reproduce or disprove a claim read-only. Optional proof needing new infrastructure remains a gap rather than expanding the audit. Cluster only items that share one remediation boundary or unresolved decision structure, and keep every member finding visible.
