<h1 align="center">Programming Agent Skills</h1>

<p align="center"><strong>Thoughtful engineering for AI-assisted development.</strong></p>

<p align="center">
  Built specifically for GPT 6 Astra in Codex: clarify the problem, make sound design decisions,<br>
  and check that the finished work holds up.
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
</p>

<p align="center">
  <a href="#what-it-helps-with">Explore the pack</a> ·
  <a href="#getting-started">Get started</a> ·
  <a href="docs/astra/design-brief.md">Read the design brief</a>
</p>

---

Good software takes more than working code. It takes a clear understanding of
the problem, decisions that fit the existing system, and evidence that a change
does what people need.

I built this pack to bring those habits into everyday work with coding agents.
The **Astra skills pack** is designed specifically for **GPT 6 Astra**. It combines
shared engineering guidance with 16 focused skills for planning, design,
debugging, review, and delivery. Each skill
is a set of instructions and, where useful, supporting tools that Codex can use
for a particular kind of work.

The aim is straightforward: code that is easier to understand, changes that are
easier to review, and decisions that the next person can follow.

The instructions assume GPT 6 Astra's baseline capabilities and concentrate on
context and methods that add to them. **Smaller models may need the
[custom skill pack](skills/custom/)**, which contains more detailed instructions.
The installer below installs the Astra skills pack; it does not install the
custom pack. Model-specific comparisons are still limited.

## What it helps with

| When the work involves… | The pack provides… |
| --- | --- |
| An idea that is still taking shape | Questions that clarify the outcome, constraints, and what success means. |
| A feature that must fit an existing system | Design guidance and small prototypes to test consequential assumptions. |
| A difficult bug or an unfamiliar codebase | Methods for tracing root causes and examining architecture, with an optional visual system map. |
| A change that needs careful review | Focused review of correctness and maintainability, with deeper assurance when requested. |
| Several people or agents working together | Clear ownership, dependency-aware task planning, and recovery guidance for interrupted work. |

You can use one skill for a specific problem or combine several for a larger
piece of work. Routine coding can proceed directly; there is no required
planning-to-ticket-to-implementation pipeline.

## The engineering philosophy

> Explore imaginatively. Converge under proof. Simplify ruthlessly.

- **Understand before changing.** Read the existing code, follow its callers,
  and identify the behavior people rely on.
- **Build what the problem needs.** Prefer a clear, small design. Reuse what
  fits, and add abstractions when they earn their place.
- **Check the result that matters.** Use tests and experiments that can expose
  a real failure. More tests do not automatically mean stronger evidence.
- **Leave useful context.** Preserve decisions, reasons, and local conventions
  so future contributors can continue the work confidently.

These principles live in the
[engineering contract](skills/astra/repo-bootstrap/templates/engineering-contract.md).
Repository setup adapts that guidance to a project's own conventions. The skills
add specialized methods where the task benefits from them.

## Explore the skills

| Purpose | Skills |
| --- | --- |
| Clarify and plan | [Shape work](skills/astra/shape-work/SKILL.md) · [Create tickets](skills/astra/to-tickets/SKILL.md) |
| Design and investigate | [Codebase design](skills/astra/codebase-design/SKILL.md) · [Prototype](skills/astra/prototype/SKILL.md) · [Research](skills/astra/research/SKILL.md) |
| Assess and improve | [Audit a codebase](skills/astra/audit-codebase/SKILL.md) · [Diagnose bugs](skills/astra/diagnosing-bugs/SKILL.md) · [Hillclimb: measured optimization](skills/astra/hillclimb/SKILL.md) · [Review changes](skills/astra/change-review/SKILL.md) |
| Coordinate implementation | [Parallel implementation](skills/astra/parallel-implement/SKILL.md) · [Resolve merge conflicts](skills/astra/resolving-merge-conflicts/SKILL.md) |
| Experiment with model allocation | [Cost-aware coding](skills/astra/cost-aware-coding/SKILL.md) — route work across models; savings and quality tradeoffs still need calibration |
| Maintain agent guidance | [Repository setup](skills/astra/repo-bootstrap/SKILL.md) · [Writing for agents](skills/astra/writing-for-agents/SKILL.md) · [Context hygiene](skills/astra/context-hygiene/SKILL.md) |
| Guide a human-operated procedure | [Wizard](skills/astra/wizard/SKILL.md) |

<a id="install"></a>

## Getting started

You'll need [Codex](https://github.com/openai/codex), Git, and Python 3.11 or newer.
The installer uses only Python's standard library.

Clone the repository, preview the changes, then install:

```bash
git clone https://github.com/stevennitesh/programming-agent-skills.git
cd programming-agent-skills

python3 -m scripts.install_skills --dry-run
python3 -m scripts.install_skills
```

<details>
<summary><strong>PowerShell commands</strong></summary>

```powershell
git clone https://github.com/stevennitesh/programming-agent-skills.git
Set-Location programming-agent-skills

python -m scripts.install_skills --dry-run
python -m scripts.install_skills
```

</details>

The installer deploys the Astra skills pack to `$HOME/.agents/skills` and manages a small
bootstrap section in `$HOME/.codex/AGENTS.md`. It preserves unrelated skills
and personal instructions, and stops if managed skills contain local edits or
an unmanaged folder has the same name. Add `--skip-global-agents` to leave
global instructions untouched.

To update, pull this repository and repeat the preview and install commands.
See [installation and recovery](INSTALLATION.md) for migration from the older
pack, custom locations, and verification.

**Prefer to start with just the principles?** Adapt the
[portable engineering guidance](AGENTS_PORTABLE_FALLBACK.md) into your global
`AGENTS.md`, preserving your existing preferences. It needs no installer and
leaves out the specialized skills and managed updates.

## Try it on real work

Ask Codex for the work you need, or name a skill directly with its `$` prefix:

```text
$shape-work help me clarify how failed imports should be retried

$codebase-design where should retry state live in this application?

$diagnosing-bugs investigate why this import sometimes stalls

$change-review review this branch for correctness and maintainability
```

For repository guidance, ask `$repo-bootstrap` to inspect or set up the project.
It can reconcile existing instructions and engineering conventions with this pack;
you can also request an inspection without changes. GitHub, GitLab, and local
Markdown trackers are supported when the project needs ticketed work.

<details>
<summary><strong>Which skills run only when requested?</strong></summary>

`$audit-codebase`, `$context-hygiene`, `$hillclimb`, `$parallel-implement`,
`$repo-bootstrap`, `$shape-work`, `$to-tickets`, `$wizard`, and `$cost-aware-coding` require a user
request. The other seven skills can be selected from matching task descriptions.
Suggesting an explicit workflow does not automatically start it.

For larger work, shape the outcome first, create tickets when useful, and
request parallel implementation when the accepted tasks have independent
ownership. These are optional steps. Continuation handoffs are part of
`$writing-for-agents`; deeper assurance is an option within `$change-review`.

</details>

## How the pack is developed

The Astra skills pack is being refined through source comparisons, critical reviews, and
focused workflow tests. The repository includes executable helpers and tests
for areas such as installation, architecture reports, and parallel worktree
management.

Those checks establish specific behavior. Whether the pack improves coding
quality over an agent's default capabilities needs broader comparative
validation; the comparisons so far are limited. The
[design brief](docs/astra/design-brief.md), shaped by
[issue #94](https://github.com/stevennitesh/programming-agent-skills/issues/94),
records the decisions, evidence, and open questions behind the current pack.

## Influences and contributions

This project began with
[Matt Pocock's skills](https://github.com/mattpocock/skills) and draws on ideas
from [pstack](https://github.com/cursor/plugins/tree/main/pstack),
[Ponytail](https://github.com/DietrichGebert/ponytail), and
[Superpowers](https://github.com/obra/superpowers). Their approaches to focused
workflows, simple design, and disciplined engineering helped shape this pack.
See [Acknowledgments](ACKNOWLEDGMENTS.md) for more.

If you're exploring the implementation or contributing a change, start with
[the Astra skills pack source](skills/astra/), [repository context](CONTEXT.md), and
[contributor instructions](AGENTS.md). The more detailed
[custom pack](skills/custom/) remains available for users evaluating other models.
Earlier research is retained as historical evidence; the installer deploys only
the Astra skills pack.

---

[MIT License](LICENSE)
