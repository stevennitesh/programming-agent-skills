---
name: codebase-design
description: Resolve a consequential architecture or integration question about ownership, interfaces, state, dependencies, or migration. Use when the design itself is unresolved; exclude straightforward feature implementation, repository-wide improvement discovery, and standalone runnable experiments.
---

# Codebase design

Resolve a bounded design question so implementation can proceed with the
important decisions explicit. The question may cross several systems; its
boundary follows the behavior and ownership involved, not a single file.

For a design-only request, inspect and recommend without changing product code.
When called within authorized implementation, return the decision to that work;
do not introduce another approval gate. Prototype remains a separate skill.

## 1. Locate the decision

State what must be decided and why the current shape or obvious extension is
insufficient. Trace a representative request through its real callers, owning
state, dependencies, and observable result. Read relevant accepted decisions
and contracts, distinguishing intended guarantees from accidental dependence.

For an existing design, identify a demonstrated cost: callers coordinating an
invariant, one policy changing in several places, leaked representation, or
repeated workarounds. Check sibling callers or relevant history when they could
confirm or disprove the pattern. One awkward case does not establish a systemic
problem. For new behavior, identify the new constraint that makes the choice
consequential. Retaining the current design is a valid answer.

Use audit findings as leads and recheck their decisive evidence. Repository-wide
discovery belongs to a separate audit; do not turn this decision into a full map
or require an audit report before beginning.

## 2. Design from usage and ownership

Sketch the ordinary caller's usage and the consequential failure or state
transition. Derive the interface and data shape from what that caller needs to
know. An interface includes ordering, errors, effects, and guarantees, not just
its function signature.

Put each invariant where it can actually be enforced. A small interface earns
its place by hiding useful decisions, not merely by forwarding calls. Imagine
removing a proposed boundary while preserving behavior: does complexity vanish,
or spread into callers? Preserve repository and domain terminology.

For cross-system state, external dependencies, or compatibility-sensitive
migration, read the relevant section of
[Integration decisions](references/integration-decisions.md). Use it to resolve
the affected ownership and guarantees, not as a checklist for unrelated risks.

## 3. Compare credible shapes

Compare against the current shape or its smallest sound extension. Develop a
materially different option when competing designs remain credible; do not
invent alternatives just to reach a quota. Give options the same required
behavior and constraints. Different names or extra layers are not different
designs.

Walk concrete usage through each option, including the case driving the design
question. Compare caller burden, enforceable guarantees, concentration of policy,
operational consequences, and migration cost. A smaller diagram or more hidden
implementation is not enough to outweigh harder failure handling or deployment.
Treat a design from scratch as a useful comparison, not permission to rewrite.

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
what evidence could change the recommendation. Include ownership, a usage example,
affected interfaces and guarantees, and the migration and verification
implications that matter for this decision. Scale the form to the problem;
reuse the caller's artifact rather than creating a mandatory design document.

Finish when the next implementer can locate the affected owners, understand the
chosen behavior, and identify what must be proved without inventing consequential
policy. Keep unresolved assumptions visible. A design-only request ends here;
already-authorized implementation can continue under its original scope.
