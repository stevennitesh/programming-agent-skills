---
name: parallel-implement
description: Coordinate an explicitly requested parallel implementation across bounded items, with exclusive ownership, safe integration, cross-item proof, and recoverable worktree cleanup. Use for implementation fanout, not parallel research or a single coding task.
---

# Parallel implement

The root owns decomposition, scheduling, integration, and the final outcome.
Workers implement directly using repository guidance and the engineering
contract; no implement skill is required. Keep fanout at the root. Use the
available agent tools, not a new orchestration service or a fixed model roster.

## 1. Admit independent work

Establish the accepted outcome, fixed delivery scope, dependencies, and proof.
Derive bounded items from that scope when needed; tickets and a formal spec are
optional. Resolve material product uncertainty with its owner before dispatching
affected work. Do not invent architecture boundaries to occupy workers. If only
one useful item exists, implement directly within authority. If all items are
coupled, execute serially and explain why parallelism would not help.

Admit concurrent items only when behavior ownership, proof, and write effects
are independent. Check shared schemas, callers, fixtures, generated files,
configuration, package environments, databases, ports, and external services.
Disjoint files alone are insufficient. Remove unnecessary sharing; otherwise
give the shared resource one exclusive owner or serialize affected work. Land a
shared enabling change before its consumers when that preserves a coherent design.

Pin a clean integration checkout and exact base in each writable repository.
Preserve unrelated dirty work: use a separate clean integration checkout when
appropriate, or resolve the missing baseline within authority. Never stash or
commit unrelated work to manufacture cleanliness. Establish local commit authority
under repository policy before dispatching any committing worker, including one
using the serial integration checkout. Concurrent lanes additionally require
ancestry-preserving integration. A no-commit constraint needs
a different agreed delivery method, not a silent bypass of cleanup checks.

Each worker gets at most one writable repository and exclusive mutation domains.
Keep a change requiring coordinated writes across repositories with the serial
root or reslice at a real compatibility boundary. Global installs and external
effects stay with the serial root and their existing authorization. For authorized
tracker delivery, read [Tracker delivery](references/tracker-delivery.md).

## 2. Isolate and dispatch

Choose isolation for the current ready frontier: items whose required predecessor
outcomes are integrated. With one ready item and no other writer, the root can
implement directly or give one worker exclusive custody of the integration
checkout. With overlapping writers, read [Agent lanes](references/agent-lanes.md)
and prepare distinct helper-managed lanes at the same exact integration HEAD.
A dependent starts at the newer HEAD after its predecessors land. A host-managed
checkout is not automatically a helper lane; do not double-manage its lifecycle.

Bound concurrency by available resources and the root's ability to inspect and
land returns. Use a fresh-context worker per item. Send the goal, acceptance,
exact checkout and base, allowed writes, exclusive resources, applicable guidance,
predecessor outcomes, proof obligations, prohibited effects, and stopping condition.
Point to accessible source context; supply essential facts the worker cannot read.
For helper lanes, pass the complete returned packet, including runtime paths.
Tell workers they are not alone and must preserve others' changes. Workers do
not delegate, change tracker state, land changes, or dispatch successors.

Before mutation, each worker verifies its checkout, exact base, and clean state.
Every repository command runs there. Concurrent workers must not stash, change
shared refs, or switch/rebase shared branches. Require focused verification and
a task-scoped commit with no unrelated changes. The return names actual commit,
changed scope, proof commands/results/runtime paths, material skips, blockers,
and stopped processes or sessions. Prose is evidence, not state.

Persist a compact root-owned run record in the repository's run-scoped scratch
location: item/actor, repository/base/lane packet, dependency and landing state,
proof, and next action. After interruption or context loss, reconcile it against
actual state before dispatching again. Retain every successful
lane packet through final cleanup verification. Record partial prepare failures
too; a failed command does not establish that nothing was created.

## 3. Inspect and land continuously

Inspect returned state before accepting it. For a lane use helper inspection;
require `mechanical.resume_or_land_eligible` before resuming normal work or landing.
Also inspect scope, commit ancestry, actual diff and proof. Serial worker commits
already reside on the integration checkout: reacquire custody and verify them
in place, never apply them a second time. Root landing never overlaps a writer
using the integration checkout.

Return item-local gaps to the same worker while its lane is safe. For silence,
failure, dirty returns, conflicts, or interruption, read
[Recovery](references/recovery.md). Never replace an actor that might still write.

Land accepted commits one at a time. Fast-forward if integration HEAD still equals
the lane base; merge independent siblings so their commits remain ancestors.
Do not cherry-pick or squash helper-lane commits: cleanup relies on ancestry.
When integration has advanced, compare intervening behavior owners, inputs,
callers, fixtures, configuration, resources, and proof. If affected, return the
same worker to incorporate the current integration commit and rerun affected
proof before landing; clean textual merging is not semantic independence.

Read back HEAD and the resulting diff after every landing. Run proof invalidated
by that transition or required there by policy. Checkout normalization invalidates
proof that depends on repository bytes or generated identities; run it on the
integration checkout. Recompute the frontier and dispatch newly independent work
without waiting for an entire batch. If landing order changes meaning, serialize.

Stop new dispatch if scope becomes invalid or safe integration cannot keep up.
Let healthy active workers finish unless the user changes course or continued
mutation is unsafe. The root may make small integration wiring or displaced-code
corrections with all workers idle; return substantive item behavior to its owner.

## 4. Prove the composed outcome

With all writers idle and accepted items landed, inspect the integrated diff and
run the smallest proof set covering the outcome and material interactions.
For each cross-item claim, pass actual produced output or its persisted form
through affected public transformations to the ordinary consumer. Assert the
accepted observations and identities the composition could lose, including
material failure or partial-success behavior. Hand-constructed substitute inputs
and isolated passing workers do not establish this handoff.

Reuse worker evidence only while its relevant inputs, code, path, environment,
and observations remain valid. Missing required proof is incomplete delivery.
Use change review when requested, required by the repository, or needed for a
concrete unresolved shared-contract or migration judgment; worker count alone
does not trigger extra reviewers. Fixes invalidate affected evidence and any
review tied to the previous candidate.

## 5. Finish or preserve a recoverable handoff

Read back authorized external landing or rollback effects. Finish applicable
tracker transitions through the conditional reference. Stop worker-created
processes and command sessions and verify actor quiescence before cleanup.
Use the lane reference to clean only named, clean, integrated lanes and verify
the entire retained set at the proved integration HEAD. Never force removal or
infer cleanup authority from a worker's success message.

Completion means the accepted outcome is integrated and proved, all writers are
idle, required external state is read back, and every created lane is accounted
for with cleanup verified. Residual helper state is unfinished cleanup even if
the code is complete. On interruption return the actual integration HEAD,
unfinished items/actors/lanes/bases/commits or dirty state, proof gaps, blockers,
and next safe actions. Do not infer a push, PR, deployment, or another campaign.
