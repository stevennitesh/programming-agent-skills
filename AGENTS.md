# Repository Instructions

## Commands

- Create the repo environment if needed: `python -m venv .venv`
- Activate `.venv` for your shell before running Python commands.
- Install dev/test dependencies: `python -m pip install -r requirements-dev.txt`
- Focused pytest run: `python -m scripts.pytest_focused`
- Full pytest suite when repository policy or broad shared impact requires it:
  `python -m pytest`
- Pytest config: `pyproject.toml`
- Put disposable test, review, and scratch output under `.tmp/<purpose>`; do
  not create cache or `.tmp-*` directories at the repository root.
- Validate skill-pack integrity: `python -m scripts.validate_skills`
- Preview managed install/update: `python -m scripts.install_skills --dry-run`
- Sync the installed custom pack: `python -m scripts.install_skills`.
  This uses `skills/custom/`; for Astra installation, read `CONTEXT.md` first.
- Whitespace/diff checks: `git diff --check`, `git diff --cached --check`

## Pointers

- Purpose, source ownership, and repo invariants: `CONTEXT.md`
- When designing or changing Astra skills: `docs/astra/design-brief.md`
- Active plans and runbooks: `docs/plans/README.md`
- For `Run Deploy Campaign on <skill>`, read
  `docs/synthesis/methods/deploy-prompts.md`.
- Before nontrivial coding, read `docs/agents/engineering-contract.md`.
- For tracker-backed work: `docs/agents/issue-tracker.md`,
  `docs/agents/triage-labels.md`
- When domain meaning or accepted decisions matter: `docs/agents/domain.md`

## Invariants

- Do not rewrite historical research, synthesis, validation, issue notes, or
  run logs as current instructions.
- Preserve unrelated dirty work and run both whitespace/diff checks before handoff.
