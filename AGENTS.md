# Repository Instructions

Explore imaginatively. Converge under proof. Simplify ruthlessly.

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
- Sync the installed custom pack: `python -m scripts.install_skills`
- Whitespace/diff checks: `git diff --check`, `git diff --cached --check`

## Pointers

- Stable vocabulary and repo invariants: `CONTEXT.md`
- Active plans and runbooks: `docs/plans/README.md`
- One-skill deployment: each `Run Deploy Campaign on <skill>` uses Contract
  Lock, Candidate Lock, conditional Behavioral Proof, and Release under
  `docs/synthesis/methods/deploy-prompts.md`; the obligations are not persisted
  lifecycle state.
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
