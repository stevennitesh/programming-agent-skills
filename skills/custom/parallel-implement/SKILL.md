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
two accepted, independently implementable items. The set may come from a
tracker-backed parent graph or another caller-owned fixed delivery scope. Send
one item to `$implement`. Send vague work, unsettled meaning, or missing
dependencies back to its owner or `$to-tickets` before mutation.

Pin a clean integration `HEAD`. For tracker-backed delivery, refresh the graph,
claim the parent and selected children, and read each claim back. Direct work
creates no tracker state.

Derive the ready frontier from dependencies whose changes are already
integrated. Admit concurrent siblings only when their behavior ownership and
write effects are independent. Account for shared schemas, callers, fixtures,
configuration, generated destinations, databases, ports, package environments,
external services, and other mutable resources. File separation alone does
not prove independence. Assign one exclusive owner to a shared writable
resource or run the affected items serially.

Run a shared enabling refactor before dependent slices when that preserves the
real design better than artificial file boundaries. Keep only enough workers
active for the root to inspect and land their returns promptly.

## Isolate

Read [Agent Lanes](references/AGENT-LANES.md). Give every concurrent writer a
distinct helper-created worktree at current integration `HEAD`. Siblings
admitted from one frontier share that exact base; a dependent item starts only
after its predecessors land and therefore uses the newer `HEAD`. Give a serial
writer the integration checkout only after every other actor that can write
there is idle. Root landing and direct serial implementation never overlap.

Use one fresh worker per item. Give it the exact absolute worktree path, base,
scope, allowed writes, acceptance, predecessor outcomes, proof, assigned
exclusive resources, and prohibited external effects.

## Dispatch

Require the worker to verify its assigned worktree and exact base before its
first mutation and to run every repository and Git command there. Concurrent
workers do not stash, switch or rebase shared branches, mutate shared refs,
change tracker state, land commits, or dispatch successors.

Each worker implements its bounded item, runs focused proof, makes one task
commit, and returns the commit, changed scope, proof, skips, and blocker if one
remains. The root verifies the registered lane, base, current status, commit,
diff, scope, and proof from the checkout. Worker prose is evidence, not state.

Send an actionable item-local gap back to the same worker while its lane is
safe. Silence or a missed checkpoint triggers inspection, not another worker.
Before replacement, stop the prior actor, confirm it stopped, and inspect its
lane and commit state. Never run two actors on one item.

## Land

When a serial worker commits in the integration checkout, reacquire custody and
verify current `HEAD`, the commit, diff, scope, and proof. Accept that direct
landing without applying its commit again.

Verify and land accepted worker commits one at a time. After each landing,
read back integration `HEAD`, inspect the resulting diff, run proof invalidated
by that transition or required by repository policy, recompute the ready
frontier, and dispatch another independent item without waiting for a batch.

When integration `HEAD` advanced since dispatch:

- Land directly when the intervening changes do not touch the item's behavior
  owner, inputs, callers, fixtures, configuration, resources, or proof.
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

Invoke `$change-review` only when the user or repository requires it, or a
concrete unresolved shared-contract or migration judgment remains after proof.
Pin the clean candidate first and let Change Review own its procedure. Multiple
workers alone do not trigger review.

## Finish

For tracker-backed delivery, close children before the parent under the
configured tracker rules and read back each durable change. Otherwise create
no closeout state.

Remove only named lanes whose commits are integrated and whose checkouts are
clean. If the run stops early, preserve work and report the integration `HEAD`,
each unfinished item's actor, lane, base, commit or dirty state, landing state,
blocker, and next safe action. Infer no deployment, PR, merge, push, or later
campaign.
