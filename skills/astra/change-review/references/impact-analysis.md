# Impact analysis

Read when the user asks for blast radius or when consequential assumptions extend
beyond the selected diff and direct callers, or shared validation, persisted-input
acceptance, or supported compatibility changes.

The result identifies affected behavior and consumers, the assumptions on which
compatibility or safety depends, and evidence sufficient to judge them. Follow
representations and ownership boundaries as needed; a symbol search alone may
miss persisted formats, generated configuration, external consumers, or lifecycle
interactions. Keep the analysis tied to the candidate and supported workflows.

Choose evidence suited to the claim: contracts, exact source, a traced argument,
focused checks, or running-product evidence. There is no required sequence or
default full-system audit. Reuse valid evidence and stop when it settles the
material obligation; a substitute proves only the properties it preserves.

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
