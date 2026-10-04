---
name: codebase-design
description: Resolve code reuse, ownership, simplification, or integration decisions. Exclude product/domain meaning, edits with a settled design, and whole-codebase audits.
---

# Codebase design

Choose the simplest complete design for the accepted behavior, grounded in
existing capabilities and clear ownership. Resolve how affected callers move and
what superseded code can be retired. The boundary follows the behavior and owners
involved, not a file or module count. Choose the investigation and design methods
for the decision; no architecture pattern or formal design phase is required.

For a design-only request, inspect and recommend without changing product code.
When design is part of already-authorized implementation, return the decision to
that work without adding another approval gate.

## 1. Establish the design pressure

Identify the unresolved decision and the accepted requirement or uncertainty that
makes it consequential. Determine first whether the current design or its smallest
sound extension already satisfies the need.

Before proposing another implementation, inspect relevant existing capabilities
and their real callers, owners, state, and dependencies. Prefer extending or
consolidating a suitable owner; identify the material mismatch when a separate
implementation is justified. Distinguish intended guarantees from accidental
dependence. Keep this investigation bounded to the decision rather than mapping
the whole repository.

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

Organize code around cohesive responsibilities and useful local conventions.
Consolidate genuinely shared behavior and policy at a clear owner. Similar-looking
code can have different semantics; keep those responsibilities separate when
sharing would couple unrelated concerns or spread exceptions into callers.

Before strengthening shared validation, inspect its real callers and distinguish
integrity checks from operation-specific eligibility. If it reads persisted
artifacts, state which existing artifacts remain readable and which require
migration before new execution. Identify a focused regression test through the
affected caller that distinguishes those obligations.

Judge simplicity across the whole change: caller burden, dependencies, state,
configuration, indirection, and maintenance. Additional machinery should serve a
current requirement or concrete benefit. A boundary earns its place when it hides
meaningful policy, state, external translation, or coordination. Collapse it when
doing so removes complexity; retain it when removal merely spreads complexity
into callers. Fewer files or lines alone do not establish a simpler design.

When representation is the decision, ground it in the real access pattern and
material scale or consistency requirements rather than hypothetical future use.

For cross-system state, trust boundaries, external dependencies, replacement, or
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
establish, identify the missing observation and its effect on the recommendation.
Use [prototype](../prototype/SKILL.md) when an authorized experiment can resolve it.
Prototype evidence supports only the property and conditions it actually
exercised; it does not prove production integration.

Keep unresolved assumptions explicit rather than filling them with plausible
architecture.

## 4. Return the implementable decision

Return the selected direction, a supported retain decision, or the precise
unresolved choice. State the decisive tradeoff and the affected owner, interface,
or guarantee. Include caller transition, retirement, and verification obligations
when they matter to this decision, including why any superseded path must remain.

Reuse the caller's artifact when one already exists; no design document is
required merely because design work occurred. When the request includes durable
decision capture, use shape-work's
[Domain meaning and decision records](../shape-work/references/domain-modeling.md)
for the settled rationale and applicability without another feature interview.

Finish when implementation can proceed with the owners, guarantees, necessary
transition and cleanup, and decisive verification clear enough to act on.
A design-only request ends here; already-authorized implementation may continue
within its original scope.
