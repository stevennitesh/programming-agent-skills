# Target-Mapping Evidence

Load this branch when the answer depends on how a requirement, definition,
method, or named behavior maps through an artifact or repository. Otherwise do
not load it.

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

Classify only the layers the claim needs. Static correspondence is `aligned`,
`materially different`, or `unresolved`; runtime behavior and empirical
effectiveness use the common claim statuses. Evidence from one layer cannot
settle another. An aligned static mapping proves neither runtime behavior nor
effectiveness.

Report the sourced concept, observed local expression, material discrepancy,
and only consequences entailed by inspected evidence. If exact mapping is
unavailable, name the evidence needed. Do not infer unobserved effects, design a
repair, perform caller-owned validation, or own implementation.

For engineering motivation, code establishes mechanics, not intent. Require a
contemporaneous decision, commit, review, issue, or comment for a causal claim;
otherwise label the inference. Treat an explanation embedded in the request as
a hypothesis to test.
