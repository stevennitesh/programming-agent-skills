---
name: parallel-implement
description: Drain one parent spec or PRD's ready implementation ticket graph through serial or parallel isolated lanes, serial integration, root-owned review, Lock, and verified child and parent closeout.
---

# Parallel Implement

Own one outcome: complete every in-scope implementation ticket associated with one parent spec or PRD, using parallel lanes when the ready frontier permits and serial lanes when it does not.

Run one resumable **wavefront campaign**:

**Trace -> Gate -> Wave -> Integrate -> Review -> Lock -> Release**

## Contract

- **Orchestrator:** sole dispatcher and owner of the parent scope, DAG, ledger, frontier mode, worker acceptance, formal review, tracker mutation, push, outcome, and release.
- **Lane worker:** one direct fresh-context child implementing one ready item in one isolated worktree; returns one clean commit plus focused proof, or a `needs-feedback` or `blocker` packet.
- **Integration lane:** serially lands accepted commits and validates integration. The orchestrator owns it unless a hot or late child integrator is routed. A child integrator never dispatches or invokes formal review; it returns a review-ready packet.

**Two isolations:** every delegated lane requires both fresh context and an independently preflighted Git worktree.

**Root-only fan-out:** workers, an optional child integrator, and formal reviewers are direct children of the orchestrator. Workers and integrators never spawn.

**Frontier width chooses execution, not ownership:** one ready item is a serial wave; two or more semantically independent items may run in parallel; write-overlapping items serialize in tracker order. An empty frontier with unfinished tickets is blocked. `$implement` retains standalone one-ticket work outside a parent campaign.

The parent selects existing work; it is never direct implementation scope. `$to-tickets` owns missing slices, readiness repair, and durable dependency changes. If the parent has no associated implementation tickets, an in-scope commitment is unsliced, or a needed edge is missing, recommend `$to-tickets` and stop without inventing work. Pause the campaign for that handoff; resume only after the repaired graph is published, read back, and reconciled with the ledger.

## References

- Always apply `docs/agents/engineering-contract.md`.
- Read `docs/agents/issue-tracker.md` when tracker work is in scope and `docs/agents/domain.md` when domain semantics affect the run.
- Before dispatch or resume, instantiate or load `references/RUN-LEDGER.md`.
- Establish every worker or child-integrator checkout through `references/CODEX-WORKTREE-LAUNCH.md`. Read its Explicit Background Task branch only when the user requests visible or background tasks.
- Dispatch each worker with `references/WORKER-BRIEF.md`.
- Start a routed hot or late child integrator with `references/INTEGRATOR-BRIEF.md`.

## Trace

Apply the **setup gate**. If a required setup surface or named operation is absent or incompatible with this skill, recommend `$repo-bootstrap` and stop.

Resolve exactly one parent spec or PRD and its associated implementation tickets through the configured tracker relationship. Build one Source Trace from the request, parent, every in-scope child and follow-up, decision-bearing comments, repo instructions, and named sources.

Inventory every associated ticket as completed, ready, blocked, claimed, excluded, or unresolved and record the parent closeout rule. Every in-scope open ticket needs the Ready-for-agent contract: settled acceptance, dependency state, proof lane, expected write scope, parallel-safety note, scope fence, and any load-bearing seam. A parent without that complete ticket graph returns to `$to-tickets`.

Build the ready frontier from tracker state plus reconciled ledger events. Inside this campaign, an accepted landed item satisfies execution dependencies while tracker closeout waits for Lock. Record the initial child-set snapshot; a later added, removed, or relinked child triggers scope reconciliation and must be completed, explicitly excluded by its owner, or returned for slicing before the campaign can complete. Add a contract matrix when correctness depends on permissions, data contracts, public semantics, claim levels, or state transitions.

Start the thin ledger. On resume, reconcile it with Git, worktrees, agents, claims, and tracker state before dispatch. Accepted, landed, review-ready, tracker-lock, and release events become authoritative only after reconciliation. Never redispatch or reland them. An unreconciled mismatch returns `blocked` with the exact state.

## Gate

Apply the **frontier gate** across acceptance, contracts, interfaces, write scopes, proof lanes, and dependency assumptions. Non-overlapping files do not prove semantic independence. A discovered missing durable edge or unsliced commitment returns to `$to-tickets`; runtime serialization may protect overlapping work but does not rewrite ticket ownership.

Choose one frontier mode and record it in the ledger:

- **Serial:** dispatch the first ready ticket in tracker order when the frontier has one item or safe independence is absent.
- **Parallel:** dispatch up to the worker limit when at least two ready tickets are semantically independent.
- **Blocked:** return the unfinished tickets and exact blockers when no ticket is executable.

Record the integration mode, landing mode, executor, review route, proof budget, environment route, and permission plan in the ledger.

- **Shallow:** one or more finite serial or parallel waves; the orchestrator lands.
- **Hot:** a child integrator can land while another worker continues or unlock the next frontier.
- **Late:** complex integration or long loop-close validation justifies a fresh integration context after worker completion.

Otherwise the orchestrator owns serial landing.

Apply the **slot lock**: worker limit is the smaller of three or live slots remaining after reserving the orchestrator and any child integrator. A serial wave requires one worker slot; a parallel wave requires at least two. Every mode requires enough review bandwidth to inspect each packet before the next frontier decision. No worker slot is blocked, not a transfer to `$implement`.

The selected run authorizes scoped worker commits and the recorded serial landing route. Other external, destructive, privileged, tracker, push, dependency, or cleanup actions retain their normal authority gates.

## Wave

For each item selected by the current frontier mode, create and preflight the isolated worktree, then launch one direct fresh-context worker with `fork_turns="none"` and the complete worker brief.

When tracker work is in scope, claim each item and apply tracker-policy **Mutation read-back** before dispatch.

Dispatch only the selected serial item or current independent parallel subset. Never dispatch write-overlapping tickets together.

Classify each returned packet:

- `done`: verify acceptance accounting, the commit, actual diff, scope, proof, final status, and residual risk; accept or reject it.
- `needs-feedback`: keep the lane and claim open; send one delta or return the commitment change to its owner.
- `blocker`: retry only after the input, base, route, capability, authority, or task shape changes; otherwise preserve and record its disposition.

Only an accepted `done` packet may land.

Apply the **proof budget**: worker focused proof, integration touched-area proof, loop-close broad validation and fixed-point review. Route broader worker proof only for shared-behavior risk.

## Integrate

Land accepted commits serially through the recorded executor and route. Default detached one-commit workers to `cherry-pick` unless repo policy selects another mode.

Before every landing, inspect the actual `base..head` diff, expected scope, new files, stale-base overlap, conflicts, and focused proof. Verify the landed result, run touched-area proof, append one ledger event, and mark the item execution-complete for dependency calculation without claiming tracker closeout.

A stale base returns a **stale-base packet**; the orchestrator chooses rebase, redispatch, serialization, or rejection.

When landing conflicts or partially applies, preserve the Git state and invoke `$resolving-merge-conflicts` within its authority boundary. Resume only from its verified, authorized return state. Otherwise return `blocked`; never invent authority to abort, continue, reset, discard, or force-clean.

After each landing, refetch the parent relationship and rescan every associated ticket. Reconcile child-set changes, then choose the next serial, parallel, or blocked frontier. Repeat Wave and Integrate until every in-scope ticket is execution-complete or has an owner-approved non-implementation disposition. An empty frontier with unfinished tickets returns `blocked`; it never implies completion.

## Review

Enter Review only after the parent graph is execution-drained and every child is accounted for. Assemble review-visible parent and child closeout metadata, require a clean in-scope integration state, run final validation, and produce or accept the integration lane's review-ready packet.

Wait until every lane agent is idle. Pin the integration `HEAD` as the immutable review target. The orchestrator invokes `$review` by default or `$convergent-pr-review` when its high-risk trigger matches, with `Spec required: yes`, the parent, complete child accounting and acceptance, Source Trace, run fixed point, integration `HEAD`, and complete diff.

Keep Lock closed for an unavailable route, P0/P1 finding, required-validation P2, missing required validation, incomplete Spec axis, `blocked` or `incomplete` review, or unaccepted residual risk. Every lower-severity ordinary-review finding must be fixed or explicitly accepted as residual risk by the routing packet, repo policy, or user.

A `pass with residual risk` opens Lock only when the routing packet, repo policy, or user accepts that risk.

After a review fix, inspect the delta. A material behavior, scope, contract, schema, dependency, security, or public-interface change requires a new review target and review. A tiny finding-only fix may use targeted proof only when the routing packet permits it.

## Lock

Record the approved closeout `HEAD`. Closeout tracker mutation and push require the current integration `HEAD` to match it.

Follow `docs/agents/issue-tracker.md`. Fill the closeout summary before closeout tracker mutation. For each execution-complete child, post its closeout packet, apply the implemented state, release its claim, close it when policy requires, and apply **Mutation read-back** to the child and affected dependents.

Then refetch the parent and its complete child and follow-up set. Close the parent only when every in-scope item is closed or has its owner-approved disposition and the tracker parent-close rule passes. Post the final parent summary, apply parent closeout, and read back the parent, relationships, children, claims, and resulting frontier. A new or unresolved child, partial mutation, or unverifiable read-back keeps Lock closed and returns the exact recovery state.

After an authorized push, verify the remote branch or PR head resolves to the approved closeout `HEAD`.

## Release

Finish or stop every worker and integrator. Record one disposition for the parent and every associated child, packet, frontier generation, lane, claim, worktree, commit, branch, tracker action, push, skipped check, and residual risk.

Remove only clean worker worktrees whose commits are integrated or explicitly preserved. Preserve dirty, untracked, unintegrated, conflicted, or unauthorized state.

Return exactly one ledger Outcome: `complete`, `partial`, or `blocked`.

`complete` requires a current approved closeout `HEAD`, final validation, the assigned formal review, every in-scope child accounted for and closed when tracker-backed, verified parent closeout, applicable tracker Lock, and the release sweep.

`partial` or `blocked` claims only events that occurred. Record current `HEAD` and Git state, landed and unlanded items, exact blockers, next owner, remaining authority or mutations, and preserved state.

Every outcome requires the Source Trace, parent and child-set snapshot, frontier history, packet and landing accounting, child and parent closeout state, no active lane or unaccounted partial mutation, skipped checks, residual risk, and release state.
