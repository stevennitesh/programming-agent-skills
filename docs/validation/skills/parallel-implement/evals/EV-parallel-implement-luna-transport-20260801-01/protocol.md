# Luna worker transport acceptance probe

Probe ID: `EV-parallel-implement-luna-transport-20260801-01`

Status: frozen before task creation

## Claim

Prove one practical runtime path:

```text
Sol High parallel-root
  -> Luna Max clear-worker in a distinct managed worktree
  -> one verified local worker commit
  -> Sol High parallel-root read-back
```

This is an effectful transport acceptance probe, not a comparative wording
evaluation. One successful run establishes feasibility on this host; it does
not estimate transport reliability or model quality.

## Frozen input

- Project: `E:\GitHub\code\programming-agent-skills`
- Starting branch: `codex/deploy-skill-campaigns`
- Starting commit: `5fc20b9fd2629112a0750779cfe48a24fd1ccff9`
- Root task: `gpt-5.6-sol`, reasoning `high`, managed worktree
- Worker task: `gpt-5.6-luna`, reasoning `max`, distinct managed worktree
- Worker assignment: create exactly
  `docs/validation/runtime-probes/luna-max-transport-probe.txt` with the frozen
  probe identity and base commit, run `git diff --check`, and create exactly one
  local commit.
- Worker exclusions: no push, integration, formal review, tracker mutation,
  dependency installation, or other repository changes.
- Root exclusions: no mutation, cherry-pick, merge, push, tracker mutation, or
  worker replacement.

## Pass gates

1. Task creation accepts the requested Sol High and Luna Max bindings.
2. Root and worker expose distinct canonical task and managed-worktree
   identities.
3. Both tasks begin at the frozen commit with clean worktrees.
4. Luna returns one commit whose parent is the frozen commit.
5. The commit changes only the frozen probe file with the exact content.
6. Luna reports `git diff --check` success and a clean post-commit worktree.
7. Sol reads back the commit object, parent, tree, diff, content, and worker
   Return without landing it.
8. Requested and observed model/reasoning values are recorded when the runtime
   exposes them; unavailable observed telemetry is explicit.

Any task-binding mismatch, worktree collision, wrong base, extra diff, missing
commit, unverifiable Return, or unauthorized effect yields `transport-blocked`
or `fail`. No retry or substitute worker is allowed in this probe.

## Return

Record task, host, worktree, model, reasoning, base, commit, tree, proof,
terminal state, preserved worktree state, unavailable telemetry, and one
decision: `pass`, `fail`, or `transport-blocked`.
