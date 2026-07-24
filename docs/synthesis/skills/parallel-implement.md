# Parallel Implement Synthesis

## Decision

Status: `promoted-installed` in Deploy Campaign epoch `2026-07-23`.

Campaign shape: `pruning-only`.

Runtime decision:

```text
current != B0 = C1
C1 exact delta: none
```

`B0`, `C1`, and the canonical package at
`skills/custom/parallel-implement` are the same behavior-complete corpus at
tree SHA-256
`036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc`.
Prompt 4 accepted those exact bytes without repair; the Pruning Pass retained
them byte-identically.

Parallel Implement delivers one explicitly requested, root-owned,
parent-backed Ready-for-agent ticket graph through qualified serial or
concurrent isolated lanes, independent review, verified integration, and
child-first then parent-last closeout. It owns runtime width after admission;
parallel activity is optional and never the outcome.

This synthesis supersedes the earlier efficiency proposal as a normative
design. That proposal remains decision-changing history only: warm-primary
reuse, compact receipts, adaptive width, result queues, a prepared terminal
facade, and passive efficiency results are not admitted into `B0` or `C1`.

## Viability Floor

### Invocation and exclusions

Admit only an explicit top-level request to deliver one parent and its
exhaustive associated non-empty Ready-for-agent graph. The parent is the
delivery boundary, not direct implementation scope. A delegated invocation
returns a routing blocker before mutation.

Exclude:

- one selected item, which belongs to `$implement`;
- raw, incomplete, ambiguous, unsettled, or not-Ready-for-agent work;
- graph creation, repair, slicing, or publication, which belongs to
  `$to-tickets`;
- generic parallel investigation;
- review-only work;
- invocation merely because concurrency is available; and
- any worker or child-integrator attempt to invoke or widen the campaign.

### Authority and relationships

The root alone admits the graph, reconciles durable state, qualifies
concurrency, claims work, dispatches, accepts returns, lands commits, chooses
conflict and correction routes, invokes formal review, admits findings,
integrates Repair, mutates the tracker, accepts residual risk, closes items,
pushes when authorized, and declares completion.

A lane worker is a direct fresh-context child assigned one bounded item in one
isolated worktree. It implements and proves only that assignment, returns one
typed packet, and owns no fan-out, integration, formal review, tracker
mutation, push, or campaign completion. A child integrator is permitted only
for a genuinely bounded independent integration lane; it has the same
prohibitions and returns landing and review authority to the root.

Parallel Implement invokes:

| Callee | Observable trigger | Authority and Return |
| --- | --- | --- |
| `$tdd` | A lane has red-testable new behavior or a fully known red-capable bug | The lane retains its assignment and consumes the proved implementation return. |
| `$diagnosing-bugs` | A lane bug lacks settled expected behavior, exact symptom, cause, or trusted reproduction | Diagnosis or authorized fix returns to the same bounded lane. |
| `$review` | The drained proved current candidate needs ordinary formal review | Review returns a fixed-snapshot Spec and Standards decision; the root retains Repair and Lock. |
| `$convergent-pr-review` | The drained proved target is a local PR or bounded high-risk diff | Review returns its terminal release decision; the root retains Repair, integration, tracker, and Lock. |
| `$resolving-merge-conflicts` | Serial landing enters a preserved conflict or partial Git operation | The resolver returns exact verified Git state and the authorized next boundary. |
| `$repo-bootstrap` | Required repository setup is missing or incompatible | Recommend and stop with the missing setup packet. |
| `$to-tickets` | The parent graph is incomplete, ambiguous, uneconomically sliced, or not ready | Return one exhaustive repair packet and stop; this skill does not repair the graph. |

### Safe failure and completion

On failure, preserve accepted and unrelated state; halt affected progression;
quiesce or account for actors; release ended claims; invalidate an unsafe
`landed-awaiting-lock` overlay; leave incomplete items open; and return the
blocker, exact retained state, and safest recovery or resume action.

Complete only when the exhaustive graph is drained; every accepted change is
in the reviewed current integration `HEAD`; required final proof and
independent review pass; every child is closed with mutation read-back before
the parent; all claims are released; every lane is removed or explicitly
preserved safely; applicable authorized push evidence is read back; and the
canonical campaign state admits terminal `complete`. A checkpoint is
nonterminal.

## Source-First Checkpoint

The Prompt 1 gate froze this block before current-runtime comparison:

```text
checkpoint:
  sha256: b008e3183714ab70151fb298ec7d3e8413d64d87bae8a119d5916a7183df2789
  decision: ready-for-prompt-2
  campaign_shape: pruning-only
  identity: current != B0 = C1
  c1_delta: none
  b0_units:
    01 admission
    02 source/campaign trace
    03 canonical durable recovery ledger/reconciliation
    04 dependency-ready set including landed-awaiting-lock
    05 concurrency gate over semantic/write/proof/resource/order isolation
    06 claim plus isolated fresh-context lane
    07 bounded child delivery and typed Return
    08 fixed-point Spec plus Standards acceptance and repair/re-review
    09 root serial integration, conflict routing, and recombined proof
    10 reversible dependency overlay
    11 recovery-complete failure Return
    12 reviewed-current-HEAD Lock and child-first/parent-last closeout
```

The fingerprint is Prompt 1's root-verified content identity. Prompt 2
preserves it and does not claim to reconstruct or re-hash the unavailable
Prompt 1 packet bytes.

### Exact source identities

Local intent and independent owners, SHA-256 prefixes:

| Source | Identity | Authority or limit |
| --- | --- | --- |
| `CONTEXT.md` | `ea6cb7894` | Local skill-pack ownership and lifecycle language. |
| `docs/agents/engineering-contract.md` | `c3d52491` | Charter, proof, worker, review, recovery, and Lock contracts. |
| `docs/agents/issue-tracker.md` | `d79c8dbd` | Ready graph, claim, `landed-awaiting-lock`, closeout, and mutation read-back. |
| `skills/custom/skill-router/SKILL.md` | `2bbf8e9c` | Explicit parent-delivery route and adjacent exclusions. |
| `skills/custom/to-tickets/SKILL.md` | `8b51672f` | Graph creation, readiness, execution profile, and recommendation boundary. |
| `skills/custom/triage/SKILL.md` | `3a1ce646` | Ready-item production and later-delivery boundary. |

Upstream packages:

| Source | Exact revision and qualifying identities | Claim limit |
| --- | --- | --- |
| Matt Pocock Skills | `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; clean, non-shallow, 314 commits, last commit 2026-07-21; implement `SKILL.md` `30cd7bc1`, metadata `8494f836`, docs `09886c4a` | Serial implementation only; no parallel implementer proof. |
| Superpowers | `d884ae04edebef577e82ff7c4e143debd0bbec99`; clean, non-shallow, 628 commits, last commit 2026-07-02; SDD `41ab239a`, implementer `49018b28`, reviewer `2eb9d543`, review package `0c0629f6`, workspace `9430befa`, task brief `5380283f`, parallel agents `f0df13f5`, executing plans `bbd8d28b`, worktrees `e2c3ec14` | Serial subagent-driven development, file handoff, status/review, worktree isolation, and qualified parallel investigation. It does not prove parallel implementation. |
| Ponytail | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; clean, non-shallow, 206 commits, last commit 2026-07-15 | No plausible equivalent for this skill. |

Research identities:

| Packet | SHA-256 prefix | Disposition |
| --- | --- | --- |
| Upper-bound engineering language | `dab0407c` | Source vocabulary and limitations only. |
| `UBL-01` | `16e99712` | Research support; no steering-effect proof. |
| `UBL-24` | `8ac08c71` | Research support; no steering-effect proof. |
| Matt historical change record | `d251b283` | Historical provenance only. |

No Research, Prototype, or Behavior Decision Interlude was admitted. Research
establishes source meaning; it does not establish local behavioral efficacy.

## Semantic-Unit Ledger

`Protected` means independently required, not merely present in the current
runtime. `Current disposition` is discovery after the checkpoint and never
selects the baseline.

| Unit | Settled intended-contract obligation | Source mechanic or required compatibility | Owner and basis | Current, research, Prototype, protected, and C1 dispositions | Destination and proof |
| --- | --- | --- | --- | --- | --- |
| `B0-01` | Admit only explicit root-owned delivery of one parent-backed ready graph; reject delegated and adjacent invocations before mutation. | Local router, To Tickets, tracker, and root-only authority; upstream offers only serial execution corroboration. | Root; independently required invocation and authority contract. | Current: preserve root/delegated gate but sharpen exclusions. Research: source limit. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md` description and Admission. Positive and adjacent-negative invocation cases plus delegated blocker read-back. |
| `B0-02` | Freeze the parent outcome, exhaustive graph, Charter, Source Trace, fixed point, acceptance, proof, non-goals, review route, and closeout rule; reconcile them on resume. | Engineering Source Trace/Charter; Superpowers plan/task handoff; current scope packet compatibility. | Root; source-derived mechanics plus required local packet compatibility. | Current: simplify while preserving exhaustive trace. Research: corroborated. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md` Trace and ledger start/status surfaces. Structural packet checks and start/resume scenarios. |
| `B0-03` | Use one canonical durable event stream; after interruption or interaction, reconcile Git, worktrees, actors, claims, tracker, remote, and derived state before progression. | Engineering refresh/recovery discipline; current runtime-contract-3 helper schema, CLI, receipts, event authority, idempotency, checkpoint/resume. | Root writes; reducer validates mechanical state. Required compatibility and non-intuitive recovery safety. | Current: preserve and simplify operator wording. Research: no direct efficacy proof. Prototype: N/A. Protected: helper contract yes. C1: none. | `RUN-LEDGER.md`, `run_ledger.py`, and concise `SKILL.md` pointer. Deterministic helper tests plus D0/B0 steering comparison for reconciliation wording. |
| `B0-04` | Select only the reconciled dependency-ready set; a valid same-campaign landing may satisfy readiness while still open. | Tracker contract and current `landed-awaiting-lock` derivation. | Root decides semantic readiness; reducer projects facts. Independently required tracker relationship. | Current: preserve. Research: N/A. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md` Select and ledger projection. Exhaustive graph/frontier matrix including serial, empty, newly linked, resumed, and invalidated cases. |
| `B0-05` | Qualify concurrency only across semantic ownership, expected writes, proof seams/resources, and ordering/tripwires; otherwise dispatch serially. | Superpowers qualified parallel-investigation condition transfers only as counterpressure; local To Tickets execution profile and safety contracts settle implementation use. | Root; source-derived condition plus local intent. Efficacy is unproved. | Current: cut arbitrary `up to three`, small/substantial savings calculus, root bandwidth heuristic, and Downshift vocabulary unless independently needed by exact B0. Research: condition only. Prototype: N/A. Protected: uncertainty serializes. C1: none. | `SKILL.md` readiness/concurrency gate. Serial/concurrent qualification matrix and D0/B0 comparison; no speed claim. |
| `B0-06` | Claim each selected item with read-back, then open one isolated fresh-context lane from an exact base with containment, provenance, startup, and cleanup evidence. | Tracker claim contract; Superpowers SDD fresh implementer and worktree isolation; current Windows-safe lane helper compatibility. | Root claims/dispatches; worker owns only its lane; helper owns mechanical preflight. | Current: preserve helper schema, Windows paths, provenance, containment, and cleanup. Research: corroborated mechanics. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md`, `CODEX-WORKTREE-LAUNCH.md`, `lane_worktree.py`. Claim/preflight read-back and lifecycle matrix. |
| `B0-07` | Give one bounded complete child brief; accept only a typed return that accounts for scope, acceptance, proof, commit/state, skips, risk, and next need. | Superpowers file-backed task brief/status handoff; current worker and integrator packet compatibility. | Root authors/accepts assignment; worker returns evidence without semantic acceptance. | Current: preserve modes and schema where caller-compatible; remove efficiency rationale. Research: corroborated mechanics. Prototype: N/A. Protected: worker prohibitions and typed failure. C1: none. | `WORKER-BRIEF.md`, `INTEGRATOR-BRIEF.md`, ledger brief/receipt surfaces. Packet fixtures and child-return scenarios. |
| `B0-08` | Pin one current candidate; obtain separate fixed-point Spec and Standards judgment; admit only bounded findings under Repair and successor-review budgets; review every successor. | Engineering fixed point, Repair generation, and Lock; Superpowers implementer/reviewer separation and review package; review-skill contracts. | Independent reviewer judges; root admits findings and owns Repair. | Current: preserve Repair budgets, required review identities, and no self-review. Research: corroborated. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md` Review, ledger events, and review relationship packets. Drained/wrong-HEAD/budget/decision-required matrices. |
| `B0-09` | Root accepts and lands one child result at a time, routes preserved conflicts, and runs recombined affected proof after landing and final proof before review. | Superpowers serial SDD and handoffs; engineering proof seams/state matrix; current integration-correction and conflict compatibility. | Root integrates; optional integrator is bounded and returns authority; conflict resolver owns only reconciliation. | Current: preserve serial landing, trusted RED, structured correction, and current-HEAD proof; simplify wave/queue optimization language. Research: corroborated serial mechanics. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md`, briefs, ledger, relationship map. Partial failure, concurrent returns/serial landing, conflict, correction, and recombined-proof scenarios. |
| `B0-10` | Treat `landed-awaiting-lock` as a reversible same-campaign dependency overlay, never tracker closure; rollback, invalidation, or failed proof reblocks dependents. | Tracker independent-owner contract and current reducer compatibility. | Tracker owns meaning; root records qualifying evidence; reducer derives overlay. | Current: preserve exactly. Research: N/A. Prototype: N/A. Protected: yes. C1: none. | Tracker pointer, `SKILL.md`, `RUN-LEDGER.md`, helper. Overlay lifecycle and invalidation tests. |
| `B0-11` | Any nonterminal return is recovery-complete: preserve accepted/unrelated state, halt unsafe progression, account for actors and lanes, release ended claims, invalidate unsafe overlays, leave items open, and state blocker/recovery. | Engineering stewardship/recovery/Lock; tracker release/read-back; current checkpoint and lane safety compatibility. | Root owns disposition; helper validates recorded facts. | Current: preserve mechanics, remove Release terminology from nonterminal outcomes. Research: no direct efficacy proof. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md` Return, ledger checkpoint/resume, lane lifecycle. Connector partial-failure and checkpoint/resume behavior plus deterministic state validation. |
| `B0-12` | Lock only the accepted reviewed current `HEAD`; then close children with mutation read-back, close the parent last after its rule passes, release claims, verify authorized push, and make lanes safe. | Engineering Lock; tracker closeout/read-back; review relationships; current closeout helper compatibility. | Root alone owns Lock and external mutations. | Current: preserve reviewed-HEAD, friction compatibility, closeout and push evidence; cut unsupported efficiency result. Research: corroborated review separation only. Prototype: N/A. Protected: yes. C1: none. | `SKILL.md` Lock/completion, ledger closeout, tracker relationship. Live child/parent closeout, partial mutation, wrong-HEAD, lane, and push-proof cases. |

Every unit has one basis, owner, disposition, destination, and proof. None
depends on a current-only efficiency hypothesis.

## Executable B0

The promoted runtime expresses this irreversible order:

```text
admit root + exact parent graph
-> trace and reconcile canonical state
-> derive dependency-ready set
-> qualify serial or concurrent frontier
-> claim and read back
-> isolate, execute, and prove each bounded lane
-> accept child returns at the root
-> integrate serially and run recombined proof
-> repeat until the exhaustive graph drains
-> run final current-HEAD proof
-> obtain independent fixed-point Spec + Standards review
-> run bounded Repair and successor review when admitted
-> Lock the accepted reviewed current HEAD
-> close children with read-back
-> close parent last with read-back
-> release claims, verify authorized push, and make lanes safe
-> return complete
```

At every arrow, a failed gate returns `partial` or `blocked` with the
recovery-complete `B0-11` packet; it does not skip ahead. Accepted prior work
and unrelated work survive. Affected dependency overlays are invalidated
before unsafe progression.

The common-path runtime lives in `SKILL.md`. Branch-only executable schema,
Windows worktree lifecycle, worker/integrator packet detail, and ledger
operations remain disclosed behind their triggered pointers. Rejected
efficiency hypotheses have no canonical runtime expression; the protected
compatibility set below remains intact.

## C1 Decision

There are no admitted hypotheses. Exact delta:

```diff
# C1 relative to B0
# no additions, removals, or substitutions
```

Former proposal dispositions:

| Hypothesis | Origin | Owner | Expected B0 failure | Cheapest expression | Wrong-condition case | Required proof | Destination | Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Friction synthesis as campaign behavior | Current retention | Parallel Implement | None established | Existing finish path | Ordinary delivery with no generic gap | Exact control showing B0 loses required recovery or quality | Historical evidence only | Reject from candidate; keep current helper compatibility only where required. |
| Warm-primary reuse and compact receipts | Current synthesis | Parallel Implement | No B0 failure demonstrated | Reuse actor plus compact delta | Item needs fresh ownership/context or delta omits governing facts | D0/B0 behavioral and context evidence | Future research/behavior decision | Not admitted. |
| Adaptive width, result queue, and Downshift | Current synthesis | Parallel Implement | No B0 failure demonstrated | Width state and queue gates | Shared semantics, proof resources, order, or integration | Exact contribution and worst-case recovery evidence | Future research/Prototype | Not admitted. |
| Prepared terminal facade | Current synthesis | Helper/runtime owner | No B0 failure demonstrated | `prepare`/`apply` facade | Root judgment or external mutation is unsettled | Operator behavior plus authority-negative controls | Future Prototype | Not admitted. |
| Passive efficiency result | Current synthesis | Evaluation owner | No B0 failure demonstrated | Derived terminal metrics | Telemetry unavailable or metric becomes a completion proxy | Fixed control/candidate protocol with real telemetry | Validation only | Not admitted. |

These rows preserve decision-changing alternatives and rejection reasons
without leaving duplicate normative proposals.

## Protected Compatibility Set

The promoted package preserves:

- current `run_ledger.py` schema version, compatibility CLI, stable event
  authority, prospective validation, receipts, idempotency, Repair budgets,
  review counters, checkpoint/resume, closeout planning, and mutation
  read-back;
- `lane_worktree.py` Windows path handling, explicit containment, Git trust
  handling, checkout/index/object probes, Python provenance, stable temporary
  roots, registered cleanup, long-path residual recovery, and non-destructive
  failure;
- exhaustive graph, To Tickets execution-profile, state-boundary, review,
  Repair, tracker, and closeout matrices;
- root-only invocation and the delegated routing blocker;
- worker no-fanout, no-integration, no-formal-review, no-tracker, and no-push
  boundaries;
- one canonical event stream with generated projections never substituted for
  authority;
- serial landing and current-HEAD recombined proof;
- reversible `landed-awaiting-lock`;
- independent formal review and reviewed-current-HEAD Lock; and
- child-first, parent-last closeout with per-mutation read-back.

Protection does not preserve current prose, section names, actor counts,
efficiency rationale, or unsupported optimization behavior.

## Runtime Surfaces

| Surface | Promoted state | Foreign behavior kept with owner |
| --- | --- | --- |
| `skills/custom/parallel-implement/SKILL.md` | Invocation, outcome, root authority, common order, concurrency qualification, acceptance, integration, review handoff, safe Return, Lock, and completion | Engineering, tracker, review, resolver, bootstrap, TDD, diagnosis, and To Tickets procedure remain pointers. |
| `agents/openai.yaml` | Explicit-only policy and concise prompt consistent with B0 | No runtime procedure in metadata. |
| `references/WORKER-BRIEF.md` | Complete bounded assignment and typed return; worker prohibitions | TDD/diagnosis details remain with callees. |
| `references/INTEGRATOR-BRIEF.md` | Optional bounded integration-only packet and return | Root dispatch, formal review, tracker, push, and Lock stay out. |
| `references/CODEX-WORKTREE-LAUNCH.md` | Isolation, provenance, containment, recovery, and cleanup branches | Actor selection and semantic acceptance stay out. |
| `references/RUN-LEDGER.md` | Canonical stream operation, recovery, artifact authority, compatibility commands, and read-back | Root judgment and external provider mutation stay out. |
| `scripts/run_ledger.py` | Protected machine contract retained byte-identically | No semantic independence, finding admission, or tracker-provider authority. |
| `scripts/lane_worktree.py` | Protected lane contract retained byte-identically | No worker selection or campaign completion. |
| `docs/synthesis/skill-context-relationships.md` | Published the changed invocation, review, resolver, graph-defect, and closeout wording without changing topology | No copied Parallel Implement procedure. |
| `tests/test_skill_pack_contracts.py` and `docs/validation/evals/core-workflows.md` | Deliberately unchanged; existing general contracts remain valid and candidate-owned proof covers the promoted bytes | No incidental prose snapshots or simulated efficacy claims. |
| Installed mirror | Managed only by `scripts.install_skills`; identity is recorded in the Prompt 5 validation record | Never edit independently. |

## Proof Matrix

| Lane | Claim | Exact control or cases | Gate |
| --- | --- | --- | --- |
| B0 viability | Constructed B0 can deliver the admitted graph without a C1 addition. | Fixed live parent graph; serial graph; qualified concurrent frontier; partial worker/connector failure; conflict; integration regression; Repair; child/parent closeout. Use at least five fresh samples only for behavioral steering claims. | Every B0 unit passes with no critical authority, recovery, or completion failure. |
| Conditional D0 | Recovery-ledger steering and qualified-concurrency wording change behavior beyond no steering. | Invocation held constant; fixed context/tools/authority/evidence; omit only the tested B0 wording for `B0-03` or `B0-05`; inspect every sample under `BEHAVIOR-EVALS.md`. | Control exhibits the claimed failure and B0 materially improves it without critical regression. Otherwise remove or restate as contract without an efficacy claim. |
| C1 contribution | No C1 delta exists. | Identity read-back: exact B0 bytes equal exact C1 bytes. | Hash equality; no contribution claim. |
| Invocation | Explicit parent delivery fires; one item, raw graph, generic investigation, review-only, and delegated invocation do not execute the campaign. | Positive and adjacent-negative tasks using exact metadata and skill bytes; current-byte results are historical only. | Correct route/Return with no unauthorized mutation. |
| Protected contracts | Helper schema/CLI, event authority, idempotency, Windows/provenance/containment/cleanup, budgets, checkpoint/resume, matrices, overlay, review, and read-back remain intact. | Focused deterministic tests, relationship traces, helper fixtures, and exact current-to-candidate compatibility audit. | All affected contracts pass; unrelated protected behavior unchanged. |
| Pruning | Every retained instruction changes required behavior or preserves a protected contract. | Complete line/semantic-unit cut audit against Prompt 4-accepted C1. | No safe material cut remains, or every material cut passes exact equivalence proof. |
| Deterministic structure | Package, metadata, links, references, helper commands, and relationships are coherent. | Skill validation, focused pack tests, affected Markdown gate, hashes, and both diff checks. | All current affected checks pass. |

Future context transport, terminal-facade, or efficiency-result optimization
requires a new owner-matched D0/B0 claim protocol; this campaign makes no such
efficacy claim.

## Prior Evidence Dispositions

| Evidence | Disposition | Reusable claim and limit |
| --- | --- | --- |
| Current helper tests | `lane-limited` | Exact current helper schema, CLI, reducer, worktree, and compatibility lanes only; not constructed B0 behavior. |
| 2026-07-18 coordinated-v2 evaluation | `historical-admission-only` | Historical current-runtime behavior; bytes and selected B0 contract differ. |
| 2026-07-18 checkpoint-correction evaluation | `historical-admission-only` | Supports inspecting recovery mechanics; not a current B0 control. |
| 2026-07-13 workflow and cohesion traces | `historical-admission-only` | Relationship and route history only. |
| Current relationship map | `lane-limited` | Current independent-owner relationships; exact candidate trigger/Return must be rechecked. |
| Preserved experimental package and synthesis | `historical-admission-only` | Former efficiency hypotheses and extraction history; baseline drift invalidates control use. |
| Prompt 4 recovery D0/B0 controls | `exact-reusable` | Exact candidate hash, fixed resume task, runtime, five samples per arm, and recorded rubric only. |
| Prompt 4 concurrency D0/B0 controls | `exact-reusable` | Exact candidate hash and fixed frontier task only; no efficacy credit because both arms passed `5/5`. |
| Prompt 4 whole-package viability | `exact-reusable` | Five exact-context samples for the recorded invocation, authority, Return, completion, Repair, and relationship cases. |
| Prompt 4 candidate-path helper suite | `exact-reusable` | Protected helper mechanics only; `46/46` maintained tests executed through experimental paths. |
| Live parent graph, external connector failure, remote push, and irreversible closeout | `missing` | Named residual risk; no external mutation was authorized. |

Exact reuse remains limited to matching bytes, task, protocol, configuration,
tools, authority, evidence, runtime, rubric, and proof lane.

## Facts, Synthesis, and Inference

Facts:

- the checkpoint and source identities above are the root-verified Prompt 1
  packet;
- pre-promotion canonical runtime file identities at Prompt 2 start were:
  `SKILL.md` `6f26f85d...`, metadata `e209a55b...`,
  `CODEX-WORKTREE-LAUNCH.md` `b43a9621...`,
  `INTEGRATOR-BRIEF.md` `2524980d...`, `RUN-LEDGER.md` `5f5da643...`,
  `WORKER-BRIEF.md` `2d9a247d...`, `lane_worktree.py` `0884edd6...`,
  and `run_ledger.py` `caa17452...`;
- source packages prove their recorded instructions and mechanics, not
  behavioral effectiveness; and
- exact B0/C1 bytes are canonical at
  `036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc`;
  Prompt 4 produced candidate-owned behavioral and deterministic evidence.

Synthesis:

- the 12 units are jointly sufficient for the settled viability floor;
- the source-derived minimum retains qualified concurrency, serial
  integration, durable recovery, and formal review while removing unproved
  efficiency mechanisms; and
- `C1` needs no addition.

Prompt 4 learned:

- recovery-ledger wording improved the fixed resume case from `0/5` D0 samples
  to `5/5` B0 samples by preventing premature tracker closure;
- qualified-concurrency wording received no efficacy credit because D0 and B0
  both passed `5/5`; the unit remains only as an independently required
  protected contract; and
- five whole-package B0 samples passed invocation, authority, required-input,
  recovery, integration, Repair, relationship, Return, and completion cases
  with no critical failure.

These conclusions are scoped to the exact promoted bytes, fixed packets,
runtime, sample counts, rubrics, and deterministic lanes recorded by Prompt 4.

## Promotion Lifecycle and Residual Gaps

Lifecycle state after Prompt 5 canonical integration:

```text
Prompt 1 checkpoint: verified
Prompt 2 synthesis: decision-complete
B0 bytes/hash: skills/custom/parallel-implement at 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
C1 bytes/hash: same corpus and hash as B0; no C1 delta
Prompt 3 construction record: docs/validation/transcripts/2026-07-23-parallel-implement-prompt3-construction.md
Prompt 4 behavior-complete package: accepted at the same B0=C1 hash
Prompt 4 record: docs/validation/transcripts/2026-07-23-parallel-implement-prompt4-behavior-audit.md
Pruning disposition: pruning-not-needed; C1 remains byte-identical at 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc
Pruning record: docs/validation/transcripts/2026-07-23-parallel-implement-pruning.md
Canonical promotion: exact final C1 promoted; candidate/canonical parity proved before experimental retirement
Relationship publication: changed trigger and Return wording published without topology change
Managed installation: canonical and installed trees match at 036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc; clean post-install dry-run
Git delivery: pending
```

Residual gaps preserved for successors:

- live external parent-graph, tracker connector, remote push, and irreversible
  closeout evidence remain unavailable and are not claimed;
- the required xdist-configured full suite exposed Windows Git-subprocess
  instability in two helper cases per run; both isolated cases and the full
  207-test suite pass serially, so parallel-run stability remains an explicit
  proof-environment residual rather than a canonical behavior claim.

Prompt 4 accepted B0=C1 without repair. The recovery comparison demonstrated
the registered control failure and removed it; the concurrency comparison did
not demonstrate a control failure, so it created no efficacy claim or byte
change. Candidate-path helper tests passed `46/46`; exact invocation, context,
safe Return, completion, and relationship cases passed `5/5`. Prompt 5 reused
that exact evidence because bytes, tasks, claims, and evidence contracts were
unchanged.

## Pruning Decision

The Deploy Pruning Pass audited the complete eight-file runtime-facing package
at the accepted Prompt 4 hash. Every instruction-bearing passage was
classified once against the question, “If I cut this, what behavior may
change?” No `collapse`, `disclose`, or `delete` proposal reduced an
always-loaded description, common-path instruction, duplicated semantic
ownership, branch load, or unused package surface without risking a protected
contract.

The most plausible apparent repetitions were retained deliberately:

- metadata routing and body admission serve distinct invocation and execution
  surfaces;
- root, worker, and integrator authority is repeated only in the packet each
  actor receives;
- the phase spine and detailed gates encode order at different levels;
- normal ledger commands and compatibility commands serve distinct branches;
  and
- negative worktree and completion clauses are non-intuitive safety
  guardrails paired with the safe action.

Disposition: `pruning-not-needed`. No accepted bytes changed, no pre-prune
fixture was created, and no behavioral equivalence wave ran. The complete cut
ledger and focused proof are in
`docs/validation/transcripts/2026-07-23-parallel-implement-pruning.md`.

Load delta:

| Named load | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Always-loaded description | 304 characters | 304 characters | 0 |
| Common-path `SKILL.md` | 7,689 bytes | 7,689 bytes | 0 |
| Disclosed branch reference | 18,915 bytes | 18,915 bytes | 0 |
| Unused package surface | 0 files | 0 files | 0 |
| Complete candidate corpus | 8 files / 162,792 bytes | 8 files / 162,792 bytes | 0 |

The exact promoted canonical tree SHA-256 is
`036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc`.
