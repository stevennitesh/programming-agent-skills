# Programming Agent Skills

A skill pack for coding agents that need compact engineering discipline:
clear repo-local contracts, bounded slices, proof, review, and durable language.

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
