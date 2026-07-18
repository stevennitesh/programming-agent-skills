# Isolated Lane Lifecycle

Use this to establish, preflight, inspect, recover, and release every worker or child-integrator lane.

Fresh context does not create checkout isolation. Dispatch requires both.

## Select

Choose one provider:

1. **Runtime-managed:** use only a dedicated worktree whose provider identifier and absolute path are supplied to the orchestrator.
2. **Manual Git:** select an explicit `--root`, then `PARALLEL_IMPLEMENT_WORKTREE_ROOT`, then `<repo-parent>/worktrees/parallel-implement`.
3. **Blocked:** stop when neither provider proves checkout and shared Git-metadata writes.

Provider namespaces never overlap. The runtime owns managed cleanup. The helper owns only manual paths beneath the recorded root. A user-owned Codex App task remains explicit-only and passes the same preflight.

## Create

Run manual creation as one standalone command and inspect its JSON before continuing:

```text
python <skill-dir>/scripts/lane_worktree.py create --repo <repo> --root <root> --base <sha> --run-id <run> --item-id <item>
```

Omit `--root` to use the environment value when present, otherwise the repo-parent default. Pass `--branch <name>` only for a routed integrator. The helper records `root_source`, uses a bounded hashed lane name, verifies containment, budgets generated and tracked path space before filesystem or Git mutation, creates detached workers by default, verifies registration and base, and reports command-scoped Git trust. A path failure returns `blocked-path-budget` with the selected root and recovery route.

Record every attempt as `lane-create`. Retry only after its base, root, trust, permission, capability, or conflicting filesystem state changes.

## Preflight

Run preflight separately with a unique actor identifier:

```text
python <skill-dir>/scripts/lane_worktree.py preflight --worktree <path> --base <sha> --actor-id <actor> --proof-command-json <json-array>
```

For Windows or complex argv transport, prefer a UTF-8 JSON file (a Windows-authored UTF-8 BOM is accepted):

```text
python <skill-dir>/scripts/lane_worktree.py preflight --worktree <path> --base <sha> --actor-id <actor> --proof-command-file <path>
```

The file contains one JSON array of argv strings, is mutually exclusive with inline JSON and `--skip-proof`, is never evaluated through a shell, and is recorded by resolved path and SHA-256 digest. Resolve the root choice and proof transport during Trace before creating lanes.

Proof startup is required. When no repository startup proof exists, use `--skip-proof --reason <reason>` and carry that skip as residual risk. Inline JSON, proof file, and skip are mutually exclusive.

Require `ok: true`. The packet proves exact root and base, detached or routed branch state, clean status, checkout writes, Git index-lock and shared-object writes, command-scoped trust, effective identity, and proof startup. It also creates and returns stable, actor-specific `temp_root`, `pytest_basetemp`, and `cache_root`; pass those exact paths to the actor.

Record the packet as `lane-preflight`. A failed operation returns `state`, `recoverable`, and `next_action`; it never authorizes dispatch.

## Dispatch

Launch one direct fresh-context child with the complete brief, absolute worktree, preflight packet, temp roots, and liveness checkpoint. Every command and edit targets that path. The worker reconciles the packet before editing.

One checkout has one writer. A worker without both isolations blocks its item. An integrator without a dedicated branch worktree returns landing to the orchestrator.

## Stall

A missed recorded checkpoint plus no agent or process progress triggers inspection, not redispatch.

1. Record `lane-stall` with the missed checkpoint and last evidence.
2. Stop the worker and reconcile its child processes.
3. Inspect worktree registration, root, `HEAD`, status, commit, patch, temp roots, and claim.
4. Preserve dirty or uncommitted work and emit one recovery packet.
5. Record `lane-recovery`; redispatch only after the inherited lane and packet reconcile.

Never infer completion from a missing worker. Never start two writers in the inherited lane.

## Resume

Reconcile provider identifier, Git registration, directory, `HEAD`, status, agent or process, commit disposition, temp roots, claim, and ledger packets. Preserve every mismatch. Recreate, redispatch, remove, or purge only from observed state plus the returned recovery route.

## Release

Make the lane idle. A runtime-managed lane records the provider's released or preserved state and never enters manual cleanup.

For a manual lane, record its exact commit as integrated or preserved, then run:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup --repo <repo> --root <root> --worktree <path> --expected-head <sha> --disposition <integrated-or-preserved>
```

The helper resolves abbreviated SHAs, verifies containment, exact `HEAD`, clean status, and disposition, then removes the Git registration. If Git unregisters but leaves a directory, the same invocation performs containment-checked extended-path cleanup. Record registration and directory results separately as `lane-cleanup`.

Safe terminal states are `removed`, `provider-preserved`, or an explicitly accepted `unregistered-residual-directory`. Dirty, registered, unpreserved, or unaccounted state blocks `complete`.

A residual found after registration was already lost cannot be reverified automatically. Preserve it until explicit cleanup authority permits:

```text
python <skill-dir>/scripts/lane_worktree.py purge-residual --repo <repo> --root <root> --worktree <path> --confirm-unregistered-residual
```

Forced Git removal, branch deletion, global `safe.directory` mutation, and cleanup outside the recorded root remain outside helper authority.
