# Terminal Gap Routing

Return `Route gap` with kind `multi-decision route` when the bounded interview
cannot close in one conversation because several coupled unresolved questions
or prerequisites, including at least one non-conversational resolver, need a
tracker-backed multi-session route. Preserve the intact bound, unresolved branches or
prerequisites, and impact. When active `$wayfinder` is the return owner, return
the intact gap to it for graph reconciliation without recommending another
Wayfinder. Otherwise recommend uninvoked `$wayfinder` and stop.

When no `Route gap` applies, return `Evidence gap` with kind `evidence` or
`decision authority` and exactly one uninvoked owner. Choose `$research` when
claim-owning sources can answer, `$prototype` for runnable design evidence,
`$to-questionnaire` for an external stakeholder, and the caller or `none`
otherwise. Mark a hard failure that needs dedicated causal investigation as
missing causal evidence and return it to the caller for classification.

Every gap names the bounded decision, missing or unresolved input, impact,
owner, required result, and exact instruction for returning that result to the
original decision owner. Preserve the gap identity across the detour.

When the intact gap must cross into a fresh context, preserve the evidence or
decision owner and add uninvoked `$handoff` only as transport. Handoff neither
answers nor owns the gap.
