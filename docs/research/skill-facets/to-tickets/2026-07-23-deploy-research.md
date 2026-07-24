# To Tickets Deploy Research Pass

- Date and freshness check: 2026-07-23
- M0 checkpoint: `docs/validation/transcripts/2026-07-23-to-tickets-prompt1-m0.md`
- M0 payload fingerprint: `sha256:c4238c81fa861543f492de8db11e5111c8517e4fa071aaf6628b286b2ad90a2f`
- Research status: answered
- Note authority: create exactly this file
- Return owner: fresh Deploy Campaign coordinator

## Locked Research Contract

**Question:** Which methods, vocabulary, conditions, and alternatives best
support `to-tickets`' settled intended behavior: converting one settled source
packet into an exhaustive, dependency-ordered set of bounded,
Ready-for-agent implementation tickets, publishing the graph safely, and
returning one authorized downstream recommendation without starting it?

**Caller use:** a decision-ready Research Pass packet for Deploy Prompt 2. The
caller, not Research, owns H1 design, campaign state, and the next transition.

**Scope:** the six intended-behavior facets frozen in M0: slice boundaries and
coverage; dependencies and ordering; fresh-session ticket quality; execution
profiles and state matrices; mutation safety; and completion/downstream route.
The applicable fixed point is the supplied 2026-07-23 M0 checkpoint at Git
`dd3cfa647190e94e40b1e213d8b8cf7e1762a3c6`. Independent sources were checked
live on 2026-07-23; repository observations use their recorded revisions.

**Exclusions:** no change to M0, synthesis, runtime, relationships, evaluation,
installation, tests, or Git state; no behavioral-effectiveness claim about
exact skill wording; no H1 decision; no tracker mutation; no practitioner
conversation.

## Blind Independent Discovery Record

This section was written before opening `.tmp/mattpocock-skills`,
`.tmp/superpowers`, `.tmp/ponytail`, the current
`skills/custom/to-tickets` package, its synthesis, or historical candidate
conclusions.

Discovery queries covered:

- vertical/value slices, INVEST, backlog refinement, and readiness;
- complete work decomposition, predecessor/successor logic, cycles, dangling
  activities, and resource constraints;
- human and AI-agent issue-report information needs;
- acceptance criteria, examples, decision tables, and state-transition models;
- parallel software changes, merge-conflict indicators, shared resources, and
  semantic conflicts; and
- non-idempotent mutation retries, partial API results, read-back, and
  desired/current-state reconciliation.

The strongest blind lanes queued for exact extraction were:

1. GAO scheduling and work-breakdown guidance for completeness, network logic,
   cycles, dangling nodes, and scarce resources.
2. The Scrum Guide plus Agile Alliance/Cucumber practitioner evidence for
   small valuable slices, refinement, observable acceptance, and the
   counterpressure against rigid or exhaustive pre-work specification.
3. Peer-reviewed studies of human bug reports, software-issue conversations,
   and the 2026 preprint on bug reports for repair agents for focused,
   executable, localized context and its limits.
4. ISTQB decision-table and state-transition techniques for systematic branch
   coverage, including minimization and combinatorial-cost counterpressure.
5. Empirical merge-conflict work for parallel-risk indicators and the
   counterfinding that simple shared-file/change-size heuristics are not
   sufficient.
6. RFC 9110, GitHub API documentation, and Kubernetes reconciliation semantics
   for ambiguous non-idempotent outcomes, partial results, and post-mutation
   convergence.

Blind counterpressure found before package inspection:

- the official Scrum Guide makes backlog attributes domain-dependent and
  leaves delivery decomposition to Developers; a universal heavyweight
  Ready checklist would exceed that source;
- Scrum.org practitioner material warns that a Definition of Ready can become
  gatekeeping or analysis paralysis;
- ISTQB warns that complete decision tables grow exponentially and permits
  minimization or risk-based reduction;
- an empirical merge-conflict study rejected both shared-file count and change
  size as sufficient conflict predictors; and
- RFC 9110 forbids guessing that a non-idempotent request is safe to retry:
  the client needs idempotency knowledge or evidence that the first operation
  was not applied.

This recorded blind-search boundary is sealed. Subsequent package observations
cannot be presented as independent discovery.

## Answer

The settled behavior is best supported by a **coverage ledger plus a typed work
graph**, not by ticket count or a generic story template. The ledger must
dispose every source commitment; the graph must make product slices,
necessary support or migration stages, dependencies, shared-resource risks,
and observable proof explicit. A fresh-session ticket should be concise and
focused but carry enough context to execute and verify its own outcome.
Conditional or stateful work benefits from decision/state tables, while
compatibility-sensitive changes benefit from a staged expand-migrate-contract
sequence.

The evidence also narrows this answer. "Ready" is not a demand for complete
up-front design, every possible example, or a universal checklist. File
overlap is not proof of merge safety or conflict. Independent tickets are not
automatically safe to execute concurrently. A non-idempotent tracker write
must not be retried blindly after an ambiguous result.

No inspected evidence shows that M0 omitted behavior essential to its settled
intent. Exact field names, approval protocol, proposal-revision mechanism, and
return schema remain local contract choices rather than externally proven
universal methods. Their status does not create an evidence gap because M0,
not Research, owns those settled requirements.

## Load-Bearing Claims

| Claim | Research classification | Owning evidence and applicability | Counterevidence, inference, and answer impact |
|---|---|---|---|
| Complete decomposition needs an explicit completeness rule and traceable disposition of parent work. | `supported` | The GAO Cost Estimating and Assessment Guide applies the 100-percent rule to work-breakdown structures: child elements account for all parent scope. The [GAO guide](https://www.gao.gov/assets/a77186.html) is governing U.S. federal project-estimation guidance, inspected 2026-07-23. M0 independently requires every commitment to map to a ticket or explicit disposition. | Applying a project WBS rule to software-ticket commitments is a labeled inference. The transfer supports a ledger/audit, not a mandated hierarchy or ticket granularity. |
| Ordering needs explicit predecessor/successor logic, cycle and dangling-node checks, and attention to scarce shared resources. | `supported` | The [GAO Schedule Assessment Guide, GAO-16-89G](https://www.gao.gov/assets/690/687052.pdf) requires complete activities, logical sequencing, predecessor/successor links, and checks for circular logic and dangling activities; it also treats resources as schedule constraints. Applicable as a mature graph-audit method, not as a demand for federal scheduling machinery. | Product dependencies and resource contention are different relations. The evidence supports checking both, not collapsing them or importing critical-path estimates into tickets. |
| Backlog work can be refined into smaller precise, finishable items, but readiness attributes and decomposition remain context-dependent. | `supported` | The November 2020 [Scrum Guide](https://scrumguides.org/scrum-guide.html) describes an emergent ordered Product Backlog, refinement into smaller and more precise items, readiness for selection when work can be completed within a Sprint, domain-varying attributes, and Developers' responsibility for decomposition. | Scrum.org practitioner counterpressure warns that a Definition of Ready can become gatekeeping or analysis paralysis: [DoR versus DoD](https://www.scrum.org/resources/blog/what-difference-between-definition-done-dod-and-definition-ready-dor) and [waiting for perfect information](https://www.scrum.org/resources/blog/definition-ready-analysis-paralysis-waiting-perfect-information). Therefore M0's Ready packet should be treated as a minimum executable contract, not universal full specification. |
| Observable behavior and concrete examples improve acceptance clarity; systematic tables help conditional/stateful work. | `supported` | Cucumber's practitioner guidance distinguishes rules from concrete context-action-outcome examples in [Better requirements by harnessing the power of examples](https://cucumber.io/blog/bdd/better-requirements-by-harnessing-the-power-of-exa/). The official [ISTQB CTFL 4.0.1 syllabus](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf) describes decision tables for combinations, gaps, and contradictions and state-transition models for states, events, guards, actions, and invalid transitions. | ISTQB also notes exponential table growth and permits minimization or risk-based selection. Use matrices when branching or lifecycle semantics warrant them, not as mandatory ceremony for stateless work. Examples clarify rules but are not identical to implementation test cases. |
| A useful agent ticket is focused and carries expected behavior, an executable reproducer or proof path, relevant source context, and localization cues. | `supported` with bounded applicability | Zimmermann et al.'s peer-reviewed study, [What Makes a Good Bug Report?](https://research.vu.nl/en/publications/what-makes-a-good-bug-report-2/), found reproduction steps, stack traces, and tests useful to developers. Khatib et al.'s 2026 preprint, [What Makes a Good Bug Report for an AI Agent?](https://arxiv.org/abs/2607.07593), reports observational and controlled evidence that fix suggestions, reproduction scripts, source/localization information, and expected behavior can improve repair resolution, while greater length can reduce it. Ehsani et al.'s peer-reviewed [study of ChatGPT in GitHub issue conversations](https://link.springer.com/article/10.1007/s10664-025-10745-8) associates specific, focused contextual prompts with more helpful responses and long or multi-question prompts with less helpfulness. | The AI-agent paper is a July 2026 preprint bounded to its SWE-bench populations, two controlled models, and tested mutations; the other studies concern human bug reports or ChatGPT conversations. They support information shape, not the exact M0 schema or universal causal gains. |
| Vertical behavior slices are a useful default, while necessary preparatory and compatibility work need their own observable, bounded stages. | `supported` with conditions | An Agile Alliance experience report, [A Tale of Slicing and Imagination](https://agilealliance.org/resources/experience-reports/a-tale-of-slicing-and-imagination/), reports end-to-end slices across technical layers delivering business value, with adoption friction. Fowler's [preparatory refactoring example](https://martinfowler.com/articles/preparatory-refactoring-example.html) and [refactoring workflow](https://martinfowler.com/articles/workflowsOfRefactoring/fallback.html) justify small behavior-preserving restructuring when its investment is recouped. Sato's [Parallel Change](https://martinfowler.com/bliki/ParallelChange.html) presents expand, migrate, and contract as separately releasable compatibility stages. | These are practitioner methods, not comparative trials. Preparatory work is justified only when it unlocks settled delivery and remains behavior-preserving; parallel change incurs temporary dual-form cost and must finish contraction. A migration stage need not masquerade as direct user value. |
| Dependency readiness, concurrent write safety, and shared proof/state resources are distinct properties. | `supported` for the distinction; exact profile fields are local | GAO separates network logic from resource constraints. Empirical merge research found that simple shared-file count and change size did not sufficiently predict conflicts: [Indicators for Merge Conflicts in the Wild](https://www.se.cs.uni-saarland.de/papers/conflict-prediction/). This supports checking semantic ownership and shared resources in addition to graph dependencies. | The exact M0 execution-profile fields are not independently validated as a universal schema. File overlap can be a conservative signal, but absence of overlap does not prove semantic safety and presence does not prove conflict. |
| Ambiguous non-idempotent publication outcomes require evidence before retry and post-write reconciliation. | `supported` for the safety rule; tracker mechanism is provider-specific | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) says clients should not automatically retry a non-idempotent request unless its semantics are known to be idempotent or there is evidence the original request was not applied. GitHub documents issue creation as a POST in its [Issues REST API](https://docs.github.com/en/rest/issues/issues), resource and secondary limits in [GraphQL limits](https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api), and explicit blocking relations in its [issue dependency API](https://docs.github.com/en/rest/issues/issue-dependencies). Kubernetes' [declarative API model](https://v1-35.docs.kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) provides the broader current-state/desired-state reconciliation pattern. | Kubernetes is an analogy, not tracker authority. GitHub documentation does not establish a general issue-create idempotency key. Therefore a provider-supported key may be used when available; otherwise preflight, a stable local publication identity, search/read-back, and explicit ambiguous-state return are safer than blind replay. Exact implementation belongs to H1. |

Every load-bearing claim is supported within the limits shown. No applicable
claim is `conflicted` or `unknown`; narrower counterevidence changes conditions
and method scope rather than defeating the answer.

## Method Classification And H1 Consequences

| Proposed method | Deploy classification | Conditions and alternatives | Consequence for H1 |
|---|---|---|---|
| Commitment ledger with explicit ticket/disposition coverage audit | `independently-supported` | Use for settled source commitments. A plain checklist can implement the method; a WBS hierarchy is optional. | Preserve M0's exhaustive coverage gate. Do not infer coverage from ticket count. |
| Vertical behavior slice with observable proof | `independently-supported` | Default for delivery work. Allow a bounded support or migration stage when it unlocks delivery and has independently observable completion. | Preserve slice-type distinctions and proof per slice; do not require every technical stage to claim direct user value. |
| Separate judgments for size, value, testability, dependency readiness, and parallel safety | `independently-supported` | INVEST/SMART-style practitioner vocabulary is useful but not a substitute for the individual checks. Bill Wake's original [INVEST and SMART tasks](https://xp123.com/invest-in-good-stories-and-smart-tasks/) emphasizes specificity, measurability, relevance, bounded size, and whether tasks add up to the story. | Keep the properties separate. "Independent" must not imply concurrently safe. |
| Typed dependency graph plus cycle, dangling, and resource audit | `independently-supported` | Distinguish consumes-an-outcome edges from shared-resource coordination. Tracker-native blocking links are optional transport. | Preserve blocker semantics and deterministic order; reject decorative dependencies. |
| Focused Ready packet with expected outcome, evidence path, and source/localization context | `independently-supported` with bounded transfer | Apply minimum sufficient context. Alternative is a conversation/refinement loop, but that is unavailable to a fresh autonomous session. | Preserve the core Ready information while resisting verbosity and full-specification creep. |
| Decision table or state-transition matrix | `independently-supported` | Apply only to material conditional/stateful behavior; minimize or select risk-relevant combinations when exhaustive enumeration explodes. | Preserve M0's conditional use, not a mandatory matrix on every ticket. |
| Execution profile that names semantic owner, write surface, proof resource, shared state, and tripwires | `pack-specific` as an exact schema; constituent distinction is independently supported | Alternative is a lighter resource/ownership annotation. Neither simple file lists nor dependency edges alone are adequate concurrency proof. | Retain the M0 profile because it operationalizes settled intent, but treat exact fields as a local experiment to test in Prompt 3 rather than professionally validated doctrine. |
| Preparatory support slice | `independently-supported` under an economic/necessity condition | Inline small setup in the consuming slice when it does not need separate proof or ordering; split only when it independently unlocks work. | Keep the necessity and observability tests; avoid coordination-only tickets. |
| Expand-migrate-contract for compatibility-sensitive work | `independently-supported` | Use when old and new forms must coexist or an atomic switch is unsafe. Direct replacement remains simpler when compatibility is unnecessary. | Preserve phase order, releasability, and explicit contraction. |
| Freeze and approve the whole proposal before publication | `pack-specific` | Collaborative backlog refinement is an alternative. Exact-revision approval is a local safety protocol, not independently proven as the single best workflow. | Preserve because M0 settled it; Prompt 3 should test stale-revision and mutation-before-approval failures. |
| Stable publication identity, preflight, read-back, and reconcile-before-retry | `independently-supported` as a safety pattern; exact tracker encoding is `unverified` | Prefer provider-native idempotency when documented. Otherwise use deterministic correlation plus read-back; on unresolved ambiguity, stop rather than guess. | H1 may choose a locally testable identity/reconciliation mechanism, clearly labeled provider-dependent. |
| One typed downstream recommendation and stop | `pack-specific` | This is repository routing policy, not a generally researched ticketing method. | Preserve as relationship authority; do not use external evidence to redesign it. |

## Blind-to-Pack Comparison

Blind discovery and later package inspection converged on complete
decomposition, graph logic, focused executable context, explicit proof,
conditional/state modeling, resource-aware concurrency, staged compatibility,
and mutation reconciliation. The comparison did **not** upgrade repeated pack
behavior into independent support.

### Matt Pocock pack

- Revision: `ed37663cc5fbef691ddfecd080dff42f7e7e350d`
- Worktree: clean
- Access depth: complete target skill, agent metadata, human-facing target
  documentation, and all three target tracker transports; not a fresh
  file-by-file review of the entire upstream repository
- Files inspected:
  `skills/engineering/to-tickets/SKILL.md`,
  `skills/engineering/to-tickets/agents/openai.yaml`,
  `docs/engineering/to-tickets.md`, and the local, GitHub, and GitLab tracker
  setup documents under `skills/engineering/setup`
- Observed pack behavior: explicit invocation; context exploration; tracer
  bullets and vertical slices; fresh-context-sized, verifiable tickets;
  prefactor-first support work; expand-contract exception; human quiz and
  approval; blocker-first publication; a simple issue template; avoidance of
  file/code prescription except when a prototype fixes it
- Limit: these are pack observations at the recorded revision. The checkout
  required per-command Git safe-directory allowance for read-only metadata;
  no Git configuration or worktree state changed.

### Superpowers pack

- Revision: `d884ae04edebef577e82ff7c4e143debd0bbec99`
- Worktree: clean
- Access depth: complete relevant planning/execution/subagent skills and their
  implementer and reviewer prompts; not a full unrelated-pack audit
- Files inspected: `skills/writing-plans/SKILL.md`, its plan-reviewer prompt,
  `skills/executing-plans/SKILL.md`,
  `skills/subagent-driven-development/SKILL.md`, its task-reviewer prompt, and
  its implementer prompt
- Observed pack behavior: smallest reviewed tasks with their own test cycle;
  setup/configuration/documentation folded into consuming delivery; split
  boundaries where one task can be accepted independently; exact task briefs;
  fresh context and file-backed handoffs; serial execution even for
  independently assigned tasks; per-task specification and quality review
- Limit: this pack often prescribes exact files and code in plans, which is an
  alternative artifact style rather than support for durable issue-ticket
  specificity.

### Ponytail pack

- Revision: `16f29800fd2681bdf24f3eb4ccffe38be3baec6b`
- Worktree: clean
- Access depth: all six canonical Ponytail skill bodies, root instructions,
  and repository-wide semantic search for ticket, plan, dependency, slicing,
  and related mechanics
- Files inspected: all `skills/ponytail*/SKILL.md` files and root `AGENTS.md`
- Observed pack behavior: understand and trace before change, ordered
  sufficiency/YAGNI, preservation of safety, and at least one runnable check
- Limit: no ticket-decomposition, dependency-graph, or publication skill was
  present. Absence is evidence only about this revision, not a contrary
  professional method.

### Current canonical target and local packets

- Repository fixed point: campaign starting HEAD
  `dd3cfa647190e94e40b1e213d8b8cf7e1762a3c6`
- Current package inspected completely:
  `skills/custom/to-tickets/SKILL.md` and `agents/openai.yaml`
- Observed current behavior: Trace, Map, Slice, Approve, Publish; complete
  coverage; vertical and necessary support/migration slices; blocker semantics;
  decision/state matrices; execution profiles; expand-migrate-contract;
  exact-proposal approval; reconcile-before-mutation/read-back; typed returns;
  and one downstream route
- Current synthesis inspected only after the blind boundary:
  `docs/synthesis/skills/to-tickets.md`. Its earlier C101-C103 results and
  package identity are historical admissions, not fresh evidence for this M0.
- Applicable local language packets inspected completely:
  `matt-pocock-skills-vocabulary.md`,
  `superpowers-skill-pack-vocabulary.md`,
  `ponytail-skill-pack-vocabulary.md`,
  `upper-bound-engineering-language.md`,
  `03-high-signal-steering-words.md`,
  `04-agentic-bridge-vocabulary.md`, and
  `validation/UBL-01-slicing-and-migration.md`
- Limit: local packets are historical source intake. UBL-01's source packet
  supports keeping tracer learning, vertical delivery, size, value,
  testability, dependency readiness, concurrency safety, and migration
  staging distinct, but it explicitly leaves behavioral transfer untested.

## Targeted Verification After Pack Inspection

Three mechanics newly salient after pack inspection received targeted
independent checks:

1. **Preparatory refactoring:** Fowler supports small, behavior-preserving
   restructuring when it makes the next feature easier and the investment is
   recouped. This verifies the conditional support-slice method, not an
   entitlement to split every refactor into a ticket.
2. **Expand-migrate-contract:** Parallel Change supports staged coexistence and
   releasable phases, but also exposes the cost of supporting two forms and the
   need to finish contraction. This verifies M0's compatibility condition and
   its ordering, not universal use.
3. **Specific task quality:** Wake's SMART task formulation supports specific,
   measurable, relevant, bounded tasks and explicitly asks whether tasks add
   up to the whole story. It does not establish the target's exact template or
   concurrency profile.

Targeted countersearch also confirmed that shared-file count and change size
are inadequate standalone merge-conflict predictors. No targeted result
required reopening intent.

## Intent-Adjacent Candidates

These candidates may inform H1 without changing M0:

- **Minimum-sufficient Ready check:** require each field because it closes an
  execution or proof ambiguity, and reject padding. Classification:
  `independently-supported` in principle; the exact threshold remains local.
- **Risk-triggered matrices:** require a state/decision matrix only when
  material branches, guards, lifecycle states, or invalid transitions exist;
  otherwise use direct criteria. Classification: `independently-supported`.
- **Publication correlation identity:** attach a deterministic campaign and
  ticket key that can be queried before retry after an ambiguous write.
  Classification: `unverified` as a tracker encoding and admissible only as a
  local Prompt 3 experiment; provider-native idempotency supersedes it.
- **Concurrency falsification:** treat the execution profile as a set of
  reasons two tickets might not be parallel-safe, never as proof from
  non-overlapping file lists. Classification: constituent method
  `independently-supported`, exact profile `pack-specific`.

None is an M0 omission essential to settled intent.

## Alternatives, Rejected Lanes, Conflicts, And Gaps

- A universal heavyweight Definition of Ready was rejected: official Scrum
  leaves attributes domain-dependent, and practitioner counterpressure shows
  gatekeeping and analysis-paralysis failure modes.
- Ticket count, equal sizing, or a hierarchy without a commitment ledger was
  rejected as completeness proof.
- Full combinatorial decision tables were rejected as a default; minimized or
  risk-based tables are the applicable alternative.
- Shared-file count, change size, or "no dependency edge" was rejected as
  concurrency proof.
- Blind automatic retry of issue creation was rejected. No inspected GitHub
  source established a general issue-create idempotency key.
- Treating upstream agreement as professional validation was rejected.
- A practitioner conversation was unnecessary: published evidence resolved
  the operational conditions material to H1.

There is no material unresolved evidence gap. Exact local wording, field
names, proposal revision representation, and tracker-specific correlation
mechanics remain appropriately testable design choices rather than research
unknowns.

## Source Identities And Authority

Strongest owners inspected were official method/specification sources (Scrum
Guide, GAO guides, ISTQB syllabus, RFC 9110, and GitHub/Kubernetes
documentation), original empirical studies (Zimmermann et al.; Ehsani et al.;
the merge-conflict study), and one explicitly labeled 2026 preprint (Khatib et
al.). Practitioner sources were used only for operational techniques and
counterpressure, with that authority limit preserved. Repository sources own
only observed pack/current behavior and local contracts.

All online sources were inspected on 2026-07-23. Upstream observations are
fixed to the revisions recorded above. The M0 payload identity is
`sha256:c4238c81fa861543f492de8db11e5111c8517e4fa071aaf6628b286b2ad90a2f`;
H1, V1, and P1 do not yet exist in this epoch.

## Stopping Basis

Decision saturation was reached. Every load-bearing claim has an inspected
claim-owning source, explicit applicability, and material counterpressure.
Blind discovery, three upstream comparisons, the complete current package,
applicable local packets, and targeted verification converged without an
essential-intent omission. Additional credible lanes would refine examples or
provider implementations but are unlikely to change a method classification,
condition, or H1 consequence.

## Caller-Use Boundary And Return

Campaign disposition: `research-complete`.

This note informs Deploy Prompt 2. It does not choose H1, change campaign
state, validate runtime behavior, authorize publication, or start a successor.
The ordinary unverified publication-identity idea is disclosed for local
testing and is not an evidence gap.

- Recommended successor: Deploy Prompt 2
- Tracked mutation authorized: this note only
- Return owner: fresh Deploy Campaign coordinator
- Next: none
