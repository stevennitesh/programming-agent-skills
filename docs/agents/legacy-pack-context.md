# Legacy pack context

Read this reference when maintaining the custom pack's composition, deployment,
review, or worker mechanisms. It preserves their vocabulary and ownership; it
is not a required workflow or composition contract for Astra development.
Paths written as code are repository-relative. Follow links for the relevant
method or decision rather than loading every referenced record.

The existing composition baseline and ADRs continue to explain their legacy
mechanisms. For Astra's accepted direction and differences in applicability,
read [the Astra design brief](../astra/design-brief.md).

## Pack vocabulary

**Skill pack**

A coordinated set of skills, setup contracts, validators, and reference that produces one engineering operating model.
_Avoid_: prompt collection, script bundle

**Fresh Composition Epoch**

A pack-wide epistemic reset in which prior research, synthesis, validation, and
change conclusions are historical intake until independently rediscovered or
explicitly revalidated. The active method lives in
[`fresh-composition-epoch.md`](../../docs/synthesis/methods/fresh-composition-epoch.md).
_Avoid_: clean slate, destructive reset, pack-wide change-control method

**Pack Composition Baseline**

The approved pack-level synthesis of selected capabilities, roles, ownership
boundaries, relationships, exclusions, collisions, gaps, and required
integration proof. It constrains one-skill work without copying its procedure.
_Compatibility alias_: Pack Composition Contract
_Avoid_: skill inventory, route list, change-control charter

**Evidence Catalog**

An index of reusable Evidence Records by the behavior or failure they address,
conditions, evidence class, freshness, limits, and source pointers. It supports
retrieval and never selects skill composition or behavior.
_Compatibility alias_: Research Catalog
_Avoid_: recommendation engine, synthesis index, source dump

**Evidence Record**

A reusable evidence unit describing one behavior or method, the failure it may
prevent, applicability, counterconditions, claim-owning evidence, freshness,
limits, and source pointers.
_Compatibility alias_: Research Card
_Avoid_: adopted behavior, H1 unit, source summary

**Active skill in the legacy pack**

A supported skill under `skills/custom/`; it is eligible for validation, routing, managed installation, and mirror comparison.
_Avoid_: custom variant, production experiment

**Experimental skill**

An inactive alternative under `skills/experimental/` that shadows one active skill name while its design is evaluated. It is preserved and hash-tracked, but never routed or installed until explicitly promoted into `skills/custom/`.
_Avoid_: active skill, installed skill, archive

**Target repo**

A repository configured to use the pack for shaping, implementation, triage, review, or maintenance.
_Avoid_: client repo, downstream repo

**Setup surface**

The legacy target-repo contract configured by the custom `$repo-bootstrap`: primer, commands, tracker configuration, label vocabulary, domain routing, engineering contract, and work-state policy.
Compatibility comes from the applicable configuration and owner checks, not one aggregate marker.
_Avoid_: generated docs, bootstrap output

**Agent primer**

The short repo `AGENTS.md` surface that points to commands and owning contracts before a skill acts.
_Avoid_: manual, full contract, router

**Engineering contract**

The target repo's source of engineering taste, shared runtime language, and convergence discipline.
_Avoid_: style guide, copied philosophy

**Local contract slice**

The part of a shared contract a skill must enforce because it directly governs that skill's work.
_Avoid_: duplicated contract

**Delegated implementation handoff**

Plain ticket-specific context sent by a delivery coordinator to one fresh
implementation worker. `$implement` owns its contents and return contract; it
is not a machine-validated execution protocol.
_Avoid_: capsule, assignment schema, planner transcript

**Implementation worker**

The delegated agent that implements one bounded handoff. The coordinator owns
acceptance and delivery; `$implement` owns the worker contract.
_Avoid_: delivery coordinator, change-control owner, reviewer

**Concurrent worker lane**

An isolated exact-base Git worktree for a writer that may overlap another
writer in time. The lane helper owns preparation and cleanup;
`$parallel-implement` owns scheduling and integration.
_Avoid_: worker runtime, scheduler, execution ledger

**Change review candidate**

A caller-selected implementation diff or PR. `$change-review` owns read-only
judgment of the identified content; its formal branch requires one fixed
candidate and returns the terminal decision.
_Avoid_: low-priority review, risk-free review

**High-assurance review candidate**

A fixed code candidate explicitly sent to `$high-assurance-review` for two
fresh whole-candidate reviews and one verified decision. Typical candidates are
an integrated ticket-graph result or an exact PR before merge; neither PR
presence nor risk implicitly selects the route.
_Avoid_: automatic escalation, every risky change

**Supported high-risk trigger**

A supported reachable scenario with concrete material impact. After review is
admitted, it may expand candidate-scoped coverage; it never activates review.
The reviewing skill applies it only to reachable behavior inside the accepted
request and repository contracts.
_Avoid_: hypothetical edge case, risk label, PR route

**Router skill**

An explicit-only skill that returns one next route and leaves downstream work unstarted.
_Avoid_: dispatcher, automatic router

**Skill Change-Control Method**

The controllerless one-skill authoring method owned by
[`deploy-prompts.md`](../../docs/synthesis/methods/deploy-prompts.md). Its ordered
reasoning and proof obligations are not persisted semantic lifecycle state.
_Compatibility aliases_: Deploy Campaign; Contract Lock; Candidate Lock;
Behavioral Proof; Release (for this method stage only)
_Avoid_: mega-prompt, self-chaining prompt, pack-wide method

**Legacy global AGENTS template**

The complete template seeds a missing global `AGENTS.md`; later installs update
only the pack-owned bootstrap section without replacing delegation or personal
rules.
_Avoid_: pack manual, copied route map

## Vocabulary owners

- Fresh Composition Epoch, Pack Composition Baseline, Evidence Catalog, and
  Evidence Record vocabulary belongs to this context and
  [ADR-0014](../../docs/adr/0014-source-native-vocabulary-names-active-pack-concepts.md).
  [ADR-0009](../../docs/adr/0009-fresh-composition-epochs-revalidate-skill-pack-knowledge.md)
  remains the Fresh Composition Epoch decision. The accepted
  `docs/synthesis/skill-pack.md` payload is the current Pack Composition
  Baseline owner.
- Skill Change-Control Method proof-obligation vocabulary belongs to
  [`deploy-prompts.md`](../../docs/synthesis/methods/deploy-prompts.md) and
  [ADR-0014](../../docs/adr/0014-source-native-vocabulary-names-active-pack-concepts.md).
  [ADR-0010](../../docs/adr/0010-deploy-campaigns-advance-through-proof-gates.md)
  remains the controllerless proof-ordering decision.
- Change review candidate, High-assurance review candidate, and Supported
  high-risk trigger belong to this context and
  [ADR-0016](../../docs/adr/0016-ordinary-and-formal-review-share-one-lean-judgment-owner.md).
  The caller owns activation, each review skill validates its admitted
  candidate, and risk expands only applicable candidate-scoped judgment.
- For authoring agent instructions in this repository, use
  [Astra writing-for-agents](../../skills/astra/writing-for-agents/SKILL.md).
  Its conditional [skill-authoring reference](../../skills/astra/writing-for-agents/references/skill-authoring.md)
  covers discovery and packaging. The custom version remains the legacy pack's
  source, not the authoring method selected for this repository.
- Shared engineering judgment belongs to
  [the repository-owned contract](../../docs/agents/engineering-contract.md).
  Specialized workflow vocabulary remains with the skill or decision that
  defines it; the contract does not require the legacy vocabulary catalog.
  Project-specific domain language and decisions remain with routed domain
  records.
- Delegated implementation handoff language and worker evidence Returns belong
  to `$implement` and its disclosed reference. Concurrent-lane preparation and
  cleanup are shared mechanics. Parallel delivery scheduling, concurrency
  qualification, serial landing, recombination, and parent closeout belong to
  `$parallel-implement`. [ADR-0012](../../docs/adr/0012-shared-delegated-execution-separates-delivery-authority-from-executor-transport.md)
- Domain vocabulary belongs to routed `CONTEXT.md` files and ADRs in each target repo.
