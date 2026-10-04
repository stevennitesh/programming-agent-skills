# Helper lanes

Use only for lanes created by the bundled
[lane helper](../scripts/lane_worktree.py).
Its `--help` owns current command syntax. [Agent lanes](agent-lanes.md) owns the
shared readiness, data, custody, and integration obligations; this reference owns
the helper-specific lifecycle. Host-managed and unrelated worktrees are outside
the helper's ownership.

## Prepare

Choose an allowed worktree root outside the repository. The root alone performs
helper mutations, sequentially. Prepare each lane from the exact integration HEAD
specified by the calling workflow. Pass the complete returned lane packet to the
worker and retain it until final cleanup verification.

For a multi-lane delivery, supply the same optional `--run` name to each `prepare`.
The helper maintains a run inventory and `status --run` inspects its complete lane
set in one call. Status retains cleaned lanes' candidate and integration commit
identities, rechecks integration against the current repository HEAD, and exposes
the live checkout identity separately as `observed_lane_head`. During interrupted
cleanup, a valid receipt supplies the removed candidate's identity and integration
check. Invalid metadata or failed observations, including unreadable readiness
metadata, make status fail. Absent readiness records and recorded failed health
checks remain reportable. Dirty, active, or unintegrated work also remains
reportable without being eligible for cleanup. Use a new lane name for a new
assignment after cleanup. Existing lanes cannot be silently adopted into another
run. An interrupted prepare remains
visible in the inventory; inspect and recover it instead of assuming it completed.

Successful preparation checks Git identity, clean state, and writable directories;
it does not bootstrap dependencies, establish data access, or run project health
checks. Use `ready` with explicit setup and health commands for repeatable
readiness checks, or establish equivalent evidence through the repository's tools
under [Agent lanes](agent-lanes.md). Complete readiness before dispatching
implementation.

Use the returned checkout and runtime paths for temporary files, caches, generated
databases, logs, and tests when tools support redirection. Runtime paths belong to
the helper's disposable state. Keep permanent data, borrowed environments, and
retained results outside that state. The helper rejects reparse points in its
runtime lifecycle; do not redirect its owned paths to shared resources.

A helper-lane worker returns a task-scoped commit and focused proof after stopping
its background processes and command sessions. The helper cannot establish actor
or process quiescence.

## Readiness and command execution

`ready` runs supplied setup commands followed by at least one health check, stopping
at the first failure. `exec` runs the command after `--` in the lane's checkout and
environment, including while implementation has uncommitted changes. It does not
rerun setup or require a readiness record. Supply the same profile or overrides
when the two operations need the same environment. No profile is auto-discovered,
and the helper does not guess installation commands or copy datasets.

Both accept an optional JSON `--profile` and one-off `--env KEY=value`,
`--input KEY=path`, `--output KEY=path`, and `--timeout` overrides. `ready` also
accepts repeatable `--setup` and `--check` JSON argument arrays. Commands use argument
arrays without a shell; call a specific shell explicitly only when needed.
Read [Execution profiles](execution-profiles.md) when choosing these settings.

The runner supplies lane-specific temporary and common cache locations. Explicit
input paths become environment variables after a small access check; they stay
at their existing locations. Declared output directories belong inside disposable
lane runtime storage. These declarations route and check paths; they do not sandbox
arbitrary commands or prove that a data consumer is read-only.

Results include exit status, timing, timeout state, and a bounded output tail.
The latest command and readiness records live in disposable runtime storage;
preserve any evidence needed after cleanup elsewhere. Inspection reports the last
readiness observation without claiming it is still fresh. Choose checks for import
resolution, data meaning, and the real prerequisite path. Use `ready --checks-only`
to avoid repeating setup when its dependencies and environment remain valid.

Commands are synchronous: do not use this runner to leave background services
running. On Windows, the supplied command starts only after its waiting launcher
is assigned to a dedicated Job Object; closing that job ends its process tree.
On other platforms timeout handling targets the launched process group. The helper
does not track independently launched agents or processes that escape its group.
An active or interrupted command marker blocks new runner commands and cleanup.
After an interruption, establish process quiescence and preserve needed evidence
before removing that marker; never clear it solely because its recorded PID is absent.

## Inspect and integrate

`ok: true` means inspection ran successfully; it is not permission to resume,
integrate, or clean. Require `mechanical.resume_or_land_eligible` before normal
resume or integration and `mechanical.cleanup_eligible` before cleanup. Use
[Recovery](recovery.md) for dirty or uncertain partial work.

The root integrates accepted helper-lane commits while preserving their ancestry.
Do not cherry-pick or squash them when doing so would break the ancestry the
cleanup contract uses. Mechanical eligibility does not establish semantic
compatibility with intervening integration changes.

## Cleanup

Establish actor quiescence and retain evidence needed for unresolved failures.
The helper treats ignored entries as cleanup blockers; remove only artifacts whose
ownership and disposability are established, then inspect again. Environment or
setup artifacts are subject to the same ownership check.

Supply `cleanup --integration-head` with the full proved commit ID. The helper
checks it before deleting runtime artifacts as well as before removing a worktree.
This argument is required for new cleanup calls; existing lane manifests and
supported cleanup receipts remain readable without readiness metadata or migration.

Clean only named lanes that are clean, free of ignored artifacts, and integrated
into the current final candidate. For named runs, supply their `--run`; optionally
select a subset with `--completed`. Without that subset, cleanup considers the
complete owned inventory, so establish quiescence for that set first. Before
unregistering a lane, the helper records
the lane's filesystem identity in its cleanup receipt when the platform exposes
one. A residual path is eligible for automatic retry only when it is absent or
still matches that recorded identity; a new object at the same pathname is
preserved. Only the current receipt schema is accepted. Older or malformed
receipts are preserved as unsupported recovery state rather than migrated or
overwritten automatically. Partial cleanup must retain the receipt and helper
state needed for recovery. Do not replace helper recovery with manual recursive
deletion.

After cleanup attempts, run cleanup verification over the complete retained
helper-lane set, using `verify-cleanup --run` for named runs. Do not restrict final
verification to the latest completed subset. Run inventory retains completion
evidence so repeated cleanup can recognize already removed lanes; an unrelated
replacement at an old path is preserved. The inventory itself remains available
for handoff and does not mean all lanes are disposable. Helper cleanup is complete
only when it reports
`finish_clean: true` for the proved final integration HEAD, or delivery HEAD H
under [Tracker delivery](tracker-delivery.md). Keep host-managed lanes accounted
for separately under their lifecycle owner.

The helper never proves code semantics or actor liveness, forces removal, deletes
branches, changes global Git configuration, or chooses a lane for the caller.
