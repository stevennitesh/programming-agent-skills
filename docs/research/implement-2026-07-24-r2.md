# Implement Research Pass R2 — 2026-07-24

## Research lock

- **Question:** Which methods, vocabulary, conditions, alternatives, and
  counterpressure best support the corrected frozen `implement` M0 contract,
  with fresh attention to repository-local tracker closeout, staging/commit
  identity, connector post-commit mutation, and partial-state recovery?
- **Caller use:** decision-ready evidence for Deploy Prompt 2. This note does
  not alter M0, choose exact H1 wording, prove behavioral efficacy, or
  authorize a successor.
- **Fixed point:** Git `HEAD`
  `94d68e78d8812e9a2ceffd093e729402cac1cff2`; corrected marker-bounded M0
  payload
  `sha256:c56d01368a49d19ed33fb4d0c4b926029d6264885e36bea5af820f40c31d5f0c`.
- **Checkpoint source:** complete
  `docs/validation/transcripts/2026-07-24-implement-prompt1-m0-r2.md`;
  whole-file SHA-256
  `55b67451767f28ab1f9ead001df9ba84f23575483b951f05b8f48dbaa346d4e6`.
- **Freshness:** online sources checked 2026-07-24; local and upstream
  repositories are identified below at their inspected revisions.
- **Write authority:** create only
  `docs/research/implement-2026-07-24-r2.md`.
- **Return owner:** Deploy Campaign coordinator.

## Blind independent discovery

This section was established from the corrected intended behavior before
opening upstream packages, the current canonical target, target synthesis, or
historical research conclusions.

The blind search used these lanes:

- Git's index, tree, commit, and hook mechanics;
- GitHub and GitLab issue read/update surfaces;
- HTTP retry and idempotence semantics;
- distributed-workflow recovery and compensation counterpressure; and
- bounded change and review convergence.

The provisional result was:

1. A repository-local tracker file staged with selected work can inhabit the
   same Git tree and commit. That is one versioned repository snapshot, not a
   general distributed transaction.
2. Connector closeout is a separate service mutation. A verified repository
   commit therefore becomes the durable anchor for forward recovery; connector
   completion needs its own read-back.
3. An absent response does not establish whether an external write applied.
   Recovery must classify current state before retry, especially where the
   transport is not known to be idempotent.
4. A recovery record must retain completed steps, unknown effects, failed
   steps, and the exact safe continuation. Automatic rollback is not a sound
   default when a committed repository result is already durable.
5. Small coherent changes and review convergence remain professionally
   supported, but neither source class settles this repository's tracker order
   or commit authority.

Blind counterpressure retained:

- staging is recoverable preparation, not delivery;
- a successful commit does not imply successful tracker closeout;
- “atomic closeout” must not blur one Git snapshot with multiple systems;
- HTTP method labels alone do not prove provider-specific side effects safe to
  replay; and
- compensation can fail, overwrite concurrent state, or require human
  judgment, so forward reconciliation is often safer than automatic undo.

Popularity lists, generic workflow posts, search snippets, and upstream
repetition were rejected as claim authority.

## Answer

The corrected M0 remains viable and requires no intent reopen.

Its tracker-kind split is technically coherent:

- **Local Markdown:** the configured local tracker owns the order. After
  acceptable review, closeout metadata joins selected work in the index; Git
  then records the current index as one commit tree. Lock and post-commit tree
  comparison prove cohort identity. A closeout that is edited but unstaged, or
  staged but uncommitted, is truthful incomplete repository state.
- **GitHub/GitLab connector:** the verified commit is completed first. The
  connector mutation occurs afterward and cannot be claimed as part of the Git
  transaction. Completion waits for provider read-back of item state, claim,
  relationships, and frontier.
- **Partial connector state:** preserve the commit as the recovery anchor,
  refetch before replay, classify each intended field or operation as
  `applied`, `missing`, `conflicted`, or `unknown`, and perform only the
  provider-owned safe continuation. Never report complete from the request
  attempt alone.

Git directly supports the local identity mechanism: `git write-tree` creates a
tree from the current index, and `git commit` records the current index in a
new commit ([Git write-tree](https://git-scm.com/docs/git-write-tree),
[Git commit](https://git-scm.com/docs/git-commit)). Git does not decide which
files belong in the cohort; the corrected local tracker contract and M0 own
that choice.

GitHub and GitLab expose issue mutation as service API operations separate
from Git. GitHub provides distinct get and update endpoints and documents
success and failure responses; GitLab uses its issue update operation and
`state_event` to close or reopen
([GitHub Issues REST API](https://docs.github.com/en/rest/issues/issues?apiVersion=2022-11-28),
[GitLab Issues API](https://docs.gitlab.com/api/issues/)). These sources
support provider read-back and the cross-system boundary, but not a universal
retry recipe.

RFC 9110 says clients should not automatically retry a non-idempotent request
without known idempotence or evidence that the original request did not apply
([RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2)).
Microsoft's retry guidance gives the matching failure case: a service can
apply a request and lose the response, making blind replay unsafe
([Retry pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/retry)).
Its compensating-transaction guidance adds that recovery progress must be
recorded for resumption, retries should be idempotent, compensation can fail,
and manual intervention can be necessary
([Compensating Transaction pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/compensating-transaction)).

No professional source makes Local-Markdown-before-Lock the universal order;
that order is local authority. Independent evidence supports the mechanics and
recovery conditions, not the repository decision itself.

## Classified method support

| Method or claim | Research status | Method evidence | Applicability, counterpressure, and H1 consequence |
| --- | --- | --- | --- |
| Stage selected work and repository-local tracker closeout into one index tree, then verify that exact tree is committed. | `supported` | `independently-supported` for Git identity; local authority for cohort membership and order | Git's current manuals directly support index-to-tree-to-commit identity. Hooks and command failure can leave recoverable index/worktree state, so post-commit identity and status read-back remain necessary. This is already M0 U12–U14; no added H1 behavior is justified. |
| Describe the Local Markdown result as one versioned repository snapshot, not cross-system atomicity. | `supported` | `independently-supported` mechanics plus local application inference | The tracker file and selected work can share one commit tree. The claim must stay bounded to Git; it says nothing about external services or remote push. Candidate wording may clarify the boundary, but must not enlarge M0. |
| Keep connector work open through verified commit, then mutate and refetch the external item. | `supported` | `independently-supported` boundary; local authority for order | Git and provider APIs are distinct state systems. The sources do not prescribe this exact order; corrected M0 does. Preserve M0 rather than presenting the order as professional doctrine. |
| Reconcile external state before retry after an ambiguous or partial mutation. | `supported` | `independently-supported` | RFC 9110, provider get/update surfaces, and retry guidance support inspecting actual state before replay. Exact commands, retryable statuses, and field order remain tracker-transport owned. Retain and sharpen the prior H1 candidate. |
| Preserve a verified commit as the anchor and recover forward through missing connector steps. | `supported` | `independently-supported` under the settled no-rollback condition | Distributed-workflow guidance supports progress records and resumable steps; the local contract makes the commit the accepted durable result. Automatic commit rollback or issue reopening is not admitted. This can be an intent-adjacent quality-lift candidate only if M0 samples lose the anchor or choose unsafe replay/undo. |
| Treat PUT alone as proof that every GitLab closeout side effect is safe to replay, or PATCH alone as proof that GitHub is unsafe. | `unknown` | `unverified` | HTTP method semantics do not establish provider-specific comments, labels, assignments, events, or connector composition. Require configured read-back; do not admit method-name heuristics into H1. |
| Automatically compensate every failed post-commit connector closeout. | `conflicted` | `contested` by applicability | Compensation is domain-specific, can fail, and may overwrite concurrent state. Prefer forward reconciliation; escalate only the remaining ambiguous or owner-controlled action. |
| Work as one small, coherent, independently provable change. | `supported` | `independently-supported` | Google's current guidance defines a small CL as one self-contained change and records review, reasoning, rollback, and merge benefits ([Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)). “Small” is conceptual, not a line-count gate. Prior admission remains applicable. |
| Review should converge on a definite code-health improvement rather than perfection. | `supported` | `independently-supported` | Google's review standard balances forward progress with code health ([The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html)). It does not support a universal numeric repair count. |

## Prior evidence disposition

The prior packet
`docs/research/implement-2026-07-24.md` was inspected completely after blind
discovery; its current whole-file SHA-256 is
`bfba44c1fb0848da8896e3355855b9b00c9639c3cf6b4c2a222a5a6fe80a145d`.
It is evidence, not completion of this R2 Research Pass.

| Prior evidence | Identity/applicability result | Disposition |
| --- | --- | --- |
| Broad completion, small-batch, proof-selection, conditional-TDD, simplification, review-freshness, Git-identity, and push-authority claims | Same intended outcome and conditions; cited owner classes remain applicable; no corrected clause reverses them | `exact-reusable` for method admission only; never candidate behavioral proof |
| Prior RFC/GitHub “reconcile before retry” claim | Same claim and conditions, refreshed against RFC 9110 and current GitHub docs; extended with GitLab and distributed-recovery counterpressure | `lane-limited` to external-mutation recovery, now strengthened |
| Prior Git identity claim | Same Git mechanics; corrected M0 now makes local tracker cohort membership explicit | `lane-limited` to identity mechanics; local order remains local authority |
| Prior upstream and current-package observations | Revisions, worktree cleanliness, and inspected file hashes match exactly | `exact-reusable` as observation, not endorsement |
| Prior comparison between old M0 and current | Old marker-bounded M0 identity was `ff4ea3bc80cc12820d1debe8142d26832a0449d392ec843439118157902affbc`; corrected M0 is `c56d01368a49d19ed33fb4d0c4b926029d6264885e36bea5af820f40c31d5f0c` | `invalidated` for current M0 disposition |
| Prior `research-complete` lifecycle decision | Belonged to the old checkpoint and first authorized note | `invalidated` as R2 completion; retained as historical evidence |
| Prior candidate behavioral proof | None existed | `missing` |

The local implement research map
(`sha256:53ac14ae93c61b12fab9e0aebb37c309bd7b407b76f0f323b253554bb321462e`)
and search vocabulary
(`sha256:f37886f04988ee2f95c787588264be9e04f3e4feb30a4c08552be147980165c3`)
remain `historical-admission-only`. They own neither corrected intent nor
candidate proof.

## Upstream and current observations

These are observed package behaviors, not professional endorsements.

### Matt Pocock

- Revision `ed37663cc5fbef691ddfecd080dff42f7e7e350d`; clean worktree.
- Complete target package rechecked:
  `skills/engineering/implement/SKILL.md`
  (`sha256:30cd7bc1ebfb3891e85a1eed3b3b81aea0fa4ad4553a784de7f8e421b2d223e0`)
  and `agents/openai.yaml`
  (`sha256:8494f83602c58f8ab33d047d0516cdb90b8c29e6d564de0cef810daaca378bcb`).
- Observed behavior remains: explicit implementation of a spec/ticket,
  conditional TDD at pre-agreed seams, recurring focused proof, one final
  suite, review, and commit.
- Limit: no tracker-kind order, partial-state recovery, or commit/connector
  reconciliation behavior is present.

### Superpowers

- Revision `d884ae04edebef577e82ff7c4e143debd0bbec99`; clean worktree.
- Relevant files rechecked completely:
  `executing-plans/SKILL.md`
  (`sha256:bbd8d28bb655a52817cc129ce49f9e46fa7c6303f72ed5de95bfe914ef8e0ce8`),
  `verification-before-completion/SKILL.md`
  (`sha256:ea52d15aabaf72bc6b558efe2c126f161b53961090ddcd712000273bfe8c7b6c`),
  `requesting-code-review/SKILL.md`
  (`sha256:1017ccdd5bc61fab67c654cf118cbdb520464b313073a0a6b9a6b9aa647a3ad6`),
  `requesting-code-review/code-reviewer.md`
  (`sha256:b2f2ec7596925fe52dac158fdfbca19b3a7d779d619c481e6706a6c0001662d3`),
  `receiving-code-review/SKILL.md`
  (`sha256:647036bbdab7bf2317e14e079595e984c9030f64295e2b4c0fb57dbeb48f25dd`),
  `finishing-a-development-branch/SKILL.md`
  (`sha256:e6d4a812de900d33c6eacfb40747f99427f25c304a7b7099120f9373b115a47f`),
  and `test-driven-development/SKILL.md` plus its anti-pattern reference
  (`sha256:b5b4717b8b761cce15a6cfe9022e33fd959e0894c0c39d72c9cb49c23486c10e`
  and
  `sha256:bde453bc258f06543987477c837939afaa774ea2acbd9f308d702fc452bc4283`).
- Observed behavior remains: stop on plan gaps, demand fresh evidence before
  completion, review early, verify feedback, test repair, and offer explicit
  integration choices.
- Limit: it supplies no tracker-kind atomicity or connector recovery method;
  universal TDD and per-task review frequency do not transfer automatically.

### Ponytail

- Revision `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`; clean worktree.
- Relevant files rechecked completely:
  `skills/ponytail/SKILL.md`
  (`sha256:46a57e26a2632e7fa40eae6a3cf3011ccdc4d8db19d8f8617907d6b5deef055e`),
  `skills/ponytail-review/SKILL.md`
  (`sha256:40df33b58fc6ef889b93585733feb9566b76e9586efa7f376785c1e995197ac0`),
  and `benchmarks/agentic/README.md`
  (`sha256:bcd5dfea01aa15b03587de47699ff0ef9dadd49cef661896154cec308d5d542b`).
- Observed behavior remains a minimum-solution ladder plus
  complexity-only deletion pressure, with package-owned bounded benchmark
  evidence.
- Limit: it contributes no closeout, commit, connector, or partial-state
  recovery mechanic.

### Current canonical target

- Complete package rechecked:
  `skills/custom/implement/SKILL.md`
  (`sha256:7a8b391a92609e08e1b8f70526981381ddb9336c218aed8d3c28cc4fdb618b65`)
  and `agents/openai.yaml`
  (`sha256:d1331038252c7012dceebe0627884e12bb2a9975263b974bf9a991168d6dc3b8`).
- It already distinguishes local closeout before Lock from connector closeout
  after commit, uses exact review/lock/commit tree checks, and returns blocked
  on partial connector read-back.
- Current presence is compatibility evidence only. Its compact connector
  recovery wording does not prove that an agent will preserve the commit
  anchor, inspect before replay, or enumerate unknown effects.

## Intent-adjacent candidates and H1 effect

| Candidate | Mapping: term → recruited behavior → expected M0 weakness → observable gate → comparative proof | Admission |
| --- | --- | --- |
| **Self-contained small batch** | term → hold one independently understandable and testable change → “bounded” may be read as few files rather than one coherent result → every concern maps to the selected acceptance/proof story → M0/H1 fixtures containing tempting horizontal fragments and broad adjacent work | Preserve prior `independently-supported` candidate. |
| **Evidence before claims** | term → match every completion claim to fresh evidence → a green focused check may be extrapolated to delivery → every positive Return claim cites matching proof or is downgraded → stale, skipped, focused-only, and full-proof fixtures | Preserve prior intent-adjacent candidate; no tracker-specific change. |
| **Latest accepted tree** | term → bind review, Local Markdown cohort, Lock, and commit to one current identity → metadata edits or staging drift may be treated as still accepted → only permitted closeout metadata differs before Lock and committed tree equals Lock → structural identity plus post-review drift fixtures | Preserve and extend to corrected local cohort; method admission remains independently supported. |
| **Commit-anchored reconciliation** | term → preserve verified commit, refetch connector state, classify applied/missing/conflicted/unknown effects, then resume only safe missing steps → generic “partial-publication recovery” may invite blind replay, false rollback, or loss of the commit identity → ambiguous-before-apply, ambiguous-after-apply, partial-label/comment/claim, concurrent-change, and provider-error fixtures all return truthful state and one safe continuation → M0/H1 quality-lift comparison under fixed provider facts | Admit as `independently-supported` intent-adjacent candidate, bounded to post-commit connector failure. It refines the prior “reconcile before retry” candidate rather than adding a second recovery method. |
| **Green simplification** | term → simplify only under current proof → adjacent cleanup may widen the item → no acceptance, scope, or evidence delta → proof-invalidating and unrelated-cleanup fixtures | Preserve prior `independently-supported` candidate. |
| **Atomic tracker closeout** | term → imply one transaction across repository and connector → M0 already separates the systems → gate would obscure rather than clarify partial states → not applicable | Reject the cross-system term. For Local Markdown, prefer bounded “same commit tree/cohort” language if any wording candidate is needed. |
| **Provider retry by HTTP verb** | term → infer retry safety from PATCH/PUT alone → composite connector effects remain unverified → replay can occur only on method name → provider failure fixtures | Reject as `unverified`; configured tracker owner and read-back remain authoritative. |

The corrected local order adds no new H1 behavior: M0 already specifies the
review, mutation, staging, read-back, Lock, and commit gates. The research
effect is to prevent Prompt 2 from importing a cross-system “atomic” claim and
to focus the recovery hypothesis on connector failures after commit.

## Conflicts, limits, and rejected lanes

- **Local authority versus professional evidence:** the repository's Local
  Markdown and connector contracts settle order. Professional evidence only
  supports identity, distributed-state, and recovery mechanics.
- **Git atomicity:** one commit tree can contain selected work and local
  tracker metadata. This does not make staging terminal, eliminate hook
  failures, include unstaged bytes, or transact with a connector.
- **Connector idempotence:** GitHub's issue update uses PATCH and GitLab's
  documented update uses PUT, but exact closeout may include several effects.
  No inspected source proves the configured composite operation replay-safe.
- **Compensation:** distributed-workflow literature supports compensation only
  under domain-specific conditions. It does not authorize automatic commit
  reversal or tracker reopening here.
- **Repair count and universal TDD:** the prior unverified/contested
  dispositions remain unchanged.
- **Practitioner conversation:** none was needed; published governing,
  provider, and practitioner material resolved the operational condition.
- **Behavioral efficacy:** exact candidate wording remains untested. Prompt 4,
  not research, owns whether `commit-anchored reconciliation` changes agent
  behavior.

## Source identity and authority registry

| Source | Identity/access | Authority and limit |
| --- | --- | --- |
| Git commit and write-tree manuals | Official current HTML; `git-commit` last updated for Git 2.55.0 on 2026-06-29; complete relevant description and hook surface inspected 2026-07-24 | Governs Git index/tree/commit mechanics, not cohort authority or tracker policy |
| RFC 9110 §9.2.2 | Internet Standard HTML, exact idempotent-method section inspected 2026-07-24 | Governs HTTP semantics; not provider composition |
| GitHub Issues REST API | Official current provider documentation, get/update operations and response states inspected 2026-07-24 | Governs documented GitHub API surface; not local order or connector implementation |
| GitLab Issues API | Official current provider documentation, update and `state_event` close/reopen surface inspected 2026-07-24 | Governs documented GitLab API surface; not `glab` recovery composition |
| Microsoft Retry pattern | Official Azure Architecture Center guidance, idempotence and lost-response condition inspected 2026-07-24 | Credible practitioner guidance for transient external calls; not a tracker command owner |
| Microsoft Compensating Transaction pattern | Official Azure Architecture Center guidance, resumable progress, idempotence, compensation failure, and human-intervention conditions inspected 2026-07-24 | Credible distributed-workflow guidance; analogy is bounded and does not authorize compensation |
| Google Engineering Practices | Official Small CLs and review-standard pages inspected 2026-07-24 | Google's practitioner policy; not a universal standard or local tracker authority |
| Local tracker contracts | Exact current local/GitHub/GitLab files at `sha256:4c8c31836b0e6428e51eb8b169b9126b1f905ed4988d5cc116c766d8bbe51e36`, `sha256:d79c8dbdc0e3c77583b461ac2d50eb678d0ce77aed69a9e759e3c0818646f933`, and `sha256:b2306fc978d12a17658f30bf48a5e80e3f28407e1daa904d03298a0ba463e709` | Local intent authority for order, fields, read-back, release, relationships, and frontier; not professional method proof |

## Stopping basis and caller-use boundary

Decision saturation is reached. Every load-bearing corrected-order claim is
classified; Git, HTTP, both connector providers, distributed-recovery
counterpressure, current/upstream packages, and exact prior evidence identities
were inspected; provider-specific idempotence remains explicitly unverified;
and another bounded lane is unlikely to change the method, condition,
classification, or H1 admission.

Research status is `answered`. The packet supports a `research-complete`
Deploy decision. It may inform Prompt 2 admission and pre-registration only.
It does not modify corrected M0, decide exact runtime wording, treat upstream
usage as endorsement, prove candidate efficacy, alter tracker transport, or
authorize Prompt 2.

Authorized unit completed: Deploy Research Pass
Decision: research-complete
Campaign shape: unclassified; exact M0 runtime and H1 are not materialized
Runtime identities: current package inspected; corrected M0 checkpoint frozen at sha256:c56d01368a49d19ed33fb4d0c4b926029d6264885e36bea5af820f40c31d5f0c; exact M0 runtime and H1 unmaterialized
Artifacts changed: docs/research/implement-2026-07-24-r2.md
Evidence used or reused: fresh Git, HTTP, GitHub, GitLab, retry, compensation, and review evidence; exact-matching upstream/current observations; prior packet reclassified by lane as recorded; no candidate behavioral proof reused
Residual gaps: exact candidate wording and behavioral efficacy remain unproved; provider-composite retry idempotence is unverified; exact M0/H1 runtime identities remain for Prompt 2
Recommended next unit: Deploy Prompt 2
Git HEAD: 94d68e78d8812e9a2ceffd093e729402cac1cff2 -> 94d68e78d8812e9a2ceffd093e729402cac1cff2
Git delivery: pending
Exact stop reason: the R2 Research Pass produced its one authorized evidence packet, and the Shared Run Contract forbids starting Prompt 2.
