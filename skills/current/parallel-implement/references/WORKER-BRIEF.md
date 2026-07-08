# Worker Brief

Implement exactly one assigned issue.

## Assignment

**Issue:** `<issue id and title>`
**Issue source:** `<GitHub issue / local tracker file / packet child issue / PRD slice>`
**Codex worker thread:** `<thread id or pending worktree id>`
**Codex worktree source:** `<create_thread worktree / manual app Worktree / approved manual worktree>`
**Starting state:** `<project default branch / existing branch or ref / working-tree>`
**Base SHA:** `<sha expected by orchestrator>`
**Isolation mode:** `<Codex-managed worktree / approved manual worktree>`
**Worker worktree path:** `<actual path from preflight>`
**Commit target:** `<detached HEAD commit / worker branch>`
**Starting dirty state:** `<git status --short --branch before edits>`
**Preflight mode:** `<full / compact after host proven>`
**Preflight result:** `<repo root + HEAD + status + scratch write/delete + focused proof startup>`
**Expected write scope:** `<paths/modules, or "discover and report before widening">`
**Acceptance packet:** `<acceptance criteria, blockers, out-of-scope, dependency notes>`
**Parent context:** `<PRD/spec/issue packet links>`
**Focused proof:** `<commands or expected evidence>`
**Proof budget:** `<focused-only / routed shared-behavior broad check>`
**Validation environment:** `<interpreter/venv, cwd, PYTHONPATH, isolated temp/cache env vars, focused runner>`
**Env lock:** `<no shared dependency mutation / routed exception>`
**Integration branch:** `<branch name, read-only for worker>`

## Contract

Read the issue packet and `docs/agents/engineering-contract.md`. Issue packet owns acceptance; this brief owns worker process.

You are one fresh worker for one issue. Produce exactly one clean worker commit plus focused proof, or return a blocker packet.

Preflight before edits. Full preflight reports:

- `pwd`
- `git rev-parse --show-toplevel`
- `git status --short --branch`
- `git rev-parse HEAD`
- `git branch --show-current`
- scratch write/delete in the repo root
- the routed focused proof command, or the setup blocker that prevents it from starting

Use compact preflight only when the routing packet says the worktree host is already proven. Compact preflight reports cwd, repo root, `HEAD`, status, interpreter/env, and focused proof startup.

Stop before edits if the root is not the assigned repo, `HEAD` is not the assigned base, scratch writes fail, or the focused proof command cannot start.

Use `$tdd` for red-testable behavior; otherwise prove the slice with the routed focused evidence. Run broad suites only when routed or when the slice changes shared behavior. If repo defaults fight the worker checkout, retry once with worker-safe proof and report both results.

Use the assigned validation environment. If `.venv` is absent, use the assigned interpreter/routed env and report the fallback. Do not run broad dependency-mutating commands such as `uv sync`, `pip install`, `npm install`, or cache-rebuilding setup against a shared checkout/env unless routed.

Do not fan out, run formal review, mutate tracker state, merge integration work, or perform lock steps. Stop before changing commitments: product intent, acceptance, public/domain contracts, dependencies, or security/privacy posture.

## Report

Done means verified preflight, clean `git status --short`, and exactly one worker commit SHA, or a blocker packet.

Return preflight, commit SHA, owned files, validation, acceptance proof, skipped checks, residual risk/blockers, scope notes, unrelated dirty files, and skill feedback.

Packet skeleton:

```text
status: <done / blocker / needs-feedback>
issue:
base:
commit:
owned files:
proof:
skipped checks:
risk/blockers:
scope notes:
final status: <clean / dirty + reason>
skill feedback:
```
