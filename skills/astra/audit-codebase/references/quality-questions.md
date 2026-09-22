# Quality questions

Use only questions that could expose a meaningful defect, avoidable cost, justified
complexity, or evidence gap in the selected scope. These are discovery prompts,
not a checklist or finding quota.

## Ownership and change

Does a caller need knowledge the interface should own? Does one policy require
coordinated edits in several places, or are independent policies forced to change
together? Would removing a layer eliminate complexity or merely push necessary
decisions into callers?

Do transport, storage, framework, or vendor details force unrelated domain-policy
changes? Use real change history when it can test that explanation. Cycles, long
call chains, and similar syntax are leads only; show the actual coordination or
change burden before reporting a problem.

## Domain and valid state

Do names, units, representations, states, and relationships preserve accepted
meaning? Where is authoritative state, who can write it, and can that owner enforce
its invariants through supported entry paths?

Can ordinary representations express invalid combinations that callers must
repeatedly repair? Distinguish accepted meaning from accidental current behavior.

## Failure, trust, lifecycle, and resources

Inspect only conditions activated by the supported workflow or observed evidence.
When relevant, ask whether callers can distinguish rejection, partial success,
completion, cancellation, retry, restart, or uncertain effects and whether the
real owner can enforce recovery.

For reachable trust boundaries, check where authorization or sensitive handling
is actually enforced. Preserve mechanisms required for durability, security,
accessibility, or data-loss prevention even when they look cumbersome.

When components deploy independently or data outlives a release, inspect real
compatibility combinations, migration races, and rollback limitations. Designing a
replacement migration belongs to [codebase-design](../../codebase-design/SKILL.md).

For shared resources, require a concrete exhaustion or interference path before
recommending limits, queues, timeouts, or concurrency controls.

## Simplification and dependencies

Could repository, standard-library, platform, or existing dependency behavior
replace custom machinery while preserving semantics? Before calling code or
configuration dead, check dynamic registration, generated ownership, persisted
formats, external consumers, and relevant history.

Fewer files, one implementation, or shorter code does not establish that removal
is safe. Include real migration and lifecycle costs in the judgment.

## Proof and maintainability

Does current proof establish the property that matters to an ordinary caller?
Could substitutes bypass the integration, persistence, concurrency, or rendering
mechanism under review?

Do tests have independent expectations and distinct regression responsibilities?
Different test layers may deliberately establish different properties.

Would the current checks reject a plausible wrong implementation? Seek a
discriminating input, transition, invariant, or negative control when ordinary
success also fits the wrong rule. Passing tests or high coverage alone do not
establish this distinction.

Require concrete ambiguity, coordination, or change burden before suggesting
naming, type, control-flow, comment, or test-structure cleanup.

## Performance and operation

Support performance or resource-cost claims with an attributable trace,
representative measurement, or deterministic work count. Compare equivalent work
under relevant scale, environment, and variability.

A suspected bottleneck is a lead, not a measured benefit. A demonstrated cost can
be an opportunity without a formal budget; a defect claim requires a violated
expectation.

When operational correctness depends on detection or attribution, check whether
the necessary signals exist. State missing production evidence rather than
presenting a local observation as proof of production behavior.
