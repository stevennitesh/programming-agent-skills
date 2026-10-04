# Setup defaults

Use for initial guidance or a requested setup migration that needs these seeds. Established
repository choices take precedence; an absent optional setting is not a gap.

For a new repository, one compact root `AGENTS.md` is a useful default. Split
guidance when substantial content or different reading conditions justify it.
`CONTEXT.md`, `docs/adr/`, and `docs/agents/` are available conventions, not a
required document tree.

Use [Domain routing](../templates/domain.md) when agents need a route to maintained
domain meaning and accepted decisions. Replace its generic route with verified
repository pointers and their reading conditions; omit a separate guide when an
existing owner already provides that route.

No generic engineering-contract seed is supplied. Keep brief local requirements
in `AGENTS.md` or their existing owner. A separate guide needs substantial
project-specific content, such as compatibility obligations or scientific
assumptions; general engineering advice alone does not justify one.

Keep brief local meaning inline and preserve established domain owners. Bootstrap
records how to find meaning; it does not invent domain content or create empty
context records. Missing records need resolution only when consequential meaning
cannot be obtained from the actual owner or user.

Tracker configuration and parallel prerequisites remain conditional branches of
the skill; initial setup does not make tickets or parallel execution mandatory.
