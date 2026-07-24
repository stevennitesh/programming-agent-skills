---
name: to-tickets
description: Create dependency-ordered ready-for-agent tickets from settled source material.
---

# To Tickets

Transform one bounded packet of settled source into an exhaustive,
dependency-ordered set of **Ready-for-agent tickets**.

Admit only an explicit request to slice settled source. Preserve the source
owner's outcome, commitments, acceptance, scope, exclusions, domain meaning,
and Source Trace. Leave product decisions, parent-spec creation, raw-intake
triage, implementation, parent delivery, worker dispatch, closeout,
installation, and Git delivery to their owners.

`docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md` own tracker
transport, relationships, roles, lifecycle mappings, and Mutation read-back.
The engineering contract owns shared Source Trace, proof, and state-boundary
semantics. This skill owns slicing, coverage, blocker order, ticket readiness,
execution profiles, publication scope, and Return.

## Shape

Apply the setup gate through the target repository's `AGENTS.md`. Load the
routed tracker, label, domain, and engineering contracts. When a required
surface or operation is missing or incompatible, name it, recommend
`$repo-bootstrap`, preserve source and tracker state, and stop before tracker
access or mutation.

Read the complete supplied source packet and every decision-bearing pointer.
Record its identity and owner, accepted decisions, commitments, deferrals,
exclusions, domain terms, proof seams, and unresolved but nonblocking notes.
When a missing or conflicting decision could change a commitment, return that
decision and every affected slice without mutation. Leave implementation
technique to the delivery owner.

Build an in-memory commitment ledger and exhaustive slice graph. Account for
every source-visible implementation commitment and scope boundary as ticket
acceptance, an explicit deferral or exclusion, or a no-ticket reason.

Prefer one independently completable vertical behavior slice. Admit a support
slice or migration stage only when it has observable proof and names the
behavior slice, compatibility obligation, or risk it unlocks. Split only when
separate proof, authority, rollback, dependency unlock, permission, state,
migration, or ownership makes separate completion valuable.

Give every ticket:

- one bounded slice and work-unit form, including any learning or migration
  role;
- its parent or bounded-source reference and relevant Source Trace pointers;
- observable desired behavior, edge and error cases, and acceptance;
- relevant seams, expected durable write scope, and a scope fence;
- dependency state, true blockers or `none`, and stable tracker order;
- proof lane plus verification authority and evidence; and
- a parallel-safety judgment.

Every ticket must also satisfy the configured tracker's Ready-for-agent
contract. Keep a ticket unready and return all defects when any required
acceptance, blocker, proof, scope, or verification fact is missing.

Derive a blocking edge only when the dependent consumes a required predecessor
outcome. Detect cycles, missing edges, contradictory order, and nodes made
falsely ready by unresolved blockers. Tracker order and serial constraints are
not blockers. The ready frontier is open, ready-for-agent, unclaimed work whose
true blockers are satisfied, in tracker order.

Give every ticket an execution profile covering semantic ownership, expected
production writes, proof seams and scarce proof resources, ordering, serial
tripwires, and evidenced independence or serialization. Treat expected write
overlap, shared proof resources, trust boundaries, migrations, cutovers,
permissions, protected data, irreversible state, and uncertain independence as
serial constraints.

For each stateful ticket, include the applicable state-boundary matrix:
absent or initial state, current reusable state, legacy or incompatible state,
public access paths, supported variants, and relevant lifecycle transitions,
reduced to distinct supported branches and high-risk interactions. For a
stateless ticket, record `not applicable` and the reason.

For an incompatible interface, schema, client, or data change that cannot
switch atomically, use expand-migrate-contract: expand a compatible new form,
migrate through operable and releasable stages, then contract only after old
usage ends and compatibility proof passes.

If exhaustive coverage justifies no implementation ticket, return the complete
coverage result, preserve tracker state, recommend `none`, and stop.

## Publish

Apply the configured `ready-for-agent` state only after a ticket passes every
ready gate. Apply a category role only when settled source authorizes it.

Freeze and audit the complete commitment ledger, ticket bodies, graph, stable
order, predicted frontier, roles, readiness, execution profiles, state
matrices, and intended mutations before external mutation. Publish only a
complete non-contradictory design. Through tracker-owned operations, create the
items first, then apply parent and dependency relationships, authorized roles,
and mapped state. Preserve the parent as intent owner and do not fabricate a
parent for authorized standalone tickets.

Refetch every created or changed item and every affected dependent. Verify the
exact body, relationships, roles, assignee, status, and resulting frontier.
A failed, unknown, or mismatched mutation returns applied operations, failed
operations, affected dependents, observed frontier, and the safest recovery;
claim no complete graph.

## Return

Return exactly one typed result: setup precondition, source-gap packet,
no-ticket coverage result, consumer repair packet, partial-publication
recovery, or published graph. Each result names its evidence, unchanged or
observed tracker state, gaps, and exact safe continuation.

A published graph includes the source or parent, ordered ticket references,
coverage map, dependency graph and frontier, execution profiles, applicable
state matrices, and mutation read-back. Recommend exactly one next owner:

- `$parallel-implement` only when the user explicitly requested top-level
  delivery of the verified parent and its non-empty exhaustive graph;
- `$implement` for a single ready item or the first ready item in tracker order
  when overlap, a serial tripwire, uncertainty, or uneconomic parallel
  dispatch requires serial work; or
- `none` when neither delivery relationship applies.

Recommend and stop without invoking the owner.

Complete only when source is settled; every commitment has a disposition;
every ticket passes Ready-for-agent; the graph, profiles, and applicable
matrices are complete and non-contradictory; every authorized mutation and
affected relationship reads back; the frontier is truthful; and one
recommendation or `none` is returned without starting it.
