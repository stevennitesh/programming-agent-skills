# Tracker delivery

Read only when delivery includes authorized tracker claims or closeout. Use the
repository's configured tracker, status, category, readiness, claim, and closure
conventions. Missing or incompatible policy is a setup gap; do not invent tracker
semantics. Direct parallel implementation does not require a tracker.

## Own claims before dispatch

Refresh accepted items, decision-changing comments, dependencies, and active
ownership before making claims. A selected subset does not authorize closing its
parent or changing unrelated siblings.

For whole-parent delivery, claim and read back the parent for this coordinator
before dispatching children. For a subset, preserve the parent's current ownership
and coordinate with that owner.

Bind claims to this run and actor using the configured representation. Read-back
alone is not an atomic lock; where coordinators can race, use a supported exclusive
claim mechanism or establish one coordinator before dispatch. Stop on ambiguous
ownership.

Claim only agent-ready work whose required predecessor outcomes are actually
integrated. Human-only readiness remains a handoff. Confirm each claimed item has
one current actor before dispatch and leave blocked or permission-gated descendants
unclaimed.

After an item lands and its applicable proof passes, apply only the configured
completion transition, clear only this run's active claim, and read the resulting
state back. Refetch dependents before changing their readiness. A closed
predecessor does not by itself prove that its required outcome is integrated.

If accepted meaning or acceptance changes while tracker items, assignments, or
proof depend on the current revision, use
[Active delivery revisions](../../shape-work/references/active-delivery-revisions.md)
before changing affected contracts. Then update only the affected tracker
representation and preserve unaffected work and evidence.

Mark a requested complete parent implemented only after refetching its complete
child graph, confirming every required child is complete, and satisfying the main
skill's integrated proof for the exact candidate.

A partial, failed, or indeterminate tracker mutation stops further dependent
mutation. Refetch the affected state before deciding whether to retry. Never
blindly replay writes or release an ambiguous claim.

On pause, leave incomplete items and their parent unimplemented. Retain a claim
only while this run will resume and its custody remains established; otherwise
release only this run's claims after writers stop and preserve a recoverable
handoff.

## Version-controlled local tracker

The root integration checkout is the canonical tracker. Worker copies are
read-only snapshots of tracker state; reserve tracker paths to the root and do not
merge worker tracker edits.

Before the first dispatch, commit the accepted graph and initial claims under
existing local commit authority. At each tracker transition, read back owned
changes and commit them before creating new lanes, landing code, or granting
exclusive integration-checkout custody. Claim siblings selected together in one
transition, then prepare them from that same clean HEAD.

Snapshot-only tracker differences between a sibling's base and current integration
HEAD do not invalidate code proof unless they change acceptance, dependencies,
permissions, or ownership.

After code proof at commit C, completion records cite C. Commit the root's
metadata-only completion changes to produce final delivery HEAD H. Inspect C..H
and establish that it changes only the intended tracker records and cannot affect
behavior or proof inputs; otherwise rerun affected proof.

Read back final tracker state and perform lane cleanup verification against H.
Report both proved code commit C and final delivery HEAD H with the reason the code
proof remains applicable. Do not rewrite records to cite their own containing
commit. Pending tracker edits leave delivery incomplete even when the code works.
