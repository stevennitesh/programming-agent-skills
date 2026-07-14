---
name: parallel-implement
description: Orchestrate two or more ready, semantically independent work items through isolated one-commit lanes, serial integration, root-owned review, Lock, and release.
---

# Parallel Implement

Run one **wavefront**:

**Trace -> Gate -> Wave -> Integrate -> Review -> Lock -> Release**

## Contract

- **Orchestrator:** sole dispatcher and owner of scope, DAG, ledger, worker acceptance, formal review, tracker mutation, push, outcome, and release.
- **Lane worker:** one direct fresh-context child implementing one ready item in one isolated worktree; returns one clean commit plus focused proof, or a `needs-feedback` or `blocker` packet.
- **Integration lane:** serially lands accepted commits and validates integration. The orchestrator owns it unless a hot or late child integrator is routed. A child integrator never dispatches or invokes formal review; it returns a review-ready packet.

**Two isolations:** every delegated lane requires both fresh context and an independently preflighted Git worktree.

**Root-only fan-out:** workers, an optional child integrator, and formal reviewers are direct children of the orchestrator. Workers and integrators never spawn.

**Downshift:** fewer than two safe parallel items is not a wave. Recommend `$implement` and stop for one bounded item. Return serial order or readiness gaps to their owner when isolation or semantic independence cannot be established.

## References

- Always apply `docs/agents/engineering-contract.md`.
- Read `docs/agents/issue-tracker.md` when tracker work is in scope and `docs/agents/domain.md` when domain semantics affect the run.
- Before dispatch or resume, instantiate or load `references/RUN-LEDGER.md`.
- Establish every worker or child-integrator checkout through `references/CODEX-WORKTREE-LAUNCH.md`. Read its Explicit Background Task branch only when the user requests visible or background tasks.
- Dispatch each worker with `references/WORKER-BRIEF.md`.
- Start a routed hot or late child integrator with `references/INTEGRATOR-BRIEF.md`.

## Trace

Apply the **setup gate**. If a required setup surface or named operation is absent or incompatible with this skill, recommend `$repo-bootstrap` and stop.

Build one Source Trace from the request, selected parent or packet, every in-scope item and decision-bearing comment, repo instructions, and named sources.

Build the ready frontier. Each item needs settled acceptance, dependency state, parallel-safety notes, proof lane, expected write scope, and any load-bearing seam. Add a contract matrix when correctness depends on permissions, data contracts, public semantics, claim levels, or state transitions.

Start the thin ledger. On resume, reconcile it with Git, worktrees, agents, claims, and tracker state before dispatch. Accepted, landed, review-ready, tracker-lock, and release events become authoritative only after reconciliation. Never redispatch or reland them. An unreconciled mismatch returns `blocked` with the exact state.

## Gate

Apply the **frontier gate** across acceptance, contracts, interfaces, write scopes, proof lanes, and dependency assumptions. Non-overlapping files do not prove semantic independence. Add dependency edges or Downshift when one item changes an assumption another consumes.

Record the integration mode, landing mode, executor, review route, proof budget, environment route, and permission plan in the ledger.

- **Shallow:** one finite wave of two or three workers; the orchestrator lands.
- **Hot:** a child integrator can land while another worker continues or unlock the next frontier.
- **Late:** complex integration or long loop-close validation justifies a fresh integration context after worker completion.

Otherwise the orchestrator owns serial landing.

Apply the **slot lock**: worker limit is the smaller of three or live slots remaining after reserving the orchestrator and any child integrator. Require two worker slots and enough review bandwidth to inspect every packet before the next frontier decision.

The selected run authorizes scoped worker commits and the recorded serial landing route. Other external, destructive, privileged, tracker, push, dependency, or cleanup actions retain their normal authority gates.

## Wave

For each frontier item, create and preflight the isolated worktree, then launch one direct fresh-context worker with `fork_turns="none"` and the complete worker brief.

When tracker work is in scope, claim each item and apply tracker-policy **Mutation read-back** before dispatch.

Dispatch only the current independent frontier.

Classify each returned packet:

- `done`: verify acceptance accounting, the commit, actual diff, scope, proof, final status, and residual risk; accept or reject it.
- `needs-feedback`: keep the lane and claim open; send one delta or return the commitment change to its owner.
- `blocker`: retry only after the input, base, route, capability, authority, or task shape changes; otherwise preserve and record its disposition.

Only an accepted `done` packet may land.

Apply the **proof budget**: worker focused proof, integration touched-area proof, loop-close broad validation and fixed-point review. Route broader worker proof only for shared-behavior risk.

## Integrate

Land accepted commits serially through the recorded executor and route. Default detached one-commit workers to `cherry-pick` unless repo policy selects another mode.

Before every landing, inspect the actual `base..head` diff, expected scope, new files, stale-base overlap, conflicts, and focused proof. Verify the landed result, run touched-area proof, and append one ledger event.

A stale base returns a **stale-base packet**; the orchestrator chooses rebase, redispatch, serialization, or rejection.

When landing conflicts or partially applies, preserve the Git state and invoke `$resolving-merge-conflicts` within its authority boundary. Resume only from its verified, authorized return state. Otherwise return `blocked`; never invent authority to abort, continue, reset, discard, or force-clean.

Rescan the frontier after each landing. Repeat Wave and Integrate until drained or blocked.

## Review

Assemble review-visible closeout metadata, require a clean in-scope integration state, run final validation, and produce or accept the integration lane's review-ready packet.

Wait until every lane agent is idle. Pin the integration `HEAD` as the immutable review target. The orchestrator invokes `$review` by default or `$convergent-pr-review` when its high-risk trigger matches, with `Spec required: yes`, the Source Trace, selected items and acceptance, run fixed point, integration `HEAD`, and complete diff.

Keep Lock closed for an unavailable route, P0/P1 finding, required-validation P2, missing required validation, incomplete Spec axis, `blocked` or `incomplete` review, or unaccepted residual risk. Every lower-severity ordinary-review finding must be fixed or explicitly accepted as residual risk by the routing packet, repo policy, or user.

A `pass with residual risk` opens Lock only when the routing packet, repo policy, or user accepts that risk.

After a review fix, inspect the delta. A material behavior, scope, contract, schema, dependency, security, or public-interface change requires a new review target and review. A tiny finding-only fix may use targeted proof only when the routing packet permits it.

## Lock

Record the approved closeout `HEAD`. Closeout tracker mutation and push require the current integration `HEAD` to match it.

Follow `docs/agents/issue-tracker.md`. Fill the closeout summary before closeout tracker mutation, mutate only under the configured authority, and apply **Mutation read-back**. A partial or unverifiable mutation keeps Lock closed.

After an authorized push, verify the remote branch or PR head resolves to the approved closeout `HEAD`.

## Release

Finish or stop every worker and integrator. Record one disposition for every selected item, packet, lane, claim, worktree, commit, branch, tracker action, push, skipped check, and residual risk.

Remove only clean worker worktrees whose commits are integrated or explicitly preserved. Preserve dirty, untracked, unintegrated, conflicted, or unauthorized state.

Return exactly one ledger Outcome: `complete`, `partial`, or `blocked`.

`complete` requires a current approved closeout `HEAD`, final validation, the assigned formal review, applicable tracker Lock, and the release sweep.

`partial` or `blocked` claims only events that occurred. Record current `HEAD` and Git state, landed and unlanded items, exact blockers, next owner, remaining authority or mutations, and preserved state.

Every outcome requires the Source Trace, routing packet, packet and landing accounting, no active lane or unaccounted partial mutation, skipped checks, residual risk, and release state.
