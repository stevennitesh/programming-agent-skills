# Agent lanes

Use this reference when concurrent workers need checkout isolation or when
their lanes need cleanup.

## Prepare

Use Python 3 and Git. Select an allowed worktree root outside the repository;
the helper rejects an in-repository root. Respect configured workspace placement
and permissions. If suitable placement is unavailable, retain the scope and
fall back to serial work rather than bypassing isolation. The root alone runs
helper operations, sequentially; this helper does not supply a multi-root lock.
It owns only lanes it prepared, not host-created or unrelated worktrees.

Create each concurrent lane from integration `HEAD` at dispatch. Siblings
selected together share that base. A later dependent lane uses the newer
integration `HEAD` after its predecessors land:

```text
python <skill-dir>/scripts/lane_worktree.py prepare \
  --repo <repo> --root <worktree-root> --base <sha> --name <lane-name>
```

Start the worker only when the result says `ok: true`. The helper persists the
returned lane packet as `lane_manifest`. Pass the whole packet to the
worker and retain it in the root's run-local cleanup set until verification
discharges it. It includes absolute `worktree`, `runtime_root`, `temp_root`,
`cache_root`, `pytest_basetemp`, `pytest_cache`, and cleanup paths. The worker
must confirm the lane's `HEAD` and clean status before mutation, use the
worktree for every repository and Git command, and route temporary files,
tests, package caches, generated databases, and logs to the returned runtime
paths when the tool supports redirection. Record any off-contract runtime path;
it invalidates proof when it can change repository bytes, shared state,
cleanup, or the truth of proof.

One active writer owns each lane. Worktrees still share repository refs and
stash state, so concurrent workers must not stash, switch or rebase shared
branches, or mutate shared refs. Assign or serialize every writable resource
outside the checkout.

Before a worker return, record its exact proof commands and runtime paths, then
stop every background process and command session it started. A worker response
does not prove process exit.

## Inspect

Inspect after a worker returns, before replacement, before landing or cleanup,
and when resuming interrupted work:

```text
python <skill-dir>/scripts/lane_worktree.py inspect \
  --repo <repo> --root <worktree-root> --lane <path>
```

The result reports manifest validity, registration, `HEAD`, clean and
integration state, runtime directory presence, cleanup receipt state, known
checkout-local cache violations, and mechanical eligibility. `ok: true` means
inspection succeeded; it does not make the lane eligible to resume, land, or
clean up. Require `mechanical.resume_or_land_eligible` before normal resume or
landing and `mechanical.cleanup_eligible` before cleanup. For dirty partial work,
use the exclusive-custody repair path in [Recovery](recovery.md). The helper
cannot prove that an actor or
command session stopped. The root checks that separately. Never infer
cancellation from silence and never start a replacement while the prior actor
may still write.

## Cleanup

Before removing even a successful lane, retain evidence needed for unresolved
failures and establish that ignored lane artifacts are disposable. Clean Git
status does not protect ignored files. Preserve user-created or externally owned
artifacts even when Git does not track them.

After landing, pass only explicitly completed lanes:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup \
  --repo <repo> --root <worktree-root> --completed <path>
```

After the root confirms actor quiescence, the helper removes only a named lane
that is clean and integrated into current repository `HEAD`. It also supports
an exact retry after Git removed the worktree but helper-owned state remains.
Dirty, unintegrated, active, or uncertain work stays in place.

Before unregistering a lane, the helper records exact retry authority. Runtime
cleanup failure preserves the registered checkout and its recovery state. The
helper rechecks lane identity and integration ancestry immediately before
unregistering, and a pending cleanup blocks lane reuse.

After every cleanup attempt, verify the full retained set:

```text
python <skill-dir>/scripts/lane_worktree.py verify-cleanup \
  --repo <repo> --root <worktree-root> \
  --integration-head <proved-sha> \
  --lane <path> [--lane <path> ...]
```

The result names lanes that need cleanup, exact retry, or preservation. Pass
every retained lane and finish only when `finish_clean` is true for the proved
integration `HEAD`.

With a version-controlled tracker, pass final delivery HEAD H after the tracker
reference's C..H evidence-applicability check, not the earlier proved code commit C.

The helper never forces removal, deletes branches, changes global Git config,
or chooses a lane on the caller's behalf.
