# Programming Agent Skills

This repository packages a shared engineering discipline as skills, setup contracts, validators, and focused reference.

## Repository Invariants

- `AGENTS.md` is a short agent primer: verified commands, context pointers, and local invariants.
- `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md` is the minimal global bootstrap for `$skill-router` and `$repo-bootstrap`. Personal environment rules stay outside it.
- `docs/plans/README.md` routes current work without copying plans or runbooks.
- `docs/agents/engineering-contract.md` owns engineering taste, preventive code quality, shared runtime language, and cross-cutting discipline.
- `docs/agents/issue-tracker.md`, `triage-labels.md`, and `domain.md` own tracker mechanics, state roles, and domain routing.
- `skills/custom/` is the active supported install set and the only source for managed installation. `skills/experimental/` holds inactive named alternatives to active skills. `skills/extra/` is optional, and `skills/.archive/` is retired history.
- Historical research, synthesis, transcripts, issue notes, and run logs remain evidence. They become current instructions only when an owning README or `docs/plans/README.md` says so.
- A Fresh Composition Epoch treats prior research, synthesis, validation, and campaign conclusions as historical by default. It admits them only after independent rediscovery or explicit revalidation against the epoch's fixed identities and claims.
- Mechanical rules belong in scripts or config. Prose owns routing, judgment, and behavior that cannot be enforced directly.
- Deploy-campaign automation may write only reproducible mechanical evidence
  state. The campaign owner alone settles semantic gate decisions.

## Context Trace

Load context through one directional trace:

```text
global bootstrap -> repo AGENTS.md -> owning docs -> selected skill -> branch reference -> evidence
```

Each layer points to the next and keeps only its own contract:

- the global bootstrap exposes route and setup;
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
- `skills/experimental/<skill>/`: inactive candidate behavior with the same name as an active custom skill; it is not routed, installed, or an edit source for the active pack.
- `$HOME/.agents/skills/<skill>`: installed mirror, never the edit source of truth.

Canonical extraction has one ownership chain. For a new package, the bundled
`skill-creator` owns scaffolding and metadata. `$writing-great-skills` Author
owns semantic edits to the requested canonical package and directly affected
proof or relationship surfaces, then stops after canonical proof. Installation,
publishing, and Git delivery resume only under their own authority.

The installer records pack-managed names in `.programming-agent-skills-manifest.json`. It may update or retire those names while preserving unrelated skills in the shared install directory.

## Work State

- `.tmp/` holds disposable local work. Delete it before delivery or name each intentionally preserved path.
- `.scratch/` holds durable, version-controlled local work state. Include in-scope changes in review and staging.
- Prompt outputs under `docs/synthesis/facets/` are synthesis evidence, not boot instructions.
- Generated data, caches, downloads, and bulky outputs stay untracked unless the repository explicitly needs them.

## Stable Defaults

- Activate `.venv`, then use portable `python -m ...` commands.
- Keep pytest defaults in `pyproject.toml`.
- Use `python -m scripts.pytest_focused` for narrow tests without full-suite fanout.
- Use `python -m scripts.validate_skills` for repo integrity.
- Use `python -m scripts.install_skills` for managed install or update, then validate the installed root.

## Pack Vocabulary

**Skill pack**

A coordinated set of skills, setup contracts, validators, and reference that produces one engineering operating model.
_Avoid_: prompt collection, script bundle

**Fresh Composition Epoch**

A pack-wide epistemic reset that freezes intended composition before prior
research, synthesis, validation, campaign conclusions, or current skill bodies
can steer discovery. It rebuilds a Pack Composition Contract and Research
Catalog, runs gate-driven one-skill Deploy Campaigns under that contract,
proves the composed pack, and cleans up superseded material only after Lock.
Prior artifacts are historical intake until Contract Lock independently binds
current intent and explicitly revalidates their complete identities.
_Avoid_: clean slate, destructive reset, pack-wide Deploy Campaign

**Pack Composition Contract**

The pack-level synthesis contract for selected capabilities, each skill's
essential outcome and router, executable-aggregate, or leaf role, ownership
boundaries, relationships, exclusions, collisions, gaps, and required
integration proof. It constrains one-skill Deploy Campaigns without selecting
their H1 behavior or copying their procedures.
_Avoid_: skill inventory, route list, campaign charter

**Research Catalog**

The campaign-facing index of reusable Research Cards, organized by the
behavior or failure they address, conditions, evidence class, freshness,
limits, and source pointers. A one-skill campaign opens it only when Contract
Lock finds a decision-relevant method, concept, hypothesis, or source-evidence
gap, and only after recording an independent problem-first packet. It supports
retrieval and never selects skill composition or admits H1.
_Avoid_: recommendation engine, synthesis index, source dump

**Research Card**

A reusable evidence unit describing one behavior or method, the failure it may
prevent, applicability and counterconditions, claim-owning evidence,
freshness, limits, and source-packet pointers. Per-skill synthesis decides
whether a card contributes to H1.
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

The verified target-repo contract installed by `$repo-bootstrap`: primer, commands, tracker lifecycle, label vocabulary, domain routing, engineering contract, and work-state policy.
A hidden setup-schema marker identifies contract compatibility, not the installed pack version.
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

**Change review candidate**

A fixed-snapshot diff or PR that is neither a release candidate nor governed by
a Supported high-risk trigger. `$change-review` owns its separate Spec and
Standards gate.
_Avoid_: non-PR review, low-priority review

**High-assurance review candidate**

A fixed-snapshot release candidate or diff or PR governed by a Supported
high-risk trigger. `$high-assurance-review` owns its root-only fresh-context
review and terminal release decision.
_Avoid_: every PR, large diff, severe-looking change

**Supported high-risk trigger**

A changed surface with a supported scenario, reachable behavior or failure
path, and concrete impact involving a trust boundary, irreversible effect or
migration, concurrency or recovery, high-impact domain or model invariant, or
measured performance obligation. PR existence, size, and labels do not qualify.
_Avoid_: hypothetical edge case, risk label, PR route

**Router skill**

An explicit-only skill that returns one next route and leaves downstream work unstarted.
_Avoid_: dispatcher, automatic router

**Deploy Campaign**

An explicitly invoked one-skill controller, owned by
[`deploy-prompts.md`](docs/synthesis/methods/deploy-prompts.md), that advances
one skill only through satisfied proof gates: Contract Lock, Candidate Lock,
Behavioral Proof, and Release. Research is conditional on a decision-relevant
evidence gap. Behavioral evaluation runs only for claims that deterministic
or real-state proof cannot establish. Release performs a cheap cut scan and
runs pruning proof only for a concrete material cut.

Prior evidence may satisfy a gate only after Contract Lock independently binds
current intent and dependencies and the complete evidence identity matches.
Bare runs include promotion/install; Git delivery must be named. The controller
retains user interaction and bounded fresh-context delegation without making
research, behavioral sampling, or pruning a mandatory unit.
_Avoid_: mega-prompt, self-chaining prompt, pack-wide campaign

**Deploy runtime identities**

M0 is an intent-derived, behavior-minimal control; H1 is a method- or
concept-informed hypothesis; V1 is the behavior-verified runtime; and P1 is
the exact Release candidate after the cut gate. They are conditional evidence
identities, not mandatory lifecycle stages. When no material cut exists,
P1 equals V1 by exact identity. Historical B0/C1 records keep their original
campaign meaning.
_Avoid_: current baseline, source-derived minimum, final C1

**Campaign control manifest**

The machine-readable control plane for one exact Deploy Campaign epoch. It owns
campaign identity, artifact pointers and identities, proof registrations and
receipts, invalidations, and mechanical gate state. It points to semantic
decisions in synthesis and the decision record instead of copying their
meaning or rationale.
_Avoid_: second synthesis, campaign diary, latest campaign

**Mechanical evidence state**

Reproducible campaign state that automation may compute and write
transactionally, such as leases, bounded identities, deterministic proof
receipts, cache validity, isolation checks, and parity. Optional `.tmp` data
may recover exact reusable evidence but is never promotion-critical authority
and cannot replace explicitly fresh behavioral proof.
_Avoid_: automated judgment, inferred decision

**Semantic decision state**

The campaign owner's settled intent, research interpretation, hypothesis,
applicability, evaluation judgment, proof sufficiency, disposition, pruning,
promotion, and gate decision. Automation may verify referenced mechanical
facts but cannot manufacture, alter, or advance this state.
_Avoid_: verifier decision, test-determined adoption

**Campaign continuation modes**

Resume continues one epoch with unchanged semantic inputs and identities.
Repair changes an authorized artifact in that epoch and mechanically stales
dependent proof. Restart creates a new epoch that explicitly supersedes the
old manifest when the target, intended contract, delivery authority, or a
terminal campaign changes.
_Avoid_: silent reopen, latest-run recovery

**Global AGENTS template**

The pack-owned bootstrap section merged into a user's global `AGENTS.md` without replacing personal rules.
_Avoid_: pack manual, copied route map

## Vocabulary Owners

- Fresh Composition Epoch, Pack Composition Contract, Research Catalog, and Research Card vocabulary belongs to this context and [ADR-0009](docs/adr/0009-fresh-composition-epochs-revalidate-skill-pack-knowledge.md). The accepted `docs/synthesis/skill-pack.md` owner remains to be materialized by the separately authorized topology migration.
- Deploy-campaign gate vocabulary and the conditional M0, H1, V1, and P1
  identities belong to
  [`deploy-prompts.md`](docs/synthesis/methods/deploy-prompts.md) and
  [ADR-0010](docs/adr/0010-deploy-campaigns-advance-through-proof-gates.md).
- Change review candidate, High-assurance review candidate, and Supported
  high-risk trigger belong to this context and
  [ADR-0011](docs/adr/0011-review-assurance-follows-release-risk.md).
- Deploy-campaign automation authority and control-plane vocabulary belong to [ADR-0008](docs/adr/0008-deploy-campaign-automation-separates-mechanical-evidence-from-semantic-decisions.md) and this context.
- Skill-authoring vocabulary—Predictability, invocation, information hierarchy, leading words, completion criteria, and pruning—belongs to [`skills/custom/writing-great-skills/GLOSSARY.md`](skills/custom/writing-great-skills/GLOSSARY.md).
- Runtime engineering vocabulary and preventive code-quality defaults—Source
  Trace, bounded slice, commitment boundary, proof seam, proof lane, fixed
  point, Spec / Standards, correctness, robustness, Change Closure, code shape,
  simplification, implementation clarity, measured performance, Lock, and
  residual risk—belong to `docs/agents/engineering-contract.md`.
  Project-specific domain language and decisions remain with routed domain
  records.
- Parallel-delivery roles, gates, and packets belong to `$parallel-implement` and its disclosed references.
- Domain vocabulary belongs to routed `CONTEXT.md` files and ADRs in each target repo.
