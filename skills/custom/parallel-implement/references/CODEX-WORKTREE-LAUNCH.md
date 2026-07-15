# Isolated Worktree Launch

Use this after the orchestrator resolves the routing packet and completes the worker or integrator brief.

**Capability boundary:** `spawn_agent` creates a child context, not a Git checkout. Establish checkout isolation before spawning.

## Internal Lane

1. Resolve the exact base SHA.
2. Create a detached worker worktree with `git worktree add --detach "<absolute-path>" "<base-sha>"`, or a dedicated branch worktree for a child integrator.
3. From the orchestrator, verify the worktree root, `HEAD`, status, and writable `.tmp/` path.
4. Launch one direct child with `fork_turns="none"` and the complete brief.
5. Require every shell call and edit to target the assigned absolute worktree.
6. Accept the lane only after its independent preflight proves the root, path, `HEAD`, branch or detached state, starting status, `.tmp/` write/delete, environment, and focused-proof startup.

A worker without both isolations stops and blocks that frontier item until an isolated lane is available. A child integrator without a dedicated worktree returns landing to the orchestrator. Never run concurrent writers in one checkout.

Record worktree creation, cleanup authority, and branch preservation in the permission plan. Use the repo-approved worktree root or a run-scoped sibling root.

## Explicit Background Task

Use a separate Codex App task only when the user explicitly requests a visible or background task. When available, launch it against a project worktree with the complete brief and capture its task/worktree identifier. Use a working-tree start only when the lane must inherit authorized uncommitted changes.

A user-owned task passes the same isolation and preflight gate.

## Release

Require every lane agent to be idle before formal review. Finish or stop every lane during the orchestrator's Release. Remove a worker worktree only after verifying clean status and that every commit is integrated or explicitly preserved. Dirty state, untracked work, or an unpreserved commit blocks cleanup. Forced removal and branch deletion require explicit destructive authority.
