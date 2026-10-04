---
name: triage
description: Assess and reconcile requested tracker intake or backlog against current evidence. Exclude implementation, deep diagnosis, and code review.
---

# Triage

Assess and reconcile a requested set of tracked work using current evidence and
the repository's tracking conventions. Cover new intake and existing backlog,
including stale status, missing context, duplicates, superseded work, dependencies,
and apparently completed items. Choose investigation depth, ordering, grouping,
and tools for the task; leave each assessed item with a supported disposition or
an explicit uncertainty and next owner.

## Establish scope and tracker meaning

Identify the requested items or queue, whether the task is assessment or cleanup,
and the tracker effects already authorized. Overviews and read-only audits return
findings. An explicit cleanup request authorizes the routine tracker corrections
it encompasses within repository policy, without approval for every item. It does
not authorize unrelated housekeeping or implementation.

Locate the established tracker guidance, category/state mappings, relationships,
readiness, and closure conventions wherever the repository keeps them. Follow
configured invariants, including role cardinality when specified; do not impose
another taxonomy. A missing preferred document alone does not block work when the
needed contract is established elsewhere. Include PRs or MRs only when configured
as tracked work for this purpose.

For missing or stale guidance about an established tracker, recommend
[context-hygiene](../context-hygiene/SKILL.md); for needed setup or migration,
recommend [repo-bootstrap](../repo-bootstrap/SKILL.md). Block only mutations that
depend on an unresolved convention and continue independent assessment or cleanup.
Do not force a blocked item into a misleading state to work around a mapping gap.

For a queue overview or broader cleanup, read
[Attention scan](references/attention-scan.md). For selected items, inspect the
body, decision-bearing discussion, current state, relevant relationships, active
ownership, and useful attachments.

When the user names an exact disposition, skip investigation that cannot change
that instruction. Inspect enough to identify concrete conflicts with dependencies,
ownership, or tracker policy, and distinguish a directed disposition from verified
completion. Do not fabricate evidence to justify the requested state.

## Establish a supported disposition

Use code, discussions, prior fixes, accepted requirements, and bounded safe checks
as needed to distinguish missing information, actionable work, unresolved gates,
completion, duplication, or an authorized rejection. Translate the conclusion
into the configured tracker model. Keep observations separate from hypotheses.

Age, inactivity, failed reproduction, or insufficient evidence alone does not
establish that a request is invalid, completed, or no longer wanted. Ask only for
missing facts or owner-held decisions that can change the disposition, preserving
what is already known. An item may need no change after assessment.

Before treating work as completed, compare current acceptance with the actual
implementation and applicable verification. For a parent, account for required
children and properties of their combined result. A merged PR, closed children,
or stale completion claim alone may not establish the requested outcome. Do not
recreate work solely because an old description omits later delivered results.

For duplicates or superseded work, identify the surviving item or governing
decision and preserve unique requirements and evidence. Reconcile affected
relationships within authority so closure does not expose dependents as ready
while their required result remains unavailable.

Preserve active claims and unrelated content. Coordinate with the execution owner
before rewriting active assignments, releasing claims, or changing the accepted
scope of ongoing work. A stale-looking record does not establish abandoned custody.

## Make the next action usable

Before marking work ready, establish one bounded actionable outcome, sufficient
context, and resolved consequential decisions, permissions, and prerequisites.
Read [Ready brief](references/ready-brief.md) for that handoff. A closed predecessor
alone does not prove its required outcome is available; a human handoff must name
an action that person can actually take.

When an item needs deep causal investigation, fixed-candidate review, consequential
product decisions, or several implementation slices, identify the next owner and
recommend [diagnosing-bugs](../diagnosing-bugs/SKILL.md),
[change-review](../change-review/SKILL.md), [shape-work](../shape-work/SKILL.md), or
[to-tickets](../to-tickets/SKILL.md) as applicable. Keep the unresolved item honest
and continue independent cleanup. Triage does not itself start those workflows.

## Apply and verify authorized corrections

Prepare the concrete content, state, relationship, and ownership effects needed
for each correction. Preserve configured invariants and existing authority; ask
only for a consequential decision or additional effect the task does not cover.

Refresh relevant state before writing when intervening activity can affect the
decision, or use supported conditional writes against the inspected version.
Reconcile material drift instead of overwriting it. Choose individual, batched,
or atomic operations according to tracker capabilities and repository policy.
Honor actual ordering requirements: required context and prerequisites must be
established before readiness, and relationship repairs must prevent false
unblocking during closure. No fixed comment/label/closure recipe is required.

Read back changed content, states, relationships, and ownership as required by
repository policy. After a partial or uncertain result, inspect actual state before
dependent writes or retries. Resume from confirmed effects without duplicating
comments or changes that succeeded. Claim completion or rollback only when the
observed tracker state supports it. Add attribution only when policy requires it.

## Return a clear cleanup result

Complete when the requested set has been assessed and authorized corrections are
verified, or remaining gaps are explicit. Distinguish changed, recommended,
unchanged, unresolved, and unexamined work in a useful format, with decisive
evidence, material uncertainty, next owners, and recovery actions where needed.
State coverage limits for a bounded scan or unavailable data; do not imply the
whole backlog was reconciled. Continue already authorized downstream work only
under its owning workflow and scope.
