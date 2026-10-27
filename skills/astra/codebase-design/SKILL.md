---
name: codebase-design
description: Resolve code reuse, ownership, simplification, or integration decisions. Exclude product/domain meaning, edits with a settled design, and whole-codebase audits.
---

# Codebase design

Choose the simplest complete design for accepted behavior using existing
capabilities and enforceable ownership. Include caller transitions and retirement
of displaced paths. Design-only work returns a decision without edits; within
authorized implementation, resolve the design and continue without another
approval gate. No architecture pattern or separate design document is required.

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

Consolidate genuinely shared policy; similar-looking code may have different
semantics. Judge simplicity across callers, state, configuration, dependencies,
and maintenance. Keep boundaries that hide meaningful policy or coordination;
collapse those that merely relocate complexity. File or line counts alone do not
establish a simpler design. Ground representation choices in actual access and
material scale or consistency needs.

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

## Return an implementable decision

State the selected direction, supported retain decision, or precise unresolved
choice, with the decisive tradeoff and affected owners or guarantees. Include
caller migration, retirement, compatibility, and verification obligations, and
why any superseded path must remain. Reuse the caller's artifact. For requested
durable capture, use shape-work's
[Domain meaning and decision records](../shape-work/references/domain-modeling.md)
without another feature interview. Stop at the design-only endpoint or resume
already-authorized implementation.
