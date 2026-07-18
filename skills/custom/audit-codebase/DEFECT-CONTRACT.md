# Audit Defect Contract

Use this for repository-baseline defects. Diff findings remain owned by `review/FINDING-CONTRACT.md`.

## Admit

Admit a defect only when all five gates close:

- **Expectation:** an authoritative Charter contract, methodology, invariant, or required evidence rule.
- **Reach:** a supported scenario inside the named repository baseline.
- **Evidence:** direct evidence from the immutable snapshot.
- **Impact:** a concrete correctness, methodology, model-risk, data, validation, metric, analytics, or performance failure under that expectation.
- **Proportion:** a required proof proportionate to the claim.

Assign severity only after admission. Omit unsupported possibilities. A verified beneficial opportunity without a violated expectation is an advisory only when enabled.

## Return

```text
Defect ID:
Domain or lens:
Severity: P0 | P1 | P2 | P3
Location:
Expected contract or methodology:
Supported scenario:
Verified evidence:
Impact:
Confidence:
Required proof:
```

Severity communicates impact; it does not issue a release decision or authorize mutation. A caller independently decides remediation and routing.

## Bound

Verification may reproduce or disprove a claim read-only. Required evidence that cannot be obtained makes the affected lens incomplete. Optional proof needing new infrastructure becomes an explicit evidence gap instead of expanding the audit.
