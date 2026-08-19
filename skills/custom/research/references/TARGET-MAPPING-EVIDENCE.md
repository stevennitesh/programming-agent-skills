# Target-Mapping Evidence

Load this branch when the answer depends on how an external requirement,
definition, or method maps to a named artifact or repository behavior.
Otherwise do not load it.

Inspect each target at an exact artifact identity or, for a repository, an
exact revision or captured state, even when the request does not explicitly
ask for a comparison. Map every material external requirement, definition, or
method through the complete local chain needed for the claim: inputs, source or
formulas, configuration and precedence, transformations, outputs, tests, and
observed behavior, including generators, overrides, policies, decisions, or
rendered artifacts when applicable. Record inspected identities and missing
links; reread mutable load-bearing surfaces before Return. On drift or an
incomplete chain, preserve unaffected results and keep the mapping `unresolved`
rather than synthesizing a hybrid state.

Before synthesizing a target mapping, classify each applicable layer
independently:

- static correspondence as `aligned`, `materially different`, or `unresolved`;
- runtime behavior as `supported`, `conflicted`, or `unknown`; and
- empirical effectiveness as `supported`, `conflicted`, or `unknown`.

If sufficient applicable evidence for a layer is unavailable, use `unresolved`
for static correspondence or `unknown` for runtime behavior or empirical
effectiveness; do not substitute evidence from another layer. Static
correspondence supports neither runtime behavior nor empirical effectiveness by
itself. An evidenced `aligned` or `materially different` static classification
resolves the mapping; mapping resolution does not determine the packet's
terminal status.

Report the sourced concept, observed local expression, material discrepancy,
mechanically entailed consequences, source-supported alignment constraints,
and only explicitly described applicable alternatives whose authority, state,
prerequisites, and constraints are evidenced. Do not compose, rank, or
recommend alternatives without defined comparative criteria. If exact mapping
is unavailable, name the exact evidence or validation needed. Do not infer
unobserved effects, invent, choose, or design a repair, perform caller-owned
validation, or own implementation.
