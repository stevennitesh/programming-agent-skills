# Programming Agent Skills

AI coding agents are already astonishingly fast. The breakthrough is making that speed dependable by giving Codex the habits of a strong senior engineer: clarify intent before coding, work in bounded slices, prove the behavior that matters, review the real diff, and leave the repository easier to trust.

Programming Agent Skills is a Codex-first skill pack built around that idea. It turns fuzzy requests into named workflows, keeps product commitments with the human, gives implementation technique to the agent, and puts evidence gates between "looks done" and done.

## Purpose

Fast agents fail in predictable ways: vague scope, shallow exploration, premature implementation, brittle abstractions, weak proof, broad diffs, stale handoffs, and confident summaries without evidence.

This pack turns those failure modes into small, composable workflows. Each skill owns one engineering job; together they cover the path from an unclear idea to a verified change:

- sharpen intent before code is written;
- turn product decisions into specs and ready-for-agent tickets;
- implement one bounded slice at a time;
- prove behavior through meaningful seams and focused feedback loops;
- review the actual diff from a fixed point;
- preserve domain language, decisions, evidence, and handoff state;
- keep large, foggy efforts navigable across sessions.

The payoff is visible uncertainty, inspectable proof, and named residual risk before work is accepted.

## Philosophy

Build faster without making the repo harder to trust.

Move quickly through reversible exploration. Slow down at the gates that protect commitments, correctness, and trust.

- **Shape before build**: turn unclear intent into a grilling session, spec, wayfinding map, research note, or prototype before implementation starts.
- **Tracer bullets**: deliver observable vertical slices that keep proof close to each change.
- **Semantic proof**: prove that the result means the right thing; output existence alone is not correctness.
- **Fixed-point review**: judge the actual diff against Spec and Standards instead of trusting the agent's story.
- **Ubiquitous language**: preserve domain terms and decisions across code, tests, docs, tickets, and handoffs.
- **One owner**: skills own workflows, repo docs own local contracts, and supporting files own detailed mechanics.

## Engineering Contract

[`$repo-bootstrap`](skills/custom/repo-bootstrap/SKILL.md) installs a small `docs/agents/engineering-contract.md` in each target repo. The contract gives Codex strong handles for the decisions that matter while leaving implementation technique flexible.

The shared loop is `Orient -> Explore -> Decide -> Prove -> Cover -> Converge -> Simplify -> Lock`. A **source trace** grounds the work. A **bounded slice** controls scope. **Semantic proof** establishes that the result means the right thing. A **fixed point** anchors review. Separate **Spec / Standards** passes ask "right thing?" and "built right?" independently. **Lock** closes only with evidence and named residual risk.

That compact vocabulary recruits senior engineering habits while keeping prompts and workflows small.

## Inspiration

This pack started with [Matt Pocock's engineering skills](https://github.com/mattpocock/skills), which showed how powerful small, named, composable workflows can be. This repository is a Codex-first adaptation shaped by practical multi-session work on real codebases.

It keeps the upstream emphasis on strong leading words, then extends it with repo-local contracts, tracker-backed delivery, long-running wayfinding, isolated parallel implementation, source-traced review, TDD, domain modeling, deep module design, architecture review, and careful conflict resolution.

## What's Included

- **Shape before building**: `$grilling`, `$grill-with-docs`, `$wayfinder`, `$research`, `$prototype`, `$handoff`
- **Turn intent into delivery**: `$to-spec`, `$to-tickets`, `$triage`, `$implement`, `$parallel-implement`
- **Prove and protect behavior**: `$tdd`, `$diagnosing-bugs`, `$resolving-merge-conflicts`, `$review`, `$convergent-pr-review`
- **Deepen design and language**: `$domain-modeling`, `$codebase-design`, `$improve-codebase-architecture`
- **Route and maintain the pack**: `$repo-bootstrap`, `$skill-router`, `$writing-great-skills`

The small [`GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md`](GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md) bootstrap teaches Codex when to suggest `$skill-router` and `$repo-bootstrap`. Workflows stay with their skills, and personal global instructions stay local.

## Setup

Requirements: Codex, Git, and Python 3.10 or newer. GitHub or GitLab authentication is optional; the pack can use a local Markdown tracker.

Codex reads global skills from `$HOME/.agents/skills` and global instructions from `$HOME/.codex/AGENTS.md`.

Clone the repository and install the active skills.

Bash:

```bash
git clone https://github.com/stevennitesh/programming-agent-skills.git
cd programming-agent-skills

python -m scripts.install_skills
python -m scripts.validate_skills --installed-root "$HOME/.agents/skills" --require-installed
```

PowerShell:

```powershell
git clone https://github.com/stevennitesh/programming-agent-skills.git
Set-Location programming-agent-skills

python -m scripts.install_skills
python -m scripts.validate_skills --installed-root "$HOME\.agents\skills" --require-installed
```

The installer creates or updates only the template's `## Skill Pack Bootstrap` section, migrates the legacy `## Skill Pack Guide` block, and preserves personal global instructions. It records pack-managed skills in `$HOME/.agents/skills/.programming-agent-skills-manifest.json`, so updates can retire old pack skills without touching unrelated personal skills. Use `python -m scripts.install_skills --dry-run` to report skill deltas and the global-bootstrap action.

`skills/custom/` is the supported install set. `skills/extra/` is optional, and `skills/.archive/` is not active.

## Using The Pack

Start in each target repo with `$repo-bootstrap`. It inventories the repo, resolves tracker, label, and domain-layout choices, shows the exact proposed changes, waits for approval, then provisions and verifies the local setup surface. Run it again after pack upgrades: it reconciles existing setup, carries forward confirmed choices and repo-specific additions, and proposes only the required delta.

After setup, invoke a skill directly or let `$skill-router` carry the route map. The router recommends exactly one next skill and stops.

Representative paths:

- Fuzzy product idea needing durable decisions -> `$grill-with-docs` -> `$to-spec` -> `$to-tickets`
- One bounded ready item -> `$implement`; parallel-safe ready frontier -> `$parallel-implement`
- Incoming issue or configured external PR -> `$triage`; ready-for-agent item -> `$implement`
- Multi-session fog of war -> `$wayfinder` until the map closes -> `$to-spec`, `$to-tickets`, or `$implement`
- Known behavior with a red-capable seam -> `$tdd`; uncertain symptom, cause, or reproduction -> `$diagnosing-bugs`
- Ordinary diff -> `$review`; local PR or high-risk diff -> `$convergent-pr-review`

These are examples. `$skill-router` owns the complete route map and tie-breakers.

## Repository Layout

- `skills/custom/`: active skills to install
- `skills/extra/`: optional extra skills
- `skills/.archive/`: inactive historical or experimental skills
- `GLOBAL_AGENTS_TEMPLATE_SKILL_PACK.md`: minimal global Codex bootstrap
- `skills/custom/repo-bootstrap/`: target-repo setup workflow and contract templates
- `CONTEXT.md`: stable vocabulary and maintenance invariants for this repository
- `docs/synthesis/skill-context-relationships.md`: maintainer map for skill boundaries and context ownership
- `scripts/install_skills.py`: managed install and update that preserves unrelated skills
- `scripts/validate_skills.py`: integrity checks for the pack

## License

MIT licensed. See [LICENSE](LICENSE).
