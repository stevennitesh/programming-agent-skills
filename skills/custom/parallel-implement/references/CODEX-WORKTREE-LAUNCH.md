# Isolated Worktree Launch

Use this after the orchestrator resolves the routing packet and builds a brief from `WORKER-BRIEF.md` or `INTEGRATOR-BRIEF.md`.

## Internal Lane

Use the native collaboration subagent route for internal workers and a routed integrator.

1. Assign one isolated worktree per lane. Use a native isolated worktree when the tool provides one.
2. When collaboration agents share the parent checkout, create an approved manual worktree at the assigned base and record its absolute path in the brief.
3. Prefer a detached worker worktree so one clean commit is the complete handoff. Give a dedicated integrator the routed integration branch.
4. Launch one fresh subagent with the complete brief.
5. Require every shell command and file operation to use the assigned worktree.
6. Accept the lane only after its preflight reports the actual repo root, checkout path, `HEAD`, branch or detached state, starting status, `.tmp/` write/delete result, and focused-proof startup.

A manually assigned worktree is isolated only when the lane uses that path for its entire lifetime. If isolation cannot be established, stop or downshift; never run parallel writers in one checkout.

Record worktree creation, writable-root approval, cleanup, and branch preservation in the permission plan. Use the repo's approved worktree root when one exists; otherwise route a run-scoped sibling root such as `<repo-parent>/worktrees/<repo>/<run-id>/<work-item>`.

## User-Owned Background Task

Use a separate Codex task only when the user explicitly asks for a background, separate, or user-owned task. This is not the default subagent route.

When available, use the thread-creation tool with a project worktree target and the complete brief. Select the saved project for the repo, start from the recorded branch or ref, and capture the returned task or pending-worktree ID. Use a working-tree start only when the lane must inherit current uncommitted changes.

A user-owned task still passes the same isolation and preflight gate before edits.

## Release

Finish or stop every lane before closeout. Remove run-scoped worker worktrees under the routed cleanup rule. Preserve branches unless that rule explicitly authorizes deletion. Record each lane, worktree, and branch disposition in the release event.
