---
name: to-tickets
description: Turn specs or sufficiently clear ideas into bounded delivery tickets with acceptance and dependencies. Use only for explicit ticketing requests.
---

# To tickets

Turn shaped work, specifications, or sufficiently clear ideas into cohesive,
bounded tickets that a fresh agent can understand, implement, and verify. Preserve
accepted meaning and use the repository's established tracking method. Ticketing
does not itself authorize implementation or concurrent execution.

## Establish context and tracking conventions

Recover the intended outcome, scope, constraints, acceptance, rationale, and
remaining consequential decisions from the conversation, specification, audit
direction, or other supplied source. A formal specification or prior shaping
session is not required when the idea is sufficiently clear.

Locate repository tracking guidance and follow its configured project or local
path, ticket format, hierarchy, dependency representation, and readiness
conventions. Inspect relevant existing work so equivalent tickets can be reused.
Do not infer the tracker solely from Git hosting or invent a replacement when
setup is missing; leave a useful draft and identify the publication gap.

Do not reopen settled requirements during decomposition. If creating a ticket
would require inventing consequential product meaning, use
[shape-work](../shape-work/SKILL.md) for that unresolved behavior. Keep affected
work conditional while decomposing independent settled work. Resolve routine
decomposition choices without requiring another planning phase.

For one coherent outcome with no useful ownership or dependency handoff, return one
bounded work item rather than manufacturing a graph.

## Choose bounded delivery outcomes

Each ticket should give one agent a coherent assignment with a clear completion
boundary and independently checkable outcome. Balance avoiding fragmentation with
keeping assignments manageable; minimizing ticket count is not the objective.
Split when a boundary provides useful ownership, a required predecessor result,
independently verifiable enabling work, migration sequencing, or learning that
changes later decisions. Use affected code and existing ownership to ground the
boundaries where needed.

Keep a coherent path together when splitting would manufacture temporary
compatibility, hide unfinished integration, or create schema/API/UI tickets that
are not useful on their own. Include supporting setup, documentation, tests, caller
transitions, and cleanup made necessary by the outcome within its scope.

For wide changes, cross-ticket integration, migration, or learning that can revise
later work, read [Delivery boundaries](references/delivery-boundaries.md).

## Give a fresh agent sufficient context

Write for an implementer without the original conversation. Include applicable
decision-bearing context in the repository's format; no universal ticket template
is required:

- the bounded outcome and why it matters;
- scope, exclusions, preservation requirements, and consequential constraints;
- accessible source pointers and relevant code owners, interfaces, or decisions;
- observable acceptance and the evidence needed to establish it;
- required predecessor results and unresolved human or permission gates; and
- binding implementation choices, distinguished from suggestions and open choices.

A parent ticket or specification can hold the overall idea. Give children precise
section references and enough local context to act; identify the accepted revision
when source changes could alter the assignment. Capture decisive facts from a
transient conversation in the ticket or its accessible shared source. Verify that
the reading path supplies the assignment without requiring the original chat or
guessing which parts of a broad source apply.

Leave tools, techniques, local design, and implementation sequencing to the worker
within those constraints. Suggested mechanisms do not become binding merely by
being included in a ticket.

Preserve distinguishing inputs, states, results, metrics, thresholds, baselines,
or operating conditions when they are necessary to prevent a plausible wrong
implementation from satisfying generic wording.

## Describe dependencies and potential parallel work

For each dependency, name the predecessor, its required result, and the condition
that makes the dependent actionable. A closed predecessor alone does not establish
that its result is accepted and integrated or otherwise available to the consumer.
Keep unresolved decisions and permission gates explicit.

A blocking edge represents a required predecessor outcome. Record preferred order
and known shared-file or resource conflicts separately, so they do not create
false prerequisites. Give each delivery-changing commitment an owner and put
cross-ticket proof at the first consumer that can lose the produced meaning.

Read the resulting graph for missing commitments, duplicate work, cycles, unknown
blockers, and a truthful starting set. Show which tickets can start now and which
outcomes unlock later work. Identify potential parallel work and known coordination
constraints without prescribing fixed waves or worker counts. Readiness means
prerequisites are resolved; [parallel-implement](../parallel-implement/SKILL.md)
owns live independence, resource ownership, and scheduling when requested.

## Deliver the requested draft or published graph

Return the outcomes, acceptance, dependencies, gates, source relationship, and
potential parallel work in the requested form. Do not copy the
whole source into every ticket when a stable pointer plus compact local context is
sufficient.

When durable tracker publication or repair is requested, read
[Tracker publication](references/tracker-publication.md). A request to create or
publish tickets authorizes those requested tracker effects within repository
policy; a draft or read-only request stays within that boundary. Invoking the
skill alone does not authorize unspecified tracker mutations.

Complete when the requested draft exists or the published graph has been verified
and its concrete identities, dependencies, actionable starting work, unresolved
gates, and material limits are known. Ticketing stops with that result;
implementation, worker spawning, delivery, and parent closeout belong to the
calling workflow and their existing authority.
