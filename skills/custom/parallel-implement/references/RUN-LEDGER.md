# Parallel Implement Run Ledger

Instantiate this disposable append-only ledger at `.tmp/parallel-implement/<run-id>/LEDGER.md`. Copy durable facts to the routed closeout destination before cleanup.

Append each event once. Derive routing and closeout from the event stream.

## Routing Packet

**Started:** `<date/time>`
**Source Trace:** `<request / parent / packet / items / decisions / repo sources>`
**Parent:** `<id / title / source type / relationship source / closeout rule>`
**Run fixed point:** `<starting ref for bases, integration, and review>`
**Child-set snapshot:** `<every associated child and follow-up / state / disposition / late relationship changes>`
**Selected scope and DAG:** `<in-scope items / dependencies / exclusions / blockers>`
**Frontier plan:** `<serial or parallel generations / tracker order / independence decisions>`
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
| `<time>` | `<scope/scope-change/resume/frontier/serial-frontier/parallel-frontier/integrator-ready/dispatch/handoff/accept/reject/stale-base/conflict/land/feedback/wave-validation/graph-drained/review-ready/review-target/review-decision/closeout-head/child-closeout/parent-closeout/tracker-lock/push/release/friction>` | `<id/all>` | `<sha/none>` | `<sha/none>` | `<command/result/skipped>` | `<short decision>` | `<none/short>` |

## Closeout Summary

Fill this before closeout tracker mutation.

**Outcome:** `<complete / partial / blocked>`
**Parent and closeout:** `<id / final state / read-back>`
**Child-set reconciliation:** `<initial snapshot / late additions, removals, or relinks / resolution>`
**Run fixed point:** `<sha>`
**Current integration HEAD:** `<sha / none>`
**Current Git state:** `<clean / exact in-progress state>`
**Reviewed HEAD:** `<sha / not reached>`
**Approved closeout HEAD:** `<sha / not reached>`
**Child disposition and closeout:** `<every id / landing order or non-implementation disposition / tracker state / read-back>`
**Frontier history:** `<serial and parallel generations / blockers / drain evidence>`
**Final validation and review:** `<commands and route result / not reached>`
**Blockers and next owner:** `<none / exact blockers and owner>`
**Remaining permissions or mutations:** `<none / exact actions and authority>`
**Tracker, claims, parent, push, and durable closeout:** `<actions and read-back / skipped>`
**Release sweep:** `<every lane, worktree, commit, branch, and preserved state>`
**Skipped checks and residual risks:** `<none / list>`
**Skill feedback and follow-ups:** `<none / list>`
