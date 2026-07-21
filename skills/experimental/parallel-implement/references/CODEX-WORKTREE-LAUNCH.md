# Isolated Lane Lifecycle

Fresh context does not isolate a checkout. Every dispatched worker needs both. Campaign start also classifies the integration checkout as either user-owned `existing-checkout` or campaign-owned `managed-integration-worktree`; unknown ownership blocks lane creation.

## Open

For a manual Git lane, create and preflight in one command:

```text
python <skill-dir>/scripts/lane_worktree.py open \
  --repo <repo> --base <sha> --run-id <run> --item-id <item> --actor-id <actor> \
  --proof-command-file <argv.json> --python-provenance-file <python.json>
```

Root selection is explicit `--root`, then `PARALLEL_IMPLEMENT_WORKTREE_ROOT`, then `E:\pi` on Windows or `<repo-parent>/worktrees/parallel-implement` elsewhere. Windows defaults to maximum path `320`; override only from recorded repository evidence. Detached HEAD is the worker default; pass `--branch` only for a routed integrator.

For a campaign-owned integration checkout, use the same lifecycle helper with an explicit branch and role:

```text
python <skill-dir>/scripts/lane_worktree.py open \
  --role integration --branch <campaign-branch> \
  --repo <repo> --base <sha> --run-id <run> --item-id integration --actor-id <actor> \
  --proof-command-file <argv.json> --python-provenance-file <python.json>
```

Never remove an `existing-checkout`; its cleanup authority is `none`. A managed integration worktree has helper-owned lifecycle authority and uses the same verified cleanup and residual-recovery path as a worker lane.

The helper verifies containment and path budget before mutation, creates the worktree, verifies its registration and base, and performs preflight. `ok: true, state: ready` is the only dispatchable result. A preflight failure preserves the created lane and returns the exact retry route.

Use a runtime-managed lane only when the provider supplies its identifier and absolute path and owns cleanup. Provider namespaces never overlap.

## Startup proof

Supply one UTF-8 JSON argv array through `--proof-command-file`; inline JSON is acceptable for simple commands. The helper never invokes a shell. Preflight proves viability, not throughput, so disable test parallelism by default (`-n 0` for pytest/xdist) unless concurrency is itself under proof.

Use the repository's verified Python executable. A shared environment may provide dependencies, but project imports must resolve beneath the lane. Supply one UTF-8 provenance object:

```json
{
  "executable": "<absolute verified Python executable>",
  "import_roots": ["<repo-owned project root>"],
  "packages": ["project_package"]
}
```

The helper resolves every root beneath the lane, imports each package in isolated Python, and rejects concrete origins or namespace-package locations outside it. Derive roots from repo-owned configuration; do not assume one layout. When the repository has no importable project package, explicitly use `--skip-python-provenance --python-provenance-reason <reason>` and carry the residual risk.

When no startup proof exists, use `--skip-proof --reason <reason>`. A skipped check is evidence of a gap, not a pass.

The ready packet includes exact root, worktree, base, branch state, clean status, checkout/index/object write probes, Git trust route, actor ID, proof and provenance, and stable `temp_root`, `pytest_basetemp`, and `cache_root`. Pass those exact values to the worker.

## Dispatch and liveness

Apply the ready packet to the ledger, generate the brief, and launch one direct fresh-context child. Every command and edit targets the recorded worktree.

A missed liveness checkpoint plus no actor or process progress triggers inspection, not duplicate dispatch. Stop the actor, reconcile child processes, then inspect registration, root, HEAD, status, commit, patch, temp roots, and claim. Preserve dirty or uncommitted work. Never start two writers in one inherited lane.

## Recovery commands

`create` and `preflight` remain separately callable for diagnosis and retry. Retry only after the observed base, root, trust, permission, capability, startup proof, or conflicting filesystem state changes.

On resume, reconcile provider identity, registration, directory, HEAD, status, actor/process, commit disposition, temp roots, claim, and ledger packet. Missing is not done.

## Cleanup

Make the lane idle and record its commit as integrated or preserved, then run:

```text
python <skill-dir>/scripts/lane_worktree.py cleanup --role <worker|integration> --repo <repo> --root <root> --worktree <path> --expected-head <sha> --disposition <integrated-or-preserved>
```

The helper verifies containment, exact HEAD, clean status, and disposition before unregistering. If Git unregisters but leaves a directory, containment-checked extended-path cleanup runs in the same invocation. A successful fallback remains `ok: true, state: removed` and retains Git's raw error as diagnostics.

Safe terminal states are `removed`, `provider-preserved`, or an explicitly accepted `unregistered-residual-directory`. Dirty, registered, unpreserved, or unknown state blocks complete.

Lost registration cannot be reverified automatically. Preserve the residual until explicit cleanup authority permits `purge-residual --confirm-unregistered-residual` beneath the recorded root.

Forced removal, branch deletion, global `safe.directory` mutation, and cleanup outside the recorded root are outside helper authority.
