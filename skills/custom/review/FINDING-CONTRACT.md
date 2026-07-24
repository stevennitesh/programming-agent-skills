# Finding Contract

Load this contract after judgment has generated candidate observations.

## Admit

Admit a finding only when all five gates close:

| Gate | Required evidence |
| --- | --- |
| **Anchor** | Governing acceptance, repository Standard, required validation, or reachable behavior changed or promised by the target |
| **Reach** | A supported scenario within the Charter or requested slice |
| **Evidence** | Direct evidence from the immutable snapshot and safe read-only verification |
| **Impact** | Concrete correctness, security, privacy, data, required-proof, operability, or maintainability failure |
| **Proportion** | A required outcome with a remedy proportionate to the anchored contract |

Admission precedes severity. Reject disproved, speculative, preference-only,
unsupported-environment, tooling-style, optional-hardening, and adjacent
cleanup candidates unless direct evidence establishes a reachable Charter
impact.

A target's omission of contract-required proof may pass the normal gates.
Reviewer inability to obtain evidence needed to decide a candidate or required
axis makes that coverage `incomplete`, not a finding. Optional unavailable
verification is residual risk and does not admit the candidate.

## Record

Every admitted finding records:

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

Keep IDs stable through remediation. Name the tightest useful captured line or
missing seam. Separate direct observation from inference. Required proof is
the smallest semantic proof that can close the Repair.

## Classify

- `P0`: catastrophic production, security, privacy, or data failure.
- `P1`: merge-blocking supported correctness or contract failure.
- `P2`: significant supported edge-case, required-validation, CI, release, or
  operator risk.
- `P3`: lower-risk actionable correctness or maintainability.

`P0` and `P1` block. `P2` and `P3` follow the Charter or repository policy.

Classify remediation independently:

- `automatic-in-scope` preserves the Charter with bounded proof.
- `decision-required` changes an accepted commitment or authority.
- `residual-hardening` identifies a directly evidenced reachable risk outside
  automatic acceptance.

Classification grants no mutation. The caller validates it before Repair.
