# Terminal Gap Routing

Load only when no Grilling frontier decision can advance and at least one
required branch remains blocked. Otherwise do not load it.

Return `Route gap` with kind `multi-decision route` when the bounded interview
cannot close in one conversation because several interdependent unresolved
decisions or non-conversational prerequisites need a tracker-backed
multi-session route. Preserve the intact bound, unresolved branches or
prerequisites, and impact. When active `$wayfinder` is the return owner, return
the intact gap to it for graph reconciliation without recommending another
Wayfinder. Otherwise recommend uninvoked `$wayfinder`, give the exact re-entry
instruction, and stop.

When no `Route gap` applies, return `Evidence gap` with kind `evidence` or
`decision authority`, missing input, impact, exactly one uninvoked owner, and
the exact instruction for returning its result to the original decision owner
without changing the gap identity. Choose `$research` for an authoritative
source, `$prototype` for runnable design evidence, `$to-questionnaire` for an
external stakeholder, and the caller or `none` otherwise. Mark causal or
reproduction uncertainty `diagnosis-required`.

When the intact gap must cross into a fresh context, preserve the evidence or
decision owner and add uninvoked `$handoff` only as transport. Handoff neither
answers nor owns the gap.
