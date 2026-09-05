# Programming Agent Skills

This repository packages a shared engineering discipline as skills, setup contracts, validators, and focused reference.

## Repository Invariants

- `AGENTS.md` is a short agent primer: verified commands, context pointers, and local invariants.
- `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md` is the lean global delegation gate and bootstrap for `$skill-router` and `$repo-bootstrap`. Personal environment rules stay outside it.
- `docs/plans/README.md` routes current work without copying plans or runbooks.
- `docs/agents/engineering-contract.md` owns engineering taste, preventive code quality, shared runtime language, and cross-cutting discipline.
- `docs/agents/issue-tracker.md`, `triage-labels.md`, and `domain.md` own tracker mechanics, state roles, and domain routing.
- `skills/custom/` is the active supported install set and the only source for managed installation. `skills/experimental/` holds inactive named alternatives to active skills. `skills/extra/` is optional, and `skills/.archive/` is retired history.
- `skills/astra/` owns the new Astra packages. They are outside managed installation; edit their source there rather than changing a same-named custom skill.
- Historical research, synthesis, transcripts, issue notes, and run logs remain evidence. They become current instructions only when an owning README or `docs/plans/README.md` says so.
- Mechanical rules belong in scripts or config. Prose owns routing, judgment, and behavior that cannot be enforced directly.

## Context Trace

Load context through one directional trace:

```text
global bootstrap -> repo AGENTS.md -> owning docs -> selected skill -> branch reference -> evidence
```

Each layer points to the next and keeps only its own contract:

- the global template exposes delegation activation, route, and setup;
- `AGENTS.md` primes commands and pointers;
- `docs/agents/*` teaches repo-wide mechanics and vocabulary;
- a skill owns one procedure, its gates, outputs, mutations, and completion;
- disclosed files hold branch-specific reference;
- source, tests, diffs, commands, and read-back prove the result.

Copying downstream procedure upward is duplication. Repeating one leading word across layers is intentional when it improves invocation or execution.

## Artifact Ownership

- `README.md`: human-facing product overview, install, update, and first-use path.
- `scripts/install_skills.py`: managed installation and installed-pack manifest.
- `scripts/validate_skills.py`: skill schema, policy, reference, setup, mirror, publication, and diff integrity.
- `skills/experimental/manifest.json`: current experimental tree identities, capture provenance, and active baselines.
- `docs/research/`: source intake and historical source evidence.
- `docs/synthesis/`: selected design, evidence, extraction maps, methods, family notes, and historical prompt outputs; synthesis does not authorize runtime mutation.
- `docs/validation/`: repeatable fixtures and evidence that wording changes behavior.
- `docs/adr/`: durable decisions that routine skill edits should not relitigate.
- `skills/custom/<skill>/SKILL.md`: active skill behavior; sibling files hold disclosed branch reference.
- `skills/astra/<skill>/SKILL.md`: Astra skill behavior; templates are seeds for repository-owned guidance, not managed mirrors.
- `skills/astra/repo-bootstrap/templates/global-agents.md`: Astra global guidance seed, separate from the legacy global template; personal environment rules remain user-owned.
- `skills/experimental/<skill>/`: inactive candidate behavior with the same name as an active custom skill; it is not routed, installed, or an edit source for the active pack.
- `$HOME/.agents/skills/<skill>`: installed mirror, never the edit source of truth.

Canonical extraction has one ownership chain. For a new package, the bundled
`skill-creator` owns scaffolding and metadata. `$writing-for-agents` owns the
instructions agents consume and directly affected pointers. Skill-only
packaging and metadata mechanics remain with `skill-creator`. Installation,
publishing, and Git delivery resume only under their own authority.

The installer records pack-managed names in `.programming-agent-skills-manifest.json`. It may update or retire those names while preserving unrelated skills in the shared install directory.

## Astra and legacy coexistence

The Astra `writing-for-agents` and `repo-bootstrap` packages have been installed
as manual overrides of the same-named custom skills. Before changing an installed
copy, inspect its current content and selected source. The managed installer
still selects `skills/custom/`; it does not deploy Astra and may replace these
overrides. Use the requested source package for a targeted Astra installation.

This repository retains the legacy tracker, labels, and domain routes for their
current consumers. Direct coding does not require a tracker item. The local
engineering contract adopts the Astra seed and is repository-owned. Validation
checks its structure without requiring template parity or a legacy source marker.
Changes to either bootstrap seed do not automatically change this repository's
contract. The custom bootstrap retains managed-marker validation by default for
repositories that still use that contract.

## Pack Vocabulary

**Skill pack**

A coordinated set of skills, setup contracts, validators, and reference that produces one engineering operating model.
_Avoid_: prompt collection, script bundle

**Fresh Composition Epoch**

A pack-wide epistemic reset in which prior research, synthesis, validation, and
change conclusions are historical intake until independently rediscovered or
explicitly revalidated. The active method lives in
[`fresh-composition-epoch.md`](docs/synthesis/methods/fresh-composition-epoch.md).
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

**Active skill**

A supported skill under `skills/custom/`; it is eligible for validation, routing, managed installation, and mirror comparison.
_Avoid_: custom variant, production experiment

**Experimental skill**

An inactive alternative under `skills/experimental/` that shadows one active skill name while its design is evaluated. It is preserved and hash-tracked, but never routed or installed until explicitly promoted into `skills/custom/`.
_Avoid_: active skill, installed skill, archive

**Target repo**

A repository configured to use the pack for shaping, implementation, triage, review, or maintenance.
_Avoid_: client repo, downstream repo

**Setup surface**

The verified target-repo contract installed by `$repo-bootstrap`: primer, commands, tracker configuration, label vocabulary, domain routing, engineering contract, and work-state policy.
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
[`deploy-prompts.md`](docs/synthesis/methods/deploy-prompts.md). Its ordered
reasoning and proof obligations are not persisted semantic lifecycle state.
_Compatibility aliases_: Deploy Campaign; Contract Lock; Candidate Lock;
Behavioral Proof; Release (for this method stage only)
_Avoid_: mega-prompt, self-chaining prompt, pack-wide method

**Global AGENTS template**

The complete template seeds a missing global `AGENTS.md`; later installs update
only the pack-owned bootstrap section without replacing delegation or personal
rules.
_Avoid_: pack manual, copied route map

## Vocabulary Owners

- Fresh Composition Epoch, Pack Composition Baseline, Evidence Catalog, and
  Evidence Record vocabulary belongs to this context and
  [ADR-0014](docs/adr/0014-source-native-vocabulary-names-active-pack-concepts.md).
  [ADR-0009](docs/adr/0009-fresh-composition-epochs-revalidate-skill-pack-knowledge.md)
  remains the Fresh Composition Epoch decision. The accepted
  `docs/synthesis/skill-pack.md` payload is the current Pack Composition
  Baseline owner.
- Skill Change-Control Method proof-obligation vocabulary belongs to
  [`deploy-prompts.md`](docs/synthesis/methods/deploy-prompts.md) and
  [ADR-0014](docs/adr/0014-source-native-vocabulary-names-active-pack-concepts.md).
  [ADR-0010](docs/adr/0010-deploy-campaigns-advance-through-proof-gates.md)
  remains the controllerless proof-ordering decision.
- Change review candidate, High-assurance review candidate, and Supported
  high-risk trigger belong to this context and
  [ADR-0016](docs/adr/0016-ordinary-and-formal-review-share-one-lean-judgment-owner.md).
  The caller owns activation, each review skill validates its admitted
  candidate, and risk expands only applicable candidate-scoped judgment.
- For authoring agent instructions in this repository, use
  [Astra writing-for-agents](skills/astra/writing-for-agents/SKILL.md).
  Its conditional [skill-authoring reference](skills/astra/writing-for-agents/references/skill-authoring.md)
  covers discovery and packaging. The custom version remains the legacy pack's
  source, not the authoring method selected for this repository.
- Shared engineering judgment belongs to
  [the repository-owned contract](docs/agents/engineering-contract.md).
  Specialized workflow vocabulary remains with the skill or decision that
  defines it; the contract does not require the legacy vocabulary catalog.
  Project-specific domain language and decisions remain with routed domain
  records.
- Delegated implementation handoff language and worker evidence Returns belong
  to `$implement` and its disclosed reference. Concurrent-lane preparation and
  cleanup are shared mechanics. Parallel delivery scheduling, concurrency
  qualification, serial landing, recombination, and parent closeout belong to
  `$parallel-implement`. [ADR-0012](docs/adr/0012-shared-delegated-execution-separates-delivery-authority-from-executor-transport.md)
- Domain vocabulary belongs to routed `CONTEXT.md` files and ADRs in each target repo.
