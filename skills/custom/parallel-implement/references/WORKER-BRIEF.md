# Lane Worker Brief

Implement exactly one assigned work item.

## Assignment

**Work item:** `<id and title>`
**Source Trace:** `<issue / local packet / spec slice / decision-bearing comments / named repo sources>`
**Lane worker:** `<agent id / explicit user-owned task id>`
**Context mode:** `<fresh direct child with fork_turns="none" / explicit user-owned task>`
**Launch route:** `<root-created detached worktree / explicit user-owned Codex App worktree task>`
**Starting state:** `<project default branch / existing branch or ref / working tree>`
**Base SHA:** `<sha expected by orchestrator>`
**Worker worktree path:** `<absolute path from preflight>`
**Commit target:** `<detached HEAD commit / worker branch>`
**Starting dirty state:** `<git status --short --branch before edits>`
**Preflight mode:** `<full / compact after host proven>`
**Preflight result:** `<repo root + HEAD + status + .tmp/ write/delete + focused proof startup>`
**Expected write scope:** `<paths/modules, or "discover and report before widening">`
**Acceptance packet:** `<criteria, blockers, out-of-scope work, dependency notes>`
**Integration context:** `<interfaces or decisions from already-landed work that the Source Trace does not contain / none>`
**Report transport:** `<compact inline packet / exact lane-local .tmp path plus short envelope>`
**Focused proof:** `<commands or expected evidence>`
**Proof budget:** `<focused-only / routed shared-behavior broad check>`
**Validation environment:** `<interpreter/venv, cwd, PYTHONPATH, isolated .tmp/ cache and temp paths, focused runner>`
**Env lock:** `<no shared dependency mutation / routed exception>`
**Integration branch:** `<branch name, read-only for worker>`

## Contract

Read every source in the Source Trace and `docs/agents/engineering-contract.md`. The work-item source owns acceptance; this brief owns lane-worker process.

**Workspace boundary:** the assigned worktree, not the process startup cwd, is your workspace. Before any edit, prove its absolute path, repo root, `HEAD`, branch or detached state, and status. Set that path as `workdir` on every shell call. Use absolute paths under it for every file edit. Never modify the parent or integration checkout.

**One worker, one lane, one packet:** do not spawn subagents, integrate, review, mutate trackers, push, or widen scope.

Produce exactly one clean local commit plus focused proof, or return a `blocker` or `needs-feedback` packet.

Preflight before edits. Full preflight reports:

- `pwd`
- `git rev-parse --show-toplevel`
- `git status --short --branch`
- `git rev-parse HEAD`
- `git branch --show-current`
- `.tmp/` write/delete in the assigned worktree
- routed focused-proof startup, or the setup blocker that prevents it

Use compact preflight only when the routing packet says the worktree host is proven. Report cwd, repo root, `HEAD`, status, interpreter/env, and focused-proof startup.

Stop before edits when the root is wrong, `HEAD` differs from the assigned base, starting status contains unexpected changes, `.tmp/` writes fail, or focused proof cannot start.

Invoke `$tdd` for red-testable behavior; otherwise prove the slice with routed focused evidence. Run a broad suite only when routed or when the slice changes shared behavior. If repo defaults fail only because of the isolated checkout, retry once with the routed worker-safe proof and report both results.

Use the assigned validation environment. If `.venv` is absent, use the routed interpreter/env and report the fallback. Shared dependency mutation requires an explicit route.

Keep one lane: patch, focused proof, one local commit, packet. Return adjacent work or commitment changes as `needs-feedback`. Formal review, tracker mutation, integration, push, and lock remain upstream.

Stop before changing product intent, acceptance, public or domain contracts, dependencies, or security/privacy posture.

## Report

`done` means verified preflight, a clean `git status --short`, and exactly one worker commit SHA. `blocker` or `needs-feedback` makes no completion claim and reports exact state, reason, next need, and any preserved commit or worktree state.

Return Source Trace, preflight, base SHA, commit SHA, owned files, validation, acceptance proof, skipped checks, residual risk or blockers, scope notes, unrelated dirty files, final status, and skill feedback.

Packet skeleton:

```text
status: <done / blocker / needs-feedback>
work item:
source trace:
base:
commit:
owned files:
proof:
skipped checks:
risk/blockers:
next need:
scope notes:
final status: <clean / dirty + reason>
skill feedback:
```
