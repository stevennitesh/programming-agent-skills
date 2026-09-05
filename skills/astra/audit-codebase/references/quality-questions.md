# Quality questions

Use only dimensions relevant to the audit. Architecture findings need observable
costs; broad audit requests also warrant the applicable correctness and operational
questions below. Existing repository contracts supply the expected behavior.

## Ownership and change

Which knowledge must a caller learn despite the interface? Does one policy change
in several places, or do independent policies have to change together? Would
removing a layer eliminate complexity or push its necessary decisions into callers?
Check both excessive fragmentation and excessive concentration. Cycles and long
call chains are leads; show the concrete coordination or discovery burden.

Does domain policy depend on transport, storage, or framework details in ways
that force unrelated policy edits when those details change? Trace the dependency
direction and a concrete consequence before recommending inversion or an adapter.

Look at real change history when it can test this explanation. Similar syntax
does not establish shared domain meaning. Multiple independent releases, resource
lifetimes, or authoritative models may warrant separate boundaries.

## Domain and valid state

Do names, units, representations, and relationships preserve accepted meaning?
Where is authoritative state, who can write it, and can that owner enforce its
invariants through all supported entry paths? Can ordinary data shapes represent
invalid combinations that callers must repeatedly repair? Distinguish accepted
contracts from accidental current behavior and identify consequential ADR conflicts.

## Failure, trust, and lifecycle

Trace relevant rejection, partial success, cancellation, retry, restart, and
concurrency paths. Can a caller distinguish accepted from completed work? Do shared
state and remote effects have real enforcement and recovery mechanisms? Check
reachable trust boundaries, authorization, sensitive output, and resource cleanup.
Use the supported environment and compatibility obligations, not a Cartesian
product of hypothetical failures. Preserve mechanisms needed for durability,
security, accessibility, or data-loss prevention even when they look cumbersome.

When components deploy independently or data outlives a release, check supported
combinations of clients, workers, and stored records. Can conversion race with
old writers, or can rollback leave new data unreadable? Audit the existing
transition guarantees; leave designing a replacement migration to codebase-design.

For shared resources, can one slow dependency, tenant, or request exhaust capacity
needed by others? Check queue growth, retry amplification, timeouts, cancellation,
and concurrency limits against supported workloads. Require a concrete exhaustion
path or evidence of cost rather than prescribing limits to every local operation.

## Simplification and dependencies

Could existing repository, standard-library, or platform behavior remove a custom
mechanism while preserving semantics? Is configuration or compatibility still
used? Check registration, dynamic imports, serialization, generated ownership,
external consumers, and relevant history before calling code dead. Fewer files,
one implementation, or a shorter diff does not independently justify removal.
Include lifecycle and migration costs when comparing alternatives.

## Proof and maintainability

Can ordinary callers exercise the contract without depending on internal layout?
Do substitutes hide the integration property that matters? Do tests have independent
expectations and distinct regression responsibilities? For test consolidation,
identify the overlap and the risk the surviving checks preserve; different layers
may deliberately establish different properties. Name concrete ambiguity or change
burden before suggesting naming, control-flow, type, or comment changes.

Would the checks reject a plausible wrong implementation of the claimed behavior?
Look for a discriminating input, transition, or negative control when ordinary
success also fits the wrong rule. Passing tests or a high coverage percentage do
not establish that distinction; do not require mutation testing for every audit.

## Performance and operation

Use an attributable trace, representative measurement, or deterministic resource
count to support cost claims. Bind comparisons to equivalent work, environment,
scale, and relevant variability. A suspected bottleneck is a lead, not measured
benefit. An observed cost can be an opportunity without a formal budget; a defect
claim needs a violated expectation. Check whether important failures can be
detected and attributed when operation depends on those signals. State missing
evidence rather than claiming a local check proves production behavior.
