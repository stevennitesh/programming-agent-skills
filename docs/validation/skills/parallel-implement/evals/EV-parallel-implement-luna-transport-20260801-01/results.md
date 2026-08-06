# Luna worker transport acceptance results

Probe ID: `EV-parallel-implement-luna-transport-20260801-01`

Decision: **pass**

One Sol High task created one Luna Max task in a distinct managed worktree.
Luna returned one verified local commit, and the Sol task independently read the
commit back without landing it.

## Binding receipt

| Role | Requested binding | Canonical task | Host | Managed worktree |
|---|---|---|---|---|
| `parallel-root` | `gpt-5.6-sol` / `high` | `019fbe23-2aef-7bc3-a368-3a7c12d6540f` | `local` | `E:\GitHub\code\worktrees\codex\da91\programming-agent-skills` |
| `clear-worker` | `gpt-5.6-luna` / `max` | `019fbe23-af8f-7bb1-be85-2ea551da29fb` | `local` | `E:\GitHub\code\worktrees\codex\d9e9\programming-agent-skills` |

The task-creation interface accepted both requested model/reasoning bindings.
Task read-back did not expose runtime model and reasoning telemetry; the caller
inspected the Codex UI and confirmed the observed bindings matched the requests:
Sol High / High and Luna Max / Max.

Task IDs and worktrees were canonical and distinct before the worker assignment
was dispatched.

## Worker Return

- Starting commit: `5fc20b9fd2629112a0750779cfe48a24fd1ccff9`
- Worker commit: `95b0f94cb02654ec93ae93ef3c4f8b556aef0b87`
- Parent: `5fc20b9fd2629112a0750779cfe48a24fd1ccff9`
- Tree: `c8cec4296d5ee45a91e51ffec9785695ebc5ce0d`
- Message: `test: prove Luna Max task transport`
- Changed path:
  `docs/validation/runtime-probes/luna-max-transport-probe.txt`
- Blob: `46472cf6a8fa5fa3f6e0398d5c6df082f6b2bce1`
- Payload: exact 124-byte UTF-8 content with final LF
- Payload SHA-256:
  `7fda68b8080e845cc148d78fbaba30685a4f8247a767ed50d61978ec6280eea3`
- `git diff --check`: exit `0`, no output
- Final worker worktree: clean

## Sol read-back

The Sol task verified the raw commit object, sole parent, tree, full changed
path, exact payload bytes, SHA-256, commit message, diff check, and clean worker
state. This task repeated the parent, tree, path, SHA-256, and clean-state
checks after the Sol Return.

The current checkout remained at
`5fc20b9fd2629112a0750779cfe48a24fd1ccff9`, and the probe path is absent from
it. No cherry-pick, merge, integration, formal review, push, tracker mutation,
installation, replacement worker, or additional worker task occurred.

Both managed worktrees remain provider-preserved with their idle tasks. Codex
owns their cleanup; no manual cleanup was attempted.

## Gate result

| Gate | Result |
|---|---|
| Sol task binding accepted | pass |
| Luna Max task binding accepted | pass |
| Distinct canonical task identities | pass |
| Distinct managed worktrees | pass |
| Exact clean starting commit | pass |
| One local worker commit | pass |
| Exact parent, path, and content | pass |
| Clean proof and final worker state | pass |
| Sol commit-object read-back | pass |
| No integration or unauthorized effect | pass |
| Observed model/reasoning telemetry | pass; caller verified in Codex UI |

## Runtime friction

- The first project-list call reported no registered handler; an unchanged
  retry succeeded.
- One pre-probe root-creation request included an unsupported extra field and
  created no task or worktree. Read-back confirmed absence before the valid
  request created the sole Sol root task.
- Sol's first direct worker-worktree read hit Git ownership protection. It
  retried with a command-scoped `safe.directory` value for that exact worktree;
  global Git configuration remained unchanged.

These events caused no duplicate worker, state mutation, identity ambiguity, or
evidence loss.

## Conclusion

The practical transport path is feasible on this host:

```text
Sol High parallel-root
  -> Luna Max clear-worker in an isolated managed worktree
  -> one verified local commit
  -> Sol High parallel-root verification
```

This single probe establishes feasibility, not reliability frequency or worker
implementation quality.
