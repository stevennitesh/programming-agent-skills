# Impact analysis

Read for requested blast radius, changes to shared validation, persisted-input
acceptance, or supported compatibility. Use it when a consequential assumption
needs evidence beyond the direct callers.

The result identifies affected behavior and consumers, the assumptions on which
compatibility or safety depends, and evidence sufficient to judge them. Follow
representations and ownership boundaries as needed; a symbol search alone may
miss persisted formats, generated configuration, external consumers, or lifecycle
interactions. Keep the analysis tied to the candidate and supported workflows.

Choose evidence suited to the claim: contracts, exact source, a traced argument,
focused checks, or running-product evidence. There is no required sequence or
default full-system audit. Reuse valid evidence and stop when it settles the
material obligation; a substitute proves only the properties it preserves.

Where correctness depends on a type or data contract, trace what the producer
actually emits, what is validated at the boundary, and what the consumer assumes.
Check static type errors and runtime semantics as relevant. For example, both
ends can agree on `int | None` while the consumer incorrectly turns an unknown
value into zero.

For a material test claim, name a plausible failure and check whether the test is
collected, exercises the relevant mechanism, and asserts its observable result.
A test that only checks the number of attempts can pass while a retry writes a
duplicate record. Existing focused coverage is sufficient if it would catch the
failure. When further proof is needed, choose the smallest faithful check.

For shared validation, check affected callers and distinguish integrity rules
from operation-specific eligibility. For persisted-input changes, establish which
previously supported inputs remain accepted and which require migration. If test
fixtures were updated to satisfy a stricter contract, determine whether they
represented supported existing data. Require a distinguishing compatibility
regression case using the previous input wherever that workflow remains supported;
passing only migrated fixtures does not establish compatibility.

Report confirmed risks, consequential assumptions checked and cleared, and facts
that remain unresolved. Admit candidate-caused problems under
[Finding standards](finding-standards.md); an unproved assumption may instead be a
coverage limit.
