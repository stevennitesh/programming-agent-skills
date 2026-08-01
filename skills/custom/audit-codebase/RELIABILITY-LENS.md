# Reliability Lens

Audit what the subsystem promises and every meaningful supported way that
promise can succeed, fail, persist, resume, or interact.

## Contract-Derived Ledger

Derive rows from actual contracts rather than a blind Cartesian product:

```text
Supported scenario or transition:
Entry paths and affected callers:
Applicable state, edge, failure, security, compatibility, and environment:
Expected observable behavior:
Evidence checked:
Proof Seam:
Coverage: complete | incomplete
Admitted item IDs: <IDs> | none
```

Cover included, excluded, edge, state-transition, and failure branches. Verify
sibling callers when a shared function owns behavior. One finding or a green
broad suite never closes the remaining ledger.

## Questions That Find Reliability Issues

- **Semantic correctness:** Do public behavior, data meaning, ordering, errors,
  budgets, and compatibility match their authority?
- **Invariant enforcement:** Does the causal owner protect the condition across
  every supported transition and entry path?
- **Trust Boundaries:** Are reachable inputs, encoded outputs, privileges,
  secrets, authority, and external effects validated and minimally exposed?
- **Failure atomicity:** Does failure leave the old valid state or the complete
  new state?
- **Recovery and idempotency:** Do retry, resume, restart, rollback, cleanup,
  and repetition restore an explicit valid state without duplicate effects?
- **Concurrency and cancellation:** Do supported interleavings preserve
  invariants, ownership, ordering, resource bounds, and cleanup?
- **Lifecycle and compatibility:** Are absent, current, legacy, incompatible,
  expired, and restarted states intentional?
- **Environmental variation:** Do time, locale, filesystem, network, hardware,
  resources, and configuration behave within supported bounds?
- **Observability:** When repository authority requires operational signals,
  are critical failures and transitions detectable and attributable without
  leaking sensitive data?

Claim a shared Root Cause only after verifying the causal owner and sibling
paths. A symptom-level defect may remain valid when cause is unresolved; record
the causal limitation or gap. A Proof Seam establishes caller-visible meaning;
it does not by itself earn a design Seam or Adapter.

Example: if `load()` and `refresh()` both write through `_store()`, validating
expiry only in `refresh()` fixes one symptom; enforcing it at `_store()` protects
the shared lifecycle invariant for both callers.

## Floors

Never propose removing the smallest mechanism required for validation,
authorization, safe parsing/encoding, data-loss prevention, privacy, security,
accessibility, durability, failure atomicity, recovery, idempotency,
compatibility, physical calibration, or nontrivial behavior proof.

Prefer repository-owned tests, fixtures, schemas, traces, and observable
interfaces. A proposed enforcement rule's eventual proof needs a negative
control: clean pass, one intended violation failing for the intended reason,
restoration, and final pass.

Static smell, narration, and line count do not prove behavior. Unchecked
obtainable evidence makes coverage incomplete; evidence unavailable inside
Audit becomes a gap.
