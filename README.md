<h1 align="center">Programming Agent Skills</h1>

<p align="center"><strong>Give your coding agent the context and methods the work needs.</strong></p>

<p align="center">
  18 focused skills, built primarily for GPT 6 Astra in Codex.<br>
  Optional cost-aware routing uses GPT 6 Sol and Luna. Ordinary coding stays direct.
</p>

<p align="center">
  <img src="docs/astra/assets/skill-pack-overview.png" width="960" alt="The pack brings together relevant project context, focused methods for shaping, design, debugging and review, and evidence from meaningful checks. Use each when the task needs it; there is no required pipeline.">
</p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
</p>

<p align="center">
  <a href="#find-the-right-skill">Find a skill</a> ·
  <a href="#in-practice-clearer-project-guidance">Real example</a> ·
  <a href="#cost-aware-coding">Cost-aware coding</a> ·
  <a href="#getting-started">Get started</a> ·
  <a href="docs/astra/design-brief.md">Read the design brief</a>
</p>

---

A capable coding agent still needs to know what matters in your project: which
behavior must stay intact, where a decision belongs, and what would prove a change
works. The **Astra skills pack** combines shared engineering guidance with focused
methods for planning, design, debugging, review, and delivery. Each skill is a
small package of instructions and, where useful, executable tools.

I built it around a practical question: **what guidance earns its place beyond
the model's baseline?** That means keeping useful context and methods, testing
assumptions, and removing instructions that add work without improving decisions.

<details>
<summary><strong>Which models is it for?</strong></summary>

The pack is tuned primarily for **GPT 6 Astra**. Its optional cost-aware workflow
uses Astra Medium for consequential reasoning and final review, Sol Medium for
substantial implementation, and Luna Max for compact bounded work when handoff and
verification stay cheap.

The historical [custom skill pack](skills/custom/) contains more detailed
instructions and remains available for comparison or separate evaluation. The
managed installer deploys only the Astra skills pack, and current model-specific
comparisons are not sufficient to claim that the historical pack performs better
for smaller models.

</details>

## What using it looks like

Suppose an import job sometimes fails halfway through, and you want a safe retry.
After [installation](#getting-started), give Codex a concrete question:

```text
$shape-work Help me design retries for failed imports in this repo.
Some records may already have been saved. Clarify what can be retried safely,
what users should see, and how we will know the feature works.
```

A useful result settles what counts as the same import, how partial progress is
handled, and which outcomes acceptance checks must distinguish. Those decisions
give implementation something concrete to follow. The exact decisions depend on
your repository.

Once the behavior is settled, ask Codex to implement it directly. For other
starting points, [find the right skill](#find-the-right-skill) below.

## Find the right skill

Each linked skill name is a command you can invoke in Codex. **Request explicitly** means
Codex waits for a user request; **Automatic when relevant** means it can select
the skill when the task matches. You can also invoke those skills explicitly.
These are alternative starting points, not a required pipeline.

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

A review or audit alone does not authorize its proposed fixes. Repository setup
can inspect without changing files; request reconciliation when you want edits.

## In practice: clearer project guidance

We used context-hygiene while maintaining this repository. Older architecture
decision records (ADRs) still described retired skill routes, and an index notice
was not enough for someone opening those records directly.

| Before | What changed |
| --- | --- |
| Old ADRs retained historical status and route descriptions without explaining at the top which instructions still apply. | Added scope notices to 17 records and a new decision record explaining what still applies. |
| Domain guidance pointed readers toward ADR history broadly. | Narrowed the route to relevant decisions when rationale or applicability is needed. |
| A completed legacy plan remained under active plans. | Moved it to the archive and updated its links. |

See the [actual cleanup diff](https://github.com/stevennitesh/programming-agent-skills/commit/3f3df36a6befe6d9c221dbd3f2b9252ae34c3f14)
and the [follow-up scope notices](https://github.com/stevennitesh/programming-agent-skills/commit/daf9fd95755e653b632043cfbf9a4605bd7f5995).
The historical ADR bodies were preserved. This demonstrates the resulting
reconciliation, not a measured reduction in tokens or a controlled comparison
against an agent without the skill.

## Cost-aware coding

The optional [$cost-aware-coding](skills/astra/cost-aware-coding/SKILL.md)
workflow reduces expensive Astra lead-token and context churn without weakening the
accepted result. It is explicit-only and uses GPT 6 model roles as part of the
routing policy:

- **Astra Medium** owns consequential reasoning, ambiguous decisions, orchestration,
  exception handling, and final review.
- **Sol Medium** owns substantial repository investigation, implementation,
  debugging, verification, and repair.
- **Luna Max** owns compact bounded tasks with a small self-contained brief and
  cheap verification.

Delegate only when the expected Astra-context savings exceed briefing,
coordination, verification, and recovery overhead. A cheap worker is not a cheap
workflow when Astra must continuously supervise or reconstruct its work.

During delegated implementation, Astra should remain mostly dormant. The worker
owns the checkout until it returns a stable candidate, decisive evidence, material
limits, and released custody. Astra does not shadow the implementation, poll for
routine progress, or consume an implementation transcript. Corrections normally
return to the same worker while its accumulated context remains useful.

When Codex overrides Astra to Sol or Luna, the worker assignment uses
`fork_turns="none"` by default or a small bounded fork when recent turns are
actually cheaper than an explicit brief. Full-history forks inherit the parent
model and effort, so they are not the cost-aware route.

```text
$cost-aware-coding implement the accepted import-retry plan. Keep Astra on
consequential decisions and final review, route coherent implementation to Sol,
and use Luna Max only for compact bounded work.
```

For coordinated serial delivery, the
[planned-delivery reference](skills/astra/cost-aware-coding/references/planned-delivery.md)
adds checkpoints only when early evidence can prevent consequential downstream
rework—for example, an interface, persisted representation, or integration
decision that later work depends on. Checkpoint passes do not replace the final
integrated review.

Recovery follows the actual cause rather than a fixed repair-round allowance.
Requirement, permission, environment, and contradictory-acceptance problems return
to their owner. Local implementation problems normally return to the same worker.
A Luna task that grows beyond its bounded contract moves to Sol. A demonstrated
Sol reasoning failure can escalate Sol **Medium → High → Max** before coherent
implementation is pulled back into Astra. Astra lead reasoning can escalate
**Medium → High → XHigh → Max** when it can materially change a consequential
decision; Ultra is excluded from this serial route because it changes Codex
multi-agent behavior.

When the user explicitly combines cost-aware routing with
[$parallel-implement](skills/astra/parallel-implement/SKILL.md),
parallel-implement owns decomposition, concurrency, lane custody, integration, and
parallel recovery. Cost-aware-coding retains model/effort routing, budget policy,
and final review.

Usage measurement is optional. When it matters, compare equivalent accepted
outcomes and track Astra lead usage separately from Sol/Luna worker usage, handoff
size, corrections, total usage, and wall time. The strongest success signal is a
substantial worker implementation interval with little or no Astra activity,
followed by Astra reviewing a stable candidate.

<a id="install"></a>

## Getting started

You'll need [Codex](https://github.com/openai/codex), Git, and Python 3.11 or newer.
The installer uses only Python's standard library.

Clone the repository, preview the changes, then install:

```sh
git clone https://github.com/stevennitesh/programming-agent-skills.git
cd programming-agent-skills

python -m scripts.install_skills --dry-run
python -m scripts.install_skills
```

On macOS/Linux, use `python3` if needed.

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

## How the pack is developed

The Astra skills pack is being refined through source comparisons, critical reviews, and
focused workflow tests. The repository includes executable helpers and tests
for installation, architecture reports, parallel worktree management, and bounded
session-metadata capture.

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
[contributor instructions](AGENTS.md). Earlier research remains available as historical evidence.

---

[MIT License](LICENSE)
