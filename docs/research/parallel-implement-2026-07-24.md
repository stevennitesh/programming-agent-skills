# Parallel Implement Research Packet

Campaign epoch: `2026-07-24`

<!-- DECISION-CONTENT-BEGIN -->

## Research Contract

- Question: Which methods, vocabulary, conditions, and alternatives best
  support the settled intended behavior of `parallel-implement`?
- Caller use: Deploy Prompt 2 may reconcile this evidence with the exact M0
  checkpoint and current runtime; this packet does not design or prove H1.
- M0 checkpoint:
  `../validation/transcripts/2026-07-24-parallel-implement-prompt1-m0.md`
- Verified M0 content fingerprint:
  `c91962879ff9bd03b48c34fa422974fff8a2aee8362c8a879627ebc66039271a`
- Repository fixed point: Git `HEAD`
  `94d68e78d8812e9a2ceffd093e729402cac1cff2`.
- Freshness: independent online sources were inspected on `2026-07-24`;
  checked-out upstream and current packages were inspected at the identities
  below.
- Write authority: create only this note.
- Exclusions: no M0, synthesis, runtime, relationship, evaluation,
  installation, tracker, remote, or Git mutation; no behavioral-effectiveness
  claim for untested candidate wording.
- Return owner: the active Deploy Campaign coordinator.

Research status: `answered`.

Deploy Research Pass decision: `research-complete`.

## Executive Answer

The strongest supported operating model is a root-owned reconciliation and
integration controller over an exhaustive dependency graph:

1. derive a ready frontier from authoritative dependency and campaign state;
2. qualify concurrency across semantic, write, proof-resource, ordering, and
   irreversible-state boundaries;
3. claim before dispatch and isolate each bounded worker;
4. treat each return as evidence, not integration authority;
5. refresh and land accepted commits serially;
6. prove accumulated semantics on the current integrated snapshot;
7. review one immutable drained snapshot;
8. bound repair generations and review successors; and
9. reconcile and read back child-first external closeout before completion.

This model is `independently-supported` under the conditions recorded below.
The evidence does not support parallel dispatch merely because capacity
exists, work stealing for human-scale agent campaigns, concurrent integration,
projection-as-authority, unbounded review/repair, or optimistic external
closeout. Those alternatives are either narrower than this problem,
counterindicated by shared state, or `unverified`.

The exact current package covers every M0 semantic unit. Research found no
settled-intent omission, so M0 does not reopen. Exact current, M0, and H1 byte
identities remain `unknown-until-prompt2`: semantic coverage is not byte
identity and this pass does not materialize M0.

## Blind Independent Discovery

This discovery was completed and recorded before inspecting Matt Pocock,
Superpowers, Ponytail, the current target package, target synthesis, or
historical target evaluations.

### Graph scheduling and truthful frontiers

- **Claim:** dependency-ready is necessary but insufficient for safe
  concurrency; shared semantic state, write targets, proof resources, and
  irreversible operations can impose additional precedence or mutual
  exclusion. **Label:** `synthesis`. **Method:** `independently-supported`.
  Git worktrees isolate per-worktree `HEAD` and index state, but share repository
  state and configuration; SQLite WAL permits concurrent readers with one
  writer and documents checkpoint starvation under sustained readers. These
  are directly applicable analogues for isolated execution plus serialized
  authority, not proofs about agents.
  ([Git worktree](https://git-scm.com/docs/git-worktree),
  [SQLite WAL](https://www.sqlite.org/wal.html))
- **Claim:** randomized work stealing has strong bounds for fully strict
  multithreaded computations. **Label:** `direct`.
  **Method:** `contested` for this application. The original result assumes a
  formal fully strict computation and machine-level scheduling; an agent
  campaign has semantic dependencies, heterogeneous judgments, external
  mutations, and scarce proof environments that violate the direct
  applicability conditions. The DOI landing rejected automated access, so the
  paper text was inspected through an accessible scholarly copy and its
  bibliographic identity was cross-checked against the Cilk project
  publication registry.
  ([Cilk publications](https://cilk.mit.edu/publications/),
  [JACM DOI](https://doi.org/10.1145/324133.324234))
- **Consequence:** use a resource-qualified frontier and serialize on
  uncertainty. Do not add work stealing, adaptive width, or throughput claims
  without a candidate-owned protocol that models semantic and external-state
  hazards.

### Isolated workers and serial integration

- **Claim:** linked Git worktrees provide distinct working trees with
  per-worktree `HEAD` and index, while repository configuration and some
  administrative state remain shared. Git refuses common unsafe cases and
  preserves explicit worktree states for inspection and repair.
  **Label:** `direct`. **Method:** `independently-supported`.
  ([Git worktree](https://git-scm.com/docs/git-worktree))
- **Claim:** cherry-pick conflicts leave `HEAD` at the last successful commit,
  record `CHERRY_PICK_HEAD`, retain index stages and conflict markers, and
  expose explicit continue, skip, quit, and abort operations.
  **Label:** `direct`. **Method:** `independently-supported`.
  ([Git cherry-pick](https://git-scm.com/docs/git-cherry-pick))
- **Limit:** worktree isolation is not hermetic process, network, credential,
  cache, or proof-resource isolation; Git also documents incomplete submodule
  support for multiple worktrees. A preflight must therefore verify more than
  the directory path.
- **Consequence:** one bounded commit plus exact base/tree/proof evidence is a
  useful worker handoff. The root must refresh, inspect, and land serially;
  conflict detection preserves state and transfers only reconciliation
  authority to the conflict owner.

### Durable event state, resume, and reconciliation

- **Claim:** an append-oriented log can support reconstruction and temporal
  inspection, but replay must suppress or separately account for external side
  effects and external query results. **Label:** `direct` for the source,
  `inference` for this skill. **Method:** `independently-supported` with
  limits.
  ([Martin Fowler, Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html))
- **Claim:** a reconciliation controller repeatedly compares observed current
  state with declared desired state, performs bounded changes, and reports
  observed state for other controllers. **Label:** `direct`.
  **Method:** `independently-supported`.
  ([Kubernetes controllers](https://kubernetes.io/docs/concepts/architecture/controller/))
- **Claim:** a single append authority is a simpler concurrency boundary than
  concurrent writers. SQLite WAL illustrates that append-based readers can
  coexist while one writer serializes change, and also exposes log-growth and
  checkpoint counterpressure. **Label:** `direct` plus `inference`.
  **Method:** `independently-supported` as a design analogy, not a database
  prescription.
  ([SQLite WAL](https://www.sqlite.org/wal.html))
- **Consequence:** keep one canonical campaign stream with a single writer;
  derive projections; on resume reconcile stream, Git, lanes, actors, claims,
  tracker, remote, and overlays before authorizing progression. Corrupt,
  incompatible, or competing state must be preserved and returned through a
  typed recovery branch.

### Proof, review, and bounded repair

- **Claim:** review should assess tests, behavior, maintainability, and
  standards, while tests themselves require human judgment. **Label:**
  `direct`. **Method:** `independently-supported`.
  ([Google review guidance](https://google.github.io/eng-practices/review/reviewer/looking-for.html))
- **Claim:** review should improve code health without demanding perfection;
  unresolved disagreement should escalate rather than loop indefinitely.
  **Label:** `direct`. **Method:** `independently-supported`.
  ([Google review standard](https://google.github.io/eng-practices/review/reviewer/standard.html))
- **Counterpressure:** small, self-contained changes reduce review complexity,
  and early review can catch defects sooner. That supports worker-local proof
  and bounded packets, but it does not replace the locally required formal
  review of the accumulated integrated snapshot.
  ([Google small changes](https://google.github.io/eng-practices/review/developer/small-cls.html))
- **Consequence:** drain actors and prove the exact current integrated tree
  before formal review. Classify findings against the Charter, admit one
  bounded automatic batch, escalate decision-required findings, cap repair
  generations, and review every successor snapshot.

### Dependency overlay and external closeout

- **Claim:** GitHub issue dependencies explicitly represent blocked-by and
  blocking relationships and expose read and mutation APIs.
  **Label:** `direct`. **Method:** `independently-supported` for provider
  semantics only.
  ([GitHub issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/learning-about-issues/about-issues),
  [issue dependency API](https://docs.github.com/en/rest/issues/issue-dependencies))
- **Claim:** idempotency keys can make retries safer, but their semantics,
  retention window, parameter matching, and treatment of failures are
  provider-specific. **Label:** `direct`. **Method:** `independently-supported`
  only when the actual provider offers an equivalent contract.
  ([Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests))
- **Counterpressure:** multiple external mutations are not automatically one
  transaction. A successful child mutation followed by a failed parent
  mutation is a real partial state, and a generic retry key cannot prove
  current tracker truth.
- **Consequence:** use the tracker as dependency authority; keep
  `landed-awaiting-lock` as a reversible campaign-local execution overlay;
  perform child-first then parent-last closeout; read every mutation back; and
  return applied, failed, and recovery actions on partial completion.

## Method Classification by M0 Cluster

| M0 cluster | Proposed method | Classification | Conditions and counterpressure | H1 consequence |
| --- | --- | --- | --- | --- |
| C01-C05 | Root reconciliation controller over one canonical event stream | independently-supported | Single writer; projections are derived; external observations must be refreshed; replay cannot repeat side effects | Eligible vocabulary hypothesis only if M0 expression leaves projection trust or resume ordering weak |
| C06 | Resource-qualified ready frontier | independently-supported | Independence includes meaning, writes, proof resources, ordering, protected state, and reversibility; uncertainty serializes | Preserve as M0 contract; prior comparison found no steering deficit, so no efficacy claim |
| C07 | Claim then read back before dispatch | independently-supported | Provider claim semantics and partial mutation behavior must be inspected; read-back remains necessary | No beyond-minimum addition currently justified |
| C08-C09 | Isolated bounded worker with immutable base and one commit/evidence Return | independently-supported | Worktree is not full hermetic isolation; startup, provenance, temp roots, credentials, and cleanup need explicit proof | Preserve worker fence and typed Return; branch detail may remain disclosed |
| C10-C12 | Root refresh plus dependency-safe serial landing and accumulated proof | independently-supported | Clean lane output may be stale or conflict after other landings; proof must run on current integrated state | Preserve serial integration; do not admit concurrent integration |
| C11 | Preserve partial Git operation and route exact state to conflict owner | independently-supported | Abort, skip, or discard changes state and require their own authority | Preserve as non-intuitive safety boundary |
| C13-C14 | Drained immutable formal review and finite repair generations | independently-supported | Early local review helps but does not cover accumulated integration; perfection loops harm progress | Keep formal snapshot gate and budgets; no unbounded reviewer-fixer loop |
| C15 | Reversible same-campaign dependency overlay | pack-specific | Local tracker contract requires it; independent sources support reconciliation but not this exact term | Preserve as local compatibility and intent behavior, not professional upper bound |
| C16-C17 | Child-first external closeout with per-mutation read-back | independently-supported | Cross-provider changes are non-atomic; idempotency is provider-specific; unknown remote state blocks completion | Keep inline completion gate and recovery-complete Return |

## Upstream Package Observations

Upstream packages were opened only after the blind discovery above.
Repetition among packages is evidence of pack usage, not professional
correctness or local fit.

| Package | Revision and worktree | Access depth | Observed behavior | Limits and disposition |
| --- | --- | --- | --- | --- |
| Matt Pocock skills | `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; clean | Complete `skills/engineering/implement/SKILL.md` and its published `docs/engineering/implement.md` | Explicit implementation from settled specs/tickets, TDD at agreed seams, regular focused checks, one final suite, review, commit | No parent-graph orchestration, isolation, durable recovery, external closeout, or parallel integration method; useful only for child execution relationships |
| Superpowers | `d884ae04edebef577e82ff7c4e143debd0bbec99`; clean | Complete `dispatching-parallel-agents`, `subagent-driven-development`, `using-git-worktrees`, and `requesting-code-review` skill bodies; referenced plan/spec files were discovery-only | Fresh focused agents; parallelize only independent domains; shared state contraindicates concurrency; review and verify returns; worktree isolation; durable progress record; per-task and final review | Its SDD skill explicitly serializes implementer agents and reviews each task; this is a credible alternative, not authority for this pack's exhaustive graph, tracker, formal-review, or closeout contract |
| Ponytail | `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; clean | Complete `skills/ponytail-review/SKILL.md` | Complexity-only deletion review with a narrow rubric | Not a correctness, orchestration, or formal-review source; useful counterpressure against speculative scheduling and facade machinery only |

### Targeted verification of upstream-observed mechanics

- Superpowers' worktree isolation is narrowed by Git's official documentation:
  per-worktree `HEAD` and index do not imply fully independent repository
  configuration, objects, submodules, processes, or proof resources.
- Superpowers' parallel-dispatch advice is consistent with the independent
  resource-qualified frontier, but its examples do not cover tracker claims,
  serial landing, external closeout, or irreversible state.
- Superpowers' per-task review is a credible alternative for early defect
  discovery. Google review guidance supports small reviewable changes and
  timely review, while the local contract still requires a final formal review
  of the accumulated immutable snapshot.
- Matt Pocock's review-and-commit child flow supports the child contract, not
  root orchestration or completion.
- Ponytail's deletion pressure rejects unsupported adaptive-width, queue,
  facade, and passive-efficiency additions unless a measured deficit appears.

## Current Runtime Observation and M0 Mapping

The complete current package was inspected at tree SHA-256
`036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc`.
Its eight file identities are:

| Current file | SHA-256 |
| --- | --- |
| `SKILL.md` | `8e7384da3f449f459b417c6c5e6eecf99d37dfe70cabc25508768897f611edc5` |
| `agents/openai.yaml` | `e209a55b28a7700bc6cf895277f4553cb4d7feac57021f810335d4581c6e038e` |
| `references/CODEX-WORKTREE-LAUNCH.md` | `b43a96214fcbeffd1a80fffcc2d00411a2deed4f9e2ea9318693b9727a62d18c` |
| `references/INTEGRATOR-BRIEF.md` | `cd6e1c03a02ac0ebefb8b634e8435bbaa3dc0b5c697e14dc193a18b9c4b48750` |
| `references/RUN-LEDGER.md` | `0488c81c3a8608ae4d06fad8eb2ea9ebaf5a161cb0b1926e30019553d78e0627` |
| `references/WORKER-BRIEF.md` | `3dd8e5f203591a730880adb29283628c6c255a6b9bb63de7ef4ce8e1b356980b` |
| `scripts/lane_worktree.py` | `0884edd628114a9101c3e9d544ee03699fbbef93b3c3ff2a35dcb915e0897ce8` |
| `scripts/run_ledger.py` | `caa174522351d903985dbe94632bb54f6beb16e5eb3dcdcd31e64ee2bbae1f2d` |

| M0 units | Current observation | Coverage disposition |
| --- | --- | --- |
| M0-01 to M0-03 | Explicit root-only exhaustive parent-graph admission; single-item, graph-defect, delegated, generic, and missing-setup routing | Covered semantically |
| M0-04 to M0-05 | Frozen Charter and one canonical `events.jsonl` authority; generated projections; resume reconciliation; single root writer | Covered semantically |
| M0-06 to M0-07 | Dependency-ready overlay, five-dimension concurrency qualification, serialization on uncertainty, claim then read-back | Covered semantically |
| M0-08 to M0-09 | Root-only dispatch; isolated worktree preflight; immutable assignment; worker and integrator fences; typed one-commit evidence Return | Covered semantically |
| M0-10 to M0-12 | Drain and validate returns; refresh and serial landing; preserved conflict route; landing-local and final accumulated proof | Covered semantically |
| M0-13 to M0-14 | Drained immutable candidate; ordinary/high-risk review routing; finding admission, Repair budgets, successor proof and review | Covered semantically |
| M0-15 | Reversible `landed-awaiting-lock` projection with invalidation and no tracker closure | Covered semantically |
| M0-16 to M0-17 | Reviewed-current-HEAD Lock; child-first parent-last read-back; claim/lane/push reconciliation; recovery-complete nonterminal Return | Covered semantically |

No current clause contradicts M0. Current behavior beyond the minimum includes
machine-compatible helper surfaces, detailed event schema, Windows worktree
recovery, compatibility friction fields, default budgets, and branch packet
formats. Their retention or pruning is a Prompt 2 onward decision; current
presence alone does not protect them.

## Alternatives and Counterpressure

| Alternative | Strongest case | Failure mode or limit | Disposition |
| --- | --- | --- | --- |
| Fully serial root implementation | Minimal state and integration overhead | Underuses truly independent ready work and expands root context | Credible fallback whenever qualification is uncertain; not the default for a proved independent frontier |
| Parallel agents in one shared checkout | Low setup cost | Shared index, worktree, caches, files, and proof resources make interference and provenance ambiguous | Reject |
| Work stealing or dynamic actor reassignment | Better utilization for formal strict computations | Agent tasks are heterogeneous, semantically coupled, externally stateful, and hard to resume without authority drift | Reject absent a bounded prototype and behavioral protocol |
| Concurrent landing | Potentially reduces integration latency | Integration order, stale bases, conflicts, and accumulated proof become non-deterministic | Reject |
| Per-task formal review only | Early defect discovery and small diffs | Does not judge the accumulated integrated current tree or cross-task effects | Retain only as worker-local or optional early review; final drained review remains required |
| Projection or progress file as campaign authority | Cheap resume | Can be stale, incomplete, or regenerated from missing facts | Reject |
| Event sourcing with unrestricted replay | Rebuildable state | Can repeat external side effects or depend on unavailable historical queries | Use only with separated side effects, reconciliation, and explicit incompatible/corrupt recovery |
| Provider idempotency as closeout guarantee | Safer retries when supported | Semantics and retention are provider-specific and do not make multi-step closeout atomic | Conditional helper, never a replacement for mutation read-back |
| Unbounded fix-review loop | Pursues all reviewer suggestions | Can chase perfection, exceed authority, and never terminate | Reject; use Charter admission, decision packets, and finite budgets |
| Prepared terminal facade or passive efficiency metric | Lower operator friction and observability | Risks converting helper output or telemetry into completion authority; no demonstrated deficit | Historical hypothesis only; require prototype or controlled deficit before admission |

## Intent-Adjacent Steering Hypotheses

These are hypotheses for Prompt 2 admission judgment, not accepted H1 units.
Each preserves the intended contract and requires M0-first comparative proof.

| Term | Recruited behavior | Expected M0 weakness | Observable gate | Comparative proof |
| --- | --- | --- | --- | --- |
| Reconciliation loop | Repeatedly compare canonical campaign events and every external observed state before progression after resume or interaction | Neutral durable-state wording may allow a stale projection, missing actor, retained claim, or unknown remote to be treated as completion | Resume packet names stream, Git, worktrees, actors, claims, tracker, remote, and overlay; no dispatch until each is classified | At least five fixed M0 samples first; run H1 only if M0 advances from projection or omits a named source; require correction without authority or completion regression |
| Resource-qualified frontier | Evaluate semantic ownership, writes, proof seams, scarce resources, ordering, protected state, and reversibility rather than file disjointness alone | Neutral graph-readiness wording may over-dispatch a pair with hidden semantic or proof coupling | Mixed frontier dispatches only the fully isolated set and records exact blockers for the coupled pair | At least five fixed M0 samples; run H1 only if M0 dispatches or cannot justify a coupled pair; prior current-runtime comparison cannot substitute |
| Semantic operation identity | Bind a retryable external mutation or event append to stable intent plus payload identity and reject changed replay | M0 read-back and recovery may still permit duplicate or altered retry after an ambiguous transport failure | Same identity plus same payload replays safely; changed payload rejects; observed provider state is still read back | Deterministic provider/helper branch proof plus partial-failure negative control; behavioral arm only if operator judgment changes |
| Drain barrier | Refuse formal review until actors are idle, accepted returns are landed, current-head proof passes, and the immutable target is frozen | Neutral review-order wording may review an incomplete or moving snapshot | Active actor, unlanded accepted packet, dirty tree, or proof failure blocks review target creation | M0-first mixed-state cases; run H1 only on a demonstrated early-review defect |
| Generation budget | Admit one bounded automatic finding batch and escalate decision-required or exhausted cases | Neutral bounded-Repair wording may allow perfection loops or silently discard findings | Automatic batch proceeds within counters; decision-required and exhausted cases return to root; successor gets new review identity | Deterministic counter and authority cases; behavioral comparison only if M0 loops, widens, or falsely completes |

Admission pressure:

- `Reconciliation loop` has the strongest intent-adjacent basis because prior
  historical evidence observed a control failure, but that evidence belongs
  to the prior epoch and does not prove a fresh M0 deficit.
- `Resource-qualified frontier`, `drain barrier`, and `generation budget`
  largely restate settled M0 behavior. Admit them beyond M0 only if the
  cheapest M0 expression demonstrably fails the registered gate.
- `Semantic operation identity` is conditional on the actual tracker/provider
  interface. It is `unverified` as a universal runtime addition.

## Prior Evidence Dispositions

No prior target artifact completes any unit of this fresh campaign.

| Prior evidence | Identity inspected | Disposition for this campaign | Exact reusable boundary |
| --- | --- | --- | --- |
| 2026-07-23 Prompt 3 construction | SHA-256 `ccbdef8477e1962bd54ef99d95d3f7ca9d697a0e8663a84a5fa01fd61661f106` | historical-admission-only | Historical construction and inventory discovery; fresh M0 and future H1 were not its inputs |
| 2026-07-23 Prompt 4 audit | SHA-256 `a1aeb85aa99fd796397a6ea8a501e5774fa681d4f6b408db6ee0709bccdb1e2f` | historical-admission-only | Hypothesis and task discovery only; fresh campaign control, candidate, and protocol identities are absent |
| Prompt 4 recovery samples | Five D0 and five B0 samples at prior tree `036dfdb8...` | historical-admission-only | Evidence that prior recovery wording corrected its fixed control; not fresh M0 deficit or current H1 contribution proof |
| Prompt 4 concurrency samples | Five D0 and five B0 samples at prior tree `036dfdb8...` | historical-admission-only | Both arms passed; supplies no efficacy claim and no fresh-campaign control |
| Prompt 4 viability samples | Five prior exact-candidate samples | historical-admission-only | Historical current-runtime behavior; fresh M0/H1 bytes, prompts, and proof lane are not fixed |
| Prompt 4 candidate helper suite | `46/46` at prior candidate paths and tree | lane-limited | Exact unchanged helper mechanics may be identity-rechecked later; it does not prove M0 viability or H1 contribution |
| 2026-07-23 Pruning Pass | SHA-256 `d54252f39cc70e5a33aba5f0345c2f05ac6ba6ead96604c8f10f6a7b0e773502` | historical-admission-only | Prior cut audit and load discovery only |
| 2026-07-23 Prompt 5 promotion | SHA-256 `b47586a0eb9f7f08003657d94cbfb47549d73a3fbeaf66cb14d7bab9d531d47c` | historical-admission-only | Establishes provenance of current tree; not fresh lifecycle completion |
| Current canonical helper bytes | `run_ledger.py` `caa17452...`; `lane_worktree.py` `0884edd6...` | lane-limited | Deterministic current helper behavior only after exact command, environment, and fixture identity read-back |
| Live parent graph, real tracker partial failure, remote push, irreversible closeout | none | missing | Requires separately authorized external-state proof |

There is no `exact-reusable` candidate-owned behavioral proof at this Research
Pass because exact fresh M0/H1 bytes, tasks, prompts, protocol, host,
configuration, rubric, and proof lane do not yet coexist.

## Conflicts, Rejected Lanes, and Gaps

### Conflicts retained

- Work stealing is effective under formal fully strict computation assumptions,
  while the target problem contains judgment, heterogeneous tasks, external
  state, and semantic resource conflicts. The source is strong but its
  application here is contested.
- Early per-task review reduces defect latency, while local intent requires one
  final formal review of a drained immutable integration snapshot. Both can be
  true; early checks do not replace the final gate.
- Append logs improve reconstruction, while external side effects and queries
  make unrestricted replay unsafe. The event stream must separate durable
  record from external mutation authority.

### Rejected discovery lanes

- Popularity, download counts, testimonials, and generic multi-agent
  productivity claims were rejected because they do not own correctness,
  applicability, or local fit.
- Search snippets and secondary summaries were used only to locate the
  inspected governing or primary source.
- General distributed consensus, cluster schedulers, and database transaction
  protocols were rejected as heavier than the root-owned local campaign and
  unable to settle agent behavior without a specific mechanism claim.
- Ponytail benchmark results were not used because its inspected review skill
  owns only over-engineering feedback, not orchestration efficacy.

### Residual gaps

- No live parent graph, tracker connector failure, remote push, or irreversible
  closeout was authorized; real-provider partial-state behavior remains
  unproved.
- The actual tracker may or may not offer idempotency or conditional mutation;
  provider-specific retry mechanics remain `unverified`.
- Git worktrees do not establish process, credential, cache, network, or scarce
  proof-resource isolation; those branches require local preflight proof.
- Independent sources support the methods and limits, not exact skill wording
  or behavior on a particular model/host.
- Fresh M0 viability and any H1 contribution belong to Prompt 4 and cannot be
  inferred from this packet.

None of these gaps blocks Prompt 2 because they constrain claims and proof
design rather than leaving a load-bearing method unknown.

## Source Registry and Identity Verification

| Source | Identity and access | Authority for retained claim | Limitation |
| --- | --- | --- | --- |
| Blumofe and Leiserson, "Scheduling Multithreaded Computations by Work Stealing" | JACM 46(5), 720-748; DOI `10.1145/324133.324234`; accessible paper text inspected and identity cross-checked in the Cilk publication registry on 2026-07-24; DOI landing returned HTTP 403 to automated access | Fully strict work-stealing conditions and bounds | Not an agent, tracker, Git, or external-mutation study |
| Git worktree documentation | Live official manual, version selector current on access 2026-07-24; commands, configuration, details, examples, and bugs inspected | Worktree separation, shared state, lifecycle, and limits | Git mechanics only |
| Git cherry-pick documentation | Live official manual, version selector current on access 2026-07-24; conflict and sequencer behavior inspected | Preserved conflict/partial-operation state and explicit recovery commands | Does not choose campaign authority |
| SQLite WAL | Official live documentation accessed 2026-07-24; overview, concurrency, checkpoint, and limitations inspected | Append/concurrency/single-writer analogy and counterpressure | Database mechanism, not a prescribed campaign store |
| Kubernetes controllers | Official live documentation accessed 2026-07-24; controller pattern and desired/current state inspected | Reconciliation-loop method | Cluster control loop, not exact local implementation |
| Martin Fowler Event Sourcing | Identifiable practitioner article accessed 2026-07-24; rebuild, temporal query, replay, external gateway/query limits inspected | Event-log reconstruction concepts and replay limits | Practitioner evidence; not a standard |
| Google Engineering Practices | Official public review standard, review targets, and small-change guidance accessed 2026-07-24 | Review scope, progress/perfection tradeoff, escalation, test judgment | Organization practice, not empirical agent evaluation |
| GitHub Issues and dependency API | Official live product/API documentation accessed 2026-07-24 | Dependency representation and read/mutation surfaces | Provider behavior only; local tracker may differ |
| Stripe idempotent requests | Official live API documentation accessed 2026-07-24 | Conditions and limits of one concrete idempotency contract | Not authority for another provider |
| Matt Pocock skills | Local checkout `ed37663cc5fbef691ddfecd080dff42f7e7e350d`, clean | Exact inspected upstream text | Pack behavior only |
| Superpowers | Local checkout `d884ae04edebef577e82ff7c4e143debd0bbec99`, clean | Exact inspected upstream text | Pack behavior only |
| Ponytail | Local checkout `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`, clean | Exact inspected upstream text | Complexity-review behavior only |
| Current target package | Tree SHA-256 `036dfdb8afc4bb34968c83a9bbd429e14d63819f2041c61b9518336d0e4770dc` | Exact current instructions and mechanics | Current presence is not intent or efficacy |

Every load-bearing claim was checked for source identity, direct entailment,
authority, applicability, and counterpressure. The independent sources own
their stated technical or practice claims; upstream packs own only their
inspected text; current observations own only current behavior.

## Stopping Basis and Caller Boundary

Decision saturation was reached:

- every M0 research cluster has a classified method, applicability conditions,
  credible alternative, and counterpressure;
- the strongest available official, governing, original, or identifiable
  practitioner owner was inspected for each load-bearing claim;
- all three required upstream checkouts, the complete current package, target
  synthesis, historical construction/promotion records, raw behavioral
  outputs, and helper-verification evidence were inspected at recorded
  identities;
- every M0 unit has a current-runtime mapping and no omitted settled-intent
  behavior was found;
- prior evidence has an exact fresh-campaign disposition; and
- another bounded source is unlikely to change a method classification,
  applicability condition, or proposed observable gate.

Prompt 2 may decide which hypotheses, if any, merit H1 construction. It must
not treat independent support, upstream repetition, current presence, or
historical proof as candidate-owned behavioral effectiveness.

Return owner: active Deploy Campaign coordinator.

Decision: `research-complete`.

<!-- DECISION-CONTENT-END -->

Content fingerprint algorithm: SHA-256 over the exact UTF-8 bytes after the
`DECISION-CONTENT-BEGIN` marker line through the byte immediately before the
`DECISION-CONTENT-END` marker line, including the intervening line endings.

Content fingerprint: `3d8ad3acb1aedaf5a3c857d2a2ca573b67472072149ed7df71e8e07bc52b0d54`
