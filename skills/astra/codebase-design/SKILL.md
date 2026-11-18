---
name: codebase-design
description: Choose or simplify a technical design when ownership, interfaces, dependencies, reuse, or migration materially affect the work. Exclude product and domain decisions, settled implementation, and whole-codebase audits.
---

# Codebase design

Choose the simplest complete design that preserves accepted behavior. Use the
repository's existing capabilities and put each guarantee where it can be enforced.

## Establish the decision

Identify the accepted requirement or concrete cost driving the choice. Inspect
existing capabilities and their actual callers, state, and dependencies before
proposing another implementation. Use the current design or smallest sound
extension as the baseline. A retain decision is valid; one awkward caller or an
audit suggestion alone does not prove a systemic problem.

Distinguish required guarantees from accidental dependence. An interface includes
errors, ordering, effects, state transitions, and supported behavior, not just its
signature. Put invariants where an owner can enforce them under real operating
conditions. Stronger recovery, compatibility, or scale guarantees need a supported
workflow requirement.

## Choose ownership and evidence

Trace a real caller through the proposed boundary. When it can change the choice,
walk through a consequential failure or the next realistic change. See where the
rule is enforced, which details callers still have to coordinate, and where
changes would land. Favor a boundary that reduces coordination across the system
and preserves caller behavior. Similar code can have different policies. Ground
representation choices in actual access and material scale or consistency needs.

Before strengthening shared validation, inspect its real callers and distinguish
integrity checks from operation-specific eligibility. If it reads persisted
artifacts, state which existing artifacts remain readable and which require
migration before new execution. Identify a focused regression test through the
affected caller that distinguishes those obligations.

Compare credible alternatives under the same accepted behavior, focusing on the
tradeoff that changes the decision; do not manufacture alternatives. Use the
relevant [Integration decisions](references/integration-decisions.md) branch for
cross-system state, trust boundaries, external interfaces, replacement, or
compatibility-sensitive migration.

Reuse still-valid evidence. When an empirical fact remains unknown, identify the
deciding observation and use [prototype](../prototype/SKILL.md) within authority.
Its result proves only the conditions exercised. Return to the product/domain
owner only when the choice would change accepted behavior, scope, risk tolerance,
or another owner-held guarantee; keep unresolved assumptions explicit.

## Use or return the decision

During authorized implementation, apply the decision and continue. Surface a
decisive tradeoff or material assumption in the task's normal response. For a
design-only request, return the recommendation, case for retaining the current
design, or exact unresolved choice, with the reason and affected guarantees.
Keep implementation edits within separately authorized work.
Include migration, retirement, compatibility, or verification details where they
affect the decision or delivery. If a superseded path must remain, say why.

Reuse the caller's artifact. For requested durable capture, use shape-work's
[Domain meaning and decision records](../shape-work/references/domain-modeling.md).
