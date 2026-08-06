# Audit Finding Contract

Use this for repository-baseline defects and evidence gaps. Opportunities and
retained complexity use `QUALITY-LENS.md`; user-selectable improvement
boundaries and next-step suggestions use `CANDIDATE-CONTRACT.md`. Diff
findings remain owned by `change-review/FINDING-CONTRACT.md`.

## Burden Of Proof

Admit a defect only when all five gates close:

- **Expectation:** an authoritative audit-scope contract, methodology,
  invariant, budget, acceptance threshold, or required evidence rule. A
  comparison basis counts only when its authority defines pass/fail.
- **Reach:** a supported scenario inside the named repository baseline.
- **Evidence:** direct evidence bound to the selected objective's current source
  identity; governing external contracts, attributable traces, or dependency
  behavior may contribute when their applicability is proved.
- **Impact:** a concrete correctness, domain, robustness, security, privacy,
  methodology, model-risk, data, validation, metric, analytics, performance,
  or repository-governed maintenance or proof failure under that expectation.
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
Causal owner and affected callers: <required for a Root Cause or shared-owner claim> | not applicable
Confidence:
Required proof:
```

When a Root Cause or shared owner is claimed, verify the causal owner and
sibling entry paths. Apply `QUALITY-LENS.md`'s coverage-completion rule;
unavailable required causal evidence is a gap.

Assign severity only after admission:

- **P0:** catastrophic or irreversible production, security, privacy,
  availability, or data-integrity impact.
- **P1:** major failure across a critical or widely supported scenario.
- **P2:** concrete bounded failure with meaningful user, operational, domain,
  or maintenance impact.
- **P3:** localized low-impact violation of an authoritative expectation.

Severity orders defects. It grants no release, mutation, or next-step
authority. Omit unsupported possibilities. A verified beneficial change
without a violated expectation is an opportunity under `QUALITY-LENS.md`.

## Evidence Gap

Preserve required evidence unavailable from current source within Audit's
authorized read-only boundary as a gap, not a defect or speculative opportunity:

```text
Gap ID:
Domain or lens:
Blocked claim or decision:
Missing evidence:
Why the audit cannot obtain it:
Coverage and confidence impact:
Re-entry requirement:
```

## Bound

Verification may reproduce or disprove a claim read-only. Optional proof
needing new infrastructure remains a gap rather than expanding the audit.
If proportionate evidence is available within Audit authority but has not been
checked, it is unfinished work under Quality's completion rule, not a gap.
Candidate grouping belongs only to `CANDIDATE-CONTRACT.md`.
