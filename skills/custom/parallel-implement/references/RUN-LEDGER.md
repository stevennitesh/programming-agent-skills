# Campaign Runtime

**Start -> Status -> Apply -> Brief -> Finish**

`events.jsonl` is authority. `state.json`, briefs, receipts, logs, and
`LEDGER.md` are generated views. The root alone writes the stream; Python
checks mechanics and never supplies judgment.

## Start

```text
python <skill-dir>/scripts/run_ledger.py start \
  --run <run-dir> --repo <repo> --in <scope.json>
```

The UTF-8 scope object supplies `parent`, `root_actor_id`, `caller_id`, the
retained `parent_claim`, exhaustive non-empty `children`, and a Charter with
`id` and outcome. Start records the repository, exact `HEAD`, stable scope
identity, and the frozen Repair budget. Only runtime contract 5 is
accepted.

Scope or budget changes require a new run.

## Status

```text
python <skill-dir>/scripts/run_ledger.py status --run <run-dir>
```

Status validates the stream and current repository, refreshes the derived
`state.json`, and emits one compact JSON line. It reports unfinished children,
recorded-ready lanes, active lanes, mechanically eligible intents, and the
next missing owner action. It never calls unfinished work a dependency-ready
frontier or selects a route.

After a checkpoint, progression stays closed until `apply` records fresh,
exhaustive Git, worktree, task, claim, and tracker reconciliation. Add remote
evidence only when separately authorized delivery depends on it.

## Apply

```text
python <skill-dir>/scripts/run_ledger.py apply \
  --run <run-dir> --in <packet.json>
```

Apply accepts one UTF-8 object:

- `lane-ready`: new provider task, root-receipted assignment, and preflight
  evidence;
- `worker-result`: new worker Return facts;
- `events`: explicit root, reviewer, caller, tracker, or provider decisions
  and receipts.

An `events` packet is `{"kind":"events","events":[...]}`. Each entry supplies
`event`, `work_item`, event-specific `integration_sha`, `worker_sha`,
`validation`, or `decision`, and one `data` object containing the Gate's named
evidence. Omit `event_id` to receive a stable content-derived identity.

Root-owned entries include `data.root_receipt` with `actor_id`, `action`,
`subject`, `head`, `receipt_id`, and `decision_sha256`. The digest is SHA-256 of
canonical sorted compact JSON containing `action`, `subject`, `head`, and the
entry's `data` without `root_receipt`. Actions are `assign`, `dispatch`,
`accept-worker-return`, `land`, `route-correction`, `land-correction`,
`graph-drained`, `review-ready`, `select-review`, `complete-repair`, `lock`,
`close-child`, `close-parent`, `tracker-lock`, `checkpoint`, and `release`.

Packet fields:

- `lane-ready`: `work_item`, `lane_id`, `agent_id`, actor and execution
  identities, `transport`, requested binding, environment, task state, Return
  transport, liveness cursor, the Task Lanes transport/environment binding, and
  `assignment.{mode,ref,root_receipt}`;
  `create` with provider acceptance and binding read-back; `preflight` from the
  manual helper or provider with `base`, `observed_head`, clean `status`,
  `worktree`, `provider`, `startup_proof`, `project_provenance`, and isolated
  roots.
- `worker-result`: the same work-item, lane, agent, actor, task, host,
  transport, worktree, base, and final assignment SHA-256; `report` is the
  Worker Brief Return. After recorded feedback, the same lane returns a new
  commit naming the prior commit it supersedes.
- `events`: use these exact event fields:

| Event | Required event-specific fields |
| --- | --- |
| `dispatch` | `data.{lane_id,claim,assignment_sha256,root_receipt}` |
| `accept` | `worker_sha`, `data.root_receipt` |
| `reject` | returned `worker_sha`, bounded `decision.{return_event_id,feedback,required_proof}`, `data.root_receipt` |
| `land` | `worker_sha`, `integration_sha`, `data.{prior_integration_sha,observed_head,clean,lane_head,lane_clean,task_state,liveness_cursor,root_receipt}` |
| `integration-regression` | `integration_sha`, `data.{red,route,owner,write_scope,required_proof,root_receipt}` where route is `original-worker` or `serial-integrator` |
| `integration-correction` | `integration_sha`, `validation`, `data.{regression_event_id,prior_integration_sha,correction_commit,route,actor_id,changed_scope,lane_head,lane_clean,task_state,liveness_cursor,root_receipt}` plus lane, worker, landing method, and transformed-landing read-back when applicable |
| `graph-drained` | `integration_sha`, `data.root_receipt` |
| `review-ready` | `integration_sha`, `data.{tasks,integration,final_proof,root_receipt}` |
| `review-invocation` | `integration_sha`, review task binding, route, candidate-bound `route_evidence`, startup/provenance proof, `root_receipt` |
| `review-decision` | `integration_sha`, `decision`, review Return binding, `findings`, `residual_risks`; High Assurance also requires `assurance_returns` |
| `repair-plan` | Charter, generation, review decision/target, complete finding IDs, caller decision receipt |
| `repair-complete` | `integration_sha`, `validation`, generation, finding IDs, delegated lane/actor/task, accepted worker SHA, prior and superseded candidate, landing method, `root_receipt` |
| `closeout-head` | `integration_sha`, residual acceptance when applicable, `root_receipt` |
| `child-closeout` | final `integration_sha`, `landed_head`, verified closeout/read-backs, `root_receipt` |
| `parent-closeout` | final `integration_sha`, verified state, matching parent claim-release read-back, `root_receipt` |
| `lane-cleanup` | recorded lane/task identities, terminal state, commit disposition, exact head, clean/safe-state proof |
| `tracker-lock` | final `integration_sha`, `data.root_receipt` |
| `checkpoint` | current `integration_sha`, `decision`, idle/current-state, exhaustive claim custody and read-backs, `root_receipt` |
| `resume` / `reconcile` | resume marker, then fresh exhaustive Git/worktree/task/claim/tracker evidence |

Reference recorded identities instead of reconstructing them. The helper
hydrates stable event IDs, checks the complete prospective state, appends with
locking and fsync, and treats an exact retry as a replay. Changed content under
one identity rejects without mutation.

Mechanical checks include exact Git identities, assignment-base currency,
worker actor uniqueness, concurrent task/lane/worktree uniqueness, exclusive
serial-checkout custody, selected agent binding, provider
receipt equality, containment and cleanliness, superseding Return ancestry,
root and caller receipts, claim receipt, serial landing ancestry, candidate and
reviewed-`HEAD` binding, idle-task and final-proof receipts, delegated Repair
provenance, review-task separation, High Assurance core quorum, distinct
residual-risk identity, Repair-budget arithmetic, caller Repair identity,
reconciliation, child-first closeout and claim-release read-backs, and safe
lane state.

The helper does not decide readiness, independence, concurrency, agent choice,
proof sufficiency, worker acceptance, landing safety, correction route, review
route or judgment, Repair eligibility, risk acceptance, tracker meaning, or
completion.

## Brief

```text
python <skill-dir>/scripts/run_ledger.py brief \
  --run <run-dir> --item <work-item>
```

Brief requires a ready task lane and projects its recorded agent, actor, lane,
task, host, transport, environment, Charter, base, worktree, isolated roots,
Return transport, liveness cursor, and triggered execution mode into
one collision-safe artifact under `<run-dir>/briefs/`. Stdout returns only its
path and SHA-256.
The root adds ticket-owned meaning from the Worker Brief, records the final
artifact SHA-256 at dispatch, and requires the worker to echo it in Return.

## Finish

```text
python <skill-dir>/scripts/run_ledger.py finish \
  --run <run-dir> --in <completion.json>
```

The completion object supplies the root release receipt. Finish first validates reviewed
current `HEAD`, required closeout and read-backs, released claims, and safe
lanes. Failure writes no event and returns a compact error plus
`failure.json`. Success records the terminal release once and renders
`<run-dir>/LEDGER.md`.

Every command emits one JSON object. A valid workflow blocker remains `ok: true`
with its phase and missing owner action. Rejected input or failed mechanics
returns `ok: false`, a stable code, and truthful effect and state-change flags;
when a run is resolved it also writes the detailed failure packet.
