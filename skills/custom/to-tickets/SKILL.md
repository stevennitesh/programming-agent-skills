---
name: to-tickets
description: Create and publish approved, dependency-ordered ready-for-agent tickets from settled source material.
---

# To Tickets

Own one outcome: one approved, dependency-ordered graph of independently
grabbable **ready-for-agent tickets** from one bounded body of settled source,
with exhaustive coverage and one verified next action.

`docs/agents/issue-tracker.md` and its pointers own tracker transport, the
Ready-for-agent contract, roles, relationships, ready queries, packet
mechanics, and Mutation read-back. The engineering contract owns shared Source
Trace, proof-seam, and state-boundary rules. This skill owns admission,
coverage, slicing, approval, publication scope, and Return.

Admit only settled implementation source with an identifiable owner and
publication authority, stable outcome, decisions, scope, exclusions, and proof
expectations. Apply the setup gate through the target repo's `AGENTS.md`. Return
the exact `$repo-bootstrap` precondition when its tracker surface is absent or
incompatible.

## Process

### 1. Trace

Trace the complete bounded source: the request and approvals, repo
instructions, every supplied parent artifact, decision-bearing comments, and
directly required durable owners. Record source identity and owner, outcome,
accepted decisions, deferrals and rejections, scope and exclusions, evidence,
proof expectations, and material gaps.

Return one complete **source-gap packet** and stop before slicing when a missing
or conflicting decision could change intent, contracts, architecture,
supported state, migration, acceptance, proof, or scope. Leave
implementation-owned technique to implementation.

### 2. Map

Inspect repository reality only far enough to name stable seams, supported
state branches, **proof lanes**, expected production scope, overlap, migration
constraints, and durable domain, ADR, glossary, or prototype pointers.

Leave patch design, exact file selection, helpers, and test implementation to
the delivery owner. Return a source conflict rather than letting current code
silently override settled intent.

### 3. Slice

Default to one fresh-session-sized **vertical behavior slice**: one request or
behavior across the real components or concerns needed for its selected value.
Use a **tracer bullet** when the purpose is a skeletally thin real path for
early feedback or a load-bearing risk. One ticket may be both; the terms are
not synonyms.

**Local proof policy:** every ticket has observable proof through its claimed
boundary, and completion can be judged without unrelated sibling completion.
This independence is a To Tickets completion gate; it does not establish
concurrency.

Use **support slices** only when each names the delivery slice it unblocks or
materially de-risks, has its own behavior-preserving proof, is the smallest
durable enabling change, and is more economical than inclusion in that slice.

Every ticket satisfies the tracker's Ready-for-agent contract and adds:

- parent or bounded-source reference;
- work-unit form, tracer learning role when applicable, and migration phase
  when applicable;
- why this slice, what to build, and covered commitments; and
- relevant Source Trace and durable context pointers.

Acceptance names observable behavior and the highest meaningful proof seam.
Each ticket also names true blockers or `none`, expected write scope, semantic
ownership, shared resources and serial tripwires, and a scope fence. Split only
when distinct proof, authority, rollback, dependency unlock, permission, state,
migration, or ownership makes separate completion valuable; do not split by
layer, filename, team, or available agent slot.

Use a **blocking edge** only when the dependent consumes a required predecessor
outcome. Tracker order, predicted overlap, and serial tripwires are not
blockers. Keep the graph acyclic. Ready-for-agent means shaped completely, not
unblocked: the locally defined **ready frontier** is open, ready-for-agent,
unclaimed work whose true blockers are satisfied, in tracker order.

For stateful work, include the engineering contract's state-boundary matrix:
put every applicable branch and any evidenced non-applicable axis in acceptance
and its proof lane.

When a parent-delivery run is requested or at least two substantial slices may
be independent, add the execution profile: blockers, semantic owner, expected
production scope and exclusions, public proof seam and focused proof, size,
shared seam or scarce resource, and serial tripwire. Parallel eligibility
requires substantial work plus semantic, production-scope, and proof
isolation. Disjoint filenames or open slots do not establish it; uncertainty
defaults to serial. Parallel Implement owns runtime width.

For an incompatible interface, schema, client, or data change that cannot
switch atomically, use **expand-migrate-contract**: expand the compatible new
form beside the old; migrate through operable, releasable, backward-compatible
stages; contract only after old usage ends and compatibility proof passes.
Migration dependencies do not waive intermediate operability. These are
technical phases, not automatically vertical product slices.

Track **blast radius** separately through progressive exposure, health checks,
rollback proof, and stable exposure boundaries. Broadness or failed vertical
slicing is not an entry condition for compatibility migration, and exposure
boundaries do not define product-slice shape. Blast-radius gates constrain the
risk-bearing operation itself. When migration or backfill creates the risk,
run it in batches through stable exposure boundaries and require health,
compatibility, and rollback evidence before expanding from one boundary to the
next.

Apply the **coverage gate**: map every source-visible implementation commitment
and scope boundary to a ticket, an explicit deferral or exclusion, or a
no-ticket reason.

If exhaustive coverage requires no ticket, return the coverage map and
no-ticket result without approval or mutation. Otherwise Slice completes only
when every commitment has exactly one disposition, every ticket has source
justification, and the graph, predicted frontier, and applicable execution
profiles are coherent.

### 4. Approve

Present one identified proposal revision containing the Source Trace summary,
complete coverage map, ordered graph, predicted frontier, intended tracker
mutations, and every ticket's form and roles, blockers and consumed outcome,
commitments, acceptance, proof, rationale, write scope, parallel safety,
applicable execution profile and state matrix, and scope fence.

Obtain explicit approval of that exact revision before publication. A material
change to coverage, a ticket, edge, acceptance, proof, state, scope, readiness,
or relationship requires reconciliation and fresh approval. Return the complete
proposal awaiting approval when approval is absent.

### 5. Publish

Immediately before mutation, reconcile the source, proposal, tracker target,
and parent relationships. Material drift returns to Approve. Publish only the
fresh approved parent, tickets, relationships, roles, state, and packet
metadata, blockers first, through the tracker owner.

Preserve the parent's intent and lifecycle. Change its body only for approved,
tracker-required child or ordering metadata. Stop before implementation,
review, claim, or closeout.

Apply **Mutation read-back** to the parent, ordered children, bodies, roles,
state, relationships, blocking edges, affected dependents, and resulting ready
frontier. Provider receipts do not prove completion. A failed, unknown, or
mismatched mutation is blocked; return the approved revision, observed applied
and failed operations, unknown state, frontier risk, and safest non-duplicating
recovery.

For a completely verified graph, return its references, packet path when
applicable, coverage summary, ready frontier, and exactly one next action in
this priority order:

- empty frontier: resolve the named blocker;
- explicitly requested non-empty parent-delivery run: recommend
  `$parallel-implement` with the parent, regardless of initial frontier width;
- one ready ticket: recommend `$implement` for it;
- overlapping semantic ownership, production scope, public seam, fixture,
  proof resource, or serial tripwire: recommend `$implement` for the first
  ticket in tracker order;
- at least two substantial, semantically independent, production-isolated,
  proof-isolated tickets: recommend `$parallel-implement` with the parent; or
- uncertain independence or economics: recommend `$implement` for the first
  ticket in tracker order.

Recommend and stop; never begin the selected implementation route.

## Return

Return exactly one typed result: setup precondition, source-gap packet,
no-ticket result, proposal awaiting approval, partial-publication recovery, or
published graph. Each result names its evidence, unchanged or observed tracker
state, and exact safe continuation.

## Completion

Successful publication requires setup, source, coverage, proposal, approval,
freshness, publication, and read-back gates; tracker-owned readiness and this
skill's artifact fields; distinct blockers and serial constraints; applicable
state matrices and execution profiles; an exact observed graph without partial
failure; and one verified next action returned without starting it. Earlier
typed Returns are bounded stops, not successful publication.
