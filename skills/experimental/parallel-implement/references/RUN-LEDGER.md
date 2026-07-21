# Campaign Runtime

`events.jsonl` is the sole campaign source of truth. `LEDGER.md` is generated. The root is the sole writer.

Normal-path commands require an absolute event path. `start` alone may create a missing stream; `status`, `apply`, `brief`, `prepare`, and `finish` require that exact stream to exist. A missing or relative path is an error, never an implicit empty campaign.

## Contents

- [Normal path](#normal-path)
- [Prepared terminal path](#prepared-terminal-path)
- [Phases and decisions](#phases-and-decisions)
- [Branch packets](#branch-packets)
- [Advanced and compatibility surface](#advanced-and-compatibility-surface)

## Normal path

Start from one JSON scope packet containing `parent`, exhaustive `children`, and a Charter with at least `id` and outcome:

```text
python <skill-dir>/scripts/run_ledger.py start --events <absolute-run-dir>/events.jsonl --repo <repo> --scope-file <scope.json>
```

`start` supplies runtime contract 3, default budgets, a stable scope event ID, the repository HEAD, and integration-checkout ownership. It rejects an existing stream; use `status` to resume.

The canonical Charter counters are `repair_generation_budget` (default `4`), `review_invocation_budget` (default `5`), and `review_invocations_required` (default `1`). The fifth review slot preserves one successor review for each possible Repair. They are ceilings/minimums and change only through caller-authorized scope evidence.

Ask for the current mechanical move whenever state changes or a run resumes:

```text
python <skill-dir>/scripts/run_ledger.py status --events <absolute-events.jsonl> --repo <repo>
```

The response reports `phase`, current and integration heads, implementation state, frontier, active lanes, the uninspected `result_queue`, current and peak authorized `width`, frontier reason, serial latch, blockers, `decision_required`, currently authorized intents, and one `next_action`. It derives mechanics only. Root judgment still selects scope, independence, acceptance, correction policy, findings, and external mutation. Drain the result queue before further dispatch.

Apply a UTF-8 JSON packet:

```text
python <skill-dir>/scripts/run_ledger.py apply --events <absolute-events.jsonl> --repo <repo> --packet-file <absolute-packet.json>
```

Supported packet kinds:

- `lane-ready`: `work_item`, `lane_id`, `actor_id`, the helper's complete `create` and `preflight` evidence, and one assignment containing Source Trace, dependencies, acceptance, scope, exclusions, claim read-back, proof seam and command file, stable roots, state matrix, liveness checkpoint, and report path; records creation and preflight atomically.
- `worker-result`: `work_item` and a compact `report` with `status`, `commit` when done, `changed_scope_summary`, `proof_outcome`, `proof_log_path`, structured slice proof, `skipped_checks`, `risks`, `report_path`, and `final_status`; records a queued handoff but never accepts it automatically.
- `events`: a nonempty `events` list for decisions and exceptional branches whose semantics remain explicit.

`apply` supplies stable event IDs, locks and fsyncs the stream, validates the complete prospective state, and is idempotent for the same semantic packet. A changed payload under the same identity rejects.

Record one selected frontier before Open. Width defaults to one. A cold two-item start and every parallel hold or widening packet must carry the root's explicit `substantial`, `semantic_independence`, `proof_isolated`, and `root_capacity` attestations. Widen only by one after recorded passing `wave-validation`, up to five:

```json
{
  "kind": "events",
  "events": [{
    "event": "frontier",
    "work_item": "<parent>",
    "data": {
      "selected": ["<child-1>", "<child-2>"],
      "width": 2,
      "reason": "parallel-independent",
      "cold_start": true,
      "substantial": true,
      "semantic_independence": true,
      "proof_isolated": true,
      "root_capacity": true
    }
  }]
}
```

An uninspected result at parallel width makes `status.next_action` request Downshift. Apply a width-one frontier with the reported `downshift-*` cause; this sets the serial latch. While latched, later serial frontiers use `serial-after-downshift`. A clean serial wave does not clear it. Only `reset-after-external-change` at width one with nonempty `release_evidence` clears the latch; a later parallel frontier may reopen at two. The helper validates these facts but never decides semantic independence or changes width without a root packet.

Generate a worker brief from current state:

```text
python <skill-dir>/scripts/run_ledger.py brief --events <absolute-events.jsonl> --repo <repo> --work-item <id> --mode <implementation|integration-correction|review-repair> --output <absolute-brief.md>
```

The generated brief is complete for one assignment: actor role and reuse boundary, reconciled lane and base, acceptance, expected scope, exclusions, highest meaningful public proof seam, file-backed proof command, and absolute report path. Give the actor this brief, not the parent conversation or exhaustive issue graph.

Record a return through a compact packet; keep detailed criterion evidence and command output in `report_path` and `proof_log_path`:

```json
{
  "kind": "worker-result",
  "work_item": "<id>",
  "report": {
    "status": "done",
    "commit": "<sha>",
    "changed_scope_summary": "<expected versus actual>",
    "proof_outcome": "<criterion summary>",
    "proof_log_path": "<absolute path>",
    "proof": {
      "level": "slice",
      "command_identity": "<proof command identity>",
      "exit_code": 0,
      "duration_seconds": 0.0,
      "counts": {"passed": 0, "failed": 0},
      "environment_identity": "<runtime and provenance>",
      "log_digest": "sha256:<digest>"
    },
    "skipped_checks": [],
    "risks": [],
    "report_path": "<absolute path>",
    "final_status": "clean"
  }
}
```

Record wave, candidate, correction, and Repair proof with the same object under `data.proof`, changing `level`. Successful proof requires exit code, duration, counts, environment, and digest. A nonzero exit additionally requires `failure_excerpt` capped at 2,000 characters. The summary remains in `validation`; the object supplies measurable evidence.

## Prepared terminal path

Do not inspect helper source or hand-author event IDs for Review, Repair, closeout, or Release. Prepare the currently applicable typed packet, fill only its `values`, then apply it:

```text
python <skill-dir>/scripts/run_ledger.py prepare --events <absolute-events.jsonl> --repo <repo> --step <review|repair|closeout|release> --output <absolute-packet.json>
python <skill-dir>/scripts/run_ledger.py apply --events <absolute-events.jsonl> --repo <repo> --packet-file <absolute-packet.json>
```

Each prepared packet binds the absolute stream path, event count, last event ID, and stream hash. Stale or cross-campaign application fails; idempotent replay of an already applied packet succeeds without duplicate events.

- `review` prefills the immutable candidate and budgets; supply invocation identity, mode, reason, route, complete findings, decision, and residual risk. A recorded `review-ready` event with current candidate proof is mandatory.
- `repair` first prepares one complete admitted plan; after the bounded repair lands and passes proof, prepare it again for successor HEAD, proof, and changed scope. The helper validates budgets and finding identity but never admits findings.
- `closeout` prefills the approved HEAD, expected child mutations, pending children, and verified-field contract. Apply any observed child subset first; unresolved children remain pending. Supply parent, tracker Lock, and applicable push read-backs only when every pending child in that packet is verified. The helper performs no provider mutation.
- `release` prefills proof, review, closeout, lane, integration-checkout, push, efficiency, approved-HEAD, and friction state; supply complete disposition, residual risk, and deliberate synthesis or `none_observed` evidence.

Fill only the generated packet's `values`. Representative complete shapes are:

```json
{
  "invocation_id": "review-1",
  "mode": "initial",
  "reason": "first proved integrated candidate",
  "route": "review",
  "findings": [],
  "decision": "pass",
  "residual_risk": "none"
}
```

```json
{
  "finding_ids": ["F1"],
  "assignments": [{
    "owner": "primary-1",
    "scope": ["scope-id"],
    "required_proof": ["public regression passes"]
  }]
}
```

For the second prepared Repair packet, replace `assignments` with `successor_head`, `changed_scope`, and structured `proof` at level `repair` using the proof fields above.

```json
{
  "child_readbacks": [{
    "work_item": "child-1",
    "state": "verified",
    "delivered": "implemented acceptance",
    "acceptance_evidence": "criterion -> proof",
    "proof": "slice, wave, and candidate proof passed",
    "review": "pass",
    "reviewed_head": "<approved SHA>",
    "residual_risk": "none",
    "intended_mutation": "close child",
    "posted_comment": "<provider comment identity>",
    "mutation_readback": "closed and claim absent"
  }],
  "parent_readback": {"state": "verified", "mutation_readback": "parent closed child-first"},
  "tracker_lock": {"readback": "tracker Lock verified"},
  "push": null
}
```

A partial closeout supplies only `child_readbacks` with observed states such as `posted`; prepare again after further provider work. A final packet supplies the complete shape above. When push is required, replace `null` with `{"verified_head": "<approved SHA>", "readback": "remote contains approved SHA"}`.

```json
{
  "friction_synthesis": {
    "observations": [],
    "deduplicated_themes": [],
    "none_observed": true
  },
  "disposition": "complete",
  "residual_risk": "none"
}
```

Finish only after terminal `complete` has been recorded:

```text
python <skill-dir>/scripts/run_ledger.py finish --events <absolute-events.jsonl> --repo <repo> --output <absolute-run-dir>/LEDGER.md
```

When no friction observations exist, `finish` appends the canonical `none_observed` synthesis. When observations exist, it requires deliberate synthesis. It validates complete authority, renders the ledger, and returns passive evidence for elapsed time, available token telemetry, actor contexts, peak width, proof count and duration, result-queue backpressure, rework, terminal packets, compatibility fallbacks, correctness, Downshift cause and release, Review and Repair generations, and measurement gaps. It never estimates unavailable tokens, closes trackers, pushes, or fabricates Release.

**Adjudicate before synthesis.** Compare each observation and suggestion with the current canonical skill, helper behavior, and owning repository contract. Classify it as `generic-skill-gap`, `repo-contract-gap`, `run-specific`, or `already-satisfied`. Preserve every observation as historical evidence, but include only verified unresolved generic skill gaps in deduplicated improvement themes. Synthesis is adjudication, not transcription.

## Phases and decisions

| Phase | Root decision | Runtime derives |
| --- | --- | --- |
| Trace | outcome, graph, Charter, commitments | scope identity, budgets, starting HEAD |
| Select | readiness, independence, substantial work, worker count, reason | width, cap, result backpressure, wave evidence, serial latch |
| Open | claim, actor, proof route | lane/preflight consistency and dispatch authority |
| Drain | accept/reject, stale-base route, correction route | landing authority, integration HEAD, invalidation |
| Review | route, finding admission, repair eligibility | immutable target, counters, successor requirements |
| Lock | external mutation approval | closeout plan, approved HEAD, missing read-backs |
| Release | terminal disposition | completeness, safe lanes, friction synthesis |

If `status.next_action` is surprising, inspect the state and canonical events. Do not force the suggested command.

## Branch packets

Use `prepare` for Review, Repair, closeout, and Release. Use an `events` packet only for Checkpoint/resume, integration correction, frontier or proof evidence, and exceptional recovery whose judgment remains explicit. These branches carry root judgment or external evidence; the operator does not calculate normal-path event IDs or receipts.

Progressive evidence belongs at the gate where it becomes actionable:

- **Checkpoint:** idle actors, repository-backed nonempty current HEAD, integration-checkout ownership and registration, safe lane snapshot, continuation, frontier, serial latch, blockers, exact result queue, proof state, open correction or Repair, tracker/remote state, and complete retained-or-released claim accounting.
- **Integration regression:** trusted RED, prior integration HEAD, route, owner, structured write-scope IDs, and required proof.
- **Integration correction:** matching regression, owner and lane actor, selected scope-ID subset, worker or correction commit, actual changed files, ancestry, clean successor HEAD, and bounded regression proof.
- **Review:** drained graph, loop-close proof, immutable target, `review-invocation` identity, route, mode, classified findings, decision, and residual risk.
- **Repair:** blocked snapshot, one complete eligible finding set, generation, owners, scopes, proof, successor HEAD, and completion evidence.
- **Lock:** approved HEAD, verified child packets, child-first mutation read-backs, parent closeout, applicable push/remote proof, and lane dispositions.

Runtime contract 3 uses `checkpoint` for resumable `partial` or `blocked`. After `resume`, authority stays closed until `reconcile` records Git, worktree, actor, claim, tracker, remote, and integration-checkout observations. `release` is terminal and accepts only `complete`.

`landed-awaiting-lock` is a derived, campaign-scoped execution state. It satisfies in-scope dependency readiness only while the accepted landing remains in current integration history with valid proof. It does not close an issue or alter the tracker dependency. Rollback, invalidation, or failed proof removes the overlay and reblocks dependents.

## Advanced and compatibility surface

`append-receipt --intent <intent> --event-id <stable-id> --stdin` remains the exact low-level recovery surface. It validates the prospective event, appends once, and returns the requested and currently authorized intents. `committed: true` proves durable append only; action requires `requested_intent.allowed: true` in current state. It may require a caller-supplied event ID because it is not the generated normal path.

`validate-state`, `resume-status`, `closeout-plan`, `render`, `list`, `append`, and `append-batch` remain available for diagnosis, recovery, historical streams, and tests. New normal-path orchestration should prefer `start`, `status`, `apply`, `brief`, `prepare`, and `finish`.

The executable schema lives in `run_ledger.py`. Do not copy field-by-field event contracts into `SKILL.md` or edit generated ledger prose.
