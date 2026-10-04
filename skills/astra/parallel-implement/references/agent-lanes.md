# Agent lanes

Use for isolated worker checkouts, readiness, shared inputs, integration, and
cleanup. A lane includes its checkout and the runtime resources its worker uses.

## Choose the lifecycle owner and base

Use a supported host-managed worktree or the bundled helper when it can establish
the isolation, identity, and recovery needed for the task. Preserve the lifecycle
owner: host-managed worktrees use the host's supported inspection and removal or
archive tools; helper lanes use [Helper lanes](helper-lanes.md). Read that reference
before preparing, inspecting, integrating, or cleaning a helper lane. Do not pass
host-managed or unrelated worktrees to the helper or bypass either owner's recovery.

Choose placement permitted by the host and repository. Reuse a suitable available
lane only after establishing custody and preserving existing work. If neither
route can establish safe isolation, preserve the scope and execute serially.

Prepare from the exact integration HEAD at dispatch, including required predecessor
changes. Do not assume a creation tool's default base is correct. Siblings selected
together may share that base; a dependent starts from the newer integration HEAD
after its predecessors land. Detached HEAD is valid when the lifecycle supports it.

Retain the returned identity, checkout, base, lifecycle owner, worker mapping, and
resource locations. Host identifiers and helper packets are not interchangeable.
The root coordinates lifecycle mutations and one serialized integration stream.

## Establish readiness before implementation dispatch

The root establishes that the assignment can run and be verified in its lane.
Use repository setup commands and the smallest relevant health check; adapt these
checks to the task rather than running a full suite in every checkout:

- Confirm the intended repository, exact base, guidance, and existing work to preserve.
- Establish the needed runtime and dependencies. Check that project imports or
  build inputs resolve to this checkout, especially with editable installs or a
  reused environment that may refer to another worktree.
- Resolve required configuration and data pointers from the lane. Use a small
  representative read or metadata check when sufficient; do not scan or copy a
  whole dataset merely to establish access.
- Establish writable output locations and ownership for caches, temporary files,
  generated databases, logs, services, and ports that the assignment needs.
- Run a relevant smoke command through an existing prerequisite entry path.
  Distinguish a setup failure from a known baseline failure and record material
  limits; the feature being assigned need not already pass.

Repair missing prerequisites within authority before dispatching implementation.
Reuse setup and health evidence while its relevant inputs remain unchanged. A
worker under different permissions or environment settings confirms those affected
assumptions before editing. Missing access or dependencies are readiness problems,
not evidence that the implementation worker needs a stronger model.

Pass the effective commands, runtime and data locations, readiness results, and
material limits in the assignment. No separate readiness document is required.

## Share durable inputs and isolate writes

Reuse durable datasets through established paths, configuration, or supported
read-only access. Do not duplicate permanent data per worktree merely to isolate
code. Identify the relevant dataset version or snapshot when consistency affects
results; if shared inputs can change during the run, establish how those changes
affect workers and their evidence.

Check actual consumer behavior. Reading a dataset may also update an index,
cache, lock, checkpoint, or database. Redirect such writes to lane-owned locations,
use a supported isolated snapshot when needed, or give the shared writer one owner
and serialize access. Shared package caches or environments are suitable only
when their concurrent use is supported and one lane cannot alter another's runtime.

Keep shared data and retained results outside disposable lane runtime storage and
cleanup ownership. Prefer supported path or configuration overrides to filesystem
links. When a link is needed, distinguish its ownership from its target and use a
lifecycle that can clean it without traversing or deleting the shared target.

One active writer owns each lane. Git worktrees share most refs, stash state, and
repository configuration. Workers must not stash, switch or rebase shared branches,
or change shared refs or configuration. Give other writable resources an owner or
serialize them. A branch owned exclusively by the lane follows its host and
repository rules.

## Inspect and integrate

Before returning a reviewable candidate, the worker stops its background writers
and command sessions and releases custody. Actor status alone does not establish
process quiescence. Inspect actual lane state after return, before replacement,
before integration or cleanup, and when resuming interrupted work.

For host-managed lanes, use the host's returned identity and supported inspection
tools, alongside Git and resource state as needed. Bind review to an exact commit
or captured patch with its base; a completion message or pathname is insufficient.
For helper lanes, follow [Helper lanes](helper-lanes.md) for mechanical eligibility
and ancestry requirements. Use [Recovery](recovery.md) for dirty or uncertain work.

The root integrates accepted candidates using a method allowed by the selected
lifecycle. When a host-supported squash, cherry-pick, or patch integration changes
commit identity, verify that the intended content and behavior reached the final
candidate rather than relying on ancestry. Do not apply that exception to helper
lanes. Reassess semantic interference when integration advances even if Git merges
cleanly, and rerun only affected or required checks.

## Cleanup

Establish actor and process quiescence and preserve required evidence, ignored
artifacts, and retained results before disposal. Clean Git status does not make
those artifacts disposable. Confirm the accepted work is present in the proved
final integration candidate and limit cleanup to resources this run owns.

Remove or archive task-created host-managed lanes through their host and read back
the result. Release reused lanes without disposing of pre-existing work or resources
unless their disposal is authorized. For helper lanes, complete the receipt and
full-set verification in [Helper lanes](helper-lanes.md#cleanup); host cleanup
receipts cannot substitute for that contract.

Verify the outcome for every lane and owned runtime resource. Never treat a shared
data pointer as ownership of its target. Preserve and report uncertain or
unintegrated state instead of forcing removal; unresolved cleanup remains an
explicit delivery limit. For a version-controlled local tracker, use final delivery
HEAD H only after [Tracker delivery](tracker-delivery.md) establishes that its C..H
metadata changes leave the code proof applicable.
