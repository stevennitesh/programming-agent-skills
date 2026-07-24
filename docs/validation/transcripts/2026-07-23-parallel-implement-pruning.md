# Parallel Implement Deploy Pruning Pass

## Run Identity

- Authorized unit: Deploy Pruning Pass only
- Campaign epoch: `2026-07-23`
- Delivery mode: bare
- Starting Git `HEAD`:
  `a86bebc72c19f54a3b3b57f3c99f13b3d401c9a7`
- Campaign shape: `pruning-only`
- Runtime decision: `current != B0 = C1`
- Prompt 4 decision: `accepted`
- Accepted behavior-complete B0/C1 tree SHA-256:
  `036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc`
- Protected behavior set: B0-01 through B0-12 and protected runtime-contract-3
  ledger and Windows lane compatibility from the active synthesis
- Registered proof: Prompt 4 recovery, concurrency, whole-package viability,
  candidate structure, and 46 candidate-path helper tests

Fresh read-back matched the exact eight-file Prompt 3 inventory, all per-file
hashes, the manifest candidate hash, the active synthesis, and the Prompt 4
acceptance record. Git `HEAD` matched the campaign fixed point. No drift
blocked pruning.

## Audit Method

Writing Great Skills ran in Author mode. Each instruction-bearing passage or
machine behavior unit below appears in exactly one row. For every possible
cut, the audit asked: “If I cut this, what behavior may change?” A cut was
eligible only if the answer admitted no protected regression and it lowered
one named load: always-loaded description, common-path instructions,
duplicated semantic ownership, branch load, or unused package surface.

`keep` means the passage has one distinct behavioral or machine-contract job.
No passage qualified for `collapse`, `disclose`, or `delete`.

## Cut Ledger

### `SKILL.md`

| Passage | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Frontmatter description | `keep` | Explicit parent-graph invocation or adjacent exclusion may misroute; it is the required always-loaded predicate, not duplicated body procedure. |
| Phase spine and outcome statement | `keep` | The irreversible order or outcome-over-parallelism priority may weaken; common-path load is earned. |
| Admission: root, explicit parent, exhaustive non-empty graph | `keep` | B0-01 invocation boundary may widen. |
| Admission: delegated, single-item, graph-defect, investigation, review exclusions | `keep` | Adjacent owners or pre-mutation blocker may be skipped. |
| Admission: root authority and child no-widening rule | `keep` | Root/child authority may drift. |
| Trace: engineering/tracker/domain sources and bootstrap stop | `keep` | Governing sources or missing-setup Return may be bypassed. |
| Trace: frozen graph, Charter, Source Trace, matrix, and defect Return | `keep` | B0-02 required inputs or owner boundary may be reconstructed incorrectly. |
| Trace: canonical stream, authority, and full reconciliation | `keep` | Prompt 4-proved recovery behavior may regress, including premature tracker closure. |
| Select: reconciled readiness and reversible overlay | `keep` | B0-04/B0-10 readiness or invalidation may become unsafe. |
| Select: five-dimension concurrency qualification | `keep` | Semantic, write, proof-resource, or ordering coupling may be missed; protected contract despite no wording-efficacy credit. |
| Select: sensitive tracer and partial-state proof | `keep` | Non-intuitive safety gate may disappear. |
| Select: no-executable blocker Return | `keep` | Scope may widen instead of returning exact blockers. |
| Open: claim read-back and isolated ready packet | `keep` | B0-06 claim, containment, provenance, or dispatch gate may weaken. |
| Open: worker brief, authority, TDD, and diagnosis routes | `keep` | Typed lane ownership or callee triggers/Returns may drift. |
| Open: exceptional integrator route | `keep` | Branch-only integration authority would lack its triggered pointer; already disclosed. |
| Drain: typed worker acceptance and actor continuation | `keep` | Incomplete returns or stale actors may be accepted. |
| Drain: serial landing, recombined proof, and final state matrix | `keep` | B0-09 integration order or current-HEAD proof may regress. |
| Drain: conflict and trusted-regression correction routes | `keep` | Preserved conflict or bounded correction authority may be lost. |
| Drain: repeat-to-drained criterion | `keep` | The graph may stop early. |
| Review: immutable candidate, idle/clean/drained gates, review route | `keep` | Review may target the wrong snapshot or owner. |
| Review: no-mutation, bounded Repair, decision packet, successor review | `keep` | B0-08 review independence or re-review may regress. |
| Lock: reviewed-current-HEAD gate and ordered closeout | `keep` | B0-12 irreversible order, read-back, remote proof, or lane safety may fail. |
| Lock: exact terminal completion predicate | `keep` | Premature completion may occur. |
| Lock: recovery-complete nonterminal Return | `keep` | B0-11 accepted/unrelated state, actor, claim, overlay, or recovery accounting may be lost. |

### `agents/openai.yaml`

| Passage | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Display name and short description | `keep` | User-facing identity would degrade; machine metadata surface is not common-path body duplication. |
| Default prompt | `keep` | Explicit invocation would lose its root, isolation, serial landing, review, and Lock framing. |
| `allow_implicit_invocation: false` | `keep` | The explicit-only authority boundary would change. |

### `references/CODEX-WORKTREE-LAUNCH.md`

| Passage | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Fresh-context versus checkout isolation premise | `keep` | Workers may treat context isolation as filesystem isolation. |
| Open command contract | `keep` | The supported atomic open path becomes undiscoverable. |
| Root, path-budget, detached/branch selection | `keep` | Windows containment or branch authority may change. |
| Create/preflight ready-state and preserved-failure behavior | `keep` | Dispatch may occur without verified ready evidence. |
| Runtime-managed provider branch | `keep` | Provider identity and cleanup ownership may collide. |
| Startup argv and no-shell contract | `keep` | Command provenance or shell safety may weaken. |
| Python provenance schema and lane-local import rule | `keep` | Cross-worktree imports may go undetected. |
| No-package provenance exception | `keep` | A legitimate branch would have no explicit residual-risk route. |
| No-proof exception | `keep` | A skipped check may be misreported as a pass. |
| Ready packet fields | `keep` | Worker dispatch may omit containment, trust, proof, or temp-root evidence. |
| Dispatch application and fresh child | `keep` | The ledger/brief/lane sequence may split. |
| Missed-liveness recovery | `keep` | Duplicate writers or lost dirty work may result. |
| Diagnostic create/preflight retry | `keep` | Retry may occur without a changed condition. |
| Resume reconciliation | `keep` | Missing lane state may be treated as done. |
| Cleanup command and preconditions | `keep` | Destructive cleanup may target unsafe state. |
| Extended-path fallback semantics | `keep` | Windows residual directories may be misclassified. |
| Safe terminal states | `keep` | Completion may accept dirty or unknown lanes. |
| Lost-registration purge boundary | `keep` | Unverifiable residuals may be deleted without explicit authority. |
| Explicitly excluded destructive/global actions | `keep` | Non-intuitive safety boundaries may be crossed. |

### `references/INTEGRATOR-BRIEF.md`

| Passage | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Shallow/hot/late modes and root default | `keep` | The exceptional integration branch or default root owner may blur. |
| Assignment packet fields | `keep` | Integrator input, lane, review, or Repair authority may be incomplete. |
| Source/ledger/report read set | `keep` | Integration may act without governing evidence. |
| Integration-only authority Return | `keep` | Dispatch, review, tracker, push, or closeout may escape root ownership. |
| Dedicated-worktree blocker | `keep` | Integration may run without isolation. |
| Ready reconciliation gate | `keep` | Hot or later landing may begin from unproved state. |
| Five-step serial integration contract | `keep` | Scope inspection, one-at-a-time landing, proof, or typed report may disappear. |
| Conflict Return | `keep` | Partial Git state may be overwritten or authority retained. |
| Routed broad-proof budget | `keep` | Integration may overrun or skip wave/final proof ownership. |
| Trusted-regression correction Return | `keep` | Integrator may self-authorize fixes. |
| Review-ready handoff | `keep` | Root may receive an unclean, unproved, or unpinned target. |
| Repair bound | `keep` | Unadmitted findings or Charter changes may be edited. |

### `references/RUN-LEDGER.md`

| Passage | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Event-stream authority and sole writer | `keep` | Generated state may become authoritative or gain multiple writers. |
| `start` command and scope packet | `keep` | Canonical campaign initialization becomes ambiguous. |
| Start idempotency, contract version, budgets, and HEAD | `keep` | Resume may overwrite a nonempty stream or lose compatibility. |
| Independent budget counters | `keep` | Repair and review ceilings/minimums may be conflated. |
| `status` command and mechanical-view limit | `keep` | Root judgment may be delegated to the helper. |
| `apply` command and packet kinds | `keep` | Supported write surfaces or semantic ownership may blur. |
| Apply locking, fsync, validation, and idempotency | `keep` | Event durability or replay safety may regress. |
| `brief` command | `keep` | The worker packet would lack its supported generator. |
| `finish` command and terminal gate | `keep` | Rendering may fabricate or precede completion. |
| Friction compatibility field and authority limit | `keep` | Protected runtime-contract-3 streams may break or treat friction as outcome. |
| Phase/root-decision/runtime-derivation table | `keep` | Root versus reducer ownership may become scattered; it is the single co-located map. |
| Surprising-next-action read-back | `keep` | Helper suggestion may override canonical events. |
| Explicit branch-packet rule | `keep` | Judgment-bearing events may be forced through inferred normal-path commands. |
| Progressive evidence gates | `keep` | Recovery, correction, review, Repair, or Lock evidence may arrive too late. |
| Checkpoint/resume/reconcile authority | `keep` | Progress may resume before full state reconciliation. |
| `landed-awaiting-lock` semantics | `keep` | Tracker closure or dependency readiness may be corrupted. |
| Low-level receipt authority | `keep` | Protected compatibility clients may lose exact intent/read-back semantics. |
| Diagnostic/historical commands | `keep` | Recovery and historical streams would lose supported tools; already disclosed as an advanced branch. |
| Executable-schema pointer and no-copy rule | `keep` | Field contracts may duplicate and drift into prose. |

### `references/WORKER-BRIEF.md`

| Passage | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Generator plus ticket-owned additions | `keep` | Ledger inference may substitute for owner-supplied scope or proof. |
| Common assignment field set | `keep` | A bounded lane may lack identity, state, scope, proof, liveness, or transport. |
| Worktree reconciliation and containment | `keep` | A worker may edit the wrong checkout. |
| One-worker authority and callee routes | `keep` | Fan-out, integration, tracker, push, or scope widening may occur. |
| State-matrix completion and omitted-branch Return | `keep` | Acceptance may silently narrow or widen. |
| Focused/broad proof and commitment boundary | `keep` | Proof scope or product authority may drift. |
| Implementation mode | `keep` | Ordinary lane completion and out-of-scope discovery handling may blur. |
| Integration-correction packet and proof | `keep` | A correction may start from the wrong HEAD or exceed authorized IDs. |
| Original-worker continuation condition | `keep` | A stale actor may resume without root reconciliation. |
| Review-repair packet | `keep` | Unadmitted findings may authorize work. |
| Return schema | `keep` | Root acceptance would lose typed evidence fields. |
| Done/blocker/needs-feedback criteria | `keep` | Incomplete or dirty work may claim completion. |

### `scripts/lane_worktree.py`

| Machine behavior unit | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Process/Git trust and repository primitives (`run` through `git_with_trust`) | `keep` | Command failure, trust recovery, or exact repository identity may break. |
| Naming, containment, registration, and path-budget primitives (`slug` through `path_budget`) | `keep` | Lane collision, escape, or Windows path overflow may go undetected. |
| Structured result and blocker emitters (`emit`, `blocked`) | `keep` | Typed failure/read-back contract may change. |
| Lane creation (`create`) | `keep` | Containment, exact base, registration, or preserved-failure behavior may regress. |
| Reversible probes and Git-path resolution | `keep` | Checkout/index/object capability or linked-worktree paths may be misread. |
| Startup proof and Python provenance (`proof_command`, `python_provenance`) | `keep` | Shell-free execution or lane-local imports may be lost. |
| Full lane preflight (`preflight`) | `keep` | Dirty/base/branch/trust/temp/proof gates may be skipped. |
| Atomic helper composition and `open_lane` | `keep` | Create/preflight evidence may split or leak unsafe cleanup. |
| Verified cleanup and extended-path fallback (`cleanup`, `extended_path`) | `keep` | Registered, dirty, wrong-HEAD, or outside-root deletion may occur. |
| Explicit residual purge (`purge_residual`) | `keep` | Lost-registration recovery would have no contained authorized route. |
| CLI parser and entry point | `keep` | Protected command/argument compatibility may break. |

### `scripts/run_ledger.py`

| Machine behavior unit | Classification | If cut, behavior at risk / load judgment |
| --- | --- | --- |
| Stream locking, event I/O, validation, normalization, and append primitives | `keep` | Sole-writer, schema, durability, or replay integrity may fail. |
| Stable IDs, semantic packets, and receipt construction | `keep` | Idempotency or requested/current intent read-back may change. |
| Git observation primitives | `keep` | HEAD, cleanliness, or ancestry gates may use stale assertions. |
| State reducer and invariant checks (`derive_state`) | `keep` | Any B0 phase, overlay, review, Repair, claim, lane, or completion state may be misderived. |
| Intent validation and next actions | `keep` | Unauthorized progression may be suggested or accepted. |
| Validation/status and facade projections | `keep` | Mechanical state or normal-path operator view may drift. |
| Start/apply/brief/finish facade commands | `keep` | Protected runtime-contract-3 normal path and typed worker/finish contracts may break. |
| Closeout planning and Markdown rendering | `keep` | Ordered mutations or durable generated evidence may be wrong. |
| Diagnostic/list/init and CLI parser/entry point | `keep` | Compatibility, recovery, tests, or command surface may break. |

## Rejected Cut Groups

No cut reached candidate status. Five apparent opportunities were examined and
rejected during classification:

| Apparent cut | Decision | Reason |
| --- | --- | --- |
| Collapse description exclusions into Admission | Rejected before mutation | Description is the explicit-only routing predicate; Admission governs execution after load. Removing either changes invocation or runtime behavior. |
| Remove the opening outcome because Lock defines completion | Rejected before mutation | The opening steers the common path away from treating parallel activity as the result; Lock defines the terminal predicate. |
| Deduplicate root/worker/integrator authority | Rejected before mutation | Each audience receives a different packet and must carry its own prohibitions and Return. There is no shared loaded context. |
| Collapse the phase spine into detailed headings | Rejected before mutation | The spine encodes irreversible order while headings own gate detail; neither repeats the other's semantic job. |
| Delete advanced ledger/worktree compatibility branches | Rejected before mutation | They are protected machine/recovery surfaces and are already progressively disclosed outside `SKILL.md`. |

Because no material cut existed, the accepted C1 stayed byte-identical. The
protocol therefore forbade a pre-prune fixture and behavioral equivalence
wave. There were no ambiguous or regressing cut groups to revert.

## Load Delta

| Named load | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Always-loaded description | 304 characters | 304 characters | 0 |
| Common-path `SKILL.md` | 7,689 bytes | 7,689 bytes | 0 |
| Disclosed branch reference | 18,915 bytes | 18,915 bytes | 0 |
| Unused package surface | 0 files | 0 files | 0 |
| Complete candidate corpus | 8 files / 162,792 bytes | 8 files / 162,792 bytes | 0 |

The zero delta is intentional: word count was diagnostic, and no lower-load
expression preserved the registered behavior and protected compatibility.

## Focused Proof

The Prompt 4 candidate fixture was rerun before mutation and passed:

```text
tree_sha256=036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
structural_invocation_context_return_completion_relationship=pass
protected_byte_parity=pass
affected_markdown_gate=pass
```

It also read back all eight per-file hashes. After recording this decision,
the final focused proof reran the same exact-candidate structural fixture,
skill validation, final tree hash, and both diff checks. No behavioral evidence
was reused as equivalence evidence because no bytes changed; Prompt 4 remains
exact-reusable only for its recorded behavior claims.

Residual gaps:

- no live external parent graph, tracker connector partial failure, remote
  push, or irreversible closeout ran;
- behavioral evidence remains scoped to Prompt 4's exact model, packets,
  runtime, sample count, and rubrics; and
- canonical promotion, relationship publication, managed installation, and
  installed parity remain for Prompt 5.

## Decision And Shared Run Contract Return

```text
Authorized unit completed: Deploy Pruning Pass
Decision: complete; pruning-not-needed
Campaign shape: pruning-only
Runtime decision: current != B0 = C1; final C1 tree SHA-256 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
Artifacts changed: skills/experimental/manifest.json exact parallel-implement entry; docs/synthesis/skills/parallel-implement.md; docs/validation/transcripts/2026-07-23-parallel-implement-pruning.md
Evidence used or reused: exact Prompt 4 acceptance/hash/protected-set/proof read-back; complete eight-file cut audit; focused candidate structural/hash proof; skill validation; both diff checks
Residual gaps: live external connector/graph/remote/irreversible closeout; Prompt 4 scope limits; later canonical and installed parity
Recommended next unit: Deploy Prompt 5
Git HEAD: a86bebc72c19f54a3b3b57f3c99f13b3d401c9a7 -> a86bebc72c19f54a3b3b57f3c99f13b3d401c9a7
Git delivery: pending
Exact stop reason: no material behavior-preserving cut lowered a named load; C1 stayed byte-identical and the Pruning Pass stops before Prompt 5
```
