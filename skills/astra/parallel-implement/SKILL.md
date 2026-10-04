---
name: parallel-implement
description: Coordinate requested concurrent implementation with exclusive ownership, integration, and proof. Exclude parallel research and single-task coding.
---

# Parallel implement

Coordinate implementation fanout only when useful work can proceed concurrently
without ambiguous ownership. The root owns decomposition, scheduling, integration,
and the final composed outcome. Workers own only their assigned implementation.
They choose techniques and local sequencing within the assigned scope and
acceptance. The root adapts decomposition and concurrency as the work develops.

Workers do not delegate further, land their own work, mutate tracker state, or
dispatch successors. Product writes and external effects remain limited by the
user's existing authorization.

If the user explicitly combines this skill with
[cost-aware-coding](../cost-aware-coding/SKILL.md), this skill owns concurrency,
lane custody, integration, and parallel recovery. Cost-aware-coding continues to
own GPT-6 model and effort routing, budget constraints, and its final review
requirement.

## 1. Admit independent work

Establish the accepted outcome, fixed delivery scope, dependencies, and required
proof. Tickets and a formal specification are optional.

Admit concurrent items only when their behavior ownership and mutable effects can
be separated. Check shared schemas, callers, fixtures, generated files,
configuration, package environments, databases, ports, external services, and
other writable resources; disjoint source files alone do not establish
independence.

Give every shared mutable resource one owner or serialize the affected work. Land
a shared enabling change before dependent work when that preserves a coherent
design. Do not invent boundaries or subtasks merely to occupy workers.

If only one useful item is ready, the work is tightly coupled, or one change
requires coordinated writes across repositories, execute serially or reslice at
a real compatibility boundary.

Keep a clean integration checkout at a known exact base and preserve unrelated
work. Do not stash or commit unrelated changes to manufacture cleanliness.

When delivery includes authorized tracker claims or closeout, read
[Tracker delivery](references/tracker-delivery.md) before dispatch.

## 2. Dispatch the ready frontier

A ready item has no unmet predecessor whose outcome must first be integrated.

With concurrent writers in one repository, read
[Agent lanes](references/agent-lanes.md) and give each worker a distinct
isolated checkout from the current integration HEAD, using a supported host-managed
worktree or the bundled helper under its own lifecycle contract. With one writer
and no overlap, the root may instead grant that worker exclusive custody of the
integration checkout. Use the lane reference's readiness checks before dispatch;
worktree creation alone does not establish a usable implementation environment.

Bound concurrency by actual resource limits and the root's ability to inspect and
integrate returns safely.

Each assignment carries the goal, acceptance, exact checkout and base, allowed
writes and exclusive resources, relevant predecessor outcomes, runtime and data
pointers, readiness results and limits, required proof, prohibited effects, and
stopping condition. Reuse durable inputs by reference and isolate mutable outputs
under the lane reference. Supply facts the worker cannot infer; do not assume
inherited context.

A helper-lane worker returns a task-scoped commit because landing and cleanup
depend on its candidate identity. Host-managed and serial workers follow their
host, repository, and delivery commit policies, returning a stable identifiable
candidate without a universal commit requirement.

Retain the item-to-worker mapping, lane identity and lifecycle owner, base,
candidate, and resource ownership until cleanup or release is verified. Keep the
complete packet for helper lanes; their optional run inventory can retain lane
identities automatically. Write a separate narrative run record only when an
established repository or active workflow convention requires a durable handoff.

## 3. Integrate continuously

Inspect a worker's actual returned state before accepting it, using its lifecycle
owner's inspection and integration contract. Helper lanes require the eligibility
checks in the lane reference before normal resume or landing. Also judge the actual
diff, scope, acceptance, and returned proof; lifecycle state proves mechanics,
not semantics. Integrating a released lane need not stop independent sibling work.

Return item-local gaps to the same worker while its lane and context remain safe.
For silence, interruption, dirty returns, conflicts, replacement, or uncertain
custody, read [Recovery](references/recovery.md). Never start a competing writer
while the previous actor may still mutate the same state.

The root alone lands accepted lane work. Preserve ancestry required by the lane
contract. After integration HEAD advances, reassess whether intervening changes
alter a sibling's behavior owners, inputs, callers, fixtures, configuration,
resources, or proof assumptions. If they do, return that worker to the current
integration state and rerun affected proof before landing.
Recheck affected readiness assumptions when dependencies, data pointers, permissions,
or runtime configuration change.

After each landing, read back the integration candidate, run only proof invalidated
or required by that transition, and recompute the ready frontier. Serialize when
landing order itself changes meaning.

## 4. Prove and finish

When all writers are quiescent and accepted items are integrated, prove the
composed outcome on the actual integration candidate. Exercise material
cross-item handoffs through the ordinary consumer rather than relying only on
isolated worker tests or hand-constructed substitutes.

Reuse worker evidence only while its relevant code, inputs, environment, and
observations remain valid. Missing required proof leaves delivery incomplete.

Use [change-review](../change-review/SKILL.md) when requested, required by the
repository, or needed for a concrete unresolved shared-contract or migration
judgment. When cost-aware-coding also governs the run, its lead owns that skill's
required final review and acceptance of the stable integrated candidate.

Finish authorized tracker transitions through the tracker reference. After actor
quiescence, clean task-created lanes or release reused lanes through their lifecycle
owners under [Agent lanes](references/agent-lanes.md). Account for the full retained
lane set against the proved final integration HEAD. Never force cleanup of
uncertain, dirty, active, or unintegrated work, or include shared durable data in
lane disposal.

Complete only when the accepted outcome is integrated and proved, all writers are
quiescent, required external state is read back, and every created or reused lane
is accounted for. On interruption, return the actual integration candidate,
unfinished items and actors, retained lane identities or packets, dirty state,
proof gaps, blockers, and the next safe action.
