<h1 align="center">Programming Agent Skills</h1>

<p align="center">
  Workflows for coding agents: planning changes, research, debugging, code review, and repository maintenance.
</p>

<p align="center">
  <img src="docs/astra/assets/programming-agent-skills-hero.png" width="960" alt="Programming Agent Skills, illustrated with modules bearing code, graph, and settings icons.">
</p>

<p align="center">
  <a href="https://github.com/stevennitesh/programming-agent-skills/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/stevennitesh/programming-agent-skills/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://github.com/stevennitesh/programming-agent-skills/releases/latest"><img alt="Latest tagged release" src="https://img.shields.io/github/v/release/stevennitesh/programming-agent-skills"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
</p>

<p align="center">
  <a href="#getting-started">Get started</a> ·
  <a href="#what-you-can-ask-an-agent-to-do">Uses</a> ·
  <a href="#engineering-and-evidence">Implementation and tests</a> ·
  <a href="#find-the-right-skill">Find a skill</a> ·
  <a href="#models-and-hosts">Models and hosts</a> ·
  <a href="docs/astra/design-brief.md">Design brief</a>
</p>

---

Programming Agent Skills contains 20 workflows that an agent can load for a
specific task. Each skill describes when to use it, what work it covers, and
what result to return. The managed installer deploys the pack for Codex.

Programmers can request a named workflow or let the agent select an automatic
skill when it matches the task. The instructions specify which work is in scope,
what needs checking, and what a completed result includes. The agent chooses its
methods within those boundaries and the repository's requirements. For a clear,
bounded code change, ask the agent to implement and verify it directly.

## What you can ask an agent to do

- Develop an idea into agreed behavior and a specification with
  [shape-work](skills/astra/shape-work/SKILL.md). Resolve requirements before
  asking for implementation.
- Investigate a question or compare options with
  [research](skills/astra/research/SKILL.md). Get an answer with sources,
  uncertainty, and any gaps in the evidence.
- Investigate a difficult failure with
  [diagnosing-bugs](skills/astra/diagnosing-bugs/SKILL.md). Use observed behavior
  to distinguish likely causes and identify what failed.
- Review a proposed code change with
  [change-review](skills/astra/change-review/SKILL.md). Get findings that identify
  an affected behavior, supporting evidence, and a correction.
- Maintain repository guidance or analyze conversations and tool logs with
  [context-hygiene](skills/astra/context-hygiene/SKILL.md). Identify recurring
  problems in instructions, tools, or the agent runtime. Recommend or apply
  corrections within the authorized task.
- Coordinate requested concurrent implementation with
  [parallel-implement](skills/astra/parallel-implement/SKILL.md). Assign each agent
  a task and the files or components it owns. Check the combined changes against
  the agreed requirements.

These workflows can be used individually. The [full catalog](#find-the-right-skill)
also covers design decisions, experiments, ticketing, Git cleanup, verification
tools, and other tasks.

## Models and hosts

The skills were developed primarily for GPT 6 Astra and are intended for other
capable coding models, including Sol 6.1, Opus 5.5, Fable 5.1, and Sonnet 5.5.
The current managed pack lives in `skills/astra/`.

The managed integration targets Codex. Hosts differ in how they load skills,
select them automatically, and provide tools or subagents. Other hosts would
need their own installation and tool integration. Package checks do not
establish equivalent results across models.

The optional [cost-aware workflow](#cost-aware-coding) has specific model
assignments documented in its [model policy](skills/astra/cost-aware-coding/references/model-policy.md).

<details>
<summary><strong>Historical custom pack</strong></summary>

The historical [custom skill pack](skills/custom/) remains available for
comparison and separate evaluation, but it is not installed by the current
installer. Current model-specific comparisons are not sufficient to claim that
the historical package performs better for smaller models.

</details>

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

These commands install the current **`main` branch**. The release badge links
to a tagged snapshot, whose skill inventory and guidance may differ from `main`.
To install a release instead, check out its tag before running the installer
and consult its [release notes](https://github.com/stevennitesh/programming-agent-skills/releases).

The installer deploys `skills/astra/` to `$HOME/.agents/skills` and manages a
small bootstrap section in `$HOME/.codex/AGENTS.md`. It preserves unrelated
skills and personal instructions and refuses unsafe ownership conflicts. Use
`--skip-global-agents` if you want the skills without changing global
instructions.

After installation:

- for a clear bounded code change, **just ask Codex to implement it**;
- invoke a named skill such as `$shape-work` when you want an explicit workflow;
- automatic skills can be selected by Codex when the request matches their scope.

To update a `main` checkout, pull this repository and repeat the preview/install
commands. For a release checkout, fetch tags and select the release you want
before repeating those commands. See
[installation and recovery](INSTALLATION.md) for migration, custom targets,
installed-pack validation, and transaction recovery.

Without the managed skills, [AGENTS_PORTABLE_FALLBACK.md](AGENTS_PORTABLE_FALLBACK.md)
is an optional short starting point for global preferences and repository routing.

## How it fits together

Repository guidance records project facts and accepted decisions. Skills describe
procedures for particular tasks.

| Component | Role | When to use it |
| --- | --- | --- |
| Repository `AGENTS.md` | Verified commands, local constraints, and pointers | Read first in a repository |
| Repository context and decisions | Project meaning, source boundaries, and durable decisions | When the task depends on project-specific meaning |
| Direct coding | Normal implementation under repository guidance | Default for a clear bounded change |
| Managed skills | Procedures for specific tasks, with scope and completion conditions | When the task matches that skill |
| Historical research and evaluation | Earlier findings and pack designs | Use for past decisions and findings; current guidance governs the work |

In this repository, [AGENTS.md](AGENTS.md) lists contributor commands and
constraints. [CONTEXT.md](CONTEXT.md) identifies the managed source and historical
packages. The [Astra design brief](docs/astra/design-brief.md) explains the current
pack's design decisions. Each `skills/astra/*/SKILL.md` file describes how to run
that workflow.

## Find the right skill

**Request explicitly** means Codex waits for you to invoke or request that
workflow. **Automatic when relevant** means Codex may select it when your request
matches. You can also invoke an automatic skill explicitly.

<details>
<summary><strong>Full catalog: all 20 skills and their invocation rules</strong></summary>

| Your task | Skill | Use |
| --- | --- | --- |
| Implement a clear, bounded change | Ask Codex to implement and verify using repository guidance | Direct |
| Develop an idea into an agreed spec, or reconcile domain meaning and decision records | [$shape-work](skills/astra/shape-work/SKILL.md) | Request explicitly |
| Resolve code reuse, ownership, simplification, or integration decisions | [$codebase-design](skills/astra/codebase-design/SKILL.md) | Automatic when relevant |
| Test an uncertain approach with a runnable experiment | [$prototype](skills/astra/prototype/SKILL.md) | Automatic when relevant |
| Create or improve reusable tools for agents to exercise and verify product interfaces | [$verification-harness](skills/astra/verification-harness/SKILL.md) | Request explicitly |
| Research a question or compare options using sources | [$research](skills/astra/research/SKILL.md) | Automatic when relevant |
| Find the root cause of a difficult bug | [$diagnosing-bugs](skills/astra/diagnosing-bugs/SKILL.md) | Automatic when relevant |
| Discover codebase improvements through an HTML map and scoped audits | [$audit-codebase](skills/astra/audit-codebase/SKILL.md) | Request explicitly |
| Optimize a measurable outcome through experiments | [$hillclimb](skills/astra/hillclimb/SKILL.md) | Request explicitly |
| Review a code change for correctness and maintainability | [$change-review](skills/astra/change-review/SKILL.md) | Automatic when relevant |
| Assess intake or clean up a requested backlog using current evidence | [$triage](skills/astra/triage/SKILL.md) | Request explicitly |
| Turn a spec or sufficiently clear idea into bounded tickets with dependencies | [$to-tickets](skills/astra/to-tickets/SKILL.md) | Request explicitly |
| Implement concurrently with separate ownership and clear dependencies | [$parallel-implement](skills/astra/parallel-implement/SKILL.md) | Request explicitly |
| Assign work to GPT 6 models while the lead retains decisions and review | [$cost-aware-coding](skills/astra/cost-aware-coding/SKILL.md) | Request explicitly |
| Resolve an active Git merge or rebase conflict | [$resolving-merge-conflicts](skills/astra/resolving-merge-conflicts/SKILL.md) | Automatic when relevant |
| Assess branches and worktrees, integrate worthwhile work when requested, and clean up safely | [$git-cleanup](skills/astra/git-cleanup/SKILL.md) | Request explicitly |
| Make a project's portfolio artifacts coherent, understandable, and supported by evidence | [$portfolio-presentation](skills/astra/portfolio-presentation/SKILL.md) | Request explicitly |
| Establish repository agent guidance or migrate its setup | [$repo-bootstrap](skills/astra/repo-bootstrap/SKILL.md) | Request explicitly |
| Write or audit reusable agent guidance, a consequential assignment, or a handoff | [$writing-for-agents](skills/astra/writing-for-agents/SKILL.md) | Automatic when relevant |
| Maintain repository context and durable memory, or analyze agent sessions for reusable context and harness improvements | [$context-hygiene](skills/astra/context-hygiene/SKILL.md) | Automatic when relevant |
| Guide a private human step through the terminal and safely hand control back | [$wizard](skills/astra/wizard/SKILL.md) | Request explicitly |

</details>

For one positive request and one realistic near-miss for every skill, see
[canonical skill selection examples](docs/astra/selection-examples.md).

A review or audit does not itself request fixes. A specification or ticket does
not itself request implementation. Work proceeds under the user's existing
authorization. Selecting context-hygiene does not grant permission for unrelated
audits or memory writes. Memory changes need an explicit request and the host's
supported update process.

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
explicit workflow for assigning tasks to specific models. The user's starting
lead agent retains planning, consequential decisions, and final review. Workers
choose their methods within assigned scope.

The skill documents model selection, worker assignments, recovery, and optional
usage logs. For requested concurrent implementation,
[$parallel-implement](skills/astra/parallel-implement/SKILL.md) coordinates worker
ownership and integration. The goal is to reduce lead-model token use and
unnecessary context transfers. Assess cost across the whole task, including
handoffs, review, and repair; savings need to be measured.

## Engineering and evidence

This repository develops the workflow boundaries, packaging, and helper tools
around ideas credited in [Acknowledgments](ACKNOWLEDGMENTS.md):

- Each skill names the task it covers and the nearby tasks it excludes.
  Longer instructions for specific cases live in linked references. The
  [selection examples](docs/astra/selection-examples.md) show a matching request
  and a realistic non-match for every managed skill.
- The [installer](scripts/install_skills.py)
  tracks ownership, previews updates, preserves unrelated skills, and records
  transactions for recovery. It refuses to replace modified managed copies or
  silently adopt unmanaged copies with the same name.
- The pack includes a
  [Git worktree helper](skills/astra/parallel-implement/scripts/lane_worktree.py),
  a [codebase atlas generator](skills/astra/audit-codebase/scripts/atlas.py), and
  optional [cost telemetry](skills/astra/cost-aware-coding/scripts/telemetry.py).
  The [validator](scripts/validate_skills.py) checks package resources, references,
  catalog invocation rules, and installed copies against their source when requested.

For a concrete example, the [modified-skill test](tests/test_install_skills.py#L1208-L1226)
installs a fixture skill, edits its installed copy, then attempts an update.
It checks that the update is rejected and both the skill tree and global
instructions remain unchanged. A separate
[recovery test](tests/test_install_skills.py#L558-L596) injects a cleanup failure
after an update commits, then checks that recovery retains the new version and
clears the transaction. These are controlled tests of installer behavior.

[CI](https://github.com/stevennitesh/programming-agent-skills/actions/workflows/ci.yml)
runs public package validation and the full test suite on Ubuntu and Windows.
These checks establish specific structural and mechanical behavior. They do
**not** establish better generated code, lower total cost, or equivalent results
across models.

## What belongs in repository guidance

Keep information that changes decisions: actual commands, non-obvious constraints,
accepted behavior and compatibility requirements, and the user's priorities.
Leave methods to the agent within those boundaries. A separate guide is useful
for substantial project-specific requirements; a general engineering-contract
file is not required or supplied by bootstrap.

## Project status and evidence

The pack is refined through source comparison, critical review, focused workflow
tests, and real repository use. [Engineering and evidence](#engineering-and-evidence)
provides examples of the checked package behavior and its limits.

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
[CONTRIBUTING.md](CONTRIBUTING.md), then follow [AGENTS.md](AGENTS.md),
[CONTEXT.md](CONTEXT.md), and the
[Astra design brief](docs/astra/design-brief.md). The managed source is
[skills/astra/](skills/astra/).

---

[MIT License](LICENSE)
