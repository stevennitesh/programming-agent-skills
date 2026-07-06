# Parallel Implement Run Ledger

Scratch ledger for one parallel-implement run. Store at `.tmp/parallel-implement/<run-id>/LEDGER.md`; copy durable facts to tracker notes or the run summary before cleanup.

For shallow runs, use minimal ledger mode: Run, Worker Results, Serial Landing, Final Checks, and Run Summary.

## Run

**Started:** `<date/time>`
**Integration branch:** `<branch>`
**Integrator thread:** `<link/id>`
**Integrator checkout:** `<same as orchestrator / separate>`
**Integrator status:** `<starting/active/blocked/released>`
**Run fixed point:** `<pinned starting ref for worker bases, integration, and final review>`
**Selected scope:** `<tracker query / parent / packet / issue set>`
**Codex project ID:** `<projectId from codex_app.list_projects>`
**Worktree launch route:** `<codex_app.create_thread / manual app Worktree / approved manual fallback>`
**Starting state policy:** `<default branch / existing branch or ref / working-tree>`
**Active worker limit:** `<number and approval>`
**Claim rule:** `<ready-for-agent + blockers satisfied + in selected scope>`
**Final validation plan:** `<commands>`
**Worker isolation requirement:** `<Codex-managed worktree / approved manual worktree>`
**Commit target:** `<worker branch / detached HEAD commit>`
**Starting dirty state:** `<git status --short before edits>`
**Preflight result:** `<git status + scratch/cache write + focused proof command>`
**Validation environment:** `<shared venv/interpreter plus known temp/cache env vars>`
**Review route:** `<review / convergent review / local fallback>`
**Review executor:** `<integrator subagent>`
**Review fallback:** `<none / reason and method>`
**Launch approval:** `<approved by / already authorized / blocked>`
**Integration method:** `<squash merge / cherry-pick / patch application>`

## Selected Issues

| Issue | Title | Blocked by | State | Notes |
| --- | --- | --- | --- | --- |
| `<id>` | `<title>` | `<ids/none>` | `<ready/etc>` | `<short note>` |

## Ready Frontier

| Scan | Claim | Issue | Base SHA | Readiness | Write-scope overlap check |
| --- | --- | --- | --- | --- | --- |
| `1` | `<claimed/blocked/deferred>` | `<id>` | `<sha>` | `<why ready or blocked>` | `<none/overlap>` |

## Workers

| Worker | Issue | Thread / pending worktree | Source | Starting state | Worktree path | Commit target | Base SHA | Preflight | Status | Handoff |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<name>` | `<id>` | `<thread id / pending id>` | `<create_thread/manual app/manual fallback>` | `<branch/ref/default/working-tree>` | `<path>` | `<target>` | `<sha>` | `<pass/fail/blocker>` | `dispatched` | `<waiting/received/accepted/rejected>` |

## Worker Results

| Issue | Preflight | Commit SHA | Owned files | Validation | Acceptance proof | Skipped checks | Risk/blockers | Scope notes | Unrelated dirty files | Skill feedback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `<id>` | `<pass/fail/blocker>` | `<sha>` | `<short list>` | `<pass/fail summary>` | `<evidence>` | `<none/list>` | `<none/short>` | `<short note>` | `<none/list>` | `<none/frictions>` |

## Integration Queue

| Issue | Worker commit SHA | Queue status | Integrator decision |
| --- | --- | --- | --- |
| `<id>` | `<sha>` | `<queued/integrated/rejected/blocked>` | `<short decision>` |

## Feedback

| Issue | Round | Feedback | Result |
| --- | --- | --- | --- |
| `<id>` | `1` | `<targeted request>` | `<fixed/blocked/serialized/taken over>` |

## Staleness And Overlap

| Issue | Worker base vs integration head | Decision |
| --- | --- | --- |
| `<id>` | `<overlap/no overlap>` | `<review/update worker/serialize>` |

## Serial Landing

| Order | Issue | Worker commit SHA | Integration SHA | Validation after integration | Orchestrator route |
| --- | --- | --- | --- | --- | --- |
| `1` | `<id>` | `<sha>` | `<sha>` | `<command>` - `<result>` | `<claim more / feedback / blocked / complete>` |

## Final Checks

| Check | Result | Notes |
| --- | --- | --- |
| `<command>` | `<pass/fail/skipped>` | `<short note>` |

## Durable Tracker Notes

| Issue | Durable note fields | Closeout target |
| --- | --- | --- |
| `<id>` | `worker SHA, integration SHA, review result, validation, skipped checks, risk` | `<child issue / connector issue>` |

## Run Summary

**Integrated issues:** `<ids>`
**Merge order:** `<issue ids / integration SHAs>`
**Skipped checks:** `<none/list>`
**Residual risks:** `<none/list>`
**Skill feedback:** `<none/frictions, bugs, improvements>`
**Follow-ups:** `<none/list>`
