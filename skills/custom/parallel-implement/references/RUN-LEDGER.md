# Campaign State and Ledger

Use this before the first campaign event, on every resume, before an authority transition, and at closeout.

`events.jsonl` is the sole campaign source of truth. `LEDGER.md` is generated output. The root is the sole writer.

## Commands

Initialize once:

```text
python <skill-dir>/scripts/run_ledger.py init --events <run-dir>/events.jsonl
```

For canonical events, use a stable event ID and request one resulting intent receipt:

```text
python <skill-dir>/scripts/run_ledger.py append-receipt \
  --events <events.jsonl> \
  --repo <repo> \
  --intent <dispatch|land|review|repair|lock|push|complete> \
  --event-id <stable-id> \
  --stdin
```

The command locks the stream, validates its prior and prospective semantic state, appends once, fsyncs, re-derives state, and returns a machine-readable receipt. Retrying the same ID and semantic payload at the stream tail returns the stored receipt. After later events, the retry preserves the append position but recomputes authority from the full stream and returns `receipt_fresh: false`; a different payload rejects. `committed: true` records the event only. Authority exists only when the current `requested_intent.allowed` is true.

Keep `append` and `append-batch` for legacy or atomic evidence ingestion. They preserve structural append behavior and do not grant authority:

```text
python <skill-dir>/scripts/run_ledger.py append --events <events> --stdin
python <skill-dir>/scripts/run_ledger.py append-batch --events <events> --from-file <packet.json>
```

`validate` checks stream structure. `validate-state --intent <intent>` derives semantic state and authority. Use `status` during a run, `resume-status` after interruption, and `closeout-plan` after accepted review.

```text
python <skill-dir>/scripts/run_ledger.py validate-state --events <events> --intent <intent> --repo <repo>
```

Render after material state changes and at Release:

```text
python <skill-dir>/scripts/run_ledger.py render --events <events> --repo <repo> --output <run-dir>/LEDGER.md
```

## Canonical Charter

Set `runtime_contract: 2` and record:

- `repair_generation_budget`: nonnegative automatic Repair ceiling, default `2`;
- `review_invocation_budget`: positive formal-review ceiling, default Repair budget plus one;
- `review_invocations_required`: positive completed-review minimum, default `1`.

Legacy `repair_budget` remains an alias when it agrees with the canonical value. A budget-changing `scope-change` carries the exact prior values plus caller source and reason. Counters never authorize their own increase.

## Review State

Append `review-invocation` before the formal call. Use its event ID as the invocation identity, its `integration_sha` as the immutable target, and `data.mode` as `initial`, `remediation`, or `assurance`. The resulting `review-decision.data.review_invocation_id` must match.

Historical `review-target` events remain valid implicit invocations. New flows do not emit both event forms.

- Initial reviews the first integrated candidate.
- Remediation requires a proved Repair generation and successor SHA.
- Assurance requires an accepted immutable target and consumes a new top-level review invocation.
- Incomplete may retry the same target and mode when budget remains.

Every invocation consumes review budget. Every decision except `incomplete` counts toward required completed reviews. Internal reviewer replacement and challenge rounds do not affect campaign counters. Repair may start only when one generation and one successor review invocation remain.

## Progressive Evidence

Record evidence when its gate becomes actionable:

- **Scope:** Charter, parent, Source Trace, fixed point, exhaustive children, dependencies, dispositions, closeout rule, budgets, and push requirement.
- **Dispatch:** frontier, readiness, Tripwire, Downshift, provider, preflight, temp roots, proof budget, claim read-back, permission route, and liveness checkpoint.
- **Integration:** worker SHA, landing executor and mode, integration SHA, proof, stale-base or conflict state, and relationship fingerprint.
- **Review:** drained graph, final validation, immutable target, invocation ID, route, mode, classified findings, decision, and accepted residual risk.
- **Repair:** blocked snapshot, generation, complete blocking IDs, owners, write scopes, proof, integrated Repair HEAD, and completion evidence.
- **Lock:** approved HEAD, child packets, child-first mutation read-backs, parent closeout, push, remote verification, lane disposition, and friction synthesis.

The executable event fields live in `run_ledger.py`; do not duplicate that interface in handwritten ledger prose.

## Friction

Record observations with `kind: observation`, `surface`, `source`, `evidence`, `impact`, and `suggestion`. Record exactly one synthesis with all observation event IDs, deduplicated themes, and `none_observed`.

The synthesis is mandatory only for `runtime_contract: 2` `complete` closeout. Its content never changes implementation or review authority. Because friction is the only allowed post-release event, a missing synthesis can be appended after an otherwise recorded release without replaying mutations.

## Resume and Closeout

After `resume`, dispatch, landing, Review, Lock, and push stay closed until `reconcile` records Git, worktree, agent, and tracker evidence.

`resume-status` classifies lanes as active, clean-uncommitted, committed-unlanded, landed, dirty-preserved, or residual. Reconcile those classifications against checkout, Git registration, actor/process state, tracker claim, and remote state.

Update each `child-closeout` through `draft`, `review-final`, `posted`, and `verified`. Post only rendered packets, refetch before uncertain mutation replay, and run `closeout-plan` after each external change. Release is complete only when `validate-state --intent complete` passes.

The renderer owns tracker-comment and ledger prose; handwritten Markdown never overrides the event stream.
