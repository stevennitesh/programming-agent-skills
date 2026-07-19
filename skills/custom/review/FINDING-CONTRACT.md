# Finding Contract

**Ownership:** this contract owns finding admissibility and the interface returned to implementation callers. Read it before judging Standards or Spec.

## Admit

Admit a finding only when all five gates close:

- **Anchor:** an explicit acceptance criterion, documented repository standard, required validation, or reachable behavior changed by the target.
- **Reach:** a supported scenario inside the caller's Charter or requested slice.
- **Evidence:** direct evidence from the immutable review snapshot.
- **Impact:** a concrete correctness, security, data, required-proof, or important-path failure.
- **Proportion:** a remedy proportionate to the anchored contract.

**Admission before severity:** portability speculation, theoretical concurrency, unsupported environments, optional hardening, and adjacent cleanup are not findings unless direct evidence establishes a reachable Charter impact. When advisories are enabled, route a verified opportunity without a violated contract through `ADVISORY-CONTRACT.md`; otherwise omit it.

## Classify

Every reported finding carries:

```text
ID:
Axis:
Severity:
Location:
Anchor:
Supported scenario:
Evidence:
Impact:
Blocking: yes | no
Remediation: automatic-in-scope | decision-required | residual-hardening
Required proof:
```

- `automatic-in-scope`: the required change preserves the Charter and has bounded proof.
- `decision-required`: the required change alters product intent, acceptance, supported behavior, a public or data contract, security or privacy posture, dependency authority, or another commitment.
- `residual-hardening`: direct evidence establishes a reachable Charter risk, but automatic implementation is outside the recorded acceptance or authority. It remains a finding and does not authorize implementation.

**No laundering:** never turn a genuine contract violation into an advisory, `not checked`, or residual label to obtain a passing decision.

**Authority:** the caller validates classification before mutation. A review report supplies evidence; it never grants repair authority.

## Severity

- `P0`: catastrophic production, security, or data failure.
- `P1`: merge-blocking supported correctness or contract failure.
- `P2`: significant supported edge-case, required-validation, CI, or operator-risk defect; blocking only when the governing boundary requires the affected validation, CI, or workflow.
- `P3`: lower-risk actionable correctness or maintainability defect; nonblocking unless caller authority says otherwise.

`P0/P1` block.

## Bound

**Verification bound:** reproduce or disprove findings read-only. Missing required proof makes the review `incomplete`. Optional verification that needs substantial new infrastructure becomes explicit residual risk instead of expanding the review.

**Remediation bound:** judge only carried finding IDs, regressions introduced by their Repair delta, and remaining acceptance under the original Charter. Admit newly observed failures only through those surfaces. Do not reopen untouched surfaces with new hardening lenses.
