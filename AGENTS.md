# Repository Instructions

<!-- programming-agent-skills setup-schema: 1:859a503ba864 -->

## Commands

- Create the repo environment if needed: `python -m venv .venv`
- Activate `.venv` for your shell before running Python commands.
- Install dev/test dependencies: `python -m pip install -r requirements-dev.txt`
- Full pytest suite: `python -m pytest`
- Focused pytest run: `python -m scripts.pytest_focused`
- Pytest config: `pyproject.toml`
- Validate skill-pack integrity: `python -m scripts.validate_skills`
- Preview managed install/update: `python -m scripts.install_skills --dry-run`
- Sync the installed custom pack: `python -m scripts.install_skills`
- Whitespace/diff checks: `git diff --check`, `git diff --cached --check`

## Pointers

- Stable vocabulary and repo invariants: `CONTEXT.md`
- Active plans and runbooks: `docs/plans/README.md`
- Before nontrivial coding, read `docs/agents/engineering-contract.md`.
- Tracker and labels: `docs/agents/issue-tracker.md`,
  `docs/agents/triage-labels.md`
- Domain routing and ADR use: `docs/agents/domain.md`

## Invariants

- Keep `AGENTS.md` short: it primes; referenced docs teach; skills execute.
- Keep skill-pack maintenance vocabulary in `CONTEXT.md`, shared runtime
  engineering vocabulary in `docs/agents/engineering-contract.md`, and durable
  decisions in `docs/adr/`.
- Do not rewrite historical research, synthesis, validation, issue notes, or
  run logs as current instructions.
- Preserve unrelated dirty work and run both whitespace/diff checks before handoff.
