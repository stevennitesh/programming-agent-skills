# Programming Agent Skills

This repository packages a shared engineering discipline as skills, setup contracts, validators, and focused reference.

## Repository Invariants

- `AGENTS.md` is a short agent primer: verified commands, context pointers, and local invariants.
- `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md` is the minimal global bootstrap for `$skill-router` and `$repo-bootstrap`. Personal environment rules stay outside it.
- `docs/plans/README.md` routes current work without copying plans or runbooks.
- `docs/agents/engineering-contract.md` owns engineering taste, shared runtime language, and cross-cutting discipline.
- `docs/agents/issue-tracker.md`, `triage-labels.md`, and `domain.md` own tracker mechanics, state roles, and domain routing.
- `skills/custom/` is the active supported install set and the only source for managed installation. `skills/experimental/` holds inactive named alternatives to active skills. `skills/extra/` is optional, and `skills/.archive/` is retired history.
- Historical research, synthesis, transcripts, issue notes, and run logs remain evidence. They become current instructions only when an owning README or `docs/plans/README.md` says so.
- Mechanical rules belong in scripts or config. Prose owns routing, judgment, and behavior that cannot be enforced directly.

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

**Router skill**

An explicit-only skill that returns one next route and leaves downstream work unstarted.
_Avoid_: dispatcher, automatic router

**Deploy Campaign**

An explicitly invoked one-skill controller, owned by
[`deploy-prompts.md`](docs/synthesis/methods/deploy-prompts.md), that verifies
and serially advances Prompt 1, the Research Pass, Prompts 2 through 4, a
behavior-preserving Pruning Pass, and Prompt 5 for one fresh campaign epoch
while retaining user interaction. It freezes intent-derived M0 before
research, tests research-informed H1 into V1, prunes V1 into P1, and promotes
only P1. A prior campaign may supply exact reusable evidence but cannot skip a
unit. Bare runs include promotion/install; Git delivery must be named. It
authorizes bounded fresh-context delegation; each unit keeps its own authority
and stop.
_Avoid_: mega-prompt, self-chaining prompt, pack-wide campaign

**Deploy runtime identities**

M0 is the intent-derived, behavior-minimal runtime; H1 is the
research-informed hypothesis runtime; V1 is the behavior-verified runtime; and
P1 is the regression-checked pruned runtime and sole promotion candidate.
Historical B0/C1 records keep their original campaign meaning.
_Avoid_: current baseline, source-derived minimum, final C1

**Global AGENTS template**

The pack-owned bootstrap section merged into a user's global `AGENTS.md` without replacing personal rules.
_Avoid_: pack manual, copied route map

## Vocabulary Owners

- Deploy-campaign vocabulary—M0, H1, V1, P1, and intent-adjacent steering hypotheses—belongs to [`docs/synthesis/methods/deploy-prompts.md`](docs/synthesis/methods/deploy-prompts.md).
- Skill-authoring vocabulary—Predictability, invocation, information hierarchy, leading words, completion criteria, and pruning—belongs to [`skills/custom/writing-great-skills/GLOSSARY.md`](skills/custom/writing-great-skills/GLOSSARY.md).
- Runtime engineering vocabulary—Source Trace, bounded slice, commitment boundary, proof seam, proof lane, fixed point, review snapshot, Spec / Standards, Lock, and residual risk—belongs to `docs/agents/engineering-contract.md`.
- Parallel-delivery roles, gates, and packets belong to `$parallel-implement` and its disclosed references.
- Domain vocabulary belongs to routed `CONTEXT.md` files and ADRs in each target repo.
