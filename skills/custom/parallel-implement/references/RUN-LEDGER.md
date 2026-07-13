# Parallel Implement Run Ledger

Instantiate this disposable append-only ledger at `.tmp/parallel-implement/<run-id>/LEDGER.md`. Copy durable facts to the routed closeout destination before cleanup.

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
**Integration checkout:** `<orchestrator checkout / dedicated integration worktree>`
**Landing route:** `<repo-owned harness / manual pre-landing gate>`
**Landing mode:** `<cherry-pick / merge / squash / patch application>`
**Worker launch route:** `<root-created detached worktree / explicit user-owned Codex App worktree task>`
**Context policy:** `<fresh direct children with fork_turns="none" / explicit user-owned tasks / context control unavailable>`
**Slot lock:** `<live capacity, reserved slots, active worker limit>`
**Worker limit:** `<number and review-bandwidth rationale within slot lock>`
**Worker isolation:** `<worktree and env policy>`
**Preflight policy:** `<full first host / compact after host proven>`
**Proof budget:** `<worker focused / integration touched-area / loop-close broad>`
**Validation environment:** `<shared interpreter plus isolated worker .tmp/ cache and temp paths>`
**Review route:** `<$review / $convergent-pr-review>`
**Formal review owner:** `orchestrator`
**Review slot gate:** `<all lane agents idle / blocker>`
**Tracker lock:** `<repo-local / connector-backed / none>`
**Durable closeout destination:** `<issue comment / PR body / docs note / run summary / none>`
**Permission plan:** `<worktree create/cleanup, install, network, push, tracker mutation, external message, force operation, branch deletion>`
**Release sweep:** `<lane, agent, worktree, commit, branch, claim, tracker, push, skipped-check, and risk accounting>`

Shallow mode uses the same packet and thin ledger. Mark unused integrator fields `not applicable`.

## Event Log

| Time | Event | Work Item | Worker SHA | Integration SHA | Validation | Decision | Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `<time>` | `<scope/downshift/resume/frontier/integrator-ready/dispatch/handoff/accept/reject/stale-base/conflict/land/feedback/wave-validation/review-ready/review-target/review-decision/closeout-head/tracker-lock/push/release/friction>` | `<id/all>` | `<sha/none>` | `<sha/none>` | `<command/result/skipped>` | `<short decision>` | `<none/short>` |

## Closeout Summary

Fill this before tracker mutation.

**Outcome:** `<complete / partial / blocked>`
**Run fixed point:** `<sha>`
**Current integration HEAD:** `<sha / none>`
**Current Git state:** `<clean / in-progress operation and status>`
**Reviewed HEAD:** `<sha / not reached>`
**Approved closeout HEAD:** `<sha / not reached>`
**Integrated items:** `<ids>`
**Unintegrated items:** `<rejected / blocked / follow-up ids and reasons>`
**Landing order:** `<item ids / integration SHAs>`
**Final validation:** `<commands and results / not reached>`
**Loop-close review:** `<route and result / not reached>`
**Blockers:** `<none / exact blockers>`
**Next owner:** `<none / user / orchestrator / named skill or maintainer>`
**Remaining permissions or mutations:** `<none / exact actions and authority needed>`
**Tracker actions:** `<labels/comments/closures or skipped>`
**Claims released:** `<ids / none>`
**Durable closeout destination:** `<issue comment / PR body / docs note / run summary / none>`
**Release sweep:** `<every lane, worktree, branch, tracker action, and push state>`
**Skipped checks:** `<none/list>`
**Residual risks:** `<none/list>`
**Skill feedback:** `<none/frictions, bugs, improvements>`
**Follow-ups:** `<none/list>`
