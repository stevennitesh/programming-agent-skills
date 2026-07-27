# Reliability Lens

Audit what the subsystem promises and every meaningful supported way that
promise can succeed, fail, persist, resume, or interact.

## Semantic Correctness

**Semantic Correctness** means observable behavior has the intended meaning,
not merely that code runs or output exists.

- **Contract Fidelity:** public behavior, data contracts, ordering, errors,
  budgets, and compatibility match their authority.
- **Invariant:** a condition that must remain true across every relevant
  transition and entry path.
- **Root Cause:** the shared cause that explains all affected callers, rather
  than the nearest named symptom.
- **Proof Seam:** the observable caller-facing place where meaning can be
  established.

A Proof Seam establishes meaning. Design's **Seam** permits behavior to vary
without caller edits; a Proof Seam alone does not earn an Adapter or design
Seam.

Example: `load()` and `refresh()` both write cache entries through `_store()`.
Validating expiry only in `refresh()` fixes one symptom; enforcing it at
`_store()` protects the shared lifecycle invariant for both callers.

Trace included, excluded, edge, and failure scenarios. Verify sibling callers
when a shared function owns the behavior. Treat a green broad suite as support,
not a replacement for a missing semantic branch.

## Robustness

**Robustness** is correct, bounded behavior under supported stress, variation,
and partial failure.

- **Trust Boundary:** where reachable input, encoded output, data, privilege,
  secrets, authority, or external effects cross trust; preserve validation,
  authentication, authorization, safe parsing and encoding, and
  least-necessary exposure.
- **Failure Atomicity:** a failed operation leaves either the old valid state
  or the complete new state, never an unintended partial state.
- **Recovery:** retry, resume, restart, rollback, cleanup, or reconciliation
  restores an explicit valid state.
- **Idempotency:** repetition has the promised effect and does not duplicate
  irreversible work.
- **Concurrency:** interleavings preserve invariants, ownership, ordering, and
  cancellation behavior.
- **State Lifecycle:** initial, absent, current, legacy, incompatible, expired,
  restarted, and same-session transition branches behave intentionally.
- **Compatibility:** supported versions, schemas, formats, platforms, and
  integration contracts fail or migrate deliberately.
- **Environmental Variation:** time, locale, filesystem, network, hardware,
  resources, and configuration vary within supported bounds.
- **Observability:** repository-required logs, metrics, traces, or other
  signals make supported failures and state transitions detectable and
  attributable without leaking sensitive data.

Derive a state-boundary matrix from actual subsystem contracts. Cover distinct
branches and high-risk interactions, not a blind Cartesian product.
Ask whether each supported failure and critical transition is safely
observable when repository authority requires an operational signal.

## Robustness Floors

Never recommend simplifying away:

- input validation at Trust Boundaries;
- error handling that prevents data loss;
- security, privacy, authorization, or auditability;
- accessibility basics;
- durability, Failure Atomicity, Recovery, or Idempotency;
- required compatibility;
- calibration or tolerance needed by physical systems; or
- the smallest meaningful check for nontrivial behavior.

## Evidence

Prefer repository-owned tests, fixtures, schemas, traces, and observable
interfaces. When a new enforcement rule is proposed, its eventual proof needs
a negative control: clean pass, one intended violation failing for the intended
reason, restoration, and final pass.

Record unsupported or unobtainable behavior evidence as a gap. Static smell,
plausible narration, and line count do not prove correctness or robustness.
