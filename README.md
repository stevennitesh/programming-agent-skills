<h1 align="center">Programming Agent Skills</h1>

<p align="center"><strong>Give your coding agent the context and methods the work needs.</strong></p>

<p align="center">
  18 focused skills, built primarily for GPT 6 Astra in Codex.<br>
  Ordinary coding stays direct; specialist workflows activate only when the task needs them.
</p>

<p align="center">
  <img src="docs/astra/assets/skill-pack-overview.png" width="960" alt="Repository guidance supplies local context, ordinary coding stays direct, and focused skills handle specialized shaping, design, debugging, review, delivery, and verification work.">
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
</p>

<p align="center">
  <a href="#getting-started">Get started</a> ·
  <a href="#find-the-right-skill">Find a skill</a> ·
  <a href="#how-it-fits-together">How it fits together</a> ·
  <a href="#cost-aware-coding">Cost-aware coding</a> ·
  <a href="docs/astra/design-brief.md">Design brief</a>
</p>

---

A capable coding agent already knows how to write code. What it often lacks is
the project-specific context needed to make the right change: which behavior must
stay intact, where a decision belongs, and what would prove the result works.

The **Astra skills pack** adds that context plus focused methods for tasks that
benefit from a distinct workflow. It deliberately does **not** make ordinary
implementation pass through a skill pipeline.

> Explore imaginatively. Converge under proof. Simplify ruthlessly.

<a id="install"></a>

## Getting started

You'll need [Codex](https://github.com/openai/codex), Git, and Python 3.11 or newer.
The installer itself uses only Python's standard library.

Clone the repository, preview the managed changes, then install:

```sh
git clone https://github.com/stevennitesh/programming-agent-skills.git
cd programming-agent-skills

python -m scripts.install_skills --dry-run
python -m scripts.install_skills
```

On macOS/Linux, use `python3` if needed.

The installer deploys `skills/astra/` to `$HOME/.agents/skills` and manages a
small bootstrap section in `$HOME/.codex/AGENTS.md`. It preserves unrelated
skills and personal instructions and refuses unsafe ownership conflicts. Use
`--skip-global-agents` if you want the skills without changing global
instructions.

After installation:

- for a clear bounded code change, **just ask Codex to implement it**;
- invoke a named skill such as `$shape-work` when you want an explicit workflow;
- automatic skills can be selected by Codex when the request matches their scope.

To update, pull this repository and repeat the preview/install commands. See
[installation and recovery](INSTALLATION.md) for migration, custom targets,
installed-pack validation, and transaction recovery.

If you want only the shared engineering principles without the managed skills,
adapt [AGENTS_PORTABLE_FALLBACK.md](AGENTS_PORTABLE_FALLBACK.md) into your global
`AGENTS.md`.

<details>
<summary><strong>Model support</strong></summary>

The managed pack is tuned primarily for **GPT 6 Astra**. The optional
cost-aware workflow can route implementation-heavy work to **GPT 6 Sol** and
compact bounded work to **GPT 6 Luna**.

The historical [custom skill pack](skills/custom/) remains available for
comparison and separate evaluation, but it is not installed by the current
installer. Current model-specific comparisons are not sufficient to claim that
the historical package performs better for smaller models.

</details>

## How it fits together

The pack separates durable project context from specialized procedures:

| Surface | Owns | When to use it |
| --- | --- | --- |
| Repository `AGENTS.md` | Verified commands, local constraints, and pointers | Read first in a repository |
| Repository context and decisions | Project meaning, source boundaries, and durable decisions | When the task depends on project-specific meaning |
| Engineering contract | Shared coding judgment such as simplicity, ownership, and proportionate proof | During substantive engineering work |
| Direct coding | Normal implementation under repository guidance | Default for a clear bounded change |
| Astra skills | A distinct method or effect with its own admission and completion boundary | Only when the task matches that skill |
| Historical research/synthesis/validation | Evidence and rationale from earlier pack generations | Consult selectively; never treat as current routing by default |

For this repository specifically, [AGENTS.md](AGENTS.md) gives contributor
commands and pointers, [CONTEXT.md](CONTEXT.md) owns source boundaries, and the
[Astra design brief](docs/astra/design-brief.md) owns current composition
rationale. Each `skills/astra/*/SKILL.md` file owns its execution procedure.

Common paths stay simple:

- **Clear change → direct implementation.**
- **Unclear product behavior → `$shape-work` → direct implementation.**
- **Consequential technical design question → `$codebase-design` → implementation.**
- **Hard causal failure → diagnosing-bugs; repair only when already authorized.**
- **Fixed code candidate → change-review.**
- **Tracked decomposition → `$to-tickets`; parallel delivery only when explicitly requested.**

These are examples, not a required lifecycle. Skills remain independently usable.

## Find the right skill

**Request explicitly** means Codex waits for you to invoke or request that
workflow. **Automatic when relevant** means Codex may select it when your request
matches. You can also invoke an automatic skill explicitly.

| Your task | Skill | Use |
| --- | --- | --- |
| Implement a clear, bounded change | **No skill needed**—ask Codex to implement and verify using repository guidance | Direct |
| Clarify product behavior, scope, acceptance, or domain meaning | [$shape-work](skills/astra/shape-work/SKILL.md) | Request explicitly |
| Resolve a consequential technical architecture or integration decision | [$codebase-design](skills/astra/codebase-design/SKILL.md) | Automatic when relevant |
| Test an uncertain approach with a runnable experiment | [$prototype](skills/astra/prototype/SKILL.md) | Automatic when relevant |
| Create durable tooling that drives and proves real user-facing behavior | [$verification-harness](skills/astra/verification-harness/SKILL.md) | Request explicitly |
| Research a question or compare options using sources | [$research](skills/astra/research/SKILL.md) | Automatic when relevant |
| Find the root cause of a difficult bug | [$diagnosing-bugs](skills/astra/diagnosing-bugs/SKILL.md) | Automatic when relevant |
| Map a codebase visually, audit subsystems, and analyze improvement candidates | [$audit-codebase](skills/astra/audit-codebase/SKILL.md) | Request explicitly |
| Optimize a measurable outcome through experiments | [$hillclimb](skills/astra/hillclimb/SKILL.md) | Request explicitly |
| Review a code change for correctness and maintainability | [$change-review](skills/astra/change-review/SKILL.md) | Automatic when relevant |
| Classify raw incoming tracker issues into an honest next state | [$triage](skills/astra/triage/SKILL.md) | Request explicitly |
| Turn an accepted plan or spec into tracked work units | [$to-tickets](skills/astra/to-tickets/SKILL.md) | Request explicitly |
| Implement concurrently with separate ownership and clear dependencies | [$parallel-implement](skills/astra/parallel-implement/SKILL.md) | Request explicitly |
| Route GPT 6 work to reduce Astra lead-token churn while preserving acceptance | [$cost-aware-coding](skills/astra/cost-aware-coding/SKILL.md) | Request explicitly |
| Resolve an active Git merge or rebase conflict | [$resolving-merge-conflicts](skills/astra/resolving-merge-conflicts/SKILL.md) | Automatic when relevant |
| Set up, migrate, or repair repository agent guidance | [$repo-bootstrap](skills/astra/repo-bootstrap/SKILL.md) | Request explicitly |
| Write or audit a specific agent instruction, skill, guide, prompt, or handoff | [$writing-for-agents](skills/astra/writing-for-agents/SKILL.md) | Automatic when relevant |
| Audit persistent context and reconcile requested cleanup | [$context-hygiene](skills/astra/context-hygiene/SKILL.md) | Request explicitly |
| Create an interactive guide for a human-operated procedure | [$wizard](skills/astra/wizard/SKILL.md) | Request explicitly |

A review or audit does not authorize its proposed fixes. A specification or
ticket does not authorize implementation. Each skill keeps its own effect and
completion boundary.

## Example: shape before implementation

Suppose an import job can fail after partially saving records. The product
behavior is not yet settled, so start with shaping:

```text
$shape-work Help me design retries for failed imports in this repo.
Some records may already have been saved. Clarify what can be retried safely,
what users should see, and how we will know the feature works.
```

Once those behavioral decisions are settled, ask Codex to implement them
directly. Ticketing, delegation, parallel work, or another skill is unnecessary
unless the task actually needs it.

## Cost-aware coding

[$cost-aware-coding](skills/astra/cost-aware-coding/SKILL.md) is an optional,
explicit workflow for reducing Astra lead-token/context churn while preserving
the accepted result:

- **Astra** owns consequential reasoning, exceptions, and final review.
- **Sol** owns substantial repository investigation, implementation, debugging,
  verification, and repair.
- **Luna** is reserved for compact bounded tasks whose briefing and verification
  stay cheap.

Delegation is worthwhile only when it saves more Astra context than the handoff,
coordination, review, and recovery cost. While a worker owns implementation,
Astra should remain mostly dormant rather than shadowing it.

When combined with
[$parallel-implement](skills/astra/parallel-implement/SKILL.md),
parallel-implement owns concurrency, lane custody, integration, and parallel
recovery; cost-aware-coding retains model/effort routing, budget policy, and its
final review requirement.

The skill itself owns current model policy, worker assignment, recovery, planned
serial delivery, and optional telemetry. Keep those changing mechanics there
rather than copying them into repository guidance.

## Engineering philosophy

- **Understand before changing.** Read the existing code, real callers, and
  behavior people rely on.
- **Build what the problem needs.** Prefer a small clear design; add abstraction
  only when it earns its place.
- **Check the result that matters.** Use evidence capable of exposing a real
  failure, not test count as a proxy for rigor.
- **Leave useful context.** Preserve decisions, reasons, and local conventions
  where future contributors can actually find them.

The maintained seed lives in the
[engineering contract template](skills/astra/repo-bootstrap/templates/engineering-contract.md).
Repository setup adapts it to local conventions rather than maintaining a
template mirror.

## Project status and evidence

The pack is refined through source comparison, critical review, focused workflow
tests, and real repository use. Package validation and helper tests establish
specific structural or mechanical behavior; they do **not** by themselves prove
that the pack produces better code, lower total cost, or equivalent behavior
across models.

The [Astra design brief](docs/astra/design-brief.md) records current composition,
ownership, evidence limits, and open questions. Historical research, synthesis,
validation, and ADRs remain available as evidence but do not override current
owners.

## Influences and contributing

This project began with
[Matt Pocock's skills](https://github.com/mattpocock/skills) and draws on ideas
from [pstack](https://github.com/cursor/plugins/tree/main/pstack),
[Ponytail](https://github.com/DietrichGebert/ponytail), and
[Superpowers](https://github.com/obra/superpowers). See
[Acknowledgments](ACKNOWLEDGMENTS.md) for provenance and influences.

If you're contributing to this repository, start with
[AGENTS.md](AGENTS.md), [CONTEXT.md](CONTEXT.md), and the
[Astra design brief](docs/astra/design-brief.md). The managed source is
[skills/astra/](skills/astra/).

---

[MIT License](LICENSE)
