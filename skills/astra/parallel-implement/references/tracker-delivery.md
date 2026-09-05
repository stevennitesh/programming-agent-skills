# Tracker delivery

Read only when delivery includes authorized tracker claims or closeout. Use the
repository's configured tracker, status, category, and readiness conventions.
Missing or incompatible policy leaves a concrete setup gap; suggest repo-bootstrap
for that gap rather than inventing labels. Direct implementation needs no tracker.

Refresh the accepted items, decision-changing comments, dependencies, and active
ownership before claims. If delivering a complete parent, enumerate its complete
child graph and reconcile drift against the fixed scope. A selected subset does
not authorize closing its parent or changing siblings outside that subset.

Claim only ready items whose required predecessor outcomes are actually integrated.
Require an item to be unclaimed or demonstrably held by this run through its known
actor, lane, and commit. Stop on another or ambiguous owner. Read each claim back
and confirm one current actor before dispatch. Refetch newly ready items before
claiming them; leave blocked or permission-gated descendants unclaimed.

After an item lands and its applicable proof passes, preserve its category and
apply the configured implemented/closure transitions, then read them back.
Refetch affected dependents; mark ready only complete accepted work whose actual
blockers and permissions are resolved. Stay within authorized graph mutations.
Do not equate a closed predecessor with an integrated required outcome.

Close a requested complete parent only after refetching the full graph, confirming
all children completed, and satisfying the main skill's integrated proof for the
exact candidate. Read the parent state back. A partial, failed, or indeterminate
effect stops further tracker mutation: refetch affected state before deciding a
retry, preserve implementation progress, and report the observed state and safest
configured recovery. Do not replay writes or release ambiguous claims blindly.
