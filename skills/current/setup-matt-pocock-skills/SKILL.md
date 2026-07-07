---
name: setup-matt-pocock-skills
description: Configure this repo for the engineering skills — set up its issue tracker, triage label vocabulary, domain doc layout, and engineering contract. Run once before first use of the other engineering skills.
---

# Setup Matt Pocock's Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub by default; local markdown is also supported out of the box)
- **Triage labels** — the category and state label strings used by the triage state machine
- **Domain docs** — where the repo's domain glossary and ADRs live, and the consumer rules for reading them
- **Engineering contract** — the repo-local vocabulary and discipline that give the skills taste: convergence loop, commitment boundary, semantic proof, and scratch cleanup

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` — is this a GitHub repo? Which one?
- `AGENTS.md` and any configured fallback instruction files at the repo root — does either exist? Is there already an `## Agent skills` section, or a portable fallback contract headed `Portable Fallback AGENTS.md For Programming Work`?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/` — does this skill's prior output already exist?
- `.scratch/` — sign that a local-markdown issue tracker convention is already in use

### 2. Present findings and ask

Summarise what's present and what's missing. Then walk the user through the three decisions **one at a time** — present a section, get the user's answer, then move to the next. Don't dump all three at once.

Assume the user does not know what these terms mean. Each section starts with a short explainer (what it is, why these skills need it, what changes if they pick differently). Then show the choices and the default.

**Section A — Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-prd`, `to-issues`, `triage`, `implement`, and `review` read from and write to it. They need to know whether to use the GitHub connector, write markdown under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If a `git remote` points at GitHub, propose that. If a `git remote` points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub** — issues live in the repo's GitHub Issues (uses the GitHub connector)
- **GitLab** — issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Local markdown** — issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.) — ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

If — and only if — the user picked **GitHub** or **GitLab**, ask one follow-up:

> Explainer: Open-source repos often receive feature requests as pull requests, not just issues — a PR is an issue with attached code. If you turn this on, `$triage` pulls *external* PRs into the same queue and runs them through the same labels and states as issues (collaborators' in-flight PRs are left alone). Leave it off if PRs aren't a request surface for you.

- **PRs as a request surface** — yes / no (default: no). Record the answer in `docs/agents/issue-tracker.md`. For local-markdown and other trackers, skip this question — there are no PRs.

**Section B — Triage label vocabulary.**

> Explainer: When the `triage` skill processes an incoming issue or external PR, it applies one category role and one state role. Category says what kind of work it is. State says where it is in the triage machine: needs evaluation, waiting on reporter, ready for an unattended Codex implementation session or delegated implementation subagent, ready for a human, implemented, or won't fix. Map these roles to labels that actually exist in your tracker so the skills apply the right labels instead of creating duplicates.

Category roles:

- `bug` — something is broken
- `enhancement` — new feature or improvement

State roles:

- `needs-triage` — maintainer needs to evaluate
- `needs-info` — waiting on reporter
- `ready-for-agent` — fully specified, ready for an unattended Codex implementation session or delegated implementation subagent
- `ready-for-human` — needs human implementation
- `implemented` — implemented, reviewed, committed, and recorded by an implementation skill
- `wontfix` — will not be actioned

Default: each role's string equals its name. Ask the user if they want to override any. If their issue tracker has no existing labels, the defaults are fine.

Also record `$wayfinder`'s fixed labels: `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, and `wayfinder:task`. These are not triage roles.

**Section C — Domain docs.**

> Explainer: Code-facing skills read the repo's domain glossary and ADRs when codebase context matters. `docs/agents/domain.md` is the router: it points agents to the right `CONTEXT.md`, `CONTEXT-MAP.md`, and relevant ADRs without loading all of them by default.

Confirm the layout:

- **Single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo).

**Section D — Engineering contract.**

> Explainer: Coding execution skills read `docs/agents/engineering-contract.md` when they make or judge repo behavior. `implement`, `tdd`, `diagnosing-bugs`, and `review` consume it directly; `improve-codebase-architecture` uses it when making repo-specific architecture recommendations. Planning, routing, triage, and domain-modeling skills use tracker and domain docs without loading the contract by default.

### 3. Confirm and edit

Show the user a draft of:

- The `## Agent skills` block to add to `AGENTS.md` or the repo's configured Codex instruction file (see step 4 for selection rules)
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`, `docs/agents/engineering-contract.md`

Let them edit before writing.

### 4. Write

**Pick the file to edit:**

- If `AGENTS.md` exists, edit it.
- Else if the repo has a configured Codex fallback instruction file, edit that file.
- If neither exists, ask the user whether to create `AGENTS.md`.

Prefer `AGENTS.md` for Codex. Do not edit unrelated cross-agent instruction files unless the repo's Codex configuration says Codex reads them or the user explicitly asks.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

If the chosen file contains the portable fallback contract, treat setup as a conversion from fallback mode to installed-pack mode:

- Replace the fallback-owned generic sections (`North Star`, `Working Loop`, `Hard Gates`, `Shape Before Build`, `Implementation Taste`, `Review And Report`) with the installed-pack `## Agent skills` block below.
- Preserve clearly repo-specific sections, commands, architecture notes, release rules, and source-of-truth routing.
- Do not leave the fallback coding contract active beside `docs/agents/engineering-contract.md`; that would duplicate the discipline.

The block:

```markdown
## Agent skills

This repo uses the Matt Pocock-style engineering skill pack.

AGENTS primes. Repo-local docs teach. Skills execute.

For nontrivial coding work, read `docs/agents/engineering-contract.md` before editing.

### Pointers

- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label roles: `docs/agents/triage-labels.md`
- Domain docs and ADR routing: `docs/agents/domain.md`
- Engineering contract: `docs/agents/engineering-contract.md`
```

Then write the four docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md) — local-markdown issue tracker
- [triage-labels.md](./triage-labels.md) — label mapping
- [domain.md](./domain.md) — domain doc consumer rules + layout
- [engineering-contract.md](./engineering-contract.md) — agentic coding vocabulary and discipline

Issue tracker docs must record the repo-equivalent operations for creating, fetching, commenting, applying labels, closing, posting ready-for-agent handoff briefs, and `$wayfinder` map/ticket operations.

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

### 5. Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later — re-running this skill is only necessary if they want to switch issue trackers, restart from scratch, or regenerate the engineering contract.
