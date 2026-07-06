# Repository Instructions

## Commands

- Create the repo environment if needed: `python -m venv .venv`
- Activate `.venv` for your shell before running Python commands.
- Install dev/test dependencies: `python -m pip install -r requirements-dev.txt`
- Full pytest suite: `python -m pytest`
- Focused pytest run: `python -m scripts.pytest_focused`
- Pytest config: `pyproject.toml`
- Validate skill-pack integrity: `python -m scripts.validate_skills`
- Whitespace/diff check: `git diff --check`

## Pointers

- Stable vocabulary and repo invariants: `CONTEXT.md`, `CONTEXT-MAP.md`
- Active plans and runbooks: `docs/plans/README.md`
- Engineering contract for nontrivial coding: `docs/agents/engineering-contract.md`
- Tracker and labels: `docs/agents/issue-tracker.md`,
  `docs/agents/triage-labels.md`
- Domain routing and ADR use: `docs/agents/domain.md`

## Invariants

- Keep `AGENTS.md` short: it primes; the contract teaches; skills execute.
- If the user names a skill, use it. Otherwise suggest a specialized skill only
  when it clearly improves the work.
- Do not copy full skill procedures into repo docs or answers; point to the
  owning skill/doc.
- Keep durable vocabulary in `CONTEXT.md` and durable decisions in `docs/adr/`.
- Do not rewrite historical research, synthesis, validation, issue notes, or
  run logs as current instructions.
- Preserve unrelated dirty work and run `git diff --check` before handoff.
