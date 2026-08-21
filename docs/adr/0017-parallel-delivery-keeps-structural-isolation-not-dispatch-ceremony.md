# Parallel Delivery Keeps Structural Isolation, Not Dispatch Ceremony

**Status**: accepted

## Context

ADR-0012 established plain delegation and safe concurrent worktrees. Later
runtime additions made pytest collection, oldest-lane eviction, model profiles,
author-count review, and structured worker returns part of delivery. Those
rules do not decide whether concurrent writers can work or integrate safely.

## Decision

Parallel delivery keeps one root integrator, dependency-aware dispatch,
independent ownership and write effects, exact-base worktrees, one writer per
lane, direct inspection of worker commits, one-at-a-time landing, integrated
proof, and conservative named-lane cleanup.

Each dispatch frontier uses current integration `HEAD`. Siblings selected
together share that base. Dependent items start only after predecessor landings
and use the newer `HEAD`. A serial worker may commit directly in the integration
checkout only while it has exclusive custody; the root verifies that direct
landing without applying it again.

Lane preparation creates checkout-external temp and cache paths but does not
run repository tests. Cleanup acts only on caller-named completed lanes and
preserves dirty, unintegrated, active, or uncertain state. The caller chooses
which completed lane to remove when runtime capacity is full.

Workers use the active runtime unless the user selects a model. Worker returns
are concise evidence, not a status taxonomy. Multiple authors require serial
integration and combined proof, but do not alone require Change Review. Review
activates only when the user or repository requires it, or a concrete unresolved
shared-contract or migration judgment remains after proof.

This decision supersedes ADR-0012's pytest collection and oldest-lane eviction
requirements, ADR-0016's implementation-profile consequence, and ADR-0015's
author-count review trigger retained through ADR-0016. Other decisions in those
ADRs remain in force.

## Consequences

- `parallel-implement` owns concurrency mechanics and no worker coding method.
- `implement` and `parallel-implement` point to Change Review only on the lean
  activation rule above.
- Repository setup needs the external worktree permission root, not a named
  model configuration.
- Historical evaluations and superseded decision text remain evidence.
