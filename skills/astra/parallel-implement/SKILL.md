---
name: parallel-implement
description: Coordinate and integrate requested work across active branches or worktrees in one repository. Use for new isolated checkouts or existing checkouts still in use. Exclude routine delegation and cleanup of finished branches.
---

# Parallel implement

Use only when requested to start or coordinate work across separate checkouts
while changes are still in flight. One lead owns the integration checkout,
landing, and the final combined result. Keep at most one active writer per
checkout and shared writable resource. Scheduling and implementation methods
are adaptable.
Use [git-cleanup](../git-cleanup/SKILL.md) when the request is to integrate or
organize finished branches. Writes and external effects require existing authority.

If the user explicitly combines this skill with
[controlled-delegation](../controlled-delegation/SKILL.md), this skill owns concurrency,
lane custody, integration, and parallel recovery. Apply
[Shared model routing](../controlled-delegation/references/model-policy.md).
Controlled-delegation retains budget constraints and its final review requirement.

## Establish ownership and the integration target

Establish the accepted scope, actual dependencies, and required proof. Identify
the integration branch and pin its current revision. Preserve unrelated work in
place and use a separate clean integration checkout when needed.

Use [Agent lanes](references/agent-lanes.md) for either starting point.

- **Existing checkouts.** Identify each checkout's actual branch or detached tip,
  base, current writer, and unresolved work. Preserve its lifecycle and custody.
- **New checkouts.** Prepare isolated worktrees from the current integration HEAD
  once required predecessors are present. Check that the worker can use its
  runtime, shared inputs, and isolated writable paths before starting.

Allow concurrent writes where the affected contracts and writable resources can
be owned independently. Check shared schemas, callers, fixtures, environments,
data, and services. Land an enabling change first when others require its result.
Serialize coupled work or work that cannot be isolated. For new assignments, give
the worker the scope, acceptance, exact checkout and base, write boundaries,
prerequisites, and proof needed. Keep tracker and landing effects with the lead.
Read [Tracker delivery](references/tracker-delivery.md) before taking on work that
includes authorized tracker claims or closeout.

Retain each checkout's identity, lifecycle owner, base, candidate, and writer
until verified cleanup or release. Keep helper packets with their lanes. Use the
existing handoff or run record when interruption could lose state.

## Land work as checkouts are released

Inspect the actual returned diff, acceptance, and evidence. Bind it to the commit
or captured change the lead will integrate. A helper lane returns a task-scoped
commit and must pass its lifecycle checks before landing. Preserve the ancestry
that helper cleanup requires. Other checkouts follow their own Git and lifecycle
contracts.

Confirm the writer and its mutating processes have stopped and released the
checkout before landing its work or transferring custody. Use
[Recovery](references/recovery.md) for uncertain custody, dirty returns, conflicts,
or partial operations. Integrate eligible candidates one at a time while independent
siblings continue. Read back the target after each landing and check which
dependencies are now satisfied. If a landing changes a sibling's contract, inputs,
runtime, or proof assumptions, reconcile that lane against the new target and
rerun the affected checks before it lands. Keep evidence that still applies.

## Verify the combined result and close out

Prove the accepted outcome on the actual integration candidate once the accepted
changes are integrated and the writers have stopped. Exercise material handoffs
through the ordinary consumer using the integrated changes. Use
[change-review](../change-review/SKILL.md) when requested, required, or needed to
settle a material integration risk. Use [pr-delivery](../pr-delivery/SKILL.md) for
requested PR delivery.

Finish authorized tracker transitions and verify their effects. Verify authorized
cleanup or release of each checkout and its owned resources through its lifecycle
owner. Preserve active, dirty, unintegrated, or uncertain work and shared data.
Report the integration revision, decisive proof, checkout dispositions, and
outstanding work. On interruption, retain the affected checkout and writer
identities, proof gaps, and next safe action in the handoff.
