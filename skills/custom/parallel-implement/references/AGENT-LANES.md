# Agent Lanes

**Prepare -> Dispatch -> Await -> Release**

Task context and checkout isolation are separate facts. Delegate every writer;
isolate concurrent writers.

## Prepare

Load [RUNTIME-PROFILES.md](RUNTIME-PROFILES.md).

`run_ledger.py dispatch` reads the writable lane root from the repo-local setup
owned by `$repo-bootstrap`. Spawned agents inherit its permission.

Give one serial writer exclusive custody of the clean integration checkout at
the exact base. The root performs no repository or Git mutation until Return.

Give every concurrent writer a distinct helper-created worktree at the exact
base. Prepare it with `../scripts/lane_worktree.py`; only `ok: true` is
dispatchable. Never assign one worktree to two active writers. The helper also
creates checkout-external pytest temp and cache roots and runs a quick pytest
collection smoke. A serial writer needs no worktree automation.

For an isolated lane, `--repo` is the root checkout and `--root` is its writable
worktree root. The worker writes only in its assigned worktree.

After all writers stop, formal reviewers use the immutable candidate read-only
in the integration checkout. High Assurance reviewers may share that checkout
because none may write.

## Dispatch

Run dispatch `prepare` after the root chooses the item, profile, environment,
write scope, and claim. It prepares the checkout, seals the final brief, records
pre-spawn authorization, and returns exact fresh-context collaboration subagent
spawn arguments. Spawn once with those arguments. Record the accepted provider identity through
dispatch `receipt`; only then is the lane active.

The receipt binds requested and observed-or-unavailable profile, transport `subagent-v2`,
environment, provider, checkout, task, and liveness identity. Supply observed
facts explicitly; the helper derives none of them.
The accepted request is binding evidence when resolved telemetry is
unavailable; never invent telemetry.

Implementation and integration mismatches return `transport-blocked`. Formal
review mismatches return `transport-invalid` before candidate judgment.

Dispatch generates writer assignments through
[WORKER-BRIEF.md](WORKER-BRIEF.md).

Formal review is read-only and has no writer lane. Spawn the selected review
agent from the pinned, hashed Review packet, then record its assignment path and
SHA-256 with the observed task and provider receipt in `review-invocation`.

## Await

Wait on the recorded collaboration subagent. A missed checkpoint without
progress triggers inspection, not duplicate dispatch. Reconcile its state,
checkout, `HEAD`, status, commit, and claim before stopping or replacing it.
Preserve dirty or uncommitted work.

Accept only a Return matching the recorded work item or candidate, profile,
actor, lane, checkout, base, and produced or reviewed `HEAD`.

Keep a clean isolated worker and worktree available through landing when a
pre-landing correction is plausible. Return that correction to the same worker
and accept only a Return naming the commit it supersedes and the root feedback
event as its current assignment reference.

If the provider confirms no task was created, clean or preserve the prepared
lane as `not-created` and dispatch a new attempt. Reconcile uncertain outcomes
instead of spawning again.

## Release

At graph end, run `lane_worktree.py cleanup` once without `--oldest` to remove
all safe completed lanes. When the worktree limit is reached, run it with
`--oldest` to free the oldest safe completed lane. Pass each explicitly
completed worktree with `--completed`; omit active or uncertain lanes. Dirty,
not-completed, unintegrated, and uncertain lanes stay preserved; a
capacity-blocked result means no new concurrent worker may start.

Serial and review agents own no extra worktree to release.

## Isolated Worktree

```text
python <skill-dir>/scripts/lane_worktree.py prepare \
  --repo <repo> --root <worktree-root> --base <sha> --name <lane-name>
```

`prepare` creates or reuses `<worktree-root>/<lane-name>` at the exact base. It
checks registration, `HEAD`, clean status, basic Git operation, and pytest
collection using a fresh process-temp directory with temp, base-temp, and cache
children. Those generated paths remain outside the tracked checkout and the
shared worktree root. Success returns the worktree and generated paths needed
to start the worker; failure returns the cause and preserves any created lane
for inspection or retry.

```text
python <skill-dir>/scripts/lane_worktree.py cleanup \
  --repo <repo> --root <worktree-root> [--completed <path>] [--oldest]
```

Cleanup considers only registered worktrees contained by the explicit root. A
lane is safe to remove only when it is explicitly completed, clean, and its
`HEAD` is already integrated into the root checkout's current `HEAD`. Forced removal,
branch deletion, global `safe.directory` mutation, and cleanup outside the
explicit root remain outside helper authority. Cleanup never recursively
deletes worker-writable temp state; the process temp owner may reclaim it.
