# Parallel Implement Run Ledger

Instantiate this append-only ledger at `.tmp/parallel-implement/<run-id>/LEDGER.md`. Copy durable facts to the routed closeout destination before cleanup.

Append events once. Derive routing and closeout from the event stream.

## Routing Packet

**Started:** `<date/time>`
**Source Trace:** `<request / parent / packet / work items / decision-bearing comments / repo sources>`
**Run fixed point:** `<pinned starting ref for worker bases, integration, and final review>`
**Selected scope:** `<tracker query / parent / packet / work-item set>`
**Dependency DAG:** `<ready frontier, blockers, wave order>`
**Integration mode:** `<shallow / hot / late>`
**Integration branch:** `<branch>`
**Integration lane owner:** `<orchestrator / integrator agent id>`
**Integration checkout:** `<orchestrator checkout / dedicated worktree / same-checkout lock>`
**Same-checkout lock:** `<not applicable / owner and rule>`
**Landing route:** `<repo-owned harness / manual pre-landing gate>`
**Worker launch route:** `<native isolated worktree / approved manual worktree / explicit user-owned background worktree>`
**Worker limit:** `<number and review-bandwidth rationale>`
**Worker isolation:** `<worktree and env policy>`
**Preflight policy:** `<full first host / compact after host proven>`
**Proof budget:** `<worker focused / integration touched-area / loop-close broad>`
**Validation environment:** `<shared interpreter plus isolated worker temp/cache paths>`
**Review route:** `<$review / $convergent-pr-review>`
**Tracker lock:** `<repo-local / connector-backed / none>`
**Durable closeout destination:** `<issue comment / PR body / docs note / run summary / none>`
**Permission plan:** `<worktree create/cleanup, install, network, push, tracker mutation>`
**Release sweep:** `<lane, worktree, branch, claim, tracker, push, skipped-check, and risk accounting>`

Shallow mode uses the same packet and thin ledger. Mark unused integrator fields `not applicable`.

## Event Log

| Time | Event | Work Item | Worker SHA | Integration SHA | Validation | Decision | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<time>` | `<scope/downshift/frontier/integrator-ready/dispatch/handoff/accept/reject/stale-base/land/feedback/wave-validation/review-target/closeout-head/tracker-lock/release/friction>` | `<id/all>` | `<sha/none>` | `<sha/none>` | `<command/result/skipped>` | `<short decision>` | `<none/short>` |

## Closeout Summary

Fill this before tracker mutation.

**Outcome:** `<complete / partial / blocked>`
**Run fixed point:** `<sha>`
**Reviewed HEAD:** `<sha>`
**Approved closeout HEAD:** `<sha>`
**Integrated items:** `<ids>`
**Unintegrated items:** `<rejected / blocked / follow-up ids and reasons>`
**Landing order:** `<item ids / integration SHAs>`
**Final validation:** `<commands and results>`
**Loop-close review:** `<route and result>`
**Tracker actions:** `<labels/comments/closures or skipped>`
**Claims released:** `<ids / none>`
**Durable closeout destination:** `<issue comment / PR body / docs note / run summary / none>`
**Release sweep:** `<every lane, worktree, branch, tracker action, and push state>`
**Skipped checks:** `<none/list>`
**Residual risks:** `<none/list>`
**Skill feedback:** `<none/frictions, bugs, improvements>`
**Follow-ups:** `<none/list>`
