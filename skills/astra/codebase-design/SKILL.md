---
name: codebase-design
description: Resolve a consequential technical architecture or integration decision. Exclude product/domain meaning, routine implementation, and whole-codebase audits.
---

# Codebase design

Resolve a bounded architecture decision so implementation does not have to invent
consequential ownership, interface, state, compatibility, or operational
guarantees. The boundary follows the behavior and owners involved, not a file or
module count.

For a design-only request, inspect and recommend without changing product code.
When design is part of already-authorized implementation, return the decision to
that work without adding another approval gate.

Design is complete when implementation can proceed with the affected owners,
guarantees, and proof clear enough that it does not need to invent consequential
architecture policy.

## 1. Establish the design pressure

Identify the unresolved decision and the accepted requirement or uncertainty that
makes it consequential. Determine first whether the current design or its smallest
sound extension already satisfies the need.

Inspect enough of the real callers, owners, state, and dependencies to establish
the affected boundary and distinguish intended guarantees from accidental
dependence. Do not turn a bounded design question into a repository-wide map.

Require demonstrated pressure before recommending redesign: an unmet requirement
or a concrete cost such as duplicated policy, caller-coordinated invariants,
representation leakage, repeated workarounds, or a guarantee the current owner
cannot enforce. One awkward caller or isolated exception does not establish a
systemic architecture problem. Retaining the current design is a valid result.

Treat audit findings as leads rather than proof. Reuse evidence while its relevant
code, inputs, dependencies, and environment remain applicable.

## 2. Design around callers and enforceable ownership

An interface is the behavior callers rely on, including relevant errors, ordering,
effects, state transitions, and guarantees, not merely a function signature.

Choose ownership and boundaries around the required behavior and actual operating
conditions. Put an invariant where an owner can enforce it. Do not add stronger
recovery, isolation, compatibility, or scale guarantees than supported workflows
require.

A boundary earns its place when it hides meaningful policy, state, external
translation, or coordination. If removing it eliminates complexity, collapse it;
if removing it merely spreads that complexity into callers, the boundary may be
useful.

When representation is the decision, ground it in the real access pattern and
material scale or consistency requirements rather than hypothetical future use.

For cross-system state, trust boundaries, external dependencies, or
compatibility-sensitive migration, read the relevant section of
[Integration decisions](references/integration-decisions.md). Use only the branch
that can change the decision.

## 3. Resolve the choice with proportionate evidence

Use the current design or its smallest sound extension as the baseline. Compare
another shape only when a materially different option remains credible. Evaluate
credible alternatives under the same accepted behavior and constraints, focusing
on the tradeoff that actually distinguishes them, such as caller burden,
enforceable guarantees, operational consequences, or migration cost.

Resolve technical design choices within settled requirements. Return to a product
or domain decision owner only when the choice would change accepted behavior,
scope, risk tolerance, or another owner-held guarantee.

When the decision depends on an empirical fact the current evidence does not
establish, keep the recommendation conditional and use
[prototype](../prototype/SKILL.md) to obtain the smallest observation capable of
distinguishing the options. Prototype evidence supports only the property and
conditions it actually exercised; it does not prove production integration.

Keep unresolved assumptions explicit rather than filling them with plausible
architecture.

## 4. Return the implementable decision

Return the selected direction, a supported retain decision, or the precise
unresolved choice. State the decisive tradeoff and the affected owner, interface,
or guarantee. Include migration or verification implications only when they
matter to this decision.

Reuse the caller's artifact when one already exists; no design document is
required merely because design work occurred.

Finish when implementation can proceed without inventing consequential
architecture policy and can identify the owners, guarantees, and proof that matter.
A design-only request ends here; already-authorized implementation may continue
within its original scope.
