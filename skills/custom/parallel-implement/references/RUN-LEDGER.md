# Campaign Runtime

**Start -> Status -> Dispatch -> Apply -> Finish**

`events.jsonl` is authority. Generated state, assignments, receipts, and
`LEDGER.md` are views. The root supplies decisions; the helper performs
deterministic checks, hashing, and recording.

## Start

```text
python <skill-dir>/scripts/run_ledger.py start \
  --run <run-dir> --repo <repo> --in <scope.json>
```

The scope object supplies:

- `root_actor_id` and `caller_id`;
- the retained `parent_claim`;
- `charter.id`, outcome, and optional Repair budget;
- `tracker_snapshot.{path,sha256}` from the configured tracker snapshot
  operation.

The snapshot file lives inside the run directory and contains the full parent
graph, ticket packets, comments, labels, assignees, and verified dependency
edges. Start derives the ordered graph from it, verifies its digest, records
exact repository `HEAD`, and binds runtime contract 7. Scope changes require a
new run.

## Status

```text
python <skill-dir>/scripts/run_ledger.py status --run <run-dir>
```

Status validates the stream and current checkout, refreshes `state.json`, and
returns the next missing owner action. It reports mechanics; it does not choose
the frontier, concurrency, worker profile, proof, review, or completion.

After a checkpoint, use `apply` to record exhaustive Git, worktree, task,
claim, and tracker reconciliation before progression reopens.

## Dispatch

Prepare one final assignment before spawning:

```text
python <skill-dir>/scripts/run_ledger.py dispatch \
  --run <run-dir> --in <prepare.json>
```

`prepare.json` supplies `kind: prepare`, `work_item`, semantic `profile`,
`actor_id`, stable `attempt_id`, `environment: local | worktree`,
`assignment.{mode,ref}`, retained child `claim`, non-empty `write_scope`, and
optional assignment `instructions`. An isolated lane may also supply startup
proof and Python provenance files; otherwise the helper reads the repo-local
parallel-lane setup.

The command prepares the lane and brief, then atomically records assignment and
dispatch receipts plus pre-spawn authorization and returns the exact
collaboration spawn arguments. The brief contains no
provider-created task identity. Spawn once from this output; do not send a
second assignment message.

If this command's output is lost before spawn, repeat the unchanged preparation
packet to recover the same sealed brief and spawn arguments without another
lane or event.

After the provider accepts the spawn, record its canonical identity:

```text
python <skill-dir>/scripts/run_ledger.py dispatch \
  --run <run-dir> --in <receipt.json>
```

`receipt.json` supplies `kind: receipt`, the same `attempt_id`, canonical task
identity and state, liveness cursor, provider, checkout, environment match, and
observed-or-unavailable model and effort telemetry. The command binds the
provider task to the authorized lane. Until this receipt lands, state remains
`spawn-authorized`, never active.

A confirmed rejected spawn creates no task. Clean or preserve the prepared lane
with `terminal_task_state: not-created`, then dispatch a new attempt. Reconcile
an uncertain spawn outcome; never duplicate it.

## Apply

```text
python <skill-dir>/scripts/run_ledger.py apply \
  --run <run-dir> --in <packet.json>
```

Apply accepts:

- `worker-result`: exact work-item, agent, actor, task, lane, checkout, base,
  assignment reference and SHA-256, plus the Worker Brief Return;
- `events`: explicit root, reviewer, caller, tracker, integration, cleanup, or
  provider decisions and receipts.

`events` packets are `{"kind":"events","events":[...]}`. Omit an event ID to
receive a stable content-derived identity. Root-owned decisions carry the
recorded root receipt. Dispatch-owned `lane-create`, `lane-preflight`,
`dispatch`, and `spawn-receipt` cannot enter through this generic surface.

The reducer rehashes the frozen tracker snapshot and enforces exact Git and assignment identities, exclusive lane and
task custody, profile binding, Return provenance, landing ancestry, review
independence and quorum, Repair budget, closeout order, claim read-back, and
safe lane state. Exact `apply` event retries replay; changed content under one
identity rejects without mutation.

## Finish

```text
python <skill-dir>/scripts/run_ledger.py finish \
  --run <run-dir> --in <completion.json>
```

Finish verifies reviewed current `HEAD`, closeout read-backs, released claims,
and safe lanes before recording the root release and rendering `LEDGER.md`. Failure
records no event and returns compact JSON plus `failure.json`.

Every command emits one JSON object. `ok: true` may still name a workflow
blocker or missing owner action. Invalid input or failed mechanics returns
`ok: false` with truthful effect and change flags.
