# Finding Contract

Load this contract before coverage and judgment. It owns review
classification, risk admission, finding fields, severity, and remediation
bounds.

## Classify

Use one primary class per candidate. Cite secondary anchors without duplicating
the finding.

| Axis | Class | Brief |
| --- | --- | --- |
| **Spec** | **Commitment Fidelity** | Required outcomes are implemented with their intended meaning. |
| **Spec** | **Scope and Contracts** | Scope, non-goals, compatibility, public and data contracts, domain rules, and accepted decisions hold. |
| **Spec** | **Acceptance and Change Closure** | Required acceptance is proved and displaced or redundant paths are removed or supported. |
| **Standards** | **Semantic Correctness** | Actual behavior preserves applicable meaning, invariants, state, and data. |
| **Standards** | **Robustness and Operability** | Failure, recovery, idempotency, concurrency, environmental, and operational behavior are safe where applicable. |
| **Standards** | **Code Quality and Design** | Ownership, cohesion, depth, clarity, duplication, coupling, complexity, and simplification have a concrete supported shape. |
| **Standards** | **Proof Discipline** | Required proof exercises the meaningful seam and applicable branches on the reviewed candidate. |
| **Standards** | **Stewardship** | Retained complexity has an owner and reason, unrelated work is preserved, and changed code remains maintainable. |

Behavior is evidence used by both axes, not another axis. Risk is a
cross-cutting modifier. A risk may widen coverage or justify a specialist only
when the changed surface, one supported scenario, a reachable behavior or
failure path, and concrete impact are all identified. Hypothetical
permutations do not qualify.

## Admit

Admit a finding only when all five gates close:

| Gate | Required evidence |
| --- | --- |
| **Anchor** | Governing acceptance, repository Standard, required validation, or reachable behavior changed or promised by the target |
| **Reach** | A supported scenario inside the Charter or requested slice |
| **Evidence** | Direct evidence from the immutable snapshot and safe read-only verification |
| **Impact** | Concrete correctness, security, privacy, data, proof, operability, or maintainability failure |
| **Proportion** | A required outcome with a remedy proportionate to the anchored contract |

Admission precedes severity. Reject disproved, speculative, preference-only,
unsupported-environment, tooling-style, optional-hardening, and adjacent
cleanup candidates. Exclude pre-existing problems unless the target creates or
worsens them, or Change Closure brings them into scope. Record one finding per
violated primary obligation; do not multiply one observation across classes.

A target's omission of contract-required proof may pass the normal gates.
Reviewer inability to obtain evidence needed to decide a candidate or required
axis makes coverage `incomplete`, not a finding. Optional unavailable
verification is residual risk and does not admit a candidate.

## Record

Every admitted finding records:

```text
ID:
Axis:
Class:
Severity:
Location:
Anchor:
Supported scenario:
Behavior or failure path:
Evidence:
Impact:
Supported risk trigger: <trigger or none>
Blocking: yes | no
Remediation: automatic-in-scope | decision-required | residual-hardening
Required proof:
```

Keep IDs stable through remediation. Name the tightest useful captured line or
missing seam. Separate direct observation from inference. Required proof is
the smallest semantic proof that can close the Repair.

## Severity And Remediation

- `P0`: catastrophic production, security, privacy, or data failure.
- `P1`: merge-blocking supported correctness or contract failure.
- `P2`: significant supported edge-case, required-validation, CI, release, or
  operator risk.
- `P3`: lower-risk actionable correctness or maintainability.

`P0` and `P1` block. `P2` and `P3` follow the Charter or repository policy.

- `automatic-in-scope` preserves the Charter with bounded proof.
- `decision-required` changes an accepted commitment or authority.
- `residual-hardening` identifies a directly evidenced reachable risk outside
  automatic acceptance.

Classification grants no mutation. The caller validates it before Repair.
