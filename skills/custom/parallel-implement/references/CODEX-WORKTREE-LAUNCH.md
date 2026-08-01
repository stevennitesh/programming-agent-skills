# Codex Task Lanes

**Route -> Create -> Bind -> Await -> Close**

Task context and checkout isolation are separate facts. Delegate every writer;
isolate concurrent writers.

## Route

This table records the skill pack's semantic agent bindings. The task runtime
resolves these IDs; an unavailable or mismatched binding is `transport-blocked`.

| Agent ID | Model | Reasoning |
| --- | --- | --- |
| `parallel-root` | `gpt-5.6-sol` | `high` |
| `clear-worker` | `gpt-5.6-luna` | `max` |
| `adaptive-worker` | `gpt-5.6-terra` | `max` |
| `fast-adaptive-worker` | `gpt-5.6-sol` | `medium` |
| `demanding-worker` | `gpt-5.6-sol` | `high` |
| `serial-integrator` | `gpt-5.6-sol` | `medium` |
| `ordinary-reviewer` | `gpt-5.6-sol` | `high` |
| `assurance-coordinator` | `gpt-5.6-sol` | `high` |
| `har-spec-reviewer` | `gpt-5.6-sol` | `xhigh` |
| `har-standards-reviewer` | `gpt-5.6-sol` | `xhigh` |
| `har-specialist` | `gpt-5.6-sol` | `xhigh` |

Escalate `serial-integrator` to `high` only for conflicting architectural
intent, cross-module invariants, migrations or compatibility behavior,
security-sensitive boundaries, or a repeated failed correction.

## Create

For serial work, delegate from the exact base in the integration checkout:

- `clear-worker`: create a local Codex task;
- `adaptive-worker`, `fast-adaptive-worker`, `demanding-worker`, or
  `serial-integrator`: use a same-checkout Subagents V2 task.

Record exclusive worker custody. Until Return, the root performs no repository
or Git mutation. For concurrent work, create one separate Codex task and
distinct Codex-managed worktree per worker. Never create a manual Git worktree
for a task that also owns a managed worktree.

For formal review, create a fresh read-only Codex task bound to the immutable
candidate. Use the local checkout only after every writer stops; otherwise use
a distinct managed worktree. The `assurance-coordinator` alone creates its core
and specialist tasks using their recorded bindings.

Supply the selected model and reasoning. Start Codex tasks with a non-mutating
bootstrap containing the role, work item or candidate, exact base, and the
instruction to wait for Bind.

Task creation is asynchronous. A returned client task ID is provisional. Bind
no lane as ready until the canonical task ID and host ID are available.

## Bind

Record one immutable launch receipt:

- assignment identity (work item or candidate), semantic agent ID, actor ID,
  lane ID;
- task ID, host ID, transport (`codex-task` or `subagent-v2`), and task state;
- requested model and reasoning, plus resolved values when exposed;
- local or managed-worktree environment, absolute worktree, and provider;
- exact base, clean status, startup proof, project provenance, and stable temp,
  pytest, and cache roots;
- report transport and liveness cursor.

The accepted task-creation request is binding evidence for requested model,
reasoning, and environment. Mark unavailable resolved telemetry explicitly;
never invent it.

The task reconciles its receipt, current directory, `HEAD`, clean status,
project imports, and temp roots before editing. Dispatch is ready only when the
canonical task, binding, checkout, and exact base agree. Preserve the claim and
return `transport-blocked` on mismatch.

Every new lane gets a distinct actor identity. Distinct concurrent tasks must
also have distinct task and managed-worktree identities. Only one delegated
writer may hold the integration checkout.
After recording the receipt, augment the ledger-owned assignment, record its
final SHA-256 in the dispatch receipt, and send the bound
[Worker Brief](WORKER-BRIEF.md) or review packet through the task transport.
Mutation or review starts only after the task echoes the binding and dispatch
SHA-256.

## Await

Wait on canonical task IDs. A missed checkpoint without task progress triggers
inspection, not duplicate dispatch. Reconcile task state, cursor, worktree,
`HEAD`, status, commit, processes, temp roots, and claim before continuing,
stopping, or replacing a task. Preserve dirty or uncommitted work.

Accept a Return only through the recorded task transport with matching work
item or candidate, agent, actor, lane, task, worktree, base, and produced or
reviewed `HEAD` identities.

Keep a clean worker task and checkout idle while its Return awaits landing and,
when useful, through formal Review. Send pre-landing feedback to that task and
accept only a Return naming the commit it supersedes. Replace that lane only
when its binding, custody, or authority is invalid.

## Close

After Review no longer needs the worker, record the task terminal state and its
subject as integrated, preserved, or reviewed before disposing the lane.

Codex owns managed-worktree cleanup. Record it as `provider-preserved` until the
provider reports removal or preserved custody; never run the manual helper
against it. A manually created lane follows Manual Lane cleanup below.

Safe terminal states are `removed`, `provider-preserved`, or an explicitly
accepted `unregistered-residual-directory`. Dirty, registered, unpreserved, or
unknown state blocks campaign completion.

## Manual Lane

Use a manual lane only for an explicitly authorized serial or recovery route
that does not also create a managed-worktree task:

```text
python <skill-dir>/scripts/lane_worktree.py open \
  --repo <repo> --base <sha> --run-id <run> --item-id <item> --actor-id <actor> \
  --proof-command-file <argv.json> --python-provenance-file <python.json>
```

Root selection is explicit `--root`, then
`PARALLEL_IMPLEMENT_WORKTREE_ROOT`, then `E:\pi` on Windows or
`<repo-parent>/worktrees/parallel-implement` elsewhere. Detached `HEAD` is the
default; pass `--branch` only when the authorized recovery route requires it.
Windows defaults to maximum path `320`; use no extended-path prefix.

`ok: true, state: ready` is the only dispatchable result. Startup proof uses
one UTF-8 argv array without a shell and the repository's verified executable.
Project imports must resolve beneath the lane. A repository with no importable
package may use `--skip-python-provenance` with its reason; missing startup proof
may use `--skip-proof` with its reason. Either skip remains residual risk.
The startup command proves viability, not throughput; disable parallel test
execution such as with `-n 0`. Derive executables, import roots, and packages
from repo-owned configuration, and verify ordinary and namespace-package
locations beneath the lane.

After the lane is idle and its commit is integrated or preserved:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup --repo <repo> --root <root> --worktree <path> --expected-head <sha> --disposition <integrated-or-preserved>
```

Cleanup verifies containment, exact `HEAD`, clean status, and disposition.
Lost registration remains preserved. Under explicit residual-removal authority,
repeat cleanup with `--confirm-unregistered-residual`.
Forced removal, branch deletion, global `safe.directory` mutation, and cleanup
outside the recorded root remain outside helper authority.
