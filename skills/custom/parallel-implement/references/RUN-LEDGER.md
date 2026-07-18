# Campaign State and Ledger

Use this before the first campaign event, on every resume, before an authority transition, and at closeout.

`events.jsonl` is the sole campaign source of truth. `LEDGER.md` is generated output. The orchestrator is the sole writer.

## Commands

Initialize once:

```text
python <skill-dir>/scripts/run_ledger.py init --events <run-dir>/events.jsonl
```

Append one JSON event through `--stdin`, one flag-built event, or an atomic JSON-array batch through `append-batch --from-file`. Use file or stdin input for evidence packets that would otherwise require escaped shell prose.

```text
python <skill-dir>/scripts/run_ledger.py append --events <events> --stdin
python <skill-dir>/scripts/run_ledger.py append-batch --events <events> --from-file <packet.json>
```

`validate` checks event-stream structure. `validate-state --intent <dispatch|land|review|repair|lock|push|complete>` checks event fields, ordering, reconciled state, SHA continuity, lane disposition, and the requested authority. Append success records evidence; only a successful intent check grants authority.

```text
python <skill-dir>/scripts/run_ledger.py validate-state --events <events> --intent <intent> --repo <repo>
```

Use `status` during a live campaign, `resume-status` after interruption, and `closeout-plan` after accepted review. Each returns machine-readable errors, lane classifications, and next actions.

Render the human ledger after material state changes and at Release:

```text
python <skill-dir>/scripts/run_ledger.py render --events <events> --repo <repo> --output <run-dir>/LEDGER.md
```

## Progressive Evidence

Record evidence when its gate becomes actionable:

- **Scope:** Charter identity, parent, Source Trace, fixed point, exhaustive children, dependencies, exclusions or owner-approved dispositions, closeout rule, Repair Budget, and whether push is required.
- **Dispatch:** frontier, readiness, Tripwire result, Downshift decision, lane provider, preflight packet, stable temp roots, proof budget, claim read-back, permission route, and liveness checkpoint.
- **Integration:** accepted worker SHA, landing executor and mode, integration SHA, touched-area proof, stale-base or conflict state, and relationship fingerprint.
- **Review:** graph-drained evidence, final validation, immutable review target, route, mode, complete classified findings, decision, and accepted residual risk.
- **Repair:** blocked snapshot, Charter identity, generation, every blocking finding ID, owner and write scope, required proof, integrated repair HEAD, and completion proof.
- **Lock:** approved closeout HEAD, structured child packets, child-first mutations and read-backs, parent closeout, push, remote verification, and release disposition.

The executable event names and required transition fields live in `run_ledger.py`; do not duplicate that interface in handwritten Markdown.

## State Invariants

Semantic validation enforces at least:

- lane creation before preflight before dispatch;
- dispatch before acceptance or rejection;
- acceptance before landing, with matching worker SHA;
- an exhaustive execution-drained graph before Review;
- review-ready before an immutable target and decision;
- blocked review plus one `repair-plan` tied to that decision event and snapshot before Repair authority;
- every blocking finding admitted as `automatic-in-scope` and batched once;
- `repair-complete` with matching generation, finding IDs, integrated HEAD, and proof before successor Review;
- no more than the Charter's maximum two Repair generations;
- accepted review target equal to integration and closeout `HEAD`;
- verified child closeout before parent closeout;
- pushed SHA equal to the approved closeout SHA;
- safe disposition for every lane before `complete`.

After a `resume` event, dispatch, landing, Review, Lock, and push remain closed until one `reconcile` event records Git, worktree, agent, and tracker evidence. The ledger proves internal consistency; reconciliation supplies external observations.

## Structured Child Closeout

Update a child's `child-closeout` event as it moves through `draft`, `review-final`, `posted`, and `verified`. A verified packet supplies every field in `run_ledger.py`'s `CLOSEOUT_FIELDS`.

The renderer owns tracker-comment and ledger prose. Post only rendered content, then append the comment reference and mutation read-back. When a mutation may have happened without recorded read-back, refetch first; never replay uncertain mutation.

## Resume and Closeout

`resume-status` classifies lanes as active, clean-uncommitted, committed-unlanded, landed, dirty-preserved, or residual. Reconcile those classifications against the actual checkout, Git registration, process or agent, tracker claim, and remote state before appending `reconcile`.

`closeout-plan` returns remaining child, parent, push, and lane actions. Execute it serially and rerun it after each external mutation. Release is complete only when `validate-state --intent complete` passes; generated prose cannot override that result.
