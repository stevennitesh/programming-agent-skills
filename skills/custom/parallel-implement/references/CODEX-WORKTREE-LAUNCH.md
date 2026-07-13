# Isolated Worktree Launch

Use this after the orchestrator resolves the routing packet and builds a brief from `WORKER-BRIEF.md` or `INTEGRATOR-BRIEF.md`.

**Capability boundary:** `spawn_agent` creates a child context, not a Git checkout. Establish checkout isolation before spawning the lane.

## Internal Lane

Use the collaboration subagent route for internal workers and a routed integrator.

1. Resolve the exact base SHA.
2. For a worker, create a detached worktree with `git worktree add --detach "<absolute-path>" "<base-sha>"`. For a hot or late integrator, create a dedicated branch worktree for the routed integration branch.
3. Verify the worktree root, `HEAD`, status, and writable `.tmp/` path from the orchestrator.
4. Launch one direct child with `fork_turns="none"` and the complete brief.
5. Require every shell call to set the assigned worktree as `workdir` and every file edit to use an absolute path under that worktree.
6. Accept the lane only after its own preflight independently reports the actual repo root, checkout path, `HEAD`, branch or detached state, starting status, `.tmp/` write/delete result, and focused-proof startup.

A root-created worktree is isolated only when the lane uses that path for its entire lifetime. If worker isolation cannot be established, stop or downshift. If a dedicated child-integrator worktree cannot be established, keep landing with the orchestrator. Never run parallel writers in one checkout.

Record worktree creation, writable-root approval, cleanup, and branch preservation in the permission plan. Use the repo's approved worktree root when one exists; otherwise route a run-scoped sibling root such as `<repo-parent>/worktrees/<repo>/<run-id>/<work-item>`.

## Explicit Background Task

Use a separate Codex App task only when the user explicitly asks for separate, visible, or background worker tasks. Otherwise use the default internal lane route.

When available, use the thread-creation tool with a project worktree target and the complete brief. Select the saved project for the repo, start from the recorded branch or ref, and capture the returned task or pending-worktree ID. Use a working-tree start only when the lane must inherit current uncommitted changes.

A user-owned task still passes the same isolation and preflight gate before edits.

## Release

Finish or stop every lane before formal review. Before removing a worker worktree, verify clean status and that every worker commit is integrated or named as preserved. Dirty state, untracked work, or an unpreserved commit blocks cleanup. Remove clean run-scoped worktrees without force under the routed cleanup rule. Forced removal and branch deletion require explicit destructive authority. Record each lane, worktree, commit, and branch disposition in the release event.
