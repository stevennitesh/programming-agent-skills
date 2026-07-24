# Implement Research Pass — 2026-07-24

## Research lock

- **Question:** Which methods, vocabulary, conditions, alternatives, and
  counterpressure best support the frozen `implement` M0 contract?
- **Caller use:** decision-ready evidence for Deploy Prompt 2; this note does
  not alter M0, design H1 wording, prove behavioral efficacy, or authorize a
  successor.
- **Fixed point:** Git `HEAD`
  `94d68e78d8812e9a2ceffd093e729402cac1cff2`; M0 marker-bounded payload
  `sha256:ff4ea3bc80cc12820d1debe8142d26832a0449d392ec843439118157902affbc`.
- **Freshness:** online sources checked 2026-07-24; local and upstream
  repositories are identified below at their inspected revisions.
- **Write authority:** create only
  `docs/research/implement-2026-07-24.md`.
- **Return owner:** Deploy Campaign coordinator.

## Blind independent discovery

This section was recorded before opening any upstream package, the current
canonical `implement` package, target synthesis, or historical candidate
conclusion.

Search began from M0's intended behavior, using these independent lanes:

- readiness and transparent completion: official Scrum Guide and Agile
  Manifesto principles;
- bounded change, review, and review/repair counterpressure: Google Engineering
  Practices and Google Research;
- batch size and delivery outcomes: DORA research;
- proof selection and security-sensitive assurance: NIST SSDF;
- test-first effectiveness and limits: systematic reviews and meta-analyses of
  TDD;
- reviewed-byte and delivery identity: Git documentation and GitHub protected
  branch documentation.

The blind search produced these provisional findings for later verification:

1. A formal, shared completion state prevents incomplete work from being
   represented as done, but a heavyweight Charter is not independently
   justified for every tiny change.
2. One self-contained change with related proof is a strong professional
   default. Smallness is conceptual, not a line-count rule; decomposition can
   become harmful when a slice cannot work or be understood independently.
3. Review should evaluate a coherent exact change and should converge when the
   change improves code health, not pursue perfection. Changes after approval
   create stale-review risk.
4. Proof should be selected by risk and by the behavior a lower-level check
   cannot cover. TDD evidence is mixed by context and productivity outcome, so
   test-first is a conditional technique rather than a universal entry gate.
5. Git and protected-branch mechanics can establish snapshot and approval
   identity, but do not themselves settle local authorization, tracker
   semantics, or whether push belongs to completion.

Blind counterpressure retained for targeted inspection:

- readiness checklists can become ceremony when intent is already settled;
- small batches can fragment an inseparable change or hide whole-system risk;
- repeated review/repair can expand scope and delay useful improvement;
- focused tests can miss integration and state-boundary failures, while broad
  suites can add cost without claim-matched confidence;
- a local commit can be a complete repository result even when external push is
  neither required nor authorized.

Rejected discovery lanes: popularity lists, course material, generic “best
practice” posts, search snippets as evidence, and upstream-skill repetition.
They do not own the professional claims needed here.

## Answer

The M0 contract is professionally supportable without adding a heavyweight
universal implementation ceremony. The strongest method is a **bounded,
self-contained change under an explicit completion contract**: reconcile the
selected outcome and acceptance, establish the exact repository state, make
the smallest coherent observable change, choose proof by behavior and risk,
review one immutable snapshot, accept only bounded requirement-preserving
repair, and prove that the committed and externally recorded state is the state
actually accepted.

Three qualifications are load-bearing:

1. “Small” means independently understandable, usable, and testable—not few
   lines or few files.
2. Test-first is a conditional inner-loop technique. Evidence supports
   fine-grained, steady feedback more consistently than it supports mandatory
   test-before-code sequencing.
3. Neither a fixed repair count nor push-as-completion has general
   professional authority. Repair limits must be local/risk-owned, and push
   remains subject to the settled delivery and authorization boundary.

No evidence requires reopening M0. Research narrows candidate additions and
rejects several tempting upstream mechanics.

## Classified claims and method support

| Method or claim | Research status | Method support | Evidence, applicability, counterpressure, and H1 consequence |
| --- | --- | --- | --- |
| Use a shared, checkable completion state; do not represent an incomplete increment as done. | `supported` | `independently-supported` | The current official [Scrum Guide](https://scrumguides.org/scrum-guide.html) defines Done as the state meeting product quality measures and says work that does not meet it is not part of an Increment. The [Agile Manifesto principles](https://agilemanifesto.org/principles) treat working software as the primary progress measure. These sources do not prescribe M0's exact completion packet. H1 may sharpen truthful completion, but the packet schema remains local intent. |
| Reconcile intent and acceptance before changing technique; concrete examples help expose ambiguity. | `supported` | `independently-supported` for shared behavior examples; `pack-specific` for an exact Charter schema | [Cucumber's BDD documentation](https://cucumber.io/docs/bdd/) centers shared understanding on concrete real-world examples and rapid small iterations; its [examples guidance](https://cucumber.io/docs/bdd/examples/) says useful examples are concrete and technology-independent. The Scrum Guide supplies a formal completion commitment. Neither source supports every current Charter field or mandatory ceremony for trivial work. Preserve M0's locally owned Charter content; express it proportionately. |
| Work in one small, coherent, independently provable change. | `supported` | `independently-supported` | DORA's current [Working in small batches](https://dora.dev/capabilities/working-in-small-batches/) page (updated 2025-12-08, linked to the corrected 2025 report) connects small batches to faster feedback and requires independent, valuable, testable work. Google's [Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html) defines a small CL as one self-contained change including related tests and says size is contextual. Decomposition that leaves the system unusable or the change unintelligible fails both sources. Admit “self-contained small batch” as supporting vocabulary, not a line-count gate. |
| Prove one narrow observable path, then cover distinct acceptance and state boundaries. | `supported` | `independently-supported` as incremental feedback and claim-matched coverage; exact “tracer bullet” wording remains `unverified` | DORA supports independently testable batches and rapid feedback. Cucumber supports concrete observable examples. The official [ISTQB CTFL 4.0.1 syllabus](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf) owns decision-table and state-transition techniques for conditional/stateful behavior. These sources do not require exhaustive matrices for stateless work. H1 may recruit “one observable path” and conditional state-boundary expansion; do not claim independent support for the tracer-bullet label itself. |
| Select review and testing methods by risk, lifecycle stage, behavior, and the confidence each seam adds. | `supported` | `independently-supported` | NIST [SP 800-218 SSDF 1.1](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=934124), PW.7–PW.8, directs organizations to choose review/testing methods by stage, scope tests, record results, include production-relevant infrastructure, and use stronger methods for high-risk scenarios. The practitioner [Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html) argues for the lowest seam that supplies confidence and a higher seam only for behavior lower levels cannot cover. These sources counter both “focused tests alone prove delivery” and “always run every possible suite.” Preserve M0's proportionate, claim-matched proof. |
| Make TDD mandatory for every feature, bug fix, refactor, and behavior change. | `conflicted` | `contested` | Superpowers instructs universal test-first except user-approved exceptions, but the 2013 [TDD meta-analysis](https://doi.org/10.1109/TSE.2012.28) reports only a small average quality effect and little overall productivity effect with setting moderators. A 12-experiment [family study](https://arxiv.org/abs/2011.11942) found novices slightly better under iterative test-last and strong task/context dependence. A process [dissection study](https://arxiv.org/abs/1611.05994) associated quality/productivity with fine granularity and uniformity, not sequencing. These studies are bounded laboratory/industrial samples, not proof against all TDD. Reject universal TDD; preserve M0's conditional TDD/diagnosis/direct-evidence routing. |
| Keep implementation and refactoring distinct; simplify through small behavior-preserving changes while proof stays green. | `supported` | `independently-supported` | Fowler's [Refactoring](https://martinfowler.com/books/refactoring.html) defines refactoring as small behavior-preserving transformations, and [Workflows of Refactoring](https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html) separates adding function from refactoring on a green base while warning against cleanup that grows too long. This supports M0's simplify-and-reprove unit. It does not support unrelated cleanup or Ponytail's exact ladder. |
| Review one coherent snapshot; later behavior-affecting change makes prior acceptance stale. | `supported` | `independently-supported` | Google's 2018 [Modern Code Review case study](https://research.google/pubs/modern-code-review-a-case-study-at-google/) inspected 9 million changes and records review as a lightweight quality/knowledge/conformance practice. Google's [review standard](https://google.github.io/eng-practices/review/reviewer/standard.html) favors approval once a change definitely improves code health rather than pursuing perfection. GitHub's current [protected-branch documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) explicitly models approvals as attached to a diff and supports dismissal/reapproval after later pushes. The evidence supports fresh successor review after repair, but not a universal number of repair generations. |
| Default every repair loop to exactly two generations. | `unknown` | `unverified` | No inspected professional or empirical source establishes two as a general optimum. Google recommends forward progress and escalation for unresolved conflict; GitHub supplies freshness controls, not a retry count. The current target's number is an observed local policy only. Do not admit “two” as research-backed H1 behavior; Prompt 2 may preserve it solely as an explicit local choice or replace it with a caller/repository-owned bound. |
| Prove the commit contains exactly the accepted staged tree and excludes unrelated work. | `supported` | `independently-supported` for Git identity; local policy owns what may be staged | The Git [user manual](https://git-scm.com/docs/user-manual.html#the-index) states that the index uniquely determines a tree and `git commit` uses that tree in the commit. GitHub's protected-branch rules provide independent operational counterpressure against unreviewed latest pushes. This supports exact tree comparison and intentional staging. It does not prove acceptance or authorize a commit; those remain local. |
| After an ambiguous or partial external mutation, inspect current state before retry and report partial application truthfully. | `supported` | `independently-supported` | [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2) says a client should not automatically retry a non-idempotent request without known idempotence or evidence the original was not applied, and specifically describes revision inspection/recovery for version-control clients. GitHub's current [Issues REST API](https://docs.github.com/en/rest/issues/issues) exposes separate get/update operations and update failure states. Exact tracker recovery remains provider-owned. Preserve M0's Mutation read-back and partial-state Return. |
| Push or deploy is inherently part of single-item implementation completion. | `conflicted` | `contested` by applicability | DORA's delivery model treats deployment and user feedback as the completion of a small delivery batch, while Git and review sources distinguish a local commit from remote integration. Neither source grants external-write authority. M0 explicitly makes push conditional on separate authority and verification; local intent controls. Reject unconditional push and retain an explicit external-delivery state. |
| Use Ponytail's full “first rung that holds” ladder and one-check minimum. | `unknown` | `pack-specific` | Ponytail directly instructs codebase reuse, standard-library/native options, minimum working code, whole-flow comprehension, safety exceptions, and one runnable check for nontrivial logic. Its preserved benchmark reports bounded Haiku 4.5 tasks, deterministic safety gates, and explicit contamination correction, but cannot establish production readiness or general comparative efficacy. Independently supported pieces—simplicity, small changes, behavior preservation, and safety boundaries—already have stronger owners. Keep the exact ladder out of H1 unless registered as a local experiment with comparative proof. |

## Upstream and current observations

These are observations of package behavior, not professional endorsements.

### Matt Pocock

- Repository revision `ed37663cc5fbef691ddfecd080dff42f7e7e350d`;
  clean worktree.
- Complete target package inspected:
  `skills/engineering/implement/SKILL.md`
  (`sha256:30cd7bc1ebfb3891e85a1eed3b3b81aea0fa4ad4553a784de7f8e421b2d223e0`)
  and `agents/openai.yaml`
  (`sha256:8494f83602c58f8ab33d047d0516cdb90b8c29e6d564de0cef810daaca378bcb`).
- Observed: explicit-only invocation; implement a spec/ticket; use TDD where
  possible at pre-agreed seams; typecheck and focused-test regularly; run the
  full suite at the end; review; commit.
- Limit: the package is extremely compact and supplies no admission, failure,
  repair, identity, tracker, or external-delivery mechanics. Its repeated-test
  and end-suite schedule is pack behavior, not a universally supported proof
  budget.

### Superpowers

- Repository revision `d884ae04edebef577e82ff7c4e143debd0bbec99`;
  clean worktree.
- Relevant implementation cluster inspected completely:
  `executing-plans/SKILL.md`
  (`sha256:bbd8d28bb655a52817cc129ce49f9e46fa7c6303f72ed5de95bfe914ef8e0ce8`),
  `verification-before-completion/SKILL.md`
  (`sha256:ea52d15aabaf72bc6b558efe2c126f161b53961090ddcd712000273bfe8c7b6c`),
  requesting-review skill and reviewer template
  (`sha256:1017ccdd5bc61fab67c654cf118cbdb520464b313073a0a6b9a6b9aa647a3ad6`,
  `sha256:b2f2ec7596925fe52dac158fdfbca19b3a7d779d619c481e6706a6c0001662d3`),
  receiving-review skill
  (`sha256:647036bbdab7bf2317e14e079595e984c9030f64295e2b4c0fb57dbeb48f25dd`),
  finishing-branch skill
  (`sha256:e6d4a812de900d33c6eacfb40747f99427f25c304a7b7099120f9373b115a47f`),
  and TDD skill/reference
  (`sha256:b5b4717b8b761cce15a6cfe9022e33fd959e0894c0c39d72c9cb49c23486c10e`,
  `sha256:bde453bc258f06543987477c837939afaa774ea2acbd9f308d702fc452bc4283`).
- Observed: critically review a plan; stop for blockers; require fresh full
  verification before completion claims; review early/often; verify feedback
  technically; test each repair; offer explicit branch-finishing choices; and
  require universal TDD with narrow exceptions.
- Limits: this is a composition of several skills, frequently assumes human
  choice or subagents, and neither its universal TDD rule nor per-task review
  frequency transfers automatically to one local `implement` owner.

### Ponytail

- Repository revision `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`;
  clean worktree.
- Relevant files inspected completely: `skills/ponytail/SKILL.md`
  (`sha256:46a57e26a2632e7fa40eae6a3cf3011ccdc4d8db19d8f8617907d6b5deef055e`),
  `skills/ponytail-review/SKILL.md`
  (`sha256:40df33b58fc6ef889b93585733feb9566b76e9586efa7f376785c1e995197ac0`),
  and the agentic benchmark README
  (`sha256:bcd5dfea01aa15b03587de47699ff0ef9dadd49cef661896154cec308d5d542b`).
- Observed: trace the real flow before simplifying; prefer reuse, standard
  library, native capability, and the minimum working change; fix shared root
  causes; retain security/error/accessibility boundaries; leave one runnable
  check for nontrivial logic; review for deletable complexity.
- Limits: Ponytail is an always-active coding style rather than a
  single-item delivery owner. Its benchmark is package-owned, model/task
  bounded, and explicitly not production-readiness evidence.

### Current canonical target

- Complete package inspected:
  `skills/custom/implement/SKILL.md`
  (`sha256:7a8b391a92609e08e1b8f70526981381ddb9336c218aed8d3c28cc4fdb618b65`)
  and `agents/openai.yaml`
  (`sha256:d1331038252c7012dceebe0627884e12bb2a9975263b974bf9a991168d6dc3b8`).
- It already owns selection, a Charter, conditional TDD/diagnosis, focused
  proof, immutable review, bounded repair, Lock, one commit, tracker closeout,
  and a typed Return. It also contains an explicit staged-worker mode, a
  default two-generation repair budget, and different local-versus-connector
  closeout ordering.
- M0 is not the current runtime: M0 removes staged-worker delivery from the
  minimum, adds fuller readiness/authority/state reconciliation, explicitly
  explores technique and proves a narrow path before expansion, requires
  tracker closeout after verified commit, and retains separately authorized
  push verification. Exact M0 runtime bytes and H1 do not yet exist, so the
  formal campaign identity shape remains unclassified until Prompt 2.
- Current behavior is compatibility evidence only. The staged-worker branch,
  numeric repair default, and pre-commit local tracker closeout are not
  protected merely because they exist.

### Historical local source intake

The complete implement research map
(`sha256:53ac14ae93c61b12fab9e0aebb37c309bd7b407b76f0f323b253554bb321462e`)
and search vocabulary
(`sha256:f37886f04988ee2f95c787588264be9e04f3e4feb30a4c08552be147980165c3`)
were inspected after blind discovery. They supplied facet coverage and search
terms only. Their prior target-shape statements are
`historical-admission-only`, not current control, candidate proof, or intent
authority. No historical behavioral result was reused.

## Intent-adjacent candidates

| Candidate | Mapping: term → recruited behavior → expected M0 weakness → observable gate → comparative proof | Admission |
| --- | --- | --- |
| **Self-contained small batch** | term → hold one independently understandable and testable change → “bounded slice” may be read as merely few files → every changed concern maps to one acceptance/proof story and the result works at each committed boundary → M0 versus H1 fixtures with tempting horizontal fragments and broad multi-feature changes | Admit as `independently-supported` vocabulary candidate; preserve M0 scope. |
| **Evidence before claims** | term → identify and run the evidence that entails each completion assertion → a generic proof list may invite extrapolation from one green check → every positive Return claim cites fresh matching evidence or is downgraded → M0 versus H1 completion samples with focused-only, stale, skipped, and full claim-matched evidence | Admit as an intent-adjacent hypothesis; phrase proportionately rather than importing Superpowers' absolute rhetoric. |
| **Latest accepted tree** | term → bind review, repair, staging, commit, and closeout to one current identity → review may be treated as durable after later edits → any behavior-affecting delta invalidates acceptance and requires successor review → exact-tree structural checks plus behavior samples containing post-review drift | Admit; independently supported and directly aligned with M0 U10–U14. |
| **Reconcile before retry** | term → inspect external current state after ambiguous mutation → an agent may blindly replay a failed tracker operation → applied/failed/unknown effects are read back and only safe idempotent recovery proceeds → provider fixtures injecting timeout before/after application | Admit; independently supported, while provider transport remains owned elsewhere. |
| **Green simplification** | term → simplify only as small behavior-preserving changes under current proof → M0 “simplify and reconcile” may invite adjacent cleanup → authored complexity shrinks without acceptance, scope, or evidence delta → M0 versus H1 samples with attractive unrelated cleanup and proof-invalidating refactors | Admit as independently supported vocabulary candidate. |
| **Two repair generations** | term → stop after a fixed count → open-ended review could loop → generation counter stops at two → comparative review simulations across risk profiles | Do not admit from research; `unverified` and exact count is locally owned. |
| **Universal test-first** | term → always create RED before code → direct implementation may skip a useful causal check → every change deletes/restarts when RED was not first → comparative tasks by novelty, legacy state, configuration, generated artifacts, and testability | Reject as `contested`; preserve conditional inner-owner routing and fine-grained feedback. |
| **Ponytail ladder** | term → stop at first minimal solution rung → implementation may overbuild → dependency/files/LOC fall without safety or completeness loss → fresh multi-model controls with deterministic safety/completeness gates | Defer as a clearly labeled `pack-specific` local experiment; M0 already owns simplification without importing the whole style. |

## Conflicts, gaps, and rejected lanes

- **Repair count:** no source justifies two generations as a general
  risk-scaled bound. This is not an evidence gap for M0 because M0 only
  requires a recorded bound; it is a disclosed H1 disposition.
- **Push completion:** delivery research often assumes deployment, while the
  local contract deliberately distinguishes commit from authorized external
  delivery. Keep the conflict visible; local authority wins.
- **Review efficacy:** Google's case study is very large but single-company and
  exploratory. It supports review motives and workflow, not a universal defect
  removal rate or proof that one reviewer/model is sufficient.
- **TDD:** evidence varies by study design, participant experience, task, and
  comparator. It supports neither “never TDD” nor “always TDD.”
- **Agent-specific efficacy:** Ponytail's benchmark is useful pack-specific
  admission evidence, but no inspected external study proves these exact
  runtime terms improve Codex behavior. Prompt 4 owns candidate proof.
- **Practitioner conversation:** none was needed; published evidence resolved
  the material method conditions. No conversation was simulated.
- **Rejected for H1:** full-suite-on-every-item as a universal rule,
  review-after-every-subtask, fixed two-generation repair as professional
  doctrine, unconditional push/deploy, the complete Ponytail ladder, and any
  source's provider-specific Git/tracker procedure copied into `implement`.

## Source identity and authority registry

| Source | Identity/access | Authority and limit |
| --- | --- | --- |
| Scrum Guide | Official HTML, current November 2020 edition, checked 2026-07-24 | Governs Scrum's Definition of Done; not this repository's completion schema. |
| Agile Manifesto principles | Original signatory site, complete principles page, checked 2026-07-24 | Original values/principles; deliberately non-procedural. |
| DORA small-batch capability and 2025 report errata | Google DORA pages, capability updated 2025-12-08; report latest identified as v2025.2, checked 2026-07-24 | Research program's capability synthesis and current correction identity; organizational survey evidence does not prove exact agent wording. |
| Google Engineering Practices | Complete cited Small CLs and review-standard pages, checked 2026-07-24 | Google's practitioner policy; strong operational evidence, not a universal standard. |
| Google modern code-review study | ICSE SEIP 2018 abstract/identity page; methods and population visible, checked 2026-07-24 | Primary empirical case study at Google; single-organization/exploratory limit. |
| NIST SP 800-218 SSDF 1.1 | Official 2022 PDF, PW.7–PW.8 inspected, checked 2026-07-24 | Governing secure-development recommendation; directly applicable to security-sensitive proof, not every low-risk change. |
| TDD studies | IEEE meta-analysis DOI/abstract; 2020 family-of-12-experiments manuscript; 2016 process dissection manuscript, checked 2026-07-24 | Primary/aggregate empirical evidence with heterogeneous tasks and populations; supports a contested classification, not a universal prohibition. |
| Git user manual | Current official manual, index section inspected, checked 2026-07-24 | Governs Git object/index/commit identity mechanics only. |
| GitHub protected branches and Issues API | Current official provider documentation, checked 2026-07-24 | Governs GitHub behavior at the documented API/version surface; other trackers require their own owner. |
| RFC 9110 | Internet Standard, §9.2.2 inspected, checked 2026-07-24 | Governs HTTP retry semantics; supports reconciliation principle, not tracker-specific commands. |
| Cucumber BDD/examples | Current official practitioner documentation, checked 2026-07-24 | Owns Cucumber's BDD method; examples are not automatically executable acceptance tests. |
| ISTQB CTFL 4.0.1 | Official syllabus PDF, decision-table/state-transition sections identified, checked 2026-07-24 | Professional testing syllabus; techniques are conditional, not mandatory exhaustive tables. |
| Fowler refactoring sources | Author's official book/workflow pages, checked 2026-07-24 | Original practitioner account of refactoring mechanics; not empirical effect-size evidence. |

## Stopping basis and caller-use boundary

Decision saturation is reached. Every load-bearing method is classified; the
strongest applicable governing, primary empirical, official technical, and
credible practitioner owners were inspected; upstream mechanics received
targeted independent corroboration or counterpressure; source identities and
access limits are recorded; and another bounded lane is unlikely to change an
admitted method, condition, or rejected hypothesis.

This packet is `answered` for Research's bounded question and supports a
`research-complete` Deploy decision. It may inform Prompt 2 admission and
pre-registration only. It does not change the frozen intent, select exact H1
wording, validate M0/H1 behavior, preserve current behavior by existence,
alter tracker policy, mutate runtime, or authorize Prompt 2.

Authorized unit completed: Deploy Research Pass
Decision: research-complete
Campaign shape: unclassified; exact M0 runtime and H1 are not materialized
Runtime identities: current inspected; exact M0 runtime and H1 unmaterialized; exact pre-evaluation identity relationship unavailable
Artifacts changed: docs/research/implement-2026-07-24.md
Evidence used or reused: fresh independent sources and verified upstream/current observations listed above; local implement map was historical-admission-only; no prior candidate proof reused
Residual gaps: exact candidate wording and behavioral efficacy remain unproved; the numeric repair bound lacks independent support; exact M0/H1 runtime identities remain for Prompt 2
Recommended next unit: Deploy Prompt 2
Git HEAD: 94d68e78d8812e9a2ceffd093e729402cac1cff2 -> 94d68e78d8812e9a2ceffd093e729402cac1cff2
Git delivery: pending
Exact stop reason: the Research Pass produced its one authorized evidence packet, and the Shared Run Contract forbids starting Prompt 2.
