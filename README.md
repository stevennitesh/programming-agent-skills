<h1 align="center">Programming Agent Skills</h1>

<p align="center"><strong>Engineering judgment for Codex, without turning every task into a process.</strong></p>

<p align="center">
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white">
</p>

Coding agents can move fast and still leave a mess: speculative abstractions,
defensive checks nobody needed, compatibility paths with no real consumer, and
green tests that never touch the behavior a user depends on.

I built this pack to push Codex toward better engineering judgment without
turning an ordinary task into a compliance exercise. It combines a shared
engineering contract with focused skills for shaping work, designing code,
implementation, diagnosis, delivery, and review.

Ordinary work stays ordinary. Heavier methods activate when the request, the
repository, or a concrete risk calls for them.

[Install the full pack](#install) ·
[Use only the portable contract](AGENTS_PORTABLE_FALLBACK.md) ·
[Browse the skills](#what-is-in-the-pack)

## The philosophy

> Explore imaginatively. Converge under proof. Simplify ruthlessly.

The pack teaches Codex to understand the code before changing it, choose the
smallest integrated design, and prove the result through a caller or artifact
that matters. It favors readable code, clear data shapes, small interfaces,
local state, and one obvious owner for each behavior.

It also applies YAGNI with some conviction. A local feature does not need a
framework for imagined future requirements. Internal code does not need to
defend against states its types and established invariants already exclude.
Tests are evidence, not a quota. Documentation should explain a real contract
or decision, not restate readable code.

For one bounded implementation, the common path is deliberately short:

1. Understand the request, current behavior, real callers, and existing proof.
2. Choose the smallest sound design and a clear data shape.
3. Implement the whole change in the current behavior owner.
4. Run the nearest useful check that can fail for the changed behavior.
5. Inspect the result, remove displaced code, and stop.

Risk changes the method. The skills that own external writes, destructive work,
concurrent delivery, recovery, formal review, and measured claims activate the
extra protection those jobs require. If the condition is absent, it creates no
checklist, artifact, reviewer, or explanation obligation.

## What is in the pack

Each skill owns one recognizable engineering job. They compose when the work
needs more than one job, but they are not a mandatory pipeline.

| Area | Skills | Use for |
| --- | --- | --- |
| Build and improve | `$implement`, `$diagnosing-bugs`, `$codebase-design`, `$simplify-code`, `$hillclimb`, `$tdd` | Implementation, hard bugs, a design recommendation for one bounded module or interface, simplification, measured improvement, and test-first work. |
| Shape decisions | `$grilling`, `$grill-with-docs`, `$research`, `$prototype`, `$domain-modeling`, `$wayfinder`, `$to-questionnaire` | Live decisions, evidence, design probes, domain meaning, coupled multi-session decision routes, and drafting a questionnaire for an external stakeholder. |
| Plan and deliver | `$to-spec`, `$to-tickets`, `$parallel-implement`, `$triage`, `$handoff` | Durable specs, ticket graphs, parallel delivery, incoming tracker work, and continuation in a fresh context. |
| Review and conflict resolution | `$change-review`, `$high-assurance-review`, `$audit-codebase`, `$resolving-merge-conflicts` | Change review, explicitly heavy review, organized codebase audits, and inspecting or resolving an active Git conflict. |
| Setup and instructions | `$repo-bootstrap`, `$skill-router`, `$writing-for-agents`, `$context-hygiene`, `$wizard` | Repository setup, skill selection, instructions for agents, persistent-context hygiene, and guided scripts for procedures only a human can perform. |

The active skills live in [`skills/custom/`](skills/custom). Optional skills
live in [`skills/extra/`](skills/extra) and are not part of the managed install.

### Recommended companion

For clearer, more natural communication with coding agents, I recommend
pstack's [`unslop`](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop)
skill. It cleans up agent-written prose without changing its meaning. This
repository does not bundle or manage it, so install it separately from the
upstream project.

## Install

You need [Codex](https://github.com/openai/codex), Git, and Python 3.11 or
newer. GitHub or GitLab authentication is optional. The pack can also use a
local Markdown tracker.

By default, the installer manages this pack's skills under
`$HOME/.agents/skills` and its small bootstrap section in
`$HOME/.codex/AGENTS.md`. It preserves unrelated skills and personal global
instructions. Add `--skip-global-agents` to both installer commands if you want
to leave the global `AGENTS.md` untouched.

Preview the affected skills and bootstrap action, then install them. The
installer uses only the Python standard library.

Bash:

```bash
git clone https://github.com/stevennitesh/programming-agent-skills.git
cd programming-agent-skills

python3 -m scripts.install_skills --dry-run
python3 -m scripts.install_skills
```

PowerShell:

```powershell
git clone https://github.com/stevennitesh/programming-agent-skills.git
Set-Location programming-agent-skills

python -m scripts.install_skills --dry-run
python -m scripts.install_skills
```

Pull the repository and run the same commands to update.

See [installation and recovery](INSTALLATION.md) for custom locations, how the
installer handles global `AGENTS.md`, optional installed-parity validation,
transaction recovery, and directory ownership.

## Use it

After installation, you can invoke a skill directly:

```text
$implement issue 123
```

If a repository should carry the pack's engineering, tracker, label, or domain
setup, run `$repo-bootstrap`. It inspects what is missing or outdated, shows the
proposed change, and waits for approval before writing anything. You can skip
it when the repository already has the instructions the work needs.

Ask Codex for the work you want. Context-enabled skills can be selected from
their descriptions. Use a skill's `$`-prefixed name when you want a specific
workflow or when the skill is intentionally explicit-only.

```text
$diagnosing-bugs investigate why the import sometimes stalls

$simplify-code src/billing/reconciliation.py

$high-assurance-review the completed ticket graph before merge
```

Use `$skill-router` when choosing the next skill is itself the question. It
returns one skill name or `none`, then stops. It does not start that skill.

You do not need a specification or ticket graph for every change.

- Use `$implement` for one ready, bounded item.
- Use `$to-spec` to publish a settled decision that needs to survive several
  slices or sessions.
- Use `$to-tickets` to publish a graph when settled work benefits from
  dependency-ordered delivery.
- Use `$parallel-implement` for an explicit set of at least two accepted items
  with a ready frontier and independent behavior ownership and write effects.

<details>
<summary>Skills that require explicit invocation</summary>

`$audit-codebase`, `$diagnosing-bugs`, `$handoff`,
`$high-assurance-review`, `$hillclimb`, `$implement`,
`$parallel-implement`, `$repo-bootstrap`, `$simplify-code`, `$skill-router`,
`$to-questionnaire`, `$to-spec`, `$to-tickets`, `$triage`, `$wayfinder`, and
`$wizard` do not activate from context alone.

</details>

## The engineering contract

[`$repo-bootstrap`](skills/custom/repo-bootstrap/SKILL.md) can install the
shared [`engineering-contract.md`](docs/agents/engineering-contract.md). The
contract defines the pack's coding defaults; skills define procedures for
particular jobs. Repository instructions and the user remain authoritative.

Its advice is concrete: trace the current owner and real callers, subtract
before adding, model the domain instead of scattering conditionals, validate
untrusted input once at its owning boundary, trust valid internal
representations, remove displaced paths, and prove only what the result claims.
It is engineering taste, not a checklist or review gate.

If you want the engineering defaults without the skills, copy
[`AGENTS_PORTABLE_FALLBACK.md`](AGENTS_PORTABLE_FALLBACK.md) to your global
Codex `AGENTS.md`. It needs no installer or Python runtime. It leaves out skill
routing, specialized workflows, tracker setup, templates, and managed updates.

## Where this came from

This pack began with
[Matt Pocock's engineering skills](https://github.com/mattpocock/skills) and
also draws on [pstack](https://github.com/cursor/plugins/tree/main/pstack),
[Ponytail](https://github.com/DietrichGebert/ponytail), and
[Superpowers](https://github.com/obra/superpowers). Matt's work shaped the
short, named workflows. Pstack pushed the engineering guidance toward smaller,
clearer designs. Ponytail reinforced the YAGNI ladder: do not build, reuse,
reach for the platform, then add the minimum that works. This repository adapts
those ideas for Codex and adds narrow controls for external writes, parallel
work, recovery, trackers, and source-backed review.

See [Acknowledgments](ACKNOWLEDGMENTS.md) for the broader list of influences.

## For contributors

- [`skills/custom/`](skills/custom): active skills installed by the pack
- [`skills/experimental/`](skills/experimental): inactive alternatives
- [`skills/extra/`](skills/extra): optional skills outside the managed install
- [`CONTEXT.md`](CONTEXT.md): stable repository vocabulary and ownership
- [`docs/synthesis/`](docs/synthesis): design decisions and source-backed
  reasoning behind the runtime skills
- [`scripts/install_skills.py`](scripts/install_skills.py): managed installer
- [`scripts/validate_skills.py`](scripts/validate_skills.py): pack validation

## License

MIT licensed. See [LICENSE](LICENSE).
