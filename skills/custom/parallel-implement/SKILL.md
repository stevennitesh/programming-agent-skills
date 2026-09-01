---
name: parallel-implement
description: Deliver one explicitly requested fixed set of two or more accepted implementation items with concurrent workers when their ownership and write effects are independent. Root-only; exclude shaping vague work or implementing one item.
---

# Parallel Implement

**Admit -> Isolate -> Dispatch -> Land -> Prove -> Finish**

Deliver one fixed set of accepted implementation items. Parallelism is useful
only when independent work saves more time than coordination costs. One root
integrator owns scheduling, landing, and the final outcome. Each worker owns
one bounded item.

## Admit

Run only at the top-level root after an explicit request to deliver at least
two accepted items with a non-empty ready frontier. The set may be one complete
tracker-backed parent graph or another caller-owned fixed delivery scope. For
a one-item scope, return it with a recommendation that the user invoke
`$implement`. Send vague work, unsettled meaning, or missing
dependencies back to its owner or `$to-tickets` before mutation.

Pin a clean integration `HEAD`. For a complete tracker-backed parent graph,
read [Tracker Delivery](references/TRACKER-DELIVERY.md) and follow its admission
and closeout rules. Direct work creates no tracker state.

Derive the ready frontier from dependencies whose changes are already
integrated. Admit concurrent siblings only when their behavior ownership,
proof, and write effects are independent. Account for shared schemas, callers, fixtures,
configuration, generated destinations, databases, ports, package environments,
external services, and other mutable resources. File separation alone does
not prove independence. Serialize when either item can change the other's
accepted behavior or proof. First remove unnecessary sharing when natural
ownership can give the items independent outputs. Otherwise assign one
exclusive owner to shared behavior or a shared writable resource, or run the
affected items serially.

Pin every writable Git repository independently. Give each worker exclusive
custody of its mutation domains and at most one writable Git repository. Return
an item that must change multiple repositories for cohesive reslicing or
separate serial implementation before admitting the campaign. Keep installed
packages, user-level destinations, and external systems with the serial root
after repository work. The worker returns the final state of each assigned
domain; the root reads back each named landing or rollback before marking the
item landed. Apply external read-back and partial-effect recovery only when
their contract triggers.

Run a shared enabling refactor before dependent slices when that preserves the
real design better than artificial file boundaries. Keep only enough workers
active for the root to inspect and land their returns promptly.

## Isolate

Choose isolation for the current ready frontier, not the campaign. When one
item is ready and no other writer is active, give its worker the integration
checkout under exclusive custody. Do not create a lane because later
descendants may run concurrently. When two or more admitted writers can
overlap, read [Agent Lanes](references/AGENT-LANES.md) and give each writer a
distinct helper-created worktree at current integration `HEAD`. Siblings
admitted from one frontier share that exact base; a dependent item starts only
after its predecessors land and therefore uses the newer `HEAD`. Root landing
and direct serial implementation never overlap.

Use one fresh worker per item. Give it the exact checkout, base, scope, allowed
writes, acceptance, predecessor outcomes, proof, assigned exclusive resources,
and prohibited external effects. For a concurrent lane, also give it the full
helper-returned lane packet and treat every absolute runtime path in its
manifest as part of the lane contract. Point to
accessible specifications, tickets, research, and predecessor commits instead
of copying them; include only context the worker cannot recover from those
sources.

## Dispatch

Require the worker to verify its assigned worktree and exact base before its
first mutation and to run every repository and Git command there. Concurrent
workers do not stash, switch or rebase shared branches, mutate shared refs,
change tracker state, land commits, or dispatch successors.

Each worker implements its bounded item, runs focused proof, makes one task
commit, and returns the commit, changed scope, exact proof commands and results,
material skips, and blocker if one remains. For a
concurrent lane, the root runs the helper's inspection operation. For a serial
worker, it verifies the integration checkout in place. Reject off-contract
runtime use when it can change repository bytes, shared state, cleanup, or the
truth of proof. Worker prose is evidence, not state.

Send an actionable item-local gap back to the same worker while its lane is
safe. Silence or a missed checkpoint triggers inspection, not another worker.
Before replacement, stop the prior actor and confirm it stopped. Inspect a
concurrent lane and commit with the helper; inspect a serial worker's
integration checkout in place. Never run two actors on one item.

## Land

When a serial worker commits in the integration checkout, that commit is
already landed. Reacquire custody and verify current `HEAD`, the commit, diff,
scope, and proof in place. Do not reapply the commit or perform lane cleanup.

Verify and land accepted worker commits one at a time. After each landing,
read back integration `HEAD`, inspect the resulting diff, run proof invalidated
by that transition or explicitly required by policy at that transition,
recompute the ready
frontier, and dispatch another independent item without waiting for a batch.
Preserve each lane commit as an ancestor of integration `HEAD`. Fast-forward
when integration `HEAD` still equals the lane base; merge later independent
siblings. Do not cherry-pick lane commits. Cleanup uses ancestry as integration
proof.

When behavior depends on repository bytes or generated identities, checkout
normalization invalidates lane proof. Rerun that proof in the integration
checkout after landing.

When integration `HEAD` advanced since dispatch:

- Merge the lane commit when the intervening changes do not touch the item's
  behavior owner, inputs, callers, fixtures, configuration, resources, or proof.
- Return the same worker to update from current `HEAD` and rerun affected proof
  when any of those overlap.
- Preserve an active Git conflict and invoke `$resolving-merge-conflicts`.

Landing order does not matter for independent siblings. If order changes
meaning, serialize them. Stop new dispatch when scope becomes invalid or safe
integration cannot keep up. Let healthy active workers finish unless the user
overrides the run or continued mutation is unsafe.

The root may make a small integration-only wiring, conflict, or displaced-code
correction after all workers are idle. Return substantive item behavior to its
worker.

## Prove

After all writers are idle and every item is landed, inspect the integrated
diff and run the smallest proof set that covers the accepted outcome, real
callers, and material interactions. Do not repeat worker proof that remains
valid.

For every accepted claim that crosses item boundaries, pass the actual produced
result or its actually persisted form through each affected public
transformation to the lowest ordinary caller on integrated `HEAD`. Assert the
source-named observations and governing identity the composition could lose.
Exercise only materially different accepted outcomes. Evidence closes only
claims its input, path, and observations distinguish; reuse worker proof only
while those remain valid after landing.

Invoke `$change-review` only when the user or repository requires it, or a
concrete unresolved shared-contract or migration judgment remains after proof.
Pin the clean candidate first and let Change Review own its procedure. Multiple
workers alone do not trigger review.

## Finish

For tracker-backed delivery, finish through
[Tracker Delivery](references/TRACKER-DELIVERY.md). Otherwise create no
closeout state.

Before final return, each worker stops background processes and command
sessions it started. Before cleanup, the root confirms the worker is idle and
no known session remains attached to its lane, then runs helper inspection.
Retain every successful helper-created lane packet in run-local state until
cleanup verification discharges it. Inspection success does not grant action
eligibility; require `resume_or_land_eligible` before either action and
`cleanup_eligible` before cleanup.
Remove only named lanes whose commits are integrated and whose checkouts are
clean. If the run stops early, preserve work and report the integration `HEAD`,
each unfinished item's actor, lane, base, commit or dirty state, landing state,
blocker, and next safe action. Infer no deployment, PR, merge, push, or later
campaign. A cleanup failure or residual helper-owned state is unfinished
cleanup; preserve it and report the exact retry.

Complete when every accepted item is landed, all writers are idle, integrated
proof supports the requested outcome, applicable tracker state is read back,
and, when this run created a lane, the root supplies every retained lane to
`verify-cleanup`, which confirms that supplied set is gone at the proved
integration `HEAD`.
