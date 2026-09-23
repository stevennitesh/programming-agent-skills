# Feature map

Read only when a repository has enough user-facing breadth that agents would
otherwise keep rediscovering how features are reached and proved, or when the user
explicitly requests a maintained verification map.

The map is navigation for verification, not a second product specification and
not evidence that every listed feature was exercised.

## Record user-facing proof routes

Use the repository's existing documentation structure. Prefer one compact index
when it remains readable; split feature entries only when their drive or evidence
instructions need independent maintenance.

For each mapped feature, record only what a future verifier needs:

- the user-visible capability;
- how a user reaches it from a supported entry point;
- the harness command, route, selector, or interaction needed to drive it;
- the observable end state and material side effects that establish success; and
- prerequisites or isolation constraints that materially change the run.

Use stable user-facing handles rather than coordinates, incidental DOM structure,
private methods, or implementation-only names when the supported interface offers
a better anchor.

## Keep coverage claims honest

A feature map can contain unexercised entries. Mark an entry's recipe as known,
verified, blocked, or stale only from evidence that supports that state. One
representative harness proof does not certify every mapped feature.

When source changes make a mapped route, selector, command, prerequisite, or
expected result doubtful, reconcile the affected entry rather than silently
teaching future agents an obsolete path.

Product behavior that no longer satisfies an accepted feature is a product gap,
not documentation drift. Keep that defect separate from harness or map repair.
