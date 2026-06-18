# Programming Agent Skills

A portable skill pack for coding agents working in real software repos.

These skills give coding agents just enough operating structure to learn a repo, clarify scope, plan tracked work, make reviewable source changes, debug from evidence, protect user work, track durable issue or PR context, coordinate subagents, isolate parallel implementation when needed, and verify before claiming success. The goal is better engineering behavior, not a bigger process framework.

The workflows favor fast feedback loops, tracer-bullet slices, ownership-boundary cleanup, pressure-tested skill edits, disposable prototypes, explicit readiness states, and evidence-mapped completion claims.

## Why This Exists

Coding agents often fail in predictable ways. They over-plan, overbuild, trust stale summaries, skip reproduction, edit before understanding the baseline, lose track of user changes, or report completion without fresh evidence.

This pack nudges agents toward a better default:

- Read relevant source, tests, fixtures, logs, docs, diffs, or CI output before acting.
- Choose one useful workflow instead of every possible process.
- Prefer small, reviewable changes over broad rewrites.
- Treat tests, commands, diffs, CI status, and observed behavior as evidence.
- Protect user work and state uncertainty honestly.

## Design Influences

This pack was shaped by a few ideas people in the coding-agent space already recognize: Superpowers-style skill workflows, Matt Pocock's bias toward engineering discipline, and Andrej Karpathy's discussions of agent failure modes and the tradeoffs of coding with agents.

The intent is not to give agents a giant rulebook. It is to steer them toward grounded, scoped, verified work while leaving room for exploration when the task calls for it.

## Who This Is For

- Developers using coding agents to make real repo changes.
- Maintainers who want portable guardrails for coding-agent behavior.
- Teams that want fewer skipped checks, unsafe Git moves, and vague completion claims.
- People who like small reusable procedures more than heavyweight process.

## Quick Start

There are three useful adoption paths.

Use [AGENTS_PORTABLE_FALLBACK.md](AGENTS_PORTABLE_FALLBACK.md) when you want portable global defaults without installing any skills. Copy it into an agent's global instruction location or into a programming repo, using whatever filename that agent host expects, then add repo-specific source-of-truth files, commands, constraints, and release rules.

Use `skills/` when your agent runtime supports loadable skills. Copy the skills you want into your local skill directory, or point your tooling at this repo's `skills/` directory if it supports repo-local skills.

Use [AGENTS_SKILL_PACK_ROUTER.md](AGENTS_SKILL_PACK_ROUTER.md) when you install skills and want a thin global reminder to use one controlling skill or gate when it prevents a concrete failure mode. It can name the full pack without requiring every skill to be installed; unavailable skills should not be simulated.

Set `AGENT_SKILLS_DIR` to the skills directory your agent runtime reads. Common defaults to check:

- Codex: `~/.codex/skills`
- Claude Code: `~/.claude/skills`
- Shared local pack setup: `~/.agents/skills/programming-agent-skills`

Use the directory that directly receives individual skill folders such as `repo-onboarding/`, `coding-router/`, and `verify-before-done/`.

For a full router-compatible setup:

```bash
: "${AGENT_SKILLS_DIR:?Set AGENT_SKILLS_DIR to your agent's skills directory}"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R skills/* "$AGENT_SKILLS_DIR/"
```

For a smaller starter setup with the router and core local skills:

```bash
: "${AGENT_SKILLS_DIR:?Set AGENT_SKILLS_DIR to your agent's skills directory}"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R skills/repo-onboarding "$AGENT_SKILLS_DIR/"
cp -R skills/coding-router "$AGENT_SKILLS_DIR/"
cp -R skills/workspace-safety "$AGENT_SKILLS_DIR/"
cp -R skills/verify-before-done "$AGENT_SKILLS_DIR/"
cp -R skills/tdd-slice "$AGENT_SKILLS_DIR/"
cp -R skills/diagnose-loop "$AGENT_SKILLS_DIR/"
cp -R skills/codebase-cleanup "$AGENT_SKILLS_DIR/"
```

You can copy the whole pack, but you do not have to. If you install only part of the pack, start with `repo-onboarding` for unfamiliar repos, use `coding-router` when you want the agent to choose the right route for actual work, and add the GitHub or subagent skills only when those workflows exist in your environment. If the router selects a skill that is not installed, the agent should not simulate it; it should use the closest installed route only when that prevents the same failure mode, otherwise stay in the default loop and name the missing skill.

## How It Works

Most nontrivial work starts with `coding-router`. It chooses the smallest reliable next workflow based on the request, repo evidence, risk, and expected completion check.

The pack uses two kinds of skills:

- Controlling skills own the main workflow: repo entry, scope, planning, tracked execution, implementation, debugging, cleanup, or skill authoring.
- Gate skills step in at risk boundaries: workspace safety, durable tracking, subagent coordination, worktree isolation for parallel implementation, or final verification.

Typical paths:

- New repo or stale repo context: `repo-onboarding` -> `coding-router` -> selected workflow
- GitHub-backed multi-issue work with explicit checkpoint policy: `issue-driven-execution` -> plan doc and issues -> claim, implement, record evidence, checkpoint, and verify each issue
- Approved feature or behavior change: `coding-router` -> `clarify-scope` only if material behavior or contract remains unresolved, `slice-plan` only if a written multi-step handoff is needed, otherwise `tdd-slice` for the approved caller/user-visible behavior and focused check -> `verify-before-done`
- Bug, failing test, build, CI job, or log error: `coding-router` -> `diagnose-loop` -> focused source change and regression check -> `verify-before-done`
- Cleanup discovery, explicit human-reviewability cleanup, or structure-risk refactor: `coding-router` -> `codebase-cleanup` -> lane-appropriate check -> `verify-before-done`
- PR or review work: `coding-router` -> `pre-pr-review` for semantic review, or `github-tracking` when issue/PR records, claims, blocker/status comments, or CI/review evidence need durable updates; use `verify-before-done` only for explicit readiness, passing, reviewed, safe, or mergeable claims
- Multi-agent implementation: controlling skill -> `subagent-workflow` -> `worktree-isolation` for approved parallel implementation -> parent integration, diff review, and verification

## Skill Map

| Skill | Use it when |
| --- | --- |
| `repo-onboarding` | A coding agent needs to learn an unfamiliar repo's instructions, commands, context, tracker conventions, and safety constraints before work. |
| `coding-router` | A nontrivial repo task needs the right next workflow. |
| `clarify-scope` | Cheap repo evidence cannot resolve a material target behavior, public or caller contract, test, data/security, rollback, ownership, or durable-record decision. |
| `slice-plan` | Approved multi-step repo work truly needs a written plan or handoff with task boundaries, checks, continuity, and final verification. |
| `issue-driven-execution` | Approved GitHub-backed work should become a plan document, issues, one claimed and verified implementation or research issue at a time, and an explicit checkpoint policy. |
| `tdd-slice` | You are implementing or changing one caller-visible or user-visible behavior with a focused check. |
| `diagnose-loop` | Tests, builds, CI, logs, output, crashes, or behavior are failing and the cause is not yet clear. |
| `codebase-cleanup` | Cleanup discovery, continued cleanup, explicit human-reviewability cleanup, duplicated logic, module-boundary or caller-interface cleanup, obsolete-code removal, or behavior-preserving refactors with structure risk. |
| `github-tracking` | Durable GitHub issue/PRD/slice bodies, claim/status/blocker comments, PR/issue links, readiness fields, or CI/review evidence need to be recorded. |
| `pre-pr-review` | A branch, commit, working tree, or PR-ready diff needs a focused semantic review before opening or updating a pull request. |
| `subagent-workflow` | Bounded codebase exploration, implementation, or review can safely run through subagents. |
| `worktree-isolation` | Approved parallel implementation across agents or sessions needs separate branches/worktrees; overlap also needs an integration strategy. |
| `workspace-safety` | Overlapping dirty paths, relevant untracked files, branches, staging, commits, generated output, dependency installs, or risky Git/file operations need care. |
| `verify-before-done` | The agent is about to claim work is done, fixed, reviewed, passing, safe, ready, or mergeable. |
| `author-skills` | You are creating or revising coding-agent skills or skill-pack instructions. |

## What This Is Not

- Not a package manager or runtime framework.
- Not tied to one agent host. `AGENTS_PORTABLE_FALLBACK.md` is portable instruction text for no-skill setups, `AGENTS_SKILL_PACK_ROUTER.md` is a thin router for installed-skill setups, and `skills/` works where the runtime supports skills.
- Not a replacement for repo docs, source code, tests, review, CI, or user instruction.
- Not a rule that every task needs extra process. Tiny safe edits can use a tiny source-read, edit, check loop.
- Not a promise that process creates correctness. Evidence still has to come from the repo and the checks that matter.

## Principles

- Evidence over impressions.
- Source, tests, fixtures, logs, diffs, and CI output over stale summaries.
- One controlling workflow at a time.
- Smallest useful slice before broad rewrites.
- Reproduce bugs before fixing them.
- Preserve existing behavior during refactors unless asked to change it.
- Protect user work, agent work, and unrelated changes.
- Verify before completion claims.
- Use subagents only when delegation is authorized, the work is bounded, and the parent can review the result.

## What This Repo Contains

- `skills/`: reusable coding-agent skills. Each skill has a `SKILL.md` with trigger, purpose, procedure, stop/ask conditions, and handoffs.
- `AGENTS_PORTABLE_FALLBACK.md`: portable global coding-agent instructions for environments that do not install the skill pack.
- `AGENTS_SKILL_PACK_ROUTER.md`: a thinner global router for environments where the skill pack is installed.
- `scripts/validate-skills.sh`: a portable validator for skill metadata, relative skill resource references, README skill-map consistency, optional installed-copy drift, retired vocabulary, public-release hygiene, trailing whitespace, and `git diff --check`.
- `ACKNOWLEDGMENTS.md`: inspiration and no-affiliation notes.
- `LICENSE`: MIT license.

## Status

This is an experimental baseline, but it is not untested. The pack includes static validation and has been exercised against several high-risk workflows during development.

Future revisions are expected as real work exposes weak wording, missing checks, unclear handoffs, or unnecessary process.

## Maintainer Check

For routine local skill edits, run:

```bash
./scripts/validate-skills.sh
```

This checks skill frontmatter, relative skill resource references, the README skill map, retired vocabulary, trailing whitespace in published markdown, and `git diff --check`.

To catch installed-copy drift, set `AGENT_SKILLS_DIR` to the directory your agent runtime reads:

```bash
AGENT_SKILLS_DIR=~/.agents/skills/programming-agent-skills ./scripts/validate-skills.sh
```

When `AGENT_SKILLS_DIR` is set, the validator compares each installed skill that exists in the repo, fails on unknown or stale installed skill folders, and ignores Windows `*:Zone.Identifier` files. Partial installs are allowed by default; set `AGENT_SKILLS_REQUIRE_ALL=1` when you want the validator to require every repo skill in the installed copy. Leave `AGENT_SKILLS_DIR` unset for repo-only validation.

Before publishing or cutting a release, run:

```bash
./scripts/validate-skills.sh --public
```

This adds public-repo hygiene checks for tracked source-corpus paths, ignored local source-corpus directories, stale skill names, local identifiers or secret-like patterns, and Git history/object paths.

## License

MIT. See [LICENSE](LICENSE).
