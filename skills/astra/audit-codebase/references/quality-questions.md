# Quality questions

Use only questions that could expose a meaningful defect, avoidable cost, justified
complexity, or evidence gap in the selected scope. These are discovery prompts,
not a checklist or finding quota.

## User and developer workflows

For product or developer-experience opportunities, identify the actor, task,
current path, and concrete friction or limitation. Where relevant, inspect how a
user completes a product workflow or a developer configures, builds, diagnoses,
or releases the system, including supported platform differences.

A proposed capability must address an evidenced limitation of an existing
workflow. Separate the observed limitation from unverified assumptions about
user demand or benefit. Recommend a change only when its practical value
justifies implementation complexity and ongoing maintenance. Keep unresolved
product behavior or acceptance explicit and route it to
[shape-work](../../shape-work/SKILL.md) when clarification is requested; an audit
recommendation does not settle product policy.

## Ownership and change

Does a caller need knowledge the interface should own? Does one policy require
coordinated edits in several places, or are independent policies forced to change
together? Would removing a layer eliminate complexity or merely push necessary
decisions into callers?

Do transport, storage, framework, or vendor details force unrelated domain-policy
changes? Use real change history when it can test that explanation. Cycles, long
call chains, and similar syntax are leads only; show the actual coordination or
change burden before reporting a problem.

Would a smaller caller-facing interface hide meaningful policy and complexity,
so callers need less knowledge? A deeper module can improve locality and proof
without adding another abstraction layer. Compare the burden across the owner and
its callers; deleting a shallow wrapper is useful only when it removes complexity
rather than dispersing required decisions. Shared syntax alone does not justify
coupling different policies through one abstraction.

Do independent paths enforce conflicting rules or claim the same authority? Trace
the concrete disagreement and its consequence. If a recommendation conflicts
with an accepted decision, name that decision and the evidence for revisiting it;
do not silently replace its meaning or reopen it for a hypothetical benefit.

Look for hand-synchronized registries, caller imports of implementation internals,
or competing implementation paths when they cause missed updates, leaked policy,
or behavior drift. Compatibility paths and different semantics can justify separate
implementations; establish the actual burden before proposing consolidation.

## Domain and valid state

Do names, units, representations, states, and relationships preserve accepted
meaning? Where is authoritative state, who can write it, and can that owner enforce
its invariants through supported entry paths?

Can ordinary representations express invalid combinations that callers must
repeatedly repair? Distinguish accepted meaning from accidental current behavior.

When several stores or components appear to own the same state, trace writers,
synchronization, and read expectations. Multiple representations can be legitimate;
the improvement case needs an actual inconsistency or avoidable coordination cost.

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

Is the expensive result consumed by the supported workflow? Can filtering earlier
avoid unnecessary work, or can equivalent repeated work be avoided while preserving
required outputs? Establish whether the work is needed before choosing how to
make it faster.

Where is data read, copied, decoded, transformed, materialized, or retained? Follow
representative data paths to expose repeated work, unnecessary copies, oversized
intermediates, and poor locality. Consider existing capabilities, batching,
streaming, reuse, or caching when supported by the actual workload. Preserve
ordering, freshness, ownership, scientific meaning, and evaluation boundaries;
less work is useful only when it produces the same required result.

Support performance or resource-cost claims with an attributable trace,
representative measurement, or deterministic work count. Compare equivalent work
under relevant scale, environment, and variability.

A suspected bottleneck is a lead, not a measured benefit. A demonstrated cost can
be an opportunity without a formal budget; a defect claim requires a violated
expectation.

When operational correctness depends on detection or attribution, check whether
the necessary signals exist. State missing production evidence rather than
presenting a local observation as proof of production behavior.
