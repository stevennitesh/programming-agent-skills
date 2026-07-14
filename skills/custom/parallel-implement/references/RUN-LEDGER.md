# Parallel Implement Run Ledger

Instantiate this disposable append-only ledger at `.tmp/parallel-implement/<run-id>/LEDGER.md`. Copy durable facts to the routed closeout destination before cleanup.

Append each event once. Derive routing and closeout from the event stream.

## Routing Packet

**Started:** `<date/time>`
**Source Trace:** `<request / parent / packet / items / decisions / repo sources>`
**Run fixed point:** `<starting ref for bases, integration, and review>`
**Selected scope and DAG:** `<items / frontier / blockers / wave order>`
**Integration:** `<shallow, hot, or late / branch / owner / checkout>`
**Landing:** `<executor / harness or manual gate / cherry-pick, merge, squash, or patch>`
**Lanes:** `<launch route / fresh-context policy / worktree and env isolation / preflight>`
**Slot lock:** `<capacity / reservations / worker limit / review-bandwidth rationale>`
**Proof budget:** `<worker focused / integration touched-area / loop-close broad>`
**Review:** `<route / orchestrator owner / all-lanes-idle gate>`
**Tracker and closeout:** `<lock mode / durable destination>`
**Permission plan:** `<worktrees, install, network, push, tracker, messages, destructive Git>`
**Release rule:** `<lane, worktree, commit, branch, claim, tracker, push, checks, and risk accounting>`

Resolve every field or mark it `not applicable` before dispatch. Shallow mode uses the same packet.

## Event Log

| Time | Event | Work Item | Worker SHA | Integration SHA | Validation | Decision | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<time>` | `<scope/downshift/resume/frontier/integrator-ready/dispatch/handoff/accept/reject/stale-base/conflict/land/feedback/wave-validation/review-ready/review-target/review-decision/closeout-head/tracker-lock/push/release/friction>` | `<id/all>` | `<sha/none>` | `<sha/none>` | `<command/result/skipped>` | `<short decision>` | `<none/short>` |

## Closeout Summary

Fill this before closeout tracker mutation.

**Outcome:** `<complete / partial / blocked>`
**Run fixed point:** `<sha>`
**Current integration HEAD:** `<sha / none>`
**Current Git state:** `<clean / exact in-progress state>`
**Reviewed HEAD:** `<sha / not reached>`
**Approved closeout HEAD:** `<sha / not reached>`
**Integrated and unintegrated items:** `<ids, landing order, reasons>`
**Final validation and review:** `<commands and route result / not reached>`
**Blockers and next owner:** `<none / exact blockers and owner>`
**Remaining permissions or mutations:** `<none / exact actions and authority>`
**Tracker, claims, push, and durable closeout:** `<actions and read-back / skipped>`
**Release sweep:** `<every lane, worktree, commit, branch, and preserved state>`
**Skipped checks and residual risks:** `<none / list>`
**Skill feedback and follow-ups:** `<none / list>`
