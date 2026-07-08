# Parallel Implement Run Ledger

Scratch append-only ledger for one `$parallel-implement` run. Store at `.tmp/parallel-implement/<run-id>/LEDGER.md`; copy durable facts to tracker notes or the run summary before cleanup.

Do not maintain duplicate state tables. Append events, then derive closeout from the event stream.

## Run

**Started:** `<date/time>`
**Run fixed point:** `<pinned starting ref for worker bases, integration, and final review>`
**Selected scope:** `<tracker query / parent / packet / issue set>`
**Dependency DAG:** `<ready frontier, blockers, wave order>`
**Integration branch:** `<branch>`
**Integrator thread:** `<link/id>`
**Integrator checkout:** `<dedicated integration worktree / same-checkout lock>`
**Codex project ID:** `<projectId from codex_app.list_projects>`
**Worktree launch route:** `<codex_app.create_thread / manual app Worktree / approved manual fallback>`
**Worker limit:** `<number and approval>`
**Worker isolation:** `<Codex-managed worktree / approved manual worktree>`
**Preflight policy:** `<full first host / compact after host proven>`
**Proof budget:** `<worker focused / integrator touched-area / loop-close broad>`
**Validation environment:** `<shared interpreter plus isolated worker temp/cache env vars>`
**Loop-close route:** `<$review / approved $convergent-pr-review / local fallback>`
**Tracker lock:** `<repo-local / connector-backed / none>`
**Durable closeout destination:** `<issue comment / PR body / docs note / run summary / none>`
**Expected approvals:** `<git/tool operations expected before dispatch>`
**Release sweep:** `<one release event covers active threads / worktrees / branches / tracker / push state / skipped checks / residual risk>`

## Routing Packet

```text
scope:
fixed point:
DAG/frontier:
worker limit:
integration checkout:
proof budget:
env lock:
review route:
tracker lock:
durable closeout destination:
approvals:
release rule:
```

## Event Log

| Time | Event | Issue | Worker SHA | Integration SHA | Validation | Decision | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<time>` | `<scope/downshift/frontier/dispatch/handoff/accept/reject/stale-base/land/feedback/wave-validation/loop-close/tracker-lock/release/friction>` | `<id/all>` | `<sha/none>` | `<sha/none>` | `<command/result/skipped>` | `<short decision>` | `<none/short>` |

## Closeout Summary

Fill this before tracker mutation.

**Integrated issues:** `<ids>`
**Merge order:** `<issue ids / integration SHAs>`
**Final validation:** `<commands and results>`
**Loop-close review:** `<route and result>`
**Tracker actions:** `<labels/comments/closures or skipped>`
**Durable closeout destination:** `<issue comment / PR body / docs note / run summary / none>`
**Release sweep:** `<one release event covering active threads, worktrees, branches, tracker, push state, skipped checks, residual risk>`
**Skipped checks:** `<none/list>`
**Residual risks:** `<none/list>`
**Skill feedback:** `<none/frictions, bugs, improvements>`
**Follow-ups:** `<none/list>`
