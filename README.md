# Programming Agent Skills

A skill pack for coding agents that need compact engineering discipline:
clear repo-local contracts, bounded slices, proof, review, and durable language.

The pack is organized around a suggestion map, not a hidden dispatcher. It gives
agents and humans shared routing vocabulary, then leaves each skill and
repo-local doc to own its procedure.

The pack's target shape is:

```text
AGENTS.md primes
  -> docs/agents/engineering-contract.md teaches the discipline
  -> skills execute the workflow
```

## Setup

Set `AGENT_SKILLS_DIR` to the skills directory your agent runtime reads.
Common locations are `~/.codex/skills`, `~/.claude/skills`, and
`~/.agents/skills`.

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

Run `setup-matt-pocock-skills` inside each target repo before first use.

## Suggestion Map

Use the map when you know the shape of the work but not the best skill. The
copyable installed-pack guide lives in
[`AGENTS_SKILL_PACK_GUIDE.md`](AGENTS_SKILL_PACK_GUIDE.md).
Recommend `ask-matt` when route choice itself is the work.

North star: build faster without making the repo harder to trust.

Routing handles:

- **grilling session**: reduce ambiguity before building.
- **wayfinding map**: make fog of war visible.
- **prototype**: answer one design question by trying it.
- **PRD**: preserve product intent beyond the current thread.
- **ready-for-agent**: specific enough for a fresh implementation session.
- **fixed-point review**: review a diff from a known starting point.
- **convergent review**: use independent passes when one review is not enough.
- **handoff**: preserve workflow state for a fresh session.

Shaping before implementation:

- `grill-with-docs` when product intent is foggy and repo context matters.
- `grilling` when the user needs a grilling session without repo-doc work.
- `wayfinder` when unresolved decisions block a PRD, plan, or implementation.
- `prototype` when conversation cannot settle a design question without trying it.
- `handoff` when context must cross sessions.

Product to implementation:

- `to-prd` when a multi-session idea needs a durable parent PRD before implementation issues.
- `to-issues` when a PRD, spec, plan, or parent issue should become dependency-ordered, ready-for-agent tracer-bullet issues.
- `triage` when incoming issues or external PRs need state roles and ready-for-agent briefs.
- `implement` when one ready-for-agent issue should be implemented, verified, reviewed, committed, and noted.
- `parallel-implement` when a parent, packet, or batch of ready-for-agent issues should be implemented through delegated workers and serialized integration.

Quality loops:

- `tdd` when behavior is clear enough for red-green-refactor.
- `diagnosing-bugs` when the symptom, cause, or reproduction is uncertain.
- `review` when an ordinary branch or work-in-progress diff needs fixed-point Standards and Spec review.
- `convergent-pr-review` when a local PR review or high-risk local-diff review needs independent passes, a finding ledger, and patch-ready triage.

Design and language:

- `domain-modeling` for shared language, glossary terms, or ADR-worthy decisions.
- `codebase-design` for module, interface, seam, adapter, depth, leverage, and locality vocabulary.
- `improve-codebase-architecture` for architecture review and deepening candidates.
- `writing-great-skills` for skill language, invocation, context load, and predictability.
- `setup-matt-pocock-skills` when a repo needs the issue tracker, triage labels, domain docs, or engineering contract expected by the pack.

The map may name leading words and suggest one next route. It does not teach
skill procedures, tracker operations, repo-specific domain rules, label policy,
engineering-contract discipline, or invocation mechanics.

## Doc Map

- `AGENTS.md`: agent boot commands, pointers, and costly-mistake invariants.
- `CONTEXT.md`: stable vocabulary, workflow model, artifact ownership, and
  durable repo rules.
- `docs/plans/README.md`: current work and runbook router.
- `docs/agents/`: issue tracker, triage labels, domain routing, and
  engineering contract for repos using the skill pack.
- `docs/adr/`: durable decisions.
- `docs/research/`, `docs/synthesis/`, `docs/validation/`: evidence and
  workbench lanes; enter through `docs/plans/README.md` only when current.
- `pyproject.toml`: pytest defaults.
- `scripts/`: focused test and validation wrappers.

Routine setup, test, and validation commands live in `AGENTS.md`.

## License

MIT. See [LICENSE](LICENSE).
