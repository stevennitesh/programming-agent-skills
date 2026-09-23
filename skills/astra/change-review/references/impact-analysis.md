# Impact analysis

Read when the user asks for blast radius or when candidate safety depends on a
downstream, lifecycle, library, storage, wire-format, or cross-system assumption
that the selected diff and direct callers cannot establish.

## Identify the load-bearing assumptions

Start from the changed behavior and name the small number of facts that must remain
true for the change to be safe. Do not produce a speculative inventory merely
because many things are reachable.

Trace beyond symbol search where meaning can cross representations or ownership:
pinned dependency behavior and local patches, generated configuration, persisted
or wire formats, cross-language consumers, feature flags, lifecycle or teardown
ordering, shared state, and other boundaries that can preserve or destroy the
assumption.

## Prove proportionally

Take each consequential assumption to the strongest evidence that is useful for
the decision:

1. applicable contract or exact source;
2. a traced argument that rules out the bad path;
3. a focused runnable check through the real mechanism; or
4. running-product evidence when only the deployed behavior can establish it.

Higher-cost proof is not automatically better. Stop when the evidence can decide
the relevant review obligation.

Report confirmed risks, assumptions that were checked and cleared, and any
load-bearing fact that remains unproved. Convert only supported candidate-caused
problems into findings under
[Finding standards](finding-standards.md); an unproved assumption may instead be a
coverage limit.
