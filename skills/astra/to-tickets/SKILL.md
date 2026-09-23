---
name: to-tickets
description: Draft, publish, or repair delivery tickets from settled work, with acceptance and real dependencies. Use only for explicit ticketing requests.
---

# To tickets

Turn settled work into the fewest useful delivery units without changing its
accepted meaning. Ticket boundaries describe ownership and predecessor outcomes;
they do not authorize implementation or predict safe runtime concurrency.

## 1. Establish the accepted source

Recover the settled outcome, scope, constraints, acceptance, source rationale, and
remaining owner-held decisions from the supplied conversation, specification,
audit direction, or other accepted source.

Do not reopen settled requirements during decomposition. If creating a ticket
would require inventing consequential product meaning, preserve that decision as a
gate and continue decomposing independent settled work.

For one coherent outcome with no useful ownership or dependency handoff, return one
bounded work item rather than manufacturing a graph.

## 2. Choose meaningful delivery boundaries

Create the fewest tickets that each deliver a cohesive, independently checkable
outcome. Split when a boundary provides useful ownership, a required predecessor
result, independently verifiable enabling work, migration sequencing, or learning
that changes later decisions.

Keep a coherent path together when splitting would manufacture temporary
compatibility, hide unfinished integration, or create schema/API/UI tickets that
are not useful on their own. Fold setup, documentation, and tests into the outcome
they support.

For wide changes, cross-ticket integration, migration, or learning that can revise
later work, read [Delivery boundaries](references/delivery-boundaries.md).

## 3. Preserve meaning and real dependencies

Each ticket must give a fresh implementer the decision-bearing context it cannot
safely infer:

- why the outcome belongs in the accepted result;
- a source pointer;
- settled scope and consequential constraints;
- observable acceptance;
- required predecessor results or human/permission gates; and
- any source mechanism that is genuinely binding rather than merely suggested.

Preserve distinguishing inputs, states, results, metrics, thresholds, baselines,
or operating conditions when they are necessary to prevent a plausible wrong
implementation from satisfying generic wording.

A dependency edge means that a predecessor outcome is required, not that one item
is preferred first or may touch overlapping files. Give each delivery-changing
commitment an owner and put cross-ticket proof at the first consumer that can lose
the produced meaning.

Read the resulting graph for missing commitments, duplicate work, cycles, unknown
blockers, and a truthful starting set. Readiness means prerequisites are resolved;
it does not establish that ready tickets can execute concurrently.
[parallel-implement](../parallel-implement/SKILL.md) owns that live independence
and resource-ownership check.

## 4. Draft or publish

Return the proposed outcomes, acceptance, dependencies, gates, and source
relationship in the conversation or requested draft artifact. Do not copy the
whole source into every ticket when a stable pointer plus compact local context is
sufficient.

When durable tracker publication or repair is requested, read
[Tracker publication](references/tracker-publication.md). Missing tracker setup
blocks publication, not production of a useful draft. Invoking this skill does not
by itself authorize tracker mutation.

Complete when the requested draft exists or the published graph has been verified
and its concrete identities, dependencies, actionable starting work, unresolved
gates, and material limits are known. Ticketing stops with that result;
implementation, worker spawning, delivery, and parent closeout belong to the
calling workflow and their existing authority.
