# Campaign Runtime

`events.jsonl` is the sole campaign source of truth. `LEDGER.md` is generated. The root is the sole writer.

## Normal path

Start from one JSON scope packet containing `parent`, exhaustive `children`, and a Charter with at least `id` and outcome:

```text
python <skill-dir>/scripts/run_ledger.py start --events <run-dir>/events.jsonl --repo <repo> --scope-file <scope.json>
```

`start` supplies runtime contract 3, default budgets, a stable scope event ID, and the repository HEAD. It rejects a nonempty stream; use `status` to resume.

The canonical Charter counters are `repair_generation_budget` (default `2`), `review_invocation_budget` (default `3`), and `review_invocations_required` (default `1`). They are independent ceilings/minimums and change only through caller-authorized scope evidence.

Ask for the current mechanical move whenever state changes or a run resumes:

```text
python <skill-dir>/scripts/run_ledger.py status --events <events.jsonl> --repo <repo>
```

The response reports `phase`, current and integration heads, implementation state, frontier, active lanes, blockers, `decision_required`, currently authorized intents, and one `next_action`. It derives mechanics only. Root judgment still selects scope, independence, acceptance, correction policy, findings, and external mutation.

Apply a UTF-8 JSON packet:

```text
python <skill-dir>/scripts/run_ledger.py apply --events <events.jsonl> --repo <repo> --packet-file <packet.json>
```

Supported packet kinds:

- `lane-ready`: `work_item`, `lane_id`, `actor_id`, and the helper's `create` and `preflight` evidence; records creation and preflight atomically.
- `worker-result`: `work_item` and `report`; records a handoff but never accepts it automatically.
- `events`: a nonempty `events` list for decisions and exceptional branches whose semantics remain explicit.

`apply` supplies stable event IDs, locks and fsyncs the stream, validates the complete prospective state, and is idempotent for the same semantic packet. A changed payload under the same identity rejects.

Generate a worker brief from current state:

```text
python <skill-dir>/scripts/run_ledger.py brief --events <events.jsonl> --repo <repo> --work-item <id> --mode <implementation|integration-correction|review-repair> --output <brief.md>
```

Finish only after terminal `complete` has been recorded:

```text
python <skill-dir>/scripts/run_ledger.py finish --events <events.jsonl> --repo <repo> --output <run-dir>/LEDGER.md
```

When no friction observations exist, `finish` appends the canonical `none_observed` synthesis. When observations exist, it requires deliberate synthesis. It then validates complete authority and renders the ledger. It never closes trackers, pushes, or fabricates Release.

**Adjudicate before synthesis.** Compare each observation and suggestion with the current canonical skill, helper behavior, and owning repository contract. Classify it as `generic-skill-gap`, `repo-contract-gap`, `run-specific`, or `already-satisfied`. Preserve every observation as historical evidence, but include only verified unresolved generic skill gaps in deduplicated improvement themes. Synthesis is adjudication, not transcription.

## Phases and decisions

| Phase | Root decision | Runtime derives |
| --- | --- | --- |
| Trace | outcome, graph, Charter, commitments | scope identity, budgets, starting HEAD |
| Select | readiness, independence, worker count | unfinished children and recorded blockers |
| Open | claim, actor, proof route | lane/preflight consistency and dispatch authority |
| Drain | accept/reject, stale-base route, correction route | landing authority, integration HEAD, invalidation |
| Review | route, finding admission, repair eligibility | immutable target, counters, successor requirements |
| Lock | external mutation approval | closeout plan, approved HEAD, missing read-backs |
| Release | terminal disposition | completeness, safe lanes, friction synthesis |

If `status.next_action` is surprising, inspect the state and canonical events. Do not force the suggested command.

## Branch packets

Use an `events` packet for checkpoint/resume, integration correction, formal review, Repair, Lock, and Release. These branches are explicit because they carry judgment or external evidence, not because the operator must calculate IDs or receipts.

Progressive evidence belongs at the gate where it becomes actionable:

- **Checkpoint:** idle actors, repository-backed nonempty current HEAD, safe lanes, continuation, frontier, blockers, tracker/remote state, and complete retained-or-released claim accounting.
- **Integration regression:** trusted RED, prior integration HEAD, route, owner, structured write-scope IDs, and required proof.
- **Integration correction:** matching regression, owner and lane actor, selected scope-ID subset, worker or correction commit, actual changed files, ancestry, clean successor HEAD, and bounded regression proof.
- **Review:** drained graph, loop-close proof, immutable target, `review-invocation` identity, route, mode, classified findings, decision, and residual risk.
- **Repair:** blocked snapshot, one complete eligible finding set, generation, owners, scopes, proof, successor HEAD, and completion evidence.
- **Lock:** approved HEAD, verified child packets, child-first mutation read-backs, parent closeout, applicable push/remote proof, and lane dispositions.

Runtime contract 3 uses `checkpoint` for resumable `partial` or `blocked`. After `resume`, authority stays closed until `reconcile` records Git, worktree, actor, tracker, and remote observations. `release` is terminal and accepts only `complete`.

`landed-awaiting-lock` is a derived, campaign-scoped execution state. It satisfies in-scope dependency readiness only while the accepted landing remains in current integration history with valid proof. It does not close an issue or alter the tracker dependency. Rollback, invalidation, or failed proof removes the overlay and reblocks dependents.

## Advanced and compatibility surface

`append-receipt --intent <intent> --event-id <stable-id> --stdin` remains the exact low-level authority surface. It validates the prospective event, appends once, and returns the requested and currently authorized intents. `committed: true` proves durable append only; action requires `requested_intent.allowed: true` in current state.

`validate-state`, `resume-status`, `closeout-plan`, `render`, `list`, `append`, and `append-batch` remain available for diagnosis, recovery, historical streams, and tests. New normal-path orchestration should prefer `start`, `status`, `apply`, `brief`, and `finish`.

The executable schema lives in `run_ledger.py`. Do not copy field-by-field event contracts into `SKILL.md` or edit generated ledger prose.
