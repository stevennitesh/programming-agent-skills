# Terminate

Load only when Orient selects `Terminate` from destination-owner confirmation
and evidence for `cancelled`, `superseded`, or `out of scope`. Otherwise do not
load it.

Capture unresolved obligations and the recovery or successor boundary. Build
the terminal closing packet, then run the Mutation Gate with the map claim:
post, close, read back the closed state, release, prove claim absence, and
Orient. Do not run Closure, Domain Modeling, or To Spec. Closed maps remain
immutable.
