---
name: ticketing
description: Assess or reconcile tracker work, or turn accepted ideas into bounded tickets. Explicit requests only; excludes implementation, deep diagnosis, and code review.
---

# Ticketing

Prepare and reconcile tracked work under the repository's conventions. Select
the requested effects: assessment stays read-only; cleanup permits supported
corrections; decomposition produces drafts or authorized publication. These are
independent modes, not stages. Assessment or cleanup does not authorize creating
new work, and ticketing grants no implementation or concurrent execution authority.

## Establish scope and tracker meaning

Identify the selected items or accepted source, requested result, and authorized
effects. Preserve unrelated content, active claims, and assignments. Coordinate
changes to accepted scope or live ownership with the execution owner.

Follow configured categories, states, hierarchy, relationships, readiness, closure,
and role cardinality. Include PRs/MRs only when configured as tracked work. Do not
infer the tracker from Git hosting or invent a taxonomy/replacement. Missing
preferred guidance alone is no blocker when conventions are available elsewhere;
unresolved setup leaves a useful draft or a gap for dependent mutations. Recommend
[context-hygiene](../context-hygiene/SKILL.md) for stale guidance or
[repo-bootstrap](../repo-bootstrap/SKILL.md) for requested setup/migration.

Use [Work-item brief](references/work-item-brief.md) for actionable context and
readiness. A closed predecessor is insufficient: establish its actual result,
permissions, and resolved gates. Drafts may retain blockers; do not call them ready.

## Assess or reconcile existing work

Use [Attention scan](references/attention-scan.md) for a queue overview. Inspect
decision-bearing content, state, relationships, ownership, and current evidence
for selected items. Directed dispositions need only investigation that can expose
policy, dependency, or ownership conflicts; do not label them verified completion.

Use acceptance, code, discussion, delivered results, and bounded checks to support
missing information, actionable work, blockers, completion, duplication, or
authorized rejection. Age, silence, failed reproduction, or missing evidence alone
proves none of these. Preserve uncertainty and ask only for consequential missing
facts or owner-held decisions, continuing independent work.

Completion requires actual outcomes and verification; account for required children
and combined properties before parent closure. For duplication or supersession,
preserve unique requirements/evidence at the survivor and repair relationships
before closure can falsely unblock dependents. Reuse later delivered evidence
even when an old description omits it. A finding may call for diagnosis, review,
shaping, or decomposition; identify that next action without starting it unless
already authorized. No change may be the correct assessment result.

## Decompose accepted work

A clear idea can go directly to tickets without prior assessment, shaping, or a
formal spec. Recover outcome, scope, acceptance, rationale, constraints, and open
decisions without inventing product policy. Use [shape-work](../shape-work/SKILL.md)
for unsettled meaning and [codebase-design](../codebase-design/SKILL.md) for a
technical choice preventing a useful boundary; decompose independent settled work.

Inspect equivalent existing work for reuse. Give each ticket a coherent outcome
with checkable completion. Split for useful ownership, predecessor results,
independently verifiable enabling work, real migration sequencing, or learning
that changes later decisions. Avoid artificial schema/API/UI slices, compatibility
added only for ticketing, and fragmentation that hides unfinished integration.
One ticket may suffice. Include necessary setup, docs, tests, caller transitions,
and retirement; leave methods and local implementation choices open unless binding.

For cross-ticket composition, migration, or plan-changing learning, read
[Delivery boundaries](references/delivery-boundaries.md). Name predecessor results
and observable unblock conditions. Preferred order and mutable-resource overlap
are coordination constraints, not automatically dependency edges. Assign each
delivery-changing commitment an owner and cross-ticket proof to its first consumer.

Check missing commitments, duplicates, cycles, unknown blockers, and a truthful
starting set. Show potential parallel work without fixed waves or worker counts;
[parallel-implement](../parallel-implement/SKILL.md) owns live independence,
scheduling, custody, execution, and parent closeout when requested.

## Publish only authorized effects and return

Return the requested assessment or draft, or apply authorized corrections and
publication through [Tracker publication and repair](references/tracker-publication.md).
That reference supplies mutation mechanics, not additional scope. Verify actual
content, identities, relationships, readiness, and ownership rather than intended
writes; recover uncertain effects from observed state without blind replay.

Report verified changes or recommendations, unchanged/unresolved items,
unexamined scope, decisive evidence, and remaining blockers or recovery needs.
Partial coverage cannot establish whole-queue reconciliation. Continue downstream
work only under existing authority and its owner; ticket publication does not
grant human-action, execution, parent-closeout, or Git-commit authority.
