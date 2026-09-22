# Setup defaults

Use these defaults only for initial repository setup or a focused request that
needs them. Preserve established repository choices. An absent optional setting
is not a setup gap.

## Start with the smallest useful surface

For a new repository, prefer one compact root `AGENTS.md` containing:

- commands grounded in current scripts or configuration;
- non-obvious repository constraints; and
- conditional pointers to maintained guidance that future work actually needs.

Preserve useful existing instruction files and their scopes. Split guidance only
when substantial content or different reading conditions justify another owner.
Do not create documents, routes, or pointers merely to complete a template set.

Use these seeds only when their content is applicable:

- [Engineering contract](../templates/engineering-contract.md)
- [Domain routing](../templates/domain.md)

Adapt them to repository meaning rather than copying them wholesale. The resulting
documents are repository-owned, not managed mirrors.

## Domain and context routes

Preserve existing owners for domain meaning and accepted decisions. Keep brief
local meaning inline; introduce a separate route only when real maintained
content needs one. Root `CONTEXT.md`, `docs/adr/`, and `docs/agents/` are
available conventions, not required outputs.

Do not create empty context records or routes to nonexistent material. Missing
records are not automatically blockers; future work can resolve consequential
meaning from the actual owner or user.

## Optional setup branches

Tracker configuration is separate from ordinary bootstrap. When requested or
already established by repository practice, use [Tracker setup](tracker-setup.md).

For requested parallel-execution support or a concrete execution prerequisite
gap, use [Parallel support](parallel-support.md).

Do not install dependencies, provision external resources, create tracker items,
or broaden permissions unless the user's authorization separately covers those
effects.
