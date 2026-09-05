# Tracker delivery

Read only when delivery includes authorized tracker claims or closeout. Use the
repository's configured tracker, status, category, and readiness conventions.
Missing or incompatible policy leaves a concrete setup gap; suggest repo-bootstrap
for that gap rather than inventing labels. Direct implementation needs no tracker.

Refresh the accepted items, decision-changing comments, dependencies, and active
ownership before claims. If delivering a complete parent, enumerate its complete
child graph and reconcile drift against the fixed scope. A selected subset does
not authorize closing its parent or changing siblings outside that subset.

For whole-parent delivery, claim and read back the parent for this coordinator
before dispatching children. For a subset, preserve the parent's ownership and
coordinate with its owner rather than taking over the graph. Bind claims to the
run and actor, not merely a shared tracker account; use the configured claim
representation plus a run marker when needed. Refetch/read-back is not an atomic
lock: where independent coordinators may race, use a supported exclusive claim
mechanism or establish one coordinator before dispatch. Stop on ambiguous ownership.

Claim only agent-ready items (the mapped `ready-for-agent` role or policy equivalent)
whose required predecessor outcomes are actually integrated. Preserve human-only
readiness as a handoff; it never permits agent dispatch. Independent agent-ready
work may continue while that handoff is pending.
Require an item to be unclaimed or demonstrably held by this run through its known
actor, lane, and commit. Stop on another or ambiguous owner. Read each claim back
and confirm one current actor before dispatch. Refetch newly ready items before
claiming them; leave blocked or permission-gated descendants unclaimed.

After an item lands and its applicable proof passes, preserve its category,
remove readiness roles, apply the mapped implemented state, and close only when
configured. Clear this run's active claim when finished; preserve historical
attribution separately if useful. Never clear another actor's claim. Read all
changed state back, including when the provider keeps implemented items open.
Refetch affected dependents; mark agent-ready only complete accepted agent work whose actual
blockers and permissions are resolved. Stay within authorized graph mutations.
Do not equate a closed predecessor with an integrated required outcome.

On an accepted source revision, pause affected dispatch and coordinate affected
writers before changing their contracts. Reconcile source, tickets, assignments
and gates against that revision, and reassess affected landed behavior and proof.
Resume only the reconciled work; unchanged items and evidence remain usable.

Mark a requested complete parent implemented only after refetching the full graph, confirming
all children completed, and satisfying the main skill's integrated proof for the
exact candidate. Preserve its category, remove readiness and this run's claim,
apply the mapped implemented state, and close only when configured; an implemented
parent may remain open. Read the parent state back. A partial, failed, or indeterminate
effect stops further tracker mutation: refetch affected state before deciding a
retry, preserve implementation progress, and report the observed state and safest
configured recovery. Do not replay writes or release ambiguous claims blindly.

On a pause, leave incomplete items and the parent unimplemented. Retain a claim
only while this run will resume and its custody is established; otherwise release
only this run's claims after writers stop and record the recoverable handoff.
Parent completion removes readiness and the run's claim just like child completion.

## Version-controlled local tracker

The root's integration checkout is the canonical tracker. Reserve its tracker
paths to the root; worker copies are read-only snapshots. Send workers current
accepted scope and predecessor evidence, not instructions to reread stale lane
status as live authority. Serialize tracker edits with integration-checkout writers
and helper mutations. Do not merge worker changes to tracker files.

Before the first dispatch, commit the accepted graph and initial claims under
existing local commit authority. At each transition, read back owned tracker edits
and commit them before creating new lanes, landing changes, or handing exclusive
integration custody to a serial worker. Claim all siblings selected together in
one transition, then prepare them from that same clean HEAD. Snapshot-only tracker
differences between sibling bases and current HEAD do not by themselves invalidate
code proof; acceptance, dependency, permission, or ownership changes can.

After code proof at commit C, completion records cite C, not the commit that will
contain those records. Commit the root's metadata-only completion changes to yield
final HEAD H. Inspect C..H and verify that it changes only the intended tracker
records and cannot affect behavior or proof inputs; otherwise rerun affected proof.
Read back final tracker state and run cleanup verification with H. Report both the
proved code commit and final delivery HEAD, with the reason proof remains applicable.
Do not rewrite records to refer to their own containing commit. A pending tracker
edit leaves delivery incomplete even if the code works.
