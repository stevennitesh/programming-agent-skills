---
name: parallel-implement
description: Deliver one explicitly requested parent through its exhaustive ready ticket graph using plain delegated workers, isolated concurrent lanes, adaptive serial execution, one fresh Change Review, and child-first closeout. Root-only.
---

# Parallel Implement

**Admit -> Wave -> Integrate -> Review -> Close**

Deliver one parent-backed graph. Parallelism is an optimization, not a goal.
Use it only where independent work saves time without increasing total
coordination or proof burden.

## Admit

Pass only at the top-level root after an explicit request to deliver one parent
and its exhaustive, non-empty Ready-for-agent graph. Return one standalone item
without parent-delivery custody to `$implement`, graph defects to `$to-tickets`,
unsettled meaning to its owner, missing setup to `$repo-bootstrap`, and active
conflicts to `$resolving-merge-conflicts` before mutation. Once admitted, retain
the parent campaign through serial or concurrent frontiers until every child is
accepted or has an exact blocker.

The root owns campaign scope, live concurrency decisions, claims, dispatch,
acceptance, serial landing, integration judgment, formal review, Repair
admission, tracker closeout, and completion. Workers own their assigned
implementation and tests. Workers never widen scope or dispatch successors.
The root does not author implementation or Repair code.

Freeze only the facts needed to run: parent outcome, ordered children,
dependencies, acceptance, source, fixed point, ticket scopes and expected
writes, proof owners, known overlap, closeout rule, and a graph-level Repair
budget. Preserve an explicit budget or default to `2`. Refetch current tracker
and Git state; consequential drift returns one factual repair or authority
packet. Use that live state directly; create no campaign ledger.

Claim the parent and read the claim back before dispatch; a losing race returns
`blocked`. Retain that campaign claim through final closeout or a verified
repair handoff.

One Repair generation is one admitted complete blocker set, one bounded repair
batch with proof, and one fresh successor review. Increment once per batch, not
per finding or worker. Transport retry and proof-only rerun do not consume a
generation.

## Wave

Repeat until every child has an accepted landing or an exact blocker.

Derive the dependency-ready frontier from the verified graph and current landed
state. For each frontier item, compare semantic ownership, expected production
writes, proof owners, scarce resources, and known serial tripwires. Run items
concurrently only when they are independently bounded and the expected time
saving exceeds coordination and integration cost. Uncertain or overlapping
items run serially. Protected data, permissions, trust boundaries, migrations,
cutovers, and irreversible state start with one tracer bullet through the
production path.

Choose the first matching capable profile using the ordered conditions in
[Runtime Profiles](references/RUNTIME-PROFILES.md).

Claim each selected ticket and read the claim back. Give the worker the ticket,
source pointers, exact base, allowed writes, dependencies, acceptance, proof,
and exclusions as plain task context. The implement-owned
[Plain Worker Handoff](../implement/references/WORKER-HANDOFF.md) is guidance,
not a schema. Start the worker once the information is sent. Do not validate or
seal the prose packet and do not require a machine-shaped Return.

Use [Agent Lanes](references/AGENT-LANES.md) for checkout handling. A serial
writer may receive exclusive custody of the clean integration checkout. Every
concurrent writer gets a distinct worktree prepared by the one lane helper;
dispatch only when it returns `ok: true` after Git and any applicable pytest
preflight.

Before choosing an implementation seam, each worker traces every assigned
acceptance commitment to its proof seam. When a commitment depends on
integration, the worker follows the canonical production caller to the
observable output and proof. Existing code or component tests count only when
that path reaches them. Do this directly; create no matrix or artifact.

Each worker implements the smallest acceptance-complete solution, runs focused
proof, commits its bounded work, and returns concise prose naming the commit,
changed scope, proof, skips, and blockers. The root verifies the actual lane,
base, commit, diff, scope, and proof. Prose is evidence, not trusted state.
Do not accept a lane merely because its first component seam is green. Require
evidence that each acceptance commitment reaches its proof seam and, when
integration-dependent, that the canonical production caller reaches the
observable output. If an in-scope gap remains safely actionable, resume the
same worker before accepting the landing.
Retry only after an observed blocking condition changes; never duplicate an
uncertain task.

## Integrate

A serial worker commits provisionally in the integration checkout. When it
returns, the root reacquires custody, reads back `HEAD`, and verifies the base,
commit, actual diff, scope, and proof before accepting that direct landing; it
does not land the same commit again.

For a concurrent lane, land one accepted worker commit at a time onto the
current integration branch. Before landing, verify its base, actual diff,
scope, and overlap with changes landed since dispatch. After either accepted
transition, read back `HEAD`, inspect the resulting diff, run only proof
invalidated by the transition or required by repository policy. Recompute the
frontier after each accepted landing.

The root judges integration but does not create a second implementation layer.
If a landing exposes a localized defect, return it with exact evidence to the
responsible worker when safely resumable or to one fresh capable worker. If it
invalidates ticket commitments or graph facts, return one `$to-tickets` repair
packet while retaining campaign claims. On an explicit To Tickets repair
invocation that admits the packet, transfer only the exact verified
campaign-owned claims named there. The repair owner releases them only after
verified repaired-graph publication or a terminal handoff. If it creates a
real Git conflict, preserve state and use
`$resolving-merge-conflicts`. Do not dispatch a warm general integrator or
rebuild a campaign ledger.

Carry worker proof only while its dependencies, inputs, and landing context
remain valid. When the graph drains, reconcile one owner per proof obligation,
remove duplicated campaign-created proof, run the smallest final proof set that
covers current integrated behavior and material interactions, and complete
Change Closure.

## Review And Repair

Pin one immutable candidate only when every writer is idle, the integration
checkout is clean, every child is accepted and landed, no blocker remains, and
final proof passes. An exact child blocker returns under the terminal classifier
before final proof and review.

Launch exactly one fresh `integration-reviewer` using `$change-review`, with an
actor, task, and context distinct from every implementation actor and from the
root integration actor. Supply the parent Charter, source, fixed point,
immutable integrated candidate, implementation and integration actor and task
identities, proof, skips, supported risks, contradictory evidence, and
`Spec required: yes`.
Supported risk expands
coverage; it does not change the automatic review system.
`$high-assurance-review` runs only when the user explicitly invokes it.

Accept only a complete Review Return bound to the candidate. Never self-certify.
Automatically repair only when every blocker is Charter-preserving, in scope,
and within the graph Repair budget. Send localized findings to the responsible
worker when safely resumable; otherwise dispatch one fresh capable worker.
Land and prove the correction, then use a new fresh integration reviewer.
Decision-required, scope-changing, speculative, mixed, or over-budget findings
return to the caller intact.

A review transport failure before candidate judgment may be retried once with
a fresh reviewer. After a second failure, preserve the candidate and return
`partial`.

## Close

Open closeout only when reviewed `HEAD` still equals current integration
`HEAD`, required final proof passes, and any residual risk has caller acceptance.

Close children in dependency order using the configured tracker rules. Retain
each claim through verified non-dispatchable closeout and read-back, then
release it. Close the parent only after every child verifies, then release its
claim and verify the final frontier.

Apply configured mutation read-back to every closeout and frontier transition.

At graph end, remove all safe completed worktrees. If the configured worktree
limit is reached earlier, remove the oldest safe completed worktree first.
Never remove a dirty, active, uncertain, or unintegrated lane.

Return `complete` only when the graph is drained; every accepted change is in
reviewed current `HEAD`; focused final proof, proof ownership, Change Closure,
and one independent Change Review pass; children and parent close child-first
with read-back; claims are released; and lanes are safe. Otherwise return
`partial` or `blocked` with the exact retained state, custody, blocker, and
safest resume action plus Repair generations used and remaining. `blocked`
means no authorized in-scope progress is possible until a named authority or
external-state change. `partial` means accepted progress is preserved while an
internal execution, proof, review, or cleanup gate remains safely resumable.
When both descriptions apply, return `blocked`. Do not infer deployment, PR,
merge, push, or another campaign.
