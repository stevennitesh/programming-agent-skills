# Programming Agent Skills

Programming Agent Skills is a skill pack for coding agents that need compact, repeatable engineering discipline.

It helps an agent move from fuzzy product intent to scoped implementation, proof, review, and handoff without making the repo harder to trust. The pack is not a hidden dispatcher. It is a shared vocabulary plus a set of explicit workflows an agent or human can choose when the shape of the work calls for them.

## Purpose

This pack gives coding agents durable habits for:

- sharpening vague ideas before code is written
- turning product intent into PRDs and ready-for-agent issues
- implementing one bounded slice at a time
- proving behavior through tests, seams, and useful validation
- reviewing diffs from a fixed point
- preserving domain language, decisions, and handoff context
- keeping large, foggy efforts navigable across sessions

The target shape is:

```text
AGENTS.md primes
  -> repo-local docs teach the contract
  -> skills execute the workflow
```

## Philosophy

Build faster without making the repo harder to trust.

The skills favor small, inspectable moves over broad agent autonomy. A good agent run should know its source material, name its scope, protect unrelated work, prove load-bearing behavior, and leave a fresh session enough context to continue.

The pack leans on a few recurring ideas:

- **Leading words**: compact terms like `tracer bullet`, `fixed point`, `fog of war`, and `deep module` carry behavior without long prose.
- **Single source of truth**: setup docs, tracker rules, domain language, and workflow procedures each live in one owning place.
- **Progressive disclosure**: top-level skills own process and boundaries; supporting files own detailed mechanics.
- **Commitment boundaries**: users own requirements, semantics, and product commitments; agents own ordinary implementation technique unless it changes the promised result.
- **Evidence over vibes**: tests, source links, fixtures, logs, diffs, tracker state, and explicit confirmation beat plausible summaries.

## Inspiration

This pack is inspired by Matt Pocock's AI engineering skills and by practical multi-session Codex work on real repositories. It borrows the idea that skills should be small, named workflows with strong leading words, then adapts that style for repo-local contracts, issue trackers, long-running agent work, parallel implementation, and source-traced review.

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

## Repository Layout

- `skills/current/`: active skills to install
- `skills/extra/`: optional extra skills
- `skills/.archive/`: inactive historical or experimental skills
- `AGENTS_SKILL_PACK_GUIDE.md`: copyable installed-pack suggestion map
- `docs/synthesis/skill-context-relationships.md`: design-analysis map for skill boundaries and context ownership
- `scripts/validate_skills.py`: integrity checks for the pack

## License

MIT licensed. See [LICENSE](LICENSE).
