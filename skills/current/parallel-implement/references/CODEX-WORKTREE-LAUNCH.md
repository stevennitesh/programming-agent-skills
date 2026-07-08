# Codex Worktree Launch

Use this only after the orchestrator has a routing packet and a worker prompt built from `WORKER-BRIEF.md`.

Prefer Codex-managed worktrees created by the Codex app, not `git worktree`.

If launch tools are not visible, use `tool_search` for `create_thread` and project/list tools before manual app fallback.

## App Route

1. Run `codex_app.list_projects` and choose the saved project for this repo.
2. Run `codex_app.create_thread` once per issue with a Worktree target:

```json
{
  "prompt": "<worker prompt built from WORKER-BRIEF.md>",
  "target": {
    "type": "project",
    "projectId": "<projectId>",
    "environment": {
      "type": "worktree",
      "startingState": { "type": "branch", "branchName": "<existing base branch or ref>" }
    }
  }
}
```

Omit `startingState` to use the project default branch. Use `{ "type": "working-tree" }` only when the worker must inherit current local uncommitted changes. Do not use `startingState` to name a new branch.

## Verification

A Codex-managed worktree counts as verified only after the worker reports: thread ID or pending worktree ID, actual repo root, `HEAD`, branch or detached state, clean starting status, scratch write/delete result, and focused-proof preflight result.

## Fallback

If the app route is unavailable, create the thread manually in the Codex app: new thread -> Worktree -> existing starting branch/ref -> submit the worker prompt.

If no Codex-managed worktree can be created, stop and report the blocked launch, or ask the user to approve the manual worktree fallback.

Manual fallback worktrees are not Codex-managed: `<repo-parent>/worktrees/<repo>/<run-id>/<issue-id>`, with `<repo-parent>/worktrees/` approved as a writable root.
