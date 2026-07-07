# Programming Agent Skills

Programming Agent Skills is a skill pack for preventing AI coding agents from falling into common coding failure modes.

It gives agents and engineers a structured method for designing, implementing, proving, reviewing, and handing off product work with discipline. The pack is not a hidden dispatcher. It is a shared vocabulary plus a set of explicit workflows an agent or human can choose when the shape of the work calls for them.

## Purpose

This pack exists because AI coding agents drift into predictable bad habits: vague scope, shallow exploration, premature implementation, brittle abstractions, weak proof, broad diffs, stale handoffs, and confident summaries without evidence.

It gives agents and engineers durable habits for:

- sharpening vague ideas before code is written
- turning product intent into PRDs and ready-for-agent issues
- implementing one bounded slice at a time
- proving behavior through tests, seams, and useful validation
- reviewing diffs from a fixed point
- preserving domain language, decisions, and handoff context
- keeping large, foggy efforts navigable across sessions

## Philosophy

Build faster without making the repo harder to trust.

The skills favor small, inspectable moves over broad agent autonomy. A good agent run should know its source material, name its scope, protect unrelated work, prove load-bearing behavior, and leave a fresh session enough context to continue.

The pack leans on a few recurring ideas:

- **Leading words**: compact terms like `tracer bullet`, `fixed point`, `fog of war`, and `deep module` carry behavior without long prose.
- **Single source of truth**: setup docs, tracker rules, domain language, and workflow procedures each live in one owning place.
- **Progressive disclosure**: top-level skills own process and boundaries; supporting files own detailed mechanics.
- **Commitment boundaries**: users own requirements, semantics, and product commitments; agents own ordinary implementation technique unless it changes the promised result.
- **Evidence over vibes**: tests, source links, fixtures, logs, diffs, tracker state, and explicit confirmation beat plausible summaries.

## Engineering Contract

Every target repo gets a local `docs/agents/engineering-contract.md` from [`setup-matt-pocock-skills`](skills/current/setup-matt-pocock-skills/SKILL.md). That file is the repo-specific contract for nontrivial coding work: how an agent explores, proves, reviews, locks, and reports changes.

The contract works by activating good engineering habit priors with leading words. Instead of telling an agent every small move to make, it gives compact handles that pull useful behavior from familiar engineering practice:

| Leading word | Source | Meaning | Agent habit it activates |
| --- | --- | --- | --- |
| `convergence loop` | Debugging, design review, and release discipline | `Orient -> Explore -> Choose -> Prove -> Expand -> Converge -> Simplify -> Lock` | Explore without drifting, then force the work toward proof, simplification, and closure. |
| `fixed point` | Code review and diff-based verification | A known starting ref for judging what changed | Review the actual diff instead of the whole repo or the agent's memory of the task. |
| `commitment boundary` | Product ownership, API contracts, and safety review | The line between user-owned outcomes and agent-owned technique | Ask before changing requirements, semantics, public behavior, data meaning, security posture, or scope. |
| `load-bearing internal` | Testing discipline and interface design | Internal behavior that determines whether the requested result is correct | Give correctness-critical internals a contract and prove them through the smallest meaningful seam. |
| `tracer bullet` | Vertical-slice delivery and TDD | One observable path through the real system | Prefer thin end-to-end proof over broad horizontal work that cannot yet prove behavior. |
| `support slice` | Refactoring and migration practice | Behavior-preserving work that unlocks or de-risks tracer bullets | Allow setup work only when it has observable validation and a clear reason. |
| `seam` | Testing, modular design, and adapter patterns | A useful boundary where behavior can be observed, substituted, or protected | Prove behavior at meaningful interfaces instead of mocking owned internals by default. |
| `deep module` | Deep-module design vocabulary | A small interface hiding substantial, coherent behavior | Move complexity behind stable boundaries instead of spreading decisions across callers. |
| `domain language` | Domain-driven design and ADR practice | The repo's accepted words for business concepts and decisions | Preserve shared meaning across code, tests, docs, issues, and reviews. |
| `evidence` | Scientific debugging, CI, and review culture | Source material, tests, fixtures, logs, diffs, command output, screenshots, CI, or explicit confirmation | Replace plausible claims with proof a future maintainer can inspect. |

These words shape agents because language changes the search space. A prompt that says "make a small fix" invites generic coding. A contract that says "orient to the fixed point, keep the bounded slice, prove load-bearing internals through a seam, then lock with evidence" steers the model toward high-quality engineering moves it already has priors for.

## Inspiration

This pack is inspired by [Matt Pocock's AI engineering skills](https://github.com/mattpocock/skills) and by practical multi-session Codex work on real repositories. It borrows the idea that skills should be small, named workflows with strong leading words, then adapts that style for repo-local contracts, issue trackers, long-running agent work, parallel implementation, and source-traced review.

It also draws from common engineering habits: TDD, PRDs, issue triage, domain modeling, deep module design, architecture review, and careful merge-conflict resolution.

## What's Included

- **Shaping**: `grilling`, `grill-with-docs`, `wayfinder`, `research`, `prototype`, `handoff`
- **Product to implementation**: `to-prd`, `to-issues`, `triage`, `implement`, `parallel-implement`
- **Quality loops**: `tdd`, `diagnosing-bugs`, `resolving-merge-conflicts`, `review`, `convergent-pr-review`
- **Design and language**: `domain-modeling`, `codebase-design`, `improve-codebase-architecture`
- **Pack maintenance**: `setup-matt-pocock-skills`, `ask-matt`, `writing-great-skills`

For the installed-pack suggestion map, see [`AGENTS_SKILL_PACK_GUIDE.md`](AGENTS_SKILL_PACK_GUIDE.md).

## Setup

Set `AGENT_SKILLS_DIR` to the skills directory your agent runtime reads. Common locations are `~/.codex/skills`, `~/.claude/skills`, and `~/.agents/skills`.

Install the current active skills:

```bash
: "${AGENT_SKILLS_DIR:?Set AGENT_SKILLS_DIR to your agent's skills directory}"
mkdir -p "$AGENT_SKILLS_DIR"
cp -R skills/current/* "$AGENT_SKILLS_DIR/"
```

PowerShell:

```powershell
$env:AGENT_SKILLS_DIR = "$HOME\.codex\skills"
New-Item -ItemType Directory -Force $env:AGENT_SKILLS_DIR | Out-Null
Copy-Item -Recurse -Force skills/current/* $env:AGENT_SKILLS_DIR
```

Run `setup-matt-pocock-skills` once inside each target repo before using the engineering workflows there. That creates the repo-local issue tracker, triage label, domain, and engineering-contract docs that the skills expect.

`skills/current/` is the supported install set. `skills/extra/` is optional, and `skills/.archive/` is not active.

## Using The Pack

After installation, run `setup-matt-pocock-skills` once in each repo. That creates the repo-local contract the skills read: tracker operations, triage labels, domain routing, and engineering discipline.

Then use skills by naming them directly, or ask `ask-matt` when you know the shape of the work but not the route.

Typical paths:

- Fuzzy idea -> `grill-with-docs` -> `to-prd` -> `to-issues` -> `implement`
- Incoming issue or PR -> `triage` -> `implement`
- Large unclear effort -> `wayfinder` -> `research` / `prototype` / `grilling` tickets -> `to-prd` or `implement`
- Clear behavior change -> `tdd` or `implement`
- Hard bug -> `diagnosing-bugs`
- Risky diff -> `review` or `convergent-pr-review`

## Repository Layout

- `skills/current/`: active skills to install
- `skills/extra/`: optional extra skills
- `skills/.archive/`: inactive historical or experimental skills
- `AGENTS_SKILL_PACK_GUIDE.md`: copyable installed-pack suggestion map
- `docs/synthesis/skill-context-relationships.md`: design-analysis map for skill boundaries and context ownership
- `scripts/validate_skills.py`: integrity checks for the pack

## License

MIT licensed. See [LICENSE](LICENSE).
