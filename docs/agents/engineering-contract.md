# Engineering Contract

<!-- programming-agent-skills setup-file: engineering-contract.md:84cdfdac09f5 -->

Explore imaginatively. Converge under proof. Simplify ruthlessly.

This document states durable engineering philosophy, shared concepts, and
condition-triggered methods. It is not a workflow, checklist, review gate,
completion contract, or authority to mutate files, Git state, trackers,
deployments, or external systems.

Repository instructions own local commands and boundaries. Domain records own
product meaning and settled decisions. Skills own procedures, checks, stopping
conditions, and outputs.

## How To Read This Contract

- **Must** marks a correctness, safety, integrity, or honesty floor.
- **Prefer** marks the default engineering choice. Deviation needs a supported
  reason; authority is required only when the deviation changes a commitment.
- **Method** names a practice triggered by a stated condition. Methods are not
  universal steps. When a condition applies, the outcome is binding; the
  responsible task or skill owns the procedure and evidence.

No generic rule overrides an explicit product commitment or repository
contract.

## Shared Concepts

- **Bounded slice:** the smallest useful scope that preserves commitments and
  is capable of producing meaningful evidence.
- **Commitment boundary:** product intent, accepted behavior, public and data
  contracts, security and privacy posture, compatibility promises, and agreed
  scope. Technique remains agent-owned until it changes a commitment.
- **Proof seam:** the caller-facing interface or observable boundary where
  correct meaning can be established.
- **Proof lane:** a repository-owned fixture, check, workflow, or artifact that
  exercises a proof seam. It proves only the behavior and conditions it covers.
- **Change closure:** removal or justified retention of paths made obsolete,
  redundant, or contradictory by a change.
- **Residual risk:** material uncertainty or unexecuted proof that limits a
  claim.

## Keep Faith With The Work

### Preserve Commitments And Domain Truth — Must

Trace behavior to the governing request, repository authority, accepted domain
language, invariants, decisions, and contracts. Keep meaning consistent across
code, tests, interfaces, data, and documentation.

Every decision-bearing acceptance term, threshold, unit, comparison, or
equivalence needs an operational definition or exact authoritative owner.
Surface ambiguity and contradiction instead of silently inventing meaning.

Implementation technique remains free where commitments leave it free.

### Make Correctness Robust — Must

Correctness includes behavior over relevant inputs, states, lifecycle
transitions, failures, supported environments, accessibility, and observable
effects—not merely a successful happy path.

Where the supported contract exposes them, preserve atomicity, recovery, retry,
idempotency, compatibility, cancellation, concurrency, and observability
semantics. Defect correction should address the causal owner and prevent the
supported failure across affected callers rather than mask one symptom.

Do not add machinery for risks the system cannot reach.

### Respect Trust And Data Boundaries — Must

Treat crossings between differently trusted callers, services, files,
processes, users, and privilege levels according to their actual contracts.

Validate untrusted or contract-sensitive input at the boundary that owns it.
Preserve data meaning, identity, integrity, provenance, schema, units, ordering,
and lifecycle where applicable. Protect authentication, authorization, secrets,
confidentiality, privacy, encoding, and external effects in proportion to the
governing contract and potential harm.

Simplification never discounts these obligations.

### Keep Evidence Honest — Must

Make no claim broader than fresh, relevant evidence supports. A focused check
proves only its covered slice. Tie behavioral claims to an observable proof
seam and a proof lane that actually exercises the claimed meaning.

Mocks, generated artifacts, structural inspection, and plausible narration do
not establish live behavior by themselves. When direct execution is unsafe or
unavailable, use the strongest safe proxy and identify it as a proxy.

Keep assumptions, skipped proof, unsupported conditions, and residual risk
visible. Residual risk is not failure; hidden or understated risk is.

### Practice Stewardship — Must

Preserve unrelated behavior, work, and durable decisions. Improve the selected
scope without silently widening it. Remove only fallout owned by the selected
change; do not disguise adjacent cleanup as necessary work.

## Shape Code For Understanding

### Deep Simplicity — Prefer

Give callers a small, honest interface that hides necessary complexity and has
a clear owner. Earn abstraction, indirection, adapters, configurability, and
seams through supported variation, repeated policy, or a real external
boundary.

Remove pass-through layers and ceremonial abstractions that do not reduce
caller burden.

### Local Readability — Prefer

Make important behavior understandable where it is owned and used. Let names,
types, units, state ownership, and control flow reveal meaning and valid
transitions. Comment surprising reasons and constraints, not syntax the reader
can already see.

### Fit Before Novelty — Prefer

Start with repository conventions, owned abstractions, standard or native
facilities, platform capabilities, and established dependencies.

Add a new abstraction, dependency, framework, or mechanism only when its
demonstrated value exceeds its learning, integration, maintenance, and failure
costs.

### Build Only What Is Needed — Prefer

Apply YAGNI to speculative behavior, configuration, compatibility, flexibility,
and extensibility.

Apply DRY to shared meaning and policy, not every repeated line. Repetition may
remain when unification would couple different meanings, owners, change rates,
or failure modes.

A deliberate limit is acceptable when its ceiling is known and there is a clear
reason to reconsider it.

### Keep Tests Lean And Meaningful — Prefer

Treat tests as durable evidence for behavior, invariants, failure paths, and
risks—not as a diary of tickets or edits. Reuse or extend a clear existing test
before adding a separate one.

A separate test earns its place through a distinct behavior, invariant, oracle,
proof seam, state or failure branch, material risk, or need for diagnostic
isolation. Consolidation must preserve coverage and diagnostic clarity.

Test count is not a goal. Unique evidence, clarity, maintenance burden, and
execution cost determine the portfolio.

## Methods When The Condition Applies

### Reason Across State Boundaries — Method

When correctness depends on cached, persisted, resumed, grouped, projected,
distributed, or session-scoped state, distinguish the supported states, access
paths, and lifecycle transitions that can change meaning.

Cover distinct behavior and high-risk interactions, not a blind Cartesian
product.

### Use A Negative Control — Method

When adding or changing a validator, hook, policy check, dependency boundary,
or other enforcement mechanism, show that the rule is causal: a conforming case
passes, one controlled violation fails for the intended reason, and the
restored conforming case passes.

### Close Displaced Paths — Method

When a change replaces or makes behavior redundant, trace the affected
implementations, callers, registrations, exports, flags, tests, configuration,
documentation, and migrations.

Remove obsolete or duplicate paths. Retain an older path only for a supported
compatibility obligation with a clear reason, owner, evidence, and removal
condition.

### Measure Consequential Claims — Method

When a decision or claim depends on performance, capacity, reliability,
latency, cost, or resource use, measure before claiming improvement.

Bind the result to a comparable workload, environment, build, method, sample
and material variation, and baseline or budget. If meaningful measurement is
unavailable, narrow the claim and record the residual risk.
