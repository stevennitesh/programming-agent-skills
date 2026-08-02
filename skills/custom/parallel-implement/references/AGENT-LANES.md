# Agent Lanes

**Prepare -> Dispatch -> Await -> Release**

Task context and checkout isolation are separate facts. Delegate every writer;
isolate concurrent writers.

## Prepare

Load [RUNTIME-PROFILES.md](RUNTIME-PROFILES.md).

Read the permanent project key and writable lane root from the repo-local setup
owned by `$repo-bootstrap`. The key is shaped
`<short-name>-<three-digit-ID>`, and the root is
`<base-root>/<project-key>/wt`. Spawned agents inherit its permission. Do not
put lane permissions in agent-role TOMLs.

Give one serial writer exclusive custody of the clean integration checkout at
the exact base. The root performs no repository or Git mutation until Return.

Give every concurrent writer a distinct helper-created worktree at the exact
base. Open it with `../scripts/lane_worktree.py`; only `ok: true, state: ready` is
dispatchable. Never assign one worktree to two active writers.

For an isolated lane, `--repo` is the root checkout. The helper supplies it to
startup proof as `PARALLEL_IMPLEMENT_ROOT_CHECKOUT`; the worker may read needed
ignored inputs there but writes only in its assigned worktree.

After all writers stop, formal reviewers use the immutable candidate read-only
in the integration checkout. High Assurance reviewers may share that checkout
because none may write.

## Dispatch

Spawn one fresh-context collaboration subagent for the selected profile. Use
the profile's named custom agent type when present; otherwise use `default` and
supply its model and reasoning explicitly. Assign the exact role, work item or
candidate, base, absolute checkout, actor and lane identities, and Return
transport. The agent echoes the binding before work.

Record the accepted spawn receipt, requested and observed-or-unavailable
binding, transport `subagent-v2`, environment, provider, checkout, base, clean
status, startup proof, and liveness identity. The accepted request is binding
evidence when the runtime exposes no resolved telemetry; never invent it.

Implementation and integration mismatches return `transport-blocked`. Formal
review mismatches return `transport-invalid` before candidate judgment.

Generate writer assignments through [WORKER-BRIEF.md](WORKER-BRIEF.md).

## Await

Wait on the recorded collaboration subagent. A missed checkpoint without
progress triggers inspection, not duplicate dispatch. Reconcile its state,
checkout, `HEAD`, status, commit, and claim before stopping or replacing it.
Preserve dirty or uncommitted work.

Accept only a Return matching the recorded work item or candidate, profile,
actor, lane, checkout, base, and produced or reviewed `HEAD`.

Keep a clean isolated worker and worktree available through landing when a
pre-landing correction is plausible. Return that correction to the same worker
and accept only a Return naming the commit it supersedes.

## Release

After the commit is integrated or preserved and no correction needs the lane,
run `lane_worktree.py cleanup` with its recorded project key, base root,
worktree, run and item IDs, expected `HEAD`, and disposition. Cleanup must
report `removed`; otherwise preserve the lane and return its exact recovery
state.

Serial and review agents own no extra worktree to release.

## Isolated Worktree

```text
python <skill-dir>/scripts/lane_worktree.py open \
  --repo <repo> --project-key <name-NNN> --base <sha> \
  --run-id <run> --item-id <item> --actor-id <actor> \
  --proof-command-file <argv.json> --python-provenance-file <python.json>
```

The helper owns `<base-root>/<project-key>/wt/<lane>`. It binds the permanent
project key to one repository with a marker outside `wt`; a conflicting or
unmarked project root blocks creation. Lane names omit the repository name.

Base-root selection is explicit `--base-root`, then
`PARALLEL_IMPLEMENT_BASE_ROOT`, then `<repo-drive>:\pi` on Windows or
`<repo-parent>/worktrees` elsewhere. Detached `HEAD` is the default. `--repo`
remains the read-only root checkout; the isolated worktree remains the command
working directory. On Windows, the worktree path plus the longest tracked path
at the selected base must not exceed 259 characters. Keep `pi` and `wt` short;
use temporary storage only for the UTF-8 argv files. Correct a failed preflight
and repeat the same `open`; it reuses the preserved lane.
Startup proof uses one UTF-8 argv array without a shell and the repository's
verified executable. It proves viability, not throughput; disable parallel
test execution such as with `-n 0`.
Derive executables, import roots, and packages from repo-owned configuration.
Project imports must resolve beneath the lane, including namespace-package
locations. A non-Python repository may use
`--skip-python-provenance` with its reason. Missing startup proof may use
`--skip-proof` with its reason. Either skip remains residual risk.

```text
python <skill-dir>/scripts/lane_worktree.py cleanup \
  --repo <repo> --project-key <name-NNN> --base-root <root> --worktree <path> \
  --run-id <run> --item-id <item> \
  --expected-head <sha> --disposition <integrated-or-preserved>
```

Cleanup verifies the project marker, recomputes the exact helper-created lane
path, then verifies containment, exact `HEAD`, clean status, and disposition.
Lost registration remains preserved. A confirmed contained unregistered
residual may use the helper's extended-path cleanup.
Forced removal, branch deletion, global `safe.directory` mutation, and cleanup
outside the recorded root remain outside helper authority.
