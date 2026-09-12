---
name: codebase-design
description: Resolve unsettled architecture or integration decisions about ownership, interfaces, state, or migration. Exclude routine implementation and whole-codebase audits.
---

# Codebase design

Resolve a bounded design question so implementation can proceed with the
important decisions explicit. The question may cross several systems; its
boundary follows the behavior and ownership involved, not a single file.

For a design-only request, inspect and recommend without changing product code.
When called within authorized implementation, return the decision to that work;
do not introduce another approval gate. Prototype remains a separate skill.

## 1. Locate the decision

Identify the unsettled decision and the requirement or uncertainty driving it.
Determine whether the current design or its smallest extension already satisfies
it. Inspect the callers, state, dependencies, and accepted guarantees needed to
resolve this decision. Trace a representative path when interactions or ownership
are uncertain. Distinguish intended guarantees from accidental dependence.

Before recommending a redesign, identify a demonstrated cost or an unmet new
requirement. Costs include callers coordinating an invariant, one policy changing
in several places, leaked representation, or repeated workarounds. Check sibling
callers or relevant history when they could
confirm or disprove the pattern. One awkward case does not establish a systemic
problem. For new behavior, identify the new constraint that makes the choice
consequential. Retaining the current design is a valid answer.

Use audit findings as leads. Reuse attributable evidence while its relevant code,
inputs, and environment remain valid; recheck gaps, contradictions, or relevant
drift. Repository-wide discovery belongs to a separate audit; do not turn this decision into a full map
or require an audit report before beginning.

## 2. Design from usage and ownership

Evaluate the ordinary caller's usage and relevant failure or state transitions.
Derive the interface and data shape from what that caller needs to
know. An interface includes ordering, errors, effects, and guarantees, not just
its function signature.

When data access drives the choice, compare representative reads, writes, updates,
and expected volume. Choose representation and ownership around those patterns;
make consequential latency, memory, and consistency tradeoffs explicit.

Put each invariant where it can actually be enforced. A small interface earns
its place by hiding useful decisions, not merely by forwarding calls. Imagine
removing a proposed boundary while preserving behavior: does complexity vanish,
or spread into callers? Preserve repository and domain terminology.

For cross-system state, trust boundaries, external dependencies, or compatibility-sensitive
migration, read the relevant section of
[Integration decisions](references/integration-decisions.md). Use it to resolve
the affected ownership and guarantees, not as a checklist for unrelated risks.

## 3. Compare credible shapes

Compare against the current shape or its smallest sound extension. Develop a
materially different option when competing designs remain credible; do not
invent alternatives just to reach a quota. Give options the same required
behavior and constraints. Different names or extra layers are not different
designs.

Evaluate credible options through the usage or change scenario that distinguishes
them. Compare caller burden, enforceable guarantees, concentration of policy,
operational consequences, and migration cost. A smaller diagram or more hidden
implementation is not enough to outweigh harder failure handling or deployment.
Treat a design from scratch as a useful comparison, not permission to rewrite.

Consider which owners must change together when a governing rule changes.
Group shared knowledge where it can remain consistent,
while preserving independent policies even when their code looks similar. Use
current requirements or known variation, not hypothetical future extensibility.

Make technical recommendations within the settled requirements. If the tradeoff
requires an unresolved product priority or a change to an accepted guarantee
that is not already authorized, present the specific choice and consequences to
its owner. Continue independent
design work while that choice is pending.

## 4. Resolve the uncertainty that could change the choice

Separate what current source establishes from an assumption needing evidence.
Prefer the cheapest observation that can distinguish viable options. A usage
sketch demonstrates clarity; it does not prove runtime behavior or performance.

When an executable experiment is needed, frame the decision, competing outcomes,
representative conditions, and the observation that would change the choice.
Use the separate `$prototype` skill when available and within the authorized
scope; its procedure owns building, observing, and cleaning up the probe. If it
is unavailable, return the framed experiment to authorized implementation for
execution with available tools. Design-only work can return the evidence gap.
Keep the recommendation conditional until the needed evidence returns. Do not
invent a substitute result or treat a successful probe as proof of production
integration.

## 5. Recommend an implementable direction

Return one recommendation, a supported retain decision, or a precise unresolved
choice. Where a credible alternative was compared, explain why it loses. State
what evidence could change the recommendation. Include a usage example when it
clarifies the choice, and the ownership, affected interfaces and guarantees,
migration and verification implications that matter for this decision. Scale the form to the problem;
reuse the caller's artifact rather than creating a mandatory design document.

Finish when the next implementer can locate the affected owners, understand the
chosen behavior, and identify what must be proved without inventing consequential
policy. Keep unresolved assumptions visible. A design-only request ends here;
already-authorized implementation can continue under its original scope.
