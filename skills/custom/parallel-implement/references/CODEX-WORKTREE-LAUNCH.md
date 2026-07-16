# Isolated Worktree Launch

Use this after the orchestrator resolves the routing packet and completes the worker or integrator brief.

**Capability boundary:** fresh context does not create checkout isolation. Every lane needs one dedicated worktree and a verified preflight packet before dispatch.

## Select

Choose one provider:

1. **Runtime-managed:** use a dedicated worktree only when the runtime supplies its identifier and absolute path to the orchestrator.
2. **Manual Git:** use the helper with an explicit configured root, then `<repo-parent>/worktrees/parallel-implement`, then an environment-declared auxiliary writable root.
3. **Blocked:** stop when neither provider can prove both checkout and shared Git-metadata writes.

Keep owner namespaces separate. A runtime-managed provider owns its worktree and cleanup. The manual provider owns only paths beneath its selected root. Do not place manual lanes inside the active checkout unless the environment explicitly supports that layout.

Use a separate user-owned Codex App task only when the user explicitly requests a visible or background task. Capture its task and worktree identifiers; it passes the same preflight gate.

## Create

For a manual lane, run creation as one standalone command:

```text
python <skill-dir>/scripts/lane_worktree.py create --repo <repo> --root <root> --base <sha> --run-id <run> --item-id <item>
```

Omit `--root` to use `<repo-parent>/worktrees/parallel-implement`. Pass `--branch <name>` only for a routed child integrator.

Stop and inspect the JSON result before any probe or dispatch. Do not combine creation with later commands in one shell expression. The helper rejects unsafe containment, existing targets, an excessive platform path budget, failed Git registration, and a mismatched base.

Record each attempt as `lane-create`. Retry only after the base, root, trust, permission, capability, or conflicting filesystem state changes; record that change with the next attempt.

On Windows, prefer a short configured root. The helper budgets the resolved lane path against the longest tracked repository path rather than prescribing a machine-specific drive or directory.

## Preflight

Run preflight separately with the exact created path and base:

```text
python <skill-dir>/scripts/lane_worktree.py preflight --worktree <path> --base <sha> --proof-command-json <json-array>
```

Require `ok: true` and record the complete packet. It proves:

- exact root, `HEAD`, detached or routed branch state, and clean status;
- checkout `.tmp/` write/delete;
- Git index-lock and shared object-metadata write/delete;
- normal or command-scoped `safe.directory` trust;
- effective identity and focused-proof startup;
- the cleanup route.

The helper never mutates global Git trust. A failed probe blocks the lane even when checkout creation succeeded.

Record the accepted packet as `lane-preflight`; rejected packets remain friction evidence and never authorize dispatch.

## Dispatch

Launch one direct fresh-context child with the complete brief, absolute worktree, and preflight packet. Require every shell call and edit to target that path. The worker independently verifies the root, `HEAD`, status, and packet before editing.

Never run concurrent writers in one checkout. A worker without both isolations blocks its frontier item. A child integrator without a dedicated worktree returns landing to the orchestrator.

## Recover

On resume, reconcile the provider identifier, Git registration, directory, `HEAD`, status, agent, commit disposition, and recorded packets. Preserve mismatches and return their exact state; do not recreate, redispatch, remove, or purge from ledger claims alone.

## Release

Require the lane agent to be idle and its worktree clean. A runtime-managed lane records the provider's released or preserved result and never enters manual cleanup. For a manual lane, record the exact worker `HEAD` as `integrated` or `preserved`, then run cleanup as one standalone command:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup --repo <repo> --worktree <path> --expected-head <sha> --disposition <integrated-or-preserved>
```

Verify Git registration removal and directory removal separately. Record the result as `lane-cleanup` with one returned state: `removed`, `unregistered-residual-directory`, `registered-preserved`, `blocked-dirty`, or `blocked-unpreserved`.

An `unregistered-residual-directory` is a verified intentionally preserved disposition only when its root, owner, cleanup route, and residual risk are recorded; it does not claim full removal. A registered, dirty, or unpreserved lane blocks completion.

Preserve an unregistered residual until explicit destructive authority permits the containment-checked recovery command:

```text
python <skill-dir>/scripts/lane_worktree.py purge-residual --repo <repo> --root <root> --worktree <path> --confirm-unregistered-residual
```

The purge route uses extended-length paths on Windows. Forced Git removal, branch deletion, or cleanup outside the recorded root remains outside helper authority.
