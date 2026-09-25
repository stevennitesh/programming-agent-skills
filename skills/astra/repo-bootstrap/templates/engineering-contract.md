# Engineering contract

Use this guidance for engineering decisions that are easy to over-assume or
mis-prove. Repository-specific requirements and accepted domain decisions supply
the local meaning. Apply a conditional practice only when its condition is present.

Implement guarantees required by actual supported workflows. Do not infer scale,
concurrency, independent consumers, crash recovery, future reuse, or stronger
reliability from broad goals alone. A plausible failure, generic best practice, or
agent-written plan does not establish a requirement. Preserve explicit user
commitments and accepted project meaning; surface a proposed change to an accepted
guarantee to its owner.

## Understand the changed behavior

Trace enough of the owning code and affected callers to establish the behavior
being changed and the consequences that matter. Distinguish intended behavior
from an implementation accident. Resolve only consequential ambiguity.

Use the smallest useful slice that can complete the requested outcome. A thin real
path or probe may resolve an uncertainty, but it is evidence rather than completion.

## Prefer the smallest complete design

Reuse language, platform, dependency, and repository capabilities when they
already satisfy the real caller. Add a boundary or abstraction when it owns useful
policy, variation, state, or failure semantics rather than merely forwarding work.

Keep related decisions together when they must change together. Separate different
domain policies when sharing an owner creates real coupling. Preserve valid-state
and domain distinctions where losing them could create a meaningful error.

Do not add compatibility, fallback, recovery, or configurability machinery without
a supported workflow that needs it. When real consumers or stored data require
coexistence, make the migration and removal condition explicit; otherwise migrate
owned callers and remove displaced paths together.

Preserve meaningful failure and partial-result semantics. A fallback must not turn
an error or incomplete result into apparent success.

When many similar edits or checks share one mechanical recipe, and a small
deterministic script, codemod, generator, or check would materially reduce
inconsistency or verification cost, build the smallest rerunnable lever and prove
it on a representative unit. Do not add tooling when direct work is simpler and
equally reviewable.

When a deliberate simplification has a non-obvious material ceiling whose
violation would change correctness, performance, or operations, record that
ceiling and the condition that should trigger reconsideration at its natural
owner.

## Match proof to the claim

Run required checks and the nearest useful evidence that can fail for the changed
behavior. When a plausible wrong rule also passes the ordinary case, choose an
input, state, invariant, or independently derived expectation that distinguishes
the intended result.

For numerical or data transformations, preserve material identity, units, time and
availability semantics, missing-value meaning, precision, and consequential method
assumptions.

For a changed integration, prove that the ordinary caller reaches the new behavior.
When meaning can be lost across a handoff, pass actual produced output through the
affected public path; a reconstructed substitute or isolated helper does not prove
that connection.

Preserve the mechanism relevant to the claim. A substitute can prove local policy
while leaving persistence, concurrency, transport, rendering, or other mechanism-
specific behavior unproved.

Reuse evidence while the code, inputs, dependencies, configuration, environment,
and candidate identity relevant to its claim remain valid. Broaden verification
only for demonstrated shared impact, repository policy, or a concrete unresolved
risk. Completion follows the requested outcome, not a green command or exhausted
effort budget.

Continue through authorized implementation, verification, and necessary
corrections until the requested outcome is complete. Status updates, intermediate
findings, passing checks, and reversible non-blocking choices are not stopping
points. When reporting status mid-run, pair the update with the next safe action
in the same turn when practical instead of reporting and pausing. Stop when
required user input or authority is missing, or when a hard safety or operational
boundary prevents safe progress.

## Handle consequential effects explicitly

When retrying can duplicate or corrupt effects, choose the smallest adequate
protection. After partial or uncertain external effects, inspect actual state before
retrying.

Separate files or worktrees do not isolate shared databases, ports, services, or
other external resources. When concurrent mutation must share state, enforce the
required ownership or serialization at the real shared boundary.

For consequential performance or resource claims, compare equivalent work against
a relevant baseline. For external mutations, establish the target and authority and
read back the result when confirmation matters.

These conditions do not start additional workflows. Use TDD, delegation, formal
review, optimization campaigns, or specialized operational procedures only when
the user or applicable instructions call for them.

Report the outcome, decisive evidence, and material limits.
